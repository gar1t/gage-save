# SPDX-License-Identifier: Apache-2.0

from typing import *

from ..types import *

from .. import cli
from .. import run_sourcecode

from ..opdef_util import opdef_for_spec


class Args(NamedTuple):
    operation: str
    preview_sourcecode: bool
    preview_all: bool


def run(args: Args):
    try:
        opdef = opdef_for_spec(args.operation)
    except OpDefNotFound as e:
        _opdef_not_found_error(e)
    else:
        _handle_opdef(opdef, args)


def _handle_opdef(opdef: OpDef, args: Args):
    if _preview_opts(args):
        _preview_and_exit(opdef, args)
    else:
        print(f"TODO: run {opdef.name}")


# =================================================================
# Preview
# =================================================================

def _preview_opts(args: Args):
    return args.preview_sourcecode or args.preview_all


def _preview_and_exit(opdef: OpDef, args: Args) -> NoReturn:
    if args.preview_sourcecode or args.preview_all:
        _preview_sourcecode(opdef)
    if args.preview_all:
        _preview_config(opdef, args)
        _preview_deps(opdef)
        _preview_runtime_init(opdef)
        _preview_run_exec(opdef)
        _preview_run_finalize(opdef)
    raise SystemExit(0)


def _preview_sourcecode(opdef: OpDef):
    sourcecode = run_sourcecode.init(opdef)
    cli.out(run_sourcecode.preview(sourcecode))


def _preview_config(opdef: OpDef, args: Args):
    cli.out("TODO: preview config")


def _preview_deps(opdef: OpDef):
    cli.out("TODO: preview deps")


def _preview_runtime_init(opdef: OpDef):
    cli.out("TODO: preview runtime init")


def _preview_run_exec(opdef: OpDef):
    cli.out("TODO: preview run exec")


def _preview_run_finalize(opdef: OpDef):
    cli.out("TODO: preview finalize")


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
