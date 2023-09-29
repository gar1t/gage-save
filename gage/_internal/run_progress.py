# SPDX-License-Identifier: Apache-2.0

from typing import *

from .types import *

import rich.progress

__all__ = [
    "NullProgress",
    "RichProgress",
]


class _NullProgressTask:
    def __enter__(self):
        return self

    def __exit__(self, *exc: Any):
        pass

    def update(
        self,
        advance: float | None = None,
        description: str | None = None,
        total: float | None = None,
        completed: float | None = None,
    ):
        pass


class NullProgress:
    def task(self, description: str, total: float | None = None):
        return _NullProgressTask()

    def __enter__(self):
        return self

    def __exit__(self, *exc: Any):
        pass


class _RichProgressTask:
    def __init__(
        self,
        progress: rich.progress.Progress,
        task: rich.progress.TaskID,
    ):
        self._p = progress
        self._t = task

    def __enter__(self):
        return self

    def __exit__(self, *exc: Any):
        self._p.remove_task(self._t)

    def update(
        self,
        advance: float | None = None,
        description: str | None = None,
        total: float | None = None,
        completed: float | None = None,
    ):
        self._p.update(
            self._t,
            advance=advance,
            description=description,
            total=total,
            completed=completed,
        )


class RichProgress:
    def __init__(self):
        self._p = rich.progress.Progress(
            rich.progress.SpinnerColumn(),
            rich.progress.TextColumn("[dim]{task.description}"),
            transient=True,
            expand=False,
        )

    def task(self, description: str, total: float | None = None):
        task = self._p.add_task(description, total=total)
        return _RichProgressTask(self._p, task)

    def __enter__(self):
        self._p.__enter__()
        return self

    def __exit__(self, *exc: Any):
        self._p.__exit__(*exc)
