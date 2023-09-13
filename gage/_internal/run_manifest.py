# SPDX-License-Identifier: Apache-2.0

from typing import *

from .types import *


class RunManifest:
    def __init__(self, run: Run):
        self.run = run

    def __enter__(self):
        return self

    def __exit__(*exc: Any):
        pass


# TODO: make sure we're using `sha256` and noting somewhere this scheme
# (perhaps this is implied in the `__schema__` written to the meta dir)
