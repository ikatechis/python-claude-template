# Dependency Management

Manage Python dependencies with uv.

## Purpose

Add, remove, and update project dependencies efficiently with uv.

## Usage

```
/deps
```

## What this command does

1. **Manages dependencies** in pyproject.toml
2. **Updates lockfile** for reproducibility
3. **Syncs virtual environment** with changes
4. **Shows dependency tree** for debugging

## Example Commands

### Adding dependencies
```bash
# Add runtime dependency
uv add requests

# Add multiple dependencies
uv add fastapi uvicorn pydantic

# Add specific version
uv add "django>=4.2,<5.0"

# Add dev dependency
uv add --dev pytest-mock

# Add from git
uv add git+https://github.com/user/repo.git
```

### Removing dependencies
```bash
# Remove dependency
uv remove requests

# Remove dev dependency
uv remove --dev pytest-mock
```

### Updating dependencies
```bash
# Update all dependencies
uv lock --upgrade

# Update specific package
uv lock --upgrade-package requests

# Sync environment after update
uv sync
```

### Inspecting dependencies
```bash
# Show dependency tree
uv tree

# Show outdated packages
uv pip list --outdated

# Show installed packages
uv pip list
```

### Installing from lockfile
```bash
# Install all dependencies (respects uv.lock)
uv sync

# Install without dev dependencies
uv sync --no-dev

# Install with all extras
uv sync --all-extras
```

## Best Practices

- ✅ Commit `uv.lock` for reproducible builds
- ✅ Use version constraints (`>=`, `<`, `~=`)
- ✅ Separate runtime and dev dependencies
- ✅ Run `uv sync` after pulling changes
- ✅ Update regularly but test thoroughly
- ✅ Check `uv tree` for conflicts

## Quick Reference

| Task | Command |
|------|---------|
| Add package | `uv add <package>` |
| Add dev package | `uv add --dev <package>` |
| Remove package | `uv remove <package>` |
| Update all | `uv lock --upgrade` |
| Sync environment | `uv sync` |
| Show tree | `uv tree` |
