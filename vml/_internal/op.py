# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

from .opdef import OpDef
from .run import Run

from . import run_manifest
from . import run_util


class OpError(Exception):
    pass


class Op:
    def __init__(self):
        self.opdef: Optional[OpDef] = None


def stage_op(op: Op):
    run = run_util.init_run()
    with run_manifest.Manifest(run):
        _copy_sourcecode(op, run)
        _resolve_deps(op, run)
    return run


def _copy_sourcecode(op: Op, run: Run):
    pass


def _resolve_deps(op: Op, run: Run):
    pass


def run_op(op: Op):
    run = stage_op(op)
    try:
        _run_proc(run)
    except Exception as e:
        _handle_run_error(e, run)
    else:
        _handle_run_success(run)
    finally:
        _finalize_run(run)


def _run_proc(run: Run):
    pass


def _handle_run_error(e: Exception, run: Run):
    pass


def _handle_run_success(run: Run):
    pass


def _finalize_run(run: Run):
    pass
