# SPDX-License-Identifier: Apache-2.0

from typing import *

import json
import logging
import os
import platform

# import re
import subprocess
import sys
import warnings

import pkg_resources

import vml

from vml._vendor import click

from vml._internal import test as testlib
from vml._internal import cli

# from vml._internal import config
from vml._internal import file_util

# from vml._internal import plugin
# from vml._internal import uat
from vml._internal import util

# from vml._internal import var

# from . import remote_impl_support

log = logging.getLogger("guild")

# (mod_name, required_flag)
CHECK_MODS = [
    ("click", True),
    ("dask", False),
    ("distutils", False),
    ("numpy", True),
    ("pandas", False),
    ("pip", True),
    ("sklearn", True),
    ("setuptools", True),
    ("twine", False),
    ("yaml", True),
    ("werkzeug", True),
]

ATTR_COL_WIDTH = 26


class Check:
    def __init__(self, args: Any):
        self._errors = False
        # self.offline = self._init_offline(args)
        self.newer_version_available = False

    # @staticmethod
    # def _init_offline(args):
    #     if args.offline is not None:
    #         return args.offline
    #     return _check_config().get("offline")

    def error(self):
        self._errors = True

    @property
    def has_error(self):
        return self._errors


# def _check_config():
#     return config.user_config().get("check") or {}


def main(args: Any):
    if args.remote:
        assert False
        # remote_impl_support.check(args)
    else:
        _check(args)


def _check(args: Any):
    try:
        _check_impl(args)
    except SystemExit as e:
        _maybe_notify(args, e)
        raise
    else:
        _maybe_notify(args)


def _check_impl(args: Any):
    if args.version:
        _check_version_and_exit(args.version)
    if args.external:
        _check_external_and_exit(args)
    # if args.uat or args.force_uat:
    #     _uat_and_exit(args)
    if args.all_tests or args.tests:
        _run_tests_and_exit(args)
    _print_info_and_exit(args)


def _check_version_and_exit(req: str):
    try:
        match = util.check_vml_version(req)
    except ValueError:
        cli.error(
            f"invalid requirement spec '{req}'\n"
            "See https://bit.ly/guild-help-req-spec for more information."
        )
    else:
        if not match:
            cli.error(
                f"version mismatch: current version '{vml.__version__}' "
                f"does not match '{req}'"
            )
        raise SystemExit(0)


def _check_external_and_exit(args: Any):
    if args.external == "git-ls-files":
        assert False, "TODO"
        # _check_git_ls_files()
    else:
        cli.error(f"unsupported external check: {args.external}")


# def _check_git_ls_files():
#     from vml._internal import vcs_util

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


# def _uat_and_exit(args):
#     with _TestEnv(
#         no_vcs_commit=False,
#         no_pip_freeze=False,
#         concurrency=args.concurrency,
#     ):
#         uat.run(force=args.force_uat, fail_fast=args.fast)
#     sys.exit(0)


def _TestEnv(
    no_vcs_commit: bool = True,
    no_pip_freeze: bool = True,
    concurrency: Optional[int] = None,
):
    return util.Env(
        {
            "NO_IMPORT_FLAGS_PROGRESS": "1",
            "COLUMNS": "999",
            "SYNC_RUN_OUTPUT": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
            "CONCURRENCY": str(concurrency or 1),
            # The following are optimizations for tests. They must be
            # overridden for any tests that check the disabled behavior.
            "NO_PIP_FREEZE": "1" if no_pip_freeze else "",
            "NO_VCS_COMMIT": "1" if no_vcs_commit else "",
        }
    )


def _run_tests_and_exit(args: Any):
    with _TestEnv(concurrency=args.concurrency):
        success = _run_tests(args)
    if success:
        raise SystemExit(0)
    cli.error(_tests_failed_msg() if not args.no_chrome else None)


def _run_tests(args: Any):
    if not args.no_chrome:
        sys.stdout.write("internal tests:\n")
    if args.all_tests:
        if args.tests:
            log.warning(
                "running all tests (--all-tests specified) - "
                "ignoring individual tests"
            )
        success = testlib.run_all(
            skip=args.skip,
            fail_fast=args.fast,
            concurrency=args.concurrency,
            force=args.force_test,
        )
    elif args.tests:
        if args.skip:
            log.warning("running individual tests - ignoring --skip")
        success = testlib.run(
            args.tests,
            fail_fast=args.fast,
            concurrency=args.concurrency,
            force=args.force_test,
        )
    else:
        assert False
    return success


