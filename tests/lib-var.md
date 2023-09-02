# gage `var` support

The `var` module provides system wide data related services. It's primary
feature is to read Runs from a runs location.

    >>> from gage._internal import var

    >>> var_home = make_temp_dir()

    >>> set_var_home(var_home)

    >>> var.runs()
    []
