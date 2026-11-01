#!/usr/bin/env python3
"""行均匀相关读出：整数势下降、全局匹配与实际不相关机调度。

An explicit simple bipartite graph has left labels and total edge maps.  At a
right vertex v, every edge map is uniform onto the q_v = deg(v) resources.
One label controls all incident requests of a left vertex.  No independent
choice per edge is permitted.  The production constructor uses integer
arithmetic and matching; the audit alone enumerates small label profiles and
some complete schedules.  This is a restricted-class 3/2 absolute bound.
"""
from collections import Counter, deque
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json
import sys


if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)


def validate(data):
    """Validate only explicit, finite, simple, exactly row-uniform input."""
    if type(data) is not dict or set(data) != {'left', 'right', 'edges'}:
        raise ValueError('exact left/right/edges keys required')
    if any(type(data[k]) is not list for k in data):
        raise ValueError('explicit lists required')
    left, right, edges = data['left'], data['right'], data['edges']
    uid, vid, labels = {}, {}, []
    for u, row in enumerate(left):
        if type(row) is not dict or set(row) != {'id', 'labels'}:
            raise ValueError('exact left id/labels keys required')
        if type(row['id']) is not str or row['id'] in uid:
            raise ValueError('distinct string left ids required')
        aa = row['labels']
        if (type(aa) is not list or not aa or
                any(type(a) is not str for a in aa) or len(set(aa)) != len(aa)):
            raise ValueError('nonempty distinct explicit string labels required')
        uid[row['id']] = u
        labels.append(tuple(aa))
    for v, row in enumerate(right):
        if type(row) is not dict or set(row) != {'id'}:
            raise ValueError('exact right id key required')
        if type(row['id']) is not str or row['id'] in vid:
            raise ValueError('distinct string right ids required')
        vid[row['id']] = v
    incidence = [[] for _ in left]
    q = [0 for _ in right]
    parsed, seen = [], set()
    for e, row in enumerate(edges):
        if type(row) is not dict or set(row) != {'u', 'v', 'map'}:
            raise ValueError('exact edge u/v/map keys required')
        if type(row['u']) is not str or row['u'] not in uid:
            raise ValueError('unknown left endpoint')
        if type(row['v']) is not str or row['v'] not in vid:
            raise ValueError('unknown right endpoint')
        u, v = uid[row['u']], vid[row['v']]
        if (u, v) in seen:
            raise ValueError('parallel (u,v) edges forbidden')
        seen.add((u, v))
        mapping = row['map']
        if type(mapping) is not dict or set(mapping) != set(labels[u]):
            raise ValueError('edge map must be total on exactly the left labels')
        if any(type(r) is not int for r in mapping.values()):
            raise ValueError('resource indices must be exact integers')
        parsed.append({'u': u, 'v': v,
                       'map': tuple(mapping[a] for a in labels[u])})
        incidence[u].append(e)
        q[v] += 1
    resource_ids = {}
    resources = []
    for v, degree in enumerate(q):
        for r in range(degree):
            resource_ids[v, r] = len(resources)
            resources.append((v, r))
    for edge in parsed:
        degree = q[edge['v']]
        counts = Counter(edge['map'])
        if (any(not 0 <= r < degree for r in edge['map']) or
                len(labels[edge['u']]) % degree or
                any(counts[r] != len(labels[edge['u']]) // degree
                    for r in range(degree))):
            raise ValueError('edge map is not uniform onto all right resources')
        edge['resources'] = tuple(resource_ids[edge['v'], r]
                                  for r in edge['map'])
    return {'data': data, 'labels': labels, 'edges': parsed,
            'incidence': incidence, 'q': q, 'resources': resources}


def request_loads(instance, chosen):
    loads = [0] * len(instance['resources'])
    for edge in instance['edges']:
        loads[edge['resources'][chosen[edge['u']]]] += 1
    return loads


