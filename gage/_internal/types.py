# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

Data = Dict[str, Any]


class OpDef:
    def __init__(self, name: str, data: Data):
        self._name = name
        self._data = data

    @property
    def name(self):
        return self._name

    @property
    def description(self) -> Optional[str]:
        return self._data.get("description")

    @property
    def default(self):
        return bool(self._data.get("default"))


class GageFile:
    def __init__(self, filename: str, data: Data):
        self._filename = filename
        self._data = data

    @property
    def operations(self):
        return {name: OpDef(name, self._data[name]) for name in self._data}
