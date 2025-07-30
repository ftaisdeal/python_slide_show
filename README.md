# SlideShow

A cross-platform full-screen photo slideshow application with smooth dissolve transitions.

![Platform Support](https:/## Keyboard Controls

| Key | Action |
|-----|--------|
| `Right Arrow` | Next image |
| `Left Arrow` | Previous image |
| `Space` | Pause/Resume |
| `Escape` | Return to launcher (or quit if launched from command line) |

**To quit the application:**
- **macOS**: `Cmd+Q` or SlideShow menu → Quit
- **Windows**: Click the X button, Alt+F4, or File menu → Exit  
- **Linux**: `Ctrl+Q` or application menu → Quitelds.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![License](https://img.shields.io/badge/License-CC%20BY--NC%204.0-orange)

## Features

- **Full-screen slideshow** with automatic image cycling
- **Smooth dissolve transitions** between images
- **Cross-platform compatibility** (Windows, macOS, Linux)
- **Multiple image formats** (JPG, PNG, WebP, BMP, TIFF, GIF)
- **Customizable timing** for display and transition duration
- **Keyboard controls** for navigation and playback
- **Natural file sorting** matching your operating system
- **GUI and command-line** interfaces available

> **📄 License Notice**: SlideShow is free for personal, educational, and research use under the CC BY-NC 4.0 license. Commercial use is prohibited. [Learn more](#license)

## Installation

### Option 1: Download Pre-built Application (Recommended)

#### Windows
1. Go to [Releases](../../releases)
2. Download \`SlideShow-Windows.zip\`
3. Extract and run \`SlideShow.exe\`

#### macOS
1. Go to [Releases](../../releases)
2. Download \`SlideShow-macOS.zip\`
3. Extract and run \`SlideShow.app\`
4. If macOS shows security warnings, go to System Preferences > Security & Privacy > General and click "Open Anyway"

#### Linux
1. Go to [Releases](../../releases)
2. Download \`SlideShow-Linux.zip\`
3. Extract and run \`./SlideShow\`

### Option 2: Run from Source

#### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

#### Installation Steps

1. **Clone the repository**
   \`\`\`bash
   git clone https://github.com/ftaisdeal/python_slide_show.git
   cd python_slide_show
   \`\`\`

2. **Create virtual environment (recommended)**
   
   **Windows:**
   \`\`\`cmd
   python -m venv .venv
   .venv\\Scripts\\activate
   \`\`\`
   
   **macOS/Linux:**
   \`\`\`bash
   python3 -m venv .venv
   source .venv/bin/activate
   \`\`\`

3. **Install dependencies**
   \`\`\`bash
   pip install pillow
   \`\`\`

4. **Run the application**
   
   **GUI Version (recommended):**
   \`\`\`bash
   python slide_show_gui.py
   \`\`\`
   
   **Command Line Version:**
   \`\`\`bash
   python slide_show.py /path/to/your/photos
   \`\`\`

### Option 3: Build Your Own Executable

1. **Install PyInstaller**
   \`\`\`bash
   pip install pyinstaller
   \`\`\`

2. **Build the application**
   
   **Windows:**
   \`\`\`cmd
   pyinstaller --onedir --windowed --name "SlideShow" slide_show_gui.py
   \`\`\`
   
   **macOS/Linux:**
   \`\`\`bash
   pyinstaller --onedir --windowed --name "SlideShow" slide_show_gui.py
   \`\`\`

3. **Find your executable in the \`dist/\` folder**

## Usage

### GUI Version
1. Launch the application
2. Click "Browse..." to select your photo directory
3. Adjust display time and dissolve time if desired
4. Click "Start Slideshow"

### Command Line Version
\`\`\`bash
python slide_show.py <directory> [display_time_seconds] [dissolve_time_seconds]
\`\`\`

**Examples:**
\`\`\`bash
# Basic usage with defaults (5s display, 1s dissolve)
python slide_show.py ~/Pictures/vacation

# Custom timing (8s display, 2s dissolve)
python slide_show.py ~/Pictures/vacation 8 2

# Fast slideshow (1s display, 0.5s dissolve)
python slide_show.py ~/Pictures/vacation 1 0.5
\`\`\`

## Keyboard Controls

| Key | Action |
|-----|--------|
| \`Escape\` or \`q\` | Quit slideshow |
| \`Space\` | Pause/Resume |
| \`Right Arrow\` | Next image |
| \`Left Arrow\` | Previous image |

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)
- BMP (.bmp)
- TIFF (.tiff, .tif)
- GIF (.gif)

*All formats support both uppercase and lowercase extensions*

## Technical Details

### Image Processing
- Images are automatically resized to fit your screen while maintaining aspect ratio
- Images are centered on a black background
- Smooth dissolve transitions are rendered in real-time
- **Automatic orientation correction** based on EXIF data ensures photos display correctly regardless of camera orientation

### EXIF Orientation Support
The application automatically reads and applies EXIF orientation data from your images:
- **Correct rotation**: Photos taken in portrait or rotated positions display upright
- **Seamless processing**: No manual rotation needed - works automatically
- **Preserves quality**: Orientation correction is applied without image degradation
- **Camera compatibility**: Works with photos from smartphones, digital cameras, and other devices that embed orientation metadata

*Note: Images without EXIF orientation data will display as-is*

### File Sorting
- **Windows**: Natural sorting (image1.jpg, image2.jpg, image10.jpg)
- **macOS**: Finder-compatible locale-aware sorting
- **Linux**: Case-insensitive alphabetical sorting

### Performance
- Optimized for large image collections
- Efficient memory usage with image caching
- Smooth 60fps dissolve animations

## Troubleshooting

### Common Issues

**"No image files found"**
- Ensure your directory contains supported image formats
- Check that file extensions are recognized (.jpg, .png, etc.)

**App won't start on macOS**
- Right-click the app and select "Open"
- Go to System Preferences > Security & Privacy and allow the app

**Slideshow runs too fast/slow**
- Adjust the display time in the GUI or command line arguments
- Minimum recommended display time: 0.1 seconds

**Images appear distorted**
- Images are automatically resized to fit screen while maintaining aspect ratio
- Very wide or tall images will have black bars to preserve proportions

### Getting Help
- Check the [Issues](../../issues) page for known problems
- Create a new issue with your problem description and system details
- Include error messages and steps to reproduce

## License

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License** (CC BY-NC 4.0).

### What this means:
- ✅ **You can**: Use, modify, and share this software freely for personal, educational, and research purposes
- ✅ **You can**: Create derivative works and improvements (with attribution)
- ❌ **You cannot**: Use this software for commercial purposes or sell it
- 📝 **You must**: Provide appropriate attribution when sharing or modifying

For the complete license terms, see the [LICENSE](LICENSE) file or visit [Creative Commons BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).

**Note**: This non-commercial license ensures the SlideShow software remains free and accessible while preventing commercial exploitation.

## Acknowledgments

- Built with Python and Tkinter
- Image processing powered by Pillow (PIL)
- Cross-platform compatibility through PyInstaller
