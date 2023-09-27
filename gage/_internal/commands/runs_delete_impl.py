# SPDX-License-Identifier: Apache-2.0

from typing import *

__all__ = ["Args", "runs_delete"]


class Args(NamedTuple):
    runs: list[str] | None
    where: str


def runs_delete(args: Args):
    print("TODO: Delete ze runs")
