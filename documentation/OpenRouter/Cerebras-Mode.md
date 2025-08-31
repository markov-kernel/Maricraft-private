---
title: Cerebras OpenAI: GPT OSS 120B API Guide
subtitle: Complete guide to using OpenAI: GPT OSS 120B models on Cerebras infrastructure via OpenRouter
headline: Cerebras OpenAI: GPT OSS 120B Models | Ultra-Fast AI with OpenRouter API
canonical-url: 'https://openrouter.ai/docs/features/cerebras-api-guide'
'og:site_name': OpenRouter Documentation
'og:title': Cerebras OpenAI: GPT OSS 120B Models API Guide - Ultra-Fast AI with OpenRouter
'og:description': >-
  Complete API guide for using OpenAI: GPT OSS 120B models on Cerebras wafer-scale infrastructure.
  Get 1,500+ tokens/second with advanced features like tool calling and structured outputs.
'og:image':
  type: url
  value: >-
    https://openrouter.ai/dynamic-og?title=Cerebras%20API%20Guide&description=Ultra-Fast%20AI%20with%20OpenRouter
'og:image:width': 1200
'og:image:height': 630
'twitter:card': summary_large_image
'twitter:site': '@OpenRouterAI'
noindex: false
nofollow: false
---

# Cerebras OpenAI: GPT OSS 120B Models API Guide

This comprehensive guide shows you how to use OpenRouter's API with Cerebras-provided OpenAI: GPT OSS 120B models, leveraging their wafer-scale engine for ultra-fast inference (≈1,500 tokens/second).

## Available Model

OpenRouter provides access to the OpenAI: GPT OSS 120B model on Cerebras infrastructure:

### OpenAI: GPT OSS 120B
- **Model ID**: `openai/gpt-oss-120b`
- **Context**: 131K tokens
- **Special Feature**: Chain-of-thought with `<think>` blocks and Enhanced alignment and instruction following.
- **Use Case**: Transparent reasoning, agent workflows, tool use traces, chat assistants, coding, concise responses.
- **Speed**: ~1,500 tokens/second
- **Pricing**: $0.60/M input, $1.20/M output (Cerebras provider)

## Authentication & Setup

All requests require authentication using your OpenRouter API key:

```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

## Basic API Usage

### Force Cerebras Provider (Required)

To ensure you're using Cerebras infrastructure exclusively (no fallbacks), always use provider routing:

```typescript
const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer $OPENROUTER_API_KEY',
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'openai/gpt-oss-120b',
    provider: {
      order: ['Cerebras'],
      require_parameters: true
    },
    messages: [
      {
        role: 'user',
        content: 'Explain quantum computing in simple terms'
      }
    ]
  })
});
```

```python
import requests

response = requests.post(
    'https://openrouter.ai/api/v1/chat/completions',
    headers={
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
    },
    json={
        'model': 'openai/gpt-oss-120b',
        'provider': {
            'order': ['Cerebras'],
            'require_parameters': True
        },
        'messages': [
            {
                'role': 'user',
                'content': 'Explain quantum computing in simple terms'
            }
        ]
    }
)
```

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -d '{
    "model": "openai/gpt-oss-120b",
    "provider": {
      "order": ["Cerebras"],
      "require_parameters": true
    },
    "messages": [
      {
        "role": "user",
        "content": "Explain quantum computing in simple terms"
      }
    ]
  }'
```

## Chain-of-Thought

The model supports visible reasoning with `<think>` blocks:

```python
import requests

response = requests.post(
    'https://openrouter.ai/api/v1/chat/completions',
    headers={
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
    },
    json={
        'model': 'openai/gpt-oss-120b',
        'provider': {
            'order': ['Cerebras'],
            'require_parameters': True
        },
        'messages': [
            {
                'role': 'user',
                'content': '''Solve this step by step: If a train travels 120 miles in 2 hours, 
                then speeds up and travels 180 miles in the next 1.5 hours, what's the average speed?'''
            }
        ]
    }
)

# Response will include <think> blocks showing the reasoning process
print(response.json()['choices'][0]['message']['content'])
```

```typescript
const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer $OPENROUTER_API_KEY',
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'openai/gpt-oss-120b',
    provider: {
      order: ['Cerebras'],
      require_parameters: true
    },
    messages: [
      {
        role: 'user',
        content: `Solve this step by step: If a train travels 120 miles in 2 hours, 
        then speeds up and travels 180 miles in the next 1.5 hours, what's the average speed?`
      }
    ]
  })
});

