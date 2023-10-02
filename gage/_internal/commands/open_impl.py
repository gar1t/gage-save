# SPDX-License-Identifier: Apache-2.0

from typing import *

import logging
import os
import shlex
import subprocess
import sys

from .. import cli

from .impl_util import one_run

log = logging.getLogger(__name__)


class Args(NamedTuple):
    run: str
    path: str
    cmd: str
    meta: bool


def open(args: Args):
    run = one_run(args)
    dirname = run.meta_dir if args.meta else run.run_dir
    path = os.path.join(dirname, args.path)
    _open(path, args)
    _flush_streams_and_exit()


def _open(path: str, args: Args):
    try:
        _open_f(args)(path)
    except Exception as e:
        if log.getEffectiveLevel() <= logging.DEBUG:
            log.exception("opening %s", path)
        cli.exit_with_error(str(e))


def _open_f(args: Args):
    if args.cmd:
        return _proc_f(args.cmd)
    if os.name == "nt":
        return os.startfile
    if sys.platform.startswith("darwin"):
        return _proc_f("open")
    if os.name == "posix":
        return _proc_f("xdg-open")
    cli.exit_with_error(
        f"unsupported platform: {sys.platform} {os.name}\n"  # \
        "Try --cmd with a program."
    )


def _proc_f(prog: str):
    cmd = shlex.split(prog)

    def f(path: str):
        p = subprocess.Popen(
            cmd + [path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        p.wait()

    return f


def _flush_streams_and_exit():
    sys.stdout.flush()
    sys.exit(0)
