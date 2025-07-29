import os
import sys
import platform
from pathlib import Path
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import locale

def get_image_files(directory):
    exts = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tiff', '.tif')
    files = [f for f in Path(directory).iterdir() if f.suffix.lower() in exts and f.is_file()]
    
    # Sort according to the operating system's default file sorting
    system = platform.system()
    
    if system == "Darwin":  # macOS
        # Use locale-aware sorting like Finder
        files.sort(key=lambda x: locale.strxfrm(x.name.lower()))
    elif system == "Windows":
        # Windows Explorer uses case-insensitive natural sorting
        import re
        def natural_sort_key(path):
            def convert(text):
                return int(text) if text.isdigit() else text.lower()
            return [convert(c) for c in re.split(r'(\d+)', path.name)]
        files.sort(key=natural_sort_key)
    else:  # Linux and other Unix-like systems
        # Most Linux file managers use case-sensitive alphabetical by default
        # but we'll use case-insensitive for better user experience
        files.sort(key=lambda x: x.name.lower())
    
    return files

def get_directory_and_settings():
    """Show dialogs to get directory and timing settings"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Ask for directory
    desktop_path = os.path.expanduser("~/Desktop")
    directory = filedialog.askdirectory(
        title="Select folder containing images",
        initialdir=desktop_path
    )
    
    if not directory:
        root.destroy()
        return None, None, None
    
    # Ask for display time
    display_time = simpledialog.askfloat(
        "Display Time",
        "How many seconds should each image be displayed?",
        initialvalue=5.0,
        minvalue=0.1,
        maxvalue=3600.0
    )
    
    if display_time is None:
        display_time = 5.0
    
    # Ask for dissolve time
    dissolve_time = simpledialog.askfloat(
        "Dissolve Time", 
        "How many seconds for the dissolve transition?",
        initialvalue=1.0,
        minvalue=0.0,
        maxvalue=60.0
    )
    
    if dissolve_time is None:
        dissolve_time = 1.0
    
    root.destroy()
    return directory, display_time, dissolve_time

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
    # Check if command line arguments are provided
    if len(sys.argv) >= 2:
        # Use command line arguments (original behavior)
        directory = sys.argv[1]
        
        # Parse optional timing arguments
        display_time_seconds = 5.0  # default 5 seconds
        dissolve_time_seconds = 1.0  # default 1 second
        
        if len(sys.argv) >= 3:
            try:
                display_time_seconds = float(sys.argv[2])
                if display_time_seconds <= 0:
                    raise ValueError("Display time must be positive")
            except ValueError as e:
                print(f"Error: Invalid display time '{sys.argv[2]}'. Must be a positive number.")
                sys.exit(1)
        
        if len(sys.argv) >= 4:
            try:
                dissolve_time_seconds = float(sys.argv[3])
                if dissolve_time_seconds < 0:
                    raise ValueError("Dissolve time must be non-negative")
            except ValueError as e:
                print(f"Error: Invalid dissolve time '{sys.argv[3]}'. Must be a non-negative number.")
                sys.exit(1)
    else:
        # No command line arguments - show GUI dialogs
        try:
            directory, display_time_seconds, dissolve_time_seconds = get_directory_and_settings()
            if directory is None:
                print("No directory selected. Exiting.")
                sys.exit(0)
        except Exception as e:
            print(f"Error getting settings: {e}")
            sys.exit(1)
    
    # Convert to milliseconds for the viewer
    display_time_ms = int(display_time_seconds * 1000)
    dissolve_time_ms = int(dissolve_time_seconds * 1000)
    
    image_files = get_image_files(directory)
    if not image_files:
        if len(sys.argv) >= 2:
            print("No image files found.")
        else:
            messagebox.showerror("Error", "No image files found in the selected directory.")
        sys.exit(1)
    
    print(f"Starting slideshow with {len(image_files)} images")
    print(f"Display time: {display_time_seconds}s, Dissolve time: {dissolve_time_seconds}s")
    
    FullscreenImageViewer(image_files, display_time_ms, dissolve_time_ms)
