# Gage file support

## Validation

Gage files are represented by JSON-decoded objects Python.

The `validate_data()` function is used to validate a Python object.

    >>> from gage._internal.gagefile import *

`validate_data()` returns silently when data is valid.

    >>> validate_data({})

It raises `ValidationError` for invalid date.

    >>> validate_data(123)
    Traceback (most recent call last):
    gage._internal.gagefile.ValidationError: invalid

The function `validation_error_output()` returns a JSON compatible
object of error information.

    >>> try:
    ...     validate_data(123)
    ... except ValidationError as e:
    ...     json_pprint(validation_error_output(e))
    {
      "absoluteKeywordLocation": "https://gageml.org/gagefile#",
      "errors": [
        {
          "absoluteKeywordLocation": "https://gageml.org/gagefile#/title",
          "annotation": "Gage ML Project File",
          "instanceLocation": "",
          "keywordLocation": "/title",
          "valid": true
        },
        {
          "absoluteKeywordLocation": "https://gageml.org/gagefile#/type",
          "error": "The instance must be of type \"object\"",
          "instanceLocation": "",
          "keywordLocation": "/type",
          "valid": false
        }
      ],
      "instanceLocation": "",
      "keywordLocation": "",
      "valid": false
    }

`validation_errors()` provides a list of error messages.

    >>> try:
    ...     validate_data(123)
    ... except ValidationError as e:
    ...     json_pprint(validation_errors(e))
    [
      "The instance must be of type \"object\""
    ]

Create functions that validates Gage file data and prints results.

    >>> def validate(data, verbose=False):
    ...     try:
    ...         validate_data(data)
    ...     except ValidationError as e:
    ...         if verbose:
    ...             import json
    ...             output = validation_error_output(e)
    ...             print(json.dumps(output, indent=2, sort_keys=True))
    ...         else:
    ...             for err in validation_errors(e):
    ...                 print(err)
    ...     else:
    ...         print("ok")

    >>> def validate_opdef(data):
    ...     validate({"test": data})

At a minimum, a Gage file must be a dict.

    >>> validate({})
    ok

    >>> validate([])
    The instance must be of type "object"

    >>> validate(None)
    The instance must be of type "object"

    >>> validate(123)
    The instance must be of type "object"

## Operations

Top-level entries must be valid operation defs.

An operation def doesn't require any attributes.

    >>> validate({"test": {}})
    ok

An operation must be an object however.

    >>> validate({"test": 123})
    Properties ['test'] are invalid
    The instance must be of type "object"

    >>> validate({"test": []})
    Properties ['test'] are invalid
    The instance must be of type "object"

### `description`

`description` is an optional string describing the operation.

    >>> validate_opdef({"description": "An example, naturally"})
    ok

    >>> validate({"test": {"description": 123}})
    Properties ['test'] are invalid
    Properties ['description'] are invalid
    The instance must be of type "string"

### `default`

`default` is boolean value that indicates if the operation is the
default for a project.

    >>> validate_opdef({"default": True})
    ok

    >>> validate_opdef({"default": 123})
    Properties ['test'] are invalid
    Properties ['default'] are invalid
    The instance must be of type "boolean"

`default` only applies to one operation. However, the schema does not
validate this.

    >>> validate({"a": {"default": True}, "b": {"default": True}})
    ok

### `exec`

`exec` is one of:

- string
- list of strings
- object of exec string expressions

When `exec` an object, it may have any of the following properties:

- `stage-sourcecode`
- `stage-dependencies`
- `resolve-dependencies`
- `stage-runtime`
- `run`
- `finalize-run`

A single string is a shell command.

    >>> validate_opdef({"exec": "echo hello"})
    ok

An empty string is valid.

    >>> validate_opdef({"exec": ""})
    ok

A list of string arguments may be specified as a command.

    >>> validate_opdef({"exec": ["echo", "hello"]})
    ok

A shell command may be empty.

    >>> validate_opdef({"exec": ""})
    ok

A list of command args may be empty.

    >>> validate_opdef({"exec": []})
    ok

However, an entry in a command args list cannot be empty.

    >>> validate_opdef({"exec": [""]})  # +wildcard
    Properties ['test'] are invalid
    Properties ['exec'] are invalid
    ...
    The text is too short (minimum 1 characters)
    ...

