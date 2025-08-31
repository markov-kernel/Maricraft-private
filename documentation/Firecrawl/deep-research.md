# Example Usage

This API is being deprecated in favor of our new [Search API](https://docs.firecrawl.dev/features/search). For an example of how to build deep research, check out our open source [Firesearch project](https://github.com/mendableai/firesearch). This API endpoint will still remain active but we will no longer be maintaining it after June 30, 2025.

Introducing Deep Research (Alpha)

The `/deep-research` endpoint enables AI-powered deep research and analysis on any topic. Simply provide a research query, and Firecrawl will autonomously explore the web, gather relevant information, and synthesize findings into comprehensive insights.

Building with Deep Research

Deep Research works by:

1. Analyzing your query to identify key research areas
2. Iteratively searching and exploring relevant web content
3. Synthesizing information from multiple sources
4. Providing structured findings with source attribution

Firecrawl provides structured results that enable you to build powerful applications:

- **Activities**: Detailed timeline of research steps and findings
- **Sources**: Curated list of relevant URLs with titles and descriptions
- **Final Analysis**: Comprehensive synthesis of key insights and conclusions
- **Progress Tracking**: Real-time status updates on research depth and completion

#Example Usage

```
from firecrawl import FirecrawlApp

# Initialize the client
firecrawl = FirecrawlApp(api_key="your_api_key")

# Start research with real-time updates
def on_activity(activity):
    print(f"[{activity['type']}] {activity['message']}")

# Run deep research
results = firecrawl.deep_research(
    query="What are the latest developments in quantum computing?",
    max_depth=5,
    time_limit=180,
    max_urls=15,
    on_activity=on_activity
)

# Access research findings.
print(f"Final Analysis: {results['data']['finalAnalysis']}")

print(f"Sources: {len(results['data']['sources'])} references")

```

**Key Parameters:**

- **query**: The research topic or question you want to investigate
- **maxDepth** (Optional): Maximum number of research iterations (1-10, default: 7)
- **timeLimit** (Optional): Time limit in seconds (30-300, default: 270)
- **maxUrls** (Optional): Maximum number of URLs to analyze (1-1000, default: 20)

See [API Reference](https://docs.firecrawl.dev/api-reference/endpoint/deep-research) for more details.

#Response

```
{
  "success": true,
  "data": {
    "finalAnalysis": "Recent developments in quantum computing show significant progress in several key areas:\n\n1. Error Correction: Improved quantum error correction techniques have increased qubit stability\n2. Quantum Supremacy: Multiple demonstrations of quantum advantage in specific computational tasks\n3. Hardware Advances: New architectures using superconducting circuits and trapped ions\n4. Commercial Applications: Growing industry adoption in optimization and cryptography",
    "activities": [\
      {\
        "type": "search",\
        "status": "completed",\
        "message": "Analyzing quantum computing breakthroughs in 2024",\
        "timestamp": "2024-03-15T10:30:00Z",\
        "depth": 1\
      }\
    ],
    "sources": [\
      {\
        "url": "https://example.com/quantum-computing-2024",\
        "title": "Latest Quantum Computing Breakthroughs",\
        "description": "Overview of recent advances in quantum computing technology"\
      }\
    ]
  },
  "status": "completed",
  "currentDepth": 5,
  "maxDepth": 5,
  "expiresAt": "2024-03-16T10:30:00Z"
}

```

Monitoring Research Progress

Deep Research jobs run asynchronously. You can monitor progress and receive real-time updates:

```
from firecrawl import FirecrawlApp

# Initialize the client
firecrawl = FirecrawlApp(api_key="your_api_key")

# Check research status
status = firecrawl.check_deep_research_status("job_id")

# Print current progress
print(f"Status: {status.status}")
print(f"Progress: {status.current_depth}/{status.max_depth} iterations")

if status.status == 'completed':
    print(f"Final Analysis: {status.data.final_analysis}")
    print(f"Sources found: {len(status.data.sources)}")

```

#Research Activities

The data response includes:

- **activities**: List of research activities with the following properties:
- `type`: Type of activity (‘search’, ‘extract’, ‘analyze’, ‘reasoning’, ‘synthesis’, ‘thought’)
- `status`: Activity status (‘processing’, ‘complete’, ‘error’)
- `message`: Description of the activity or finding
- `timestamp`: ISO timestamp of when the activity occurred
- `depth`: Current research depth level
- **sources**: Referenced URLs with titles and descriptions
- `title`: Title of the source
- `description`: Description of the source
- `url`: URL of the source
- `icon`: Icon of the source
- **finalAnalysis**: Comprehensive analysis (when completed)

#Status Examples

##In Progress

```
{
  "success": true,
  "status": "processing",
  "data": {
    "activities": [\
      {\
        "type": "search",\
        "status": "completed",\
        "message": "Initial research on quantum computing trends",\
        "timestamp": "2024-03-15T10:30:00Z",\
        "depth": 1\
      },\
      {\
        "type": "analyze",\
        "status": "in_progress",\
        "message": "Analyzing quantum error correction advances",\
        "timestamp": "2024-03-15T10:31:00Z",\
        "depth": 2\
      }\
    ],
    "sources": [\
      {\
        "url": "https://example.com/quantum-computing-2024",\
        "title": "Latest Quantum Computing Breakthroughs",\
        "description": "Overview of recent advances in quantum computing technology"\
        }\
      ],
    },
  "currentDepth": 2,
  "maxDepth": 5,
  "expiresAt": "2024-03-16T10:30:00Z"
}

```

##Completed

```
{
  "success": true,
  "status": "completed",
  "data": {
    "finalAnalysis": "Recent developments in quantum computing show significant progress in several key areas:\n\n1. Error Correction: Improved quantum error correction techniques have increased qubit stability\n2. Quantum Supremacy: Multiple demonstrations of quantum advantage in specific computational tasks\n3. Hardware Advances: New architectures using superconducting circuits and trapped ions\n4. Commercial Applications: Growing industry adoption in optimization and cryptography",
    "activities": [\
      {\
        "type": "search",\
        "status": "completed",\
        "message": "Initial research on quantum computing trends",\
        "timestamp": "2024-03-15T10:30:00Z",\
        "depth": 1\
      },\
      {\
        "type": "analyze",\
        "status": "completed",\
        "message": "Analyzing quantum error correction advances",\
        "timestamp": "2024-03-15T10:31:00Z",\
        "depth": 2\
      },\
      {\
        "type": "synthesize",\
        "status": "completed",\
        "message": "Synthesizing findings from multiple sources",\
        "timestamp": "2024-03-15T10:32:00Z",\
        "depth": 5\
      }\
    ],
    "sources": [\
      {\
        "url": "https://example.com/quantum-computing-2024",\
        "title": "Latest Quantum Computing Breakthroughs",\
        "description": "Overview of recent advances in quantum computing technology"\
      },\
      {\
        "url": "https://example.com/quantum-error-correction",\
        "title": "Advances in Quantum Error Correction",\
        "description": "Deep dive into recent quantum error correction techniques"\
      }\
    ]
  },
  "currentDepth": 5,
  "maxDepth": 5,
  "expiresAt": "2024-03-16T10:30:00Z"
}

```

#JSON Output

You can now specify the JSON output format by setting the `formats` parameter to `json`. Set the `jsonOptions` parameter to specify the schema for the JSON output.

#Customize even further

You can also specify a `systemPrompt` and an `analysisPrompt` to customize the agentic process and the final analysis, respectively.

Models

While in Alpha we use a combination of small models to explore the web and synthesize information. That way we can keep the cost low and the research fast. But this can result in the synthesis not being very long and detailed.

Known Limitations (Alpha)

1. **Research Scope**

Best suited for topics with publicly available information. May not access paywalled or private content.
2. **Time Constraints**

Research jobs are limited to 10 minutes maximum to ensure reasonable response times.
3. **Source Verification**

While sources are provided, manual verification of critical information is recommended.
4. **Alpha State**

As an Alpha feature, the research methodology and output format may evolve based on feedback.

Billing and Usage

Billing is done based on the number of `urls` analyzed. Each `url` is 1 credit. You can specify the max number of urls to analyze with the `maxUrls` parameter.