# Starting a staged run

    >>> from gage._internal.run_util import *
    >>> from gage._internal.types import *

## Basic run

`start_run()` starts a staged run. Once a run is staged, it's
independent of the originating project.

Create a sample project.

    >>> cd(make_temp_dir())

Use a simple Python script to print a message.

    >>> write("say.py", """
    ... msg = "Hi there"
    ... print(msg)
    ... """.lstrip())

Create an opdef that runs the script.

    >>> opdef = OpDef("test", {
    ...   "exec": "python say.py",
    ...   "config": "say.py"
    ... })

Initialize a new run.

    >>> runs_home = make_temp_dir()

    >>> run = make_run(runs_home)

TODO: do we need cmd/env? Why not just use the opdef? Or is this derived?

TODO: OpCmd needs to support shell command str vs list of args.

    >>> init_run_meta(
    ...     run,
    ...     OpRef("test", "test"),
    ...     opdef,
    ...     {},
    ...     OpCmd(["python", "say.py"], {})
    ... )

Stage a run.

    >>> stage_run(run, ".")

    >>> ls(run.run_dir)
    say.py

Start the run.

    >>> p = start_run(run)

Open run output.

    >>> output = open_run_output(run, p)

Wait for the run process to exit.

    >>> p.wait()
    0

Wait for output to finish.

    >>> output.wait_and_close()

List meta dir contents.

    >>> ls(run_meta_dir(run))  # +diff
    __schema__
    config.json
    id
    initialized
    log/files
    log/patched
    log/runner
    manifest
    opdef.json
    opref
    output/40_run
    output/40_run.index
    proc/cmd
    proc/env
    staged

Show run output.

    >>> cat(run_meta_path(run, "output", "40_run"))
    Hi there

## Run with config

Start another run with different config.

    >>> run = make_run(runs_home)

    >>> init_run_meta(
    ...     run,
    ...     OpRef("test", "test"),
    ...     opdef,
    ...     {"msg": "Ho there"},
    ...     OpCmd(["python", "say.py"], {})
    ... )

    >>> stage_run(run, ".")

Start the run with output.

    >>> p = start_run(run)
    >>> output = open_run_output(run, p)
    >>> p.wait()
    0
    >>> output.wait_and_close()

Show run output.

    >>> cat(run_meta_path(run, "output", "40_run"))
    Ho there
