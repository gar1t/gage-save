# SPDX-License-Identifier: Apache-2.0

from typing import *


def check(version: str = ""):
    """Check Gage ML.

    Shows version and configuration details.
    """
    from .check_impl import check

    check(version)
