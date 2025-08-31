# Webhooks

````
# Webhooks

> Real-time notifications for your Firecrawl operations

Webhooks allow you to receive real-time notifications about your Firecrawl operations as they progress. Instead of polling for status updates, Firecrawl will automatically send HTTP POST requests to your specified endpoint when events occur.

## Overview

Webhooks are supported for:

* **Crawl operations** - Get notified as pages are crawled and when crawls complete
* **Batch scrape operations** - Receive updates for each URL scraped in a batch

## Basic Configuration

Configure webhooks by adding a `webhook` object to your request:

```json JSON
{
  "webhook": {
    "url": "https://your-domain.com/webhook",
    "metadata": {
      "any_key": "any_value"
    },
    "events": ["started", "page", "completed", "failed"]
  }
}
```

### Configuration Options

| Field      | Type   | Required | Description                                   |
| ---------- | ------ | -------- | --------------------------------------------- |
| `url`      | string | ✅        | Your webhook endpoint URL                     |
| `headers`  | object | ❌        | Custom headers to include in webhook requests |
| `metadata` | object | ❌        | Custom data included in all webhook payloads  |
| `events`   | array  | ❌        | Event types to receive (default: all events)  |

## Event Types

### Crawl Events

| Event             | Description                 | When Triggered                          |
| ----------------- | --------------------------- | --------------------------------------- |
| `crawl.started`   | Crawl job initiated         | When crawl begins                       |
| `crawl.page`      | Individual page scraped     | After each page is successfully scraped |
| `crawl.completed` | Crawl finished successfully | When all pages are processed            |
| `crawl.failed`    | Crawl encountered an error  | When crawl fails or is cancelled        |

### Batch Scrape Events

| Event                    | Description                | When Triggered                          |
| ------------------------ | -------------------------- | --------------------------------------- |
| `batch_scrape.started`   | Batch scrape job initiated | When batch scrape begins                |
| `batch_scrape.page`      | Individual URL scraped     | After each URL is successfully scraped  |
| `batch_scrape.completed` | Batch scrape finished      | When all URLs are processed             |
| `batch_scrape.failed`    | Batch scrape failed        | When batch scrape fails or is cancelled |

## Webhook Payload Structure

All webhook payloads follow this structure:

```json
{
  "success": true,
  "type": "crawl.page",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [...],
  "metadata": {
    "user_id": "12345",
    "project": "web-scraping"
  },
  "error": null,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Payload Fields

| Field       | Type    | Description                                               |
| ----------- | ------- | --------------------------------------------------------- |
| `success`   | boolean | Whether the operation was successful                      |
| `type`      | string  | Event type (e.g., `crawl.page`, `batch_scrape.completed`) |
| `id`        | string  | Unique identifier for the crawl/batch scrape job          |
| `data`      | array   | Scraped content (populated for `page` events)             |
| `metadata`  | object  | Custom metadata from your webhook configuration           |
| `error`     | string  | Error message (present when `success` is `false`)         |
| `timestamp` | string  | ISO 8601 timestamp of when the event occurred             |

## Examples

### Crawl with Webhook

```bash cURL
curl -X POST https://api.firecrawl.dev/v1/crawl \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer YOUR_API_KEY' \
    -d '{
      "url": "https://docs.firecrawl.dev",
      "limit": 100,
      "webhook": {
        "url": "https://your-domain.com/webhook",
        "metadata": {
          "any_key": "any_value"
        },
        "events": ["started", "page", "completed"]
      }
    }'
```

### Batch Scrape with Webhook

```bash cURL
curl -X POST https://api.firecrawl.dev/v1/batch/scrape \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer YOUR_API_KEY' \
    -d '{
      "urls": [\
        "https://example.com/page1",\
        "https://example.com/page2",\
        "https://example.com/page3"\
      ],
      "webhook": {
        "url": "https://your-domain.com/webhook",
        "metadata": {
          "any_key": "any_value"
        },
        "events": ["started", "page", "completed"]
      }
    }'
