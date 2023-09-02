# SPDX-License-Identifier: Apache-2.0

from typing import *

import pkgutil


def iter_plugins():
    from gage import __pkgdir__
    import os

    for name in sorted(
        [m.name for m in pkgutil.iter_modules([os.path.join(__pkgdir__, "_internal")])]
    ):
        print(name)
