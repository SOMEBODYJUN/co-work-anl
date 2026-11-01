"""Independent unit-expanded audit of the 16-client no-pure-SC witness.

Standard library only; does not read/import the construction, optimizer,
repository model, or SPE solver. The input is transcribed from the discovered
certificate and every ordered decision history is checked from definitions.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
COUNTS = {2: 1, 14: 1, 16: 1, 18: 1, 29: 3, 38: 1,
          41: 1, 43: 2, 45: 2, 47: 1, 49: 1, 52: 1}
M, K = 3, 6
UNITS = [frozenset(a for a in range(K) if mask & (1 << a))
         for mask, count in COUNTS.items() for _ in range(count)]


def action(h):
    if len(h) == 0:
        return 0
    if len(h) == 1:
        return 3 if h[0] < 3 else 0
    assert len(h) == 2
    group = range(3) if h[1] < 3 else range(3, 6)
    return next(a for a in group if a not in h)


def finish(h):
    while len(h) < M:
        h = h + (action(h),)
    return h


def utility(terminal, position):
    a = terminal[position]
    return sum((F(1, sum(b in S for b in terminal)) for S in UNITS if a in S), F(0))


def main():
    assert len(UNITS) == 16
    topics = [frozenset(i for i, S in enumerate(UNITS) if a in S) for a in range(K)]
    assert len(set(topics)) == K
    comparisons = []
    second_table, third_table = [], []
    for length in range(M):
        for h in product(range(K), repeat=length):
            prescribed = finish(h)
            actual_payoff = utility(prescribed, length)
            branch_payoffs = []
            for a in range(K):
                deviation = finish(h + (a,))
                branch_payoff = utility(deviation, length)
                gap = actual_payoff - branch_payoff
                assert gap >= 0, (h, a, gap)
                comparisons.append(gap)
                branch_payoffs.append(str(branch_payoff))
            if length == 1:
                second_table.append(branch_payoffs)
            if length == 2:
                third_table.append({"history": list(h), "prescribed": action(h),
                                    "branch_payoffs": branch_payoffs})
    assert len(comparisons) == 258
    actual = finish(())
    actual_payoffs = [utility(actual, i) for i in range(M)]
    W = sum(any(a in S for a in actual) for S in UNITS)
    OPT = max(sum(any(a in S for a in A) for S in UNITS)
              for n in range(M + 1) for A in combinations(range(K), n))
    assert sum(actual_payoffs) == W

    pooled_table, column_counts, diagonal_margins = [], [], []
    for a in range(K):
        branch_terminals = [finish(actual[:i] + (a,)) for i in range(M)]
        competitor_tuples = [z[:i] + z[i+1:] for i, z in enumerate(branch_terminals)]
        counts = [sum(z.count(t) for z in competitor_tuples) for t in range(K)]
        assert sum(counts) == M*(M-1)
        column_counts.append(counts)
        mu = [F(sum(sum(b in S for b in z) for z in competitor_tuples), M) for S in UNITS]
        g = [sum((1/(1+mu[x]) for x,S in enumerate(UNITS) if t in S), F(0))
             for t in range(K)]
        pooled_table.append(g)
        real_deviation_sum = sum(utility(z, i) for i,z in enumerate(branch_terminals))
        assert M*g[a] <= real_deviation_sum <= W
        diagonal_margins.append(str(F(W, M)-g[a]))

    challengers = [5,5,5,2,2,2]
    gaps = [pooled_table[a][b]-pooled_table[a][a] for a,b in enumerate(challengers)]
    assert gaps == [F(3,8), F(1,35), F(3,56), F(9,28), F(1,12), F(1,12)]
    assert min(gaps) > 0
    best = [[t for t,v in enumerate(g) if v==max(g)] for g in pooled_table]
    assert all(a not in best[a] for a in range(K))
    universal_column_cap = max(max(g) for g in pooled_table)
    assert universal_column_cap == F(107,24) < F(W,M)
    report = {"status": "PASS", "scope": "One unit-client instance, full ordered-history pure SPE, strict absence of every pure self-consistent query. No half or mixed-payment counterexample.",
              "integer_type_counts": COUNTS, "unit_clients": len(UNITS), "players": M,
              "topic_count": K, "distinct_topic_coverage": True,
              "ordered_decision_histories": 43, "all_spe_comparisons": len(comparisons),
              "minimum_spe_gap": str(min(comparisons)), "spe_ties_including_self": sum(gap==0 for gap in comparisons),
              "actual_path": list(actual), "actual_payoffs": list(map(str,actual_payoffs)),
              "W": W, "OPT": OPT, "half_margin": 2*W-OPT,
              "competitor_topic_count_sums_by_forced_query": column_counts,
              "g_table_rows_forced_A_columns_query_T": [[str(v) for v in g] for g in pooled_table],
              "best_response_topics_by_forced_query": best, "challengers": challengers,
              "strict_challenger_gaps": list(map(str,gaps)),
              "maximum_of_all_pure_column_query_values": str(universal_column_cap),
              "W_over_m_minus_universal_column_cap": str(F(W,M)-universal_column_cap),
              "diagonal_W_over_m_minus_g_A": diagonal_margins,
              "second_player_branch_payoff_table": second_table,
              "third_player_all_history_tables": third_table}
    (HERE/"no_pure_selfconsistent_audit.json").write_text(json.dumps(report,indent=2)+"\n")
    compact = {k:v for k,v in report.items() if k not in {"third_player_all_history_tables"}}
    print(json.dumps(compact,indent=2))


if __name__ == "__main__":
    main()
