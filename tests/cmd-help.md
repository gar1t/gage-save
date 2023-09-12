# `help` command

    >>> run("gage help")
    Usage: gage help [OPTIONS] TOPIC
    ⤶
      Show help for a topic.
    ⤶
    Commands:
      filters     Filtering results.
      gagefile    Defining and using gage files.
      operations  Defining and running operations.
    <0>

Note that topics are listed under the heading **Commands**, which is
misleading. This is due to our use of Typer/Click to implement help
topics as sub-commands. The Typer interface uses Rich formatting and
correctly uses **Topics** as the header. We see the style-free version
above.

When we unset `TERM`, the correct header is used.

    >>> run("gage help", env={"TERM": ""})  # +wildcard -space
    Usage: gage help [OPTIONS] TOPIC
    ⤶
      Show help for a topic.
    ⤶
    ... Topics ...
    <0>
