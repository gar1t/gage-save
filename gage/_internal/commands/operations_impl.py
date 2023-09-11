# SPDX-License-Identifier: Apache-2.0

from typing import *

from .. import config
from .. import gagefile


def main(args: Any):
    try:
        gf = gagefile.for_dir(config.cwd())
    except FileNotFoundError:
        raise SystemExit("No operations defined for the current project")
    else:
        data = [
            {"name": name, "desc": opdef.description}
            for name, opdef in sorted(gf.operations.items())
        ]
        assert False, "TODO"
        ##cli.table(data, ["name", "desc"])
