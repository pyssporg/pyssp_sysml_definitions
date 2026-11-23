# AGENTS

## Rules

1. **Don't assume. Surface tradeoffs.** If a contract is ambiguous, stop and say
   so rather than picking a behaviour silently.
2. **Minimum code that solves the problem.** Nothing speculative.
3. **Touch only what you must.** Clean up only your own mess.
4. **Define success criteria and verify.**

## Repository Focus

`pyssp_sysml_definitions` ships the installable, dependency-free SysML
vocabulary that artifact families share: `core.sysml` (`package PysspCore`) and
`interop.sysml` (`package PyfmiInterop`). It has no parser and no runtime
dependencies; a consumer supplies its own loader.

- `core_definitions()` and `interop_definitions()` return real file paths and
  refuse a zipped install; `include_roots()` returns both, core first.
- Export selection and conditional includes are composition policy: they live
  in the consuming layer (for FMI, `pyfmi_sysml`), not here.
- The version lives in `src/pyssp_sysml_definitions/__init__.py` only;
  `pyproject.toml` is dynamic.
- `README.md` is the landing page, `docs/roles.md` the long-form role contract
  with rationale and examples, and the packaged `.sysml` files the vocabulary
  itself; `CHANGELOG.md` records releases.

## Hard constraints

- **No parser, no artifact.** Do not add a loader, parser dependency, artifact
  writer, or model semantics. The package ships files and resolves paths.
- **One copy of the vocabulary.** Edit a shipped `.sysml` file here and nowhere
  downstream; consumers include these files as roots and never copy them.
  Renaming or removing a public definition is a breaking vocabulary change:
  update the consumers and the drift tests in the same coordinated change.
- **Real paths only.** `importlib.resources` must resolve an unpacked directory;
  a zipped install is refused rather than handing a non-path to a loader.
- **Package data stays declared.** `pyproject.toml` and `MANIFEST.in` list the
  `.sysml` files so the wheel and sdist both carry them.
- **One statement per fact.** The vocabulary states roles, carriers, and
  reserved names once: short in `core.sysml`, long in `docs/roles.md`.
  Consuming repositories reference them and state only their own artifact
  landing.

## Workspace rule

The workspace is this checkout. Sibling repositories — `pycps_sysml2`,
`pyssp_sysml2`, `pyfmi_interfaces`, `pyfmi_interop`, `pyfmi_sysml`,
`pysos_sysml`, and the `pyssp_workflow` consumer — are read-only unless the
task explicitly names one. Never scan outside this checkout to infer a
contract, and never treat an installed copy as more authoritative than the
workspace source.

## Environment

- Python >= 3.11.
- Install: `python3 -m venv venv && . venv/bin/activate && pip install -e ".[dev]"`.
- Tests: `python -m pytest`; lint: `ruff check src tests` (configuration in
  `pyproject.toml` under `[tool.ruff]`).
- Build: `python -m build --wheel --sdist`.
