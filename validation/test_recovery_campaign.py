"""Check the single-note, three-subagent campaign guard."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from recovery_campaign import init_plan, snapshot, validate


def main() -> None:
    current = snapshot(ROOT, "real-analysis")
    assert [item["note_id"] for item in current["notes"]] == ["RA06", "RA07", "RA09", "RA10", "RA11", "RA12"]
    with tempfile.TemporaryDirectory(prefix="recovery-campaign-test-") as temp:
        plan_path = Path(temp) / "campaign.json"
        init_plan(ROOT, "real-analysis", "synthetic-run", plan_path)
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        assert plan["subagents_per_note"] == 3
        assert plan["same_note_parallel"] is True
        assert plan["manual_intervention"] is False
        result = validate(ROOT, "real-analysis", plan_path)
        assert result["complete"] is False
        assert any("execution log" in error for error in result["errors"])
    print(json.dumps({"campaign_notes": 6, "three_subagents_same_note": True}))


if __name__ == "__main__":
    main()
