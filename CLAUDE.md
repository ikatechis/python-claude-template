# Project Instructions for Claude

## Tech Stack

- **Python:** 3.12 (pyenv)
- **Package Manager:** uv
- **Testing:** pytest + coverage
- **Linting:** ruff, mypy

## Commands

```bash
uv sync                    # Install deps
uv run python src/main.py  # Run (normal)
DEBUG=1 uv run python ...  # Run (debug)
uv run pytest              # Test
uv run ruff check .        # Lint
uv run mypy src            # Type check
```

## Verification Protocol

**Before suggesting code:**
1. Search docs with ref.tools (`ref_search_documentation` + `ref_read_url`)
2. Verify function signatures and parameters
3. Check pyproject.toml for library versions
4. State confidence: VERIFIED, OBVIOUS, or UNCERTAIN

**Verify:** External library APIs, version-specific features, unfamiliar functions
**Skip:** Basic Python syntax, standard operators, already-verified APIs

## Token Efficiency Best Practices

**Use LSP for zero-token lookups:**
- ✅ `LSP goToDefinition` - Find function definitions without reading files
- ✅ `LSP findReferences` - Find all usages across codebase
- ✅ `LSP hover` - Get type hints and documentation
- ❌ Reading entire files just to find one function

**Batch operations in parallel:**
- ✅ Multiple reads in single message: `Read file1.py`, `Read file2.py`
- ❌ Sequential reads across multiple messages

**Smart search patterns:**
- ✅ Specific Glob patterns: `**/*config*.py`
- ✅ LSP for code navigation (zero file reads)
- ❌ Task tool for simple file searches
- ❌ Speculative reading of 5+ files

**When unsure:**
- ✅ Ask user for file paths
- ❌ Read multiple files hoping to find the right one

## Logging

```python
from logger import get_logger
logger = get_logger(__name__)

logger.debug("Detailed state")     # DEBUG=1 only
logger.info("Normal operation")    # File only
logger.warning("Recoverable error") # Console + file
logger.error("Critical", exc_info=True)  # Console + file
```

**Never suppress errors silently - always log them.**

## Development Workflow

1. Verify APIs with ref.tools
2. Write code
3. Test with `uv run pytest`
4. Commit with conventional format (feat:, fix:, docs:)

## Project-Specific Notes

<!-- CUSTOMIZE: Add your project-specific documentation here -->
