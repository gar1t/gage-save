# Hello example

The [`hello`](../examples/hello) example demonstrates the simplest
possible Gage project.

    >>> use_example("hello")

- Simple Gage file with one operation
- No language-specific features
- No parameter bindings

    >>> cat("gage.json")
    {
      "hello": {
        "description": "Say hello to my friend",
        "exec": ["python", "-c", "print('Hello Gage!')"]
      }
    }

List operations.

    >>> run("gage ops")
    | operation | description            |
    |-----------|------------------------|
    | hello     | Say hello to my friend |
    <0>

Run hello.

FIXME - expects something to be said, namely "Hello"

    >> run("gage run hello -y")
    <0>
