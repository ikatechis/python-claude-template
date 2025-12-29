#!/bin/bash
# Session startup script
# Hook: SessionStart
# Purpose: Display project status and configure environment

echo "=== Python Project Session ==="
echo "Python: $(python --version 2>&1)"
echo "Working dir: $CLAUDE_PROJECT_DIR"

# Enable debug logging for development
if [ -n "$CLAUDE_ENV_FILE" ]; then
    echo 'export DEBUG=1' >> "$CLAUDE_ENV_FILE"
fi
