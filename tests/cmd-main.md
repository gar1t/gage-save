# `gage` command

## Default command

Running `gage` without arguments shows help.

    >>> run("gage")  # +diff
    Usage: gage [OPTIONS] COMMAND [ARGS]...
    ⤶
      Gage ML command line interface.
    ⤶
    Options:
      --version  Print program version and exit.
      -C PATH    Change to PATH directory for command.
      --help     Show this message and exit.
    ⤶
    Commands:
      check            Show and validate settings.
      help             Show help for a topic.
      operations, ops  Show available operations.
      run              Start or stage an operation.
    <0>

## Help

Using `--help` shows help explicitly.

    >>> run("gage --help")  # +wildcard
    Usage: gage [OPTIONS] COMMAND [ARGS]...
    ⤶
      Gage ML command line interface.
    ⤶
    ...

## Version

    >>> run("gage --version")
    gage 0.1.0
    <0>

## Changing cwd

The `-C` runs the command in the specified directory.

    >>> tmp = make_temp_dir()

    >>> run(f"gage -C {tmp} check -v")  # +parse -space
    {}
    | command_directory   | {x:path} |
    | project_directory   | <none>   |
    | gagefile            | <none>   |
    <0>

    >>> assert x == tmp
