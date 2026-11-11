"""Finish the frozen runtime using the current manifest's actual schema.

The archived materializer was run first. Its base materializer successfully
copied and SHA-checked 47 dependencies, then the overlay failed with
KeyError('stored_path'). This adapter records that mismatch and independently
checks all 47 copied dependencies before overlaying the 8 manifest entries.
No source archive or repository-control file is changed.
"""
from pathlib import Path
from hashlib import sha256
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
DEST = HERE / "runtime"
BASE = REPO / "archives/customer-attraction/tools/evidence/combined-branch-master-program"
PACK = REPO / "archives/customer-attraction/tools/evidence/b-family-menu-prices-boss3"
R2 = Path("research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_2")


def main():
    checked = []
    for rec in json.loads((BASE / "source-manifest.json").read_text())["frozen_sources"]:
        data = (DEST / rec["path"]).read_bytes()
        assert len(data) == rec["size"] and sha256(data).hexdigest() == rec["sha256"], rec["id"]
        checked.append({"id": rec["id"], "path": rec["path"], "sha256": rec["sha256"]})
    overlays = []
    for rec in json.loads((PACK / "source-manifest.json").read_text()):
        source = REPO / rec.get("local_original", rec.get("local_replay", ""))
        data = source.read_bytes()
        assert len(data) == rec["size"] and sha256(data).hexdigest() == rec["sha256"], rec["id"]
        relative = Path(rec["path"]) if "path" in rec else R2 / rec["basename"]
        target = DEST / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        overlays.append({"id": rec["id"], "source": str(source.relative_to(REPO)),
                         "destination": str(relative), "sha256": rec["sha256"], "size": len(data)})
    report = {"archived_materializer_result": "47 base files copied; overlay failed: KeyError('stored_path')",
              "manifest_schema": "8 entries; local_original or local_replay; path or basename",
              "adapter": str(Path(__file__).relative_to(REPO)),
              "base_verified_files": checked, "overlaid_files": overlays,
              "runtime": str(DEST), "status": "ready; no mathematical entrypoint executed"}
    (HERE / "materialization.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "base_files": len(checked), "overlays": len(overlays)}, indent=2))


if __name__ == "__main__":
    main()
