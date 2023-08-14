# SPDX-License-Identifier: Apache-2.0

from typing import *

from vml._vendor import click

from vml._internal import click_util


def _ac_remote(ctx: click.Context, param: click.Parameter, incomplete: str):
    return None
    # from guild import config

    # remotes = config.user_config().get("remotes", {})
    # return sorted([r for r in remotes if r.startswith(incomplete)])


def remote_arg(fn: Callable[..., Any]) -> click.Command:
    """`REMOTE` is the name of a configured remote. Use ``guild remotes``
    to list available remotes.

    For information on configuring remotes, see ``guild remotes
    --help``.

    """
    click_util.append_params(
        fn, [click.Argument(("remote",), shell_complete=_ac_remote)]
    )
    return cast(click.Command, fn)


def remote_option(help: str):
    """
    `REMOTE` is the name of a configured remote or an inline remote spec. Run
    ``vml help remotes`` for more information.
    """
    assert isinstance(help, str), "@remote_option must be called with help"

    def f(f0: Callable[..., Any]) -> click.Command:
        click_util.append_params(
            f0,
            [
                click.Option(
                    ("-r", "--remote"),
                    metavar="REMOTE",
                    help=help,
                    shell_complete=_ac_remote,
                )
            ],
        )
        return cast(click.Command, f0)

    return f


def remotes():
    """### Remotes

    Remotes are non-local systems that Guild can interact with. They
    are defined in ``~/.guild/config.yml`` under the ``remotes``
    section.

    For a list of supported remotes, see https://guild.ai/remotes/.

    """


# def remote_for_args(args):
#     from guild import remote as remotelib  # expensive

#     assert args.remote, args

#     try:
#         return remotelib.for_name(args.remote)
#     except remotelib.NoSuchRemote:
#         inline_remote = _try_inline_remote(args.remote)
#         if inline_remote:
#             return inline_remote
#         cli.error(
#             f"remote {args.remote} is not defined\n"
#             "Show remotes by running 'guild remotes' or "
#             "'guild remotes --help' for more information."
#         )
#     except remotelib.UnsupportedRemoteType as e:
#         cli.error(f"remote {args.remote} has unsupported type: {e.args[0]}")
#     except remotelib.MissingRequiredConfig as e:
#         cli.error(f"remote {args.remote} is missing required config: {e.args[0]}")
#     except remotelib.ConfigError as e:
#         cli.error(f"remote {args.remote} has a configuration error: {e.args[0]}")


# def _try_inline_remote(remote_arg):
#     from guild import remote as remotelib  # expensive

#     try:
#         return remotelib.for_spec(remote_arg)
#     except remotelib.InvalidRemoteSpec as e:
#         cli.error(e.args[0])
#     except remotelib.RemoteForSpecNotImplemented as e:
#         cli.error(f"remote type '{e.args[0]}' does not support inline specifications")
#     except remotelib.UnsupportedRemoteType as e:
#         cli.error(f"unknown remote type '{e.args[0]}'")
