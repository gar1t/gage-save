# SPDX-License-Identifier: Apache-2.0

from typing import *

import errno
import hashlib
import os

__all__ = [
    "compare_paths",
    "ensure_dir",
    "expand_path",
    "files_differ",
    "find",
    "find_up",
    "is_text_file",
    "make_dir",
    "realpath",
    "standardize_path",
]


def standardize_path(path: str):
    return path.replace(os.path.sep, "/")


_text_ext = {
    ".csv",
    ".html",
    ".html",
    ".json",
    ".jsx",
    ".md",
    ".py",
    ".r",
    ".sh",
    ".ts",
    ".tsx.txt",
    ".yaml",
    ".yml",
    "js",
}

_binary_ext = {
    ".ai",
    ".bmp",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".png",
    ".ps",
    ".psd",
    ".svg",
    ".tif",
    ".tiff",
    ".aif",
    ".mid",
    ".midi",
    ".mpa",
    ".mp3",
    ".ogg",
    ".wav",
    ".wma",
    ".avi",
    ".mov",
    ".mp4",
    ".mpeg",
    ".swf",
    ".wmv",
    ".7z",
    ".deb",
    ".gz",
    ".pkg",
    ".rar",
    ".rpm",
    ".tar",
    ".xz",
    ".z",
    ".zip",
    ".doc",
    ".docx",
    ".key",
    ".pdf",
    ".ppt",
    ".pptx",
    ".xlr",
    ".xls",
    ".xlsx",
    ".bin",
    ".pickle",
    ".pkl",
    ".pyc",
}

_control_chars = b"\n\r\t\f\b"

_printable_ascii = _control_chars + bytes(range(32, 127))

_printable_high_ascii = bytes(range(127, 256))


def is_text_file(path: str, ignore_ext: bool = False):
    import chardet

    # Adapted from https://github.com/audreyr/binaryornot under the
    # BSD 3-clause License
    if not os.path.exists(path):
        raise OSError(f"{path} does not exist")
    if not os.path.isfile(path):
        return False
    if not ignore_ext:
        ext = os.path.splitext(path)[1].lower()
        if ext in _text_ext:
            return True
        if ext in _binary_ext:
            return False
    try:
        with open(path, "rb") as f:
            sample = f.read(1024)
    except IOError:
        return False
    if not sample:
        return True
    low_chars = sample.translate(None, _printable_ascii)
    nontext_ratio1 = float(len(low_chars)) / float(len(sample))
    high_chars = sample.translate(None, _printable_high_ascii)
    nontext_ratio2 = float(len(high_chars)) / float(len(sample))
    likely_binary = (nontext_ratio1 > 0.3 and nontext_ratio2 < 0.05) or (
        nontext_ratio1 > 0.8 and nontext_ratio2 > 0.8
    )
    detected_encoding = chardet.detect(sample)
    decodable_as_unicode = False
    if (
        detected_encoding["confidence"] > 0.9
        and detected_encoding["encoding"] != "ascii"
    ):
        try:
            sample.decode(encoding=detected_encoding["encoding"] or "utf-8")
        except LookupError:
            pass
        except UnicodeDecodeError:
            pass
        else:
            decodable_as_unicode = True
    if likely_binary:
        return decodable_as_unicode
    if decodable_as_unicode:
        return True
    if b"\x00" in sample or b"\xff" in sample:
        return False
    return True


def ensure_dir(d: str):
    try:
        make_dir(d)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def make_dir(d: str):
    os.makedirs(realpath(d))


# def disk_usage(path: str):
#     total = _file_size(path)
#     for root, dirs, names in os.walk(path, followlinks=False):
#         for name in dirs + names:
#             path = os.path.join(root, name)
#             total += _file_size(os.path.join(root, name))
#     return total


# def _file_size(path: str):
#     stat = os.lstat if os.path.islink(path) else os.stat
#     try:
#         return stat(path).st_size
#     except (OSError, IOError) as e:
#         log.warning("could not read size of %s: %s", path, e)
#         return 0


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
    stop_dir = realpath(stop_dir) if stop_dir else _user_home()

    cur = start_dir
    while True:
        maybe_target = os.path.join(cur, relpath)
        if check(maybe_target):
            return maybe_target
        if realpath(cur) == stop_dir:
            return None
        parent = os.path.dirname(cur)
        if parent == cur:
            return None
        cur = parent

    # `parent == cur` above should be the definitive terminal case
    assert False


def _user_home():
    return os.path.expanduser("~")


def realpath(path: str):
    # Workaround for https://bugs.python.org/issue9949
    try:
        link = os.readlink(path)
    except OSError:
        return os.path.realpath(path)
    else:
        path_dir = os.path.dirname(path)
        return os.path.abspath(os.path.join(path_dir, _strip_windows_prefix(link)))


def _strip_windows_prefix(path: str):
    if os.name != "nt":
        return path
    if path.startswith("\\\\?\\"):
        return path[4:]
    return path


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


def _apply_digest_file_bytes(path: str, d: Any):
    buf_size = 1024 * 1024
    with open(path, "rb") as f:
        while True:
            buf = f.read(buf_size)
            if not buf:
                break
            d.update(buf)


def compare_paths(p1: str, p2: str):
    return _resolve_path(p1) == _resolve_path(p2)


def _resolve_path(p: str):
    return realpath(os.path.expanduser(p))
