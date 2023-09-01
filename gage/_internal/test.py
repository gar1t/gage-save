# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

# import codecs
# import doctest
import fnmatch

# import glob
import errno

# import filecmp
# import json
import os

# import platform
# import pprint
# import queue
import re

# import shutil
import signal
import subprocess
import sys
import tempfile
import threading

# import time

# import yaml

import gage

# from . import ansi_util
# from . import cli
from . import config
from . import file_util
from . import util

# from . import yaml_util

__all__ = [
    "LogCapture",
    "SysPath",
    "basename",
    "cat",
    "cd",
    "find",
    "findl",
    "mkdtemp",
    "normlf",
    "parse_path",
    "parse_any",
    "parse_ver",
    "path",
    "quiet",
    "run",
    "sample",
    "samples_dir",
    "set_var_home",
    "symlink",
    "touch",
    "use_example",
    "use_project",
    "write",
]


def parse_type(name: str, pattern: str, group_count: int = 0):
    def decorator(f: Callable[[str], Any]):
        f.type_name = name
        f.pattern = pattern
        f.regex_group_count = group_count
        return f

    return decorator


@parse_type("any", r"[^\n]+")
def parse_any(s: str):
    return s


# Simplified https://regex101.com/r/Ly7O1x/3/
VER_PATTERN = (
    r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))?"
)

__ver_pattern_compiled = re.compile(VER_PATTERN)


@parse_type("ver", VER_PATTERN, 3)
def parse_ver(s: str):
    m = __ver_pattern_compiled.match(s)
    if not m:
        return None
    return m.groups()


@parse_type("path", r"/.*")
def parse_path(s: str):
    return s


# PLATFORM = platform.system()

# TEST_NAME_WIDTH = 27

# FIXME = doctest.register_optionflag("FIXME")
# FIXME_CI = doctest.register_optionflag("FIXME_CI")
# FIXME_WINDOWS = doctest.register_optionflag("FIXME_WINDOWS")
# GIT_LS_FILES_TARGET = doctest.register_optionflag("GIT_LS_FILES_TARGET")
# KEEP_LF = doctest.register_optionflag("KEEP_LF")
# MACOS = doctest.register_optionflag("MACOS")
# NORMALIZE_PATHS = doctest.register_optionflag("NORMALIZE_PATHS")
# NORMALIZE_PATHSEP = doctest.register_optionflag("NORMALIZE_PATHSEP")
# TIMING_CRITICAL = doctest.register_optionflag("TIMING_CRITICAL")
# PY3 = doctest.register_optionflag("PY3")
# PY310 = doctest.register_optionflag("PY310")
# PY311 = doctest.register_optionflag("PY311")
# PY37 = doctest.register_optionflag("PY37")
# PY38 = doctest.register_optionflag("PY38")
# PY39 = doctest.register_optionflag("PY39")
# R = doctest.register_optionflag("R")
# STRICT = doctest.register_optionflag("STRICT")
# STRIP_ANSI_FMT = doctest.register_optionflag("STRIP_ANSI_FMT")
# STRIP_EXIT_0 = doctest.register_optionflag("STRIP_EXIT_0")
# WINDOWS = doctest.register_optionflag("WINDOWS")
# WINDOWS_ONLY = doctest.register_optionflag("WINDOWS_ONLY")

# DEFAULT_TIMING_MIN_CPUS = 4

# _Options = Dict[int, bool]


# def run_all_tests(
#     skip: Optional[List[str]] = None,
#     fail_fast: bool = False,
#     force: bool = False,
#     concurrency: Optional[int] = None,
# ):
#     return run_tests(
#         all_tests(),
#         skip=skip,
#         fail_fast=fail_fast,
#         concurrency=concurrency,
#         force=force,
#     )


# def all_tests():
#     test_pattern = os.path.join(tests_dir(), "*.md")
#     return sorted([_test_name_for_path(path) for path in glob.glob(test_pattern)])


def tests_dir():
    return os.path.join(gage.__pkgdir__, "tests")


# def _test_name_for_path(path: str):
#     name, _ext = os.path.splitext(os.path.basename(path))
#     return name


# def run_tests(
#     tests: List[str],
#     skip: Optional[List[str]] = None,
#     fail_fast: bool = False,
#     force: bool = False,
#     concurrency: Optional[int] = None,
# ):
#     if concurrency and concurrency > 1:
#         return _run_tests_parallel(tests, skip, fail_fast, force, concurrency)
#     return _run_tests(tests, skip, fail_fast, force)


# def _run_tests(
#     tests: List[str],
#     skip: Optional[List[str]],
#     fail_fast: bool,
#     force: bool,
# ):
#     skip = skip or []
#     success = True
#     for test in tests:
#         if test not in skip:
#             run_success = _run_test(test, fail_fast, force)
#             success &= run_success
#         else:
#             sys.stdout.write(_test_skipped_output(test))
#     return success


# def _test_skipped_output(test: str):
#     return f"  {test}:{' ' * (TEST_NAME_WIDTH - len(test))} skipped\n"


# def _run_test(name: str, fail_fast: bool, force: bool):
#     sys.stdout.write(f"  {name}: ")
#     sys.stdout.flush()
#     filename = _filename_for_test(name)
#     if not os.path.exists(filename):
#         _log_test_not_found(name)
#         return False
#     if (
#         not force
#         and os.getenv("FORCE_TEST") != "1"
#         and front_matter_skip_test(filename)
#     ):
#         _log_skipped_test(name)
#         return True
#     try:
#         failures, _tests = run_test_file(filename, fail_fast=fail_fast)
#     except IOError:
#         _log_test_not_found(name)
#         return False
#     except RuntimeError as e:
#         _log_general_error(name, e)
#         return False
#     else:
#         if not failures:
#             _log_test_ok(name)
#         return failures == 0


