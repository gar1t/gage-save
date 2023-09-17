# Run Config

*Run configuration* is a set of values available to a run script.
Configuration is provided by way of source code files.

Gage modifies source code files for a run to provide alternative
configuration.

Consider a script `hello.py`.

``` python
# hello.py

name = "Joe"
print(f"Hello {name}")
```

The `name` variable represents the script configuration. The value
`Joe`is used by default and is used if otherwise not specified by a flag
for the `run` command.

If the user changed `name` using a flag, Gage rewrites the script to
contain the new name value. This is called the *application of run
configuration*.

Let's say the user runs the command `gage run hello.py name="Mike"`.
When Gage stages the run, it copies the unmodified source code file
`train.py` according to its default source code select rules. Then it
applies run configuration by modifying the copied version of `hello.py`
to be:

``` python
# hello.py

name = "Mike"
print(f"Hello {name}")
```

When the script runs, it prints the message "Hello Mike".

This scheme is applied to any supported configuration file type. In
addition to Python source code files, Gage supports JSON, YAML, and TOML
formats. New formats are added as Gage expands (e.g. R, Julia, etc.)

Note that Gage is language independent in terms of what is run. The
application of configuration to source code files, however, is dependent
on support for specific file formats.

The module `run_config` provides support for the following:

- Abstract facility for loading, modifying, and saving supported file
  formats
- XXX

File format specific config support is provide by `run_config_xxx`
modules.

### Helper functions

    >>> def print_config(config):
    ...     if not config:
    ...         print("<none>")
    ...     else:
    ...         for key, val in sorted(config.items()):
    ...             print(f"{key}: {val}")

## Python config

Python config support is provided by `run_config_py`.

    >>> from gage._internal.run_config_py import *

A Python config file is a Python module that defines configuration
variables as top-level name assignments.

    >>> config = PythonConfig("""
    ... name = "Joe"
    ... print(f"Hello Joe")
    ... """)

    >>> print_config(config)
    name: Joe

TODO: demo set + render

### Keys

Keys correspond to top-level assignments of config values. Keys are comprised of the top-level variable and nested keys separated by dots.

Create a function to list keys for module source.

Variables must be assigned config values to be considered keys. A config
value is a string, number, or boolean. Config values may be contained in
lists and dictionaries.

    >>> config = PythonConfig("""
    ... i = 1
    ... f = 1.0
    ... b = True
    ... s = "Hello"
    ... n = None
    ... l = [1, 1.0, "Hello", False]
    ... d = {
    ...     "i": 1,
    ...     "f": 1.0,
    ...     "s": "Hi",
    ...     "b": False
    ... }
    ... """)

    >>> print_config(config)
    b: True
    d.b: False
    d.f: 1.0
    d.i: 1
    d.s: Hi
    f: 1.0
    i: 1
    l.0: 1
    l.1: 1.0
    l.2: Hello
    l.3: False
    n: None
    s: Hello

Assignments inside functions and class defs are not treated as keys.

    >>> config = PythonConfig("""
    ... def foo():
    ...     x = 1
    ...
    ... class Foo:
    ...     y = 2
    ...
    ...     def __init__(self):
    ...         self.z = 3
    ... """)

    >>> print_config(config)
    <none>

Assignments to tuples are not treated as config value assignments.

    >>> config = PythonConfig("""
    ... x, y = 1, 2
    ... """)

    >>> print_config(config)
    <none>
