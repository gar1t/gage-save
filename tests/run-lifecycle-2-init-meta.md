# Initialing run meta

Run metadata ("meta") is information about the run that is independent
of the run directory and its contents. Meta is located in a side-car
directory (i.e. located along side the run directory) with the same name
but ending in `.meta`.

Specifically excluded from the meta directory:

- Source code
- Dependencies
- User generated files

A run must be initialized before it can be staged or run. Once
initialized, the run appears in a run listing.

Initializing a run does not affect the run directory.

Run meta init is performed by `init_run_meta`. Meta must be initialized
before a run is staged or started.

    >>> from gage._internal.run_util import *
    >>> from gage._internal.types import *

Runs must exist before their meta directory is initialized.

    >>> runs_home = make_temp_dir()
    >>> run = make_run(runs_home)

`run_meta_dir` returns the meta directory path for a run.

    >>> meta_dir = run_meta_dir(run)
    >>> assert meta_dir == run.run_dir + ".meta"

The meta directory does not exist initially.

    >>> assert not path_exists(meta_dir)

To initialize a run, provide the following:

- Run
- Op reference
- Op definition
- Op command
- User attributes
- System attributes

Define inputs to the init function.

    >>> opref = OpRef("test", "test")

    >>> opdef = OpDef("test", {})

    >>> cmd = OpCmd(
    ...     ["echo", "hello"],
    ...     {"foo": "123", "bar": "abc"}
    ... )

    >>> user_attrs = {
    ...     "label": "A test run",
    ...     "params": {"x": 1.1, "y": True},
    ... }

    >>> system_attrs = {
    ...     "platform": "test 123"
    ... }

Initialize the run by calling `init_run_meta`.

    >>> init_run_meta(
    ...     run,
    ...     opref,
    ...     opdef,
    ...     cmd,
    ...     user_attrs,
    ...     system_attrs
    ... )

The following files are created:

    >>> find(meta_dir, include_dirs=True, permissions=True)  # +diff
    -r--r--r-- __schema__
    -r--r--r-- id
    -r--r--r-- initialized
    drwxrwxr-x log
    -rw-rw-r-- log/runner
    -r--r--r-- opdef.json
    -r--r--r-- opref
    drwxrwxr-x proc
    -r--r--r-- proc/cmd
    -r--r--r-- proc/env
    drwxrwxr-x sys
    -r--r--r-- sys/platform
    drwxrwxr-x user
    -r--r--r-- user/label
    -r--r--r-- user/params

Files are read only with the exception of the runner log, which is
assumed to be writable until the run is finalized (see below).

### `__schema__`

`__schema__` contains the schema used for the directory layout and
contents.

    >>> cat(path_join(meta_dir, "__schema__"))  # +parse
    {x:d}

The current schema is defined by `META_SCHEMA`.

    >>> assert x == META_SCHEMA

### `id`

`id` is the run ID. This is saved in the meta dir for the contents to
remain independent of the container name.

    >>> cat(path_join(meta_dir, "id"))  # +parse
    {x:run_id}

    >>> assert x == run.id

### `opref`

`opref` is an encoded op reference. This is used in run listings to read
the run name efficiently.

    >>> cat(path_join(meta_dir, "opref"))  # +parse
    1 test test

### `opdef.json`

`opdef.json` is the JSON encoded operation definition, as provided by
either the project or otherwise generated for the run (e.g. dynamically
when running a language script).

This file is used when re-running the run or when using the run as a
prototype.

    >>> json.load(open(path_join(meta_dir, "opdef.json")))  # +pprint
    {}

### `proc/cmd` and `proc/env`

`proc/cmd` and `proc/env` contain the run process command args and env
vars respectively. These are used to start the run process.

    >>> cat(path_join(meta_dir, "proc", "cmd"))
    echo
    hello

    >>> cat(path_join(meta_dir, "proc", "env"))
    bar=abc
    foo=123

### `initialized`

`initialized` is a run timestamp that indicates when the run meta dir
was initialized. This is written at the end of the initialization
process.

    >>> cat(path_join(meta_dir, "initialized"))  # +parse
    {:timestamp}

### Runner log

The runner log contains log entries for the actions performed.

    >>> cat(path_join(meta_dir, "log", "runner"))  # +parse +diff
    {:date} Writing id
    {:date} Writing opdef.json
    {:date} Writing proc/cmd
    {:date} Writing proc/env
    {:date} Writing user/label
    {:date} Writing user/params
    {:date} Writing sys/platform
    {:date} Writing opref
    {:date} Writing initialized

Sample runner format:

    2023-09-03T11:59:00-0500 Writing id

- Date is ISO 8016
- No error level - all messages are equivalent
- Messages start with a capital letter
