# SPDX-License-Identifier: Apache-2.0

from typing import *

import fnmatch
import errno
import glob
import logging
import os
import re
import shutil

from .shlex_util import shlex_quote

from .file_util import ensure_dir
from .file_util import is_text_file
from .file_util import standardize_path


__all__ = [
    "FileCopyHandler",
    "FileSelectTestFunc",
    "FileSelectTest",
    "FileSelectResult",
    "FileSelectRuleType",
    "FileSelectRule",
    "FileSelectResults",
    "FileSelect",
    "DisabledFileSelect",
    "include",
    "exclude",
    "copyfiles",
    "copytree",
]

log = logging.getLogger(__name__)

FileSelectTestFunc = Callable[..., bool | None]


class FileSelectTest:
    def __init__(self, name: str, test_f: FileSelectTestFunc, *test_args: Any):
        self.name = name
        self.test_f = test_f
        self.test_args = test_args

    def __call__(self):
        return self.test_f(*self.test_args)


FileSelectResult = tuple[bool | None, FileSelectTest | None]

FileSelectRuleType = Literal["text", "binary", "dir"]


class FileSelectRule:
    def __init__(
        self,
        result: bool,
        patterns: list[str] | str,
        type: FileSelectRuleType | None = None,
        regex: bool = False,  # treat patterns as regex, otherwise globs
        sentinel: str = "",
        size_gt: int | None = None,
        size_lt: int | None = None,
        max_matches: int | None = None,
    ):
        self.result = result
        self.patterns = _init_patterns(patterns, regex)
        self.regex = regex
        self._patterns_match = _patterns_match_f(self.patterns, regex)
        self.type = _validate_type(type)
        self.sentinel = sentinel
        self.size_gt = size_gt
        self.size_lt = size_lt
        self.max_matches = max_matches
        self._matches = 0

    def __str__(self):
        parts = [self.result and "include" or "exclude"]
        if self.type:
            parts.append(self.type)
        parts.append(", ".join([_quote_pattern(p) for p in self.patterns]))
        extras = self._format_file_select_rule_extras()
        if extras:
            parts.append(extras)
        return " ".join(parts)

    def _format_file_select_rule_extras(self):
        parts = []
        if self.regex:
            parts.append("regex")
        if self.sentinel:
            parts.append(f"containing {_quote_pattern(self.sentinel)}")
        if self.size_gt:
            parts.append(f"size > {self.size_gt}")
        if self.size_lt:
            parts.append(f"size < {self.size_lt}")
        if self.max_matches:
            parts.append(f"max match {self.max_matches}")
        return ", ".join(parts)

    @property
    def matches(self):
        return self._matches

    def test(self, src_root: str, relpath: str) -> FileSelectResult:
        """Returns a tuple of result and applicable test.

        Applicable test can be used as a reason for the result -
        e.g. to provide details to a user on why a particular file was
        selected or not.
        """
        fullpath = os.path.join(src_root, relpath)
        tests = [
            FileSelectTest("max matches", self._test_max_matches),
            FileSelectTest("pattern", self._test_patterns, relpath),
            FileSelectTest("type", self._test_type, fullpath),
            FileSelectTest("size", self._test_size, fullpath),
        ]
        for test in tests:
            if not test():
                return None, test
        self._matches += 1
        return self.result, None

    def _test_max_matches(self):
        if self.max_matches is None:
            return True
        return self._matches < self.max_matches

    def _test_patterns(self, path: str):
        return self._patterns_match(path)

    def _test_type(self, path: str):
        if self.type is None:
            return True
        if self.type == "text":
            return _is_text_file(path)
        if self.type == "binary":
            return not _is_text_file(path)
        if self.type == "dir":
            return self._test_dir(path)
        assert False, self.type

    def _test_dir(self, path: str):
        if not os.path.isdir(path):
            return False
        if self.sentinel:
            return len(glob.glob(os.path.join(path, self.sentinel))) > 0
        return True

    def _test_size(self, path: str):
        if self.size_gt is None and self.size_lt is None:
            return True
        size = _file_size(path)
        if size is None:
            return True
        if self.size_gt and size > self.size_gt:
            return True
        if self.size_lt and size < self.size_lt:
            return True
        return False


def _init_patterns(patterns: list[str] | str, regex: bool):
    if isinstance(patterns, str):
        patterns = [patterns]
    return patterns if regex else _native_paths(patterns)


def _native_paths(patterns: list[str]):
    return [p.replace("/", os.path.sep) for p in patterns]


