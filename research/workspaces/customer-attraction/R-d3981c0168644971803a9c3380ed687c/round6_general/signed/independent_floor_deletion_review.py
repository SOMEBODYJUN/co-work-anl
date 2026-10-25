"""Independent unit-expanded, ordered-tree audit of floor deletion budget.

No imports from customer_attraction or from the construction author's scripts.
All 31 clients and the supplied original policy are treated as raw input data.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "credible/true_reset_floor_counterexample.json"


def main():
    raw = json.loads(SOURCE.read_text())
    types = raw["instance"]["customers"]
    clients = tuple(frozenset(row["topics"]) for row in types
                    for _ in range(row["multiplicity"]))
    assert len(clients) == 31
    actions = tuple(range(len(raw["instance"]["topics"])))
    original_target = tuple(raw["path"])
    supplied_policy = {tuple(row["history"]): row["action"]
                       for row in raw["certificate"]["actions"]}

    @lru_cache(None)
    def payoffs(terminal):
        values = [F(0) for _ in terminal]
        for client in clients:
            owners = [i for i, a in enumerate(terminal) if a in client]
            for i in owners:
                values[i] += F(1, len(owners))
        return tuple(values)

    def welfare(path):
        return sum(any(a in client for a in path) for client in clients)

    def optimum(m):
        return max(welfare(support)
                   for k in range(1, min(m, len(actions)) + 1)
                   for support in combinations(actions, k))

    def build(m):
        thresholds, rows, all_outcomes = {}, {}, {}

        def ordered_BI(h):
            if len(h) == m:
                outcomes = frozenset({h})
            else:
                i = len(h)
                children = {a: ordered_BI(h + (a,)) for a in actions}
                ell = {a: min(payoffs(t)[i] for t in children[a]) for a in actions}
                floor = max(ell.values())
                thresholds[h] = floor
                rows[h] = ell
                outcomes = frozenset(t for a in actions for t in children[a]
                                     if payoffs(t)[i] >= floor)
                assert outcomes
            all_outcomes[h] = outcomes
            return outcomes

        root = ordered_BI(())
        assert len(all_outcomes) == sum(len(actions)**i for i in range(m+1))
        assert len(rows) == sum(len(actions)**i for i in range(m))
        assert all(set(row) == set(actions) for row in rows.values())
        return root, thresholds, rows, all_outcomes

    def replay(policy, h, m):
        while len(h) < m:
            h += (policy[h],)
        return h

    def audit_policy(policy, m):
        histories = [h for i in range(m) for h in product(actions, repeat=i)]
        assert set(policy) == set(histories)
        comparisons, minimum = [], None
        for h in histories:
            obey = replay(policy, h, m)
            i = len(h)
            for a in actions:  # own action deliberately included
                dev = replay(policy, h + (a,), m)
                gap = payoffs(obey)[i] - payoffs(dev)[i]
                comparisons.append({"history": h, "forced": a,
                                    "obey_terminal": obey, "forced_terminal": dev,
                                    "IC_gap": str(gap)})
                minimum = gap if minimum is None else min(minimum, gap)
                assert gap >= 0, (h, a, gap)
        return {"decision_histories":len(histories), "all_forced_comparisons":len(comparisons),
                "including_own":len(histories), "minimum_IC_gap":str(minimum),
                "comparisons":comparisons}

    root4, threshold4, ell4, outcomes4 = build(4)
    assert original_target in root4
    supplied_audit = audit_policy(supplied_policy, 4)
    assert replay(supplied_policy, (), 4) == original_target

    # Reconstruct a second complete policy from this independent ordered BI.
    reconstructed = {}
    def realize(h, desired):
        assert desired in outcomes4[h]
        if len(h) == 4:
            return
        i = len(h)
        candidates = [a for a in actions if desired in outcomes4[h+(a,)]
                      and payoffs(desired)[i] >= threshold4[h]]
        chosen = min(candidates)
        reconstructed[h] = chosen
        for a in actions:
            child = h+(a,)
            if a == chosen:
                realize(child, desired)
            else:
                target = min(outcomes4[child], key=lambda t:(payoffs(t)[i],t))
                realize(child, target)
    realize((), original_target)
    independent_audit = audit_policy(reconstructed, 4)
    assert replay(reconstructed, (), 4) == original_target

    root3, threshold3, ell3, outcomes3 = build(3)
    shortened = original_target[1:]
    profits = payoffs(shortened)
    floors = tuple(threshold3[shortened[:i]] for i in range(3))
    deficits = tuple(x-y for x,y in zip(floors,profits))
    deleted_payoff = payoffs(original_target)[0]
    positive_cost = sum(max(x,0) for x in deficits)
    signed_cost = sum(deficits)
    assert floors == (F(12),F(12),F(10))
    assert profits == (F(8),F(15,2),F(15,2))
    assert positive_cost == signed_cost == 11 > deleted_payoff == F(28,3)

    floor_table = []
    for i in range(3):
        h = shortened[:i]
        action_rows = []
        for a in actions:
            child = h+(a,)
            witness = min(outcomes3[child], key=lambda t:(payoffs(t)[i],t))
            action_rows.append({"forced_action":a, "is_target_action":a==shortened[i],
                                "ell":str(ell3[h][a]), "minimizing_SPE_terminal":witness,
                                "all_child_SPE_terminals":sorted(outcomes3[child])})
        floor_table.append({"prefix":h, "mu":str(floors[i]), "all_forced_actions":action_rows})

    report = {
        "status":"PASS: positive-part and untruncated-net floor deletion budgets both fail",
        "independence":"No author-script or canonical-model/solver imports; unit clients and ordered trees rebuilt.",
        "unit_clients":len(clients), "raw_types":types,
        "original":{"players":4,"target":original_target,
                    "payoffs":list(map(str,payoffs(original_target))),
                    "W":welfare(original_target),"OPT":optimum(4),
                    "ordered_tree_states":len(outcomes4),
                    "BI_decision_states":len(ell4),
                    "BI_all_forced_entries_including_own":sum(len(v) for v in ell4.values()),
                    "supplied_policy_audit":supplied_audit,
                    "independently_reconstructed_policy":
                    [{"history":h,"action":a} for h,a in sorted(reconstructed.items())],
                    "reconstructed_policy_audit":independent_audit},
        "deleted_game":{"players":3,"target":shortened,
                        "target_is_SPE_path":shortened in root3,
                        "target_profits":list(map(str,profits)),
                        "target_W":welfare(shortened),"OPT":optimum(3),
                        "root_SPE_welfares":sorted({welfare(t) for t in root3}),
                        "mu":list(map(str,floors)),
                        "signed_deficits":list(map(str,deficits)),
                        "positive_deficit_sum":str(positive_cost),
                        "signed_deficit_sum":str(signed_cost),
                        "deleted_original_profit":str(deleted_payoff),
                        "strict_failure_gap":str(positive_cost-deleted_payoff),
                        "ordered_tree_states":len(outcomes3),
                        "decision_states":len(ell3),
                        "all_forced_entries_including_own":sum(len(v) for v in ell3.values()),
                        "target_prefix_floor_table":floor_table,
                        "full_floor_table":[{"history":h,"mu":str(threshold3[h]),
                                             "ell":{str(a):str(v) for a,v in ell3[h].items()}}
                                            for h in sorted(ell3)]},
        "scope":"The contract includes the last target role and does not reset its action to BR first. A failure of positive-part and direct signed-net floor-deletion payment helpers only; no half counterexample; no refutation of last-BR-reset variants."}
    target = HERE / "independent_floor_deletion_review.json"
    target.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"original_payoffs":report["original"]["payoffs"],
                      "original_states":len(outcomes4),"original_IC":supplied_audit["all_forced_comparisons"],
                      "mu":list(map(str,floors)),"new_profits":list(map(str,profits)),
                      "positive_and_net_cost":str(positive_cost),"deleted_profit":str(deleted_payoff),
                      "gap":str(positive_cost-deleted_payoff),"smaller_states":len(outcomes3)},indent=2))


if __name__ == "__main__":
    main()
