# Staging a run dir

A staged run can be started by a runner using only the run directory and
the contents of the run meta directory. Staged runs (i.e. the run and
meta directories) can be relocated to another compatible system and
started there.

A staged run is independent of its project.

A staged run relies on a compatible system (platform, installed
applications and libraries, etc.) to run. If a staged run is moved to an
incompatible system, it won't run.

To stage a run, the runner must copy all files required by the run that
are not otherwise provided by the system to the run directory.

When staging a run, meta is updated with a manifest file and additional
log entries, which reflect the actions performed during the staging
process.

Run meta must be initialized before the run can be staged. For more
information on this process, see [*Initializing run
meta*](topic-run-lifecycle-2-init-meta.md).

Create a run and initialize its meta.

    >>> from gage._internal.run_util import *

    >>> runs_home = make_temp_dir()

    >>> run = make_run(runs_home)

    >>> from gage._internal.types import *

    >>> opref = OpRef("test", "test")
    >>> opdef = OpDef("test", {})
    >>> cmd = OpCmd(["python", "-c", "print('Hello!')"], {})

    >>> init_run_meta(run, opref, opdef, cmd, {}, {})

    >>> find(run_meta_dir(run))
    __schema__
    id
    initialized
    log/runner
    name
    opdef.json
    opref
    proc/cmd
    proc/env

Stage the run using `stage_run()`.

    >>> stage_run(run)

According to the meta configuration above, nothing is copied for
staging.

Two changes are made in this case.

- A `staged` timestamp is written

    >>> meta_dir = run_meta_dir(run)

    >>> find(meta_dir, include_dirs=True, permissions=True)  # +wildcard
    -r--r--r-- __schema__
    ...
    -r--r--r-- staged

- Runner logs are updated

    >>> cat(path_join(meta_dir, "log", "runner"))  # +parse
    {}
    {:date} Writing staged

## Copying files

Gage divides staged file copies into three phases:

- Source code copy
- Runtime init
- Dependency resolution

Each of these these phases is implemented by `stages`

## Errors

Stage a non-existing run directory.

    >>> missing_run_dir = make_temp_dir()
    >>> delete_temp_dir(missing_run_dir)

    >>> stage_run(Run("", missing_run_dir))  # +parse
    Traceback (most recent call last):
    FileNotFoundError: Run dir does not exist: {:path}

Stage a run without a meta dir.

    >>> run_dir_no_meta = make_temp_dir()
    >>> stage_run(Run("", run_dir_no_meta))  # +parse
    Traceback (most recent call last):
    FileNotFoundError: Run meta dir does not exist: {:path}.meta
