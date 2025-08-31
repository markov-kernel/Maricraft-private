# fastmcp.cli.cli
# fastmcp.cli.cli

> **Category:** fastmcp.cli.cli
> **Source:** gofastmcp.com_python-sdk_fastmcp-cli-cli.json

---

fastmcp.cli

cli

fastmcp.cli.cli

FastMCP CLI tools using Cyclopts.

## Functions

version

Copy

```
version()

```

Display version information and platform details.

dev

Copy

```
dev(server_spec: str) -> None

```

Run an MCP server with the MCP Inspector for development.**Args:**

- `server_spec`: Python file to run, optionally with :object suffix

run

Copy

```
run(server_spec: str) -> None

```

Run an MCP server or connect to a remote one.The server can be specified in four ways:

1. Module approach: “server.py” - runs the module directly, looking for an object named ‘mcp’, ‘server’, or ‘app’
2. Import approach: “server.py:app” - imports and runs the specified server object
3. URL approach: “ [http://server-url](http://server-url/)” \- connects to a remote server and creates a proxy
4. MCPConfig file: “mcp.json” - runs as a proxy server for the MCP Servers in the MCPConfig file

Server arguments can be passed after, :
fastmcp run server.py,,config config.json,debug**Args:**

- `server_spec`: Python file, object specification (file:obj), MCPConfig file, or URL

inspect

Copy

```
inspect(server_spec: str) -> None

```

Inspect an MCP server and generate a JSON report.This command analyzes an MCP server and generates a comprehensive JSON report
containing information about the server’s name, instructions, version, tools,
prompts, resources, templates, and capabilities.**Examples:**fastmcp inspect server.py
fastmcp inspect server.py -o report.json
fastmcp inspect server.py:mcp -o analysis.json
fastmcp inspect path/to/server.py:app -o /tmp/server-info.json**Args:**

- `server_spec`: Python file to inspect, optionally with :object suffix

[claude](https://gofastmcp.com/python-sdk/fastmcp-cli-claude) [\_\_init\_\_](https://gofastmcp.com/python-sdk/fastmcp-cli-install-__init__)