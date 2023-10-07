# SPDX-License-Identifier: Apache-2.0

from typing import *

from ..types import *


class Args(NamedTuple):
    runs: list[str]
    msg: str
    delete: str
    edit: str
    list: bool
    where: str
    all: bool
    yes: bool


def comment(args: Args):
    pass
