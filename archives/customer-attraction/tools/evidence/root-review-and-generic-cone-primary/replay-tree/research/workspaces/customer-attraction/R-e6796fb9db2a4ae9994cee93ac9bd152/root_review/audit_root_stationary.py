"""Independent unit-customer audit of the weak root-stationary kernel.

Reads only the already published closed strategy automaton. Does not import
the discovering agent's code, the canonical model, or a numerical optimizer.
"""
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from math import lcm
from pathlib import Path
import gzip
import json

ROOT = Path(__file__).resolve().parents[5]
SOURCE = ROOT / 'research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz'


def unique_solution(rows, variables):
    """Exact reduced row elimination, including all redundant equations."""
    rows = [list(map(F, r)) for r in rows]
    rank = 0
    pivots = []
    for col in range(variables):
        pivot = next((i for i in range(rank,len(rows)) if rows[i][col]),None)
        if pivot is None:
            continue
        rows[rank],rows[pivot] = rows[pivot],rows[rank]
        scale = rows[rank][col]
        rows[rank] = [x/scale for x in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][col]:
                scale = rows[i][col]
                rows[i] = [x-scale*y for x,y in zip(rows[i],rows[rank])]
        pivots.append(col)
        rank += 1
    assert all(any(row[:-1]) or row[-1] == 0 for row in rows)
    assert rank == variables, 'Stationary probability is not unique'
    answer = [F(0)]*variables
    for i,j in enumerate(pivots):
        answer[j] = rows[i][-1]
    return tuple(answer),rank


def main():
    raw = SOURCE.read_bytes()
    packet = json.loads(gzip.decompress(raw))
    instance = packet['instance']
    m = instance['players']
    p = len(instance['topics'])
    customers = tuple(frozenset(c['topics']) for c in instance['customers']
                      for _ in range(c['multiplicity']))
    nodes = packet['nodes']
    root = packet['root']
    assert nodes[root]['counts'] == [0]*p
    seen = set()
    stack = [root]
    while stack:
        v = stack.pop()
        if v in seen:
            continue
        seen.add(v)
        node = nodes[v]
        q = node['counts']
        assert len(q) == p and all(type(x) is int and x >= 0 for x in q)
        assert sum(q) <= m
        if sum(q) == m:
            assert node['terminal'] is True and 'children' not in node
            continue
        assert len(node['children']) == p and node['action'] in range(p)
        for a,w in enumerate(node['children']):
            target = [x+int(j==a) for j,x in enumerate(q)]
            assert nodes[w]['counts'] == target
            stack.append(w)
    assert len(seen) == len(nodes)
    denominator = lcm(*range(1,m+1))

    @lru_cache(None)
    def pay(q,a):
        total = 0
        for B in customers:
            if a in B:
                load = sum(q[b] for b in B)
                assert load > 0
                total += denominator//load
        return total

    outcomes = {}
    true_deviations = 0
    for v in sorted(seen,key=lambda v:sum(nodes[v]['counts']),reverse=True):
        node = nodes[v]
        if sum(node['counts']) == m:
            outcomes[v] = tuple(node['counts'])
            continue
        a = node['action']
        outcomes[v] = outcomes[node['children'][a]]
        actual = pay(outcomes[v],a)
        for b,w in enumerate(node['children']):
            assert actual >= pay(outcomes[w],b)
            true_deviations += int(a != b)

    q = outcomes[root]
    W = sum(any(q[b] for b in B) for B in customers)
    tails = []
    for a,w in enumerate(nodes[root]['children']):
        tail = tuple(x-int(j==a) for j,x in enumerate(outcomes[w]))
        assert min(tail) >= 0 and sum(tail) == m-1
        tails.append(tail)
    K = tuple(tuple(F(x,m-1) for x in tail) for tail in tails)
    equations = [[K[a][b]-int(a==b) for a in range(p)]+[F(0)] for b in range(p)]
    equations.append([F(1)]*p+[F(1)])
    pi,rank = unique_solution(equations,p)
    assert all(x >= 0 for x in pi) and sum(pi)==1
    assert all(sum(pi[a]*K[a][b] for a in range(p))==pi[b] for b in range(p))
    query_values = []
    for t in range(p):
        value = sum((pi[a]*sum((F(1,1+sum(tails[a][b] for b in B))
                     for B in customers if t in B),F(0)) for a in range(p)),F(0))
        query_values.append(value)
    cap = max(query_values)
    weak_bound = F(2*W,2*m-1)
    assert cap > weak_bound
    # Unrestricted legal static backgrounds still pay genuine security.
    H = (1,1,1,0,0,9)
    assert sum(H) == m-1
    safe = tuple(sum((F(1,1+sum(H[b] for b in B)) for B in customers if t in B),F(0)) for t in range(p))
    assert max(safe) == F(5,2) and m*max(safe) <= W
    report = {'status':'exact independent audit passed','source':str(SOURCE.relative_to(ROOT)),
        'source_sha256':sha256(raw).hexdigest(),'players':m,'unit_customers':len(customers),
        'reachable_automaton_nodes':len(seen),'checked_true_deviations':true_deviations,
        'actual_counts':q,'W':W,'root_tail_counts':tails,
        'stationary_probability':[str(x) for x in pi],'augmented_rank':rank,
        'queries':dict(zip(instance['topics'],map(str,query_values))),
        'cap':str(cap),'weak_bound_W_over_m_minus_half':str(weak_bound),
        'exact_weak_violation':str(cap-weak_bound),'unrestricted_safe_background':H,
        'unrestricted_query_values':[str(x) for x in safe],
        'scope':'Only prescribed root stationary kernel is refuted; true security and half are not refuted'}
    output = Path(__file__).with_name('root_stationary_audit.json')
    with output.open('x') as stream:
        json.dump(report,stream,ensure_ascii=False,indent=2)
        stream.write('\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
