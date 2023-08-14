# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

from ..._vendor import click

from .. import click_util

from . import runs_support


def import_params(fn: Callable[..., Any]):
    click_util.append_params(
        fn,
        [
            click.Argument(
                ("archive",),
                # shell_complete=runs_support.ac_archive
            ),
            runs_support.runs_arg,
            click.Option(
                ("-m", "--move"),
                help="Move imported runs rather than copy.",
                is_flag=True,
            ),
            click.Option(
                ("--copy-resources",),
                help="Copy resources for each imported run.",
                is_flag=True,
            ),
            runs_support.all_filters,
            click.Option(
                ("-y", "--yes"),
                help="Do not prompt before importing.",
                is_flag=True,
            ),
        ],
    )
    return fn


@click.command("import")
@import_params
@click.pass_context
@click_util.use_args
@click_util.render_doc
def import_runs(ctx: click.Context, args: Any):
    """Import one or more runs from `ARCHIVE`.

    `ARCHIVE` must be a directory that contains exported runs. Archive
    directories can be created using ``guild export``.

    You may use ``guild runs list --archive ARCHIVE`` to view runs in `ARCHIVE`.

    By default, resources are NOT copied with each imported run, but their links
    are maintained. To copy resources, use `--copy-resources`.

    **WARNING**: Use `--copy-resources` with care as each imported run will
    contain a separate copy of each resource!

    {{ runs_support.runs_arg }}

    If a `RUN` argument is not specified, ``:`` is assumed (all runs are
    selected).

    {{ runs_support.all_filters }}
    """
    print("TODO: import runs")

    # from . import runs_impl

    # runs_impl.import_(args, ctx)
