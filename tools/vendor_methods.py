#!/usr/bin/env python3
"""Fetch only pinned, licensed research references. Never executes upstream code."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "FRBNY-Nowcasting": ("FRBNY-TimeSeriesAnalysis/Nowcasting", "19f365cab8269e3aac3faa11ad091d6e913c5c43", "BSD-3-Clause", ["LICENSE", "README.md", "example_DFM.m", "example_Nowcast.m", "functions/update_nowcast.m"]),
    "TradingAgents": ("TauricResearch/TradingAgents", "121265d18d467ac717f7af99cb0d669c15d2e73c", "Apache-2.0", ["LICENSE", "specs/skills/macro-outlook/SKILL.md", "specs/skills/scenario-analysis/SKILL.md", "specs/skills/thesis-review/SKILL.md"]),
    "humanizer-chinese": ("jiji262/humanizer-chinese", "1d6c08e10fbfe0e1b36ac784834451c6aae0a92c", "MIT", ["LICENSE", "SKILL.md"]),
    "GMD-license": ("KMueller-Lab/Global-Macro-Database", "2930dade4a9afefee614eb79091b6de3d90933e3", "upstream-terms-read-before-data-distribution", ["LICENSE"]),
    "BoE-license": ("bank-of-england/MachineLearningCrisisPrediction", "282fcbf0111af169053118110b4031d16c64bd56", "GPL-3.0-or-later (code); JST data separate", ["licence.txt"]),
}


def fetch(entry):
    name, repo, commit, licence, relative = entry
    url = f"https://raw.githubusercontent.com/{repo}/{commit}/{relative}"
    with urllib.request.urlopen(url, timeout=45) as response:
        content = response.read()
    target = ROOT / "vendor" / name / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
    return {"path": str(target.relative_to(ROOT)), "source_url": url, "commit": commit,
            "license": licence, "sha256": hashlib.sha256(content).hexdigest(),
            "use": "reference-only; not executed as an upstream application"}


def main():
    entries = [(name, repo, commit, licence, f) for name, (repo, commit, licence, files) in PINS.items() for f in files]
    with ThreadPoolExecutor(max_workers=6) as executor:
        rows = list(executor.map(fetch, entries))
    path = ROOT / "vendor" / "manifest.json"
    existing = json.loads(path.read_text()) if path.exists() else []
    retained = [x for x in existing if not any(x["path"].startswith("vendor/" + name + "/") for name in PINS)]
    path.write_text(json.dumps(sorted(retained + rows, key=lambda x: x["path"]), ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"downloaded": len(rows), "manifest": str(path.relative_to(ROOT))}))


if __name__ == "__main__":
    main()
