# Stage a run

    >>> use_example("hello")

    >>> from gage._internal import sys_config

    >>> ls(sys_config.runs_home())
    <empty>

    >>> run("gage run hello --stage -y")
    <0>

    >>> for path in lsl(sys_config.runs_home()):
    ...     print(path[36:])  # +diff
    .meta/__schema__
    .meta/config.json
    .meta/id
    .meta/initialized
    .meta/log/files
    .meta/log/runner
    .meta/manifest
    .meta/opdef.json
    .meta/opref
    .meta/proc/cmd.json
    .meta/proc/env.json
    .meta/staged
    .meta/sys/platform.json
    /gage.toml
    /hello.py

    >>> run("gage list")  # +parse
    | #   | name     | operation       | started    | status   |
    |-----|----------|-----------------|------------|----------|
    | 1   | {:rn}    | hello:hello     |            | staged   |
    <0>
