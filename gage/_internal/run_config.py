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


class RunConfig(dict[str, RunConfigValue]):
    def render(self) -> str:
        raise NotImplementedError()
