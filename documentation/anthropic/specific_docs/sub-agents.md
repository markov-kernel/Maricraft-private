Of course. Here is the documentation for Claude Code Sub Agents, rewritten and restructured to remove all non-content elements.

***

# Claude Code: Sub Agents

Custom sub agents in Claude Code are specialized AI assistants that can be invoked to handle specific types of tasks. They enable more efficient problem-solving by providing task-specific configurations with customized system prompts, tools, and a separate context window.

## What are Sub Agents?

Sub agents are pre-configured AI personalities that Claude Code can delegate tasks to. When Claude Code encounters a task that matches a sub agent’s expertise, it can delegate that task to the specialized sub agent, which works independently and returns results.

Each sub agent:

*   Has a specific purpose and expertise area.
*   Uses its own context window, separate from the main conversation.
*   Can be configured with a specific set of tools it’s allowed to use.
*   Includes a custom system prompt that guides its behavior.

### Key Benefits

*   **Context Preservation**: Each sub agent operates in its own context, preventing pollution of the main conversation and keeping it focused on high-level objectives.
*   **Specialized Expertise**: Sub agents can be fine-tuned with detailed instructions for specific domains, leading to higher success rates on designated tasks.
*   **Reusability**: Once created, sub agents can be used across different projects and shared with your team for consistent workflows.
*   **Flexible Permissions**: Each sub agent can have different tool access levels, allowing you to limit powerful tools to specific sub agent types.

## Quick Start

To create your first sub agent:

1.  **Open the sub agents interface** by running the command:
    ```
    /agents
    ```
2.  **Select 'Create New Agent'** and choose whether to create a project-level or user-level sub agent.
3.  **Define the sub agent**. It's recommended to generate the agent with Claude first, then customize it.
    *   Describe your sub agent in detail and when it should be used.
    *   Select the tools you want to grant it access to (or leave blank to inherit all tools). The interface shows all available tools, making selection easy.
    *   If you’re generating with Claude, you can also press `e` to edit the system prompt in your own editor.
4.  **Save and use**. Your sub agent is now available. Claude will use it automatically when appropriate, or you can invoke it explicitly:
    ```
    > Use the code-reviewer sub agent to check my recent changes
    ```

## Sub Agent Configuration

Sub agents are stored as Markdown files with YAML frontmatter.

### File Locations

| Type                 | Location            | Scope                         | Priority |
| -------------------- | ------------------- | ----------------------------- | -------- |
| **Project sub agents** | `.claude/agents/`   | Available in the current project | Highest  |
| **User sub agents**    | `~/.claude/agents/` | Available across all projects   | Lower    |

When sub agent names conflict, project-level sub agents take precedence over user-level ones.

### File Format

Each sub agent is defined in a Markdown file with YAML frontmatter and a system prompt.

```markdown
---
name: your-sub-agent-name
description: A natural language description of when this sub agent should be invoked.
tools: tool1, tool2, tool3  # Optional - inherits all tools from the main thread if omitted.
---

Your sub agent's system prompt goes here. This can be multiple paragraphs
and should clearly define the sub agent's role, capabilities, and approach
to solving problems. Include specific instructions, best practices, and any
constraints the sub agent should follow.
```

**Configuration Fields:**

| Field         | Required | Description                                                                    |
| ------------- | -------- | ------------------------------------------------------------------------------ |
| `name`        | Yes      | A unique identifier using lowercase letters and hyphens.                       |
| `description` | Yes      | A natural language description of the sub agent’s purpose and when to use it.  |
| `tools`       | No       | A comma-separated list of specific tools. If omitted, it inherits all tools. |

### Available Tools

Sub agents can be granted access to any of Claude Code’s internal tools and any connected MCP server tools.

It is recommended to use the `/agents` command to manage tool access, as it provides an interactive interface that lists all available tools. You can either omit the `tools` field to inherit all tools from the main thread or specify individual tools for more granular control.

## Managing Sub Agents

### Using the `/agents` Command (Recommended)

The `/agents` command opens a comprehensive, interactive menu where you can:

*   View all available sub agents (built-in, user, and project).
*   Create new sub agents with a guided setup.
*   Edit existing custom sub agents, including their tool access.
*   Delete custom sub agents.
*   See which sub agents are active when duplicates exist.

### Direct File Management

You can also manage sub agents by creating and editing their Markdown files directly.

```bash
# Create a project sub agent
mkdir -p .claude/agents
echo '---
name: test-runner
description: Use proactively to run tests and fix failures
---

You are a test automation expert. When you see code changes, proactively run the appropriate tests. If tests fail, analyze the failures and fix them while preserving the original test intent.' > .claude/agents/test-runner.md
```

## Using Sub Agents Effectively

### Automatic Delegation

Claude Code proactively delegates tasks based on the task description in your request and the `description` field in the sub agent's configuration. To encourage more proactive use, include phrases like “use PROACTIVELY” or “MUST BE USED” in your `description` field.

### Explicit Invocation

You can request a specific sub agent by mentioning it in your command:

```
> Use the test-runner sub agent to fix failing tests
> Have the code-reviewer sub agent look at my recent changes
> Ask the debugger sub agent to investigate this error
```

## Example Sub Agents

### Code Reviewer

```markdown
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes.
2. Focus on modified files.
3. Begin review immediately.

Review checklist:
- Code is simple and readable.
- Functions and variables are well-named.
- No duplicated code.
- Proper error handling.
- No exposed secrets or API keys.
- Input validation implemented.
- Good test coverage.
- Performance considerations addressed.

Provide feedback organized by priority: Critical issues (must fix), Warnings (should fix), and Suggestions (consider improving). Include specific examples of how to fix issues.
```

### Debugger

```markdown
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture the error message and stack trace.
2. Identify reproduction steps.
3. Isolate the failure location.
4. Implement a minimal fix.
5. Verify the solution works.

For each issue, provide:
- A root cause explanation.
- Evidence supporting the diagnosis.
- The specific code fix.
- The testing approach.
- Prevention recommendations.

Focus on fixing the underlying issue, not just the symptoms.
```

### Data Scientist

```markdown
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement.
2. Write efficient SQL queries.
3. Use BigQuery command line tools (bq) when appropriate.
4. Analyze and summarize results.
5. Present findings clearly.

Always ensure queries are efficient and cost-effective. For each analysis, explain the query approach, document any assumptions, highlight key findings, and suggest next steps.
```

## Best Practices

*   **Start with Claude-generated agents**: Generate your initial sub agent with Claude and then iterate on it. This gives you a solid foundation that you can customize to your specific needs.
*   **Design focused sub agents**: Create sub agents with single, clear responsibilities rather than making one agent do everything.
*   **Write detailed prompts**: Include specific instructions, examples, and constraints in your system prompts. The more guidance you provide, the better the sub agent will perform.
*   **Limit tool access**: Only grant the tools that are necessary for the sub agent’s purpose to improve security and focus.
*   **Use version control**: Check project-level sub agents into version control so your team can benefit from and improve them collaboratively.

## Advanced Usage

### Chaining Sub Agents

For complex workflows, you can instruct Claude to chain multiple sub agents:

```
> First use the code-analyzer sub agent to find performance issues, then use the optimizer sub agent to fix them
```

### Dynamic Sub Agent Selection

Claude Code intelligently selects sub agents based on context. Make your `description` fields specific and action-oriented for the best results.

## Performance Considerations

*   **Context Efficiency**: Sub agents help preserve the main conversation's context, enabling longer overall sessions.
*   **Latency**: Sub agents start with a clean slate each time they are invoked, which may add latency as they gather the context required to do their job effectively.