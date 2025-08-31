# Scrape a website:

Firecrawl provides different proxy types to help you scrape websites with varying levels of anti-bot protection. The proxy type can be specified using the `proxy` parameter.

> By default, Firecrawl routes all requests through proxies to help ensure reliability and access, even if you do not specify a proxy type or location.

Location-Based Proxy Selection

Firecrawl automatically selects the best proxy based on your specified or detected location. This helps optimize scraping performance and reliability. However, not all locations are currently supported. The following locations are available:

| Country Code | Country Name | Stealth Mode Support |
| --- | --- | --- |
| AE | United Arab Emirates | No |
| AU | Australia | No |
| BR | Brazil | Yes |
| CN | China | No |
| DE | Germany | Yes |
| FR | France | Yes |
| GB | United Kingdom | No |
| JP | Japan | No |
| QA | Qatar | No |
| TR | Turkey | No |
| US | United States | Yes |
| VN | Vietnam | No |

The list of supported proxy locations was last updated on May 15, 2025. Availability may change over time.

If you need proxies in a location not listed above, please [contact us](mailto:help@firecrawl.com) and let us know your requirements.If you do not specify a proxy or location, Firecrawl will automatically select the best option based on the target site and your request.

How to Specify Proxy Location

You can request a specific proxy location by setting the `location.country` parameter in your request. For example, to use a Brazilian proxy, set `location.country` to `BR`.For full details, see the [API reference for `location.country`](http://localhost:3001/api-reference/endpoint/scrape#body-location-country).

```
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-YOUR_API_KEY")

# Scrape a website:
scrape_result = app.scrape_url('airbnb.com',
    formats=['markdown', 'html'],
    location={
        'country': 'BR',
        'languages': ['pt-BR']
    }
)
print(scrape_result)

```

If you request a country where a proxy is not available, Firecrawl will use the closest available region (EU or US) and set the browser location to your requested country.

Proxy Types

Firecrawl supports three types of proxies:

- **basic**: Proxies for scraping sites with none to basic anti-bot solutions. Fast and usually works.
- **stealth**: Stealth proxies for scraping sites with advanced anti-bot solutions, or for sites that block regular proxies. Slower, but more reliable on certain sites. [Learn more about Stealth Mode →](https://docs.firecrawl.dev/features/stealth-mode)
- **auto**: Firecrawl will automatically retry scraping with stealth proxies if the basic proxy fails. If the retry with stealth is successful, 5 credits will be billed for the scrape. If the first attempt with basic is successful, only the regular cost will be billed.

* * *

> **Note:** For detailed information on using stealth proxies, including credit costs and retry strategies, see the [Stealth Mode documentation](https://docs.firecrawl.dev/features/stealth-mode).

[Suggest edits](https://github.com/mendableai/firecrawl-docs/edit/main/features/proxies.mdx) [Raise issue](https://github.com/mendableai/firecrawl-docs/issues/new?title=Issue%20on%20docs&body=Path:%20/features/proxies)

[Stealth Mode](https://docs.firecrawl.dev/features/stealth-mode) [Webhooks](https://docs.firecrawl.dev/features/webhooks)