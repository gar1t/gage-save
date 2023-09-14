# SPDX-License-Identifier: Apache-2.0

from typing import *

from ..types import *

from .. import cli
from .. import config
from .. import gagefile


def operations():
    try:
        table = operations_table()
    except FileNotFoundError:
        cli.exit_with_error("No operations defined for the current project")
    else:
        cli.out(table)


def operations_table():
    gf = gagefile.gagefile_for_dir(config.cwd())
    table = cli.Table(header=["operation", "description"])
    for name, opdef in sorted(gf.operations.items()):
        table.add_row(cli.label(name), _opdef_desc(opdef))
    return table


def _opdef_desc(opdef: OpDef):
    if not opdef.description:
        return ""
    return (
        f"{opdef.description} [dim](default)[/dim]"
        if opdef.default
        else opdef.description
    )
