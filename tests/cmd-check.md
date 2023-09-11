# `check` command

    >>> run("gage check")  # -space +parse
    gage_version           0.1.0
    gage_install_location  {:path}
    python_version         {:ver} {:any}
    python_exe             {:path}
    platform               {:any}
    <0>

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
    gage: invalid version spec '==foobar': Expected end or semicolon (after name and
    no valid version specifier)
        fakepkg==foobar
               ^
    See https://bit.ly/45AerAj for help with version specs.
    <1>