```

### Webhook Endpoint Example

Here's how to handle webhooks in your application:

<CodeGroup>
  ```javascript Node.js/Express
  const express = require('express');
  const app = express();

  app.post('/webhook', express.json(), (req, res) => {
    const { success, type, id, data, metadata, error } = req.body;

    switch (type) {
      case 'crawl.started':
      case 'batch_scrape.started':
        console.log(`${type.split('.')[0]} ${id} started`);
        break;

      case 'crawl.page':
      case 'batch_scrape.page':
        if (success && data.length > 0) {
          console.log(`Page scraped: ${data[0].metadata.sourceURL}`);
          // Process the scraped page data
          processScrapedPage(data[0]);
        }
        break;

      case 'crawl.completed':
      case 'batch_scrape.completed':
        console.log(`${type.split('.')[0]} ${id} completed successfully`);
        break;

      case 'crawl.failed':
      case 'batch_scrape.failed':
        console.error(`${type.split('.')[0]} ${id} failed: ${error}`);
        break;
    }

    // Always respond with 200 to acknowledge receipt
    res.status(200).send('OK');
  });

  function processScrapedPage(pageData) {
    // Your processing logic here
    console.log('Processing:', pageData.metadata.title);
  }

  app.listen(3000, () => {
    console.log('Webhook server listening on port 3000');
  });
  ```

  ```python Python/Flask
  from flask import Flask, request, jsonify

  app = Flask(__name__)

  @app.route('/webhook', methods=['POST'])
  def handle_webhook():
      payload = request.get_json()

      success = payload.get('success')
      event_type = payload.get('type')
      job_id = payload.get('id')
      data = payload.get('data', [])
      metadata = payload.get('metadata', {})
      error = payload.get('error')

      if event_type in ['crawl.started', 'batch_scrape.started']:
          operation = event_type.split('.')[0]
          print(f"{operation} {job_id} started")

      elif event_type in ['crawl.page', 'batch_scrape.page']:
          if success and data:
              page = data[0]
              print(f"Page scraped: {page['metadata']['sourceURL']}")
              process_scraped_page(page)

      elif event_type in ['crawl.completed', 'batch_scrape.completed']:
          operation = event_type.split('.')[0]
          print(f"{operation} {job_id} completed successfully")

      elif event_type in ['crawl.failed', 'batch_scrape.failed']:
          operation = event_type.split('.')[0]
          print(f"{operation} {job_id} failed: {error}")

      return jsonify({"status": "received"}), 200

  def process_scraped_page(page_data):
      # Your processing logic here
      print(f"Processing: {page_data['metadata']['title']}")

  if __name__ == '__main__':
      app.run(host='0.0.0.0', port=3000)
  ```
</CodeGroup>

## Event-Specific Payloads

### `started` Events

```json
{
  "success": true,
  "type": "crawl.started",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [],
  "metadata": {
    "user_id": "12345",
    "project": "web-scraping"
  },
  "error": null
}
```

### `page` Events

```json
{
  "success": true,
  "type": "crawl.page",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [\
    {\
      "markdown": "# Page Title\n\nPage content...",\
      "metadata": {\
        "title": "Page Title",\
        "description": "Page description",\
        "sourceURL": "https://example.com/page1",\
        "statusCode": 200\
      }\
    }\
  ],
  "metadata": {
    "any_key": "any_value"
  },
  "error": null
}
```

### `completed` Events

```json
{
  "success": true,
  "type": "crawl.completed",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [],
  "metadata": {
    "any_key": "any_value"
  },
  "error": null
}
```

### `failed` Events

```json
{
  "success": false,
  "type": "crawl.failed",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [],
  "metadata": {
    "any_key": "any_value"
  },
  "error": "Error message"
}
```

## Monitoring and Debugging

### Testing Your Webhook

Use tools like [ngrok](https://ngrok.com) for local development:

```bash
# Expose local server
ngrok http 3000

# Use the ngrok URL in your webhook configuration
# https://abc123.ngrok.io/webhook
```

### Webhook Logs

Monitor webhook delivery in your application:

```javascript
app.post('/webhook', (req, res) => {
  console.log('Webhook received:', {
    timestamp: new Date().toISOString(),
    type: req.body.type,
    id: req.body.id,
    success: req.body.success
  });

  res.status(200).send('OK');
});
```

## Common Issues

### Webhook Not Receiving Events

1. **Check URL accessibility** - Ensure your endpoint is publicly accessible
2. **Verify HTTPS** - Webhook URLs must use HTTPS
3. **Check firewall settings** - Allow incoming connections to your webhook port
4. **Review event filters** - Ensure you're subscribed to the correct event types

````