# def _filename_for_test(name_or_path: str):
#     if os.path.sep in name_or_path or "." in name_or_path:
#         return os.path.abspath(name_or_path)
#     return _named_test_filename(name_or_path)


# def _named_test_filename(name: str):
#     return _resolve_relative_test_filename(os.path.join("tests", name + ".md"))


# def _resolve_relative_test_filename(filename: str):
#     if os.path.isabs(filename):
#         return filename
#     package = doctest._normalize_module(None, 3)  # type: ignore
#     return cast(str, doctest._module_relative_path(package, filename))  # type: ignore


# def front_matter_skip_test(filename: str):
#     filename = _resolve_relative_test_filename(filename)
#     fm = yaml_util.yaml_front_matter(filename)
#     options = _parse_doctest_options(fm.get("doctest"), filename)
#     return options and _skip_for_doctest_options(options) is True


# def _parse_doctest_options(encoded_options: str, filename: str) -> _Options:
#     if not encoded_options:
#         return {}
#     parser = doctest.DocTestParser()
#     parser._OPTION_DIRECTIVE_RE = re.compile(r"([^\n'\"]*)$", re.MULTILINE)  # type: ignore
#     return parser._find_options(encoded_options, filename, 1)  # type: ignore


# def _skip_for_doctest_options(options: _Options):
#     return util.any_apply(
#         [
#             _skip_fixme,
#             _skip_platform,
#             _skip_python_version,
#             _skip_timing_critical,
#             # _skip_git_ls_files_target,
#         ],
#         options,
#     )


# def _skip_platform(options: _Options):
#     is_windows = PLATFORM == "Windows"
#     is_macos = PLATFORM == "Darwin"
#     if options.get(WINDOWS) is False and is_windows:
#         return True
#     if options.get(WINDOWS_ONLY) is True and not is_windows:
#         return True
#     if options.get(MACOS) is False and is_macos:
#         return True
#     return None


# def _skip_python_version(options: _Options):
#     py_major_ver = sys.version_info[0]
#     py_minor_ver = sys.version_info[1]
#     skip = None
#     # All Python 3 targets are enabled by default - check if
#     # explicitly disabled
#     if options.get(PY3) is False and py_major_ver == 3:
#         skip = True
#     # Force tests on/off if more specific Python versions specified.
#     for opt, maj_ver, min_ver in [
#         (options.get(PY37), 3, 7),
#         (options.get(PY38), 3, 8),
#         (options.get(PY39), 3, 9),
#         (options.get(PY310), 3, 10),
#         (options.get(PY311), 3, 11),
#     ]:
#         if opt in (True, False) and py_major_ver == maj_ver and py_minor_ver == min_ver:
#             skip = not opt
#     return skip


# def _skip_fixme(options: _Options):
#     return (
#         options.get(FIXME) is True
#         or (options.get(FIXME_CI) is True and _running_under_ci())
#         or (options.get(FIXME_WINDOWS) is True and PLATFORM == "Windows")
#     )


# def _running_under_ci():
#     return os.getenv("gage_CI") == "1"


# def _skip_timing_critical(options: _Options):
#     """Skips tests that rely on a performant system to test timings.

#     Performance threshold is measured by CPU cores, as returned by
#     `os.cpu_count()`. The minimum number of cores for a performant
#     system can be configured using the environment variable
#     `TIMING_MIN_CPUS`.
#     """
#     opt = options.get(TIMING_CRITICAL)
#     if opt is None:
#         return False
#     return opt != _is_performant_system()


# def _is_performant_system():
#     min_cpus = util.get_env("TIMING_MIN_CPUS", int, DEFAULT_TIMING_MIN_CPUS)
#     return os.cpu_count() >= min_cpus


# # def _skip_git_ls_files_target(options):
# #     """Skips test if system Git does not support ls-files target behavior.

# #     Earlier versions of Git do no support a behavior that gage relies
# #     on for source code detection optimization. Tests that exerise this
# #     behavior can use the option `GIT_LS_FILES_TARGET` to skip tests
# #     that don't apply to the current version of Git.
# #     """
# #     opt = options.get(GIT_LS_FILES_TARGET)
# #     if opt is None:
# #         return False
# #     return opt != _git_ls_files_is_target()


# # def _git_ls_files_is_target():
# #     from . import vcs_util

# #     return vcs_util.git_version() >= vcs_util.GIT_LS_FILES_TARGET_VER


# def _log_skipped_test(name: str):
#     sys.stdout.write(" " * (TEST_NAME_WIDTH - len(name)))
#     if os.getenv("NO_SKIPPED_MSG") == "1":
#         sys.stdout.write("ok\n")
#     else:
#         sys.stdout.write("ok (skipped)\n")
#     sys.stdout.flush()


# def _log_test_not_found(name: str):
#     sys.stdout.write(" " * (TEST_NAME_WIDTH - len(name)))
#     sys.stdout.write(cli.style("TEST NOT FOUND\n", fg="red"))
#     sys.stdout.flush()


# def _log_test_ok(name: str):
#     sys.stdout.write(" " * (TEST_NAME_WIDTH - len(name)))
#     sys.stdout.write("ok\n")
#     sys.stdout.flush()


# def _log_general_error(name: str, error: Exception):
#     sys.stdout.write(" " * (TEST_NAME_WIDTH - len(name)))
#     sys.stdout.write(cli.style(f"ERROR ({error})\n", fg="red"))
#     sys.stdout.flush()


# _Globs = Dict[str, Any]


# def run_test_file(
#     filename: str, globs: Optional[_Globs] = None, fail_fast: bool = False
# ):
#     filename = _resolve_relative_test_filename(filename)
#     globs = globs or test_globals()
#     return run_test_file_with_config(
#         filename,
#         globs=globs,
#         optionflags=(
#             _fail_fast_flag(fail_fast)
#             | _report_first_flag()
#             | doctest.ELLIPSIS
#             | doctest.NORMALIZE_WHITESPACE
#             | NORMALIZE_PATHS
#             | WINDOWS
#             | STRIP_ANSI_FMT
#             | STRIP_EXIT_0
#         ),
#     )


