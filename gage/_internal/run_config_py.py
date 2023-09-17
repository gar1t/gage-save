# SPDX-License-Identifier: Apache-2.0

from typing import *

import libcst as cst

from .run_config import *

__all__ = ["PythonConfig"]


class PythonConfig(RunConfig):
    def __init__(self, source: str, filename: str | None = None):
        self._cst = cst.parse_module(source)
        self.filename = filename
        _init_config(self._cst, self)

    def render(self):
        return self._cst.code


def _init_config(module: cst.Module, config: RunConfig):
    visitor = ConfigVisitor(config)
    module.visit(visitor)


class ConfigVisitor(cst.CSTVisitor):
    def __init__(self, config: RunConfig):
        self.config = config

    def on_visit(self, node: cst.CSTNode):
        """Traverses the module to find top-level value assignments.

        Value assignments must be of config value types (numbers,
        strings, etc.)

        Skips further traversal by returning False.
        """
        module = cst.ensure_type(node, cst.Module)
        for assign in _iter_top_level_assigns(module):
            self.config.update(_iter_config_kv(assign))
        return False


def _iter_top_level_assigns(module: cst.Module):
    for node in module.body:
        if isinstance(node, cst.SimpleStatementLine):
            for stmt_node in node.body:
                if isinstance(stmt_node, cst.Assign):
                    yield stmt_node


def _iter_config_kv(
    assign: cst.Assign,
) -> Generator[tuple[str, RunConfigValue], Any, None]:
    try:
        val = _config_val(assign.value)
    except TypeError:
        pass
    else:
        for t in assign.targets:
            if isinstance(t.target, cst.Name):
                name = t.target.value
                if isinstance(val, dict):
                    for nested_key, nested_val in _iter_dict_keys(val, [name]):
                        yield nested_key, nested_val
                else:
                    yield name, val


def _iter_dict_keys(
    d: dict[str, RunConfigValue],
    key_path: list[str],
) -> Generator[tuple[str, RunConfigValue], Any, None]:
    for key, val in d.items():
        val_key_path = key_path + [key]
        if isinstance(val, dict):
            for nested_key, nested_val in _iter_dict_keys(val, val_key_path):
                yield nested_key, nested_val
        else:
            yield ".".join(val_key_path), val


_NAMES = {"True": True, "False": False, "None": None}


def _config_val(val: cst.BaseExpression) -> RunConfigValue:
    if isinstance(val, cst.Integer):
        return int(val.value)
    if isinstance(val, cst.Float):
        return float(val.value)
    if isinstance(val, cst.SimpleString):
        return val.value[1:-1]
    if isinstance(val, cst.Name):
        try:
            return _NAMES[val.value]
        except KeyError:
            raise TypeError()
    if isinstance(val, cst.List):
        return dict(_iter_list_config_vals(val))
    if isinstance(val, cst.Dict):
        return dict(_iter_dict_config_vals(val))
    raise TypeError()


def _iter_list_config_vals(l: cst.List):
    for i, element in enumerate(l.elements):
        try:
            val = _config_val(element.value)
        except TypeError:
            pass
        else:
            yield str(i), val


def _iter_dict_config_vals(d: cst.Dict):
    for i, element in enumerate(d.elements):
        if not isinstance(element, cst.DictElement):
            continue
        if not isinstance(element.key, cst.SimpleString):
            continue
        try:
            val = _config_val(element.value)
        except TypeError:
            pass
        else:
            yield element.key.value[1:-1], val
