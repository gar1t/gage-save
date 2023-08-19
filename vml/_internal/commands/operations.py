# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

from ..._vendor import click

from .. import click_util


# def _ac_operation(ctx, _param, incomplete):
#     from guild import cmd_impl_support
#     from . import operations_impl

#     cmd_impl_support.init_model_path()
#     ops = operations_impl.filtered_ops(click_util.Args(**ctx.params))
#     return sorted(
#         [op["fullname"] for op in ops if op["fullname"].startswith(incomplete)]
#     )


@click.command(name="operations, ops")
@click.argument(
    "filters",
    metavar="[FILTER]...",
    required=False,
    nargs=-1,
    # shell_complete=_ac_operation,
)
@click_util.use_args
def operations(args: Any):
    """Show available operations.

    Use one or more `FILTER` arguments to show only operations with
    names or models that match the specified values.
    """
    from . import operations_impl

    operations_impl.main(args)
