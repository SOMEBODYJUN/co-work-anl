"""Verify grouped exact equilibrium spectra and all layouts in the mixing-cap family."""
from collections import Counter
from fractions import Fraction as F
from itertools import product

def instance(r):
    w, delta = F(2*r), F(1, 2)
    q = 1 - F(1, 2*r)
    return [
        ("AB", (w + delta - q) / 2),
        ("AB", (w + delta - q) / 2),
        ("AC", (w + delta + q) / 2),
        ("A", (w - delta + 3*q) / 2),
        ("B", 2*q),
        ("C", (w - delta + q) / 2),
    ] + [("BC", F(1))] * (2*r)

def group_options(n):
    for first in range(n + 1):
        for second in range(n - first + 1):
            yield first, second, n - first - second

def local_spectrum(clients, layout, cap):
    a, b = F(0), F(0)
    common = Counter()
    for allowed, w in clients:
        left, right = (site in allowed for site in layout)
        if left and right:
            common[w] += 1
        elif left:
            a += w
        elif right:
            b += w
    total = a + b + sum(w*n for w, n in common.items())
    weights = tuple(common)
    intervals = set()
    for counts in product(*(group_options(common[w]) for w in weights)):
        lo, hi, signed, m = -total, total, a-b, 0
        for w, (left, right, mix) in zip(weights, counts):
            if right or mix:
                lo = max(lo, -w)
            if left or mix:
                hi = min(hi, w)
            signed += w*(left-right)
            m += mix
        if lo > hi:
            continue
        if m == 1:
            if signed == 0 and cap >= 1:
                intervals.add((lo, hi))
            continue
        gap = signed / (1-m)
        if lo <= gap <= hi:
            actual = sum(mix for w, (_, _, mix) in zip(weights, counts) if abs(gap) < w)
            if actual <= cap:
                intervals.add((gap, gap))
    assert intervals
    return total, intervals

def whole_instance(clients, sites, cap):
    layouts = tuple(product(sites, repeat=2))
    local = {x: local_spectrum(clients, x, cap) for x in layouts}
    minima = {}
    for x, (total, intervals) in local.items():
        minima[x] = ((total+min(lo for lo, _ in intervals))/2,
                     (total-max(hi for _, hi in intervals))/2)
    alpha = {}
    for x, (total, intervals) in local.items():
        d1 = max(minima[r, x[1]][0] for r in sites if r != x[0])
        d2 = max(minima[x[0], r][1] for r in sites if r != x[1])
        target = total*(d1-d2)/(d1+d2) if d1+d2 else F(0)
        candidates = {min(hi, max(lo, target)) for lo, hi in intervals}
        feasible = []
        for gap in candidates:
            p1, p2 = (total+gap)/2, (total-gap)/2
            if (p1 or not d1) and (p2 or not d2):
                feasible.append(max(F(1), d1/p1 if p1 else 0, d2/p2 if p2 else 0))
        alpha[x] = min(feasible) if feasible else None
    return min(x for x in alpha.values() if x is not None), alpha, minima

counts = {"sizes": 0, "catalogue_cap_runs": 0, "labeled_layouts": 0}
for r in range(2, 9):
    clients = instance(r)
    q = 1 - F(1, 2*r)
    w, delta = F(2*r), F(1, 2)
    h, k = (3*w+delta+q)/2, (3*w+delta+3*q)/2
    s = F(1, 4*r*(r-1))
    for sites in (("ABC", "ABCDE") if r in (2, 5) else ("ABC",)):
        alpha_r, rows_r, minima_r = whole_instance(clients, sites, r)
        alpha_rp, rows_rp, minima_rp = whole_instance(clients, sites, r+1)
        assert alpha_r == rows_r["B", "C"] == k/(k-s)
        assert alpha_rp == rows_rp["A", "C"] == 1
        assert minima_r["B", "C"][0] == h+s and minima_rp["B", "C"][0] == h
        if len(sites) > 3:
            assert all(v is None for row,v in rows_r.items() if set(row)-set("ABC"))
        counts["catalogue_cap_runs"] += 2
        counts["labeled_layouts"] += 2*len(sites)**2
    counts["sizes"] += 1
print(counts)
