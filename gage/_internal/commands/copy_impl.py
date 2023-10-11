# SPDX-License-Identifier: Apache-2.0

from typing import *

from ..types import *

import json
import os
import re
import subprocess

from .. import cli

from ..run_util import run_user_dir

from ..sys_config import get_runs_home

from ..util import flatten

from .impl_support import runs_table
from .impl_support import selected_runs


class Args(NamedTuple):
    runs: list[str]
    dest: str
    src: str
    where: str
    all: bool
    yes: bool


def copy(args: Args):
    if not args.runs and not args.all:
        cli.exit_with_error(
            "Specify a run to copy or use '--all'.\n\n"
            "Use '[cmd]gage list[/]' to show available runs.\n\n"
            f"Try '[cmd]gage copy -h[/]' for additional help."
        )
    if args.dest:
        _copy_to(args)
    elif args.src:
        _copy_from(args)
    else:
        cli.exit_with_error(
            "Option '--src' or '--dest' is required.\n\n"
            f"Try '[cmd]gage copy -h[/]' for additional help."
        )


def _copy_to(args: Args):
    runs, from_count = selected_runs(args)
    if not runs:
        cli.exit_with_error("Nothing selected")
    _maybe_prompt_copy_to(args, runs)
    with cli.status("Preparing for copy"):
        src_dir, includes = _src_run_includes([run for index, run in runs])
        total_bytes = _rclone_size(src_dir, includes)
    with cli.Progress(transient=True) as p:
        task = p.add_task("Copying runs", total=total_bytes)
        for total_copied in _rclone_copy_to(src_dir, args.dest, includes):
            p.update(task, completed=total_copied)
    runs_count = "1 run" if len(runs) == 1 else f"{len(runs)} runs"
    cli.err(f"Copied {runs_count}")


def _maybe_prompt_copy_to(args: Args, runs: list[tuple[int, Run]]):
    if args.yes:
        return
    table = runs_table(runs)
    cli.out(table)
    run_count = "1 run" if len(runs) == 1 else f"{len(runs)} runs"
    cli.err(f"You are about copy {run_count} to {args.dest}.")
    cli.err()
    if not cli.confirm(f"Continue?"):
        raise SystemExit(0)


def _src_run_includes(runs: list[Run]):
    assert runs
    src_root = None
    includes: list[str] = []
    for run in runs:
        for src_dir in _run_src_dirs(run):
            src_parent, name = os.path.split(src_dir)
            if not src_root:
                src_root = src_parent
            assert src_parent == src_root, (src_dir, src_parent)
            includes.append(name + "/**")
    assert src_root
    return src_root, includes


def _run_src_dirs(run: Run):
    if not os.path.exists(run.meta_dir):
        return
    yield run.meta_dir
    if os.path.exists(run.run_dir):
        yield run.run_dir
    user_dir = run_user_dir(run)
    if os.path.exists(user_dir):
        yield user_dir


def _rclone_size(src: str, includes: list[str]):
    p = subprocess.Popen(
        ["rclone", "size", src, "--include-from", "-", "--json"],
        text=True,
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
    )
    assert p.stdin
    assert p.stdout
    for include in includes:
        p.stdin.write(include + "\n")
    p.stdin.close()
    result = p.wait()
    out = p.stdout.read()
    if result != 0:
        raise RuntimeError(result, out)
    data = json.loads(out)
    bytes = data.get("bytes")
    assert isinstance(bytes, int), data
    return bytes


_TRANSFERRED_P = re.compile(r"-Transferred:\s+([\d\.]+) ([\S]+) /")


def _rclone_copy_to(src: str, dest: str, includes: list[str]):
    p = subprocess.Popen(
        [
            "rclone",
            "copy",
            src,
            dest,
            "--include-from",
            "-",
            "--progress",
            "--stats",
            "200ms",
        ],
        text=True,
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
    )
    assert p.stdin
    assert p.stdout
    for include in includes:
        p.stdin.write(include + "\n")
    p.stdin.close()
    while True:
        line = p.stdout.readline()
        if not line:
            break
        m = _TRANSFERRED_P.search(line)
        if m:
            assert m.group(2) == "KiB", line
            yield int(float(m.group(1)) * 1024)
    result = p.wait()
    if result != 0:
        raise RuntimeError(result)


def _copy_from(args: Args):
    # TODO: Deferring substantial functionality of supporting remote run
    # listings and filters. Currently only supporting a non-filterable,
    # non-previewable copy of all remote runs.
    assert args.src
    if not args.all:
        cli.exit_with_error("'--all' is required when using '-s / --source'")
    if args.where:
        cli.exit_with_error("'--where' cannot be used with '-s / --source'")
    _maybe_prompt_copy_from(args)
    with cli.Progress(transient=True) as p:
        task = p.add_task("Copying runs")
        for copied, total in _rclone_copy_from(
            args.src, get_runs_home(), excludes=["*.project", ".deleted"]
        ):
            p.update(task, completed=copied, total=total)
    # TODO: Deferring even reasonable UI like "copied N runs" as we're
    # just copying blindly from the src with the applied excludes
    # (above)
    cli.err(f"Copied runs")


def _maybe_prompt_copy_from(args: Args):
    if args.yes:
        return
    cli.err(f"You are about copy all runs from {args.src}.")
    cli.err()
    if not cli.confirm(f"Continue?"):
        raise SystemExit(0)


_TRANSFERRED2_P = re.compile(r"-Transferred:\s+([\d\.]+) ([\S]+) / ([\d\.]+) ([\S]+)")


def _rclone_copy_from(src: str, dest: str, excludes: list[str]):
    exclude_opts = flatten([["--exclude", pattern] for pattern in excludes])
    p = subprocess.Popen(
        [
            "rclone",
            "copy",
            src,
            dest,
            "--progress",
            "--stats",
            "10ms",
        ]
        + exclude_opts,
        text=True,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
    )
    assert p.stdout
    while True:
        line = p.stdout.readline()
        if not line:
            break
        m = _TRANSFERRED2_P.search(line)
        if m:
            assert m.group(2) == "KiB", line
            assert m.group(4) == "KiB", line
            yield int(float(m.group(1)) * 1024), int(float(m.group(3)) * 1024)
            import time

            time.sleep(0.1)
    result = p.wait()
    if result != 0:
        raise RuntimeError(result)
