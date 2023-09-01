# `runs list` command

## Incompatible options

    >>> run("gage runs --json --verbose")
    gage: --json and --verbose cannot both be specified
    Try 'gage runs list --help' for more information.
    ↪ 1

    >>> run("gage runs --archive X --deleted")
    gage: --archive and --deleted cannot both be specified
    Try 'gage runs list --help' for more information.
    ↪ 1

    >>> run("gage runs list --all --limit 5")
    gage: --all and --limit cannot both be specified
    Try 'gage runs list --help' for more information.
    ↪ 1
