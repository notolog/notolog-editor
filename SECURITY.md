<!-- {"notolog.app": {"created": "2026-01-18 13:57:00.794379", "updated": "2026-01-18 13:57:00.794379"}} -->
# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in Notolog, please report it responsibly.

### How to Report

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, please report security vulnerabilities by emailing the maintainers directly or using GitHub's private vulnerability reporting feature:

1. Go to the [Security tab](https://github.com/notolog/notolog-editor/security) of the repository
2. Click "Report a vulnerability"
3. Provide detailed information about the vulnerability

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Resolution Target**: Within 30 days (depending on severity)

### After Reporting

1. We will acknowledge receipt of your report
2. We will investigate and validate the issue
3. We will work on a fix
4. We will coordinate disclosure with you
5. We will credit you in the release notes (unless you prefer anonymity)

## Security Best Practices for Users

### File Encryption

- Use strong, unique passwords for encrypted files
- Notolog uses AES-128 encryption with PBKDF2 key derivation (768,000 iterations)
- There is no password recovery - keep secure backups

### API Keys

- Store OpenAI API keys securely
- API keys are encrypted in local storage
- Never share your API key

### Local LLM Models

- Only download models from trusted sources
- Verify model checksums when available

## Known Security Considerations

### Encryption Details

| Property | Value |
|----------|-------|
| Algorithm | AES-128 CBC (Fernet) |
| Key Derivation | PBKDF2HMAC with SHA-256 |
| Iterations | 768,000 |
| Salt | 32 bytes, cryptographically random |

### Data Storage

- Settings are stored locally using Qt's QSettings
- Sensitive settings (API keys) are encrypted
- No data is sent to external servers except when using cloud AI APIs

## Acknowledgments

We thank all security researchers who responsibly disclose vulnerabilities.

---

*Last updated: January 2026*
