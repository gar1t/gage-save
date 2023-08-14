# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

from ..._vendor import click

from .. import click_util

from . import remote_support
from . import runs_support


# def _ac_tag(ctx: click.Context, param: click.Parameter, incomplete: str):
#     if ctx.params.get("remote"):
#         return []

#     tags = set()
#     ctx.params["runs"] = ctx.args or ["1"]
#     for run in runs_support.runs_for_ctx(ctx):
#         tags.update(_safe_list(run.get("tags")))
#     return [t for t in sorted(tags) if t.startswith(incomplete)]


# def _safe_list(x):
#     if isinstance(x, list):
#         return x
#     return []


def tag_params(fn: Callable[..., Any]):
    click_util.append_params(
        fn,
        [
            runs_support.runs_arg,
            click.Option(
                ("-a", "--add"),
                metavar="TAG",
                help="Associate TAG with specified runs. May be used multiple times.",
                multiple=True,
            ),
            click.Option(
                ("-d", "--delete"),
                metavar="TAG",
                help="Delete TAG from specified runs. May be used multiple times.",
                multiple=True,
                # shell_complete=_ac_tag,
            ),
            click.Option(
                ("-c", "--clear"),
                help="Clear all tags associated with specified runs.",
                is_flag=True,
            ),
            click.Option(
                ("-s", "--sync-labels"),
                help=(
                    "Update run label by adding and deleting corresponding tag parts."
                ),
                is_flag=True,
            ),
            click.Option(
                ("--list-all",),
                help="List all tags used for the specified runs.",
                is_flag=True,
            ),
            runs_support.all_filters,
            remote_support.remote_option("Tag remote runs."),
            click.Option(
                ("-y", "--yes"),
                help="Do not prompt before modifying tags.",
                is_flag=True,
            ),
        ],
    )
    return fn


@click.command("tag")
@tag_params
@click.pass_context
@click_util.use_args
@click_util.render_doc
def tag_runs(ctx: click.Context, args: Any):
    """Add or remove run tags.

    Tags may be used to filter runs using the `--tag` option with run related
    commands.

    Use this command to add and remove tags for one or more runs. To remove all
    tags, use `--clear`.

    Note that modifying tags for a run does not modify the run label, which may
    contain tags from when the run was generated. To update run labels, use the
    `label` command.

    {{ runs_support.runs_arg }}

    If a `RUN` argument is not specified, ``1`` is assumed (the most recent
    run).

    {{ runs_support.all_filters }}

    ### Tag Remote Runs

    To tag remote runs, use `--remote`.

    {{ remote_support.remote_option }}
    """
    print("TODO tags runs")

    # from . import runs_impl

    # runs_impl.tag(args, ctx)
