# SPDX-License-Identifier: Apache-2.0

from typing import *

from .command_types import *

__all__ = ["runs_list"]


def runs_list(
    where: RunsWhere = "",
    first: RunsFirst = 20,
):
    """List runs."""
    from .runs_list_impl import runs_list, Args

    args = Args(
        where=where,
        first=first,
    )
    runs_list(args)
