---
test-options: +parse
---

# `check` command

    >>> run("gage check")
    gage_version:              {:ver}
    gage_install_location:     {:path}
    python_version:            {:ver} {:any}
    python_exe:                {:path}
    platform:                  {:any}
    <0>

Test version.

    >>> run("gage check --version 0.1.0")
    <0>

    >>> run("gage check --version 999")
    gage: version mismatch: current version '{:ver}' does not match '999'
    <1>

## Text external functions

The `--external` options is a hidden flag used to apply external checks.
External checks are specified with a single string argument to the option.

### `git-ls-files`

gage uses Git to list source code files and relies on a particular version for
required functionality. The `git-ls-files` check tests if this functionality
exists.

We test only the positive case here, assuming that systems under test all have
current versions of Git installed.

    >>> run("gage check --external git-ls-files")
    git-ls-files is ok (git version {:ver}; {:path})
    <0>

### Other checks

`check` exits with an error for other external checks.

    >>> run("gage check --external other")
    gage: unsupported external check: other
    <1>
