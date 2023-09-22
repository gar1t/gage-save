---
parse-types:
  timestamp: 1[6-7]\d{11}
---

# Run output

Run output is logged and read using facilities in
`gage._internal.run_output`.

    >>> from gage._internal.run_output import *

Output is written to two files: a plain text file containing merged
stderr and stdout output and an index, which annotates each logged line
with a timestamp and a stream time (err or out).

Create a sample script to generate output.

    >>> cd(make_temp_dir())

    >>> write("test.py", """
    ... import sys
    ...
    ... for i in range(5):
    ...     sys.stdout.write(f"stdout line {i}\\n")
    ...     sys.stdout.flush()
    ...     sys.stderr.write(f"stderr line {i}\\n")
    ... """)

Create a run output instance.

    >>> output = RunOutput("output")

Output is read from process output via `output.open()`. Create a process
to read from. To read both stdout and stderr, use pipes for each stream.

    >>> import subprocess

    >>> proc = subprocess.Popen(
    ...     [sys.executable, "test.py"],
    ...     stdout=subprocess.PIPE,
    ...     stderr=subprocess.PIPE,
    ... )

Open run output with the process.

    >>> output.open(proc)

Process output is read using background threads.

Wait for the process to exit.

    >>> proc.wait()
    0

Wait for output to be written.

    >>> output.wait_and_close(timeout=1.0)

Two files are generated.

    >>> ls()
    output
    output.index
    test.py

The output log contains process output.

    >>> cat("output")
    stdout line 0
    stdout line 1
    stdout line 2
    stdout line 3
    stdout line 4
    stderr line 0
    stderr line 1
    stderr line 2
    stderr line 3
    stderr line 4

While output can be read directly from `output_filename` as a text file,
a run output reader provides timestamp and stream type information for
each line.

    >>> with RunOutputReader("output") as reader:  # +parse
    ...     for timestamp, stream, line in reader:
    ...         print(timestamp, stream, line)
    {:timestamp} 0 stdout line 0
    {:timestamp} 0 stdout line 1
    {:timestamp} 0 stdout line 2
    {:timestamp} 0 stdout line 3
    {:timestamp} 0 stdout line 4
    {:timestamp} 1 stderr line 0
    {:timestamp} 1 stderr line 1
    {:timestamp} 1 stderr line 2
    {:timestamp} 1 stderr line 3
    {:timestamp} 1 stderr line 4
