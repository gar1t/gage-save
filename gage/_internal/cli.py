# SPDX-License-Identifier: Apache-2.0

from typing import *

import os
import re
import shlex

import click

import rich.box
import rich.console
import rich.json
import rich.markdown
import rich.panel
import rich.style
import rich.text
import rich.table

import typer.core

__all__ = [
    "AliasGroup",
    "Table",
    "err",
    "error_message",
    "exit_with_error",
    "excludes",
    "label",
    "markdown",
    "out",
]

_out = rich.console.Console(soft_wrap=False)
_err = rich.console.Console(stderr=True, soft_wrap=False)

is_plain = os.getenv("TERM") in ("dumb", "unknown")

TABLE_HEADER_STYLE = "yellow"
TABLE_BORDER_STYLE = "dim"
LABEL_STYLE = "bold cyan"


def out(val: Any, style: str | None = None, wrap: bool = False, err: bool = False):
    print = _err.print if err else _out.print
    print(val, soft_wrap=not wrap, style=style)


def err(val: Any, style: str | None = None):
    out(val, err=True)


def error_message(msg: str):
    err(f"[red bold]ERROR:[/red bold] {msg}")


def exit_with_error(msg: str, code: int = 1) -> NoReturn:
    error_message(msg)
    raise SystemExit(code)


def text(s: str, style: str | rich.style.Style = ""):
    return rich.text.Text(s, style=style)


def json(val: Any):
    return rich.json.JSON.from_data(val)


def label(s: str):
    return text(s, style=LABEL_STYLE)


def markdown(md: str):
    return rich.markdown.Markdown(md)


def excludes(*params: str):
    def callback(value: Any, param: typer.core.TyperArgument, ctx: click.Context):
        if value:
            for other_name in params:
                if param.name != other_name and other_name in ctx.params:
                    raise SystemExit(
                        f"{param.name} and {other_name} cannot both be specified\n"
                        f"Try '{ctx.command_path} --help' for more information."
                    )
        return value

    return callback


class pager:
    _pager_env = os.getenv("PAGER") or os.getenv("MANPAGER")

    def __init__(self):
        self._pager = _out.pager(styles=_pager_supports_styles(self._pager_env))

    def __enter__(self):
        if self._pager_env is None:
            os.environ["PAGER"] = "less -r"
        return self._pager.__enter__()

    def __exit__(self, *exc: Any):
        self._pager.__exit__(*exc)
        if self._pager_env is None:
            del os.environ["PAGER"]


def _pager_supports_styles(pager: str | None):
    if pager is None:
        return True
    parts = shlex.split(pager)
    return parts[0] == "less" and "-r" in parts[1:]


def Table(header: list[str] | None = None, **kw: Any):
    t = rich.table.Table(
        show_header=header is not None,
        box=rich.box.ROUNDED if not is_plain else None,
        border_style=TABLE_BORDER_STYLE,
        header_style=TABLE_HEADER_STYLE,
        **kw
    )
    for col_name in header or []:
        t.add_column(col_name)
    return t


class AliasGroup(typer.core.TyperGroup):
    """click Group subclass that supports commands with aliases.

    To alias a command, include the aliases in the command name,
    separated by commas.
    """

    _CMD_SPLIT_P = re.compile(r", ?")

    def get_command(self, ctx: click.Context, cmd_name: str):
        return super().get_command(ctx, self._map_name(cmd_name))

    def _map_name(self, default_name: str):
        for cmd in self.commands.values():
            if cmd.name and default_name in self._CMD_SPLIT_P.split(cmd.name):
                return cmd.name
        return default_name


class _MarkdownHeading(rich.markdown.Heading):
    """Internal Rich Markdown heading.

    To change the hard-coded heading alignment from center to left, we
    need to patch `rich.markdown.Markdown.elements` with a modified
    heading implementation.
    """

    def __rich_console__(
        self,
        console: rich.console.Console,
        options: rich.console.ConsoleOptions,
    ) -> rich.console.RenderResult:
        text = self.text
        text._text = [s.upper() for s in text._text]
        if self.tag == "h1":
            text.justify = "center"
            yield rich.panel.Panel(text)
        else:
            if self.tag == "h2":
                yield Text("")
            yield text


class _TableElement(rich.markdown.TableElement):
    def __rich_console__(
        self,
        console: rich.console.Console,
        options: rich.console.ConsoleOptions,
    ) -> rich.console.RenderResult:
        table = rich.table.Table(box=rich.box.ROUNDED)

        if self.header is not None and self.header.row is not None:
            for column in self.header.row.cells:
                table.add_column(column.content)

        if self.body is not None:
            for row in self.body.rows:
                row_content = [element.content for element in row.cells]
                table.add_row(*row_content)

        yield table


rich.markdown.Markdown.elements["heading_open"] = _MarkdownHeading
rich.markdown.Markdown.elements["table_open"] = _TableElement
