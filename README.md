# Python Project Template

A modern Python project template with Claude Code best practices, automated tooling, and CI/CD.

## Features

- **Python 3.12** with pyenv
- **uv** package manager (fast, modern)
- **ruff** linting and formatting
- **mypy** type checking
- **pytest** with coverage
- **pre-commit** hooks
- **GitHub Actions** CI/CD (lint, type-check, test)
- **Gemini Code Review** for PRs
- **Claude Code** hooks and automation
- **MCP servers**: GitHub + ref.tools

## Quick Start

```bash
# Prerequisites: Python 3.12 (via pyenv) + uv package manager

# Clone and setup
git clone <repo-url>
cd <project-name>
uv sync

# Run (customize src/main.py first)
uv run python src/main.py

# Run with debug logging
DEBUG=1 uv run python src/main.py
```

## Development

### Commands

```bash
# Run tests
uv run pytest

# Code quality
uv run ruff check src/
uv run ruff format src/
uv run mypy src/

# Pre-commit hooks
pre-commit install
pre-commit run --all-files
```

### Project Structure

```
project/
├── .claude/           # Claude Code configuration
│   ├── hooks/         # Auto-format, command logging, session start
│   └── skills/        # Python testing skill
├── .gemini/           # Gemini code review settings
├── .github/           # CI/CD workflows
│   └── workflows/
│       └── ci.yml     # Automated testing and checks
├── src/               # Source code
│   ├── logger.py      # Logging configuration
│   └── config.py      # Configuration classes
├── tests/             # Test files
│   └── conftest.py    # Shared fixtures
├── logs/              # Log files (git-ignored)
└── pyproject.toml     # Project configuration
```

## Customization

After cloning, customize these files:

1. **pyproject.toml** - Project name, description, dependencies
2. **src/config.py** - Application-specific settings
3. **tests/conftest.py** - Project-specific fixtures
4. **CLAUDE.md** - Project-specific notes section
5. **README.md** - This file

## License

[Choose your license]
