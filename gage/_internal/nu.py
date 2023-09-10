# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

NuList: TypeAlias = "list[NuValue]"
NuRecord: TypeAlias = "dict[str, NuValue]"
NuTable = list[NuRecord]
NuValue = Union[None, str, int, float, NuList, NuTable, NuRecord]


def table(data: NuTable, cols: list[str]):
    pass
