---
parse-types:
  # ISO 8601 format
  date: '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:[+-]\d{4}(?:\d{2})?)?'
---

# Run lifecycle

Runs are represented by the `Run` types.

    >>> from gage._internal.types import Run

The Run type is little more than a data container. It provides
property-based access to basic run attributes. Other run information is
read using various functions provided by the `run_util` module.

- `run_status`

      >>> from gage._internal.run_util import run_status

- `run_attrs`

      >>> from gage._internal.run_util import run_attrs

Runs are created and updated using life-cycle functions provided by
`run_util`.

- `make_run`

      >>> from gage._internal.run_util import make_run

The `var` module is used to list available runs. A run only appears in a
listing when it reaches a certain stage in its life cycle.

    >>> from gage._internal.var import list_runs

## Initial run (`make_run`)

A run is created with an ID and a run directory. Runs are always local
to a system.

A run is typically created using `make_run`. This function generates a
unique ID and creates a corresponding run directory in a given parent
directory.

Create a parent directory.

    >>> runs_home = make_temp_dir()

Create a new run.

    >>> run = make_run(runs_home)

We know three things about this run:

1. It has a unique ID

       >>> run.id  # +parse
       '{run_id:run_id}'

2. It has a corresponding run directory under `runs_home`

       >>> run.run_dir  # +parse
       '{run_dir:path}'

       >>> assert path_exists(run_dir)

       >>> assert run_dir == path_join(runs_home, run_id)

3. It's status is `unknown`

       >>> run_status(run)
       'unknown'

There's nothing more to the run.

The run directory is empty.

    >>> find(run_dir)
    <empty>

It's attributes cannot be read.

    >>> run_attrs(run)  # +parse
    Traceback (most recent call last):
    FileNotFoundError: {x}.meta/attrs

    >>> assert x == run_dir

The run doesn't show up in a run listing.

    >>> list_runs(runs_home)
    []

## Initialized run (`init_run_meta`)

`init_run_meta` initializes a run meta directory in preparation for
either staging or running.

    >>> from gage._internal.run_util import init_run_meta

The run meta directory is a side-car directory (i.e. located along side
the run directory) with the same name but ending in `.meta.`

`run_meta_dir` returns the meta directory path for a run.

    >>> from gage._internal.run_util import run_meta_dir

    >>> meta_dir = run_meta_dir(run)

    >>> assert meta_dir == run_dir + ".meta"

The meta directory does not exist initially.

    >>> assert not path_exists(meta_dir)

The meta directory contains all run-related information that is not part
of the run directory itself. Specifically excluded from the meta
directory:

- Source code
- Dependencies
- User generated files

A run must be initialized before it can be staged or run. Once
initialized, the run appears in a run listing.

Initializing a run does not affect the run directory.

To initialize a run, provide the following:

- Run
- Op reference
- Op definition
- Op command

    >>> from gage._internal.types import OpRef, OpDef, OpCmd

    >>> opref = OpRef("test", "test")
    >>> opdef = OpDef("test", {})
    >>> cmd = OpCmd(["echo", "hello"], {"foo": "123", "bar": "abc"})

Initialize the run by calling `init_run_meta`.

    >>> init_run_meta(run, opref, opdef, cmd)

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

Files are read only with the exception of the runner log, which is
assumed to be writable until the run is finalized (see below).

### `__schema__`

`__schema__` contains the schema used for the directory layout and
contents.

    >>> cat(path_join(meta_dir, "__schema__"))  # +parse
    {x:d}

The current schema is defined by `META_SCHEMA`.

    >>> from gage._internal.run_util import META_SCHEMA

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
    {:date} Writing opref
    {:date} Writing initialized

Sample runner format:

    2023-09-03T11:59:00-0500 Writing id

- Date is ISO 8016
- No error level - all messages are equivalent
- Messages start with a capital letter
