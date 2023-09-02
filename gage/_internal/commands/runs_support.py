# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

import logging

from ..._vendor import click

from .. import click_util

log = logging.getLogger()


# def ac_run(ctx, param, incomplete):
#     # ensure that other_run follows the same logic as run, without needing to make
#     #    that logic know about other_run
#     if param.name == "other_run":
#         ctx.params["run"] = ctx.params["other_run"]
#     runs = runs_for_ctx(ctx)
#     return sorted([run.id for run in runs if run.id.startswith(incomplete)])


# def ac_local_run(ctx, param, incomplete):
#     runs = runs_for_ctx(ctx)
#     return sorted([run.id for run in runs if run.id.startswith(incomplete)])


# def runs_for_ctx(ctx):
#     from guild import config
#     from . import runs_impl

#     args = _runs_args_for_ctx(ctx)
#     with config.SetGuildHome(ctx.parent.params.get("guild_home")):
#         try:
#             return runs_impl.runs_for_args(args, ctx=ctx)
#         except SystemExit:
#             # Raised when cannot find runs for args.
#             return []


# def _runs_args_for_ctx(ctx):
#     args = click_util.Args(**ctx.params)
#     if not hasattr(args, "runs"):
#         maybe_run = getattr(args, "run", None)
#         args.runs = (maybe_run,) if maybe_run else ()
#     return args


# def run_for_ctx(ctx):
#     runs = runs_for_ctx(ctx)
#     return runs[0] if runs else None


# def ac_operation(ctx, _param, incomplete):
#     from guild import run_util
#     runs = runs_for_ctx(ctx)
#     ops = {run_util.format_operation(run, nowarn=True) for run in runs}
#     return sorted([op for op in ops if op.startswith(incomplete)])


# def ac_label(ctx, _param, incomplete):
#     runs = runs_for_ctx(ctx)
#     labels = {run.get("label") or "" for run in runs}
#     return sorted([_quote_label(l) for l in labels if l and l.startswith(incomplete)])


# def _quote_label(l):
#     return f"\"{l}\""


# def ac_tag(ctx, _param, incomplete):
#     # Reset tags to avoid limiting results based on selected tags.
#     ctx.params["tags"] = []
#     runs = runs_for_ctx(ctx)
#     return [tag for tag in _all_tags_sorted(runs) if tag.startswith(incomplete)]


# def _all_tags_sorted(runs):
#     tags = set()
#     for run in runs:
#         tags.update(run.get("tags") or [])
#     return sorted(tags)


# def ac_digest(ctx, _param, incomplete):
#     runs = runs_for_ctx(ctx)
#     digests = {run.get("sourcecode_digest") or "" for run in runs}
#     return sorted([d for d in digests if d and d.startswith(incomplete)])


# def ac_archive(ctx, param, incomplete):
#     return (
#         ac_support.ac_dir(incomplete)  #
#         + ac_support.ac_filename(["zip"], incomplete)  #
#         + ac_named_archive(ctx, param, incomplete, no_quote=True)
#     )


# def ac_named_archive(_ctx, _param, incomplete, no_quote=False):
#     """Returns named archives.

#     When used in isolation, values should be quoted as needed as they
#     can cotain spaces. If used with file system directives on systems
#     that support ac directives, values should not be quotes as their
#     spaces will be escaped by the shell support.
#     """
#     from guild import config

#     names = [
#         val for val in sorted([a.label or a.name for a in config.archives()])
#         if val.startswith(incomplete)
#     ]

#     return (
#         ac_support.quote(names)  #
#         if not no_quote or not ac_support.active_shell_supports_directives()  #
#         else names
#     )


def runs_arg(fn: Callable[..., Any]):
    """### Specify Runs

    You may use one or more `RUN` arguments to indicate which runs apply to the
    command. `RUN` may be a run ID, a run ID prefix, or a one-based index
    corresponding to a run returned by the list command.

    Indexes may also be specified in ranges in the form `START:END` where
    `START` is the start index and `END` is the end index. Either `START` or
    `END` may be omitted. If `START` is omitted, all runs up to `END` are
    selected. If `END` id omitted, all runs from `START` on are selected. If
    both `START` and `END` are omitted (i.e. the ``:`` char is used by itself)
    all runs are selected.
    """
    click_util.append_params(
        fn,
        [
            click.Argument(
                ("runs",),
                metavar="[RUN...]",
                nargs=-1,
                # shell_complete=ac_run,
            )
        ],
    )
    return cast(click.Command, fn)


def run_arg(fn: Callable[..., Any]):
    """### Specify a Run

    You may specify a run using a run ID, a run ID prefix, or a one-based index
    corresponding to a run returned by the `list` command.
    """
    click_util.append_params(
        fn,
        [
            click.Argument(
                ("run",),
                metavar="[RUN]",
                required=False,
                # shell_complete=ac_run,
            )
        ],
    )
    return fn


