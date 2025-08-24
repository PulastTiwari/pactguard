# Contributing to PactGuard

Thank you for your interest in contributing to PactGuard! This document provides guidelines for contributing to the project.

## Code of Conduct

This project adheres to a code of conduct that promotes a welcoming and inclusive environment. By participating, you are expected to uphold this standard.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, please include:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Your environment (OS, browser, versions)
- Screenshots if applicable

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- A clear, descriptive title
- A detailed description of the proposed feature
- Explain why this enhancement would be useful
- Include mockups or examples if applicable

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Ensure the test suite passes
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Setup

Please refer to the [Manual Development Environment Setup](README.md#manual-development-environment-setup) section in the README.

## Style Guidelines

### Code Style

- **Python**: Follow PEP 8 guidelines
- **TypeScript/JavaScript**: Use Prettier and ESLint configurations
- **Commits**: Use conventional commit messages

### Documentation

- Update README.md if needed
- Document new functions and classes
- Update API documentation for backend changes

## Development Workflow

1. **Backend Development**:

   - Make changes in `pactguard-backend/`
   - Test with `pytest` if tests are available
   - Verify API functionality at `http://localhost:8001/docs`

2. **Frontend Development**:

   - Make changes in Next.js components
   - Test in development mode (`npm run dev`)
   - Ensure TypeScript compilation passes

3. **Integration Testing**:
   - Test the full stack locally
   - Verify Docker deployment works
   - Test with real API keys if possible

## Questions?

Feel free to open an issue for any questions about contributing to PactGuard.

## Recognition

Contributors will be recognized in the project documentation and release notes.
