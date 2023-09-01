# gage `var` support

The `var` module provides system wide data related services. It's primary
feature is to read Runs from a runs location.

    >>> from gage._internal import var

    >>> var_home = mkdtemp()

    >>> set_var_home(var_home)

    >>> var.runs()
    []

Generate one run.

    >>> import gage

    >>> run = gage.run(sample("hello"))

    >>> run.run_dir
    'yyy.run'

    >>> find(run.run_dir)
    <empty>
