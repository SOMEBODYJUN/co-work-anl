"""Definition-level exact audit of frozen CCE benchmarks and shrinking records.

No author code, canonical model, optimizer, or first-batch audit is imported.
Complete ordered histories are kept in the independent outcome recursion.
"""
from fractions import Fraction as F
from functools import cache
from itertools import product, permutations
from math import comb, lcm
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
BASE = HERE / "source/research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c"


def model(m, k, weights):
    weights = {int(mask): F(v) for mask, v in weights.items()}

    @cache
    def utilities(z):
        out = [F(0)] * m
        for mask, mass in weights.items():
            selected = [i for i, a in enumerate(z) if mask & (1 << a)]
            for i in selected:
                out[i] += mass / len(selected)
        return tuple(out)

    def welfare(z):
        return sum((mass for mask, mass in weights.items()
                    if any(mask & (1 << a) for a in z)), F(0))

    def regret(z):
        w = welfare(z)
        return tuple(w - sum((utilities(z[:i] + (a,) + z[i + 1:])[i]
                              for i in range(m)), F(0)) for a in range(k))

    @cache
    def outcomes(h):
        if len(h) == m:
            return frozenset({h})
        i = len(h)
        children = [outcomes(h + (a,)) for a in range(k)]
        floor = max(min(utilities(z)[i] for z in child) for child in children)
        # Child strategies are independently selectable after distinct ordered
        # histories. This is the finite SPE recursion, not one Markov selector.
        return frozenset(z for child in children for z in child
                         if utilities(z)[i] >= floor)

    return utilities, welfare, regret, outcomes


def parse_instance(data):
    weights = {}
    for row in data["customers"]:
        mask = sum(1 << a for a in row["topics"])
        weights[mask] = weights.get(mask, 0) + row["multiplicity"]
    return data["players"], len(data["topics"]), weights


def certify_benchmark(raw, instance):
    m, k, weights = instance
    utilities, welfare, regret, outcomes = model(m, k, weights)
    gamma, lam = F(raw["value"]), tuple(map(F, raw["deviation_multipliers"]))
    assert gamma == F(raw["dual_value"]) and min(lam) >= 0
    mu = {}
    for q, p in raw["distribution"]:
        assert len(q) == k and sum(q) == m and min(q) >= 0
        p = F(p)
        assert p >= 0
        ordered = set(permutations(tuple(a for a, count in enumerate(q) for _ in range(count))))
        for z in ordered:
            mu[z] = mu.get(z, F(0)) + p / len(ordered)
    assert sum(mu.values()) == 1
    individual = [[sum((prob * (utilities(z)[i] - utilities(z[:i] + (a,) + z[i + 1:])[i])
                        for z, prob in mu.items()), F(0)) for a in range(k)] for i in range(m)]
    assert all(v >= 0 for row in individual for v in row)
    aggregate = [sum(individual[i][a] for i in range(m)) for a in range(k)]
    assert list(map(str, aggregate)) == raw["regret_slacks"]
    assert sum((p * welfare(z) for z, p in mu.items()), F(0)) == gamma
    dual_columns = {}
    for z in product(range(k), repeat=m):
        assert sum(utilities(z)) == welfare(z)
        d = welfare(z) - sum((a * b for a, b in zip(lam, regret(z))), F(0))
        assert d >= gamma
        dual_columns[tuple(z.count(a) for a in range(k))] = d
    min_slack = min(dual_columns.values()) - gamma
    assert str(min_slack) == raw["minimum_dual_slack"]
    assert len(dual_columns) == raw["profile_count"] == comb(m + k - 1, k - 1)
    root = outcomes(())
    minimum = min(welfare(z) for z in root)
    optimum = max(welfare(z) for z in product(range(k), repeat=m))
    assert minimum == raw["minimum_spe_welfare"]
    assert optimum == raw["optimum"]
    assert raw["exact_optimal"]
    return {"players": m, "topics": k, "unit_customer_count": str(sum(map(F, weights.values()))),
            "ordered_static_profile_count": k ** m, "count_profile_count": len(dual_columns),
            "ordered_CCE_support": [[list(z), str(p)] for z, p in sorted(mu.items())],
            "individual_CCE_slacks": [list(map(str, row)) for row in individual],
            "exact_minimum_CCE_welfare": str(gamma),
            "dual_columns": [[list(q), str(v)] for q, v in sorted(dual_columns.items())],
            "independent_full_ordered_recursion_minimum_SPE": str(minimum),
            "independent_OPT": str(optimum),
            "all_SPE_root_ordered_outcomes": [list(z) for z in sorted(root)],
            "minimum_CCE_minus_minimum_SPE": str(gamma - minimum)}


