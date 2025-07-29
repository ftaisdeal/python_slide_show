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
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SlideShow")
        self.root.geometry("600x300")
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Variables
        self.directory_var = tk.StringVar()
        self.display_time_var = tk.StringVar(value="5")
        self.dissolve_time_var = tk.StringVar(value="1")
        
        self.setup_ui()
        
    def validate_numeric_input(self, var_name):
        """Validate that input is numeric, clear if not"""
        def validate():
            try:
                value = getattr(self, var_name).get()
                if value == "":  # Allow empty string
                    return
                float(value)  # Try to convert to number
            except ValueError:
                # If conversion fails, clear the field
                getattr(self, var_name).set("")
        return validate
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for centering
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="SlideShow", 
                               font=("Verdana", 24, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 30))
        
        # Directory chooser frame
        dir_frame = ttk.Frame(main_frame)
        dir_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Directory selection section - all on one row
        dir_label = ttk.Label(dir_frame, text="Image directory", 
                             font=("Verdana", 14))
        dir_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 0))
        
        self.dir_entry = ttk.Entry(dir_frame, textvariable=self.directory_var, 
                                  font=("Verdana", 14), width=32)
        self.dir_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 0))
        
        browse_btn = ttk.Button(dir_frame, text="Browse...", 
                               command=self.browse_directory)
        browse_btn.grid(row=0, column=2)
        
        # Settings section
        settings_frame = ttk.Frame(main_frame, padding="20")
        settings_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 0))
        
        # Create inner frame to center the controls
        inner_settings = ttk.Frame(settings_frame)
        inner_settings.pack(anchor="center")
        
        # Slide duration
        ttk.Label(inner_settings, text="Slide duration", 
                 font=("Verdana", 14)).grid(row=0, column=0, sticky=tk.E, pady=(0, 15), padx=(0, 5))
        
        duration_entry = ttk.Entry(inner_settings, textvariable=self.display_time_var, 
                                  font=("Verdana", 14), width=2)
        duration_entry.grid(row=0, column=1, sticky=tk.W, pady=(0, 15), padx=(0, 20))
        
        # Bind validation to slide duration field
        self.display_time_var.trace_add('write', lambda *args: self.validate_numeric_input('display_time_var')())
        
        # Dissolve duration
        ttk.Label(inner_settings, text="Dissolve duration", 
                 font=("Verdana", 14)).grid(row=0, column=2, sticky=tk.E, pady=(0, 15), padx=(0, 5))
        
        dissolve_entry = ttk.Entry(inner_settings, textvariable=self.dissolve_time_var, 
                                  font=("Verdana", 14), width=2)
        dissolve_entry.grid(row=0, column=3, sticky=tk.W, pady=(0, 15), padx=(0, 0))
        
        # Bind validation to dissolve duration field
        self.dissolve_time_var.trace_add('write', lambda *args: self.validate_numeric_input('dissolve_time_var')())
        
        # Start button - using Canvas for guaranteed green color
        button_frame = tk.Frame(main_frame, bg="#90EE90", relief="raised", bd=3)
        button_frame.grid(row=3, column=0, pady=(0, 20))
        
        start_btn = tk.Label(button_frame, text="START", 
                            font=("Verdana", 14),
                            bg="#88aa88",
                            fg="black",
                            padx=10,
                            pady=8,
                            cursor="hand2")
        start_btn.pack()
        
        # Bind click events to make it act like a button
        def on_click(event):
            start_btn.configure(bg="#889988")  # Darker green when clicked
            self.root.after(100, lambda: start_btn.configure(bg="#88aa88"))  # Return to normal
            self.start_slideshow()
        
        def on_enter(event):
            start_btn.configure(bg="#88bb88")  # Slightly lighter on hover
        
        def on_leave(event):
            start_btn.configure(bg="#88aa88")  # Back to normal
        
        start_btn.bind("<Button-1>", on_click)
        start_btn.bind("<Enter>", on_enter)
        start_btn.bind("<Leave>", on_leave)
        button_frame.bind("<Button-1>", on_click)
        button_frame.bind("<Enter>", on_enter)
        button_frame.bind("<Leave>", on_leave)
        
        # Configure ttk styles for other elements
        style = ttk.Style()
        
    def browse_directory(self):
        desktop_path = os.path.expanduser("~/Desktop")
        directory = filedialog.askdirectory(
            title="Select Photo Directory",
            initialdir=desktop_path
        )
        if directory:
            self.directory_var.set(directory)
    
    def start_slideshow(self):
        directory = self.directory_var.get().strip()
        if not directory:
            messagebox.showerror("Error", "Please select a directory")
            return
        
        if not os.path.exists(directory):
            messagebox.showerror("Error", "Selected directory does not exist")
            return
        
        try:
            display_time = float(self.display_time_var.get())
            dissolve_time = float(self.dissolve_time_var.get())
            
            if display_time <= 0:
                raise ValueError("Display time must be positive")
            if dissolve_time < 0:
                raise ValueError("Dissolve time must be non-negative")
                
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid timing values: {e}")
            return
        
        # Hide the launcher window
        self.root.withdraw()
        
        try:
            # Get image files from the directory first to validate
            # Remove the import line that's no longer needed
            image_files = get_image_files(directory)
            if not image_files:
                messagebox.showerror("Error", "No image files found in the selected directory.")
                self.root.deiconify()
                return
            
            print(f"Starting slideshow with {len(image_files)} images")
            print(f"Display time: {display_time}s, Dissolve time: {dissolve_time}s")
            
            # Close the launcher window
            self.root.quit()
            self.root.destroy()
            
            # Launch slideshow directly
            display_time_ms = int(display_time * 1000)
            dissolve_time_ms = int(dissolve_time * 1000)
            
            image_files = get_image_files(directory)
            if not image_files:
                messagebox.showerror("Error", "No image files found in the selected directory.")
                return
                
            print(f"Starting slideshow with {len(image_files)} images")
            print(f"Display time: {display_time}s, Dissolve time: {dissolve_time}s")
            
            FullscreenImageViewer(image_files, display_time_ms, dissolve_time_ms)
            
        except ImportError as e:
            error_msg = f"Failed to import slideshow module: {e}"
            print(f"Error: {error_msg}")
            try:
                messagebox.showerror("Import Error", error_msg)
            except:
                print("Could not show error dialog")
            self.root.deiconify()
        except Exception as e:
            error_msg = f"Failed to start slideshow: {e}"
            print(f"Error: {error_msg}")
            try:
                messagebox.showerror("Slideshow Error", error_msg)
            except:
                print("Could not show error dialog")
            try:
                self.root.deiconify()
            except:
                pass
    
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
    def __init__(self, image_files, display_time_ms=5000, dissolve_time_ms=1000, dissolve_frames=30):
        self.image_files = image_files
        self.display_time_ms = display_time_ms
        self.dissolve_time_ms = dissolve_time_ms
        self.dissolve_frames = dissolve_frames
        self.img_idx = 0
        self.timer_id = None
        self.dissolve_id = None
        self.paused = False
        
        # Create and configure the root window
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.config(cursor="none", bg='black')
        
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
        self.root.bind("<Escape>", self.quit_app)
        self.root.bind("q", self.quit_app)
        
        # Show first image and start slideshow
        self.root.focus_force()  # Ensure window has focus
        
        # Initialize the slideshow
        self.show_image(self.img_idx, dissolve=False)
        self.root.mainloop()

    def prepare_canvas(self, img_path):
        """Resize image with aspect ratio, center it on transparent canvas"""
        try:
            print(f"Loading image: {img_path}")
            img = Image.open(img_path).convert('RGBA')
            print(f"Image loaded successfully: {img.size}")
            
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

            img = img.resize((new_width, new_height), Image.LANCZOS)
            canvas = Image.new('RGBA', (screen_width, screen_height), (0, 0, 0, 255))
            offset_x = (screen_width - new_width) // 2
            offset_y = (screen_height - new_height) // 2
            canvas.paste(img, (offset_x, offset_y))
            print(f"Canvas prepared successfully: {canvas.size}")
            return canvas
        except Exception as e:
            print(f"Error loading image {img_path}: {e}")
            # Return a black canvas if image loading fails
            screen_width, screen_height = self.screen_size
            print(f"Creating fallback black canvas: {screen_width}x{screen_height}")
            return Image.new('RGBA', (screen_width, screen_height), (0, 0, 0, 255))

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
            # Convert to RGB if needed  
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # Create PhotoImage using ImageTk
            photo = ImageTk.PhotoImage(pil_image)
            return photo
        except Exception as e:
            print(f"Failed to create PhotoImage: {e}")
            # Create a black fallback image
            try:
                black_img = Image.new('RGB', self.screen_size, (0, 0, 0))
                return ImageTk.PhotoImage(black_img)
            except:
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
            
            # Store multiple references to prevent garbage collection
            self.photo = photo
            self.current_photo = photo
            self.label.image = photo
            
            # Update the label display
            print("Updating label...")
            self.label.config(image=photo)
            
            # Force immediate update
            self.label.update_idletasks()
            self.root.update_idletasks()
            print("Image display completed")
            
        except Exception as e:
            print(f"Error displaying image: {e}")
            # Try to display a black screen if image display fails
            try:
                black_img = Image.new('RGB', self.screen_size, (0, 0, 0))
                fallback_photo = self.safe_create_photoimage(black_img)
                if fallback_photo:
                    self.photo = fallback_photo
                    self.current_photo = fallback_photo
                    self.label.image = fallback_photo
                    self.label.config(image=fallback_photo)
                    self.label.update_idletasks()
                    print("Fallback black image displayed")
            except Exception as fallback_error:
                print(f"Error creating fallback image: {fallback_error}")

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
    app = SlideshowApp()
    app.run()
