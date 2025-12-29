# Test Runner

Run Python tests with pytest and generate coverage reports.

## Purpose

Quickly run tests with proper configuration and coverage reporting.

## Usage

```
/test
```

## What this command does

1. **Runs pytest** with coverage tracking
2. **Shows test results** with clear pass/fail status
3. **Generates coverage report** (terminal + HTML)
4. **Highlights uncovered code** for improvement

## Example Commands

### Basic testing
```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_models.py

# Run tests matching pattern
uv run pytest -k "test_user"
```

### Coverage
```bash
# Run with coverage (configured in pyproject.toml)
uv run pytest

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Debug mode
```bash
# Run with debug logging
DEBUG=1 uv run pytest -s

# Stop on first failure
uv run pytest -x

# Run last failed tests
uv run pytest --lf
```

## Best Practices

- ✅ Write tests alongside new code
- ✅ Aim for 80%+ coverage
- ✅ Use parametrization for multiple cases
- ✅ Keep tests isolated and fast
- ✅ Mock external dependencies only
