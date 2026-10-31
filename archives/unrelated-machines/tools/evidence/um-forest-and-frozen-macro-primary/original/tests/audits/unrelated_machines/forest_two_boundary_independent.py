#!/usr/bin/env python3
"""双边界森林菜单：独立局部floor算法与强域完整分配审计。

The implementation core uses no author/repository code. Optional comparison
loads an immutable source string only after the independent audit completes.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import platform
import sys
import types


def actual_loads(jobs, assignment, vertices):
    assert len(jobs) == len(assignment)
    out = dict.fromkeys(vertices, F(0))
    for job, machine in zip(jobs, assignment):
        assert machine in job
        out[machine] += job[machine]
    return out


def forest_data(jobs, a, b):
    if a == b:
        raise ValueError('boundaries must be distinct')
    vertices = sorted({a, b} | {v for job in jobs for v in job})
    adjacent = {v: set() for v in vertices}
    private = {v: [] for v in vertices}
    bundles = {}
    for j, job in enumerate(jobs):
        if not 1 <= len(job) <= 2 or any(p < 0 for p in job.values()):
            raise ValueError('each job needs one/two nonnegative finite endpoints')
        if len(job) == 1:
            private[next(iter(job))].append(j)
        else:
            u, v = sorted(job)
            bundles.setdefault((u, v), []).append(j)
            adjacent[u].add(v)
            adjacent[v].add(u)
    parent, order = {}, []
    children = {v: [] for v in vertices}
    for start in [a] + [v for v in vertices if v != a]:
        if start in parent:
            continue
        parent[start] = None
        stack = [start]
        while stack:
            v = stack.pop()
            order.append(v)
            for w in sorted(adjacent[v], reverse=True):
                if w == parent[v]:
                    continue
                if w in parent:
                    raise ValueError('simple bundle support must be a forest')
                parent[w] = v
                children[v].append(w)
                stack.append(w)
    return vertices, private, bundles, parent, children, order


def floor_budget_witness(jobs, a, b, target, budget, eps, graph):
    """Real messages, and floor only the current node's parent bundle.

    At each non-a vertex, children have already minimized their contribution
    to this vertex under the corresponding original descendant capacities.
    No rounded descendant weight is passed upwards.
    """
    vertices, private, bundles, parent, children, order = graph
    assignment = [None] * len(jobs)
    message = {}
    max_capacity = updates = zero_capacity_nodes = 0
    for v in reversed(order):
        fixed = sum((jobs[j][v] for j in private[v]), F(0))
        for j in private[v]:
            assignment[j] = v
        fixed += sum((message[w] for w in children[v]), F(0))
        if v == a:
            # a roots its component and has no capacity, even when T=0.
            continue
        cap = budget if v == b else target
        if fixed > cap:
            return None, {'updates': updates, 'max_capacity': max_capacity,
                          'zero_capacity_nodes': zero_capacity_nodes}
        u = parent[v]
        if u is None:
            continue
        js = bundles[tuple(sorted((u, v)))]
        if cap == 0:
            zero_capacity_nodes += 1
            kept = {j for j in js if jobs[j][v] == 0}
        else:
            step = eps * cap / len(js)
            capacity = int((cap-fixed) // step)
            max_capacity = max(max_capacity, capacity)
            assert 0 <= capacity <= len(js) // eps
            # dp: rounded used weight -> (maximum exact saved parent load,
            # chosen child-assigned task identities). Explicit layers keep
            # zero-weight jobs 0/1 rather than allowing unbounded reuse.
            dp = {0: (F(0), ())}
            for j in js:
                weight = int(jobs[j][v] // step)
                nxt = dict(dp)
                for used, (profit, chosen) in dp.items():
                    updates += 1
                    after = used + weight
                    candidate = profit + jobs[j][u]
                    if after <= capacity and (after not in nxt or candidate > nxt[after][0]):
                        nxt[after] = (candidate, chosen + (j,))
                dp = nxt
            _, chosen = max(dp.values(), key=lambda pair: pair[0])
            kept = set(chosen)
        for j in js:
            assignment[j] = v if j in kept else u
        message[v] = sum((jobs[j][u] for j in js if j not in kept), F(0))
    assert all(v is not None for v in assignment)
    return tuple(assignment), {'updates': updates, 'max_capacity': max_capacity,
                               'zero_capacity_nodes': zero_capacity_nodes}


def boundary_menu(jobs, a, b, target, eta):
    jobs = tuple({v: F(p) for v, p in job.items()} for job in jobs)
    target, eta = F(target), F(eta)
    if target < 0 or not 0 < eta <= 1:
        raise ValueError('T>=0 and 0<eta<=1 required')
    graph = forest_data(jobs, a, b)
    vertices = graph[0]
    eps = eta / 3
    budgets = [F(0)]
    positive = [job[b] for job in jobs if b in job and job[b] > 0]
    if positive and min(positive) <= target:
        guess = min(positive)
        while True:
            budgets.append(guess)
            if guess >= target:
                break
            guess *= 1 + eps
    menu, seen = [], set()
    stats = Counter()
    for budget in budgets:
        witness, counts = floor_budget_witness(jobs, a, b, target, budget, eps, graph)
        stats['budget_queries'] += 1
        stats['knapsack_updates'] += counts['updates']
        stats['zero_capacity_nodes'] += counts['zero_capacity_nodes']
        stats['max_capacity'] = max(stats['max_capacity'], counts['max_capacity'])
        if witness is None or witness in seen:
            continue
        seen.add(witness)
        load = actual_loads(jobs, witness, vertices)
        assert all(load[v] <= (1+eps)*target for v in vertices if v not in (a,b))
        assert load[b] <= (1+eps)*budget
        if budget == 0:
            assert load[b] == 0
        menu.append({'a_load': load[a], 'b_load': load[b], 'assignment': witness,
                     'budget': budget})
    return menu, {'epsilon': eps, 'budgets': budgets, 'vertices': vertices, **stats}


def domain_schedules(jobs, a, b, target, vertices):
    """Exhaust the strong contract: a is entirely unbounded."""
    for rho in product(*(tuple(sorted(job)) for job in jobs)):
        load = actual_loads(jobs, rho, vertices)
        if load[b] <= target and all(load[v] <= target for v in vertices if v not in (a,b)):
            yield rho, load


def check_menu(jobs, a, b, target, eta, menu, vertices, counters):
    for item in menu:
        load = actual_loads(jobs, item['assignment'], vertices)
        assert load[a] == item['a_load'] and load[b] == item['b_load']
        assert load[b] <= (1+eta)*target
        assert all(load[v] <= (1+eta)*target for v in vertices if v not in (a,b))
        counters['actual_menu_witnesses'] += 1
    found = 0
    for rho, load in domain_schedules(jobs, a, b, target, vertices):
        # One and the same item must satisfy both boundary inequalities.
        matches = [item for item in menu if item['a_load'] <= load[a]
                   and item['b_load'] <= (1+eta)*load[b]]
        assert matches, (jobs, a, b, target, eta, rho, load, menu)
        if load[b] == 0:
            assert any(item['b_load'] == 0 for item in matches)
        counters['covered_strong_domain_schedules'] += 1
        counters['zero_b_reference_schedules'] += load[b] == 0
        counters['references_with_a_above_T'] += load[a] > target
        found += 1
    counters['instances_with_reference'] += found > 0
    counters['empty_menus'] += not menu
    counters['nonempty_without_reference'] += bool(menu) and found == 0
    return found


def exhaustive_cases():
    values = (F(0), F(1), F(2))
    pairs = tuple(product(values, repeat=2))
    # Every processing vector on a-u-b with these three endpoint values.
    for k, (x,y) in enumerate(product(pairs, repeat=2)):
        yield f'path_{k}', [{0:x[0],2:x[1]}, {2:y[0],1:y[1]}], 0,1,F(1),F(1,2)
    # b is in a component that does not contain a, with its own descendant.
    for k, (x,y) in enumerate(product(pairs, repeat=2)):
        yield f'b_separate_{k}', [{1:x[0],2:x[1]}, {2:y[0],3:y[1]}, {0:F(3)}], 0,1,F(1),F(1,2)
    patterns = ((F(0),F(1)),(F(1),F(0)),(F(1,2),F(1)),
                (F(1),F(1,2)),(F(3,2),F(1,2)),(F(1,2),F(3,2)))
    for k, (x,y,z) in enumerate(product(patterns, repeat=3)):
        yield f'branch_{k}', [{0:x[0],2:x[1]}, {2:y[0],1:y[1]},
                            {2:z[0],3:z[1]}, {2:F(1,2)}], 0,1,F(1),F(1,2)
    bundle_patterns = ((F(0),F(1)), (F(1),F(0)), (F(1,2),F(1)), (F(1),F(1,2)))
    for k, patterns3 in enumerate(product(bundle_patterns, repeat=3)):
        yield f'parallel_{k}', [{0:x,1:y} for x,y in patterns3], 0,1,F(1),F(1,2)


def explicit_cases():
    d = 2**257 + 13
    huge = 2**257
    data = [
        ('empty_T0', [],0,1,F(0),F(1,2)),
        ('empty_T1', [],0,1,F(1),F(1,5)),
        ('positive_private_a_T0', [{0:F(7)}],0,1,F(0),F(1,2)),
        ('positive_a_forced_T0', [{0:F(7),2:F(1)}, {2:F(0)}, {1:F(0)}],0,1,F(0),F(1,2)),
        ('T0_positive_b_impossible', [{1:F(1)}],0,1,F(0),F(1)),
        ('T0_zero_options', [{0:F(3),2:F(0)}, {2:F(0),1:F(0)}, {0:F(4)}],0,1,F(0),F(1,3)),
        ('positive_private_a_T1', [{0:F(70)}, {1:F(1)}, {2:F(1)}],0,1,F(1),F(1,2)),
        ('isolated_internal_infeasible', [{2:F(2)}],0,1,F(1),F(1,2)),
        ('augmented_only_not_an_iff', [{2:F(1,2),3:F(101,200)} for _ in range(4)],0,1,F(1),F(1,2)),
        ('correlated_two_item_bundle', [{0:F(1),1:F(1)}, {0:F(1),1:F(1)}],0,1,F(1),F(1,5)),
        ('private_parallel_path', [{0:F(3),2:F(1,3)}, {0:F(1),2:F(2,3)},
                                  {2:F(2,5),1:F(1,7)}, {2:F(1,5),1:F(3,7)}, {3:F(1)}],0,1,F(1),F(1,7)),
        ('b_separate_root_private', [{0:F(11)}, {1:F(1,4)}, {1:F(1,2),2:F(1,3)},
                                    {2:F(2,3),3:F(1,2)}],0,1,F(1),F(1,5)),
        ('tiny_denominator', [{0:F(1,17),1:F(1,d)}, {0:F(2,17),1:F(3,d)},
                              {0:F(4,17),1:F(5,d)}],0,1,F(13,d),F(1,5)),
        ('wide_geometric_range', [{0:F(1),1:F(1,2**40+87)}, {0:F(2),1:F(1)}],0,1,F(1),F(1,2)),
        ('sparse_huge_labels', [{huge:F(7)}, {huge+1:F(0),huge+2:F(0)}],huge,huge+1,F(0),F(1,2)),
        ('small_eta_zero_weights', [{0:F(1),2:F(1,1000)}, {0:F(2),2:F(0)},
                                   {2:F(999,1000),1:F(1,1000)}],0,1,F(1),F(1,50)),
    ]
    yield from data


def independent_audit():
    totals = Counter()
    rows = []
    all_cases = list(exhaustive_cases()) + list(explicit_cases())
    for name, jobs, a, b, target, eta in all_cases:
        menu, meta = boundary_menu(jobs,a,b,target,eta)
        count = check_menu(jobs,a,b,target,eta,menu,meta['vertices'],totals)
        totals['instances'] += 1
        for key in ('budget_queries','knapsack_updates','zero_capacity_nodes'):
            totals[key] += meta[key]
        totals['max_capacity'] = max(totals['max_capacity'],meta['max_capacity'])
        totals['max_guesses'] = max(totals['max_guesses'],len(meta['budgets']))
        totals['max_menu'] = max(totals['max_menu'],len(menu))
        rows.append({'name':name,'N':len(jobs),'T':str(target),'eta':str(eta),
                     'reference_schedules':count,'menu_items':len(menu),'guesses':len(meta['budgets'])})
    # Invalid cycles must be rejected even though parallel edges are allowed.
    invalid = [[{0:F(1),1:F(1)}, {1:F(1),2:F(1)}, {2:F(1),0:F(1)}],
               [{}], [{0:F(-1)}]]
    rejected = 0
    for jobs in invalid:
        try:
            boundary_menu(jobs,0,1,F(1),F(1,2))
        except ValueError:
            rejected += 1
        else:
            raise AssertionError('invalid input accepted')
    # An iterative 1500-edge forest check, not exhaustive assignment enumeration.
    deep_jobs = [{v:F(1),v+1:F(1)} for v in range(1500)]
    deep, meta = boundary_menu(deep_jobs,0,1500,F(1),F(1,2))
    assert deep
    assert any(x['a_load'] <= 1 and x['b_load'] == 0 for x in deep)
    for item in deep:
        load = actual_loads(deep_jobs,item['assignment'],meta['vertices'])
        assert max(load.values()) <= F(3,2)
    # Task-disjoint gadgets may share b. Select using a given reference only;
    # this is a composition witness, not an independent core-selection algorithm.
    shared_b = F(0)
    shared_reference = F(0)
    assembled_jobs, assembled_assignment = [], []
    gadgets = 12
    for g in range(1,gadgets+1):
        a = 10*g+2
        jobs = [{a:F(1,3),0:F(g,1000)}, {a:F(1,3),0:F(g+1,1000)}]
        menu, meta = boundary_menu(jobs,a,0,F(1),F(1,5))
        candidate = min((item for item in menu if item['a_load'] <= F(1,3)
                         and item['b_load'] <= F(6,5)*F(g,1000)),
                        key=lambda item:item['b_load'])
        assembled_jobs.extend(jobs)
        assembled_assignment.extend(candidate['assignment'])
        shared_b += candidate['b_load']
        shared_reference += F(g,1000)
    load = actual_loads(assembled_jobs,assembled_assignment,
                        {v for job in assembled_jobs for v in job})
    assert load[0] == shared_b <= F(6,5)*shared_reference
    for g in range(1,gadgets+1):
        assert load[10*g+2] <= F(1,3)
    return {'status':'all independent strong-contract checks passed','totals':dict(totals),
            'structured_family_sizes':{'path':81,'separate_b_component':81,'branch_private':216,
                                       'parallel_bundle':64,'explicit':16},
            'invalid_inputs_rejected':rejected,'deep_path_edges':1500,'deep_menu_items':len(deep),
            'task_disjoint_shared_b_gadgets':gadgets,
            'shared_reference_b':str(shared_reference),'shared_output_b':str(shared_b),
            'instances':rows}, all_cases


def compare_author(path, cases):
    source = path.read_text()
    module_name = '_two_boundary_author_snapshot_for_comparison'
    module = types.ModuleType(module_name)
    module.__file__ = str(path)
    sys.modules[module_name] = module
    exec(compile(source,str(path),'exec'),module.__dict__)
    totals = Counter()
    failures = []
    for name,jobs,a,b,target,eta in cases:
        try:
            raw, meta = module.boundary_menu(jobs,a,b,target,eta)
            menu = [{'a_load':x.a_load,'b_load':x.b_load,'assignment':x.assignment} for x in raw]
            vertices = {a,b} | {v for job in jobs for v in job}
            check_menu(jobs,a,b,target,eta,menu,vertices,totals)
        except Exception as error:
            failures.append({'name':name,'type':type(error).__name__,'message':str(error)[:1000]})
        totals['instances'] += 1
    return {'source':str(path),'source_sha256':hashlib.sha256(source.encode()).hexdigest(),
            'status':'passed' if not failures else 'failures found',
            'totals':dict(totals),'failures':failures}


def run(author=None, proof=None):
    result,cases = independent_audit()
    result.update({'arithmetic':'Fraction/integer; exact profits and true-load messages',
                   'algorithm':'local parent-bundle floor, exact real parent-load objective, geometric b budgets',
                   'python_version':platform.python_version(),
                   'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   'scope':'Finite complete schedule enumeration on each stated small instance; no claim of exhaustive arbitrary forests, ordinary-job compression, core selection, or error-free nesting.'})
    if proof:
        result['proof_target'] = {'path':str(proof), 'source_sha256':hashlib.sha256(proof.read_bytes()).hexdigest()}
    if author:
        result['author_comparison'] = compare_author(author,cases)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--compare-author',type=Path)
    parser.add_argument('--proof-target',type=Path)
    args = parser.parse_args()
    result = run(args.compare_author,args.proof_target)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('instances',)},ensure_ascii=False,indent=2))
