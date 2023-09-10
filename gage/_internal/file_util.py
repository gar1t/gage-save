# SPDX-License-Identifier: Apache-2.0

from typing import *

import fnmatch
import glob
import hashlib
import logging
import os
import re
import shutil

from . import util

log = logging.getLogger()

FileSelectRuleType = Literal["text", "binary", "dir"]

_TestFunc = Callable[..., bool | None]


class FileSelectTest:
    def __init__(self, name: str, test_f: _TestFunc, *test_args: Any):
        self.name = name
        self.test_f = test_f
        self.test_args = test_args

    def __call__(self):
        return self.test_f(*self.test_args)


FileSelectTestResult = tuple[Optional[bool], Optional[FileSelectTest]]


class FileSelectRule:
    def __init__(
        self,
        result: bool,
        patterns: list[str],
        type: Optional[FileSelectRuleType] = None,
        regex: bool = False,  # treat patterns as regex otherwise globs
        sentinel: Optional[str] = None,
        size_gt: Optional[int] = None,
        size_lt: Optional[int] = None,
        max_matches: Optional[int] = None,
    ):
        self.result = result
        if isinstance(patterns, str):
            patterns = [patterns]
        if not regex:
            patterns = _native_paths(patterns)
        self.patterns = patterns
        self.regex = regex
        self._patterns_match = self._patterns_match_f(patterns, regex)
        self.type = self._validate_type(type)
        self.sentinel = sentinel
        self.size_gt = size_gt
        self.size_lt = size_lt
        self.max_matches = max_matches
        self._matches = 0

    def __str__(self):
        parts = ["include" if self.result else "exclude"]
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

    def _patterns_match_f(self, patterns: list[str], regex: bool):
        if regex:
            return self._regex_match_f(patterns)
        return self._fnmatch_f(patterns)

    @staticmethod
    def _regex_match_f(patterns: list[str]):
        compiled = [re.compile(p) for p in patterns]

        def f(path: str):
            return any((p.match(util.standardize_path(path)) for p in compiled))

        return f

    @staticmethod
    def _fnmatch_f(patterns: list[str]):
        def f(path: str):
            return any((_fnmatch(path, p) for p in patterns))

        return f

    @staticmethod
    def _validate_type(type: Optional[str]):
        valid = ("text", "binary", "dir")
        if type is not None and type not in valid:
            raise ValueError(
                f"invalid value for type {type!r}: expected one of {', '.join(valid)}"
            )
        return type

    @property
    def matches(self):
        return self._matches

    def test(self, src_root: str, relpath: str) -> FileSelectTestResult:
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
            return self._test_text_file(path)
        if self.type == "binary":
            return self._test_binary_file(path)
        if self.type == "dir":
            return self._test_dir(path)
        assert False, self.type

    @staticmethod
    def _test_text_file(path: str):
        return util.safe_is_text_file(path)

    @staticmethod
    def _test_binary_file(path: str):
        return not util.safe_is_text_file(path)

    def _test_dir(self, path: str):
        if not os.path.isdir(path):
            return False
        if self.sentinel:
            return len(glob.glob(os.path.join(path, self.sentinel))) > 0
        return True

    def _test_size(self, path: str):
        if self.size_gt is None and self.size_lt is None:
            return True
        size = util.safe_filesize(path)
        if size is None:
            return True
        if self.size_gt and size > self.size_gt:
            return True
        if self.size_lt and size < self.size_lt:
            return True
        return False


FileSelectResults = list[tuple[FileSelectTestResult, FileSelectRule]]


