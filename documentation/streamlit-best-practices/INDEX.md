# Streamlit Documentation - Best Practices Guide

This is a curated collection of Streamlit documentation organized for easy reference and best practices.

## Table of Contents


### Architecture & Execution Model

- [Add statefulness to apps](architecture/session-state.md)
- [Caching overview](architecture/caching.md)
- [Run your Streamlit app](architecture/run-your-app.md)
- [The app chrome](architecture/app-chrome.md)
- [Understanding Streamlit's client-server architecture](architecture/architecture.md)
- [Understanding widget behavior](architecture/widget-behavior.md)
- [Using forms](architecture/forms.md)
- [Working with fragments](architecture/fragments.md)
- **[Working with Streamlit's execution model](architecture/README.md)**

### App Testing

- [App testing cheat sheet](app-testing/cheat-sheet.md)
- [App testing example](app-testing/examples.md)
- [Automate your tests with CI](app-testing/automate-tests.md)
- [Beyond the basics of app testing](app-testing/beyond-the-basics.md)
- [Get started with app testing](app-testing/get-started.md)
- **[Streamlit's native app testing framework](app-testing/README.md)**

### Multipage Applications

- [Creating multipage apps using the `pages/` directory](multipage-apps/pages-directory.md)
- [Define multipage apps with `st.Page` and `st.navigation`](multipage-apps/page-and-navigation.md)
- [Overview of multipage apps](multipage-apps/overview.md)
- [Working with widgets in multipage apps](multipage-apps/widgets.md)
- **[Multipage apps](multipage-apps/README.md)**

### Design & UI Patterns

- [Animate and update elements](design/animate.md)
- [Button behavior and examples](design/buttons.md)
- [Dataframes](design/dataframes.md)
- [Multithreading in Streamlit](design/multithreading.md)
- [Using custom Python classes in your Streamlit app](design/custom-classes.md)
- [Working with timezones](design/timezone-handling.md)
- **[App design concepts and considerations](design/README.md)**

### Configuration & Theming

- [Customize colors and borders in your Streamlit app](configuration/theming-customize-colors-and-borders.md)
- [Customize fonts in your Streamlit app](configuration/theming-customize-fonts.md)
- [HTTPS support](configuration/https-support.md)
- [Static file serving](configuration/serving-static-files.md)
- [Theming overview](configuration/theming.md)
- [Working with configuration options](configuration/options.md)
- **[Configure and customize your app](configuration/README.md)**

### Connections & Secrets

- [Connecting to data](connections/connecting-to-data.md)
- [Secrets management](connections/secrets-management.md)
- [Security reminders](connections/security-reminders.md)
- [User authentication and information](connections/authentication.md)
- **[Working with connections, secrets, and user authentication](connections/README.md)**

### Custom Components

- [Create a Component](custom-components/create.md)
- [Intro to custom components](custom-components/intro.md)
- [Limitations of custom components](custom-components/limitations.md)
- [Publish a Component](custom-components/publish.md)
- **[Custom Components](custom-components/README.md)**


## Quick Reference

### Core Concepts
- **Execution Model**: Streamlit runs your script from top to bottom on every interaction
- **Caching**: Use `@st.cache_data` for data and `@st.cache_resource` for resources
- **Session State**: Manage stateful behavior across reruns
- **Forms**: Group input widgets to prevent unnecessary reruns

### Best Practices
1. **Performance**: Always cache expensive operations
2. **State Management**: Use Session State for user-specific data
3. **Layout**: Organize complex apps with columns, tabs, and expanders
4. **Testing**: Write automated tests for your Streamlit apps
5. **Configuration**: Customize your app with config files and theming

### Common Patterns
- Data loading and transformation
- User authentication and secrets management
- Multi-page navigation
- Custom components integration
- Real-time data updates

---
*Generated from official Streamlit documentation - organized for clarity and best practices*
