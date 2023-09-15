# Staging a run dir

A staged run can be started by a runner using only the run directory and
the contents of the run meta directory. Staged runs (i.e. the run and
meta directories) can be relocated to another compatible system and
started there.

A staged run is independent of its project.

A staged run relies on a compatible system (platform, installed
applications and libraries, etc.) to run. If a staged run is moved to an
incompatible system, it won't run.

To stage a run, the runner must copy all files required by the run that
are not otherwise provided by the system to the run directory.

When staging a run, meta is updated with a manifest file and additional
log entries, which reflect the changes made to the run directory during
staging.

## Run meta

Run meta must be initialized before the run can be staged. For more
information on this process, see [*Initializing run
meta*](topic-run-lifecycle-2-init-meta.md).

Create a run and initialize its meta.

    >>> from gage._internal.run_util import *

    >>> runs_home = make_temp_dir()

    >>> run = make_run(runs_home)

    >>> from gage._internal.types import *

Op ref identifies the run:

    >>> opref = OpRef("test", "test")

Source code specifies what files to copy. In this test, the `sourcecode`
spec is empty, which applies the default include/exclude rules.

    >>> sourcecode = {}

Create the op def.

    >>> opdef = OpDef("test", {"sourcecode": sourcecode})

The command is what is run. As tests below only stage the run, this
command is merely an example.

    >>> cmd = OpCmd(["python", "train.py"], {})

Initialize the run meta.

    >>> init_run_meta(run, opref, opdef, cmd, {}, {})

List the generated files.

    >>> ls(run_meta_dir(run))
    __schema__
    id
    initialized
    log/runner
    name
    opdef.json
    opref
    proc/cmd
    proc/env

## Run stage phases

Run staging consists of the following phases:

- Copy source code
- Apply configuration
- Initialize runtime
- Resolve dependencies
- Finalize staged run

The order of these phases is important:

1. Source code must be copied before configuration is applied
2. A runtime may require configured source code
3. Dependency resolution may required an initialized runtime
4. All files must be written before a staged run is finalized

Each phase is implemented by a function in `run_util`:

- `copy_sourcecode`
- `apply_config`
- `init_runtime`
- `resolve_deps`
- `finalize_staged_run`

Each of these functions is called by `run_util.stage_run()` to stage a
run.

Changes made to the run directory for each phase up to stage finalizing
are written to `log/files`. This log is used to generate a run manifest,
which contains a record of source code, resolved dependencies, and
runtime files.

## Copy source code

`copy_sourcecode()` requires a source directory and a run.

Create a sample source code directory structure.

    >>> sourcecode_dir = make_temp_dir()
    >>> touch(path_join(sourcecode_dir, "train.py"))
    >>> touch(path_join(sourcecode_dir, "eval.py"))
    >>> touch(path_join(sourcecode_dir, "gage.toml"))
    >>> make_dir(path_join(sourcecode_dir, "conf"))
    >>> touch(path_join(sourcecode_dir, "conf", "train.yaml"))
    >>> touch(path_join(sourcecode_dir, "conf", "eval.yaml"))

    >>> ls(sourcecode_dir)
    conf/eval.yaml
    conf/train.yaml
    eval.py
    gage.toml
    train.py

Before copying anything, confirm the run directory is empty.

    >>> ls(run.run_dir)
    <empty>

Copy the source code to the run directory.

    >>> copy_sourcecode(sourcecode_dir, run)

Source code files are copied and left in a writeable state.

    >>> ls(sourcecode_dir, permissions=True)
    -rw-rw-r-- conf/eval.yaml
    -rw-rw-r-- conf/train.yaml
    -rw-rw-r-- eval.py
    -rw-rw-r-- gage.toml
    -rw-rw-r-- train.py

The list of files is written to the files log. Log entries are per line
and consist of an event, a file type, a modified timestamp, and a path.

    >>> cat(run_meta_path(run, "log", "files"))  # +parse
    a s {:d} conf/eval.yaml
    a s {:d} conf/train.yaml
    a s {:d} eval.py
    a s {:d} gage.toml
    a s {:d} train.py

In this case, "a" means the file was added. "s" means it's a source code
type.

    >>> cat(run_meta_path(run, "log", "runner"))  # +parse -space
    {}
    {:date} Copying source code (see log/files for details)
    {:date} Source code include:
      ['**/* text size<10000 max-matches=500']
    {:date} Source code exclude:
      ['**/.* dir',
       '**/* dir sentinel=bin/activate',
       '**/* dir sentinel=.nocopy']

## Apply config

TODO: `apply_config()`

## Init runtime

TODO: `init_runtime()`

## Resolve dependencies

TODO: `resolve_deps()`

## Finalize staged run

As the last phase of staging, two changes are made:

- Run directory files are made read-only
- Run manifest is written

Files copied to the run directory for staging are typically inputs only
and are not modified by the run.

TODO: how to make an exception in the general case? We can specify that
a dependency is writable but what about source code/config and runtime
files? We need a general facility to exempt a file from read-only
status.

The run manifest is written so that tools can rely on a list of input
files (source code, dependencies, and runtime).

Finalize the staged run.

    >>> finalize_staged_run(run)

List the run files.

    >>> ls(run.run_dir, permissions=True)
    -r--r--r-- conf/eval.yaml
    -r--r--r-- conf/train.yaml
    -r--r--r-- eval.py
    -r--r--r-- gage.toml
    -r--r--r-- train.py

Show the run manifest.

    >>> cat(run_meta_path(run, "manifest"))  # +parse
    s {:sha256} conf/eval.yaml
    s {:sha256} conf/train.yaml
    s {:sha256} eval.py
    s {:sha256} gage.toml
    s {:sha256} train.py

## Errors

    >>> # +skiprest TODO reinstate

Stage a non-existing run directory.

    >>> missing_run_dir = make_temp_dir()
    >>> delete_temp_dir(missing_run_dir)

    >>> stage_run(Run("", missing_run_dir, ""))  # +parse
    Traceback (most recent call last):
    FileNotFoundError: Run dir does not exist: {:path}

Stage a run without a meta dir.

    >>> run_dir_no_meta = make_temp_dir()
    >>> stage_run(Run("", run_dir_no_meta, ""))  # +parse
    Traceback (most recent call last):
    FileNotFoundError: Run meta dir does not exist: {:path}.meta
