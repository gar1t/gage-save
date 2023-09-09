# Making a run

A run is created with an ID and a run directory. Runs are always local
to a system.

A run is typically created using `make_run`. This function generates a
unique ID and creates a corresponding run directory in a given parent
directory.

    >>> from gage._internal.run_util import *
    >>> from gage._internal.var import list_runs

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
