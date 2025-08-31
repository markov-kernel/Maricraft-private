Of course. Here is the documentation for Claude Code Settings, rewritten and restructured to remove all non-content elements.

***

# Claude Code: Settings and Configuration

Claude Code offers a variety of settings to configure its behavior. You can manage these settings by running the `/config` command in the interactive REPL, by editing JSON files directly, or by using environment variables.

## Settings Files

Claude Code uses a hierarchical system of `settings.json` files for configuration.

*   **User settings**: Defined in `~/.claude/settings.json` and apply to all of your projects.
*   **Project settings**: Saved in your project's root directory.
    *   `.claude/settings.json`: For settings that are checked into source control and shared with your team.
    *   `.claude/settings.local.json`: For personal preferences and local overrides that are not checked into source control. Claude Code will automatically add this file to `.gitignore` when it's created.
*   **Enterprise managed policy settings**: For enterprise deployments, these settings take precedence over all others. System administrators can deploy policies to:
    *   **macOS**: `/Library/Application Support/ClaudeCode/managed-settings.json`
    *   **Linux/WSL**: `/etc/claude-code/managed-settings.json`
    *   **Windows**: `C:\ProgramData\ClaudeCode\managed-settings.json`

**Example `settings.json`:**

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test:*)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl:*)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  }
}
```

### Settings Precedence

Settings are applied in the following order of precedence, from highest to lowest:

1.  Enterprise policies
2.  Command-line arguments
3.  Local project settings (`.claude/settings.local.json`)
4.  Shared project settings (`.claude/settings.json`)
5.  User settings (`~/.claude/settings.json`)

### Available Settings

The `settings.json` file supports the following options:

| Key                         | Description                                                                                             | Example                                  |
| --------------------------- | ------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| `apiKeyHelper`              | A custom script to generate an auth value for model requests.                                           | `"/bin/generate_temp_api_key.sh"`        |
| `cleanupPeriodDays`         | How long to locally retain chat transcripts (default: 30).                                              | `20`                                     |
| `env`                       | Environment variables to apply to every session.                                                        | `{"FOO": "bar"}`                         |
| `hooks`                     | Configure custom commands to run at different points in the workflow. See the Hooks documentation.      | `{"PreToolUse": ...}`                    |
| `includeCoAuthoredBy`       | Whether to include the `co-authored-by Claude` byline in git commits (default: `true`).                 | `false`                                  |
| `model`                     | Override the default model used by Claude Code.                                                         | `"claude-3-5-sonnet-20241022"`           |
| `forceLoginMethod`          | Restrict login to `claudeai` (Claude.ai accounts) or `console` (Anthropic Console API billing).         | `"claudeai"`                             |
| `enableAllProjectMcpServers`| Automatically approve all MCP servers defined in project `.mcp.json` files.                             | `true`                                   |
| `enabledMcpjsonServers`     | A list of specific MCP servers from `.mcp.json` files to approve.                                       | `["memory", "github"]`                   |
| `disabledMcpjsonServers`    | A list of specific MCP servers from `.mcp.json` files to reject.                                        | `["filesystem"]`                         |
| `awsAuthRefresh`            | A custom script that modifies the `.aws` directory for advanced credential configuration.               | `"aws sso login --profile myprofile"`    |
| `awsCredentialExport`       | A custom script that outputs JSON with AWS credentials for advanced credential configuration.           | `"/bin/generate_aws_grant.sh"`           |

### Permission Settings

The `permissions` object within `settings.json` controls tool access.

| Key                          | Description                                                              | Example                   |
| ---------------------------- | ------------------------------------------------------------------------ | ------------------------- |
| `allow`                      | An array of permission rules to allow specific tool use.                 | `[ "Bash(git diff:*)" ]`  |
| `deny`                       | An array of permission rules to deny specific tool use.                  | `[ "WebFetch", "Bash(curl:*)" ]` |
| `additionalDirectories`      | Additional working directories that Claude has access to.                | `[ "../docs/" ]`          |
| `defaultMode`                | The default permission mode when starting Claude Code.                   | `"acceptEdits"`           |
| `disableBypassPermissionsMode` | Set to `"disable"` to prevent the `bypassPermissions` mode from being activated. | `"disable"`               |

## Sub Agent Configuration

Custom AI sub agents can be configured at both the user and project levels. They are stored as Markdown files with YAML frontmatter in the following locations:

*   **User sub agents**: `~/.claude/agents/` (available across all your projects)
*   **Project sub agents**: `.claude/agents/` (specific to your project and can be shared with your team)

## Environment Variables

Claude Code supports the following environment variables. These can also be set in the `env` object within `settings.json` to automatically apply them to each session.

| Variable                               | Purpose                                                                          |
| -------------------------------------- | -------------------------------------------------------------------------------- |
| `ANTHROPIC_API_KEY`                    | API key for authenticating with the Claude SDK.                                  |
| `ANTHROPIC_AUTH_TOKEN`                 | Custom value for the `Authorization: Bearer` header.                             |
| `ANTHROPIC_CUSTOM_HEADERS`             | Custom headers to add to requests (in `Name: Value` format).                     |
| `ANTHROPIC_MODEL`                      | Name of a custom model to use.                                                   |
| `ANTHROPIC_SMALL_FAST_MODEL`           | Name of a Haiku-class model for background tasks.                                |
| `AWS_BEARER_TOKEN_BEDROCK`             | Bedrock API key for authentication.                                              |
| `BASH_DEFAULT_TIMEOUT_MS`              | Default timeout for long-running bash commands.                                  |
| `BASH_MAX_TIMEOUT_MS`                  | Maximum timeout the model can set for long-running bash commands.                |
| `BASH_MAX_OUTPUT_LENGTH`               | Maximum number of characters in bash outputs before truncation.                  |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` | If set, returns to the original working directory after each Bash command.       |
| `CLAUDE_CODE_API_KEY_HELPER_TTL_MS`    | Credential refresh interval in milliseconds when using `apiKeyHelper`.           |
| `CLAUDE_CODE_USE_BEDROCK`              | Set to use Amazon Bedrock.                                                       |
| `CLAUDE_CODE_USE_VERTEX`               | Set to use Google Vertex AI.                                                     |
| `CLAUDE_CODE_SKIP_BEDROCK_AUTH`        | Skip AWS authentication for Bedrock (e.g., when using an LLM gateway).           |
| `CLAUDE_CODE_SKIP_VERTEX_AUTH`         | Skip Google authentication for Vertex (e.g., when using an LLM gateway).         |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | Disables autoupdater, bug command, error reporting, and telemetry.               |
| `DISABLE_AUTOUPDATER`                  | Set to `1` to disable automatic updates.                                         |
| `DISABLE_ERROR_REPORTING`              | Set to `1` to opt out of Sentry error reporting.                                 |
| `DISABLE_TELEMETRY`                    | Set to `1` to opt out of Statsig telemetry.                                      |
| `HTTP_PROXY` / `HTTPS_PROXY`           | Specify an HTTP or HTTPS proxy server for network connections.                   |

