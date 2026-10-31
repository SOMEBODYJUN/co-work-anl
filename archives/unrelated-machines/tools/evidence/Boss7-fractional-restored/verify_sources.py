#!/usr/bin/env python3
"""Check restored source identities and exact arithmetic, not the NSW backend."""
from fractions import Fraction
import argparse
import gzip
import hashlib
import json
from pathlib import Path


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[5])
    args = parser.parse_args()
    repo = args.repo.resolve()
    evidence = Path(__file__).resolve().parent
    manifest = json.loads((evidence / "manifest.json").read_text())
    inventory = {
        row["id"]: row
        for row in map(json.loads, (repo / "cleanup/inventory.jsonl").read_text().splitlines())
    }
    source_results = []
    statements = {}
    for row in manifest["sources"]:
        original = repo / row["original_evidence"]
        raw = original.read_bytes()
        frozen = inventory[row["id"]]
        assert len(raw) == frozen["size"] == row["size"]
        assert sha(raw) == frozen["sha256"] == row["sha256"]
        decoded = gzip.decompress(raw) if original.suffix == ".gz" else raw
        assert sha(decoded) == row["decoded_sha256"]
        assert len(decoded) == row["decoded_bytes"]
        assert len(decoded.splitlines()) == row["decoded_lines"]
        assert (repo / row["decoded_evidence"]).read_bytes() == decoded
        if original.suffix == ".gz":
            statements[row["id"]] = decoded
        source_results.append({"id": row["id"], "original_sha256": sha(raw),
                               "decoded_sha256": sha(decoded), "passed": True})
    sections = []
    for data in statements.values():
        section = data[data.index(b"## A."):data.index(b"## B.")]
        assert len(section) == 3565
        assert sha(section) == "1c1250fb4e62c641d2bdc1d688d967cc5334e999ad61862a2641c1e3bd0f4828"
        sections.append(section)
    assert len(sections) == 2 and sections[0] == sections[1]
    assert sha((repo / manifest["diff"]["path"]).read_bytes()) == manifest["diff"]["sha256"]

    d = Fraction(5, 2)
    delta = 1 / (7 * d)
    assert delta == Fraction(2, 35)
    assert delta / 6 - Fraction(1, 210) == delta / 12 == Fraction(1, 210)
    assert 200 / delta**2 == 61250 == 9800 * d**2 < 10000 * d**2 == 62500
    assert 60000 * d**2 == 375000
    assert 60000 * 3 * d**2 == 1125000
    assert 2 * 1125000 == 2250000
    assert Fraction(3, 4) / 2250000 == Fraction(1, 3000000)
    assert Fraction(1, 3000000) > Fraction(1, 2**24)
    # e<3 is the analytic premise in the proof; this checks its integer slack.
    assert 12 * 9 == 108 < 200
    report = {"status": "PASS", "sources": source_results,
              "section_A_v4_v5_byte_identical": True,
              "exact_constant_arithmetic": True,
              "scope": "Byte identity, decompression, recorded full diff identity, exact rational arithmetic only. No NSW/LP/CDF/mask backend implementation or execution test."}
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
