from __future__ import annotations

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
            {"name": name, "desc": opdef.get("description", "")}
            for name, opdef in gagefile.operations(gf)
        ]
        cli.table(data, ["name", "desc"])
