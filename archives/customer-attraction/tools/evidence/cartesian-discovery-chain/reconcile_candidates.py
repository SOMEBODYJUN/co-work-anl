"""Exact fixed-data reconciliation; no stochastic discovery loop is rerun."""
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def payoff(weights, profile, i):
    total = F(0)
    for component in range(2):
        actions = [a//3 if component == 0 else a%3 for a in profile]
        for mask, w in enumerate(weights[component*7:(component+1)*7], 1):
            if mask >> actions[i] & 1:
                total += F(w, sum(mask >> a & 1 for a in actions))
    return total


def coverage(weights, profile):
    return sum(w for component in range(2)
               for mask, w in enumerate(weights[component*7:(component+1)*7], 1)
               if any(mask >> (a//3 if component == 0 else a%3) & 1 for a in profile))


def analytic(h):
    if not h:
        return 0
    i, c = divmod(h[0], 2)
    if len(h) == 1:
        return 2*i+1-c
    j, d = divmod(h[1], 2)
    k = min(set(range(3))-{i, j})
    colour = 1-c if c == d else c if i == j else d
    return 2*k+colour


def main():
    original = HERE/"original"
    summaries = {}
    for name in ["cartesian_best.json", "cartesian_n5_best.json"]:
        a = json.loads((original/name).read_text())
        z = tuple(a["target"])
        assert len(a["weights"]) == 14 and len(z) == a["n"]
        W = coverage(a["weights"], z)
        assert W == a["W"]
        profiles = list(combinations_with_replacement(range(9), a["n"]))
        pair = a["pair"]
        paired_profile = profiles[pair[3]]
        b, d = pair[1:3]
        assert paired_profile.count(b) >= 1+int(b == d)
        assert paired_profile.count(d) >= 1
        first = paired_profile.index(b)
        second = next(i for i, x in enumerate(paired_profile) if x == d and i != first)
        paired_value = payoff(a["weights"], paired_profile, first)+payoff(a["weights"], paired_profile, second)
        assert abs(float(paired_value)-pair[0]) < 1e-12
        summaries[name] = {"clients": sum(a["weights"]), "target": z, "target_exact_coverage": W,
                           "pair_terminal_index": pair[3], "pair_terminal": paired_profile,
                           "pair_labels": [b, d], "pair_exact_payoff_sum": str(paired_value),
                           "scope": "Exact input/profile arithmetic only; no independent SPE or LP certification for the numerical search checkpoint."}

    a = json.loads((original/"simple_cartesian_q1.json").read_text())
    game, cert = a["instance"], a["certificate"]
    units = [frozenset(r["topics"]) for r in game["customers"] for _ in range(r["multiplicity"])]
    histories = [h for depth in range(3) for h in product(range(6), repeat=depth)]
    policy = {tuple(r["history"]): r["action"] for r in cert["actions"]}
    assert len(policy) == len(cert["actions"]) == 43 and set(policy) == set(histories)

    def leaf(h):
        while len(h) < 3:
            h += (policy[h],)
        return h

    def own(z, i):
        return sum((F(1, sum(b in T for b in z)) for T in units if z[i] in T), F(0))

    def W(z):
        return sum(any(b in T for b in z) for T in units)

    slacks = []
    for h in histories:
        for d in range(6):
            gap = own(leaf(h), len(h))-own(leaf(h+(d,)), len(h))
            assert gap >= 0
            slacks.append(gap)
    z = leaf(())
    assert z == (5, 4, 3) and [z.count(i) for i in range(6)] == cert["terminal_counts"]
    assert [own(z, i) for i in range(3)] == [F(1), F(3, 2), F(3, 2)]
    O = max(W(z) for z in product(range(6), repeat=3))
    assert (len(units), W(z), O) == (5, 4, 5)
    mismatches = []
    for h in histories:
        translated = tuple(5-x for x in h)
        if 5-policy[h] != analytic(translated):
            mismatches.append({"history": h, "translated": translated})
    summaries["simple_cartesian_q1.json"] = {
        "all_histories": 43, "all_comparisons_including_self": len(slacks),
        "strict": sum(g > 0 for g in slacks), "ties": sum(g == 0 for g in slacks),
        "actual": z, "utilities": [str(own(z, i)) for i in range(3)], "W": W(z), "OPT": O,
        "relabel_s_to_5_minus_s_matches_analytic_strategy": not mismatches,
        "relabel_mismatches": mismatches,
        "scope": "Direct unit-customer full ordered-history validation of the preserved five-customer certificate."}
    fixed = json.loads((HERE/"replay-fixed51/exact_cartesian_candidate.json").read_text())
    assert [r["W"] for r in fixed] == [27, 24, 49]
    assert [r["OPT"] for r in fixed] == [27, 24, 51]
    summaries["fixed51_exact_replay"] = [{"index": r["index"], "W": r["W"], "OPT": r["OPT"],
                                           "root_outcome_count": len(r["outcomes"]),
                                           "complete_policy_rows": len(r["certificate"]["actions"]),
                                           "verification": r["verification"]} for r in fixed]
    print(json.dumps(summaries, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
