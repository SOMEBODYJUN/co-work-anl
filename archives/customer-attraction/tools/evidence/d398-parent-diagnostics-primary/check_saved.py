"""Bind and check saved root-only certificates and seven fixed insurer inputs.

Standard library only. No import of original probes, StrategyCone, canonical
solver/verifier, NumPy or SciPy; no LP, random sample or count-policy DFS.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import platform
import sys


def read(path):
    def pairs(items):
        out = {}
        for key, value in items:
            assert key not in out
            out[key] = value
        return out
    return json.loads(path.read_text(), object_pairs_hook=pairs)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


class Model:
    def __init__(self, data):
        self.p, self.m = len(data["topics"]), data["players"]
        assert self.p > 0 and self.m > 0
        assert len(set(data["topics"])) == self.p
        self.customers = []
        for item in data["customers"]:
            liked = tuple(item["topics"])
            n = item.get("multiplicity", 1)
            assert liked == tuple(sorted(set(liked))) and liked
            assert all(isinstance(a, int) and 0 <= a < self.p for a in liked)
            assert isinstance(n, int) and not isinstance(n, bool) and n > 0
            self.customers.append((liked, n))
        self.root = (0,) * self.p
        self.thresholds = {}
        self.states = set()

    @lru_cache(None)
    def pay(self, q, a):
        if not q[a]:
            return F(0)
        return sum((F(n, sum(q[b] for b in liked)) for liked, n in self.customers if a in liked), F(0))

    def welfare(self, q):
        return sum(n for liked, n in self.customers if any(q[a] for a in liked))

    def optimum(self):
        return max(self.welfare(tuple(int(a in J) for a in range(self.p)))
                   for size in range(min(self.p, self.m) + 1)
                   for J in combinations(range(self.p), size))

    def inc(self, q, a):
        return q[:a] + (q[a] + 1,) + q[a + 1:]

    @lru_cache(None)
    def outcomes(self, q):
        self.states.add(q)
        if sum(q) == self.m:
            return frozenset({q})
        children = [self.outcomes(self.inc(q, a)) for a in range(self.p)]
        threshold = max(min(self.pay(t, a) for t in child) for a, child in enumerate(children))
        self.thresholds[q] = threshold
        return frozenset(t for a, child in enumerate(children) for t in child if self.pay(t, a) >= threshold)


def sparse(items, length):
    result = [F(0)] * length
    seen = set()
    for pair in items:
        assert len(pair) == 2
        j, value = pair
        assert isinstance(j, int) and not isinstance(j, bool) and 0 <= j < length and j not in seen
        seen.add(j)
        result[j] = F(value)
        assert result[j] > 0
    return tuple(result)


def root_certificates(original, repository, manifest):
    saved = read(original / "root_regret_probe.json")
    assert set(saved) == {"criterion", "inputs"}
    assert saved["criterion"] == "OPT-2W>3Delta; failure of finite cones is not general evidence"
    expected_names = ["root_tax_failure", "eight_cce_welfare_gap", "aggregate_theta_failure", "fractional_actual_load_failure"]
    all_results = []
    summaries = []
    for group, name in zip(saved["inputs"], expected_names):
        assert set(group) == {"source_instance", "source_certificate", "source_certificate_sha256",
                              "topics", "players", "scope", "records"}
        assert Path(group["source_instance"]).stem == Path(group["source_certificate"]).stem == name
        paths = manifest["input_bindings"][name]
        ip, cp = repository / paths["instance"], repository / paths["certificate"]
        assert sha(cp) == group["source_certificate_sha256"]
        I = Model(read(ip))
        p, m = I.p, I.m
        assert (group["topics"], group["players"]) == (p, m)
        assert group["scope"] == "Only this fixed positive-depth policy cone, all actual roots and all m-topic comparison supports. Not a general bound."
        certificate = read(cp)
        strategy = certificate.get("strategy", certificate)
        actions = {}
        for item in strategy["actions"]:
            h, a = tuple(item["history"]), item["action"]
            assert h not in actions and 0 <= a < p
            actions[h] = a
        histories = [h for d in range(m) for h in product(range(p), repeat=d)]
        assert set(actions) == set(histories)
        @lru_cache(None)
        def ending(h):
            if len(h) == m:
                return tuple(h.count(a) for a in range(p))
            return ending(h + (actions[h],))
        @lru_cache(None)
        def coeff(q, a):
            result = []
            for mask in range(1, 1 << p):
                if mask >> a & 1:
                    load = sum(q[b] for b in range(p) if mask >> b & 1)
                    assert load > 0
                    result.append(F(1, load))
                else:
                    result.append(F(0))
            return tuple(result)
        def coverage(J):
            mask = sum(1 << a for a in J)
            return tuple(F(bool(mask & z)) for z in range(1, 1 << p))
        base = set()
        for h in histories:
            if not h:
                continue
            own = coeff(ending(h), actions[h])
            for a in range(p):
                row = tuple(u - v for u, v in zip(own, coeff(ending(h + (a,)), a))) + (F(0),)
                if any(row):
                    base.add(row)
        portfolios = list(combinations(range(p), min(m, p)))
        assert len(group["records"]) == p * len(portfolios)
        expected = [(a, J) for a in range(p) for J in portfolios]
        cones = {}
        for actual in range(p):
            q = ending((actual,))
            own = coeff(q, actual)
            rows = set(base)
            for b in range(p):
                rows.add(tuple(u - v for u, v in zip(own, coeff(ending((b,)), b))) + (F(1),))
            rows = tuple(sorted(rows))
            w = coverage(a for a, count in enumerate(q) if count) + (F(0),)
            cones[actual] = rows, w
        values = []
        positive_regrets = 0
        for rec, (actual, J) in zip(group["records"], expected):
            assert set(rec) == {"actual_root", "portfolio", "status", "value", "dual_bound",
                                "exact_optimal", "sparse_primal", "sparse_dual", "root_regret", "actual_gap"}
            assert rec["actual_root"] == actual and tuple(rec["portfolio"]) == J
            assert rec["status"] == "Optimization terminated successfully. (HiGHS Status 7: Optimal)"
            rows, w = cones[actual]
            x = sparse(rec["sparse_primal"], (1 << p))
            mu = sparse(rec["sparse_dual"], len(rows))
            assert dot(w, x) == 1
            primal_minimum = min(dot(row, x) for row in rows)
            assert primal_minimum >= 0
            v = coverage(J) + (F(-3),)
            value, beta = dot(v, x), F(rec["dual_bound"])
            assert rec["exact_optimal"] is True and value == F(rec["value"]) == beta
            residuals = [beta * w[j] - sum((weight * row[j] for weight, row in zip(mu, rows)), F(0)) - v[j]
                         for j in range(len(w))]
            assert min(residuals) >= 0
            d = [dot(coeff(ending((b,)), b), x[:-1]) for b in range(p)]
            regret = max(d) - d[actual]
            assert regret == F(rec["root_regret"]) >= 0
            assert x[-1] >= regret
            assert dot(coverage(J), x[:-1]) - 2 == F(rec["actual_gap"])
            positive_regrets += int(regret > 0)
            values.append(value)
            all_results.append({"input": name, "actual_root": actual, "portfolio": list(J),
                                "exact_value_and_bound": str(value), "positive_depth_row_count": len(base),
                                "total_sorted_rows": len(rows), "minimum_primal_slack": str(primal_minimum),
                                "minimum_dual_residual": str(min(residuals)), "root_regret": str(regret),
                                "Delta": str(x[-1]), "Delta_is_exact_regret": x[-1] == regret,
                                "comparison_gap_above_two": rec["actual_gap"],
                                "primal_nonzeros_read": len(rec["sparse_primal"]),
                                "dual_nonzeros_read": len(rec["sparse_dual"])})
        summaries.append({"input": name, "players": m, "topics": p, "source_certificate_sha256": sha(cp),
                          "source_instance_sha256": sha(ip), "ordered_nodes": len(histories),
                          "certificate_action_records_read": len(actions), "records": len(values),
                          "maximum": str(max(values)), "positive_regret_records": positive_regrets,
                          "all_exact_primal_and_dual_checks": True})
    assert len(saved["inputs"]) == 4 and len(all_results) == 230
    assert [x["maximum"] for x in summaries] == ["7/4", "3/2", "33/23", "9/8"]
    return {"scope": "Stored 230 coefficient certificates replayed exactly; zero LP or original probe execution.",
            "summaries": summaries, "records": all_results}


def insurer(original, repository, manifest):
    saved = read(original / "overlap_insurer_probe.json")
    assert set(saved) == {"criterion", "records"} and saved["criterion"] == "3(h-M)-(2W_H-OPT)>0"
    assert len(saved["records"]) == 7
    results = []
    for rec in saved["records"]:
        assert set(rec) == {"instance", "players", "topics", "minimum_SPE_root", "best_3e_minus_D",
                            "root", "terminal", "high_root", "effective_amplitude", "half_dilution", "scope"}
        path = repository / manifest["input_bindings"][rec["instance"]]["instance"]
        I = Model(read(path))
        assert (I.m, I.p) == (rec["players"], rec["topics"])
        roots = I.outcomes(I.root)
        M = I.thresholds[I.root]
        optimum = I.optimum()
        candidates = []
        child_sets = []
        for a in range(I.p):
            child = I.outcomes(I.inc(I.root, a))
            child_sets.append({"root": a, "suffix_terminal_counts": [list(q) for q in sorted(child)]})
            for q in child:
                h = I.pay(q, a)
                if h >= M:
                    e, D = h - M, 2 * I.welfare(q) - optimum
                    candidates.append((3 * e - D, a, q, h, e, D))
        assert candidates
        score = max(x[0] for x in candidates)
        a, q = rec["root"], tuple(rec["terminal"])
        assert q in I.outcomes(I.inc(I.root, a))
        h = I.pay(q, a)
        e, D = h - M, 2 * I.welfare(q) - optimum
        assert h >= M and score == 3 * e - D
        assert [str(M), str(score), str(h), str(e), D] == [
            rec["minimum_SPE_root"], rec["best_3e_minus_D"], rec["high_root"],
            rec["effective_amplitude"], rec["half_dilution"]]
        assert score <= 0
        assert rec["scope"] == "This finite fixed instance; no statement about all customer multiplicities or catalogs."
        results.append({"input": rec["instance"], "input_sha256": sha(path), "players": I.m, "topics": I.p,
                        "unit_customers": sum(n for _, n in I.customers), "root_threshold_M": str(M),
                        "OPT": optimum, "best_score": str(score), "submitted_winner_attains_maximum": True,
                        "submitted_winner_W": I.welfare(q), "states": len(I.states),
                        "eligible_root_terminal_pairs": len(candidates), "root_outcomes": [list(q) for q in sorted(roots)],
                        "all_root_suffix_sets": child_sets})
    return {"scope": "Seven exact original integer inputs only; complete suffix sets reconstructed with definition-level set recurrence.",
            "records": results}


def mature_records(original):
    markov = read(original / "known_markov_obstruction_replay.json")
    assert set(markov) == {"source", "target", "exact_unsat", "all_markov_roots", "full_min_welfare",
                           "markov_min_welfare", "dfs_nodes", "rejections", "identity"}
    assert markov["source"] == "R-18e993.../strategy_duality/markov_obstruction_report.json"
    assert markov["target"] == [1, 0, 1, 1, 0] and markov["exact_unsat"] is True
    expected = {(0, 1, 0, 1, 1), (0, 0, 1, 1, 1), (1, 0, 0, 1, 1),
                (0, 1, 1, 0, 1), (1, 0, 1, 0, 1), (1, 1, 0, 0, 1)}
    assert {tuple(q) for q in markov["all_markov_roots"]} == expected and len(markov["all_markov_roots"]) == 6
    assert (markov["full_min_welfare"], markov["markov_min_welfare"]) == (22428, 22429)
    assert (markov["dfs_nodes"], markov["rejections"]) == (100, 2)
    assert markov["identity"] == "Independent implementation replay; known obstruction, no novelty or half claim."
    static = read(original / "static_crowding_review.json")
    assert set(static) == {"independent_unit_check", "histories", "comparisons", "theta", "root_payoffs",
                          "demand_edges", "minimum_integer_crowding_cover", "available_slots"}
    assert static["independent_unit_check"] is True
    assert (static["histories"], static["comparisons"], static["theta"], static["root_payoffs"],
            static["minimum_integer_crowding_cover"], static["available_slots"]) == (31, 155, "3", ["3"] * 5, 3, 2)
    assert static["demand_edges"] == [[0, 1], [0, 4], [1, 2], [2, 3], [3, 4]]
    return {"scope": "All fields compared with existing self-contained exact K5 and count-separation proofs; neither original entry nor DFS replayed.",
            "markov_fields_read": sorted(markov), "static_fields_read": sorted(static),
            "new_count_CSP_DFS_runs": 0, "new_K5_original_runs": 0,
            "historical_DFS_counts_not_reproduced": True}


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: check_saved.py REPOSITORY OUTPUT_JSON")
    repository, output = map(Path, sys.argv[1:])
    here = Path(__file__).parent
    original = here / "original"
    manifest = read(here / "manifest.json")
    result = {"python": platform.python_version(),
              "scope": "First explicit binding of these original root-dual coordinates and seven insurer suffix maxima; no optimizer.",
              "root_regret": root_certificates(original, repository, manifest),
              "insurer": insurer(original, repository, manifest),
              "mature_records": mature_records(original),
              "primary_sha256": {p.name: sha(p) for p in sorted(original.iterdir())},
              "original_probe_runs": 0, "optimization_calls": 0}
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"root_certificates": len(result["root_regret"]["records"]),
                      "root_maxima": [x["maximum"] for x in result["root_regret"]["summaries"]],
                      "insurer_inputs": len(result["insurer"]["records"]),
                      "all_insurer_scores_nonpositive": True, "new_CSP_or_K5_runs": 0,
                      "original_probe_runs": 0, "optimization_calls": 0}))


if __name__ == "__main__":
    main()
