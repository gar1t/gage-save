# File select / copy tree support

The `file_select` module provides rules-based copy file support. Its two
main functions are `copyfiles` and `copytree`. Both functions use the
same file selection scheme. `copyfiles` selects from a list of files.
`copytree` selects files under a root directory.

    >>> from gage._internal.file_select import *

## Support functions

Functions for generating test files:

    >>> from gage._internal.file_util import ensure_dir

    >>> def make_src(specs):
    ...     src = make_temp_dir()
    ...     for spec in specs:
    ...         spec.mk(src)
    ...     return src

    >>> class file_base(object):
    ...     def __init__(self, path, write_mode, base_char, size):
    ...         self.path = path
    ...         self.write_mode = write_mode
    ...         self.base_char = base_char
    ...         self.size = size
    ...
    ...     def mk(self, root):
    ...         path = path_join(root, self.path)
    ...         ensure_dir(os.path.dirname(path))
    ...         with open(path, "w" + self.write_mode) as f:
    ...             f.write(self.base_char * self.size)

    >>> def empty(path):
    ...     return text(path)

    >>> def text(path, size=0):
    ...     return file_base(path, "", "0", size)

    >>> def binary(path, size):
    ...     return file_base(path, "b", b"\x01", size)

## Copy list

`copyfiles` selects files from a provided list.

Create a source list to copy.

    >>> src = make_src([
    ...     empty("a"),
    ...     empty("sub-1/b"),
    ...     empty("sub-2/c"),
    ... ])

    >>> ls(src)
    a
    sub-1/b
    sub-2/c

Copy all files to a new directory.

    >>> dest = make_temp_dir()

    >>> copyfiles(src, dest, ["a", "sub-1/b", "sub-2/c"])

    >>> ls(dest)
    a
    sub-1/b
    sub-2/c

Define a select spec that matches files named 'b'. The spec uses a
single `include` rule to match a file name pattern.

    >>> b_select = FileSelect([include(["b"])])

    >>> dest = make_temp_dir()

    >>> copyfiles(src, dest, ["a", "sub-1/b", "sub-2/c"], b_select)

    >>> ls(dest)
    sub-1/b

The filter mechanism supports a variety of tests beyond name matching.
These are covered in the **Copy tree** tests below.

## Copy tree

`copytree` is like `copyfiles` in that it uses an optional filter
mechanism to select files to copy. Unlike `copyfiles`, which uses an
explicit list of file candidates, `copytree` scans the source directory
for files to copy.

Select configuration is a list of rules, which can exclude or include
files based on file attributes.

Attributes include:

- Name
- Size
- Type (text file, binary file, or directory)
- Number of files previously selected by the rule

`copytree` uses a copy handler, which provides an optional *select*
specification. The spec tells the handler whether or not to copy a file.
It also tells `copytree` whether or not to scan the contents of a
directory in the first place.

Define a function that copies files from a source directory to a new
destination using `copytree` and select rules. The function prints the
copied files.

    >>> def copy_src(src, select_rules, handler=None):
    ...     dest = make_temp_dir()
    ...     select = FileSelect(select_rules)
    ...     copytree(src, dest, select, handler)
    ...     ls(dest)

### Basic file selection

Here's a src containing a single text file:

    >>> src = make_src([empty("a.txt")])
    >>> ls(src)
    a.txt

Without any rules, `copytree` will not copy any files:.

    >>> copy_src(src, [])
    <empty>

Include all files using a '*' include rule.

    >>> copy_src(src, [include("*")])
    a.txt

Rules are evaluated in the order specified. The last rule to match a
file is the applied rule.

Include all files and then exclude all files.

    >>> copy_src(src, [include("*"), exclude("*")])
    <empty>

Reverse the logic again.

    >>> copy_src(src, [include("*"), exclude("*"), include("*")])
    a.txt

