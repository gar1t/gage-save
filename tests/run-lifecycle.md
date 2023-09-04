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

TODO:

High level (skip detail) calls to init meta, stage, etc. - apply status,
etc. to these dates.
