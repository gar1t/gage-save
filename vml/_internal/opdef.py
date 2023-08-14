# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *


class OpDef:
    def __init__(self, name: str):
        self.name = name


class Flag:
    pass


def opdef_to_opspec(opdef: OpDef, cwd: Optional[str] = None):
    return opdef.name
