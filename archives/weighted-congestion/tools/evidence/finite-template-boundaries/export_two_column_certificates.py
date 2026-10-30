#!/usr/bin/env python3
"""Export the audit's deterministic 819-certificate stream without editing it.

This reuses the preserved audit's two solvers; it is not an independent solver.
The original report stores only this stream's canonical SHA256.  The complete
stream is emitted here, with that same digest and exact certificate checks.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
root = Path(__file__).resolve().parent
source = root / "original/tests/audits/weighted_congestion/template_certificates/independent_two_column_alternative.py"
frozen_path = root / "original/evidence/runs/weighted_congestion/template_certificates/independent_two_column_alternative.json"
spec = importlib.util.spec_from_file_location("preserved_two_column_audit", source)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
frozen = json.loads(frozen_path.read_text())
records = []
counts = {"primal": 0, "dual": 0, "dual_all_columns_equal_zero": 0}
for row_count in (1, 2, 3):
    for entries in product(map(Q, (-1, 0, 1)), repeat=2 * row_count):
        matrix = tuple(entries[2 * i:2 * i + 2] for i in range(row_count))
        primal = audit.primal_two_columns(matrix)
        dual = audit.dual_vertex(matrix)
        assert (primal is None) != (dual is None)
        if primal is not None:
            kind, certificate = "primal", primal
            assert all(a >= 0 for a in primal) and sum(primal) == 1
            assert all(sum(a * b for a, b in zip(primal, row)) > 0 for row in matrix)
        else:
            kind, certificate = "dual", dual
            assert all(a >= 0 for a in dual) and sum(dual) == 1
            values = tuple(sum(dual[i] * matrix[i][j] for i in range(row_count)) for j in range(2))
            assert all(a <= 0 for a in values)
            counts["dual_all_columns_equal_zero"] += all(a == 0 for a in values)
        counts[kind] += 1
        records.append({"matrix": [[str(a) for a in row] for row in matrix],
                        "kind": kind, "certificate": list(map(str, certificate))})
canonical = json.dumps(records, sort_keys=True, separators=(",", ":"))
digest = hashlib.sha256(canonical.encode()).hexdigest()
assert len(records) == frozen["matrices_exactly_checked"] == 819
assert counts == frozen["counts"]
assert digest == frozen["ordered_certificate_stream_sha256"]
print(json.dumps({
    "scope": "Full deterministic certificate export using preserved audit functions; not an independent solver or a general proof",
    "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    "exporter_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "matrices_exactly_checked": len(records), "counts": counts,
    "ordered_certificate_stream_sha256": digest, "matches_frozen_stream_digest": True,
    "records": records,
}, ensure_ascii=False, indent=2))
