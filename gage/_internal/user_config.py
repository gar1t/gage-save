# SPDX-License-Identifier: Apache-2.0

from typing import *

from .types import *

import os

from . import sys_config

from .project_util import find_project_dir
from .project_util import load_data
from .schema_util import validate_data
from .util import find_apply

__all__ = [
    "load_user_config",
    "load_user_config_data",
    "user_config_for_dir",
    "user_config_for_project",
    "user_config_path_for_dir",
    "user_config_candidates",
    "validate_user_config_data",
]

USER_CONFIG_NAMES = [
    "gageconfig.toml",
    "gageconfig.yaml",
    "gageconfig.json",
    os.path.join(".gage", "config.toml"),
    os.path.join(".gage", "config.yaml"),
    os.path.join(".gage", "config.json"),
]


def validate_user_config_data(obj: JSONCompatible):
    result = validate_data(obj, "userconfig")
    if not result.valid:
        raise UserConfigValidationError(result)


def load_user_config(filename: str):
    data = load_user_config_data(filename)
    return UserConfig(filename, data)


def load_user_config_data(filename: str):
    try:
        return load_data(filename)
    except Exception as e:
        raise UserConfigLoadError(filename, str(e))


def user_config_for_dir(dirname: str):
    path = user_config_path_for_dir(dirname)
    if not path:
        return None
    return load_user_config(path)


def user_config_path_for_dir(dirname: str):
    for name in user_config_candidates():
        path = os.path.join(dirname, name)
        if not os.path.exists(path):
            continue
        return path
    return None


def user_config_candidates():
    return USER_CONFIG_NAMES


def user_config_for_project(cwd: str | None = None):
    return find_apply([_project_config, _system_config], cwd)


def _project_config(cwd: str | None):
    cwd = cwd or sys_config.cwd()
    project_dir = find_project_dir(cwd)
    if not project_dir:
        return None
    return user_config_for_dir(project_dir)


def _system_config(cwd: str | None):
    return user_config_for_dir(os.path.expanduser("~"))
