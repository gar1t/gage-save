# File Utils

The module `gage._internal.file_util` implements advanced file utilities.

    >>> from gage._internal import file_util

## Test for file difference

Use `util.files_differ()` to check if two files differ.

    >>> from gage._internal.file_util import files_differ

Write some files to test:

    >>> tmp = make_temp_dir()

    >>> with open(path_join(tmp, "a"), "wb") as f:
    ...     _ = f.write(b"abc123")

    >>> with open(path_join(tmp, "b"), "wb") as f:
    ...     _ = f.write(b"abc1234")

    >>> with open(path_join(tmp, "c"), "wb") as f:
    ...     _ = f.write(b"abc321")

    >>> with open(path_join(tmp, "d"), "wb") as f:
    ...     _ = f.write(b"abc123")

Compare the files:

    >>> files_differ(path_join(tmp, "a"), path_join(tmp, "a"))
    False

    >>> files_differ(path_join(tmp, "a"), path_join(tmp, "b"))
    True

    >>> files_differ(path_join(tmp, "a"), path_join(tmp, "c"))
    True

    >>> files_differ(path_join(tmp, "a"), path_join(tmp, "d"))
    False

Compare links:

    >>> symlink("a", path_join(tmp, "link-to-a"))

    >>> symlink("link-to-a", path_join(tmp, "link-to-link-to-a"))

    >>> files_differ(
    ...     path_join(tmp, "a"),
    ...     path_join(tmp, "link-to-a")
    ... )
    False

    >>> files_differ(
    ...     path_join(tmp, "a"),
    ...     path_join(tmp, "link-to-link-to-a")
    ... )
    False

    >>> files_differ(
    ...     path_join(tmp, "link-to-a"),
    ...     path_join(tmp, "link-to-link-to-a")
    ... )
    False

## Files digest

A single digest is generated for a directory using `files_digest`.

Use `textorbinary` sample files to generate a digest.

    >>> sample_dir = sample("textorbinary")

    >>> file_util.files_digest(findl(sample_dir), sample_dir)
    '0c5df8c6437e23df5371bdd1b5db7bc9'

## Testing text files

Use `is_text_file` to test if a file is text or binary. This is used
to provide a file viewer for text files.

    >>> from gage._internal.file_util import is_text_file

The test uses known file extensions as an optimization. To test the
file content itself, we need to ignore extensions:

    >>> def is_text(sample_path):
    ...     path = sample("textorbinary", sample_path)
    ...     return is_text_file(path, ignore_ext=True)

Our samples:

    >>> is_text("cookiecutter.json")
    True

    >>> is_text("empty.pyc")
    False

    >>> is_text("empty.txt")
    True

    >>> is_text("hello.py")
    True

    >>> is_text("hello_world.pyc")
    False

    >>> is_text("lena.jpg")
    False

    >>> is_text("lookup-error")
    False

    >>> is_text("lookup-error.txt")
    True

A non-existing file generates an error:

    >>> is_text("non-existing")  # +wildcard
    Traceback (most recent call last):
    OSError: .../samples/textorbinary/non-existing does not exist

Directories aren't text files:

    >>> is_text(".")
    False
