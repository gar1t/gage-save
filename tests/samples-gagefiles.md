# Gage file samples

Use `check` to validate sample Gage files.

    >>> cd(sample("gagefiles"))

    >>> run("gage check empty.json")
    ERROR: empty.json: invalid JSON: Expecting value: line 1 column 1 (char 0)
    <1>

    >>> run("gage check object.json")
    object.json is a valid Gage file
    <0>

    >>> run("gage check minimal.json")
    minimal.json is a valid Gage file
    <0>

    >>> run("gage check full-exec.json")
    full-exec.json is a valid Gage file
    <0>

    >>> run("gage check invalid-exec.json")  # +wildcard
    ERROR: invalid-exec.json has problems
    Properties ['train'] are invalid
    Properties ['exec'] are invalid
    The instance must be valid against exactly one subschema; it is valid against [] and invalid against [0, 1, 2]
    The instance must be of type "string"
    The instance must be of type "array"
    Properties ['copy-deps', 'init-runtime', 'finalize-run'] are invalid
    ...
    <1>
