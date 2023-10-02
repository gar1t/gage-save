# SPDX-License-Identifier: Apache-2.0

from typing import *

from ..types import *

import logging
import os
import platform

from rich.console import Console

from .. import cli
from .. import run_output
from .. import run_sourcecode

from ..sys_config import runs_home

from ..run_context import resolve_run_context

from ..run_util import *

from . import error_handlers

__all__ = ["Args", "run"]

log = logging.getLogger(__name__)


class Args(NamedTuple):
    opspec: str
    flags: list[str] | None
    label: str
    stage: bool
    quiet: bool
    yes: bool
    preview_sourcecode: bool
    preview_all: bool
    json: bool


def run(args: Args):
    try:
        context = resolve_run_context(args.opspec)
    except GageFileError as e:
        error_handlers.gagefile_error(e)
    except OpDefNotFound as e:
        error_handlers.opdef_not_found(e)
    else:
        _handle_run_context(context, args)


def _handle_run_context(context: RunContext, args: Args):
    if _preview_opts(args):
        _preview(context, args)
    elif args.stage:
        _stage(context, args)
    else:
        _run(context, args)


# =================================================================
# Preview
# =================================================================


def _preview_opts(args: Args):
    return args.preview_sourcecode or args.preview_all


def _preview(context: RunContext, args: Args):
    previews = _init_previews(context.opdef, args)
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


def _stage(context: RunContext, args: Args):
    run = make_run(context.opref, runs_home())
    config = _run_config(args)
    _maybe_prompt(args, run, config)
    cmd = _op_cmd(context, config)
    user_attrs = _user_attrs(args)
    sys_attrs = _sys_attrs()
    init_run_meta(run, context.opdef, config, cmd, user_attrs, sys_attrs)
    with _RunPhaseStatus(args):
        stage_run(run, context.project_dir)
    return run


class _RunPhaseStatus:
    phase_desc = {
        "stage-sourcecode": "Staging source code",
        "stage-config": "Applying configuration",
        "stage-runtime": "Staging runtime",
        "stage-dependencies": "Staging dependencies",
        "finalize": "Finalizing run",
    }

    def __init__(self, args: Args):
        self._status = cli.status("", args.quiet)

    def __enter__(self):
        self._status.start()
        run_phase_channel.add(self)

    def __exit__(self, *exc: Any):
        self._status.stop()
        run_phase_channel.remove(self)

    def __call__(self, name: str, arg: Any | None = None):
        if name == "exec-output":
            assert isinstance(arg, tuple), arg
            phase_name, stream, output = arg
            self._status.console.out(output.decode(), end="")
        else:
            desc = self.phase_desc.get(name)
            if desc:
                self._status.update(f"[dim]{desc}")
            else:
                log.debug("Unexpected run phase callback: %r %r", name, arg)


def _maybe_prompt(args: Args, run: Run, config: RunConfig) -> None | NoReturn:
    if args.yes:
        return
    cli.out(f"You are about to run [yellow]{run.opref.get_full_name()}[/]")
    if not cli.confirm(f"Continue?", default=True):
        raise SystemExit(0)


def _run_config(args: Args):
    return cast(RunConfig, {})


def _op_cmd(context: RunContext, config: RunConfig):
    cmd_args = context.opdef.get_exec().get_run()
    if not cmd_args:
        error_handlers.missing_exec_error(context)
    env = {}
    return OpCmd(cmd_args, env)


def _user_attrs(args: Args):
    attrs: dict[str, Any] = {}
    if args.label:
        attrs["label"] = args.label
    return attrs


def _sys_attrs():
    return {"platform": platform.platform()}


class _OutputCallback(run_output.OutputCallback):
    def __init__(self, console: Console):
        self.console = console

    def output(self, stream: run_output.StreamType, out: bytes):
        self.console.out(out.decode(), end="")

    def close(self):
        pass


def _run(context: RunContext, args: Args):
    run = _stage(context, args)
    status = cli.status(_running_status_desc(context), args.quiet)
    output_cb = _OutputCallback(status.console)
    with status:
        proc = start_run(run)
        output = open_run_output(run, proc, output_cb=output_cb)
        exit_code = proc.wait()
        output.wait_and_close()
    with _RunPhaseStatus(args):
        finalize_run(run, exit_code)


def _running_status_desc(context: RunContext):
    return f"[dim]Running [{cli.PANEL_TITLE_STYLE}]{context.opref.get_full_name()}"
