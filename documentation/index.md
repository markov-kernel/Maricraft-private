# Claude Code-Mind Documentation Index

Welcome to the Claude Code-Mind project documentation. This directory contains **hundreds of comprehensive documentation files** across multiple frameworks and services.

## 🚨 Quick Troubleshooting Guide

### When You're Stuck - Use Discovery!
1. **Explore**: Use `LS(path="/SWE/documentation")` to see what's available
2. **Search**: Use `Grep(pattern="your_error_or_topic", path="/SWE/documentation")` to find relevant docs
3. **Read**: Open whatever documentation seems relevant to your problem
4. **Iterate**: If first doc doesn't help, keep searching - there's extensive coverage
5. **Last Resort**: Only report blocked if you've searched and found no relevant documentation

## 📚 Major Documentation Categories

This is just a high-level overview. **Use `LS` and `Grep` to discover the full depth of documentation available!**

| Category | What's Inside | Key Subdirectories |
|----------|---------------|-------------------|
| **OpenAI/** | Complete OpenAI Agent SDK documentation | `OpenAI Agent SDK/` (concepts, examples, guides, reference, prompting) |
| **MCP/** | Model Context Protocol comprehensive guides | Architecture, quickstarts, specification, remote integration |
| **FastMCP/** | Fast MCP Python SDK documentation | Clients, servers, deployment, patterns, integrations |
| **OpenRouter/** | OpenRouter API and integration guides | API reference, routing, structured outputs, tool calling, web search |
| **Anthropic/** | Claude prompting and agent design | Prompting strategies, agent docs, sub-agents, tools, hooks |
| **Streamlit/** | Streamlit best practices and patterns | Architecture, testing, connections, multipage apps, custom components |
| **AWS/** | AWS services documentation | SES (email service) with comprehensive API docs |
| **Firecrawl/** | Web scraping and crawling guides | Scraping, crawling, extraction, webhooks, stealth mode |

### Special Documentation Files
- `agent-evaluation-guide.md` - Comprehensive evaluation patterns with JSON schemas
- `2025_scoring_systems_openai_research.md` - Latest research on scoring systems
- Various merged documentation files that combine related topics

## 📋 Common Search Patterns

Instead of prescriptive mappings, use these search strategies to find what you need:

### Finding Documentation by Error/Issue
```bash
# Search for your specific error message
Grep(pattern="Tool not found", path="/SWE/documentation")
Grep(pattern="upload.*artifact.*fail", path="/SWE/documentation", output_mode="files_with_matches")

# Search for concepts
Grep(pattern="multi-agent", path="/SWE/documentation/OpenAI")
Grep(pattern="structured output", path="/SWE/documentation/OpenRouter")
Grep(pattern="evaluation.*pattern", path="/SWE/documentation")
```

### Finding Documentation by Technology
```bash
# Explore specific technology directories
LS(path="/SWE/documentation/MCP")
LS(path="/SWE/documentation/FastMCP")
LS(path="/SWE/documentation/OpenAI/OpenAI Agent SDK")
LS(path="/SWE/documentation/streamlit-best-practices")

# Search across all docs for a technology
Grep(pattern="FastAPI", path="/SWE/documentation")
Grep(pattern="React", path="/SWE/documentation")
```

### Finding Documentation by Task
```bash
# For agent design
Grep(pattern="agent.*design|design.*agent", path="/SWE/documentation")

# For testing patterns
Grep(pattern="test.*pattern|TDD", path="/SWE/documentation")

# For parallelization
Grep(pattern="parallel|concurrent|batch", path="/SWE/documentation")
```

## 🗂️ Discovery Tips by Role

Rather than fixed documentation lists, use these discovery strategies based on what you're working on:

### If You're Building/Implementing
- Explore `/SWE/documentation/OpenAI/OpenAI Agent SDK/` for agent patterns
- Search for your specific framework: `Grep(pattern="Streamlit|FastAPI|React", path="/SWE/documentation")`
- Check `/SWE/documentation/streamlit-best-practices/` for UI patterns
- Look in `/SWE/documentation/FastMCP/` for MCP implementation details

### If You're Designing Architecture
- Browse `/SWE/documentation/OpenAI/OpenAI Agent SDK/concepts/` for design patterns
- Search `Grep(pattern="architecture|design pattern", path="/SWE/documentation")`
- Explore `/SWE/documentation/MCP/` for coordination patterns

### If You're Reviewing/Testing
- Check `agent-evaluation-guide.md` for evaluation patterns
- Search `Grep(pattern="test|review|evaluation", path="/SWE/documentation")`
- Look for specific quality patterns you need to verify

### If You're Integrating Services
- Explore service-specific dirs: `/SWE/documentation/AWS/`, `/SWE/documentation/Firecrawl/`
- Search for API patterns: `Grep(pattern="API|integration", path="/SWE/documentation")`
- Check `/SWE/documentation/OpenRouter/` for LLM integration

## 🔍 Example: How to Find What You Need

### Scenario 1: "MCP tool not found" error
```bash
# Step 1: Search for the error
Grep(pattern="tool not found", path="/SWE/documentation", output_mode="files_with_matches")

# Step 2: Explore MCP-specific docs
LS(path="/SWE/documentation/MCP")
LS(path="/SWE/documentation/FastMCP")

# Step 3: Search for MCP connection/setup info
Grep(pattern="mcp.*connection|mcp.*setup", path="/SWE/documentation/MCP")
```

### Scenario 2: Need to implement agent evaluation
```bash
# Step 1: Find evaluation documentation
Grep(pattern="evaluation", path="/SWE/documentation", output_mode="files_with_matches")

# Step 2: Read the main evaluation guide
Read(file_path="/SWE/documentation/agent-evaluation-guide.md")

# Step 3: Search for specific patterns
Grep(pattern="BinaryGate|RubricScoring|JSON schema", path="/SWE/documentation")
```

### Scenario 3: Working with Streamlit
```bash
# Step 1: Explore Streamlit documentation structure
LS(path="/SWE/documentation/streamlit-best-practices")

# Step 2: Search for your specific Streamlit topic
Grep(pattern="session state|caching|multipage", path="/SWE/documentation/streamlit-best-practices")
```

## 💡 Pro Tips

1. **Use ULTRATHINK** - Deep reflection before acting (see CLAUDE.md)
2. **Check artifacts** - Always verify required artifacts before status updates
3. **Parallel first** - Default to parallel execution, justify sequential
4. **Document paths** - Use absolute paths when referencing docs
5. **Error context** - Include full error messages when reporting issues

## 🚦 When to Report Blocked

Only report blocked state if:
1. ✅ Explored the documentation directory with LS
2. ✅ Searched comprehensively with Grep for your issue/error
3. ✅ Read any documentation that seemed relevant
4. ✅ Attempted documented solutions
5. ✅ Error persists with no workaround found in the extensive docs

Include in blocked report:
- Exact error message
- What documentation you checked
- What solutions you tried
- Current task context
- Suggested resolution (if any)

---

Need something else? Explore each section's own index or README for a deeper table of contents.

*Last Updated: 2025-08-13* 