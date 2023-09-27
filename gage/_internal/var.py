# SPDX-License-Identifier: Apache-2.0

from typing import *
from .types import *

import functools
import logging
import os
import shutil

from . import sys_config

from .run_util import run_attr
from .run_util import run_for_meta_dir

from .file_util import safe_delete_tree

log = logging.getLogger(__name__)

RunFilter = Callable[[Run], bool]

# =================================================================
# List runs
# =================================================================


def list_runs(
    root: str | None = None,
    filter: RunFilter | None = None,
    sort: list[str] | None = None,
):
    root = root or sys_config.runs_home()
    filter = filter or _all_runs_filter
    runs = [run for run in _iter_runs(root) if filter(run)]
    if not sort:
        return runs
    return sorted(runs, key=_run_sort_key(sort))


def _all_runs_filter(run: Run):
    return True


def _iter_runs(root: str):
    try:
        names = set(os.listdir(root))
    except OSError:
        names: Set[str] = set()
    for name in names:
        if not name.endswith(".meta"):
            continue
        meta_dir = os.path.join(root, name)
        run = run_for_meta_dir(meta_dir)
        if run:
            yield run


def _run_sort_key(sort: list[str]):
    def cmp(a: Run, b: Run):
        return _run_cmp(a, b, sort)

    return functools.cmp_to_key(cmp)


def _run_cmp(a: Run, b: Run, sort: list[str]):
    for attr in sort:
        attr_cmp = _run_attr_cmp(a, b, attr)
        if attr_cmp != 0:
            return attr_cmp
    return 0


def _run_attr_cmp(a: Run, b: Run, attr: str):
    if attr.startswith("-"):
        attr = attr[1:]
        rev = -1
    else:
        rev = 1
    x_val = run_attr(a, attr, None)
    if x_val is None:
        return -rev
    y_val = run_attr(b, attr, None)
    if y_val is None:
        return rev
    return rev * ((x_val > y_val) - (x_val < y_val))


# =================================================================
# Delete runs
# =================================================================


def delete_runs(runs: list[Run], permanent: bool = False):
    for run in runs:
        _delete_run(run, permanent)


def _delete_run(run: Run, permanent: bool):
    if permanent:
        _delete_tree(run.meta_dir)
        _delete_tree(run.run_dir)
    else:
        _move(run.meta_dir, _deleted_meta_dir(run))


def _deleted_meta_dir(run: Run):
    return run.meta_dir + ".deleted"


def _delete_tree(dirname: str):
    safe_delete_tree(dirname)


def _move(src: str, dest: str):
    shutil.move(src, dest)
