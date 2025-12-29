#!/bin/bash
# Auto-format Python files after edits
# Hook: PostToolUse (Edit|Write)
# Purpose: Automatically run ruff format on Python files

file_path=$(jq -r '.tool_input.file_path // empty')

if [[ "$file_path" == *.py ]]; then
    ruff format "$file_path" 2>/dev/null
    echo "Formatted: $file_path"
fi