def _patterns_match_f(patterns: list[str], regex: bool):
    return _regex_match_f(patterns) if regex else _fnmatch_f(patterns)


def _regex_match_f(patterns: list[str]):
    compiled = [re.compile(p) for p in patterns]

    def f(path: str):
        return any((p.match(standardize_path(path)) for p in compiled))

    return f


def _fnmatch_f(patterns: list[str]):
    def f(path: str):
        return any((_fnmatch(path, p) for p in patterns))

    return f


def _fnmatch(path: str, pattern: str):
    if os.path.sep not in pattern:
        path = os.path.basename(path)
    pattern = _strip_leading_path_sep(pattern)
    return fnmatch.fnmatch(path, pattern)


def _strip_leading_path_sep(pattern: str):
    while pattern:
        if pattern[0] != os.path.sep:
            break
        pattern = pattern[1:]
    return pattern


def _validate_type(type: str | None):
    valid = ("text", "binary", "dir")
    if type is not None and type not in valid:
        raise ValueError(
            f"invalid value for type {type!r}: expected one of {', '.join(valid)}"
        )
    return type


def _quote_pattern(s: str):
    return shlex_quote(s) if " " in s else s


def _is_text_file(path: str):
    try:
        return is_text_file(path)
    except OSError as e:
        log.warning("could not check for text file %s: %s", path, e)
        return False


def _file_size(path: str):
    try:
        return os.path.getsize(path)
    except OSError:
        return None


FileSelectResults = list[tuple[FileSelectResult, FileSelectRule]]


class FileSelect:
    _disabled = None

    def __init__(self, rules: list[FileSelectRule]):
        self.rules = rules

    @property
    def disabled(self):
        if self._disabled is None:
            self._disabled = self._init_disabled()
        return self._disabled

    def _init_disabled(self):
        """Returns True if file select is disabled.

        This is an optimization to disable file select by appending an
        exclude '*' to a rule set.

        Assumes not disabled until finds a disable all pattern (untyped
        match of '*'). Disable pattern can be reset by any subsequent
        include pattern.
        """
        disabled = False
        for rule in self.rules:
            if rule.result:
                disabled = False
            elif "*" in rule.patterns and rule.type is None:
                disabled = True
        return disabled

    def select_file(
        self,
        src_root: str,
        relpath: str,
    ) -> tuple[bool, FileSelectResults]:
        """Apply rules to file located under src_root with relpath.

        All rules are applied to the file. The last rule to apply
        (i.e. its `test` method returns a non-None value) determines
        whether or not the file is selected - selected if test returns
        True, not selected if returns False.

        If no rules return a non-None value, the file is not selected.

        Returns a tuple of the selected flag (True or False) and list
        of applied rules and their results (two-tuples).
        """
        test_results = [
            (rule.test(src_root, relpath), rule)
            for rule in self.rules
            if rule.type != "dir"
        ]
        result, _test = _reduce_file_select_results(test_results)
        return result is True, test_results

    def prune_dirs(
        self, src_root: str, relroot: str, dirs: list[str]
    ) -> list[tuple[str, FileSelectResults]]:
        """Deletes from dirs values that excluded as 'dir' type.

        Returns a list of pruned dir / file select results. The file
        select results are the cause of the excluded dir.
        """
        pruned: list[tuple[str, FileSelectResults]] = []
        for name in sorted(dirs):
            last_select_result: FileSelectResult | None = None
            last_select_result_rule: FileSelectRule | None = None
            relpath = os.path.join(relroot, name)
            for rule in self.rules:
                if rule.type != "dir":
                    continue
                selected, _ = select_result = rule.test(src_root, relpath)
                if selected is not None:
                    last_select_result = select_result
                    last_select_result_rule = rule
            if last_select_result and last_select_result[0] is False:
                assert last_select_result_rule
                log.debug("skipping directory %s", relpath)
                select_results: FileSelectResults = [
                    (last_select_result, last_select_result_rule)
                ]
                pruned.append((name, select_results))
                dirs.remove(name)
        return pruned


def _reduce_file_select_results(results: FileSelectResults) -> FileSelectResult:
    for (result, test), _rule in reversed(results):
        if result is not None:
            return result, test
    return None, None


class DisabledFileSelect(FileSelect):
    def __init__(self):
        super().__init__([])

    @property
    def disabled(self):
        return True


def include(patterns: list[str], **kw: Any):
    return FileSelectRule(True, patterns, **kw)


def exclude(patterns: list[str], **kw: Any):
    return FileSelectRule(False, patterns, **kw)


