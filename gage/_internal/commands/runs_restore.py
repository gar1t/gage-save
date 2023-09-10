# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

import click

from .. import click_util

from . import runs_support


@click.command("restore")
@runs_support.runs_arg
@runs_support.all_filters
@click.option("-y", "--yes", help="Do not prompt before restoring.", is_flag=True)
@click.pass_context
@click_util.use_args
@click_util.render_doc
def restore_runs(ctx: click.Context, args: Any):
    """Restore one or more deleted runs.

    Runs are restored using `RUN` arguments. If a `RUN` argument is not
    specified, all runs matching the filter criteria are restored. See
    SPECIFYING RUNS and FILTERING topics for more information.

    Use ``guild runs list --deleted`` for a list of runs that can be restored.

    By default, Guild will display the list of runs to be restored and ask you
    to confirm the operation. If you want to restore the runs without being
    prompted, use the ``--yes`` option.

    {{ runs_support.runs_arg }}

    If a `RUN` argument is not specified, ``:`` is assumed (all runs are
    selected).

    {{ runs_support.all_filters }}
    """
    print("TODO")

    # from . import runs_impl

    # runs_impl.restore_runs(args, ctx)
