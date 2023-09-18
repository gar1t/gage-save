# SPDX-License-Identifier: Apache-2.0

from typing import *

Data = dict[str, Any]

# NO IMPORTS ALLOWED


class OpDefNotFound(Exception):
    def __init__(self, spec: str | None):
        self.spec = spec


class OpError(Exception):
    pass


class OpRef:
    def __init__(self, op_ns: str, op_name: str):
        self.op_ns = op_ns
        self.op_name = op_name

    def get_full_name(self):
        if not self.op_ns:
            return self.op_name
        return f"{self.op_ns}:{self.op_name}"


class OpCmd:
    def __init__(self, args: list[str], env: dict[str, str]):
        self.args = args
        self.env = env


class OpDef:
    def __init__(self, name: str, data: Data, src: str | None = None):
        self.name = name
        self._data = data
        self.src = src

    def as_json(self) -> Data:
        return self._data

    def get_src(self):
        if self.src is None:
            raise TypeError(
                "OpDef was not created with src - read src attribute "
                "directly to bypass this check"
            )
        return self.src

    def get_description(self) -> Optional[str]:
        return self._data.get("description")

    def get_default(self):
        return bool(self._data.get("default"))

    def get_exec(self):
        val = self._data.get("exec")
        if val is None:
            return None
        if isinstance(val, str):
            return val
        return OpDefExec(self, val)

    def get_sourcecode(self):
        return OpDefSourceCode(self, self._data.get("sourcecode") or {})


class OpDefExec:
    def __init__(self, opdef: OpDef, data: Data):
        self.opdef = opdef
        self._data = data

    def get_copy_sourcecode(self) -> str | None:
        return self._data.get("copy-sourcecode")

    def get_copy_deps(self) -> str | None:
        return self._data.get("copy-deps")

    def get_init_runtime(self) -> str | None:
        return self._data.get("init-runtime")

    def get_run(self) -> str | None:
        return self._data.get("run")

    def get_finalize_run(self) -> str | None:
        return self._data.get("finalize-run")


class OpDefSourceCode:
    def __init__(self, opdef: OpDef, data: Data):
        self.opdef = opdef
        self._data = data

    def as_json(self) -> Data:
        return self._data

    def get_include(self) -> list[str] | None:
        return _path_patterns(self._data.get("include"))

    def get_exclude(self) -> list[str] | None:
        return _path_patterns(self._data.get("exclude"))


def _path_patterns(data: Any) -> list[str] | None:
    if data is None:
        return None
    if isinstance(data, str):
        return [data]
    return data


class GageFile:
    def __init__(self, filename: str, data: Data):
        self.filename = filename
        self._data = data

    def get_operations(self):
        return {
            name: OpDef(name, self._data[name], self.filename)  # \
            for name in self._data
        }


class Run:
    def __init__(self, run_id: str, run_dir: str, name: str):
        self.id = run_id
        self.run_dir = run_dir
        self.name = name


RunStatus = Literal["unknown", "foobar"]  # TODO!


RunConfigValue = (
    None
    | int
    | float
    | bool
    | str
    | list['RunConfigValue']
    | dict[str, 'RunConfigValue']
)

RunConfig = dict[str, RunConfigValue]
