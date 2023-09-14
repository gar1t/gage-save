# SPDX-License-Identifier: Apache-2.0

from typing import *

from .types import *

from . import cli

__all__ = [
    "init",
    "preview",
]


class RunSourceCode:
    def __init__(self, paths: list[str]):
        self.paths = paths


def init(opdef: OpDef):
    return RunSourceCode(["file1", "file2"])


def preview(sourcecode: RunSourceCode):
    from rich.panel import Panel
    from rich.console import Group

    table = cli.Table(["path"])
    for path in sourcecode.paths:
        table.add_row(path)
    return Panel(Group(table), title="Source Code")
