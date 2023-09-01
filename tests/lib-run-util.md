# Run utils

General run utilities are provided by `gage._internal.run_util`.

## Run output

Run output can be read using util.RunOutputReader.

    >>> from gage._internal.run_util import RunOutputReader

For these tests, we'll use a sample run:

    >>> run_dir = sample("runs/7d145216ae874020b735f001a7bfd27d")

Our reader:

    >>> reader = RunOutputReader(run_dir)

We use the `read` method to read output. By default `read` returns all
available output.

    >>> reader.read()  # +pprint
    [(1524584359781, 0, 'Tue Apr 24 10:39:19 CDT 2018'),
     (1524584364782, 0, 'Tue Apr 24 10:39:24 CDT 2018'),
     (1524584369785, 0, 'Tue Apr 24 10:39:29 CDT 2018'),
     (1524584374790, 0, 'Tue Apr 24 10:39:34 CDT 2018')]

We can alternatively read using start and end indices.

    >>> reader.read(0, 0)
    [(1524584359781, 0, 'Tue Apr 24 10:39:19 CDT 2018')]

    >>> reader.read(1, 1)
    [(1524584364782, 0, 'Tue Apr 24 10:39:24 CDT 2018')]

    >>> reader.read(2, 3)  # +pprint
    [(1524584369785, 0, 'Tue Apr 24 10:39:29 CDT 2018'),
     (1524584374790, 0, 'Tue Apr 24 10:39:34 CDT 2018')]

If start is omitted, output is read form the start.

    >>> reader.read(end=2)  # +pprint
    [(1524584359781, 0, 'Tue Apr 24 10:39:19 CDT 2018'),
     (1524584364782, 0, 'Tue Apr 24 10:39:24 CDT 2018'),
     (1524584369785, 0, 'Tue Apr 24 10:39:29 CDT 2018')]

If end is omitted, output is read to the end.

    >>> reader.read(start=2)  # +pprint
    [(1524584369785, 0, 'Tue Apr 24 10:39:29 CDT 2018'),
     (1524584374790, 0, 'Tue Apr 24 10:39:34 CDT 2018')]

When we're run reading we can close the reader:

    >>> reader.close()
