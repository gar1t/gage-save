# Staging a run dir

A staged run can be started by a runner using only the run directory and
the contents of the run meta directory. Staged runs can be relocated to
run on another compatible system. A staged run is independent of its
project.

A staged run requires a compatible system (platform, installed
applications and libraries, etc.)

For staging to occur, the runner must copy all files required by the run
that are not otherwise required of the system to the run directory.

Apart from creating a run manifest and logging actions performed during
staging, the run meta directory is not changed.

    >>> from gage._internal.run_util import *
    >>> from gage._internal.types import *

Run meta must be initialized before the run can be staged.

    >>> runs_home = make_temp_dir()
    >>> run = make_run(runs_home)

    >>> opref = OpRef("test", "test")
    >>> opdef = OpDef("test", {})
    >>> cmd = OpCmd(["python", "-c", "print('Hello!')"], {})

    >>> init_run_meta(run, opref, opdef, cmd, {}, {})

    >>> find(run_meta_dir(run))
    __schema__
    id
    initialized
    log/runner
    opdef.json
    opref
    proc/cmd
    proc/env

For details about initializing run meta, see
[`run-lifecycle-2-init-meta.md`](run-lifecycle-2-init-meta.md).

Stage the run using `stage_run`.


## Notes

What are we doing here? What does it actually mean to stage something?

I think this is more like "configure your 'system' for a run". In this
case the system is the run directory (cwd) and the command + env that's
needed to run the thing successfully.

Here's some scenarios:

``` bash
# cwd is the run directory
virtualenv .venv
.venv/bin/pip install $PROJECT  # What's the correct var here??

```
- Run `virtual env `