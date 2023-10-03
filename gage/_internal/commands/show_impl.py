# SPDX-License-Identifier: Apache-2.0

from typing import *

from ..types import *

import logging
import os

import rich.box

from rich.console import Group
from rich.padding import Padding
from rich.text import Text
from rich.table import Table, Column

import human_readable

from natsort import natsorted

from .. import cli

from ..run_output import RunOutputReader

from ..run_util import RunManifest
from ..run_util import RunFileType
from ..run_util import format_run_timestamp
from ..run_util import meta_config
from ..run_util import run_attr
from ..run_util import run_meta_path
from ..run_util import run_status
from ..run_util import run_timestamp
from ..run_util import run_user_attr

from ..util import format_dir

from .impl_support import one_run


log = logging.getLogger(__name__)


class Args(NamedTuple):
    run: str
    files: bool


def show(args: Args):
    run = one_run(args)
    default = True
    if args.files:
        _show_files(run)
        default = False
    if default:
        with cli.pager():
            _show(run)


def Header(run: Run):
    status = run_status(run)
    label = run_user_attr(run, "label") or ""

    header = Table.grid(
        Column(),
        Column(justify="right"),
        expand=True,
        padding=(0, 1),
        collapse_padding=False,
    )
    header.add_row(
        Text(run.opref.get_full_name(), style="bold " + cli.LABEL_STYLE),
        Text(status, style=cli.run_status_style(status)),
    )
    if label:
        header.add_row(Text(label, style=cli.SECOND_LABEL_STYLE))

    return cli.Panel(header, title=run.id)


def Attributes(run: Run):
    started = run_timestamp(run, "started")
    stopped = run_timestamp(run, "stopped")
    location = format_dir(os.path.dirname(run.run_dir))
    exit_code = str(run_attr(run, "exit_code", None))

    attributes = Table.grid(
        Column(style=cli.LABEL_STYLE),
        Column(style=cli.VALUE_STYLE),
        padding=(0, 1),
        collapse_padding=False,
    )
    attributes.add_row("id", run.id)
    attributes.add_row("name", run.name)
    attributes.add_row("started", format_run_timestamp(started))
    attributes.add_row("stopped", format_run_timestamp(stopped))
    attributes.add_row("location", location)
    attributes.add_row("exit_code", str(exit_code) if exit_code is not None else "")

    return cli.Panel(attributes, title="Attributes")


def Config(run: Run):
    config = meta_config(run)
    if not config:
        return Group()
    config_table = Table.grid(
        Column(style=cli.LABEL_STYLE),
        Column(style=cli.VALUE_STYLE),
        padding=(0, 1),
        collapse_padding=False,
    )
    for name in sorted(config):
        config_table.add_row(name, str(config[name]))

    return cli.Panel(config_table, title="Configuration")


def Files(run: Run, table_only: bool = False):
    with RunManifest(run) as m:
        files = list(m)
    files_table = cli.Table(
        expand=not table_only,
        show_footer=not table_only,
        show_edge=table_only,
        box=None
        if table_only
        else rich.box.MARKDOWN
        if cli.is_plain
        else rich.box.SIMPLE,
        padding=(0, 1) if table_only else 0,
    )
    files_table.add_column(
        "name",
    )
    files_table.add_column(
        "type",
        style="dim",
    )
    files_table.add_column(
        "size",
        justify="right",
        style="magenta",
        footer_style="not b magenta",
    )
    total_size = 0
    for type, digest, path in natsorted(files):
        stat = os.stat(os.path.join(run.run_dir, path))
        files_table.add_row(
            path,
            _type_desc(type),
            _format_file_size(stat.st_size),
        )
        total_size += stat.st_size

    files_table.columns[2].footer = f"total: {_format_file_size(total_size)}"

    if table_only:
        return files_table
    return cli.Panel(files_table, title="Files")


def _type_desc(type: RunFileType):
    match type:
        case "s":
            return "source code"
        case "d":
            return "dependency"
        case "r":
            return "runtime"
        case "g":
            return "generated"
        case _:
            return f"unknown (type)"


def _format_file_size(size: int):
    if size < 1000:
        # human_readable applies (decimal) formatting to bytes, bypass
        return f"{size} B"
    return human_readable.file_size(size, formatting=".1f")


def OutputTable(reader: RunOutputReader, name: str = "", pad: bool = False):
    table = cli.Table(
        (name, {"style": "dim"}),
        show_header=name != "",
        expand=True,
        show_edge=False,
        padding=0,
        box=rich.box.SIMPLE_HEAD,
    )
    try:
        lines = list(reader)
    except Exception as e:
        log.warning(
            "Error reading run output (%s): %s",
            reader.filename,
            e,
        )
    else:
        # TODO truncate lines and show message if too long
        for line in lines:
            table.add_row(Text(line.text, style="orange3" if line.stream == 1 else ""))
    return Padding(table, (1 if pad else 0, 0, 0, 0))


def Output(run: Run):
    output = list(_iter_run_output(run))
    if not output:
        return Group()
    if len(output) == 1:
        name, reader = output[0]
        return cli.Panel(OutputTable(reader), title="Output")
    return cli.Panel(
        Group(
            *(
                OutputTable(reader, name, pad=i > 0)
                for i, (name, reader) in enumerate(output)
            )
        ),
        title="Output",
    )


def _iter_run_output(run: Run) -> Generator[tuple[str, RunOutputReader], Any, None]:
    output_dirname = run_meta_path(run, "output")
    for name in sorted(os.listdir(output_dirname)):
        if os.path.splitext(name)[1] != ".index":
            continue
        name = name[:-6]
        filename = os.path.join(output_dirname, name)
        if not os.path.exists(filename):
            continue
        parts = name.split("_")
        output_name = parts[1] if len(parts) == 2 else parts[0]
        yield output_name, RunOutputReader(filename)


def _output_desc(name: str):
    return {
        "sourcecode": "stage source code",
        "runtime": "stage runtime",
        "dependencies": "stage dependencies",
        "run": "run",
        "finalize": "finalize run",
    }.get(name, name)


def _show(run: Run):
    cli.out(Header(run))
    cli.out(Attributes(run))
    cli.out(Config(run))
    cli.out(Files(run))
    cli.out(Output(run))


def _show_files(run: Run):
    cli.out(Files(run, table_only=True))