# def _fail_fast_flag(fail_fast: Optional[bool]):
#     if fail_fast:
#         return doctest.FAIL_FAST
#     return 0


# def _report_first_flag():
#     if os.getenv("REPORT_ONLY_FIRST_FAILURE") == "1":
#         return doctest.REPORT_ONLY_FIRST_FAILURE
#     return 0


# class Checker(doctest.OutputChecker):
#     """gage ML test checker

#     Transforms got and want for tests based:

#     - Remove ANSI formatting (disable with `-STRIP_ANSI_FMT`
#     - Normalizes paths on Windows (disable with `-NORMALIZE_PATHS`
#     - Support 'leading wildcard' of "???" as "..." is treated as block
#       continuation

#     Optional transforms, enabled with `+<option>`:

#     - `+NORMALIZE_PATHSEP` - Replace '::' with with platform specific
#       path sep char

#     All transforms including ELLIPSIS support are disabled with
#     `+STRICT`.

#     Default doctest checker options enabled by default:

#     - doctest.ELLIPSIS
#     - doctest.NORMALIZE_WHITESPACE

#     The option `doctest.REPORT_ONLY_FIRST_FAILURE` may be enabled
#     globally for tests by setting the `REPORT_ONLY_FIRST_FAILURE`
#     environment variable to `1`.

#     """

#     def check_output(self, want: str, got: str, optionflags: int):
#         if optionflags & STRICT:
#             optionflags -= optionflags & doctest.ELLIPSIS
#         else:
#             got = self._got(got, optionflags)
#             want = self._want(want, optionflags)
#         return doctest.OutputChecker.check_output(self, want, got, optionflags)

#     def _got(self, got: str, optionflags: int):
#         if optionflags & STRICT:
#             return got
#         if PLATFORM == "Windows" and optionflags & NORMALIZE_PATHS:
#             got = _windows_normalize_paths(got)
#         if optionflags & STRIP_ANSI_FMT:
#             got = ansi_util.strip_ansi_format(got)
#         if optionflags & STRIP_EXIT_0:
#             got = _strip_exit_0(got)
#         return got

#     def _want(self, want: str, optionflags: int):
#         if optionflags & STRICT:
#             return want
#         if optionflags & NORMALIZE_PATHSEP:
#             want = _normalize_pathsep(want)
#         want = _leading_wildcard_want(want)
#         if optionflags & STRIP_EXIT_0:
#             want = _strip_exit_0(want)
#         return want


# def _strip_exit_0(s: str):
#     """Removes trailing '\n<exit 0>' from s.

#     Use to optionally omit `<exit 0>` at the end of run output that is
#     expected to succed.
#     """
#     if s.endswith("\n<exit 0>\n"):
#         return s[:-9]
#     return s


# def _windows_normalize_paths(s: str):
#     return re.sub(r"[c-zC-Z]:\\\\?|\\\\?", "/", s)


# def _normalize_pathsep(s: str):
#     return s.replace("::", os.path.pathsep)


# def _leading_wildcard_want(want: str):
#     # Treat leading "???" like "..." (work around for "..." as code
#     # continuation token in doctest)
#     return re.sub(r"^\?\?\?", "...", want)


# _Out = Callable[[str], None]


# class TestRunner(doctest.DocTestRunner):
#     def __init__(
#         self,
#         checker: Optional[doctest.OutputChecker] = None,
#         verbose: Optional[bool] = None,
#         optionflags: int = 0,
#     ):
#         super().__init__(checker, verbose, optionflags)
#         self.skipped = 0

#     def run(
#         self,
#         test: doctest.DocTest,
#         compileflags: Optional[int] = None,
#         out: Optional[_Out] = None,
#         clear_globs: bool = True,
#     ):
#         self._apply_skip(test)
#         super().run(test, compileflags, out, clear_globs)

#     @staticmethod
#     def _apply_skip(test: doctest.DocTest):
#         for example in test.examples:
#             skip = _skip_for_doctest_options(example.options)
#             if skip is not None:
#                 example.options[doctest.SKIP] = skip


# def run_test_file_with_config(filename: str, globs: _Globs, optionflags: int):
#     test_dir = os.path.dirname(filename)
#     with _safe_chdir(test_dir):
#         return _run_test_file_with_config(filename, globs, optionflags)


# def _safe_chdir(dir: str):
#     if not os.path.exists(dir):

#         class NoOp:
#             def __enter__(self):
#                 pass

#             def __exit__(self, *_args: Any):
#                 pass

#         return NoOp()

#     return util.Chdir(dir)


# def _run_test_file_with_config(filename: str, globs: _Globs, optionflags: int):
#     """Modified from doctest.py to use custom checker."""
#     fm = yaml_util.yaml_front_matter(filename)
#     doctest_type = fm.get("doctest-type", "python")
#     if doctest_type == "python":
#         return _run_python_doctest(filename, globs, optionflags)
#     if doctest_type == "bash":
#         return _run_bash_doctest(filename, globs, optionflags)
#     raise RuntimeError(f"unsupported doctest type '{doctest_type}'")


# def _run_python_doctest(filename: str, globs: _Globs, optionflags: int):
#     return _gen_run_doctest(filename, globs, optionflags)


