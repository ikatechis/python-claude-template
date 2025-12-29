# Python Project Justfile
# Install just: https://github.com/casey/just

# List available commands
default:
    @just --list

# Install dependencies
install:
    uv sync

# Run tests with coverage
test:
    uv run pytest

# Run tests in watch mode
test-watch:
    uv run pytest-watch

# Lint and format code
lint:
    uv run ruff check .
    uv run ruff format .
    uv run mypy src

# Fix linting issues automatically
fix:
    uv run ruff check --fix .
    uv run ruff format .

# Run pre-commit hooks
pre-commit:
    uv run pre-commit run --all-files

# Clean build artifacts and caches
clean:
    rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov
    rm -rf build dist *.egg-info
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete

# Run the application (customize src/main.py first)
run:
    uv run python src/main.py

# Run in debug mode
debug:
    DEBUG=1 uv run python src/main.py

# Add a new dependency
add package:
    uv add {{package}}

# Add a dev dependency
add-dev package:
    uv add --dev {{package}}

# Update dependencies
update:
    uv lock --upgrade

# Show dependency tree
tree:
    uv tree
