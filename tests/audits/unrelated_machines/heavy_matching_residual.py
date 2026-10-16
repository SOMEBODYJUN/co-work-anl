#!/usr/bin/env python3
"""大边匹配残余过滤及容量逃逸反例的精确有限审计。

This is a necessary-condition filter, NOT a (2-epsilon) approximation.
None denotes a forbidden edge. Floats/bools are rejected. CLI only writes stdout.
The matching optimizer uses job weights and augmenting paths, not an LP oracle.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import importlib.util
import json
import platform
import random


def rational(value):
    if isinstance(value, (float, bool)):
        raise ValueError('Use exact rational numbers')
    try:
        return F(value)
    except (TypeError, ZeroDivisionError) as exc:
        raise ValueError('Invalid rational') from exc


def matrix(raw):
    if not raw or any(len(row) != len(raw[0]) for row in raw):
        raise ValueError('Need a rectangular matrix with at least one machine')
    p = [[None if v is None else rational(v) for v in row] for row in raw]
    if any(v is not None and v < 0 for row in p for v in row):
        raise ValueError('Negative time')
    if any(all(row[j] is None for row in p) for j in range(len(p[0]))):
        raise ValueError('A job has no finite edge')
    return p


def weighted_cover_matching(neighbors, mandatory, weights, forced=None):
    """Max optional job-weight matching covering mandatory, or None.

    neighbors: job -> iterable of machines; weights: optional job -> nonnegative
    rational reward. If forced=(j,i), j is mandatory and may use only i.
    Optional jobs and mandatory jobs must be disjoint (except forced is removed
    from optional). Returns {'weight': Fraction, 'assignment': job->machine}.
    """
    adj = {j: sorted(set(values)) for j, values in neighbors.items()}
    required = set(mandatory)
    optional = {j: rational(w) for j, w in weights.items()}
    if any(w < 0 for w in optional.values()):
        raise ValueError('Nonnegative optional weights required')
    if forced is not None:
        j, i = forced
        if i not in adj.get(j, ()):
            return None
        adj[j] = [i]
        required.add(j)
        optional.pop(j, None)
    if required & optional.keys():
        raise ValueError('Mandatory/optional overlap')
    if not (required | optional.keys()) <= adj.keys():
        raise ValueError('A matching job is missing from neighbors')
    matched = {}  # machine -> job

    def augment(start):
        queue, seen_jobs, previous = [start], {start}, {}
        free = None
        for j in queue:
            for i in adj[j]:
                if i in previous:
                    continue
                previous[i] = j
                if i not in matched:
                    free = i
                    break
                old = matched[i]
                if old not in seen_jobs:
                    seen_jobs.add(old)
                    queue.append(old)
            if free is not None:
                break
        if free is None:
            return False
        inverse = {j: i for i, j in matched.items()}
        while True:
            j = previous[free]
            old = inverse.get(j)
            matched[free] = j
            if old is None:
                return True
            free = old

    for j in sorted(required):
        if not augment(j):
            return None
    for j in sorted(optional, key=lambda j: (-optional[j], j)):
        augment(j)
    assignment = {j: i for i, j in matched.items()}
    assert required <= assignment.keys()
    if forced is not None:
        assert assignment[forced[0]] == forced[1]
    value = sum((optional.get(j, F(0)) for j in assignment), F(0))
    return {'weight': value, 'assignment': assignment}


def filter_domains(raw, target, include_mandatory=True):
    """GHMR fixed point. Local variant omits other mandatory-big jobs.

    Output feasible=True means only 'not rejected'; it is NOT feasibility.
    All deletions are simultaneous per round. Only big edges can be removed.
    Empty/zero inputs are accepted as necessary tests, with no division by T.
    """
    p, t = matrix(raw), rational(target)
    if t < 0:
        raise ValueError('Negative target')
    m, n = len(p), len(p[0])
    domains = [{i for i in range(m) if p[i][j] is not None and p[i][j] <= t}
               for j in range(n)]
    trace, rounds = [], 0
    while True:
        if any(not domain for domain in domains):
            return {'feasible': False, 'domains': domains, 'trace': trace,
                    'rounds': rounds, 'reason': 'empty_domain'}
        small = [{i for i in domains[j] if 2*p[i][j] <= t} for j in range(n)]
        mandatory = {j for j in range(n) if not small[j]}
        big = {j: sorted(i for i in domains[j] if 2*p[i][j] > t) for j in range(n)}
        if include_mandatory and weighted_cover_matching(big, mandatory, {}) is None:
            return {'feasible': False, 'domains': domains, 'trace': trace,
                    'rounds': rounds, 'reason': 'mandatory_matching'}
        unique = [{j for j in range(n) if small[j] == {i}} for i in range(m)]
        totals = [sum((p[i][j] for j in unique[i]), F(0)) for i in range(m)]
        remove = []
        for j in range(n):
            for i in big[j]:
                result = weighted_cover_matching(
                    big, mandatory if include_mandatory else set(),
                    {s: p[i][s] for s in unique[i]}, (j, i))
                if result is None:
                    remove.append((j, i, 'no_matching', None))
                elif p[i][j]+totals[i]-result['weight'] > t:
                    remove.append((j, i, 'residual_load', result['weight']))
        rounds += 1
        if not remove:
            return {'feasible': True, 'domains': domains, 'trace': trace,
                    'rounds': rounds, 'reason': 'fixed_point'}
        for j, i, reason, weight in remove:
            domains[j].remove(i)
            trace.append({'job': j, 'machine': i, 'round': rounds,
                          'reason': reason, 'weight': None if weight is None else str(weight)})


def height(k):
    if type(k) is not int or k < 2:
        raise ValueError('integer k>=2')
    h, a = 1, F(1, k-1)
    while a < F(1, 2):
        h, a = h+1, a*F(k, k-1)
    return h, a


def escape_instance(k, escape=True):
    """Expanded path-terminal tree, with optional 1/2 escape machine.

    Expansion capped at k=4; the general lower bound is a mathematical proof,
    not an output of materializing huge instances.
    """
    if type(k) is not int or not 2 <= k <= 4:
        raise ValueError('Materialization limited to integer 2<=k<=4')
    h, _ = height(k)
    edges, configs, groups = [], [], []

    def node():
        configs.append([])
        return len(configs)-1

    def edge(times):
        edges.append(times)
        return len(edges)-1

    roots = [node(), node()]
    central = edge({roots[0]: F(1), roots[1]: F(1)})
    z = node() if escape else None
    if escape:
        configs[z] = [(F(1), ())]

    def subtree(root, depth, incoming):
        if depth == 1:
            terminals = [node() for _ in range(k)]
            children = [edge({root: F(1,k), v: F(1)}) for v in terminals]
            reserve = [edge({terminals[l]: F(1), terminals[l+1]: F(1),
                             **({z: F(1,2)} if escape else {})}) for l in range(k-1)]
            for l, v in enumerate(terminals):
                terms = [(F(1,k), (children[l],))]
                if l:
                    terms.append((F(l,k), (reserve[l-1],)))
                if l < k-1:
                    terms.append((F(k-l-1,k), (reserve[l],)))
                configs[v] = terms
            groups.append({'parent': root, 'terminals': terminals,
                           'stars': children, 'reserve': reserve})
            a = F(1,k-1)
        else:
            children = []
            for _ in range(k):
                child = node()
                j = edge({root: F(1,k), child: F(1)})
                children.append(j)
                child_a = subtree(child, depth-1, j)
            a = child_a*F(k,k-1)
        configs[root] = [(1-a, tuple(children))] + [(a/k, (incoming,j)) for j in children]
        return a

    for root in roots:
        a = subtree(root, h, central)
        thinned = []
        for weight, jobs in configs[root]:
            if central in jobs:
                thinned += [(weight/(2*a), jobs),
                            (weight*(1-1/(2*a)), tuple(j for j in jobs if j != central))]
            else:
                thinned.append((weight, jobs))
        configs[root] = [(w, jobs) for w, jobs in thinned if w]
    p = [[times.get(i) for times in edges] for i in range(len(configs))]
    return p, configs, 1+F(1,k), {'roots': roots, 'central': central, 'escape': z, 'groups': groups}


def check_configurations(p, configs, target):
    totals = [F(0)]*len(p[0])
    for i, terms in enumerate(configs):
        assert sum((w for w, _ in terms), F(0)) == 1
        for w, jobs in terms:
            assert w >= 0 and len(set(jobs)) == len(jobs)
            assert all(p[i][j] is not None for j in jobs)
            assert sum((p[i][j] for j in jobs), F(0)) <= target
            for j in jobs:
                totals[j] += w
    assert all(value == 1 for value in totals)


def audit():
    seed = 20261016
    rng = random.Random(seed)
    matrices = tested = feasible_schedules = 0
    # Independent schedule enumeration checks edge preservation, not just OPT.
    for flat in product((None, 0, 1, 2), repeat=6):
        p = [list(flat[:3]), list(flat[3:])]
        choices = [[i for i in range(2) if p[i][j] is not None] for j in range(3)]
        if any(not c for c in choices):
            continue
        matrices += 1
        schedules = [(s, max(sum(p[i][j] for j in range(3) if s[j] == i)
                                 for i in range(2))) for s in product(*choices)]
        for t in range(5):
            tested += 1
            result = filter_domains(p, t)
            for s, value in schedules:
                if value <= t:
                    feasible_schedules += 1
                    assert result['feasible']
                    assert all(s[j] in result['domains'][j] for j in range(3))
    random_cases = 120
    for _ in range(random_cases):
        m, n = rng.randrange(1, 5), rng.randrange(0, 7)
        p = [[None if rng.randrange(5) == 0 else F(rng.randrange(7), rng.randrange(1,7))
              for _ in range(n)] for _ in range(m)]
        for j in range(n):
            if all(p[i][j] is None for i in range(m)):
                p[0][j] = F(0)
        t = F(rng.randrange(10), rng.randrange(1,5))
        result = filter_domains(p, t)
        choices = [[i for i in range(m) if p[i][j] is not None] for j in range(n)]
        for s in product(*choices):
            if max(sum((p[i][j] for j in range(n) if s[j] == i), F(0)) for i in range(m)) <= t:
                assert result['feasible'] and all(s[j] in result['domains'][j] for j in range(n))
    boundary = [([[]], 0), ([[0,0], [0,0]], 0),
                ([[F(1,2**127-1)]], F(1,2**127-1)), ([[1], [None]], 1),
                ([[0, 1], [1, 0]], 0)]
    for p, t in boundary:
        assert filter_domains(p, t)['feasible']
    invalid = [([], 0), ([[None]], 0), ([[-1]], 0), ([[1.0]], 1),
               ([[1]], True), ([[0]], -1), ([[False]], 0)]
    for p, t in invalid:
        try:
            filter_domains(p, t)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid accepted')
    spec = importlib.util.spec_from_file_location('old_gap', Path(__file__).with_name('rounding_and_gap.py'))
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    k = 4
    original, _, t = old.gap_instance(k)
    original_result = filter_domains(original, t)
    assert not original_result['feasible']
    assert filter_domains(original, F(2*k-1,k))['feasible']
    path, cert, t, metadata = escape_instance(k, False)
    check_configurations(path, cert, t)
    local = filter_domains(path, t, include_mandatory=False)
    global_result = filter_domains(path, t)
    assert local['feasible'] and not local['trace']
    assert not global_result['feasible']
    escaped, cert, t, metadata = escape_instance(k, True)
    check_configurations(escaped, cert, t)
    escaped_result = filter_domains(escaped, t)
    assert escaped_result['feasible'] and not escaped_result['trace']
    # Check formulae and branching at many k; no expanded OPT enumeration here.
    parameters = []
    for k in range(4, 65):
        h, a = height(k)
        assert h >= 3 and F(k, (k-1)**2) < F(1,2)
        opt, target = F(2*k-1,k), 1+F(1,k)
        ratio = opt/target
        assert ratio == 2-F(3,k+1) and ratio*target == opt
        for b in (target, opt-F(1,100*k)):
            kept = min(k, (k*(b-1)).numerator//(k*(b-1)).denominator)
            assert k-kept >= 2
            assert F(1,2)*2**(h-1) >= 2 > b
        parameters.append({'k': k, 'h': h, 'optimum': str(opt),
                           'configuration_target': str(target), 'ratio_lower_bound': str(ratio)})
    return {'schema_version': 1, 'python_version': platform.python_version(), 'seed': seed,
            'arithmetic': 'Fraction/integer; no floating point or generic LP solver',
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'matrix_count': matrices, 'threshold_tests': tested,
            'preserved_feasible_schedules_with_threshold_multiplicity': feasible_schedules,
            'random_rational_cases': random_cases, 'boundary_cases': len(boundary),
            'rejected_invalid_cases': len(invalid),
            'expanded_k4': {'original_rejected': not original_result['feasible'],
                            'path_only_local_survives': local['feasible'],
                            'path_only_global_rejected': not global_result['feasible'],
                            'escape_machines': len(escaped), 'escape_jobs': len(escaped[0]),
                            'escape_deleted_edges': len(escaped_result['trace']),
                            'escape_configuration_checked': True},
            'compressed_parameters': parameters,
            'limits': ['No universal approximation algorithm or feasible-schedule output is supplied.',
                       'Only k=4 expanded; k=4..64 formula checks do not enumerate schedules.',
                       'Optimizer oracle cross-check and independent family reconstruction are separate.',
                       'Counterexample concerns separate configuration feasibility and this exact filter, not a coupled hierarchy.']}


if __name__ == '__main__':
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
