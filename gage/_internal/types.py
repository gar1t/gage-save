# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

Data = Dict[str, Any]


class OpDefNotFound(Exception):
    pass


class OpError(Exception):
    pass


class OpDef:
    def __init__(self, name: str, data: Data):
        self.name = name
        self._data = data

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


class Run:
    def __init__(self, run_id: str, run_dir: str):
        self.id = run_id
        self.run_dir = run_dir


RunStatus = Union[
    Literal["unknown"],
    Literal["foobar"],
]


class Op:
    def __init__(self):
        self.opdef: Optional[OpDef] = None
