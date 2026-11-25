"""Synthetic check for the no-human autonomous recovery queue."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile

import fitz

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.autonomous_recovery import build


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="autonomous-recovery-test-") as name:
        project = Path(name)
        pdf = project / "source.pdf"
        document = fitz.open()
        page = document.new_page(width=240, height=160)
        page.insert_text((20, 40), "x + 1 = 2")
        document.save(pdf)
        document.close()
        manifest = {
            "source_pdf": {"path": "source.pdf", "page_count": 1},
            "render": {"dpi": 220},
            "pages": [{"id": "p0001", "number": 1,
                       "image": {"path": "pages/p0001.png", "bbox_px": [0, 0, 734, 489]},
                       "regions": [{"id": "p0001-r1c1", "row": 1, "column": 1,
                                    "bbox_px": [0, 0, 734, 489],
                                    "image": {"path": "regions/p0001-r1c1.png"}}]}],
        }
        ledger = {"source_units": [{"id": "S1", "page_id": "p0001",
                                     "bbox_px": [40, 20, 360, 70],
                                     "evidence_ids": ["image:p0001"]}]}
        report = {"audit_pass": True, "content_resolved": False,
                  "unresolved": [{"kind": "source_unit", "id": "S1",
                                  "reason": "source interpretation remains unresolved"}]}
        (project / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        (project / "ledger.json").write_text(json.dumps(ledger), encoding="utf-8")
        report_path = project / "report.json"
        report_path.write_text(json.dumps(report), encoding="utf-8")
        plan_path = build(project, report_path, project / "autonomous-recovery", dpi=600)
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        assert plan["mode"] == "autonomous_model_recovery"
        assert plan["manual_intervention"] is False
        assert plan["status"] == "ready"
        assert plan["records"][0]["crop_paths"]
        assert (project / plan["records"][0]["crop_paths"][0]).is_file()
    print(json.dumps({"autonomous_recovery_queue": True, "manual_intervention": False}))


if __name__ == "__main__":
    main()
