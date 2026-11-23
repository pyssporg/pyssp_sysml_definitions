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

## Roles

The vocabulary defines the role of every fact a model declares, and the carrier
decides which: build metadata, initialization configuration, or runtime signal.
The contract — the roles, their carriers, the reserved `parameters` usage name,
and each marker's fields — is stated once, in `core.sysml`, next to the markers
it governs. Consuming libraries implement recognition and document how a role
lands in their artifacts; they reference `core.sysml` instead of restating it.

`interop.sysml` is the worked example: `InteropDeployment` is initialization
configuration bound before initialization and never a wire field.

The long-form rationale, a full model example, and the anti-patterns are in
[`docs/roles.md`](docs/roles.md).

## API

- `CORE_FILE` / `INTEROP_FILE` — the package-data file names;
- `core_definitions()` / `interop_definitions()` — real file paths, refusing a
  zipped install;
- `include_roots()` — both roots, core first.

The package has no loader and no export-selection policy. A composition layer
supplies its own loader and decides when to include a root; for FMI that is
`pyfmi_sysml.load_with_interop`.

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
