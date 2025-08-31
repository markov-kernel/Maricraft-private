# How it works

Batch scraping multiple URLs

You can now batch scrape multiple URLs at the same time. It takes the starting URLs and optional parameters as arguments. The params argument allows you to specify additional options for the batch scrape job, such as the output formats.

#How it works

It is very similar to how the `/crawl` endpoint works. It submits a batch scrape job and returns a job ID to check the status of the batch scrape.The sdk provides 2 methods, synchronous and asynchronous. The synchronous method will return the results of the batch scrape job, while the asynchronous method will return a job ID that you can use to check the status of the batch scrape.

#Usage

```
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Scrape multiple websites:
batch_scrape_result = app.batch_scrape_urls(['firecrawl.dev', 'mendable.ai'], formats=['markdown', 'html'])
print(batch_scrape_result)

# Or, you can use the asynchronous method:
batch_scrape_job = app.async_batch_scrape_urls(['firecrawl.dev', 'mendable.ai'], formats=['markdown', 'html'])
print(batch_scrape_job)

# (async) You can then use the job ID to check the status of the batch scrape:
batch_scrape_status = app.check_batch_scrape_status(batch_scrape_job.id)
print(batch_scrape_status)

```

#Response

If you’re using the sync methods from the SDKs, it will return the results of the batch scrape job. Otherwise, it will return a job ID that you can use to check the status of the batch scrape.

##Synchronous

Completed

