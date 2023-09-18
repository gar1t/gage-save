# SPDX-License-Identifier: Apache-2.0

from typing import *

__all__ = ["RunConfig", "RunConfigValue"]

RunConfigValue = (
    None
    | int
    | float
    | bool
    | str
    | list['RunConfigValue']
    | dict[str, 'RunConfigValue']
)


class RunConfig(MutableMapping):
    _initialized = False

    def __init__(self):
        self._data: dict[str, RunConfigValue] = {}

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key: str):
        return self._data[key]

    def __setitem__(self, key: str, item: RunConfigValue):
        if self._initialized and key not in self._data:
            raise ValueError(f"key does not exist: {key!r}")
        self._data[key] = item

    def __delitem__(self, key: str):
        del self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __contains__(self, key: str):
        return key in self._data

    def __repr__(self):
        return repr(self._data)

    def __copy__(self):
        inst = self.__class__.__new__(self.__class__)
        inst.__dict__.update(self.__dict__)
        inst.__dict__["_data"] = self.__dict__["_data"].copy()
        return inst

    def apply(self) -> str:
        """Applies config returning the new source."""
        raise NotImplementedError()
