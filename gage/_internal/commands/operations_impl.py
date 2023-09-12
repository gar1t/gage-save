# SPDX-License-Identifier: Apache-2.0

from typing import *

from ..types import GageFile

from .. import cli
from .. import config
from .. import gagefile


def operations():
    try:
        gf = gagefile.gagefile_for_dir(config.cwd())
    except FileNotFoundError:
        raise SystemExit("No operations defined for the current project")
    else:
        _print_operations(gf)


def _print_operations(gf: GageFile):
    table = cli.Table(header=["operation", "description"])
    for name, opdef in sorted(gf.operations.items()):
        table.add_row(cli.label(name), opdef.description)
    cli.out(table)
