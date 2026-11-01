"""Independent standard-library reconstruction of the frozen 41-row witness.

The original program is not imported.  This additionally checks a necessary
common-container condition that the original 4,064-column relaxation omits.
It does not search for strategies or certify any complete SPE.
"""
from fractions import Fraction as Q
from itertools import combinations_with_replacement
from math import comb
from pathlib import Path
import json

N, S = 6, 7
BETA = tuple(map(Q, ("1/21", "2/37", "1/16", "2/27", "1/11", "7/72")))
MASSES = {
    (1, 1, ()): Q(7017572, 321392367),
    (1, 1, (3,)): Q(3133900, 321392367),
    (0, 1, ()): Q(111186481, 214261578),
    (0, 1, (4,)): Q(2017043, 71420526),
    (1, 2, (2, 3)): Q(42350, 3967807),
    (1, 2, (1, 2, 3)): Q(387200, 35710263),
    (1, 2, (0, 1, 2, 3)): Q(3573215, 71420526),
    (1, 2, (0, 1, 2, 3, 4)): Q(8325175, 23806842),
}
PAIRS = list(combinations_with_replacement(range(S), 2))
LABELS = [f"M_{t}" for t in range(N)] + [f"L_{j}" for j in range(S)]
LABELS += [f"T_{j}_{k}" for j, k in PAIRS]


def coefficients(I, J):
    count = len(J)
    share = [Q(int(t in J), count) if count else Q() for t in range(N)]
    a = [share[t] - (Q(1, 6) if len(I) == 7 else
                     Q(1, 12) if len(I) == 1 else BETA[t])
         for t in range(N)]
    previous = len(J - {5})
    a += [share[5] - Q(int(j in I), previous + 1) for j in range(S)]
    early = len(J & set(range(4)))
    before_last = int(4 in J)
    for j, k in PAIRS:
        z = int(j in I) + int(k in I)
        compare = Q(z, early + z) if z else Q()
        a.append(share[4] + share[5]
                 + Q(before_last, (early + 1) * (early + 2)) - compare)
    return a


def main():
    assert sum(MASSES.values(), Q()) == 1
    assert min(MASSES.values()) > 0
    averages = [Q() for _ in LABELS]
    base, omit_base = Q(), [Q() for _ in range(S)]
    support, orbits = [], set()
    route = (0, 0, 0, 0, 1, 0)
    route_legal_count = 0
    literal_count = 0
    for im in range(1, 1 << S):
        I = {j for j in range(S) if im & (1 << j)}
        f = int(0 in I)
        for em in range(1 << (N - 1)):
            E = tuple(t for t in range(5) if em & (1 << t))
            J = set(E) | ({5} if f else set())
            key = f, len(I), E
            orbits.add(key)
            literal_count += 1
            route_legal = all(route[t] in I for t in J)
            route_legal_count += int(route_legal)
            mass = MASSES.get(key, Q())
            if not mass:
                continue
            weight = mass / comb(6, len(I) - f)
            assert weight > 0
            values = coefficients(I, J)
            averages = [x + weight * y for x, y in zip(averages, values)]
            h = int(bool(J))
            base += weight * (Q(h) - Q(1, 2))
            for omitted in range(S):
                covered = bool(I - {omitted})
                omit_base[omitted] += weight * (Q(h) - Q(int(covered), 2))
            support.append({"I": sorted(I), "J": sorted(J),
                            "weight": str(weight), "route_000010_legal": route_legal})
    assert literal_count == 4064 and len(orbits) == 416
    assert len(support) == 38
    assert sum((Q(c["weight"]) for c in support), Q()) == 1
    assert min(averages) == 0
    assert base == Q(-2027846, 107130789)
    assert omit_base[0] == Q(-12442, 3967807)
    containers = []
    for t in range(N):
        possible = set(range(S))
        for c in support:
            if t in c["J"]:
                possible &= set(c["I"])
        containers.append(sorted(possible))
    assert containers[4] == []
    private_columns = [c for c in support if len(c["I"]) == 1 and c["J"] == [4]]
    assert len(private_columns) == 6
    assert {Q(c["weight"]) for c in private_columns} == {Q(2017043, 428523156)}
    report = {
        "literal_columns": literal_count, "orbit_groups": len(orbits),
        "positive_literal_support": len(support),
        "total_mass": "1", "base_W_minus_U_over_2": str(base),
        "base_W_minus_six_maxima_union_over_2_by_omitted_label": list(map(str, omit_base)),
        "row_averages": dict(zip(LABELS, map(str, averages))),
        "possible_common_maximal_containers_by_actual_position": containers,
        "route_000010_legal_literal_domain_size": route_legal_count,
        "positive_support_columns_illegal_for_route_000010": sum(not c["route_000010_legal"] for c in support),
        "support": support,
        "scope": "41-row separation on the relaxed column domain; no realizable actual profile or full-history SPE",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