class FileCopyHandler:
    def copy(
        self,
        src: str,
        dest: str,
        select_results: FileSelectResults | None = None,
    ):
        if select_results:
            log.debug("%s selected for copy: %s", src, select_results)
        log.debug("copying %s to %s", src, dest)
        ensure_dir(os.path.dirname(dest))
        self._try_copy_file(src, dest)

    def _try_copy_file(self, src: str, dest: str):
        try:
            shutil.copyfile(src, dest)
            shutil.copymode(src, dest)
        except IOError as e:
            if e.errno != errno.EEXIST:
                if not self.handle_copy_error(e, src, dest):
                    raise

    def ignore(self, src: str, results: FileSelectResults | None):
        """Called when a file is ignored for copy.

        `results` is the file select results that caused the decision to
        ignore the file. If `result` is None it can be inferred that no
        select rules were applied and the copy behavior is to ignore all
        files by default.
        """
        pass

    def handle_copy_error(self, error: Exception, src: str, dest: str):
        return False

    def close(self):
        pass


def copyfiles(
    src: str,
    dest: str,
    files: list[str],
    select: FileSelect | None = None,
    handler: FileCopyHandler | None = None,
):
    """Copies a list of files located under a source directory.

    `files` is a list of relative paths under `src`. Files are copied to
    `dest` as their relative paths.

    `handler_cls` is an optional class to create a `FileCopyHandler`
    instance. This is used to filter and otherwise handle a file copy.
    The default is a "select all" handler that copies each file in
    `files` without additional behavior.
    """
    if select and select.disabled:
        return
    handler = handler or FileCopyHandler()
    try:
        _copyfiles_impl(src, dest, files, select, handler)
    finally:
        handler.close()


def _copyfiles_impl(
    src: str,
    dest: str,
    files: list[str],
    select: FileSelect | None,
    handler: FileCopyHandler,
):
    for path in files:
        file_src = os.path.join(src, path)
        file_dest = os.path.join(dest, path)
        if select is None:
            handler.copy(file_src, file_dest)
        else:
            selected, results = select.select_file(src, path)
            if selected:
                handler.copy(file_src, file_dest, results)
            else:
                handler.ignore(file_src, results)


def copytree(
    src: str,
    dest: str,
    select: FileSelect | None = None,
    handler: FileCopyHandler | None = None,
    followlinks: bool = True,
):
    """Copies files from src to dest for a FileSelect.

    If followlinks is True (default), follows linked directories when
    copying the tree.

    A file select spec may be specified to control the copy process. The
    select determines if a directory is scanned and whether or not
    scanned files are copied.

    A handler may be specified to implement the copy logic, including
    logging and handling ignored files.
    """
    if select and select.disabled:
        return
    handler = handler or FileCopyHandler()
    try:
        _copytree_impl(src, dest, select, handler, followlinks)
    finally:
        handler.close()


def _copytree_impl(
    src: str,
    dest: str,
    select: FileSelect | None,
    handler: FileCopyHandler,
    followlinks: bool,
):
    for root, dirs, files in os.walk(src, followlinks=followlinks):
        dirs.sort()
        relroot = _relpath(root, src)
        pruned = _prune_dirs(src, relroot, select, dirs)
        for name, select_results in pruned:
            handler.ignore(os.path.join(root, name), select_results)
        for name in sorted(files):
            selected, file_src, file_dest, select_results = _select_file_for_copy(
                src, relroot, name, dest, select
            )
            if selected:
                assert file_dest
                handler.copy(file_src, file_dest, select_results)
            else:
                handler.ignore(file_src, select_results)


def _relpath(path: str, start: str):
    if path == start:
        return ""
    return os.path.relpath(path, start)


def _prune_dirs(
    src: str,
    relroot: str,
    select: FileSelect | None,
    dirs: list[str],
) -> list[tuple[str, FileSelectResults]]:
    if not select:
        return []
    return select.prune_dirs(src, relroot, dirs) if select else []


def _select_file_for_copy(
    src_root: str,
    relroot: str,
    name: str,
    dest_root: str,
    select: FileSelect | None,
) -> tuple[bool, str, str | None, FileSelectResults | None]:
    relpath = os.path.join(relroot, name)
    file_src = os.path.join(src_root, relroot, name)
    if not select:
        return True, file_src, os.path.join(dest_root, relroot, name), None
    selected, results = select.select_file(src_root, relpath)
    if selected:
        return True, file_src, os.path.join(dest_root, relroot, name), results
    return False, file_src, None, results