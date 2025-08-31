Of course. Here is the documentation rewritten and restructured, with all HTML elements, navigation, and other non-content "slop" removed.

***

# Claude Code Hooks

## Hook Events Overview

Claude Code provides several hook events that run at different points in the workflow. Each event receives different data and can control Claude’s behavior in different ways.

*   **PreToolUse**: Runs before tool calls and can block them.
*   **PostToolUse**: Runs after tool calls complete.
*   **Notification**: Runs when Claude Code sends notifications.
*   **UserPromptSubmit**: Runs when a user submits a prompt, before Claude processes it.
*   **Stop**: Runs when the main Claude Code agent has finished responding.
*   **SubagentStop**: Runs when a Claude Code sub-agent task has finished responding.
*   **PreCompact**: Runs before Claude Code is about to run a context compacting operation.

## Quickstart: Log Shell Commands

In this quickstart, you’ll add a hook that logs the shell commands that Claude Code runs.

### Prerequisites

Install `jq` for JSON processing in the command line.

### Step 1: Open Hooks Configuration

Run the `/hooks` slash command and select the `PreToolUse` hook event. `PreToolUse` hooks run before tool calls and can block them while providing Claude feedback on what to do differently.

### Step 2: Add a Matcher

Select `+ Add new matcher…` to run your hook only on Bash tool calls. Type `Bash` for the matcher. You can also use `*` to match all tools.

### Step 3: Add the Hook

Select `+ Add new hook…` and enter this command:

```bash
jq -r '"\(.tool_input.command) - \(.tool_input.description // "No description")"' >> ~/.claude/bash-command-log.txt
```

### Step 4: Save Your Configuration

For storage location, select `User settings` since you’re logging to your home directory. This hook will then apply to all projects, not just your current project. Then press Esc until you return to the REPL. Your hook is now registered.

### Step 5: Verify Your Hook

Run `/hooks` again or check `~/.claude/settings.json` to see your configuration:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"\\(.tool_input.command) - \\(.tool_input.description // \"No description\")\"' >> ~/.claude/bash-command-log.txt"
          }
        ]
      }
    ]
  }
}
```

### Step 6: Test Your Hook

Ask Claude to run a simple command like `ls` and then check your log file:

```bash
cat ~/.claude/bash-command-log.txt
```

You should see an entry like:
`ls - Lists files and directories`

## Configuration

Claude Code hooks are configured in your settings files:

*   `~/.claude/settings.json` - User settings
*   `.claude/settings.json` - Project settings
*   `.claude/settings.local.json` - Local project settings (not committed to version control)
*   Enterprise managed policy settings

### Structure

Hooks are organized by event, then by matchers. Each matcher can have multiple hook commands.

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

*   **matcher**: A case-sensitive pattern to match tool names. This is only applicable for `PreToolUse` and `PostToolUse`.
    *   Simple strings match exactly: `Write` matches only the Write tool.
    *   Regex is supported: `Edit|Write` or `Notebook.*`.
    *   Use `*`, an empty string (`""`), or leave the field blank to match all tools.
*   **hooks**: An array of commands to execute when the pattern matches.
    *   **type**: Currently, only `"command"` is supported.
    *   **command**: The bash command to execute.
    *   **timeout**: (Optional) How long a command should run, in seconds, before being canceled. The default is 60 seconds.

For events that don’t use tool matchers (like `UserPromptSubmit`, `Notification`, `Stop`, and `SubagentStop`), you can omit the `matcher` field entirely.

### Project-Specific Hook Scripts

You can use the `CLAUDE_PROJECT_DIR` environment variable to reference scripts stored in your project. This ensures they work regardless of Claude’s current working directory. This variable is only available when Claude Code spawns the hook command.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/check-style.sh"
          }
        ]
      }
    ]
  }
}
```

## Hook Events and Input Data

Hooks receive JSON data via stdin containing session information and event-specific data.

**Common Fields in all Hook Inputs:**

