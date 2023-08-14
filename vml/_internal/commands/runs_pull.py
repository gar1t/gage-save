# SPDX-License-Identifier: Apache-2.0

from typing import *

from vml._vendor import click

from vml._internal import click_util

from . import remote_support
from . import runs_support


def pull_params(fn: Callable[..., Any]):
    click_util.append_params(
        fn,
        [
            remote_support.remote_arg,
            runs_support.runs_arg,
            runs_support.all_filters,
            click.Option(
                ("-d", "--delete"),
                help="Delete local files missing on remote.",
                is_flag=True,
            ),
            click.Option(
                ("-y", "--yes"), help="Do not prompt before copying.", is_flag=True
            ),
        ],
    )
    return fn


@click.command("pull")
@pull_params
@click.pass_context
@click_util.use_args
@click_util.render_doc
def pull_runs(ctx: click.Context, args: Any):
    """Copy one or more runs from a remote location.

    `RUN` must be the complete run ID of the remote run.

    **NOTE:** Guild does not currently support listing remote runs. To pull
    specific runs, query the remote server for the full run ID of each run you
    want to pull.

    You may alternatively use `--all` to pull all remote runs. If `--all` is
    specified, `RUN` arguments cannot be specified.

    `--verbose` is always enabled when `--all` is specified.

    `REMOTE` must be define in ``~/.guild/config.yml``. See REMOTES below for
    more information.

    By default Guild will prompt you before copying. If you want to apply the
    changes without being prompted, use the ``--yes`` option.

    {{ runs_support.runs_arg }}

    {{ runs_support.all_filters }}

    {{ remote_support.remotes }}
    """
    print("TODO pull runs")

    # from . import runs_impl

    # runs_impl.pull(args, ctx)
