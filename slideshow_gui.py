#!/usr/bin/env python3
"""
GUI wrapper for the slideshow application
Provides a simple interface to select directory and timing options
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import sys
import os
from pathlib import Path

class SlideshowLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Photo Slideshow Launcher")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Variables
        self.directory_var = tk.StringVar()
        self.display_time_var = tk.StringVar(value="5.0")
        self.dissolve_time_var = tk.StringVar(value="1.0")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Photo Slideshow", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Directory selection
        ttk.Label(main_frame, text="Select Photo Directory:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        dir_frame = ttk.Frame(main_frame)
        dir_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.dir_entry = ttk.Entry(dir_frame, textvariable=self.directory_var, width=40)
        self.dir_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(dir_frame, text="Browse...", 
                  command=self.browse_directory).grid(row=0, column=1)
        
        dir_frame.columnconfigure(0, weight=1)
        
        # Timing options
        ttk.Label(main_frame, text="Display Time (seconds):").grid(row=3, column=0, sticky=tk.W, pady=(20, 5))
        ttk.Entry(main_frame, textvariable=self.display_time_var, width=10).grid(row=3, column=1, sticky=tk.W, pady=(20, 5))
        
        ttk.Label(main_frame, text="Dissolve Time (seconds):").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.dissolve_time_var, width=10).grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=(30, 0))
        
        ttk.Button(button_frame, text="Start Slideshow", 
                  command=self.start_slideshow).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Exit", 
                  command=self.root.quit).grid(row=0, column=1, padx=5)
        
        # Instructions
        instructions = """Instructions:
• Press Escape or 'q' to quit slideshow
• Press Space to pause/resume
• Use Left/Right arrows to navigate
• Supports JPG, PNG, WebP, BMP, TIFF files"""
        
        ttk.Label(main_frame, text=instructions, 
                 justify=tk.LEFT, font=("Arial", 9)).grid(row=6, column=0, columnspan=3, pady=(20, 0))
        
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
            # Run the slideshow
            script_path = Path(__file__).parent / "slide_show.py"
            cmd = [sys.executable, str(script_path), directory, 
                   str(display_time), str(dissolve_time)]
            
            subprocess.run(cmd, check=True)
            
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to start slideshow: {e}")
        except FileNotFoundError:
            messagebox.showerror("Error", "slide_show.py not found")
        finally:
            # Show the launcher window again
            self.root.deiconify()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SlideshowLauncher()
    app.run()
