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

    >>> config["x"]
    123

    >>> config["a"]
    Traceback (most recent call last):
    KeyError: 'a'

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

## Matching keys

`match_keys()` applies a list of include and exclude patterns to a list
of keys and return the corresponding list of matching keys.

Matching rules are:

- `*` matches one level of keys and can be used with other characters
- `**` matches any level of keys
- Otherwise characters and dots are matched as specified

Empty include list never matches.

    >>> match_keys([], [], [])
    []

    >>> match_keys([], [], ["a"])
    []

Use `*` to match one level.

    >>> match_keys(["*"], [], ["a"])
    ['a']

    >>> match_keys(["*"], [], ["a", "b"])
    ['a', 'b']

    >>> match_keys(["*"], [], ["a", "b", "c.d"])
    ['a', 'b']

    >>> match_keys(["c.*"], [], ["a", "b", "c.d"])
    ['c.d']

`*` may be used with other characters to match within a level.

    >>> match_keys(["a*"], [], ["aaa", "aba", "bab", "bcb"])
    ['aaa', 'aba']

    >>> match_keys(["b*"], [], ["aaa", "aba", "bab", "bcb"])
    ['bab', 'bcb']

    >>> match_keys(["*a"], [], ["aaa", "aba", "bab", "bcb"])
    ['aaa', 'aba']

    >>> match_keys(["*c*"], [], ["aaa", "aba", "bab", "bcb"])
    ['bcb']

`**` matches any level but must be used in conjunction with another
pattern.

    >>> match_keys(["**"], [], ["a"])
    []

    >>> match_keys(["**.*"], [], ["a"])
    ['a']

    >>> match_keys(["**.*"], [], ["a", "a.b", "a.b.c", "a.b.c.d"])
    ['a', 'a.b', 'a.b.c', 'a.b.c.d']

    >>> match_keys(["**.b"], [], ["a", "a.b", "a.b.c", "a.b.c.d"])
    ['a.b']

    >>> match_keys(["**.c"], [], ["a", "a.b", "a.b.c", "a.b.c.d"])
    ['a.b.c']

    >>> match_keys(["a.**.*"], [], ["a", "a.b", "a.b.c", "a.b.c.d"])
    ['a.b', 'a.b.c', 'a.b.c.d']

    >>> match_keys(["**.c.**.*"], [], ["a", "a.b", "a.b.c", "a.b.c.d"])
    ['a.b.c.d']

Exclude matches apply the same rules but remove matches.

    >>> match_keys(["a"], ["a"], ["a"])
    []

    >>> match_keys(["*"], ["a"], ["a"])
    []

    >>> match_keys(["*"], ["a"], ["a", "b"])
    ['b']

    >>> match_keys(["a.**.*"], ["**.d"], ["a", "a.b", "a.b.c", "a.b.c.d"])
    ['a.b', 'a.b.c']

Multiple includes extend the selected results.

    >>> match_keys(["a", "a.**.*"], [], ["a", "a.b", "a.b.c", "a.b.c.d"])
    ['a', 'a.b', 'a.b.c', 'a.b.c.d']

Multiple excludes extend the excluded results.

    >>> match_keys(["a.**.*"], ["**.d", "**.c"],
    ...            ["a", "a.b", "a.b.c", "a.b.c.d"])
    ['a.b']

## Configuration paths

`iter_config_paths()` yields tuples of path and applicable run config
for files that should be modified.

Create a sample directory structure.

    >>> target_dir = make_temp_dir()
    >>> cd(target_dir)

    >>> write("hello.py", """
    ... x = 1
    ... y = 2
    ... op = "add"
    ... """)

    >>> write("config.json", """
    ... {
    ...     "a": 3,
    ...     "b": 4
    ... }
    ... """)

    >>> touch("sample.txt")
    >>> touch("sample.bin")

    >>> ls(target_dir)
    config.json
    hello.py
    sample.bin
    sample.txt

Create an op def with config targeting various values.

    >>> from gage._internal.types import *

    >>> opdef = OpDef("test", {
    ...   "config": [
    ...     {
    ...       "include": "hello.py",
    ...       "exclude": "hello.py#op"
    ...     },
    ...     {
    ...       "name": "A",
    ...       "path": "config.json#a"
    ...     }
    ...   ]
    ... })

Print targeted files and their associated config keys for the op def.


    >>> for path, keys, config in iter_config_paths(opdef, target_dir):
    ...     print(path, keys, config)
