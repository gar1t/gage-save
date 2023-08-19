# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

class Project:

    def __init__(self, data: object, source: str):
        self.data = data
        self.src = source
