"""Unit-customer reconciliation of the two fixed uniform-background witnesses.

Reads only literal input dictionaries from the preserved original audit;
does not import its payoff or policy code, a solver, or a discovery routine.
Exports every actual history/action comparison, including ties and repeats.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import ast
import json

HERE = Path(__file__).resolve().parent


def policy(h):
    if not h:
        return 0
    if len(h) == 1:
        return 3 if h[0] in (0, 1, 2) else 0
    group = (0, 1, 2) if h[1] in (0, 1, 2) else (3, 4, 5)
    return min(a for a in group if a not in h)


def finish(h):
    while len(h) < 3:
        h += (policy(h),)
    return h


def audit(weights):
    units = tuple((mask, j) for mask, w in sorted(weights.items()) for j in range(w))
    topics = tuple(frozenset(u for u in units if u[0] >> a & 1) for a in range(6))

    def own(z, i):
        return sum((F(1, sum(x in topics[a] for a in z)) for x in topics[z[i]]), F())

    def welfare(z):
        return len(set().union(*(topics[a] for a in z)))

    rows = []
    for depth in range(3):
        for h in product(range(6), repeat=depth):
            chosen = finish(h)
            for a in range(6):
                alternative = finish(h+(a,))
                gap = own(chosen, depth)-own(alternative, depth)
                assert gap >= 0
                rows.append(dict(history=h, prescribed_action=policy(h),
                    prescribed_profile=chosen, prescribed_payoff=own(chosen, depth),
                    alternative_action=a, alternative_profile=alternative,
                    alternative_payoff=own(alternative, depth), gap=gap))
    q_uniform = (F(1, 6),)*6
    q_free = (F(1, 4), F(1, 8), F(1, 8), F(1, 4), F(1, 8), F(1, 8))

    def query_values(q):
        return tuple(sum((F(1)/(1+2*sum(q[b] for b in range(6) if x in topics[b]))
                          for x in topics[a]), F()) for a in range(6))

    actual = finish(())
    W = welfare(actual)
    optimum = max(welfare(z) for z in product(range(6), repeat=3))
    return dict(unit_clients=len(units), weights=weights,
        unit_customer_topics=[dict(customer=x, topics=tuple(a for a in range(6) if x in topics[a])) for x in units],
        topic_customer_sets=[sorted(T) for T in topics],
        label_equivalence_classes=[[b for b in range(6) if topics[b] == topics[a]]
                                  for a in range(6) if a == min(b for b in range(6) if topics[b] == topics[a])],
        distinct_physical_topics=len(set(topics)), complete_policy=[dict(history=h, action=policy(h))
            for depth in range(3) for h in product(range(6), repeat=depth)],
        comparisons=rows, comparison_count=len(rows), strict=sum(r['gap'] > 0 for r in rows),
        ties=sum(r['gap'] == 0 for r in rows), actual=actual,
        utilities=tuple(own(actual, i) for i in range(3)), welfare=W, OPT=optimum,
        q_uniform=q_uniform, query_uniform=query_values(q_uniform),
        q_free=q_free, query_free=query_values(q_free))


def main():
    tree = ast.parse((HERE/'original/audit_uniform_fractional_obstruction.py').read_text())
    literal = {node.targets[0].id: ast.literal_eval(node.value)
               for node in tree.body if isinstance(node, ast.Assign)
               and isinstance(node.targets[0], ast.Name)
               and node.targets[0].id in ('base', 'w34')}
    base = literal['base']
    combined = dict(literal['w34'])
    for mask, w in base.items():
        combined[mask] = combined.get(mask, 0)+10*w
    small, canonical = audit(base), audit(combined)
    assert small['label_equivalence_classes'] == [[0, 3], [1], [2, 5], [4]]
    assert canonical['distinct_physical_topics'] == 6
    assert small['utilities'] == (F(1),)*3
    assert canonical['utilities'] == (F(59, 3), F(127, 6), F(127, 6))
    assert (small['welfare'], small['OPT']) == (3, 4)
    assert (canonical['welfare'], canonical['OPT']) == (62, 73)
    assert canonical['query_uniform'][0] == F(303, 14)
    assert max(canonical['query_free']) == F(3188, 165)
    report = dict(status='exact_pass', five_client_label_extension=small,
        eighty_four_client_distinct_catalog=canonical,
        scope='Full unit-customer fixed-input reconciliation. The5-unit script has6 aliases but only4 physical sets; the84-unit catalog has6 distinct physical sets. No quotient strategy or arbitrary optimized fractional value is certified.')
    (HERE/'unit-tables.json').write_text(json.dumps(report, default=str, ensure_ascii=False, indent=2)+'\n')
    exact_stdout = [ast.literal_eval(s) for s in (HERE/'replay/exact/stdout.txt').read_text().splitlines()]
    (HERE/'exact-replay.json').write_text(json.dumps(exact_stdout, ensure_ascii=False, indent=2)+'\n')
    discovery = []
    for line in (HERE/'replay/discovery/stdout.txt').read_text().splitlines():
        a, objective, weights = line.split(' ', 2)
        discovery.append(dict(query=int(a), maximum_gap_float=float(objective),
                              positive_type_weights=ast.literal_eval(weights)))
    (HERE/'discovery-replay.json').write_text(json.dumps(dict(
        status='numerical-discovery-only', rows=discovery,
        scope='Six original fixed-uniform-q floating LP outputs; unrounded float data preserved. No rational saddle or general cone optimality proof.'), ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(dict(status='exact_pass', physical_topic_counts=[4, 6],
        comparison_counts=[small['comparison_count'], canonical['comparison_count']],
        strict=[small['strict'], canonical['strict']], ties=[small['ties'], canonical['ties']],
        W=[3, 62], OPT=[4, 73])))


if __name__ == '__main__':
    main()
