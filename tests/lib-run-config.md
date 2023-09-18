# Core run config support

`run_config` provides support for run configuration implementation.

    >>> from gage._internal.run_config import *

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