def _print_info_and_exit(args: Any):
    check = Check(args)
    _print_guild_info(check)
    _print_python_info(args, check)
    if not args.env:
        _print_platform_info(check)
        # _print_psutil_info(check)
        # _print_tensorboard_info(check)
        # if check.args.r_script:
        #     _print_r_script_info(check)
        # if check.args.tensorflow:
        #     _print_tensorflow_info(check)
        # if check.args.pytorch:
        #     _print_pytorch_info(check)
        # _print_cuda_info(check)
        # _print_nvidia_tools_info(check)
        if args.verbose:
            _print_mods_info(check)
    # _print_guild_latest_versions(check)
    if check.newer_version_available:
        _notify_newer_version()
    if not args.env:
        if args.space:
            _print_disk_usage()
    if not check.has_error:
        raise SystemExit(0)
    cli.error(_general_error_msg(args) if not args.no_chrome else None)


def _print_guild_info(check: Check):
    _attr("vistaml_version", vml.__version__)
    _attr("vistaml_install_location", _safe_apply(check, _vistaml_install_location))
    # _attr("vistaml_home", _safe_apply(check, config.guild_home))
    # _attr("vistaml_resource_cache", _safe_apply(check, _guild_resource_cache))
    # if not check.args.env:
    #     _attr("installed_plugins", _safe_apply(check, _format_plugins))


def _attr(name: str, val: Union[int, float, str]):
    padding = (ATTR_COL_WIDTH - len(name)) * " "
    cli.out(f"{name}:{padding}{val}")


def _safe_apply(check: Check, f: Callable[..., Any], *args: Any, **kw: Any):
    """Always return a string for application f(*args, **kw).

    If f(*args, **kw) fails, returns a higlighted error message and
    sets error flag on check.
    """
    try:
        return f(*args, **kw)
    except Exception as e:
        if log.getEffectiveLevel() <= logging.DEBUG:
            log.exception("safe call: %r %r %r", f, args, kw)
        check.error()
        return _warn(f"ERROR: {e}")


def _vistaml_install_location():
    return pkg_resources.resource_filename("vml", "")


# def _guild_resource_cache():
#     return util.realpath(var.cache_dir("resources"))


# def _format_plugins():
#     names = {name for name, _ in plugin.iter_plugins()}
#     return ", ".join(sorted(names))


def _print_python_info(args: Any, check: Check):
    _attr("python_version", _safe_apply(check, _python_version))
    _attr("python_exe", sys.executable)
    if args.verbose:
        _attr("python_path", _safe_apply(check, _python_path))


def _python_version():
    return sys.version.replace("\n", "")


def _python_path():
    return os.path.pathsep.join(sys.path)


def _print_platform_info(check: Check):
    _attr("platform", _safe_apply(check, _platform))


def _platform():
    system, _node, release, _ver, machine, _proc = platform.uname()
    return " ".join([system, release, machine])


# def _print_psutil_info(check):
#     ver = _try_module_version("psutil", check)
#     _attr("psutil_version", ver)


# def _print_tensorboard_info(check):
#     _attr("tensorboard_version", _safe_apply(check, _tensorboard_version, check))


# def _tensorboard_version(check):
#     try:
#         from tensorboard import version
#     except ImportError:
#         if log.getEffectiveLevel() <= logging.DEBUG:
#             log.exception("tensorboard version")
#         check.error()  # TB is required
#         return _warn("not installed")
#     else:
#         return version.VERSION


# def _print_r_script_info(check):
#     from vml._internal.plugins import r_util

#     _attr("rscript_version", _safe_apply(check, r_util.r_script_version))


# def _print_tensorflow_info(check):
#     # Run externally to avoid tf logging to our stderr.
#     cmd = [sys.executable, "-um", "guild.commands.tensorflow_check_main"]
#     env = util.safe_osenv()
#     env["PYTHONPATH"] = os.path.pathsep.join(sys.path)
#     if check.args.verbose:
#         stderr = None
#     else:
#         stderr = open(os.devnull, "w")
#     p = subprocess.Popen(cmd, stderr=stderr, env=env)
#     exit_status = p.wait()
#     if exit_status != 0:
#         check.error()


