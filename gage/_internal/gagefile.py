# SPDX-License-Identifier: Apache-2.0

from typing import *
from .types import *

import json
import os

# Avoid jschon imports here - expensive

import tomli

from . import sys_config

from .project_util import find_project_dir

__all__ = [
    "ValidationError",
    "gagefile_candidates",
    "gagefile_path_for_dir",
    "load_gagefile",
    "load_data",
    "validate_data",
    "validation_error_output",
    "validation_errors",
]

__schema: Any = None


JSONCompatible = None | bool | int | float | str | Sequence[Any] | Mapping[str, Any]


class ValidationError(Exception):
    def __init__(self, validation_result: Any):
        super().__init__(validation_result)
        self.validation_result = validation_result


def validation_error_output(e: ValidationError):
    return e.validation_result.output("verbose")


def validation_errors(e: ValidationError):
    return list(e.validation_result.collect_errors())


def validate_data(obj: JSONCompatible):
    import jschon

    schema = _ensure_schema()
    result = schema.evaluate(jschon.JSON(obj))
    if not result.valid:
        raise ValidationError(result)


def _ensure_schema():
    if not __schema:
        import jschon

        catalog = jschon.create_catalog("2020-12")
        globals()["__schema"] = _load_schema()
    assert __schema
    return __schema


def _load_schema():
    from jschon import JSONSchema

    src = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "gagefile.schema.json",
    )
    with open(src) as f:
        schema_data = json.load(f)
    return JSONSchema(schema_data)


def load_gagefile(filename: str):
    data = load_data(filename)
    return GageFile(filename, data)


def load_data(filename: str):
    if not os.path.exists(filename):
        raise GageFileLoadError(filename, f"file does not exist: {filename}")
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".toml":
        return _load_toml(filename)
    if ext == ".json":
        return _load_json(filename)
    if ext in (".yaml", ".yml"):
        return _load_yaml(filename)
    raise GageFileLoadError(filename, f"unsupported file extension for {filename}")


def _load_toml(filename: str):
    with open(filename, "rb") as f:
        return tomli.load(f)


def _load_json(filename: str):
    with open(filename) as f:
        s = "".join([line for line in f if line.lstrip()[:2] != "//"])
        try:
            return json.loads(s)
        except json.JSONDecodeError as e:
            raise GageFileLoadError(filename, f"invalid JSON: {e}")


def _load_yaml(filename: str):
    import yaml

    with open(filename) as f:
        return yaml.safe_load(f)


def gagefile_for_dir(dirname: str):
    return load_gagefile(gagefile_path_for_dir(dirname))


def gagefile_path_for_dir(dirname: str):
    for name in gagefile_candidates():
        path = os.path.join(dirname, name)
        if not os.path.exists(path):
            continue
        return path
    raise GageFileNotFoundError(dirname)


def gagefile_candidates():
    return [
        os.path.join(".gage", "settings.json"),
        "gage.toml",
        "gage.yaml",
        "gage.json",
    ]


def gagefile_for_project(cwd: str | None = None):
    cwd = cwd or sys_config.cwd()
    project_dir = find_project_dir(cwd)
    if not project_dir:
        raise GageFileNotFoundError(cwd)
    return gagefile_for_dir(project_dir)
