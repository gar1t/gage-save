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
        "description": "Hello world style operation",
        "exec": ["python", "-c", "print('Hello Gage!')"]
      }
    }

List operations.

    >>> run("gage ops")
    hello  Hello world style operation
    <0>

Run hello.

FIXME - expects something to be said, namely "Hello"

    >>> run("gage run hello -y")
    <0>
