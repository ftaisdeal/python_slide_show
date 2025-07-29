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
    
    # Use the current Python executable
    python_cmd = sys.executable
    
    # On macOS, prefer system Python over Homebrew Python for better tkinter support
    # But in CI environments, just use the current Python
    if platform.system() == "Darwin" and "GITHUB_ACTIONS" not in os.environ:
        # Get the current Python version (e.g., "3.11" or "3.12")
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        system_python = f"/Library/Frameworks/Python.framework/Versions/{python_version}/bin/python3"
        if os.path.exists(system_python):
            python_cmd = system_python
            print(f"Using system Python: {python_cmd}")
        else:
            print(f"System Python not found at {system_python}, using current Python: {python_cmd}")
    elif "GITHUB_ACTIONS" in os.environ:
        print(f"Running in GitHub Actions, using setup Python: {python_cmd}")
    
    # Verify tkinter is available (critical for GUI)
    try:
        subprocess.run([python_cmd, "-c", "import tkinter; print('✅ tkinter available')"], 
                      capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("❌ tkinter not available. GUI applications require tkinter.")
        print("On Ubuntu/Debian: sudo apt-get install python3-tk")
        print("On CentOS/RHEL: sudo yum install tkinter")
        sys.exit(1)
    
    # Check if pyinstaller is installed
    try:
        result = subprocess.run([python_cmd, "-c", "import PyInstaller; print(f'PyInstaller: {PyInstaller.__version__}')"], 
                              capture_output=True, text=True, check=True)
        print(result.stdout.strip())
    except (ImportError, subprocess.CalledProcessError):
        print("❌ PyInstaller not found. It should be installed via requirements.txt")
        sys.exit(1)
    
    # Check if Pillow is installed
    try:
        result = subprocess.run([python_cmd, "-c", "import PIL; print(f'Pillow: {PIL.__version__}')"], 
                              capture_output=True, text=True, check=True)
        print(result.stdout.strip())
    except (ImportError, subprocess.CalledProcessError):
        print("❌ Pillow not found. It should be installed via requirements.txt")
        sys.exit(1)
    
    # Build the application
    print("\n🏗️  Building executable...")
    
    cmd = [
        python_cmd, "-m", "PyInstaller",
        "--onedir",
        "--windowed",
        "--name", "SlideShow",
        "slideshow_gui.py",
        "--noconfirm"
    ]
    
    # Platform-specific options
    if platform.system() == "Darwin":
        cmd.extend(["--osx-bundle-identifier", "com.slideshow.app"])
        # On macOS ARM64, ensure we build for the native architecture
        if platform.machine() == "arm64":
            cmd.extend(["--target-arch", "arm64"])
    elif platform.system() == "Linux":
        # Add hidden imports that might be needed on Linux
        cmd.extend(["--hidden-import", "PIL._tkinter_finder"])
    
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
