# SPDX-License-Identifier: Apache-2.0

from typing import *

__all__ = [
    "GageFile",
    "OpCmd",
    "OpDef",
    "OpDefNotFound",
    "OpRef",
    "OpDefExec",
    "OpDefConfig",
    "Run",
    "RunConfig",
    "RunConfigValue",
    "RunStatus",
    "UnifiedDiff",
]

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


class OpDefExec:
    def __init__(self, data: Data):
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


class OpDefConfig:
    def __init__(self, data: Data):
        self._data = data

    def get_name(self) -> str | None:
        return self._data.get("name")

    def get_description(self) -> str | None:
        return self._data.get("description")

    def get_paths(self) -> list[str]:
        # Expect path or paths
        try:
            return [self._data["path"]]
        except KeyError:
            return self._data.get("paths") or []


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

    def get_exec(self) -> OpDefExec:
        val = self._data.get("exec")
        if val is None:
            val = {}
        elif isinstance(val, str) or isinstance(val, list):
            val = {"run": val}
        return OpDefExec(val)

    def get_sourcecode(self) -> list[str] | bool | None:
        val = self._data.get("sourcecode")
        if val in (True, False, None):
            return val
        return _path_patterns(val)

    def get_config(self) -> list[OpDefConfig]:
        val = self._data.get("config")
        if val is None:
            val = []
        elif isinstance(val, dict):
            val = [val]
        return [OpDefConfig(item) for item in val]


def _path_patterns(data: Any) -> list[str]:
    if data is None:
        data = []
    elif isinstance(data, str):
        data = [data]
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


RunConfigValue = None | int | float | bool | str


class RunConfig(dict[str, RunConfigValue]):
    _initialized = False

    def __setitem__(self, key: str, item: RunConfigValue):
        if self._initialized and key not in self:
            raise KeyError(key)
        super().__setitem__(key, item)

    def apply(self) -> str:
        """Applies config returning the new source."""
        raise NotImplementedError()


UnifiedDiff = list[str]
