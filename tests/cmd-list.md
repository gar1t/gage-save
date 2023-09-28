# List command

`list` shows runs.

Generate some sample runs.

    >>> use_example("hello")

    >>> run("gage run hello -l run-1 -y")
    <0>

    >>> run("gage run hello -l run-2 -y")
    <0>

    >>> run("gage run hello -l run-3 -y")
    <0>

    >>> run("gage run hello -l run-4 -y")
    <0>

List runs.

    >>> run("gage list")  # +parse
    | # | name  | operation   | started | status    | description |
    |---|-------|-------------|---------|-----------|-------------|
    | 1 | {:aa} | hello:hello | now     | completed | run-4       |
    | 2 | {:aa} | hello:hello | now     | completed | run-3       |
    | 3 | {:aa} | hello:hello | now     | completed | run-2       |
    | 4 | {:aa} | hello:hello | now     | completed | run-1       |
    <0>

## Incompatible params

    >>> run("gage list -n1 -a")
    all and limit cannot be used together.
    ⤶
    Try 'gage list -h' for help.
    <1>
