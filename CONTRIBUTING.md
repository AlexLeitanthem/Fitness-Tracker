# Contributing to Fitness Tracker Pro

Thank you for your interest in contributing to Fitness Tracker Pro! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a virtual environment
4. Install dependencies
5. Make your changes
6. Test your changes
7. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone <your-fork-url>
cd fitness-tracker-pro

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and small
- Use type hints where appropriate

## Testing

Before submitting changes:

1. Test the application thoroughly
2. Verify database operations work correctly
3. Test both strength and cardio workout entries
4. Check that the calendar view updates properly
5. Ensure file parser functionality works

## Pull Request Process

1. Create a feature branch from main
2. Make your changes
3. Test thoroughly
4. Update documentation if needed
5. Submit a pull request with a clear description

## Feature Requests

When suggesting new features:

1. Check existing issues first
2. Provide a clear description of the feature
3. Explain the use case and benefits
4. Consider implementation complexity

## Bug Reports

When reporting bugs:

1. Check existing issues first
2. Provide steps to reproduce
3. Include system information (OS, Python version)
4. Attach screenshots if relevant
5. Describe expected vs actual behavior

## Areas for Contribution

- UI/UX improvements
- Additional exercise database entries
- Export/import functionality
- Data visualization features
- Mobile app companion
- Cloud sync capabilities
- Advanced analytics

## Questions?

Feel free to open an issue for questions or discussions about the project.
