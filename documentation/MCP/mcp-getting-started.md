> **Target Audience:** Newcomers
> 
> Entry point for newcomers - what MCP is and why it matters

- [MCP Architecture And Concepts](./mcp-architecture-and-concepts.md)
- [MCP Quickstart User](./mcp-quickstart-user.md)

---

## Source: https://modelcontextprotocol.io/docs/getting-started/intro

Get started with the Model Context Protocol (MCP)

MCP is an open protocol that standardizes how applications provide context to large language models (LLMs). Think of MCP like a USB-C port for AI applications. Just as USB-C provides a standardized way to connect your devices to various peripherals and accessories, MCP provides a standardized way to connect AI models to different data sources and tools. MCP enables you build agents and complex workflows on top of LLMs and connects your models with the world.

MCP provides:

* **A growing list of pre-built integrations** that your LLM can directly plug into
* **A standardized way** to build custom integrations for AI applications
* **An open protocol** that everyone is free to implement and use
* **The flexibility to change** between different apps and take your context with you

    Learn the core concepts and architecture of MCP


    Connect to existing MCP servers and start using them


    Create MCP servers to expose your data and tools

    Develop applications that connect to MCP servers

MCP provides official **SDKs** in multiple languages, see the [SDK documentation](/docs/sdk) to find the right SDK for your project. The SDKs handle the protocol details so you can focus on building your features.


## Source: https://modelcontextprotocol.io/overview/index

The open protocol that connects AI applications to the systems where context lives

<div className="landing-page">
  <div className="hero-section">
    <div className="intro-video-section">
      <div className="intro-content-wrapper">
        <div className="intro-content left-aligned">
          <h2 className="intro-title">Connect your AI applications to the world</h2>

          <p className="intro-description">
            AI-enabled tools are powerful, but they're often limited to the information you manually provide or require bespoke integrations.
          </p>

          <p className="intro-description">
            Whether it's reading files from your computer, searching through an internal or external knowledge base, or updating tasks in an project management tool, MCP provides a secure, standardized, *simple* way to give AI systems the context they need.
          </p>
        </div>

        <div className="intro-logo">
          <img src="https://mintlify.s3.us-west-1.amazonaws.com/mcp/mcp.png" alt="MCP Logo" />
        </div>
      </div>
    </div>

    <div className="how-section">
      <h2 className="section-title">How it works</h2>

      <div className="steps-container">
        <div className="step-item">
          <div className="step-content">
            <h3><span className="step-number">1</span> Choose MCP servers</h3>
            <p>Pick from pre-built servers for popular tools like GitHub, Google Drive, Slack and hundreds of others. Combine multiple servers for complete workflows, or easily build your own for custom integrations.</p>
          </div>
        </div>

        <div className="step-connector" />

        <div className="step-item">
          <div className="step-content">
            <h3><span className="step-number">2</span> Connect your AI application</h3>
            <p>Configure your AI application (like Claude, VS Code, or ChatGPT) to connect to your MCP servers. The application can now see available tools, resources and prompts from all connected servers.</p>
          </div>
        </div>

        <div className="step-connector" />

        <div className="step-item">
          <div className="step-content">
            <h3><span className="step-number">3</span> Work with context</h3>
            <p>Your AI-powered application can now access real data, execute actions, and provide more helpful responses based on your actual context.</p>
          </div>
        </div>
      </div>
    </div>

    <div className="ecosystem-section">
      <h2 className="section-title">Join a growing ecosystem</h2>

      <div className="stats-container">
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-number">9</div>
            <div className="stat-label">Official SDKs</div>
          </div>

          <div className="stat-card">
            <div className="stat-number">1000+</div>
            <div className="stat-label">Available Servers</div>
          </div>

          <div className="stat-card">
            <div className="stat-number">70+</div>
            <div className="stat-label">Compatible Clients</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div className="cta-buttons">
    <a href="/docs/getting-started/intro" className="cta-primary">
      Get Started
    </a>
  </div>
</div>


## Source: https://modelcontextprotocol.io/faqs

Explaining MCP and why it matters in simple terms

MCP (Model Context Protocol) is a standard way for AI applications and agents to connect to and work with your data sources (e.g. local files, databases, or content repositories) and tools (e.g. GitHub, Google Maps, or Puppeteer).

Think of MCP as a universal adapter for AI applications, similar to what USB-C is for physical devices. USB-C acts as a universal adapter to connect devices to various peripherals and accessories. Similarly, MCP provides a standardized way to connect AI applications to different data and tools.

Before USB-C, you needed different cables for different connections. Similarly, before MCP, developers had to build custom connections to each data source or tool they wanted their AI application to work with,a time-consuming process that often resulted in limited functionality. Now, with MCP, developers can easily add connections to their AI applications, making their applications much more powerful from day one.

MCP means your AI applications can access the information and tools you work with every day, making them much more helpful. Rather than AI being limited to what it already knows about, it can now understand your specific documents, data, and work context.

For example, by using MCP servers, applications can access your personal documents from Google Drive or data about your codebase from GitHub, providing more personalized and contextually relevant assistance.

Imagine asking an AI assistant: "Summarize last week's team meeting notes and schedule follow-ups with everyone."

By using connections to data sources powered by MCP, the AI assistant can:

* Connect to your Google Drive through an MCP server to read meeting notes
* Understand who needs follow-ups based on the notes
* Connect to your calendar through another MCP server to schedule the meetings automatically

MCP reduces development time and complexity when building AI applications that need to access various data sources. With MCP, developers can focus on building great AI experiences rather than repeatedly creating custom connectors.

Traditionally, connecting applications with data sources required building custom, one-off connections for each data source and each application. This created significant duplicative work,every developer wanting to connect their AI application to Google Drive or Slack needed to build their own connection.

MCP simplifies this by enabling developers to build MCP servers for data sources that are then reusable by various applications. For example, using the open source Google Drive MCP server, many different applications can access data from Google Drive without each developer needing to build a custom connection.

This open source ecosystem of MCP servers means developers can leverage existing work rather than starting from scratch, making it easier to build powerful AI applications that seamlessly integrate with the tools and data sources their users already rely on.

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/mcp/images/mcp-simple-diagram.png" />
</Frame>

MCP creates a bridge between your AI applications and your data through a straightforward system:

* **MCP servers** connect to your data sources and tools (like Google Drive or Slack)
* **MCP clients** are run by AI applications (like Claude Desktop) to connect them to these servers
* When you give permission, your AI application discovers available MCP servers
* The AI model can then use these connections to read information and take actions

This modular system means new capabilities can be added without changing AI applications themselves,just like adding new accessories to your computer without upgrading your entire system.

MCP servers are developed and maintained by:

* Developers at Anthropic who build servers for common tools and data sources
* Open source contributors who create servers for tools they use
* Enterprise development teams building servers for their internal systems
* Software providers making their applications AI-ready

Once an open source MCP server is created for a data source, it can be used by any MCP-compatible AI application, creating a growing ecosystem of connections. See our [list of example servers](/examples), or [get started building your own server](/quickstart/server).


