"""确定性关联着色给资源束碰撞地板；精确审计只输出 JSON。

Polynomial interfaces:
  bounded_collision_floor(resource_sets, demands, owner_orders=None)
  select_locally_full_labels(label_groups)
  to_dag_and_tree(resource_sets, demands, result)
  group_degree_label_approximation(label_groups)
  label_dag_and_tree(label_groups, result)

Each resource set is explicit, nonempty, contains distinct nonnegative integers,
and has positive integer demand at most its size.  owner_orders, when supplied,
is a dict mapping every used resource to a permutation of its chosen-bundle
owners.  The theorem uses multiplicity in ONE selected label per group, not the
number of occurrences over all alternative labels.  Exact optimum enumeration
below is an audit oracle only, never used by the constructive interface.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import platform
import time


def _normalized(resource_sets, demands):
    if len(resource_sets) != len(demands):
        raise ValueError('one demand per bundle required')
    normalized = []
    for resources, demand in zip(resource_sets, demands):
        if type(demand) is not int or demand < 1:
            raise ValueError('positive integer demand required')
        resources = tuple(resources)
        if any(type(u) is not int or u < 0 for u in resources):
            raise ValueError('nonnegative integer resource identities required')
        if len(resources) != len(set(resources)):
            raise ValueError('a resource may occur only once in one bundle')
        if demand > len(resources):
            raise ValueError('locally full demand is infeasible')
        normalized.append(tuple(sorted(resources)))
    return normalized, list(demands)


def bounded_collision_floor(resource_sets, demands, owner_orders=None):
    """Return an actual collision-free partial allocation of score >= 1/Delta.

    Resource sets are first truncated deterministically to their demand.  Delta
    is the maximum resource multiplicity AFTER this truncation, hence is at most
    the multiplicity before truncation.  With q=0 the root is a zero-demand
    terminal and the returned score is 1; Delta=0 is merely an empty marker.
    Loops depend on explicit incidences, never the numeric size of a demand.
    """
    resource_sets, demands = _normalized(resource_sets, demands)
    q = len(resource_sets)
    trimmed = [resources[:d] for resources, d in zip(resource_sets, demands)]
    owners = {}
    for x, resources in enumerate(trimmed):
        for u in resources:
            owners.setdefault(u, []).append(x)
    if owner_orders is not None:
        if set(owner_orders) != set(owners):
            raise ValueError('owner_orders must cover exactly the used resources')
        for u, xs in owners.items():
            order = list(owner_orders[u])
            if len(order) != len(xs) or set(order) != set(xs):
                raise ValueError('resource owner order must be a permutation')
            owners[u] = order
    if not q:
        return {'delta': 0, 'color': None, 'selected': [], 'allocated': [],
                'score': F(1), 'fulfilled_per_color': [], 'trimmed': trimmed}
    delta = max(map(len, owners.values()))
    allocations = [[[] for _ in range(q)] for _ in range(delta)]
    for u, xs in owners.items():
        for color, x in enumerate(xs):
            allocations[color][x].append(u)
    fulfilled = [[x for x in range(q) if delta * len(alloc[x]) >= demands[x]]
                 for alloc in allocations]
    # The local pigeonhole fact is checked independently for every center.
    assert all(any(x in good for good in fulfilled) for x in range(q))
    color = max(range(delta), key=lambda a: (len(fulfilled[a]), -a))
    selected = fulfilled[color]
    allocated = [sorted(allocations[color][x]) if x in selected else []
                 for x in range(q)]
    score = min([F(1), F(len(selected), q)] +
                [F(len(allocated[x]), demands[x]) for x in selected])
    result = {'delta': delta, 'color': color, 'selected': selected,
              'allocated': allocated, 'score': score,
              'fulfilled_per_color': list(map(len, fulfilled)), 'trimmed': trimmed}
    validate_allocation(resource_sets, demands, result)
    assert len(selected) * delta >= q
    assert score >= F(1, delta)
    return result


def validate_allocation(resource_sets, demands, result):
    """Check the concrete allocation and exact rooted-tree score."""
    resource_sets, demands = _normalized(resource_sets, demands)
    q = len(resource_sets)
    selected = result['selected']
    if len(selected) != len(set(selected)) or any(not 0 <= x < q for x in selected):
        raise ValueError('invalid selected centers')
    if len(result['allocated']) != q:
        raise ValueError('allocation length')
    used = []
    for x, allocation in enumerate(result['allocated']):
        if (x not in selected and allocation) or not set(allocation) <= set(resource_sets[x]):
            raise ValueError('unselected or unavailable resource')
        used.extend(allocation)
    if len(used) != len(set(used)):
        raise ValueError('resource reuse')
    expected = F(1) if not q else min(
        [F(1), F(len(selected), q)] +
        [F(len(result['allocated'][x]), demands[x]) for x in selected])
    if result['score'] != expected:
        raise ValueError('wrong score')
    return expected


def select_locally_full_labels(label_groups):
    """Select first locally full label per x or certify full b*=1 impossible.

    A label is (positive demand, iterable of distinct integer resources).  A
    failed group has no label whose support size reaches its demand.  This
    excludes score ONE only; it does not exclude all positive lower scores.
    Even enormous binary demands are tested by comparison, not expansion.
    """
    chosen = []
    deficient = []
    for x, group in enumerate(label_groups):
        feasible = []
        for a, (demand, resources) in enumerate(group):
            resources = tuple(resources)
            if type(demand) is not int or demand < 1:
                raise ValueError('positive label demand required')
            if any(type(u) is not int or u < 0 for u in resources):
                raise ValueError('invalid resource identity')
            if len(resources) != len(set(resources)):
                raise ValueError('duplicate label resource')
            if demand <= len(resources):
                feasible.append((a, tuple(sorted(resources)), demand))
        if feasible:
            chosen.append(feasible[0])
        else:
            deficient.append(x)
            chosen.append(None)
    if deficient:
        return {'status': 'full_value_one_impossible_by_local_deficit',
                'deficient_groups': deficient, 'chosen': chosen}
    return {'status': 'all_groups_have_locally_full_choice', 'chosen': chosen,
            'resource_sets': [a[1] for a in chosen], 'demands': [a[2] for a in chosen]}


def to_dag_and_tree(resource_sets, demands, result):
    """Construct the actual depth-three DAG and actual returned root tree."""
    resource_sets, demands = _normalized(resource_sets, demands)
    validate_allocation(resource_sets, demands, result)
    q = len(resource_sets)
    resources = sorted(set().union(*map(set, resource_sets))) if q else []
    vertex = {u: 2*q+1+a for a, u in enumerate(resources)}
    n = 2*q+1+len(resources)
    k = [q]+[1]*q+demands+[0]*len(resources)
    edges = []
    chosen = []
    for x, support in enumerate(resource_sets):
        center, label = 1+x, 1+q+x
        edges.extend([(0, center), (center, label)])
        edges.extend((label, vertex[u]) for u in support)
        if x in result['selected']:
            chosen.extend([(0, center), (center, label)])
            chosen.extend((label, vertex[u]) for u in result['allocated'][x])
    return n, edges, k, chosen



def _label_groups(label_groups):
    groups = []
    for group in label_groups:
        labels = []
        for demand, resources in group:
            resources = tuple(resources)
            if type(demand) is not int or demand < 1:
                raise ValueError('positive label demand required')
            if any(type(u) is not int or u < 0 for u in resources):
                raise ValueError('invalid label resource')
            if len(resources) != len(set(resources)):
                raise ValueError('duplicate label resource')
            labels.append((demand, tuple(sorted(resources))))
        groups.append(labels)
    return groups


def group_degree_label_approximation(label_groups):
    """Actual U/Delta tree, with certified b* <= U, for group degree Delta.

    Root demand is q, each x has demand 1, each alternative label has its
    arbitrary positive binary demand, resource terminals have demand 0.
    Empty groups, empty supports and locally impossible labels are allowed.
    The global degree counts distinct x groups, not alternative label nodes.
    Returned ``selected_labels`` entries are (group, label, resource list).
    No optimum oracle or threshold enumeration is called.  Local capacities
    a_x=max_e min(1, |S_e|/K_e) upper-bound each group's attainable score.
    The deterministic prefix bound U=max_s min(s/q, a_(s)) satisfies b*<=U.
    A maximizing prefix is colored after its best label supports are truncated
    to min(K_e,|S_e|); the resulting original-demand tree has score >=U/Delta.
    """
    groups = _label_groups(label_groups)
    q = len(groups)
    owners = {}
    best_labels = []
    for x, group in enumerate(groups):
        for demand, support in group:
            for u in support:
                owners.setdefault(u, set()).add(x)
        if group:
            a = max(range(len(group)),
                    key=lambda i: (min(F(1), F(len(group[i][1]), group[i][0])), -i))
            demand, support = group[a]
            capacity = min(F(1), F(len(support), demand))
            best_labels.append((capacity, x, a, demand, support))
        else:
            best_labels.append((F(0), x, None, None, ()))
    delta = max(map(len, owners.values()), default=0)
    if not q:
        return {'score': F(1), 'delta': 0, 'selected_delta': 0,
                'upper_bound': F(1), 'prefix_size': 0, 'selected_labels': []}
    best_labels.sort(key=lambda z: (-z[0], z[1]))
    size = max(range(1, q+1), key=lambda s: (min(F(s, q), best_labels[s-1][0]), -s))
    upper_bound = min(F(size, q), best_labels[size-1][0])
    if not upper_bound:
        return {'score': F(0), 'delta': delta, 'selected_delta': 0,
                'upper_bound': F(0), 'prefix_size': 0, 'selected_labels': []}
    prefix = best_labels[:size]
    supports = [support[:min(demand, len(support))]
                for capacity, x, a, demand, support in prefix]
    partial = bounded_collision_floor(supports, list(map(len, supports)))
    selected = [(prefix[i][1], prefix[i][2], partial['allocated'][i])
                for i in partial['selected']]
    value = min([F(1), F(len(selected), q)] +
                [F(len(resources), groups[x][a][0]) for x, a, resources in selected])
    assert value >= upper_bound/partial['delta'] >= upper_bound/delta
    return {'score': value, 'delta': delta, 'selected_delta': partial['delta'],
            'upper_bound': upper_bound, 'prefix_size': size,
            'selected_labels': selected}


def label_dag_and_tree(label_groups, result):
    """Actual full-menu DAG and selected tree; verifies original demand score."""
    groups = _label_groups(label_groups)
    q = len(groups)
    labels = [(x, a, demand, support) for x, group in enumerate(groups)
              for a, (demand, support) in enumerate(group)]
    label_vertex = {(x, a): q+1+i for i, (x, a, demand, support) in enumerate(labels)}
    resources = sorted({u for x, a, demand, support in labels for u in support})
    resource_vertex = {u: q+1+len(labels)+i for i, u in enumerate(resources)}
    n = q+1+len(labels)+len(resources)
    demands = [q]+[1]*q+[demand for x, a, demand, support in labels]+[0]*len(resources)
    edges = [(0, x+1) for x in range(q)]
    for x, a, demand, support in labels:
        v = label_vertex[x, a]
        edges.append((x+1, v))
        edges.extend((v, resource_vertex[u]) for u in support)
    selected = result['selected_labels']
    seen_groups = set()
    seen_resources = set()
    tree = []
    for x, a, allocation in selected:
        if x in seen_groups or not 0 <= x < q or not 0 <= a < len(groups[x]):
            raise ValueError('invalid selected label or repeated group')
        if len(allocation) != len(set(allocation)) or not set(allocation) <= set(groups[x][a][1]):
            raise ValueError('invalid selected resources')
        if seen_resources.intersection(allocation):
            raise ValueError('resource collision')
        seen_groups.add(x)
        seen_resources.update(allocation)
        v = label_vertex[x, a]
        tree.extend([(0, x+1), (x+1, v)])
        tree.extend((v, resource_vertex[u]) for u in allocation)
    expected = F(1) if not q else min(
        [F(1), F(len(selected), q)] +
        [F(len(allocation), groups[x][a][0]) for x, a, allocation in selected])
    if expected != result['score']:
        raise ValueError('incorrect original-demand score')
    return n, edges, demands, tree


def exact_label_optimum(label_groups):
    """Independent exponential full-menu oracle, used only on small audits.

    One label per selected group suffices because group demand is 1 and the
    capped target score never exceeds 1.  Deleting other labels frees resources.
    This oracle enumerates original labels and original resource assignments.
    """
    groups = _label_groups(label_groups)
    q = len(groups)
    if not q:
        return F(1), 1
    best = F(0)
    states = 0
    for choices in product(*[[-1]+list(range(len(group))) for group in groups]):
        centers = [x for x in range(q) if choices[x] >= 0]
        if not centers:
            continue
        supports = [groups[x][choices[x]][1] for x in centers]
        demands = [groups[x][choices[x]][0] for x in centers]
        resources = sorted(set().union(*map(set, supports)))
        options = [[-1]+[i for i, support in enumerate(supports) if u in support]
                   for u in resources]
        for assignment in product(*options):
            counts = Counter(assignment)
            value = min([F(1), F(len(centers), q)] +
                        [F(counts[i], demands[i]) for i in range(len(centers))])
            best = max(best, value)
            states += 1
    return best, states

def exact_bundle_optimum(resource_sets, demands):
    """Independent exponential oracle via resource owners and all center subsets."""
    q = len(resource_sets)
    if not q:
        return F(1), 1
    resources = sorted(set().union(*map(set, resource_sets)))
    options = [[-1]+[x for x, support in enumerate(resource_sets) if u in support]
               for u in resources]
    best = F(0)
    enumerated = 0
    for assignment in product(*options):
        counts = Counter(assignment)
        for mask in range(1, 1 << q):
            selected = [x for x in range(q) if mask >> x & 1]
            value = min([F(1), F(len(selected), q)] +
                        [F(counts[x], demands[x]) for x in selected])
            best = max(best, value)
            enumerated += 1
    return best, enumerated


def _orders(resource_sets, demands, variant):
    owners = {}
    for x, support in enumerate(resource_sets):
        for u in sorted(support)[:demands[x]]:
            owners.setdefault(u, []).append(x)
    for u, xs in owners.items():
        if variant == 'reverse':
            owners[u] = xs[::-1]
        elif variant == 'rotate':
            shift = u % len(xs)
            owners[u] = xs[shift:]+xs[:shift]
    return owners


def main():
    started = time.monotonic()
    exhaustive_families = color_runs = exact_oracle_families = oracle_states = 0
    degree_counts = Counter()
    for r in range(1, 5):
        bundles = [(s, d) for z in range(1, r+1)
                   for s in combinations(range(r), z) for d in range(1, z+1)]
        for q in range(1, 4):
            for data in product(bundles, repeat=q):
                supports, demands = zip(*data)
                exhaustive_families += 1
                results = []
                for variant in ('forward', 'reverse', 'rotate'):
                    result = bounded_collision_floor(
                        supports, demands, _orders(supports, demands, variant))
                    results.append(result)
                    color_runs += 1
                degree_counts[results[0]['delta']] += 1
                if r <= 3:
                    optimum, states = exact_bundle_optimum(supports, demands)
                    exact_oracle_families += 1
                    oracle_states += states
                    assert all(a['score'] <= optimum for a in results)
    empty = bounded_collision_floor([], [])
    assert empty['score'] == 1
    sharpness = []
    for delta in range(1, 6):
        supports = [(u,) for u in range(2) for _ in range(delta)]
        optimum, states = exact_bundle_optimum(supports, [1]*len(supports))
        assert optimum == F(1, delta)
        sharpness.append({'type': 'singleton_multiplicity', 'delta': delta,
                          'q': len(supports), 'b_star': str(optimum),
                          'oracle_states': states})
    for k in range(1, 7):
        supports = [tuple(range(k))]*2
        optimum, states = exact_bundle_optimum(supports, [k, k])
        assert optimum == F(1, 2)
        sharpness.append({'type': 'identical_pair_all_k', 'delta': 2, 'k': k,
                          'q': 2, 'b_star': str(optimum), 'oracle_states': states})
    # Broader-label scan: full infeasibility is not called zero-score infeasibility.
    label_checks = [
        [[(10**100, [0]), (1, [0])], [(2, [1, 2])]],
        [[(10**100, [0])]], [[], [(1, [0])]], [],
        [[(1, [0]), (2, [0, 1])], [(1, [0])]]]
    scan_statuses = []
    for groups in label_checks:
        scan = select_locally_full_labels(groups)
        scan_statuses.append(scan['status'])
        if scan['status'] == 'all_groups_have_locally_full_choice':
            bounded_collision_floor(scan['resource_sets'], scan['demands'])
    assert scan_statuses[1:3] == ['full_value_one_impossible_by_local_deficit']*2
    bad = [([[]], [1]), ([(0, 0)], [1]), ([(0,)], [0]),
           ([(0,)], [True]), ([(0,)], [10**100]), ([(0,)], [])]
    for args in bad:
        try:
            bounded_collision_floor(*args)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid contract input accepted')
    # Limited actual-DAG / actual-schedule checks use the existing bridge only.
    import rooted_dag_token_bridge as bridge
    example_path = Path(__file__).resolve().parents[3] / 'examples/unrelated_machines/pairwise_label_resource_floor.json'
    examples = json.loads(example_path.read_text())['cases']
    schedule_records = []
    samples = [(a['resource_sets'], a['demands'], a['name']) for a in examples]
    samples.extend([([], [], 'empty_root_terminal'),
                    ([(0, 1), (1, 2, 3, 4), (3,)], [2, 3, 1], 'heterogeneous_private_resources')])
    for supports, demands, name in samples:
        result = bounded_collision_floor(supports, demands)
        n, edges, k, tree = to_dag_and_tree(supports, demands, result)
        bridge.validate(n, edges, k)
        assert bridge.score(n, tree, k) == result['score']
        jobs, assignment = bridge.tree_to_schedule(n, edges, k, tree)
        loads = bridge.loads(n, jobs, assignment)
        makespan = max(loads)
        assert makespan <= 2-result['score']
        decoded = bridge.decode(n, edges, k, jobs, assignment)
        assert bridge.score(n, decoded, k) >= 2-makespan
        optimum, states = exact_bundle_optimum(supports, demands)
        expected = next((F(a['expected_b_star']) for a in examples if a['name'] == name), None)
        if expected is not None:
            assert optimum == expected
        schedule_records.append({'name': name, 'vertices': n, 'jobs': len(jobs),
                                 'delta': result['delta'], 'score': str(result['score']),
                                 'b_star': str(optimum), 'tree': tree,
                                 'assignment': assignment, 'loads': list(map(str, loads)),
                                 'makespan': str(makespan), 'oracle_states': states})
    # Global distinct-group degree: arbitrary menus and local deficits.
    menu_families = menu_oracle_states = menu_bridge_checks = 0
    menu_degrees = Counter()
    def audit_menu(groups):
        nonlocal menu_families, menu_oracle_states, menu_bridge_checks
        result = group_degree_label_approximation(groups)
        optimum, states = exact_label_optimum(groups)
        menu_families += 1
        menu_oracle_states += states
        menu_degrees[result['delta']] += 1
        if not groups:
            assert result['score'] == optimum == 1
        elif result['delta'] == 0:
            assert result['score'] == optimum == 0
        else:
            assert optimum <= result['upper_bound']
            assert result['upper_bound']/result['delta'] <= result['score'] <= optimum
        n, edges, k, tree = label_dag_and_tree(groups, result)
        assert bridge.score(n, tree, k) == result['score']
        # Calls to actual scheduling bridge are deliberately a limited subset.
        if menu_families <= 12 or menu_families % 251 == 0:
            bridge.validate(n, edges, k)
            jobs, assignment = bridge.tree_to_schedule(n, edges, k, tree)
            makespan = max(bridge.loads(n, jobs, assignment))
            assert makespan <= 2-result['score']
            if result['delta'] >= 1:
                assert makespan <= (2-F(1, result['delta']))*(2-optimum)
            if makespan < 2:
                decoded = bridge.decode(n, edges, k, jobs, assignment)
                assert bridge.score(n, decoded, k) >= 2-makespan
            menu_bridge_checks += 1
    for r in range(1, 4):
        options = [(d, support) for size in range(r+1)
                   for support in combinations(range(r), size) for d in range(1, 4)]
        for a, b in product(options, repeat=2):
            audit_menu([[a], [b]])
    options = [(d, support) for size in range(3)
               for support in combinations(range(2), size) for d in range(1, 4)]
    for a, b, c in product(options, repeat=3):
        audit_menu([[a, b], [c]])
    for groups in [[], [[]], [[], []], [[(10**100, [0])], [(1, [])]],
                   [[(1, [0]), (1, [1])], [(1, [0]), (1, [2])],
                    [(1, [1]), (1, [2])]],
                   [[(1, [0]), (2, [0, 1])], [(1, [0])], [(1, [0, 1])]]]:
        audit_menu(groups)
    out = {'title': '有界资源碰撞的关联着色地板精确审计',
           'python': platform.python_version(), 'precision': 'integers / fractions.Fraction; exact',
           'seed': None, 'parameters': {'q': [1, 3], 'resource_universe': [1, 4],
                   'demands': 'all integers 1..support size',
                   'owner_orders': ['forward', 'reverse', 'resource-index rotation'],
                   'independent_optimum_resource_universe': [1, 3]},
           'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'example_sha256': hashlib.sha256(example_path.read_bytes()).hexdigest(),
           'bridge_sha256': hashlib.sha256(Path(bridge.__file__).read_bytes()).hexdigest(),
           'exhaustive_families': exhaustive_families, 'coloring_runs': color_runs,
           'families_by_selected_multiplicity': dict(degree_counts),
           'independent_optimum_families': exact_oracle_families,
           'independent_oracle_states': oracle_states,
           'invalid_cases_rejected': len(bad), 'local_label_scan_statuses': scan_statuses,
           'sharpness': sharpness, 'actual_schedule_checks': schedule_records,
           'global_group_degree_menus': menu_families,
           'global_group_degree_menu_oracle_states': menu_oracle_states,
           'menu_families_by_global_distinct_group_degree': dict(menu_degrees),
           'menu_actual_schedule_checks': menu_bridge_checks,
           'elapsed_seconds': round(time.monotonic()-started, 6),
           'limits': 'Finite enumeration checks implementation only. General 1/Delta floor follows the incidence-coloring proof. Multiplicity is measured after one locally full label per x is chosen and supports are truncated to demand. The global distinct-group-degree algorithm uses a sorted local-capacity upper bound U and original-demand rescoring; it is not an algorithm for arbitrary unbounded-degree DAGs. No Label Cover soundness or general scheduling hardness theorem is proved.'}
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
