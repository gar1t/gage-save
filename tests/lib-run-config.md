# Run Config

Run config determines the configuration available to user code for a run.

Run config is applied to source code files by modifying the source code
files with modified values.

Consider a Python script `hello.py`.

``` python
name = "Joe"

print(f"Hello {name}")
```

The configuration when running this script is defined by the variable
`msg` in the Python script.

A different name `"Mike"` can be applied as updated configuration,
resulting in a modified script.

``` python
name = "Mike"

print(f"Hello {name}")
```

Such a configuration change can be applied for a run using a flag.

    $ run hello.py name="Mike"

To apply the new name, Gage needs to know that `hello.py` contains run
configuration.

TODO: This is the default when running a script.

Configuration for an operation is specified using the `config` op def
attribute.

``` toml
[hello]

exec = "python hello.py"

[config]

include = "hello.py"
```

`config` specified include and exclude patterns, which resolve to zero
or more source code files. Gage parses these source code files to create
a configuration map. That map can be modified through flags for a run
and applied to modify source code files accordingly.

    >>> from gage._internal.run_config import *

## SCRATCH

    >>> py = """
    ... name = "Joe"
    ...
    ... print(f"Hello {name}")
    ... """

    >> parse_py(py)
