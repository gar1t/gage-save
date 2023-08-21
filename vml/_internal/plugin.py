# SPDX-License-Identifier: Apache-2.0

from typing import *

from .opdef import OpDefNotFound


def plugin_opdef_for_opspec(opspec: Optional[str], cwd: Optional[str]):
    raise OpDefNotFound(opspec)
