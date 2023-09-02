# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *
from typing import BinaryIO

import os
import errno
import struct


RunOutput = Tuple[float, int, str]


class RunOutputReader:
    def __init__(self, run_dir: str):
        self.run_dir = run_dir
        self._lines = []
        self._output: Optional[BinaryIO] = None
        self._index: Optional[BinaryIO] = None

    def read(self, start: int = 0, end: Optional[int] = None) -> List[RunOutput]:
        """Read run output from start to end.

        Both start and end are zero-based indexes to run output lines
        and are both inclusive. Note this is different from the Python
        slice function where end is exclusive.
        """
        self._read_next(end)
        if end is None:
            slice_end = None
        else:
            slice_end = end + 1
        return self._lines[start:slice_end]

    def _read_next(self, end: Optional[int]):
        if end is not None and end < len(self._lines):
            return
        try:
            output, index = self._ensure_open()
        except IOError as e:
            if e.errno != errno.EEXIST:
                raise
        else:
            lines = self._lines
            while True:
                line = output.readline().rstrip().decode()
                if not line:
                    break
                header = index.read(9)
                if len(header) < 9:
                    break
                time, stream = struct.unpack("!QB", header)
                lines.append((time, stream, line))
                if end is not None and end < len(self._lines):
                    break

    def _ensure_open(self):
        if self._output is None:
            guild_path = os.path.join(self.run_dir, ".guild")
            output = open(os.path.join(guild_path, "output"), "rb")
            index = open(os.path.join(guild_path, "output.index"), "rb")
            self._output, self._index = output, index
        assert self._output is not None
        assert self._index is not None
        return self._output, self._index

    def close(self):
        self._try_close(self._output)
        self._try_close(self._index)

    @staticmethod
    def _try_close(f: Optional[BinaryIO]):
        if f is None:
            return
        try:
            f.close()
        except IOError:
            pass
