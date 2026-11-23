# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- `InteropMetadata` now extends `SourcedMetadata` and inherits `source` instead
  of declaring it again, so a build-metadata family container is recognized by
  reaching the shared base rather than by name. `docs/roles.md` no longer
  carves out a name-based exception for it.
- Documented the three-role contract — build metadata, initialization
  configuration, runtime signal — as a short statement in `core.sysml` and a
  long-form `docs/roles.md` with rationale, a worked example, and anti-patterns;
  consuming libraries cite them instead of restating them.

### Removed

- `load_with_interop`: export selection is composition policy, so it moved to
  `pyfmi_sysml`. The package now exposes paths and package data only.

## [0.1.0] - 2026-11-22

### Added

- The `PysspCore` vocabulary, moved verbatim from `pycps_sysml2`, with
  `core_definitions()` and the `CORE_FILE` file name.
- The `PyfmiInterop` vocabulary, moved verbatim from `pyfmi_interop`, with
  `interop_definitions()` and the `INTEROP_FILE` file name.
- `include_roots()` for the whole vocabulary, and `load_with_interop()`, which
  adds the interop root only when the architecture imports `PyfmiInterop`.
- Real-path resolution through `importlib.resources`, refusing a zipped install
  instead of handing a non-path to a loader.
