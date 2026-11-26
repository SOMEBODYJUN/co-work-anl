#!/usr/bin/env python3
"""Plan and validate the single-Boss, three-subagent doubt campaigns."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

from recovery_inventory import inventory


CAMPAIGNS = {
    "ra12-then-commutative-algebra": {
        "label": "RA12 收尾后交换代数全量处理",
        "notes": ["RA12", "CA07", "CA09", "CA10", "CA11", "CA12"],
        "next_campaign": None,
    },
    "real-analysis": {
        "label": "实分析疑点清扫",
        "notes": ["RA06", "RA07", "RA09", "RA10", "RA11", "RA12"],
        "next_campaign": "commutative-algebra",
    },
    "commutative-algebra": {
        "label": "交换代数疑点清扫",
        "notes": ["CA07", "CA09", "CA10", "CA11", "CA12"],
        "next_campaign": None,
    },
}


def load_tasks(repo: Path) -> dict[str, dict[str, Any]]:
    result = {}
    for path in (repo / "tasks").glob("*.json"):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            continue
        if value.get("note_id"):
            result[value["note_id"]] = value
    return result


def snapshot(repo: Path, subject: str) -> dict[str, Any]:
    if subject not in CAMPAIGNS:
        raise ValueError("unknown campaign: " + subject)
    all_notes = {item["note_id"]: item for item in inventory(repo)["tasks"]}
    entries = []
    for note_id in CAMPAIGNS[subject]["notes"]:
        task = all_notes.get(note_id)
        if not task:
            raise ValueError("campaign note is not registered: " + note_id)
        entries.append(task)
    return {
        "subject": subject,
        "label": CAMPAIGNS[subject]["label"],
        "notes": entries,
        "unresolved_audit_records": sum(item["unresolved_records"] or 0 for item in entries),
        "notes_done": sum(item["status"] == "done" for item in entries),
        "notes_remaining": sum(item["status"] != "done" for item in entries),
    }


def init_plan(repo: Path, subject: str, run: str, out: Path) -> Path:
    current = snapshot(repo, subject)
    plan = {
        "schema_version": "1.0",
        "mode": "doubt_recovery_campaign",
        "manual_intervention": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "subject": subject,
        "label": CAMPAIGNS[subject]["label"],
        "boss_run": run,
        "notes": CAMPAIGNS[subject]["notes"],
        "subagents_per_note": 3,
        "same_note_parallel": True,
        "rotation": "replace all three subagents only after the current note is fully resolved",
        "sequence": [
            "Claim exactly one campaign note at a time under this Boss/RUN.",
            "Assign three independent subagents to that same note; they inspect the same frozen snapshot and keep separate observations.",
            "Merge their candidate readings and mathematical checks without averaging away disagreements.",
            "Resolve every source, target, recovery, issue, page and region record before sealing the note.",
            "After content changes, invalidate the old final-round chain and run a fresh second pass plus three new final rounds.",
            "Only when the note audit reports audit_pass=true, content_resolved=true and unresolved_count=0 may the trio be replaced for the next note.",
        ],
        "gate": {
            "require_audit_pass": True,
            "require_content_resolved": True,
            "require_unresolved_count_zero": True,
            "require_three_final_rounds_after_last_change": True,
            "allow_manual_handoff": False,
        },
        "initial_snapshot": current,
        "execution_log": [],
        "next_campaign": CAMPAIGNS[subject]["next_campaign"],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def validate(repo: Path, subject: str, plan_path: Path | None = None) -> dict[str, Any]:
    current = snapshot(repo, subject)
    errors: list[str] = []
    if plan_path:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        if plan.get("subject") != subject:
            errors.append("campaign plan subject does not match")
        if plan.get("subagents_per_note") != 3 or plan.get("same_note_parallel") is not True:
            errors.append("plan does not require three subagents on one note")
        if plan.get("manual_intervention") is not False:
            errors.append("plan permits manual intervention")
        logs = {record.get("note_id"): record for record in plan.get("execution_log", [])}
        ordered_logs = plan.get("execution_log", [])
        if [record.get("note_id") for record in ordered_logs] != CAMPAIGNS[subject]["notes"]:
            errors.append("execution log must contain each campaign note exactly once in the required order")
        all_agents = [agent for record in ordered_logs for agent in record.get('subagents', [])]
        if len(all_agents) != len(set(all_agents)):
            errors.append("subagents must be replaced between notes; an identity was reused")
        tasks = load_tasks(repo)
        for note_id in CAMPAIGNS[subject]["notes"]:
            record = logs.get(note_id)
            if not record:
                errors.append("execution log is missing note: " + note_id)
                continue
            if len(record.get("subagents", [])) != 3 or len(set(record.get("subagents", []))) != 3:
                errors.append("execution log has a note without three distinct subagents: " + note_id)
            if record.get("completed") is not True:
                errors.append("execution log does not mark the note complete: " + note_id)
            if record.get("unresolved_after") != 0:
                errors.append("execution log still has unresolved records: " + note_id)
            if subject == 'ra12-then-commutative-algebra':
                task = tasks[note_id]
                completion = task.get('completion', {})
                if task.get('run') != plan.get('boss_run'):
                    errors.append('task is not completed under the campaign RUN: ' + note_id)
                if record.get('model') != 'gpt-6.2-sol' or record.get('reasoning_effort') != 'max':
                    errors.append('execution log does not record the requested agent configuration: ' + note_id)
                if not record.get('snapshot_sha256') or record.get('snapshot_sha256') != completion.get('snapshot_sha256'):
                    errors.append('final snapshot differs from the submitted task: ' + note_id)
                for relative, expected_hash in completion.get('files', {}).items():
                    path = repo / relative
                    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected_hash:
                        errors.append('submitted content/report hash changed: ' + relative)
                if not completion.get('files'):
                    errors.append('task has no verified submission files: ' + note_id)
    complete = (
        current["notes_remaining"] == 0
        and current["unresolved_audit_records"] == 0
        and all(item["audit_pass"] is True and item["content_resolved"] is True
                and item["unresolved_records"] == 0 for item in current["notes"])
        and not errors
    )
    return {"subject": subject, "complete": complete, "errors": errors, "current": current}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("inventory", "validate"):
        p = sub.add_parser(command)
        p.add_argument("--subject", choices=sorted(CAMPAIGNS), required=True)
        if command == "validate":
            p.add_argument("--plan", type=Path)
    p = sub.add_parser("init")
    p.add_argument("--subject", choices=sorted(CAMPAIGNS), required=True)
    p.add_argument("--run", required=True)
    p.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    if args.command == "inventory":
        print(json.dumps(snapshot(repo, args.subject), ensure_ascii=False, indent=2))
    elif args.command == "validate":
        print(json.dumps(validate(repo, args.subject, args.plan), ensure_ascii=False, indent=2))
    else:
        print(init_plan(repo, args.subject, args.run, args.out))


if __name__ == "__main__":
    main()
