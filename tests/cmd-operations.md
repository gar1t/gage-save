---
test-options: +wildcard
---

# `operations` command

    >>> run("gage operations --help")
    Usage: gage operations [OPTIONS] [FILTER]...
    ⤶
      Show available operations.
    ⤶
      Use one or more FILTER arguments to show only operations with names or
      models that match the specified values.
    ⤶
    Options:
      --help  Show this message and exit.
    <exit 0>

The alias `ops` may also be used.

    >>> run("gage ops --help")
    Usage: gage ops [OPTIONS] [FILTER]...
    ⤶
      Show available operations.
    ⤶
    ...
    <exit 0>
