# Plugin support

The `plugin` module provides a high level interface for discovering and
using gage ML plugins.

    >>> from gage._internal import plugin as pluginlib

## Iterating available plugins

    >>> pluginlib.iter_plugins()
