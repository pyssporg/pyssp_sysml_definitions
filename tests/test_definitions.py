"""The shipped vocabulary: package data, packages, and conditional loading."""

from __future__ import annotations

from pathlib import Path

from pyssp_sysml_definitions import (
    CORE_FILE,
    INTEROP_FILE,
    core_definitions,
    include_roots,
    interop_definitions,
    load_with_interop,
)


class _Architecture:
    """The only part of a loaded architecture ``load_with_interop`` reads."""

    def __init__(self, imports: dict[str, object]) -> None:
        self.imports = imports


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


def test_load_with_interop_skips_the_library_without_an_import() -> None:
    calls: list[tuple[object, tuple[object, ...]]] = []

    def load(source, *roots):
        calls.append((source, roots))
        return _Architecture({})

    result = load_with_interop("model.sysml", load, includes=["lib"])

    assert result.imports == {}
    assert calls == [("model.sysml", ("lib",))]


def test_load_with_interop_adds_the_library_when_imported() -> None:
    calls: list[tuple[object, tuple[object, ...]]] = []

    def load(source, *roots):
        calls.append((source, roots))
        return _Architecture({"PyfmiInterop": object()})

    load_with_interop("model.sysml", load)

    assert calls == [
        ("model.sysml", ()),
        ("model.sysml", (interop_definitions(),)),
    ]


def test_an_include_root_can_make_the_import_visible() -> None:
    calls: list[tuple[object, tuple[object, ...]]] = []

    def load(source, *roots):
        calls.append((source, roots))
        imports = {"PyfmiInterop": object()} if "lib" in roots else {}
        return _Architecture(imports)

    load_with_interop("model.sysml", load, includes=["lib"])

    assert calls == [
        ("model.sysml", ("lib",)),
        ("model.sysml", ("lib", interop_definitions())),
    ]