// Response will include <think> blocks showing the reasoning process
const data = await response.json();
console.log(data.choices[0].message.content);
```

## Streaming for Real-time Applications

Take advantage of Cerebras' 1,500 tokens/second speed with streaming:

```typescript
const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer $OPENROUTER_API_KEY',
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'openai/gpt-oss-120b',
    provider: {
      order: ['Cerebras'],
      require_parameters: true
    },
    stream: true,
    messages: [
      {
        role: 'user',
        content: 'Write a detailed explanation of machine learning algorithms'
      }
    ]
  })
});

// Handle streaming response
const reader = response.body?.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  
  const chunk = decoder.decode(value);
  const lines = chunk.split('\n');
  
  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = line.slice(6);
      if (data === '[DONE]') continue;
      
      try {
        const parsed = JSON.parse(data);
        const content = parsed.choices[0]?.delta?.content;
        if (content) {
          process.stdout.write(content);
        }
      } catch (e) {
        // Skip invalid JSON
      }
    }
  }
}
```

```python
import requests
import json

response = requests.post(
    'https://openrouter.ai/api/v1/chat/completions',
    headers={
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
    },
    json={
        'model': 'openai/gpt-oss-120b',
        'provider': {
            'order': ['Cerebras'],
            'require_parameters': True
        },
        'stream': True,
        'messages': [
            {
                'role': 'user',
                'content': 'Write a detailed explanation of machine learning algorithms'
            }
        ]
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        decoded_line = line.decode('utf-8')
        if decoded_line.startswith('data: '):
            data = decoded_line[6:]
            if data == '[DONE]':
                break
            try:
                parsed = json.loads(data)
                content = parsed['choices'][0]['delta'].get('content')
                if content:
                    print(content, end='', flush=True)
            except json.JSONDecodeError:
                continue
```

## Structured Outputs

Force Cerebras models to return valid JSON with structured outputs:

```python
import requests

response = requests.post(
    'https://openrouter.ai/api/v1/chat/completions',
    headers={
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
    },
    json={
        'model': 'openai/gpt-oss-120b',
        'provider': {
            'order': ['Cerebras'],
            'require_parameters': True
        },
        'response_format': {
            'type': 'json_schema',
            'json_schema': {
                'name': 'code_analysis',
                'strict': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'language': {
                            'type': 'string',
                            'description': 'Programming language detected'
                        },
                        'complexity': {
                            'type': 'string',
                            'enum': ['low', 'medium', 'high']
                        },
                        'suggestions': {
                            'type': 'array',
                            'items': {'type': 'string'},
                            'description': 'Improvement suggestions'
                        },
                        'score': {
                            'type': 'number',
                            'minimum': 0,
                            'maximum': 10
                        }
                    },
                    'required': ['language', 'complexity', 'suggestions', 'score'],
                    'additionalProperties': False
                }
            }
        },
        'messages': [
            {
                'role': 'user',
                'content': '''Analyze this code:
                
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr'''
            }
        ]
    }
)

# Returns guaranteed valid JSON matching the schema
data = response.json()
analysis = json.loads(data['choices'][0]['message']['content'])
print(f"Language: {analysis['language']}")
print(f"Complexity: {analysis['complexity']}")
print(f"Score: {analysis['score']}/10")
```

```typescript
const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer $OPENROUTER_API_KEY',
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'openai/gpt-oss-120b',
    provider: {
      order: ['Cerebras'],
      require_parameters: true
    },
    response_format: {
      type: 'json_schema',
      json_schema: {
        name: 'code_analysis',
        strict: true,
        schema: {
          type: 'object',
          properties: {
            language: {
              type: 'string',
              description: 'Programming language detected'
            },
            complexity: {
              type: 'string',
              enum: ['low', 'medium', 'high']
            },
            suggestions: {
              type: 'array',
              items: { type: 'string' },
              description: 'Improvement suggestions'
            },
            score: {
              type: 'number',
              minimum: 0,
              maximum: 10
            }
          },
          required: ['language', 'complexity', 'suggestions', 'score'],
          additionalProperties: false
        }
      }
    },
    messages: [
      {
        role: 'user',
        content: `Analyze this code:
        
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr`
      }
    ]
  })
});

// Returns guaranteed valid JSON matching the schema
const data = await response.json();
const analysis = JSON.parse(data.choices[0].message.content);
console.log(`Language: ${analysis.language}`);
console.log(`Complexity: ${analysis.complexity}`);
console.log(`Score: ${analysis.score}/10`);
```

## Tool Calling

Use Cerebras models with function calling for agent workflows:

```python
import requests
import json

