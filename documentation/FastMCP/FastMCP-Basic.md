# FastMCP Basic Guide

A comprehensive guide to building MCP servers with FastMCP. This guide combines essential documentation in logical learning order.

## Table of Contents

1. [What is FastMCP?](#what-is-fastmcp?)
2. [Installation & Setup](#installation-and-setup)
3. [Your First Server](#your-first-server)
4. [FastMCP Server API Reference](#fastmcp-server-api-reference)
5. [Using Decorators (@tool, @resource)](#using-decorators-tool-resource)
6. [Server Tools](#server-tools)
7. [Server Resources](#server-resources)
8. [Server Prompts](#server-prompts)
9. [Tools API Reference](#tools-api-reference)
10. [Resources API Reference](#resources-api-reference)
11. [Prompts API Reference](#prompts-api-reference)
12. [Server Context](#server-context)
13. [Context API Reference](#context-api-reference)
14. [Testing Your Server](#testing-your-server)
15. [Running & Deploying Servers](#running-and-deploying-servers)

---

================================================================================
# 1. What is FastMCP?
================================================================================

# Getting Started Welcome

> **Category:** Getting Started
> **Source:** gofastmcp.com_getting-started_welcome.json

---

Welcome to FastMCP 2.0!

The [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) is a new, standardized way to provide context and tools to your LLMs, and FastMCP makes building MCP servers and clients simple and intuitive. Create tools, expose resources, define prompts, and more with clean, Pythonic code:


```
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
"""Add two numbers"""
return a + b

if __name__ == "__main__":
mcp.run()

```

## Beyond the Protocol

FastMCP is the standard framework for working with the Model Context Protocol. FastMCP 1.0 was incorporated into the [official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) in 2024.This is FastMCP 2.0, the **actively maintained version** that provides a complete toolkit for working with the MCP ecosystem.FastMCP 2.0 has a comprehensive set of features that go far beyond the core MCP specification, all in service of providing **the simplest path to production**. These include deployment, auth, clients, server proxying and composition, generating servers from REST APIs, dynamic tool rewriting, built-in testing tools, integrations, and more.Ready to upgrade or get started? Follow the [installation instructions](https://gofastmcp.com/getting-started/installation), which include steps for upgrading from the official MCP SDK.

## What is MCP?

The Model Context Protocol lets you build servers that expose data and functionality to LLM applications in a secure, standardized way. It is often described as “the USB-C port for AI”, providing a uniform way to connect LLMs to resources they can use. It may be easier to think of it as an API, but specifically designed for LLM interactions. MCP servers can:

- Expose data through `Resources` (think of these sort of like GET endpoints; they are used to load information into the LLM’s context)
- Provide functionality through `Tools` (sort of like POST endpoints; they are used to execute code or otherwise produce a side effect)
- Define interaction patterns through `Prompts` (reusable templates for LLM interactions)
- And more!

FastMCP provides a high-level, Pythonic interface for building, managing, and interacting with these servers.

## Why FastMCP?

The MCP protocol is powerful but implementing it involves a lot of boilerplate - server setup, protocol handlers, content types, error management. FastMCP handles all the complex protocol details and server management, so you can focus on building great tools. It’s designed to be high-level and Pythonic; in most cases, decorating a function is all you need.FastMCP 2.0 has evolved into a comprehensive platform that goes far beyond basic protocol implementation. While 1.0 provided server-building capabilities (and is now part of the official MCP SDK), 2.0 offers a complete ecosystem including client libraries, authentication systems, deployment tools, integrations with major AI platforms, testing frameworks, and production-ready infrastructure patterns.FastMCP aims to be:🚀 **Fast**: High-level interface means less code and faster development🍀 **Simple**: Build MCP servers with minimal boilerplate🐍 **Pythonic**: Feels natural to Python developers🔍 **Complete**: A comprehensive platform for all MCP use cases, from dev to prodFastMCP is made with 💙 by [Prefect](https://www.prefect.io/).

## LLM-Friendly Docs

This documentation is also available in [llms.txt format](https://llmstxt.org/), which is a simple markdown standard that LLMs can consume easily.There are two ways to access the LLM-friendly documentation:

- [llms.txt](https://gofastmcp.com/llms.txt) is essentially a sitemap, listing all the pages in the documentation.
- [llms-full.txt](https://gofastmcp.com/llms-full.txt) contains the entire documentation. Note this may exceed the context window of your LLM.

In addition, any page can be accessed as markdown by appending `.md` to the URL. For example, this page would become `https://gofastmcp.com/getting-started/welcome.md`, which you can view [here](https://gofastmcp.com/getting-started/welcome.md).Finally, you can copy the contents of any page as markdown by pressing “Cmd+C” (or “Ctrl+C” on Windows) on your keyboard.

[Installation](https://gofastmcp.com/getting-started/installation)


================================================================================
# 2. Installation & Setup
================================================================================

# Before

> **Category:** Getting Started
> **Source:** gofastmcp.com_getting-started_installation.json

---

### Installation

## Install FastMCP

We recommend using [uv](https://docs.astral.sh/uv/getting-started/installation/) to install and manage FastMCP.If you plan to use FastMCP in your project, you can add it as a dependency with:


```
uv add fastmcp

```

Alternatively, you can install it directly with `pip` or `uv pip`:

uv

pip


```
uv pip install fastmcp

```

### Verify Installation

To verify that FastMCP is installed correctly, you can run the following command:


```
fastmcp version

```

You should see output like the following:


```
$ fastmcp version

FastMCP version: 0.4.2.dev41+ga077727.d20250410
MCP version: 1.6.0
Python version: 3.12.2
Platform: macOS-15.3.1-arm64-arm-64bit
FastMCP root path: ~/Developer/fastmcp

```

## Upgrading from the Official MCP SDK

Upgrading from the official MCP SDK’s FastMCP 1.0 to FastMCP 2.0 is generally straightforward. The core server API is highly compatible, and in many cases, changing your import statement from `from mcp.server.fastmcp import FastMCP` to `from fastmcp import FastMCP` will be sufficient.


```
# Before

# After
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

```

Prior to `fastmcp==2.3.0` and `mcp==1.8.0`, the 2.x API always mirrored the official 1.0 API. However, as the projects diverge, this can not be guaranteed. You may see deprecation warnings if you attempt to use 1.0 APIs in FastMCP 2.x. Please refer to this documentation for details on new capabilities.

## Versioning and Breaking Changes

While we make every effort not to introduce backwards-incompatible changes to our public APIs and behavior, FastMCP exists in a rapidly evolving MCP landscape. We’re committed to bringing the most cutting-edge features to our users, which occasionally necessitates changes to existing functionality.As a practice, breaking changes will only occur on minor version changes (e.g., 2.3.x to 2.4.0). A minor version change indicates either:

- A significant new feature set that warrants a new minor version
- Introducing breaking changes that may affect behavior on upgrade

For users concerned about stability in production environments, we recommend pinning FastMCP to a specific version in your dependencies.Whenever possible, FastMCP will issue deprecation warnings when users attempt to use APIs that are either deprecated or destined for future removal. These warnings will be maintained for at least 1 minor version release, and may be maintained longer.Note that the “public API” includes the public functionality of the `FastMCP` server, core FastMCP components like `Tool`, `Prompt`, `Resource`, and `ResourceTemplate`, and their respective public methods. It does not include private methods, utilities, or objects that are stored as private attributes, as we do not expect users to rely on those implementation details.

## Installing for Development

If you plan to contribute to FastMCP, you should begin by cloning the repository and using uv to install all dependencies (development dependencies are installed automatically):


```
git clone https://github.com/jlowin/fastmcp.git
cd fastmcp
uv sync

```

This will install all dependencies, including ones for development, and create a virtual environment, which you can activate and use as normal.

### Unit Tests

FastMCP has a comprehensive unit test suite, and all PR’s must introduce and pass appropriate tests. To run the tests, use pytest:


```
pytest

```

### Pre-Commit Hooks

FastMCP uses pre-commit to manage code quality, including formatting, linting, and type-safety. All PRs must pass the pre-commit hooks, which are run as a part of the CI process. To install the pre-commit hooks, run:


```
uv run pre-commit install

```

Alternatively, to run pre-commit manually at any time, use:


```
pre-commit run --all-files

```

[Welcome!](https://gofastmcp.com/getting-started/welcome) [Quickstart](https://gofastmcp.com/getting-started/quickstart)


================================================================================
# 3. Your First Server
================================================================================

# Getting Started Quickstart

> **Category:** Getting Started
> **Source:** gofastmcp.com_getting-started_quickstart.json

---

### Quickstart

Welcome! This guide will help you quickly set up FastMCP and run your first MCP server.If you haven’t already installed FastMCP, follow the [installation instructions](https://gofastmcp.com/getting-started/installation).

## Creating a FastMCP Server

A FastMCP server is a collection of tools, resources, and other MCP components. To create a server, start by instantiating the `FastMCP` class.Create a new file called `my_server.py` and add the following code:

my\_server.py


```
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

```

That’s it! You’ve created a FastMCP server, albeit a very boring one. Let’s add a tool to make it more interesting.

## Adding a Tool

To add a tool that returns a simple greeting, write a function and decorate it with `@mcp.tool` to register it with the server:

my\_server.py


```
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
return f"Hello, {name}!"

```

## Testing the Server

To test the server, create a FastMCP client and point it at the server object.

my\_server.py


```
import asyncio
from fastmcp import FastMCP, Client

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
return f"Hello, {name}!"

client = Client(mcp)

async def call_tool(name: str):
async with client:
result = await client.call_tool("greet", {"name": name})
print(result)

asyncio.run(call_tool("Ford"))

```

There are a few things to note here:

- Clients are asynchronous, so we need to use `asyncio.run` to run the client.
- We must enter a client context ( `async with client:`) before using the client. You can make multiple client calls within the same context.

## Running the server

In order to run the server with Python, we need to add a `run` statement to the `__main__` block of the server file.

my\_server.py


```
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
return f"Hello, {name}!"

if __name__ == "__main__":
mcp.run()

```

This lets us run the server with `python my_server.py`, using the default `stdio` transport, which is the standard way to expose an MCP server to a client.

Why do we need the `if __name__ == "__main__":` block?Within the FastMCP ecosystem, this line may be unnecessary. However, including it ensures that your FastMCP server runs for all users and clients in a consistent way and is therefore recommended as best practice.

### Interacting with the Python server

Now that the server can be executed with `python my_server.py`, we can interact with it like any other MCP server.In a new file, create a client and point it at the server file:

my\_client.py


```
import asyncio
from fastmcp import Client

client = Client("my_server.py")

async def call_tool(name: str):
async with client:
result = await client.call_tool("greet", {"name": name})
print(result)

asyncio.run(call_tool("Ford"))

```

### Using the FastMCP CLI

To have FastMCP run the server for us, we can use the `fastmcp run` command. This will start the server and keep it running until it is stopped. By default, it will use the `stdio` transport, which is a simple text-based protocol for interacting with the server.


```
fastmcp run my_server.py:mcp

```

Note that FastMCP _does not_ require the `__main__` block in the server file, and will ignore it if it is present. Instead, it looks for the server object provided in the CLI command (here, `mcp`). If no server object is provided, `fastmcp run` will automatically search for servers called “mcp”, “app”, or “server” in the file.

We pointed our client at the server file, which is recognized as a Python MCP server and executed with `python my_server.py` by default. This executes the `__main__` block of the server file. There are other ways to run the server, which are described in the [server configuration](https://gofastmcp.com/servers/server#running-the-server) guide.

[Installation](https://gofastmcp.com/getting-started/installation) [Overview](https://gofastmcp.com/servers/server)


================================================================================
# 4. FastMCP Server API Reference
================================================================================

# fastmcp.server.server

> **Category:** fastmcp.server.server
> **Source:** gofastmcp.com_python-sdk_fastmcp-server-server.json

---

fastmcp.server.server

FastMCP - A more ergonomic interface for MCP servers.

## Functions

default_lifespan


```
default_lifespan(server: FastMCP[LifespanResultT]) -> AsyncIterator[Any]

```

Default lifespan context manager that does nothing.**Args:**

- `server`: The server instance this lifespan is managing

**Returns:**

- An empty context object

add_resource_prefix


```
add_resource_prefix(uri: str, prefix: str, prefix_format: Literal['protocol', 'path'] | None = None) -> str

```

Add a prefix to a resource URI.**Args:**

- `uri`: The original resource URI
- `prefix`: The prefix to add

**Returns:**

- The resource URI with the prefix added

**Examples:**With new style:


```
add_resource_prefix("resource://path/to/resource", "prefix")
"resource://prefix/path/to/resource"

```

With legacy style:


```
add_resource_prefix("resource://path/to/resource", "prefix")
"prefix+resource://path/to/resource"

```

With absolute path:


```
add_resource_prefix("resource:///absolute/path", "prefix")
"resource://prefix//absolute/path"

```

**Raises:**

- `ValueError`: If the URI doesn’t match the expected protocol://path format

remove_resource_prefix


```
remove_resource_prefix(uri: str, prefix: str, prefix_format: Literal['protocol', 'path'] | None = None) -> str

```

Remove a prefix from a resource URI.**Args:**

- `uri`: The resource URI with a prefix
- `prefix`: The prefix to remove
- `prefix_format`: The format of the prefix to remove

Returns:
The resource URI with the prefix removed**Examples:**With new style:


```
remove_resource_prefix("resource://prefix/path/to/resource", "prefix")
"resource://path/to/resource"

```

With legacy style:


```
remove_resource_prefix("prefix+resource://path/to/resource", "prefix")
"resource://path/to/resource"

```

With absolute path:


```
remove_resource_prefix("resource://prefix//absolute/path", "prefix")
"resource:///absolute/path"

```

**Raises:**

- `ValueError`: If the URI doesn’t match the expected protocol://path format

has_resource_prefix


```
has_resource_prefix(uri: str, prefix: str, prefix_format: Literal['protocol', 'path'] | None = None) -> bool

```

Check if a resource URI has a specific prefix.**Args:**

- `uri`: The resource URI to check
- `prefix`: The prefix to look for

**Returns:**

- True if the URI has the specified prefix, False otherwise

**Examples:**With new style:


```
has_resource_prefix("resource://prefix/path/to/resource", "prefix")
### True

```

With legacy style:


```
has_resource_prefix("prefix+resource://path/to/resource", "prefix")
### True

```

With other path:


```
has_resource_prefix("resource://other/path/to/resource", "prefix")
### False

```

**Raises:**

- `ValueError`: If the URI doesn’t match the expected protocol://path format

## Classes

FastMCP

**Methods:**

settings


```
settings(self) -> Settings

```

name


```
name(self) -> str

```

instructions


```
instructions(self) -> str | None

```

run_async


```
run_async(self, transport: Transport | None = None, show_banner: bool = True, **transport_kwargs: Any) -> None

```

Run the FastMCP server asynchronously.**Args:**

- `transport`: Transport protocol to use (“stdio”, “sse”, or “streamable-http”)

run


```
run(self, transport: Transport | None = None, show_banner: bool = True, **transport_kwargs: Any) -> None

```

Run the FastMCP server. Note this is a synchronous function.**Args:**

- `transport`: Transport protocol to use (“stdio”, “sse”, or “streamable-http”)

add_middleware


```
add_middleware(self, middleware: Middleware) -> None

```

get_tools


```
get_tools(self) -> dict[str, Tool]

```

Get all registered tools, indexed by registered key.

get_tool


```
get_tool(self, key: str) -> Tool

```

get_resources


```
get_resources(self) -> dict[str, Resource]

```

Get all registered resources, indexed by registered key.

get_resource


```
get_resource(self, key: str) -> Resource

```

get_resource_templates


```
get_resource_templates(self) -> dict[str, ResourceTemplate]

```

Get all registered resource templates, indexed by registered key.

get_resource_template


```
get_resource_template(self, key: str) -> ResourceTemplate

```

Get a registered resource template by key.

get_prompts


```
get_prompts(self) -> dict[str, Prompt]

```

List all available prompts.

get_prompt


```
get_prompt(self, key: str) -> Prompt

```

custom_route


```
custom_route(self, path: str, methods: list[str], name: str | None = None, include_in_schema: bool = True) -> Callable[[Callable[[Request], Awaitable[Response]]], Callable[[Request], Awaitable[Response]]]

```

Decorator to register a custom HTTP route on the FastMCP server.Allows adding arbitrary HTTP endpoints outside the standard MCP protocol,
which can be useful for OAuth callbacks, health checks, or admin APIs.
The handler function must be an async function that accepts a Starlette
Request and returns a Response.**Args:**

- `path`: URL path for the route (e.g., “/oauth/callback”)
- `methods`: List of HTTP methods to support (e.g., \[“GET”, “POST”\])
- `name`: Optional name for the route (to reference this route with
Starlette’s reverse URL lookup feature)
- `include_in_schema`: Whether to include in OpenAPI schema, defaults to True

add_tool


```
add_tool(self, tool: Tool) -> Tool

```

Add a tool to the server.The tool function can optionally request a Context object by adding a parameter
with the Context type annotation. See the @tool decorator for examples.**Args:**

- `tool`: The Tool instance to register

**Returns:**

- The tool instance that was added to the server.

remove_tool


```
remove_tool(self, name: str) -> None

```

Remove a tool from the server.**Args:**

- `name`: The name of the tool to remove

**Raises:**

- `NotFoundError`: If the tool is not found

add_tool_transformation


```
add_tool_transformation(self, tool_name: str, transformation: ToolTransformConfig) -> None

```

Add a tool transformation.

remove_tool_transformation


```
remove_tool_transformation(self, tool_name: str) -> None

```

Remove a tool transformation.

tool


```
tool(self, name_or_fn: AnyFunction) -> FunctionTool

```

tool


```
tool(self, name_or_fn: str | None = None) -> Callable[[AnyFunction], FunctionTool]

```

tool


```
tool(self, name_or_fn: str | AnyFunction | None = None) -> Callable[[AnyFunction], FunctionTool] | FunctionTool

```

Decorator to register a tool.Tools can optionally request a Context object by adding a parameter with the
Context type annotation. The context provides access to MCP capabilities like
logging, progress reporting, and resource access.This decorator supports multiple calling patterns:

- @server.tool (without parentheses)
- @server.tool (with empty parentheses)
- @server.tool(“custom\_name”) (with name as first argument)
- @server.tool(name=“custom\_name”) (with name as keyword argument)
- server.tool(function, name=“custom\_name”) (direct function call)

**Args:**

- `name_or_fn`: Either a function (when used as @tool), a string name, or None
- `name`: Optional name for the tool (keyword-only, alternative to name\_or\_fn)
- `description`: Optional description of what the tool does
- `tags`: Optional set of tags for categorizing the tool
- `output_schema`: Optional JSON schema for the tool’s output
- `annotations`: Optional annotations about the tool’s behavior
- `exclude_args`: Optional list of argument names to exclude from the tool schema
- `enabled`: Optional boolean to enable or disable the tool

**Examples:**Register a tool with a custom name:


```
@server.tool
def my_tool(x: int) -> str:
return str(x)

# Register a tool with a custom name
@server.tool
def my_tool(x: int) -> str:
return str(x)

@server.tool("custom_name")
def my_tool(x: int) -> str:
return str(x)

@server.tool(name="custom_name")
def my_tool(x: int) -> str:
return str(x)

# Direct function call
server.tool(my_function, name="custom_name")

```

add_resource


```
add_resource(self, resource: Resource) -> Resource

```

Add a resource to the server.**Args:**

- `resource`: A Resource instance to add

**Returns:**

- The resource instance that was added to the server.

add_template


```
add_template(self, template: ResourceTemplate) -> ResourceTemplate

```

Add a resource template to the server.**Args:**

- `template`: A ResourceTemplate instance to add

**Returns:**

- The template instance that was added to the server.

add_resource_fn


```
add_resource_fn(self, fn: AnyFunction, uri: str, name: str | None = None, description: str | None = None, mime_type: str | None = None, tags: set[str] | None = None) -> None

```

Add a resource or template to the server from a function.If the URI contains parameters (e.g. “resource://”) or the function
has parameters, it will be registered as a template resource.**Args:**

- `fn`: The function to register as a resource
- `uri`: The URI for the resource
- `name`: Optional name for the resource
- `description`: Optional description of the resource
- `mime_type`: Optional MIME type for the resource
- `tags`: Optional set of tags for categorizing the resource

resource


```
resource(self, uri: str) -> Callable[[AnyFunction], Resource | ResourceTemplate]

```

Decorator to register a function as a resource.The function will be called when the resource is read to generate its content.
The function can return:

- str for text content
- bytes for binary content
- other types will be converted to JSON

Resources can optionally request a Context object by adding a parameter with the
Context type annotation. The context provides access to MCP capabilities like
logging, progress reporting, and session information.If the URI contains parameters (e.g. “resource://”) or the function
has parameters, it will be registered as a template resource.**Args:**

- `uri`: URI for the resource (e.g. “resource://my-resource” or “resource://”)
- `name`: Optional name for the resource
- `description`: Optional description of the resource
- `mime_type`: Optional MIME type for the resource
- `tags`: Optional set of tags for categorizing the resource
- `enabled`: Optional boolean to enable or disable the resource

**Examples:**Register a resource with a custom name:


```
@server.resource("resource://my-resource")
def get_data() -> str:
return "Hello, world!"

@server.resource("resource://my-resource")
async get_data() -> str:
data = await fetch_data()
return f"Hello, world! {data}"

@server.resource("resource://{city}/weather")
def get_weather(city: str) -> str:
return f"Weather for {city}"

@server.resource("resource://{city}/weather")
def get_weather_with_context(city: str, ctx: Context) -> str:
ctx.info(f"Fetching weather for {city}")
return f"Weather for {city}"

@server.resource("resource://{city}/weather")
async def get_weather(city: str) -> str:
data = await fetch_weather(city)
return f"Weather for {city}: {data}"

```

add_prompt


```
add_prompt(self, prompt: Prompt) -> Prompt

```

Add a prompt to the server.**Args:**

- `prompt`: A Prompt instance to add

**Returns:**

- The prompt instance that was added to the server.

prompt


```
prompt(self, name_or_fn: AnyFunction) -> FunctionPrompt

```

prompt


```
prompt(self, name_or_fn: str | None = None) -> Callable[[AnyFunction], FunctionPrompt]

```

prompt


```
prompt(self, name_or_fn: str | AnyFunction | None = None) -> Callable[[AnyFunction], FunctionPrompt] | FunctionPrompt

```

Decorator to register a prompt.Prompts can optionally request a Context object by adding a parameter with the
Context type annotation. The context provides access to MCP capabilities like
logging, progress reporting, and session information.This decorator supports multiple calling patterns:

- @server.prompt (without parentheses)
- @server.prompt() (with empty parentheses)
- @server.prompt(“custom\_name”) (with name as first argument)
- @server.prompt(name=“custom\_name”) (with name as keyword argument)
- server.prompt(function, name=“custom\_name”) (direct function call)

Args:
name\_or\_fn: Either a function (when used as @prompt), a string name, or None
name: Optional name for the prompt (keyword-only, alternative to name\_or\_fn)
description: Optional description of what the prompt does
tags: Optional set of tags for categorizing the prompt
enabled: Optional boolean to enable or disable the promptExamples:


```
@server.prompt
def analyze_table(table_name: str) -> list[Message]:
schema = read_table_schema(table_name)
return [\
{\
"role": "user",\
"content": f"Analyze this schema:\
{schema}"\
}\
]

@server.prompt()
def analyze_with_context(table_name: str, ctx: Context) -> list[Message]:
ctx.info(f"Analyzing table {table_name}")
schema = read_table_schema(table_name)
return [\
{\
"role": "user",\
"content": f"Analyze this schema:\
{schema}"\
}\
]

@server.prompt("custom_name")
def analyze_file(path: str) -> list[Message]:
content = await read_file(path)
return [\
{\
"role": "user",\
"content": {\
"type": "resource",\
"resource": {\
"uri": f"file://{path}",\
"text": content\
}\
}\
}\
]

@server.prompt(name="custom_name")
def another_prompt(data: str) -> list[Message]:
return [{"role": "user", "content": data}]

# Direct function call
server.prompt(my_function, name="custom_name")

```

run_stdio_async


```
run_stdio_async(self, show_banner: bool = True) -> None

```

Run the server using stdio transport.

run_http_async


```
run_http_async(self, show_banner: bool = True, transport: Literal['http', 'streamable-http', 'sse'] = 'http', host: str | None = None, port: int | None = None, log_level: str | None = None, path: str | None = None, uvicorn_config: dict[str, Any] | None = None, middleware: list[ASGIMiddleware] | None = None, stateless_http: bool | None = None) -> None

```

Run the server using HTTP transport.**Args:**

- `transport`: Transport protocol to use - either “streamable-http” (default) or “sse”
- `host`: Host address to bind to (defaults to settings.host)
- `port`: Port to bind to (defaults to settings.port)
- `log_level`: Log level for the server (defaults to settings.log\_level)
- `path`: Path for the endpoint (defaults to settings.streamable\_http\_path or settings.sse\_path)
- `uvicorn_config`: Additional configuration for the Uvicorn server
- `middleware`: A list of middleware to apply to the app
- `stateless_http`: Whether to use stateless HTTP (defaults to settings.stateless\_http)

run_sse_async


```
run_sse_async(self, host: str | None = None, port: int | None = None, log_level: str | None = None, path: str | None = None, uvicorn_config: dict[str, Any] | None = None) -> None

```

Run the server using SSE transport.

sse_app


```
sse_app(self, path: str | None = None, message_path: str | None = None, middleware: list[ASGIMiddleware] | None = None) -> StarletteWithLifespan

```

Create a Starlette app for the SSE server.**Args:**

- `path`: The path to the SSE endpoint
- `message_path`: The path to the message endpoint
- `middleware`: A list of middleware to apply to the app

streamable_http_app


```
streamable_http_app(self, path: str | None = None, middleware: list[ASGIMiddleware] | None = None) -> StarletteWithLifespan

```

Create a Starlette app for the StreamableHTTP server.**Args:**

- `path`: The path to the StreamableHTTP endpoint
- `middleware`: A list of middleware to apply to the app

http_app


```
http_app(self, path: str | None = None, middleware: list[ASGIMiddleware] | None = None, json_response: bool | None = None, stateless_http: bool | None = None, transport: Literal['http', 'streamable-http', 'sse'] = 'http') -> StarletteWithLifespan

```

Create a Starlette app using the specified HTTP transport.**Args:**

- `path`: The path for the HTTP endpoint
- `middleware`: A list of middleware to apply to the app
- `transport`: Transport protocol to use - either “streamable-http” (default) or “sse”

**Returns:**

- A Starlette application configured with the specified transport

run_streamable_http_async


```
run_streamable_http_async(self, host: str | None = None, port: int | None = None, log_level: str | None = None, path: str | None = None, uvicorn_config: dict[str, Any] | None = None) -> None

```

mount


```
mount(self, server: FastMCP[LifespanResultT], prefix: str | None = None, as_proxy: bool | None = None) -> None

```

Mount another FastMCP server on this server with an optional prefix.Unlike importing (with import\_server), mounting establishes a dynamic connection
between servers. When a client interacts with a mounted server’s objects through
the parent server, requests are forwarded to the mounted server in real-time.
This means changes to the mounted server are immediately reflected when accessed
through the parent.When a server is mounted with a prefix:

- Tools from the mounted server are accessible with prefixed names.
Example: If server has a tool named “get\_weather”, it will be available as “prefix\_get\_weather”.
- Resources are accessible with prefixed URIs.
Example: If server has a resource with URI “weather://forecast”, it will be available as
“weather://prefix/forecast”.
- Templates are accessible with prefixed URI templates.
Example: If server has a template with URI “weather://location/”, it will be available
as “weather://prefix/location/”.
- Prompts are accessible with prefixed names.
Example: If server has a prompt named “weather\_prompt”, it will be available as
“prefix\_weather\_prompt”.

When a server is mounted without a prefix (prefix=None), its tools, resources, templates,
and prompts are accessible with their original names. Multiple servers can be mounted
without prefixes, and they will be tried in order until a match is found.There are two modes for mounting servers:

1. Direct mounting (default when server has no custom lifespan): The parent server
directly accesses the mounted server’s objects in-memory for better performance.
In this mode, no client lifecycle events occur on the mounted server, including
lifespan execution.
2. Proxy mounting (default when server has a custom lifespan): The parent server
treats the mounted server as a separate entity and communicates with it via a
Client transport. This preserves all client-facing behaviors, including lifespan
execution, but with slightly higher overhead.

**Args:**

- `server`: The FastMCP server to mount.
- `prefix`: Optional prefix to use for the mounted server’s objects. If None,
the server’s objects are accessible with their original names.
- `as_proxy`: Whether to treat the mounted server as a proxy. If None (default),
automatically determined based on whether the server has a custom lifespan
(True if it has a custom lifespan, False otherwise).
- `tool_separator`: Deprecated. Separator character for tool names.
- `resource_separator`: Deprecated. Separator character for resource URIs.
- `prompt_separator`: Deprecated. Separator character for prompt names.

import_server


```
import_server(self, server: FastMCP[LifespanResultT], prefix: str | None = None, tool_separator: str | None = None, resource_separator: str | None = None, prompt_separator: str | None = None) -> None

```

Import the MCP objects from another FastMCP server into this one,
optionally with a given prefix.Note that when a server is _imported_, its objects are immediately
registered to the importing server. This is a one-time operation and
future changes to the imported server will not be reflected in the
importing server. Server-level configurations and lifespans are not imported.When a server is imported with a prefix:

- The tools are imported with prefixed names
Example: If server has a tool named “get\_weather”, it will be
available as “prefix\_get\_weather”
- The resources are imported with prefixed URIs using the new format
Example: If server has a resource with URI “weather://forecast”, it will
be available as “weather://prefix/forecast”
- The templates are imported with prefixed URI templates using the new format
Example: If server has a template with URI “weather://location/”, it will
be available as “weather://prefix/location/”
- The prompts are imported with prefixed names
Example: If server has a prompt named “weather\_prompt”, it will be available as
“prefix\_weather\_prompt”

When a server is imported without a prefix (prefix=None), its tools, resources,
templates, and prompts are imported with their original names.**Args:**

- `server`: The FastMCP server to import
- `prefix`: Optional prefix to use for the imported server’s objects. If None,
objects are imported with their original names.
- `tool_separator`: Deprecated. Separator for tool names.
- `resource_separator`: Deprecated and ignored. Prefix is now
applied using the protocol://prefix/path format
- `prompt_separator`: Deprecated. Separator for prompt names.

from_openapi


```
from_openapi(cls, openapi_spec: dict[str, Any], client: httpx.AsyncClient, route_maps: list[RouteMap] | list[RouteMapNew] | None = None, route_map_fn: OpenAPIRouteMapFn | OpenAPIRouteMapFnNew | None = None, mcp_component_fn: OpenAPIComponentFn | OpenAPIComponentFnNew | None = None, mcp_names: dict[str, str] | None = None, tags: set[str] | None = None, **settings: Any) -> FastMCPOpenAPI | FastMCPOpenAPINew

```

Create a FastMCP server from an OpenAPI specification.

from_fastapi


```
from_fastapi(cls, app: Any, name: str | None = None, route_maps: list[RouteMap] | list[RouteMapNew] | None = None, route_map_fn: OpenAPIRouteMapFn | OpenAPIRouteMapFnNew | None = None, mcp_component_fn: OpenAPIComponentFn | OpenAPIComponentFnNew | None = None, mcp_names: dict[str, str] | None = None, httpx_client_kwargs: dict[str, Any] | None = None, tags: set[str] | None = None, **settings: Any) -> FastMCPOpenAPI | FastMCPOpenAPINew

```

Create a FastMCP server from a FastAPI application.

as_proxy


```
as_proxy(cls, backend: Client[ClientTransportT] | ClientTransport | FastMCP[Any] | AnyUrl | Path | MCPConfig | dict[str, Any] | str, **settings: Any) -> FastMCPProxy

```

Create a FastMCP proxy server for the given backend.The `backend` argument can be either an existing `fastmcp.client.Client`
instance or any value accepted as the `transport` argument of
`fastmcp.client.Client`. This mirrors the convenience of the
`fastmcp.client.Client` constructor.

from_client


```
from_client(cls, client: Client[ClientTransportT], **settings: Any) -> FastMCPProxy

```

Create a FastMCP proxy server from a FastMCP client.

MountedServer

[proxy](https://gofastmcp.com/python-sdk/fastmcp-server-proxy) [\_\_init\_\_](https://gofastmcp.com/python-sdk/fastmcp-tools-__init__)


================================================================================
# 5. Using Decorators (@tool, @resource)
================================================================================

# Create an instance first, then register the bound methods

> **Category:** Patterns
> **Source:** gofastmcp.com_patterns_decorating-methods.json

---

### Patterns

Decorating Methods

FastMCP’s decorator system is designed to work with functions, but you may see unexpected behavior if you try to decorate an instance or class method. This guide explains the correct approach for using methods with all FastMCP decorators ( `@tool`, `@resource`, and `.prompt`).

## Why Are Methods Hard?

When you apply a FastMCP decorator like `@tool`, `@resource`, or `@prompt` to a method, the decorator captures the function at decoration time. For instance methods and class methods, this poses a challenge because:

1. For instance methods: The decorator gets the unbound method before any instance exists
2. For class methods: The decorator gets the function before it’s bound to the class

This means directly decorating these methods doesn’t work as expected. In practice, the LLM would see parameters like `self` or `cls` that it cannot provide values for.Additionally, **FastMCP decorators return objects (Tool, Resource, or Prompt instances) rather than the original function**. This means that when you decorate a method directly, the method becomes the returned object and is no longer callable by your code:

**Don’t do this!**The method will no longer be callable from Python, and the tool won’t be callable by LLMs.


```

from fastmcp import FastMCP
mcp = FastMCP()

class MyClass:
@mcp.tool
def my_method(self, x: int) -> int:
return x * 2

obj = MyClass()
obj.my_method(5) # Fails - my_method is a Tool, not a function

```

This is another important reason to register methods functionally after defining the class.

## Recommended Patterns

### Instance Methods

**Don’t do this!**


```
from fastmcp import FastMCP

mcp = FastMCP()

class MyClass:
@mcp.tool # This won't work correctly
def add(self, x, y):
return x + y

```

When the decorator is applied this way, it captures the unbound method. When the LLM later tries to use this component, it will see `self` as a required parameter, but it won’t know what to provide for it, causing errors or unexpected behavior.

**Do this instead**:


```
from fastmcp import FastMCP

mcp = FastMCP()

class MyClass:
def add(self, x, y):
return x + y

# Create an instance first, then register the bound methods
obj = MyClass()
mcp.tool(obj.add)

# Now you can call it without 'self' showing up as a parameter
await mcp._mcp_call_tool('add', {'x': 1, 'y': 2}) # Returns 3

```

This approach works because:

1. You first create an instance of the class ( `obj`)
2. When you access the method through the instance ( `obj.add`), Python creates a bound method where `self` is already set to that instance
3. When you register this bound method, the system sees a callable that only expects the appropriate parameters, not `self`

### Class Methods

The behavior of decorating class methods depends on the order of decorators:

**Don’t do this** (decorator order matters):


```
from fastmcp import FastMCP

mcp = FastMCP()

class MyClass:
@classmethod
@mcp.tool # This won't work but won't raise an error
def from_string_v1(cls, s):
return cls(s)

@mcp.tool
@classmethod # This will raise a helpful ValueError
def from_string_v2(cls, s):
return cls(s)

```

- If `@classmethod` comes first, then `@mcp.tool`: No error is raised, but it won’t work correctly
- If `@mcp.tool` comes first, then `@classmethod`: FastMCP will detect this and raise a helpful `ValueError` with guidance

**Do this instead**:


```
from fastmcp import FastMCP

mcp = FastMCP()

class MyClass:
@classmethod
def from_string(cls, s):
return cls(s)

# Register the class method after the class is defined
mcp.tool(MyClass.from_string)

```

This works because:

1. The `@classmethod` decorator is applied properly during class definition
2. When you access `MyClass.from_string`, Python provides a special method object that automatically binds the class to the `cls` parameter
3. When registered, only the appropriate parameters are exposed to the LLM, hiding the implementation detail of the `cls` parameter

### Static Methods

Static methods “work” with FastMCP decorators, but this is not recommended because the FastMCP decorator will not return a callable method. Therefore, you should register static methods the same way as other methods.

**This is not recommended, though it will work.**


```
from fastmcp import FastMCP

mcp = FastMCP()

class MyClass:
@mcp.tool
@staticmethod
def utility(x, y):
return x + y

```

This works because `@staticmethod` converts the method to a regular function, which the FastMCP decorator can then properly process. However, this is not recommended because the FastMCP decorator will not return a callable staticmethod. Therefore, you should register static methods the same way as other methods.

**Prefer this pattern:**


```
from fastmcp import FastMCP

mcp = FastMCP()

class MyClass:
@staticmethod
def utility(x, y):
return x + y

# This also works
mcp.tool(MyClass.utility)

```

## Additional Patterns

### Creating Components at Class Initialization

You can automatically register instance methods when creating an object:


```
from fastmcp import FastMCP

mcp = FastMCP()

class ComponentProvider:
def __init__(self, mcp_instance):
# Register methods
mcp_instance.tool(self.tool_method)
mcp_instance.resource("resource://data")(self.resource_method)

def tool_method(self, x):
return x * 2

def resource_method(self):
return "Resource data"

# The methods are automatically registered when creating the instance
provider = ComponentProvider(mcp)

```

This pattern is useful when:

- You want to encapsulate registration logic within the class itself
- You have multiple related components that should be registered together
- You want to ensure that methods are always properly registered when creating an instance

The class automatically registers its methods during initialization, ensuring they’re properly bound to the instance before registration.

## Summary

The current behavior of FastMCP decorators with methods is:

- **Static methods**: Can be decorated directly and work perfectly with all FastMCP decorators
- **Class methods**: Cannot be decorated directly and will raise a helpful `ValueError` with guidance
- **Instance methods**: Should be registered after creating an instance using the decorator calls

For class and instance methods, you should register them after creating the instance or class to ensure proper method binding. This ensures that the methods are properly bound before being registered.Understanding these patterns allows you to effectively organize your components into classes while maintaining proper method binding, giving you the benefits of object-oriented design without sacrificing the simplicity of FastMCP’s decorator system.

[Tool Transformation](https://gofastmcp.com/patterns/tool-transformation) [HTTP Requests](https://gofastmcp.com/patterns/http-requests)


================================================================================
# 6. Server Tools
================================================================================

# Implementation...

> **Category:** General
> **Source:** gofastmcp.com_servers_tools.json

---

Core Components

### Tools

Tools are the core building blocks that allow your LLM to interact with external systems, execute code, and access data that isn’t in its training data. In FastMCP, tools are Python functions exposed to LLMs through the MCP protocol.

## What Are Tools?

Tools in FastMCP transform regular Python functions into capabilities that LLMs can invoke during conversations. When an LLM decides to use a tool:

1. It sends a request with parameters based on the tool’s schema.
2. FastMCP validates these parameters against your function’s signature.
3. Your function executes with the validated inputs.
4. The result is returned to the LLM, which can use it in its response.

This allows LLMs to perform tasks like querying databases, calling APIs, making calculations, or accessing files,extending their capabilities beyond what’s in their training data.

## Tools

### The `@tool` Decorator

Creating a tool is as simple as decorating a Python function with `@mcp.tool`:


```
from fastmcp import FastMCP

mcp = FastMCP(name="CalculatorServer")

@mcp.tool
def add(a: int, b: int) -> int:
"""Adds two integer numbers together."""
return a + b

```

When this tool is registered, FastMCP automatically:

- Uses the function name ( `add`) as the tool name.
- Uses the function’s docstring ( `Adds two integer numbers...`) as the tool description.
- Generates an input schema based on the function’s parameters and type annotations.
- Handles parameter validation and error reporting.

The way you define your Python function dictates how the tool appears and behaves for the LLM client.

Functions with `*args` or `**kwargs` are not supported as tools. This restriction exists because FastMCP needs to generate a complete parameter schema for the MCP protocol, which isn’t possible with variable argument lists.

#### Decorator Arguments

While FastMCP infers the name and description from your function, you can override these and add additional metadata using arguments to the `@mcp.tool` decorator:


```
@mcp.tool(
name="find_products", # Custom tool name for the LLM
description="Search the product catalog with optional category filtering.", # Custom description
tags={"catalog", "search"}, # Optional tags for organization/filtering
meta={"version": "1.2", "author": "product-team"} # Custom metadata
)
def search_products_implementation(query: str, category: str | None = None) -> list[dict]:
"""Internal function description (ignored if description is provided above)."""
# Implementation...
print(f"Searching for '{query}' in category '{category}'")
return [{"id": 2, "name": "Another Product"}]

```

## @tool Decorator Arguments

name

str \| None

Sets the explicit tool name exposed via MCP. If not provided, uses the function name

description

str \| None

Provides the description exposed via MCP. If set, the function’s docstring is ignored for this purpose

tags

set\[str\] \| None

A set of strings used to categorize the tool. These can be used by the server and, in some cases, by clients to filter or group available tools.

enabled

bool

default:"True"

A boolean to enable or disable the tool. See [Disabling Tools](https://gofastmcp.com/servers/tools#disabling-tools) for more information

exclude\_args

list\[str\] \| None

A list of argument names to exclude from the tool schema shown to the LLM. See [Excluding Arguments](https://gofastmcp.com/servers/tools#excluding-arguments) for more information

annotations

ToolAnnotations \| dict \| None

An optional `ToolAnnotations` object or dictionary to add additional metadata about the tool.

Show ToolAnnotations attributes

title

str \| None

A human-readable title for the tool.

readOnlyHint

bool \| None

If true, the tool does not modify its environment.

destructiveHint

bool \| None

If true, the tool may perform destructive updates to its environment.

idempotentHint

bool \| None

If true, calling the tool repeatedly with the same arguments will have no additional effect on the its environment.

openWorldHint

bool \| None

If true, this tool may interact with an “open world” of external entities. If false, the tool’s domain of interaction is closed.

meta

dict\[str, Any\] \| None

`New in version: 2.11.0` Optional meta information about the tool. This data is passed through to the MCP client as the `_meta` field of the client-side tool object and can be used for custom metadata, versioning, or other application-specific purposes.

### Async and Synchronous Tools

FastMCP is an async-first framework that seamlessly supports both asynchronous ( `async def`) and synchronous ( `def`) functions as tools. Async tools are preferred for I/O-bound operations to keep your server responsive.While synchronous tools work seamlessly in FastMCP, they can block the event loop during execution. For CPU-intensive or potentially blocking synchronous operations, consider alternative strategies. One approach is to use `anyio` (which FastMCP already uses internally) to wrap them as async functions, for example:


```
import anyio
from fastmcp import FastMCP

mcp = FastMCP()

def cpu_intensive_task(data: str) -> str:
# Some heavy computation that could block the event loop
return processed_data

@mcp.tool
async def wrapped_cpu_task(data: str) -> str:
"""CPU-intensive task wrapped to prevent blocking."""
return await anyio.to_thread.run_sync(cpu_intensive_task, data)

```

Alternative approaches include using `asyncio.get_event_loop().run_in_executor()` or other threading techniques to manage blocking operations without impacting server responsiveness. For example, here’s a recipe for using the `asyncer` library (not included in FastMCP) to create a decorator that wraps synchronous functions, courtesy of [@hsheth2](https://github.com/jlowin/fastmcp/issues/864#issuecomment-3103678258):

Decorator Recipe

Using the Decorator


```
import asyncer
import functools
from typing import Callable, ParamSpec, TypeVar, Awaitable

_P = ParamSpec("_P")
_R = TypeVar("_R")

def make_async_background(fn: Callable[_P, _R]) -> Callable[_P, Awaitable[_R]]:
@functools.wraps(fn)
async def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
return await asyncer.asyncify(fn)(*args, **kwargs)

return wrapper

```

### Type Annotations

Type annotations for parameters are essential for proper tool functionality. They:

1. Inform the LLM about the expected data types for each parameter
2. Enable FastMCP to validate input data from clients
3. Generate accurate JSON schemas for the MCP protocol

Use standard Python type annotations for parameters:


```
@mcp.tool
def analyze_text(
text: str,
max_tokens: int = 100,
language: str | None = None
) -> dict:
"""Analyze the provided text."""
# Implementation...

```

FastMCP supports a wide range of type annotations, including all Pydantic types:

| Type Annotation | Example | Description |
| --- | --- | --- |
| Basic types | `int`, `float`, `str`, `bool` | Simple scalar values - see [Built-in Types](https://gofastmcp.com/servers/tools#built-in-types) |
| Binary data | `bytes` | Binary content - see [Binary Data](https://gofastmcp.com/servers/tools#binary-data) |
| Date and Time | `datetime`, `date`, `timedelta` | Date and time objects - see [Date and Time Types](https://gofastmcp.com/servers/tools#date-and-time-types) |
| Collection types | `list[str]`, `dict[str, int]`, `set[int]` | Collections of items - see [Collection Types](https://gofastmcp.com/servers/tools#collection-types) |
| Optional types | `float | None`, `Optional[float]` | Parameters that may be null/omitted - see [Union and Optional Types](https://gofastmcp.com/servers/tools#union-and-optional-types) |
| Union types | `str | int`, `Union[str, int]` | Parameters accepting multiple types - see [Union and Optional Types](https://gofastmcp.com/servers/tools#union-and-optional-types) |
| Constrained types | `Literal["A", "B"]`, `Enum` | Parameters with specific allowed values - see [Constrained Types](https://gofastmcp.com/servers/tools#constrained-types) |
| Paths | `Path` | File system paths - see [Paths](https://gofastmcp.com/servers/tools#paths) |
| UUIDs | `UUID` | Universally unique identifiers - see [UUIDs](https://gofastmcp.com/servers/tools#uuids) |
| Pydantic models | `UserData` | Complex structured data - see [Pydantic Models](https://gofastmcp.com/servers/tools#pydantic-models) |

For additional type annotations not listed here, see the [Parameter Types](https://gofastmcp.com/servers/tools#parameter-types) section below for more detailed information and examples.

### Parameter Metadata

You can provide additional metadata about parameters in several ways:

#### Simple String Descriptions

`New in version: 2.11.0` For basic parameter descriptions, you can use a convenient shorthand with `Annotated`:


```
from typing import Annotated

@mcp.tool
def process_image(
image_url: Annotated[str, "URL of the image to process"],
resize: Annotated[bool, "Whether to resize the image"] = False,
width: Annotated[int, "Target width in pixels"] = 800,
format: Annotated[str, "Output image format"] = "jpeg"
) -> dict:
"""Process an image with optional resizing."""
# Implementation...

```

This shorthand syntax is equivalent to using `Field(description=...)` but more concise for simple descriptions.

This shorthand syntax is only applied to `Annotated` types with a single string description.

#### Advanced Metadata with Field

For validation constraints and advanced metadata, use Pydantic’s `Field` class with `Annotated`:


```
from typing import Annotated
from pydantic import Field

@mcp.tool
def process_image(
image_url: Annotated[str, Field(description="URL of the image to process")],
resize: Annotated[bool, Field(description="Whether to resize the image")] = False,
width: Annotated[int, Field(description="Target width in pixels", ge=1, le=2000)] = 800,
format: Annotated[\
Literal["jpeg", "png", "webp"],\
Field(description="Output image format")\
] = "jpeg"
) -> dict:
"""Process an image with optional resizing."""
# Implementation...

```

You can also use the Field as a default value, though the Annotated approach is preferred:


```
@mcp.tool
def search_database(
query: str = Field(description="Search query string"),
limit: int = Field(10, description="Maximum number of results", ge=1, le=100)
) -> list:
"""Search the database with the provided query."""
# Implementation...

```

Field provides several validation and documentation features:

- `description`: Human-readable explanation of the parameter (shown to LLMs)
- `ge`/ `gt`/ `le`/ `lt`: Greater/less than (or equal) constraints
- `min_length`/ `max_length`: String or collection length constraints
- `pattern`: Regex pattern for string validation
- `default`: Default value if parameter is omitted

### Optional Arguments

FastMCP follows Python’s standard function parameter conventions. Parameters without default values are required, while those with default values are optional.


```
@mcp.tool
def search_products(
query: str, # Required - no default value
max_results: int = 10, # Optional - has default value
sort_by: str = "relevance", # Optional - has default value
category: str | None = None # Optional - can be None
) -> list[dict]:
"""Search the product catalog."""
# Implementation...

```

In this example, the LLM must provide a `query` parameter, while `max_results`, `sort_by`, and `category` will use their default values if not explicitly provided.

### Excluding Arguments

`New in version: 2.6.0` You can exclude certain arguments from the tool schema shown to the LLM. This is useful for arguments that are injected at runtime (such as `state`, `user_id`, or credentials) and should not be exposed to the LLM or client. Only arguments with default values can be excluded; attempting to exclude a required argument will raise an error.Example:


```
@mcp.tool(
name="get_user_details",
exclude_args=["user_id"]
)
def get_user_details(user_id: str = None) -> str:
# user_id will be injected by the server, not provided by the LLM
...

```

With this configuration, `user_id` will not appear in the tool’s parameter schema, but can still be set by the server or framework at runtime.For more complex tool transformations, see [Transforming Tools](https://gofastmcp.com/patterns/tool-transformation).

### Disabling Tools

`New in version: 2.8.0` You can control the visibility and availability of tools by enabling or disabling them. This is useful for feature flagging, maintenance, or dynamically changing the toolset available to a client. Disabled tools will not appear in the list of available tools returned by `list_tools`, and attempting to call a disabled tool will result in an “Unknown tool” error, just as if the tool did not exist.By default, all tools are enabled. You can disable a tool upon creation using the `enabled` parameter in the decorator:


```
@mcp.tool(enabled=False)
def maintenance_tool():
"""This tool is currently under maintenance."""
return "This tool is disabled."

```

You can also toggle a tool’s state programmatically after it has been created:


```
@mcp.tool
def dynamic_tool():
return "I am a dynamic tool."

# Disable and re-enable the tool
dynamic_tool.disable()
dynamic_tool.enable()

```

### Return Values

FastMCP tools can return data in two complementary formats: **traditional content blocks** (like text and images) and **structured outputs** (machine-readable JSON). When you add return type annotations, FastMCP automatically generates **output schemas** to validate the structured data and enables clients to deserialize results back to Python objects.Understanding how these three concepts work together:

- **Return Values**: What your Python function returns (determines both content blocks and structured data)
- **Structured Outputs**: JSON data sent alongside traditional content for machine processing
- **Output Schemas**: JSON Schema declarations that describe and validate the structured output format

The following sections explain each concept in detail.

#### Content Blocks

FastMCP automatically converts tool return values into appropriate MCP content blocks:

- **`str`**: Sent as `TextContent`
- **`bytes`**: Base64 encoded and sent as `BlobResourceContents` (within an `EmbeddedResource`)
- **`fastmcp.utilities.types.Image`**: Sent as `ImageContent`
- **`fastmcp.utilities.types.Audio`**: Sent as `AudioContent`
- **`fastmcp.utilities.types.File`**: Sent as base64-encoded `EmbeddedResource`
- **A list of any of the above**: Converts each item appropriately
- **`None`**: Results in an empty response

#### Structured Output

`New in version: 2.10.0` The 6/18/2025 MCP spec update [introduced](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#structured-content) structured content, which is a new way to return data from tools. Structured content is a JSON object that is sent alongside traditional content. FastMCP automatically creates structured outputs alongside traditional content when your tool returns data that has a JSON object representation. This provides machine-readable JSON data that clients can deserialize back to Python objects.**Automatic Structured Content Rules:**

- **Object-like results** ( `dict`, Pydantic models, dataclasses) → Always become structured content (even without output schema)
- **Non-object results** ( `int`, `str`, `list`) → Only become structured content if there’s an output schema to validate/serialize them
- **All results** → Always become traditional content blocks for backward compatibility

This automatic behavior enables clients to receive machine-readable data alongside human-readable content without requiring explicit output schemas for object-like returns.

##### Object-like Results (Automatic Structured Content)

Dict Return (No Schema Needed)

Traditional Content

Structured Content (Automatic)


```
@mcp.tool
def get_user_data(user_id: str) -> dict:
"""Get user data without type annotation."""
return {"name": "Alice", "age": 30, "active": True}

```

##### Non-object Results (Schema Required)

Integer Return (No Schema)

Traditional Content Only

Integer Return (With Schema)

Traditional Content

Structured Content (From Schema)


```
@mcp.tool
def calculate_sum(a: int, b: int):
"""Calculate sum without return annotation."""
return a + b # Returns 8

```

##### Complex Type Example

Tool Definition

Generated Output Schema

Structured Output


```
from dataclasses import dataclass
from fastmcp import FastMCP

mcp = FastMCP()

@dataclass
class Person:
name: str
age: int
email: str

@mcp.tool
def get_user_profile(user_id: str) -> Person:
"""Get a user's profile information."""
return Person(name="Alice", age=30, email="alice@example.com")

```

#### Output Schemas

`New in version: 2.10.0` The 6/18/2025 MCP spec update [introduced](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#output-schema) output schemas, which are a new way to describe the expected output format of a tool. When an output schema is provided, the tool _must_ return structured output that matches the schema.When you add return type annotations to your functions, FastMCP automatically generates JSON schemas that describe the expected output format. These schemas help MCP clients understand and validate the structured data they receive.

##### Primitive Type Wrapping

For primitive return types (like `int`, `str`, `bool`), FastMCP automatically wraps the result under a `"result"` key to create valid structured output:

Primitive Return Type

Generated Schema (Wrapped)

Structured Output


```
@mcp.tool
def calculate_sum(a: int, b: int) -> int:
"""Add two numbers together."""
return a + b

```

##### Manual Schema Control

You can override the automatically generated schema by providing a custom `output_schema`:


```
@mcp.tool(output_schema={
"type": "object",
"properties": {
"data": {"type": "string"},
"metadata": {"type": "object"}
}
})
def custom_schema_tool() -> dict:
"""Tool with custom output schema."""
return {"data": "Hello", "metadata": {"version": "1.0"}}

```

Schema generation works for most common types including basic types, collections, union types, Pydantic models, TypedDict structures, and dataclasses.

**Important Constraints**:

- Output schemas must be object types ( `"type": "object"`)
- If you provide an output schema, your tool **must** return structured output that matches it
- However, you can provide structured output without an output schema (using `ToolResult`)

#### Full Control with ToolResult

For complete control over both traditional content and structured output, return a `ToolResult` object:


```
from fastmcp.tools.tool import ToolResult

@mcp.tool
def advanced_tool() -> ToolResult:
"""Tool with full control over output."""
return ToolResult(
content=[TextContent(text="Human-readable summary")],
structured_content={"data": "value", "count": 42}
)

```

When returning `ToolResult`:

- You control exactly what content and structured data is sent
- Output schemas are optional - structured content can be provided without a schema
- Clients receive both traditional content blocks and structured data

If your return type annotation cannot be converted to a JSON schema (e.g., complex custom classes without Pydantic support), the output schema will be omitted but the tool will still function normally with traditional content.

### Error Handling

`New in version: 2.4.1` If your tool encounters an error, you can raise a standard Python exception ( `ValueError`, `TypeError`, `FileNotFoundError`, custom exceptions, etc.) or a FastMCP `ToolError`.By default, all exceptions (including their details) are logged and converted into an MCP error response to be sent back to the client LLM. This helps the LLM understand failures and react appropriately.If you want to mask internal error details for security reasons, you can:

1. Use the `mask_error_details=True` parameter when creating your `FastMCP` instance:


```
mcp = FastMCP(name="SecureServer", mask_error_details=True)

```

2. Or use `ToolError` to explicitly control what error information is sent to clients:


```
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

@mcp.tool
def divide(a: float, b: float) -> float:
"""Divide a by b."""

if b == 0:
# Error messages from ToolError are always sent to clients,
raise ToolError("Division by zero is not allowed.")

# If mask_error_details=True, this message would be masked
if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
raise TypeError("Both arguments must be numbers.")

return a / b

```

When `mask_error_details=True`, only error messages from `ToolError` will include details, other exceptions will be converted to a generic message.

### Annotations

`New in version: 2.2.7` FastMCP allows you to add specialized metadata to your tools through annotations. These annotations communicate how tools behave to client applications without consuming token context in LLM prompts.Annotations serve several purposes in client applications:

- Adding user-friendly titles for display purposes
- Indicating whether tools modify data or systems
- Describing the safety profile of tools (destructive vs. non-destructive)
- Signaling if tools interact with external systems

You can add annotations to a tool using the `annotations` parameter in the `@mcp.tool` decorator:


```
@mcp.tool(
annotations={
"title": "Calculate Sum",
"readOnlyHint": True,
"openWorldHint": False
}
)
def calculate_sum(a: float, b: float) -> float:
"""Add two numbers together."""
return a + b

```

FastMCP supports these standard annotations:

| Annotation | Type | Default | Purpose |
| --- | --- | --- | --- |
| `title` | string | - | Display name for user interfaces |
| `readOnlyHint` | boolean | false | Indicates if the tool only reads without making changes |
| `destructiveHint` | boolean | true | For non-readonly tools, signals if changes are destructive |
| `idempotentHint` | boolean | false | Indicates if repeated identical calls have the same effect as a single call |
| `openWorldHint` | boolean | true | Specifies if the tool interacts with external systems |

Remember that annotations help make better user experiences but should be treated as advisory hints. They help client applications present appropriate UI elements and safety controls, but won’t enforce security boundaries on their own. Always focus on making your annotations accurately represent what your tool actually does.

### Notifications

`New in version: 2.9.1` FastMCP automatically sends `notifications/tools/list_changed` notifications to connected clients when tools are added, removed, enabled, or disabled. This allows clients to stay up-to-date with the current tool set without manually polling for changes.


```
@mcp.tool
def example_tool() -> str:
return "Hello!"

# These operations trigger notifications:
mcp.add_tool(example_tool) # Sends tools/list_changed notification
example_tool.disable() # Sends tools/list_changed notification
example_tool.enable() # Sends tools/list_changed notification
mcp.remove_tool("example_tool") # Sends tools/list_changed notification

```

Notifications are only sent when these operations occur within an active MCP request context (e.g., when called from within a tool or other MCP operation). Operations performed during server initialization do not trigger notifications.Clients can handle these notifications using a [message handler](https://gofastmcp.com/clients/messages) to automatically refresh their tool lists or update their interfaces.

## MCP Context

Tools can access MCP features like logging, reading resources, or reporting progress through the `Context` object. To use it, add a parameter to your tool function with the type hint `Context`.


```
from fastmcp import FastMCP, Context

mcp = FastMCP(name="ContextDemo")

@mcp.tool
async def process_data(data_uri: str, ctx: Context) -> dict:
"""Process data from a resource with progress reporting."""
await ctx.info(f"Processing data from {data_uri}")

# Read a resource
resource = await ctx.read_resource(data_uri)
data = resource[0].content if resource else ""

# Report progress
await ctx.report_progress(progress=50, total=100)

# Example request to the client's LLM for help
summary = await ctx.sample(f"Summarize this in 10 words: {data[:200]}")

await ctx.report_progress(progress=100, total=100)
return {
"length": len(data),
"summary": summary.text
}

```

The Context object provides access to:

- **Logging**: `ctx.debug()`, `ctx.info()`, `ctx.warning()`, `ctx.error()`
- **Progress Reporting**: `ctx.report_progress(progress, total)`
- **Resource Access**: `ctx.read_resource(uri)`
- **LLM Sampling**: `ctx.sample(...)`
- **Request Information**: `ctx.request_id`, `ctx.client_id`

For full documentation on the Context object and all its capabilities, see the [Context documentation](https://gofastmcp.com/servers/context).

## Parameter Types

FastMCP supports a wide variety of parameter types to give you flexibility when designing your tools.FastMCP generally supports all types that Pydantic supports as fields, including all Pydantic custom types. This means you can use any type that can be validated and parsed by Pydantic in your tool parameters.FastMCP supports **type coercion** when possible. This means that if a client sends data that doesn’t match the expected type, FastMCP will attempt to convert it to the appropriate type. For example, if a client sends a string for a parameter annotated as `int`, FastMCP will attempt to convert it to an integer. If the conversion is not possible, FastMCP will return a validation error.

### Built-in Types

The most common parameter types are Python’s built-in scalar types:


```
@mcp.tool
def process_values(
name: str, # Text data
count: int, # Integer numbers
amount: float, # Floating point numbers
enabled: bool # Boolean values (True/False)
):
"""Process various value types."""
# Implementation...

```

These types provide clear expectations to the LLM about what values are acceptable and allow FastMCP to validate inputs properly. Even if a client provides a string like “42”, it will be coerced to an integer for parameters annotated as `int`.

### Date and Time Types

FastMCP supports various date and time types from the `datetime` module:


```
from datetime import datetime, date, timedelta

@mcp.tool
def process_date_time(
event_date: date, # ISO format date string or date object
event_time: datetime, # ISO format datetime string or datetime object
duration: timedelta = timedelta(hours=1) # Integer seconds or timedelta
) -> str:
"""Process date and time information."""
# Types are automatically converted from strings
assert isinstance(event_date, date)
assert isinstance(event_time, datetime)
assert isinstance(duration, timedelta)

return f"Event on {event_date} at {event_time} for {duration}"

```

- `datetime` \- Accepts ISO format strings (e.g., “2023-04-15T14:30:00”)
- `date` \- Accepts ISO format date strings (e.g., “2023-04-15”)
- `timedelta` \- Accepts integer seconds or timedelta objects

### Collection Types

FastMCP supports all standard Python collection types:


```
@mcp.tool
def analyze_data(
values: list[float], # List of numbers
properties: dict[str, str], # Dictionary with string keys and values
unique_ids: set[int], # Set of unique integers
coordinates: tuple[float, float], # Tuple with fixed structure
mixed_data: dict[str, list[int]] # Nested collections
):
"""Analyze collections of data."""
# Implementation...

```

All collection types can be used as parameter annotations:

- `list[T]` \- Ordered sequence of items
- `dict[K, V]` \- Key-value mapping
- `set[T]` \- Unordered collection of unique items
- `tuple[T1, T2, ...]` \- Fixed-length sequence with potentially different types

Collection types can be nested and combined to represent complex data structures. JSON strings that match the expected structure will be automatically parsed and converted to the appropriate Python collection type.

### Union and Optional Types

For parameters that can accept multiple types or may be omitted:


```
@mcp.tool
def flexible_search(
query: str | int, # Can be either string or integer
filters: dict[str, str] | None = None, # Optional dictionary
sort_field: str | None = None # Optional string
):
"""Search with flexible parameter types."""
# Implementation...

```

Modern Python syntax ( `str | int`) is preferred over older `Union[str, int]` forms. Similarly, `str | None` is preferred over `Optional[str]`.

### Constrained Types

When a parameter must be one of a predefined set of values, you can use either Literal types or Enums:

#### Literals

Literals constrain parameters to a specific set of values:


```
from typing import Literal

@mcp.tool
def sort_data(
data: list[float],
order: Literal["ascending", "descending"] = "ascending",
algorithm: Literal["quicksort", "mergesort", "heapsort"] = "quicksort"
):
"""Sort data using specific options."""
# Implementation...

```

Literal types:

- Specify exact allowable values directly in the type annotation
- Help LLMs understand exactly which values are acceptable
- Provide input validation (errors for invalid values)
- Create clear schemas for clients

#### Enums

For more structured sets of constrained values, use Python’s Enum class:


```
from enum import Enum

class Color(Enum):
RED = "red"
GREEN = "green"
BLUE = "blue"

@mcp.tool
def process_image(
image_path: str,
color_filter: Color = Color.RED
):
"""Process an image with a color filter."""
# Implementation...

```

When using Enum types:

- Clients should provide the enum’s value (e.g., “red”), not the enum member name (e.g., “RED”)
- FastMCP automatically coerces the string value into the appropriate Enum object
- Your function receives the actual Enum member (e.g., `Color.RED`)
- Validation errors are raised for values not in the enum

### Binary Data

There are two approaches to handling binary data in tool parameters:

#### Bytes


```
@mcp.tool
def process_binary(data: bytes):
"""Process binary data directly.

The client can send a binary string, which will be
converted directly to bytes.
"""
# Implementation using binary data
data_length = len(data)
# ...

```

When you annotate a parameter as `bytes`, FastMCP will:

- Convert raw strings directly to bytes
- Validate that the input can be properly represented as bytes

FastMCP does not automatically decode base64-encoded strings for bytes parameters. If you need to accept base64-encoded data, you should handle the decoding manually as shown below.

#### Base64-encoded strings


```
from typing import Annotated
from pydantic import Field

@mcp.tool
def process_image_data(
image_data: Annotated[str, Field(description="Base64-encoded image data")]
):
"""Process an image from base64-encoded string.

The client is expected to provide base64-encoded data as a string.
You'll need to decode it manually.
"""
# Manual base64 decoding
import base64
binary_data = base64.b64decode(image_data)
# Process binary_data...

```

This approach is recommended when you expect to receive base64-encoded binary data from clients.

### Paths

The `Path` type from the `pathlib` module can be used for file system paths:


```
from pathlib import Path

@mcp.tool
def process_file(path: Path) -> str:
"""Process a file at the given path."""
assert isinstance(path, Path) # Path is properly converted
return f"Processing file at {path}"

```

When a client sends a string path, FastMCP automatically converts it to a `Path` object.

### UUIDs

The `UUID` type from the `uuid` module can be used for unique identifiers:


```
import uuid

@mcp.tool
def process_item(
item_id: uuid.UUID # String UUID or UUID object
) -> str:
"""Process an item with the given UUID."""
assert isinstance(item_id, uuid.UUID) # Properly converted to UUID
return f"Processing item {item_id}"

```

When a client sends a string UUID (e.g., “123e4567-e89b-12d3-a456-426614174000”), FastMCP automatically converts it to a `UUID` object.

### Pydantic Models

For complex, structured data with nested fields and validation, use Pydantic models:


```
from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
username: str
email: str = Field(description="User's email address")
age: int | None = None
is_active: bool = True

@mcp.tool
def create_user(user: User):
"""Create a new user in the system."""
# The input is automatically validated against the User model

```

Using Pydantic models provides:

- Clear, self-documenting structure for complex inputs
- Built-in data validation
- Automatic generation of detailed JSON schemas for the LLM
- Automatic conversion from dict/JSON input

Clients can provide data for Pydantic model parameters as either:

- A JSON object (string)
- A dictionary with the appropriate structure
- Nested parameters in the appropriate format

### Pydantic Fields

FastMCP supports robust parameter validation through Pydantic’s `Field` class. This is especially useful to ensure that input values meet specific requirements beyond just their type.Note that fields can be used _outside_ Pydantic models to provide metadata and validation constraints. The preferred approach is using `Annotated` with `Field`:


```
from typing import Annotated
from pydantic import Field

@mcp.tool
def analyze_metrics(
# Numbers with range constraints
count: Annotated[int, Field(ge=0, le=100)], # 0 <= count <= 100
ratio: Annotated[float, Field(gt=0, lt=1.0)], # 0 < ratio < 1.0

# String with pattern and length constraints
user_id: Annotated[str, Field(\
pattern=r"^[A-Z]{2}\d{4}$", # Must match regex pattern\
description="User ID in format XX0000"\
)],

# String with length constraints
comment: Annotated[str, Field(min_length=3, max_length=500)] = "",

# Numeric constraints
factor: Annotated[int, Field(multiple_of=5)] = 10, # Must be multiple of 5
):
"""Analyze metrics with validated parameters."""
# Implementation...

```

You can also use `Field` as a default value, though the `Annotated` approach is preferred:


```
@mcp.tool
def validate_data(
# Value constraints
age: int = Field(ge=0, lt=120), # 0 <= age < 120

# String constraints
email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$"), # Email pattern

# Collection constraints
tags: list[str] = Field(min_length=1, max_length=10) # 1-10 tags
):
"""Process data with field validations."""
# Implementation...

```

Common validation options include:

| Validation | Type | Description |
| --- | --- | --- |
| `ge`, `gt` | Number | Greater than (or equal) constraint |
| `le`, `lt` | Number | Less than (or equal) constraint |
| `multiple_of` | Number | Value must be a multiple of this number |
| `min_length`, `max_length` | String, List, etc. | Length constraints |
| `pattern` | String | Regular expression pattern constraint |
| `description` | Any | Human-readable description (appears in schema) |

When a client sends invalid data, FastMCP will return a validation error explaining why the parameter failed validation.

## Server Behavior

### Duplicate Tools

`New in version: 2.1.0` You can control how the FastMCP server behaves if you try to register multiple tools with the same name. This is configured using the `on_duplicate_tools` argument when creating the `FastMCP` instance.


```
from fastmcp import FastMCP

mcp = FastMCP(
name="StrictServer",
# Configure behavior for duplicate tool names
on_duplicate_tools="error"
)

@mcp.tool
def my_tool(): return "Version 1"

# This will now raise a ValueError because 'my_tool' already exists

```

The duplicate behavior options are:

- `"warn"` (default): Logs a warning and the new tool replaces the old one.
- `"error"`: Raises a `ValueError`, preventing the duplicate registration.
- `"replace"`: Silently replaces the existing tool with the new one.
- `"ignore"`: Keeps the original tool and ignores the new registration attempt.

### Removing Tools

`New in version: 2.3.4` You can dynamically remove tools from a server using the `remove_tool` method:


```
from fastmcp import FastMCP

mcp = FastMCP(name="DynamicToolServer")

@mcp.tool
def calculate_sum(a: int, b: int) -> int:
"""Add two numbers together."""
return a + b

mcp.remove_tool("calculate_sum")

```

[Running the Server](https://gofastmcp.com/deployment/running-server) [Resources](https://gofastmcp.com/servers/resources)


================================================================================
# 7. Server Resources
================================================================================

# Basic dynamic resource returning a string

> **Category:** General
> **Source:** gofastmcp.com_servers_resources.json

---

Core Components

Resources & Templates

Resources represent data or files that an MCP client can read, and resource templates extend this concept by allowing clients to request dynamically generated resources based on parameters passed in the URI.FastMCP simplifies defining both static and dynamic resources, primarily using the `@mcp.resource` decorator.

## What Are Resources?

Resources provide read-only access to data for the LLM or client application. When a client requests a resource URI:

1. FastMCP finds the corresponding resource definition.
2. If it’s dynamic (defined by a function), the function is executed.
3. The content (text, JSON, binary data) is returned to the client.

This allows LLMs to access files, database content, configuration, or dynamically generated information relevant to the conversation.

## Resources

### The `@resource` Decorator

The most common way to define a resource is by decorating a Python function. The decorator requires the resource’s unique URI.


```
import json
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

# Basic dynamic resource returning a string
@mcp.resource("resource://greeting")
def get_greeting() -> str:
"""Provides a simple greeting message."""
return "Hello from FastMCP Resources!"

# Resource returning JSON data (dict is auto-serialized)
@mcp.resource("data://config")
def get_config() -> dict:
"""Provides application configuration as JSON."""
return {
"theme": "dark",
"version": "1.2.0",
"features": ["tools", "resources"],
}

```

**Key Concepts:**

- **URI:** The first argument to `@resource` is the unique URI (e.g., `"resource://greeting"`) clients use to request this data.
- **Lazy Loading:** The decorated function ( `get_greeting`, `get_config`) is only executed when a client specifically requests that resource URI via `resources/read`.
- **Inferred Metadata:** By default:

- Resource Name: Taken from the function name ( `get_greeting`).
- Resource Description: Taken from the function’s docstring.

#### Decorator Arguments

You can customize the resource’s properties using arguments in the `@mcp.resource` decorator:


```
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

# Example specifying metadata
@mcp.resource(
uri="data://app-status", # Explicit URI (required)
name="ApplicationStatus", # Custom name
description="Provides the current status of the application.", # Custom description
mime_type="application/json", # Explicit MIME type
tags={"monitoring", "status"}, # Categorization tags
meta={"version": "2.1", "team": "infrastructure"} # Custom metadata
)
def get_application_status() -> dict:
"""Internal function description (ignored if description is provided above)."""
return {"status": "ok", "uptime": 12345, "version": mcp.settings.version} # Example usage

```

## @resource Decorator Arguments

uri

str

required

The unique identifier for the resource

name

str \| None

A human-readable name. If not provided, defaults to function name

description

str \| None

Explanation of the resource. If not provided, defaults to docstring

mime\_type

str \| None

Specifies the content type. FastMCP often infers a default like `text/plain` or `application/json`, but explicit is better for non-text types

tags

set\[str\] \| None

A set of strings used to categorize the resource. These can be used by the server and, in some cases, by clients to filter or group available resources.

enabled

bool

default:"True"

A boolean to enable or disable the resource. See [Disabling Resources](https://gofastmcp.com/servers/resources#disabling-resources) for more information

annotations

Annotations \| dict \| None

An optional `Annotations` object or dictionary to add additional metadata about the resource.

Show Annotations attributes

readOnlyHint

bool \| None

If true, the resource is read-only and does not modify its environment.

idempotentHint

bool \| None

If true, reading the resource repeatedly will have no additional effect on its environment.

meta

dict\[str, Any\] \| None

`New in version: 2.11.0` Optional meta information about the resource. This data is passed through to the MCP client as the `_meta` field of the client-side resource object and can be used for custom metadata, versioning, or other application-specific purposes.

### Return Values

FastMCP automatically converts your function’s return value into the appropriate MCP resource content:

- **`str`**: Sent as `TextResourceContents` (with `mime_type="text/plain"` by default).
- **`dict`, `list`, `pydantic.BaseModel`**: Automatically serialized to a JSON string and sent as `TextResourceContents` (with `mime_type="application/json"` by default).
- **`bytes`**: Base64 encoded and sent as `BlobResourceContents`. You should specify an appropriate `mime_type` (e.g., `"image/png"`, `"application/octet-stream"`).
- **`None`**: Results in an empty resource content list being returned.

### Disabling Resources

`New in version: 2.8.0` You can control the visibility and availability of resources and templates by enabling or disabling them. Disabled resources will not appear in the list of available resources or templates, and attempting to read a disabled resource will result in an “Unknown resource” error.By default, all resources are enabled. You can disable a resource upon creation using the `enabled` parameter in the decorator:


```
@mcp.resource("data://secret", enabled=False)
def get_secret_data():
"""This resource is currently disabled."""
return "Secret data"

```

You can also toggle a resource’s state programmatically after it has been created:


```
@mcp.resource("data://config")
def get_config(): return {"version": 1}

# Disable and re-enable the resource
get_config.disable()
get_config.enable()

```

### Accessing MCP Context

`New in version: 2.2.5` Resources and resource templates can access additional MCP information and features through the `Context` object. To access it, add a parameter to your resource function with a type annotation of `Context`:


```
from fastmcp import FastMCP, Context

mcp = FastMCP(name="DataServer")

@mcp.resource("resource://system-status")
async def get_system_status(ctx: Context) -> dict:
"""Provides system status information."""
return {
"status": "operational",
"request_id": ctx.request_id
}

@mcp.resource("resource://{name}/details")
async def get_details(name: str, ctx: Context) -> dict:
"""Get details for a specific name."""
return {
"name": name,
"accessed_at": ctx.request_id
}

```

For full documentation on the Context object and all its capabilities, see the [Context documentation](https://gofastmcp.com/servers/context).

### Async Resources

Use `async def` for resource functions that perform I/O operations (e.g., reading from a database or network) to avoid blocking the server.


```
import aiofiles
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

@mcp.resource("file:///app/data/important_log.txt", mime_type="text/plain")
async def read_important_log() -> str:
"""Reads content from a specific log file asynchronously."""
try:
async with aiofiles.open("/app/data/important_log.txt", mode="r") as f:
content = await f.read()
return content
except FileNotFoundError:
return "Log file not found."

```

### Resource Classes

While `@mcp.resource` is ideal for dynamic content, you can directly register pre-defined resources (like static files or simple text) using `mcp.add_resource()` and concrete `Resource` subclasses.


```
from pathlib import Path
from fastmcp import FastMCP
from fastmcp.resources import FileResource, TextResource, DirectoryResource

mcp = FastMCP(name="DataServer")

# 1. Exposing a static file directly
readme_path = Path("./README.md").resolve()
if readme_path.exists():
# Use a file:// URI scheme
readme_resource = FileResource(
uri=f"file://{readme_path.as_posix()}",
path=readme_path, # Path to the actual file
name="README File",
description="The project's README.",
mime_type="text/markdown",
tags={"documentation"}
)
mcp.add_resource(readme_resource)

# 2. Exposing simple, predefined text
notice_resource = TextResource(
uri="resource://notice",
name="Important Notice",
text="System maintenance scheduled for Sunday.",
tags={"notification"}
)
mcp.add_resource(notice_resource)

# 3. Using a custom key different from the URI
special_resource = TextResource(
uri="resource://common-notice",
name="Special Notice",
text="This is a special notice with a custom storage key.",
)
mcp.add_resource(special_resource, key="resource://custom-key")

# 4. Exposing a directory listing
data_dir_path = Path("./app_data").resolve()
if data_dir_path.is_dir():
data_listing_resource = DirectoryResource(
uri="resource://data-files",
path=data_dir_path, # Path to the directory
name="Data Directory Listing",
description="Lists files available in the data directory.",
recursive=False # Set to True to list subdirectories
)
mcp.add_resource(data_listing_resource) # Returns JSON list of files

```

**Common Resource Classes:**

- `TextResource`: For simple string content.
- `BinaryResource`: For raw `bytes` content.
- `FileResource`: Reads content from a local file path. Handles text/binary modes and lazy reading.
- `HttpResource`: Fetches content from an HTTP(S) URL (requires `httpx`).
- `DirectoryResource`: Lists files in a local directory (returns JSON).
- ( `FunctionResource`: Internal class used by `@mcp.resource`).

Use these when the content is static or sourced directly from a file/URL, bypassing the need for a dedicated Python function.

#### Custom Resource Keys

`New in version: 2.2.0` When adding resources directly with `mcp.add_resource()`, you can optionally provide a custom storage key:


```
# Creating a resource with standard URI as the key
resource = TextResource(uri="resource://data")
mcp.add_resource(resource) # Will be stored and accessed using "resource://data"

# Creating a resource with a custom key
special_resource = TextResource(uri="resource://special-data")
mcp.add_resource(special_resource, key="internal://data-v2") # Will be stored and accessed using "internal://data-v2"

```

Note that this parameter is only available when using `add_resource()` directly and not through the `@resource` decorator, as URIs are provided explicitly when using the decorator.

### Notifications

`New in version: 2.9.1` FastMCP automatically sends `notifications/resources/list_changed` notifications to connected clients when resources or templates are added, enabled, or disabled. This allows clients to stay up-to-date with the current resource set without manually polling for changes.


```
@mcp.resource("data://example")
def example_resource() -> str:
return "Hello!"

# These operations trigger notifications:
mcp.add_resource(example_resource) # Sends resources/list_changed notification
example_resource.disable() # Sends resources/list_changed notification
example_resource.enable() # Sends resources/list_changed notification

```

Notifications are only sent when these operations occur within an active MCP request context (e.g., when called from within a tool or other MCP operation). Operations performed during server initialization do not trigger notifications.Clients can handle these notifications using a [message handler](https://gofastmcp.com/clients/messages) to automatically refresh their resource lists or update their interfaces.

### Annotations

`New in version: 2.11.0` FastMCP allows you to add specialized metadata to your resources through annotations. These annotations communicate how resources behave to client applications without consuming token context in LLM prompts.Annotations serve several purposes in client applications:

- Indicating whether resources are read-only or may have side effects
- Describing the safety profile of resources (idempotent vs. non-idempotent)
- Helping clients optimize caching and access patterns

You can add annotations to a resource using the `annotations` parameter in the `@mcp.resource` decorator:


```
@mcp.resource(
"data://config",
annotations={
"readOnlyHint": True,
"idempotentHint": True
}
)
def get_config() -> dict:
"""Get application configuration."""
return {"version": "1.0", "debug": False}

```

FastMCP supports these standard annotations:

| Annotation | Type | Default | Purpose |
| --- | --- | --- | --- |
| `readOnlyHint` | boolean | true | Indicates if the resource only provides data without side effects |
| `idempotentHint` | boolean | true | Indicates if repeated reads have the same effect as a single read |

Remember that annotations help make better user experiences but should be treated as advisory hints. They help client applications present appropriate UI elements and optimize access patterns, but won’t enforce behavior on their own. Always focus on making your annotations accurately represent what your resource actually does.

## Resource Templates

Resource Templates allow clients to request resources whose content depends on parameters embedded in the URI. Define a template using the **same `@mcp.resource` decorator**, but include `{parameter_name}` placeholders in the URI string and add corresponding arguments to your function signature.Resource templates share most configuration options with regular resources (name, description, mime\_type, tags, annotations), but add the ability to define URI parameters that map to function parameters.Resource templates generate a new resource for each unique set of parameters, which means that resources can be dynamically created on-demand. For example, if the resource template `"user://profile/{name}"` is registered, MCP clients could request `"user://profile/ford"` or `"user://profile/marvin"` to retrieve either of those two user profiles as resources, without having to register each resource individually.

Functions with `*args` are not supported as resource templates. However, unlike tools and prompts, resource templates do support `**kwargs` because the URI template defines specific parameter names that will be collected and passed as keyword arguments.

Here is a complete example that shows how to define two resource templates:


```
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

# Template URI includes {city} placeholder
@mcp.resource("weather://{city}/current")
def get_weather(city: str) -> dict:
"""Provides weather information for a specific city."""
# In a real implementation, this would call a weather API
return {
"city": city.capitalize(),
"temperature": 22,
"condition": "Sunny",
"unit": "celsius"
}

# Template with multiple parameters and annotations
@mcp.resource(
"repos://{owner}/{repo}/info",
annotations={
"readOnlyHint": True,
"idempotentHint": True
}
)
def get_repo_info(owner: str, repo: str) -> dict:
"""Retrieves information about a GitHub repository."""
# In a real implementation, this would call the GitHub API
return {
"owner": owner,
"name": repo,
"full_name": f"{owner}/{repo}",
"stars": 120,
"forks": 48
}

```

With these two templates defined, clients can request a variety of resources:

- `weather://london/current` → Returns weather for London
- `weather://paris/current` → Returns weather for Paris
- `repos://jlowin/fastmcp/info` → Returns info about the jlowin/fastmcp repository
- `repos://prefecthq/prefect/info` → Returns info about the prefecthq/prefect repository

### Wildcard Parameters

`New in version: 2.2.4`

Please note: FastMCP’s support for wildcard parameters is an **extension** of the Model Context Protocol standard, which otherwise follows RFC 6570. Since all template processing happens in the FastMCP server, this should not cause any compatibility issues with other MCP implementations.

Resource templates support wildcard parameters that can match multiple path segments. While standard parameters ( `{param}`) only match a single path segment and don’t cross ”/” boundaries, wildcard parameters ( `{param*}`) can capture multiple segments including slashes. Wildcards capture all subsequent path segments _up until_ the defined part of the URI template (whether literal or another parameter). This allows you to have multiple wildcard parameters in a single URI template.


```
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

# Standard parameter only matches one segment
@mcp.resource("files://{filename}")
def get_file(filename: str) -> str:
"""Retrieves a file by name."""
# Will only match files://<single-segment>
return f"File content for: {filename}"

# Wildcard parameter can match multiple segments
@mcp.resource("path://{filepath*}")
def get_path_content(filepath: str) -> str:
"""Retrieves content at a specific path."""
# Can match path://docs/server/resources.mdx
return f"Content at path: {filepath}"

# Mixing standard and wildcard parameters
@mcp.resource("repo://{owner}/{path*}/template.py")
def get_template_file(owner: str, path: str) -> dict:
"""Retrieves a file from a specific repository and path, but
only if the resource ends with `template.py`"""
# Can match repo://jlowin/fastmcp/src/resources/template.py
return {
"owner": owner,
"path": path + "/template.py",
"content": f"File at {path}/template.py in {owner}'s repository"
}

```

Wildcard parameters are useful when:

- Working with file paths or hierarchical data
- Creating APIs that need to capture variable-length path segments
- Building URL-like patterns similar to REST APIs

Note that like regular parameters, each wildcard parameter must still be a named parameter in your function signature, and all required function parameters must appear in the URI template.

### Default Values

`New in version: 2.2.0` When creating resource templates, FastMCP enforces two rules for the relationship between URI template parameters and function parameters:

1. **Required Function Parameters:** All function parameters without default values (required parameters) must appear in the URI template.
2. **URI Parameters:** All URI template parameters must exist as function parameters.

However, function parameters with default values don’t need to be included in the URI template. When a client requests a resource, FastMCP will:

- Extract parameter values from the URI for parameters included in the template
- Use default values for any function parameters not in the URI template

This allows for flexible API designs. For example, a simple search template with optional parameters:


```
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

@mcp.resource("search://{query}")
def search_resources(query: str, max_results: int = 10, include_archived: bool = False) -> dict:
"""Search for resources matching the query string."""
# Only 'query' is required in the URI, the other parameters use their defaults
results = perform_search(query, limit=max_results, archived=include_archived)
return {
"query": query,
"max_results": max_results,
"include_archived": include_archived,
"results": results
}

```

With this template, clients can request `search://python` and the function will be called with `query="python", max_results=10, include_archived=False`. MCP Developers can still call the underlying `search_resources` function directly with more specific parameters.An even more powerful pattern is registering a single function with multiple URI templates, allowing different ways to access the same data:


```
from fastmcp import FastMCP

mcp = FastMCP(name="DataServer")

# Define a user lookup function that can be accessed by different identifiers
@mcp.resource("users://email/{email}")
@mcp.resource("users://name/{name}")
def lookup_user(name: str | None = None, email: str | None = None) -> dict:
"""Look up a user by either name or email."""
if email:
return find_user_by_email(email) # pseudocode
elif name:
return find_user_by_name(name) # pseudocode
else:
return {"error": "No lookup parameters provided"}

```

Now an LLM or client can retrieve user information in two different ways:

- `users://email/alice@example.com` → Looks up user by email (with name=None)
- `users://name/Bob` → Looks up user by name (with email=None)

In this stacked decorator pattern:

- The `name` parameter is only provided when using the `users://name/{name}` template
- The `email` parameter is only provided when using the `users://email/{email}` template
- Each parameter defaults to `None` when not included in the URI
- The function logic handles whichever parameter is provided

Templates provide a powerful way to expose parameterized data access points following REST-like principles.

## Error Handling

`New in version: 2.4.1` If your resource function encounters an error, you can raise a standard Python exception ( `ValueError`, `TypeError`, `FileNotFoundError`, custom exceptions, etc.) or a FastMCP `ResourceError`.By default, all exceptions (including their details) are logged and converted into an MCP error response to be sent back to the client LLM. This helps the LLM understand failures and react appropriately.If you want to mask internal error details for security reasons, you can:

1. Use the `mask_error_details=True` parameter when creating your `FastMCP` instance:


```
mcp = FastMCP(name="SecureServer", mask_error_details=True)

```

2. Or use `ResourceError` to explicitly control what error information is sent to clients:


```
from fastmcp import FastMCP
from fastmcp.exceptions import ResourceError

mcp = FastMCP(name="DataServer")

@mcp.resource("resource://safe-error")
def fail_with_details() -> str:
"""This resource provides detailed error information."""
# ResourceError contents are always sent back to clients,
raise ResourceError("Unable to retrieve data: file not found")

@mcp.resource("resource://masked-error")
def fail_with_masked_details() -> str:
"""This resource masks internal error details when mask_error_details=True."""
# This message would be masked if mask_error_details=True
raise ValueError("Sensitive internal file path: /etc/secrets.conf")

@mcp.resource("data://{id}")
def get_data_by_id(id: str) -> dict:
"""Template resources also support the same error handling pattern."""
if id == "secure":
raise ValueError("Cannot access secure data")
elif id == "missing":
raise ResourceError("Data ID 'missing' not found in database")
return {"id": id, "value": "data"}

```

When `mask_error_details=True`, only error messages from `ResourceError` will include details, other exceptions will be converted to a generic message.

## Server Behavior

### Duplicate Resources

`New in version: 2.1.0` You can configure how the FastMCP server handles attempts to register multiple resources or templates with the same URI. Use the `on_duplicate_resources` setting during `FastMCP` initialization.


```
from fastmcp import FastMCP

mcp = FastMCP(
name="ResourceServer",
on_duplicate_resources="error" # Raise error on duplicates
)

@mcp.resource("data://config")
def get_config_v1(): return {"version": 1}

# This registration attempt will raise a ValueError because

```

The duplicate behavior options are:

- `"warn"` (default): Logs a warning, and the new resource/template replaces the old one.
- `"error"`: Raises a `ValueError`, preventing the duplicate registration.
- `"replace"`: Silently replaces the existing resource/template with the new one.
- `"ignore"`: Keeps the original resource/template and ignores the new registration attempt.

[Tools](https://gofastmcp.com/servers/tools) [Prompts](https://gofastmcp.com/servers/prompts)


================================================================================
# 8. Server Prompts
================================================================================

# Basic prompt returning a string (converted to user message automatically)

> **Category:** General
> **Source:** gofastmcp.com_servers_prompts.json

---

Core Components

### Prompts

Prompts are reusable message templates that help LLMs generate structured, purposeful responses. FastMCP simplifies defining these templates, primarily using the `@mcp.prompt` decorator.

## What Are Prompts?

Prompts provide parameterized message templates for LLMs. When a client requests a prompt:

1. FastMCP finds the corresponding prompt definition.
2. If it has parameters, they are validated against your function signature.
3. Your function executes with the validated inputs.
4. The generated message(s) are returned to the LLM to guide its response.

This allows you to define consistent, reusable templates that LLMs can use across different clients and contexts.

## Prompts

### The `@prompt` Decorator

The most common way to define a prompt is by decorating a Python function. The decorator uses the function name as the prompt’s identifier.


```
from fastmcp import FastMCP
from fastmcp.prompts.prompt import Message, PromptMessage, TextContent

mcp = FastMCP(name="PromptServer")

# Basic prompt returning a string (converted to user message automatically)
@mcp.prompt
def ask_about_topic(topic: str) -> str:
"""Generates a user message asking for an explanation of a topic."""
return f"Can you please explain the concept of '{topic}'?"

# Prompt returning a specific message type
@mcp.prompt
def generate_code_request(language: str, task_description: str) -> PromptMessage:
"""Generates a user message requesting code generation."""
content = f"Write a {language} function that performs the following task: {task_description}"
return PromptMessage(role="user", content=TextContent(type="text", text=content))

```

**Key Concepts:**

- **Name:** By default, the prompt name is taken from the function name.
- **Parameters:** The function parameters define the inputs needed to generate the prompt.
- **Inferred Metadata:** By default:

- Prompt Name: Taken from the function name ( `ask_about_topic`).
- Prompt Description: Taken from the function’s docstring.

Functions with `*args` or `**kwargs` are not supported as prompts. This restriction exists because FastMCP needs to generate a complete parameter schema for the MCP protocol, which isn’t possible with variable argument lists.

#### Decorator Arguments

While FastMCP infers the name and description from your function, you can override these and add additional metadata using arguments to the `@mcp.prompt` decorator:


```
@mcp.prompt(
name="analyze_data_request", # Custom prompt name
description="Creates a request to analyze data with specific parameters", # Custom description
tags={"analysis", "data"}, # Optional categorization tags
meta={"version": "1.1", "author": "data-team"} # Custom metadata
)
def data_analysis_prompt(
data_uri: str = Field(description="The URI of the resource containing the data."),
analysis_type: str = Field(default="summary", description="Type of analysis.")
) -> str:
"""This docstring is ignored when description is provided."""
return f"Please perform a '{analysis_type}' analysis on the data found at {data_uri}."

```

## @prompt Decorator Arguments

name

str \| None

Sets the explicit prompt name exposed via MCP. If not provided, uses the function name

description

str \| None

Provides the description exposed via MCP. If set, the function’s docstring is ignored for this purpose

tags

set\[str\] \| None

A set of strings used to categorize the prompt. These can be used by the server and, in some cases, by clients to filter or group available prompts.

enabled

bool

default:"True"

A boolean to enable or disable the prompt. See [Disabling Prompts](https://gofastmcp.com/servers/prompts#disabling-prompts) for more information

meta

dict\[str, Any\] \| None

`New in version: 2.11.0` Optional meta information about the prompt. This data is passed through to the MCP client as the `_meta` field of the client-side prompt object and can be used for custom metadata, versioning, or other application-specific purposes.

### Argument Types

`New in version: 2.9.0` The MCP specification requires that all prompt arguments be passed as strings, but FastMCP allows you to use typed annotations for better developer experience. When you use complex types like `list[int]` or `dict[str, str]`, FastMCP:

1. **Automatically converts** string arguments from MCP clients to the expected types
2. **Generates helpful descriptions** showing the exact JSON string format needed
3. **Preserves direct usage** \- you can still call prompts with properly typed arguments

Since the MCP specification only allows string arguments, clients need to know what string format to use for complex types. FastMCP solves this by automatically enhancing the argument descriptions with JSON schema information, making it clear to both humans and LLMs how to format their arguments.

Python Code

Resulting MCP Prompt


```
@mcp.prompt
def analyze_data(
numbers: list[int],
metadata: dict[str, str],
threshold: float
) -> str:
"""Analyze numerical data."""
avg = sum(numbers) / len(numbers)
return f"Average: {avg}, above threshold: {avg > threshold}"

```

**MCP clients will call this prompt with string arguments:**


```
{
"numbers": "[1, 2, 3, 4, 5]",
"metadata": "{\"source\": \"api\", \"version\": \"1.0\"}",
"threshold": "2.5"
}

```

**But you can still call it directly with proper types:**


```
# This also works for direct calls
result = await prompt.render({
"numbers": [1, 2, 3, 4, 5],
"metadata": {"source": "api", "version": "1.0"},
"threshold": 2.5
})

```

Keep your type annotations simple when using this feature. Complex nested types or custom classes may not convert reliably from JSON strings. The automatically generated schema descriptions are the only guidance users receive about the expected format.Good choices: `list[int]`, `dict[str, str]`, `float`, `bool`
Avoid: Complex Pydantic models, deeply nested structures, custom classes

### Return Values

FastMCP intelligently handles different return types from your prompt function:

- **`str`**: Automatically converted to a single `PromptMessage`.
- **`PromptMessage`**: Used directly as provided. (Note a more user-friendly `Message` constructor is available that can accept raw strings instead of `TextContent` objects.)
- **`list[PromptMessage | str]`**: Used as a sequence of messages (a conversation).
- **`Any`**: If the return type is not one of the above, the return value is attempted to be converted to a string and used as a `PromptMessage`.


```
from fastmcp.prompts.prompt import Message

@mcp.prompt
def roleplay_scenario(character: str, situation: str) -> list[Message]:
"""Sets up a roleplaying scenario with initial messages."""
return [\
Message(f"Let's roleplay. You are {character}. The situation is: {situation}"),\
Message("Okay, I understand. I am ready. What happens next?", role="assistant")\
]

```

### Required vs. Optional Parameters

Parameters in your function signature are considered **required** unless they have a default value.


```
@mcp.prompt
def data_analysis_prompt(
data_uri: str, # Required - no default value
analysis_type: str = "summary", # Optional - has default value
include_charts: bool = False # Optional - has default value
) -> str:
"""Creates a request to analyze data with specific parameters."""
prompt = f"Please perform a '{analysis_type}' analysis on the data found at {data_uri}."
if include_charts:
prompt += " Include relevant charts and visualizations."
return prompt

```

In this example, the client _must_ provide `data_uri`. If `analysis_type` or `include_charts` are omitted, their default values will be used.

### Disabling Prompts

`New in version: 2.8.0` You can control the visibility and availability of prompts by enabling or disabling them. Disabled prompts will not appear in the list of available prompts, and attempting to call a disabled prompt will result in an “Unknown prompt” error.By default, all prompts are enabled. You can disable a prompt upon creation using the `enabled` parameter in the decorator:


```
@mcp.prompt(enabled=False)
def experimental_prompt():
"""This prompt is not ready for use."""
return "This is an experimental prompt."

```

You can also toggle a prompt’s state programmatically after it has been created:


```
@mcp.prompt
def seasonal_prompt(): return "Happy Holidays!"

# Disable and re-enable the prompt
seasonal_prompt.disable()
seasonal_prompt.enable()

```

### Async Prompts

FastMCP seamlessly supports both standard ( `def`) and asynchronous ( `async def`) functions as prompts.


```
# Synchronous prompt
@mcp.prompt
def simple_question(question: str) -> str:
"""Generates a simple question to ask the LLM."""
return f"Question: {question}"

# Asynchronous prompt
@mcp.prompt
async def data_based_prompt(data_id: str) -> str:
"""Generates a prompt based on data that needs to be fetched."""
# In a real scenario, you might fetch data from a database or API
async with aiohttp.ClientSession() as session:
async with session.get(f"https://api.example.com/data/{data_id}") as response:
data = await response.json()
return f"Analyze this data: {data['content']}"

```

Use `async def` when your prompt function performs I/O operations like network requests, database queries, file I/O, or external service calls.

### Accessing MCP Context

`New in version: 2.2.5` Prompts can access additional MCP information and features through the `Context` object. To access it, add a parameter to your prompt function with a type annotation of `Context`:


```
from fastmcp import FastMCP, Context

mcp = FastMCP(name="PromptServer")

@mcp.prompt
async def generate_report_request(report_type: str, ctx: Context) -> str:
"""Generates a request for a report."""
return f"Please create a {report_type} report. Request ID: {ctx.request_id}"

```

For full documentation on the Context object and all its capabilities, see the [Context documentation](https://gofastmcp.com/servers/context).

### Notifications

`New in version: 2.9.1` FastMCP automatically sends `notifications/prompts/list_changed` notifications to connected clients when prompts are added, enabled, or disabled. This allows clients to stay up-to-date with the current prompt set without manually polling for changes.


```
@mcp.prompt
def example_prompt() -> str:
return "Hello!"

# These operations trigger notifications:
mcp.add_prompt(example_prompt) # Sends prompts/list_changed notification
example_prompt.disable() # Sends prompts/list_changed notification
example_prompt.enable() # Sends prompts/list_changed notification

```

Notifications are only sent when these operations occur within an active MCP request context (e.g., when called from within a tool or other MCP operation). Operations performed during server initialization do not trigger notifications.Clients can handle these notifications using a [message handler](https://gofastmcp.com/clients/messages) to automatically refresh their prompt lists or update their interfaces.

## Server Behavior

### Duplicate Prompts

`New in version: 2.1.0` You can configure how the FastMCP server handles attempts to register multiple prompts with the same name. Use the `on_duplicate_prompts` setting during `FastMCP` initialization.


```
from fastmcp import FastMCP

mcp = FastMCP(
name="PromptServer",
on_duplicate_prompts="error" # Raise an error if a prompt name is duplicated
)

@mcp.prompt
def greeting(): return "Hello, how can I help you today?"

# This registration attempt will raise a ValueError because

```

The duplicate behavior options are:

- `"warn"` (default): Logs a warning, and the new prompt replaces the old one.
- `"error"`: Raises a `ValueError`, preventing the duplicate registration.
- `"replace"`: Silently replaces the existing prompt with the new one.
- `"ignore"`: Keeps the original prompt and ignores the new registration attempt.

[Resources](https://gofastmcp.com/servers/resources) [Context](https://gofastmcp.com/servers/context)


================================================================================
# 9. Tools API Reference
================================================================================

# fastmcp.tools.tool

> **Category:** fastmcp.tools.tool
> **Source:** gofastmcp.com_python-sdk_fastmcp-tools-tool.json

---

fastmcp.tools

tool

fastmcp.tools.tool

## Functions

default_serializer


```
default_serializer(data: Any) -> str

```

## Classes

ToolResult

**Methods:**

to_mcp_result


```
to_mcp_result(self) -> list[ContentBlock] | tuple[list[ContentBlock], dict[str, Any]]

```

### Tool

Internal tool registration info.**Methods:**

enable


```
enable(self) -> None

```

disable


```
disable(self) -> None

```

to_mcp_tool


```
to_mcp_tool(self, **overrides: Any) -> MCPTool

```

from_function


```
from_function(fn: Callable[..., Any], name: str | None = None, title: str | None = None, description: str | None = None, tags: set[str] | None = None, annotations: ToolAnnotations | None = None, exclude_args: list[str] | None = None, output_schema: dict[str, Any] | None | NotSetT | Literal[False] = NotSet, serializer: Callable[[Any], str] | None = None, enabled: bool | None = None) -> FunctionTool

```

Create a Tool from a function.

run


```
run(self, arguments: dict[str, Any]) -> ToolResult

```

Run the tool with arguments.This method is not implemented in the base Tool class and must be
implemented by subclasses.`run()` can EITHER return a list of ContentBlocks, or a tuple of
(list of ContentBlocks, dict of structured output).

from_tool


```
from_tool(cls, tool: Tool, transform_fn: Callable[..., Any] | None = None, name: str | None = None, title: str | None | NotSetT = NotSet, transform_args: dict[str, ArgTransform] | None = None, description: str | None | NotSetT = NotSet, tags: set[str] | None = None, annotations: ToolAnnotations | None = None, output_schema: dict[str, Any] | None | Literal[False] = None, serializer: Callable[[Any], str] | None = None, enabled: bool | None = None) -> TransformedTool

```

FunctionTool

**Methods:**

from_function


```
from_function(cls, fn: Callable[..., Any], name: str | None = None, title: str | None = None, description: str | None = None, tags: set[str] | None = None, annotations: ToolAnnotations | None = None, exclude_args: list[str] | None = None, output_schema: dict[str, Any] | None | NotSetT | Literal[False] = NotSet, serializer: Callable[[Any], str] | None = None, enabled: bool | None = None) -> FunctionTool

```

Create a Tool from a function.

run


```
run(self, arguments: dict[str, Any]) -> ToolResult

```

Run the tool with arguments.

ParsedFunction

**Methods:**

from_function


```
from_function(cls, fn: Callable[..., Any], exclude_args: list[str] | None = None, validate: bool = True, wrap_non_object_output_schema: bool = True) -> ParsedFunction

```

[\_\_init\_\_](https://gofastmcp.com/python-sdk/fastmcp-tools-__init__) [tool\_manager](https://gofastmcp.com/python-sdk/fastmcp-tools-tool_manager)


================================================================================
# 10. Resources API Reference
================================================================================

# fastmcp.resources.resource

> **Category:** fastmcp.resources.resource
> **Source:** gofastmcp.com_python-sdk_fastmcp-resources-resource.json

---

fastmcp.resources

resource

fastmcp.resources.resource

Base classes and interfaces for FastMCP resources.

## Classes

### Resource

Base class for all resources.**Methods:**

enable


```
enable(self) -> None

```

disable


```
disable(self) -> None

```

from_function


```
from_function(fn: Callable[..., Any], uri: str | AnyUrl, name: str | None = None, title: str | None = None, description: str | None = None, mime_type: str | None = None, tags: set[str] | None = None, enabled: bool | None = None) -> FunctionResource

```

set_default_mime_type


```
set_default_mime_type(cls, mime_type: str | None) -> str

```

Set default MIME type if not provided.

set_default_name


```
set_default_name(self) -> Self

```

Set default name from URI if not provided.

read


```
read(self) -> str | bytes

```

Read the resource content.

to_mcp_resource


```
to_mcp_resource(self, **overrides: Any) -> MCPResource

```

Convert the resource to an MCPResource.

key


```
key(self) -> str

```

The key of the component. This is used for internal bookkeeping
and may reflect e.g. prefixes or other identifiers. You should not depend on
keys having a certain value, as the same tool loaded from different
hierarchies of servers may have different keys.

FunctionResource

A resource that defers data loading by wrapping a function.The function is only called when the resource is read, allowing for lazy loading
of potentially expensive data. This is particularly useful when listing resources,
as the function won’t be called until the resource is actually accessed.The function can return:

- str for text content (default)
- bytes for binary content
- other types will be converted to JSON

**Methods:**

from_function


```
from_function(cls, fn: Callable[..., Any], uri: str | AnyUrl, name: str | None = None, title: str | None = None, description: str | None = None, mime_type: str | None = None, tags: set[str] | None = None, enabled: bool | None = None) -> FunctionResource

```

Create a FunctionResource from a function.

read


```
read(self) -> str | bytes

```

Read the resource by calling the wrapped function.

[\_\_init\_\_](https://gofastmcp.com/python-sdk/fastmcp-resources-__init__) [resource\_manager](https://gofastmcp.com/python-sdk/fastmcp-resources-resource_manager)


================================================================================
# 11. Prompts API Reference
================================================================================

# fastmcp.prompts.prompt

> **Category:** fastmcp.prompts.prompt
> **Source:** gofastmcp.com_python-sdk_fastmcp-prompts-prompt.json

---

fastmcp.prompts

prompt

fastmcp.prompts.prompt

Base classes for FastMCP prompts.

## Functions

### Message


```
Message(content: str | ContentBlock, role: Role | None = None, **kwargs: Any) -> PromptMessage

```

A user-friendly constructor for PromptMessage.

## Classes

PromptArgument

An argument that can be passed to a prompt.

### Prompt

A prompt template that can be rendered with parameters.**Methods:**

enable


```
enable(self) -> None

```

disable


```
disable(self) -> None

```

to_mcp_prompt


```
to_mcp_prompt(self, **overrides: Any) -> MCPPrompt

```

Convert the prompt to an MCP prompt.

from_function


```
from_function(fn: Callable[..., PromptResult | Awaitable[PromptResult]], name: str | None = None, title: str | None = None, description: str | None = None, tags: set[str] | None = None, enabled: bool | None = None) -> FunctionPrompt

```

Create a Prompt from a function.The function can return:

- A string (converted to a message)
- A Message object
- A dict (converted to a message)
- A sequence of any of the above

render


```
render(self, arguments: dict[str, Any] | None = None) -> list[PromptMessage]

```

Render the prompt with arguments.

FunctionPrompt

A prompt that is a function.**Methods:**

from_function


```
from_function(cls, fn: Callable[..., PromptResult | Awaitable[PromptResult]], name: str | None = None, title: str | None = None, description: str | None = None, tags: set[str] | None = None, enabled: bool | None = None) -> FunctionPrompt

```

Create a Prompt from a function.The function can return:

- A string (converted to a message)
- A Message object
- A dict (converted to a message)
- A sequence of any of the above

render


```
render(self, arguments: dict[str, Any] | None = None) -> list[PromptMessage]

```

Render the prompt with arguments.

[\_\_init\_\_](https://gofastmcp.com/python-sdk/fastmcp-prompts-__init__) [prompt\_manager](https://gofastmcp.com/python-sdk/fastmcp-prompts-prompt_manager)


================================================================================
# 12. Server Context
================================================================================

# Context is available as the ctx parameter

> **Category:** General
> **Source:** gofastmcp.com_servers_context.json

---

Advanced Features

MCP Context

When defining FastMCP [tools](https://gofastmcp.com/servers/tools), [resources](https://gofastmcp.com/servers/resources), resource templates, or [prompts](https://gofastmcp.com/servers/prompts), your functions might need to interact with the underlying MCP session or access advanced server capabilities. FastMCP provides the `Context` object for this purpose.

## What Is Context?

The `Context` object provides a clean interface to access MCP features within your functions, including:

- **Logging**: Send debug, info, warning, and error messages back to the client
- **Progress Reporting**: Update the client on the progress of long-running operations
- **Resource Access**: Read data from resources registered with the server
- **LLM Sampling**: Request the client’s LLM to generate text based on provided messages
- **User Elicitation**: Request structured input from users during tool execution
- **State Management**: Store and share data across middleware and tool calls within a request
- **Request Information**: Access metadata about the current request
- **Server Access**: When needed, access the underlying FastMCP server instance

## Accessing the Context

### Via Dependency Injection

To use the context object within any of your functions, simply add a parameter to your function signature and type-hint it as `Context`. FastMCP will automatically inject the context instance when your function is called.**Key Points:**

- The parameter name (e.g., `ctx`, `context`) doesn’t matter, only the type hint `Context` is important.
- The context parameter can be placed anywhere in your function’s signature; it will not be exposed to MCP clients as a valid parameter.
- The context is optional - functions that don’t need it can omit the parameter entirely.
- Context methods are async, so your function usually needs to be async as well.
- The type hint can be a union ( `Context | None`) or use `Annotated[]` and it will still work properly.
- Context is only available during a request; attempting to use context methods outside a request will raise errors. If you need to debug or call your context methods outside of a request, you can type your variable as `Context | None=None` to avoid missing argument errors.

#### Tools


```
from fastmcp import FastMCP, Context

mcp = FastMCP(name="Context Demo")

@mcp.tool
async def process_file(file_uri: str, ctx: Context) -> str:
"""Processes a file, using context for logging and resource access."""
# Context is available as the ctx parameter
return "Processed file"

```

#### Resources and Templates

`New in version: 2.2.5`


```
from fastmcp import FastMCP, Context

mcp = FastMCP(name="Context Demo")

@mcp.resource("resource://user-data")
async def get_user_data(ctx: Context) -> dict:
"""Fetch personalized user data based on the request context."""
# Context is available as the ctx parameter
return {"user_id": "example"}

@mcp.resource("resource://users/{user_id}/profile")
async def get_user_profile(user_id: str, ctx: Context) -> dict:
"""Fetch user profile with context-aware logging."""
# Context is available as the ctx parameter
return {"id": user_id}

```

#### Prompts

`New in version: 2.2.5`


```
from fastmcp import FastMCP, Context

mcp = FastMCP(name="Context Demo")

@mcp.prompt
async def data_analysis_request(dataset: str, ctx: Context) -> str:
"""Generate a request to analyze data with contextual information."""
# Context is available as the ctx parameter
return f"Please analyze the following dataset: {dataset}"

```

### Via Dependency Function

`New in version: 2.2.11` While the simplest way to access context is through function parameter injection as shown above, there are cases where you need to access the context in code that may not be easy to modify to accept a context parameter, or that is nested deeper within your function calls.FastMCP provides dependency functions that allow you to retrieve the active context from anywhere within a server request’s execution flow:


```
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_context

mcp = FastMCP(name="Dependency Demo")

# Utility function that needs context but doesn't receive it as a parameter
async def process_data(data: list[float]) -> dict:
# Get the active context - only works when called within a request
ctx = get_context()
await ctx.info(f"Processing {len(data)} data points")

@mcp.tool
async def analyze_dataset(dataset_name: str) -> dict:
# Call utility function that uses context internally
data = load_data(dataset_name)
await process_data(data)

```

**Important Notes:**

- The `get_context` function should only be used within the context of a server request. Calling it outside of a request will raise a `RuntimeError`.
- The `get_context` function is server-only and should not be used in client code.

## Context Capabilities

FastMCP provides several advanced capabilities through the context object. Each capability has dedicated documentation with comprehensive examples and best practices:

### Logging

Send debug, info, warning, and error messages back to the MCP client for visibility into function execution.


```
await ctx.debug("Starting analysis")
await ctx.info(f"Processing {len(data)} items")
await ctx.warning("Deprecated parameter used")
await ctx.error("Processing failed")

```

See [Server Logging](https://gofastmcp.com/servers/logging) for complete documentation and examples.

### Client Elicitation

`New in version: 2.10.0` Request structured input from clients during tool execution, enabling interactive workflows and progressive disclosure. This is a new feature in the 6/18/2025 MCP spec.


```
result = await ctx.elicit("Enter your name:", response_type=str)
if result.action == "accept":
name = result.data

```

See [User Elicitation](https://gofastmcp.com/servers/elicitation) for detailed examples and supported response types.

### LLM Sampling

`New in version: 2.0.0` Request the client’s LLM to generate text based on provided messages, useful for leveraging AI capabilities within your tools.


```
response = await ctx.sample("Analyze this data", temperature=0.7)

```

See [LLM Sampling](https://gofastmcp.com/servers/sampling) for comprehensive usage and advanced techniques.

### Progress Reporting

Update clients on the progress of long-running operations, enabling progress indicators and better user experience.


```
await ctx.report_progress(progress=50, total=100) # 50% complete

```

See [Progress Reporting](https://gofastmcp.com/servers/progress) for detailed patterns and examples.

### Resource Access

Read data from resources registered with your FastMCP server, allowing access to files, configuration, or dynamic content.


```
content_list = await ctx.read_resource("resource://config")
content = content_list[0].content

```

**Method signature:**

- **`ctx.read_resource(uri: str | AnyUrl) -> list[ReadResourceContents]`**: Returns a list of resource content parts

### State Management

`New in version: 2.11.0` Store and share data across middleware and tool calls within a request. Context objects maintain a state dictionary that’s especially useful for passing information from [middleware](https://gofastmcp.com/servers/middleware) to your tools.To store a value in the context state, use `ctx.set_state(key, value)`. To retrieve a value, use `ctx.get_state(key)`.This simplified example shows how to use MCP middleware to store user info in the context state, and how to access that state in a tool:


```
from fastmcp.server.middleware import Middleware, MiddlewareContext

class UserAuthMiddleware(Middleware):
async def on_call_tool(self, context: MiddlewareContext, call_next):

# Middleware stores user info in context state
context.fastmcp_context.set_state("user_id", "user_123")
context.fastmcp_context.set_state("permissions", ["read", "write"])

return await call_next()

@mcp.tool
async def secure_operation(data: str, ctx: Context) -> str:
"""Tool can access state set by middleware."""

user_id = ctx.get_state("user_id") # "user_123"
permissions = ctx.get_state("permissions") # ["read", "write"]

if "write" not in permissions:
return "Access denied"

return f"Processing {data} for user {user_id}"

```

**Method signatures:**

- **`ctx.set_state_value(key: str, value: Any) -> None`**: Store a value in the context state
- **`ctx.get_state_value(key: str) -> Any`**: Retrieve a value from the context state (returns None if not found)

**State Inheritance:**
When a new context is created (nested contexts), it inherits a copy of its parent’s state. This ensures that:

- State set on a child context never affects the parent context
- State set on a parent context after the child context is initialized is not propagated to the child context

This makes state management predictable and prevents unexpected side effects between nested operations.

### Change Notifications

`New in version: 2.9.1` FastMCP automatically sends list change notifications when components (such as tools, resources, or prompts) are added, removed, enabled, or disabled. In rare cases where you need to manually trigger these notifications, you can use the context methods:


```
@mcp.tool
async def custom_tool_management(ctx: Context) -> str:
"""Example of manual notification after custom tool changes."""
# After making custom changes to tools
await ctx.send_tool_list_changed()
await ctx.send_resource_list_changed()
await ctx.send_prompt_list_changed()
return "Notifications sent"

```

These methods are primarily used internally by FastMCP’s automatic notification system and most users will not need to invoke them directly.

### FastMCP Server

To access the underlying FastMCP server instance, you can use the `ctx.fastmcp` property:


```
@mcp.tool
async def my_tool(ctx: Context) -> None:
# Access the FastMCP server instance
server_name = ctx.fastmcp.name
...

```

### MCP Request

Access metadata about the current request and client.


```
@mcp.tool
async def request_info(ctx: Context) -> dict:
"""Return information about the current request."""
return {
"request_id": ctx.request_id,
"client_id": ctx.client_id or "Unknown client"
}

```

**Available Properties:**

- **`ctx.request_id -> str`**: Get the unique ID for the current MCP request
- **`ctx.client_id -> str | None`**: Get the ID of the client making the request, if provided during initialization
- **`ctx.session_id -> str | None`**: Get the MCP session ID for session-based data sharing (HTTP transports only)

The MCP request is part of the low-level MCP SDK and intended for advanced use cases. Most users will not need to use it directly.

[Prompts](https://gofastmcp.com/servers/prompts) [Proxy Servers](https://gofastmcp.com/servers/proxy)


================================================================================
# 13. Context API Reference
================================================================================

# fastmcp.server.context

> **Category:** fastmcp.server.context
> **Source:** gofastmcp.com_python-sdk_fastmcp-server-context.json

---

context

fastmcp.server.context

## Functions

set_context


```
set_context(context: Context) -> Generator[Context, None, None]

```

## Classes

### Context

Context object providing access to MCP capabilities.This provides a cleaner interface to MCP’s RequestContext functionality.
It gets injected into tool and resource functions that request it via type hints.To use context in a tool function, add a parameter with the Context type annotation:


```
@server.tool
def my_tool(x: int, ctx: Context) -> str:
# Log messages to the client
ctx.info(f"Processing {x}")
ctx.debug("Debug info")
ctx.warning("Warning message")
ctx.error("Error message")

# Report progress
ctx.report_progress(50, 100, "Processing")

# Access resources
data = ctx.read_resource("resource://data")

# Get request info
request_id = ctx.request_id
client_id = ctx.client_id

# Manage state across the request
ctx.set_state_value("key", "value")
value = ctx.get_state_value("key")

return str(x)

```

State Management:
Context objects maintain a state dictionary that can be used to store and share
data across middleware and tool calls within a request. When a new context
is created (nested contexts), it inherits a copy of its parent’s state, ensuring
that modifications in child contexts don’t affect parent contexts.The context parameter name can be anything as long as it’s annotated with Context.
The context is optional - tools that don’t need it can omit the parameter.**Methods:**

request_context


```
request_context(self) -> RequestContext

```

Access to the underlying request context.If called outside of a request context, this will raise a ValueError.

report_progress


```
report_progress(self, progress: float, total: float | None = None, message: str | None = None) -> None

```

Report progress for the current operation.**Args:**

- `progress`: Current progress value e.g. 24
- `total`: Optional total value e.g. 100

read_resource


```
read_resource(self, uri: str | AnyUrl) -> list[ReadResourceContents]

```

Read a resource by URI.**Args:**

- `uri`: Resource URI to read

**Returns:**

- The resource content as either text or bytes

log


```
log(self, message: str, level: LoggingLevel | None = None, logger_name: str | None = None) -> None

```

Send a log message to the client.**Args:**

- `message`: Log message
- `level`: Optional log level. One of “debug”, “info”, “notice”, “warning”, “error”, “critical”,
“alert”, or “emergency”. Default is “info”.
- `logger_name`: Optional logger name

client_id


```
client_id(self) -> str | None

```

Get the client ID if available.

request_id


```
request_id(self) -> str

```

Get the unique ID for this request.

session_id


```
session_id(self) -> str | None

```

Get the MCP session ID for HTTP transports.Returns the session ID that can be used as a key for session-based
data storage (e.g., Redis) to share data between tool calls within
the same client session.**Returns:**

- The session ID for HTTP transports (SSE, StreamableHTTP), or None
- for stdio and in-memory transports which don’t use session IDs.

session


```
session(self) -> ServerSession

```

Access to the underlying session for advanced usage.

debug


```
debug(self, message: str, logger_name: str | None = None) -> None

```

Send a debug log message.

info


```
info(self, message: str, logger_name: str | None = None) -> None

```

Send an info log message.

warning


```
warning(self, message: str, logger_name: str | None = None) -> None

```

Send a warning log message.

error


```
error(self, message: str, logger_name: str | None = None) -> None

```

Send an error log message.

list_roots


```
list_roots(self) -> list[Root]

```

List the roots available to the server, as indicated by the client.

send_tool_list_changed


```
send_tool_list_changed(self) -> None

```

Send a tool list changed notification to the client.

send_resource_list_changed


```
send_resource_list_changed(self) -> None

```

Send a resource list changed notification to the client.

send_prompt_list_changed


```
send_prompt_list_changed(self) -> None

```

Send a prompt list changed notification to the client.

sample


```
sample(self, messages: str | list[str | SamplingMessage], system_prompt: str | None = None, include_context: IncludeContext | None = None, temperature: float | None = None, max_tokens: int | None = None, model_preferences: ModelPreferences | str | list[str] | None = None) -> ContentBlock

```

Send a sampling request to the client and await the response.Call this method at any time to have the server request an LLM
completion from the client. The client must be appropriately configured,
or the request will error.

elicit


```
elicit(self, message: str, response_type: None) -> AcceptedElicitation[dict[str, Any]] | DeclinedElicitation | CancelledElicitation

```

elicit


```
elicit(self, message: str, response_type: type[T]) -> AcceptedElicitation[T] | DeclinedElicitation | CancelledElicitation

```

elicit


```
elicit(self, message: str, response_type: list[str]) -> AcceptedElicitation[str] | DeclinedElicitation | CancelledElicitation

```

elicit


```
elicit(self, message: str, response_type: type[T] | list[str] | None = None) -> AcceptedElicitation[T] | AcceptedElicitation[dict[str, Any]] | AcceptedElicitation[str] | DeclinedElicitation | CancelledElicitation

```

Send an elicitation request to the client and await the response.Call this method at any time to request additional information from
the user through the client. The client must support elicitation,
or the request will error.Note that the MCP protocol only supports simple object schemas with
primitive types. You can provide a dataclass, TypedDict, or BaseModel to
comply. If you provide a primitive type, an object schema with a single
“value” field will be generated for the MCP interaction and
automatically deconstructed into the primitive type upon response.If the response\_type is None, the generated schema will be that of an
empty object in order to comply with the MCP protocol requirements.
Clients must send an empty object ("")in response.**Args:**

- `message`: A human-readable message explaining what information is needed
- `response_type`: The type of the response, which should be a primitive
type or dataclass or BaseModel. If it is a primitive type, an
object schema with a single “value” field will be generated.

get_http_request


```
get_http_request(self) -> Request

```

Get the active starlette request.

set_state


```
set_state(self, key: str, value: Any) -> None

```

Set a value in the context state.

get_state


```
get_state(self, key: str) -> Any

```

Get a value from the context state. Returns None if the key is not found.

[in\_memory](https://gofastmcp.com/python-sdk/fastmcp-server-auth-providers-in_memory) [dependencies](https://gofastmcp.com/python-sdk/fastmcp-server-dependencies)


================================================================================
# 14. Testing Your Server
================================================================================

# Pass the server directly to the Client constructor

> **Category:** Patterns
> **Source:** gofastmcp.com_patterns_testing.json

---

### Patterns

Testing MCP Servers

Testing your MCP servers thoroughly is essential for ensuring they work correctly when deployed. FastMCP makes this easy through a variety of testing patterns.

## In-Memory Testing

The most efficient way to test an MCP server is to pass your FastMCP server instance directly to a Client. This enables in-memory testing without having to start a separate server process, which is particularly useful because managing an MCP server programmatically can be challenging.Here is an example of using a `Client` to test a server with pytest:


```
import pytest
from fastmcp import FastMCP, Client

@pytest.fixture
def mcp_server():
server = FastMCP("TestServer")

@server.tool
def greet(name: str) -> str:
return f"Hello, {name}!"

return server

async def test_tool_functionality(mcp_server):
# Pass the server directly to the Client constructor
async with Client(mcp_server) as client:
result = await client.call_tool("greet", {"name": "World"})
assert result.data == "Hello, World!"

```

This pattern creates a direct connection between the client and server, allowing you to test your server’s functionality efficiently.

If you’re using pytest for async tests, as shown above, you may need to configure appropriate markers or set `asyncio_mode = "auto"` in your pytest configuration in order to handle async test functions automatically.

## Mocking

FastMCP servers are designed to work seamlessly with standard Python testing tools and patterns. There’s nothing special about testing FastMCP servers - you can use all the familiar Python mocking, patching, and testing techniques you already know.

[HTTP Requests](https://gofastmcp.com/patterns/http-requests) [CLI](https://gofastmcp.com/patterns/cli)


================================================================================
# 15. Running & Deploying Servers
================================================================================

# Run with a specific Python version

> **Category:** Deployment
> **Source:** gofastmcp.com_deployment_running-server.json

---

### Essentials

Running Your FastMCP Server

FastMCP servers can be run in different ways depending on your application’s needs, from local command-line tools to persistent web services. This guide covers the primary methods for running your server, focusing on the available transport protocols: STDIO, Streamable HTTP, and SSE.

## The `run()` Method

FastMCP servers can be run directly from Python by calling the `run()` method on a `FastMCP` instance.

For maximum compatibility, it’s best practice to place the `run()` call within an `if __name__ == "__main__":` block. This ensures the server starts only when the script is executed directly, not when imported as a module.

my\_server.py


```
from fastmcp import FastMCP

mcp = FastMCP(name="MyServer")

@mcp.tool
def hello(name: str) -> str:
return f"Hello, {name}!"

if __name__ == "__main__":
mcp.run()

```

You can now run this MCP server by executing `python my_server.py`.MCP servers can be run with a variety of different transport options, depending on your application’s requirements. The `run()` method can take a `transport` argument and other transport-specific keyword arguments to configure how the server operates.

## The FastMCP CLI

FastMCP also provides a command-line interface for running servers without modifying the source code. After installing FastMCP, you can run your server directly from the command line:


```
fastmcp run server.py

```

**Important**: When using `fastmcp run`, it **ignores** the `if __name__ == "__main__"` block entirely. Instead, it looks for a FastMCP object named `mcp`, `server`, or `app` and calls its `run()` method directly with the transport options you specify.This means you can use `fastmcp run` to override the transport specified in your code, which is particularly useful for testing or changing deployment methods without modifying the code.

You can specify transport options and other configuration:


```
fastmcp run server.py --transport sse --port 9000

```

### Dependency Management with CLI

When using the FastMCP CLI, you can pass additional options to configure how `uv` runs your server:


```
# Run with a specific Python version
fastmcp run server.py --python 3.11

# Run with additional packages
fastmcp run server.py --with pandas --with numpy

# Run with dependencies from a requirements file
fastmcp run server.py --with-requirements requirements.txt

# Combine multiple options
fastmcp run server.py --python 3.10 --with httpx --transport http

# Run within a specific project directory
fastmcp run server.py --project /path/to/project

```

When using `--python`, `--with`, `--project`, or `--with-requirements`, the server runs via `uv run` subprocess instead of using your local environment. The `uv` command will manage dependencies based on your project configuration.

The `--python` option is particularly useful when you need to run a server with a specific Python version that differs from your system’s default. This addresses common compatibility issues where servers require a particular Python version to function correctly.

For development and testing, you can use the `dev` command to run your server with the MCP Inspector:


```
fastmcp dev server.py

```

The `dev` command also supports the same dependency management options:


```
# Dev server with specific Python version and packages
fastmcp dev server.py --python 3.11 --with pandas

```

See the [CLI documentation](https://gofastmcp.com/patterns/cli) for detailed information about all available commands and options.

### Passing Arguments to Servers

When servers accept command line arguments (using argparse, click, or other libraries), you can pass them after `--`:


```
fastmcp run config_server.py -- --config config.json
fastmcp run database_server.py -- --database-path /tmp/db.sqlite --debug

```

This is useful for servers that need configuration files, database paths, API keys, or other runtime options.

## Transport Options

Below is a comparison of available transport options to help you choose the right one for your needs:

| Transport | Use Cases | Recommendation |
| --- | --- | --- |
| **STDIO** | Local tools, command-line scripts, and integrations with clients like Claude Desktop | Best for local tools and when clients manage server processes |
| **Streamable HTTP** | Web-based deployments, microservices, exposing MCP over a network | Recommended choice for web-based deployments |
| **SSE** | Existing web-based deployments that rely on SSE | Deprecated - prefer Streamable HTTP for new projects |

### STDIO

The STDIO transport is the default and most widely compatible option for local MCP server execution. It is ideal for local tools, command-line integrations, and clients like Claude Desktop. However, it has the disadvantage of having to run the MCP code locally, which can introduce security concerns with third-party servers.STDIO is the default transport, so you don’t need to specify it when calling `run()`. However, you can specify it explicitly to make your intent clear:


```
from fastmcp import FastMCP

mcp = FastMCP()

if __name__ == "__main__":
mcp.run(transport="stdio")

```

When using Stdio transport, you will typically _not_ run the server yourself as a separate process. Rather, your _clients_ will spin up a new server process for each session. As such, no additional configuration is required.

### Streamable HTTP

`New in version: 2.3.0` Streamable HTTP is a modern, efficient transport for exposing your MCP server via HTTP. It is the recommended transport for web-based deployments.To run a server using Streamable HTTP, you can use the `run()` method with the `transport` argument set to `"http"`. This will start a Uvicorn server on the default host ( `127.0.0.1`), port ( `8000`), and path ( `/mcp/`).

server.py

client.py


```
from fastmcp import FastMCP

mcp = FastMCP()

if __name__ == "__main__":
mcp.run(transport="http")

```

For backward compatibility, wherever `"http"` is accepted as a transport name, you can also pass `"streamable-http"` as a fully supported alias. This is particularly useful when upgrading from FastMCP 1.x in the official Python SDK and FastMCP <= 2.9, where `"streamable-http"` was the standard name.

To customize the host, port, path, or log level, provide appropriate keyword arguments to the `run()` method.

server.py

client.py


```
from fastmcp import FastMCP

mcp = FastMCP()

if __name__ == "__main__":
mcp.run(
transport="http",
host="127.0.0.1",
port=4200,
path="/my-custom-path",
log_level="debug",
)

```

### SSE

The SSE transport is deprecated and may be removed in a future version.
New applications should use Streamable HTTP transport instead.

Server-Sent Events (SSE) is an HTTP-based protocol for server-to-client streaming. While FastMCP still supports SSE, it is deprecated and Streamable HTTP is preferred for new projects.To run a server using SSE, you can use the `run()` method with the `transport` argument set to `"sse"`. This will start a Uvicorn server on the default host ( `127.0.0.1`), port ( `8000`), and with default SSE path ( `/sse/`) and message path ( `/messages/`).

server.py

client.py


```
from fastmcp import FastMCP

mcp = FastMCP()

if __name__ == "__main__":
mcp.run(transport="sse")

```

Notice that the client in the above example uses an explicit `SSETransport` to connect to the server. FastMCP will attempt to infer the appropriate transport from the provided configuration, but HTTP URLs are assumed to be Streamable HTTP (as of FastMCP 2.3.0).

To customize the host, port, or log level, provide appropriate keyword arguments to the `run()` method. You can also adjust the SSE path (which clients should connect to) and the message POST endpoint (which clients use to send subsequent messages).

server.py

client.py


```
from fastmcp import FastMCP

mcp = FastMCP()

if __name__ == "__main__":
mcp.run(
transport="sse",
host="127.0.0.1",
port=4200,
log_level="debug",
path="/my-custom-sse-path",
)

```

## Async Usage

FastMCP provides both synchronous and asynchronous APIs for running your server. The `run()` method seen in previous examples is a synchronous method that internally uses `anyio.run()` to run the asynchronous server. For applications that are already running in an async context, FastMCP provides the `run_async()` method.


```
from fastmcp import FastMCP
import asyncio

mcp = FastMCP(name="MyServer")

@mcp.tool
def hello(name: str) -> str:
return f"Hello, {name}!"

async def main():
# Use run_async() in async contexts
await mcp.run_async(transport="http")

if __name__ == "__main__":
asyncio.run(main())

```

The `run()` method cannot be called from inside an async function because it already creates its own async event loop internally. If you attempt to call `run()` from inside an async function, you’ll get an error about the event loop already running.Always use `run_async()` inside async functions and `run()` in synchronous contexts.

Both `run()` and `run_async()` accept the same transport arguments, so all the examples above apply to both methods.

## Custom Routes

You can also add custom web routes to your FastMCP server, which will be exposed alongside the MCP endpoint. To do so, use the `@custom_route` decorator. Note that this is less flexible than using a full ASGI framework, but can be useful for adding simple endpoints like health checks to your standalone server.


```
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

mcp = FastMCP("MyServer")

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
return PlainTextResponse("OK")

if __name__ == "__main__":
mcp.run()

```

[Overview](https://gofastmcp.com/servers/server) [Tools](https://gofastmcp.com/servers/tools)


---

## About This Guide

This guide was automatically generated by combining essential FastMCP documentation files.
It provides a comprehensive learning path for building MCP servers with FastMCP.

**Generated from 15 source files.**

For the most up-to-date information, refer to the individual documentation files
in the FastMCP documentation directory.

---
*FastMCP - The fast, Pythonic way to build MCP servers and clients*