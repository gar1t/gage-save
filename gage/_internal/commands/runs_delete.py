# SPDX-License-Identifier: Apache-2.0

from typing import *

import click

from .. import click_util

from . import runs_support


@click.command("delete, rm")
@runs_support.runs_arg
@runs_support.archive_option("Delete archived runs in PATH.")
@runs_support.all_filters
@click.option("-y", "--yes", help="Do not prompt before deleting.", is_flag=True)
@click.option(
    "-p",
    "--permanent",
    help="Permanently delete runs so they cannot be recovered.",
    is_flag=True,
)
@click.pass_context
@click_util.use_args
@click_util.render_doc
def delete_runs(ctx: click.Context, args: Any):
    """Delete one or more runs.

    Runs are deleting by specifying `RUN` arguments. If a `RUN` argument is not
    specified, all runs matching the filter criteria are deleted. See SPECIFYING
    RUNS and FILTERING topics for more information on how runs are selected.

    By default, Guild will display the list of runs to be deleted and ask you to
    confirm the operation. If you want to delete the runs without being
    prompted, use the ``--yes`` option.

    **WARNING**: Take care when deleting runs using indexes as the runs selected
    with indexes can change. Review the list of runs carefully before confirming
    a delete operation.

    If a run is still running, Guild will stop it first before deleting it.

    If you delete a run by mistake, provided you didn't use the ``--permanent``
    option, you can restore it using ``guild runs restore``.

    If you want to permanently delete runs, use the ``--permanent`` option.

    **WARNING**: Permanently deleted runs cannot be restored.

    {{ runs_support.runs_arg }}

    If a `RUN` argument is not specified, ``:`` is assumed (all runs are
    selected).

    {{ runs_support.all_filters }}
    """
    print("TODO: delete runs")

    # from . import runs_impl

    # with click_util.CmdContext("guild.runs.delete", args, ctx):
    #     runs_impl.delete_runs(args, ctx)
