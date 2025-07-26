import os
import sys
from pathlib import Path
from PIL import Image, ImageTk
import tkinter as tk
import locale

def get_image_files(directory):
    exts = ('.jpg', '.jpeg', '.png', '.webp')
    files = [f for f in Path(directory).iterdir() if f.suffix.lower() in exts and f.is_file()]
    # Sort using macOS Finder's natural sorting (locale-aware)
    files.sort(key=lambda x: locale.strxfrm(x.name.lower()))
    return files

class FullscreenImageViewer:
    def __init__(self, image_files, display_time_ms=5000, dissolve_time_ms=1000, dissolve_frames=30):
        self.image_files = image_files
        self.display_time_ms = display_time_ms
        self.dissolve_time_ms = dissolve_time_ms
        self.dissolve_frames = dissolve_frames
        self.img_idx = 0
        self.timer_id = None
        self.dissolve_id = None
        self.paused = False
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.config(cursor="none")
        self.label = tk.Label(self.root, bg='black')
        self.label.pack(expand=True, fill=tk.BOTH)
        self.photo = None
        self.next_img_canvas = None
        self.dissolving = False
        self.screen_size = (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        self.root.bind("<Right>", self.next_image)
        self.root.bind("<Left>", self.prev_image)
        self.root.bind("<space>", self.toggle_pause)
        self.root.bind("<Escape>", self.quit_app)
        self.root.bind("q", self.quit_app)
        self.show_image(self.img_idx, dissolve=False)
        self.root.mainloop()

    def prepare_canvas(self, img_path):
        """Resize image with aspect ratio, center it on transparent canvas"""
        img = Image.open(img_path).convert('RGBA')
        screen_width, screen_height = self.screen_size
        img_ratio = img.width / img.height
        screen_ratio = screen_width / screen_height

        if img_ratio > screen_ratio:
            new_width = screen_width
            new_height = int(screen_width / img_ratio)
        else:
            new_height = screen_height
            new_width = int(screen_height * img_ratio)

        img = img.resize((new_width, new_height), Image.LANCZOS)
        canvas = Image.new('RGBA', (screen_width, screen_height), (0, 0, 0, 255))
        offset_x = (screen_width - new_width) // 2
        offset_y = (screen_height - new_height) // 2
        canvas.paste(img, (offset_x, offset_y))
        return canvas

    def show_image(self, idx, dissolve=True):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        if self.dissolve_id:
            self.root.after_cancel(self.dissolve_id)
            self.dissolve_id = None
        img_path = self.image_files[idx]
        self.root.title(f"{img_path.name} ({idx+1}/{len(self.image_files)})")
        new_canvas = self.prepare_canvas(img_path)
        if dissolve and hasattr(self, "current_canvas"):
            self.dissolving = True
            self.dissolve_step = 0
            self.next_img_canvas = new_canvas
            self._dissolve_images()
        else:
            self.display_img(new_canvas)
            self.current_canvas = new_canvas
            if not self.paused:
                self.timer_id = self.root.after(self.display_time_ms, self.next_image)

    def _dissolve_images(self):
        frames = self.dissolve_frames
        step = self.dissolve_step
        alpha = step / frames
        blended = Image.blend(self.current_canvas, self.next_img_canvas, alpha)
        photo = ImageTk.PhotoImage(blended)
        self.label.config(image=photo)
        self.label.image = photo
        self.photo = photo
        if step < frames:
            self.dissolve_step += 1
            self.dissolve_id = self.root.after(self.dissolve_time_ms // frames, self._dissolve_images)
        else:
            self.display_img(self.next_img_canvas)
            self.current_canvas = self.next_img_canvas
            self.dissolving = False
            if not self.paused:
                self.timer_id = self.root.after(self.display_time_ms, self.next_image)

    def display_img(self, img):
        photo = ImageTk.PhotoImage(img)
        self.label.config(image=photo)
        self.label.image = photo
        self.photo = photo

    def next_image(self, event=None):
        if self.dissolving:
            return
        self.img_idx = (self.img_idx + 1) % len(self.image_files)
        self.show_image(self.img_idx, dissolve=True)

    def prev_image(self, event=None):
        if self.dissolving:
            return
        self.img_idx = (self.img_idx - 1) % len(self.image_files)
        self.show_image(self.img_idx, dissolve=True)

    def toggle_pause(self, event=None):
        """Toggle pause/resume of the slideshow"""
        if self.dissolving:
            return
        
        self.paused = not self.paused
        
        if self.paused:
            # Cancel the timer if we're pausing
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None
        else:
            # Resume by setting a new timer
            self.timer_id = self.root.after(self.display_time_ms, self.next_image)

    def quit_app(self, event=None):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        if self.dissolve_id:
            self.root.after_cancel(self.dissolve_id)
        self.root.destroy()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python images_dissolve.py <directory>")
        sys.exit(1)
    directory = sys.argv[1]
    image_files = get_image_files(directory)
    if not image_files:
        print("No image files found.")
        sys.exit(1)
    FullscreenImageViewer(image_files)
