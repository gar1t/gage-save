# `show` command

    >>> run("gage show -h")
    Usage: gage show [options] [run]
    ⤶
      Show information about a run.
    ⤶
    Arguments:
      [run]  Run to show information for. Value may be an
             index number, run ID, or run name.
    ⤶
    Options:
      -h, --help  Show this message and exit.
    <0>

Generate a run.

    >>> use_example("hello")
    >>> run("gage run -q -y")
    <0>

Show the run.

    >>> run("gage show")  # +parse -space +diff
    {:run_id}
    | hello:hello                                    completed |
    ⤶
                             Attributes
    | id         {:run_id}                                     |
    | name       {:run_name}                                   |
    | started    {:datetime}                                   |
    | stopped    {:datetime}                                   |
    | location   {:path}                                       |
    | exit_code  0                                             |
    ⤶
                               Output
    | Hello Gage!                                              |
    <0>
