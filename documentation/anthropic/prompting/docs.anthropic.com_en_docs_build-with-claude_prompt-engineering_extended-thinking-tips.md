---
url: "https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips"
title: "Extended thinking tips - Anthropic"
---

[Anthropic home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/anthropic/logo/dark.svg)](https://docs.anthropic.com/)

English

Search...

Ctrl K

Search...

Navigation

Prompt engineering

Extended thinking tips

[Welcome](https://docs.anthropic.com/en/home) [Developer Platform](https://docs.anthropic.com/en/docs/intro) [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) [Model Context Protocol (MCP)](https://docs.anthropic.com/en/docs/mcp) [API Reference](https://docs.anthropic.com/en/api/messages) [Resources](https://docs.anthropic.com/en/resources/overview) [Release Notes](https://docs.anthropic.com/en/release-notes/overview)

This guide provides advanced strategies and techniques for getting the most out of Claude’s extended thinking features. Extended thinking allows Claude to work through complex problems step-by-step, improving performance on difficult tasks.

See [Extended thinking models](https://docs.anthropic.com/en/docs/about-claude/models/extended-thinking-models) for guidance on deciding when to use extended thinking.

## [​](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips\#before-diving-in)  Before diving in

This guide presumes that you have already decided to use extended thinking mode and have reviewed our basic steps on [how to get started with extended thinking](https://docs.anthropic.com/en/docs/about-claude/models/extended-thinking-models#getting-started-with-extended-thinking-models) as well as our [extended thinking implementation guide](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking).

### [​](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips\#technical-considerations-for-extended-thinking)  Technical considerations for extended thinking

- Thinking tokens have a minimum budget of 1024 tokens. We recommend that you start with the minimum thinking budget and incrementally increase to adjust based on your needs and task complexity.
- For workloads where the optimal thinking budget is above 32K, we recommend that you use [batch processing](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing) to avoid networking issues. Requests pushing the model to think above 32K tokens causes long running requests that might run up against system timeouts and open connection limits.
- Extended thinking performs best in English, though final outputs can be in [any language Claude supports](https://docs.anthropic.com/en/docs/build-with-claude/multilingual-support).
- If you need thinking below the minimum budget, we recommend using standard mode, with thinking turned off, with traditional chain-of-thought prompting with XML tags (like `<thinking>`). See [chain of thought prompting](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought).

## [​](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips\#prompting-techniques-for-extended-thinking)  Prompting techniques for extended thinking

### [​](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips\#use-general-instructions-first%2C-then-troubleshoot-with-more-step-by-step-instructions)  Use general instructions first, then troubleshoot with more step-by-step instructions

Claude often performs better with high level instructions to just think deeply about a task rather than step-by-step prescriptive guidance. The model’s creativity in approaching problems may exceed a human’s ability to prescribe the optimal thinking process.

For example, instead of:

User

Copy

```text
Think through this math problem step by step:
1. First, identify the variables
2. Then, set up the equation
3. Next, solve for x
...

```

Consider:

User

[Try in Console](https://console.anthropic.com/workbench/new?user=Please+think+about+this+math+problem+thoroughly+and+in+great+detail.+%0AConsider+multiple+approaches+and+show+your+complete+reasoning.%0ATry+different+methods+if+your+first+approach+doesn%27t+work.&thinking.budget_tokens=16000)

Copy

```text
Please think about this math problem thoroughly and in great detail.
Consider multiple approaches and show your complete reasoning.
Try different methods if your first approach doesn't work.

```

That said, Claude can still effectively follow complex structured execution steps when needed. The model can handle even longer lists with more complex instructions than previous versions. We recommend that you start with more generalized instructions, then read Claude’s thinking output and iterate to provide more specific instructions to steer its thinking from there.

### [​](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips\#multishot-prompting-with-extended-thinking)  Multishot prompting with extended thinking

[Multishot prompting](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting) works well with extended thinking. When you provide Claude examples of how to think through problems, it will follow similar reasoning patterns within its extended thinking blocks.

You can include few-shot examples in your prompt in extended thinking scenarios by using XML tags like `<thinking>` or `<scratchpad>` to indicate canonical patterns of extended thinking in those examples.

Claude will generalize the pattern to the formal extended thinking process. However, it’s possible you’ll get better results by giving Claude free rein to think in the way it deems best.

Example:

User

[Try in Console](https://console.anthropic.com/workbench/new?user=I%27m+going+to+show+you+how+to+solve+a+math+problem%2C+then+I+want+you+to+solve+a+similar+one.%0A%0AProblem+1%3A+What+is+15%25+of+80%3F%0A%0A%3Cthinking%3E%0ATo+find+15%25+of+80%3A%0A1.+Convert+15%25+to+a+decimal%3A+15%25+%3D+0.15%0A2.+Multiply%3A+0.15+%C3%97+80+%3D+12%0A%3C%2Fthinking%3E%0A%0AThe+answer+is+12.%0A%0ANow+solve+this+one%3A%0AProblem+2%3A+What+is+35%25+of+240%3F&thinking.budget_tokens=16000)

Copy

```text
I'm going to show you how to solve a math problem, then I want you to solve a similar one.

Problem 1: What is 15% of 80?

<thinking>
To find 15% of 80:
1. Convert 15% to a decimal: 15% = 0.15
2. Multiply: 0.15 × 80 = 12
</thinking>

The answer is 12.

Now solve this one:
Problem 2: What is 35% of 240?

```

### [​](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips\#maximizing-instruction-following-with-extended-thinking)  Maximizing instruction following with extended thinking

Claude shows significantly improved instruction following when extended thinking is enabled. The model typically:

1. Reasons about instructions inside the extended thinking block
2. Executes those instructions in the response

To maximize instruction following:

- Be clear and specific about what you want
- For complex instructions, consider breaking them into numbered steps that Claude should work through methodically
- Allow Claude enough budget to process the instructions fully in its extended thinking

### [​](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips\#using-extended-thinking-to-debug-and-steer-claude%E2%80%99s-behavior)  Using extended thinking to debug and steer Claude’s behavior

You can use Claude’s thinking output to debug Claude’s logic, although this method is not always perfectly reliable.

To make the best use of this methodology, we recommend the following tips:

- We don’t recommend passing Claude’s extended thinking back in the user text block, as this doesn’t improve performance and may actually degrade results.
- Prefilling extended thinking is explicitly not allowed, and manually changing the model’s output text that follows its thinking block is likely going to degrade results due to model confusion.

When extended thinking is turned off, standard `assistant` response text [prefill](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prefill-claudes-response) is still allowed.

Sometimes Claude may repeat its extended thinking in the assistant output text. If you want a clean response, instruct Claude not to repeat its extended thinking and to only output the answer.

### [​](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips\#making-the-best-of-long-outputs-and-longform-thinking)  Making the best of long outputs and longform thinking

For dataset generation use cases, try prompts such as “Please create an extremely detailed table of…” for generating comprehensive datasets.

For use cases such as detailed content generation where you may want to generate longer extended thinking blocks and more detailed responses, try these tips:

- Increase both the maximum extended thinking length AND explicitly ask for longer outputs
- For very long outputs (20,000+ words), request a detailed outline with word counts down to the paragraph level. Then ask Claude to index its paragraphs to the outline and maintain the specified word counts

We do not recommend that you push Claude to output more tokens for outputting tokens’ sake. Rather, we encourage you to start with a small thinking budget and increase as needed to find the optimal settings for your use case.

Here are example use cases where Claude excels due to longer extended thinking:

Complex STEM problems

Complex STEM problems require Claude to build mental models, apply specialized knowledge, and work through sequential logical steps,processes that benefit from longer reasoning time.

- Standard prompt
- Enhanced prompt

User

[Try in Console](https://console.anthropic.com/workbench/new?user=Write+a+python+script+for+a+bouncing+yellow+ball+within+a+square%2C%0Amake+sure+to+handle+collision+detection+properly.%0AMake+the+square+slowly+rotate.&thinking.budget_tokens=16000)

Copy

```text
Write a python script for a bouncing yellow ball within a square,
make sure to handle collision detection properly.
Make the square slowly rotate.

```

This simpler task typically results in only about a few seconds of thinking time.

User

[Try in Console](https://console.anthropic.com/workbench/new?user=Write+a+python+script+for+a+bouncing+yellow+ball+within+a+square%2C%0Amake+sure+to+handle+collision+detection+properly.%0AMake+the+square+slowly+rotate.&thinking.budget_tokens=16000)

Copy

```text
Write a python script for a bouncing yellow ball within a square,
make sure to handle collision detection properly.
Make the square slowly rotate.

```

This simpler task typically results in only about a few seconds of thinking time.

User

[Try in Console](https://console.anthropic.com/workbench/new?user=Write+a+Python+script+for+a+bouncing+yellow+ball+within+a+tesseract%2C+%0Amaking+sure+to+handle+collision+detection+properly.+%0AMake+the+tesseract+slowly+rotate.+%0AMake+sure+the+ball+stays+within+the+tesseract.&thinking.budget_tokens=16000)

Copy

```text
Write a Python script for a bouncing yellow ball within a tesseract,
making sure to handle collision detection properly.
Make the tesseract slowly rotate.
Make sure the ball stays within the tesseract.

```

This complex 4D visualization challenge makes the best use of long extended thinking time as Claude works through the mathematical and programming complexity.

Constraint optimization problems

Constraint optimization challenges Claude to satisfy multiple competing requirements simultaneously, which is best accomplished when allowing for long extended thinking time so that the model can methodically address each constraint.

- Standard prompt
- Enhanced prompt

User

[Try in Console](https://console.anthropic.com/workbench/new?user=Plan+a+week-long+vacation+to+Japan.&thinking.budget_tokens=16000)

Copy

```text
Plan a week-long vacation to Japan.

```

This open-ended request typically results in only about a few seconds of thinking time.

User

[Try in Console](https://console.anthropic.com/workbench/new?user=Plan+a+week-long+vacation+to+Japan.&thinking.budget_tokens=16000)

Copy

```text
Plan a week-long vacation to Japan.

```

This open-ended request typically results in only about a few seconds of thinking time.

User

[Try in Console](https://console.anthropic.com/workbench/new?user=Plan+a+7-day+trip+to+Japan+with+the+following+constraints%3A%0A-+Budget+of+%242%2C500%0A-+Must+include+Tokyo+and+Kyoto%0A-+Need+to+accommodate+a+vegetarian+diet%0A-+Preference+for+cultural+experiences+over+shopping%0A-+Must+include+one+day+of+hiking%0A-+No+more+than+2+hours+of+travel+between+locations+per+day%0A-+Need+free+time+each+afternoon+for+calls+back+home%0A-+Must+avoid+crowds+where+possible&thinking.budget_tokens=16000)

Copy

```text
Plan a 7-day trip to Japan with the following constraints:
- Budget of $2,500
- Must include Tokyo and Kyoto
- Need to accommodate a vegetarian diet
- Preference for cultural experiences over shopping
- Must include one day of hiking
- No more than 2 hours of travel between locations per day
- Need free time each afternoon for calls back home
- Must avoid crowds where possible

```

With multiple constraints to balance, Claude will naturally perform best when given more space to think through how to satisfy all requirements optimally.

Thinking frameworks

Structured thinking frameworks give Claude an explicit methodology to follow, which may work best when Claude is given long extended thinking space to follow each step.

- Standard prompt
- Enhanced prompt

User

[Try in Console](https://console.anthropic.com/workbench/new?user=Develop+a+comprehensive+strategy+for+Microsoft+%0Aentering+the+personalized+medicine+market+by+2027.&thinking.budget_tokens=16000)

Copy

```text
Develop a comprehensive strategy for Microsoft
entering the personalized medicine market by 2027.

```

This broad strategic question typically results in only about a few seconds of thinking time.

User

[Try in Console](https://console.anthropic.com/workbench/new?user=Develop+a+comprehensive+strategy+for+Microsoft+%0Aentering+the+personalized+medicine+market+by+2027.&thinking.budget_tokens=16000)

Copy

```text
Develop a comprehensive strategy for Microsoft
entering the personalized medicine market by 2027.

```

This broad strategic question typically results in only about a few seconds of thinking time.

User

[Try in Console](https://console.anthropic.com/workbench/new?user=Develop+a+comprehensive+strategy+for+Microsoft+entering+%0Athe+personalized+medicine+market+by+2027.%0A%0ABegin+with%3A%0A1.+A+Blue+Ocean+Strategy+canvas%0A2.+Apply+Porter%27s+Five+Forces+to+identify+competitive+pressures%0A%0ANext%2C+conduct+a+scenario+planning+exercise+with+four+%0Adistinct+futures+based+on+regulatory+and+technological+variables.%0A%0AFor+each+scenario%3A%0A-+Develop+strategic+responses+using+the+Ansoff+Matrix%0A%0AFinally%2C+apply+the+Three+Horizons+framework+to%3A%0A-+Map+the+transition+pathway%0A-+Identify+potential+disruptive+innovations+at+each+stage&thinking.budget_tokens=16000)

Copy

```text
Develop a comprehensive strategy for Microsoft entering
the personalized medicine market by 2027.

Begin with:
1. A Blue Ocean Strategy canvas
2. Apply Porter's Five Forces to identify competitive pressures

Next, conduct a scenario planning exercise with four
distinct futures based on regulatory and technological variables.

For each scenario:
- Develop strategic responses using the Ansoff Matrix

Finally, apply the Three Horizons framework to:
- Map the transition pathway
- Identify potential disruptive innovations at each stage

```

By specifying multiple analytical frameworks that must be applied sequentially, thinking time naturally increases as Claude works through each framework methodically.

### [​](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips\#have-claude-reflect-on-and-check-its-work-for-improved-consistency-and-error-handling)  Have Claude reflect on and check its work for improved consistency and error handling

You can use simple natural language prompting to improve consistency and reduce errors:

1. Ask Claude to verify its work with a simple test before declaring a task complete
2. Instruct the model to analyze whether its previous step achieved the expected result
3. For coding tasks, ask Claude to run through test cases in its extended thinking

Example:

User

[Try in Console](https://console.anthropic.com/workbench/new?user=Write+a+function+to+calculate+the+factorial+of+a+number.+%0ABefore+you+finish%2C+please+verify+your+solution+with+test+cases+for%3A%0A-+n%3D0%0A-+n%3D1%0A-+n%3D5%0A-+n%3D10%0AAnd+fix+any+issues+you+find.&thinking.budget_tokens=16000)

Copy

```text
Write a function to calculate the factorial of a number.
Before you finish, please verify your solution with test cases for:
- n=0
- n=1
- n=5
- n=10
And fix any issues you find.

```

## [​](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips\#next-steps)  Next steps

[**Extended thinking cookbook** \\
\\
Explore practical examples of extended thinking in our cookbook.](https://github.com/anthropics/anthropic-cookbook/tree/main/extended_thinking) [**Extended thinking guide** \\
\\
See complete technical documentation for implementing extended thinking.](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)

Was this page helpful?

YesNo

[Long context tips](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips) [Define success criteria](https://docs.anthropic.com/en/docs/test-and-evaluate/define-success)

On this page

- [Before diving in](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips#before-diving-in)
- [Technical considerations for extended thinking](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips#technical-considerations-for-extended-thinking)
- [Prompting techniques for extended thinking](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips#prompting-techniques-for-extended-thinking)
- [Use general instructions first, then troubleshoot with more step-by-step instructions](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips#use-general-instructions-first%2C-then-troubleshoot-with-more-step-by-step-instructions)
- [Multishot prompting with extended thinking](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips#multishot-prompting-with-extended-thinking)
- [Maximizing instruction following with extended thinking](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips#maximizing-instruction-following-with-extended-thinking)
- [Using extended thinking to debug and steer Claude’s behavior](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips#using-extended-thinking-to-debug-and-steer-claude%E2%80%99s-behavior)
- [Making the best of long outputs and longform thinking](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips#making-the-best-of-long-outputs-and-longform-thinking)
- [Have Claude reflect on and check its work for improved consistency and error handling](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips#have-claude-reflect-on-and-check-its-work-for-improved-consistency-and-error-handling)
- [Next steps](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips#next-steps)