# def _gen_run_doctest(
#     filename: str,
#     globs: _Globs,
#     optionflags: int,
#     parser: Optional[doctest.DocTestParser] = None,
#     checker: Optional[doctest.OutputChecker] = None,
# ):
#     parser = parser or doctest.DocTestParser()
#     text, filename = _load_testfile(filename)
#     name = os.path.basename(filename)
#     if globs is None:
#         globs = {}
#     else:
#         globs = globs.copy()
#     if "__name__" not in globs:
#         globs["__name__"] = "__main__"
#     checker = checker or Checker()
#     runner = TestRunner(checker=checker, verbose=None, optionflags=optionflags)
#     try:
#         test = parser.get_doctest(text, globs, name, filename, 0)
#     except ValueError as e:
#         return _handle_doctest_value_error(e, name, filename)
#     else:
#         runner.run(test)
#         results = runner.summarize()
#         if doctest.master is None:
#             doctest.master = runner
#         else:
#             doctest.master.merge(runner)
#         return results


# def _handle_doctest_value_error(e: ValueError, name: str, filename: str):
#     print("*" * 70)
#     m = re.match(r"line (\d+) of the doctest for", str(e))
#     if m:
#         print(f"File \"{filename}\", line {m.group(1)}, in {name}")
#     print(e)
#     print("*" * 70)
#     return 1, 0


# class BashDocTestParser(doctest.DocTestParser):
#     """Hacked DocTestParser to support running bash commands.

#     Uses `$` as the prompt and `>` as a continuation char.

#     Wraps examples in `run("<example>")` to run them as shell
#     commands.
#     """

#     _EXAMPLE_RE = re.compile(
#         r"""
#         # Source consists of a PS1 line followed by zero or more PS2 lines.
#         (?P<source>
#             (?:^(?P<indent> [ ]{4}) \$    .*) # PS1 line
#             (?:\n           [ ]{4}  > .*)*)   # PS2 lines
#         \n?
#         # Want consists of any non-blank lines that do not start with PS1.
#         (?P<want> (?:(?![ ]*$)    # Not a blank line
#                      (?![ ]*>>>)  # Not a line starting with PS1
#                      .+$\n?       # But any other line
#                   )*)
#         """,
#         re.MULTILINE | re.VERBOSE,
#     )

#     def _parse_example(
#         self, m: Match[str], name: str, lineno: int
#     ) -> Tuple[str, _Options, str, Optional[str]]:
#         indent = len(m.group("indent"))

#         source_lines = m.group("source").split("\n")
#         _check_prompt_blank(source_lines, indent, name, lineno)
#         self._check_prefix(source_lines[1:], " " * indent + ">", name, lineno)  # type: ignore
#         source = "\n".join([sl[indent + 2 :] for sl in source_lines])

#         want = m.group("want")
#         want_lines = want.split("\n")
#         if len(want_lines) > 1 and re.match(r" *$", want_lines[-1]):
#             del want_lines[-1]  # forget final newline & spaces after it
#         self._check_prefix(want_lines, " " * indent, name, lineno + len(source_lines))  # type: ignore
#         want = "\n".join([wl[indent:] for wl in want_lines])

#         m = self._EXCEPTION_RE.match(want)  # type: ignore
#         if m:
#             exc_msg = m.group("msg")
#         else:
#             exc_msg = None
#         options = cast(_Options, self._find_options(source, name, lineno))  # type: ignore
#         return _wrap_bash(source, options), options, want, exc_msg


# def _wrap_bash(source: str, options: _Options):
#     if source.startswith("cd "):
#         return _cd_from_bash(source)
#     if source.startswith("export "):
#         return _set_bash_env_from_bash(source)
#     if source.startswith("unset "):
#         return _unset_bash_env_from_bash(source)
#     if not options.get(KEEP_LF):
#         source = source.replace("\n", " ")
#     return _run_from_bash(source)


# def _cd_from_bash(source: str):
#     assert source.startswith("cd ")
#     return f"cd(\"{source[3:]}\")"


# def _set_bash_env_from_bash(source: str):
#     assert source.startswith("export ")
#     parts = source[7:].split("=", 1)
#     assert len(parts) == 2, source
#     env_name, env_val = parts
#     return f"_bash_env[\"{env_name}\"] = \"{env_val}\""


# def _unset_bash_env_from_bash(source: str):
#     assert source.startswith("unset ")
#     return f"_ = _bash_env.pop(\"{source[6:]}\", None)"


# def _run_from_bash(source: str):
#     source = source.replace('"', '\\"')
#     return f"run(\"\"\"{source}\"\"\", env=_bash_env)"


# def _check_prompt_blank(lines: List[str], indent: int, name: str, lineno: int, *_: Any):
#     for i, line in enumerate(lines):
#         if len(line) >= indent + 2 and line[indent + 1] != " ":
#             raise ValueError(
#                 f"line {lineno + i + 1} of the docstring for {name} "
#                 f"lacks blank after {line[indent : indent + 1]}: {line!r}"
#             )


# class BashDocTestChecker(doctest.OutputChecker):
#     def check_output(self, want: str, got: str, optionflags: int):
#         got = self._normalize_exit_0(want, got)
#         want = _leading_wildcard_want(want)
#         return doctest.OutputChecker.check_output(self, want, got, optionflags)

#     @staticmethod
#     def _normalize_exit_0(want: str, got: str):
#         want = want.rstrip()
#         got = got.rstrip()
#         if got.endswith("\n<exit 0>") and not want.endswith("\n<exit 0>"):
#             return got[:-9]
#         if got == "<exit 0>" and want == "":
#             return ""
#         return got


# def _run_bash_doctest(filename: str, globs: _Globs, optionflags: int):
#     parser = BashDocTestParser()
#     checker = BashDocTestChecker()
#     return _gen_run_doctest(filename, globs, optionflags, parser, checker)


