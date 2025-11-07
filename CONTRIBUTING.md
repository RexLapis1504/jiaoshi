# Contributing to Jiaoshi - AI Paper Checker

Thank you for your interest in contributing to Jiaoshi! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/RexLapis1504/jiaoshi.git
   cd jiaoshi
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run tests**
   ```bash
   python validate_structure.py
   python test_system.py
   ```

## 📝 How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- System information (Python version, OS, etc.)

### Suggesting Features

For feature requests, please:
- Check if the feature already exists
- Explain the use case
- Provide examples if possible

### Submitting Pull Requests

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the existing code style
   - Add tests for new features
   - Update documentation as needed

3. **Test your changes**
   ```bash
   python validate_structure.py
   python test_system.py
   ```

4. **Commit your changes**
   ```bash
   git commit -m "Add: Brief description of changes"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## 🎨 Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and modular
- Comment complex logic

### Example:
```python
def calculate_score(correct: int, total: int) -> float:
    """
    Calculate percentage score.
    
    Args:
        correct: Number of correct answers
        total: Total number of questions
    
    Returns:
        Percentage score (0-100)
    """
    return (correct / total * 100) if total > 0 else 0
```

## 🧪 Testing

- Write tests for new features
- Ensure existing tests pass
- Test edge cases
- Include integration tests where appropriate

## 📚 Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Update inline comments as needed
- Include examples for new features

## 🔍 Code Review Process

1. All PRs require review before merging
2. Address reviewer feedback promptly
3. Keep PRs focused and manageable
4. Ensure CI checks pass

## 🏗️ Project Structure

```
jiaoshi/
├── app.py              # Main Gradio UI
├── agents.py           # Grading agents
├── document_utils.py   # Document processing
├── batch_processor.py  # Batch processing
├── excel_exporter.py   # Excel export
├── config.py          # Configuration
└── tests/             # Test files
```

## 🎯 Priority Areas

We especially welcome contributions in:

1. **New file format support** (e.g., images with OCR)
2. **Improved AI prompts** for better grading
3. **Additional export formats** (CSV, JSON, etc.)
4. **Performance optimizations**
5. **UI/UX improvements**
6. **Better error handling**
7. **Internationalization (i18n)**

## 💬 Communication

- Use GitHub Issues for bugs and features
- Be respectful and constructive
- Ask questions if anything is unclear

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for making Jiaoshi better! 🎓
