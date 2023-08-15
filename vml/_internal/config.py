# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

import os

__var_home: Optional[str] = None


def cwd():
    return os.getcwd()


def var_home():
    return __var_home or os.path.expanduser("~/.vistaml")


def set_var_home(path: str):
    globals()["__var_home"] = path


def runs_home(deleted: bool = False):
    if deleted:
        return os.path.join(var_home(), "trash", "runs")
    return os.path.join(var_home(), "runs")
