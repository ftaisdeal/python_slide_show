# Contributing to SlideShow

Thank you for your interest in contributing to SlideShow! We welcome contributions from everyone and appreciate your help in making this project better.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Issue Guidelines](#issue-guidelines)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the [existing issues](../../issues) to see if the problem has already been reported. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** with sample images or directories if applicable
- **Describe the behavior you observed** and what behavior you expected
- **Include system information**: OS, Python version, screen resolution
- **Add screenshots** if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as [GitHub issues](../../issues). When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful** to most SlideShow users
- **List any alternatives** you've considered

### Code Contributions

We welcome code contributions! Here are some areas where help is particularly appreciated:

- **Bug fixes**
- **Performance improvements**
- **New image format support**
- **UI/UX enhancements**
- **Cross-platform compatibility improvements**
- **Documentation improvements**

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic knowledge of Python and Tkinter

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/python_slide_show.git
   cd python_slide_show
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller  # For building executables
   ```

5. **Create a new branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

6. **Test the application** to ensure everything works:
   ```bash
   python slideshow_gui.py
   ```

## Development Process

### Making Changes

1. **Make your changes** in your feature branch
2. **Test your changes thoroughly**:
   - Test on multiple image formats
   - Test with different image sizes and orientations
   - Test GUI interactions
   - Test command-line interface if applicable

3. **Follow the coding standards** (see below)
4. **Update documentation** if necessary
5. **Commit your changes** with clear, descriptive messages

### Commit Message Guidelines

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

**Examples:**
```
Add support for HEIC image format

- Implement HEIC decoding using Pillow
- Add HEIC to supported formats list
- Update documentation

Fixes #123
```

## Pull Request Guidelines

### Before Submitting

- Ensure your code follows the project's coding standards
- Test your changes thoroughly
- Update documentation if needed
- Make sure all existing tests still pass
- Add new tests if you're adding functionality

### Submitting Your Pull Request

1. **Push your changes** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a pull request** on GitHub with:
   - **Clear title** describing the change
   - **Detailed description** of what you changed and why
   - **Reference any related issues** using "Fixes #issue-number"
   - **Screenshots** if the change affects the UI

3. **Be responsive** to feedback and be prepared to make changes

### Pull Request Review Process

- All pull requests require review before merging
- We may suggest changes, improvements, or alternatives
- Once approved, a maintainer will merge your pull request

## Coding Standards

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and reasonably sized

### Code Organization

- Keep related functionality together
- Use clear imports and avoid wildcard imports
- Comment complex logic and algorithms
- Handle errors gracefully with appropriate error messages

### Example Code Style

```python
def load_image_with_orientation(image_path):
    """
    Load an image and apply EXIF orientation correction.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        PIL.Image: Processed image with correct orientation
        
    Raises:
        IOError: If the image cannot be loaded
    """
    try:
        with Image.open(image_path) as img:
            # Apply EXIF orientation
            img = ImageOps.exif_transpose(img)
            return img.copy()
    except Exception as e:
        raise IOError(f"Cannot load image {image_path}: {e}")
```

## Testing

### Manual Testing

Before submitting changes, please test:

- **Basic functionality**: Can you start a slideshow?
- **Image formats**: Test with JPEG, PNG, WebP, etc.
- **Edge cases**: Empty directories, corrupted images, very large images
- **Cross-platform**: Test on different operating systems if possible
- **Performance**: Test with large image collections

### Test Images

Create a test directory with:
- Various image formats (JPEG, PNG, WebP, BMP, TIFF, GIF)
- Different orientations (portrait, landscape, rotated)
- Different sizes (small thumbnails to large high-resolution)
- Images with and without EXIF data

## Documentation

### Updating Documentation

When making changes, please update:

- **README.md** for user-facing changes
- **Code comments** for complex logic
- **Docstrings** for new functions/classes
- **This CONTRIBUTING.md** if you change the development process

### Documentation Style

- Use clear, simple language
- Provide examples where helpful
- Keep documentation up-to-date with code changes
- Use proper Markdown formatting

## Issue Guidelines

### Creating Issues

- **Search existing issues** first to avoid duplicates
- **Use issue templates** when available
- **Provide detailed information** including system specs
- **Add appropriate labels** (bug, enhancement, question, etc.)

### Issue Labels

- `bug`: Something isn't working correctly
- `enhancement`: New feature or improvement
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `question`: Questions about usage

## Recognition

Contributors will be recognized in:
- The project's README acknowledgments section
- Release notes for significant contributions
- GitHub's contributor graph

## Questions?

If you have questions about contributing, please:

1. Check this document and the README
2. Search existing issues
3. Create a new issue with the "question" label
4. Reach out to the maintainers

Thank you for contributing to SlideShow! 🎉