# def _load_testfile(filename: str) -> Tuple[str, str]:
#     # Copied from Python 3.6 doctest._load_testfile to ensure consistent
#     # interface.
#     package = doctest._normalize_module(None, 3)  # type: ignore
#     if getattr(package, "__loader__", None) is not None:
#         if hasattr(package.__loader__, "get_data"):
#             file_contents_raw: bytes = package.__loader__.get_data(filename)  # type: ignore
#             file_contents: str = file_contents_raw.decode("utf-8")
#             return file_contents.replace(os.linesep, "\n"), filename
#     with codecs.open(filename, encoding="utf-8") as f:
#         return f.read(), filename


# def test_globals() -> Dict[str, Any]:
#     return {
#         "_dir": _py_dir,
#         "_bash_env": {},
#         "PLATFORM": PLATFORM,
#         "Chdir": util.Chdir,
#         "Env": util.Env,
#         "Ignore": _Ignore,
#         "LogCapture": util.LogCapture,
#         # "ModelPath": ModelPath,
#         "Platform": _Platform,
#         "PrintStderr": PrintStderr,
#         # "RunError": gapi.RunError,
#         # "SetCwd": config.SetCwd,
#         # "SetGuildHome": config.SetGuildHome,
#         # "SetUserConfig": config.SetUserConfig,
#         "StderrCapture": util.StderrCapture,
#         "SysPath": SysPath,
#         "TempFile": util.TempFile,
#         # "UserConfig": UserConfig,
#         "abspath": os.path.abspath,
#         "basename": os.path.basename,
#         "cat": cat,
#         "cat_json": cat_json,
#         "cli": cli,
#         "compare_dirs": _compare_dirs,
#         "compare_paths": util.compare_paths,
#         "copyfile": copyfile,
#         "copytree": util.copytree,
#         "cd": _chdir,
#         "cwd": os.getcwd,
#         "diff": _diff,
#         "dir": dir,
#         "dirname": os.path.dirname,
#         "ensure_dir": util.ensure_dir,
#         "exists": os.path.exists,
#         "example": _example,
#         "examples_dir": _examples_dir,
#         "find": find,
#         "findl": file_util.find,
#         # "guild_home": config.guild_home,
#         # "guild": guild,
#         # "guildfile": guildfile,
#         "isdir": os.path.isdir,
#         "isfile": os.path.isfile,
#         "islink": os.path.islink,
#         "join_path": os.path.join,
#         "json": json,
#         "make_executable": util.make_executable,
#         "mkdir": os.mkdir,
#         "mkdtemp": mkdtemp,
#         # "mktemp_guild_dir": mktemp_guild_dir,
#         "normlf": _normlf,
#         "not_used": object(),  # an uncooperative value
#         "os": os,
#         "path": os.path.join,
#         # "print_runs": _print_runs,
#         "printl": _printl,
#         "pprint": pprint.pprint,
#         "quiet": lambda cmd, **kw: _run_cmd(cmd, quiet=True, **kw),
#         "re": re,
#         "realpath": util.realpath,
#         "relpath": os.path.relpath,
#         "rm": _rm,
#         "rmdir": util.safe_rmtree,
#         "run": _run_cmd,
#         "run_capture": _run_cmd_capture,
#         "sample": sample,
#         # "samples_dir": samples_dir,
#         "set_var_home": _set_var_home,
#         "sha256": util.file_sha256,
#         "shlex_quote": util.shlex_quote,
#         "sleep": time.sleep,
#         "symlink": os.symlink,
#         "sys": sys,
#         "tests_dir": tests_dir,
#         "touch": util.touch,
#         "use_project": use_project,
#         "which": util.which,
#         "write": write,
#         "yaml": yaml,
#     }


LogCapture = util.LogCapture

basename = os.path.basename
findl = file_util.find
path = os.path.join
symlink = os.symlink
touch = util.touch


def sample(*parts: str):
    return os.path.join(*(samples_dir(),) + parts)


def samples_dir():
    return os.path.join(tests_dir(), "samples")


def mkdtemp(prefix: str = "gage-test-"):
    return tempfile.mkdtemp(prefix=prefix)


# # def mktemp_guild_dir():
# #     guild_dir = mkdtemp()
# #     init.init_guild_dir(guild_dir)
# #     return guild_dir

FindIgnore = Union[str, List[str]]


def find(
    root: str,
    followlinks: bool = False,
    includedirs: bool = False,
    ignore: Optional[FindIgnore] = None,
):
    import natsort

    paths = file_util.find(root, followlinks, includedirs)
    if ignore:
        paths = _filter_ignored(paths, ignore)
    paths = _standarize_paths(paths)
    paths.sort(key=natsort.natsort_key)
    if not paths:
        print("<empty>")
    else:
        for path in paths:
            print(path)


def _filter_ignored(paths: List[str], ignore: Union[str, List[str]]):
    if isinstance(ignore, str):
        ignore = [ignore]
    return [
        p for p in paths if not any((fnmatch.fnmatch(p, pattern) for pattern in ignore))
    ]


def _standarize_paths(paths: List[str]):
    return [util.stdpath(path) for path in paths]


# def _diff(path1: str, path2: str):
#     import difflib

#     lines1 = [s.rstrip() for s in open(path1).readlines()]
#     lines2 = [s.rstrip() for s in open(path2).readlines()]
#     for line in difflib.unified_diff(lines1, lines2, path1, path2, lineterm=""):
#         print(line)


def cat(*parts: str):
    with open(os.path.join(*parts), "r") as f:
        s = f.read()
        if not s:
            print("<empty>")
        else:
            if s[-1:] == "\n":
                s = s[:-1]
            print(s)


# def cat_json(*parts: str):
#     # pylint: disable=no-value-for-parameter
#     with open(os.path.join(*parts), "r") as f:
#         data = json.load(f)
#         json.dump(data, sys.stdout, sort_keys=True, indent=4, separators=(",", ": "))


# _py_dir = dir


