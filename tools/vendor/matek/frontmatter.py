"""Flat-frontmatter codec extracted from MATEK; see LICENSE and UPSTREAM.md."""
from __future__ import annotations
import json, re
from collections.abc import Mapping
_KEY = re.compile(r"\A[A-Za-z_][A-Za-z0-9_-]*\Z")

class GraphMarkdownError(ValueError):
    """Raised when a managed graph note cannot be parsed safely."""


def _decode_scalar(raw: str) -> str | int | bool | None:
    value = raw.strip()
    if not value:
        return ""
    try:
        decoded = json.loads(value)
    except json.JSONDecodeError:
        if value in {"null", "~"}:
            return None
        if value.casefold() == "true":
            return True
        if value.casefold() == "false":
            return False
        if value.startswith(("{", "[", "&", "*", "!", ">", "|")):
            raise GraphMarkdownError(
                "frontmatter must remain flat; nested, anchored, tagged, or block values "
                "are not supported"
            ) from None
        return value
    if isinstance(decoded, (str, int, bool)) or decoded is None:
        return decoded
    raise GraphMarkdownError("frontmatter scalar must not contain a nested array or object")


def parse_flat_frontmatter(text: str) -> tuple[dict[str, object], str]:
    """Parse flat frontmatter and return it with the Markdown body."""

    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.startswith("---\n"):
        raise GraphMarkdownError("managed note must begin with YAML frontmatter")
    closing = normalized.find("\n---\n", 4)
    if closing < 0:
        raise GraphMarkdownError("managed note has no closing frontmatter delimiter")
    raw_frontmatter = normalized[4:closing]
    body = normalized[closing + 5 :]
    result: dict[str, object] = {}
    lines = raw_frontmatter.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        index += 1
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            raise GraphMarkdownError(f"unexpected indented frontmatter line: {line!r}")
        key, separator, raw_value = line.partition(":")
        key = key.strip()
        if not separator or not _KEY.fullmatch(key):
            raise GraphMarkdownError(f"invalid flat frontmatter property: {line!r}")
        if key in result:
            raise GraphMarkdownError(f"duplicate frontmatter property: {key}")
        if raw_value.strip():
            result[key] = _decode_scalar(raw_value)
            continue
        items: list[str] = []
        while index < len(lines) and lines[index].startswith("  - "):
            item = _decode_scalar(lines[index][4:])
            if not isinstance(item, str):
                raise GraphMarkdownError(f"frontmatter list {key!r} must contain only strings")
            items.append(item)
            index += 1
        if index < len(lines) and lines[index].startswith((" ", "\t")):
            raise GraphMarkdownError(f"frontmatter property {key!r} uses unsupported nested YAML")
        result[key] = items
    return result, body


def _yaml_scalar(value: str | int | bool | None) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    return json.dumps(value, ensure_ascii=False)


def format_flat_frontmatter(properties: Mapping[str, object]) -> str:
    """Render deterministic flat YAML accepted by Obsidian Properties."""

    lines = ["---"]
    for key, value in properties.items():
        if not _KEY.fullmatch(key):
            raise GraphMarkdownError(f"cannot render invalid frontmatter key: {key!r}")
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                if not isinstance(item, str):
                    raise GraphMarkdownError(f"frontmatter list {key!r} is not a string list")
                lines.append(f"  - {_yaml_scalar(item)}")
            continue
        if not (isinstance(value, (str, int, bool)) or value is None):
            raise GraphMarkdownError(f"frontmatter property {key!r} is not flat")
        lines.append(f"{key}: {_yaml_scalar(value)}")
    lines.append("---")
    return "\n".join(lines) + "\n"
