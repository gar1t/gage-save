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

## Initial run status

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

       >>> assert path.exists(run_dir)

       >>> assert run_dir == path.join(runs_home, run_id)

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







---------------------------------------

Gage is creating the run but it's otherwise undefined
  - Inferred by existence of meta dir containing PENDING marker
  - Meta dir under way, exists with PENDING marker
  - Run dir under way, may or may not exist


A Gage run is made up of a number of parts:

- A `.meta` directory, which is represented by `.meta.zip` after the run
  is finalized
- A `.run` directory
