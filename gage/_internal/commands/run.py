# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

import click

from .. import click_util


@click.command
@click.argument(
    "opspec",
    metavar="OPERATION",
    required=False,
)
@click.option(
    "--stage",
    help="Stage a run.",
    is_flag=True,
)
@click.option(
    "-y",
    "--yes",
    help="Do not prompt before running operation.",
    is_flag=True,
)
@click.option(
    "--help-op",
    help="Show operation help and exit.",
    is_flag=True,
)
@click.option(
    "--test-opdef",
    help="Show how the operation def is generated and exit.",
    is_flag=True,
)
@click.option(
    "--test-sourcecode",
    help="Test operation source code selection and exit.",
    is_flag=True,
)
@click.option(
    "--test-output",
    help="Test operation output and exit.",
    is_flag=True,
)
@click.option("--test-prompt", hidden=True, is_flag=True)
@click_util.use_args
@click_util.render_doc
def run(args: Any):
    """Start a run."""
    from .run_impl import main

    main(args)