# def dir(path: str = ".", ignore: Optional[List[str]] = None):
#     return sorted(
#         [
#             name
#             for name in os.listdir(path)
#             if ignore is None or not any((fnmatch.fnmatch(name, p) for p in ignore))
#         ]
#     )


# def copyfile(*args: Any, **kw: Any):
#     shutil.copy2(*args, **kw)


# def PrintStderr():
#     return util.StderrCapture(autoprint=True)


def write(filename: str, contents: str, append: bool = False):
    encoded = contents.encode()
    opts = "ab" if append else "wb"
    with open(filename, opts) as f:
        f.write(encoded)


class SysPath:
    _sys_path0 = None

    def __init__(
        self,
        path: Optional[List[str]] = None,
        prepend: Optional[List[str]] = None,
        append: Optional[List[str]] = None,
    ):
        path = path if path is not None else sys.path
        if prepend:
            path = prepend + path
        if append:
            path = path + append
        self.sys_path = path

    def __enter__(self):
        self._sys_path0 = sys.path
        sys.path = self.sys_path

    def __exit__(self, *exc: Any):
        assert self._sys_path0 is not None
        sys.path = self._sys_path0


# # class ModelPath:
# #     _model_path0 = None

# #     def __init__(self, path):
# #         self.model_path = path

# #     def __enter__(self):
# #         from guild import model

# #         self._model_path0 = model.get_path()
# #         model.set_path(self.model_path)

# #     def __exit__(self, *exc):
# #         from guild import model

# #         assert self._model_path0 is not None
# #         model.set_path(self._model_path0)


# # class _MockConfig:
# #     def __init__(self, data):
# #         self.path = config.user_config_path()
# #         self.data = data

# #     def read(self):
# #         return self.data


# # class UserConfig:
# #     def __init__(self, config):
# #         self._config = _MockConfig(config)

# #     def __enter__(self):
# #         config._user_config = self._config

# #     def __exit__(self, *exc):
# #         # None forces a lazy re-reread from disk, which is the correct
# #         # behavior for a reset here.
# #         config._user_config = None

# # def _patch_py3_exception_detail():
# #     import traceback

# #     format_exception_only = traceback.format_exception_only

# #     def patch(*args):
# #         formatted = format_exception_only(*args)
# #         formatted[-1] = _strip_error_module(formatted[-1])
# #         return formatted

# #     traceback.format_exception_only = patch


# # if sys.version_info[0] > 2:
# #     _patch_py3_exception_detail()


# # def _strip_error_module(last_line):
# #     m = re.match(r"([\w\.]+): (.+)", last_line)
# #     if not m:
# #         return _strip_class_module(last_line)
# #     return f"{_strip_class_module(m.group(1))}: {m.group(2)}"


# # def _strip_class_module(class_name):
# #     return class_name[class_name.rfind(".") + 1:]


def normlf(s: str):
    return s.replace("\r", "")


# def _printl(l: List[Any]):
#     for x in l:
#         print(x)


# def _rm(path: str, force: bool = False):
#     if force and not os.path.exists(path):
#         return
#     os.remove(path)


# def _run_cmd_capture(*args: Any, **kw: Any):
#     return _run_cmd(*args, _capture=True, **kw)


Env = Dict[str, str]


def quiet(cmd: str, **kw: Any):
    run(cmd, quiet=True, **kw)


def run(
    cmd: str,
    quiet: bool = False,
    ignore: Optional[Union[str, List[str]]] = None,
    timeout: int = 3600,
    cwd: Optional[str] = None,
    env: Optional[Env] = None,
    _capture: bool = False,
):
    proc_env = dict(os.environ)
    _apply_venv_bin_path(proc_env)
    if env:
        proc_env.update(env)
    proc_env["SYNC_RUN_OUTPUT"] = "1"
    p = _popen(cmd, proc_env, cwd)
    with _kill_after(p, timeout) as timeout_context:
        try:
            out, err = p.communicate()
        except KeyboardInterrupt:
            # Handler for Ctrl-c - ideally would be an SIGINT handler
            # (see #485)
            timeout_context.kill_now()
            raise
        else:
            assert err is None, err
            exit_code = p.returncode
    if quiet and exit_code == 0:
        return None
    out = out.strip().decode("latin-1")
    if ignore:
        out = _strip_lines(out, ignore)
    if _capture:
        if exit_code != 0:
            assert False, "TODO"
            # raise gapi.RunError((cmd, cwd, proc_env), exit_code, out)
        return out
    if out:
        print(out)
    print(f"↳{exit_code}")
    return None


def _apply_venv_bin_path(env: Dict[str, str]):
    python_bin_dir = os.path.dirname(sys.executable)
    path = env.get("PATH") or ""
    if python_bin_dir not in path:
        env["PATH"] = f"{python_bin_dir}{os.path.pathsep}${path}"


def _popen(cmd: str, env: Env, cwd: Optional[str]):
    if util.get_platform() == "Windows":
        return _popen_win(cmd, env, cwd)
    return _popen_posix(cmd, env, cwd)


def _popen_win(cmd: str, env: Env, cwd: Optional[str]):
    split_cmd = util.shlex_split(util.stdpath(cmd))
    return subprocess.Popen(
        split_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,  # type: ignore Windows only
        env=env,
        cwd=cwd,
    )


def _popen_posix(cmd: str, env: Env, cwd: Optional[str]):
    cmd = f"set -eu && {cmd}"
    return subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        preexec_fn=os.setsid,
        env=env,
        cwd=cwd,
    )


