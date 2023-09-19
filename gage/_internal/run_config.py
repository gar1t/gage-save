# SPDX-License-Identifier: Apache-2.0

from typing import *

import logging
import os
import re

from .types import *

from . import file_select

__all__ = [
    "RunConfig",
    "RunConfigValue",
    "RunConfigBase",
    "UnsupportedFileFormat",
    "apply_config",
    "iter_config_paths",
    "match_keys",
    "read_config",
]

log = logging.getLogger(__name__)


class UnsupportedFileFormat(Exception):
    pass


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
    for filename, keys, file_config in iter_config_paths(opdef, dest_dir):
        if file_config:
            apply_file_config(keys, file_config, filename)


def iter_config_paths(
    opdef: OpDef, dest_dir: str
) -> Generator[tuple[str, list[str], RunConfig | None], Any, None]:
    for c in opdef.get_config():
        include = c.get_include()
        if not include:
            if not c.get_path():
                continue
            include = [c.get_path()]
        exclude = c.get_exclude() or []
        include_file_patterns, include_key_patterns = _split_config_paths(include)
        exclude_file_patterns, exclude_key_patterns = _split_config_paths(exclude)
        select = file_select.parse_patterns(
            include_file_patterns, exclude_file_patterns
        )
        for path in file_select.select_files(dest_dir, select):
            filename = os.path.join(dest_dir, path)
            try:
                file_config = load_config(filename)
            except UnsupportedFileFormat as e:
                yield path, [], None
            else:
                yield path, match_keys(
                    include_key_patterns,
                    exclude_key_patterns,
                    file_config,
                ), file_config


def load_config(filename: str) -> RunConfig:
    _, ext = os.path.splitext(filename)
    if ext == ".py":
        from .run_config_py import PythonConfig

        return PythonConfig(open(filename).read())
    raise UnsupportedFileFormat(filename)


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


def match_keys(include: list[str], exclude: list[str], keys: list[str] | RunConfig):
    include_p = [_compile_match_pattern(p) for p in include]
    exclude_p = [_compile_match_pattern(p) for p in exclude]
    return [key for key in keys if _match_key(include_p, exclude_p, key)]


_MATCHER_P = re.compile(r"\*\*\.?|\*|\?")


def _compile_match_pattern(pattern: str):
    re_parts = []
    path_sep = re.escape(".")
    pos = 0
    for m in _MATCHER_P.finditer(pattern):
        start, end = m.span()
        re_parts.append(re.escape(pattern[pos:start]))
        matcher = pattern[start:end]
        if matcher == "*":
            re_parts.append(rf"[^{path_sep}]*")
        elif matcher in ("**.", "**"):
            re_parts.append(r"(?:.+\.)*")
        elif matcher == "?":
            re_parts.append(rf"[^{path_sep}]?")
        else:
            assert False, (matcher, pattern)
        pos = end
    re_parts.append(re.escape(pattern[pos:]))
    re_parts.append("$")
    return re.compile("".join(re_parts))


def _match_key(include: list[Pattern[str]], exclude: list[Pattern[str]], key: str):
    return any(p.match(key) for p in include) and not any(p.match(key) for p in exclude)


def apply_file_config(keys: list[str], config: RunConfig, filename: str):
    pass
