# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

from ._internal import run as runlib

FlagVal = Union[str, float, bool]

Flags = Dict[str, FlagVal]


class Operation:
    def __init__(
        self, project: str, name: Optional[str] = None, flags: Optional[Flags] = None
    ):
        self.project = project
        self.name = name
        self.flags = flags or {}

    def stage(self):
        run = Run("xxx", "yyy")
        _stage_run(run, self)
        return run

    def start(self, run: Optional[Run] = None):
        if not run:
            run = self.stage()
        _start_run(run, self)
        return run


def _stage_run(run: Run, op: Operation):
    pass


def _start_run(run: Run, op: Operation):
    pass


class Run:
    def __init__(self, id: str, run_base: str):
        self._run = runlib.Run(id, run_base)

    @property
    def run_dir(self):
        return self._run.run_dir

    def wait(self):
        pass


def run(*args: Any, **kw: Any):
    op = Operation(*args, **kw)
    run = op.start()
    run.wait()
    return run