class _kill_after:
    def __init__(self, p: "subprocess.Popen[bytes]", timeout: int):
        self._p = p
        self._timer = threading.Timer(timeout, self._kill)

    def kill_now(self):
        self._kill()

    def _kill(self):
        if util.get_platform() == "Windows":
            self._kill_win()
        else:
            self._kill_posix()

    def _kill_win(self):
        try:
            self._p.send_signal(signal.CTRL_BREAK_EVENT)  # type: ignore Windows only
            self._p.kill()
        except OSError as e:
            if e.errno != errno.ESRCH:  # no such process
                raise

    def _kill_posix(self):
        try:
            os.killpg(os.getpgid(self._p.pid), signal.SIGKILL)
        except OSError as e:
            if e.errno != errno.ESRCH:  # no such process
                raise

    def __enter__(self):
        self._timer.start()
        return self

    def __exit__(self, *exc: Any):
        self._timer.cancel()


def _strip_lines(out: str, patterns: Union[str, List[str]]):
    if isinstance(patterns, str):
        patterns = [patterns]
    stripped_lines = [
        line
        for line in out.split("\n")
        if not any((re.search(p, line) for p in patterns))
    ]
    return "\n".join(stripped_lines)


def cd(s: str):
    os.chdir(os.path.expandvars(s))


def set_var_home(path: str):
    config.set_var_home(path)


# def _compare_dirs(d1: str, d2: str):
#     if not isinstance(d1, tuple) and len(d1) != 2:
#         raise ValueError("d1 must be a tuple of (dir, label)")
#     if not isinstance(d2, tuple) and len(d2) != 2:
#         raise ValueError("d2 must be a tuple of (dir, label)")
#     d1_path, d1_label = d1
#     d2_path, d2_label = d2
#     cmp_dir = mkdtemp()
#     d1_link = os.path.join(cmp_dir, d1_label)
#     os.symlink(os.path.realpath(d1_path), d1_link)
#     d2_link = os.path.join(cmp_dir, d2_label)
#     os.symlink(os.path.realpath(d2_path), d2_link)
#     with util.StdoutCapture() as out:
#         filecmp.dircmp(d1_link, d2_link).report_full_closure()
#     print(out.get_value().replace(cmp_dir, ""), end="")


# # def _print_runs(
# #     runs,
# #     ids=False,
# #     short_ids=False,
# #     flags=False,
# #     labels=False,
# #     tags=False,
# #     status=False,
# #     scalars=False,
# #     index=None,
# # ):
# #     index = index or _index_for_print_runs(scalars)
# #     if scalars:
# #         assert index
# #         index.refresh(runs, ["scalar"])

# #     cols = _cols_for_print_runs(ids, short_ids, flags, labels, tags, status, scalars)
# #     rows = []

# #     for run in runs:
# #         rows.append(
# #             _row_for_print_run(
# #                 run,
# #                 ids,
# #                 short_ids,
# #                 flags,
# #                 labels,
# #                 tags,
# #                 status,
# #                 scalars,
# #                 index,
# #             )
# #         )
# #     cli.table(rows, cols)


# # def _index_for_print_runs(scalars):
# #     if not scalars:
# #         return None

# #     from guild import index as indexlib

# #     return indexlib.RunIndex()


# # def _cols_for_print_runs(ids, short_ids, flags, labels, tags, status, scalars):
# #     cols = ["opspec"]
# #     if ids:
# #         cols.append("id")
# #     if short_ids:
# #         cols.append("short_id")
# #     if flags:
# #         cols.append("flags")
# #     if labels:
# #         cols.append("label")
# #     if tags:
# #         cols.append("tags")
# #     if status:
# #         cols.append("status")
# #     if scalars:
# #         cols.append("scalars")
# #     return cols


# # def _row_for_print_run(
# #     run,
# #     ids,
# #     short_ids,
# #     flags,
# #     labels,
# #     tags,
# #     status,
# #     scalars,
# #     index,
# # ):
# #     from guild.commands import runs_impl

# #     fmt_run = runs_impl.format_run(run)
# #     row = {"opspec": fmt_run["op_desc"]}
# #     if ids:
# #         row["id"] = run.id
# #     if short_ids:
# #         row["short_id"] = run.short_id
# #     if flags:
# #         row["flags"] = _print_run_flags(run)
# #     if labels:
# #         row["label"] = run.get("label")
# #     if tags:
# #         row["tags"] = " ".join(sorted(run.get("tags") or []))
# #     if status:
# #         row["status"] = run.status
# #     if scalars:
# #         row["scalars"] = _print_run_scalars(run, index)
# #     return row


# # def _print_run_flags(run):
# #     flag_vals = run.get("flags") or {}
# #     return op_util.flags_desc(flag_vals, delim=" ")


# # def _print_run_scalars(run, index):
# #     assert index
# #     scalars = index.run_scalars(run)
# #     return " ".join(f"{s['tag']}={s['last_val']:.5f}" for s in scalars)


# class _Platform:
#     _platform_save = None

#     def __init__(self, platform: str):
#         self._platform = platform

#     def __enter__(self):
#         self._platform_save = PLATFORM
#         globals()["PLATFORM"] = self._platform

#     def __exit__(self, *args: Any):
#         globals()["PLATFORM"] = self._platform_save


# class _Ignore(util.StdoutCapture):
#     def __init__(self, ignore_patterns: List[str]):
#         self.ignore_patterns = _compile_ignore_patterns(ignore_patterns)

#     def __exit__(self, *args: Any):
#         super().__exit__(*args)
#         sys.stdout.write(_strip_ignored_lines(self._captured, self.ignore_patterns))


# def _compile_ignore_patterns(patterns: List[str]):
#     if not isinstance(patterns, list):
#         patterns = [patterns]
#     return [re.compile(p) for p in patterns]


# def _strip_ignored_lines(captured: List[str], ignore_patterns: List[Pattern[str]]):
#     lines = "".join(captured).split("\n")
#     filtered = [line for line in lines if not _capture_ignored(line, ignore_patterns)]
#     return "\n".join(filtered)


# def _capture_ignored(s: str, ignore_patterns: List[Pattern[str]]):
#     return any(p.search(s) for p in ignore_patterns)