def certify_policy(raw):
    m, k = len(raw["path"]), len(raw["lambda"])
    utilities, welfare, regret, outcomes = model(m, k, raw["weights"])
    rows = [(tuple(h), a) for h, a in raw["actions"]]
    actions = dict(rows)
    histories = [h for t in range(m) for h in product(range(k), repeat=t)]
    assert set(actions) == set(histories) and len(rows) == len(histories)
    assert all(0 <= a < k for a in actions.values())

    def terminal(h):
        while len(h) < m:
            h += (actions[h],)
        return h

    slacks = []
    table = []
    for h in histories:
        i = len(h)
        own = utilities(terminal(h))[i]
        values = [utilities(terminal(h + (a,)))[i] for a in range(k)]
        slacks.extend(own - v for v in values)
        table.append({"history": list(h), "action": actions[h], "utilities": list(map(str, values))})
    assert min(slacks) >= 0 and str(min(slacks)) == raw["min_SPE_slack"]
    path = terminal(())
    assert list(path) == raw["path"] and welfare(path) == F(raw["W"])
    lam = tuple(map(F, raw["lambda"]))
    assert min(lam) >= 0
    ds = [welfare(z) - sum((a * b for a, b in zip(lam, regret(z))), F(0))
          for z in product(range(k), repeat=m)]
    lower = min(ds)
    assert lower == F(raw["CCE_lower"])
    assert lower - welfare(path) == F(raw["gap"])
    assert raw["valid_strict_failure"] == (lower > welfare(path))
    # Reconstruct the two integerization denominators recorded in the small
    # certificate, on every nonempty unit-customer incidence type.
    spe_den, static_den = 1, 1
    if "constraint_scales" in raw:
        for mask in range(1, 1 << k):
            u1, w1, g1, _ = model(m, k, {mask: 1})
            for h in histories:
                for a in range(k):
                    value = u1(terminal(h))[len(h)] - u1(terminal(h + (a,)))[len(h)]
                    spe_den = lcm(spe_den, value.denominator)
            for z in product(range(k), repeat=m):
                coefficient = w1(z) - sum((a * b for a, b in zip(lam, g1(z))), F(0)) - w1(path)
                static_den = lcm(static_den, coefficient.denominator)
        assert [spe_den, static_den] == raw["constraint_scales"]
        assert sum(F(v) for v in raw["weights"].values()) == raw["total_clients"]
    return {"unit_customer_count": str(sum(F(v) for v in raw["weights"].values())),
            "history_count": len(histories), "SPE_comparison_count_including_chosen": len(slacks),
            "minimum_SPE_slack": str(min(slacks)), "path": list(path),
            "payoffs": list(map(str, utilities(path))), "W": str(welfare(path)),
            "certified_CCE_lower": str(lower), "gap": str(lower - welfare(path)),
            "OPT": str(max(welfare(z) for z in product(range(k), repeat=m))),
            "checked_constraint_scales": [spe_den, static_den] if "constraint_scales" in raw else None,
            "SPE_table": table}


def main():
    for row in json.loads((HERE / "source-manifest.json").read_text()):
        p = HERE / row["local_path"]
        assert p.stat().st_size == row["bytes"]
        assert hashlib.sha256(p.read_bytes()).hexdigest() == row["sha256"]
    frozen = json.loads((BASE / "continuation_cce/benchmark_regression.json").read_text())
    pne = json.loads((HERE / "source/examples/customer_attraction/worst_pne_welfare_failure.json").read_text())
    strong = json.loads((BASE / "dynamic_security/strong_iid_472_five_topics.json").read_text())
    instances = {"pne_failure": parse_instance(pne),
                 "strong_iid": (3, 5, strong["weights"]),
                 "zero": (3, 2, {}), "single_player": (1, 2, {1: 1, 2: 2}),
                 "duplicate_empty": (3, 3, {6: 1})}
    out = {"author_or_canonical_code_imported": False,
           "benchmarks": {name: certify_benchmark(raw, instances[name]) for name, raw in frozen.items()},
           "shrinking_certificates": {}}
    for filename in ["cce_failure_candidate.json", "cce_failure_small.json"]:
        out["shrinking_certificates"][filename] = certify_policy(json.loads((BASE / "continuation_cce" / filename).read_text()))
    small_bench = json.loads((BASE / "continuation_cce/cce_failure_small_benchmark.json").read_text())
    out["thirteen_customer_alternative_primal"] = certify_benchmark(small_bench, parse_instance(small_bench["instance"]))
    initial = json.loads((HERE / "comparison/alternating_cone_result.json").read_text())
    initial_actions = {tuple(h): a for h, a in initial["strong_iid_policy"]["trace"][0]["rational"]["actions"]}
    assert all({tuple(h): a for h, a in json.loads((BASE / "continuation_cce" / filename).read_text())["actions"]} == initial_actions
               for filename in ["cce_failure_candidate.json", "cce_failure_small.json"])
    out["all_three_discovery_and_shrinking_policies_identical"] = True
    probe_replay = json.loads((HERE / "probe-replay.json").read_text())
    cone_replay = json.loads((HERE / "cone-replay.json").read_text())
    assert probe_replay == frozen
    assert cone_replay == initial
    out["seed_policy_checks"] = {}
    for name, actions, weights, path in [
        ("strong_iid", strong["actions"], strong["weights"], strong["path"]),
        ("pne_failure", cone_replay["pne_policy"]["trace"][0]["rational"]["actions"],
         {str(mask): count for mask, count in parse_instance(pne)[2].items()}, [0, 3, 3]),
    ]:
        benchmark = frozen[name]
        minimum = F(benchmark["minimum_spe_welfare"])
        lower = F(benchmark["value"])
        raw = {"actions": actions, "weights": weights, "path": path,
               "W": str(minimum), "lambda": benchmark["deviation_multipliers"],
               "CCE_lower": str(lower), "gap": str(lower - minimum),
               "min_SPE_slack": "0", "valid_strict_failure": False}
        out["seed_policy_checks"][name] = certify_policy(raw)
    out["author_probe_full_replay_structurally_equal_to_frozen"] = True
    out["author_cone_full_replay_structurally_equal_to_frozen"] = True
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
