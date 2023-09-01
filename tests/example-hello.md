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
        "description": "A simple 'hello world' style operation",
        "exec": ["python", "-c", "print('Hello Gage!')"]
      }
    }

List operations.

    >>> run("gage ops")
    hello  A simple 'hello world' style operation
    ↪ 0

    >>> run("gage ops")
    hello  A simple 'hello world' style operation
    ↪ 0

    >>> run("gage ops")
    hello  A simple 'hello world' style operation
    ↪ 0

    >>> run("gage ops")
    hello  A simple 'hello world' style operation
    ↪ 0
