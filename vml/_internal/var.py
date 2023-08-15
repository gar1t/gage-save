# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

import functools
import os

from .run import Run

from . import config

RunFilter = Callable[[Run], bool]


def runs(
    root: Optional[str] = None,
    sort: Optional[str] = None,
    filter: Optional[RunFilter] = None,
):
    root = root or config.runs_home()
    filter = filter or _all_runs_filter
    runs = [run for run in _all_runs(root) if filter(run)]
    if not sort:
        return runs
    return sorted(runs, key=_run_sort_key(sort))


def _all_runs_filter(run: Run):
    return True


def _all_runs(root: str):
    return [Run(id, run_base) for id, run_base in _iter_runs(root)]


def _iter_runs(root: str):
    try:
        names = set(os.listdir(root))
    except OSError:
        names: Set[str] = set()
    for name in names:
        if not name.endswith(".meta"):
            continue
        base_name = name[:-5]
        run_dir_name = base_name + ".run"
        if not run_dir_name in names:
            continue
        yield base_name, os.path.join(root, base_name)


def _run_sort_key(sort: str):
    def cmp(a: Run, b: Run):
        return _run_cmp(a, b, sort)

    return functools.cmp_to_key(cmp)


def _run_cmp(a: Run, b: Run, sort: str):
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
    x_val = _run_attr(a, attr)
    if x_val is None:
        return -rev
    y_val = _run_attr(b, attr)
    if y_val is None:
        return rev
    return rev * ((x_val > y_val) - (x_val < y_val))


def _run_attr(run: Run, name: str):
    if name in Run.__properties__:
        return getattr(run, name)
    return run.read_attr(name)
