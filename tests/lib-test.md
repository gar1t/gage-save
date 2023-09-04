---
test-options: +parse
---

# gage test support

## Pattern matching

### Semantic versions

Use `semver` to match valid semantic versions.

    >>> ["0.1.2", "2.0.10", "0.0.0-rc2"]
    ['{:ver}', '{:ver}', '{:ver}']

Failure cases:

    >>> "0.0.0.1"  # +fails
    {:semver}

### Paths

Paths can be matched with the `path` type.

    >>> "/usr/bin/git"
    '{:path}'

Paths must be absolute to match.

    >>> "bin/git"  # +fails
    '{:path}'

### Any value

`any` is used to match anything within the same line. This is an
important distinction from `{}`, which matches across lines. It's
important to avoid `{}` when it might consume output that would
otherwise negate a successful test.

The following test makes this mistake:

    >>> print("""SUCCESS: well done!
    ...
    ... ERROR: I was joking earlier""" )
    SUCCESS: {}

The example should use `any`.

    >>> print("""SUCCESS: well done!
    ...
    ... ERROR: I was joking earlier""")  # +fails
    SUCCESS: {:any}

### Dates

ISO 8601 formats:

    >>> print("2023-09-03T11:21:33-0500")
    {:date}

    >>> print("2023-09-03T11:21:33+0500")
    {:date}

    >>> print("2023-09-03T11:21:33+050030")
    {:date}

Valid formats but not supported:

    >>> print("2023-09-03T11:21:33-05:00")  # +fails
    {:date}

    >>> print("2023-09-03T11:21:33-05:00:30")  # +fails
    {:date}
