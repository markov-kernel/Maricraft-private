# fastmcp.server.elicitation
# fastmcp.server.elicitation

> **Category:** fastmcp.server.elicitation
> **Source:** gofastmcp.com_python-sdk_fastmcp-server-elicitation.json

---

elicitation

fastmcp.server.elicitation

## Functions

get_elicitation_schema

Copy

```
get_elicitation_schema(response_type: type[T]) -> dict[str, Any]

```

Get the schema for an elicitation response.**Args:**

- `response_type`: The type of the response

validate_elicitation_json_schema

Copy

```
validate_elicitation_json_schema(schema: dict[str, Any]) -> None

```

Validate that a JSON schema follows MCP elicitation requirements.This ensures the schema is compatible with MCP elicitation requirements:

- Must be an object schema
- Must only contain primitive field types (string, number, integer, boolean)
- Must be flat (no nested objects or arrays of objects)
- Allows const fields (for Literal types) and enum fields (for Enum types)
- Only primitive types and their nullable variants are allowed

**Args:**

- `schema`: The JSON schema to validate

**Raises:**

- `TypeError`: If the schema doesn’t meet MCP elicitation requirements

## Classes

AcceptedElicitation

Result when user accepts the elicitation.

ScalarElicitationType

[dependencies](https://gofastmcp.com/python-sdk/fastmcp-server-dependencies) [http](https://gofastmcp.com/python-sdk/fastmcp-server-http)