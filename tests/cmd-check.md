---
test-options: +parse
---

# `check` command

    >>> run("vml check")
    vistaml_version:           {:ver}
    vistaml_install_location:  {:abspath}
    python_version:            {:ver} {:any}
    python_exe:                {:abspath}
    platform:                  {:any}
    <exit 0>

Test version.

    >>> run("vml check -V 0.1.0")
    <exit 0>

    >>> run("vml check -V 999")
    vml: version mismatch: current version '{:ver}' does not match '999'
    <exit 1>

## Text external functions

The `--external` options is a hidden flag used to apply external checks.
External checks are specified with a single string argument to the option.

### `git-ls-files`

Vista uses Git to list source code files and relies on a particular version for
required functionality. The `git-ls-files` check tests if this functionality
exists.

We test only the positive case here, assuming that systems under test all have
current versions of Git installed.

    >>> run("vml check --external git-ls-files")
    git-ls-files is ok (git version {:ver}; {:abspath})
    <exit 0>

### Other checks

`check` exits with an error for other external checks.

    >>> run("vml check --external other")
    vml: unsupported external check: other
    <exit 1>