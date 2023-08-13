# SPDX-License-Identifier: Apache-2.0

from typing import *
from typing import BinaryIO

import functools
import logging
import os
import sys
import shutil

from vml._vendor import click

from . import ansi_util

log = logging.getLogger("guild")

TABLE_COL_SPACING = 2

_shell = os.getenv("SHELL")


def _max_width():
    try:
        return int(os.environ["COLUMNS"])
    except (KeyError, ValueError):
        return shutil.get_terminal_size()[0]


_noted = set()


def error(msg: Optional[str] = None, exit_status: int = 1) -> NoReturn:
    raise SystemExit(msg, exit_status)


def out(s: str = "", wrap: bool = False, **kw: Any):
    if wrap:
        s = globals()["wrap"](s)
    _echo(s, **kw)


def wrap(s: str, width: Optional[int] = None):
    width = width or _default_terminal_width()
    return click.wrap_text(s, width)


def _default_terminal_width():
    width = terminal_width()
    return max(min(width, 78), 40)


def terminal_width():
    return shutil.get_terminal_size().columns


def _echo(s: str, err: bool = False, **kw: Any):
    click.echo(s, err=err, **kw)


def note(msg: str, err: bool = True, **kw: Any):
    _echo(click.style(msg, dim=True), err=err, **kw)


def note_once(msg: str):
    if msg not in _noted:
        note(msg)
        _noted.add(msg)


_TableSort = Union[str, List[str]]

_TableDataVal = Union[None, int, float, str]

_TableDataItem = Dict[str, _TableDataVal]

_TableData = List[_TableDataItem]

_TableCols = List[str]

_TableFormattedItem = Dict[str, str]

_TableFormattedData = List[_TableFormattedItem]

_TableColInfo = Dict[str, Any]

_TableDetail = List[str]

_TableDetailCallback = Callable[[Dict[str, Any]], None]


def table(
    data: _TableData,
    cols: _TableCols,
    sort: Optional[_TableSort] = None,
    detail: Optional[_TableDetail] = None,
    detail_cb: Optional[_TableDetailCallback] = None,
    indent: int = 0,
    err: bool = False,
    max_width_adj: int = 0,
    file: Optional[BinaryIO] = None,
    **style_kw: Any,
):
    data = sorted(data, key=_table_row_sort_key(sort))
    formatted = _format_table_data(data, cols + (detail or []))
    col_info = _col_info(formatted, cols)
    if sys.stdout.isatty():
        max_width = _max_width() + max_width_adj
    else:
        max_width = None
    for formatted_item, data_item in zip(formatted, data):
        _table_item_out(
            formatted_item,
            data_item,
            cols,
            col_info,
            detail,
            detail_cb,
            indent,
            max_width,
            err,
            file,
            style_kw,
        )


def _table_row_sort_key(sort: Union[None, _TableSort]):
    def sort_key(x: _TableDataItem, y: _TableDataItem):
        assert sort
        return _item_cmp(x, y, sort)

    def no_sort(X: _TableDataItem, y: _TableDataItem):
        return 0

    cmp = sort_key if sort else no_sort
    return functools.cmp_to_key(cmp)


def _item_cmp(x: _TableDataItem, y: _TableDataItem, sort: _TableSort):
    if isinstance(sort, str):
        return _val_cmp(x, y, sort)
    for part in sort:
        part_cmp = _val_cmp(x, y, part)
        if part_cmp != 0:
            return part_cmp
    return 0


def _val_cmp(x: _TableDataItem, y: _TableDataItem, sort: str) -> int:
    if sort.startswith("-"):
        sort = sort[1:]
        rev = -1
    else:
        rev = 1
    x_val = x.get(sort)
    y_val = y.get(sort)
    x_val_coerced = _coerce_cmp_val(x_val, y_val)
    y_val_coerced = _coerce_cmp_val(y_val, x_val_coerced)
    return rev * ((x_val_coerced > y_val_coerced) - (x_val_coerced < y_val_coerced))  # type: ignore


def _coerce_cmp_val(x: _TableDataVal, y: _TableDataVal):
    if sys.version_info[0] == 2:
        return x
    if x is None:
        if y is None:
            return ""
        return type(y)()
    if type(x) == type(y):  # pylint: disable=unidiomatic-typecheck
        return x
    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        return x
    if isinstance(x, str):
        return x
    if isinstance(y, str):
        return ""
    return str(x)


def _format_table_data(data: _TableData, cols: _TableCols):
    return [{col: _format_table_val(item.get(col)) for col in cols} for item in data]


def _format_table_val(val: _TableDataVal):
    if val is None:
        return ""
    if isinstance(val, str):
        return val
    return str(val)


def _col_info(data: _TableFormattedData, cols: _TableCols) -> _TableColInfo:
    info = {}
    for item in data:
        for col in cols:
            col_info = info.setdefault(col, {})
            col_info["width"] = max(col_info.get("width", 0), len(item[col]))
    return info


def _table_item_out(
    formatted_item: _TableFormattedItem,
    data_item: _TableDataItem,
    cols: _TableCols,
    col_info: _TableColInfo,
    detail: Union[_TableDetail, None],
    detail_cb: Union[_TableDetailCallback, None],
    indent: int,
    max_col_width: Union[int, None],
    err: bool,
    file: Union[BinaryIO, None],
    style_kw: Any,
):
    indent_padding = " " * indent
    click.echo(indent_padding, file=file, nl=False, err=err)
    line_pos = indent
    for i, col in enumerate(cols):
        val = formatted_item[col]
        last_col = i == len(cols) - 1
        val = _pad_col_val(val, col, col_info) if not last_col else val
        val_display_len = len(ansi_util.strip_ansi_format(val))
        line_pos = line_pos + val_display_len
        if max_col_width is not None:
            display_val = val[: -(line_pos - max_col_width)]
        else:
            display_val = val
        if max_col_width is not None and line_pos > max_col_width:
            click.echo(
                style(display_val, **style_kw),
                file=file,
                nl=False,
                err=err,
            )
            break
        click.echo(style(val, **style_kw), file=file, nl=False, err=err)
    click.echo(file=file, err=err)
    terminal_width = shutil.get_terminal_size()[0]
    if detail_cb:
        detail_cb(data_item)
    else:
        for key in detail or []:
            click.echo(indent_padding, file=file, nl=False, err=err)
            formatted = _format_detail_val(formatted_item[key], indent, terminal_width)
            click.echo(
                style(f"  {key}:{formatted}", **style_kw),
                file=file,
                err=err,
            )


def _format_detail_val(val: Any, indent: int, terminal_width: int):
    if isinstance(val, list):
        if val:
            val_indent = " " * (indent + 4)
            val_width = terminal_width - len(val_indent)
            return "\n" + "\n".join(
                [click.wrap_text(x, val_width, val_indent, val_indent) for x in val]
            )
        return " -"
    return f" {val}"


def _pad_col_val(val: str, col: str, col_info: _TableColInfo):
    return val.ljust(col_info[col]["width"] + TABLE_COL_SPACING)


def confirm(prompt: str, default: bool = False, wrap: bool = False):
    if wrap:
        prompt = globals()["wrap"](prompt)
    click.echo(prompt, nl=False, err=True)
    yes_no_opts = "(Y/n)" if default else "(y/N)"
    click.echo(f" {yes_no_opts} ", nl=False, err=True)
    c = input()
    yes_vals = ["y", "yes"]
    if default:
        yes_vals.append("")
    return c.lower().strip() in yes_vals


def page(text: str):
    click.echo_via_pager(text)


def style(text: str, **kw: Any):
    if not _shell:
        return text
    return click.style(text, **kw)
