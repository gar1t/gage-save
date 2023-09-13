# Gage file samples

Use `check` to validate sample Gage files.

    >>> cd(sample("gagefiles"))

Use `load_gagefile()` to load a Gage file.

    >>> from gage._internal.gagefile import load_gagefile

## Empty file

An empty file is invalid JSON and can't be loaded.

    >>> run("gage check empty.json")
    ERROR: empty.json: invalid JSON: Expecting value: line 1 column 1 (char 0)
    <1>

## Empty object

An empty object is a valid Gage file.

    >>> run("gage check object.json")
    object.json is a valid Gage file
    <0>

## Minimal configuration

A minimal configuration is one operation with an exec attribute.

    >>> run("gage check minimal.json")
    minimal.json is a valid Gage file
    <0>

    >>> gf = load_gagefile("minimal.json")

    >>> gf.operations  # +wildcard
    {'train': <gage._internal.types.OpDef ...>}

    >>> train = gf.operations["train"]

    >>> train.exec
    'echo hello'

## Missing exec

An operation does not need an exec attribute.

    >>> run("gage check missing-exec.json")
    missing-exec.json is a valid Gage file
    <0>

    >>> gf = load_gagefile("missing-exec.json")

    >>> gf.operations["train"].exec

## Full exec spec

A full exec spec uses an object for `exec` to define commands for
various stages of a run lifecycle.

    >>> run("gage check full-exec.json")
    full-exec.json is a valid Gage file
    <0>

    >>> gf = load_gagefile("full-exec.json")

    >>> gf.operations  # +wildcard
    {'train': <gage._internal.types.OpDef ...>}

    >>> train = gf.operations["train"]

    >>> train.exec  # +wildcard
    <gage._internal.types.OpDefExec ...>

    >>> train.exec.copy_sourcecode
    'cp * $run_dir'

    >>> train.exec.copy_deps
    'echo pass'

    >>> train.exec.init_runtime

    >>> train.exec.run
    'dir .'

    >>> train.exec.finalize_run
    ['echo', 'pass']

## Invalid full exec

Exec commands must be either strings or arrays of strings.

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
