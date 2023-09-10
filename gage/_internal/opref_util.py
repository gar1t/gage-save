# SPDX-License-Identifier: Apache-2.0

from typing import *

from .types import OpRef

OPREF_ENCODING_SCHEME = 1


def encode_opref(opref: OpRef):
    if not opref.op_ns:
        raise ValueError("opref namespace (op_ns) cannot be empty")
    if " " in opref.op_ns:
        raise ValueError("opref namespace (op_ns) cannot contain spaces")
    if not opref.op_name:
        raise ValueError("opref name (op_name) cannot be empty")
    if " " in opref.op_name:
        raise ValueError("opref name (op_name) cannot contain spaces")
    return f"{OPREF_ENCODING_SCHEME} {opref.op_ns} {opref.op_name}"