## Command-Line Configuration

You can manage your configuration from the command line. By default, these commands modify your project configuration (`.claude/settings.json`). Use the `--global` (or `-g`) flag to manage your user configuration (`~/.claude/settings.json`).

*   **List settings**: `claude config list`
*   **Get a setting**: `claude config get <key>`
*   **Set a setting**: `claude config set <key> <value>`
*   **Add to a list**: `claude config add <key> <value>`
*   **Remove from a list**: `claude config remove <key> <value>`

### Global Configuration

The following settings are typically managed globally:

| Key                     | Description                                                              | Options                                                              |
| ----------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| `autoUpdates`           | Enable or disable automatic background updates (default: `true`).        | `true`, `false`                                                      |
| `preferredNotifChannel` | Where to receive notifications (default: `iterm2`).                      | `iterm2`, `iterm2_with_bell`, `terminal_bell`, `notifications_disabled` |
| `theme`                 | The color theme for the interface.                                       | `dark`, `light`, `light-daltonized`, `dark-daltonized`                 |
| `verbose`               | Whether to show full bash and command outputs (default: `false`).        | `true`, `false`                                                      |

## Tools Available to Claude

Claude Code has access to a set of powerful tools to understand and modify your codebase. You can run custom commands before or after any tool executes using Claude Code hooks.

| Tool         | Description                                      | Permission Required |
| ------------ | ------------------------------------------------ | ------------------- |
| **Bash**     | Executes shell commands in your environment.     | Yes                 |
| **Edit**     | Makes targeted edits to specific files.          | Yes                 |
| **Glob**     | Finds files based on pattern matching.           | No                  |
| **Grep**     | Searches for patterns in file contents.          | No                  |
| **LS**       | Lists files and directories.                     | No                  |
| **MultiEdit**| Performs multiple edits on a single file atomically. | Yes                 |
| **NotebookEdit** | Modifies Jupyter notebook cells.                 | Yes                 |
| **NotebookRead** | Reads and displays Jupyter notebook contents.    | No                  |
| **Read**     | Reads the contents of files.                     | No                  |
| **Task**     | Runs a sub-agent to handle complex tasks.        | No                  |
| **TodoWrite**| Creates and manages structured task lists.       | No                  |
| **WebFetch** | Fetches content from a specified URL.            | Yes                 |
| **WebSearch**| Performs web searches with domain filtering.     | Yes                 |
| **Write**    | Creates or overwrites files.                     | Yes                 |