# Style Guideliness

As specified in `CONTRIBUTING.md`, patches to this project should
adhere to the styles specified in this document.

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”,
“SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this
document are to be interpreted as described in [RFC
2119](https://datatracker.ietf.org/doc/html/rfc2119).

The terms "PATCH", "CONTRIBUTOR", and "MAINTAINER" used in this
document are defined in `CONTRIBUTING.md`.

## Python soure code formatting

### Rules

1. Code SHOULD clearly reflect the intention of its author. Code that
   is confusing to readers MAY be rewritten by any Contributor with
   the intent of improving its clarity.

2. A section of code SHOULD be understanable upon reading in a short
   period of time (e.g. less than 2-3 minutes).

3. Functions SHOULD be used in favor of code block to define the scope
   of code.

4. Object oriented patterns (classes and inheritence) SHOULD be
   avoided in favor of functions.

5. Object oriented patterms MAY be used when there is no better
   alternative.

6. All variable and function names MUST use [snake
   case](https://en.wikipedia.org/wiki/Snake_case).

7. All class names MUST use [upper camel
   case](https://en.wikipedia.org/wiki/Camel_case).

8. Functions intended for use within a module are considered "private"
   and MUST be named with a leading underscore character.

9. Functions used outside a module are considered "public" and MUST
   NOT be named with a leading underscore.

10. When using classes, avoid static methods (i.e. methods defined
    using the `staticmethod` decorator) and instead use module level
    private functions that are associated with the class in proximity
    within the module source code file.

11. Names SHOULD be as short as possible without compromising clarity.

12. Names SHOULD follow establised naming conventions and patterns in
    the project code base. Contributors SHALL be free to rename
    variables, functions, etc. to improve readability or improve the
    consistency of code. Such changes MUST NOT be capricious or
    arbitrary and MAY be reverted if deemed so by maintainers.

### Automatic formatting

This project uses the code formatting tool
[YAPF](https://github.com/google/yapf) to automate code formatting for
Python source code. The application of this tool may be automated by
running the following command:

    $ yapf -vv -r -i <Python files and packages>

Rules used by YAPF are defined in `pyproject.toml` in the
`[tool.yapf]` section. These rules as applied by YAPF constitute the
required code formatting style for this project.

### Comment-configured line breaks

In some cases it may be necessary to use hash characters in Python
within an expression to control how YAPF formats that expression.

For example, the following function uses a series of conditional
boolean tests:

``` python
def _has_non_path_options(params):
    return (
        params.get("env") or params.get("flags") or params.get("attrs")
        or params.get("deps")
    )
```

The return expression would be clearer if each test occurred on a
separate line. In this case, YAPF can be made to adhere to an ad hoc
style using a single comment character as follows:

``` python
def _has_non_path_options(params):
    return (
        params.get("env")  #
        or params.get("flags")  #
        or params.get("attrs")  #
        or params.get("deps")
    )
```

This technique is an unfortunate requirement in the use of YAPF, which
otherwise makes a less-readable formatting decision.

The of of comment characters to control formatting in this way should
be used sparingly.

### Other style considerations

Where YAPF formatting does not apply, consult [PEP
8](https://peps.python.org/pep-0008/).

## Reformatting patches

A Contributor or Maintainer may reformat a patch to apply styles
defined in this guide or to apply styles of their choosing that are
not otherwise documented ("Ad Hoc styles"). Ad hoc styles are subject
to further revision. Ad hoc styles
