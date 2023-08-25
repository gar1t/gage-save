# `runs list` command

## Incompatible options

    >>> run("vml runs --json --verbose")
    vml: --json and --verbose cannot both be specified
    Try 'vml runs list --help' for more information.
    <exit 1>

    >>> run("vml runs --archive X --deleted")
    vml: --archive and --deleted cannot both be specified
    Try 'vml runs list --help' for more information.
    <exit 1>

    >>> run("vml runs list --all --limit 5")
    vml: --all and --limit cannot both be specified
    Try 'vml runs list --help' for more information.
    <exit 1>
