"""The shipped vocabulary: package data, packages, and path helpers."""

from __future__ import annotations

import ast
from pathlib import Path

import pyssp_sysml_definitions
from pyssp_sysml_definitions import (
    CORE_FILE,
    INTEROP_FILE,
    core_definitions,
    include_roots,
    interop_definitions,
)

ROOT = Path(__file__).resolve().parents[1]


def test_both_vocabulary_files_ship_as_package_data() -> None:
    core = core_definitions()
    interop = interop_definitions()

    assert CORE_FILE == "core.sysml"
    assert INTEROP_FILE == "interop.sysml"
    for path in (core, interop):
        assert isinstance(path, Path)
        assert path.is_file()
    assert core.name == CORE_FILE
    assert interop.name == INTEROP_FILE
    assert core.parent.name == interop.parent.name == "pyssp_sysml_definitions"


def test_the_files_declare_the_expected_packages() -> None:
    core_text = core_definitions().read_text(encoding="utf-8")
    interop_text = interop_definitions().read_text(encoding="utf-8")

    assert "package PysspCore {" in core_text
    assert "package PyfmiInterop {" in interop_text
    assert "import PysspCore::*;" in interop_text


def test_include_roots_contains_the_core_then_the_interop_vocabulary() -> None:
    assert include_roots() == (core_definitions(), interop_definitions())


def test_the_public_surface_is_path_helpers_only() -> None:
    """Export selection is composition policy, not vocabulary."""

    assert set(pyssp_sysml_definitions.__all__) == {
        "CORE_FILE",
        "INTEROP_FILE",
        "core_definitions",
        "include_roots",
        "interop_definitions",
    }
    assert not hasattr(pyssp_sysml_definitions, "load_with_interop")


def test_the_module_imports_no_parser_or_artifact_family() -> None:
    """The package stays dependency-free: no loader, no FMI or SSP import."""

    tree = ast.parse(
        (ROOT / "src" / "pyssp_sysml_definitions" / "__init__.py").read_text(
            encoding="utf-8"
        )
    )
    imported: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.append(node.module)

    assert imported, "the module should import only the standard library"
    allowed = {"__future__", "collections", "importlib", "pathlib", "typing"}
    assert {name.split(".")[0] for name in imported} <= allowed, imported


def test_the_vocabulary_files_are_declared_for_packaging() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    manifest = (ROOT / "MANIFEST.in").read_text(encoding="utf-8")

    assert 'pyssp_sysml_definitions = ["*.sysml"]' in pyproject
    assert "recursive-include src/pyssp_sysml_definitions *.sysml" in manifest
