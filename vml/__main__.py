# SPDX-License-Identifier: Apache-2.0

import os
import sys
from typing import Any, cast, Tuple, Union

from vml._internal import click_util
from vml._internal import exit_codes

from vml._vendor import click

from vml._internal.commands import vml as vml_cmd


def main():
    _configure_help_formatter()
    try:
        # pylint: disable=unexpected-keyword-arg,no-value-for-parameter
        vml_cmd.main(standalone_mode=False)  # type: ignore
    except click.exceptions.Abort:
        _handle_keyboard_interrupt()
    except click.exceptions.ClickException as e:
        _handle_click_exception(e)
    except SystemExit as e:
        handle_system_exit(e)


def _configure_help_formatter():
    if os.getenv("GUILD_HELP_JSON"):
        click.Context.make_formatter = _make_json_formatter
    else:
        click.Context.make_formatter = _make_plaintext_formatter


def _make_json_formatter(_self: Any) -> click.HelpFormatter:
    return click_util.JSONHelpFormatter()


def _make_plaintext_formatter(_self: Any):
    return click_util.HelpFormatter()


def _handle_keyboard_interrupt():
    sys.exit(1)


def _handle_click_exception(e: click.exceptions.ClickException):
    msg = click_util.format_error_message(e)
    _print_error_and_exit(msg, e.exit_code)


def _print_error_and_exit(msg: Union[str, None], exit_status: int):
    if msg:
        click.echo(f"guild: {msg}", err=True)
    sys.exit(exit_status)


def handle_system_exit(e: SystemExit):
    msg, code = system_exit_params(e)
    _print_error_and_exit(msg, code)


def system_exit_params(e: SystemExit) -> Tuple[Union[str, None], int]:
    msg: Union[str, None]
    code: int
    if isinstance(e.code, tuple) and len(e.code) == 2:
        msg, code = cast(Tuple[str, int], e.code)
    elif isinstance(e.code, int):
        msg, code = None, e.code
    else:
        msg, code = e.code, exit_codes.DEFAULT_ERROR
    return msg, code


if __name__ == "__main__":
    main()
