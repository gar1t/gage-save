# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

import os
import threading

__var_home: Optional[str] = None


__cwd_lock = threading.Lock()
__cwd = None


def set_cwd(cwd: Optional[str]):
    """Sets configured current directory.

    The configured current directory is different from `os.getcwd()` as
    it's specified by the user (or a user proxy) as a command-specific
    current directory.

    Vista maintains the distinction between `cwd` and the process
    current directory to provide meaningful user messages. If changes to
    the configured current directory were applied as `os.chdir()`,
    messages to users would no longer reflect the user-facing current
    directory.

    Consider this command:

        $ vml -C my-project run train

    To the user, this is equivalent to `cd my-project; vml run train`.
    However, Vista can't use this technique internally to run the
    command because it needs to preserve the user-facing cwd for
    messages.
    """
    with __cwd_lock:
        globals()["_cwd"] = cwd


def cwd():
    """Returns the configured current directory.

    If a configured directory is not set, returns `os.getcwd()`.

    See `set_cwd()` for details on the configured current directory vs
    the process current directory (i.e. `os.getcwd()`).
    """
    with __cwd_lock:
        return __cwd or os.getcwd()


class SetCwd:
    _save = None

    def __init__(self, path: str):
        self.path = path

    def __enter__(self):
        self._save = cwd()
        set_cwd(self.path)

    def __exit__(self, *args: Any):
        set_cwd(self._save)


def var_home():
    return __var_home or os.path.expanduser("~/.vistaml")


def set_var_home(path: str):
    globals()["__var_home"] = path


def runs_home(deleted: bool = False):
    if deleted:
        return os.path.join(var_home(), "trash", "runs")
    return os.path.join(var_home(), "runs")
