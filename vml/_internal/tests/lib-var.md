# Vista `var` support

The `var` module provides system wide data related services. It's primary
feature is to read Runs from a runs location.

    >>> from vml._internal import var

    >>> var_home = mkdtemp()

    >>> set_var_home(var_home)

    >>> var.runs()
    []

    >>> sleep(5)
