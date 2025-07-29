#!/usr/bin/env python3
"""
Build script for SlideShow application
Creates executables for the current platform
"""

import os
import sys
import subprocess
import platform

def main():
    print("🔨 Building SlideShow application...")
    print(f"Platform: {platform.system()}")
    print(f"Python: {sys.version}")
    
    # Check if pyinstaller is installed
    try:
        import PyInstaller
        print(f"PyInstaller: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller installed")
    
    # Check if Pillow is installed
    try:
        import PIL
        print(f"Pillow: {PIL.__version__}")
    except ImportError:
        print("❌ Pillow not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pillow"], check=True)
        print("✅ Pillow installed")
    
    # Build the application
    print("\n🏗️  Building executable...")
    
    cmd = [
        "pyinstaller",
        "--onedir",
        "--windowed",
        "--name", "SlideShow",
        "slide_show_gui.py",
        "--noconfirm"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Build completed successfully!")
        print(f"📦 Your executable is in: dist/SlideShow{''.join(['.app' if platform.system() == 'Darwin' else '.exe' if platform.system() == 'Windows' else ''])}")
        
        if platform.system() == "Darwin":
            print("\n💡 On macOS, you can move SlideShow.app to your Applications folder")
        elif platform.system() == "Windows":
            print("\n💡 On Windows, you can create a desktop shortcut to SlideShow.exe")
        else:
            print("\n💡 On Linux, you can create a desktop entry for the executable")
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
