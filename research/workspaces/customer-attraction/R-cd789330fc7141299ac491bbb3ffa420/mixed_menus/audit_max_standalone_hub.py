"""Exact unit-customer audit, no canonical solver or discovery-code import."""
from fractions import Fraction as F
from itertools import combinations
from math import comb
import json
from pathlib import Path


def g(t):
    return 1 - t + t * t / 3


def formula(k):
    assert k >= 12 and k % 2 == 0
    m = comb(k, k // 2)
    private = m // 2 - 1
    overlap = comb(k - 2, k // 2 - 2)
    lam = F(m, 2) * g(F(1, 2)) + private * g(F(1, k))
    hub_root = F(3 * m, 4)
    root = m - 1 - F(overlap, 2)
    assert lam > hub_root
    assert lam > F(7 * m, 12)
    assert root > lam
    assert root > hub_root
    assert m // 2 - 1 > overlap
    assert lam - hub_root == F(m * (k*k - 12*k + 4), 24*k*k) - g(F(1, k))
    return dict(k=k, core=m, private=private, pair_overlap=overlap,
                total_customers=m+k*private, hub_root=hub_root,
                lambda3=lam, gap=lam-hub_root, spe_root=root,
                welfare=2*m-2-overlap)


def explicit(k):
    # Each entry is one distinct unit customer. H=0, Pi=i+1.
    m = comb(k, k // 2)
    clients = [frozenset((0,) + tuple(i+1 for i in j))
               for j in combinations(range(k), k//2)]
    for i in range(k):
        clients.extend([frozenset((i+1,)) for _ in range(m//2-1)])
    topics = [set() for _ in range(k+1)]
    for customer, likes in enumerate(clients):
        for topic in likes:
            topics[topic].add(customer)
    assert len({frozenset(t) for t in topics}) == k+1
    assert len(topics[0]) == m
    assert all(len(t) == m-1 for t in topics[1:])

    payoff = []
    for a in range(k+1):
        row = []
        for b in range(k+1):
            overlap = len(topics[a] & topics[b])
            row.append(F(len(topics[b])) - F(overlap, 2))
        payoff.append(row)
    # payoff[a][b] is last player's utility after root a.
    reply = [1] + [1+(i+1) % k for i in range(k)]
    root_payoffs = []
    br_sets = []
    comparisons = 0
    for a in range(k+1):
        best = max(payoff[a])
        br = [b for b in range(k+1) if payoff[a][b] == best]
        br_sets.append(br)
        assert reply[a] in br
        assert br == (list(range(1, k+1)) if a == 0
                      else [b for b in range(1, k+1) if b != a])
        root_payoffs.append(payoff[reply[a]][a])
        for b in range(k+1):
            assert payoff[a][reply[a]] >= payoff[a][b]
            comparisons += 1
    root_action = 1
    assert root_payoffs[root_action] == max(root_payoffs)
    for a in range(k+1):
        assert root_payoffs[root_action] >= root_payoffs[a]
        comparisons += 1

    # True expected payoff to a pure static query against two iid q players.
    alpha = [F(0) for _ in range(k+1)]
    for likes in clients:
        probability = F(len(likes - {0}), k)
        contribution = g(probability)
        for topic in likes:
            alpha[topic] += contribution
    lam = alpha[1]
    assert all(a == lam for a in alpha[1:])
    assert alpha[0] < lam
    assert root_payoffs[0] < lam
    assert root_payoffs[root_action] > lam

    welfare = len(topics[root_action] | topics[reply[root_action]])
    optimum = max(len(a | b) for a in topics for b in topics)
    assert welfare == optimum
    f = formula(k)
    assert f['hub_root'] == root_payoffs[0]
    assert f['spe_root'] == root_payoffs[root_action]
    assert f['lambda3'] == lam
    assert f['total_customers'] == len(clients)
    assert f['welfare'] == welfare
    return dict(**f, full_ordered_histories=k+2,
                exact_deviation_comparisons=comparisons,
                hub_reply=reply[0], root_action=root_action,
                standalone_sizes=[len(t) for t in topics],
                root_payoffs=root_payoffs, static_alpha=alpha,
                actual_terminal=[root_action,reply[root_action]],
                optimum=optimum, all_checks_passed=True)


if __name__ == '__main__':
    result = dict(status='author exact audit; not independent review',
                  explicit=[explicit(12), explicit(14)],
                  formula_even_parameters=[formula(k) for k in range(12,101,2)],
                  general_evidence='Analytic proof in max_standalone_hub_boundary.md',
                  target_status='Q-CAG-HALF OPEN')
    text = json.dumps(result, default=str, ensure_ascii=False, indent=2)
    Path(__file__).with_name('max_standalone_hub_audit.json').write_text(text+'\n')
    print(json.dumps(dict(status=result['status'], explicit=result['explicit'],
                          formula_parameter_count=len(result['formula_even_parameters'])),
                     default=str, ensure_ascii=False, indent=2))
