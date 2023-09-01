---
test-options: +parse
---

# gage test support

## Example pattern matching

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

`any` is used to match anthing within the same line. This is an
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
