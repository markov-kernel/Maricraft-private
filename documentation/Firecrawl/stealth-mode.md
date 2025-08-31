# Proxy Types

Firecrawl provides different proxy types to help you scrape websites with varying levels of anti-bot protection. The proxy type can be specified using the `proxy` parameter.

#Proxy Types

Firecrawl supports three types of proxies:

- **basic**: Proxies for scraping sites with none to basic anti-bot solutions. Fast and usually works.
- **stealth**: Stealth proxies for scraping sites with advanced anti-bot solutions. Slower, but more reliable on certain sites.
- **auto**: Firecrawl will automatically retry scraping with stealth proxies if the basic proxy fails. If the retry with stealth is successful, 5 credits will be billed for the scrape. If the first attempt with basic is successful, only the regular cost will be billed.

If you do not specify a proxy, Firecrawl will default to basic.

#Using Stealth Mode

When scraping websites with advanced anti-bot protection, you can use the stealth proxy mode to improve your success rate.

```
# pip install firecrawl-py

from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="YOUR_API_KEY")

# Using stealth proxy for sites with advanced anti-bot solutions
content = app.scrape_url("https://example.com", proxy="stealth")

print(content["markdown"])

```

**Note:** Starting May 8th, stealth proxy requests cost 5 credits per request.

Using Stealth as a Retry Mechanism

A common pattern is to first try scraping with the default proxy settings, and then retry with stealth mode if you encounter specific error status codes (401, 403, or 500) in the `metadata.statusCode` field of the response. These status codes can be indicative of the website blocking your request.

```
# pip install firecrawl-py

from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="YOUR_API_KEY")

# First try with basic proxy
try:
    content = app.scrape_url("https://example.com")

    # Check if we got an error status code
    status_code = content.get("metadata", {}).get("statusCode")
    if status_code in [401, 403, 500]:
        print(f"Got status code {status_code}, retrying with stealth proxy")
        # Retry with stealth proxy
        content = app.scrape_url("https://example.com", proxy="stealth")

    print(content["markdown"])
except Exception as e:
    print(f"Error: {e}")
    # Retry with stealth proxy on exception
    try:
        content = app.scrape_url("https://example.com", proxy="stealth")
        print(content["markdown"])
    except Exception as e:
        print(f"Stealth proxy also failed: {e}")

```

This approach allows you to optimize your credit usage by only using stealth mode when necessary.

[Suggest edits](https://github.com/mendableai/firecrawl-docs/edit/main/features/stealth-mode.mdx) [Raise issue](https://github.com/mendableai/firecrawl-docs/issues/new?title=Issue%20on%20docs&body=Path:%20/features/stealth-mode)

[Change Tracking](https://docs.firecrawl.dev/features/change-tracking) [Proxies](https://docs.firecrawl.dev/features/proxies)