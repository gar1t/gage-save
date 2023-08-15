# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

from .run import Run


class Manifest:
    def __init__(self, run: Run):
        self.run = run

    def __enter__(self):
        return self

    def __exit__(*exc: Any):
        pass