```typescript
{
  session_id: string,
  transcript_path: string, // Path to the conversation JSON
  cwd: string,             // The current working directory when the hook is invoked
  hook_event_name: string,
  ... // Event-specific fields below
}
```

### PreToolUse

Runs after Claude creates tool parameters but before the tool call is processed.

**Common Matchers:** `Task`, `Bash`, `Glob`, `Grep`, `Read`, `Edit`, `MultiEdit`, `Write`, `WebFetch`, `WebSearch`.

**Input Example:**

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/path/to/project",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  }
}
```

### PostToolUse

Runs immediately after a tool completes successfully. It recognizes the same matchers as `PreToolUse`.

**Input Example:**

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/path/to/project",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  }
}
```

### Notification

Runs when Claude Code sends a notification, such as when it needs permission to use a tool or has been idle for at least 60 seconds.

**Input Example:**

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/path/to/project",
  "hook_event_name": "Notification",
  "message": "Claude needs your permission to use Bash"
}
```

### UserPromptSubmit

Runs when the user submits a prompt, before Claude processes it. This allows you to validate prompts or add additional context.

**Input Example:**

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/path/to/project",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate the factorial of a number"
}
```

### Stop and SubagentStop

`Stop` runs when the main agent finishes responding. `SubagentStop` runs when a sub-agent (Task tool call) finishes. Neither runs if the stoppage was due to a user interrupt.

**Input Example:**

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "hook_event_name": "Stop",
  "stop_hook_active": true
}
```
*`stop_hook_active` is true if Claude is already continuing as a result of a previous stop hook. Check this value to prevent infinite loops.*

### PreCompact

Runs before Claude Code performs a compact operation on the conversation history.

**Matchers:**
*   `manual`: Invoked from the `/compact` command.
*   `auto`: Invoked automatically when the context window is full.

**Input Example:**

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": ""
}
```
*For `manual` triggers, `custom_instructions` comes from the user's input to `/compact`. For `auto` triggers, it is empty.*

## Hook Output and Control Flow

Hooks can return output to Claude Code via exit codes or structured JSON to communicate status, block actions, and provide feedback.

### Simple Control: Exit Codes

*   **Exit code 0 (Success)**: The hook ran successfully. For most hooks, `stdout` is shown to the user in transcript mode (CTRL-R). For `UserPromptSubmit`, `stdout` is added to the context for Claude to see.
*   **Exit code 2 (Blocking Error)**: The hook signals a blocking error. `stderr` is fed back to Claude to process automatically. The exact behavior depends on the event (see table below).
*   **Other exit codes (Non-blocking Error)**: The hook failed, but execution continues. `stderr` is shown to the user.

**Behavior for Exit Code 2:**

| Hook Event         | Behavior                                                     |
| ------------------ | ------------------------------------------------------------ |
| `PreToolUse`       | Blocks the tool call, shows `stderr` to Claude.              |
| `PostToolUse`      | Shows `stderr` to Claude (tool has already run).             |
| `UserPromptSubmit` | Blocks prompt processing, erases the prompt, shows `stderr` to the user only. |
| `Stop` / `SubagentStop` | Blocks the agent from stopping, shows `stderr` to Claude.    |
| `Notification` / `PreCompact` | N/A, shows `stderr` to the user only.                        |

### Advanced Control: JSON Output

For more sophisticated control, hooks can return a structured JSON object in `stdout`.

**Common JSON Fields (All Hook Types):**

```json
{
  "continue": true,
  "stopReason": "Message shown to user when continue is false",
  "suppressOutput": true
}
```
*   `continue` (boolean, optional): Whether Claude should continue after the hook. If `false`, Claude stops processing. Defaults to `true`. This takes precedence over any `decision` field.
*   `stopReason` (string, optional): A message shown to the user when `continue` is `false`.
*   `suppressOutput` (boolean, optional): If `true`, hides the hook's `stdout` from the transcript mode. Defaults to `false`.

**Event-Specific JSON Control:**

