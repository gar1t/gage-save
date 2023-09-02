# Gage To Do

## Run layout

- Init run by creating `.meta`
- Copy source code to `.run`
- As copying source code, update manifest in `.meta`


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
