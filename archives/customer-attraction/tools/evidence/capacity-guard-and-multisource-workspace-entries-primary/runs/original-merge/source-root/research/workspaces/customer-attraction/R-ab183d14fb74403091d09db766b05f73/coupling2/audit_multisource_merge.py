"""Definition-level exact audit of the integrated-kernel merge route."""

from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import random
import sys

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[4]
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, Instance, ExactSPESolver


def has_duplicate(labels):
    return len(set(labels)) < len(labels)


def manufacture_duplicate(labels, reply, operation):
    """Operation mutates labels; fixed pivot zero, two other slots."""
    assert len(labels) >= 3
    if has_duplicate(labels):
        return
    operation(1, 0)
    operation(2, 0)
    assert labels[1] == labels[2] == reply(labels[0])


def main():
    graph_cases = 0
    graph_updates = 0
    for p in range(1, 5):
        for values in product(range(p), repeat=p):
            for initial in product(range(p), repeat=3):
                labels = list(initial)
                steps = [0]

                def op(i, j):
                    assert i != j
                    labels[i] = values[labels[j]]
                    steps[0] += 1
                    assert steps[0] <= 2

                manufacture_duplicate(labels, lambda b: values[b], op)
                assert has_duplicate(labels)
                graph_cases += 1
                graph_updates += steps[0]

    rng = random.Random(221022)
    spe_cases = 0
    update_rows = 0
    merges = 0
    prefixes = 0
    no_br_recovery_sufficient = 0
    route_reports = []
    for m, p in [(3, 3), (4, 3), (5, 3), (3, 4)]:
        for sample in range(5):
            types = tuple(
                CustomerType(frozenset(a for a in range(p) if mask >> a & 1), rng.randint(1, 8))
                for mask in range(1, 1 << p)
                if rng.random() < 0.65
            )
            instance = Instance(tuple(f"T{a}" for a in range(p)), types, m)
            solver = ExactSPESolver(instance)
            cert = solver.certificate(min(solver.worst_outcomes()))
            actions = dict(cert.actions)
            actual = ()
            while len(actual) < m:
                actual += (actions[actual],)

            def pay(a, path):
                return sum((F(t.multiplicity, sum(b in t.topics for b in path)) for t in types if a in t.topics), F(0))

            def coverage(path):
                return sum(t.multiplicity for t in types if any(a in t.topics for a in path))

            def tax(h):
                return sum((F(t.multiplicity * (d := sum(a in t.topics for a in h)), d + 1) for t in types), F(0))

            def kernel(h, labels):
                r = m - len(h) - 1
                return sum(
                    (t.multiplicity * (F(int(d > 0), h0 + 1) + F(d - int(d > 0), h0 + r + 1))
                     for t in types
                     for d in [sum(a in t.topics for a in labels)]
                     for h0 in [sum(a in t.topics for a in h)]),
                    F(0),
                )

            optimum_source = max(product(range(p), repeat=m), key=coverage)
            optimum = coverage(optimum_source)
            labels = list(optimum_source)
            start = kernel((), labels)
            bonus = start - optimum
            assert bonus == sum((F(t.multiplicity * max(sum(a in t.topics for a in labels) - 1, 0), m) for t in types), F(0))
            utilities = tuple(pay(a, actual) for a in actual)
            welfare = sum(utilities, F(0))
            debt_total = F(0)
            br_total = F(0)
            merge_credit = F(0)
            prefix_credit = F(0)
            updates_for_route = 0

            for k in range(m - 2):
                h = actual[:k]
                r = m - k - 1

                def reply(b):
                    return actions[h + (b,) * r]

                def op(i, j):
                    nonlocal debt_total, br_total, update_rows, updates_for_route
                    assert i != j
                    a, b, new = labels[i], labels[j], reply(labels[j])
                    old_kernel = kernel(h, labels)
                    br = pay(new, h + (b,) * r + (new,)) - pay(a, h + (b,) * r + (a,))
                    assert br >= 0
                    debt = F(0)
                    for t in types:
                        oldbit = int(a in t.topics)
                        newbit = int(new in t.topics)
                        pivotbit = int(b in t.topics)
                        other = sum(labels[v] in t.topics for v in range(len(labels)) if v not in (i, j))
                        if not pivotbit and other:
                            h0 = sum(v in t.topics for v in h)
                            debt += t.multiplicity * (F(1, h0 + 1) - F(1, h0 + r + 1)) * (newbit - oldbit)
                    labels[i] = new
                    assert kernel(h, labels) - old_kernel == br - debt
                    debt_total += debt
                    br_total += br
                    update_rows += 1
                    updates_for_route += 1

                old_labels = labels[:]
                debt_before = debt_total
                already_repeated = has_duplicate(labels)
                manufacture_duplicate(labels, reply, op)
                if not already_repeated:
                    a, b, c = old_labels[1], old_labels[0], old_labels[2]
                    new = reply(b)
                    combined_debt = F(0)
                    for ttype in types:
                        alpha = int(a in ttype.topics)
                        beta = int(b in ttype.topics)
                        gamma = int(c in ttype.topics)
                        eta = int(new in ttype.topics)
                        other = sum(v in ttype.topics for v in old_labels[3:])
                        if not beta:
                            h0 = sum(v in ttype.topics for v in h)
                            bracket = eta - alpha * gamma if not other else 2 * eta - alpha - gamma
                            combined_debt += ttype.multiplicity * (F(1, h0 + 1) - F(1, h0 + r + 1)) * bracket
                    assert debt_total - debt_before == combined_debt
                repeated = next(a for a, q in Counter(labels).items() if q >= 2)
                before = kernel(h, labels)
                labels.remove(repeated)
                clone_value = sum((F(t.multiplicity, sum(a in t.topics for a in h) + r + 1) for t in types if repeated in t.topics), F(0))
                assert before - kernel(h, labels) == clone_value
                assert utilities[k] >= clone_value
                merge_credit += utilities[k] - clone_value
                merges += 1

                after = kernel(actual[:k + 1], labels)
                drift = kernel(h, labels) - after
                credit = tax(actual[:k + 1]) - tax(h) - drift
                direct_credit = F(0)
                for t in types:
                    h0 = sum(a in t.topics for a in h)
                    d = sum(a in t.topics for a in labels)
                    u = int(d > 0)
                    z = int(actual[k] in t.topics)
                    direct_credit += t.multiplicity * (F(z * (1 - u), (h0 + 1) * (h0 + 2)) + F((1 - z) * (d - u), (h0 + r) * (h0 + r + 1)))
                assert credit == direct_credit >= 0
                prefix_credit += credit
                prefixes += 1

            assert len(labels) == 2
            end_credit = utilities[-2] + utilities[-1] + tax(actual[:-1]) - tax(actual[:-2]) - kernel(actual[:-2], labels)
            assert end_credit >= 0
            total_slack = br_total + merge_credit + prefix_credit + end_credit
            net_debt = debt_total - total_slack - bonus
            assert optimum == welfare + tax(actual[:-1]) + net_debt
            strong_without_br = debt_total - merge_credit - prefix_credit - end_credit - bonus
            sufficient = strong_without_br <= welfare - tax(actual[:-1])
            no_br_recovery_sufficient += int(sufficient)
            route_reports.append({"m": m, "p": p, "sample": sample, "updates": updates_for_route, "OPT": str(optimum), "W": str(welfare), "signed_debt": str(debt_total), "BR_slack": str(br_total), "net_invariant": str(net_debt), "no_BR_recovery_sufficient_half": sufficient})
            spe_cases += 1

    report = {
        "status": "exact merge-route construction/identity audit; debt payment and Q-CAG-HALF OPEN",
        "all_function_graph_cases_p_le_4_q_3": graph_cases,
        "graph_updates": graph_updates,
        "finite_full_spe_cases": spe_cases,
        "exact_true_reply_debt_identities": update_rows,
        "actual_profit_paid_merges": merges,
        "single_capacity_prefixes": prefixes,
        "fixed_pivot_no_BR_recovery_sufficient_cases": no_br_recovery_sufficient,
        "routes": route_reports,
        "seed": 221022,
    }
    (BASE / "multisource_merge_audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "routes"}, indent=2))


if __name__ == "__main__":
    main()
