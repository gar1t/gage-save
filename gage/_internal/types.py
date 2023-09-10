# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

from jschon import JSONCompatible

Data = dict[str, Any]


class OpDefNotFound(Exception):
    pass


class OpError(Exception):
    pass


class OpRef:
    def __init__(self, op_ns: str, op_name: str):
        self.op_ns = op_ns
        self.op_name = op_name


class OpCmd:
    def __init__(self, args: list[str], env: dict[str, str]):
        self.args = args
        self.env = env


class OpDef:
    def __init__(self, name: str, data: Data):
        self.name = name
        self._data = data

    def as_json(self) -> JSONCompatible:
        return self._data

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


RunStatus = Literal["unknown", "foobar"]  # TODO!


class Op:
    def __init__(self):
        self.opdef: Optional[OpDef] = None
