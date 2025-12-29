#!/bin/bash
# Log Bash commands to file
# Hook: PreToolUse (Bash)
# Purpose: Create audit trail of all commands executed

mkdir -p "$CLAUDE_PROJECT_DIR/logs" && jq -r '"[\(.session_id[0:8])] \(.tool_input.command)"' >> "$CLAUDE_PROJECT_DIR/logs/claude-commands.log"