*   **`PreToolUse` Decision Control**
    *   `"permissionDecision": "allow"`: Bypasses the permission system and runs the tool.
    *   `"permissionDecision": "deny"`: Prevents the tool call. The `permissionDecisionReason` is shown to Claude.
    *   `"permissionDecision": "ask"`: Asks the user for confirmation in the UI.

    ```json
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow" | "deny" | "ask",
        "permissionDecisionReason": "My reason here"
      }
    }
    ```

*   **`PostToolUse` Decision Control**
    *   `"decision": "block"`: Automatically prompts Claude with the content of the `reason` field.

    ```json
    {
      "decision": "block",
      "reason": "Explanation for Claude"
    }
    ```

*   **`UserPromptSubmit` Decision Control**
    *   `"decision": "block"`: Prevents the prompt from being processed and erases it. The `reason` is shown to the user.
    *   `"hookSpecificOutput.additionalContext"`: A string to add to the context for Claude to see.

    ```json

    {
      "decision": "block",
      "reason": "Explanation for user",
      "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": "My additional context for Claude"
      }
    }
    ```

*   **`Stop` / `SubagentStop` Decision Control**
    *   `"decision": "block"`: Prevents Claude from stopping. You **must** provide a `reason` for Claude to know how to proceed.

    ```json
    {
      "decision": "block",
      "reason": "Must be provided when Claude is blocked from stopping"
    }
    ```

## Examples

### Code Formatting Hook

Automatically format TypeScript files with Prettier after they are edited.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | { read file_path; if echo \"$file_path\" | grep -q '\\.ts$'; then npx prettier --write \"$file_path\"; fi; }"
          }
        ]
      }
    ]
  }
}
```

### Custom Notification Hook

Get desktop notifications when Claude needs input. This example uses `notify-send`, common on Linux systems.

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Awaiting your input'"
          }
        ]
      }
    ]
  }
}
```

### File Protection Hook

Block edits to sensitive files like `.env` or `package-lock.json` using a `PreToolUse` hook and a Python script.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c \"import json, sys; data=json.load(sys.stdin); path=data.get('tool_input',{}).get('file_path',''); sys.exit(2 if any(p in path for p in ['.env', 'package-lock.json', '.git/']) else 0)\""
          }
        ]
      }
    ]
  }
}
```

### Script Example: Bash Command Validation (Exit Code)

This Python script for a `PreToolUse` hook checks for suboptimal shell commands and uses exit code 2 to block them and provide feedback to Claude.

```python
#!/usr/bin/env python3
import json
import re
import sys

VALIDATION_RULES = [
    (r"\bgrep\b(?!.*\|)", "Use 'rg' (ripgrep) instead of 'grep' for better performance."),
    (r"\bfind\s+\S+\s+-name\b", "Use 'rg --files | rg pattern' instead of 'find -name'."),
]

def validate_command(command: str) -> list[str]:
    issues = []
    for pattern, message in VALIDATION_RULES:
        if re.search(pattern, command):
            issues.append(message)
    return issues

input_data = json.load(sys.stdin)
tool_name = input_data.get("tool_name", "")
command = input_data.get("tool_input", {}).get("command", "")

if tool_name != "Bash" or not command:
    sys.exit(1)

issues = validate_command(command)
if issues:
    for message in issues:
        print(f"• {message}", file=sys.stderr)
    # Exit code 2 blocks the tool call and shows stderr to Claude
    sys.exit(2)
```

### Script Example: Add Context and Validation (JSON Output)

This `UserPromptSubmit` hook script checks for potential secrets and blocks the prompt if found. Otherwise, it adds the current time to the context for Claude.

```python
#!/usr/bin/env python3
import json
import sys
import re
import datetime

input_data = json.load(sys.stdin)
prompt = input_data.get("prompt", "")

# Check for sensitive patterns
if re.search(r"(?i)\b(password|secret|key|token)\s*[:=]", prompt):
    output = {
        "decision": "block",
        "reason": "Security policy violation: Prompt contains potential secrets. Please rephrase."
    }
    print(json.dumps(output))
    sys.exit(0)

