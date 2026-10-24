"""Definition-level finite regression of the general virtual-replay lemma.

The proof is in virtual_replay_regret.md; these finite checks are not its proof.
No repository solver is imported. Running prints JSON and does not overwrite evidence.
"""

from fractions import Fraction as F
from itertools import combinations, product
import json


def audit(m, topics, sigma):
    labels = tuple(topics)
    customers = set().union(*topics.values())

    def rollout(prefix):
        path = list(prefix)
        while len(path) < m:
            path.append(sigma(tuple(path)))
        return tuple(path)

    def utility(path, player, retained=None):
        if retained is None:
            retained = range(m)
        return sum((F(1, sum(x in topics[path[j]] for j in retained))
                    for x in topics[path[player]]), F())

    original_comparisons = 0
    for depth in range(m):
        for h in product(labels, repeat=depth):
            z = rollout(h)
            for action in labels:
                other = rollout(h + (action,))
                assert utility(z, depth) >= utility(other, depth)
                original_comparisons += 1

    projected_comparisons = 0
    nonconsecutive_subsets = 0
    max_gain = F()
    for q in range(m):
        for deleted_tuple in combinations(range(m), q):
            deleted = set(deleted_tuple)
            retained = tuple(i for i in range(m) if i not in deleted)
            if q and deleted_tuple != tuple(range(m-q, m)):
                nonconsecutive_subsets += 1

            def lift(new_h):
                old_h = []
                read = 0
                while len(old_h) < m:
                    if len(old_h) in deleted:
                        old_h.append(sigma(tuple(old_h)))
                    elif read < len(new_h):
                        old_h.append(new_h[read])
                        read += 1
                    else:
                        break
                return tuple(old_h)

            def reduced_action(new_h):
                return sigma(lift(new_h))

            def reduced_rollout(new_h):
                path = list(new_h)
                while len(path) < len(retained):
                    path.append(reduced_action(tuple(path)))
                return tuple(path)

            for depth in range(len(retained)):
                old_player = retained[depth]
                for new_h in product(labels, repeat=depth):
                    old_h = lift(new_h)
                    z = rollout(old_h)
                    actual = utility(z, old_player, retained)
                    old_actual = utility(z, old_player)
                    refund = actual - old_actual
                    regret = F()
                    for action in labels:
                        z_dev = rollout(old_h + (action,))
                        assert tuple(z_dev[i] for i in retained) == reduced_rollout(new_h + (action,))
                        value = utility(z_dev, old_player, retained)
                        old_value = utility(z_dev, old_player)
                        slack = old_actual-old_value
                        refund_dev = value-old_value
                        assert value-actual == refund_dev-refund-slack
                        assert value <= (q+1)*actual
                        regret = max(regret, value-actual)
                        projected_comparisons += 1
                    assert regret <= q*old_actual-refund
                    max_gain = max(max_gain, regret)

            reduced_path = reduced_rollout(())
            z = rollout(())
            assert reduced_path == tuple(z[i] for i in retained)
            total_regret = F()
            spectral_cap_sum = F()
            h = ()
            p_deleted = sum((utility(z, i) for i in deleted), F())
            largest_topic = max(map(len, topics.values()))
            for player in retained:
                old_h = lift(h)
                value = utility(z, player, retained)
                gain = max(F(), max(utility(rollout(old_h+(a,)), player, retained)-value
                                   for a in labels))
                old_value = utility(z, player)
                cap = min(q*old_value, F(q*largest_topic, q+1))
                assert gain <= cap-(value-old_value)
                assert gain <= F(m, q+1)*p_deleted-(value-old_value)
                spectral_cap_sum += cap
                total_regret += gain
                h += (z[player],)
            p_kept = sum((utility(z, i) for i in retained), F())
            lost = sum(not any(x in topics[z[i]] for i in retained)
                       and any(x in topics[z[i]] for i in deleted) for x in customers)
            refunds = sum((utility(z, i, retained)-utility(z, i) for i in retained), F())
            assert refunds == p_deleted-lost
            assert total_regret <= q*p_kept-p_deleted+lost
            assert total_regret <= spectral_cap_sum-p_deleted+lost

    return dict(original_comparisons=original_comparisons,
                projected_comparisons=projected_comparisons,
                deletion_subsets_not_suffix=nonconsecutive_subsets,
                largest_single_regret=str(max_gain))


reports = []
# A complete three-player history-dependent SPE, including different AB / BA replies.
topics = {"A": {0, 1}, "B": {2, 3}}
def policy(h):
    if not h:
        return "A"
    if len(h) == 1:
        return h[0]
    return "B" if h[0] == "A" else "A"
reports.append(dict(name="history_dependent_two_blocks", **audit(3, topics, policy)))

# Exact sharpness family for every tested q; its symbolic proof handles all q.
for q in range(1, 7):
    topics = {"A": {0}, "B": set(range(1, q+2))}
    policy = lambda h: "A" if not h else "B"
    reports.append(dict(name=f"sharp_q_{q}", **audit(q+1, topics, policy)))

print(json.dumps(dict(status="pass", scope="finite implementation regression only", reports=reports), indent=2))
