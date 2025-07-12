# Contributing to Baresha Downloader

Thank you for your interest in contributing to Baresha Downloader! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **🐛 Bug Reports**: Help us identify and fix issues
- **✨ Feature Requests**: Suggest new features or improvements
- **📝 Documentation**: Improve guides, README, or code comments
- **🎨 UI/UX Improvements**: Enhance the user interface
- **🌍 Translations**: Add support for new languages
- **🧪 Testing**: Help test features and report issues
- **🔧 Code Contributions**: Submit pull requests with code changes

### Before You Start

1. **Check existing issues** to avoid duplicates
2. **Read the documentation** to understand the project
3. **Follow the code of conduct** in all interactions
4. **Use the issue templates** when reporting bugs or requesting features

## 🚀 Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Basic knowledge of Python and Tkinter

### Local Development

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/baresha-downloader.git
   cd baresha-downloader
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python youtube_downloader.py
   ```

### Development Dependencies

For development, you might also want to install:

```bash
pip install black flake8 pytest
```

## 📝 Code Style Guidelines

### Python Code

- Follow **PEP 8** style guidelines
- Use **type hints** where appropriate
- Write **docstrings** for functions and classes
- Keep functions **small and focused**
- Use **meaningful variable names**

### Example Code Style

```python
def download_video(url: str, output_path: str, quality: str = 'best') -> bool:
    """
    Download a video from YouTube.
    
    Args:
        url: YouTube video URL
        output_path: Directory to save the video
        quality: Video quality preference
        
    Returns:
        True if download successful, False otherwise
    """
    try:
        # Implementation here
        return True
    except Exception as e:
        logger.error(f"Download failed: {e}")
        return False
```

### UI Guidelines

- Follow **Tkinter best practices**
- Use **consistent naming** for UI elements
- Implement **proper error handling**
- Add **tooltips** for better UX
- Support **keyboard shortcuts**

## 🐛 Reporting Bugs

### Bug Report Template

When reporting bugs, please include:

1. **Environment Information**
   - Operating System and version
   - Python version
   - Baresha Downloader version

2. **Steps to Reproduce**
   - Clear, step-by-step instructions
   - Include any specific URLs or data

3. **Expected vs Actual Behavior**
   - What you expected to happen
   - What actually happened

4. **Additional Information**
   - Screenshots (if applicable)
   - Error messages or logs
   - Any workarounds you found

### Example Bug Report

```
**Bug Description**
The download button doesn't work when clicking after fetching video info.

**Steps to Reproduce**
1. Launch Baresha Downloader
2. Enter a YouTube URL
3. Click "Fetch Video Info"
4. Click "Download Batch"
5. Notice the button doesn't respond

**Expected Behavior**
Download should start when clicking the button.

**Actual Behavior**
Button appears disabled and doesn't respond to clicks.

**Environment**
- OS: Windows 11
- Python: 3.9.7
- Baresha Downloader: 1.0.0
```

## ✨ Requesting Features

### Feature Request Template

1. **Feature Description**
   - Clear description of the feature
   - Use cases and benefits

2. **Implementation Ideas**
   - How you think it could be implemented
   - Any technical considerations

3. **Mockups or Examples**
   - UI mockups (if applicable)
   - Code examples (if applicable)

### Example Feature Request

```
**Feature: Download Playlists**

**Description**
Add support for downloading entire YouTube playlists with a single click.

**Use Cases**
- Download educational course playlists
- Save music playlists for offline listening
- Archive channel content

**Implementation Ideas**
- Add playlist URL detection
- Create playlist download queue
- Show playlist progress in UI
- Allow selective playlist item download

**Mockup**
[Include UI mockup if applicable]
```

## 🔧 Making Code Contributions

### Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the code style guidelines
   - Add tests if applicable
   - Update documentation

3. **Test your changes**
   ```bash
   python youtube_downloader.py
   # Run any additional tests
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add playlist download support"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a pull request**
   - Use the PR template
   - Describe your changes clearly
   - Link any related issues

### Commit Message Guidelines

Use conventional commit messages:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

### Pull Request Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] UI/UX improvement
- [ ] Translation
- [ ] Other (please describe)

## Testing
- [ ] Tested on Windows
- [ ] Tested on macOS
- [ ] Tested on Linux
- [ ] Added unit tests
- [ ] Updated documentation

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## 🌍 Translation Contributions

### Adding New Languages

1. **Create language dictionary**
   ```python
   'new_lang': {
       'app_title': 'Your App Title',
       'download_tab': 'Download',
       # ... add all required keys
   }
   ```

2. **Update language selector**
   - Add new language to settings
   - Test all UI elements

3. **Test thoroughly**
   - Check all text displays correctly
   - Verify no missing translations

### Translation Guidelines

- Use **clear, concise language**
- Maintain **consistent terminology**
- Consider **cultural context**
- Test with **native speakers** if possible

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest test_downloader.py

# Run with coverage
pytest --cov=youtube_downloader
```

### Writing Tests

- Write tests for **new features**
- Include **edge cases**
- Test **error conditions**
- Use **descriptive test names**

### Example Test

```python
def test_download_video_success():
    """Test successful video download."""
    downloader = YouTubeDownloader()
    result = downloader.download_video(
        "https://www.youtube.com/watch?v=test",
        "/tmp",
        "720p"
    )
    assert result is True
```

## 📚 Documentation

### Documentation Guidelines

- Write **clear, concise** documentation
- Include **examples** where helpful
- Keep documentation **up to date**
- Use **proper markdown** formatting

### Documentation Types

- **README.md**: Project overview and quick start
- **GUIDE.md**: User manual and tutorials
- **API Documentation**: Code documentation
- **Contributing Guide**: This file

## 🎯 Project Roadmap

### Current Priorities

1. **Bug fixes** and stability improvements
2. **Performance optimization**
3. **Additional language support**
4. **Enhanced UI/UX features**

### Future Features

- **Playlist download support**
- **Scheduled downloads**
- **Advanced search filters**
- **Mobile app version**
- **Cloud storage integration**

## 🤝 Community Guidelines

### Communication

- Be **respectful** and **inclusive**
- Use **clear, constructive** language
- **Listen** to others' perspectives
- **Help** newcomers

### Code Review

- **Review** others' code respectfully
- Provide **constructive feedback**
- Suggest **improvements** kindly
- **Appreciate** good contributions

## 📞 Getting Help

### Questions and Support

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: For private or sensitive matters

### Resources

- [Python Documentation](https://docs.python.org/)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp)

## 🙏 Recognition

Contributors will be recognized in:

- **README.md** contributors section
- **Release notes**
- **GitHub contributors** page
- **Project documentation**

---

**Thank you for contributing to Baresha Downloader! 🎬**

Your contributions help make this project better for everyone. 