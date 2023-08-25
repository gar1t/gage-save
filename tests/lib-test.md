---
test-options: +parse
---

# Vista test support

## Example pattern matching

### Semantic versions

Use `semver` to match valid semantic versions.

    >>> ["0.1.2", "2.0.10", "0.0.0-rc2"]
    ['{:semver}', '{:semver}', '{:semver}']

Failure cases:

    >>> "0.0.0.1"  # +fails
    {:semver}

### Paths

Paths can be matched with the `path` type.

    >>> "/usr/bin/git"
    '{:abspath}'
