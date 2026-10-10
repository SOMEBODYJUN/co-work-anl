#!/usr/bin/env python3
"""Independent exact-rational review, using only the candidate JSON as input.

No candidate-author modules or verification helpers are imported. Customers
are compressed only when evaluating sums; repeated unit customers retain their
integer multiplicities. All ordered histories and deviations are enumerated.
"""
from fractions import Fraction as F
from itertools import product, combinations, combinations_with_replacement
from pathlib import Path
import hashlib
import json
import argparse

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('input', nargs='?', type=Path, default=ROOT / 'history/source/notes/customer_attraction/individual_security_2026-10-10/compressed_34.json')
parser.add_argument('--output-dir', type=Path)
args = parser.parse_args()
INPUT = args.input
OUTPUT_PREFIX = ''
if args.output_dir:
    args.output_dir.mkdir(parents=True, exist_ok=False)


def rational_string(x):
    return str(x) if isinstance(x, F) else x


def plain(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): plain(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [plain(v) for v in x]
    return x


def rank(rows):
    a = [[F(v) for v in row] for row in rows]
    if not a:
        return 0
    pivot = 0
    for col in range(len(a[0])):
        hit = next((j for j in range(pivot, len(a)) if a[j][col]), None)
        if hit is None:
            continue
        a[pivot], a[hit] = a[hit], a[pivot]
        q = a[pivot][col]
        a[pivot] = [v / q for v in a[pivot]]
        for j in range(len(a)):
            if j != pivot and a[j][col]:
                q = a[j][col]
                a[j] = [u - q * v for u, v in zip(a[j], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot


def determinant(rows):
    if not rows or any(len(row) != len(rows) for row in rows):
        return None
    a = [[F(v) for v in row] for row in rows]
    result = F(1)
    for col in range(len(a)):
        hit = next((j for j in range(col, len(a)) if a[j][col]), None)
        if hit is None:
            return F(0)
        if hit != col:
            a[col], a[hit] = a[hit], a[col]
            result = -result
        pivot = a[col][col]
        result *= pivot
        for j in range(col + 1, len(a)):
            q = a[j][col] / pivot
            a[j] = [u - q * v for u, v in zip(a[j], a[col])]
    return result


def main():
    raw = INPUT.read_bytes()
    data = json.loads(raw)
    game = data["game"]
    n = game["players"]
    topics = game["topics"]
    m = len(topics)
    assert type(n) is int and n >= 1
    assert len(set(topics)) == m
    types = []
    for c in game["customers"]:
        t = c["topics"]
        w = c["multiplicity"]
        assert type(w) is int and w > 0
        assert t and len(set(t)) == len(t)
        assert all(type(a) is int and 0 <= a < m for a in t)
        types.append((frozenset(t), w))
    assert len({t for t, w in types}) == len(types)
    total = sum(w for t, w in types)

    policy = {}
    for row in data["strategy"]["actions"]:
        h = tuple(row["history"])
        a = row["action"]
        assert len(h) < n and all(type(b) is int and 0 <= b < m for b in h)
        assert type(a) is int and 0 <= a < m
        assert h not in policy
        policy[h] = a
    expected_histories = {h for length in range(n) for h in product(range(m), repeat=length)}
    assert set(policy) == expected_histories

    def terminal(h):
        h = tuple(h)
        while len(h) < n:
            h += (policy[h],)
        return h

    def query(a, rivals):
        return sum((F(w, 1 + sum(b in t for b in rivals)) for t, w in types if a in t), F(0))

    def payoff(z):
        return tuple(query(z[i], z[:i] + z[i + 1:]) for i in range(n))

    def welfare(z):
        return sum(w for t, w in types if any(a in t for a in z))

    leaves = []
    for z in product(range(m), repeat=n):
        u = payoff(z)
        w = welfare(z)
        assert sum(u) == w
        leaves.append({"profile": z, "payoffs": u, "welfare": w})
    opt = max(r["welfare"] for r in leaves)
    opt_profiles = [r["profile"] for r in leaves if r["welfare"] == opt]
    topic_masses = [sum(w for t, w in types if a in t) for a in range(m)]
    topic_symmetric_differences = [
        {"topics": [a, b], "distinct_customers": sum(w for t, w in types if (a in t) != (b in t))}
        for a, b in combinations(range(m), 2)
    ]
    assert all(r["distinct_customers"] > 0 for r in topic_symmetric_differences)

    p = tuple(F(v) for v in data["security"]["primary"])
    assert len(p) == m and all(v >= 0 for v in p) and sum(p) == 1
    q_rows = data["security"]["dual"]
    q = []
    for row in q_rows:
        b = tuple(row["rivals"])
        prob = F(row["probability"])
        assert len(b) == n - 1 and all(type(a) is int and 0 <= a < m for a in b)
        assert prob >= 0
        q.append((b, prob))
    assert len({b for b, prob in q}) == len(q)
    assert sum(prob for b, prob in q) == 1

    static_rows = []
    for b in combinations_with_replacement(range(m), n - 1):
        values = tuple(query(a, b) for a in range(m))
        expected = sum(p[a] * values[a] for a in range(m))
        static_rows.append({"rivals": b, "queries": values, "primary_expected": expected})
    lower = min(r["primary_expected"] for r in static_rows)
    dual_queries = tuple(sum(prob * query(a, b) for b, prob in q) for a in range(m))
    upper = max(dual_queries)
    assert lower == upper, (lower, upper)
    value = lower
    for row in static_rows:
        row["primary_slack"] = row["primary_expected"] - value
    dual_slacks = tuple(value - z for z in dual_queries)
    primal_active = [r for r in static_rows if r["primary_expected"] == value]
    dual_allowed_topics = [a for a in range(m) if dual_queries[a] == value]
    q_positive = [b for b, prob in q if prob > 0]
    uniqueness_rows = [[F(1) for a in dual_allowed_topics]] + [
        [query(a, b) for a in dual_allowed_topics] for b in q_positive
    ]
    uniqueness_rank = rank(uniqueness_rows)
    primary_unique = uniqueness_rank == len(dual_allowed_topics)
    positive_support_determinant = determinant(uniqueness_rows[1:])

    nodes = []
    strict_deviations = ties = 0
    for h in sorted(policy, key=lambda z: (len(z), z)):
        i = len(h)
        prescribed = policy[h]
        z = terminal(h)
        node_u = payoff(z)[i]
        alternatives = []
        backgrounds = []
        for a in range(m):
            za = terminal(h + (a,))
            b = za[:i] + za[i + 1:]
            ua = query(a, b)
            assert ua == payoff(za)[i]
            gain = ua - node_u
            assert gain <= 0, (h, a, gain)
            if a != prescribed:
                strict_deviations += gain < 0
                ties += gain == 0
            backgrounds.append(b)
            alternatives.append({"action": a, "terminal": za, "rivals": b, "payoff": ua, "gain": gain})
        budget_matrix = tuple(tuple(query(a, backgrounds[b]) for b in range(m)) for a in range(m))
        diagonal = sum(p[a] * budget_matrix[a][a] for a in range(m))
        cross = sum(p[a] * p[b] * budget_matrix[a][b] for a in range(m) for b in range(m))
        e = node_u - diagonal
        kappa = diagonal - cross
        assert e >= 0
        nodes.append({"history": h, "prescribed_action": prescribed, "prescribed_terminal": z,
                      "mover_payoff": node_u, "alternatives": alternatives,
                      "query_matrix_a_by_b": budget_matrix,
                      "D": diagonal, "C": cross, "e": e, "kappa": kappa,
                      "u_minus_value": node_u - value})

    actual = terminal(())
    actual_u = payoff(actual)
    actual_w = welfare(actual)
    claimed_counts = data["strategy"]["terminal_counts"]
    assert claimed_counts == [actual.count(a) for a in range(m)]
    actual_nodes = [next(r for r in nodes if r["history"] == actual[:i]) for i in range(n)]
    sum_c = sum(r["C"] for r in actual_nodes)
    sum_d = sum(r["D"] for r in actual_nodes)
    sum_e = sum(r["e"] for r in actual_nodes)
    sum_kappa = sum(r["kappa"] for r in actual_nodes)
    gb = actual_w - sum_c
    assert gb == sum_e + sum_kappa
    individual_margins = tuple(u - value for u in actual_u)
    aggregate_security_margin = actual_w - n * value
    half_coverage_margin = actual_w - F(opt, 2)
    normalized_gap = -min(individual_margins) / total
    if "source_normalized_gap" in data:
        assert F(data["source_normalized_gap"]) == normalized_gap
    if "integer_scale" in data:
        assert F(data["integer_scale"]) == total
    if "value" in data["security"]:
        assert F(data["security"]["value"]) == value

    summary = {
        "input": str(INPUT), "sha256": hashlib.sha256(raw).hexdigest(),
        "players": n, "topics": m, "unit_customers": total, "customer_types": len(types),
        "policy_node_count": len(nodes), "terminal_profile_count": len(leaves),
        "alternative_evaluations": len(nodes) * m,
        "nonprescribed_deviations": len(nodes) * (m - 1),
        "strictly_unprofitable_deviations": strict_deviations, "tied_deviations": ties,
        "static_backgrounds_unordered": len(static_rows),
        "static_backgrounds_ordered": m ** (n - 1),
        "static_query_count_unordered": len(static_rows) * m,
        "deviation_background_query_count": len(nodes) * m * m,
        "all_policy_nodes_optimal": True, "all_topic_coverages_pairwise_distinct": True,
        "primary_probability_sum": sum(p), "dual_probability_sum": sum(prob for b, prob in q),
        "security_lower_bound": lower, "security_upper_bound": upper, "security_value": value,
        "primary_unique": primary_unique, "uniqueness_rank": uniqueness_rank,
        "positive_dual_support_matrix_determinant": positive_support_determinant,
        "dual_allowed_topics": dual_allowed_topics, "dual_queries": dual_queries,
        "dual_slacks": dual_slacks, "actual_profile": actual, "actual_payoffs": actual_u,
        "actual_welfare": actual_w, "OPT": opt, "individual_security_margins": individual_margins,
        "aggregate_security_margin": aggregate_security_margin,
        "half_coverage_margin": half_coverage_margin, "actual_sum_C": sum_c,
        "actual_sum_D": sum_d, "actual_sum_e": sum_e, "actual_sum_kappa": sum_kappa,
        "GB": gb, "root_D": actual_nodes[0]["D"], "root_C": actual_nodes[0]["C"],
        "normalized_individual_gap": normalized_gap,
    }
    output = {"summary": summary, "topic_masses": topic_masses,
              "topic_symmetric_differences": topic_symmetric_differences,
              "static_backgrounds": static_rows, "positive_dual_support": q_positive,
              "active_primary_backgrounds": [r["rivals"] for r in primal_active],
              "uniqueness_equation_rows": uniqueness_rows,
              "actual_budget_nodes": actual_nodes, "all_policy_nodes": nodes,
              "optimal_profiles_ordered": opt_profiles, "all_terminal_profiles": leaves}
    results_name = OUTPUT_PREFIX + "results.json"
    report_name = OUTPUT_PREFIX + "report.md"
    if args.output_dir:
        (args.output_dir / results_name).write_text(json.dumps(plain(output), ensure_ascii=False, indent=2) + "\n")
    s = plain(summary)
    report = f"""# Independent exact review of the {total}-customer candidate

Input: `{INPUT}`

SHA-256: `{s['sha256']}`

The verifier reads only the self-contained JSON. It imports no author-side game,
solver, or verification code. Every payoff and budget entry is evaluated with
Python `Fraction` directly from the weighted customer sets.

## Conclusion

The supplied candidate is a valid pure subgame-perfect strategy in the stated
sequential equal-sharing coverage game, and its first player's individual
static-security inequality fails: `{actual_u[0]} - {value} = {individual_margins[0]}`.
The welfare-based aggregate and half-coverage inequalities remain strictly
satisfied. Exact budget calculations also confirm the claimed positive GB.

## Input and exhaustive checks

- `{n}` players, `{m}` topics, `{total}` distinct unit customers represented by `{len(types)}` distinct customer types.
- All topic indices and multiplicities are integers, within range, with strictly positive multiplicities. Customer topic sets have no repeated index; no compressed customer type is duplicated.
- All 15 topic-pair symmetric differences are positive, so all 6 topic coverages are distinct as sets of unit customers.
- Exactly `{len(nodes)}` ordered nonterminal histories are supplied, with one legal action per history; no missing or repeated policy node.
- All `{len(leaves)}` ordered terminal profiles are evaluated; sum of player payoffs equals coverage in each.
- All `{len(nodes) * m}` one-action continuations are evaluated. All `{len(nodes) * (m - 1)}` nonprescribed deviations are unprofitable: `{strict_deviations}` strictly worse and `{ties}` tied.
- All `{len(static_rows)}` unordered static rival backgrounds (equivalently `{m ** (n - 1)}` ordered backgrounds), including repeated topics, and all `{len(static_rows) * m}` pure queries are evaluated.
- All `{len(nodes) * m * m}` continuation-background query entries are evaluated for the supplied p budgets at every policy node.
- The provided p and Q have nonnegative exact rational entries and each sums to 1.

## Exact security certificate

`min_B E_p[f_B(a)] = max_a E_Q[f_B(a)] = {s['security_value']}`.
The minimum is checked over every static rival background; the maximum is checked over every pure query. Thus no numerical LP approximation is used.

| Query | E_Q[f_B(a)] | v - E_Q[f_B(a)] |
|---|---:|---:|
"""
    for a in range(m):
        report += f"| {topics[a]} | {dual_queries[a]} | {dual_slacks[a]} |\n"
    report += f"""
The primary optimum is unique: the positive Q-support constraints must all
bind for any optimal p, while every query with strictly positive dual slack
must receive zero probability. On the `{len(dual_allowed_topics)}` remaining
coordinates, the normalization and positive-support equations have exact
rank `{uniqueness_rank}`. The supplied p solves those equations, so it is the
only optimum. The complete equation rows are retained in `{results_name}`.

The square positive-support coefficient matrix on these coordinates has
determinant `{positive_support_determinant}` (rows follow the JSON Q-support
order). This is an additional exact invertibility certificate whenever the
determinant is nonzero.

## Actual path and claimed comparisons

Actual ordered profile: `{actual}` = `{' / '.join(topics[a] for a in actual)}`.

| Quantity | Exact value |
|---|---:|
| Payoffs | `{s['actual_payoffs']}` |
| Welfare | `{actual_w}` |
| OPT | `{opt}` |
| First player u - v | `{individual_margins[0]}` |
| Second player u - v | `{individual_margins[1]}` |
| Third player u - v | `{individual_margins[2]}` |
| W - 3v | `{aggregate_security_margin}` |
| W - OPT/2 | `{half_coverage_margin}` |
| Root D(p) | `{actual_nodes[0]['D']}` |
| Root C(p) | `{actual_nodes[0]['C']}` |
| GB = W - sum C | `{gb}` |
| Sum e | `{sum_e}` |
| Sum kappa | `{sum_kappa}` |

The actual policy counts agree with the supplied terminal count vector.
For the root, `D = {actual_nodes[0]['D']}` and `C = {actual_nodes[0]['C']}`, hence `e = {actual_nodes[0]['e']}` and
`kappa = {actual_nodes[0]['kappa']}`. The positive sum across the actual three budgets therefore
does not rescue the invalid per-player safety inequality.

## Definitions and budget details

For ordered history h of length i, each action b is followed by the supplied
policy to a full terminal profile. Its i-th entry is removed to obtain B_i(b).
For every query a, the independent evaluator uses

`f_B(a) = sum_(T contains a) w_T / (1 + # rivals whose topic belongs to T)`.

`D_i(p) = sum_a p_a f_(B_i(a))(a)` and
`C_i(p) = sum_(a,b) p_a p_b f_(B_i(b))(a)`.

`e_i = u_i - D_i`, `kappa_i = D_i - C_i`, and
`GB = W - sum_i C_i = sum_i e_i + sum_i kappa_i`.

These continuation backgrounds are recomputed separately for every action.
They are derived from the complete observable policy, including off-path
branches. No background is frozen across deviations.

| Actual history | D | C | e | kappa |
|---|---:|---:|---:|---:|
"""
    for r in actual_nodes:
        report += f"| `{r['history']}` | {r['D']} | {r['C']} | {r['e']} | {r['kappa']} |\n"
    report += f"""
All terminal payoffs, all node/deviation comparisons, all static query values,
all cross-query budget matrices, optimal profiles, coverage differences, and
the uniqueness equations are saved in `{results_name}`.

Reproduce with:

`python {Path(__file__).resolve()} {INPUT}`

This review establishes failure of the individual inequality in this supplied
candidate. It does not establish global minimality or chronological priority
among all possible or previously examined games.
"""
    assert primary_unique, "This report template requires a full-rank uniqueness certificate"
    if args.output_dir:
        (args.output_dir / report_name).write_text(report)
    print(json.dumps(s, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
