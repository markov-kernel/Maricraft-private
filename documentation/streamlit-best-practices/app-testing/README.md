# Streamlit's native app testing framework

Streamlit app testing enables developers to build and run automated tests. Bring your favorite test automation software and enjoy simple syntax to simulate user input and inspect rendered output.

The provided class, AppTest, simulates a running app and provides methods to set up, manipulate, and inspect the app contents via API instead of a browser UI. AppTest provides similar functionality to browser automation tools like Selenium or Playwright, but with less overhead to write and execute tests. Use our testing framework with a tool like [pytest](https://docs.pytest.org/) to execute or automate your tests. A typical pattern is to build a suite of tests for an app to ensure consistent functionality as the app evolves. The tests run locally and/or in a CI environment like GitHub Actions.

[_science_](https://docs.streamlit.io/develop/concepts/app-testing/get-started)

[Get started](https://docs.streamlit.io/develop/concepts/app-testing/get-started) introduces you to the app testing framework and how to execute tests using `pytest`. Learn how to initialize and run simulated apps, including how to retrieve, manipulate, and inspect app elements.

[_password_](https://docs.streamlit.io/develop/concepts/app-testing/beyond-the-basics)

[Beyond the basics](https://docs.streamlit.io/develop/concepts/app-testing/beyond-the-basics) explains how to work with secrets and Session State within app tests, including how to test multipage apps.

[_play\_circle_](https://docs.streamlit.io/develop/concepts/app-testing/automate-tests)

[Automate your tests](https://docs.streamlit.io/develop/concepts/app-testing/automate-tests) with Continuous Integration (CI) to validate app changes over time.

[_quiz_](https://docs.streamlit.io/develop/concepts/app-testing/examples)

[Example](https://docs.streamlit.io/develop/concepts/app-testing/examples) puts together the concepts explained above. Check out an app with multiple tests in place.

[_saved\_search_](https://docs.streamlit.io/develop/concepts/app-testing/cheat-sheet)

[Cheat sheet](https://docs.streamlit.io/develop/concepts/app-testing/cheat-sheet) is a compact reference summarizing the available syntax.