#!/usr/bin/env python3
"""Compare the frozen independent 64-row mathematical table to its stored JSON.

This is a serialization/identity check, not a new full-matrix or optimization
audit. The original matrix/certificate validity has its own preserved checker.
"""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import argparse
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "actual_kronecker_square_independent_reconstruction.md"
CERT = HERE.parent / "actual-kronecker/evidence/certificates/unrelated_machines/actual_kronecker_square_independent_assignment.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def machine(token):
    assert re.fullmatch(r"[SR][01]{2}", token), token
    return (token[0], int(token[1]), int(token[2]))


def job(token):
    assert re.fullmatch(r"(?:f[01]|e[01]{3})", token), token
    return (token[0],) + tuple(int(v) for v in token[1:])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("Use a new output path")
    assert digest(SOURCE) == "d3c5084f2db5dc7130007f530cde2408f6541fe86ce15f6855fd8fa314fe72a7"
    assert digest(CERT) == "cc62a3c385008150e411590240c78ef8c6f6b182d7625552fc1523220ad0e9a3"
    assignment, loads, counts = {}, {}, Counter()
    for line in SOURCE.read_text().splitlines():
        if not re.match(r"^\| [SR][01]{2}×[SR][01]{2} \|", line):
            continue
        fields = [p.strip() for p in line.split("|")[1:-1]]
        assert len(fields) == 3
        left, right = fields[0].split("×")
        dest = (machine(left), machine(right))
        assert dest not in loads
        total = Fraction(0)
        for item in fields[1].split(", "):
            match = re.fullmatch(r"((?:f[01]|e[01]{3}))×((?:f[01]|e[01]{3})) \(([0-9/]+)\)", item)
            assert match, item
            j, k, value = match.groups()
            pair = (job(j), job(k))
            assert pair not in assignment
            p = Fraction(value)
            assignment[pair] = (dest, p)
            total += p
            counts[j[0] + k[0]] += 1
        assert total == Fraction(fields[2]) == 1
        loads[dest] = total
    cert = json.loads(CERT.read_text())
    from_json = {
        tuple(tuple(j) for j in row["job"]):
        (tuple(tuple(i) for i in row["machine"]), Fraction(row["p"]))
        for row in cert["assignment"]
    }
    json_loads = {tuple(tuple(i) for i in row["machine"]): Fraction(row["load"])
                  for row in cert["loads"]}
    assert len(assignment) == len(cert["assignment"]) == len(from_json) == 100
    assert len(loads) == len(cert["loads"]) == len(json_loads) == 64
    assert assignment == from_json
    assert loads == json_loads
    assert counts == {"ff": 4, "fe": 16, "ef": 16, "ee": 64}
    result = {
        "status": "exact_table_and_json_identity",
        "driver_sha256": digest(Path(__file__)),
        "source_sha256": digest(SOURCE),
        "certificate_sha256": digest(CERT),
        "machine_rows": len(loads),
        "actual_job_pairs": len(assignment),
        "job_type_counts": dict(sorted(counts.items())),
        "all_table_row_sums": "1",
        "destinations_processing_times_and_loads_equal": True,
        "scope": [
            "Read and parsed all 64 table rows and all 100 actual job-pair entries.",
            "Compared exact destinations, Fraction times and loads to the preserved original independent JSON.",
            "No search, optimizer, seed enumeration, full-edge generation, fourth-power run or old-script replay."
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as out:
        json.dump(result, out, ensure_ascii=False, indent=2)
        out.write("\n")
    print(json.dumps({"status": result["status"], "machine_rows": 64, "actual_job_pairs": 100}))


if __name__ == "__main__":
    main()
