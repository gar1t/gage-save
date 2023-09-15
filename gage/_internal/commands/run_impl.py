# SPDX-License-Identifier: Apache-2.0

from typing import *

import os

from ..types import *

from .. import cli
from .. import run_sourcecode

from ..opdef_util import opdef_for_spec


class Args(NamedTuple):
    operation: str
    preview_sourcecode: bool
    preview_all: bool
    json: bool


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
    previews = _init_previews(opdef, args)
    if args.json:
        cli.out(
            cli.json({name: as_json() for name, as_renderable, as_json in previews})
        )
    else:
        cli.out(
            cli.Group(*(as_renderable() for name, as_renderable, as_json in previews))
        )
    raise SystemExit(0)


class Preview(NamedTuple):
    name: str
    as_renderable: Callable[[], Any]
    as_json: Callable[[], Any]


def _init_previews(opdef: OpDef, args: Args):
    previews: list[Preview] = []
    if args.preview_sourcecode or args.preview_all:
        previews.append(_init_sourcecode_preview(opdef))
    # TODO: other previews
    return previews


def _init_sourcecode_preview(opdef: OpDef):
    project_dir = os.path.dirname(opdef.get_src())
    sourcecode = run_sourcecode.init(project_dir, opdef)
    return Preview(
        "sourcecode",
        lambda: run_sourcecode.preview(sourcecode),
        lambda: sourcecode.as_json(),
    )


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
