#!/usr/bin/env python3
"""Small independent Fraction coefficient audit of the frozen discover module.

This is a coefficient/interface check, not a new SPE solver or theorem checker.
The original module is imported unmodified; only its output directory is set here.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import importlib.util
import json
import platform
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "original/fourcopy_discover.py"
spec = importlib.util.spec_from_file_location("frozen_fourcopy_discover", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def geometry(n, copies):
    # Allocate fresh labels using a separate list-oriented construction.
    paths = [list(range(n))]
    fresh = n
    for pos in range(1, copies + 1):
        branch = list(range(pos)) + [n - 1]
        for _ in range(n - pos - 1):
            branch.append(fresh)
            fresh += 1
        paths.append(branch)
    return paths, fresh


def exact_row(mask, n, paths, key):
    b = lambda j: (mask >> j) & 1

    def u(k, i):
        return Q(b(paths[k][i]), sum(b(t) for t in paths[k])) if b(paths[k][i]) else Q(0)

    z = key.split(":")
    if z[0] == "CAP":
        return Q(b(0) - b(int(z[1])))
    if z[0] == "COPY":
        i = int(z[1])
        return u(0, i) - u(i, i)
    if z[0] == "FLOOR":
        k, i, j = map(int, z[1:])
        p = sum(b(t) for t in paths[k][:i])
        return u(k, i) - Q(b(j), p + n - i)
    k = int(z[1])
    if z[0] == "PAIR":
        p = sum(b(t) for t in paths[k][:-2])
        tax = Q(b(paths[k][-2]), (p + 1) * (p + 2))
        return Q(n, 2) * (u(k, n - 2) + u(k, n - 1) + tax) + Q(p, p + 1)
    if z[0] == "LAST":
        p = sum(b(t) for t in paths[k][:-1])
        return n * u(k, n - 1) + Q(p, p + 1)
    raise ValueError(key)


def check_case(n, copies):
    bits, actual_paths, names, rows, ocoef, vT = module.build(n, copies)
    paths, d = geometry(n, copies)
    assert actual_paths == paths
    expected = [f"CAP:{j}" for j in range(1, d)]
    expected += [f"COPY:{i}" for i in range(1, copies + 1)]
    for k, path in enumerate(paths):
        first = 1 if k == 0 else k + 1
        expected += [f"FLOOR:{k}:{i}:{j}" for i in range(first, n) for j in range(d) if j != path[i]]
        expected += [f"PAIR:{k}", f"LAST:{k}"]
    assert names == expected
    assert rows.shape == (1 << d, len(names))
    max_error = 0.0
    for mask in range(1 << d):
        assert list(map(int, bits[mask])) == [(mask >> j) & 1 for j in range(d)]
        assert abs(vT[mask] - float(Q(1, sum((mask >> j) & 1 for j in paths[0])) if mask & 1 else Q(0))) < 1e-14
        for col, key in enumerate(names):
            err = abs(rows[mask, col] - float(exact_row(mask, n, paths, key)))
            max_error = max(max_error, err)
            assert err < 1e-14, (n, copies, mask, key, err)
            assert ocoef[col] == (-1 if key.startswith(("PAIR:", "LAST:")) else 0)
    return dict(n=n, copies=copies, paths=paths, bits=d, types=1 << d,
                rows=len(names), checked_coefficients=(1 << d) * len(names),
                maximum_float_difference=max_error,
                semantic_warning=[f"PAIR:{copies}"] if copies == n - 2 else [],
                note="All numeric coefficients match independently reconstructed Fraction rows; semantic warning is not certified as a true SPE row.")


def inspect_discovery(record):
    n, copies = record["n"], record["copies"]
    paths, d = geometry(n, copies)
    lam = {k: Q(v) for k, v in record["multipliers"].items()}
    opt_sum = sum((v for k, v in lam.items() if k.startswith(("PAIR:", "LAST:"))), Q(0))
    B, C = Q(record["B"]), Q(record["C"])
    residuals = []
    for mask in range(1 << d):
        v = Q(1, sum((mask >> j) & 1 for j in paths[0])) if mask & 1 else Q(0)
        residuals.append(B * v + C * (mask & 1) - sum((w * exact_row(mask, n, paths, k) for k, w in lam.items()), Q(0)))
    return dict(C=record["C"], B=record["B"], opt_multiplier_sum=str(opt_sum),
                exact_opt_normalization=(opt_sum == 1),
                minimum_exact_membership_residual=str(min(residuals)),
                membership_nonnegative=(min(residuals) >= 0),
                note="Inspection of separately rationalized float output, without recovery; this is not an accepted certificate.")


def main():
    import scipy
    import numpy
    cases = [check_case(n, c) for n, c in [(3, 0), (4, 1), (4, 2)]]
    module.HERE = HERE / "runs"
    records = module.run(4, 1, [0.0, 0.1])
    assert len(records) == 2
    report = dict(source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                  source_bytes=SOURCE.stat().st_size,
                  python=platform.python_version(), numpy=numpy.__version__, scipy=scipy.__version__,
                  coefficient_cases=cases,
                  coefficient_total=sum(c["checked_coefficients"] for c in cases),
                  original_api_invocations=1, original_lp_solves=2,
                  lp_parameters=dict(n=4, copies=1, C=[0.0, 0.1]),
                  discovery_inspection=[inspect_discovery(r) for r in records],
                  exclusions=["No n=6 LP solve", "No recovery or original verifier run", "No full SPE enumeration"])
    (HERE / "runs/small-audit.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
