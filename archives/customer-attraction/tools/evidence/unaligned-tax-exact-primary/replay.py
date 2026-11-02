"""Replay the frozen rational recovery once, then check four tax cuts directly.

The original recovery runs on a disposable copy; frozen inputs are never changed.
This is a fixed 64-column calculation, not an SPE solver or LP optimization.
"""
from __future__ import annotations

import argparse
import contextlib
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import io
from itertools import product
import json
from pathlib import Path
import platform
import runpy
import shutil
import sys
import tempfile
import time

BASE = Path(__file__).resolve().parent
REL = Path("research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_credible")


def quotient(n, d):
    return F(n, d) if n else F(0)


def direct_group(atom, tag):
    """Per-customer H,D1,D2 from the actual last-two continuation definitions."""
    bits = dict(zip("ABCDEUVWXY", map(int, atom["bits"])))
    if tag in ("AB", "AE"):
        histogram = atom[tag + "_hist"]
        cells = product((0, 1), repeat=3)
        prefix = bits["A"] + bits["B" if tag == "AB" else "E"]
    else:
        histogram = atom["second_hist"]
        cells = product((0, 1), repeat=4)
        prefix = bits["A"]
    H = D1 = D2 = F(0)
    for multiplicity, cell in zip(histogram, cells):
        background = prefix + sum(cell[:-2])
        earlier, last = cell[-2:]
        H += multiplicity * (quotient(earlier + last, background + earlier + last)
                             + F(earlier, (background + 1) * (background + 2)))
        D1 += F(multiplicity, background + 1)
        D2 += F(multiplicity, background + 2)
    return H, D1, D2


def direct_menu_pair(atom, family):
    key, arity = ("AE_hist", 3) if family == "AE" else ("second_hist", 4)
    count_left = count_right = intersection = 0
    for multiplicity, cell in zip(atom[key], product((0, 1), repeat=arity)):
        left, right = cell[-2:]
        count_left += multiplicity * left
        count_right += multiplicity * right
        intersection += multiplicity * left * right
    return count_left, count_right, intersection


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=BASE / "replay-output")
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((BASE / "manifest.json").read_text())
    for item in manifest:
        raw = (BASE / "original" / item["path"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == item["sha256"]
        assert len(raw) == item["size"]

    original_stdout, original_stderr = io.StringIO(), io.StringIO()
    started = datetime.now(timezone.utc).isoformat()
    start = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="recovery-", dir=out) as temporary:
        runtime = Path(temporary) / "source"
        shutil.copytree(BASE / "original", runtime)
        script = runtime / REL / "recover_unaligned.py"
        sys.path.insert(0, str(script.parent))
        try:
            with contextlib.redirect_stdout(original_stdout), contextlib.redirect_stderr(original_stderr):
                namespace = runpy.run_path(str(script), run_name="__main__")
        finally:
            sys.path.pop(0)
        elapsed = time.perf_counter() - start
        actual = script.with_name("unaligned_exact_obstruction.json").read_bytes()
        frozen = (BASE / "original" / REL / "unaligned_exact_obstruction.json").read_bytes()
        assert actual == frozen
        (out / "recovered.json").write_bytes(actual)

    atoms, masses = namespace["atoms"], namespace["r"]
    cuts = [
        ("AB", "Sbranch", "Sbranch:V|Sbranch:W"),
        ("AE", "AE", "AE:X|AE:Y"),
        ("AE", "Sbranch", "Sbranch:V|Sbranch:W"),
        ("Sbranch", "Sbranch", "Sbranch:V|Sbranch:W"),
    ]
    direct = {}
    for group, family, label in cuts:
        name = group + ":align-tax:" + label
        coefficients = []
        for atom in atoms:
            H, D1, D2 = direct_group(atom, group)
            left, right, dot = direct_menu_pair(atom, family)
            coefficients.append(5 * H - (left + right) * D1 + 2 * dot * (D1 - D2))
        value = sum((mass * coefficient for mass, coefficient in zip(masses, coefficients)), F(0))
        assert value == namespace["extra"][name] < 0
        direct[name] = {"value": str(value), "coefficients_in_original_atom_order": list(map(str, coefficients))}

    slacks = namespace["slack"]
    record = {
        "scope": "fixed frozen 64-column necessary-condition point, not a complete SPE",
        "started_utc": started,
        "python": platform.python_version(),
        "original_recover_executions": 1,
        "original_lp_executions": 0,
        "original_global_audit_executions": 0,
        "recovery_seconds": elapsed,
        "recovered_bytes_equal_frozen": True,
        "recovered_sha256": hashlib.sha256(actual).hexdigest(),
        "rows": len(slacks),
        "zero_rows": sum(value == 0 for value in slacks.values()),
        "positive_rows": sum(value > 0 for value in slacks.values()),
        "negative_rows": sum(value < 0 for value in slacks.values()),
        "selected_support_indices": namespace["S"],
        "active_row_candidates": len(namespace["active"]),
        "rational_basis_rank": len(namespace["basis"]),
        "normalization": str(sum(w * mass for w, mass in zip(namespace["w"], masses))),
        "objective": str(namespace["value"]),
        "all_1920_slacks": {name: str(value) for name, value in slacks.items()},
        "all_276_aligned_or_offdiagonal_tax_slacks": {name: str(value) for name, value in namespace["extra"].items()},
        "direct_four_cuts": direct,
        "limits": [
            "Same source implementation replays recovery; only the four cut coefficients are reconstructed separately.",
            "No LP optimizer, full-type pricing, equilibrium reconstruction, or random search is run.",
            "The four negative valid tax rows forbid every completion preserving these recorded coordinates and masses.",
        ],
    }
    (out / "stdout.txt").write_text(original_stdout.getvalue())
    (out / "stderr.txt").write_text(original_stderr.getvalue())
    (out / "audit.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: record[key] for key in (
        "rows", "zero_rows", "positive_rows", "negative_rows", "active_row_candidates",
        "rational_basis_rank", "normalization", "objective", "recovery_seconds", "recovered_bytes_equal_frozen"
    )}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
