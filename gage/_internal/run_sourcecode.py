# SPDX-License-Identifier: Apache-2.0

from typing import *

from .types import *

import os

from . import cli

from .file_select import parse_patterns
from .file_select import preview_copytree

__all__ = [
    "init",
    "preview",
]

DEFAULT_INCLUDE = [
    "**/* text size<10000 max-matches=500",
]

DEFAULT_EXCLUDE = [
    "**/.* dir",
    "**/* dir sentinel=bin/activate",
    "**/* dir sentinel=.nocopy",
]


class RunSourceCode:
    def __init__(
        self,
        src: str,
        include: list[str],
        exclude: list[str],
        paths: list[str],
    ):
        self.src = src
        self.include = include
        self.exclude = exclude
        self.paths = paths

    def as_json(self) -> dict[str, Any]:
        return {
            "src": self.src,
            "include": self.include,
            "exclude": self.exclude,
            "paths": self.paths,
        }


def init(opdef: OpDef):
    sourcecode = opdef.get_sourcecode()
    src = os.path.dirname(opdef.get_src())
    include = _sourcecode_include(sourcecode)
    exclude = _sourcecode_exclude(sourcecode)
    select = parse_patterns(include, exclude)
    paths = [path for path, _result in preview_copytree(src, select)]
    return RunSourceCode(src, include, exclude, paths)


def _sourcecode_include(sc: OpDefSourceCode | None):
    include = sc.get_include() if sc else None
    if include is None:
        return DEFAULT_INCLUDE
    return include


def _sourcecode_exclude(sourcecode: OpDefSourceCode | None):
    include = sourcecode.get_include() if sourcecode else None
    exclude = (sourcecode.get_exclude() if sourcecode else None) or []
    if include is None:
        return DEFAULT_EXCLUDE + exclude
    return exclude


def preview(sourcecode: RunSourceCode):
    return cli.Panel(
        cli.Group(
            cli.Columns(
                [
                    _preview_include_patterns_table(sourcecode.include),
                    _preview_exclude_patterns_table(sourcecode.exclude),
                ]
            ),
            _preview_matched_files_table(sourcecode.paths),
        ),
        title="Source Code",
    )


def _preview_include_patterns_table(include: list[str]):
    table = cli.Table(["include patterns"])
    if not include:
        table.add_row("[dim]<none>[/dim]")
    else:
        for pattern in include:
            table.add_row(pattern)
    return table


def _preview_exclude_patterns_table(exclude: list[str]):
    table = cli.Table(["exclude patterns"])
    if not exclude:
        table.add_row("[dim]<none>[/dim]")
    else:
        for pattern in exclude:
            table.add_row(pattern)
    return table


def _preview_matched_files_table(paths: list[str]):
    table = cli.Table(["matched files"])
    if not paths:
        table.add_row("[dim]<none>[/dim]")
    else:
        for path in paths:
            table.add_row(path)
    return table
