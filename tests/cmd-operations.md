# `operations` command

    >>> run("gage operations --help")  # +wildcard
    Usage: gage operations [OPTIONS]
    ⤶
      Show available operations.
    ⤶
    ...
    Options:
      -h, --help  Show this message and exit.
    <0>

The alias `ops` may also be used.

    >>> run("gage ops --help")  # +wildcard
    Usage: gage ops [OPTIONS]
    ⤶
      Show available operations.
    ⤶
    ...
    <0>

Show operations for sample projects.

    >>> use_example("hello")

    >>> run("gage ops")
    | operation | description            |
    |-----------|------------------------|
    | hello     | Say hello to my friend |
    <0>
