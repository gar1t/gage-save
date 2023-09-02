# Gage file support

## Validation

Gage files are represented by JSON-decoded objects Python.

The `validate()` function is used to validate a Python object.

    >>> from gage._internal import gagefile

Create a function that validates Gage file data.

    >>> def validate(data, verbose=False):
    ...     try:
    ...         gagefile.validate(data)
    ...     except gagefile.ValidationError as e:
    ...         if verbose:
    ...             import json
    ...             output = gagefile.validation_error_output(e)
    ...             print(json.dumps(output, indent=2, sort_keys=True))
    ...         else:
    ...             for err in gagefile.validation_errors(e):
    ...                 print(err)
    ...     else:
    ...         print("ok")

In the default case, `validate()` returns False when data is not valid.

    >>> validate("not valid Gage file data")
    The instance must be of type "object"

With the `verbose` flag the function returns a detailed report when
validation fails.

    >>> validate("not valid Gage file data", verbose=True)
    ... # +json +diff -space
    {
      "absoluteKeywordLocation":
        "https://gageml.com/gagefile.schema.json#",
      "errors": [
        {
          "absoluteKeywordLocation":
            "https://gageml.com/gagefile.schema.json#/title",
          "annotation": "Gage ML Project File",
          "instanceLocation": "",
          "keywordLocation": "/title",
          "valid": true
        },
        {
          "absoluteKeywordLocation":
            "https://gageml.com/gagefile.schema.json#/description",
          "annotation": "Specification to support Gage ML operations",
          "instanceLocation": "",
          "keywordLocation": "/description",
          "valid": true
        },
        {
          "absoluteKeywordLocation":
            "https://gageml.com/gagefile.schema.json#/type",
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

At a minimum, a Gage file must be a dict.

    >>> validate({})
    ok

    >>> validate(None)
    The instance must be of type "object"

    >>> validate([])
    The instance must be of type "object"

    >>> validate(123)
    The instance must be of type "object"

### Operations

Top-level entries must be valid operation defs.

An operation def doesn't require any attributes.

    >>> validate({"test": {}})
    ok

Supported top-level attributes:

- `description` - optional description of the operation

    >>> validate({"test": {"description": "An example, naturally"}})
    ok

    >>> validate({"test": {"description": 123}})
    Properties ['test'] are invalid
    Properties ['description'] are invalid
    The instance must be of type "string"

- `default` - boolean indicating whether the operation is the default
  for the project

    >>> validate({"test": {"default": True}})
    ok

    >>> validate({"test": {"default": 123}})
    Properties ['test'] are invalid
    Properties ['default'] are invalid
    The instance must be of type "boolean"

- `exec` - must be a non-empty string or a non-empty list of non-empty
  strings.

    >>> validate({"test": {"exec": ""}})  # -space
    Properties ['test'] are invalid
    Properties ['exec'] are invalid
    The instance must be valid against exactly one subschema;
      it is valid against [] and invalid against [0, 1]
    The text is too short (minimum 1 characters)
    The instance must be of type "array"

    >>> validate({"test": {"exec": []}})  # -space
    Properties ['test'] are invalid
    Properties ['exec'] are invalid
    The instance must be valid against exactly one subschema;
      it is valid against [] and invalid against [0, 1]
    The instance must be of type "string"
    The array has too few elements (minimum 1)

Note that the following example is invalid but manages to pass the
validation. This is an issue with jschon 0.11.0. As it's not a critical
problem for Gage we're living with the behavior.

    >>> validate({"test": {"exec": [""]}})
    ok
