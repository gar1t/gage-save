# SPDX-License-Identifier: Apache-2.0

from typing import *

from vml._vendor import click

from vml._internal import click_util


@click.command
@click.argument(
    "opspec",
    metavar="OPERATION",
    required=False,
    # shell_complete=_ac_opspec,
)
@click.option(
    "-y",
    "--yes",
    help="Do not prompt before running operation.",
    is_flag=True,
)
@click_util.use_args
@click_util.render_doc
def run(args: Any):
    """Start a run.
    """
    from .run_impl import main

    main(args)
