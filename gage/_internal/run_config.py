# SPDX-License-Identifier: Apache-2.0

from typing import *

from .types import RunConfig
from .types import RunConfigValue

__all__ = ["RunConfig", "RunConfigValue", "RunConfigBase"]


class RunConfigBase(RunConfig):
    _initialized = False

    def __setitem__(self, key: str, item: RunConfigValue):
        if self._initialized and key not in self:
            raise ValueError(f"key does not exist: {key!r}")
        super().__setitem__(key, item)

    def apply(self) -> str:
        """Applies config returning the new source."""
        raise NotImplementedError()


def read_config(src_dir: str):
    pass
