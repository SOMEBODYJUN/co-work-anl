"""Small repository path and JSON helpers used by the live research runtime.

The old 2.5 curation module mixed these safety primitives with a retired
workflow.  Keeping them here makes the research path independent of retired
stage state while preserving the exact path checks.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath


_FORMAL = re.compile(r"^archives/[^/]+/(?:subarchives/[^/]+/)*(?:state/.+\.md|问题--问题\.md)$")
_RESERVED = {"tools", "evidence", "workspaces", "cleanup", "history", ".git",
             ".rsync-tmp", "original", "comparison", "comparisons", "formal-comparison"}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _safe_path(root: Path, name: str) -> Path:
    if not isinstance(name, str) or not name or "\\" in name:
        raise ValueError("a nonempty repository-relative POSIX path is required")
    pure = PurePosixPath(name)
    if pure.is_absolute() or ".." in pure.parts or ".git" in pure.parts or pure.as_posix() != name:
        raise ValueError("unsafe repository path: " + name)
    root = root.resolve()
    target = root.joinpath(*pure.parts)
    if not target.resolve().is_relative_to(root):
        raise ValueError("path escapes repository: " + name)
    cursor = root
    for part in pure.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise ValueError("symlink is not an admitted artifact path: " + name)
    return target


def is_formal_path(name: str) -> bool:
    return isinstance(name, str) and bool(_FORMAL.fullmatch(name)) and not (_RESERVED & set(PurePosixPath(name).parts))


def formal_paths(root: Path) -> tuple[Path, ...]:
    root = Path(root).resolve()
    archive = root / "archives"
    if not archive.exists():
        return ()
    result = []
    for path in archive.rglob("*.md"):
        name = path.relative_to(root).as_posix()
        if is_formal_path(name):
            _safe_path(root, name)
            if path.is_file():
                result.append(path)
    return tuple(sorted(result))


def _write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


__all__ = ["_safe_path", "_write_json", "digest", "formal_paths", "is_formal_path"]
