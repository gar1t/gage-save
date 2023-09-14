# Run utils

## Make a run

TODO: move applicable tests from `run-lifecycle.md` here and make life
cycle tests higher level.

    >>> from gage._internal.run_util import make_run

## Init run meta

TODO: move applicable tests from `run-lifecycle.md` here and make life
cycle tests higher level.

    >>> from gage._internal.types import OpRef, OpDef, OpCmd

    >>> from gage._internal.run_util import init_run_meta

### Errors

`init_run_meta` confirms that the opref op name and the op def op name
as the same.

    >>> tmp = make_temp_dir()
    >>> run = make_run(tmp)

    >>> init_run_meta(run, OpRef("test", "hi"), OpDef("bye", {}), OpCmd([], {}))
    Traceback (most recent call last):
    ValueError: mismatched names in opref ('hi') and opdef ('bye')

    >>> ls(tmp)
    <empty>
