# Integrations Gemini
# Integrations Gemini

> **Category:** Integrations
> **Source:** gofastmcp.com_integrations_gemini.json

---

Integrations

Gemini SDK 🤝 FastMCP

Google’s Gemini API includes built-in support for MCP servers in their Python and JavaScript SDKs, allowing you to connect directly to MCP servers and use their tools seamlessly with Gemini models.

## Gemini Python SDK

Google’s [Gemini Python SDK](https://ai.google.dev/gemini-api/docs) can use FastMCP clients directly.

Google’s MCP integration is currently experimental and available in the Python and JavaScript SDKs. The API automatically calls MCP tools when needed and can connect to both local and remote MCP servers.

Currently, Gemini’s MCP support only accesses **tools** from MCP servers,it queries the `list_tools` endpoint and exposes those functions to the AI. Other MCP features like resources and prompts are not currently supported.

### Create a Server

First, create a FastMCP server with the tools you want to expose. For this example, we’ll create a server with a single tool that rolls dice.

server.py

Copy

```
import random
from fastmcp import FastMCP

mcp = FastMCP(name="Dice Roller")

@mcp.tool
def roll_dice(n_dice: int) -> list[int]:
"""Roll `n_dice` 6-sided dice and return the results."""
return [random.randint(1, 6) for _ in range(n_dice)]

if __name__ == "__main__":
mcp.run()

```

### Call the Server

To use the Gemini API with MCP, you’ll need to install the Google Generative AI SDK:

Copy

```
pip install google-genai

```

You’ll also need to authenticate with Google. You can do this by setting the `GEMINI_API_KEY` environment variable. Consult the Gemini SDK documentation for more information.

Copy

```
export GEMINI_API_KEY="your-api-key"

```

Gemini’s SDK interacts directly with the MCP client session. To call the server, you’ll need to instantiate a FastMCP client, enter its connection context, and pass the client session to the Gemini SDK.

Copy

```
from fastmcp import Client
from google import genai
import asyncio

mcp_client = Client("server.py")
gemini_client = genai.Client()

async def main():
async with mcp_client:
response = await gemini_client.aio.models.generate_content(
model="gemini-2.0-flash",
contents="Roll 3 dice!",
config=genai.types.GenerateContentConfig(
temperature=0,
tools=[mcp_client.session], # Pass the FastMCP client session
),
)
print(response.text)

if __name__ == "__main__":
asyncio.run(main())

```

If you run this code, you’ll see output like:

Copy

```
Okay, I rolled 3 dice and got a 5, 4, and 1.

```

### Remote & Authenticated Servers

In the above example, we connected to our local server using `stdio` transport. Because we’re using a FastMCP client, you can also connect to any local or remote MCP server, using any [transport](https://gofastmcp.com/clients/transports) or [auth](https://gofastmcp.com/clients/auth) method supported by FastMCP, simply by changing the client configuration.For example, to connect to a remote, authenticated server, you can use the following client:

Copy

```
from fastmcp import Client
from fastmcp.client.auth import BearerAuth

mcp_client = Client(
"https://my-server.com/mcp/",
auth=BearerAuth("<your-token>"),
)

```

The rest of the code remains the same.

[FastAPI](https://gofastmcp.com/integrations/fastapi) [MCP JSON](https://gofastmcp.com/integrations/mcp-json-configuration)