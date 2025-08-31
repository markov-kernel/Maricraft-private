# /search endpoint

Firecrawl’s search API allows you to perform web searches and optionally scrape the search results in one operation.

- Choose specific output formats (markdown, HTML, links, screenshots)
- Search the web with customizable parameters (location, etc.)
- Optionally retrieve content from search results in various formats
- Control the number of results and set timeouts

For details, see the [Search Endpoint API Reference](https://docs.firecrawl.dev/api-reference/endpoint/search).

Performing a Search with Firecrawl

#/search endpoint

Used to perform web searches and optionally retrieve content from the results.

#Installation

```
pip install firecrawl-py

```

#Basic Usage

```
from firecrawl import FirecrawlApp

# Initialize the client with your API key
app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Perform a basic search
search_result = app.search("firecrawl web scraping", limit=5)

# Print the search results
for result in search_result.data:
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Description: {result['description']}")

```

#Response

SDKs will return the data object directly. cURL will return the complete payload.

```
{
  "success": true,
  "data": [\
    {\
      "title": "Firecrawl - The Ultimate Web Scraping API",\
      "description": "Firecrawl is a powerful web scraping API that turns any website into clean, structured data for AI and analysis.",\
      "url": "https://firecrawl.dev/"\
    },\
    {\
      "title": "Web Scraping with Firecrawl - A Complete Guide",\
      "description": "Learn how to use Firecrawl to extract data from websites effortlessly.",\
      "url": "https://firecrawl.dev/guides/web-scraping/"\
    },\
    {\
      "title": "Firecrawl Documentation - Getting Started",\
      "description": "Official documentation for the Firecrawl web scraping API.",\
      "url": "https://docs.firecrawl.dev/"\
    }\
    // ... more results\
  ]
}

```

Search with Content Scraping

Search and retrieve content from the search results in one operation.

```
from firecrawl import FirecrawlApp, ScrapeOptions

# Initialize the client with your API key
app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Search and scrape content
search_result = app.search(
    "firecrawl web scraping",
    limit=3,
    scrape_options=ScrapeOptions(formats=["markdown", "links"])
)

# Process the results
for result in search_result.data:
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Content: {result['markdown'][:150]}...")  # first 150 chars
    print(f"Links: {', '.join(result['links'][:3])}...")  # first 3 links

```

#Response with Scraped Content

```
{
  "success": true,
  "data": [\
    {\
      "title": "Firecrawl - The Ultimate Web Scraping API",\
      "description": "Firecrawl is a powerful web scraping API that turns any website into clean, structured data for AI and analysis.",\
      "url": "https://firecrawl.dev/",\
      "markdown": "# Firecrawl\n\nThe Ultimate Web Scraping API\n\n## Turn any website into clean, structured data\n\nFirecrawl makes it easy to extract data from websites for AI applications, market research, content aggregation, and more...",\
      "links": [\
        "https://firecrawl.dev/pricing",\
        "https://firecrawl.dev/docs",\
        "https://firecrawl.dev/guides",\
        // ... more links\
      ],\
      "metadata": {\
        "title": "Firecrawl - The Ultimate Web Scraping API",\
        "description": "Firecrawl is a powerful web scraping API that turns any website into clean, structured data for AI and analysis.",\
        "sourceURL": "https://firecrawl.dev/",\
        "statusCode": 200\
      }\
    },\
    // ... more results\
  ]
}

```

Advanced Search Options

Firecrawl’s search API supports various parameters to customize your search:

#Location Customization

```
from firecrawl import FirecrawlApp

# Initialize the client with your API key
app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Search with location settings (Germany)
search_result = app.search(
    "web scraping tools",
    limit=5,
    location="Germany"
)

# Process the results
for result in search_result.data:
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")

```

#Time-Based Search

Use the `tbs` parameter to filter results by time:

```
from firecrawl import FirecrawlApp

# Initialize the client with your API key
app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Search for results from the past week
search_result = app.search(
    "latest web scraping techniques",
    limit=5,
    tbs="qdr:w"  # qdr:w = past week
)

# Process the results
for result in search_result.data:
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")

```

Common `tbs` values:

- `qdr:h` \- Past hour
- `qdr:d` \- Past 24 hours
- `qdr:w` \- Past week
- `qdr:m` \- Past month
- `qdr:y` \- Past year

For more precise time filtering, you can specify exact date ranges using the custom date range format:

```
from firecrawl import FirecrawlApp

# Initialize the client with your API key
app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Search for results from December 2024
search_result = app.search(
    "firecrawl updates",
    limit=10,
    tbs="cdr:1,cd_min:12/1/2024,cd_max:12/31/2024"
)

```

#Custom Timeout

Set a custom timeout for search operations:

```
from firecrawl import FirecrawlApp

# Initialize the client with your API key
app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Set a 30-second timeout
search_result = app.search(
    "complex search query",
    limit=10,
    timeout=30000  # 30 seconds in milliseconds
)

```

Scraping Options

When scraping search results, you can specify multiple output formats and advanced scraping options:

```
from firecrawl import FirecrawlApp, ScrapeOptions

# Initialize the client with your API key
app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Get search results with multiple formats
search_result = app.search(
    "firecrawl features",
    limit=3,
    scrape_options=ScrapeOptions(formats=["markdown", "html", "links", "screenshot"])
)

```

Available formats:

- `markdown`: Clean, formatted markdown content
- `html`: Processed HTML content
- `rawHtml`: Unmodified HTML content
- `links`: List of links found on the page
- `screenshot`: Screenshot of the page
- `screenshot@fullPage`: Full-page screenshot
- `extract`: Structured data extraction

Cost Implications

When using the search endpoint with scraping enabled, be aware of these cost factors:

- **Standard scraping**: 1 credit per search result
- **PDF parsing**: 1 credit per PDF page (can significantly increase costs for multi-page PDFs)
- **Stealth proxy mode**: +4 additional credits per search result

To control costs:

- Set `parsePDF: false` if you don’t need PDF content
- Use `proxy: "basic"` instead of `"stealth"` when possible
- Limit the number of search results with the `limit` parameter

Advanced Scraping Options

For more details about the scraping options, refer to the [Scrape Feature documentation](https://docs.firecrawl.dev/features/scrape). Everything except for the FIRE-1 Agent and Change-Tracking features are supported by this Search endpoint.

[Suggest edits](https://github.com/mendableai/firecrawl-docs/edit/main/features/search.mdx) [Raise issue](https://github.com/mendableai/firecrawl-docs/issues/new?title=Issue%20on%20docs&body=Path:%20/features/search)

[Map](https://docs.firecrawl.dev/features/map) [Extract](https://docs.firecrawl.dev/features/extract)