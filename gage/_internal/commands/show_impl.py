# SPDX-License-Identifier: Apache-2.0

from typing import *

from ..types import *

import logging
import os

from .. import cli

from ..run_output import RunOutputReader

from ..run_util import format_run_timestamp
from ..run_util import meta_config
from ..run_util import run_attr
from ..run_util import run_meta_path
from ..run_util import run_status
from ..run_util import run_timestamp
from ..run_util import run_user_attr

from ..util import format_dir

from .impl_util import one_run

__all__ = ["Args", "show"]

log = logging.getLogger(__name__)


class Args(NamedTuple):
    run: str


def show(args: Args):
    run = one_run(args)
    with cli.pager():
        _show(run)


def _show(run: Run):
    # TODO consolidate this vvvv

    import rich.box
    from rich.panel import Panel
    from rich.text import Text
    from rich.table import Table, Column

    status = run_status(run)
    started = run_timestamp(run, "started")
    stopped = run_timestamp(run, "stopped")
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

    cli.out(
        Panel(
            header,
            title=Text(run.id, style=cli.PANEL_TITLE_STYLE),
            box=rich.box.ROUNDED if not cli.is_plain else rich.box.MARKDOWN,
        )
    )

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

    cli.out(
        Panel(
            attributes,
            title=Text("Attributes", style=cli.PANEL_TITLE_STYLE),
            box=rich.box.ROUNDED if not cli.is_plain else rich.box.MARKDOWN,
        )
    )

    config = meta_config(run)
    if config:
        config_table = Table.grid(
            Column(style=cli.LABEL_STYLE),
            Column(style=cli.VALUE_STYLE),
            padding=(0, 1),
            collapse_padding=False,
        )
        for name in sorted(config):
            config_table.add_row(name, str(config[name]))

        cli.out(
            Panel(
                config_table,
                title=Text("Configuration", style=cli.PANEL_TITLE_STYLE),
                box=rich.box.ROUNDED if not cli.is_plain else rich.box.MARKDOWN,
            )
        )

    output = list(_iter_run_output(run))
    for output_name, output_reader in output:
        try:
            output_lines = list(output_reader)
        except Exception as e:
            log.warning(
                "Error reading run output (%s): %s",
                output_reader.filename,
                e,
            )
        else:
            output_table = Table.grid(Column(style="dim"))
            for line in output_lines:
                output_table.add_row(
                    Text(line.text, style="orange3" if line.stream == 1 else "")
                )
            output_title = (
                f"Output [{_output_desc(output_name)}]"
                if len(output) > 1 or output_name != "run"
                else "Output"
            )
            cli.out(
                Panel(
                    output_table,
                    title=Text(output_title, style=cli.PANEL_TITLE_STYLE),
                    box=rich.box.ROUNDED if not cli.is_plain else rich.box.MARKDOWN,
                )
            )


def _output_desc(name: str):
    return {
        "sourcecode": "stage source code",
        "runtime": "stage runtime",
        "dependencies": "stage dependencies",
        "run": "run",
        "finalize": "finalize run",
    }.get(name, name)


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
