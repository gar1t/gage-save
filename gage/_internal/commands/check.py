# SPDX-License-Identifier: Apache-2.0

from typing import *

import click


@click.command()
def check(**params: Any):
    """Check Gage ML.

    Shows version and configuration details.
    """
    from . import check_impl

    check_impl.main(**params)
