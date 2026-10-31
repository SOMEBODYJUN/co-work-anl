"""Definition-level exact audit of the general predictable activation lemma.

One fixed branching/merging query DAG; no game/SPE search or scope inference.
Run from any cwd.  The output is frozen with exclusive create.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
from math import comb


def clean(a):
    a = list(a)
    while len(a) > 1 and not a[-1]:
        a.pop()
    return tuple(a)


def add(a, b):
    c = [F(0)] * max(len(a), len(b))
    for k, v in enumerate(a):
        c[k] += v
    for k, v in enumerate(b):
        c[k] += v
    return clean(c)


def mul(a, b):
    c = [F(0)] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            c[i + j] += u * v
    return clean(c)


def one_minus(n):
    return tuple(F((-1) ** k * comb(n, k)) for k in range(n + 1))


def bernoulli_word(n, active):
    return (F(0),) * active + one_minus(n - active)


def divide_p(a):
    assert not a[0]
    return clean(a[1:] or (F(0),))


def integral(a):
    return sum((v / (k + 1) for k, v in enumerate(a)), F(0))


P = (F(0), F(1))
ZERO = (F(0),)
ONE = (F(1),)
M = 6
DAG = {
    (0, "a"): ((1, "b"), (3, "a"), (5, "b")),
    (1, "b"): ((2, "a"), (3, "b"), (4, "a")),
    (2, "a"): ((3, "a"), (5, "a")),
    (3, "a"): ((4, "b"), (5, "a")),
    (3, "b"): ((4, "a"), (5, "b")),
    (4, "a"): ((5, "a"),),
    (4, "b"): (),
    (5, "a"): (),
    (5, "b"): (),
}
assert all(j[0] > s[0] for s, js in DAG.items() for j in js)
assert all(tuple(sorted(js)) == js for js in DAG.values())
reports = []
state_checks = 0
role_checks = 0
for source in DAG:
    owner = source[0]
    entered = defaultdict(lambda: ZERO)
    absorbed = defaultdict(lambda: ZERO)
    for bits in product((0, 1), repeat=M):
        if not bits[owner]:
            continue
        weight = bernoulli_word(M, sum(bits))
        s = source
        while True:
            entered[s] = add(entered[s], weight)
            successors = [j for j in DAG[s] if bits[j[0]]]
            if not successors:
                absorbed[s] = add(absorbed[s], weight)
                break
            s = successors[0]

    q = defaultdict(lambda: ZERO)
    q[source] = ONE
    for s in sorted(DAG):
        for rank, target in enumerate(DAG[s]):
            transition = mul(P, one_minus(rank))
            q[target] = add(q[target], mul(q[s], transition))

    entry_mass = {}
    absorb_mass = {}
    total_absorb_poly = ZERO
    for s in DAG:
        direct_q = divide_p(entered[s])
        assert q[s] == direct_q, (source, s, "entry", q[s], direct_q)
        expected_absorb = mul(mul(P, q[s]), one_minus(len(DAG[s])))
        assert absorbed[s] == expected_absorb, (source, s, "absorb")
        total_absorb_poly = add(total_absorb_poly, absorbed[s])
        entry_mass[s] = integral(direct_q)
        absorb_mass[s] = integral(divide_p(absorbed[s]))
        c = len(DAG[s]) + 1
        if s == source:
            assert absorb_mass[s] == F(1, c)
        elif q[s] != ZERO:
            assert s[0] > owner
            assert absorb_mass[s] <= F(1, c * (c + 1))
        else:
            assert absorb_mass[s] == 0
        state_checks += 1
    assert total_absorb_poly == P
    assert sum(absorb_mass.values()) == 1
    for i in range(owner + 1, M):
        assert sum(v for s, v in entry_mass.items() if s[0] == i) <= F(1, 2)
        role_checks += 1
    reports.append({
        "source": list(source),
        "total_absorb": "1",
        "states": [
            {"state": list(s), "c": len(DAG[s]) + 1,
             "entry": str(entry_mass[s]), "absorb": str(absorb_mass[s])}
            for s in DAG if q[s] != ZERO
        ],
    })

report = {
    "status": "passed",
    "scope": "one definition-level DAG with branch/merge and all state sources; no SPE scan",
    "activation_vectors_per_source": 2 ** M,
    "sources": len(DAG),
    "state_polynomial_checks": state_checks,
    "role_entry_checks": role_checks,
    "reports": reports,
}
out = Path(__file__).with_name("predictable_activation_audit.json")
with out.open("x", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(json.dumps({k: v for k, v in report.items() if k != "reports"}, ensure_ascii=False))
