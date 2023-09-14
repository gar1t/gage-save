# SPDX-License-Identifier: Apache-2.0

from typing import *

from ..types import *

from .. import cli

from ..opdef_util import opdef_for_spec


class Args(NamedTuple):
    operation: str
    preview: bool


def run(args: Args):
    try:
        opdef = opdef_for_spec(args.operation)
    except OpDefNotFound as e:
        _opdef_not_found_error(e)
    else:
        _handle_opdef(opdef, args)


def _handle_opdef(opdef: OpDef, args: Args):
    if args.preview:
        _preview_run(opdef, args)
    else:
        print(f"TODO: run {opdef.name}")


def _preview_run(opdef: OpDef, args: Args):
    print(f"TODO: preview {opdef.name}")


# =================================================================
# Errors
# =================================================================


def _opdef_not_found_error(e: OpDefNotFound):
    from .operations_impl import operations_table

    msg = (
        e.spec
        and f"Cannot find operation '{e.spec}'"
        or "Cannot find a default operation"
    )
    cli.error_message(msg)
    try:
        ops = operations_table()
    except FileNotFoundError:
        cli.err(
            "\nTo define operations, create a Gage file. For help, "
            "run 'gage help gagefile'."
        )
    else:
        cli.err("\nOperations defined for this project:\n")
        cli.err(ops)
    raise SystemExit()
