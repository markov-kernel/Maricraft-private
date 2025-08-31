# fastmcp.resources.types
# fastmcp.resources.types

> **Category:** fastmcp.resources.types
> **Source:** gofastmcp.com_python-sdk_fastmcp-resources-types.json

---

fastmcp.resources

types

fastmcp.resources.types

Concrete resource implementations.

## Classes

TextResource

A resource that reads from a string.**Methods:**

read

Copy

```
read(self) -> str

```

Read the text content.

BinaryResource

A resource that reads from bytes.**Methods:**

read

Copy

```
read(self) -> bytes

```

Read the binary content.

FileResource

A resource that reads from a file.Set is\_binary=True to read file as binary data instead of text.**Methods:**

validate_absolute_path

Copy

```
validate_absolute_path(cls, path: Path) -> Path

```

Ensure path is absolute.

set_binary_from_mime_type

Copy

```
set_binary_from_mime_type(cls, is_binary: bool, info: ValidationInfo) -> bool

```

Set is\_binary based on mime\_type if not explicitly set.

read

Copy

```
read(self) -> str | bytes

```

Read the file content.

HttpResource

A resource that reads from an HTTP endpoint.**Methods:**

read

Copy

```
read(self) -> str | bytes

```

Read the HTTP content.

DirectoryResource

A resource that lists files in a directory.**Methods:**

validate_absolute_path

Copy

```
validate_absolute_path(cls, path: Path) -> Path

```

Ensure path is absolute.

list_files

Copy

```
list_files(self) -> list[Path]

```

List files in the directory.

read

Copy

```
read(self) -> str

```

Read the directory listing.

[template](https://gofastmcp.com/python-sdk/fastmcp-resources-template) [\_\_init\_\_](https://gofastmcp.com/python-sdk/fastmcp-server-__init__)