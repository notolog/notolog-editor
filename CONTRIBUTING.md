<!-- {"notolog.app": {"created": "2026-01-18 13:57:00.794379", "updated": "2026-01-18 13:57:00.794379"}} -->
# Contributing to Notolog

Thank you for your interest in contributing to Notolog! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment (see below)
4. Create a branch for your changes
5. Make your changes
6. Test your changes
7. Submit a pull request

## How to Contribute

### Types of Contributions

- **Bug Fixes**: Fix issues reported in the issue tracker
- **Features**: Implement new features (discuss in an issue first)
- **Documentation**: Improve or add documentation
- **Translations**: Add or improve language translations
- **Tests**: Add or improve test coverage

### Before You Start

- Check existing issues and pull requests to avoid duplicates
- For significant changes, open an issue first to discuss

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/notolog-editor.git
cd notolog-editor

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install in development mode
pip install -e .

# Install development dependencies
python dev_install.py dev

# Install test dependencies
python dev_install.py test
```

### Running the Application

```bash
python -m notolog.app
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest tests/ --cov=notolog --cov-report=term

# Run specific test file
pytest tests/test_app.py -v
```

## Coding Standards

### Style Guide

- Follow PEP 8 for Python code
- Use snake_case for functions and variables
- Use CamelCase for class names
- Maximum line length: 127 characters

### Code Quality Tools

```bash
# Run flake8 for linting
flake8 . --count --exit-zero --max-complexity=15 --max-line-length=127 --per-file-ignores="__init__.py:F401" --statistics
```

### Documentation

- Add docstrings to all public methods and classes
- Follow Google-style docstrings
- Update README.md if adding user-facing features

### Type Hints

- Use type hints for function parameters and return values
- Use `TYPE_CHECKING` for import-only type hints

```python
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget
```

## Submitting Changes

### Commit Messages

Follow conventional commit format:

```
type(scope): short description

Longer description if needed.

Fixes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Add entry to CHANGELOG.md under `[Unreleased]`
4. Fill out the pull request template
5. Request review from maintainers

### Pull Request Checklist

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated (if applicable)
- [ ] CHANGELOG.md updated
- [ ] Commits are clean and well-described

## Reporting Issues

### Bug Reports

Include:
- Notolog version (`notolog --version`)
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs

### Feature Requests

Include:
- Clear description of the feature
- Use case / motivation
- Possible implementation approach (optional)

## Questions?

- Open a [GitHub Discussion](https://github.com/notolog/notolog-editor/discussions)
- Check existing [issues](https://github.com/notolog/notolog-editor/issues)

---

Thank you for contributing to Notolog! 🎉