```
{
  "status": "completed",
  "total": 36,
  "completed": 36,
  "creditsUsed": 36,
  "expiresAt": "2024-00-00T00:00:00.000Z",
  "next": "https://api.firecrawl.dev/v1/batch/scrape/123-456-789?skip=26",
  "data": [\
    {\
      "markdown": "[Firecrawl Docs home page![light logo](https://mintlify.s3-us-west-1.amazonaws.com/firecrawl/logo/light.svg)!...",\
      "html": "<!DOCTYPE html><html lang=\"en\" class=\"js-focus-visible lg:[--scroll-mt:9.5rem]\" data-js-focus-visible=\"\">...",\
      "metadata": {\
        "title": "Build a 'Chat with website' using Groq Llama 3 | Firecrawl",\
        "language": "en",\
        "sourceURL": "https://docs.firecrawl.dev/learn/rag-llama3",\
        "description": "Learn how to use Firecrawl, Groq Llama 3, and Langchain to build a 'Chat with your website' bot.",\
        "ogLocaleAlternate": [],\
        "statusCode": 200\
      }\
    },\
    ...\
  ]\
}\
\
```\
\
##Asynchronous\
\
You can then use the job ID to check the status of the batch scrape by calling the `/batch/scrape/{id}` endpoint. This endpoint is meant to be used while the job is still running or right after it has completed **as batch scrape jobs expire after 24 hours**.\
\
Copy\
\
Ask AI\
\
```\
{\
  "success": true,\
  "id": "123-456-789",\
  "url": "https://api.firecrawl.dev/v1/batch/scrape/123-456-789"\
}\
\
```\
\
Batch scrape with extraction\
\
You can also use the batch scrape endpoint to extract structured data from the pages. This is useful if you want to get the same structured data from a list of URLs.\
\
Python\
\
Node\
\
cURL\
\
Copy\
\
Ask AI\
\
```\
from firecrawl import FirecrawlApp\
\
app = FirecrawlApp(api_key="fc-YOUR_API_KEY")\
\
# Scrape multiple websites:\
batch_scrape_result = app.batch_scrape_urls(\
    ['https://docs.firecrawl.dev', 'https://docs.firecrawl.dev/sdks/overview'],\
    formats=['json'],\
    jsonOptions={\
        'prompt': 'Extract the title and description from the page.',\
        'schema': {\
            'type': 'object',\
            'properties': {\
                'title': {'type': 'string'},\
                'description': {'type': 'string'}\
            },\
            'required': ['title', 'description']\
        }\
    }\
)\
print(batch_scrape_result)\
\
# Or, you can use the asynchronous method:\
batch_scrape_job = app.async_batch_scrape_urls(\
    ['https://docs.firecrawl.dev', 'https://docs.firecrawl.dev/sdks/overview'],\
    formats=['json'],\
    jsonOptions={\
    'prompt': 'Extract the title and description from the page.',\
    'schema': {\
        'type': 'object',\
            'properties': {\
                'title': {'type': 'string'},\
                'description': {'type': 'string'}\
            },\
            'required': ['title', 'description']\
        }\
    }\
)\
print(batch_scrape_job)\
\
# (async) You can then use the job ID to check the status of the batch scrape:\
batch_scrape_status = app.check_batch_scrape_status(batch_scrape_job.id)\
print(batch_scrape_status)\
\
```\
\
#Response\
\
##Synchronous\
\
Completed\
\
Copy\
\
Ask AI\
\
```\
{\
  "status": "completed",\
  "total": 36,\
  "completed": 36,\
  "creditsUsed": 36,\
  "expiresAt": "2024-00-00T00:00:00.000Z",\
  "next": "https://api.firecrawl.dev/v1/batch/scrape/123-456-789?skip=26",\
  "data": [\
    {\
      "json": {\
        "title": "Build a 'Chat with website' using Groq Llama 3 | Firecrawl",\
        "description": "Learn how to use Firecrawl, Groq Llama 3, and Langchain to build a 'Chat with your website' bot."\
      }\
    },\
    ...\
  ]\
}\
\
```\
\
##Asynchronous\
\
Copy\
\
Ask AI\
\
```\
{\
  "success": true,\
  "id": "123-456-789",\
  "url": "https://api.firecrawl.dev/v1/batch/scrape/123-456-789"\
}\
\
```\
\
Batch Scrape with Webhooks\
\
You can configure webhooks to receive real-time notifications as each URL in your batch is scraped. This allows you to process results immediately instead of waiting for the entire batch to complete.\
\
cURL\
\
Copy\
\
Ask AI\
\
```\
curl -X POST https://api.firecrawl.dev/v1/batch/scrape \\
    -H 'Content-Type: application/json' \\
    -H 'Authorization: Bearer YOUR_API_KEY' \\
    -d '{\
      "urls": [\
        "https://example.com/page1",\
        "https://example.com/page2",\
        "https://example.com/page3"\
      ],\
      "webhook": {\
        "url": "https://your-domain.com/webhook",\
        "metadata": {\
          "any_key": "any_value"\
        },\
        "events": ["started", "page", "completed"]\
      }\
    }'\
\
```\
\
For comprehensive webhook documentation including event types, payload structure, and implementation examples, see the [Webhooks documentation](https://docs.firecrawl.dev/features/webhooks).\
\
#Quick Reference\
\
**Event Types:**\
\
- `batch_scrape.started` \- When the batch scrape begins\
- `batch_scrape.page` \- For each URL successfully scraped\
- `batch_scrape.completed` \- When all URLs are processed\
- `batch_scrape.failed` \- If the batch scrape encounters an error\
\
**Basic Payload:**\
\
Copy\
\
Ask AI\
\
```\
{\
  "success": true,\
  "type": "batch_scrape.page",\
  "id": "batch-job-id",\
  "data": [...], // Page data for 'page' events\
  "metadata": {}, // Your custom metadata\
  "error": null\
}\
\
```\
\
For detailed webhook configuration, security best practices, and troubleshooting, visit the [Webhooks documentation](https://docs.firecrawl.dev/features/webhooks).\
\
[Suggest edits](https://github.com/mendableai/firecrawl-docs/edit/main/features/batch-scrape.mdx) [Raise issue](https://github.com/mendableai/firecrawl-docs/issues/new?title=Issue%20on%20docs&body=Path:%20/features/batch-scrape)\
\
[Faster Scraping](https://docs.firecrawl.dev/features/fast-scraping) [JSON mode](https://docs.firecrawl.dev/features/llm-extract)\
\
Assistant\
\