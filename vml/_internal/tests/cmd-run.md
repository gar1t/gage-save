# Run command

## Command help

    >>> run("vml run --help")  # doctest: +REPORT_UDIFF
    Usage: vml run [OPTIONS] OPERATION
    <BLANKLINE>
      Start a run.
    <BLANKLINE>
    Options:
      --stage            Stage a run.
      -y, --yes          Do not prompt before running operation.
      --help-op          Show operation help and exit.
      --test-opdef       Show how the operation def is generated and exit.
      --test-sourcecode  Test operation source code selection and exit.
      --test-output      Test operation output and exit.
      --help             Show this message and exit.

## Op help

    >>> use_project("hello")

    >>> run("vml run hello.py --help-op")
    <exit 0>

## Python scripts

    >>> run("vml run hello.py --test-prompt")
    You are about to run hello.py
    Continue?

    >>> run("vml run hello.py -y")
    <exit 0>

## Staging

    >>> run("vml run hello.py --stage --test-prompt")
    You are about to stage hello.py
    Continue?
