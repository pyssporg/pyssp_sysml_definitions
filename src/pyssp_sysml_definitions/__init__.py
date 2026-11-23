"""Installable, dependency-free SysML vocabulary shared by artifact families.

The package ships ordinary SysML definitions as package data, not a parser. A
consumer loads a file as an include root through its own loader; this package
never imports one. That keeps the vocabulary reusable by any artifact family
without pulling a dialect, an IR, or a parser into its dependency set.
"""

from __future__ import annotations

from importlib import resources
from pathlib import Path

__version__ = "0.1.0"

__all__ = [
    "CORE_FILE",
    "INTEROP_FILE",
    "core_definitions",
    "include_roots",
    "interop_definitions",
]

#: Name of the shared core vocabulary inside the package.
CORE_FILE = "core.sysml"

#: Name of the interop vocabulary inside the package.
INTEROP_FILE = "interop.sysml"


def _definition_path(filename: str, label: str) -> Path:
    """Return a bundled definition file as a real filesystem path.

    The file is package data. An unpacked install (editable checkout or wheel)
    yields a real ``Path``; a zipped install cannot expose one and is refused
    rather than handing a non-path to the loader.

    Raises:
        RuntimeError: The package is not installed as an unpacked directory.
        FileNotFoundError: The bundled definition file is absent.
    """
    path = resources.files(__package__).joinpath(filename)
    if not isinstance(path, Path):
        raise RuntimeError(
            "pyssp-sysml-definitions must be installed as an unpacked directory "
            f"so the bundled {label} definitions have a real file path"
        )
    if not path.is_file():
        raise FileNotFoundError(
            f"no {label} definitions found at {path}; "
            "reinstall pyssp-sysml-definitions"
        )
    return path


def core_definitions() -> Path:
    """Return the bundled ``PysspCore`` vocabulary as a real file path."""

    return _definition_path(CORE_FILE, "core")


def interop_definitions() -> Path:
    """Return the bundled ``PyfmiInterop`` vocabulary as a real file path."""

    return _definition_path(INTEROP_FILE, "interop")


def include_roots() -> tuple[Path, Path]:
    """Return both vocabulary roots, core first and interop second.

    This is the whole vocabulary, offered for a caller that wants every
    definition available. A composition layer decides whether an
    unconditional root would change which export unit its loader selects.
    """

    return (core_definitions(), interop_definitions())

