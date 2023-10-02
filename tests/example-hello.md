# Hello example

The [`hello`](../examples/hello) example demonstrates the simplest
possible Gage project.

    >>> use_example("hello")

- Simple Gage file with one operation
- No language-specific features
- No parameter bindings

    >>> cat("gage.toml")
    [hello]
    ⤶
    description = "Say hello to my friend"
    ⤶
    exec = "python hello.py"
    config = "hello.py"

List operations.

    >>> run("gage ops")
    | operation | description            |
    |-----------|------------------------|
    | hello     | Say hello to my friend |
    <0>

Run hello.

    >>> run("gage run hello -y")
    Hello Gage
    <0>

    >>> run("gage show")  # +parse -space
    {:run_id}
    | hello:hello                                    completed |
    ⤶
                             Attributes
    | id         {:run_id}                                     |
    | name       {:run_name}                                   |
    | started    {:datetime}                                   |
    | stopped    {:datetime}                                   |
    | location   {:path}                                       |
    | exit_code  0                                             |
    ⤶
                               Files
    | name            |type               |               size |
    | ----------------|-------------------|------------------- |
    | gage.toml       |source code        |               94 B |
    | hello.py        |source code        |               38 B |
    | ----------------|-------------------|------------------- |
    |                 |                   |       total: 132 B |
    ⤶
                               Output
    | Hello Gage                                               |
    <0>
