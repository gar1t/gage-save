# Gage To Do

## CLI factor

- Get -H and -C core opts working again
- Drop Click
- Add `__all__` to all modules

## General

- Do tags, label, and comments from the `run` command land in the meta
  dir or in user? I suspect in meta under `./user` but want to sanity
  check why.

- Pointer to original project.

- How to identify runs by their project.

- How to re-associate runs with their project? Do we ask users to
  generate a unique ID for the project?

``` toml
"$namespace" = "my-project"
"$project-id" = "24e17ef2-4e6b-49bd-af59-f7ba0ca79349"

[train]
exec = "python train.py"
```

``` json
{
  "$namespace": "my-project",
  "$project-id": "24e17ef2-4e6b-49bd-af59-f7ba0ca79349",
  "train": {
    "exec": "python train.py"
  }
}
```

- Make sure we're using the new uuid formats (with dashes)

- Gagefile validation messages *suck* (see `lib-gagefile.md` tests) -
  must clean up before shipping to anyone. These are being passed
  through from the jschon library. Need to work with the low level error
  and create intelligible reports (current reports mangle sub-schema
  errors into a unqualified list and are nearly pointless)

- How to handle invalid Gage file content? It's temping to add this to
  `types.py` but it's maybe not great there. Types is a light weight
  data-to-py mapper. Right now it's not handling type validation at all
  -- it coerces lightly and let's bad data through. I think a validation
  error is in order but we should load and use as much as we can and not
  blow up at the slightest problem. For now bad data leaks.

- Integrate time range spec into filter spec

## Low priority

- Fix plain table printing and matching with Groktest (look for `-space`
  options in tests associated with commands that print a table)

- Gage file validation should show the line/col numbers of errors (note
  that we strip comments so adjust for that)

- Gage file comments for JSON can't be inline - find a parser or get the
  comment stripping right

- Source code preview should show the source code stage command if
  specified.

## Run layout

- Init run by creating `.meta` (done)
- Implement runs list using `.meta`
- Implement `stage_run` function
  - Copy source code to `.run` + update manifest
  - Resolve deps + update manifest
- Implement `start_run`
  - Start process
  - Launch output summaries
  - Pipe output to output + output.index
  - Handle process exit
    - Write process exits, delete locks, etc
    - Finalize manifest
    - Mark run files as readonly

## Lifting by `guild check`

- Validate a Gage file
- Other fanciful musings
  - Validate a staged run
  - Validate a generated run

``` bash
$ gage check [--run] <run ID>
$ gage check <path>
```

Here we're inferring a run by a run ID shaped arg. Can be partial. If
it's a file then we know what to do. If it points to a run, we know what
to do. Otherwise we assume it's a project.

## Dependencies

Sample:

```toml
[[a.config]]

type = "run-files"
run-select = "op in [prepare-data, prepare]"
files = "data.csv"

[[b.config]]

type = "run-files"
operation = "prepare-data"

```

```json
[
  {
    "type": "runfiles",
    "run.select": "op in [prepare-data, prepare]",  # canonical
    "operation": "prepare",  # shorthand for 'run.select: op=prepare'
    "files.select": ["data.csv"]  # or use alias 'select'
  },
  {
    "type": "dir",
    "path": "data"
  },
  {
    "type": "file",
    "path": "data.csv"
  },
  {
    "type": "dvcfile",
    "path": "data.csv"
  }
]
```

- Continue to support single string specs with a URI like syntax. E.g.
  'dvcfile: data.csv' is coerced to the example above. A more complex
  case might be 'runfiles: op=prepare-data'

- For select use glob pattern unless string is prefixed with 'regex:' -
  e.g. 'regex:data\.(csv|txt)'

- Do we want to support sha256 for 1.0 or add that back later? I don't
  think this is used much.

- Do we want to support downloads or remote files? We could punt to use
  DvC at that point.

- Drop use of pip download support! If we continue to support downloads
  use anything else. Might just drop download support for 1.0 though.

"""
