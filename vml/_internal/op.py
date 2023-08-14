# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

from .opdef import OpDef

class Op:
    def __init__(self):
        self.opdef: Optional[OpDef] = None
