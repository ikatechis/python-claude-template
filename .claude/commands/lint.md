# Lint & Format

Run code quality checks with ruff and mypy.

## Purpose

Ensure code quality and type safety with automated linting and formatting.

## Usage

```
/lint
```

## What this command does

1. **Runs ruff linting** to catch code issues
2. **Runs ruff formatting** to fix style
3. **Runs mypy type checking** for type safety
4. **Shows clear error messages** with fixes

## Example Commands

### Linting
```bash
# Check for issues
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Check specific file
uv run ruff check src/models.py
```

### Formatting
```bash
# Check formatting
uv run ruff format --check .

# Auto-format all files
uv run ruff format .

# Format specific file
uv run ruff format src/models.py
```

### Type checking
```bash
# Run mypy on src/
uv run mypy src

# Check specific file
uv run mypy src/models.py

# Verbose output
uv run mypy --verbose src
```

### All at once (via justfile)
```bash
# Run all checks
just lint

# Auto-fix everything
just fix
```

## Best Practices

- ✅ Run before committing (or use pre-commit hooks)
- ✅ Fix issues immediately (don't accumulate debt)
- ✅ Use type hints for better mypy coverage
- ✅ Configure ruff rules in pyproject.toml
- ✅ Enable format-on-save in your editor