Create a more complex source directory structure.

    >>> src = make_src([
    ...     empty("a.txt"),
    ...     empty("d1/a.txt"),
    ...     empty("d1/d1_1/b.txt"),
    ...     empty("d1/d1_2/c.txt"),
    ...     empty("d2/d.txt"),
    ...     empty("d2/d.yml"),
    ... ])

As before, the default is to copy nothing.

    >>> copy_src(src, [])
    <empty>

Include all files.

    >>> copy_src(src, [include("*")])
    a.txt
    d1/a.txt
    d1/d1_1/b.txt
    d1/d1_2/c.txt
    d2/d.txt
    d2/d.yml

Include only files with `.txt` extension.

    >>> copy_src(src, [include("*.txt")])
    a.txt
    d1/a.txt
    d1/d1_1/b.txt
    d1/d1_2/c.txt
    d2/d.txt

Include only files with `.yml` extension.

    >>> copy_src(src, [include("*.yml")])
    d2/d.yml

Select all files under `d1` subdirectory.

    >>> copy_src(src, [include("d1/*")])
    d1/a.txt
    d1/d1_1/b.txt
    d1/d1_2/c.txt

Specify multiple patterns.

    >>> copy_src(src, [include(["d1/a.txt", "d1/d1_1/*"])])
    d1/a.txt
    d1/d1_1/b.txt

Note that a single '*' matches all files under the prefix. This is the
behavior of Python's `fnmatch` module, which Gage uses to match files.

To select only `d1/a.txt` and ignore other files under `d1`, use an
exclude rule.

    >>> copy_src(src, [include("d1/*"), exclude("d1/d1*")])
    d1/a.txt

This approach assumes that there are no other files match the pattern
`d1/d1*`. This happens to work in this case to exclude subdirectories
but only because the subdirectories start with 'd1'.

To select all files but not subdirectories, use a regular expression
pattern.

    >>> copy_src(src, [include("d1/[^/]+$", regex=True)])
    d1/a.txt

### Skipping directories

Directories can be skipped using a `dir` type exclude rule. Skipping a
directory saves time by not scanning and testing its files.

Create a simple layout that includes a directory.

    >>> src = make_src([
    ...     empty("a.txt"),
    ...     empty("d/b.txt"),
    ...     empty("d/c.txt"),
    ... ])

    >>> ls(src)
    a.txt
    d/b.txt
    d/c.txt

Copy the files, skipping the `d` directory.

    >>> copy_src(src, [include("*"), exclude("d", type="dir")])
    a.txt

The same is achieved by including `a.txt`.

    >>> copy_src(src, [include("a.txt")])
    a.txt

However, in the first case, the directory `d` is skipped. In the second
case, the contents of `d` are evaluated against the include rule.

To see what the copy process does in both cases, use a custom handler
that logs ignored files.

    >>> class LogHandler(FileCopyHandler):
    ...     def ignore(self, ignored_src, results):
    ...         print(f"Ignored {os.path.relpath(ignored_src, src)}")

Run the first case again using the custom handler.

    >>> copy_src(src, [include("*"), exclude("d", type="dir")], LogHandler())
    Ignored d
    a.txt

Run the second case.

    >>> copy_src(src, [include("a.txt")], LogHandler())
    Ignored d/b.txt
    Ignored d/c.txt
    a.txt

When excluding directories containing many files, this optimization
saves time.

### Selecting text or binary files

File select rules can specify whether a file is text or binary.

Create a layout with both text and binary files.

    >>> src = make_src([
    ...     text("a.txt", 10),
    ...     binary("a.bin", 10),
    ... ])

    >>> ls(src)
    a.bin
    a.txt

Use a `text` type rule to select text files.

    >>> copy_src(src, [include("*", type="text")])
    a.txt

Use `binary` to select binary files.

    >>> copy_src(src, [include("*", type="binary")])
    a.bin

### Skipping special directories

Directories containing sentinel files can be skipped using a combination
of `dir` type and a `sentinel` path for a rule.

