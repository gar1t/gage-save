# SPDX-License-Identifier: Apache-2.0

from typing import *

import os

from ...__init__ import __version__

from .. import cli
from .. import config

class Args(NamedTuple):
    version: bool
    cwd: str


def main(args: Args):
    if args.version:
        cli.out(f"gage {__version__}")
        raise SystemExit(0)
    if args.cwd:
        _apply_cwd(args.cwd)


def _apply_cwd(cwd: str):
    config.set_cwd(_validated_dir(cwd))


def _validated_dir(path: str):
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        raise SystemExit(f"directory '{path}' does not exist")
    if not os.path.isdir(path):
        raise SystemExit(f"'{path}' is not a directory")
    return path