# Add current time to context and allow the prompt to proceed
context = f"Current time: {datetime.datetime.now()}"
print(context)
sys.exit(0)
```

## Working with MCP Tools

Claude Code hooks work seamlessly with Model Context Protocol (MCP) tools.

### MCP Tool Naming

MCP tools follow the pattern `mcp__<server>__<tool>`.

*   `mcp__memory__create_entities`
*   `mcp__filesystem__read_file`
*   `mcp__github__search_repositories`

### Configuring Hooks for MCP Tools

You can use regex in your matcher to target specific MCP tools or entire MCP servers.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation initiated' >> ~/mcp-operations.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

## Security Considerations

### Disclaimer

**USE AT YOUR OWN RISK**: Claude Code hooks execute arbitrary shell commands on your system automatically. By using hooks, you acknowledge that you are solely responsible for the commands you configure. Hooks can modify, delete, or access any files your user account can access. Malicious or poorly written hooks can cause data loss or system damage. Anthropic provides no warranty and assumes no liability for any damages resulting from hook usage. Always review and understand any hook commands before adding them, and test them in a safe environment.

### Security Best Practices

1.  **Validate and sanitize inputs**: Never trust input data from Claude blindly.
2.  **Always quote shell variables**: Use `"$VAR"` not `$VAR` to prevent word splitting and globbing.
3.  **Block path traversal**: Check for `..` in file paths to prevent access to unintended directories.
4.  **Use absolute paths**: Specify full paths for scripts, using `$CLAUDE_PROJECT_DIR` for project-relative scripts.
5.  **Skip sensitive files**: Add checks to avoid operating on files like `.env`, `.git/`, or private keys.

### Configuration Safety

Direct edits to hook settings files do not take effect immediately in a running session. Claude Code captures a snapshot of hooks at startup and uses it for the duration of the session. If the settings files are modified externally, Claude will warn you and require you to review the changes in the `/hooks` menu before they are applied. This prevents malicious hook modifications from affecting your current session without your knowledge.

## Hook Execution Details

*   **Timeout**: Hooks have a 60-second execution limit by default, which is configurable per command in the settings JSON. A timeout for one command does not affect other commands.
*   **Parallelization**: All hooks that match a given event run in parallel.
*   **Environment**: Hooks run in Claude Code’s current working directory and inherit its environment. The `CLAUDE_PROJECT_DIR` environment variable is also available.
*   **Input/Output**: Hooks receive JSON via `stdin`. Progress and output are shown in the transcript view (Ctrl-R), except for `Notification` hooks, which are only logged when running with the `--debug` flag.

## Debugging

### Basic Troubleshooting

1.  **Check Configuration**: Run `/hooks` to see if your hook is registered correctly.
2.  **Verify Syntax**: Ensure your `settings.json` is valid JSON. Pay special attention to escaping quotes (`\"`) inside command strings.
3.  **Test Commands**: Run your hook's command manually in your terminal to see if it works as expected.
4.  **Check Permissions**: Make sure any script files are executable (`chmod +x your_script.sh`).
5.  **Review Logs**: Run Claude with the `--debug` flag (`claude --debug`) to see detailed hook execution logs.

### Advanced Debugging

*   **Inspect Execution**: The `--debug` flag provides detailed logs about which matchers are running, what commands are executed, their exit status, and their output.
*   **Validate Schemas**: Test your hook scripts with sample JSON input that mimics what Claude Code sends to ensure it handles the data correctly.
*   **Use Structured Logging**: Implement logging within your hook scripts to write to a separate log file for easier debugging of complex logic.

### Debug Output Example

Using `claude --debug` will show logs like this in your terminal:

```
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Getting matching hook commands for PostToolUse with query: Write
[DEBUG] Found 1 hook matchers in settings
[DEBUG] Matched 1 hooks for query "Write"
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: <Your command> with timeout 60000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```