#!/usr/bin/env python3
"""Offline synthetic fixtures and adversarial regression tests; no OCR or API."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import fitz
from PIL import Image

from audit import (Auditor, content_snapshot, expected_scope, intersects, load_json,
                   round_hash, sha256_file, text_hash)
from prepare_pdf import prepare, region_boxes


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def synthetic_round_files(project: Path, number: int) -> dict:
    result = {}
    for phase in ["blind_reading", "report"]:
        relative = f"audit-evidence/round-{number}-{phase}.txt"
        path = project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"SYNTHETIC ONLY: round {number}, phase {phase}. Six arithmetic units and one blank page.\n")
        result[phase] = {"path": relative, "sha256": sha256_file(path)}
    return result


def reseal(manifest_path: Path, ledger_path: Path, ledger: dict, update_scope: bool = True) -> None:
    """Synthetic records only: this is not a review operation."""
    manifest = load_json(manifest_path)
    ledger["manifest_sha256"] = sha256_file(manifest_path)
    snapshot = content_snapshot(manifest_path, ledger_path, manifest, ledger)
    previous = None
    images = [f"image:{page['id']}" for page in manifest["pages"]]
    images += [f"image:{region['id']}" for page in manifest["pages"] for region in page["regions"]]
    for record in ledger["final_rounds"]:
        record["snapshot_sha256"] = snapshot
        record["previous_round_sha256"] = previous
        if update_scope:
            record["scope"] = expected_scope(manifest, ledger)
            record["evidence_ids"] = images
            record["page_notes"] = [{"page_id": page["id"], "observation": "Synthetic fixture whole-page observation."} for page in manifest["pages"]]
        record["record_sha256"] = round_hash(record)
        previous = record["record_sha256"]
    write_json(ledger_path, ledger)


def make_fixture(root: Path) -> tuple[Path, Path]:
    """Generate a 2-page PDF, with six formulas and a physically blank second page."""
    root.mkdir(parents=True, exist_ok=True)
    original = root / "synthetic-input.pdf"
    document = fitz.open()
    page = document.new_page(width=120, height=90)
    for row in range(3):
        for column in range(2):
            page.insert_text((column * 60 + 8, row * 30 + 16), "2+3=5", fontsize=6)
    document.new_page(width=120, height=90)
    document.save(original)
    document.close()
    manifest_path = prepare(original, root / "project", dpi=72)
    project = manifest_path.parent
    manifest = load_json(manifest_path)
    for name, lines in [("transcription.md", ["2+3=5"] * 6),
                        ("study.md", ["From 2+3=5, infer 5-3=2."] * 6),
                        ("old.md", ["2+3=5"]),
                        ("calculation.txt", ["Forward: 2+3=5. Reverse: 5-3=2. Synthetic arithmetic evidence."])]:
        (project / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    artifacts = [{"id": identifier, "path": name, "sha256": sha256_file(project / name),
                  "kind": kind, "format": "text"}
                 for identifier, name, kind in [("transcription", "transcription.md", "transcription"),
                                                ("study", "study.md", "study"),
                                                ("old", "old.md", "old"),
                                                ("calculation", "calculation.txt", "evidence")]]
    ledger = {"schema_version": "1.0", "manifest_sha256": sha256_file(manifest_path),
              "authors": ["synthetic-author"], "artifacts": artifacts,
              "source_units": [], "target_units": [], "old_units": [],
              "page_checks": [], "region_checks": [], "recoveries": [], "issues": [], "final_rounds": []}
    for number in range(1, 7):
        row, col = divmod(number - 1, 2)
        box = [col * 60 + 7, row * 30 + 8, col * 60 + 49, row * 30 + 19]
        ids = [region["id"] for region in manifest["pages"][0]["regions"] if intersects(box, region["bbox_px"])]
        sid, tid, wid = f"s{number:02d}", f"t{number:02d}", f"w{number:02d}"
        ledger["source_units"].append({"id": sid, "page_id": "p0001", "region_ids": ids,
            "bbox_px": box, "label": "Synthetic 2+3=5 formula", "status": "resolved",
            "transcription_target_ids": [tid], "study_target_ids": [wid],
            "evidence_ids": ["image:p0001"] + [f"image:{rid}" for rid in ids]})
        for uid, aid, filename in [(tid, "transcription", "transcription.md"), (wid, "study", "study.md")]:
            ledger["target_units"].append({"id": uid, "artifact_id": aid, "start_line": number,
                "end_line": number, "text_sha256": text_hash(project / filename, number, number),
                "source_ids": [sid], "status": "resolved", "origin": "source", "old_ids": [],
                "evidence_ids": ["image:p0001"], "explanation": ""})
    ledger["old_units"].append({"id": "o01", "artifact_id": "old", "start_line": 1,
        "end_line": 1, "text_sha256": text_hash(project / "old.md", 1, 1),
        "disposition": "migrated", "target_ids": ["w01"], "explanation": "Formula retained with reverse calculation.",
        "evidence_ids": ["artifact:old", "artifact:study"]})
    next(unit for unit in ledger["target_units"] if unit["id"] == "w01")["old_ids"] = ["o01"]
    next(unit for unit in ledger["target_units"] if unit["id"] == "w01")["evidence_ids"].append("artifact:old")
    for page in manifest["pages"]:
        source_ids = [unit["id"] for unit in ledger["source_units"] if unit["page_id"] == page["id"]]
        for pass_number in (1, 2):
            ledger["page_checks"].append({"id": f"pagecheck-{page['id']}-{pass_number}",
                "page_id": page["id"], "pass": pass_number, "reviewer_id": f"synthetic-page-reviewer-{pass_number}",
                "session_id": f"synthetic-page-session-{pass_number}", "assessment": "content" if source_ids else "blank",
                "source_unit_ids": source_ids, "cross_region_unit_ids": [],
                "evidence_ids": [f"image:{page['id']}"],
                "observation": "Synthetic whole page inspected; no real-world claim is made.",
                "layout_observation": "Synthetic two columns and three rows; blank page remains separately reviewed."})
        for region in page["regions"]:
            unit_ids = [unit["id"] for unit in ledger["source_units"] if region["id"] in unit["region_ids"]]
            for pass_number in (1, 2):
                ledger["region_checks"].append({"id": f"check-{region['id']}-{pass_number}",
                    "region_id": region["id"], "pass": pass_number,
                    "reviewer_id": f"synthetic-region-reviewer-{pass_number}",
                    "session_id": f"synthetic-region-session-{pass_number}",
                    "assessment": "content" if unit_ids else "blank", "source_unit_ids": unit_ids,
                    "evidence_ids": [f"image:{region['id']}"],
                    "observation": "Synthetic region observation; generated only to exercise record validation."})
    first = ledger["source_units"][0]
    images = first["evidence_ids"]
    ledger["recoveries"].append({"id": "recovery-01", "source_ids": ["s01"],
        "problem": "Synthetic ambiguity between the final digit five and six.",
        "candidates": [{"id": "five", "text": "2+3=5", "evidence_ids": images},
                       {"id": "six", "text": "2+3=6", "evidence_ids": images}],
        "selected_candidate_id": "five", "status": "resolved", "evidence_ids": images,
        "forward_validation": {"status": "pass", "method": "Direct integer addition of two and three",
            "inputs": "2+3", "result": "5", "evidence_ids": ["artifact:calculation"]},
        "backward_validation": {"status": "pass", "method": "Subtract three from the proposed result",
            "inputs": "5-3", "result": "2", "evidence_ids": ["artifact:calculation"]},
        "return_to_image": {"page_ids": ["p0001"], "region_ids": first["region_ids"],
            "evidence_ids": images, "observation": "Synthetic return to full-page and crop evidence for the digit."},
        "reviewer_id": "synthetic-recovery-reviewer", "session_id": "synthetic-recovery-session"})
    for number in range(1, 4):
        ledger["final_rounds"].append({"id": f"final-{number}", "round": number,
            "reviewer_id": f"synthetic-final-reviewer-{number}", "session_id": f"synthetic-final-session-{number}",
            "snapshot_sha256": "0" * 64, "previous_round_sha256": None,
            "scope": {}, "findings": [], "evidence_ids": ["image:p0001"], "page_notes": [],
            "notes": "Synthetic complete-record fixture; not an actual manuscript review.", "record_sha256": "0" * 64})
        ledger["final_rounds"][-1].update(synthetic_round_files(project, number))
    ledger_path = project / "ledger.json"
    reseal(manifest_path, ledger_path, ledger)
    return manifest_path, ledger_path


class AuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="audit-selftest-", dir=Path(__file__).parent)
        self.root = Path(self.temp.name)
        self.manifest_path, self.ledger_path = make_fixture(self.root)
        self.manifest = load_json(self.manifest_path)
        self.ledger = load_json(self.ledger_path)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def report(self, reseal_records: bool = False) -> dict:
        if reseal_records:
            reseal(self.manifest_path, self.ledger_path, self.ledger)
        else:
            write_json(self.ledger_path, self.ledger)
        return Auditor(self.manifest_path, self.ledger_path).run()

    def blocked(self, code: str, reseal_records: bool = False) -> dict:
        report = self.report(reseal_records)
        self.assertFalse(report["audit_pass"], report)
        self.assertTrue(any(error.startswith(code + ":") for error in report["structural_errors"]), report)
        return report

    def test_normal_complete_records_still_do_not_prove_visual_truth(self):
        report = self.report()
        self.assertTrue(report["audit_pass"], report)
        self.assertTrue(report["content_resolved"])
        self.assertEqual(report["unresolved_count"], 0)
        self.assertFalse(report["visual_reading_proven"])
        self.assertFalse(report["zero_omission_proven"])
        self.assertFalse(report["mathematical_correctness_proven"])

    def test_pdf_real_page_count_and_blank_hint(self):
        self.assertEqual(self.manifest["source_pdf"]["page_count"], 2)
        self.assertEqual(sum(len(page["regions"]) for page in self.manifest["pages"]), 12)
        self.assertTrue(all(region["blank_candidate"] for region in self.manifest["pages"][1]["regions"]))
        self.assertTrue(all(region["blank_status"] == "unreviewed" for page in self.manifest["pages"] for region in page["regions"]))

    def test_missing_physical_page(self):
        self.manifest["pages"].pop()
        write_json(self.manifest_path, self.manifest)
        self.blocked("PAGE_COVERAGE", True)

    def test_forged_pdf_page_count(self):
        self.manifest["source_pdf"]["page_count"] = 1
        self.manifest["pages"].pop()
        write_json(self.manifest_path, self.manifest)
        self.blocked("PAGE_COUNT", True)

    def test_missing_region(self):
        self.manifest["pages"][0]["regions"].pop()
        write_json(self.manifest_path, self.manifest)
        self.blocked("SCHEMA", True)

    def test_missing_region_second_pass(self):
        self.ledger["region_checks"].pop()
        self.blocked("REGION_TWO_PASSES", True)

    def test_blank_page_still_needs_two_whole_page_checks(self):
        self.ledger["page_checks"] = [check for check in self.ledger["page_checks"] if check["page_id"] != "p0002"]
        self.blocked("PAGE_TWO_PASSES", True)

    def test_blank_cannot_override_content_inventory(self):
        self.ledger["region_checks"][0]["assessment"] = "blank"
        self.blocked("BLANK_CONFLICT", True)

    def test_two_region_passes_cannot_share_identity(self):
        self.ledger["region_checks"][1]["reviewer_id"] = self.ledger["region_checks"][0]["reviewer_id"]
        self.blocked("REGION_INDEPENDENCE", True)

    def test_author_is_allowed_only_on_first_page_and_region_passes(self):
        for check in self.ledger["page_checks"] + self.ledger["region_checks"]:
            if check["pass"] == 1:
                check["reviewer_id"] = "synthetic-author"
        self.assertTrue(self.report(True)["audit_pass"])
        self.ledger["page_checks"][1]["reviewer_id"] = "synthetic-author"
        self.blocked("AUTHOR_SECOND_REVIEW", True)

    def test_missing_reverse_mapping(self):
        self.ledger["target_units"][0]["source_ids"] = ["s02"]
        self.blocked("BIDIRECTIONAL_MAPPING", True)

    def test_missing_study_mapping(self):
        self.ledger["source_units"][0]["study_target_ids"] = ["not-a-target"]
        self.blocked("SOURCE_TARGET", True)

    def test_text_inventory_cannot_ignore_new_line(self):
        path = self.ledger_path.parent / "study.md"
        path.write_text(path.read_text() + "Unmapped theorem.\n")
        self.ledger["artifacts"][1]["sha256"] = sha256_file(path)
        self.blocked("TEXT_COVERAGE", True)

    def test_text_unit_hash_is_exact(self):
        self.ledger["target_units"][0]["text_sha256"] = "0" * 64
        self.blocked("UNIT_TEXT_HASH", True)

    def test_old_draft_must_migrate_or_explain(self):
        self.ledger["old_units"][0]["target_ids"] = []
        self.blocked("SCHEMA", True)

    def test_explained_old_unit_needs_evidence_and_reason(self):
        old = self.ledger["old_units"][0]
        old.update(disposition="explained", explanation="done")
        self.blocked("SCHEMA", True)

    def test_explained_old_text_cannot_disappear_without_study_destination(self):
        self.ledger["old_units"][0].update(disposition="explained", target_ids=[],
            explanation="A ledger explanation alone must not delete the old mathematical content.")
        self.blocked("SCHEMA", True)

    def test_old_only_content_can_be_preserved_without_fabricated_source(self):
        study = self.ledger_path.parent / "study.md"
        old = self.ledger_path.parent / "old.md"
        study.write_text(study.read_text() + "Old-only supplement: 7-2=5.\n")
        old.write_text(old.read_text() + "7-2=5\n")
        for artifact in self.ledger["artifacts"]:
            if artifact["id"] in {"study", "old"}:
                artifact["sha256"] = sha256_file(self.ledger_path.parent / artifact["path"])
        self.ledger["old_units"].append({"id": "o02", "artifact_id": "old", "start_line": 2,
            "end_line": 2, "text_sha256": text_hash(old, 2, 2), "disposition": "migrated",
            "target_ids": ["old-only-target"], "explanation": "Retained in study as an explicitly attributed old-only supplement.",
            "evidence_ids": ["artifact:old", "artifact:study"]})
        self.ledger["target_units"].append({"id": "old-only-target", "artifact_id": "study",
            "start_line": 7, "end_line": 7, "text_sha256": text_hash(study, 7, 7),
            "source_ids": [], "old_ids": ["o02"], "origin": "old", "evidence_ids": ["artifact:old"],
            "status": "resolved", "explanation": "Old-only formula absent from the source PDF, retained with attribution."})
        self.assertTrue(self.report(True)["audit_pass"])

    def test_editorial_and_supplement_content_need_not_invent_source_units(self):
        study = self.ledger_path.parent / "study.md"
        study.write_text(study.read_text() + "A new section heading\nSupplement: 5-2=3.\n")
        self.ledger["artifacts"][1]["sha256"] = sha256_file(study)
        for line, origin, evidence in [(7, "editorial", "artifact:study"), (8, "supplement", "artifact:calculation")]:
            self.ledger["target_units"].append({"id": f"added-{line}", "artifact_id": "study",
                "start_line": line, "end_line": line, "text_sha256": text_hash(study, line, line),
                "source_ids": [], "old_ids": [], "origin": origin, "evidence_ids": [evidence],
                "status": "resolved", "explanation": "Explicitly added material; not attributed to source manuscript."})
        self.assertTrue(self.report(True)["audit_pass"])

    def test_recovery_pending_is_not_resolved(self):
        self.ledger["recoveries"][0]["forward_validation"]["status"] = "pending"
        report = self.blocked("RECOVERY_FALSE_RESOLUTION", True)
        self.assertGreater(report["unresolved_count"], 0)
        self.assertFalse(report["content_resolved"])

    def test_recovery_must_return_to_whole_page(self):
        self.ledger["recoveries"][0]["return_to_image"]["page_ids"] = ["p0002"]
        self.blocked("RECOVERY_RETURN_PAGE", True)

    def test_repeated_final_reviewer(self):
        self.ledger["final_rounds"][1]["reviewer_id"] = self.ledger["final_rounds"][0]["reviewer_id"]
        self.blocked("ROUND_REVIEWER", True)

    def test_repeated_final_session(self):
        self.ledger["final_rounds"][2]["session_id"] = self.ledger["final_rounds"][0]["session_id"]
        self.blocked("ROUND_SESSION", True)

    def test_author_cannot_be_final_reviewer(self):
        self.ledger["final_rounds"][0]["reviewer_id"] = "synthetic-author"
        self.blocked("ROUND_REVIEWER", True)

    def test_prior_region_reviewer_cannot_be_final_reviewer(self):
        self.ledger["final_rounds"][0]["reviewer_id"] = self.ledger["region_checks"][1]["reviewer_id"]
        self.blocked("ROUND_REVIEWER", True)

    def test_final_evidence_cannot_be_reused_across_rounds(self):
        self.ledger["final_rounds"][1]["blind_reading"] = copy.deepcopy(self.ledger["final_rounds"][0]["blind_reading"])
        self.blocked("ROUND_EVIDENCE_REUSE", True)

    def test_final_report_must_be_existing_nonempty_text(self):
        item = self.ledger["final_rounds"][0]["report"]
        path = self.ledger_path.parent / item["path"]
        path.write_text("")
        item["sha256"] = sha256_file(path)
        self.blocked("ROUND_EVIDENCE_INVALID", True)

    def test_evidence_file_must_exist(self):
        (self.ledger_path.parent / "calculation.txt").unlink()
        self.blocked("FILE_INTEGRITY")

    def test_hash_change_invalidates_rounds(self):
        path = self.ledger_path.parent / "study.md"
        path.write_text(path.read_text().replace("infer", "deduce"))
        report = self.blocked("FILE_INTEGRITY")
        self.assertTrue(any(error.startswith("ROUND_SNAPSHOT:") for error in report["structural_errors"]))

    def test_manifest_whitespace_change_is_pinned(self):
        self.manifest_path.write_text(self.manifest_path.read_text() + "\n")
        self.blocked("MANIFEST_HASH")

    def test_forged_crop_with_updated_hash_does_not_match_page(self):
        region = self.manifest["pages"][0]["regions"][0]
        path = self.manifest_path.parent / region["image"]["path"]
        with Image.open(path) as image:
            blank = Image.new("RGB", image.size, "white")
        blank.save(path)
        region["image"]["sha256"] = sha256_file(path)
        write_json(self.manifest_path, self.manifest)
        self.blocked("CROP_MISMATCH", True)

    def test_forged_full_page_with_updated_hash_does_not_match_pdf(self):
        page = self.manifest["pages"][0]
        path = self.manifest_path.parent / page["image"]["path"]
        Image.new("RGB", (page["width_px"], page["height_px"]), "white").save(path)
        page["image"]["sha256"] = sha256_file(path)
        write_json(self.manifest_path, self.manifest)
        self.blocked("PDF_RENDER_MISMATCH", True)

    def test_invalid_image_evidence_rejected_even_with_valid_hash(self):
        path = self.ledger_path.parent / "not-image.png"
        path.write_text("This is not an image.")
        self.ledger["artifacts"].append({"id": "bad-image", "path": path.name, "sha256": sha256_file(path),
                                        "kind": "evidence", "format": "image", "source_crop": {"page_id": "p0001", "bbox_px": [0, 0, 10, 10]}})
        self.blocked("ARTIFACT_INVALID", True)

    def test_partial_final_scope_rejected(self):
        self.ledger["final_rounds"][2]["scope"]["target_unit_ids"].pop()
        self.ledger["final_rounds"][2]["record_sha256"] = round_hash(self.ledger["final_rounds"][2])
        self.blocked("ROUND_SCOPE")

    def test_missing_explicit_findings_array(self):
        del self.ledger["final_rounds"][2]["findings"]
        self.blocked("SCHEMA")

    def test_changed_review_record_breaks_hash_chain(self):
        self.ledger["final_rounds"][0]["notes"] = "Altered after sealing, without rehashing."
        self.blocked("ROUND_HASH_CHAIN")

    def test_unresolved_issue_keeps_structural_pass_but_needs_model_recovery(self):
        self.ledger["issues"].append({"id": "issue-open", "status": "open",
            "description": "Synthetic uncertainty deliberately remains open.", "related_ids": ["s01"],
            "evidence_ids": ["image:p0001"], "resolution": ""})
        report = self.report(True)
        self.assertTrue(report["audit_pass"], report)
        self.assertFalse(report["content_resolved"])
        self.assertEqual(report["unresolved_count"], 1)
        self.assertEqual(report["status"], "NeedsModelRecovery")

    def test_findings_require_three_later_clear_rounds(self):
        self.ledger["issues"].append({"id": "issue-fixed", "status": "resolved",
            "description": "Synthetic finding discovered and then fixed.", "related_ids": ["s01"],
            "evidence_ids": ["image:p0001"], "resolution": "Rechecked synthetic arithmetic and source image."})
        self.ledger["final_rounds"][2]["findings"] = ["issue-fixed"]
        self.blocked("FINAL_FINDINGS", True)
        for number in range(4, 7):
            record = copy.deepcopy(self.ledger["final_rounds"][0])
            record.update(id=f"final-{number}", round=number, reviewer_id=f"new-reviewer-{number}", session_id=f"new-session-{number}", findings=[])
            record.update(synthetic_round_files(self.ledger_path.parent, number))
            self.ledger["final_rounds"].append(record)
        self.assertTrue(self.report(True)["audit_pass"])

    def test_report_does_not_change_snapshot_or_overwrite_content(self):
        auditor = Auditor(self.manifest_path, self.ledger_path)
        report = auditor.run()
        snapshot = report["snapshot_sha256"]
        auditor.write_report(self.ledger_path.parent / "reports" / "audit.json", report)
        self.assertEqual(Auditor(self.manifest_path, self.ledger_path).run()["snapshot_sha256"], snapshot)
        target = self.ledger_path.parent / "study.md"
        before = target.read_bytes()
        with self.assertRaises(ValueError):
            auditor.write_report(target, report)
        self.assertEqual(before, target.read_bytes())

    def test_old_snapshot_cannot_be_rebound_by_seal_round(self):
        last = self.ledger["final_rounds"][-1]
        last["record_sha256"] = None
        path = self.ledger_path.parent / "study.md"
        path.write_text(path.read_text().replace("infer", "deduce"))
        self.ledger["artifacts"][1]["sha256"] = sha256_file(path)
        write_json(self.ledger_path, self.ledger)
        before = self.ledger_path.read_bytes()
        command = [sys.executable, str(Path(__file__).parent / "audit.py"), "seal-round",
            "--manifest", str(self.manifest_path), "--ledger", str(self.ledger_path), "--round-id", last["id"]]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("predeclared snapshot", result.stderr)
        self.assertEqual(self.ledger_path.read_bytes(), before)

    def test_already_sealed_round_cannot_be_resealed(self):
        before = self.ledger_path.read_bytes()
        result = subprocess.run([sys.executable, str(Path(__file__).parent / "audit.py"), "seal-round",
            "--manifest", str(self.manifest_path), "--ledger", str(self.ledger_path),
            "--round-id", self.ledger["final_rounds"][-1]["id"]], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("already sealed", result.stderr)
        self.assertEqual(self.ledger_path.read_bytes(), before)

    def test_seal_only_computes_integrity_for_predeclared_current_snapshot(self):
        self.ledger["final_rounds"][-1]["record_sha256"] = None
        write_json(self.ledger_path, self.ledger)
        before = copy.deepcopy(self.ledger["final_rounds"][-1])
        result = subprocess.run([sys.executable, str(Path(__file__).parent / "audit.py"), "seal-round",
            "--manifest", str(self.manifest_path), "--ledger", str(self.ledger_path),
            "--round-id", before["id"]], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        after = load_json(self.ledger_path)["final_rounds"][-1]
        for field in before:
            if field not in ["record_sha256", "previous_round_sha256"]:
                self.assertEqual(before[field], after[field])
        self.assertTrue(Auditor(self.manifest_path, self.ledger_path).run()["audit_pass"])

    def test_template_is_not_preapproved(self):
        self.ledger = load_json(Path(__file__).parent / "schema" / "example.template.json")
        self.blocked("SCHEMA")

    def test_duplicate_json_keys_rejected(self):
        self.ledger_path.write_text('{"schema_version":"1.0","schema_version":"2.0"}')
        report = Auditor(self.manifest_path, self.ledger_path).run()
        self.assertFalse(report["audit_pass"])
        self.assertTrue(any("duplicate JSON key" in error for error in report["structural_errors"]))

    def test_paths_cannot_escape_project(self):
        self.ledger["artifacts"][0]["path"] = "../synthetic-input.pdf"
        self.blocked("FILE_INTEGRITY")

    def test_grid_covers_small_and_boundary_sizes(self):
        cases = 0
        for width in [1, 2, 3, 7, 120]:
            for height in [1, 2, 3, 4, 90]:
                for overlap in [0, 0.08, 0.45]:
                    boxes = region_boxes(width, height, overlap)
                    self.assertEqual(len(boxes), 6)
                    pixels = set()
                    for _, _, (x0, y0, x1, y1) in boxes:
                        self.assertTrue(0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height)
                        pixels.update((x, y) for x in range(x0, x1) for y in range(y0, y1))
                    self.assertEqual(len(pixels), width * height)
                    cases += 1
        self.assertEqual(cases, 5 * 5 * 3)

    def test_cli_exit_codes(self):
        command = [sys.executable, str(Path(__file__).parent / "audit.py"), "check",
                   "--manifest", str(self.manifest_path), "--ledger", str(self.ledger_path)]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.ledger["issues"].append({"id": "cli-open", "status": "open", "description": "Synthetic unresolved CLI case.",
            "related_ids": ["s01"], "evidence_ids": ["image:p0001"], "resolution": ""})
        self.report(True)
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.ledger["final_rounds"] = []
        write_json(self.ledger_path, self.ledger)
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-fixture", type=Path,
                        help="write a clearly synthetic, complete fixture for CLI experiments; never a real review")
    args, remaining = parser.parse_known_args()
    if args.emit_fixture:
        manifest, ledger = make_fixture(args.emit_fixture)
        print(json.dumps({"synthetic_only": True, "manifest": str(manifest), "ledger": str(ledger)}, indent=2))
    else:
        unittest.main(argv=[sys.argv[0]] + remaining, verbosity=2)