def potential(loads):
    return sum(c * (c - 1) // 2 for c in loads)


def stabilize(instance):
    """Strict integer-potential best responses, in explicit input order.

    Only genuine changes with lower integer potential are executed.  The
    potential starts at most sum_v binom(q_v, 2), so moves and full passes are
    polynomial in the explicit input length.  Label ties retain the old label.
    """
    chosen = [0] * len(instance['labels'])
    loads = request_loads(instance, chosen)
    initial = potential(loads)
    trace, passes = [], 0
    while True:
        passes += 1
        changed = False
        for u, incident in enumerate(instance['incidence']):
            old = chosen[u]
            for e in incident:
                loads[instance['edges'][e]['resources'][old]] -= 1
            scores = [sum(loads[instance['edges'][e]['resources'][a]]
                          for e in incident)
                      for a in range(len(instance['labels'][u]))]
            best = min(range(len(scores)), key=lambda a: (scores[a], a))
            if scores[best] < scores[old]:
                trace.append({'u': u, 'old': old, 'new': best,
                              'potential_drop': scores[old] - scores[best]})
                chosen[u] = best
                changed = True
            for e in incident:
                loads[instance['edges'][e]['resources'][chosen[u]]] += 1
        if not changed:
            break
    final = potential(loads)
    if initial - final != sum(t['potential_drop'] for t in trace):
        raise RuntimeError('integer potential accounting failed')
    costs, shares = [], []
    for u, incident in enumerate(instance['incidence']):
        active = [instance['edges'][e]['resources'][chosen[u]] for e in incident]
        cost = sum(loads[r] - 1 for r in active)
        share = sum((Fraction(1, loads[r]) for r in active), Fraction(0))
        d = len(incident)
        if d and (cost > d - 1 or share < Fraction(d + 1, 2)):
            raise RuntimeError('stable integer row inequality failed')
        costs.append(cost)
        shares.append(share)
    return {'chosen': chosen, 'request_loads': loads, 'costs': costs,
            'shares': shares, 'initial_potential': initial,
            'final_potential': final, 'moves': trace, 'passes': passes,
            'potential_bound': sum(x * (x - 1) // 2 for x in instance['q'])}


def covering_matching(adj, resource_count):
    """Deterministic augmenting paths; no flow or LP oracle is used."""
    slot_owner = [-1] * resource_count
    assigned = [-1] * len(adj)
    for start in range(len(adj)):
        queue, previous, seen = deque([start]), {start: None}, set()
        last = None
        while queue and last is None:
            u = queue.popleft()
            for r in adj[u]:
                if r in seen:
                    continue
                seen.add(r)
                old_owner = slot_owner[r]
                if old_owner < 0:
                    last = (u, r)
                    break
                if old_owner not in previous:
                    previous[old_owner] = (u, r)
                    queue.append(old_owner)
        if last is None:
            raise RuntimeError('proved Hall matching failed')
        u, r = last
        while True:
            assigned[u], slot_owner[r] = r, u
            if previous[u] is None:
                break
            u, r = previous[u]
    if len(set(assigned)) != len(assigned):
        raise RuntimeError('resource matching repeated a resource')
    return assigned


def compile_instance(instance):
    """List every original selector and every state-edge port explicitly."""
    machines, parent, external = [], {}, {}
    for u, aa in enumerate(instance['labels']):
        for a, label in enumerate(aa):
            parent[u, a] = len(machines)
            machines.append({'kind': 'parent', 'u': u, 'label': label})
    for r, (v, unit) in enumerate(instance['resources']):
        external[r] = len(machines)
        machines.append({'kind': 'resource', 'v': v, 'unit': unit})
    if not machines:
        machines.append({'kind': 'dummy'})
    jobs, selectors, ports = [], {}, {}
    for u, aa in enumerate(instance['labels']):
        selectors[u] = len(jobs)
        jobs.append({'kind': 'selector', 'u': u,
                     'eligible': [(parent[u, a], Fraction(1))
                                  for a in range(len(aa))]})
        d = len(instance['incidence'][u])
        for a in range(len(aa)):
            for e in instance['incidence'][u]:
                r = instance['edges'][e]['resources'][a]
                ports[u, a, e] = len(jobs)
                jobs.append({'kind': 'port', 'u': u, 'label': a, 'edge': e,
                             'eligible': [(parent[u, a], Fraction(1, d)),
                                          (external[r], Fraction(1))]})
    return {'machines': machines, 'jobs': jobs, 'parent': parent,
            'external': external, 'selectors': selectors, 'ports': ports}


def actual_loads(compiled, sigma):
    """Independently evaluate all original jobs on their selected finite edges."""
    if type(sigma) is not list or len(sigma) != len(compiled['jobs']):
        raise ValueError('a machine for every original job is required')
    loads = [Fraction(0) for _ in compiled['machines']]
    for job, machine in zip(compiled['jobs'], sigma):
        if type(machine) is not int or not 0 <= machine < len(loads):
            raise ValueError('invalid output machine')
        finite = dict(job['eligible'])
        if machine not in finite:
            raise ValueError('output uses an unavailable original edge')
        loads[machine] += finite[machine]
    return loads


def solve(data):
    instance = validate(data)
    stable = stabilize(instance)
    chosen = stable['chosen']
    adj, copies = [], []
    for u, incident in enumerate(instance['incidence']):
        neighbors = [instance['edges'][e]['resources'][chosen[u]] for e in incident]
        for _ in range((len(incident) + 1) // 2):
            copies.append(u)
            adj.append(neighbors)
    assigned = covering_matching(adj, len(instance['resources']))
    selected = [[] for _ in instance['labels']]
    for u, r in zip(copies, assigned):
        es = [e for e in instance['incidence'][u]
              if instance['edges'][e]['resources'][chosen[u]] == r]
        if len(es) != 1:
            raise RuntimeError('simple graph did not identify one selected port')
        selected[u].append(es[0])
    compiled = compile_instance(instance)
    sigma = [-1] * len(compiled['jobs'])
    for u, aa in enumerate(instance['labels']):
        sigma[compiled['selectors'][u]] = compiled['parent'][u, chosen[u]]
        for a in range(len(aa)):
            for e in instance['incidence'][u]:
                j = compiled['ports'][u, a, e]
                if a == chosen[u] and e in selected[u]:
                    r = instance['edges'][e]['resources'][a]
                    sigma[j] = compiled['external'][r]
                else:
                    sigma[j] = compiled['parent'][u, a]
    loads = actual_loads(compiled, sigma)
    makespan = max(loads, default=Fraction(0))
    if makespan > Fraction(3, 2):
        raise RuntimeError('actual complete schedule exceeded three halves')
    return {'labels': [aa[a] for aa, a in zip(instance['labels'], chosen)],
            'selected_edges': selected, 'selected_resources': assigned,
            'stable': stable, 'sigma': sigma, 'loads': loads,
            'makespan': makespan, 'bound': Fraction(3, 2),
            'machines': compiled['machines'], 'jobs': compiled['jobs']}


def jsonable(x):
    if isinstance(x, Fraction):
        return str(x)
    if type(x) is dict:
        return {str(k): jsonable(v) for k, v in x.items()}
    if type(x) in (tuple, list):
        return [jsonable(v) for v in x]
    return x


def make_example(nu, nv, pairs, label_count, shifts=None):
    q = Counter(v for u, v in pairs)
    left = [{'id': f'u{u}', 'labels': [f'a{a}' for a in range(label_count)]}
            for u in range(nu)]
    if shifts is None:
        shifts = [0] * len(pairs)
    return {'left': left, 'right': [{'id': f'v{v}'} for v in range(nv)],
            'edges': [{'u': f'u{u}', 'v': f'v{v}',
                       'map': {f'a{a}': (a + shifts[e]) % q[v]
                               for a in range(label_count)}}
                      for e, (u, v) in enumerate(pairs)]}


def independent_profile_check(instance, chosen):
    """Brute-force stability and every left-subset Hall inequality."""
    n = len(instance['labels'])
    requests = [[instance['edges'][e]['resources'][chosen[u]]
                 for e in instance['incidence'][u]] for u in range(n)]
    flat = [r for rr in requests for r in rr]
    loads = Counter(flat)
    phi = sum(Fraction(count * (count - 1), 2) for count in loads.values())
    stable = True
    for u, aa in enumerate(instance['labels']):
        for a in range(len(aa)):
            new_profile = list(chosen)
            new_profile[u] = a
            other_flat = [instance['edges'][e]['resources'][new_profile[edge['u']]]
                          for e, edge in enumerate(instance['edges'])]
            new_counts = Counter(other_flat)
            new_phi = sum(Fraction(c * (c - 1), 2) for c in new_counts.values())
            if new_phi < phi:
                stable = False
    if stable:
        for mask in range(1 << n):
            us = [u for u in range(n) if mask >> u & 1]
            neighborhood = {r for u in us for r in requests[u]}
            demand = sum((len(requests[u]) + 1) // 2 for u in us)
            if len(neighborhood) < demand:
                raise RuntimeError('independent stable Hall subset failed')
        for u, rr in enumerate(requests):
            if rr and sum((Fraction(1, loads[r]) for r in rr), Fraction(0)) < Fraction(len(rr) + 1, 2):
                raise RuntimeError('independent stable per-row share failed')
    return stable


def brute_complete_opt(compiled):
    """An independent audit oracle, never called by the production solver."""
    choices = [[m for m, p in job['eligible']] for job in compiled['jobs']]
    best, examined = None, 0
    for sigma in product(*choices):
        examined += 1
        loads = [Fraction(0)] * len(compiled['machines'])
        for j, m in enumerate(sigma):
            p = next(p for k, p in compiled['jobs'][j]['eligible'] if k == m)
            loads[m] += p
        value = max(loads, default=Fraction(0))
        if best is None or value < best:
            best = value
    return best, examined


def audit():
    cases = []
    # All simple 2-by-3 graphs, all shift maps on their degree-two rows.
    # Each right vertex independently has no edge, either single edge, or
    # both edges with four shift choices: 7^3 = 343 complete explicit inputs.
    options = [([], []), ([(0, 0)], [0]), ([(1, 0)], [0])]
    options += [([(0, 0), (1, 0)], list(shifts)) for shifts in product(range(2), repeat=2)]
    for config in product(options, repeat=3):
        pairs, shifts = [], []
        for v, (local_pairs, local_shifts) in enumerate(config):
            pairs += [(u, v) for u, _ in local_pairs]
            shifts += local_shifts
        cases.append(('exhaustive_two_by_three', make_example(2, 3, pairs, 2, shifts)))
    cases += [
        ('empty', make_example(0, 2, [], 1)),
        ('degree_zero', make_example(2, 0, [], 3)),
        ('q_one_odd_degree', make_example(1, 3, [(0, v) for v in range(3)], 1)),
        ('frustrated_triangle', make_example(3, 3, [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (0, 2)], 2)),
        ('varying_right_degrees', make_example(3, 3, [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2)], 6, [0, 1, 2, 1, 0, 0])),
        ('odd_left_degree', make_example(3, 3, [(u, v) for u in range(3) for v in range(3)], 3, [0, 0, 1, 1, 2, 0, 2, 1, 2])),
    ]
    # Deterministic, genuinely shared labels across heterogeneous tests.
    for seed in range(12):
        pairs = [(u, v) for u in range(4) for v in range(5)
                 if (u * 7 + v * 11 + seed * 3) % 5 != 0]
        shifts = [(e * e + 3 * seed + u) for e, (u, v) in enumerate(pairs)]
        cases.append(('cross_test_correlations', make_example(4, 5, pairs, 12, shifts)))
    profiles = stable_profiles = jobs = moves = 0
    max_makespan = Fraction(0)
    outputs = []
    for name, data in cases:
        instance = validate(data)
        out = solve(data)
        # Repeat independently to check deterministic construction.
        if out != solve(json.loads(json.dumps(data))):
            raise RuntimeError('constructor is not deterministic')
        for chosen in product(*(range(len(aa)) for aa in instance['labels'])):
            # Cross-test inputs have 12^4 profiles, deliberately sampled by
            # their actual stable output; all smaller cases are exhaustive.
            if name == 'cross_test_correlations':
                break
            profiles += 1
            stable_profiles += independent_profile_check(instance, chosen)
        if name == 'cross_test_correlations':
            profiles += 1
            if not independent_profile_check(instance, out['stable']['chosen']):
                raise RuntimeError('actual cross-test output is not stable')
            stable_profiles += 1
        if out['stable']['initial_potential'] > out['stable']['potential_bound']:
            raise RuntimeError('polynomial potential upper bound failed')
        if len(out['stable']['moves']) > out['stable']['potential_bound']:
            raise RuntimeError('polynomial move count failed')
        jobs += len(out['jobs'])
        moves += len(out['stable']['moves'])
        max_makespan = max(max_makespan, out['makespan'])
        outputs.append({'name': name, 'input': data,
                        'labels': out['labels'], 'selected_edges': out['selected_edges'],
                        'sigma': out['sigma'], 'loads': out['loads'],
                        'makespan': out['makespan'],
                        'moves': len(out['stable']['moves'])})
    rejected = 0
    import copy
    valid = make_example(2, 1, [(0, 0), (1, 0)], 2)
    invalid = []
    z = copy.deepcopy(valid); z['edges'][0]['map']['a1'] = 0; invalid.append(z)
    z = copy.deepcopy(valid); z['edges'].append(copy.deepcopy(z['edges'][0])); invalid.append(z)
    z = copy.deepcopy(valid); z['left'][0]['labels'] = []; invalid.append(z)
    z = copy.deepcopy(valid); del z['edges'][0]['map']['a1']; invalid.append(z)
    z = copy.deepcopy(valid); z['edges'][0]['map']['other'] = 0; invalid.append(z)
    z = copy.deepcopy(valid); z['edges'][0]['map']['a0'] = 2; invalid.append(z)
    z = copy.deepcopy(valid); z['edges'][0]['map']['a0'] = True; invalid.append(z)
    z = copy.deepcopy(valid); z['edges'][0]['u'] = 'missing'; invalid.append(z)
    z = copy.deepcopy(valid); z['left'][1]['id'] = 'u0'; invalid.append(z)
    z = copy.deepcopy(valid); z['left'][0]['labels'] = ['a0', 'a0']; invalid.append(z)
    z = copy.deepcopy(valid); z['right'].append({'id': 'v0'}); invalid.append(z)
    z = copy.deepcopy(valid); z['extra'] = 1; invalid.append(z)
    for data in invalid:
        try:
            solve(data)
        except ValueError:
            rejected += 1
        else:
            raise RuntimeError('invalid input was accepted')
    brute = []
    for name, data in cases:
        if name not in ('empty', 'degree_zero', 'q_one_odd_degree', 'frustrated_triangle'):
            continue
        instance = validate(data)
        compiled = compile_instance(instance)
        opt, count = brute_complete_opt(compiled)
        actual = solve(data)['makespan']
        if actual < opt:
            raise RuntimeError('constructed value beats exhaustive actual OPT')
        brute.append({'name': name, 'actual_opt': opt,
                      'actual_constructor': actual, 'complete_assignments': count})
    return {'audit': 'row-uniform correlated guard exact finite audit',
            'scope': 'restricted class; finite audit is not a general proof',
            'source_code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'input_cases': len(cases), 'profile_checks': profiles,
            'stable_profile_hall_checks': stable_profiles,
            'complete_constructed_jobs': jobs, 'executed_strict_moves': moves,
            'invalid_inputs_rejected': rejected,
            'largest_actual_makespan': max_makespan,
            'independent_complete_schedule_enumerations': brute,
            'actual_outputs': outputs}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, help='explicit JSON input to solve')
    parser.add_argument('--audit', action='store_true', help='run independent finite exact audit')
    parser.add_argument('--output', type=Path, help='create a fresh JSON output, never overwrite')
    args = parser.parse_args()
    if args.audit == bool(args.input):
        parser.error('choose exactly one of --audit and --input')
    result = audit() if args.audit else solve(json.loads(args.input.read_text()))
    serialized = json.dumps(jsonable(result), ensure_ascii=False, indent=2) + '\n'
    if args.output:
        with args.output.open('x') as f:
            f.write(serialized)
    else:
        print(serialized, end='')


if __name__ == '__main__':
    main()