An object is used to provide fine-grained control over what is executed
for a run.

    >>> validate_opdef({"exec": {
    ...     "stage-sourcecode": "cp *.py $run_dir",
    ...     "stage-dependencies": "cp *.data $run_dir",
    ...     "stage-runtime": "virtualenv .venv",
    ...     "run": "python train.py",
    ...     "finalize-run": "rm *.temp"
    ... }})
    ok

Invalid examples:

    >>> validate_opdef({"exec": 123})  # +wildcard
    Properties ['test'] are invalid
    Properties ['exec'] are invalid
    ...
    The instance must be of type "string"
    The instance must be of type "array"
    The instance must be of type "object"

    >>> validate_opdef({"exec": {"foo": 123}})  # +wildcard
    Properties ['test'] are invalid
    Properties ['exec'] are invalid
    ...
    The instance must be of type "string"
    The instance must be of type "array"
    ['foo']

### `sourcecode`

`sourcecode` specifies the source code include/exclude patterns for the
operation.

`sourcecode` must be a string or a list of strings.

A string cannot be empty.

    >>> validate_opdef({"sourcecode": ""})  # +wildcard
    Properties ['test'] are invalid
    Properties ['sourcecode'] are invalid
    ...
    The text is too short (minimum 1 characters)
    ...

    >>> validate_opdef({"sourcecode": "*"})
    ok

A list my be empty.

    >>> validate_opdef({"sourcecode": []})
    ok

Items in the list cannot be empty.

    >>> validate_opdef({"sourcecode": [""]})  # +wildcard
    Properties ['test'] are invalid
    Properties ['sourcecode'] are invalid
    ...
    The text is too short (minimum 1 characters)
    The instance must be of type "boolean"

Invalid values:

    >>> validate_opdef({"sourcecode": 123})  # +wildcard
    Properties ['test'] are invalid
    Properties ['sourcecode'] are invalid
    ...
    The instance must be of type "string"
    The instance must be of type "array"
    The instance must be of type "boolean"

    >>> validate_opdef({"sourcecode": {}})  # +wildcard
    Properties ['test'] are invalid
    Properties ['sourcecode'] are invalid
    ...
    The instance must be of type "string"
    The instance must be of type "array"
    The instance must be of type "boolean"

    >>> validate_opdef({"sourcecode": [123]})  # +wildcard
    Properties ['test'] are invalid
    Properties ['sourcecode'] are invalid
    ...
    [0]
    The instance must be of type "string"
    The instance must be of type "boolean"

### `config`

`config` defines operation configuration. It may be a string, a list of
strings, an object or a list of objects.

Strings must be non-empty.

    >>> validate_opdef({"config": ""})  # +wildcard
    Properties ['test'] are invalid
    Properties ['config'] are invalid
    ...
    The text is too short (minimum 1 characters)
    ...

    >>> validate_opdef({"config": [""]})  # +wildcard
    Properties ['test'] are invalid
    Properties ['config'] are invalid
    ...
    [0]
    The text is too short (minimum 1 characters)
    ...

Objects must define `keys`.

    >>> validate_opdef({"config": {}})  # +wildcard
    Properties ['test'] are invalid
    Properties ['config'] are invalid
    ...
    The object is missing required properties ['keys']
    ...

`keys` may be a string or a list of strings. String values must be
non-empty. Lists must be non-empty.

    >>> validate_opdef({"config": {"keys": ""}})  # +wildcard
    Properties ['test'] are invalid
    Properties ['config'] are invalid
    ...
    Properties ['keys'] are invalid
    ...
    The text is too short (minimum 1 characters)
    ...

    >>> validate_opdef({"config": {"keys": []}})  # +wildcard
    Properties ['test'] are invalid
    Properties ['config'] are invalid
    ...
    Properties ['keys'] are invalid
    ...
    The array has too few elements (minimum 1)
    ...

    >>> validate_opdef({"config": {"keys": ["foo", ""]}})  # +wildcard
    Properties ['test'] are invalid
    Properties ['config'] are invalid
    ...
    Properties ['keys'] are invalid
    ...
    The text is too short (minimum 1 characters)
    ...

Config objects may specify `prefix`, `strip-prefix` and `description` properties.

    >>> validate_opdef({"config": {
    ...     "prefix": "train_x",
    ...     "strip-prefix": "x",
    ...     "description": "Some var x",
    ...     "keys": "train.py#x"
    ... }})  # +wildcard
    ok

TODO: prefix/strip-prefix in the above example wants to be `rename`.
E.g. `rename = "x train_x"` where `rename` is a string or list of
strings (each string applying a rename rule to the associated keys).
