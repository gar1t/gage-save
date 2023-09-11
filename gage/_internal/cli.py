# SPDX-License-Identifier: Apache-2.0

from typing import *

import os

import rich.box
import rich.console
import rich.json
import rich.style
import rich.text
import rich.table

__all__ = [
    "Table",
    "err",
    "label",
    "out",
]

_out = rich.console.Console(soft_wrap=False)
_err = rich.console.Console(stderr=True, soft_wrap=False)

is_plain = os.getenv("TERM") in ("dumb", "unknown")


def out(val: Any, style: str | None = None, err: bool = False):
    print = _err.print if err else _out.print
    print(val, soft_wrap=True, style=style)


def err(val: Any, style: str | None = None):
    out(val, err=True)


def text(s: str, style: str | rich.style.Style = ""):
    return rich.text.Text(s, style=style)

def json(val: Any):
    return rich.json.JSON.from_data(val)


def label(s: str):
    return text(s, style="bold green")


def Table(show_header: bool = False):
    return rich.table.Table(
        show_header=show_header,
        box=rich.box.ROUNDED if not is_plain else None,
    )
