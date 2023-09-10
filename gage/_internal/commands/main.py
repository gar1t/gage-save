# SPDX-License-Identifier: Apache-2.0

from typing import *

from .. import click_util

import click

from ...__init__ import __version__

from . import ac_support

from .check import check
from .help import help
from .operations import operations
from .run import run
from .runs import runs


@click.group(cls=click_util.Group)
@click.version_option(
    version=__version__,
    prog_name="gage",
    message="%(prog)s %(version)s",
)
@click.option(
    "-C",
    "cwd",
    metavar="PATH",
    help="Use PATH as current directory for a command.",
    default=None,
    shell_complete=ac_support.ac_dir(),
)
@click_util.use_args
def main(args: Any):
    from . import main_impl

    main_impl.main(args)


main.add_command(check)
main.add_command(help)
main.add_command(operations)
main.add_command(run)
main.add_command(runs)
