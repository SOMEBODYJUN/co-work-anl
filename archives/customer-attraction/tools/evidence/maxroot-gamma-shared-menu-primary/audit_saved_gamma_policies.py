"""Check the three stored Gamma2 policies directly from unit-customer payoffs.

This checks fixed inputs only. It does not import the original solver, search
for a strategy, certify arbitrary games, or prove the half-coverage theorem.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "source-root/research/workspaces/customer-attraction/R-bfbfe64dd5f94fa09d36b75198633f2b/five_only"


def check_file(name):
    path = SOURCE / name
    src = json.loads(path.read_text())
    themes = tuple(frozenset(t) for t in src["themes"])
    customers = set().union(*themes)
    m = 5
    actions = src.get("certificate", src)["actions"]
    sigma = {tuple(a["history"]): a["action"] for a in actions}
    assert len(sigma) == len(actions)
    expected = {h for d in range(m) for h in product(range(len(themes)), repeat=d)}
    assert set(sigma) == expected
    assert all(type(t) is int and 0 <= t < len(themes) for t in sigma.values())

    def finish(h):
        while len(h) < m:
            h += (sigma[h],)
        return h

    def loads(z):
        return {x: sum(x in themes[t] for t in z) for x in customers}

    def payoff(z, position):
        n = loads(z)
        return sum((F(1, n[x]) for x in themes[z[position]]), F())

    nonself = self_comparisons = 0
    gaps = []
    for h in sorted(expected, key=lambda h: (len(h), h)):
        v = payoff(finish(h), len(h))
        for t in range(len(themes)):
            difference = v - payoff(finish(h + (t,)), len(h))
            assert difference >= 0, (name, h, t, difference)
            gaps.append(difference)
            if t == sigma[h]:
                self_comparisons += 1
                assert difference == 0
            else:
                nonself += 1
    actual = finish(())
    stored_path = tuple(src.get("path", src.get("actual")))
    assert actual == stored_path
    payoffs = [payoff(actual, i) for i in range(m)]
    assert payoffs == [F(v) for v in src["payoffs"]]
    actual_loads = loads(actual)
    harmonic = lambda n: sum((F(1, k) for k in range(1, n + 1)), F())
    phi = lambda z: sum((harmonic(v) for v in loads(z).values()), F())
    tails = []
    for a, b in combinations_with_replacement(range(len(themes)), 2):
        tails.append({"tail": [a, b], "potential": str(phi(actual[:3] + (a, b)))})
    gamma = max(F(r["potential"]) for r in tails) - phi(actual)
    gap = sum(payoffs[:3]) + gamma - 3 * payoffs[4]
    assert gamma == F(src["Gamma2"]) and gap == F(src["gap"])
    welfare = sum(n > 0 for n in actual_loads.values())
    optimum = max(len(set().union(*(themes[t] for t in z)))
                  for z in combinations_with_replacement(range(len(themes)), m))
    if "W" in src:
        assert welfare == src["W"] and optimum == src["OPT5"]
    if "certificate" in src:
        assert [actual.count(t) for t in range(len(themes))] == src["certificate"]["terminal_counts"]
    if "verification" in src:
        assert src["verification"] == {"valid": True, "histories": len(sigma), "deviations": nonself}
    if "full_checked_histories" in src:
        assert src["full_checked_histories"] == len(sigma)
        assert src["full_checked_deviations"] == nonself
    if "complete_histories" in src:
        assert src["complete_histories"] == len(sigma)
        assert src["all_action_comparisons"] == nonself + self_comparisons
        by_count = {}
        for h, t in sigma.items():
            key = (len(h), h.count(0))
            assert by_count.get(key, t) == t
            by_count[key] = t
        assert {str(d): [by_count[d, k] for k in range(d + 1)] for d in range(m)} == src["policy_by_depth_and_previous_zero_count"]
    summary = {
        "source": name, "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "histories": len(sigma), "nonself_comparisons": nonself,
        "self_comparisons": self_comparisons, "minimum_gap": str(min(gaps)),
        "actual": actual, "payoffs": list(map(str, payoffs)),
        "actual_potential": str(phi(actual)), "two_slot_potentials": tails,
        "Gamma2": str(gamma), "helper_gap": str(gap), "W": welfare, "OPT5": optimum,
    }
    return summary, sigma


def main():
    names = ["attack_two_tail_gamma.json", "two_singletons_gamma_counterexample.json", "audit_two_singletons_gamma.json"]
    results = [check_file(n) for n in names]
    left, right = results[1][1], results[2][1]
    differences = [{"history": h, "canonical": left[h], "independent": right[h]}
                   for h in sorted(left, key=lambda h: (len(h), h)) if left[h] != right[h]]
    report = {"status": "passed", "scope": __doc__, "policies": [r[0] for r in results],
              "two_singleton_policy_difference_count": len(differences), "policy_differences": differences,
              "all_action_comparisons": sum(r[0]["nonself_comparisons"] + r[0]["self_comparisons"] for r in results)}
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