Consider the following structure:

    >>> src = make_src([
    ...     empty("skip_dir/.nocopy"),
    ...     empty("skip_dir/a.txt"),
    ...     empty("skip_dir/b.txt"),
    ...     empty("venv/bin/activate"),
    ...     empty("venv/c.txt"),
    ...     empty("keep_dir/d.txt"),
    ...     empty("e.txt"),
    ... ])

There are two cases that are candidates for skipping: the directory
`skip_dir` containing `.nocopy` and the directory `venv`, which looks
like a virtual environment.

To exclude `skip_dir` and `venv`, use `dir` type rules that specify the
applicable sentinel path.

    >>> copy_src(src, [
    ...     include("*"),
    ...     exclude("*", type="dir", sentinel=".nocopy"),
    ...     exclude("*", type="dir", sentinel="bin/activate"),
    ... ])
    e.txt
    keep_dir/d.txt

As with any set of rules, a new rule can be added to modify the select
behavior. In this case we include `venv`.

    >>> copy_src(src, [
    ...     include("*"),
    ...     exclude("*", type="dir", sentinel=".nocopy"),
    ...     exclude("*", type="dir", sentinel="bin/activate"),
    ...     include("venv", type="dir"),
    ... ])
    e.txt
    keep_dir/d.txt
    venv/bin/activate
    venv/c.txt

### Skipping files by size

Use `size_gt` or `size_lt` attributes to indicate that a file should be
select based on its size.

Create a source directory containing two files.

    >>> src = make_src([
    ...   empty("small.txt"),
    ...   text("large.txt", size=100),
    ... ])

Copy only the small file by including only files less than 100 bytes.

    >>> copy_src(src, [include("*", size_lt=100)])
    small.txt

Copy the large file.

    >>> copy_src(src, [include("*", size_gt=99)])
    large.txt

### Skipping files after a number of matches

A select rule can use `max_matches`, which specifies the maximum number
of matches the rule can make before it stops matching. This is used to
prevent copying an unexpectedly large number of files.

Create a structure containing ten files.

    >>> src = make_src([empty(f"{i}.txt") for i in range(10)])
    >>> ls(src)
    0.txt
    1.txt
    2.txt
    3.txt
    4.txt
    5.txt
    6.txt
    7.txt
    8.txt
    9.txt

Limit the number of included files to 6.

    >>> copy_src(src, [include("*.txt", max_matches=6)])
    0.txt
    1.txt
    2.txt
    3.txt
    4.txt
    5.txt

### Custom copytree handlers

Custom handlers are used to change the copy behavior.

Create a custom handler that logs information and does not copy
anything.

    >>> class Handler:
    ...     def __init__(self, src):
    ...         self.src = src
    ...
    ...     def copy(self, src, dest, select_results):
    ...         print("copy:", os.path.relpath(src, self.src))
    ...
    ...     def ignore(self, src, select_results):
    ...         print("ignore:", os.path.relpath(src, self.src))
    ...
    ...     def close(self):
    ...         pass

Create some files.

    >>> src = make_src([
    ...     empty("a.txt"),
    ...     binary("a.bin", size=1),
    ... ])

Call `copy_src` with a custom handler. Nothing is copied but we see what
would be copied and what is ignored.

    >>> handler = Handler(src)

    >>> copy_src(src, [include("*")], handler)
    copy: a.bin
    copy: a.txt
    <empty>

    >>> copy_src(src, [include("*.bin")], handler)
    copy: a.bin
    ignore: a.txt
    <empty>

    >>> copy_src(src, [include("*", size_lt=1)], handler)
    ignore: a.bin
    copy: a.txt
    <empty>

### Rule type validation

Valid rule types:

    >>> _ = include("*", type=None)
    >>> _ = include("*", type="text")
    >>> _ = include("*", type="binary")
    >>> _ = include("*", type="dir")

Invalid:

    >>> include("*", type="invalid")  # -space
    Traceback (most recent call last):
    ValueError: invalid value for type 'invalid':
    expected one of text, binary, dir
