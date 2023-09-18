# Run config support

`run_config` provides support for run configuration implementation.

    >>> from gage._internal.run_config import *

## RunConfig base class

The class `RunConfigBase` is an abstract class that provides dict
support for format-specific run config.

    >>> config = RunConfigBase()

Concrete classes should implement config init in their constructors and
implement the `apply()` method.

    >>> config.apply()
    Traceback (most recent call last):
    NotImplementedError

Otherwise, the class provides a dict-like interface for setting and
reading configuration.

    >>> config["x"] = 123
    >>> config["y"] = 456
    >>> config.update({"z": 789})

    >>> config  # +pprint
    {'x': 123, 'y': 456, 'z': 789}

When initialized, `_initialized` should set to to `True` to prevent new
config keys form being added.

    >>> config._initialized = True

    >>> config["x2"] = 321
    Traceback (most recent call last):
    ValueError: key does not exist: 'x2'

Existing keys can be updated.

    >>> config["x"] = 321

    >>> config  # +pprint
    {'x': 321, 'y': 456, 'z': 789}


## Config paths

A config path is a string comprised of a file path pattern and an
optional key path pattern. If a key path pattern is included it must be
appended to the file path using a hash (`#`) separator.

Examples of config paths:

- `train.py`
- `train.py#x`
- `*.py`
- `*.py#*`

If config path doesn't specify a key pattern, the pattern is assumed to
be `*`.

The private function `_split_config_path` splits a config path into its
file and key patterns.

    >>> from gage._internal.run_config import _split_config_path as split

    >>> split("")
    ('', '*')

    >>> split("train.py")
    ('train.py', '*')

    >>> split("train.py#x")
    ('train.py', 'x')

    >>> split("conf/*.yml#**.*")
    ('conf/*.yml', '**.*')

If `#` is included in the path more than once, subsequent hash
delimiters are included in the key path.

    >>> split("foo#bar#baz")
    ('foo', 'bar#baz')
