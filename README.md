# pyssp-sysml-definitions

The installable SysML vocabulary shared by the artifact families. External
applications can author against it, and a family can extend it without copying
the core.

The package ships two ordinary SysML libraries as package data:

- `core.sysml` — `package PysspCore`, the role markers, metadata schemas,
  parameter markers, and experiment containers;
- `interop.sysml` — `package PyfmiInterop`, the interop identity, deployment
  port, and standalone FMU base. It imports `PysspCore::*`.

It has no runtime dependencies and no parser. A consumer supplies its own
loader:

```python
from pyssp_sysml_definitions import core_definitions, interop_definitions

architecture = load(model, core_definitions())
```

## API

- `CORE_FILE` / `INTEROP_FILE` — the package-data file names;
- `core_definitions()` / `interop_definitions()` — real file paths, refusing a
  zipped install;
- `include_roots()` — both roots, core first;
- `load_with_interop(source, load, includes=())` — loads the source and adds the
  interop root only when the architecture imports `PyfmiInterop`; `load` is
  injected so this package stays dependency-free.

## Install

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

Requires Python 3.11 or newer.

## Extending

An artifact family keeps its own vocabulary in its own package and includes
these files as roots. Do not edit a shipped `.sysml` file downstream: add a new
library that imports the shared packages.

## Version

The initial release is 0.1.0. See `CHANGELOG.md`; contributors read `AGENTS.md`.
