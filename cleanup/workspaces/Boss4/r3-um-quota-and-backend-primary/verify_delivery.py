"""Check exact staged delivery, claim binding, receipts and local links."""
from pathlib import Path
import hashlib
import json
import re

WS = Path(__file__).resolve().parent
STAGE = WS.parents[3]
REPO = STAGE.parent.parent / "boss4-research"

def main():
    files = json.loads((WS / "copy-files.json").read_text())
    assert len(files) == len(set(files))
    assert set(files) == {str(p.relative_to(STAGE)) for p in STAGE.rglob("*") if p.is_file()}
    manifests = json.loads((WS / "delivery-manifest.json").read_text())
    for d in manifests["files"]:
        p = STAGE / d["path"]
        assert p.stat().st_size == d["size"]
        assert hashlib.sha256(p.read_bytes()).hexdigest() == d["sha256"]
    E = STAGE / "archives/unrelated-machines/tools/evidence/um-quota-and-backend-primary"
    claim = json.loads((E / "claim-receipt.json").read_text())
    assert claim["status"] == "pushed" and claim["actor"] == "Boss4"
    assert claim["remote_tip"] == "e0fe042553c1ef8df380c69f3085b2c02a9138ff"
    receipts = json.loads((WS / "semantic-receipts.json").read_text())
    assert len(receipts) == 5 and {d["id"] for d in receipts} == set(claim["ids"])
    for d in receipts:
        for k in ["full_file_reviewed", "related_material_checked", "unique_content_accounted_for"]:
            assert d[k] is True
        for k in ["read_note", "comparison_note", "decision_note"]:
            assert len(d[k]) > 40
        assert d["disposition"] == "integrated"
        assert d["targets"] and all((STAGE / target).is_file() for target in d["targets"])
    pages = list((STAGE / "archives/unrelated-machines/state/资源").glob("*.md"))
    assert len(pages) == 3
    link_count = 0
    for p in pages + [E / "README.md"]:
        text = p.read_text()
        assert text.startswith("---\n") or p.name == "README.md"
        assert text.count(r"\[") == text.count(r"\]")
        assert text.count(r"\(") == text.count(r"\)")
        assert not any(ord(c) < 32 and c not in "\n\t\r" for c in text)
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            if "://" in target or target.startswith("#"):
                continue
            resolved = (p.parent / target.split("#")[0]).resolve()
            relative = resolved.relative_to(STAGE)
            assert resolved.exists() or (REPO / relative).exists(), (p, target)
            link_count += 1
    result = json.loads((E / "data-selfcheck.json").read_text())
    assert result["status"] == "passed" and result["original_program_new_runs"] == 0
    assert manifests["original_program_new_runs"] == 0
    print(json.dumps({
        "status": "passed", "exact_files": len(files), "primary_receipts": len(receipts),
        "formal_objects": len(pages), "local_links_checked": link_count,
        "copied_bytes": sum((STAGE / p).stat().st_size for p in files),
        "original_program_new_runs": 0
    }, ensure_ascii=False))

if __name__ == "__main__":
    main()