# def _print_pytorch_info(check):
#     torch = _try_import_torch()
#     if not torch:
#         _attr("pytorch_version", _warn("not installed"))
#         return
#     _attr("pytorch_version", _safe_apply(check, _torch_version, torch))
#     _attr("pytorch_cuda_version", _safe_apply(check, _torch_cuda_version, torch))
#     _attr("pytorch_cuda_available", _safe_apply(check, _torch_cuda_available, torch))
#     _attr("pytorch_cuda_devices", _safe_apply(check, _pytorch_cuda_devices, torch))


# def _try_import_torch():
#     # pylint: disable=import-error
#     try:
#         import torch
#         import torch.version as _unused
#     except Exception:
#         if log.getEffectiveLevel() <= logging.DEBUG:
#             log.exception("try import torch")
#         return None
#     else:
#         return torch


# def _torch_version(torch):
#     return torch.version.__version__


# def _torch_cuda_version(torch):
#     return torch.version.cuda


# def _torch_cuda_available(torch):
#     if torch.cuda.is_available():
#         return "yes"
#     return "no"


# def _pytorch_cuda_devices(torch):
#     if torch.cuda.device_count == 0:
#         return "none"
#     return ", ".join(
#         f"{torch.cuda.get_device_name(i)} ({i})"
#         for i in range(torch.cuda.device_count())
#     )


# def _print_cuda_info(check):
#     _attr("cuda_version", _safe_apply(check, _cuda_version))


# def _cuda_version():
#     version = util.find_apply([_cuda_version_nvcc, _cuda_version_nvidia_smi])
#     if not version:
#         return "not installed"
#     return version


# def _cuda_version_nvcc():
#     nvcc = util.which("nvcc")
#     if not nvcc:
#         return None
#     try:
#         out = subprocess.check_output([nvcc, "--version"])
#     except subprocess.CalledProcessError as e:
#         err_out = e.output.strip().decode("utf-8")
#         return _warn(f"ERROR: {err_out}")
#     else:
#         out = out.decode("utf-8")
#         m = re.search(r"V([0-9\.]+)", out, re.MULTILINE)
#         if m:
#             return m.group(1)
#         log.debug("Unexpected output from nvcc: %s", out)
#         return "unknown (error)"


# def _cuda_version_nvidia_smi():
#     nvidia_smi = util.which("nvidia-smi")
#     if not nvidia_smi:
#         return None
#     try:
#         out = subprocess.check_output([nvidia_smi, "--query"])
#     except subprocess.CalledProcessError as e:
#         err_out = e.output.strip().decode("utf-8")
#         return _warn(f"ERROR: {err_out}")
#     else:
#         out = out.decode("utf-8")
#         m = re.search(r"CUDA Version\s+: ([0-9\.]+)", out, re.MULTILINE)
#         if m:
#             return m.group(1)
#         log.debug("Unexpected output from nvidia-smi: %s", out)
#         return "unknown (error)"


# def _print_nvidia_tools_info(check):
#     _attr("nvidia_smi_version", _safe_apply(check, _nvidia_smi_version))


# def _nvidia_smi_version():
#     cmd = util.which("nvidia-smi")
#     if not cmd:
#         return "not installed"
#     try:
#         out = subprocess.check_output(cmd)
#     except subprocess.CalledProcessError as e:
#         err_out = e.output.strip().decode("utf-8")
#         return _warn(f"ERROR: {err_out}")
#     else:
#         out = out.decode("utf-8")
#         m = re.search(r"NVIDIA-SMI ([0-9\.]+)", out)
#         if m:
#             return m.group(1)
#         log.debug("Unexpected output from nvidia-smi: %s", out)
#         return "unknown (error)"


def _print_mods_info(check: Check):
    for mod, required in CHECK_MODS:
        ver = _try_module_version(mod, check, required)
        _attr(f"{mod}_version", ver)


def _try_module_version(
    name: str, check: Check, required: bool = True, version_attr: str = "__version__"
):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            warnings.simplefilter("ignore", RuntimeWarning)
            mod = __import__(name)
    except ImportError as e:
        if required:
            check.error()
        if log.getEffectiveLevel() <= logging.DEBUG:
            log.exception("import %s", name)
        return _warn(_not_installed_msg(e))
    else:
        try:
            ver = getattr(mod, version_attr)
        except AttributeError:
            return _warn("UNKNOWN")
        else:
            return _format_version(ver)


