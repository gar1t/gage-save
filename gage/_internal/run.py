# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

import os


class Run:
    __properties__ = ["id"]

    def __init__(self, run_id: str, run_base: str):
        self.id = run_id
        self.run_base = run_base
        self.run_dir = run_base + ".run"
        self.meta_dir = run_base + ".meta"
        self.attrs_dir = run_meta_path(self, "attrs")
        self.user_dir = run_base + ".user"

    def read_attr(self, name: str):
        return None


def run_meta_path(run: Run, *parts: str):
    return os.path.join(run.meta_dir, *parts)
