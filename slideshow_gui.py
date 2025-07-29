#!/usr/bin/env python3
"""
SlideShow Application
A unified interface for selecting directories and slideshow settings
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import sys
import os
from pathlib import Path

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
            # Run the slideshow using slide_show_gui.py directly
            script_path = Path(__file__).parent / "slide_show_gui.py"
            cmd = [sys.executable, str(script_path), directory, 
                   str(display_time), str(dissolve_time)]
            
            subprocess.run(cmd, check=True)
            
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to start slideshow: {e}")
        except FileNotFoundError:
            messagebox.showerror("Error", "slide_show_gui.py not found")
        finally:
            # Show the launcher window again
            self.root.deiconify()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SlideshowApp()
    app.run()
