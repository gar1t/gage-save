# SPDX-License-Identifier: Apache-2.0

from typing import *

from .types import *

from . import config
from . import gagefile
from . import util


def opdef_for_opspec(opspec: Optional[str], cwd: Optional[str] = None):
    cwd = cwd or config.cwd()
    return util.find_apply(
        [
            _try_project_opdef,
            # _try_plugin_opdef,
            # _try_builtin_opdef,
            _opdef_not_found,
        ],
        opspec,
        cwd,
    )


def _try_project_opdef(opspec: Optional[str], cwd: str):
    try:
        gf = gagefile.for_dir(cwd)
    except FileNotFoundError:
        return None
    else:
        return _opdef_for_name(opspec, gf) if opspec else _default_opdef(gf)


def _opdef_for_name(name: str, gf: GageFile):
    try:
        return gf.operations[name]
    except KeyError:
        return None


def _default_opdef(gf: GageFile):
    for name, opdef in sorted(gf.operations.items()):
        if opdef.default:
            return opdef
    return None


# def _try_plugin_opdef(opspec: Optional[str], cwd: str):
#     return plugin_opdef_for_opspec(opspec, cwd)


# def _try_builtin_opdef(opspec: Optional[str], cwd: str):
#     return None


def _opdef_not_found(opspec: Optional[str], *rest: Any):
    raise OpDefNotFound(opspec)


def opdef_to_opspec(opdef: OpDef, cwd: Optional[str] = None):
    return opdef.name
