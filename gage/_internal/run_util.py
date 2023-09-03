# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *
from .types import *
from logging import Logger

import json
import logging
import os
import threading
import time
import uuid

from . import config
from . import util

from .opref_util import encode_opref

META_SCHEMA = 1

__last_ts = None
__last_ts_lock = threading.Lock()


def run_timestamp():
    """Returns an integer use for run timestamps.

    Ensures that subsequent calls return increasing values.
    """
    ts = time.time_ns() // 1000
    with __last_ts_lock:
        if __last_ts is not None and __last_ts >= ts:
            ts = __last_ts + 1
        globals()["__last_ts"] = ts
    return ts


def _runner_log(run: Run):
    filename = _runner_log_filename(run)
    filename_parent = os.path.dirname(filename)
    assert os.path.exists(filename_parent), filename_parent
    log = logging.Logger("runner")
    handler = logging.FileHandler(filename)
    log.addHandler(handler)
    formatter = logging.Formatter("%(asctime)s %(message)s", "%Y-%m-%dT%H:%M:%S%z")
    handler.setFormatter(formatter)
    return log


def _runner_log_filename(run: Run):
    return run_meta_path(run, "log", "runner")


def make_run(location: Optional[str] = None):
    run_id = unique_run_id()
    location = location or config.runs_home()
    run_dir = os.path.join(location, run_id)
    util.make_dir(run_dir)
    return Run(run_id, run_dir)


def unique_run_id():
    return uuid.uuid4().hex


def run_status(run: Run) -> RunStatus:
    meta_dir = run_meta_dir(run)
    if not os.path.exists(meta_dir):
        return "unknown"
    assert False


def run_meta_dir(run: Run):
    return run.run_dir + ".meta"


def run_meta_path(run: Run, *path: str):
    return os.path.join(run_meta_dir(run), *path)


def run_attrs(run: Run) -> Dict[str, Any]:
    attrs_dir = run_meta_path(run, "attrs")
    if not os.path.exists(attrs_dir):
        raise FileNotFoundError(attrs_dir)
    assert False


def run_attr(run: Run, name: str):
    try:
        return getattr(run, name)
    except AttributeError:
        assert False, f"TODO run attr {name} somewhere in {run.run_dir}"


def init_run_meta(
    run: Run,
    opref: OpRef,
    opdef: OpDef,
    cmd: OpCmd,
    user_attrs: Optional[Dict[str, Any]] = None,
    system_attrs: Optional[Dict[str, Any]] = None,
):
    if opref.op_name != opdef.name:
        raise ValueError(
            f"mismatched names in opref ('{opref.op_name}') "
            f"and opdef ('{opdef.name}')"
        )
    meta_dir = _ensure_run_meta_dir(run)
    _write_schema_file(meta_dir)
    _ensure_meta_log_dir(meta_dir)
    log = _runner_log(run)
    _write_run_id(run, meta_dir, log)
    _write_opdef(opdef, meta_dir, log)
    _ensure_meta_proc_dir(meta_dir)
    _write_cmd_args(cmd, meta_dir, log)
    _write_cmd_env(cmd, meta_dir, log)
    # opref is here as it marks the run as discoverable in lists
    _write_opref(opref, meta_dir, log)
    _write_initialized_timestamp(meta_dir, log)


def _ensure_run_meta_dir(run: Run):
    meta_dir = run_meta_dir(run)
    util.ensure_dir(meta_dir)
    return meta_dir


def _write_schema_file(meta_dir: str):
    filename = os.path.join(meta_dir, "__schema__")
    util.write_file(filename, str(META_SCHEMA), readonly=True)


def _ensure_meta_log_dir(meta_dir: str):
    util.ensure_dir(os.path.join(meta_dir, "log"))


def _write_run_id(run: Run, meta_dir: str, log: Logger):
    log.info("Writing id")
    filename = os.path.join(meta_dir, "id")
    util.write_file(filename, run.id, readonly=True)


def _write_opdef(opdef: OpDef, meta_dir: str, log: Logger):
    log.info("Writing opdef.json")
    filename = os.path.join(meta_dir, "opdef.json")
    encoded = json.dumps(opdef.as_json())
    util.write_file(filename, encoded, readonly=True)


def _ensure_meta_proc_dir(meta_dir: str):
    util.ensure_dir(os.path.join(meta_dir, "proc"))


def _write_cmd_args(cmd: OpCmd, meta_dir: str, log: Logger):
    log.info("Writing proc/cmd")
    filename = os.path.join(meta_dir, "proc", "cmd")
    util.write_file(filename, _encode_cmd_args(cmd.args), readonly=True)


def _encode_cmd_args(args: List[str]):
    return "".join([arg + "\n" for arg in args])


def _write_cmd_env(cmd: OpCmd, meta_dir: str, log: Logger):
    log.info("Writing proc/env")
    filename = os.path.join(meta_dir, "proc", "env")
    util.write_file(filename, _encode_cmd_env(cmd.env), readonly=True)


def _encode_cmd_env(env: Dict[str, str]):
    return "".join([f"{name}={val}\n" for name, val in sorted(env.items())])


def _write_opref(opref: OpRef, meta_dir: str, log: Logger):
    log.info("Writing opref")
    filename = os.path.join(meta_dir, "opref")
    util.write_file(filename, encode_opref(opref), readonly=True)


def _write_initialized_timestamp(meta_dir: str, log: Logger):
    log.info("Writing initialized")
    filename = os.path.join(meta_dir, "initialized")
    timestamp = run_timestamp()
    util.write_file(filename, str(timestamp), readonly=True)


"""
TODO: Init run meta dir

- Write `__schema__` version (e.g. `1`)
- Write `id` (run.id)
- Write op ref (need as arg)
- Write op def (need as arg)

- Write `initialized` with timestamp
"""
