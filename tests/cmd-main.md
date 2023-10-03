# `gage` command

## Default command

Running `gage` without arguments shows help.

    >>> run("gage")  # +diff
    Usage: gage [options] command
    ⤶
      Gage ML command line interface.
    ⤶
    Options:
      --version   Print program version and exit.
      -C path     Change directory for command.
      --debug     Show debug messages.
      -h, --help  Show this message and exit.
    ⤶
    Commands:
      check            Show and validate settings.
      delete, rm       Delete runs.
      help             Show help for a topic.
      list, ls         List runs.
      open             Open a run in the file explorer.
      operations, ops  Show available operations.
      purge            Remove deleted runs.
      restore          Restore runs.
      run              Start or stage a run.
      select           Selects runs and their attributes.
      show             Show information about a run.
    <0>

## Help

Using `--help` shows help explicitly.

    >>> run("gage --help")  # +wildcard
    Usage: gage [options] command
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
