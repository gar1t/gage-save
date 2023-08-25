# Run command

## Command help

    >>> run("vml run --help")  # +blankline=.
    Usage: vml run [OPTIONS] OPERATION
    .
      Start a run.
    .
    Options:
      --stage            Stage a run.
      -y, --yes          Do not prompt before running operation.
      --help-op          Show operation help and exit.
      --test-opdef       Show how the operation def is generated and exit.
      --test-sourcecode  Test operation source code selection and exit.
      --test-output      Test operation output and exit.
      --help             Show this message and exit.
    <exit 0>

## Op help

    >>> use_project("hello")

    >>> find(".")
    hello.py
    vistaml.json

    >>> run("vml run hello.py --help-op")  # FIXME
    vml: no such operation hello.py
    Try 'vml operations' for a list of operations.
    <exit 1>

## Python scripts

    >>> run("vml run hello.py --test-prompt")  # FIXME
    vml: no such operation hello.py
    Try 'vml operations' for a list of operations.
    <exit 1>

Output should be:

    You are about to run hello.py
    Continue?

    >>> run("vml run hello.py -y")  # FIXME
    vml: no such operation hello.py
    Try 'vml operations' for a list of operations.
    <exit 1>

## Staging

    >>> run("vml run hello.py --stage --test-prompt")  # FIXME
    vml: no such operation hello.py
    Try 'vml operations' for a list of operations.
    <exit 1>

Output should be:

    You are about to stage hello.py
    Continue?
