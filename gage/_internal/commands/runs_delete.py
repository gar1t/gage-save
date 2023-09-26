# SPDX-License-Identifier: Apache-2.0

from typing import *

from .command_types import *

__all__ = ["runs_delete"]


def runs_delete(
    where: RunsWhere = "",
    first: RunsFirst = 20,
):
    """Delete runs."""
    from .runs_delete_impl import runs_delete, Args

    args = Args(
        where=where,
        first=first,
    )
    runs_delete(args)