def common_filters(fn: Callable[..., Any]):
    """
    Runs may be filtered using options listed above. For more information ``gage
    help filters``.
    """
    click_util.append_params(
        fn,
        [
            click.Option(
                ("-F", "--filter", "filter_expr"),
                metavar="EXPR",
                help=(
                    "Filter runs using a filter expression. See Filter by "
                    "Expression above for details."
                ),
            ),
            click.Option(
                ("-Fo", "--operation", "filter_ops"),
                metavar="VAL",
                help="Filter runs with operations matching `VAL`.",
                multiple=True,
                # shell_complete=ac_operation,
            ),
            click.Option(
                ("-Fl", "--label", "filter_labels"),
                metavar="VAL",
                help=(
                    "Filter runs with labels matching VAL. To show unlabeled "
                    "runs, use --unlabeled."
                ),
                multiple=True,
                # shell_complete=ac_label,
            ),
            click.Option(
                ("-Fu", "--unlabeled", "filter_unlabeled"),
                help="Filter runs without labels.",
                is_flag=True,
            ),
            click.Option(
                ("-Ft", "--tag", "filter_tags"),
                metavar="TAG",
                help="Filter runs with TAG.",
                multiple=True,
                # shell_complete=ac_tag,
            ),
            click.Option(
                ("-Fc", "--comment", "filter_comments"),
                metavar="VAL",
                help="Filter runs with comments matching VAL.",
                multiple=True,
            ),
            click.Option(
                ("-Fm", "--marked", "filter_marked"),
                help="Filter marked runs.",
                is_flag=True,
            ),
            click.Option(
                ("-Fn", "--unmarked", "filter_unmarked"),
                help="Filter unmarked runs.",
                is_flag=True,
            ),
            click.Option(
                ("-Fs", "--started", "filter_started"),
                metavar="RANGE",
                help=(
                    "Filter runs started within RANGE. See above for valid time ranges."
                ),
            ),
            click.Option(
                ("-Fd", "--digest", "filter_digest"),
                metavar="VAL",
                help="Filter runs with a matching source code digest.",
                # shell_complete=ac_digest,
            ),
        ],
    )
    return cast(click.Command, fn)


def _callbacks(*cbs: Callable[..., Any]):
    def f(ctx: click.Context, param: click.Parameter, value: Any):
        for cb in cbs:
            value = cb(ctx, param, value)
        return value

    return f


def status_filters(fn: Callable[..., Any]) -> click.Command:
    """### Filter by Run Status

    Runs may also be filtered by specifying one or more status filters:
    `--running`, `--completed`, `--error`, and `--terminated`. These may be used
    together to include runs that match any of the filters. For example to only
    include runs that were either terminated or exited with an error, use
    ``--terminated --error``, or the short form ``-Set``.

    You may combine more than one status character with ``-S`` to expand the
    filter. For example, ``-Set`` shows only runs with terminated or error
    status.

    Status filters are applied before `RUN` indexes are resolved. For example, a
    run index of ``1`` is the latest run that matches the status filters.
    """
    click_util.append_params(
        fn,
        [
            click.Option(
                ("-Sr", "--running/--not-running", "status_running"),
                help="Filter runs that are still running.",
                is_flag=True,
                default=None,
                callback=_apply_status_chars,
            ),
            click.Option(
                ("-Sc", "--completed/--not-completed", "status_completed"),
                help="Filter completed runs.",
                is_flag=True,
                default=None,
                callback=_apply_status_chars,
            ),
            click.Option(
                ("-Se", "--error/--not-error", "status_error"),
                help="Filter runs that exited with an error.",
                is_flag=True,
                default=None,
                callback=_apply_status_chars,
            ),
            click.Option(
                ("-St", "--terminated/--not-terminated", "status_terminated"),
                help="Filter runs terminated by the user.",
                is_flag=True,
                default=None,
                callback=_apply_status_chars,
            ),
            click.Option(
                ("-Sp", "--pending/--not-pending", "status_pending"),
                help="Filter pending runs.",
                is_flag=True,
                default=None,
                callback=_apply_status_chars,
            ),
            click.Option(
                ("-Ss", "--staged/--not-staged", "status_staged"),
                help="Filter staged runs.",
                is_flag=True,
                default=None,
                callback=_apply_status_chars,
            ),
            click.Option(
                # Used by _apply_status_chars to implicitly set status
                # flags using one or more chars.
                ("-S", "status_chars"),
                hidden=True,
                callback=_validate_status_chars,
            ),
        ],
    )
    return cast(click.Command, fn)


def _apply_status_chars(ctx: click.Context, param: click.Parameter, value: Any):
    if value:
        return value
    status_chars = ctx.params.get("status_chars")
    if not status_chars:
        return value
    status_char = _param_status_char(param)
    if status_char in status_chars:
        return True
    return value


def _param_status_char(param: click.Parameter):
    for opt in param.opts:
        if opt.startswith("-S"):
            char = opt[2:]
            assert len(char) == 1, param.opts
            return char
    assert False, param.opts


def _validate_status_chars(ctx: click.Context, param: click.Parameter, value: Any):
    if not value:
        return value
    for char in value:
        if char not in "rcetps":
            raise SystemExit(
                f"unrecognized status char '{char}' in option '-S'\n"
                f"Try '{ctx.command_path} --help' for more information."
            )
    return value


@click_util.render_doc
def all_filters(fn: Callable[..., Any]) -> click.Command:
    """
    {{ common_filters }}
    {{ status_filters }}
    """
    click_util.append_params(
        fn,
        [
            common_filters,
            status_filters,
        ],
    )
    return cast(click.Command, fn)


def archive_option(help: str) -> click.Command:
    """### Show Archived Runs

    Use `--archive` to show runs in an archive directory. PATH may be
    a directory or a zip file created using 'guild export'.
    """
    assert isinstance(help, str), "@archive_option must be called with help"

    def wrapper(fn: Callable[..., Any]):
        click_util.append_params(
            fn,
            [
                click.Option(
                    ("-A", "--archive"),
                    metavar="PATH",
                    help=help,
                    # shell_complete=ac_archive,
                )
            ],
        )
        return fn

    return cast(click.Command, wrapper)
