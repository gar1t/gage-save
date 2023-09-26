# SPDX-License-Identifier: Apache-2.0

from typing import *

__all__ = ["Args", "runs_delete"]


class Args(NamedTuple):
    where: str
    first: int


def runs_delete(args: Args):
    print("TODO: Delete ze runs")
