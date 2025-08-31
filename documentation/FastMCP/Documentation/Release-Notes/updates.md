# Updates
# Updates

> **Category:** Release Notes
> **Source:** gofastmcp.com_updates.json

---

FastMCP Updates

FiltersClear

Blog PostsReleasesTutorialsAnnouncements

FastMCP 2.9

ReleasesBlog Posts

June 23, 2025

[![_image?href=%2F_astro%2Fhero.BkVTdeBk](https://jlowin.dev/_image?href=%2F_astro%2Fhero.BkVTdeBk.jpg&w=1200&h=630&f=png)\\
\\
**FastMCP 2.9: MCP-Native Middleware** \\
\\
FastMCP 2.9 is a major release that, among other things, introduces two important features that push beyond the basic MCP protocol.🤝 _MCP Middleware_ brings a flexible middleware system for intercepting and controlling server operations - think authentication, logging, rate limiting, and custom business logic without touching core protocol code.✨ _Server-side type conversion_ for prompts solves a major developer pain point: while MCP requires string arguments, your functions can now work with native Python types like lists and dictionaries, with automatic conversion handling the complexity.These features transform FastMCP from a simple protocol implementation into a powerful framework for building sophisticated MCP applications. Combined with the new `File` utility for binary data and improvements to authentication and serialization, this release makes FastMCP significantly more flexible and developer-friendly while maintaining full protocol compliance.\\
\\

FastMCP 2.8

ReleasesBlog Posts

June 11, 2025

[![_image?href=%2F_astro%2Fhero.su3kspkP](https://www.jlowin.dev/_image?href=%2F_astro%2Fhero.su3kspkP.png&w=1000&h=500&f=webp)](https://www.jlowin.dev/blog/fastmcp-2-8-tool-transformation)

[**FastMCP 2.8: Transform and Roll Out**](https://www.jlowin.dev/blog/fastmcp-2-8-tool-transformation)

[FastMCP 2.8 is here, and it’s all about taking control of your tools.This release is packed with new features for curating the perfect LLM experience:🛠️ Tool TransformationThe headline feature lets you wrap any tool,from your own code, a third-party library, or an OpenAPI spec,to create an enhanced, LLM-friendly version. You can rename arguments, rewrite descriptions, and hide parameters without touching the original code.This feature was developed in close partnership with Bill Easton. As Bill brilliantly](https://www.jlowin.dev/blog/fastmcp-2-8-tool-transformation) [put it](https://www.linkedin.com/posts/williamseaston_huge-thanks-to-william-easton-for-providing-activity-7338011349525983232-Mw6T?utm_source=share&utm_medium=member_desktop&rcm=ACoAAAAd6d0B3uL9zpCsq9eYWKi3HIvb8eN_r_Q), “Tool transformation flips Prompt Engineering on its head: stop writing tool-friendly LLM prompts and start providing LLM-friendly tools.”🏷️ Component ControlNow that you’re transforming tools, you need a way to hide the old ones! In FastMCP 2.8 you can programmatically enable/disable any component, and for everyone who’s been asking what FastMCP’s tags are for,they finally have a purpose! You can now use tags to declaratively filter which components are exposed to your clients.🚀 Pragmatic by DefaultLastly, to ensure maximum compatibility with the ecosystem, we’ve made the pragmatic decision to default all OpenAPI routes to Tools, making your entire API immediately accessible to any tool-using agent. When the industry catches up and supports resources, we’ll restore the old default, but no reason you should do extra work before OpenAI, Anthropic, or Google!

Read more

FastMCP 2.7

Releases

June 6, 2025

[![release-2-7](https://mintlify.s3.us-west-1.amazonaws.com/fastmcp/assets/updates/release-2-7.png)\\
\\
**FastMCP 2.7: Pare Programming** \\
\\
FastMCP 2.7 has been released!Most notably, it introduces the highly requested (and Pythonic) “naked” decorator usage:\\
\\
Copy\\
\\
```\\
mcp = FastMCP()\\
\\
@mcp.tool\\
def add(a: int, b: int) -> int:\\
return a + b\\
\\
```\\
\\
In addition, decorators now return the objects they create, instead of the decorated function. This is an important usability enhancement.The bulk of the update is focused on improving the FastMCP internals, including a few breaking internal changes to private APIs. A number of functions that have clung on since 1.0 are now deprecated.\\
\\

FastMCP 2.6

ReleasesBlog Posts

June 2, 2025

[![_image?href=%2F_astro%2Fhero.Bsu8afiw](https://www.jlowin.dev/_image?href=%2F_astro%2Fhero.Bsu8afiw.png&w=1000&h=500&f=webp)\\
\\
**FastMCP 2.6: Blast Auth** \\
\\
FastMCP 2.6 is here!This release introduces first-class authentication for MCP servers and clients, including pragmatic Bearer token support and seamless OAuth 2.1 integration. This release aligns with how major AI platforms are adopting MCP today, making it easier than ever to securely connect your tools to real-world AI models. Dive into the update and secure your stack with minimal friction.\\
\\

Vibe-Testing

Blog PostsTutorials

May 21, 2025

[![_image?href=%2F_astro%2Fhero.BUPy9I9c](https://www.jlowin.dev/_image?href=%2F_astro%2Fhero.BUPy9I9c.png&w=1000&h=500&f=webp)\\
\\
**Stop Vibe-Testing Your MCP Server** \\
\\
Your tests are bad and you should feel bad.Stop vibe-testing your MCP server through LLM guesswork. FastMCP 2.0 introduces in-memory testing for fast, deterministic, and fully Pythonic validation of your MCP logic,no network, no subprocesses, no vibes.\\
\\

10,000 Stars

Blog Posts

May 8, 2025

[![_image?href=%2F_astro%2Fhero.Cnvci9Q_](https://www.jlowin.dev/_image?href=%2F_astro%2Fhero.Cnvci9Q_.png&w=1000&h=500&f=webp)\\
\\
**Reflecting on FastMCP at 10k stars 🌟** \\
\\
In just six weeks since its relaunch, FastMCP has surpassed 10,000 GitHub stars,becoming the fastest-growing OSS project in our orbit. What started as a personal itch has become the backbone of Python-based MCP servers, powering a rapidly expanding ecosystem. While the protocol itself evolves, FastMCP continues to lead with clarity, developer experience, and opinionated tooling. Here’s to what’s next.\\
\\

FastMCP 2.3

Blog PostsReleases

May 8, 2025

[![_image?href=%2F_astro%2Fhero.M_hv6gEB](https://www.jlowin.dev/_image?href=%2F_astro%2Fhero.M_hv6gEB.png&w=1000&h=500&f=webp)\\
\\
**Now Streaming: FastMCP 2.3** \\
\\
FastMCP 2.3 introduces full support for Streamable HTTP, a modern alternative to SSE that simplifies MCP deployments over the web. It’s efficient, reliable, and now the default HTTP transport. Just run your server with transport=“http” and connect clients via a standard URL,FastMCP handles the rest. No special setup required. This release makes deploying MCP servers easier and more portable than ever.\\
\\

Proxy Servers

Blog PostsTutorials

April 23, 2025

[![_image?href=%2F_astro%2Frobot-hero.DpmAqgui](https://www.jlowin.dev/_image?href=%2F_astro%2Frobot-hero.DpmAqgui.png&w=1000&h=500&f=webp)\\
\\
**MCP Proxy Servers with FastMCP 2.0** \\
\\
Even AI needs a good travel adapter 🔌FastMCP now supports proxying arbitrary MCP servers, letting you run a local FastMCP instance that transparently forwards requests to any remote or third-party server,regardless of transport. This enables transport bridging (e.g., stdio ⇄ SSE), simplified client configuration, and powerful gateway patterns. Proxies are fully composable with other FastMCP servers, letting you mount or import them just like local servers. Use `FastMCP.from_client()` to wrap any backend in a clean, Pythonic proxy.\\
\\

FastMCP 2.0

ReleasesBlog Posts

April 16, 2025

[![_image?href=%2F_astro%2Fhero.DpbmGNrr](https://www.jlowin.dev/_image?href=%2F_astro%2Fhero.DpbmGNrr.png&w=1000&h=500&f=webp)\\
\\
**Introducing FastMCP 2.0 🚀** \\
\\
This major release reimagines FastMCP as a full ecosystem platform, with powerful new features for composition, integration, and client interaction. You can now compose local and remote servers, proxy arbitrary MCP servers (with transport translation), and generate MCP servers from OpenAPI or FastAPI apps. A new client infrastructure supports advanced workflows like LLM sampling.FastMCP 2.0 builds on the success of v1 with a cleaner, more flexible foundation,try it out today!\\
\\

Official SDK

Announcements

December 3, 2024

[**FastMCP is joining the official MCP Python SDK!** \\
\\
FastMCP 1.0 will become part of the official MCP Python SDK!\\
\\

FastMCP 1.0

ReleasesBlog Posts

December 1, 2024

[![_image?href=%2F_astro%2Ffastmcp.Bep7YlTw](https://www.jlowin.dev/_image?href=%2F_astro%2Ffastmcp.Bep7YlTw.png&w=1000&h=500&f=webp)\\
\\
**Introducing FastMCP 🚀** \\
\\
Because life’s too short for boilerplate.This is where it all started. FastMCP’s launch post introduced a clean, Pythonic way to build MCP servers without the protocol overhead. Just write functions; FastMCP handles the rest. What began as a weekend project quickly became the foundation of a growing ecosystem.\\
\\

[Changelog](https://gofastmcp.com/changelog)