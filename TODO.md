# Gage To Do

- Labels, tags, and notes
  - Should any of these land in the meta dir, ever?
  - Get `.user` going
  - Research a distributed file store data scheme - or can we get by
    with time sortable UUIDs?

- Dependencies
  - Project files
  - Run files
  - Run summaries
  - Replace links with ref files on finalize

- Batches

- Runs list
  - Where filter
  - Sort filter

- Scan output for scalars and attrs - save in run dir root with special
  extensions (e.g. *.attrs - same as with Guild)

- Roll up tf event summaries with `metrics.json` and `attrs.json`

- API and View

- Sync / collaboration

- Command completion working again (want support for bash, zsh, fish,
  nu)

- How to identify runs by their project?

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

- How can a user specify different commands for different platforms? One
  method would be something like:

```
[train.exec]

run[windows] = "..."
run[mac] = "..."
run[linux] = "..."
```

- Use config in exec commands

``` toml
[hello]

exec = "echo {msg}"

[[hello.config]]

name = "msg"
```

- Review error messages for consistency
  - Capitalization
  - Use of periods
  - Phrasing of "run 'cmd' for more info/help"

- Review command help for consistency
  - Case of meta vars
  - Formatting of meta var refs
  - Formatting of command examples

- Review topic help - this is going to be quite out of date - this
  should be the main help for Gage

- Warn on invalid Gage file?? We can detect invalid files but what to do
  with them?

- How does this look under different terminal color combos?

- "No such command 'ops'" error message on `gage help ops` - "command"
  there needs to be "topic"

- Gage file comments for JSON can't be inline - find a parser or get the
  comment stripping right

- Source code preview should show the source code stage command if
  specified.

## Lifting by `gage check`

Fanciful (down the road):

  - Validate a run

``` bash
$ gage check [--run] <run ID>
```

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

- Delete unused code - start with dead code analysis (e.g. vulture) but
  we need test coverage as well - should be 100%

- cli.incompatible_with is not going to work as designed. ctx.param is
  under construction so it may not contain the incompatible values when
  the param callback is made. Look for a better solution or roll
  something new.

## Use cases

Running

- Basic run
- Custom config via flags
- Batches (grid, random, drive-from-file)

Sharing

- Archives runs of interest (or all runs?)
  - GitHub
  - DropBox
  - Cloud storage

- Sync with a colleague
