# Run command

## Command help

    >>> run("gage run --help")
    Usage: gage run [OPTIONS] OPERATION
    ⤶
      Start a run.
    ⤶
    Options:
      --stage            Stage a run.
      -y, --yes          Do not prompt before running operation.
      --help-op          Show operation help and exit.
      --test-opdef       Show how the operation def is generated and exit.
      --test-sourcecode  Test operation source code selection and exit.
      --test-output      Test operation output and exit.
      --help             Show this message and exit.
    ↳0


## Op help

    >>> use_project("hello-project")

    >>> run("gage run hello --help-op")
    gage: no such operation hello
    Try 'gage operations' for a list of operations.
    ↳1

## Python scripts

    >>> run("gage run hello --test-prompt")  # FIXME
    gage: no such operation hello
    Try 'gage operations' for a list of operations.
    ↳1

Output should be:

    You are about to run hello
    Continue?

    >>> run("gage run hello -y")  # FIXME
    gage: no such operation hello
    Try 'gage operations' for a list of operations.
    ↳1

## Staging

    >>> run("gage run hello --stage --test-prompt")  # FIXME
    gage: no such operation hello
    Try 'gage operations' for a list of operations.
    ↳1

Output should be:

    You are about to stage hello
    Continue?
