# Run file system layout

    >>> var_home = make_temp_dir()

    >>> use_project("hello-project", var_home)

    >>> find(".")
    gage.json
    hello.py

    >>> find(var_home)
    <empty>

TODO: implement!

    >>> run("gage run hello.py -y")
    gage: no such operation hello.py
    Try 'gage operations' for a list of operations.
    <1>

TODO: implement!

    >>> find(var_home)
    <empty>
