# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import *


class OpDefNotFound(Exception):
    pass


class OpDef:
    def __init__(self, name: str):
        self.name = name


class Flag:
    pass


class Dependency:
    def __init__(self, type: str):
        self.type = type
        # TODO: select, name, etc. from Guild


r""" Dependency notes

```json
[
  {
    "type": "runfiles",
    "run.select": "op in [prepare-data, prepare]",  # canonical
    "operation": "prepare",  # shorthand for 'run.select: op=prepare'
    "files.select": ["data.csv"]  # or use alias 'select'
  },
  {
    "type": "dir",
    "path": "data"
  },
  {
    "type": "file",
    "path": "data.csv"
  },
  {
    "type": "dvcfile",
    "path": "data.csv"
  }
]
```

- Continue to support single string specs with a URI like syntax. E.g.
  'dvcfile: data.csv' is coerced to the example above. A more complex
  case might be 'runfiles: op=prepare-data'

- For select use glob pattern unless string is prefixed with 'regex:' -
  e.g. 'regex:data\.(csv|txt)'

- Do we want to support sha256 for 1.0 or add that back later? I don't
  think this is used much.

- Do we want to support downloads or remote files? We could punt to use
  DvC at that point.

- Drop use of pip download support! If we continue to support downloads
  use anyting else. Might just drop download support for 1.0 though.

"""


def opdef_to_opspec(opdef: OpDef, cwd: Optional[str] = None):
    return opdef.name
