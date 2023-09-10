# SPDX-License-Identifier: Apache-2.0

from typing import *

import os

from .. import config
from .. import cli


def main(cwd: str | None):
    if cwd:
        _apply_cwd(cwd)


def _apply_cwd(cwd: str):
    config.set_cwd(_validated_dir(cwd))


def _validated_dir(path: str):
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        cli.error(f"directory '{path}' does not exist")
    if not os.path.isdir(path):
        cli.error(f"'{path}' is not a directory")
    return path
