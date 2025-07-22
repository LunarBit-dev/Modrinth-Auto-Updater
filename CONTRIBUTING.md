# Contributing to Modrinth Modpack Updater

First off, thank you for considering contributing to Modrinth Modpack Updater! It's people like you that make this tool better for the entire Minecraft modding community.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct. Please be respectful and constructive in all interactions.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to see if the problem has already been reported. When you create a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed and what behavior you expected**
- **Include screenshots if applicable**
- **Include your environment details** (Python version, OS, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and explain the expected behavior**
- **Explain why this enhancement would be useful**

### Pull Requests

1. Fork the repository
2. Create a new branch from `main` for your feature or bugfix
3. Make your changes in your feature branch
4. Add or update tests as needed
5. Ensure your code follows the existing style conventions
6. Update documentation if necessary
7. Submit a pull request

#### Pull Request Guidelines

- **Keep your PR focused**: One feature or bugfix per PR
- **Write clear commit messages**: Use present tense ("Add feature" not "Added feature")
- **Include tests**: Add tests for new functionality
- **Update documentation**: Update README.md and other docs as needed
- **Follow coding standards**: Use type hints, proper error handling, and clear variable names

## Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/yourusername/Modrinth-Auto-Updater.git
cd Modrinth-Auto-Updater
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

## Coding Standards

### Python Style Guide

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write docstrings for all functions and classes
- Use meaningful variable and function names
- Keep functions focused and under 50 lines when possible

### Code Structure

- Keep the main script modular with separate functions for distinct operations
- Add proper error handling with informative error messages
- Use the existing color coding system for terminal output
- Follow the existing pattern for API calls and error handling

### Example Code Style

```python
def get_mod_info(project_slug: str) -> Dict[str, Any] | None:
    """
    Retrieve mod information from Modrinth API.
    
    Args:
        project_slug: The project slug from Modrinth
        
    Returns:
        Dict containing mod info, or None if not found
    """
    try:
        url = f"{MODRINTH_API}/project/{project_slug}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"{Colors.RED}Error fetching mod info: {e}{Colors.RESET}")
        return None
```

## Testing

Before submitting a pull request:

1. Test your changes with various modpack types (Fabric, Quilt, Forge)
2. Test both client and server .mrpack generation
3. Verify that existing functionality still works
4. Test error handling with invalid inputs

## Documentation

- Update README.md for new features or changed functionality
- Add examples to the examples/ directory if applicable
- Update CHANGELOG.md following the Keep a Changelog format
- Include docstrings for new functions

## Questions?

If you have questions about contributing, feel free to:
- Open an issue with the "question" label
- Start a discussion in GitHub Discussions
- Reach out in our Discord server

Thank you for contributing! 🎉
