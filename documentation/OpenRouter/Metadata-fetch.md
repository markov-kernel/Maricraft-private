Send a completion request to a selected model (text-only format)

### Headers

AuthorizationstringRequired

Bearer authentication of the form Bearer <token>, where token is your auth token.

### Request

This endpoint expects an object.

modelstringRequired

The model ID to use. If unspecified, the user's default is used.

promptstringRequired

The text prompt to complete

modelslist of stringsOptional

Alternate list of models for routing overrides.

providerobjectOptional

Preferences for provider routing.

Show 1 properties

reasoningobjectOptional

Configuration for model reasoning/thinking tokens

Show 3 properties

usageobjectOptional

Whether to include usage information in the response

Show 1 properties

transformslist of stringsOptional

List of prompt transforms (OpenRouter-only).

streambooleanOptionalDefaults to `false`

Enable streaming of results.

max\_tokensintegerOptional

Maximum number of tokens (range: \[1, context\_length)).\
\
temperaturedoubleOptional\
\
Sampling temperature (range: \[0, 2\]).\
\
seedintegerOptional\
\
Seed for deterministic outputs.\
\
top\_pdoubleOptional\
\
Top-p sampling value (range: (0, 1\]).

top\_kintegerOptional

Top-k sampling value (range: \[1, Infinity)).\
\
frequency\_penaltydoubleOptional\
\
Frequency penalty (range: \[-2, 2\]).\
\
presence\_penaltydoubleOptional\
\
Presence penalty (range: \[-2, 2\]).\
\
repetition\_penaltydoubleOptional\
\
Repetition penalty (range: (0, 2\]).

logit\_biasmap from strings to doublesOptional

Mapping of token IDs to bias values.

top\_logprobsintegerOptional

Number of top log probabilities to return.

min\_pdoubleOptional

Minimum probability threshold (range: \[0, 1\]).

top\_adoubleOptional

Alternate top sampling parameter (range: \[0, 1\]).

userstringOptional

A stable identifier for your end-users. Used to help detect and prevent abuse.

### Response

Successful completion

idstring or null

choiceslist of objects or null

Show 3 properties
{
  "id": "string",
  "choices": [
    {
      "text": "string",
      "index": 1,
      "finish_reason": "string"
    }
  ]
}

Returns metadata about a specific generation request

### Headers

AuthorizationstringRequired

Bearer authentication of the form Bearer <token>, where token is your auth token.

### Query parameters

idstringRequired

### Response

Returns the request metadata for this generation

dataobject

Show 27 properties
{
  "data": {
    "id": "string",
    "total_cost": 1.1,
    "created_at": "string",
    "model": "string",
    "origin": "string",
    "usage": 1.1,
    "is_byok": true,
    "upstream_id": "string",
    "cache_discount": 1.1,
    "upstream_inference_cost": 1.1,
    "app_id": 1,
    "streamed": true,
    "cancelled": true,
    "provider_name": "string",
    "latency": 1,
    "moderation_latency": 1,
    "generation_time": 1,
    "finish_reason": "string",
    "native_finish_reason": "string",
    "tokens_prompt": 1,
    "tokens_completion": 1,
    "native_tokens_prompt": 1,
    "native_tokens_completion": 1,
    "native_tokens_reasoning": 1,
    "num_media_prompt": 1,
    "num_media_completion": 1,
    "num_search_results": 1
  }
}