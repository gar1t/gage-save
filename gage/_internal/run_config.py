# SPDX-License-Identifier: Apache-2.0

from typing import *

import os

from .types import *

from . import file_select

__all__ = ["RunConfig", "RunConfigValue", "RunConfigBase"]


class RunConfigBase(RunConfig):
    _initialized = False

    def __setitem__(self, key: str, item: RunConfigValue):
        if self._initialized and key not in self:
            raise ValueError(f"key does not exist: {key!r}")
        super().__setitem__(key, item)

    def apply(self) -> str:
        """Applies config returning the new source."""
        raise NotImplementedError()


def read_config(src_dir: str):
    assert False, "TODO"


def apply_config(config: RunConfig, opdef: OpDef, dest_dir: str):
    for (
        name,
        keys,
        path,
    ) in _iter_config_targets(opdef, dest_dir):
        _apply_config(config, keys, os.path.join(dest_dir, path))


def _iter_config_targets(
    opdef: OpDef, dest_dir: str
) -> Generator[tuple[str | None, list[str], str], Any, None]:
    for c in opdef.get_config():
        include = c.get_include() or [cast(str, c.get_target())]
        exclude = c.get_exclude() or []
        include_file_patterns, include_key_patterns = _split_config_paths(include)
        exclude_file_patterns, exclude_key_patterns = _split_config_paths(exclude)
        select = file_select.parse_patterns(
            include_file_patterns, exclude_file_patterns
        )
        for path in file_select.select_files(dest_dir, select):
            yield c.get_name(), [], path


def _split_config_paths(paths: list[str]):
    acc_f: list[str] = []
    acc_k: list[str] = []
    for path in paths:
        f, k = _split_config_path(path)
        acc_f.append(f)
        acc_k.append(k)
    return acc_f, acc_k


def _split_config_path(path: str):
    file_pattern, *rest = path.split("#", 1)
    return file_pattern, rest[0] if rest else "*"


def _apply_config(config: RunConfig, keys: list[str], filename: str):
    pass
