#!/usr/bin/env python3
"""私有汇点高阶负相关：精确达到分布与逐状态阶乘矩证书。

Finite Fraction checks only. No optimizer, floating point, random seed, or
imports from the previous or independent audit. The manuscript proves the
all-parameter theorem. Run without arguments; JSON is written to stdout.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from pathlib import Path
import hashlib
import json
import platform


def bound(k, r, d, q):
    if not (2 <= k <= r and 1 <= d <= k and 1 <= q <= k):
        raise ValueError("require 2<=k<=r and 1<=d,q<=k")
    candidates = [F(1)] + [F(comb(k, s), r**(s-1)*comb(q, s))
                              for s in range(2, min(d, q)+1)]
    p = min(candidates)
    t = min(d, q)
    assert p == (F(1) if t == 1 else
                 min(F(1), F(comb(k, t), r**(t-1)*comb(q, t))))
    return p


def law(k, r, d, q):
    """Atoms are (B's home, per-group bit masks of tiny jobs sent to sink)."""
    p = bound(k, r, d, q)
    out = defaultdict(F)
    for size, mass in [(q, p), (1, 1-p)]:
        if not mass:
            continue
        a = k-size
        atom_mass = mass / (r*comb(k, size)*comb(r-1, a)*k**a)
        for h in range(r):
            others = [i for i in range(r) if i != h]
            for big in combinations(range(k), size):
                for groups in combinations(others, a):
                    for jobs in product(range(k), repeat=a):
                        masks = [0]*r
                        masks[h] = sum(1 << j for j in big)
                        for i, j in zip(groups, jobs):
                            masks[i] = 1 << j
                        out[(h, tuple(masks))] += atom_mass
    return dict(out)


def check_law(k, r, d, q):
    atoms = law(k, r, d, q)
    assert sum(atoms.values(), F()) == 1
    b = [F() for _ in range(r)]
    events = defaultdict(F)
    success = F()
    for (h, masks), mass in atoms.items():
        b[h] += mass
        ds = [mask.bit_count() for mask in masks]
        assert sum(ds) == k
        loads = [F(k-ds[i]+(k if i == h else 0), k) for i in range(r)]
        loads += [F(z, k) for z in ds]
        actual = max(loads)
        assert actual == 2-F(ds[h], k)
        if actual <= 2-F(q, k):
            success += mass
        for i, mask in enumerate(masks):
            present = [j for j in range(k) if mask & (1 << j)]
            for s in range(1, min(d, len(present))+1):
                for subset in combinations(present, s):
                    events[i, subset] += mass
    assert all(v == F(1, r) for v in b)
    for i in range(r):
        for s in range(1, d+1):
            for subset in combinations(range(k), s):
                v = events[i, subset]
                if s == 1:
                    assert v == F(1, r)
                else:
                    assert v <= F(1, r**s)
    assert success == bound(k, r, d, q)
    return {"k": k, "r": r, "d": d, "q": q,
            "atoms": len(atoms), "success": str(success)}


def check_pointwise(k, r):
    states = checks = 0
    for ds in product(range(k+1), repeat=r):
        # Only counts matter for the upper certificate; all labeled assignments
        # with these counts have exactly these loads and factorial moments.
        for h in range(r):
            states += 1
            for q in range(2, k+1):
                for s in range(2, q+1):
                    val = sum(comb(z, s) for z in ds if z >= s)
                    assert (ds[h] < q) or val >= comb(q, s)
                    checks += 1
    return {"k": k, "r": r, "count_states_with_B": states,
            "pointwise_checks": checks}


def main():
    for args in [(1, 2, 1, 1), (2, 1, 1, 1), (2, 2, 0, 1), (2, 2, 1, 3)]:
        try:
            bound(*args)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid parameters accepted")
    cases = [(k, r, d, q) for k, r in [(2, 2), (3, 3), (4, 4)]
             for d in range(1, k+1) for q in range(1, k+1)]
    cases += [(4, 6, 2, 2), (4, 6, 3, 3), (4, 6, 4, 4)]
    attained = [check_law(*x) for x in cases]
    certificates = [check_pointwise(k, r) for k, r in [(2, 2), (3, 3), (4, 4)]]
    # Independent inverse checks for exact rational budgets at larger sizes.
    large = []
    for k, q in [(8, 4), (20, 10), (50, 25), (100, 50)]:
        r = k*k
        p = bound(k, r, k, q)
        assert p*r**(q-1) == comb(k, q)
        assert p <= F(2**k, k**(2*q-2))
        large.append({"k": k, "q": q, "p": str(p)})
    print(json.dumps({"arithmetic": "Fraction and integers; no numerical error",
        "seed": None, "python": platform.python_version(),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "attaining_laws": attained, "pointwise_certificates": certificates,
        "larger_formula_inverse_checks": large,
        "limits": "Finite laws/count states only; not a general proof or solver."},
        ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
