# 1\. Using Command Line Arguments

Generate LLMs.txt with NPX

[Documentation](https://docs.firecrawl.dev/introduction) [SDKs](https://docs.firecrawl.dev/sdks/overview) [Learn](https://www.firecrawl.dev/blog/category/tutorials) [Integrations](https://www.firecrawl.dev/app) [API Reference](https://docs.firecrawl.dev/api-reference/introduction)

On this page

- [generate-llmstxt](https://docs.firecrawl.dev/features/alpha/llmstxt-npx#generate-llmstxt)
- [Usage](https://docs.firecrawl.dev/features/alpha/llmstxt-npx#usage)
- [1\. Using Command Line Arguments](https://docs.firecrawl.dev/features/alpha/llmstxt-npx#1-using-command-line-arguments)
- [2\. Using Environment Variables](https://docs.firecrawl.dev/features/alpha/llmstxt-npx#2-using-environment-variables)
- [Options](https://docs.firecrawl.dev/features/alpha/llmstxt-npx#options)
- [Examples](https://docs.firecrawl.dev/features/alpha/llmstxt-npx#examples)
- [Requirements](https://docs.firecrawl.dev/features/alpha/llmstxt-npx#requirements)
- [Output](https://docs.firecrawl.dev/features/alpha/llmstxt-npx#output)
- [License](https://docs.firecrawl.dev/features/alpha/llmstxt-npx#license)

generate-llmstxt

A simple NPX package that generates LLMs.txt files in the CLI using the Firecrawl API. This package creates two files in your specified output directory (defaults to ‘public’ folder):

- `llms.txt`: Contains a summary of the LLM-related content
- `llms-full.txt`: Contains the full text content

Usage

You can run this package using NPX without installing it. There are two ways to provide your Firecrawl API key:

#1\. Using Command Line Arguments

```
npx generate-llmstxt --api-key YOUR_FIRECRAWL_API_KEY

```

#2\. Using Environment Variables

Create a `.env` file in your project root and add your API key:

```
FIRECRAWL_API_KEY=your_api_key_here

```

Then run the command without the,api-key option:

```
npx generate-llmstxt

```

#Options

- `-k, --api-key <key>` (optional if set in .env): Your Firecrawl API key
- `-u, --url <url>` (optional): URL to analyze (default: [https://example.com](https://example.com/))
- `-m, --max-urls <number>` (optional): Maximum number of URLs to analyze (default: 50)
- `-o, --output-dir <path>` (optional): Output directory path (default: ‘public’)

#Examples

```
# Using command line argument with default output directory
npx generate-llmstxt -k your_api_key -u https://your-website.com -m 20

# Using .env file with default output directory
npx generate-llmstxt -u https://your-website.com -m 20

# Specifying a custom output directory
npx generate-llmstxt -k your_api_key -u https://your-website.com -o custom/path/to/output

# Using .env file and custom output directory
npx generate-llmstxt -u https://your-website.com -o content/llms

```

Requirements

- Node.js 14 or higher
- A valid Firecrawl API key (via command line or .env file)

Output

The package will create two files in your specified output directory (defaults to ‘public’):

1. `llms.txt`: Contains a summary of the LLM-related content
2. `llms-full.txt`: Contains the full text content

License

MIT