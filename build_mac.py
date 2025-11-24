#!/usr/bin/env python3
"""
Simple build script for creating a macOS application bundle
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, text=True)
        print(f"✓ {description} completed successfully")
        return result
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(f"Error: {e}")
        return None

def main():
    print("Building SlideShow for macOS...")
    print("=" * 50)
    
    # Ensure we're in the right directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check if PyInstaller is installed
    print("\nChecking PyInstaller...")
    try:
        result = subprocess.run(["pyinstaller", "--version"], check=True, capture_output=True, text=True)
        print(f"✓ PyInstaller found: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("PyInstaller not found. Installing...")
        result = run_command("pip3 install pyinstaller", "Installing PyInstaller")
        if not result:
            print("Failed to install PyInstaller. Please install it manually:")
            print("pip3 install pyinstaller")
            sys.exit(1)
    
    # Clean previous builds
    print("\nCleaning previous builds...")
    for folder in ["build", "dist"]:
        if Path(folder).exists():
            shutil.rmtree(folder)
            print(f"✓ Removed {folder}/")
    
    # Build the application using the spec file
    build_result = run_command("pyinstaller SlideShow.spec", "Building application bundle")
    
    if build_result:
        app_path = Path("dist/SlideShow.app")
        if app_path.exists():
            print("\n" + "=" * 50)
            print("✓ BUILD COMPLETED SUCCESSFULLY!")
            print("=" * 50)
            print(f"\nApplication created: {app_path.absolute()}")
            print(f"Size: {get_folder_size(app_path):.1f} MB")
            
            print("\nTo test the application:")
            print(f"open '{app_path.absolute()}'")
            
            print("\nTo distribute:")
            print("1. Copy the SlideShow.app bundle to another Mac")
            print("2. Or create a DMG file for distribution")
            
            # Offer to create DMG
            try:
                response = input("\nCreate a DMG file for distribution? (y/n): ").lower()
                if response == 'y':
                    create_dmg()
            except KeyboardInterrupt:
                print("\nBuild completed.")
        else:
            print("✗ Application bundle not found after build")
    else:
        print("✗ Build failed")
        sys.exit(1)

def get_folder_size(path):
    """Calculate folder size in MB"""
    total = 0
    for file_path in Path(path).rglob('*'):
        if file_path.is_file():
            total += file_path.stat().st_size
    return total / (1024 * 1024)

def create_dmg():
    """Create a DMG file for distribution"""
    app_path = Path("dist/SlideShow.app")
    dmg_name = "SlideShow-macOS.dmg"
    
    # Remove existing DMG
    if Path(dmg_name).exists():
        Path(dmg_name).unlink()
    
    dmg_cmd = f'hdiutil create -volname "SlideShow" -srcfolder "{app_path}" -ov -format UDZO "{dmg_name}"'
    
    result = run_command(dmg_cmd, "Creating DMG file")
    if result and Path(dmg_name).exists():
        print(f"✓ DMG created: {Path(dmg_name).absolute()}")
        print(f"Size: {Path(dmg_name).stat().st_size / (1024*1024):.1f} MB")
    else:
        print("✗ Failed to create DMG file")

if __name__ == "__main__":
    main()