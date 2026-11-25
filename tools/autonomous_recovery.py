#!/usr/bin/env python3
"""Prepare an autonomous visual-recovery queue from an audit report.

The audit remains deliberately conservative: this tool never invents a
transcription or marks an item resolved.  It does the mechanical work that
used to be handed back as a human task: it indexes every unresolved record,
maps it back to source units/pages, and renders bounded high-resolution crops
for the model's next reading pass.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from typing import Any

import fitz


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def safe(root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"path escapes project: {value}")
    result = (root / path).resolve()
    if not result.is_relative_to(root.resolve()):
        raise ValueError(f"path escapes project: {value}")
    return result


def slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-") or "item"


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def index_records(ledger: dict[str, Any]) -> dict[str, dict[str, dict[str, Any]]]:
    names = {
        "source_unit": "source_units",
        "target_unit": "target_units",
        "old_unit": "old_units",
        "recovery": "recoveries",
        "issue": "issues",
        "page_check": "page_checks",
        "region_check": "region_checks",
    }
    return {
        kind: {str(item["id"]): item for item in ledger.get(field, [])}
        for kind, field in names.items()
    }


def image_index(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for page in manifest.get("pages", []):
        result[f"image:{page['id']}"] = {
            "page_id": page["id"], "bbox_px": page["image"]["bbox_px"],
            "path": page["image"]["path"], "kind": "page",
        }
        for region in page.get("regions", []):
            result[f"image:{region['id']}"] = {
                "page_id": page["id"], "region_id": region["id"],
                "bbox_px": region["bbox_px"], "path": region["image"]["path"],
                "kind": "region",
            }
    return result


def related_source_ids(kind: str, record: dict[str, Any], indexes: dict[str, dict[str, dict[str, Any]]]) -> list[str]:
    if kind == "source_unit":
        return [record["id"]]
    if kind == "target_unit":
        return list(record.get("source_ids", []))
    if kind == "old_unit":
        return list(record.get("source_ids", []))
    if kind == "issue":
        return [identifier for identifier in record.get("related_ids", []) if identifier in indexes["source_unit"]]
    if kind == "recovery":
        ids = list(record.get("source_ids", [])) + list(record.get("related_ids", []))
        return [identifier for identifier in ids if identifier in indexes["source_unit"]]
    if kind == "page_check":
        return []
    if kind == "region_check":
        return []
    return []


def make_entries(report: dict[str, Any], manifest: dict[str, Any], ledger: dict[str, Any]) -> list[dict[str, Any]]:
    indexes = index_records(ledger)
    images = image_index(manifest)
    entries: list[dict[str, Any]] = []
    for item in report.get("unresolved", []):
        kind, identifier = str(item.get("kind", "unknown")), str(item.get("id", "unknown"))
        record = indexes.get(kind, {}).get(identifier, {})
        evidence = list(record.get("evidence_ids", []))
        source_ids = related_source_ids(kind, {**record, "id": identifier}, indexes)
        page_ids: list[str] = []
        boxes: list[list[int]] = []
        for source_id in source_ids:
            source = indexes["source_unit"].get(source_id, {})
            if source.get("page_id"):
                page_ids.append(source["page_id"])
            if source.get("bbox_px"):
                boxes.append(source["bbox_px"])
        for evidence_id in evidence:
            image = images.get(evidence_id)
            if image:
                page_ids.append(image["page_id"])
                if image["kind"] == "region":
                    boxes.append(image["bbox_px"])
        if kind == "page_check" and record.get("page_id"):
            page_ids.append(record["page_id"])
        if kind == "region_check" and record.get("region_id"):
            image = images.get("image:" + record["region_id"])
            if image:
                page_ids.append(image["page_id"])
                boxes.append(image["bbox_px"])
        entries.append({
            "kind": kind,
            "id": identifier,
            "reason": item.get("reason", "unresolved record"),
            "source_ids": sorted(set(source_ids)),
            "page_ids": sorted(set(page_ids)),
            "bbox_px": boxes,
            "evidence_ids": evidence,
            "candidates_required": 2 if kind in {"source_unit", "target_unit", "old_unit", "recovery", "issue"} else 0,
            "checks": {
                "forward_math": kind in {"source_unit", "target_unit", "old_unit", "recovery", "issue"},
                "backward_math": kind in {"source_unit", "target_unit", "old_unit", "recovery", "issue"},
                "source_recheck": True,
            },
            "crop_paths": [],
        })
    return entries


def render_crops(project: Path, manifest: dict[str, Any], entries: list[dict[str, Any]], out: Path, dpi: int) -> None:
    pdf_path = safe(project, manifest["source_pdf"]["path"])
    if not pdf_path.is_file():
        raise ValueError(f"missing source PDF: {manifest['source_pdf']['path']}")
    base_dpi = float(manifest.get("render", {}).get("dpi", 220))
    page_map = {page["id"]: page for page in manifest.get("pages", [])}
    seen: dict[tuple[str, tuple[int, int, int, int]], str] = {}
    crop_dir = out / "crops"
    crop_dir.mkdir(parents=True, exist_ok=True)
    with fitz.open(pdf_path) as document:
        for entry in entries:
            candidates: list[tuple[str, list[int]]] = []
            for page_id, page in page_map.items():
                if page_id not in entry["page_ids"]:
                    continue
                page_box = page["image"]["bbox_px"]
                candidates.extend((page_id, box) for box in entry["bbox_px"] if box)
                if not entry["bbox_px"]:
                    # Page/region checks without a source unit are covered by
                    # the six grid regions rather than an enormous full page.
                    candidates.extend((page_id, region["bbox_px"])
                                       for region in page.get("regions", []))
            for page_id, raw_box in candidates:
                page = page_map[page_id]
                full = page["image"]["bbox_px"]
                margin = max(48, int(round(base_dpi * 0.35)))
                box = [max(full[0], raw_box[0] - margin), max(full[1], raw_box[1] - margin),
                       min(full[2], raw_box[2] + margin), min(full[3], raw_box[3] + margin)]
                key = (page_id, tuple(box))
                if key not in seen:
                    pdf_page = document[page["number"] - 1]
                    clip = fitz.Rect(*(coord * 72.0 / base_dpi for coord in box))
                    pix = pdf_page.get_pixmap(dpi=dpi, clip=clip, colorspace=fitz.csRGB, alpha=False)
                    filename = f"{slug(page_id)}-{digest(page_id + ':' + ','.join(map(str, box)))}.png"
                    path = crop_dir / filename
                    pix.save(path)
                    seen[key] = (path.relative_to(project).as_posix()
                                 if path.is_relative_to(project) else str(path))
                entry["crop_paths"].append(seen[key])
            entry["crop_paths"] = sorted(set(entry["crop_paths"]))


def build(project: Path, report_path: Path, out: Path, dpi: int = 800, ledger_path: Path | None = None) -> Path:
    if not 600 <= dpi <= 1200:
        raise ValueError("recovery dpi must be between 600 and 1200")
    project = project.resolve()
    report_path = report_path.resolve()
    manifest_path = project / "manifest.json"
    ledger_path = (ledger_path or project / "ledger.json").resolve()
    manifest, ledger, report = load(manifest_path), load(ledger_path), load(report_path)
    entries = make_entries(report, manifest, ledger)
    out = out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    render_crops(project, manifest, entries, out, dpi)
    missing = [entry["id"] for entry in entries if not entry["crop_paths"]]
    plan = {
        "schema_version": "1.0",
        "mode": "autonomous_model_recovery",
        "manual_intervention": False,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_report": report_path.relative_to(project).as_posix() if report_path.is_relative_to(project) else str(report_path),
        "source_pdf": manifest["source_pdf"],
        "audit_pass": report.get("audit_pass"),
        "content_resolved": report.get("content_resolved"),
        "unresolved_count": len(entries),
        "status": "tool_blocked" if missing else "ready",
        "next_actions": [
            "Read every crop at native resolution and compare against the full page.",
            "Write at least two visual candidates for each glyph or mathematical ambiguity.",
            "Run independent forward and backward mathematical checks, then return to the source image.",
            "Update the source/target units, recovery record, issue resolution, and both drafts.",
            "Invalidate the old final-round chain after any content change and rerun the second pass plus three final rounds.",
            "Keep the task claimed; never convert this queue into a manual block.",
        ],
        "records": entries,
    }
    path = out / "recovery-plan.json"
    path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--dpi", type=int, default=800)
    args = parser.parse_args()
    try:
        project = args.project.resolve()
        out = args.out or project / "autonomous-recovery"
        print(build(project, args.report, out, args.dpi, args.ledger))
    except (OSError, RuntimeError, ValueError, KeyError, json.JSONDecodeError) as error:
        parser.exit(1, f"autonomous_recovery: {error}\n")


if __name__ == "__main__":
    main()
