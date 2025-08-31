---
title: Using any model via OpenRouter and LiteLLM
---

# Using any model via OpenRouter and LiteLLM

This guide provides a reliable recipe for wiring **Gemini 2.5 Flash** (hosted on OpenRouter) into the **OpenAI Agents SDK** through the SDK’s built‑in LiteLLM integration.

---

## 1. Install the right extras

```bash
pip install "openai-agents[litellm]"   # pulls in litellm>=2.x
```

The `[litellm]` extra adds `agents.extensions.models.LitellmModel`, so you don’t have to write a custom provider class.

---

## 2. Gather the four values the code will need

| What                        | Where to get / set it                                                                                                                                                                                      |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`OPENROUTER_API_KEY`**    | Your key from the *OpenRouter → API Keys* page                                                                                                                                                             |
| **`model`** string          | `openrouter/openai/gpt-5-mini`  ([OpenRouter](https://openrouter.ai/openai/gpt-5-mini))                                                                                    |
| **`base_url`**              | `https://openrouter.ai/api/v1` (the OpenRouter OpenAI‑compatible endpoint) ([OpenRouter](https://openrouter.ai/docs/quickstart?utm_source=chatgpt.com))                                                                                                               |
| **Site attribution (opt.)** | Either export<br>`OR_SITE_URL` and `OR_APP_NAME` **or** pass `extra_headers={"HTTP-Referer": …, "X-Title": …}`. This helps your traffic get ranked on OpenRouter but isn’t required ([docs.litellm.ai](https://docs.litellm.ai/docs/providers/openrouter)) |

*(If you self‑host a LiteLLM proxy instead of calling OpenRouter directly, point `base_url` at your proxy instead and keep the same `model` string.)*

---

## 3. Drop the model into an Agent

```python
import os, asyncio
from agents import Agent, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel

os.environ["OPENROUTER_API_KEY"] = "sk-or-..." # or read from .env
# OPTIONAL attribution headers
os.environ["OR_SITE_URL"] = "https://mycoolapp.com"
os.environ["OR_APP_NAME"] = "Weather‑Haiku‑Bot"

@function_tool
def get_weather(city: str):
    return f"The weather in {city} is sunny."

agent = Agent(
    name="GeminiFlashAssistant",
    instructions="Answer in haiku.",
    model=LitellmModel(
        model="openrouter/openai/gpt-5-mini",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    ),
    tools=[get_weather],
)

asyncio.run(Runner.run(agent, "Weather in Tokyo?"))
```

The `LitellmModel` constructor matches the `model`, `base_url`, and `api_key` signature shown in the Agents SDK docs.

---

## 5. Common pitfalls

| Symptom                              | Likely cause / fix                                                                                                                                                                                                |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **401 Unauthorized**                 | Missing `OPENROUTER_API_KEY` *or* using OpenAI’s key instead of OpenRouter’s                                                                                                                             |
| **Tool calls never trigger**         | Gemini 2.5 Flash currently understands OpenAI‑style function‑calling but is *very* temperature‑sensitive. Set `temperature≈0.2` and give an explicit “call the tool when needed” reminder in system instructions. |
| **Long contexts silently truncated** | Agents SDK still caps context windows at 256 k tokens. Gemini 2.5 Flash supports 1 M, but anything above the SDK limit is clipped. Plan chunking accordingly.                                                     |

---

## TL;DR

1.  **Install** the Agents SDK’s `litellm` extras.
2.  **Pass** `model="openrouter/openai/gpt-5-mini"` (or `…:thinking`) into `LitellmModel`.
3.  **Point** `base_url` to `https://openrouter.ai/api/v1` and supply `OPENROUTER_API_KEY`.


---

## Working with Images and PDFs via OpenRouter

When using OpenRouter, you can send images and PDFs. However, the way you send them, especially PDFs, is different from the standard Agents SDK. You'll be interacting with the OpenRouter API directly for these file types.

### Image Inputs

Requests with images, to multimodal models, are available via the `/api/v1/chat/completions` API with a multi-part `messages` parameter. The `image_url` can either be a URL or a base64-encoded image.

#### Using Image URLs

Here's how to send an image using a URL:

```python
import litellm
import asyncio
import base64
from pathlib import Path

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

async def main():
    # Read and encode the image
    image_path = "path/to/your/image.jpg"
    base64_image = encode_image_to_base64(image_path)
    data_url = f"data:image/jpeg;base64,{base64_image}"

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What's in this image?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": data_url
                    }
                }
            ]
        }
    ]

    response = await litellm.acompletion(
      model="openrouter/openai/gpt-5-mini",
      messages=messages,
      api_base="https://openrouter.ai/api/v1",
      api_key="YOUR_OPENROUTER_API_KEY"
    )
    print(response)

asyncio.run(main())
```
Supported image content types are: `image/png`, `image/jpeg`, `image/webp`.

### PDF Support with OpenRouter

A key difference when using OpenRouter is how you handle PDFs. Instead of relying on the Agents SDK's built-in file handling, you will send the PDF data directly to the OpenRouter API using `litellm`. This is because OpenRouter has its own PDF processing capabilities.

OpenRouter supports PDF processing through `litellm.acompletion`. PDFs can be sent as base64-encoded data URLs in the messages array, via the file content type. This feature works on **any** model on OpenRouter.

When a model supports file input natively, the PDF is passed directly to the model. When the model does not support file input natively, OpenRouter will parse the file and pass the parsed results to the requested model.

#### Plugin Configuration

To configure PDF processing, use the `plugins` parameter in your request. OpenRouter provides several PDF processing engines with different capabilities and pricing:

```json
{
  "plugins": [
    {
      "id": "file-parser",
      "pdf": {
        "engine": "pdf-text"
      }
    }
  ]
}
```

#### Pricing

OpenRouter provides several PDF processing engines:

1.  `"mistral-ocr"`: Best for scanned documents or PDFs with images.
2.  `"pdf-text"`: Best for well-structured PDFs with clear text content (Free).
3.  `"native"`: Only available for models that support file input natively (charged as input tokens).

If you don't explicitly specify an engine, OpenRouter will default first to the model's native file processing capabilities, and if that's not available, it will use the `"pdf-text"` engine.

#### Processing PDFs

Here's how to send and process a PDF using `litellm`:

```python
import litellm
import asyncio
import base64
from pathlib import Path

def encode_pdf_to_base64(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        return base64.b64encode(pdf_file.read()).decode('utf-8')

async def main():
    # Read and encode the PDF
    pdf_path = "path/to/your/document.pdf"
    base64_pdf = encode_pdf_to_base64(pdf_path)
    data_url = f"data:application/pdf;base64,{base64_pdf}"

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What are the main points in this document?"
                },
                {
                    "type": "file",
                    "file": {
                        "filename": "document.pdf",
                        "file_data": data_url
                    }
                },
            ]
        }
    ]

    # Optional: Configure PDF processing engine
    # PDF parsing will still work even if the plugin is not explicitly set
    plugins = [
        {
            "id": "file-parser",
            "pdf": {
                "engine": "pdf-text"
            }
        }
    ]

    response = await litellm.acompletion(
      model="openrouter/openai/gpt-5-mini",
      messages=messages,
      plugins=plugins,
      api_base="https://openrouter.ai/api/v1",
      api_key="YOUR_OPENROUTER_API_KEY"
    )
    print(response)

asyncio.run(main())
```

#### Skip Parsing Costs

When you send a PDF to the API, the response may include file annotations in the assistant's message. By sending these annotations back in subsequent requests, you can avoid re-parsing the same PDF document multiple times, which saves both processing time and costs.

Here's how to reuse file annotations:

```python
import litellm
import asyncio
import base64
from pathlib import Path

# First, encode and send the PDF
def encode_pdf_to_base64(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        return base64.b64encode(pdf_file.read()).decode('utf-8')

async def main():
    # Read and encode the PDF
    pdf_path = "path/to/your/document.pdf"
    base64_pdf = encode_pdf_to_base64(pdf_path)
    data_url = f"data:application/pdf;base64,{base64_pdf}"

    # Initial request with the PDF
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What are the main points in this document?"
                },
                {
                    "type": "file",
                    "file": {
                        "filename": "document.pdf",
                        "file_data": data_url
                    }
                },
            ]
        }
    ]

    response = await litellm.acompletion(
      model="openrouter/openai/gpt-5-mini",
      messages=messages,
      api_base="https://openrouter.ai/api/v1",
      api_key="YOUR_OPENROUTER_API_KEY"
    )
    response_data = response.dict()

    # Store the annotations from the response
    file_annotations = None
    if response_data.get("choices") and len(response_data["choices"]) > 0:
        if "annotations" in response_data["choices"][0]["message"]:
            file_annotations = response_data["choices"][0]["message"]["annotations"]

    # Follow-up request using the annotations (without sending the PDF again)
    if file_annotations:
        follow_up_messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What are the main points in this document?"
                    },
                    {
                        "type": "file",
                        "file": {
                            "filename": "document.pdf",
                            "file_data": data_url
                        }
                    }
                ]
            },
            {
                "role": "assistant",
                "content": "The document contains information about...",
                "annotations": file_annotations
            },
            {
                "role": "user",
                "content": "Can you elaborate on the second point?"
            }
        ]

        follow_up_response = await litellm.acompletion(
          model="openrouter/openai/gpt-5-mini",
          messages=follow_up_messages,
          api_base="https://openrouter.ai/api/v1",
          api_key="YOUR_OPENROUTER_API_KEY"
        )
        print(follow_up_response)

asyncio.run(main())
```

When you include the file annotations from a previous response in your subsequent requests, OpenRouter will use this pre-parsed information instead of re-parsing the PDF, which saves processing time and costs.
This is especially beneficial for large documents or when using the `mistral-ocr` engine which incurs additional costs.
