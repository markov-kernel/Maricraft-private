# Theming overview

In this guide, we provide an overview of theming and visual customization of Streamlit apps. Streamlit themes are defined using configuration options, which are most commonly defined in a `.streamlit/config.toml` file. For more information about setting configuration options, see [Working with configuration options](https://docs.streamlit.io/develop/concepts/configuration/options). For a complete list of configuration options and definitions, see the API reference for [config.toml](https://docs.streamlit.io/develop/api-reference/configuration/config.toml#theme).

The following options can be set in the `[theme]` table of `config.toml` and can't be set separately in the `[theme.sidebar]` table:

- **Base color scheme**: Set your custom theme to inherit from Streamlit's light or dark theme.
- **Base font**: Set the base font weight and size. (This can be configured separately for heading and code font.)
- **Chart color**: Set series colors for Plotly, Altair, and Vega-Lite charts.
- **Sidebar border**: Set the visibility of the sidebar border.

The following options can be configured separately for the main body of your app and the sidebar:

- **Font family**: Set the font family for body text, headings, and code.
- **Font style**: Set the weight and size of heading and code font, and set visibility of link underlines.
- **Text color**: Set the color of body text and links.
- **Primary color**: Set the color of interactive elements and highlights.
- **Background color**: Set the color of app, widget, code block, and dataframe header backgrounds.
- **Border radius**: Set the roundness of elements and widgets.
- **Border color**: Set the color and visibility of element, widget, sidebar, and dataframe borders.

## Example themes

The following light theme is inspired by [Anthropic](https://docs.anthropic.com/en/home).

Home

keyboard\_double\_arrow\_left

[homeHome](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/)

[widgetsWidgets](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/widgets)

[articleText](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/text)

[tableData](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/data)

[insert\_chartCharts](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/charts)

[imageMedia](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/media)

[dashboardLayouts](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/layouts)

[chatChat](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/chat)

[errorStatus](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/status)

[home\\
\\
Home](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/?embed=true)

Welcome to the home page!

Select a page from above. This sidebar thumbnail shows a subset of elements from each page so you can see the sidebar theme.

This app uses [Space Grotesk](https://fonts.google.com/specimen/Space+Grotesk) and [Space Mono](https://fonts.google.com/specimen/Space+Mono) fonts.

# Streamlit element explorer

This app displays most of Streamlit's built-in elements so you can conveniently explore how they look with different theming configurations applied.

[widgets\\
\\
Widgets](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/widgets)

Text input

Pills

A

B

C

Segmented control

A

B

C

Primary

Secondary

Tertiary

[table\\
\\
Data](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/data)

[image\\
\\
Media](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/media)

[chat\\
\\
Chat](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/chat)

Hello, world!

Hello, user!

[article\\
\\
Text](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/text)

### Subheader

Markdown: **bold** _italic_ ~~strikethrough~~ [link](https://streamlit.io/) `code` ∫abf(x)\\int\_a^b f(x)∫ab​f(x) 🐶 🐱 home![Streamlit logo](data:image/svg+xml,%3csvg%20width='301'%20height='165'%20viewBox='0%200%20301%20165'%20fill='none'%20xmlns='http://www.w3.org/2000/svg'%3e%3cpath%20d='M150.731%20101.547L98.1387%2073.7471L6.84674%2025.4969C6.7634%2025.4136%206.59674%2025.4136%206.51341%2025.4136C3.18007%2023.8303%20-0.236608%2027.1636%201.0134%2030.497L47.5302%20149.139L47.5385%20149.164C47.5885%20149.281%2047.6302%20149.397%2047.6802%20149.514C49.5885%20153.939%2053.7552%20156.672%2058.2886%20157.747C58.6719%20157.831%2058.9461%20157.906%2059.4064%20157.998C59.8645%20158.1%2060.5052%20158.239%2061.0552%20158.281C61.1469%20158.289%2061.2302%20158.289%2061.3219%20158.297H61.3886C61.4552%20158.306%2061.5219%20158.306%2061.5886%20158.314H61.6802C61.7386%20158.322%2061.8052%20158.322%2061.8636%20158.322H61.9719C62.0386%20158.331%2062.1052%20158.331%2062.1719%20158.331V158.331C121.084%20164.754%20180.519%20164.754%20239.431%20158.331V158.331C240.139%20158.331%20240.831%20158.297%20241.497%20158.231C241.714%20158.206%20241.922%20158.181%20242.131%20158.156C242.156%20158.147%20242.189%20158.147%20242.214%20158.139C242.356%20158.122%20242.497%20158.097%20242.639%20158.072C242.847%20158.047%20243.056%20158.006%20243.264%20157.964C243.681%20157.872%20243.87%20157.806%20244.436%20157.611C245.001%20157.417%20245.94%20157.077%20246.527%20156.794C247.115%20156.511%20247.522%20156.239%20248.014%20155.931C248.622%20155.547%20249.201%20155.155%20249.788%20154.715C250.041%20154.521%20250.214%20154.397%20250.397%20154.222L250.297%20154.164L150.731%20101.547Z'%20fill='%23FF4B4B'/%3e%3cpath%20d='M294.766%2025.4981H294.683L203.357%2073.7483L254.124%20149.357L300.524%2030.4981V30.3315C301.691%2026.8314%20298.108%2023.6648%20294.766%2025.4981'%20fill='%237D353B'/%3e%3cpath%20d='M155.598%202.55572C153.264%20-0.852624%20148.181%20-0.852624%20145.931%202.55572L98.1389%2073.7477L150.731%20101.548L250.398%20154.222C251.024%20153.609%20251.526%20153.012%20252.056%20152.381C252.806%20151.456%20253.506%20150.465%20254.123%20149.356L203.356%2073.7477L155.598%202.55572Z'%20fill='%23BD4043'/%3e%3c/svg%3e) ← → ↔, ≥ ≤ ≈

- Red text
- Violet text

rainbow

[insert\_chart\\
\\
Charts](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/charts)

[Save as SVG](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/?embed=true#) [Save as PNG](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/?embed=true#) [View Source](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/?embed=true#) [View Compiled Vega](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/?embed=true#) [Open in Vega Editor](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/?embed=true#)

[dashboard\\
\\
Layouts](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/layouts)

Tab A

Tab B

Tab C

Tab A content

Expander

Expander content

info

Popover

Popover content

[error\\
\\
Status](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/~/+/status)

Error

Warning

Info

Success

Toast!

Balloons!

[Built with Streamlit 🎈](https://streamlit.io/)

[Fullscreen _open\_in\_new_](https://doc-theming-overview-anthropic-light-inspired.streamlit.app/?utm_medium=oembed)

The following dark theme is inspired by [Spotify](https://open.spotify.com/).

Home

keyboard\_double\_arrow\_left

[homeHome](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/)

[widgetsWidgets](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/widgets)

[articleText](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/text)

[tableData](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/data)

[insert\_chartCharts](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/charts)

[imageMedia](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/media)

[dashboardLayouts](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/layouts)

[chatChat](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/chat)

[errorStatus](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/status)

[home\\
\\
Home](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/?embed=true)

Welcome to the home page!

Select a page from above. This sidebar thumbnail shows a subset of elements from each page so you can see the sidebar theme.

This app uses [Poppins](https://fonts.google.com/specimen/Poppins) font.

# Streamlit element explorer

This app displays most of Streamlit's built-in elements so you can conveniently explore how they look with different theming configurations applied.

[widgets\\
\\
Widgets](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/widgets)

Text input

Pills

A

B

C

Segmented control

A

B

C

Primary

Secondary

Tertiary

[table\\
\\
Data](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/data)

[image\\
\\
Media](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/media)

[chat\\
\\
Chat](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/chat)

Hello, world!

Hello, user!

[article\\
\\
Text](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/text)

### Subheader

Markdown: **bold** _italic_ ~~strikethrough~~ [link](https://streamlit.io/) `code` ∫abf(x)\\int\_a^b f(x)∫ab​f(x) 🐶 🐱 home![Streamlit logo](data:image/svg+xml,%3csvg%20width='301'%20height='165'%20viewBox='0%200%20301%20165'%20fill='none'%20xmlns='http://www.w3.org/2000/svg'%3e%3cpath%20d='M150.731%20101.547L98.1387%2073.7471L6.84674%2025.4969C6.7634%2025.4136%206.59674%2025.4136%206.51341%2025.4136C3.18007%2023.8303%20-0.236608%2027.1636%201.0134%2030.497L47.5302%20149.139L47.5385%20149.164C47.5885%20149.281%2047.6302%20149.397%2047.6802%20149.514C49.5885%20153.939%2053.7552%20156.672%2058.2886%20157.747C58.6719%20157.831%2058.9461%20157.906%2059.4064%20157.998C59.8645%20158.1%2060.5052%20158.239%2061.0552%20158.281C61.1469%20158.289%2061.2302%20158.289%2061.3219%20158.297H61.3886C61.4552%20158.306%2061.5219%20158.306%2061.5886%20158.314H61.6802C61.7386%20158.322%2061.8052%20158.322%2061.8636%20158.322H61.9719C62.0386%20158.331%2062.1052%20158.331%2062.1719%20158.331V158.331C121.084%20164.754%20180.519%20164.754%20239.431%20158.331V158.331C240.139%20158.331%20240.831%20158.297%20241.497%20158.231C241.714%20158.206%20241.922%20158.181%20242.131%20158.156C242.156%20158.147%20242.189%20158.147%20242.214%20158.139C242.356%20158.122%20242.497%20158.097%20242.639%20158.072C242.847%20158.047%20243.056%20158.006%20243.264%20157.964C243.681%20157.872%20243.87%20157.806%20244.436%20157.611C245.001%20157.417%20245.94%20157.077%20246.527%20156.794C247.115%20156.511%20247.522%20156.239%20248.014%20155.931C248.622%20155.547%20249.201%20155.155%20249.788%20154.715C250.041%20154.521%20250.214%20154.397%20250.397%20154.222L250.297%20154.164L150.731%20101.547Z'%20fill='%23FF4B4B'/%3e%3cpath%20d='M294.766%2025.4981H294.683L203.357%2073.7483L254.124%20149.357L300.524%2030.4981V30.3315C301.691%2026.8314%20298.108%2023.6648%20294.766%2025.4981'%20fill='%237D353B'/%3e%3cpath%20d='M155.598%202.55572C153.264%20-0.852624%20148.181%20-0.852624%20145.931%202.55572L98.1389%2073.7477L150.731%20101.548L250.398%20154.222C251.024%20153.609%20251.526%20153.012%20252.056%20152.381C252.806%20151.456%20253.506%20150.465%20254.123%20149.356L203.356%2073.7477L155.598%202.55572Z'%20fill='%23BD4043'/%3e%3c/svg%3e) ← → ↔, ≥ ≤ ≈

- Red text
- Violet text

rainbow

[insert\_chart\\
\\
Charts](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/charts)

[Save as SVG](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/?embed=true#) [Save as PNG](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/?embed=true#) [View Source](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/?embed=true#) [View Compiled Vega](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/?embed=true#) [Open in Vega Editor](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/?embed=true#)

[dashboard\\
\\
Layouts](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/layouts)

Tab A

Tab B

Tab C

Tab A content

Expander

Expander content

info

Popover

Popover content

[error\\
\\
Status](https://doc-theming-overview-spotify-inspired.streamlit.app/~/+/status)

Error

Warning

Info

Success

Toast!

Balloons!

[Built with Streamlit 🎈](https://streamlit.io/)

[Fullscreen _open\_in\_new_](https://doc-theming-overview-spotify-inspired.streamlit.app/?utm_medium=oembed)

## Working with theme configuration during development

Most theme configuration options can be updated while an app is running. This makes it easy to iterate on your custom theme. If you change your app's primary color, save your `config.toml` file, and rerun your app, you will immediately see the new color. However, some configuration options (like `[[theme.fontFace]]`) require you to restart the Streamlit server to reflect the updates. If in doubt, when updating your app's configuration, stop the Streamlit server in your terminal and restart your app with the `streamlit run` command.