# `check` command

Help for `check`:

    >>> run("gage check --help")  # +diff
    Usage: gage check [OPTIONS]
    ⤶
      Show and validate settings.
    ⤶
      Use `check` to show Gage ML version, install location, and other
      configured settings.
    ⤶
    Options:
      --version SPEC  Test Gage version against SPEC.
      --json          Format check output as JSON.
      -v, --verbose   Show more information.
      --help          Show this message and exit.
    <0>

Default output:

    >>> run("gage check")  # -space +parse
    gage_version           0.1.0
    gage_install_location  {:path}
    python_version         {:ver} {:any}
    python_exe             {:path}
    platform               {:any}
    <0>

Verbose output:

    >>> run("gage check -v")  # -space +parse
    {}
    platform               {:any}
    command_directory      {:path}
    <0>

## Check version

The `--version` option is used to check the Gage version against a
version spec.

Matching spec:

    >>> from gage import __version__

    >>> run(f"gage check --version {__version__}")
    <0>

    >>> run(f"gage check --version =={__version__}")
    <0>

    >>> run(f"gage check --version '<={__version__}'")
    <0>

    >>> run(f"gage check --version '>={__version__}'")
    <0>

Non matching spec:

    >>> run(f"gage check --version '<{__version__}'")  # +parse
    gage: version mismatch: current version '{:ver}' does not match '<{:ver}'
    <1>

    >>> run(f"gage check --version '>{__version__}'")  # +parse
    gage: version mismatch: current version '{:ver}' does not match '>{:ver}'
    <1>

    >>> run("gage check --version 999")  # +parse
    gage: version mismatch: current version '{:ver}' does not match '999'
    <1>

    >>> run("gage check --version foobar")
    gage: invalid version spec 'foobar': missing comparison operator (==, <, >, etc.)
    See https://bit.ly/45AerAj for help with version specs.
    <1>

    >>> run("gage check --version ==foobar")  # -space
    gage: invalid version spec '==foobar': expected end or semicolon (after name and
    no valid version specifier)
    See https://bit.ly/45AerAj for help with version specs.
    <1>
