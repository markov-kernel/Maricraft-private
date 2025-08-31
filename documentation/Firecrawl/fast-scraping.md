# Use cached data if it's less than 1 hour old (3600000 ms)

How It Works

Get your scraping results **500% faster** when you don’t need the absolute freshest data. Firecrawl keeps an index of previously scraped pages. Add the `maxAge` parameter to your request and we’ll:

1. **Return instantly** if we have a recent version of the page
2. **Scrape fresh** only if our version is older than your specified age
3. **Save you time** \- results come back in milliseconds instead of seconds

When to Use This

**Great for:**

- Documentation, articles, product pages
- Bulk processing jobs
- Development and testing
- Building knowledge bases

**Skip for:**

- Real-time data (stock prices, live scores, breaking news)
- Frequently updated content
- Time-sensitive applications

Usage

Simply add the `maxAge` parameter to your scrape request. The value is in milliseconds - for example, `3600000` means “use cached data if it’s less than 1 hour old.”

```
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Use cached data if it's less than 1 hour old (3600000 ms)
# This can be 500% faster than a fresh scrape!
scrape_result = app.scrape_url(
    'https://firecrawl.dev',
    params={
        'formats': ['markdown'],
        'maxAge': 3600000  # 1 hour in milliseconds
    }
)

print(scrape_result['markdown'])

```

Common maxAge Values

Here are some helpful reference values:

- **5 minutes**: `300000` \- For semi-dynamic content
- **1 hour**: `3600000` \- For content that updates hourly
- **1 day**: `86400000` \- For daily-updated content
- **1 week**: `604800000` \- For relatively static content

Performance Impact

With `maxAge` enabled:

- **500% faster response times** for recent content
- **Instant results** instead of waiting for fresh scrapes

Important Notes

- **Default**: `maxAge` defaults to `0`, which means always scrape fresh
- **Fresh when needed**: If our data is older than `maxAge`, we scrape fresh automatically
- **No stale data**: You’ll never get data older than your specified `maxAge`

Faster Crawling

The same speed benefits apply when crawling multiple pages. Use `maxAge` within `scrapeOptions` to get cached results for pages we’ve seen recently.

```
from firecrawl import FirecrawlApp, ScrapeOptions

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Crawl with cached scraping - 500% faster for pages we've seen recently
crawl_result = app.crawl_url(
    'https://firecrawl.dev',
    limit=100,
    scrape_options=ScrapeOptions(
        formats=['markdown'],
        maxAge=3600000  # Use cached data if less than 1 hour old
    )
)

for page in crawl_result['data']:
    print(f"URL: {page['metadata']['sourceURL']}")
    print(f"Content: {page['markdown'][:200]}...")

```

When crawling with `maxAge`, each page in your crawl will benefit from the 500% speed improvement if we have recent cached data for that page.Start using `maxAge` today for dramatically faster scrapes and crawls!

[Suggest edits](https://github.com/mendableai/firecrawl-docs/edit/main/features/fast-scraping.mdx) [Raise issue](https://github.com/mendableai/firecrawl-docs/issues/new?title=Issue%20on%20docs&body=Path:%20/features/fast-scraping)

[Scrape](https://docs.firecrawl.dev/features/scrape) [Batch Scrape](https://docs.firecrawl.dev/features/batch-scrape)