# Security Policy

## Supported Versions

Currently supported versions of PactGuard:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in PactGuard, please report it responsibly:

### How to Report

1. **Do not** open a public issue for security vulnerabilities
2. Email security concerns to: [your-email@domain.com] (replace with actual email)
3. Include detailed information about the vulnerability
4. Provide steps to reproduce if possible

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact assessment
- Any suggested fixes

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Resolution**: Depends on severity and complexity

### Responsible Disclosure

We follow responsible disclosure principles:

- We will acknowledge receipt of your report
- We will provide regular updates on our progress
- We will credit you for the discovery (unless you prefer to remain anonymous)
- We will coordinate public disclosure timing with you

## Security Considerations

### API Keys and Credentials

- Never commit API keys to the repository
- Use environment variables for sensitive configuration
- Rotate API keys regularly
- Use the principle of least privilege

### Data Handling

- Legal documents may contain sensitive information
- Ensure proper data encryption in transit and at rest
- Follow data retention policies
- Implement proper access controls

### Dependencies

- Regularly update dependencies to patch security vulnerabilities
- Monitor for security advisories
- Use tools like `npm audit` and `pip-audit` for vulnerability scanning

## Best Practices for Contributors

- Review the [Contributing Guidelines](CONTRIBUTING.md)
- Run security linters and vulnerability scanners
- Test with minimal required permissions
- Document security-relevant changes

## Contact

For security-related questions or concerns, please contact the project maintainer through the appropriate channels listed in the README.
