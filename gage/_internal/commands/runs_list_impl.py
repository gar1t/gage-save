# SPDX-License-Identifier: Apache-2.0

from typing import *

from ..types import *


from . import impl_support


def filtered_runs(args: Any):
    return cast(list[Run], [])


def list_runs(args: Any):
    _check_list_runs_args(args)
    runs = filtered_runs(args)


def _check_list_runs_args(args: Any):
    impl_support.check_incompatible_args(
        [
            ("json", "verbose"),
            ("archive", "deleted"),
            ("all", "limit"),
        ],
        args,
    )
