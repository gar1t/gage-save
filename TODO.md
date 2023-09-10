# Gage To Do

- Replace annotations using latest support from Python 3.11

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
