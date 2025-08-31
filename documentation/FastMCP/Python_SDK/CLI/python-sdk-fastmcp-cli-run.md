# fastmcp.cli.run
# fastmcp.cli.run

> **Category:** fastmcp.cli.run
> **Source:** gofastmcp.com_python-sdk_fastmcp-cli-run.json

---

fastmcp.cli

run

fastmcp.cli.run

FastMCP run command implementation with enhanced type hints.

## Functions

is_url

Copy

```
is_url(path: str) -> bool

```

Check if a string is a URL.

parse_file_path

Copy

```
parse_file_path(server_spec: str) -> tuple[Path, str | None]

```

Parse a file path that may include a server object specification.**Args:**

- `server_spec`: Path to file, optionally with :object suffix

**Returns:**

- Tuple of (file\_path, server\_object)

import_server

Copy

```
import_server(file: Path, server_object: str | None = None) -> Any

```

Import a MCP server from a file.**Args:**

- `file`: Path to the file
- `server_object`: Optional object name in format “module:object” or just “object”

**Returns:**

- The server object

run_with_uv

Copy

```
run_with_uv(server_spec: str, python_version: str | None = None, with_packages: list[str] | None = None, with_requirements: Path | None = None, project: Path | None = None, transport: TransportType | None = None, host: str | None = None, port: int | None = None, path: str | None = None, log_level: LogLevelType | None = None, show_banner: bool = True) -> None

```

Run a MCP server using uv run subprocess.**Args:**

- `server_spec`: Python file, object specification (file:obj), or URL
- `python_version`: Python version to use (e.g. “3.10”)
- `with_packages`: Additional packages to install
- `with_requirements`: Requirements file to use
- `project`: Run the command within the given project directory
- `transport`: Transport protocol to use
- `host`: Host to bind to when using http transport
- `port`: Port to bind to when using http transport
- `path`: Path to bind to when using http transport
- `log_level`: Log level
- `show_banner`: Whether to show the server banner

create_client_server

Copy

```
create_client_server(url: str) -> Any

```

Create a FastMCP server from a client URL.**Args:**

- `url`: The URL to connect to

**Returns:**

- A FastMCP server instance

create_mcp_config_server

Copy

```
create_mcp_config_server(mcp_config_path: Path) -> FastMCP[None]

```

Create a FastMCP server from a MCPConfig.

import_server_with_args

Copy

```
import_server_with_args(file: Path, server_object: str | None = None, server_args: list[str] | None = None) -> Any

```

Import a server with optional command line arguments.**Args:**

- `file`: Path to the server file
- `server_object`: Optional server object name
- `server_args`: Optional command line arguments to inject

**Returns:**

- The imported server object

run_command

Copy

```
run_command(server_spec: str, transport: TransportType | None = None, host: str | None = None, port: int | None = None, path: str | None = None, log_level: LogLevelType | None = None, server_args: list[str] | None = None, show_banner: bool = True, use_direct_import: bool = False) -> None

```

Run a MCP server or connect to a remote one.**Args:**

- `server_spec`: Python file, object specification (file:obj), MCPConfig file, or URL
- `transport`: Transport protocol to use
- `host`: Host to bind to when using http transport
- `port`: Port to bind to when using http transport
- `path`: Path to bind to when using http transport
- `log_level`: Log level
- `server_args`: Additional arguments to pass to the server
- `show_banner`: Whether to show the server banner
- `use_direct_import`: Whether to use direct import instead of subprocess

[shared](https://gofastmcp.com/python-sdk/fastmcp-cli-install-shared) [\_\_init\_\_](https://gofastmcp.com/python-sdk/fastmcp-client-__init__)