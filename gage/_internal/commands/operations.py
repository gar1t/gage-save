# SPDX-License-Identifier: Apache-2.0

from typing import *

import click

from .. import click_util


@click.command(name="operations, ops")
@click_util.use_args
def operations(args: Any):
    """Show available operations."""
    from . import operations_impl

    operations_impl.main(args)
