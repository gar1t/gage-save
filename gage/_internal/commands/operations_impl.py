# SPDX-License-Identifier: Apache-2.0

from typing import *

from .. import cli
from .. import config
from .. import gagefile


def main(args: Any):
    try:
        gf = gagefile.for_dir(config.cwd())
    except FileNotFoundError:
        cli.error("No operations defined for the current project")
    else:
        data = [
            {"name": name, "desc": opdef.description}
            for name, opdef in sorted(gf.operations.items())
        ]
        cli.table(data, ["name", "desc"])
