# fastmcp.cli.install.claude_desktop
# fastmcp.cli.install.claude_desktop

> **Category:** fastmcp.cli.install.claude/desktop
> **Source:** gofastmcp.com_python-sdk_fastmcp-cli-install-claude_desktop.json

---

install

claude\_desktop

fastmcp.cli.install.claude_desktop

Claude Desktop integration for FastMCP install using Cyclopts.

## Functions

get_claude_config_path

Copy

```
get_claude_config_path() -> Path | None

```

Get the Claude config directory based on platform.

install_claude_desktop

Copy

```
install_claude_desktop(file: Path, server_object: str | None, name: str) -> bool

```

Install FastMCP server in Claude Desktop.**Args:**

- `file`: Path to the server file
- `server_object`: Optional server object name (for :object suffix)
- `name`: Name for the server in Claude’s config
- `with_editable`: Optional directory to install in editable mode
- `with_packages`: Optional list of additional packages to install
- `env_vars`: Optional dictionary of environment variables
- `python_version`: Optional Python version to use
- `with_requirements`: Optional requirements file to install from
- `project`: Optional project directory to run within

**Returns:**

- True if installation was successful, False otherwise

claude_desktop_command

Copy

```
claude_desktop_command(server_spec: str) -> None

```

Install an MCP server in Claude Desktop.**Args:**

- `server_spec`: Python file to install, optionally with :object suffix

[claude\_code](https://gofastmcp.com/python-sdk/fastmcp-cli-install-claude_code) [cursor](https://gofastmcp.com/python-sdk/fastmcp-cli-install-cursor)