class FileSelect:
    def __init__(self, root: Optional[str], rules: list[FileSelectRule]):
        self.root = root
        self.rules = rules
        self._disabled = None

    @property
    def disabled(self):
        if self._disabled is None:
            self._disabled = self._init_disabled()
        return self._disabled

    def _init_disabled(self):
        """Returns True if file select is disabled.

        This is an optimization to disable file select by appending an exclude
        '*' to a rule set.

        Assumes not disabled until finds a disable all pattern (untyped
        match of '*'). Disable pattern can be reset by any include
        pattern.
        """
        disabled = False
        for rule in self.rules:
            if rule.result:
                disabled = False
            elif "*" in rule.patterns and rule.type is None:
                disabled = True
        return disabled

    def select_file(
        self, src_root: str, relpath: str
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
        result, _test = reduce_file_select_results(test_results)
        return result is True, test_results

    def prune_dirs(self, src_root: str, relroot: str, dirs: list[str]):
        pruned: list[str] = []
        for name in sorted(dirs):
            last_rule_result = None
            relpath = os.path.join(relroot, name)
            for rule in self.rules:
                if rule.type != "dir":
                    continue
                rule_result, _test = rule.test(src_root, relpath)
                if rule_result is not None:
                    last_rule_result = rule_result
            if last_rule_result is False:
                log.debug("skipping directory %s", relpath)
                pruned.append(name)
                dirs.remove(name)
        return pruned


def reduce_file_select_results(results: FileSelectResults) -> FileSelectTestResult:
    """Reduces a list of file select results to a single determining result.

    The last non-None result from results is used to determine the reduced
    result, otherwise returns None, None, indicating that the results are
    indeterminate.

    Returns a tuple of result and determining-test.
    """
    for (result, test), _rule in reversed(results):
        if result is not None:
            return result, test
    return None, None


class DisabledFileSelect(FileSelect):
    def __init__(self):
        super().__init__(None, [])

    @property
    def disabled(self):
        return True


def _quote_pattern(s: str):
    return util.shlex_quote(s) if " " in s else s


def _native_paths(patterns: list[str]):
    return [p.replace("/", os.path.sep) for p in patterns]


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


def include(patterns: list[str], **kw: Any):
    return FileSelectRule(True, patterns, **kw)


def exclude(patterns: list[str], **kw: Any):
    return FileSelectRule(False, patterns, **kw)


class FileCopyHandler:
    def __init__(
        self, src_root: str, dest_root: str, select: Optional[FileSelect] = None
    ):
        self.src_root = src_root
        self.dest_root = dest_root
        self.select = select

    def copy(self, path: str, results: Optional[FileSelectResults] = None):
        src = os.path.join(self.src_root, path)
        dest = os.path.join(self.dest_root, path)
        log.debug("copying %s to %s", src, dest)
        util.ensure_dir(os.path.dirname(dest))
        self._try_copy_file(src, dest)

    def _try_copy_file(self, src: str, dest: str):
        try:
            shutil.copyfile(src, dest)
            shutil.copymode(src, dest)
        except IOError as e:
            if e.errno != 2:  # Ignore file not exists
                if not self.handle_copy_error(e, src, dest):
                    raise

    def ignore(self, path: str, results: FileSelectResults):
        pass

    def handle_copy_error(self, e: Exception, src: str, dest: str):
        return False

    def close(self):
        pass


_CopyHandlerType = Type[FileCopyHandler]


def copyfiles(
    src: str,
    dest: str,
    files: list[str],
    handler_cls: Optional[_CopyHandlerType] = None,
):
    # Opportunistic use of FileCopyHandler to copy files. `unused_xxx`
    # vars below signal that we're explicitly not using parts of the
    # FileCopyHandler API.
    handler = (handler_cls or FileCopyHandler)(src, dest)
    for path in files:
        handler.copy(path)


def copytree(
    dest: str,
    select: FileSelect,
    root_start: Optional[str] = None,
    followlinks: bool = True,
    ignore: Optional[list[str]] = None,
    handler_cls: Optional[_CopyHandlerType] = None,
):
    """Copies files to dest for a FileSelect.

    `root_start` is an optional location used to resolve relative
    paths in `select.root`. Defaults to current directory.

    If followlinks is True (the default), follows linked directories
    when copying the tree.

    A handler class may be specified to create a handler of copy
    events. FileCopyHandler is used by default. If specified, the
    class is used to instantiate a handler with `(src, dest,
    select)`. Handler methods `copy()` and `ignore()` are called with
    `(relpath, results)` where `results` is a list of results from
    each rule as `(result, rule)` tuples.

    As an optimization, `copytree` skips evaluation of files if the
    file select is disabled. File selects are disabled if no files can
    be selected for their rules. If select is disabled and a handler
    class is specified, the handler is still instantiated, however, no
    calls to `copy()` or `ignore()` will be made.
    """
    root_start = root_start or os.getcwd()
    src = _copytree_src(root_start, select)
    # Instantiate handler as part of the copytree contract.
    handler = (handler_cls or FileCopyHandler)(src, dest, select)
    try:
        _copytree_impl(src, select, followlinks, ignore or [], handler)
    finally:
        handler.close()


def _copytree_impl(
    src: str,
    select: FileSelect,
    followlinks: bool,
    ignore: list[str],
    copy_handler: FileCopyHandler,
):
    if select.disabled:
        return
    for root, dirs, files in os.walk(src, followlinks=followlinks):
        dirs.sort()
        relroot = _relpath(root, src)
        pruned = select.prune_dirs(src, relroot, dirs)
        for name in pruned:
            relpath = os.path.join(relroot, name)
            copy_handler.ignore(relpath, [])
        for name in sorted(files):
            relpath = os.path.join(relroot, name)
            selected, results = _select_file_to_copy(src, relpath, select, ignore)
            if selected:
                copy_handler.copy(relpath, results)
            else:
                copy_handler.ignore(relpath, results)


def _select_file_to_copy(src: str, relpath: str, select: FileSelect, ignore: list[str]):
    if relpath in ignore:
        return _ignored_path_select_result(relpath)
    return select.select_file(src, relpath)


def _ignored_path_select_result(path: str) -> tuple[bool, FileSelectResults]:
    """Proxies a select result.

    Returns a tuple of select and a select results. Select is false because
    we're explicitly ignoring the path. Results is a list of rules that
    determined the select outcome. In this there's a single False result from a
    matching pattern.
    """
    return False, [((False, None), FileSelectRule(False, [path]))]


def _copytree_src(root_start: str, select: FileSelect):
    assert root_start
    return (
        os.path.normpath(os.path.join(root_start, select.root))
        if select.root
        else root_start
    )


def _relpath(path: str, start: str):
    if path == start:
        return ""
    return os.path.relpath(path, start)


def disk_usage(path: str):
    total = _file_size(path)
    for root, dirs, names in os.walk(path, followlinks=False):
        for name in dirs + names:
            path = os.path.join(root, name)
            total += _file_size(os.path.join(root, name))
    return total


def _file_size(path: str):
    stat = os.lstat if os.path.islink(path) else os.stat
    try:
        return stat(path).st_size
    except (OSError, IOError) as e:
        log.warning("could not read size of %s: %s", path, e)
        return 0


def find(
    root: str,
    followlinks: bool = False,
    includedirs: bool = False,
    unsorted: bool = False,
):
    paths: list[str] = []

    def relpath(path: str, name: str):
        return os.path.relpath(os.path.join(path, name), root)

    for path, dirs, files in os.walk(root, followlinks=followlinks):
        for name in dirs:
            if includedirs or os.path.islink(os.path.join(path, name)):
                paths.append(relpath(path, name))
        for name in files:
            paths.append(relpath(path, name))
    return paths if unsorted else sorted(paths)


def find_up(
    relpath: str,
    start_dir: Optional[str] = None,
    stop_dir: Optional[str] = None,
    check: Callable[[str], bool] = os.path.exists,
):
    start_dir = os.path.abspath(start_dir) if start_dir else os.getcwd()
    stop_dir = util.realpath(stop_dir) if stop_dir else _user_home()

    cur = start_dir
    while True:
        maybe_target = os.path.join(cur, relpath)
        if check(maybe_target):
            return maybe_target
        if util.realpath(cur) == stop_dir:
            return None
        parent = os.path.dirname(cur)
        if parent == cur:
            return None
        cur = parent

    # `parent == cur` above should be the definitive terminal case
    assert False


def _user_home():
    return os.path.expanduser("~")


def expand_path(path: str):
    return os.path.expanduser(os.path.expandvars(path))


def files_differ(path1: str, path2: str):
    if os.stat(path1).st_size != os.stat(path2).st_size:
        return True
    f1 = open(path1, "rb")
    f2 = open(path2, "rb")
    with f1, f2:
        while True:
            buf1 = f1.read(1024)
            buf2 = f2.read(1024)
            if buf1 != buf2:
                return True
            if not buf1 or not buf2:
                break
    return False


def files_digest(paths: list[str], root_dir: str):
    md5 = hashlib.md5()
    for path in paths:
        normpath = _path_for_digest(path)
        md5.update(_encode_file_path_for_digest(normpath))
        md5.update(b"\x00")
        _apply_digest_file_bytes(os.path.join(root_dir, path), md5)
        md5.update(b"\x00")
    return md5.hexdigest()


def _path_for_digest(path: str):
    return path.replace(os.path.sep, "/")


def _encode_file_path_for_digest(path: str):
    return path.encode("UTF-8")


_Digest = Any


def _apply_digest_file_bytes(path: str, d: _Digest):
    buf_size = 1024 * 1024
    with open(path, "rb") as f:
        while True:
            buf = f.read(buf_size)
            if not buf:
                break
            d.update(buf)
