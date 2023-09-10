# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

import click

from .. import click_util

from . import runs_support


# def _ac_comment_index(ctx, incomplete, **_kw):
#     from . import runs_impl
#     args = click_util.Args(**ctx.params)
#     args.runs = ctx.args
#     runs = runs_impl.runs_op_selected(args, ctx, runs_impl.LATEST_RUN_ARG)
#     indexes = set()
#     for run in runs:
#         for i in range(len(run.get("comments") or [])):
#             indexes.add(str(i + 1))
#     return [i for i in sorted(indexes) if i.startswith(incomplete)]


def comment_params(fn: Callable[..., Any]):
    click_util.append_params(
        fn,
        [
            runs_support.runs_arg,
            click.Option(
                ("-l", "--list"),
                help="list comments for specified runs.",
                is_flag=True,
            ),
            click.Option(
                ("-a", "--add"),
                metavar="COMMENT",
                help="Add comment to specified runs.",
            ),
            click.Option(
                ("-e", "--edit"),
                help=(
                    "Use an editor to type a comment. Enabled by default if "
                    "COMMENT is not specified using --add."
                ),
                is_flag=True,
            ),
            click.Option(
                ("-d", "--delete"),
                metavar="INDEX",
                help=(
                    "Delete comment at INDEX from specified runs. Use `--list` "
                    "to show available indexes."
                ),
                type=click.INT,
                # shell_complete=_ac_comment_index,
            ),
            click.Option(
                ("-c", "--clear"),
                help="Clear all comments associated with specified runs.",
                is_flag=True,
            ),
            click.Option(
                ("-u", "--user"),
                metavar="USER",
                help=(
                    "User associated with new comments. May include host "
                    "as USER@HOST. By default the current user is used."
                ),
            ),
            runs_support.all_filters,
            click.Option(
                ("-y", "--yes"),
                help="Do not prompt before modifying comments.",
                is_flag=True,
            ),
        ],
    )
    return fn


@click.command("comment")
@comment_params
@click.pass_context
@click_util.use_args
@click_util.render_doc
def comment_runs(ctx: click.Context, args: Any):
    """Add or remove run comments.

    By default Guild opens the default text editor to add a new comment to the
    specified runs.

    To list runs, use `--list`.

    To add a comment without using an editor, use `--add`.

    To delete a comment, use `--delete` with the comment index shown using
    `--list`.

    To delete all comments associated with specified runs, use `--clear`.

    {{ runs_support.runs_arg }}

    If a `RUN` argument is not specified, ``1`` is assumed (the most recent
    run).

    {{ runs_support.all_filters }}
    """
    print("TODO: comment on runs")

    # from . import runs_impl

    # runs_impl.comment(args, ctx)
