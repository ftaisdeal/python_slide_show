# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of SlideShow seriously. If you discover a security vulnerability, please follow these guidelines:

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities by email to:
**firinn@taisdeal.com**

### What to Include

When reporting a vulnerability, please include the following information:

- **Type of issue** (e.g. buffer overflow, injection, cross-site scripting, etc.)
- **Full paths of source file(s)** related to the manifestation of the issue
- **The location of the affected source code** (tag/branch/commit or direct URL)
- **Any special configuration required** to reproduce the issue
- **Step-by-step instructions to reproduce** the issue
- **Proof-of-concept or exploit code** (if possible)
- **Impact of the issue**, including how an attacker might exploit it

### Response Timeline

- We will acknowledge receipt of your vulnerability report within **48 hours**
- We will provide a detailed response within **7 days** indicating next steps
- We will keep you informed of our progress throughout the process
- If the issue is confirmed, we will release a fix as soon as possible

### Disclosure Policy

- We request that you give us a reasonable amount of time to fix the issue before public disclosure
- We will coordinate with you on the timing of disclosure
- We will credit you in our security advisory (unless you prefer to remain anonymous)

## Security Considerations

### Application-Specific Risks

SlideShow is a desktop application that processes image files. Potential security considerations include:

#### Image Processing Vulnerabilities
- **Malicious image files** could potentially exploit vulnerabilities in image processing libraries (Pillow/PIL)
- **Large image files** could cause memory exhaustion or denial of service
- **Malformed EXIF data** could potentially cause parsing errors

#### File System Access
- The application reads files from user-specified directories
- No files are written or modified by the application
- No network access is performed

#### Mitigation Strategies
- We use well-maintained image processing libraries (Pillow)
- Input validation is performed on file types and paths
- Error handling prevents crashes from malformed files
- No execution of external commands with user input

### Safe Usage Guidelines

To use SlideShow safely:

1. **Only open image directories from trusted sources**
2. **Be cautious with images from unknown sources** or the internet
3. **Keep the application updated** to receive security patches
4. **Report any suspicious behavior** immediately

### Dependencies

SlideShow relies on the following external libraries:

- **Pillow (PIL)** - Image processing library
  - We monitor security advisories for Pillow
  - We update to patched versions promptly when security issues are discovered

- **Tkinter** - GUI framework (part of Python standard library)
  - Security updates are handled through Python updates

- **PyInstaller** - Executable building (build-time only)
  - Not included in distributed executables

### Build Process Security

Our GitHub Actions build process:

- Uses official GitHub-hosted runners
- Only builds from tagged releases
- Signs macOS applications when possible
- Generates checksums for release artifacts

### Privacy

SlideShow:
- **Does not collect any user data**
- **Does not connect to the internet**
- **Does not transmit any information**
- **Only reads image files locally**
- **Does not modify or write files**

## Security Updates

Security updates will be:

- **Released as patch versions** (e.g., 1.0.1, 1.1.1)
- **Documented in release notes** with severity and impact
- **Available through the same distribution channels** (GitHub Releases)
- **Announced through GitHub Security Advisories**

## Vulnerability Database

We will publish security advisories through:

- **GitHub Security Advisories** for this repository
- **Release notes** describing the nature and impact of fixes
- **CVE database entries** for significant vulnerabilities (if applicable)

## Contact Information

For security-related inquiries:

- **Email**: firinn@taisdeal.com
- **Subject Line**: [SECURITY] SlideShow Vulnerability Report
- **PGP**: Not currently available (plaintext email is acceptable for initial contact)

For general questions about this security policy, please open a GitHub issue with the "question" label.

## Acknowledgments

We appreciate security researchers and users who help improve the security of SlideShow by responsibly disclosing vulnerabilities.

Security contributors will be acknowledged in:
- Security advisories (unless anonymity is requested)
- Release notes for security fixes
- A dedicated security acknowledgments section (if applicable)

---

**Note**: This security policy applies to the SlideShow application itself. For security issues with dependencies (Python, Pillow, etc.), please report them to the appropriate upstream projects.

Last updated: July 29, 2025
