Of course. Here is the documentation for the Model Context Protocol (MCP), rewritten and restructured to remove all non-content elements.

***

# Claude Code: Model Context Protocol (MCP)

Model Context Protocol (MCP) is an open protocol that enables LLMs to access external tools and data sources. Claude Code can act as an MCP client, connecting to specialized servers to extend its capabilities.

**Security Warning**: Use third-party MCP servers at your own risk. Ensure you trust the servers you connect to, especially those that access the internet, as they can expose you to risks like prompt injection.

## Configuring and Managing MCP Servers

You can add, list, and remove MCP servers from the command line.

### Adding Servers

Claude Code supports three types of server transports: stdio, Server-Sent Events (SSE), and HTTP.

**1. Add a Stdio Server (for local commands)**

```bash
# Syntax
claude mcp add <name> <command> [args...]

# Example with environment variables
claude mcp add my-server -e API_KEY=123 -- /path/to/server arg1 arg2
```

**2. Add an SSE Server**

```bash
# Syntax
claude mcp add --transport sse <name> <url>

# Example with custom headers
claude mcp add --transport sse api-server https://api.example.com/mcp --header "X-API-Key: your-key"
```

**3. Add an HTTP Server**

```bash
# Syntax
claude mcp add --transport http <name> <url>

# Example with an authentication header
claude mcp add --transport http secure-server https://api.example.com/mcp --header "Authorization: Bearer your-token"
```

**Windows Users**: When adding local MCP servers that use `npx`, you must use the `cmd /c` wrapper to ensure proper execution.

```bash
claude mcp add my-server -- cmd /c npx -y @some/package
```

### Managing Servers

```bash
# List all configured servers
claude mcp list

# Get details for a specific server
claude mcp get my-server

# Remove a server
claude mcp remove my-server
```

You can also check the status of your MCP servers at any time from within the Claude Code REPL by running the `/mcp` command.

## Understanding MCP Server Scopes

MCP servers can be configured at three different scope levels, which determine their availability and how they are stored. When servers with the same name exist at multiple scopes, the order of precedence is: **local**, then **project**, then **user**.

*   **Local Scope (`-s local`)**: This is the default scope. The server configuration is stored in your project-specific user settings and is private to you. It is ideal for experimental servers or those with sensitive credentials.
*   **Project Scope (`-s project`)**: The configuration is stored in a `.mcp.json` file in your project's root directory. This file is meant to be checked into version control, allowing you to share servers with your team. For security, Claude Code will prompt for approval before using servers from a project's `.mcp.json` file.
*   **User Scope (`-s user`)**: The configuration is stored globally for your user account, making the server available across all of your projects. This is useful for personal utility servers that you use frequently.

### Environment Variable Expansion in `.mcp.json`

Claude Code supports environment variable expansion in `.mcp.json` files, allowing for flexible, shareable configurations.

*   **Syntax**: `${VAR}` or `${VAR:-default}`
*   **Supported Locations**: `command`, `args`, `env`, `url`, and `headers`.

**Example `.mcp.json`:**

```json
{
  "mcpServers": {
    "api-server": {
      "type": "sse",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

If a required environment variable is not set and has no default, Claude Code will fail to parse the configuration.

## Usage and Examples

### Authenticate with Remote MCP Servers

Many remote servers require authentication. Claude Code supports the OAuth 2.0 flow.

1.  Add the remote server as you would any other SSE or HTTP server.
2.  Inside the Claude Code REPL, run the `/mcp` command.
3.  This opens an interactive menu where you can select a server and choose "Authenticate".
4.  Your browser will open to the OAuth provider. Complete the authentication, and Claude Code will securely store the token.

### Connect to a Postgres MCP Server

You can give Claude read-only access to a PostgreSQL database for querying and schema inspection.

1.  **Add the server**:
    ```bash
    claude mcp add postgres-server /path/to/postgres-mcp-server --connection-string "postgresql://user:pass@localhost:5432/mydb"
    ```
2.  **Query your database**:
    ```
    > describe the schema of our users table
    > what are the most recent orders in the system?
    ```

### Add MCP Servers from a JSON String

You can add a server directly from a JSON configuration string.

```bash
# Syntax
claude mcp add-json <name> '<json>'

# Example
claude mcp add-json weather-api '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"]}'
```

### Import MCP Servers from Claude Desktop

If you have servers configured in Claude Desktop, you can import them directly. This feature is supported on macOS and Windows Subsystem for Linux (WSL).

1.  Run the import command:
    ```bash
    claude mcp add-from-claude-desktop
    ```
2.  An interactive dialog will appear, allowing you to select which servers to import.

### Use Claude Code as an MCP Server

You can expose Claude Code's own tools (like `Read`, `Edit`, `Bash`, etc.) to other MCP clients, such as Claude Desktop.

1.  Start the server:
    ```bash
    claude mcp serve
    ```
2.  Connect from your MCP client. The client is responsible for implementing user confirmation for any tool calls.

## Interacting with MCP Servers

Once connected, you can interact with MCP servers in two main ways: referencing resources and using slash commands.

### Using MCP Resources (`@` mentions)

MCP servers can expose resources (like GitHub issues or documentation files) that you can reference in your prompts.

1.  **Discover resources**: Type `@` in your prompt to see an autocomplete menu of available resources from all connected servers.
2.  **Reference a resource**: Use the format `@server:protocol://resource/path`.
    ```
    > Can you analyze @github:issue://123 and suggest a fix?
    > Compare @postgres:schema://users with @docs:file://database/user-model
    ```
    The referenced resources are automatically fetched and included as context for your prompt.

### Using MCP Prompts as Slash Commands (`/`)

MCP servers can also expose prompts that become available as slash commands.

1.  **Discover commands**: Type `/` to see all available commands, including those from MCP servers, which will appear with the format `/mcp__servername__promptname`.
2.  **Execute a command**:
    ```
    > /mcp__github__list_prs
    > /mcp__jira__create_issue "Bug in login flow" high
    ```
    The results of the prompt are injected directly into the conversation.