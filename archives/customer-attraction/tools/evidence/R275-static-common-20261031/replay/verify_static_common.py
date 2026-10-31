#!/usr/bin/env python3
"""Small deterministic value/structure checker for the saved static-common LP point.

This checker deliberately does not reconstruct the original floating Gamma rows:
the JSON stores only the chosen action at each history, while the source creates
the child-terminal terms from the random pre-LP point.  It therefore verifies
the serialized candidate, the exact objective value at its one-point support,
and the deterministic full-driver replay separately.
"""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parents[1]
SOURCE = HERE / "source"

EXPECTED = {
    "static_common_attack.py": (1354, "d707d5d70afac70e96420f6a58c542bd285c6afed6ab84e14a2f06846247b9fd"),
    "static_common_best.json": (80604, "b7d4fb878fd95ea812cef1ffdd16bb11245ba87eeabb7af0307262868c222914"),
    "cone_floor_attack.py": (2986, "af4f1f7f4e65a9c27d6b433e24dd1e3ff2cd7819cfd09dc140a580833d85ddb0"),
    "floor_scan.py": (1817, "ba406363e5a12959096613530441ae171df58ca9cd18a182cfc49d5dd1dbc66d"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    file_checks = {}
    for name, (size, digest) in EXPECTED.items():
        path = SOURCE / name
        actual = sha256(path)
        ok = path.stat().st_size == size and actual == digest
        file_checks[name] = {
            "bytes": path.stat().st_size,
            "sha256": actual,
            "expected_bytes": size,
            "expected_sha256": digest,
            "ok": ok,
        }
        assert ok, file_checks[name]

    candidate = json.loads((SOURCE / "static_common_best.json").read_text())
    assert set(candidate) == {"p", "n", "weights", "target", "a", "slack", "policy"}
    p = int(candidate["p"])
    n = int(candidate["n"])
    target = tuple(int(x) for x in candidate["target"])
    weights = [Fraction(str(x)) for x in candidate["weights"]]
    assert (p, n) == (7, 5)
    assert len(weights) == (1 << p) - 1
    assert sum(target) == n
    assert candidate["a"] == 0

    nonzero = [(i + 1, value) for i, value in enumerate(weights) if value]
    assert nonzero == [(91, Fraction(1))]

    loads = []
    covered = []
    objective = []
    for mask in range(1, 1 << p):
        d = sum(target[a] for a in range(p) if mask & (1 << a))
        loads.append(d)
        covered.append(int(d > 0))
        if d:
            gc = Fraction(n, n + (n - 1) * d)
            ga = Fraction(n + 1, d + 1) if mask & (1 << candidate["a"]) else Fraction(0)
            objective.append(Fraction(1) + gc - ga)
        else:
            objective.append(Fraction(0) - (Fraction(n) if mask & (1 << candidate["a"]) else Fraction(0)))

    normalization = sum(c * w for c, w in zip(covered, weights))
    exact_objective = sum(c * w for c, w in zip(objective, weights))
    assert normalization == 1
    assert exact_objective == Fraction(1, 5)
    assert abs(float(exact_objective) - float(candidate["slack"])) < 1e-15

    policy = candidate["policy"]
    expected_policy_len = sum(p**depth for depth in range(n))
    assert len(policy) == expected_policy_len == 2801
    histories = [tuple(int(x) for x in row["h"]) for row in policy]
    assert len(set(histories)) == len(histories)
    assert {len(h) for h in histories} == set(range(n))
    assert all(0 <= int(row["a"]) < p for row in policy)

    result = {
        "status": "PASS",
        "scope": "serialized candidate value/structure only; fixed floating cone, no universal SPE claim",
        "candidate": {
            "p": p,
            "n": n,
            "target": list(target),
            "a": int(candidate["a"]),
            "nonzero_weights": [{"mask": mask, "topics": [a for a in range(p) if mask & (1 << a)], "value": str(value)} for mask, value in nonzero],
            "normalization_exact": str(normalization),
            "objective_exact": str(exact_objective),
            "slack_float": candidate["slack"],
            "policy_history_count": len(policy),
            "policy_history_shape": {str(depth): sum(len(h) == depth for h in histories) for depth in range(n)},
        },
        "file_checks": file_checks,
        "reconstruction_limit": "policy stores chosen actions only; original random pre-LP point and child terminal terms are absent, so Gamma rows are not claimed reconstructed from JSON",
    }
    (Path(__file__).resolve().parent / "verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
