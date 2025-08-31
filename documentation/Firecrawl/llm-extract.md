# /scrape (with json) endpoint

JSON mode - LLM Extract

[Documentation](https://docs.firecrawl.dev/introduction) [SDKs](https://docs.firecrawl.dev/sdks/overview) [Learn](https://www.firecrawl.dev/blog/category/tutorials) [Integrations](https://www.firecrawl.dev/app) [API Reference](https://docs.firecrawl.dev/api-reference/introduction)

On this page

- [Scrape and extract structured data with Firecrawl](https://docs.firecrawl.dev/features/llm-extract#scrape-and-extract-structured-data-with-firecrawl)
- [Extract structured data](https://docs.firecrawl.dev/features/llm-extract#extract-structured-data)
- [/scrape (with json) endpoint](https://docs.firecrawl.dev/features/llm-extract#%2Fscrape-with-json-endpoint)
- [Extracting without schema (New)](https://docs.firecrawl.dev/features/llm-extract#extracting-without-schema-new)
- [JSON options object](https://docs.firecrawl.dev/features/llm-extract#json-options-object)

Scrape and extract structured data with Firecrawl

Firecrawl uses AI to get structured data from web pages in 3 steps:

1. **Set the Schema:**
Tell us what data you want by defining a JSON schema (using OpenAI’s format) along with the webpage URL.
2. **Make the Request:**
Send your URL and schema to our scrape endpoint. See how here:
[Scrape Endpoint Documentation](https://docs.firecrawl.dev/api-reference/endpoint/scrape)
3. **Get Your Data:**
Get back clean, structured data matching your schema that you can use right away.

This makes getting web data in the format you need quick and easy.

Extract structured data

#/scrape (with json) endpoint

Used to extract structured data from scraped pages.

```
from firecrawl import JsonConfig, FirecrawlApp
from pydantic import BaseModel
app = FirecrawlApp(api_key="<YOUR_API_KEY>")

class ExtractSchema(BaseModel):
    company_mission: str
    supports_sso: bool
    is_open_source: bool
    is_in_yc: bool

json_config = JsonConfig(
    schema=ExtractSchema
)

llm_extraction_result = app.scrape_url(
    'https://firecrawl.dev',
    formats=["json"],
    json_options=json_config,
    only_main_content=False,
    timeout=120000
)

print(llm_extraction_result.json)

```

Output:

JSON

```
{
    "success": true,
    "data": {
      "json": {
        "company_mission": "AI-powered web scraping and data extraction",
        "supports_sso": true,
        "is_open_source": true,
        "is_in_yc": true
      },
      "metadata": {
        "title": "Firecrawl",
        "description": "AI-powered web scraping and data extraction",
        "robots": "follow, index",
        "ogTitle": "Firecrawl",
        "ogDescription": "AI-powered web scraping and data extraction",
        "ogUrl": "https://firecrawl.dev/",
        "ogImage": "https://firecrawl.dev/og.png",
        "ogLocaleAlternate": [],
        "ogSiteName": "Firecrawl",
        "sourceURL": "https://firecrawl.dev/"
      },
    }
}

```

#Extracting without schema (New)

You can now extract without a schema by just passing a `prompt` to the endpoint. The llm chooses the structure of the data.

```
curl -X POST https://api.firecrawl.dev/v1/scrape \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer YOUR_API_KEY' \
    -d '{
      "url": "https://docs.firecrawl.dev/",
      "formats": ["json"],
      "jsonOptions": {
        "prompt": "Extract the company mission from the page."
      }
    }'

```

Output:

JSON

```
{
    "success": true,
    "data": {
      "json": {
        "company_mission": "AI-powered web scraping and data extraction",
      },
      "metadata": {
        "title": "Firecrawl",
        "description": "AI-powered web scraping and data extraction",
        "robots": "follow, index",
        "ogTitle": "Firecrawl",
        "ogDescription": "AI-powered web scraping and data extraction",
        "ogUrl": "https://firecrawl.dev/",
        "ogImage": "https://firecrawl.dev/og.png",
        "ogLocaleAlternate": [],
        "ogSiteName": "Firecrawl",
        "sourceURL": "https://firecrawl.dev/"
      },
    }
}

```

#JSON options object

The `jsonOptions` object accepts the following parameters:

- `schema`: The schema to use for the extraction.
- `systemPrompt`: The system prompt to use for the extraction.
- `prompt`: The prompt to use for the extraction without a schema.

[Suggest edits](https://github.com/mendableai/firecrawl-docs/edit/main/features/llm-extract.mdx) [Raise issue](https://github.com/mendableai/firecrawl-docs/issues/new?title=Issue%20on%20docs&body=Path:%20/features/llm-extract)

[Batch Scrape](https://docs.firecrawl.dev/features/batch-scrape) [Change Tracking](https://docs.firecrawl.dev/features/change-tracking)