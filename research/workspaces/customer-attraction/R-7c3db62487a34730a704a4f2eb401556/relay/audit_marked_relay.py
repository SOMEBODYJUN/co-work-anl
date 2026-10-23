"""Definition-level audits of the marked genuine-early-SPE relay interface.

No canonical model, solver, or certificate verifier is imported. Integer row
multiplicities encode distinct unit clients. Existing certificate is read-only.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / "R-12bf6a96d24c48eca828620d6642e203" / "direct_cover" / "actual_root_B_certificate.json"
ROWS = [((0,), 12), ((1,), 8), ((2,), 4), ((3,), 8),
        ((0, 4), 6), ((0, 5), 6), ((2, 4), 3), ((2, 5), 3),
        ((0, 4, 5), 6), ((1, 4, 5), 2), ((2, 4, 5), 1), ((3, 4, 5), 2)]


def audit(actions, rows, k, m):
    histories = {h for length in range(m) for h in product(range(k), repeat=length)}
    assert set(actions) == histories

    def walk(h):
        while len(h) < m:
            h += (actions[h],)
        return h

    def payoff(q, t):
        assert t in q
        return sum((F(n, sum(a in B for a in q)) for B, n in rows if t in B), F(0))

    def query(q, t):
        return sum((F(n, 1 + sum(a in B for a in q)) for B, n in rows if t in B), F(0))

    def rebate(q, t):
        assert t in q
        result = F(0)
        for B, n in rows:
            if t in B:
                c = sum(a in B for a in q)
                result += F(n, c * (c + 1))
        return result

    terminal_shortcuts = 0
    for h in product(range(k), repeat=m - 1):
        a = actions[h]
        target = h + (a,)
        for d, t in product(range(k), repeat=2):
            q = h + (d,)
            real_query = h + (t,)
            gamma_t = payoff(target, a) - payoff(real_query, t)
            overlap = F(0)
            for B, n in rows:
                if t in B and d in B:
                    load = sum(b in B for b in h)
                    overlap += F(n, (load + 1) * (load + 2))
            assert payoff(target, a) - query(q, t) == gamma_t + overlap
            assert gamma_t >= 0 and overlap >= 0
            terminal_shortcuts += 1

    root = walk(())
    comparisons = 0
    row_sources = {}
    for h in histories:
        a = actions[h]
        chosen = walk(h)
        for t in range(k):
            child = walk(h + (t,))
            assert payoff(chosen, a) >= payoff(child, t)
            comparisons += 1
            if t != a:
                assert child not in row_sources
                row_sources[child] = (h, t)

    leaves = tuple(product(range(k), repeat=m))
    assert set(row_sources) == set(leaves) - {root}
    info = {}
    marked_checks = query_checks = 0
    for q in leaves:
        deviations = tuple(i for i in range(m) if q[i] != actions[q[:i]])
        if not deviations:
            assert q == root
            continue
        j = deviations[-1]
        h, d, a = q[:j], q[j], actions[q[:j]]
        parent = walk(h)
        assert walk(h + (d,)) == q
        assert row_sources[q] == (h, d)
        assert tuple(i for i in range(m) if parent[i] != actions[parent[:i]]) == deviations[:-1]
        gamma = payoff(parent, a) - payoff(q, d)
        assert gamma >= 0
        for t in set(q):
            debt = payoff(q, t) - payoff(q, d)
            assert payoff(parent, a) + debt - payoff(q, t) == gamma
            marked_checks += 1
        for t in range(k):
            delta_plus = query(q, t) - query(q, d)
            assert payoff(q, d) == query(q, d) + rebate(q, d)
            assert payoff(parent, a) + delta_plus - rebate(q, d) - query(q, t) == gamma
            assert (query(parent, a) + delta_plus + rebate(parent, a)
                    - rebate(q, d) - query(q, t)) == gamma
            query_checks += 1
        info[q] = (parent, d, a, gamma, len(deviations))

    # Root capacity for sources whose first disagreement is prescribed.
    # Although the intermediate marker can move, the final original player
    # is exactly the first deviating position, not an arbitrary root sink.
    for q in info:
        first = next(i for i in range(m) if q[i] != actions[q[:i]])
        cursor, marker = q, None
        while cursor != root:
            cursor, _, marker, _, _ = info[cursor]
        assert marker == root[first]

    # Deterministic positive rational sources throughout the terminal tree.
    demand = {q: defaultdict(F) for q in leaves}
    source_value = F(0)
    for index, q in enumerate(leaves):
        if index % 11 == 0:
            for t in set(q):
                mass = F(1 + t, 2 + index % 7)
                demand[q][t] += mass
                source_value += mass * payoff(q, t)
    debt_sum = slack_sum = F(0)
    for q in sorted(info, key=lambda q: info[q][4], reverse=True):
        parent, d, a, gamma, _ = info[q]
        mass = sum(demand[q].values(), F(0))
        debt_sum += sum((weight * payoff(q, t) for t, weight in demand[q].items()), F(0)) - mass * payoff(q, d)
        slack_sum += mass * gamma
        demand[parent][a] += mass
    sink_value = sum((mass * payoff(root, t) for t, mass in demand[root].items()), F(0))
    assert source_value == sink_value + debt_sum - slack_sum
    return {"root": root, "ordered_histories": len(histories),
            "real_comparisons_including_self": comparisons,
            "terminal_outcomes": len(leaves), "nonself_edges": len(info),
            "marked_identity_checks": marked_checks,
            "extra_query_identity_checks": query_checks,
            "terminal_query_shortcut_checks": terminal_shortcuts,
            "first_disagreement_sink_checks": len(info),
            "multisource_identity": "exact", "source_value": str(source_value),
            "root_sink_value": str(sink_value), "signed_debt": str(debt_sum),
            "paid_real_slack": str(slack_sum)}


def main():
    source = json.loads(SOURCE.read_text())
    actions = {tuple(row["history"]): row["action"] for row in source["certificate"]["actions"]}
    result = audit(actions, ROWS, 6, 4)

    # Same genuine SPE, theme-balanced switches at two distinct real leaves.
    small_actions = {(): 0, (0,): 1, (1,): 0,
                     (0, 0): 1, (0, 1): 0, (1, 0): 1, (1, 1): 0}
    small = audit(small_actions, [((0,), 1), ((1,), 1)], 2, 3)
    q, q_prime = (0, 1, 0), (1, 0, 1)

    def disjoint_pay(q, t):
        return F(1, q.count(t))

    left = disjoint_pay(q, 1) - disjoint_pay(q, 0)
    right = disjoint_pay(q_prime, 0) - disjoint_pay(q_prime, 1)
    assert left == right == F(1, 2)
    print(json.dumps({"status": "PASS", "certificate_source": str(SOURCE.relative_to(HERE.parents[4])),
                      "sixty_one_clients": result, "two_singletons": small,
                      "theme_balanced_cross_terminal_debt": str(left + right),
                      "scope": "finite exact interface audit; not a general half proof"}, indent=2))


if __name__ == "__main__":
    main()