def _not_installed_msg(e: Exception):
    if "No module named " in str(e):
        return "not installed"
    return f"not installed ({e})"


def _format_version(ver: str):
    if isinstance(ver, tuple):
        return ".".join([str(part) for part in ver])
    return str(ver)


# def _print_guild_latest_versions(check):
#     if check.offline:
#         _attr("latest_guild_version", "unchecked (offline)")
#     else:
#         cur_ver = guild.__version__
#         latest_ver = _latest_version(check)
#         latest_ver_desc = latest_ver or "unknown (error)"
#         _attr("latest_guild_version", latest_ver_desc)
#         if latest_ver:
#             check.newer_version_available = _is_newer(latest_ver, cur_ver)


# def _latest_version(check):
#     url = _latest_version_url(check)
#     log.debug("getting latest version from %s", url)
#     data = {
#         "guild-version": guild.__version__,
#         "python-version": _python_short_version(),
#         "platform": _platform(),
#     }
#     try:
#         resp = util.http_post(url, data, timeout=5)
#     except Exception as e:
#         log.debug("error reading latest version: %s", e)
#         return None
#     else:
#         if resp.status_code == 404:
#             log.debug("error reading latest version: %s not found", url)
#             return None
#         if resp.status_code != 200:
#             log.debug("error reading latest version: %s", resp.text)
#             return None
#         return _parse_latest_version(resp.text)


# def _latest_version_url(check):
#     return _check_config().get("check-url") or check.args.check_url


def _python_short_version():
    return sys.version.split(" ", 1)[0]


def _parse_latest_version(s: str):
    try:
        decoded = json.loads(s)
    except Exception as e:
        log.debug("error parsing latest version response %s: %s", s, e)
        return None
    else:
        return decoded.get("latest-version", "unknown")


def _is_newer(latest: str, cur: str):
    return pkg_resources.parse_version(latest) > pkg_resources.parse_version(cur)


def _notify_newer_version():
    cli.out(
        click.style(
            "A newer version of Guild AI is available. Run "
            "'pip install guildai --upgrade' to install it.",
            bold=True,
        ),
        err=True,
    )


def _print_disk_usage():
    cli.out("disk_space:")
    paths = [
        # ("guild_home", config.guild_home()),
        # ("runs", var.runs_dir()),
        # ("deleted_runs", var.runs_dir(deleted=True)),
        # ("remote_state", var.remote_dir()),
        # ("cache", var.cache_dir()),
    ]
    formatted_disk_usage = [_formatted_disk_usage(path) for _name, path in paths]
    max_disk_usage_width = max((len(s) for s in formatted_disk_usage))
    for (name, path), disk_usage in zip(paths, formatted_disk_usage):
        _attr(
            f"  {name}",
            _format_disk_usage_and_path(disk_usage, path, max_disk_usage_width),
        )


def _formatted_disk_usage(path: str):
    if os.path.exists(path):
        size = file_util.disk_usage(path)
    else:
        size = 0
    return util.format_bytes(size)


def _format_disk_usage_and_path(usage: str, path: str, max_usage_width: int):
    padding = " " * (max_usage_width - len(usage) + 1)
    return f"{usage}{padding}{path}"


def _tests_failed_msg():
    return "one or more tests failed - see above for details"


def _general_error_msg(args: Any):
    msg = (
        "there are problems with your setup\n"
        "Refer to the issues above for more information"
    )
    if not args.verbose:
        msg += " or rerun check with the --verbose option."
    return msg


def _warn(msg: str):
    return click.style(msg, fg="red", bold=True)


def _maybe_notify(args: Any, error: Optional[SystemExit] = None):
    if not args.notify:
        return
    notify_send = util.which("notify-send")
    if not notify_send:
        log.warning("cannot notify check result - notify-send not available")
        return
    summary, body, urgency = _notify_cmd_params(error)
    cmd = ["notify-send", "-u", urgency, summary, body]
    _ignored = subprocess.check_output(cmd)


def _notify_cmd_params(error: Union[SystemExit, None]):
    from vml import __main__ as main

    summary = "guild check"
    body = "PASSED"
    urgency = "normal"
    if error:
        error_msg, code = main.system_exit_params(error)
        # SystemExit errors are used for 0 exit codes, which are not
        # actually errors.
        if code != 0:
            body = f"FAILED ({code})"
            if error_msg:
                body += f": {error_msg}"
                urgency = "critical"
    return summary, body, urgency
