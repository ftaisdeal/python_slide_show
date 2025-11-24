#!/usr/bin/env python3
"""
SlideShow Application
A unified interface for selecting directories and slideshow settings
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sys
import os
import platform
import locale
from pathlib import Path
from PIL import Image, ImageTk, ExifTags
class SlideshowApp:
    def update_thumbnails(self):
        # Clear previous thumbnails
        for widget in self.thumbnail_frame.winfo_children():
            widget.destroy()
        self.thumbnails = []
        directory = self.directory_var.get().strip()
        if not directory or not os.path.exists(directory):
            return
        image_files = get_image_files(directory)
        for idx, img_path in enumerate(image_files):
            try:
                img = Image.open(img_path)
                img.thumbnail((96, 96))
                thumb = ImageTk.PhotoImage(img)
                if idx == self.selected_thumbnail_idx:
                    # Create a white frame as border
                    border_frame = tk.Frame(self.thumbnail_frame, bg="white", bd=0)
                    border_frame.grid(row=idx, column=0, pady=2, padx=2, sticky="e")
                    lbl = tk.Label(border_frame, image=thumb, relief="flat", bd=0, bg="#444")
                    lbl.pack(padx=2, pady=2)  # This creates the white border effect
                    lbl.bind("<Button-1>", lambda e, i=idx: self.on_thumbnail_click(i))
                    self.thumbnails.append(lbl)
                else:
                    lbl = tk.Label(self.thumbnail_frame, image=thumb, relief="flat", bd=0, bg="#222")
                    lbl.grid(row=idx, column=0, pady=2, padx=2, sticky="e")
                    lbl.bind("<Button-1>", lambda e, i=idx: self.on_thumbnail_click(i))
                    self.thumbnails.append(lbl)
                lbl.image = thumb
            except Exception as e:
                print(f"Error loading thumbnail for {img_path}: {e}")
        
        # Update total time display when images change
        self.update_total_time_display()

    def on_thumbnail_click(self, idx):
        self.selected_thumbnail_idx = idx
        # First, clear all existing thumbnails and recreate them with proper styling
        self.update_thumbnails()
        self.thumbnail_frame.update_idletasks()
    def on_directory_entry_change(self, event=None):
        """Handle manual directory entry - validate, save, and update thumbnails"""
        directory = self.directory_var.get().strip()
        if directory and os.path.exists(directory) and os.path.isdir(directory):
            # Valid directory - save it and update thumbnails
            self.save_last_directory(directory)
            self.update_thumbnails()
        elif directory:
            # Invalid directory - create a temporary style with red background
            style = ttk.Style()
            style.configure('Error.TEntry', fieldbackground='#ffe6e6')
            self.dir_entry.configure(style='Error.TEntry')
            # Revert to normal style after 1 second
            self.root.after(1000, lambda: self.dir_entry.configure(style='TEntry'))
        else:
            # Empty directory - just update thumbnails (will clear them)
            self.update_thumbnails()

    def browse_directory(self):
        desktop_path = os.path.expanduser("~/Desktop")
        directory = filedialog.askdirectory(
            title="Select Photo Directory",
            initialdir=desktop_path
        )
        if directory:
            self.directory_var.set(directory)
            self.save_last_directory(directory)
            self.update_thumbnails()
    def save_last_directory(self, directory):
        """Save the last selected directory to config file"""
        try:
            with open(self.config_path, "w") as f:
                f.write(directory)
        except Exception as e:
            print(f"Could not save last directory: {e}")
    def load_last_directory(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    last_dir = f.read().strip()
                    if last_dir:
                        self.directory_var.set(last_dir)
            except Exception as e:
                print(f"Could not load last directory: {e}")
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SlideShow")
        self.root.geometry("680x500")
        self.root.resizable(False, False)
        self.center_window()
        # Store config in ~/Library/Application Support/SlideShow/
        config_dir = os.path.expanduser("~/Library/Application Support/SlideShow")
        os.makedirs(config_dir, exist_ok=True)
        self.config_path = os.path.join(config_dir, "slideshow_config.txt")
        self.directory_var = tk.StringVar()
        self.display_time_var = tk.StringVar(value="10")
        self.dissolve_time_var = tk.StringVar(value="1")
        self.loop_var = tk.BooleanVar(value=True)  # Loop by default
        self.selected_thumbnail_idx = None
        self.load_last_directory()
        self.setup_ui()
        initial_dir = self.directory_var.get().strip()
        if initial_dir:
            self.update_thumbnails()

    def center_window(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2) -200
        self.root.geometry(f'{w}x{h}+{x}+{y}')

    def validate_numeric_input(self, var_name):
        def validate():
            try:
                value = getattr(self, var_name).get()
                if value == "":
                    return
                float(value)
            except ValueError:
                getattr(self, var_name).set("")
        return validate

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="0")
        main_frame.grid(row=0, column=0, sticky="nw")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        thumb_panel = tk.Frame(main_frame)
        thumb_panel.grid(row=0, column=0, rowspan=4, sticky="nsw", padx=(0, 20))
        self.thumbnail_canvas = tk.Canvas(thumb_panel, width=106, height=500, bg="#000", highlightthickness=0, bd=0)
        self.thumbnail_canvas.grid(row=0, column=0, sticky="nsw")
        self.thumbnail_scrollbar = tk.Scrollbar(thumb_panel, orient="vertical", command=self.thumbnail_canvas.yview)
        self.thumbnail_scrollbar.grid(row=0, column=1, sticky="nsw")
        self.thumbnail_canvas.configure(yscrollcommand=self.thumbnail_scrollbar.set)
        self.thumbnail_frame = tk.Frame(self.thumbnail_canvas, bg="#222")
        self.thumbnail_canvas.create_window((0, 0), window=self.thumbnail_frame, anchor="nw")
        self.thumbnail_frame.bind("<Configure>", lambda e: self.thumbnail_canvas.configure(scrollregion=self.thumbnail_canvas.bbox("all")))

        title_label = ttk.Label(main_frame, text="SlideShow", font=("Verdana", 24, "bold"))
        title_label.grid(row=0, column=1, pady=(0, 0))

        dir_frame = ttk.Frame(main_frame)
        dir_frame.grid(row=1, column=1, sticky="ew", pady=(0, 0))
        dir_frame.columnconfigure(0, weight=1)
        dir_frame.columnconfigure(1, weight=1)
        dir_frame.columnconfigure(2, weight=1)
        dir_label = ttk.Label(dir_frame, text="Browse to the directory containing your images", font=("Verdana", 14))
        dir_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=(0, 0), pady=(0, 0))
        self.dir_entry = ttk.Entry(dir_frame, textvariable=self.directory_var, font=("Verdana", 14), width=40)
        self.dir_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(2, 0))
        self.dir_entry.bind("<Return>", self.on_directory_entry_change)
        self.dir_entry.bind("<FocusOut>", self.on_directory_entry_change)
        browse_btn = ttk.Button(dir_frame, text="Browse...", command=self.browse_directory)
        browse_btn.grid(row=1, column=2, sticky="w")
        
        # Total time display
        self.total_time_label = ttk.Label(dir_frame, text="", font=("Verdana", 11), foreground="#666")
        self.total_time_label.grid(row=2, column=0, columnspan=3, sticky="w", padx=(2, 0), pady=(5, 0))
        
        # Loop checkbox
        self.loop_checkbox = ttk.Checkbutton(dir_frame, text="Loop slideshow", variable=self.loop_var)
        self.loop_checkbox.grid(row=3, column=0, columnspan=3, sticky="w", padx=(2, 0), pady=(5, 0))
        
        self.update_total_time_display()

        settings_frame = ttk.Frame(main_frame, padding="20")
        settings_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 0))
        inner_settings = ttk.Frame(settings_frame)
        inner_settings.pack(anchor="center")
        ttk.Label(inner_settings, text="Slide duration", font=("Verdana", 14)).grid(row=0, column=0, sticky=tk.E, pady=(0, 2), padx=(0, 5))
        self.duration_entry = ttk.Entry(inner_settings, textvariable=self.display_time_var, font=("Verdana", 14), width=5)
        self.duration_entry.grid(row=0, column=1, sticky="ew", padx=(0, 5))
        self.duration_entry.bind("<FocusOut>", self.validate_numeric_input("display_time_var"))
        self.duration_entry.bind("<KeyRelease>", lambda e: self.root.after_idle(self.update_total_time_display))
        ttk.Label(inner_settings, text="Dissolve duration", font=("Verdana", 14)).grid(row=1, column=0, sticky=tk.E, pady=(0, 2), padx=(0, 5))
        self.dissolve_entry = ttk.Entry(inner_settings, textvariable=self.dissolve_time_var, font=("Verdana", 14), width=5)
        self.dissolve_entry.grid(row=1, column=1, sticky="ew", padx=(0, 5))
        self.dissolve_entry.bind("<FocusOut>", self.validate_numeric_input("dissolve_time_var"))
        self.dissolve_entry.bind("<KeyRelease>", lambda e: self.root.after_idle(self.update_total_time_display))

        # START button and its event handlers
        button_frame = tk.Frame(settings_frame, bg="#88aa88", relief="flat", bd=0)
        button_frame.pack(pady=(10, 0))
        start_btn = tk.Label(button_frame, text="START", font=("Verdana", 14), bg="#88aa88", fg="black", padx=10, pady=8, cursor="hand2", relief="flat", bd=0)
        start_btn.pack(pady=(0, 0))
        def on_click(event):
            start_btn.configure(bg="#889988")
            self.root.after(100, lambda: start_btn.configure(bg="#88aa88"))
            self.start_slideshow()
        def on_enter(event):
            start_btn.configure(bg="#88bb88")
        def on_leave(event):
            start_btn.configure(bg="#88aa88")
        start_btn.bind("<Button-1>", on_click)
        start_btn.bind("<Enter>", on_enter)
        start_btn.bind("<Leave>", on_leave)

    def update_total_time_display(self):
        """Calculate and display the total slideshow time"""
        directory = self.directory_var.get().strip()
        if not directory or not os.path.exists(directory):
            self.total_time_label.config(text="")
            return
        
        image_files = get_image_files(directory)
        num_images = len(image_files)
        
        if num_images == 0:
            self.total_time_label.config(text="No images found")
            return
        
        try:
            display_time = float(self.display_time_var.get()) if self.display_time_var.get() else 10.0
        except ValueError:
            display_time = 10.0
            
        try:
            dissolve_time = float(self.dissolve_time_var.get()) if self.dissolve_time_var.get() else 1.0
        except ValueError:
            dissolve_time = 1.0
        
        # Calculate total time for one complete cycle
        total_display_time = num_images * display_time
        total_transition_time = num_images * dissolve_time
        total_time = total_display_time + total_transition_time
        
        # Format the time display (round to nearest second)
        total_time = round(total_time)
        
        if total_time < 60:
            time_str = f"{total_time} seconds"
        elif total_time < 3600:
            minutes = int(total_time // 60)
            seconds = int(total_time % 60)
            if seconds == 0:
                time_str = f"{minutes}m"
            else:
                time_str = f"{minutes}m {seconds}s"
        else:
            hours = int(total_time // 3600)
            minutes = int((total_time % 3600) // 60)
            seconds = int(total_time % 60)
            if minutes == 0 and seconds == 0:
                time_str = f"{hours}h"
            elif seconds == 0:
                time_str = f"{hours}h {minutes}m"
            else:
                time_str = f"{hours}h {minutes}m {seconds}s"
        
        self.total_time_label.config(text=f"Total slideshow time: {time_str} ({num_images} images)")

    def start_slideshow(self):
        directory = self.directory_var.get().strip()
        if not directory or not os.path.exists(directory):
            messagebox.showerror("Error", "Please select a valid image directory.")
            return
        image_files = get_image_files(directory)
        if not image_files:
            messagebox.showerror("Error", "No images found in the selected directory.")
            return
        try:
            display_time = float(self.display_time_var.get())
        except ValueError:
            display_time = 5
        try:
            dissolve_time = float(self.dissolve_time_var.get())
        except ValueError:
            dissolve_time = 1
        # Hide launcher window
        self.root.withdraw()
        # Determine starting index
        start_idx = self.selected_thumbnail_idx if self.selected_thumbnail_idx is not None else 0
        # Launch slideshow
        FullscreenImageViewer(
            image_files,
            display_time_ms=int(display_time * 1000),
            dissolve_time_ms=int(dissolve_time * 1000),
            launcher_app=self,
            directory=directory,
            display_time=display_time,
            dissolve_time=dissolve_time,
            display_time_str=self.display_time_var.get(),
            dissolve_time_str=self.dissolve_time_var.get(),
            start_idx=start_idx,
            loop_enabled=self.loop_var.get()
        )

        
    
    def format_number_for_display(self, value):
        """Format a number for display, preserving integers as integers"""
        if value == int(value):
            return str(int(value))
        else:
            return str(value)
    
    def adjust_field_width(self, entry_widget, text_value):
        """Adjust the width of an input field based on content length"""
        # Calculate width: minimum of 2, maximum of 8, based on content length + 1 for padding
        width = max(2, min(8, len(text_value) + 1))
        entry_widget.config(width=width)
    
    def return_from_slideshow(self, directory, display_time, dissolve_time, 
                            display_time_str="", dissolve_time_str=""):
        """Called when returning from slideshow - restore settings and show launcher"""
        # Restore the settings with proper formatting (preserve integers)
        self.directory_var.set(directory)
        
        # Use original string values if available, otherwise format the numeric values
        if display_time_str:
            final_display_str = display_time_str
        else:
            final_display_str = self.format_number_for_display(display_time)
        
        if dissolve_time_str:
            final_dissolve_str = dissolve_time_str
        else:
            final_dissolve_str = self.format_number_for_display(dissolve_time)
        
        self.display_time_var.set(final_display_str)
        self.dissolve_time_var.set(final_dissolve_str)
        
        # Adjust field widths based on content
        self.adjust_field_width(self.duration_entry, final_display_str)
        self.adjust_field_width(self.dissolve_entry, final_dissolve_str)
        
        # Show the launcher window again
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
    
    def run(self):
        self.root.mainloop()

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

def apply_exif_orientation(image):
    """Apply EXIF orientation to image if present"""
    try:
        # Get EXIF data
        exif = image._getexif()
        if exif is not None:
            # Find orientation tag
            for tag, value in exif.items():
                if ExifTags.TAGS.get(tag) == 'Orientation':
                    # Apply rotation based on orientation value
                    if value == 2:
                        image = image.transpose(Image.FLIP_LEFT_RIGHT)
                    elif value == 3:
                        image = image.rotate(180, expand=True)
                    elif value == 4:
                        image = image.transpose(Image.FLIP_TOP_BOTTOM)
                    elif value == 5:
                        image = image.transpose(Image.FLIP_LEFT_RIGHT).rotate(90, expand=True)
                    elif value == 6:
                        image = image.rotate(270, expand=True)
                    elif value == 7:
                        image = image.transpose(Image.FLIP_LEFT_RIGHT).rotate(270, expand=True)
                    elif value == 8:
                        image = image.rotate(90, expand=True)
                    break
    except (AttributeError, KeyError, TypeError):
        # If there's any issue reading EXIF data, just return the original image
        pass
    
    return image

class FullscreenImageViewer:
    def __init__(self, image_files, display_time_ms=5000, dissolve_time_ms=1000, dissolve_frames=30, 
                 launcher_app=None, directory=None, display_time=None, dissolve_time=None,
                 display_time_str="", dissolve_time_str="", start_idx=0, loop_enabled=True):
        self.image_files = image_files
        self.display_time_ms = display_time_ms
        self.dissolve_time_ms = dissolve_time_ms
        self.dissolve_frames = dissolve_frames
        self.img_idx = start_idx
        self.timer_id = None
        self.dissolve_id = None
        self.paused = False
        self.loop_enabled = loop_enabled
        
        # Store launcher app reference and settings for returning
        self.launcher_app = launcher_app
        self.directory = directory
        self.display_time = display_time
        self.dissolve_time = dissolve_time
        self.display_time_str = display_time_str
        self.dissolve_time_str = dissolve_time_str
        
        # Create and configure the root window - use Toplevel if launcher exists
        if launcher_app and launcher_app.root.winfo_exists():
            self.root = tk.Toplevel(launcher_app.root)
        else:
            self.root = tk.Tk()
        
        self.root.attributes('-fullscreen', True)
        self.root.config(cursor="none", bg='black')
        
        # Ensure the slideshow window is on top
        self.root.lift()
        self.root.attributes('-topmost', True)
        
        # Create the label for displaying images
        self.label = tk.Label(self.root, bg='black')
        self.label.pack(expand=True, fill=tk.BOTH)
        
        # Initialize image-related attributes
        self.photo = None
        self.current_photo = None  # Additional reference
        self.next_img_canvas = None
        self.dissolving = False
        
        # Force window update to ensure proper initialization
        self.root.update_idletasks()
        self.root.update()  # Additional update to ensure full initialization
        self.screen_size = (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        
        # Bind keyboard events
        self.root.bind("<Right>", self.next_image)
        self.root.bind("<Left>", self.prev_image)
        self.root.bind("<space>", self.toggle_pause)
        self.root.bind("<Escape>", self.return_to_launcher)
        
        # Show first image and start slideshow
        self.root.focus_force()  # Ensure window has focus
        
        # Initialize the slideshow
        self.show_image(self.img_idx, dissolve=False)
        self.root.mainloop()

    def prepare_canvas(self, img_path):
        """Resize image with aspect ratio, center it on black canvas"""
        try:
            print(f"Loading image: {img_path}")
            img = Image.open(img_path).convert('RGBA')
            print(f"Image loaded successfully: {img.size}, mode: {img.mode}")
            # Apply EXIF orientation before processing
            img = apply_exif_orientation(img)
            screen_width, screen_height = self.screen_size
            img_ratio = img.width / img.height
            screen_ratio = screen_width / screen_height

            if img_ratio > screen_ratio:
                new_width = screen_width
                new_height = int(screen_width / img_ratio)
            else:
                new_height = screen_height
                new_width = int(screen_height * img_ratio)

            print(f"Resizing to: {new_width}x{new_height}")
            img = img.resize((new_width, new_height), Image.LANCZOS)
            # Create RGBA canvas (black background)
            canvas = Image.new('RGBA', (screen_width, screen_height), (0, 0, 0, 255))
            offset_x = (screen_width - new_width) // 2
            offset_y = (screen_height - new_height) // 2
            canvas.paste(img, (offset_x, offset_y), mask=img)
            print(f"Canvas prepared successfully: {canvas.size}, mode: {canvas.mode}")
            return canvas
        except Exception as e:
            print(f"Error loading image {img_path}: {e}")
            import traceback
            traceback.print_exc()
            # Return a black canvas if image loading fails
            screen_width, screen_height = self.screen_size
            print(f"Creating fallback black canvas: {screen_width}x{screen_height}")
            return Image.new('RGB', (screen_width, screen_height), (0, 0, 0))

    def show_image(self, idx, dissolve=True):
        print(f"Showing image {idx + 1}/{len(self.image_files)}: {self.image_files[idx]}")
        
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        if self.dissolve_id:
            self.root.after_cancel(self.dissolve_id)
            self.dissolve_id = None
            
        img_path = self.image_files[idx]
        self.root.title(f"{img_path.name} ({idx+1}/{len(self.image_files)})")
        
        try:
            new_canvas = self.prepare_canvas(img_path)
            if new_canvas is None:
                print(f"Failed to prepare canvas for {img_path}")
                return
                
            if dissolve and hasattr(self, "current_canvas") and self.current_canvas is not None:
                self.dissolving = True
                self.dissolve_step = 0
                self.next_img_canvas = new_canvas
                self._dissolve_images()
            else:
                print(f"Displaying image directly: {img_path.name}")
                self.display_img(new_canvas)
                self.current_canvas = new_canvas
                if not self.paused:
                    self.timer_id = self.root.after(self.display_time_ms, self.next_image)
        except Exception as e:
            print(f"Error in show_image: {e}")
            # Try to continue with next image
            if not self.paused:
                self.timer_id = self.root.after(1000, self.next_image)

    def safe_create_photoimage(self, pil_image):
        """Safely create a PhotoImage from PIL Image"""
        try:
            # Convert to RGB mode for better compatibility
            if pil_image.mode == 'RGBA':
                # Create a white background and paste the RGBA image
                rgb_img = Image.new('RGB', pil_image.size, (0, 0, 0))
                rgb_img.paste(pil_image, mask=pil_image.split()[-1] if len(pil_image.split()) == 4 else None)
                pil_image = rgb_img
            elif pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # Create PhotoImage using ImageTk
            photo = ImageTk.PhotoImage(pil_image)
            return photo
        except Exception as e:
            print(f"Failed to create PhotoImage: {e}")
            # Create a simple black fallback image
            try:
                black_img = Image.new('RGB', self.screen_size, (0, 0, 0))
                return ImageTk.PhotoImage(black_img)
            except Exception as fallback_error:
                print(f"Failed to create fallback image: {fallback_error}")
                return None

    def _dissolve_images(self):
        frames = self.dissolve_frames
        step = self.dissolve_step
        alpha = step / frames
        
        try:
            blended = Image.blend(self.current_canvas, self.next_img_canvas, alpha)
            
            # Create PhotoImage safely
            photo = self.safe_create_photoimage(blended)
            if photo is None:
                print("Failed to create photo during dissolve, skipping frame")
                self.dissolve_step += 1
                if self.dissolve_step < frames:
                    self.dissolve_id = self.root.after(self.dissolve_time_ms // frames, self._dissolve_images)
                else:
                    self.display_img(self.next_img_canvas)
                    self.current_canvas = self.next_img_canvas
                    self.dissolving = False
                    if not self.paused:
                        self.timer_id = self.root.after(self.display_time_ms, self.next_image)
                return
            
            # Store multiple references
            self.photo = photo
            self.current_photo = photo
            self.label.image = photo
            self.label.config(image=photo)
            
            # Force update to ensure the image is displayed
            self.label.update_idletasks()
            
            if step < frames:
                self.dissolve_step += 1
                self.dissolve_id = self.root.after(self.dissolve_time_ms // frames, self._dissolve_images)
            else:
                self.display_img(self.next_img_canvas)
                self.current_canvas = self.next_img_canvas
                self.dissolving = False
                if not self.paused:
                    self.timer_id = self.root.after(self.display_time_ms, self.next_image)
        except Exception as e:
            print(f"Error in dissolve animation: {e}")
            # Skip to final image if dissolve fails
            self.display_img(self.next_img_canvas)
            self.current_canvas = self.next_img_canvas
            self.dissolving = False
            if not self.paused:
                self.timer_id = self.root.after(self.display_time_ms, self.next_image)

    def display_img(self, img):
        print(f"display_img called with image size: {img.size if img else 'None'}")
        try:
            # Ensure we have a valid PIL Image
            if img is None:
                print("Warning: Attempting to display None image")
                return
            
            # Create PhotoImage safely
            print("Creating PhotoImage...")
            photo = self.safe_create_photoimage(img)
            if photo is None:
                print("Failed to create PhotoImage")
                return
            
            print("PhotoImage created successfully")
            
            # Clear any existing image first
            self.label.configure(image='')
            
            # Store the reference in multiple places to prevent garbage collection
            self.photo = photo
            self.current_photo = photo
            self.label.image = photo  # This is critical for keeping the reference
            
            # Update the label display
            print("Updating label...")
            self.label.configure(image=photo)
            
            # Force update
            print("Forcing display update...")
            self.label.update()
            self.root.update()
            print("Image display completed")
            
        except Exception as e:
            print(f"Error displaying image: {e}")
            import traceback
            traceback.print_exc()
            # Try to display a simple black screen
            try:
                print("Attempting fallback display...")
                self.label.configure(image='', bg='black')
                self.label.image = None
                self.photo = None
                self.current_photo = None
                self.root.update()
                print("Fallback black screen displayed")
            except Exception as fallback_error:
                print(f"Error with fallback display: {fallback_error}")

    def next_image(self, event=None):
        if self.dissolving:
            return
        
        # Check if we should loop or stop at the end
        if self.img_idx >= len(self.image_files) - 1:
            if self.loop_enabled:
                self.img_idx = 0  # Loop back to first image
            else:
                # End of slideshow - return to launcher
                self.return_to_launcher()
                return
        else:
            self.img_idx += 1
            
        self.show_image(self.img_idx, dissolve=True)

    def prev_image(self, event=None):
        if self.dissolving:
            return
            
        # Check if we should loop or stop at the beginning
        if self.img_idx <= 0:
            if self.loop_enabled:
                self.img_idx = len(self.image_files) - 1  # Loop to last image
            else:
                # Beginning of slideshow - stay at first image
                return
        else:
            self.img_idx -= 1
            
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
            # Resume and immediately show the next image
            self.next_image()

    def return_to_launcher(self, event=None):
        """Return to launcher with current settings"""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        if self.dissolve_id:
            self.root.after_cancel(self.dissolve_id)
        
        # Destroy the slideshow window
        self.root.destroy()
        
        # If we have a launcher app reference, return to it with current settings
        if self.launcher_app:
            self.launcher_app.return_from_slideshow(
                self.directory, 
                self.display_time, 
                self.dissolve_time,
                self.display_time_str,
                self.dissolve_time_str
            )

    def quit_app(self, event=None):
        """Completely quit the application"""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        if self.dissolve_id:
            self.root.after_cancel(self.dissolve_id)
        
        # Destroy the slideshow window
        self.root.destroy()
        
        # If we have a launcher app, also quit that
        if self.launcher_app:
            try:
                self.launcher_app.root.quit()
                self.launcher_app.root.destroy()
            except:
                pass

if __name__ == "__main__":
    app = SlideshowApp()
    app.run()
