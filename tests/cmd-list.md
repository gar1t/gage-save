# `list` command

`list` shows runs.

    >>> run("gage list -h")
    Usage: gage list [options] [run]...
    ⤶
      List runs.
    ⤶
      By default the latest 20 runs are shown. To show more,
      use '-n / --limit' with higher number. Use '-a / --all'
      to show all runs.
    ⤶
      Use '-w / --where' to filter runs. Try 'gage help
      filters' for help with filter expressions.
    ⤶
      Runs may be selected from the list using run IDs, names,
      indexes or slice notation. Try 'gage help select-runs'
      for help with select options.
    ⤶
    Arguments:
      [run]...  Runs to list. run may be a run ID, name, list
                index or slice.
    ⤶
    Options:
      -n, --limit max  Limit list to max runs.
      -a, --all        Show all runs. Cannot use with --limit.
      --where expr     Show runs matching filter expression.
      -h, --help       Show this message and exit.
    <0>

Generate some sample runs.

    >>> use_example("hello")

    >>> run("gage run hello -l run-1 -q -y")
    <0>

    >>> run("gage run hello -l run-2 -q -y")
    <0>

    >>> run("gage run hello -l run-3 -q -y")
    <0>

    >>> run("gage run hello -l run-4 -q -y")
    <0>

List runs.

    >>> run("gage list")  # +parse
    | #  | name    | operation       | started   | status      |
    |----|---------|-----------------|-----------|-------------|
    | 1  | {:rn}   | hello:hello     | now       | completed   |
    | 2  | {:rn}   | hello:hello     | now       | completed   |
    | 3  | {:rn}   | hello:hello     | now       | completed   |
    | 4  | {:rn}   | hello:hello     | now       | completed   |
    <0>

## Incompatible params

    >>> run("gage list -n1 -a")
    all and limit cannot be used together.
    ⤶
    Try 'gage list -h' for help.
    <1>
