# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

from .types import *

import os
import uuid

from . import config
from . import util


def make_run(location: Optional[str] = None):
    run_id = unique_run_id()
    location = location or config.runs_home()
    run_dir = os.path.join(location, run_id)
    util.make_dir(run_dir)
    return Run(run_id, run_dir)


def unique_run_id():
    return uuid.uuid4().hex


def run_status(run: Run) -> RunStatus:
    meta_dir = run_meta_dir(run)
    if not os.path.exists(meta_dir):
        return "unknown"
    assert False


def run_meta_dir(run: Run):
    return run.run_dir + ".meta"


def run_meta_path(run: Run, *path: str):
    return os.path.join(run_meta_dir(run), *path)


def run_attrs(run: Run) -> Dict[str, Any]:
    attrs_dir = run_meta_path(run, "attrs")
    if not os.path.exists(attrs_dir):
        raise FileNotFoundError(attrs_dir)
    assert False


def run_attr(run: Run, name: str):
    try:
        return getattr(run, name)
    except AttributeError:
        assert False, f"TODO run attr {name} somewhere in {run.run_dir}"
