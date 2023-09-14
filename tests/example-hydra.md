# Hydra example

    >>> use_example("hydra")

    >>> ls(ignore=[".venv/**"])  # +diff
    .gitignore
    conf/__init__.py
    conf/config.yaml
    conf/db/mysql.yaml
    conf/db/postgresql.yaml
    gage.toml
    my_app.py

    >>> run("gage check .")
    ./gage.toml is a valid Gage file
    <0>

    >>> run("gage ops")  # -space
    operation  description
     my_app     Replicates the Hydra Get Started example.
    <0>

    >>> run("gage run my_app --preview")
    TODO: preview my_app
    <0>
