# SPDX-License-Identifier: Apache-2.0

from typing import *

from vml._vendor import click

from vml._internal import click_util

from . import ac_support
from . import runs_support


def _ac_location(ctx: click.Context, param: click.Parameter, incomplete: str):
    return ac_support.ac_filename(["zip"], incomplete)


def export_params(fn: Callable[..., Any]):
    click_util.append_params(
        fn,
        [
            click.Argument(("location",), shell_complete=_ac_location),
            runs_support.runs_arg,
            click.Option(
                ("-m", "--move"),
                help="Move exported runs rather than copy.",
                is_flag=True,
            ),
            click.Option(
                ("-r", "--copy-resources"),
                help="Copy resources for each exported run.",
                is_flag=True,
            ),
            runs_support.all_filters,
            click.Option(
                ("-y", "--yes"),
                help="Do not prompt before exporting.",
                is_flag=True,
            ),
        ],
    )
    return fn


@click.command("export")
@export_params
@click.pass_context
@click_util.use_args
@click_util.render_doc
def export_runs(ctx: click.Context, args: Any):
    """Export one or more runs.

    `LOCATION` must be a writeable directory.

    By default, runs are copied to `LOCATION`. Use `--move` to move them
    instead.

    By default, resources are NOT copied with each exported run, but their links
    are maintained. To copy resources, use `--copy-resources`.

    **WARNING**: Use `--copy-resources` with care as each exported run will
    contain a separate copy of each resource!

    {{ runs_support.runs_arg }}

    If a `RUN` argument is not specified, ``:`` is assumed (all runs are
    selected).

    {{ runs_support.all_filters }}
    """
    print("TODO: export runs")

    # from . import runs_impl

    # runs_impl.export(args, ctx)
