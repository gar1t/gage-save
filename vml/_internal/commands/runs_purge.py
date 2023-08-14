# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

from ..._vendor import click

from .. import click_util

from . import remote_support
from . import runs_support


@click.command("purge")
@runs_support.runs_arg
@runs_support.all_filters
@remote_support.remote_option("Permanently delete remote runs.")
@click.option("-y", "--yes", help="Do not prompt before purging.", is_flag=True)
@click.pass_context
@click_util.use_args
@click_util.render_doc
def purge_runs(ctx: click.Context, args: Any):
    """Permanentaly delete one or more deleted runs.

    **WARNING**: Purged runs cannot be recovered!

    Runs are purged (i.e. permanently deleted) by specifying `RUN` arguments. If
    a `RUN` argument is not specified, all runs matching the filter criteria are
    purged. See SPECIFYING RUNS and FILTERING topics for more information on how
    runs are selected.

    Use ``guild runs list --deleted`` for a list of runs that can be purged.

    By default, Guild will display the list of runs to be purged and ask you to
    confirm the operation. If you want to purge the runs without being prompted,
    use the ``--yes`` option.

    **WARNING**: Take care when purging runs using indexes as the runs selected
    with indexes can change. Review the list of runs carefully before confirming
    a purge operation.

    {{ runs_support.runs_arg }}

    If a `RUN` argument is not specified, ``:`` is assumed (all runs are
    selected).

    {{ runs_support.all_filters }}

    ### Permanently Delete Remote Runs

    If a run has been deleted remotely, you can permanently delete it using
    `--remote` provided the remote type supports deleted run recovery.

    {{ remote_support.remote_option }}
    """
    print("TODO purge runs")

    # from . import runs_impl

    # runs_impl.purge_runs(args, ctx)
