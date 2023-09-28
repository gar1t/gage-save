# SPDX-License-Identifier: Apache-2.0

from typing import *


class Args(NamedTuple):
    runspec: str


def show(args: Args):
    print("Show")
