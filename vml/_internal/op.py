# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *
from subprocess import Popen

import subprocess

from .opdef import OpDef
from .run import Run

from . import run_manifest
from . import run_util


class OpError(Exception):
    pass


class Op:
    def __init__(self):
        self.opdef: Optional[OpDef] = None


def init_run(op: Op):
    return run_util.init_run()


def stage_run(run: Run, op: Op):
    with run_manifest.Manifest(run):
        _copy_sourcecode(op, run)
        _resolve_deps(op, run)


def _copy_sourcecode(op: Op, run: Run):
    pass


def _resolve_deps(op: Op, run: Run):
    pass


def start_run(run: Run, op: Op):
    stage_run(run, op)
    return _run_proc(run)


def _run_proc(run: Run):
    return subprocess.Popen(
        ["echo", "hello"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def wait_run_proc(p: Popen[bytes], run: Run, op: Op):
    result = p.wait()
    if result == 0:
        _finalize_run(run, op)
    else:
        _handle_run_error(result, run, op)
    return result


def _finalize_run(run: Run, op: Op):
    pass


def _handle_run_error(result: int, run: Run, op: Op):
    pass
