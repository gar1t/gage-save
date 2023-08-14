# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *

from ..._vendor import click

from .. import click_util

TOPICS: Dict[str, Tuple[str, str]] = {
    "remotes": (
        "Help with remotes.",
        """## Vista ML Remotes

Remotes are systems that Vista ML interacts with. Remotes are defined in user
configuration.

Remotes may be specified using either a name or an line specification.

See https://vistaml.org/remotes/ for details.

To list available remotes, use ``vml remotes``.
""",
    ),
    "filters": (
        "Help with run filter options.",
        """## Vista ML Filter Options

### Filter by Operation

Runs may be filtered by operation using `--operation`.  A run is only included
if any part of its full operation name, including the package and model name,
matches the value.

Use `--operation` multiple times to include more runs.

### Filter by Label

Use `--label` to only include runs with labels containing a specified value. To
select runs that do not contain a label, specify a dash '-' for `VAL`.

Use `--label` multiple times to include more runs.

### Filter by Tag

Use `--tag` to only include runs with a specified tag. Tags must match
completely and are case sensitive.

Use `--tag` multiple times to include more runs.

### Filter by Marked and Unmarked

Use `--marked` to only include marked runs.

Use `--unmarked` to only include unmarked runs. This option may not be used with
`--marked`.

### Filter by Expression

Use `--filter` to limit runs that match a filter expressions. Filter expressions
compare run attributes, flag values, or scalars to target values. They may
include multiple expressions with logical operators.

For example, to match runs with flag `batch-size` equal to 100 that have `loss`
less than 0.8, use:

    --filter 'batch-size = 10 and loss < 0.8'

**IMPORTANT:** You must quote EXPR if it contains spaces or characters that the
shell uses (e.g. '<' or '>').

Target values may be numbers, strings or lists containing numbers and strings.
Strings that contain spaces must be quoted, otherwise a target string values
does not require quotes. Lists are defined using square braces where each item
is separated by a comma.

Comparisons may use the following operators: '=', '!=' (or '<>'), '<', '<=',
'>', '>='. Text comparisons may use 'contains' to test for case-insensitive
string membership. A value may be tested for membership or not in a list using
'in' or 'not in' respectively. An value may be tested for undefined using 'is
undefined' or defined using 'is not undefined'.

Logical operators include 'or' and 'and'. An expression may be negated by
preceding it with 'not'. Parentheses may be used to control the order of
precedence when expressions are evaluated.

If a value reference matches more than one type of run information (e.g. a flag
is named 'label', which is also a run attribute), the value is read in order of
run attribute, then flag value, then scalar. To disambiguate the reference, use
a prefix `attr:`, `flag:`, or `scalar:` as needed. For example, to filter using
a flag value named 'label', use 'flag:label'.

Other examples:

    \b `operation = train and acc > 0.9` `operation = train and (acc > 0.9 or
    loss < 0.3)` `batch-size = 100 or batch-size = 200` `batch-size in
    [100,200]` `batch-size not in [400,800]` `batch-size is undefined`
    `batch-size is not undefined` `label contains best and operation not in
    [test,deploy]` `status in [error,terminated]`

**NOTE:** Comments and tags are not supported in filter expressions at this
time. Use `--comment` and `--tag` options along with filter expressions to
further refine a selection.

### Filter by Run Start Time

Use `--started` to limit runs to those that have started within a specified time
range.

**IMPORTANT:** You must quote RANGE values that contain spaces. For example, to
filter runs started within the last hour, use the option:

    --started 'last hour'

You can specify a time range using several different forms:

    \b `after DATETIME` `before DATETIME` `between DATETIME and DATETIME` `last
    N minutes|hours|days` `today|yesterday` `this week|month|year` `last
    week|month|year` `N days|weeks|months|years ago`

`DATETIME` may be specified as a date in the format ``YY-MM-DD`` (the leading
``YY-`` may be omitted) or as a time in the format ``HH:MM`` (24 hour clock). A
date and time may be specified together as `DATE TIME`.

When using ``between DATETIME and DATETIME``, values for `DATETIME` may be
specified in either order.

When specifying values like ``minutes`` and ``hours`` the trailing ``s`` may be
omitted to improve readability. You may also use ``min`` instead of ``minutes``
and ``hr`` instead of ``hours``.

Examples:

    \b `after 7-1` `after 9:00` `between 1-1 and 4-30` `between 10:00 and 15:00`
    `last 30 min` `last 6 hours` `today` `this week` `last month` `3 weeks ago`

### Filter by Source Code Digest

To show runs for a specific source code digest, use `-g` or `--digest` with a
complete or partial digest value.
""",
    ),
}


@click.command
@click.argument("topic", metavar="TOPIC", required=False)
def help(topic: Optional[str] = None):
    """Show Vista ML help."""
    if not topic:
        _print_general_help()
        raise SystemExit(0)
    topic_help = TOPICS.get(topic)
    if not topic_help:
        _print_unknown_topic_help(topic)
        raise SystemExit(1)
    _print_topic_help(topic_help[1])


def _print_general_help():
    out = click_util.HelpFormatter()
    assert help.__doc__
    out.write_text("Usage: vml help TOPIC")
    out.write_paragraph()
    out.write_text(help.__doc__)
    out.write_paragraph()
    out.write_heading("Topics")
    out.indent()
    out.write_dl([(topic, TOPICS[topic][0]) for topic in sorted(TOPICS)])
    print(out.getvalue(), end="")


def _print_unknown_topic_help(topic: str):
    out = click_util.HelpFormatter()
    out.write_text(f"Unknown help topic.")
    _maybe_print_similar(topic, out)
    out.write_paragraph()
    out.write_text("Available topics:")
    out.indent()
    out.write_dl([(topic, TOPICS[topic][0]) for topic in sorted(TOPICS)])
    print(out.getvalue(), end="")


def _maybe_print_similar(topic: str, out: click_util.HelpFormatter):
    import difflib

    similar = difflib.get_close_matches(topic, list(TOPICS))
    if similar:
        out.write_paragraph()
        out.write_text(f"Did you mean {similar[0]}?")


def _print_topic_help(doc: str):
    out = click_util.HelpFormatter()
    out.indent()
    out.write_text(doc)
    print(out.getvalue(), end="")
