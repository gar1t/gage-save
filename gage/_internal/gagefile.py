# SPDX-License-Identifier: Apache-2.0

from typing import *

import json
import os

import jschon
import tomli
import yaml

from .types import GageFile

__all__ = [
    "ValidationError",
    "load_gagefile",
    "load_data",
    "validate_data",
    "validation_error_output",
    "validation_errors",
]

__schema: Optional[jschon.JSONSchema] = None


JSONCompatible = None | bool | int | float | str | Sequence[Any] | Mapping[str, Any]


class ValidationError(Exception):
    def __init__(self, validation_result: jschon.Result):
        super().__init__(validation_result)
        self.validation_result = validation_result


class LoadError(Exception):
    pass


def validation_error_output(e: ValidationError):
    return e.validation_result.output("verbose")


def validation_errors(e: ValidationError):
    return list(e.validation_result.collect_errors())


def validate_data(obj: JSONCompatible):
    schema = _ensure_schema()
    result = schema.evaluate(jschon.JSON(obj))
    if not result.valid:
        raise ValidationError(result)


def _ensure_schema():
    if not __schema:
        catalog = jschon.create_catalog("2020-12")
        catalog.add_uri_source(
            jschon.URI("https://gageml.org/"),
            jschon.LocalSource(_schema_dir(), suffix=".json"),
        )
        globals()["__schema"] = _load_schema()
    assert __schema
    return __schema


def _schema_dir():
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "schema",
    )


def _load_schema():
    src = os.path.join(_schema_dir(), "gagefile.json")
    with open(src) as f:
        schema_data = json.load(f)
    return jschon.JSONSchema(schema_data)


def load_gagefile(filename: str):
    data = load_data(filename)
    return GageFile(filename, data)


def load_data(filename: str):
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".toml":
        return _load_toml(filename)
    if ext == ".json":
        return _load_json(filename)
    if ext in (".yaml", ".yml"):
        return _load_yaml(filename)
    raise TypeError(f"unsupported file extension for {filename}")


def _load_toml(filename: str):
    with open(filename, "rb") as f:
        return tomli.load(f)


def _load_json(filename: str):
    with open(filename) as f:
        s = "".join([line for line in f if line.lstrip()[:2] != "//"])
        try:
            return json.loads(s)
        except json.JSONDecodeError as e:
            raise LoadError(f"invalid JSON: {e}")


def _load_yaml(filename: str):
    with open(filename) as f:
        return yaml.safe_load(f)


def gagefile_for_dir(path: str):
    paths = [
        os.path.join(path, candidate)
        for candidate in [
            os.path.join(".gage", "settings.json"),
            "gage.toml",
            "gage.yaml",
            "gage.json",
        ]
    ]
    for path in paths:
        if not os.path.exists(path):
            continue
        return load_gagefile(path)
    raise FileNotFoundError(paths[-1])
