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
    
    # On macOS, prefer system Python over Homebrew Python for better tkinter support
    python_cmd = sys.executable
    if platform.system() == "Darwin":
        system_python = "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3"
        if os.path.exists(system_python):
            python_cmd = system_python
            print(f"Using system Python: {python_cmd}")
    
    # Check if pyinstaller is installed
    try:
        result = subprocess.run([python_cmd, "-c", "import PyInstaller; print(f'PyInstaller: {PyInstaller.__version__}')"], 
                              capture_output=True, text=True, check=True)
        print(result.stdout.strip())
    except (ImportError, subprocess.CalledProcessError):
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([python_cmd, "-m", "pip", "install", "--user", "pyinstaller"], check=True)
        print("✅ PyInstaller installed")
    
    # Check if Pillow is installed
    try:
        result = subprocess.run([python_cmd, "-c", "import PIL; print(f'Pillow: {PIL.__version__}')"], 
                              capture_output=True, text=True, check=True)
        print(result.stdout.strip())
    except (ImportError, subprocess.CalledProcessError):
        print("❌ Pillow not found. Installing...")
        subprocess.run([python_cmd, "-m", "pip", "install", "--user", "pillow"], check=True)
        print("✅ Pillow installed")
    
    # Build the application
    print("\n🏗️  Building executable...")
    
    cmd = [
        python_cmd, "-m", "PyInstaller",
        "--onedir",
        "--windowed",
        "--name", "SlideShow",
        "slideshow_gui.py",
        "--noconfirm",
        "--osx-bundle-identifier", "com.slideshow.app"
    ]
    
    # On macOS ARM64, ensure we build for the native architecture
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        cmd.extend(["--target-arch", "arm64"])
    
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
