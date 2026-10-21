"""Independent literal-client audit; no repository solver or candidate verifier imports."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
SMALL = "--small" in sys.argv
TYPES = {2: 4, 4: 1, 8: 1, 13: 2} if SMALL else {2: 17, 4: 5, 7: 3, 8: 5, 11: 3, 13: 9}
# Every entry below denotes a separate unit-valued client.
CLIENTS = [frozenset(a for a in range(4) if mask & (1 << a))
           for mask, multiplicity in TYPES.items()
           for _ in range(multiplicity)]
SECOND = (1, 2, 1, 1)
THIRD = ((1, 1, 1, 1), (1, 2, 1, 2),
         (1, 3, 1, 1), (1, 2, 1, 1))


def action(h):
    if len(h) == 0:
        return 0
    if len(h) == 1:
        return SECOND[h[0]]
    if len(h) == 2:
        return THIRD[h[0]][h[1]]
    raise ValueError(h)


def continuation(h):
    h = tuple(h)
    while len(h) < 3:
        h += (action(h),)
    return h


def payoff(s, player):
    return sum((F(1, sum(a in c for a in s))
                for c in CLIENTS if s[player] in c), F(0))


def welfare(s):
    return sum(any(a in c for a in s) for c in CLIENTS)


def main():
    spe_rows = []
    for t in range(3):
        for h in product(range(4), repeat=t):
            selected = continuation(h)
            selected_u = payoff(selected, t)
            for alternative in range(4):
                changed = continuation(h + (alternative,))
                alternative_u = payoff(changed, t)
                assert selected_u >= alternative_u, (h, alternative)
                spe_rows.append({"history": h, "alternative": alternative,
                                 "margin": str(selected_u - alternative_u)})

    y = (F(0), F(9, 29), F(20, 87), F(20, 87)) if SMALL else (F(0), F(2, 7), F(1, 4), F(1, 4))
    bound = F(544, 87) if SMALL else F(33)
    simple_y = (F(0), F(1, 3), F(2, 9), F(2, 9)) if SMALL else y
    simple_bound = F(56, 9) if SMALL else bound
    dual_rows = []
    optimum = 0
    for s in product(range(4), repeat=3):
        w = welfare(s)
        optimum = max(optimum, w)
        assert sum(payoff(s, i) for i in range(3)) == w
        aggregate_gaps = []
        for alternative in range(4):
            changed_sum = F(0)
            for i in range(3):
                changed = s[:i] + (alternative,) + s[i+1:]
                changed_sum += payoff(changed, i)
            aggregate_gaps.append(F(w) - changed_sum)
        dual_value = F(w) - sum(ya * ga for ya, ga in zip(y, aggregate_gaps))
        assert dual_value >= bound, (s, dual_value)
        simple_dual_value = F(w) - sum(ya * ga for ya, ga in zip(simple_y, aggregate_gaps))
        assert simple_dual_value >= simple_bound, (s, simple_dual_value)
        dual_rows.append({"profile": s, "welfare": w,
                          "aggregate_gaps": list(map(str, aggregate_gaps)),
                          "dual_value": str(dual_value),
                          "simple_dual_value": str(simple_dual_value)})

    s = continuation(())
    report = {
        "audit_basis": "literal separate clients, all ordered histories and all ordered profiles",
        "clients": len(CLIENTS), "types": TYPES,
        "strategy": {"root": 0, "second": SECOND, "third": THIRD},
        "spe_comparisons": len(spe_rows),
        "minimum_spe_margin": str(min(F(r["margin"]) for r in spe_rows)),
        "actual_profile": s, "actual_payoffs": [str(payoff(s, i)) for i in range(3)],
        "actual_welfare": welfare(s), "optimum": optimum,
        "dual_coefficients": list(map(str, y)),
        "static_ordered_profiles": len(dual_rows),
        "minimum_dual_value": str(min(F(r["dual_value"]) for r in dual_rows)),
        "minimum_dual_profiles": [r["profile"] for r in dual_rows if F(r["dual_value"]) == bound],
        "simple_dual_coefficients": list(map(str, simple_y)),
        "minimum_simple_dual_value": str(min(F(r["simple_dual_value"]) for r in dual_rows)),
        "spe_rows": spe_rows, "dual_rows": dual_rows,
    }
    assert report["actual_welfare"] == (6 if SMALL else 32)
    assert report["actual_welfare"] < simple_bound <= bound
    if SMALL:
        from itertools import permutations
        count_masses = {(0, 1, 1): F(17, 87), (1, 1, 2): F(29, 87),
                        (1, 1, 3): F(29, 87), (2, 2, 2): F(6, 87),
                        (3, 3, 3): F(6, 87)}
        distribution = {}
        for profile, mass in count_masses.items():
            ordered = set(permutations(profile))
            for s in ordered:
                distribution[s] = mass / len(ordered)
        assert sum(distribution.values()) == 1
        cce_gaps = []
        for player in range(3):
            for alternative in range(4):
                gap = sum((mass * (payoff(s, player) - payoff(s[:player] + (alternative,) + s[player+1:], player))
                           for s, mass in distribution.items()), F(0))
                assert gap >= 0, (player, alternative, gap)
                cce_gaps.append({"player": player, "alternative": alternative, "gap": str(gap)})
        expected_welfare = sum((mass * welfare(s) for s, mass in distribution.items()), F(0))
        assert expected_welfare == bound
        report["sharp_primal_expected_welfare"] = str(expected_welfare)
        report["sharp_primal_individual_cce_constraints"] = cce_gaps
        report["sharp_primal_distribution"] = [{"profile": s, "probability": str(p)} for s, p in sorted(distribution.items())]
    filename = "independent_cce_eight_client_audit.json" if SMALL else "independent_cce_audit.json"
    (ROOT / filename).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k not in ("spe_rows", "dual_rows")}, indent=2))


if __name__ == "__main__":
    main()
