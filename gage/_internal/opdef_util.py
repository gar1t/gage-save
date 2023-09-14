# SPDX-License-Identifier: Apache-2.0

from typing import *

from .types import *

from . import config
from . import gagefile
from . import util

__all__ = ["opdef_for_spec"]


def opdef_for_spec(spec: Optional[str], cwd: Optional[str] = None) -> OpDef:
    cwd = cwd or config.cwd()
    return cast(
        OpDef,
        util.find_apply(
            [
                _try_project_opdef,
                # _try_plugin_opdef,
                # _try_builtin_opdef,
                _opdef_not_found,
            ],
            spec,
            cwd,
        ),
    )


def _try_project_opdef(spec: Optional[str], cwd: str):
    try:
        gf = gagefile.gagefile_for_dir(cwd)
    except FileNotFoundError:
        return None
    else:
        return _opdef_for_name(spec, gf) if spec else _default_opdef(gf)


def _opdef_for_name(name: str, gf: GageFile) -> OpDef | None:
    try:
        return gf.operations[name]
    except KeyError:
        return None


def _default_opdef(gf: GageFile):
    for name, opdef in sorted(gf.operations.items()):
        if opdef.default:
            return opdef
    return None


def _opdef_not_found(spec: str | None, *rest: Any):
    raise OpDefNotFound(spec)


def opdef_to_spec(opdef: OpDef, cwd: Optional[str] = None):
    return opdef.name
