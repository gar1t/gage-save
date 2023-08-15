# SPDX-License-Identifier: Apache-2.0

from typing import *

from .. import click_util

from ..._vendor import click

from .check import check
from .help import help
from .run import run
from .runs import runs


@click.group(cls=click_util.Group)
def main():
    pass


main.add_command(check)
main.add_command(help)
main.add_command(run)
main.add_command(runs)
