# Gage To Do

- Fill in Gage MVP so we know what's going on

- Save source code digest in meta

- Save run command details in meta (e.g. `run-cmd.json`)

- Run tags

- Latest git commit / git info (should we save git index info, e.g. a
  source code diff?)

- User config and repos
  - Some CLI interface to show user config (respect parents)
  - CLI to list available repos

- Integrate repos into copy command
  - General IO command - use for backup and restore
  - Enables sync, archive features - use for collaboration and run org

- New commands: sync and archive
  - sync is to make sharing convenient (sync's configured something -
    shares? or remote)
  - archive makes archival convenient

- Concept of a "user"
  - Works without any config
  - Something that can be authenticated/verified
  - Include verifiable info in user attrs (i.e. can I rely that "sam"
    wrote a comment - e.g. a signature).

- Scalars and attributes
  - Scan run dir routinely during a run and use to update metrics and
    attrs in meta
  - Where are these written? To a `summaries` subdir I think

  ```
  ./summaries/
    metrics.json
    attrs.json
    # could write image thumbs here!
  ```

  Note that thumbnails should probably be written to `.thumbs` to keep
  their potential largeness out of meta. `.thumbs` could be a user-style
  dir where thumbnails can be written by anyone and merged over time.
  This might also be named `.cache`.

- CLI based compare view

- Record Git commit in system attrs

- Dependencies
  - Project files
  - Run files
  - Run summaries
  - Replace links with ref files on finalize

- Batches

- Restart
  - Copy to new run and re-run using same settings
  - Optional apply new flags to config
  - Optional apply latest source code

- Runs list
  - Where filter
  - Sort filter

- Scan output for scalars and attrs - save in run dir root with special
  extensions (e.g. *.attrs - same as with Guild)

- Roll up tf event summaries with `metrics.json` and `attrs.json`

- API and View

- Sync / collaboration
  - Resolve copy-from filter and preview (need support for listing remote runs)
  - Issue with run dir, user dir, and meta, and delete meta being "out
    of sync" when copying - what are the scenarios and which ones are
    problematic?

- TensorBoard command? Maybe not - just get people off TensorBoard.
  Should be out-competing them.

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

- `cli.Table` isn't doing much work - do we need this? Same for the
  other rich wrappers in `cli`, apart from the traditional cli API (e.g.
  out, err, exit_with_message, etc.)

- Make upper case section titles in help (no longer doing this markdown
  formatter)

- Annoying fast updates of estimated remaining time on copy run progress
  (shows up on anything over a network) Fix may require a custom column
  that doesn't refresh as frequently as the default.

- Language specific APIs

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

## Attributes and Scalars

Op defs should support attributes.

Gage will continue to support "output scalars" and "output attrs" log to
TF event files. These, however, will be written to the run directory and
not to the meta directory.

I think it's safe to summarize the scalars to the meta directory as
"metrics.json" or similar, under maybe "summaries".

E.g.

```
summaries/
  metrics.json
  attrs.json
```

Technically op def defined attrs aren't summaries though. But having
these in two places is a bad idea I think.

Should such summaries be included in meta? I think so, they're like
output.

Is there a distinction between op def attrs and logged attrs?

## Image thumbnails

Might it make sense to write small image thumbnails to meta?

Or maybe there's a new side car in play - `<run_id>.thumb`

Adding images to meta is a sure way to kill status update performance.
But it is nice to support some preview when viewing the run when the run
dir isn't available. These could be shown as low res placeholders and,
when clicked (or some other action) are downloaded in full resolution
from the run dir.

## Distributed training

How does Gage ML handle a "run" that's distributed across many systems?

This is where loggers are arguably a better architecture as they're less
complicated and tied to the underlying process.

Can we opt into a logging model in such cases? What would this look like?

## Mobile interface

Keeping tabs on runs from a mobile app would be very, very nice!

How would this work? Setup a share or something that shows a QR code,
scan that and then you have the ability to sync with a repo?

## Optuna interface

- Try to avoid `--optimize` with the `run` command -- it adds a lot of
  complexity

- Consider `gage optimize` -- this will look a lot like `run` but will
  move any optimization related options out of run

- Look around for previous results - look around the world even

There's opportunity here to feature the advantages of distribution:

- Collect previous trials from other runs (flag values and results)
- Use to suggest flag values
- Support pruning/early termination

The value of Optuna here is pruning/early termination.

The value of Gage for this case:

- Don't change your code to even think about hyperparameter tuning
- Gage's best-of-class visualization

## Use cases

### Running

- Basic run
- Custom config via flags
- Batches (grid, random, drive-from-file)
- Restart a run to train some more or to apply a code fix (not handled
  yet - need to! will be implemented by creating a new run - there are
  no restarts in Gage)
- Distributed training
  - Works with Ray
- Optimization with Optuna (can hide the Optuna part)

### Repos, remote copy/sync

- Archives runs of interest (or all runs?)
  - GitHub
  - DropBox
  - Cloud storage

- Sync with a colleague (sharing)

- Backup runs of import (safety)

- Archive runs for potential future use (organization)

- Get status of remote run (e.g. training on another system)

### Higher Level

- Find a "best" run
- Generate a report for a set of runs (summary ops, uses run summary
  dependency)
- Evaluate a run after the fact

### Ecosystem of reuse

- Publish something to a Gage ML public repo
- Reference a run ID that's stored in a Gage ML public repo as a dependency
- Use a HF training scenario as an example
- Can we start hosting these pre-trained whatever to seed their use?

### Platform scenarios

- Use GitHub actions to run experiments and publish results (demo)
