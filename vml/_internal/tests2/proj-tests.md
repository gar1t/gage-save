---
test-type: python
---

TODO: Remove test-type in front-matter when Groktest is in full-effect.

# Vista ML Tests

Vista ML tests are in the process of being migrated to
[Groktest](https://github.com/gar1t/groktest/). Groktest simplifies
Vista's built-in test runner and provides some key features missing in
`doctest`.

## Basic usage

Groktest uses the same format for test examples as `doctest`.

    >>> 1 + 1
    2

Groktest provides a more sophisticated pattern matching scheme, which
uses a format specification to match examples.

The following examples assert that test results are a series of digits.

    >>> 1 + 1
    {:d}

    >>> 100 + 100
    {:d}
