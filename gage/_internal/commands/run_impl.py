# SPDX-License-Identifier: Apache-2.0

from typing import *
from ..types import *

import os

from .. import cli
from .. import run_sourcecode

from ..sys_config import runs_home

from ..run_context import resolve_run_context

from ..run_util import *

from . import error_handlers

__all__ = ["Args", "run"]


class Args(NamedTuple):
    opspec: str
    stage: bool
    preview_sourcecode: bool
    preview_all: bool
    json: bool


def run(args: Args):
    try:
        ctx = resolve_run_context(args.opspec)
    except GageFileError as e:
        error_handlers.gagefile_error(e)
    except OpDefNotFound as e:
        error_handlers.opdef_not_found(e)
    else:
        _handle_run_context(ctx, args)


def _handle_run_context(ctx: RunContext, args: Args):
    if _preview_opts(args):
        _preview(ctx, args)
    elif args.stage:
        _stage(ctx, args)
    else:
        _run(ctx, args)


# =================================================================
# Preview
# =================================================================


def _preview_opts(args: Args):
    return args.preview_sourcecode or args.preview_all


def _preview(ctx: RunContext, args: Args):
    previews = _init_previews(ctx.opdef, args)
    if args.json:
        cli.out(
            cli.json({name: as_json() for name, as_renderable, as_json in previews})
        )
    else:
        cli.out(
            cli.Group(*(as_renderable() for name, as_renderable, as_json in previews))
        )


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
# Stage and run
# =================================================================


def _stage(ctx: RunContext, args: Args):
    run = make_run(ctx.opref, runs_home())
    config = _run_config(args)
    cmd = _op_cmd(ctx, config)
    user_attrs = {}
    sys_attrs = {}
    init_run_meta(run, ctx.opdef, config, cmd, user_attrs, sys_attrs)
    stage_run(run, ctx.project_dir)
    return run


def _run_config(args: Args):
    return cast(RunConfig, {})


def _op_cmd(ctx: RunContext, config: RunConfig):
    cmd_args = ctx.opdef.get_exec().get_run()
    if not cmd_args:
        error_handlers.missing_exec_error(ctx)
    env = {}
    return OpCmd(cmd_args, env)


def _run(ctx: RunContext, args: Args):
    run = _stage(ctx, args)
    p = start_run(run)
    output = open_run_output(run, p)
    exit_code = p.wait()
    output.wait_and_close()
    finalize_run(run, exit_code)
