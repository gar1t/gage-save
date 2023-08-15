# `check` command

    >>> run("vml check")
    vistaml_version:           0.1.0
    vistaml_install_location:  ...
    python_version:            ...
    python_exe:                ...
    platform:                  ...

Test version.

    >>> run("vml check -V 0.1.0")
    <exit 0>

    >>> run("vml check -V 999")
    vml: version mismatch: current version '...' does not match '999'
    <exit 1>
