# 🤝 Contributing to Meeting Summarizer Pro

Thank you for your interest in contributing to Meeting Summarizer Pro! This document provides guidelines and information for contributors.

## 🎯 How Can I Contribute?

### 🐛 **Report Bugs**
- Use the [GitHub Issues](https://github.com/satishkkrishnan/meeting-summarizer/issues) page
- Include detailed bug reports with steps to reproduce
- Provide system information and error logs

### 💡 **Suggest Features**
- Open a [Feature Request](https://github.com/satishkkrishnan/meeting-summarizer/issues/new?template=feature_request.md) issue
- Describe the feature and its benefits
- Include mockups or examples if possible

### 🔧 **Submit Code Changes**
- Fork the repository
- Create a feature branch
- Make your changes
- Submit a pull request

### 📚 **Improve Documentation**
- Fix typos and grammar
- Add examples and tutorials
- Improve code comments
- Update README sections

### 🧪 **Testing**
- Test on different platforms
- Report compatibility issues
- Suggest test improvements

## 🚀 Getting Started

### **Prerequisites**
- Python 3.8+
- Git
- Basic knowledge of Python and GUI development

### **Setup Development Environment**

1. **Fork the repository**
   ```bash
   # Go to GitHub and fork the repo
   # Then clone your fork
   git clone https://github.com/satishkkrishnan/meeting-summarizer.git
   cd meeting-summarizer
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 Development Guidelines

### **Code Style**
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) Python style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose

### **Commit Messages**
Use clear, descriptive commit messages:
```bash
# Good examples:
git commit -m "Add screenshot functionality to notes section"
git commit -m "Fix audio recording issue on Windows 11"
git commit -m "Update README with installation instructions"

# Avoid:
git commit -m "fix stuff"
git commit -m "update"
```

### **Testing**
- Test your changes thoroughly
- Test on different platforms if possible
- Include test cases for new features
- Ensure existing functionality still works

### **Documentation**
- Update README.md if adding new features
- Add inline comments for complex logic
- Update help text in the application
- Document any new configuration options

## 🔄 Pull Request Process

### **Before Submitting**
1. **Test thoroughly** - Ensure your changes work correctly
2. **Update documentation** - Modify README, help text, etc.
3. **Check code style** - Run linters and formatters
4. **Rebase if needed** - Keep your branch up to date

### **Creating the PR**
1. **Clear title** - Describe the change concisely
2. **Detailed description** - Explain what and why
3. **Screenshots** - Include UI changes if applicable
4. **Testing notes** - Describe how you tested

### **PR Template**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
- [ ] Tested on Windows
- [ ] Tested on Linux (if applicable)
- [ ] Tested on macOS (if applicable)
- [ ] All existing tests pass

## Screenshots
Include screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## 🏗️ Project Structure

```
meeting-summarizer/
├── meeting_summarizer.py      # Main application
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── README.md                 # Project documentation
├── CONTRIBUTING.md           # This file
├── LICENSE                   # MIT License
├── .github/                  # GitHub-specific files
│   ├── ISSUE_TEMPLATE/      # Issue templates
│   └── PULL_REQUEST_TEMPLATE.md
├── tests/                    # Test files
├── docs/                     # Additional documentation
└── examples/                 # Usage examples
```

## 🧪 Testing Guidelines

### **Manual Testing**
- Test all major features
- Test edge cases and error conditions
- Test on different screen resolutions
- Test with various audio inputs

### **Automated Testing**
- Write unit tests for new functions
- Ensure test coverage for critical paths
- Run existing tests before submitting

### **Cross-Platform Testing**
- Primary: Windows 10/11
- Secondary: Linux (Ubuntu/Debian)
- Tertiary: macOS (if available)

## 📋 Issue Templates

### **Bug Report Template**
```markdown
**Describe the bug**
Clear description of what the bug is

**To Reproduce**
Steps to reproduce the behavior

**Expected behavior**
What you expected to happen

**Actual behavior**
What actually happened

**Environment**
- OS: [e.g., Windows 11]
- Python version: [e.g., 3.9.7]
- App version: [e.g., 1.0.0]

**Additional context**
Any other context about the problem
```

### **Feature Request Template**
```markdown
**Is your feature request related to a problem?**
Description of the problem

**Describe the solution you'd like**
Clear description of what you want

**Describe alternatives you've considered**
Alternative solutions or features

**Additional context**
Any other context or screenshots
```

## 🎨 UI/UX Guidelines

### **Design Principles**
- **Consistency** - Follow existing design patterns
- **Accessibility** - Ensure usability for all users
- **Responsiveness** - Handle different window sizes
- **Intuitiveness** - Make features easy to discover

### **Color Scheme**
- Use existing color variables
- Maintain dark mode compatibility
- Ensure sufficient contrast
- Follow accessibility guidelines

## 🔒 Security Guidelines

### **API Keys**
- Never commit API keys to the repository
- Use environment variables for sensitive data
- Document required API keys clearly
- Provide secure examples in documentation

### **Data Privacy**
- Ensure user data stays local
- Don't log sensitive information
- Follow privacy best practices
- Document data handling policies

## 📞 Getting Help

### **Communication Channels**
- **GitHub Issues** - For bugs and feature requests
- **GitHub Discussions** - For questions and ideas
- **Pull Requests** - For code reviews and feedback

### **Code Review Process**
- All PRs require review before merging
- Maintainers will provide feedback
- Address review comments promptly
- Be open to suggestions and improvements

## 🙏 Recognition

### **Contributor Recognition**
- Contributors will be listed in README.md
- Significant contributions will be highlighted
- All contributors will be acknowledged in releases

### **Types of Contributions**
- **Code contributions** - New features, bug fixes
- **Documentation** - README, help text, tutorials
- **Testing** - Bug reports, compatibility testing
- **Community** - Helping other users, answering questions

## 📄 License

By contributing to Meeting Summarizer Pro, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Meeting Summarizer Pro! 🎉**

Your contributions help make this tool better for everyone in the community.
