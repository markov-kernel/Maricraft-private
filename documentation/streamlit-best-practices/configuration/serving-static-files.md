# Static file serving

Streamlit apps can host and serve small, static media files to support media embedding use cases that
won't work with the normal [media elements](https://docs.streamlit.io/develop/api-reference/media).

To enable this feature, set `enableStaticServing = true` under `[server]` in your config file,
or environment variable `STREAMLIT_SERVER_ENABLE_STATIC_SERVING=true`.

Media stored in the folder `./static/` relative to the running app file is served at path
`app/static/[filename]`, such as `http://localhost:8501/app/static/cat.png`.

## Details on usage

- Files with the following extensions will be served normally:
  - Common image types: `.jpg`, `.jpeg`, `.png`, `.gif`
  - Common font types: `.otf`, `.ttf`, `.woff`, `.woff2`
  - Other types: `.pdf`, `.xml`, `.json`
    Any other file will be sent with header `Content-Type:text/plain` which will cause browsers to render in plain text.
    This is included for security - other file types that need to render should be hosted outside the app.
- Streamlit also sets `X-Content-Type-Options:nosniff` for all files rendered from the static directory.
- For apps running on Streamlit Community Cloud:
  - Files available in the Github repo will always be served. Any files generated while the app is running,
    such as based on user interaction (file upload, etc), are not guaranteed to persist across user sessions.
  - Apps which store and serve many files, or large files, may run into resource limits and be shut down.

## Example usage

- Put an image `cat.png` in the folder `./static/`
- Add `enableStaticServing = true` under `[server]` in your `.streamlit/config.toml`
- Any media in the `./static/` folder is served at the relative URL like `app/static/cat.png`

`# .streamlit/config.toml
[server]
enableStaticServing = true
`

`# app.py
import streamlit as st
with st.echo():
    st.title("CAT")
    st.markdown("[![Click me](app/static/cat.png)](https://streamlit.io)")
`

Additional resources:

- [https://docs.streamlit.io/develop/concepts/configuration](https://docs.streamlit.io/develop/concepts/configuration)
- [https://static-file-serving.streamlit.app/](https://static-file-serving.streamlit.app/)

streamlit\_app · Streamlit

🐱

# Static file serving

[Code for this demo](https://github.com/streamlit/static-file-serving-demo/blob/main/streamlit_app.py)

Streamlit 1.18 allows you to serve small, static media files via URL.

## Instructions

- Create a folder `static` in your app's root directory.
- Place your files in the `static` folder.
- Add the following to your `config.toml` file:

```toml

[server]
enableStaticServing = true
```

You can then access the files on `<your-app-url>/app/static/<filename>`. Read more in our
[docs](https://docs.streamlit.io/library/advanced-features/static-file-serving).

## Examples

You can use this feature with `st.markdown` to put a link on an image:

```python

st.markdown("[![Click me](./app/static/cat.jpg)](https://streamlit.io)")
```

[![Click me](https://static-file-serving.streamlit.app/~/+/app/static/cat.jpg)](https://streamlit.io/)

Or you can use images in HTML or SVG:

```python

st.markdown(
    '<img src="./app/static/dog.jpg" height="333" style="border: 5px solid orange">',
    unsafe_allow_html=True,
)
```

![](https://static-file-serving.streamlit.app/~/+/app/static/dog.jpg)

[Built with Streamlit 🎈](https://streamlit.io/)

[Fullscreen _open\_in\_new_](https://static-file-serving.streamlit.app/?utm_medium=oembed)