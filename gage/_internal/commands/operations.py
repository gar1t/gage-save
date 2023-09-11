# SPDX-License-Identifier: Apache-2.0

from typing import *


def operations():
    """Show available operations.

    Operations are defined in a project Gage file, which may exist in
    the current directory or parent directories. If a project Gage file
    doesn't exist, you can still run scripts directly but these will not
    appear as operations show by this command.

    For more information on Gage files, run 'gage help gagefile'.

    To locate the current Gage file, run `gage check -v`.
    """

    from .operations_impl import operations

    operations()
