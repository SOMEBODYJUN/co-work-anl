#!/usr/bin/env python3
"""Summarize remaining notes and unresolved audit records.

This is a read-only preflight for a Pro recovery session.  Counts of
unresolved records are deliberately kept separate from counts of distinct
mathematical questions because one question can fan out into several ledger
records.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def load(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None


def report_score(path: Path) -> tuple[int, int, str]:
    name = path.name.lower()
    score = 0
    if name == "audit-report.json":
        score += 100
    if "final-03" in name:
        score += 90
    elif "current" in name:
        score += 80
    elif "final" in name:
        score += 60
    elif "audit" in name or "report" in name:
        score += 20
    try:
        mtime = path.stat().st_mtime_ns
    except OSError:
        mtime = 0
    return score, mtime, path.as_posix()


def latest_report(repo: Path, note_id: str) -> tuple[Path | None, dict[str, Any] | None]:
    candidates: list[tuple[tuple[int, int, str], Path, dict[str, Any]]] = []
    for run in (repo / "work").glob("notes-*"):
        note = run / "notes" / note_id
        if not note.is_dir():
            continue
        for path in note.rglob("*.json"):
            value = load(path)
            if isinstance(value, dict) and "content_resolved" in value and "unresolved_count" in value:
                candidates.append((report_score(path), path, value))
    if not candidates:
        return None, None
    _, path, value = max(candidates, key=lambda item: item[0])
    return path, value


def inventory(repo: Path) -> dict[str, Any]:
    tasks = []
    source_hashes: dict[str, list[str]] = {}
    for path in sorted((repo / "tasks").glob("*.json")):
        value = load(path)
        if not isinstance(value, dict) or not value.get("note_id"):
            continue
        note_id = value["note_id"]
        report_path, report = latest_report(repo, note_id)
        unresolved = report.get("unresolved_count", 0) if report else None
        item = {
            "note_id": note_id,
            "status": value.get("status"),
            "batch": value.get("batch"),
            "order": value.get("order"),
            "owner": value.get("owner"),
            "has_existing_work": bool(report_path),
            "audit_report": report_path.relative_to(repo).as_posix() if report_path else None,
            "audit_pass": report.get("audit_pass") if report else None,
            "content_resolved": report.get("content_resolved") if report else None,
            "unresolved_records": unresolved,
            "recovery_priority": bool(report_path) and unresolved not in (None, 0),
        }
        tasks.append(item)
        for source in value.get("source_pdfs", []):
            digest = source.get("sha256")
            if digest:
                source_hashes.setdefault(digest, []).append(note_id)
    remaining = [item for item in tasks if item["status"] != "done"]
    input_hashes: dict[str, list[str]] = {}
    for pdf in sorted((repo / "input" / "pdf").glob("*.pdf")):
        try:
            digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
        except OSError:
            continue
        input_hashes.setdefault(digest, []).append(pdf.name)
    return {
        "notes_total": len(tasks),
        "notes_remaining": len(remaining),
        "notes_done": sum(item["status"] == "done" for item in tasks),
        "unique_source_pdfs": len(input_hashes),
        "uploaded_source_entries": sum(len(v) for v in input_hashes.values()),
        "duplicate_source_groups": [names for names in input_hashes.values() if len(names) > 1],
        "unresolved_audit_records": sum(item["unresolved_records"] or 0 for item in remaining),
        "notes_needing_recovery": [item["note_id"] for item in remaining if item["recovery_priority"]],
        "notes_not_started": [item["note_id"] for item in remaining
                               if item["status"] == "pending" and not item["has_existing_work"]],
        "tasks": sorted(tasks, key=lambda item: (item["order"] or 999, item["note_id"])),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(inventory(args.repo.resolve()), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
