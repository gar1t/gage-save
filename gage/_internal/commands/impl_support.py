# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

from .. import cli
from .. import click_util

ArgSpec = Union[str, Tuple[str, str]]


def check_incompatible_args(incompatible: List[Tuple[ArgSpec, ArgSpec]], args: Any):
    for val in incompatible:
        arg1_name, opt1, arg2_name, opt2 = _incompatible_arg_items(val)
        if getattr(args, arg1_name, None) and getattr(args, arg2_name):
            cli.error(
                f"{opt1} and {opt2} cannot both be specified\nTry"
                f" '{click_util.context().command_path} --help' for more information."
            )


def _incompatible_arg_items(val: Tuple[ArgSpec, ArgSpec]):
    arg1, arg2 = val
    arg1, opt1 = _arg_parts(arg1)
    arg2, opt2 = _arg_parts(arg2)
    return arg1, opt1, arg2, opt2


def _arg_parts(part: ArgSpec):
    if isinstance(part, tuple):
        assert len(part) == 2, part
        return part
    assert isinstance(part, str)
    return part, "--" + part.replace("_", "-")
