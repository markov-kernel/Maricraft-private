# Python

Change Tracking with Crawl

[Documentation](https://docs.firecrawl.dev/introduction) [SDKs](https://docs.firecrawl.dev/sdks/overview) [Learn](https://www.firecrawl.dev/blog/category/tutorials) [Integrations](https://www.firecrawl.dev/app) [API Reference](https://docs.firecrawl.dev/api-reference/introduction)

On this page

- [Basic Usage](https://docs.firecrawl.dev/features/change-tracking-crawl#basic-usage)
- [Understanding Change Status](https://docs.firecrawl.dev/features/change-tracking-crawl#understanding-change-status)
- [Page Visibility](https://docs.firecrawl.dev/features/change-tracking-crawl#page-visibility)
- [Full Diff Support](https://docs.firecrawl.dev/features/change-tracking-crawl#full-diff-support)

Change tracking becomes even more powerful when combined with crawling. While change tracking on individual pages shows you content changes, using it with crawl lets you monitor your entire website structure - showing new pages, removed pages, and pages that have become hidden.

Basic Usage

To enable change tracking during a crawl, include it in the `formats` array of your `scrapeOptions`:

```
// JavaScript/TypeScript
const app = new FirecrawlApp({ apiKey: 'your-api-key' });
const result = await app.crawl('https://example.com', {
  scrapeOptions: {
    formats: ['markdown', 'changeTracking']
  }
});

```

```
# Python
app = FirecrawlApp(api_key='your-api-key')
result = app.crawl('https://firecrawl.dev', {
    'scrapeOptions': {
        'formats': ['markdown', 'changeTracking']
    }
})

```

```
{
  "success": true,
  "status": "completed",
  "completed": 2,
  "total": 2,
  "creditsUsed": 2,
  "expiresAt": "2025-04-14T18:44:13.000Z",
  "data": [\
    {\
      "markdown": "# Turn websites into LLM-ready data\n\nPower your AI apps with clean data crawled from any website...",\
      "metadata": {},\
      "changeTracking": {\
        "previousScrapeAt": "2025-04-10T12:00:00Z",\
        "changeStatus": "changed",\
        "visibility": "visible"\
      }\
    },\
    {\
      "markdown": "## Flexible Pricing\n\nStart for free, then scale as you grow...",\
      "metadata": {},\
      "changeTracking": {\
        "previousScrapeAt": "2025-04-10T12:00:00Z",\
        "changeStatus": "changed",\
        "visibility": "visible"\
      }\
    }\
  ]
}

```

Understanding Change Status

When using change tracking with crawl, the `changeStatus` field becomes especially valuable:

- `new`: A page that didn’t exist in your previous crawl
- `same`: A page that exists and hasn’t changed since your last crawl
- `changed`: A page that exists but has been modified since your last crawl
- `removed`: A page that existed in your previous crawl but is no longer found

Page Visibility

The `visibility` field helps you understand how pages are discovered:

- `visible`: The page is discoverable through links or the sitemap
- `hidden`: The page still exists but is no longer linked or in the sitemap

This is particularly useful for:

- Detecting orphaned content
- Finding pages accidentally removed from navigation
- Monitoring site structure changes
- Identifying content that should be re-linked or removed

Full Diff Support

For detailed change tracking with diffs, you can use the same options as described in the [Change Tracking for Scrape](https://docs.firecrawl.dev/features/change-tracking) documentation.

[Suggest edits](https://github.com/mendableai/firecrawl-docs/edit/main/features/change-tracking-crawl.mdx) [Raise issue](https://github.com/mendableai/firecrawl-docs/issues/new?title=Issue%20on%20docs&body=Path:%20/features/change-tracking-crawl)

[JSON mode](https://docs.firecrawl.dev/features/llm-extract) [Webhooks](https://docs.firecrawl.dev/features/webhooks)