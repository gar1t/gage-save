# SPDX-License-Identifier: Apache-2.0

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

from .file_util import make_dir
from .file_util import ensure_dir
from .file_util import write_file

from .opref_util import encode_opref

__all__ = [
    "META_SCHEMA",
    "run_status",
    "run_meta_dir",
    "run_attrs",
    "run_attr",
    "make_run",
    "unique_run_id",
    "run_timestamp",
    "init_run_meta",
    "stage_run",
]

META_SCHEMA = 1

__last_ts = None
__last_ts_lock = threading.Lock()

# =================================================================
# Runner log
# =================================================================


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


# =================================================================
# Run attributes
# =================================================================


def run_status(run: Run) -> RunStatus:
    meta_dir = run_meta_dir(run)
    if not os.path.exists(meta_dir):
        return "unknown"
    assert False


def run_meta_dir(run: Run):
    return run.run_dir + ".meta"


def run_meta_path(run: Run, *path: str):
    return os.path.join(run_meta_dir(run), *path)


def run_attrs(run: Run) -> dict[str, Any]:
    attrs_dir = run_meta_path(run, "attrs")
    if not os.path.exists(attrs_dir):
        raise FileNotFoundError(attrs_dir)
    assert False


def run_attr(run: Run, name: str):
    try:
        return getattr(run, name)
    except AttributeError:
        assert False, f"TODO run attr {name} somewhere in {run.run_dir}"


# =================================================================
# Make run
# =================================================================


def make_run(location: Optional[str] = None):
    run_id = unique_run_id()
    location = location or config.runs_home()
    run_dir = os.path.join(location, run_id)
    make_dir(run_dir)
    return Run(run_id, run_dir)


def unique_run_id():
    return uuid.uuid4().hex


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


# =================================================================
# Meta dir init
# =================================================================


def init_run_meta(
    run: Run,
    opref: OpRef,
    opdef: OpDef,
    cmd: OpCmd,
    user_attrs: Optional[dict[str, Any]] = None,
    system_attrs: Optional[dict[str, Any]] = None,
):
    if opref.op_name != opdef.name:
        raise ValueError(
            f"mismatched names in opref ('{opref.op_name}') and opdef ('{opdef.name}')"
        )
    meta_dir = _ensure_run_meta_dir(run)
    _write_schema_file(meta_dir)
    _ensure_meta_log_dir(meta_dir)
    log = _runner_log(run)
    _write_run_id(run, meta_dir, log)
    _write_opdef(opdef, meta_dir, log)
    _write_cmd_args(cmd, meta_dir, log)
    _write_cmd_env(cmd, meta_dir, log)
    if user_attrs:
        _write_user_attrs(user_attrs, meta_dir, log)
    if system_attrs:
        _write_system_attrs(system_attrs, meta_dir, log)
    # opref marks run as discoverable in lists - should appear last
    _write_opref(opref, meta_dir, log)
    _write_initialized_timestamp(meta_dir, log)


def _ensure_run_meta_dir(run: Run):
    meta_dir = run_meta_dir(run)
    ensure_dir(meta_dir)
    return meta_dir


def _write_schema_file(meta_dir: str):
    filename = os.path.join(meta_dir, "__schema__")
    write_file(filename, str(META_SCHEMA), readonly=True)


def _ensure_meta_log_dir(meta_dir: str):
    ensure_dir(os.path.join(meta_dir, "log"))


def _write_run_id(run: Run, meta_dir: str, log: Logger):
    log.info("Writing id")
    filename = os.path.join(meta_dir, "id")
    write_file(filename, run.id, readonly=True)


def _write_opdef(opdef: OpDef, meta_dir: str, log: Logger):
    log.info("Writing opdef.json")
    filename = os.path.join(meta_dir, "opdef.json")
    encoded = json.dumps(opdef.as_json())
    write_file(filename, encoded, readonly=True)


def _write_cmd_args(cmd: OpCmd, meta_dir: str, log: Logger):
    log.info("Writing proc/cmd")
    ensure_dir(os.path.join(meta_dir, "proc"))
    filename = os.path.join(meta_dir, "proc", "cmd")
    write_file(filename, _encode_cmd_args(cmd.args), readonly=True)


def _encode_cmd_args(args: list[str]):
    return "".join([arg + "\n" for arg in args])


def _write_cmd_env(cmd: OpCmd, meta_dir: str, log: Logger):
    log.info("Writing proc/env")
    ensure_dir(os.path.join(meta_dir, "proc"))
    filename = os.path.join(meta_dir, "proc", "env")
    write_file(filename, _encode_cmd_env(cmd.env), readonly=True)


def _encode_cmd_env(env: dict[str, str]):
    return "".join([f"{name}={val}\n" for name, val in sorted(env.items())])


def _write_user_attrs(attrs: dict[str, Any], meta_dir: str, log: Logger):
    _gen_write_attrs("user", attrs, meta_dir, log)


def _write_system_attrs(attrs: dict[str, Any], meta_dir: str, log: Logger):
    _gen_write_attrs("sys", attrs, meta_dir, log)


def _gen_write_attrs(dir: str, attrs: dict[str, Any], meta_dir: str, log: Logger):
    ensure_dir(os.path.join(meta_dir, dir))
    for name in attrs:
        log.info("Writing %s/%s", dir, name)
        filename = os.path.join(meta_dir, dir, name)
        encoded = json.dumps(attrs[name])
        write_file(filename, encoded, readonly=True)


def _write_opref(opref: OpRef, meta_dir: str, log: Logger):
    log.info("Writing opref")
    filename = os.path.join(meta_dir, "opref")
    write_file(filename, encode_opref(opref), readonly=True)


def _write_initialized_timestamp(meta_dir: str, log: Logger):
    log.info("Writing initialized")
    filename = os.path.join(meta_dir, "initialized")
    timestamp = run_timestamp()
    write_file(filename, str(timestamp), readonly=True)


# =================================================================
# Stage run
# =================================================================


def stage_run(run: Run):
    if not os.path.exists(run.run_dir):
        raise FileNotFoundError(f"Run dir does not exist: {run.run_dir}")
    meta_dir = run_meta_dir(run)
    if not os.path.exists(meta_dir):
        raise FileNotFoundError(f"Run meta dir does not exist: {meta_dir}")
    log = _runner_log(run)
    _write_staged_timestamp(meta_dir, log)


def _write_staged_timestamp(meta_dir: str, log: Logger):
    log.info("Writing initialized")
    filename = os.path.join(meta_dir, "initialized")
    timestamp = run_timestamp()
    write_file(filename, str(timestamp), readonly=True)