def use_example(name: str, var_home: Optional[str] = None):
    var_home = var_home or mkdtemp()
    cd(_example(name))
    set_var_home(var_home)


def _example(name: str):
    return os.path.join(_examples_dir(), name)


def _examples_dir():
    try:
        return os.environ["EXAMPLES"]
    except KeyError:
        return os.path.join(gage.__pkgdir__, "examples")


def use_project(project_name: str, var_home: Optional[str] = None):
    var_home = var_home or mkdtemp()
    cd(sample("projects", project_name))
    set_var_home(var_home)


# class _ConcurrentTest:
#     def __init__(self, name: str, skip: bool):
#         self.name = name
#         self.skip = skip
#         self.success = None
#         self.output = None
#         self._done_event = threading.Event()

#     def wait_done(self):
#         self._done_event.wait()

#     def set_done(self, success: bool, output: str):
#         assert success is not None
#         assert output is not None
#         self.success = success
#         self.output = output
#         self._done_event.set()


# def _run_tests_parallel(
#     tests: List[str],
#     skip: Optional[List[str]],
#     fail_fast: Optional[bool],
#     force: Optional[bool],
#     concurrency: Optional[int],
# ) -> bool:
#     skip = skip or []
#     ctests = _init_concurrent_tests(tests, skip or [])
#     test_queue = _init_test_queue([ctest for ctest in ctests if not ctest.skip])
#     test_runners = _init_test_runners(test_queue, fail_fast, force, concurrency)
#     try:
#         success = True
#         for ctest in ctests:
#             if ctest.skip:
#                 sys.stdout.write(_test_skipped_output(ctest.name))
#                 continue
#             ctest.wait_done()
#             assert ctest.output is not None
#             assert ctest.success is not None
#             sys.stdout.write(ctest.output)
#             success &= ctest.success
#         assert test_queue.empty()
#         for runner in test_runners:
#             runner.join()
#         assert all(not r.is_alive() for r in test_runners)
#         return success
#     except (KeyboardInterrupt, Exception):
#         for runner in test_runners:
#             runner.stop()
#         raise


# def _init_concurrent_tests(tests: List[str], skip: List[str]):
#     return [_ConcurrentTest(name, name in skip) for name in tests]


# def _init_test_queue(tests: List[_ConcurrentTest]) -> Queue[_ConcurrentTest]:
#     q = queue.Queue()
#     for test in tests:
#         q.put(test)
#     return q


# def _init_test_runners(
#     test_queue: Queue[_ConcurrentTest],
#     fail_fast: Optional[bool],
#     force: Optional[bool],
#     concurrency: Optional[int],
# ):
#     assert not test_queue.empty()
#     return [
#         _ConcurrentTestRunner(test_queue, fail_fast, force)
#         for _ in range(concurrency or 1)
#     ]


# class _ConcurrentTestRunner(threading.Thread):
#     def __init__(
#         self,
#         test_queue: Queue[_ConcurrentTest],
#         fail_fast: Optional[bool],
#         force: Optional[bool],
#     ):
#         super().__init__()
#         self.test_queue = test_queue
#         self.fail_fast = fail_fast
#         self.force = force
#         self._p_lock = threading.Lock()
#         self._p = None
#         self._running_lock = threading.Lock()
#         self._running = True
#         self.start()

#     @property
#     def running(self):
#         with self._running_lock:
#             return self._running

#     def stop(self, timeout: int = 5):
#         with self._running_lock:
#             self._running = False
#         with self._p_lock:
#             if not self._p:
#                 return
#             self._p.terminate()
#             self._p.wait(timeout)
#             if self._p.returncode is None:
#                 self._p.kill()
#             self._p = None

#     def run(self):
#         while self.running:
#             try:
#                 test = self.test_queue.get(block=False)
#             except queue.Empty:
#                 break
#             else:
#                 try:
#                     with self._p_lock:
#                         assert not self._p
#                         self._p = _start_external_test_proc(
#                             test.name,
#                             self.fail_fast,
#                             self.force,
#                         )
#                     out, _err = self._p.communicate()
#                     assert self._p.returncode is not None
#                     assert out is not None
#                     success = self._p.returncode == 0
#                     out = out.decode()
#                     with self._p_lock:
#                         self._p = None
#                 except AssertionError:
#                     test.set_done(False, "")
#                     raise
#                 except Exception as e:
#                     test.set_done(False, str(e))
#                 else:
#                     test.set_done(success, out)


# def _start_external_test_proc(
#     test_name: str, fail_fast: Optional[bool], force: Optional[bool]
# ):
#     env = dict(os.environ)
#     env["PYTHONPATH"] = gage.__pkgdir__
#     cmd = [
#         sys.executable,
#         "-m",
#         "gage.__main__",
#         "check",
#         "--no-chrome",  # just print test results
#         "-t",
#         test_name,
#     ]
#     if fail_fast:
#         cmd.append("--fast")
#     if force:
#         cmd.append("--force-test")
#     return subprocess.Popen(
#         cmd,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.STDOUT,
#         env=env,
#     )

# Copied from test related code in check

# def _TestEnv(
#     no_vcs_commit: bool = True,
#     no_pip_freeze: bool = True,
#     concurrency: Optional[int] = None,
# ):
#     return util.Env(
#         {
#             "NO_IMPORT_FLAGS_PROGRESS": "1",
#             "COLUMNS": "999",
#             "SYNC_RUN_OUTPUT": "1",
#             "PYTHONDONTWRITEBYTECODE": "1",
#             "CONCURRENCY": str(concurrency or 1),
#             # The following are optimizations for tests. They must be
#             # overridden for any tests that check the disabled behavior.
#             "NO_PIP_FREEZE": "1" if no_pip_freeze else "",
#             "NO_VCS_COMMIT": "1" if no_vcs_commit else "",
#         }
#     )
