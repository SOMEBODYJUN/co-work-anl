#!/usr/bin/env python3
"""Assemble an unfinished or reviewed ledger from explicitly authored records.

Only hashes, marker line ranges, bbox intersections and reverse mappings are
derived. This program never generates reading observations, identities, visual
assessment, recovery decisions, findings, review scopes or approval records.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile

import jsonschema


MARKER = re.compile(r"^\s*<!--\s*unit:\s*([^\s<>]+)\s*-->\s*$")
CONFIG_KEYS = {
    "authors", "manifest", "artifacts", "source_units", "mapping",
    "observations", "old_units", "recoveries", "issues", "final_rounds", "output",
}
SOURCE_KEYS = {"id", "page_id", "bbox_px", "label", "status", "evidence_ids"}
TARGET_KEYS = {
    "id", "artifact_id", "source_ids", "status", "origin", "old_ids",
    "evidence_ids", "explanation",
}
OLD_KEYS = {
    "id", "artifact_id", "start_line", "end_line", "disposition",
    "explanation", "evidence_ids",
}


def load_json(path: Path):
    def unique(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"{path}: duplicate JSON key {key!r}")
            value[key] = item
        return value
    return json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=unique,
        parse_constant=lambda x: (_ for _ in ()).throw(ValueError(f"invalid JSON number {x}")),
    )


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inside(project: Path, name: str) -> Path:
    if not isinstance(name, str) or not name:
        raise ValueError("file paths must be nonempty strings")
    relative = Path(name)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"path must be relative and remain inside project: {name}")
    result = (project / relative).resolve()
    if not result.is_relative_to(project):
        raise ValueError(f"path escapes project, including through a symlink: {name}")
    return result


def fields(value: dict, allowed: set[str], required: set[str], name: str):
    if not isinstance(value, dict):
        raise ValueError(f"{name}: expected object")
    extra, missing = set(value) - allowed, required - set(value)
    if extra or missing:
        raise ValueError(f"{name}: unknown fields {sorted(extra)}; missing fields {sorted(missing)}")


def index(items: list, name: str) -> dict:
    if not isinstance(items, list):
        raise ValueError(f"{name}: expected array")
    result = {}
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"]:
            raise ValueError(f"{name}: each item needs an explicit nonempty id")
        if item["id"] in result:
            raise ValueError(f"{name}: duplicate id {item['id']}")
        result[item["id"]] = item
    return result


def schema_directory() -> Path:
    suffix = Path(".agents/skills/math-notes-evidence-audit/scripts/schema")
    for parent in Path(__file__).resolve().parents:
        if (parent / suffix / "ledger.schema.json").is_file():
            return parent / suffix
    raise ValueError("cannot locate repository ledger.schema.json from this tool's location")


def validate(value, schema: dict, name: str):
    errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(value),
                    key=lambda e: "/".join(map(str, e.absolute_path)))
    if errors:
        details = [f"{name}/{'/'.join(map(str, e.absolute_path))}: {e.message}" for e in errors[:12]]
        raise ValueError("schema validation failed:\n" + "\n".join(details))


def intersects(a: list[int], b: list[int]) -> bool:
    return max(a[0], b[0]) < min(a[2], b[2]) and max(a[1], b[1]) < min(a[3], b[3])


def marker_spans(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    found = [(n, match.group(1)) for n, line in enumerate(lines, 1)
             if (match := MARKER.fullmatch(line))]
    before = lines[:found[0][0] - 1] if found else lines
    if any(line.strip() for line in before):
        raise ValueError(f"{path.name}: nonblank text precedes the first unit marker, or no marker exists")
    result = {}
    for offset, (start, identifier) in enumerate(found):
        if identifier in result:
            raise ValueError(f"{path.name}: duplicate unit marker {identifier}")
        end = found[offset + 1][0] - 1 if offset + 1 < len(found) else len(lines)
        text = "\n".join(lines[start - 1:end])
        result[identifier] = {
            "start_line": start, "end_line": end,
            "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        }
    return result


def assemble(project: Path, config_path: Path) -> tuple[dict, Path]:
    config = load_json(config_path)
    fields(config, CONFIG_KEYS, {"authors", "artifacts", "source_units", "mapping", "observations"}, "config")
    protected = {config_path}
    manifest_path = inside(project, config.get("manifest", "manifest.json"))
    if manifest_path.parent != project:
        raise ValueError("manifest must be in the project root so all ledger paths share one base")
    protected.add(manifest_path)
    manifest = load_json(manifest_path)
    schemas = schema_directory()
    validate(manifest, load_json(schemas / "manifest.schema.json"), "manifest")
    pages = index(manifest["pages"], "manifest pages")
    protected.add(inside(project, manifest["source_pdf"]["path"]))
    for page in pages.values():
        protected.add(inside(project, page["image"]["path"]))
        for region in page["regions"]:
            protected.add(inside(project, region["image"]["path"]))

    def read_input(name: str, default=None):
        if name not in config:
            return copy.deepcopy(default)
        path = inside(project, config[name])
        protected.add(path)
        return load_json(path)

    artifacts = copy.deepcopy(config["artifacts"])
    artifacts_by_id = index(artifacts, "artifacts")
    marker_index = {}
    for artifact in artifacts:
        fields(artifact, {"id", "path", "kind", "format", "source_crop"},
               {"id", "path", "kind", "format"}, f"artifact {artifact['id']}")
        path = inside(project, artifact["path"])
        protected.add(path)
        artifact["sha256"] = digest(path)
        if artifact["kind"] in {"transcription", "study"}:
            if artifact["format"] != "text":
                raise ValueError("transcription and study artifacts must be UTF-8 text")
            for identifier, span in marker_spans(path).items():
                if identifier in marker_index:
                    raise ValueError(f"unit marker appears in more than one artifact: {identifier}")
                marker_index[identifier] = {"artifact_id": artifact["id"], **span}

    source_units = read_input("source_units")
    if isinstance(source_units, dict):
        fields(source_units, {"source_units"}, {"source_units"}, "source-units wrapper")
        source_units = source_units["source_units"]
    sources = index(source_units, "source_units")
    for source in source_units:
        fields(source, SOURCE_KEYS, SOURCE_KEYS, f"source {source['id']}")
        if source["page_id"] not in pages:
            raise ValueError(f"{source['id']}: unknown page {source['page_id']}")
        page, box = pages[source["page_id"]], source["bbox_px"]
        if (not isinstance(box, list) or len(box) != 4 or any(type(x) is not int for x in box)
                or not (0 <= box[0] < box[2] <= page["width_px"] and 0 <= box[1] < box[3] <= page["height_px"])):
            raise ValueError(f"{source['id']}: bbox must have four in-page integer pixel coordinates")
        source["region_ids"] = [r["id"] for r in page["regions"] if intersects(box, r["bbox_px"])]
        source["transcription_target_ids"] = []
        source["study_target_ids"] = []

    mapping = read_input("mapping")
    fields(mapping, {"targets"}, {"targets"}, "mapping")
    targets = mapping["targets"]
    target_index = index(targets, "mapping targets")
    if set(marker_index) != set(target_index):
        raise ValueError(f"mapping/markers differ: no mapping={sorted(set(marker_index) - set(target_index))}; "
                         f"no marker={sorted(set(target_index) - set(marker_index))}")
    if set(sources) & set(target_index):
        raise ValueError("source and target IDs need distinct namespaces")

    old_units = read_input("old_units", [])
    old_index = index(old_units, "old_units")
    if set(old_index) & (set(sources) | set(target_index)):
        raise ValueError("old, source and target IDs need distinct namespaces")
    for old in old_units:
        fields(old, OLD_KEYS, OLD_KEYS, f"old unit {old['id']}")
        artifact = artifacts_by_id.get(old["artifact_id"])
        if artifact is None or artifact["kind"] != "old" or artifact["format"] != "text":
            raise ValueError(f"{old['id']}: needs an explicit old text artifact")
        lines = inside(project, artifact["path"]).read_text(encoding="utf-8").splitlines()
        first, last = old["start_line"], old["end_line"]
        if type(first) is not int or type(last) is not int or not 1 <= first <= last <= len(lines):
            raise ValueError(f"{old['id']}: invalid original text line range")
        old["text_sha256"] = hashlib.sha256("\n".join(lines[first - 1:last]).encode("utf-8")).hexdigest()
        old["target_ids"] = []

    for target in targets:
        fields(target, TARGET_KEYS, TARGET_KEYS, f"target {target['id']}")
        span = marker_index[target["id"]]
        if target["artifact_id"] != span["artifact_id"]:
            raise ValueError(f"{target['id']}: marker is in a different artifact")
        target.update({k: v for k, v in span.items() if k != "artifact_id"})
        kind = artifacts_by_id[target["artifact_id"]]["kind"]
        field = "transcription_target_ids" if kind == "transcription" else "study_target_ids"
        for identifier in target["source_ids"]:
            if identifier not in sources:
                raise ValueError(f"{target['id']}: unknown source {identifier}")
            sources[identifier][field].append(target["id"])
        for identifier in target["old_ids"]:
            if identifier not in old_index:
                raise ValueError(f"{target['id']}: unknown old unit {identifier}")
            if kind != "study":
                raise ValueError(f"{target['id']}: old units require actual study destinations")
            old_index[identifier]["target_ids"].append(target["id"])

    observations = {"page_checks": [], "region_checks": []}
    observation_paths = config["observations"]
    if isinstance(observation_paths, str):
        observation_paths = [observation_paths]
    if not isinstance(observation_paths, list):
        raise ValueError("observations must be a relative JSON filename or list of filenames")
    for filename in observation_paths:
        path = inside(project, filename)
        protected.add(path)
        value = load_json(path)
        fields(value, set(observations), set(observations), f"observations {filename}")
        for key in observations:
            if not isinstance(value[key], list):
                raise ValueError(f"{filename}/{key}: expected array")
            observations[key].extend(value[key])

    ledger = {
        "schema_version": "1.0", "manifest_sha256": digest(manifest_path),
        "authors": config["authors"], "artifacts": artifacts,
        "source_units": source_units, "target_units": targets, "old_units": old_units,
        **observations, "recoveries": read_input("recoveries", []),
        "issues": read_input("issues", []), "final_rounds": read_input("final_rounds", []),
    }
    for key in ("source_units", "target_units", "old_units", "page_checks", "region_checks", "recoveries", "issues", "final_rounds"):
        index(ledger[key], key)
    validate(ledger, load_json(schemas / "ledger.schema.json"), "ledger")
    output = inside(project, config.get("output", "ledger.json"))
    if output.parent != project:
        raise ValueError("output ledger must be in the project root")
    for record in ledger["final_rounds"]:
        for field in ("blind_reading", "report"):
            protected.add(inside(project, record[field]["path"]))
    if output in protected:
        raise ValueError("refusing to overwrite an input, artifact, image or review report")
    if output.exists():
        previous = load_json(output).get("final_rounds", [])
        if previous and ledger["final_rounds"][:len(previous)] != previous:
            raise ValueError("refusing to drop or rewrite existing final-round history; supply it unchanged via final_rounds")
    return ledger, output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path, help="prepared project directory")
    parser.add_argument("--config", required=True, type=Path, help="config inside project; relative paths are project-relative")
    args = parser.parse_args()
    project = args.project.resolve()
    config_path = args.config.resolve() if args.config.is_absolute() else inside(project, str(args.config))
    if not config_path.is_relative_to(project):
        raise ValueError("config must remain inside project")
    ledger, output = assemble(project, config_path)
    payload = json.dumps(ledger, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=project,
                                         prefix=".ledger-build-", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(payload)
        temporary.replace(output)
    finally:
        if temporary and temporary.exists():
            temporary.unlink()
    print(json.dumps({
        "ledger": str(output), "ledger_sha256": digest(output), "schema_valid": True,
        "source_units": len(ledger["source_units"]), "target_units": len(ledger["target_units"]),
        "page_checks": len(ledger["page_checks"]), "region_checks": len(ledger["region_checks"]),
        "final_rounds": len(ledger["final_rounds"]), "audit_run": False,
        "note": "Schema assembly only; use the project audit. No visual reading or review completion is inferred.",
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
