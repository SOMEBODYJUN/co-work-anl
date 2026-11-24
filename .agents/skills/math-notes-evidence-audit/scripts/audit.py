#!/usr/bin/env python3
"""Audit deterministic inventory/record integrity; never certify visual truth."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
from typing import Any

import fitz
from jsonschema import Draft202012Validator
from PIL import Image

from prepare_pdf import region_boxes, sha256_file

SCHEMA_DIR = Path(__file__).resolve().parent / "schema"
LIMITATIONS = [
    "结构/记录通过不等于图像确已被阅读，也不等于数学内容零错或零遗漏。",
    "程序核验文件、像素、覆盖清单、双向映射与审核记录；不能判断原图内容单元清单是否真实穷尽。",
    "reviewer_id/session_id 为声明的身份；记录与哈希不能证明真实独立人员或代理确实完成视觉阅读。",
    "恢复候选、前向/反向验证与回图的存在和绑定可核验，其数学结论仍须人工审查。",
]


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


def load_json(path: Path) -> Any:
    def unique_object(pairs: list[tuple[str, Any]]) -> dict:
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"invalid JSON number: {value}")))


def safe_path(root: Path, relative: str) -> Path:
    relative_path = Path(relative)
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise ValueError(f"file path must stay inside project: {relative}")
    resolved = (root / relative_path).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError(f"file path escapes project (including symlinks): {relative}")
    return resolved


def text_span(path: Path, start: int, end: int) -> tuple[str, list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not 1 <= start <= end <= len(lines):
        raise ValueError(f"invalid line range {start}..{end} in {path.name} ({len(lines)} lines)")
    return "\n".join(lines[start - 1:end]), lines


def text_hash(path: Path, start: int, end: int) -> str:
    return hashlib.sha256(text_span(path, start, end)[0].encode("utf-8")).hexdigest()


def file_inventory(manifest_path: Path, ledger_path: Path, manifest: dict, ledger: dict) -> dict[str, Path]:
    files = {"manifest": manifest_path.resolve(),
             "source_pdf": safe_path(manifest_path.parent, manifest["source_pdf"]["path"])}
    for page in manifest["pages"]:
        files[f"image:{page['id']}"] = safe_path(manifest_path.parent, page["image"]["path"])
        for region in page["regions"]:
            files[f"image:{region['id']}"] = safe_path(manifest_path.parent, region["image"]["path"])
    for artifact in ledger["artifacts"]:
        files[f"artifact:{artifact['id']}"] = safe_path(ledger_path.parent, artifact["path"])
    return files


def content_snapshot(manifest_path: Path, ledger_path: Path, manifest: dict, ledger: dict) -> str:
    files = file_inventory(manifest_path, ledger_path, manifest, ledger)
    return canonical_hash({
        "manifest_sha256": sha256_file(manifest_path),
        "file_digests": {key: sha256_file(path) for key, path in sorted(files.items())},
        "ledger_content": {key: value for key, value in ledger.items() if key != "final_rounds"},
    })


def round_hash(record: dict) -> str:
    return canonical_hash({key: value for key, value in record.items() if key != "record_sha256"})


def expected_scope(manifest: dict, ledger: dict) -> dict[str, list[str]]:
    return {
        "page_ids": sorted(page["id"] for page in manifest["pages"]),
        "region_ids": sorted(region["id"] for page in manifest["pages"] for region in page["regions"]),
        "source_unit_ids": sorted(unit["id"] for unit in ledger["source_units"]),
        "target_unit_ids": sorted(unit["id"] for unit in ledger["target_units"]),
        "old_unit_ids": sorted(unit["id"] for unit in ledger["old_units"]),
        "recovery_ids": sorted(item["id"] for item in ledger["recoveries"]),
        "artifact_ids": sorted(item["id"] for item in ledger["artifacts"]),
        "issue_ids": sorted(item["id"] for item in ledger["issues"]),
        "page_check_ids": sorted(item["id"] for item in ledger["page_checks"]),
        "region_check_ids": sorted(item["id"] for item in ledger["region_checks"]),
    }


def intersects(a: list[int], b: list[int]) -> bool:
    return max(a[0], b[0]) < min(a[2], b[2]) and max(a[1], b[1]) < min(a[3], b[3])


class Auditor:
    def __init__(self, manifest_path: Path, ledger_path: Path):
        self.manifest_path = manifest_path.resolve()
        self.ledger_path = ledger_path.resolve()
        self.errors: list[str] = []
        self.unresolved: list[dict[str, str]] = []
        self.evidence: dict[str, Path] = {}
        self.protected = {self.manifest_path, self.ledger_path}
        self.snapshot: str | None = None
        self.manifest: dict = {}
        self.ledger: dict = {}

    def error(self, code: str, detail: str) -> None:
        self.errors.append(f"{code}: {detail}")

    def pending(self, kind: str, identifier: str, reason: str) -> None:
        entry = {"kind": kind, "id": identifier, "reason": reason}
        if not any(item["kind"] == kind and item["id"] == identifier for item in self.unresolved):
            self.unresolved.append(entry)

    def schema(self, value: dict, filename: str) -> bool:
        validator = Draft202012Validator(load_json(SCHEMA_DIR / filename))
        errors = sorted(validator.iter_errors(value), key=lambda item: str(list(item.absolute_path)))
        for error in errors:
            self.error("SCHEMA", f"{filename}:{'/'.join(map(str, error.absolute_path))}: {error.message}")
        return not errors

    def checked_file(self, root: Path, item: dict, identifier: str) -> Path | None:
        try:
            path = safe_path(root, item["path"])
            self.protected.add(path)
            if not path.is_file():
                raise ValueError(f"missing evidence/content file: {item['path']}")
            digest = sha256_file(path)
            if digest != item["sha256"]:
                raise ValueError(f"sha256 mismatch for {item['path']}")
            self.evidence[identifier] = path
            return path
        except (OSError, ValueError) as error:
            self.error("FILE_INTEGRITY", str(error))
            return None

    def references(self, ids: list[str], context: str, required: set[str] | None = None) -> None:
        for identifier in ids:
            if identifier not in self.evidence:
                self.error("EVIDENCE_INVALID", f"{context}: unavailable or unverified evidence {identifier}")
        if required and not required.issubset(ids):
            self.error("EVIDENCE_BINDING", f"{context}: missing image/file evidence {sorted(required - set(ids))}")

    def unique_index(self, entries: list[dict], kind: str) -> dict[str, dict]:
        counts = Counter(entry["id"] for entry in entries)
        for identifier, count in counts.items():
            if count > 1:
                self.error("DUPLICATE_ID", f"{kind}: {identifier}")
        return {entry["id"]: entry for entry in entries}

    def check_manifest(self) -> tuple[dict, dict]:
        manifest = self.manifest
        pages = self.unique_index(manifest["pages"], "page")
        all_regions = [region for page in manifest["pages"] for region in page["regions"]]
        regions = self.unique_index(all_regions, "region")
        source = self.checked_file(self.manifest_path.parent, manifest["source_pdf"], "source_pdf")
        if sha256_file(self.manifest_path) != self.ledger["manifest_sha256"]:
            self.error("MANIFEST_HASH", "ledger does not pin the current manifest")
        expected_count = manifest["source_pdf"]["page_count"]
        if len(pages) != expected_count or [page["number"] for page in manifest["pages"]] != list(range(1, expected_count + 1)):
            self.error("PAGE_COVERAGE", "manifest pages must enumerate every physical PDF page in order")
        document = None
        if source:
            try:
                document = fitz.open(source)
                if document.page_count != expected_count:
                    self.error("PAGE_COUNT", f"PDF has {document.page_count} pages, manifest claims {expected_count}")
            except (RuntimeError, ValueError) as error:
                self.error("PDF_INVALID", str(error))
        for page in manifest["pages"]:
            page_id = page["id"]
            width, height = page["width_px"], page["height_px"]
            if page_id != f"p{page['number']:04d}":
                self.error("PAGE_ID", f"noncanonical page id: {page_id}")
            if page["image"]["bbox_px"] != [0, 0, width, height]:
                self.error("PAGE_BBOX", page_id)
            full_path = self.checked_file(self.manifest_path.parent, page["image"], f"image:{page_id}")
            full = None
            if full_path:
                try:
                    with Image.open(full_path) as image:
                        if image.format != "PNG" or image.size != (width, height):
                            raise ValueError("full-page PNG size/format mismatch")
                        full = image.convert("RGB")
                    if document and page["number"] <= document.page_count:
                        pix = document[page["number"] - 1].get_pixmap(
                            dpi=manifest["render"]["dpi"], colorspace=fitz.csRGB, alpha=False)
                        if (pix.width, pix.height) != full.size or pix.samples != full.tobytes():
                            self.error("PDF_RENDER_MISMATCH", f"{page_id}: full page does not match PDF re-render")
                except (OSError, ValueError, RuntimeError) as error:
                    self.error("IMAGE_INVALID", f"{page_id}: {error}")
            expected = region_boxes(width, height, manifest["render"]["overlap_fraction"])
            actual_cells = {(region["row"], region["column"]) for region in page["regions"]}
            if actual_cells != {(row, col) for row, col, _ in expected}:
                self.error("REGION_COVERAGE", f"{page_id}: missing/duplicate grid cells")
            for region in page["regions"]:
                rid = region["id"]
                expected_id = f"{page_id}-r{region['row']}c{region['column']}"
                box = next(box for row, col, box in expected if row == region["row"] and col == region["column"])
                if rid != expected_id or region["bbox_px"] != box:
                    self.error("REGION_BBOX", f"{rid}: id/bbox does not match full-cover overlapping grid")
                path = self.checked_file(self.manifest_path.parent, region["image"], f"image:{rid}")
                if path:
                    try:
                        with Image.open(path) as image:
                            if image.format != "PNG" or image.size != (box[2] - box[0], box[3] - box[1]):
                                raise ValueError("region PNG size/format mismatch")
                            if full and image.convert("RGB").tobytes() != full.crop(box).tobytes():
                                self.error("CROP_MISMATCH", f"{rid}: pixels differ from full-page bbox")
                    except (OSError, ValueError) as error:
                        self.error("IMAGE_INVALID", f"{rid}: {error}")
        if document:
            document.close()
        return pages, regions

    def check_artifacts(self) -> dict:
        artifacts = self.unique_index(self.ledger["artifacts"], "artifact")
        kinds = {artifact["kind"] for artifact in artifacts.values()}
        if not {"transcription", "study"}.issubset(kinds):
            self.error("DELIVERY_CONTENT", "at least one transcription and one study artifact are required")
        seen_paths = set()
        for identifier, artifact in artifacts.items():
            path = self.checked_file(self.ledger_path.parent, artifact, f"artifact:{identifier}")
            if path in seen_paths:
                self.error("ARTIFACT_ALIAS", f"different artifacts use the same file: {artifact['path']}")
            seen_paths.add(path)
            if artifact["kind"] != "evidence" and artifact["format"] != "text":
                self.error("ARTIFACT_FORMAT", f"content artifact {identifier} must be UTF-8 text with line inventory")
            if path:
                try:
                    if artifact["format"] == "text":
                        content = path.read_text(encoding="utf-8")
                        if artifact["kind"] == "evidence" and not content.strip():
                            raise ValueError("empty evidence file")
                    else:
                        with Image.open(path) as image:
                            image.load()
                            crop = artifact.get("source_crop")
                            page = next((page for page in self.manifest["pages"] if crop and page["id"] == crop["page_id"]), None)
                            if artifact["kind"] != "evidence" or not crop or page is None:
                                raise ValueError("image evidence needs a valid source_crop page_id and pixel bbox")
                            box = crop["bbox_px"]
                            if not (0 <= box[0] < box[2] <= page["width_px"] and 0 <= box[1] < box[3] <= page["height_px"]):
                                raise ValueError("extra crop bbox is outside source page")
                            full_path = self.evidence.get(f"image:{page['id']}")
                            if full_path is None:
                                raise ValueError("extra crop's full-page evidence is unverified")
                            with Image.open(full_path) as full:
                                expected = full.convert("RGB").crop(box)
                                if image.size != expected.size or image.convert("RGB").tobytes() != expected.tobytes():
                                    raise ValueError("extra crop pixels do not match source page bbox")
                except (OSError, UnicodeError, ValueError) as error:
                    self.evidence.pop(f"artifact:{identifier}", None)
                    self.error("ARTIFACT_INVALID", f"{identifier}: {error}")
        return artifacts

    def check_line_inventory(self, artifacts: dict, targets: dict, old: dict) -> None:
        inventory = defaultdict(list)
        for unit in list(targets.values()) + list(old.values()):
            artifact_id = unit["artifact_id"]
            artifact = artifacts.get(artifact_id)
            expected_kinds = {"transcription", "study"} if unit["id"] in targets else {"old"}
            if artifact is None or artifact["kind"] not in expected_kinds:
                self.error("UNIT_ARTIFACT", f"{unit['id']}: wrong or missing content artifact {artifact_id}")
                continue
            path = self.evidence.get(f"artifact:{artifact_id}")
            if path is None:
                continue
            try:
                text, _ = text_span(path, unit["start_line"], unit["end_line"])
                if not text.strip():
                    self.error("EMPTY_UNIT", f"{unit['id']}: only blank lines")
                if hashlib.sha256(text.encode("utf-8")).hexdigest() != unit["text_sha256"]:
                    self.error("UNIT_TEXT_HASH", unit["id"])
                inventory[artifact_id].extend(range(unit["start_line"], unit["end_line"] + 1))
            except (OSError, UnicodeError, ValueError) as error:
                self.error("UNIT_SPAN", f"{unit['id']}: {error}")
        for identifier, artifact in artifacts.items():
            if artifact["kind"] == "evidence" or artifact["format"] != "text":
                continue
            path = self.evidence.get(f"artifact:{identifier}")
            if path is None:
                continue
            required = {index for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1) if line.strip()}
            counts = Counter(inventory[identifier])
            missing = required - counts.keys()
            duplicate = {line for line, count in counts.items() if count > 1 and line in required}
            if missing:
                self.error("TEXT_COVERAGE", f"{identifier}: nonblank lines missing units: {sorted(missing)}")
            if duplicate:
                self.error("TEXT_OVERLAP", f"{identifier}: nonblank lines assigned more than once: {sorted(duplicate)}")

    def check_units(self, pages: dict, regions: dict, artifacts: dict) -> tuple[dict, dict, dict]:
        sources = self.unique_index(self.ledger["source_units"], "source unit")
        targets = self.unique_index(self.ledger["target_units"], "target unit")
        old = self.unique_index(self.ledger["old_units"], "old unit")
        if set(sources) & set(targets) or set(old) & (set(sources) | set(targets)):
            self.error("UNIT_ID_COLLISION", "source, target and old unit ids must use distinct namespaces")
        for identifier, unit in sources.items():
            page = pages.get(unit["page_id"])
            box = unit["bbox_px"]
            if page is None:
                self.error("SOURCE_PAGE", f"{identifier}: missing page")
            elif not (0 <= box[0] < box[2] <= page["width_px"] and 0 <= box[1] < box[3] <= page["height_px"]):
                self.error("SOURCE_BBOX", identifier)
            elif set(unit["region_ids"]) != {region["id"] for region in page["regions"] if intersects(box, region["bbox_px"])}:
                self.error("SOURCE_REGION_BINDING", f"{identifier}: regions must include all grid crops intersecting its bbox")
            self.references(unit["evidence_ids"], identifier, {f"image:{unit['page_id']}"} | {f"image:{rid}" for rid in unit["region_ids"]})
            for field, kind in [("transcription_target_ids", "transcription"), ("study_target_ids", "study")]:
                for tid in unit[field]:
                    target = targets.get(tid)
                    artifact = artifacts.get(target["artifact_id"]) if target else None
                    if target is None or artifact is None or artifact["kind"] != kind:
                        self.error("SOURCE_TARGET", f"{identifier}: invalid {kind} target {tid}")
                    elif target["origin"] not in {"source", "supplement"}:
                        self.error("SOURCE_ORIGIN", f"{identifier}: target {tid} must explicitly identify source-related content")
                    elif identifier not in target["source_ids"]:
                        self.error("BIDIRECTIONAL_MAPPING", f"{identifier} -> {tid} has no reverse mapping")
                    elif unit["status"] == "resolved" and target["status"] == "unresolved":
                        self.error("RESOLUTION_CONFLICT", f"{identifier}: target {tid} remains unresolved")
            if unit["status"] == "unresolved":
                self.pending("source_unit", identifier, "source interpretation remains unresolved")
        for identifier, unit in targets.items():
            artifact = artifacts.get(unit["artifact_id"])
            kind = artifact["kind"] if artifact else None
            field = "transcription_target_ids" if kind == "transcription" else "study_target_ids"
            self.references(unit["evidence_ids"], identifier)
            if unit["origin"] == "source" and not unit["source_ids"]:
                self.error("TARGET_ORIGIN", f"{identifier}: source-origin target needs original-image units")
            if unit["origin"] == "old" and (unit["source_ids"] or not unit["old_ids"]):
                self.error("TARGET_ORIGIN", f"{identifier}: old-only target needs old_ids and must not invent source-image ids")
            if unit["origin"] == "editorial" and (unit["source_ids"] or unit["old_ids"]):
                self.error("TARGET_ORIGIN", f"{identifier}: editorial content must not pretend to originate in the source or old draft")
            if unit["origin"] in {"supplement", "editorial"} and len(unit["explanation"].strip()) < 8:
                self.error("TARGET_EXPLANATION", f"{identifier}: added or editorial material needs an explicit explanation")
            if unit["origin"] == "supplement" and not unit["source_ids"] and not unit["old_ids"]:
                calculation = {f"artifact:{aid}" for aid, item in artifacts.items() if item["kind"] == "evidence" and item["format"] == "text"}
                if not calculation.intersection(unit["evidence_ids"]):
                    self.error("SUPPLEMENT_EVIDENCE", f"{identifier}: independent supplement needs concrete text calculation/reference evidence")
            self.references(unit["evidence_ids"], identifier,
                            {f"image:{sources[sid]['page_id']}" for sid in unit["source_ids"] if sid in sources}
                            | {f"artifact:{old[oid]['artifact_id']}" for oid in unit["old_ids"] if oid in old})
            for sid in unit["source_ids"]:
                source = sources.get(sid)
                if source is None or identifier not in source[field]:
                    self.error("BIDIRECTIONAL_MAPPING", f"{identifier} -> {sid} has no matching source mapping")
                elif source["status"] == "unresolved" and unit["status"] == "resolved":
                    self.error("RESOLUTION_CONFLICT", f"{identifier}: source {sid} remains unresolved")
            for oid in unit["old_ids"]:
                prior = old.get(oid)
                if prior is None or identifier not in prior["target_ids"]:
                    self.error("OLD_BIDIRECTIONAL_MAPPING", f"{identifier} -> {oid} has no matching old-unit destination")
            if unit["status"] == "unresolved":
                self.pending("target_unit", identifier, "target interpretation remains unresolved")
        for identifier, unit in old.items():
            self.references(unit["evidence_ids"], identifier, {f"artifact:{unit['artifact_id']}"})
            if not unit["target_ids"]:
                self.error("OLD_MIGRATION", f"{identifier}: every old unit needs a concrete study destination, including explained/unresolved material")
            for tid in unit["target_ids"]:
                target = targets.get(tid)
                target_artifact = artifacts.get(target["artifact_id"]) if target else None
                if target is None or target_artifact is None or target_artifact["kind"] != "study":
                    self.error("OLD_MIGRATION", f"{identifier}: {tid} is not a concrete study target")
                elif identifier not in target["old_ids"]:
                    self.error("OLD_BIDIRECTIONAL_MAPPING", f"{identifier} -> {tid} has no reverse old_ids mapping")
                elif unit["disposition"] == "unresolved" and target["status"] != "unresolved":
                    self.error("RESOLUTION_CONFLICT", f"{identifier}: study target {tid} must preserve unresolved status")
            if len(unit["explanation"].strip()) < 8:
                self.error("OLD_EXPLANATION", f"{identifier}: identify how the old statement is retained/corrected/discussed at the study destination")
            if unit["disposition"] == "unresolved":
                self.pending("old_unit", identifier, "old text has neither completed migration nor accepted explanation")
        self.check_line_inventory(artifacts, targets, old)
        return sources, targets, old

    def check_pages(self, pages: dict, sources: dict) -> None:
        self.unique_index(self.ledger["page_checks"], "page check")
        grouped = defaultdict(list)
        for check in self.ledger["page_checks"]:
            identifier, pid = check["id"], check["page_id"]
            grouped[pid].append(check)
            if pid not in pages:
                self.error("CHECK_PAGE", f"{identifier}: nonexistent page {pid}")
            expected = {sid for sid, unit in sources.items() if unit["page_id"] == pid}
            cross = {sid for sid in expected if len(sources[sid]["region_ids"]) > 1}
            if set(check["source_unit_ids"]) != expected or set(check["cross_region_unit_ids"]) != cross:
                self.error("PAGE_UNIT_COVERAGE", f"{identifier}: whole-page/cross-region unit inventory differs")
            if check["assessment"] == "blank" and expected:
                self.error("PAGE_BLANK_CONFLICT", identifier)
            if check["assessment"] == "content" and not expected:
                self.error("PAGE_EMPTY_CONTENT", identifier)
            if check["pass"] == 2 and check["reviewer_id"] in self.ledger["authors"]:
                self.error("AUTHOR_SECOND_REVIEW", identifier)
            self.references(check["evidence_ids"], identifier, {f"image:{pid}"})
            if check["assessment"] == "unresolved":
                self.pending("page_check", identifier, "whole-page assessment remains unresolved")
        for pid in pages:
            checks = grouped[pid]
            if len(checks) != 2 or {check["pass"] for check in checks} != {1, 2}:
                self.error("PAGE_TWO_PASSES", f"{pid}: two explicit whole-page checks are required, including blank pages")
            if len({check["reviewer_id"] for check in checks}) != len(checks) or len({check["session_id"] for check in checks}) != len(checks):
                self.error("PAGE_INDEPENDENCE", f"{pid}: the two whole-page checks require distinct reviewers and sessions")

    def check_regions(self, regions: dict, sources: dict) -> None:
        self.unique_index(self.ledger["region_checks"], "region check")
        grouped = defaultdict(list)
        for check in self.ledger["region_checks"]:
            identifier, rid = check["id"], check["region_id"]
            grouped[rid].append(check)
            if rid not in regions:
                self.error("CHECK_REGION", f"{identifier}: nonexistent region {rid}")
            expected_units = {sid for sid, unit in sources.items() if rid in unit["region_ids"]}
            if set(check["source_unit_ids"]) != expected_units:
                self.error("REGION_UNIT_COVERAGE", f"{identifier}: source unit inventory differs from region")
            if check["assessment"] == "blank" and expected_units:
                self.error("BLANK_CONFLICT", f"{identifier}: blank assessment conflicts with source units")
            if check["assessment"] == "content" and not expected_units:
                self.error("EMPTY_CONTENT_INVENTORY", f"{identifier}: content assessment has no source units")
            if check["pass"] == 2 and check["reviewer_id"] in self.ledger["authors"]:
                self.error("AUTHOR_SECOND_REVIEW", f"{identifier}: second pass requires a nonauthor")
            self.references(check["evidence_ids"], identifier, {f"image:{rid}"})
            if check["assessment"] == "unresolved":
                self.pending("region_check", identifier, "content/blank assessment remains unresolved")
        for rid in regions:
            checks = grouped[rid]
            if len(checks) != 2 or {check["pass"] for check in checks} != {1, 2}:
                self.error("REGION_TWO_PASSES", f"{rid}: exactly one pass 1 and one pass 2 are required")
            if len({check["reviewer_id"] for check in checks}) != len(checks) or len({check["session_id"] for check in checks}) != len(checks):
                self.error("REGION_INDEPENDENCE", f"{rid}: the two passes require distinct reviewer and session ids")

    def check_recoveries(self, sources: dict, regions: dict) -> dict:
        recoveries = self.unique_index(self.ledger["recoveries"], "recovery")
        for identifier, recovery in recoveries.items():
            for sid in recovery["source_ids"]:
                if sid not in sources:
                    self.error("RECOVERY_SOURCE", f"{identifier}: missing source {sid}")
            candidates = self.unique_index(recovery["candidates"], f"{identifier} candidate")
            if len({candidate["text"].strip() for candidate in candidates.values()}) < 2:
                self.error("RECOVERY_CANDIDATES", f"{identifier}: alternatives must contain distinct content")
            self.references(recovery["evidence_ids"], identifier)
            for candidate in candidates.values():
                self.references(candidate["evidence_ids"], f"{identifier}/{candidate['id']}")
            for direction in ["forward_validation", "backward_validation"]:
                self.references(recovery[direction]["evidence_ids"], f"{identifier}/{direction}")
            back = recovery["return_to_image"]
            needed_regions = {rid for sid in recovery["source_ids"] if sid in sources for rid in sources[sid]["region_ids"]}
            needed_pages = {sources[sid]["page_id"] for sid in recovery["source_ids"] if sid in sources}
            if set(back["region_ids"]) != needed_regions or not set(back["region_ids"]).issubset(regions):
                self.error("RECOVERY_RETURN_IMAGE", f"{identifier}: return-to-image must cover every associated source region")
            if set(back["page_ids"]) != needed_pages:
                self.error("RECOVERY_RETURN_PAGE", f"{identifier}: return-to-image must include whole source pages")
            self.references(back["evidence_ids"], f"{identifier}/return_to_image", {f"image:{rid}" for rid in needed_regions | needed_pages})
            if recovery["reviewer_id"] in self.ledger["authors"]:
                self.error("AUTHOR_RECOVERY_REVIEW", identifier)
            validations_pass = all(recovery[key]["status"] == "pass" for key in ["forward_validation", "backward_validation"])
            if recovery["status"] == "resolved":
                if recovery["selected_candidate_id"] not in candidates or not validations_pass:
                    self.error("RECOVERY_FALSE_RESOLUTION", f"{identifier}: selected candidate and both passing validations are required")
                if recovery["forward_validation"]["method"].strip() == recovery["backward_validation"]["method"].strip():
                    self.error("RECOVERY_VALIDATION", f"{identifier}: forward and reverse methods must describe distinct checks")
            if recovery["status"] == "unresolved" or not validations_pass:
                self.pending("recovery", identifier, "candidate selection or validation remains unresolved")
                for sid in recovery["source_ids"]:
                    if sid in sources and sources[sid]["status"] != "unresolved":
                        self.error("RESOLUTION_CONFLICT", f"{identifier}: source {sid} must retain unresolved status")
        return recoveries

    def check_issues(self, known_ids: set[str]) -> dict:
        issues = self.unique_index(self.ledger["issues"], "issue")
        for identifier, issue in issues.items():
            self.references(issue["evidence_ids"], identifier)
            for related in issue["related_ids"]:
                if related not in known_ids:
                    self.error("ISSUE_REFERENCE", f"{identifier}: unknown related id {related}")
            if issue["status"] == "open":
                self.pending("issue", identifier, issue["description"])
            elif len(issue["resolution"].strip()) < 8:
                self.error("ISSUE_RESOLUTION", f"{identifier}: resolved issue needs a substantive resolution")
        return issues

    def check_rounds(self, issues: dict) -> None:
        rounds = self.ledger["final_rounds"]
        self.unique_index(rounds, "final round")
        reviewers, sessions = set(), set()
        prior_reviews = self.ledger["page_checks"] + self.ledger["region_checks"] + self.ledger["recoveries"]
        prior_reviewers = {item["reviewer_id"] for item in prior_reviews}
        prior_sessions = {item["session_id"] for item in prior_reviews}
        prior_evidence_paths = set(self.evidence.values()) | self.protected
        audit_evidence_paths, audit_evidence_hashes = set(), set()
        previous = None
        for number, record in enumerate(rounds, 1):
            identifier = record["id"]
            if record["round"] != number:
                self.error("ROUND_SEQUENCE", f"{identifier}: rounds must be consecutive starting at 1")
            if record["previous_round_sha256"] != previous or record["record_sha256"] != round_hash(record):
                self.error("ROUND_HASH_CHAIN", f"{identifier}: altered, unsealed, or broken previous-round link")
            previous = record["record_sha256"]
            if record["reviewer_id"] in self.ledger["authors"] or record["reviewer_id"] in reviewers or record["reviewer_id"] in prior_reviewers:
                self.error("ROUND_REVIEWER", f"{identifier}: each final round needs a new reviewer uninvolved in authoring or earlier review")
            if record["session_id"] in sessions or record["session_id"] in prior_sessions:
                self.error("ROUND_SESSION", f"{identifier}: session id was reused from earlier review or across rounds")
            reviewers.add(record["reviewer_id"])
            sessions.add(record["session_id"])
            for phase in ["blind_reading", "report"]:
                item = record[phase]
                path = self.checked_file(self.ledger_path.parent, item, f"round:{identifier}:{phase}")
                if path:
                    if path in prior_evidence_paths or path in audit_evidence_paths or item["sha256"] in audit_evidence_hashes:
                        self.error("ROUND_EVIDENCE_REUSE", f"{identifier}/{phase}: use an independent file and content for each review phase and round")
                    audit_evidence_paths.add(path)
                    audit_evidence_hashes.add(item["sha256"])
                    try:
                        if len(path.read_text(encoding="utf-8").strip()) < 8:
                            raise ValueError("audit evidence must be substantive, nonempty UTF-8 text")
                    except (OSError, UnicodeError, ValueError) as error:
                        self.evidence.pop(f"round:{identifier}:{phase}", None)
                        self.error("ROUND_EVIDENCE_INVALID", f"{identifier}/{phase}: {error}")
            self.references(record["evidence_ids"], identifier)
            for finding in record["findings"]:
                if finding not in issues:
                    self.error("ROUND_FINDING", f"{identifier}: finding {finding} needs an issue record")
        if len(rounds) < 3:
            self.error("FINAL_THREE_ROUNDS", "three consecutive complete rounds are required")
        scope = expected_scope(self.manifest, self.ledger)
        required_images = {f"image:{identifier}" for identifier in scope["page_ids"] + scope["region_ids"]}
        for record in rounds[-3:]:
            identifier = record["id"]
            if record["snapshot_sha256"] != self.snapshot:
                self.error("ROUND_SNAPSHOT", f"{identifier}: snapshot no longer matches all current delivery files and records")
            if record["findings"] != []:
                self.error("FINAL_FINDINGS", f"{identifier}: last three rounds must explicitly have an empty new-findings list")
            for field, ids in scope.items():
                if set(record["scope"][field]) != set(ids):
                    self.error("ROUND_SCOPE", f"{identifier}/{field}: scope must contain the entire current inventory")
            notes = [entry["page_id"] for entry in record["page_notes"]]
            if len(notes) != len(set(notes)) or set(notes) != set(scope["page_ids"]):
                self.error("ROUND_PAGE_NOTES", f"{identifier}: each physical page needs an observation")
            self.references(record["evidence_ids"], identifier, required_images)

    def run(self) -> dict:
        try:
            self.manifest = load_json(self.manifest_path)
            self.ledger = load_json(self.ledger_path)
            manifest_ok = self.schema(self.manifest, "manifest.schema.json")
            ledger_ok = self.schema(self.ledger, "ledger.schema.json")
            if manifest_ok and ledger_ok:
                pages, regions = self.check_manifest()
                artifacts = self.check_artifacts()
                sources, targets, old = self.check_units(pages, regions, artifacts)
                self.check_pages(pages, sources)
                self.check_regions(regions, sources)
                recoveries = self.check_recoveries(sources, regions)
                known = set(pages) | set(regions) | set(artifacts) | set(sources) | set(targets) | set(old) | set(recoveries)
                issues = self.check_issues(known)
                try:
                    self.snapshot = content_snapshot(self.manifest_path, self.ledger_path, self.manifest, self.ledger)
                except (OSError, ValueError) as error:
                    self.error("SNAPSHOT_UNAVAILABLE", str(error))
                self.check_rounds(issues)
        except (OSError, ValueError, UnicodeError, RuntimeError) as error:
            self.error("INPUT_INVALID", str(error))
        audit_pass = not self.errors
        content_resolved = audit_pass and not self.unresolved
        return {
            "audit_pass": audit_pass,
            "content_resolved": content_resolved,
            "status": "RecordsComplete_ContentUnverified" if content_resolved else "NeedsHuman",
            "snapshot_sha256": self.snapshot,
            "unresolved_count": len(self.unresolved),
            "unresolved": self.unresolved,
            "structural_error_count": len(self.errors),
            "structural_errors": self.errors,
            "visual_reading_proven": False,
            "zero_omission_proven": False,
            "mathematical_correctness_proven": False,
            "limitations": LIMITATIONS,
        }

    def write_report(self, report_path: Path, report: dict) -> None:
        report_path = report_path.resolve()
        if report_path in self.protected:
            raise ValueError("report path is a locked input/content file; choose a separate audit report path")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ["check", "snapshot", "scope", "seal-round"]:
        subparser = commands.add_parser(command)
        subparser.add_argument("--manifest", type=Path, required=True)
        subparser.add_argument("--ledger", type=Path, required=True)
        if command == "check":
            subparser.add_argument("--report", type=Path)
        if command == "seal-round":
            subparser.add_argument("--round-id", required=True)
    hash_parser = commands.add_parser("hash")
    hash_parser.add_argument("file", type=Path)
    text_parser = commands.add_parser("text-hash")
    text_parser.add_argument("file", type=Path)
    text_parser.add_argument("--start", type=int, required=True)
    text_parser.add_argument("--end", type=int, required=True)
    args = parser.parse_args()
    try:
        if args.command == "hash":
            print(sha256_file(args.file))
        elif args.command == "text-hash":
            print(text_hash(args.file, args.start, args.end))
        elif args.command == "check":
            auditor = Auditor(args.manifest, args.ledger)
            report = auditor.run()
            if args.report:
                auditor.write_report(args.report, report)
            print(json.dumps(report, ensure_ascii=False, indent=2))
            raise SystemExit(0 if report["audit_pass"] and report["content_resolved"] else 2 if report["audit_pass"] else 1)
        else:
            manifest, ledger = load_json(args.manifest), load_json(args.ledger)
            if args.command == "snapshot":
                print(content_snapshot(args.manifest.resolve(), args.ledger.resolve(), manifest, ledger))
            elif args.command == "scope":
                print(json.dumps(expected_scope(manifest, ledger), ensure_ascii=False, indent=2))
            else:
                rounds = ledger["final_rounds"]
                if not rounds or rounds[-1]["id"] != args.round_id:
                    raise ValueError("only the last existing round can be sealed; author its complete record first")
                last = rounds[-1]
                if last.get("record_sha256") not in (None, ""):
                    raise ValueError("already sealed records cannot be resealed; append a genuinely new round")
                if "findings" not in last or "scope" not in last or "page_notes" not in last:
                    raise ValueError("seal-round never creates findings, observations, identities or scope")
                actual_snapshot = content_snapshot(args.manifest.resolve(), args.ledger.resolve(), manifest, ledger)
                if last.get("snapshot_sha256") != actual_snapshot:
                    raise ValueError("review's predeclared snapshot does not match current content; do not rebind an old review, start a new review")
                last["previous_round_sha256"] = rounds[-2]["record_sha256"] if len(rounds) > 1 else None
                last["record_sha256"] = round_hash(last)
                args.ledger.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                print(last["record_sha256"])
    except (OSError, ValueError, KeyError, UnicodeError, RuntimeError) as error:
        parser.exit(1, f"audit: {error}\n")


if __name__ == "__main__":
    main()