def get_weather(location: str) -> str:
    """Mock weather function"""
    return f"The weather in {location} is sunny, 22°C"

def calculate_math(expression: str) -> str:
    """Safe math evaluation"""
    try:
        result = eval(expression)  # In production, use a safer eval
        return str(result)
    except:
        return "Invalid expression"

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_math",
            "description": "Perform mathematical calculations",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

messages = [
    {
        "role": "user",
        "content": "What's the weather in Tokyo and what's 15 * 23?"
    }
]

# Initial request
response = requests.post(
    'https://openrouter.ai/api/v1/chat/completions',
    headers={
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
    },
    json={
        'model': 'openai/gpt-oss-120b',
        'provider': {
            'order': ['Cerebras'],
            'require_parameters': True
        },
        'tools': tools,
        'messages': messages
    }
)

response_data = response.json()
assistant_message = response_data['choices'][0]['message']
messages.append(assistant_message)

# Process tool calls
if assistant_message.get('tool_calls'):
    for tool_call in assistant_message['tool_calls']:
        function_name = tool_call['function']['name']
        arguments = json.loads(tool_call['function']['arguments'])
        
        if function_name == 'get_weather':
            result = get_weather(arguments['location'])
        elif function_name == 'calculate_math':
            result = calculate_math(arguments['expression'])
        
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call['id'],
            "name": function_name,
            "content": result
        })

# Final response with tool results
final_response = requests.post(
    'https://openrouter.ai/api/v1/chat/completions',
    headers={
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
    },
    json={
        'model': 'openai/gpt-oss-120b',
        'provider': {
            'order': ['Cerebras'],
            'require_parameters': True
        },
        'tools': tools,
        'messages': messages
    }
)

print(final_response.json()['choices'][0]['message']['content'])
```

## Prompt Caching

Optimize costs for large contexts with prompt caching:

```python
import requests

# First request with cache setup
response1 = requests.post(
    'https://openrouter.ai/api/v1/chat/completions',
    headers={
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
    },
    json={
        'model': 'openai/gpt-oss-120b',
        'provider': {
            'order': ['Cerebras'],
            'require_parameters': True
        },
        'messages': [
            {
                'role': 'system',
                'content': [
                    {
                        'type': 'text',
                        'text': 'You are a helpful coding assistant. Here is a large codebase to analyze:'
                    },
                    {
                        'type': 'text',
                        'text': '''
                        # Very large codebase content here (multiple files, docs, etc.)
                        # This content will be cached for subsequent requests
                        ''',
                        'cache_control': {
                            'type': 'ephemeral'
                        }
                    }
                ]
            },
            {
                'role': 'user',
                'content': 'What are the main functions in this codebase?'
            }
        ]
    }
)

# Subsequent requests will use cached content and be much faster/cheaper
response2 = requests.post(
    'https://openrouter.ai/api/v1/chat/completions',
    headers={
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
    },
    json={
        'model': 'openai/gpt-oss-120b',
        'provider': {
            'order': ['Cerebras'],
            'require_parameters': True
        },
        'messages': [
            # Same cached system message
            {
                'role': 'system',
                'content': [
                    {
                        'type': 'text',
                        'text': 'You are a helpful coding assistant. Here is a large codebase to analyze:'
                    },
                    {
                        'type': 'text',
                        'text': '''
                        # Same large codebase content
                        ''',
                        'cache_control': {
                            'type': 'ephemeral'
                        }
                    }
                ]
            },
            {
                'role': 'user',
                'content': 'What are the main functions in this codebase?'
            },
            {
                'role': 'assistant',
                'content': 'Previous response...'
            },
            {
                'role': 'user',
                'content': 'Now find potential bugs in the authentication module.'
            }
        ]
    }
)
```

## Web Search Integration

Add real-time web data to Cerebras models:

```typescript
const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer $OPENROUTER_API_KEY',
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'openai/gpt-oss-120b',
    provider: {
      order: ['Cerebras'],
      require_parameters: true
    },
    plugins: [
      {
        id: 'web',
        max_results: 5,
        search_prompt: 'Use the following current web search results to answer the user:'
      }
    ],
    messages: [
      {
        role: 'user',
        content: 'What are the latest developments in quantum computing in 2024?'
      }
    ]
  })
});

