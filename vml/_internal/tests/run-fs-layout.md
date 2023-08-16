# Run file system layout

    >>> var_home = mkdtemp()

    >>> use_project("hello", var_home)

    >>> find(".")
    hello.py
    vistaml.json

    >>> find(var_home)
    <empty>

TODO: implement!

    >>> run("vml run hello.py -y")
    <exit 0>

TODO: implement!

    >>> find(var_home)
    <empty>
