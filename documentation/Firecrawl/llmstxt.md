# Example Usage

Generate LLMs.txt with an API

[Documentation](https://docs.firecrawl.dev/introduction) [SDKs](https://docs.firecrawl.dev/sdks/overview) [Learn](https://www.firecrawl.dev/blog/category/tutorials) [Integrations](https://www.firecrawl.dev/app) [API Reference](https://docs.firecrawl.dev/api-reference/introduction)

On this page

- [Introducing LLMs.txt Generator Endpoint (Alpha) 📃](https://docs.firecrawl.dev/features/alpha/llmstxt#introducing-llms-txt-generator-endpoint-alpha-%F0%9F%93%83)
- [How It Works](https://docs.firecrawl.dev/features/alpha/llmstxt#how-it-works)
- [Example Usage](https://docs.firecrawl.dev/features/alpha/llmstxt#example-usage)
- [Checking Generation Status](https://docs.firecrawl.dev/features/alpha/llmstxt#checking-generation-status)
- [Status Examples](https://docs.firecrawl.dev/features/alpha/llmstxt#status-examples)
- [In Progress](https://docs.firecrawl.dev/features/alpha/llmstxt#in-progress)
- [Completed](https://docs.firecrawl.dev/features/alpha/llmstxt#completed)
- [Known Limitations (Alpha)](https://docs.firecrawl.dev/features/alpha/llmstxt#known-limitations-alpha)
- [Billing and Usage](https://docs.firecrawl.dev/features/alpha/llmstxt#billing-and-usage)

This API is being deprecated in favor of our main endpoints. Here is an example repo that generates LLMs.txt files: [https://github.com/mendableai/create-llmstxt-py](https://github.com/mendableai/create-llmstxt-py). This API endpoint will still remain active but we will no longer be maintaining it after June 30, 2025.

Introducing LLMs.txt Generator Endpoint (Alpha) 📃

The `/llmstxt` endpoint allows you to transform any website into clean, [LLM-ready text files](https://www.firecrawl.dev/blog/How-to-Create-an-llms-txt-File-for-Any-Website). Simply provide a URL, and Firecrawl will crawl the site and generate both `llms.txt` and `llms-full.txt` files that can be used for training or analysis with any LLM.

How It Works

The LLMs.txt Generator:

1. Crawls the provided website URL and its linked pages
2. Extracts clean, meaningful text content
3. Generates two formats:
   - `llms.txt`: Concise summaries and key information
   - `llms-full.txt`: Complete text content with more detail

#Example Usage

```
from firecrawl import FirecrawlApp

# Initialize the client
firecrawl = FirecrawlApp(api_key="your_api_key")

# Generate LLMs.txt with polling
results = firecrawl.generate_llms_text(
    url="https://example.com",
    max_urls=2,
    show_full_text=True
)

# Access generation results
if results.success:
    print(f"Status: {results.status}")
    print(f"Generated Data: {results.data}")
else:
    print(f"Error: {results.error}")

```

**Key Parameters:**

- **url**: The website URL to generate LLMs.txt files from
- **maxUrls** (Optional): Maximum number of pages to crawl (1-100, default: 10)
- **showFullText** (Optional): Generate llms-full.txt in addition to llms.txt (default: false)

See [API Reference](https://docs.firecrawl.dev/api-reference/endpoint/llmstxt) for more details.

Checking Generation Status

LLMs.txt generation runs asynchronously. Make the aync call and monitor the status with:

```
from firecrawl import FirecrawlApp

# Initialize the client
firecrawl = FirecrawlApp(api_key="your_api_key")

# Create async job
job = firecrawl.async_generate_llms_text(
    url="https://example.com",
)

if job.success:
    job_id = job.id

# Check LLMs.txt generation status
status = firecrawl.check_generate_llms_text_status("job_id")

# Print current status
print(f"Status: {status.status}")

if status.status == 'completed':
    print("LLMs.txt Content:", status.data.llmstxt)
    if 'llmsfulltxt' in status.data:
        print("Full Text Content:", status.data.llmsfulltxt)
    print(f"Processed URLs: {len(status.data.processed_urls)}")

```

#Status Examples

##In Progress

```
{
  "success": true,
  "data": {
    "llmstxt": "# Firecrawl.dev llms.txt\n\n- [Web Data Extraction Tool](https://www.firecrawl.dev/)...",
    "llmsfulltxt": "# Firecrawl.dev llms-full.txt\n\n"
  },
  "status": "processing",
  "expiresAt": "2025-03-03T23:19:18.000Z"
}

```

##Completed

```
{
  "success": true,
  "data": {
    "llmstxt": "# http://firecrawl.dev llms.txt\n\n- [Web Data Extraction Tool](https://www.firecrawl.dev/): Transform websites into clean, LLM-ready data effortlessly.\n- [Flexible Web Scraping Pricing](https://www.firecrawl.dev/pricing): Flexible pricing plans for web scraping and data extraction.\n- [Web Scraping and AI](https://www.firecrawl.dev/blog): Explore tutorials and articles on web scraping and AI...",
    "llmsfulltxt": "# http://firecrawl.dev llms-full.txt\n\n## Web Data Extraction Tool\nIntroducing /extract - Get web data with a prompt [Try now](https://www.firecrawl.dev/extract)\n\n[💥Get 2 months free with yearly plan](https://www.firecrawl.dev/pricing)..."
  },
  "status": "completed",
  "expiresAt": "2025-03-03T22:45:50.000Z"
}

```

Known Limitations (Alpha)

1. **Access Restrictions**

Only publicly accessible pages can be processed. Login-protected or paywalled content is not supported.
2. **Site Size**

We are only are allowing processing for up to 5000 URLs during the alpha stage.
3. **Alpha State**

As an Alpha feature, the output format and processing may evolve based on feedback.

Billing and Usage

Billing is based on the number of URLs processed:

- Base cost: 1 credit per URL processed
- Control URL costs with `maxUrls` parameter