---
url: "https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables"
title: "Use prompt templates and variables - Anthropic"
---

[Anthropic home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/dark.svg)](https://docs.anthropic.com/)

English

Search...

Ctrl K

Search...

Navigation

Prompt engineering

Use prompt templates and variables

[Welcome](https://docs.anthropic.com/en/home) [Developer Platform](https://docs.anthropic.com/en/docs/intro) [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) [Model Context Protocol (MCP)](https://docs.anthropic.com/en/docs/mcp) [API Reference](https://docs.anthropic.com/en/api/messages) [Resources](https://docs.anthropic.com/en/resources/overview) [Release Notes](https://docs.anthropic.com/en/release-notes/overview)

When deploying an LLM-based application with Claude, your API calls will typically consist of two types of content:

- **Fixed content:** Static instructions or context that remain constant across multiple interactions
- **Variable content:** Dynamic elements that change with each request or conversation, such as:

  - User inputs
  - Retrieved content for Retrieval-Augmented Generation (RAG)
  - Conversation context such as user account history
  - System-generated data such as tool use results fed in from other independent calls to Claude

A **prompt template** combines these fixed and variable parts, using placeholders for the dynamic content. In the [Anthropic Console](https://console.anthropic.com/), these placeholders are denoted with **{{double brackets}}**, making them easily identifiable and allowing for quick testing of different values.

* * *

# [​](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables\#when-to-use-prompt-templates-and-variables)  When to use prompt templates and variables

You should always use prompt templates and variables when you expect any part of your prompt to be repeated in another call to Claude (only via the API or the [Anthropic Console](https://console.anthropic.com/). [claude.ai](https://claude.ai/) currently does not support prompt templates or variables).

Prompt templates offer several benefits:

- **Consistency:** Ensure a consistent structure for your prompts across multiple interactions
- **Efficiency:** Easily swap out variable content without rewriting the entire prompt
- **Testability:** Quickly test different inputs and edge cases by changing only the variable portion
- **Scalability:** Simplify prompt management as your application grows in complexity
- **Version control:** Easily track changes to your prompt structure over time by keeping tabs only on the core part of your prompt, separate from dynamic inputs

The [Anthropic Console](https://console.anthropic.com/) heavily uses prompt templates and variables in order to support features and tooling for all the above, such as with the:

- **[Prompt generator](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-generator):** Decides what variables your prompt needs and includes them in the template it outputs
- **[Prompt improver](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-improver):** Takes your existing template, including all variables, and maintains them in the improved template it outputs
- **[Evaluation tool](https://docs.anthropic.com/en/docs/test-and-evaluate/eval-tool):** Allows you to easily test, scale, and track versions of your prompts by separating the variable and fixed portions of your prompt template

* * *

# [​](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables\#example-prompt-template)  Example prompt template

Let’s consider a simple application that translates English text to Spanish. The translated text would be variable since you would expect this text to change between users or calls to Claude. This translated text could be dynamically retrieved from databases or the user’s input.

Thus, for your translation app, you might use this simple prompt template:

Copy

```
Translate this text from English to Spanish: {{text}}

```

* * *

## [​](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables\#next-steps)  Next steps

[**Generate a prompt** \\
\\
Learn about the prompt generator in the Anthropic Console and try your hand at getting Claude to generate a prompt for you.](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-generator) [**Apply XML tags** \\
\\
If you want to level up your prompt variable game, wrap them in XML tags.](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags) [**Anthropic Console** \\
\\
Check out the myriad prompt development tools available in the Anthropic Console.](https://console.anthropic.com/)

Was this page helpful?

YesNo

[Prompt generator](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-generator) [Prompt improver](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-improver)

On this page

- [When to use prompt templates and variables](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables#when-to-use-prompt-templates-and-variables)
- [Example prompt template](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables#example-prompt-template)
- [Next steps](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables#next-steps)