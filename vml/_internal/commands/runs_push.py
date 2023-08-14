# SPDX-License-Identifier: Apache-2.0

from typing import *

from vml._vendor import click

from vml._internal import click_util

from . import remote_support
from . import runs_support


def push_params(fn: Callable[..., Any]):
    click_util.append_params(
        fn,
        [
            remote_support.remote_arg,
            runs_support.runs_arg,
            runs_support.all_filters,
            click.Option(
                ("-n", "--delete"),
                help="Delete remote files missing locally.",
                is_flag=True,
            ),
            click.Option(
                ("-y", "--yes"), help="Do not prompt before copying.", is_flag=True
            ),
        ],
    )
    # _set_remote_ac_local_runs(fn)
    return fn


# def _set_remote_ac_local_runs(fn):
#     assert fn.__click_params__[-2].name == "runs", fn.__click_params__
#     fn.__click_params__[-2].shell_complete = runs_support.ac_local_run


@click.command("push")
@push_params
@click.pass_context
@click_util.use_args
@click_util.render_doc
def push_runs(ctx: click.Context, args: Any):
    """Copy one or more runs to a remote location.

    `REMOTE` must be define in ``~/.guild/config.yml``. See REMOTES below for
    more information.

    By default Guild will prompt you before copying. If you want to apply the
    changes without being prompted, use the ``--yes`` option.

    {{ runs_support.runs_arg }}

    If a `RUN` argument is not specified, ``:`` is assumed (all runs are
    selected).

    {{ runs_support.all_filters }}

    {{ remote_support.remotes }}
    """
    print("TODO")

    # from . import runs_impl

    # runs_impl.push(args, ctx)
