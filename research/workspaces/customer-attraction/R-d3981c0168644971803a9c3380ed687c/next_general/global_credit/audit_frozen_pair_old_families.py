"""Exact attacks of FROZEN-PAIR on two already proved families only.

No game/parameter search. A passing check is not evidence for arbitrary games.
The two-player complete strategies are the old A=2h, B=h terminal-transport
examples at h=1; homogeneity gives arbitrary h. The PB constants are copied
from round5/menu/pair_attack.md, whose full-SPE proof is not repeated here.
"""
from fractions import Fraction as F
from pathlib import Path
import json


def two_player(last_after_a):
    topics = ({0, 1}, {2})
    actions = {(): 0, (0,): last_after_a, (1,): 0}

    def finish(h):
        while len(h) < 2:
            h += (actions[h],)
        return h

    def utility(leaf, role):
        return sum((F(1, sum(x in topics[a] for a in leaf))
                    for x in topics[leaf[role]]), F())

    checked = 0
    for h in actions:
        chosen = utility(finish(h), len(h))
        for a in range(2):
            assert chosen >= utility(finish(h + (a,)), len(h))
            checked += 1
    z = finish(())
    profit = [utility(z, j) for j in range(2)]
    queries = [sum((F(1, 1 + int(x in topics[z[1]]))
                    for x in topics[a]), F()) for a in range(2)]
    assert max(queries) <= sum(profit)
    return {"old_family": "terminal_reply_transport: |A|=2h, |B|=h, h=1",
            "last_after_A": last_after_a, "complete_history_actions": {
                "empty": 0, "A": last_after_a, "B": 0},
            "checked_IC_including_self": checked, "actual_leaf": list(z),
            "profits": list(map(str, profit)), "frozen_root_queries": list(map(str, queries)),
            "pair_minus_max_query": str(sum(profit) - max(queries))}


def pb_old_family():
    k, d, q, t = 3, 20, 12, 10
    r, Q, H, M = 2475, 2063, 100000, 10**9

    def f(c):
        return F(q - 1, M + c) + F(1, M + c + 1)

    def g(c):
        return F(H * q, H * M + c)

    u = d * k * f(k)
    root_IC_margin = k * f(k) - (f(t) + (k - 1) * g(1))
    assert root_IC_margin > 0
    assert g(r) > 2 * f(1) - f(2)
    assert f(1) <= k * f(k)

    # On the old actual path, first three choose the three-real-block action.
    # Greedy then fills Q-3 zero blocks before doubling some of them.
    greedy_count = r - 3
    doubled = greedy_count - (Q - k)
    single = (Q - k) - doubled
    assert 0 < single and 0 < doubled < Q - k
    # Removing either of the first two actors leaves minimum real count 1;
    # dummy count is r-3. The new query therefore sees f(2), g(r-2).
    root_query = d * max(ell * f(2) + (k - ell) * g(r - 2)
                         for ell in range(1, k + 1))
    assert root_query == d * (f(2) + (k - 1) * g(r - 2))

    # A bound for every frozen query, at every actual position: deleting
    # a real actor never makes final query density exceed f(1),g(1).
    all_position_query_upper = d * (f(1) + (k - 1) * g(1))
    assert g(1) > f(1)
    assert all_position_query_upper < 2 * u - d * f(t)
    # Each Greedy actor's own real block ends at count 1 or 2; all dummy
    # final counts are at most r. Hence it earns strictly more than u.
    greedy_payoff_lower = d * (f(2) + (k - 1) * g(r))
    assert greedy_payoff_lower > u
    assert root_query < 2 * u
    singleton_query_upper = F(1, M + 1)
    assert singleton_query_upper < all_position_query_upper

    return {"old_family": "round5/menu/pair_attack.md fixed published constants",
            "scope": "Only algebra of the already proved PB actual path; no new SPE certification",
            "parameters": dict(k=k, d=d, q=q, t=t, r=r, Q=Q, H=H, M=M),
            "unused_real_blocks": 0, "single_greedy_real_blocks_per_segment": single,
            "double_greedy_real_blocks_per_segment": doubled,
            "first_three_payoff_u": str(u), "root_frozen_query_max": str(root_query),
            "first_pair_margin": str(2 * u - root_query),
            "all_position_frozen_query_upper": str(all_position_query_upper),
            "all_position_pair_lower": str(2 * u),
            "all_position_margin_lower": str(2 * u - all_position_query_upper),
            "strict_root_IC_margin_per_segment": str(root_IC_margin),
            "greedy_profit_lower_minus_u": str(greedy_payoff_lower - u)}


result = {"candidate_status": "OPEN; these old-family checks do not prove FROZEN-PAIR",
          "two_player_old_certificates": [two_player(0), two_player(1)],
          "PB_old_background_family": pb_old_family()}
output = Path(__file__).with_name("frozen_pair_old_families_audit.json")
output.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