// Response will include web search results and citations
const data = await response.json();
console.log(data.choices[0].message.content);
console.log('Citations:', data.choices[0].message.annotations);
```

## Large Context Usage (131K tokens)

Leverage the full 131K context window:

```python
import requests

# Example: Analyzing a very large document
large_document = """
# Insert very large document here - up to ~131K tokens
# This could be multiple research papers, code files, books, etc.
"""

response = requests.post(
    'https://openrouter.ai/api/v1/chat/completions',
    headers={
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json',
    },
    json={
        'model': 'openai/gpt-oss-120b',
        'provider': {
            'order': ['Cerebras'],
            'require_parameters': True
        },
        'messages': [
            {
                'role': 'system',
                'content': f'You are analyzing this large document: {large_document}'
            },
            {
                'role': 'user',
                'content': 'Create a comprehensive summary with key insights, methodology, and conclusions.'
            }
        ],
        'max_tokens': 4000,  # Long response
        'temperature': 0.3   # Focused analysis
    }
)

print(response.json()['choices'][0]['message']['content'])
```

## Error Handling & Rate Limits

Handle Cerebras-specific considerations:

```python
import requests
import time
from typing import Dict, Any

def make_cerebras_request(payload: Dict[str, Any], max_retries: int = 3):
    """Make request to Cerebras with retry logic"""
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {OPENROUTER_API_KEY}',
                    'Content-Type': 'application/json',
                },
                json=payload,
                timeout=60  # Cerebras is fast, but large contexts may take time
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                # Rate limit - wait and retry
                wait_time = 2 ** attempt
                print(f"Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
            elif response.status_code == 503:
                # Service unavailable - Cerebras may be down
                print("Cerebras unavailable, retrying...")
                time.sleep(5)
            else:
                response.raise_for_status()
                
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            print(f"Request failed (attempt {attempt + 1}): {e}")
            time.sleep(2)
    
    raise Exception(f"Failed after {max_retries} attempts")

# Usage
payload = {
    'model': 'openai/gpt-oss-120b',
    'provider': {
        'order': ['Cerebras'],
        'require_parameters': True
    },
    'messages': [
        {
            'role': 'user',
            'content': 'Your query here'
        }
    ]
}

result = make_cerebras_request(payload)
print(result['choices'][0]['message']['content'])
```

## Monitoring Usage

Check your API usage and costs:

```python
import requests

# Check API key stats
auth_response = requests.get(
    'https://openrouter.ai/api/v1/auth/key',
    headers={'Authorization': f'Bearer {OPENROUTER_API_KEY}'}
)

print("API Key Stats:", auth_response.json())

# Check generation details (after making a request)
generation_id = "your_generation_id_from_response"
generation_response = requests.get(
    f'https://openrouter.ai/api/v1/generation?id={generation_id}',
    headers={'Authorization': f'Bearer {OPENROUTER_API_KEY}'}
)

print("Generation Stats:", generation_response.json())
```

```typescript
// Check API key stats
const authResponse = await fetch('https://openrouter.ai/api/v1/auth/key', {
  headers: { 'Authorization': 'Bearer $OPENROUTER_API_KEY' }
});

console.log("API Key Stats:", await authResponse.json());

// Check generation details (after making a request)
const generationId = "your_generation_id_from_response";
const generationResponse = await fetch(
  `https://openrouter.ai/api/v1/generation?id=${generationId}`,
  { headers: { 'Authorization': 'Bearer $OPENROUTER_API_KEY' } }
);

console.log("Generation Stats:", await generationResponse.json());
```

## Performance Tips

1. **Force Cerebras Provider**: Always specify Cerebras in provider routing to ensure ultra-fast inference
2. **Leverage Speed**: Enable streaming to see Cerebras' 1,500 tokens/second in action
3. **Cache Large Contexts**: Use prompt caching for repeated analysis of large documents
4. **Optimize Parameters**: Use appropriate temperature settings (0.1-0.3 for reasoning, 0.7-0.9 for creativity)

## Important Notes

- **Always force Cerebras provider** using the `provider` parameter to ensure you get the ultra-fast wafer-scale inference
- **No fallbacks** - If Cerebras is unavailable, requests will fail rather than falling back to slower providers
- **131K context limit** - The model is currently capped at 131K tokens on Cerebras infrastructure
- **Ultra-fast streaming** - Take advantage of 1,500 tokens/second throughput with streaming enabled

This guide covers all major OpenRouter features specifically configured for Cerebras infrastructure, ensuring you get maximum performance from this ultra-fast model.
