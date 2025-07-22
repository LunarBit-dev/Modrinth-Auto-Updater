# Security Policy

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability in this project, please follow these steps:

### How to Report

1. **Do NOT create a public GitHub issue** for security vulnerabilities
2. Email us directly at [your-email@example.com] with:
   - A clear description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact of the vulnerability
   - Any suggested fixes (if available)

### What to Expect

- **Response Time**: We aim to respond to security reports within 48 hours
- **Initial Assessment**: We will assess the vulnerability within 7 days
- **Resolution Timeline**: Critical vulnerabilities will be patched within 30 days
- **Credit**: We will acknowledge your contribution in the security advisory (unless you prefer to remain anonymous)

### Security Best Practices

When using this tool:

1. **Keep Dependencies Updated**: Regularly update Python and the `requests` library
2. **Network Security**: Be aware that this tool makes HTTPS requests to the Modrinth API
3. **File Permissions**: Ensure proper file permissions when running the script
4. **Input Validation**: Be cautious when processing untrusted .mrpack files

### Known Security Considerations

- This tool downloads files from the internet (Modrinth CDN)
- It extracts .mrpack files which are essentially ZIP archives
- It makes HTTP requests to the Modrinth API

We implement the following security measures:
- HTTPS-only API requests
- Safe file extraction (no path traversal)
- Input validation for file paths
- Temporary file cleanup

## Scope

This security policy applies to:
- The main `update_modpack.py` script
- All code in this repository
- Dependencies listed in `requirements.txt`

This policy does not cover:
- Third-party mods downloaded by the tool
- User-provided modpack configurations
- External services (Modrinth API, CDN)

Thank you for helping keep our project secure!
