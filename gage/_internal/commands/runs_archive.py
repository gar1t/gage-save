# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

import click

from .. import click_util

from . import runs_support


def archive_params(fn: Callable[..., Any]):
    click_util.append_params(
        fn,
        [
            click.Argument(
                ("name",),
                # shell_complete=runs_support.ac_named_archive,
                required=False,
            ),
            runs_support.runs_arg,
            click.Option(
                ("-c", "--create"),
                help="Create a new archive if NAME doesn't exist.",
                is_flag=True,
            ),
            click.Option(
                ("-l", "--list"),
                help="list archives.",
                is_flag=True,
            ),
            click.Option(
                ("-c", "--copy"),
                help="Copy archived runs rather than move.",
                is_flag=True,
            ),
            click.Option(
                ("-r", "--copy-resources"),
                help="Copy resources for each exported run.",
                is_flag=True,
            ),
            click.Option(
                ("-d", "--description"),
                help="Description used for archive when creating.",
            ),
            click.Option(
                ("-v", "--verbose"),
                help="Show more information when listing archives.",
                is_flag=True,
            ),
            runs_support.all_filters,
            click.Option(
                ("-y", "--yes"),
                help="Do not prompt before archiving.",
                is_flag=True,
            ),
        ],
    )
    return fn


@click.command("archive")
@archive_params
@click.pass_context
@click_util.use_args
@click_util.render_doc
def archive_runs(ctx: click.Context, args: Any):
    """Archive one or more runs.

    `NAME` must refer to an exlisting archive unless `--create` is used, in
    which case a new archive is created.

    By default, run are moved to the archive. To copy runs, use `--copy`.

    By default, resources are NOT copied with each archiveed run, but their
    links are maintained. To copy resources, use `--copy-resources`.

    **WARNING**: Use `--copy-resources` with care as each archiveed run will
    contain a separate copy of each resource!

    {{ runs_support.runs_arg }}

    If a `RUN` argument is not specified, ``:`` is assumed (all runs are
    selected).

    {{ runs_support.all_filters }}
    """
    print("TODO: archive runs")

    # from . import runs_impl

    # runs_impl.archive(args, ctx)
