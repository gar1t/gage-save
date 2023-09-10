# SPDX-License-Identifier: Apache-2.0

from typing import *

# import logging
# import os
# import platform
# import sys

# import gage

# #import click

# from .. import cli
# from .. import util

# log = logging.getLogger(__name__)


# ATTR_COL_WIDTH = 26


# class Check:
#     def __init__(self, args: Any):
#         self._errors = False
#         # self.offline = self._init_offline(args)
#         self.newer_version_available = False

#     def error(self):
#         self._errors = True

#     @property
#     def has_error(self):
#         return self._errors


def main(**params: Any):
    print(params)
    # _check_impl(args)


# def _check_impl(args: Any):
#     if args.version:
#         _check_version_and_exit(args.version)
#     if args.external:
#         _check_external_and_exit(args)
#     _print_info_and_exit(args)


# def _check_version_and_exit(req: str):
#     try:
#         match = util.check_gage_version(req)
#     except ValueError:
#         cli.error(
#             f"invalid requirement spec '{req}'\n"
#             "See https://bit.ly/45AerAj for more information."
#         )
#     else:
#         if not match:
#             cli.error(
#                 f"version mismatch: current version '{gage.__version__}' "
#                 f"does not match '{req}'"
#             )
#         raise SystemExit(0)


# def _check_external_and_exit(args: Any):
#     if args.external == "git-ls-files":
#         _check_git_ls_files()
#     else:
#         cli.error(f"unsupported external check: {args.external}")


# def _check_git_ls_files():
#     from .. import vcs_util

#     result = vcs_util.check_git_ls_files()
#     if result.error:
#         cli.error(
#             f"git-ls-files NOT OK (git version {result.formatted_git_version}; "
#             f"{result.git_exe})\n{result.error}"
#         )
#     cli.out(
#         f"git-ls-files is ok (git version {result.formatted_git_version}; "
#         f"{result.git_exe})"
#     )
#     sys.exit(0)


# def _print_info_and_exit(args: Any):
#     check = Check(args)
#     _print_guild_info(check)
#     _print_python_info(args, check)
#     _print_platform_info(check)
#     if check.newer_version_available:
#         _notify_newer_version()
#     if not check.has_error:
#         raise SystemExit(0)
#     cli.error(_general_error_msg(args) if not args.no_chrome else None)


# def _print_guild_info(check: Check):
#     _attr("gage_version", gage.__version__)
#     _attr("gage_install_location", _safe_apply(check, _gage_install_location))


# def _attr(name: str, val: int | float | str):
#     padding = (ATTR_COL_WIDTH - len(name)) * " "
#     cli.out(f"{name}:{padding}{val}")


# def _safe_apply(check: Check, f: Callable[..., Any], *args: Any, **kw: Any):
#     """Always return a string for application f(*args, **kw).

#     If f(*args, **kw) fails, returns a highlighted error message and
#     sets error flag on check.
#     """
#     try:
#         return f(*args, **kw)
#     except Exception as e:
#         if log.getEffectiveLevel() <= logging.DEBUG:
#             log.exception("safe call: %r %r %r", f, args, kw)
#         check.error()
#         return _warn(f"ERROR: {e}")


# def _gage_install_location():
#     import pkg_resources

#     return pkg_resources.resource_filename("gage", "")


# def _print_python_info(args: Any, check: Check):
#     _attr("python_version", _safe_apply(check, _python_version))
#     _attr("python_exe", sys.executable)
#     if args.verbose:
#         _attr("python_path", _safe_apply(check, _python_path))


# def _python_version():
#     return sys.version.replace("\n", "")


# def _python_path():
#     return os.path.pathsep.join(sys.path)


# def _print_platform_info(check: Check):
#     _attr("platform", _safe_apply(check, _platform))


# def _platform():
#     system, _node, release, _ver, machine, _proc = platform.uname()
#     return " ".join([system, release, machine])


# def _notify_newer_version():
#     pass
#     # cli.out(
#     #     click.style(
#     #         "A newer version of Gage ML is available. Run "
#     #         "'pip install gageml --upgrade' to install it.",
#     #         bold=True,
#     #     ),
#     #     err=True,
#     # )


# def _general_error_msg(args: Any):
#     msg = (
#         "there are problems with your setup\n"
#         "Refer to the issues above for more information"
#     )
#     if not args.verbose:
#         msg += " or rerun check with the --verbose option."
#     return msg


# def _warn(msg: str):
#     pass
#     # return click.style(msg, fg="red", bold=True)
