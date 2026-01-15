# Contributing to LegacyLoop

Thank you for your interest in contributing to LegacyLoop! This document provides guidelines and information for contributors.

## 🚀 Getting Started

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create a branch** for your changes
4. **Make your changes** and test them
5. **Submit a Pull Request**

## 💻 Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/LegacyLoop.git
cd LegacyLoop

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 📝 Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular

## 🧪 Testing

Before submitting a PR:
1. Ensure the app runs without errors
2. Test all three views (Primary, Heir, Advisor)
3. Verify both simulation mode and live API mode work

## 📋 Pull Request Process

1. Update the README.md if needed
2. Ensure your code follows the existing style
3. Write a clear PR description explaining your changes
4. Link any related issues

## 🐛 Reporting Bugs

Use the GitHub Issues tab with the bug report template. Include:
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Your environment details

## 💡 Feature Requests

Use the GitHub Issues tab with the feature request template. Describe:
- The problem you're trying to solve
- Your proposed solution
- Any alternatives you've considered

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.
