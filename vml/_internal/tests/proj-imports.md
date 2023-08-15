# Imports

    >>> import importlib
    >>> import os
    >>> import vml

    >>> SKIP_DIRS = ["tests", "_vendor"]
    >>> SKIP_MODS = []

    >>> def iter_mods():
    ...     proj_root = os.path.dirname(vml.__file__)
    ...     for root, dirs, files in os.walk(proj_root, topdown=True):
    ...         for name in SKIP_DIRS:
    ...             if name in dirs: dirs.remove(name)
    ...         for name in files:
    ...             if not name.endswith(".py"): continue
    ...             mod_path = os.path.join(root, name)
    ...             mod_relpath = os.path.relpath(mod_path, proj_root)
    ...             mod_name = (
    ...                 "vml."
    ...                 + mod_relpath.replace(os.path.sep, ".")[:-3])
    ...             if mod_name in SKIP_MODS: continue
    ...             yield importlib.import_module(mod_name)

    >>> for name in sorted([m.__name__ for m in iter_mods()]):
    ...     print(name) # doctest: +REPORT_UDIFF
    vml.__init__
    vml.__main__
    vml._internal.ansi_util
    vml._internal.cli
    vml._internal.click_util
    vml._internal.commands.ac_support
    vml._internal.commands.check
    vml._internal.commands.check_impl
    vml._internal.commands.help
    vml._internal.commands.impl_support
    vml._internal.commands.main
    vml._internal.commands.run
    vml._internal.commands.run_impl
    vml._internal.commands.runs
    vml._internal.commands.runs_archive
    vml._internal.commands.runs_comment
    vml._internal.commands.runs_delete
    vml._internal.commands.runs_export
    vml._internal.commands.runs_import
    vml._internal.commands.runs_info
    vml._internal.commands.runs_label
    vml._internal.commands.runs_list
    vml._internal.commands.runs_list_impl
    vml._internal.commands.runs_mark
    vml._internal.commands.runs_merge
    vml._internal.commands.runs_publish
    vml._internal.commands.runs_purge
    vml._internal.commands.runs_restore
    vml._internal.commands.runs_stop
    vml._internal.commands.runs_support
    vml._internal.commands.runs_tag
    vml._internal.config
    vml._internal.exit
    vml._internal.file_util
    vml._internal.log
    vml._internal.op
    vml._internal.opdef
    vml._internal.python_util
    vml._internal.run
    vml._internal.run_manifest
    vml._internal.run_util
    vml._internal.test
    vml._internal.util
    vml._internal.var
    vml._internal.yaml_util
