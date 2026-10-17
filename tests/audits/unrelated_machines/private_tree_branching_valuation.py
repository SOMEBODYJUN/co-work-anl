#!/usr/bin/env python3
"""私有分叉树估值：精确demand、加性minorant分离及紧凑LP数据。

Instance schema:
 {"k": k, "h": h, "resources": [distinct int/string IDs],
  "states": [{"id": distinct int/string ID,
              "leaves": [{"path": [h exact digits], "resource": ID}, ...]}]}
Every state explicitly lists ALL leaves of a full k-ary height-h tree, k,h>=1.
Its leaf-resource map must be injective; resource sharing across states is legal.
Full leaf addresses charge the actual height to input length, including k=1.
Query prices follow the complete resources list.  Single-state leaf_weights
follow lexicographically sorted leaf paths, regardless of input leaf order.
The state query argument is its zero-based list index, not its arbitrary ID.

Exact value and demand return actual subsets/subtrees, not UM schedules.
The single-state minorant oracle returns actual complementary blocking trees.
compact_minorant_lp outputs the proved finite LP, not a generic LP optimizer.
No floating-point solver or OPT oracle is used in production.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json
import re
import sys

if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)

SOURCE_CLAIMS = ('UM-PRIVATE-TREE-Q-VALUATION-v1',
                 'UM-TREE-Q-XOS-ENVELOPE-v1',
                 'UM-TREE-Q-MINORANT-LP-v1')


def integer(x, minimum=0):
    if type(x) is int:
        value = x
    elif type(x) is str and re.fullmatch(r'\+?\d+', x):
        value = int(x)
    else:
        raise ValueError('exact nonnegative integer required')
    if value < minimum:
        raise ValueError('integer outside domain')
    return value


def rational(x):
    if isinstance(x, F):
        return x
    if type(x) not in (int, str):
        raise ValueError('exact finite rational string/int required')
    try:
        return F(x)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError('exact finite rational required') from exc


def identifier(x):
    if type(x) not in (int, str):
        raise ValueError('exact int/string identifier required')
    return x


def build_instance(data):
    if type(data) is not dict or set(data) != {'k', 'h', 'resources', 'states'}:
        raise ValueError('exact instance keys required')
    k, h = integer(data['k'], 1), integer(data['h'], 1)
    if type(data['resources']) not in (list, tuple):
        raise ValueError('explicit ground resource list required')
    resources = [identifier(x) for x in data['resources']]
    if len(set(resources)) != len(resources):
        raise ValueError('distinct ground resources required')
    resource_index = {u: i for i, u in enumerate(resources)}
    if type(data['states']) not in (list, tuple) or not data['states']:
        raise ValueError('nonempty explicit state list required')
    states = []
    labels = set()
    for state in data['states']:
        if type(state) is not dict or set(state) != {'id', 'leaves'}:
            raise ValueError('exact state keys required')
        label = identifier(state['id'])
        if label in labels:
            raise ValueError('distinct state IDs required')
        labels.add(label)
        if type(state['leaves']) not in (list, tuple) or not state['leaves']:
            raise ValueError('nonempty full explicit leaf list required')
        wiring = {}
        children = {}
        seen_resources = set()
        for leaf in state['leaves']:
            if type(leaf) is not dict or set(leaf) != {'path', 'resource'}:
                raise ValueError('exact leaf path/resource required')
            path = leaf['path']
            if (type(path) not in (list, tuple) or len(path) != h
                    or any(type(d) is not int or not 0 <= d < k for d in path)):
                raise ValueError('invalid full leaf address')
            path = tuple(path)
            u = identifier(leaf['resource'])
            if u not in resource_index:
                raise ValueError('leaf uses unknown ground resource')
            ri = resource_index[u]
            if path in wiring:
                raise ValueError('duplicate leaf path')
            if ri in seen_resources:
                raise ValueError('state-internal leaf map must be injective')
            seen_resources.add(ri)
            wiring[path] = ri
            for depth in range(h):
                children.setdefault(path[:depth], set()).add(path[depth])
        if any(len(digits) != k for digits in children.values()):
            raise ValueError('all prefixes must have exactly k children')
        nodes = sorted(set(children) | set(wiring), key=lambda p: (len(p), p))
        states.append({'id': label, 'wiring': wiring,
                       'children': {p: sorted(ds) for p, ds in children.items()},
                       'nodes': nodes, 'leaves': sorted(wiring)})
    return {'k': k, 'h': h, 'resources': resources,
            'resource_index': resource_index, 'states': states}


def state_index(I, a):
    a = integer(a)
    if a >= len(I['states']):
        raise ValueError('unknown state index')
    return a


def subset_indices(I, subset, allowed=None):
    if type(subset) not in (list, tuple, set, frozenset):
        raise ValueError('explicit subset required')
    answer = set()
    for u in subset:
        u = identifier(u)
        if u not in I['resource_index']:
            raise ValueError('subset contains unknown resource')
        ri = I['resource_index'][u]
        if allowed is not None and ri not in allowed:
            raise ValueError('subset outside chosen state leaf universe')
        if ri in answer:
            raise ValueError('duplicate subset resource')
        answer.add(ri)
    return answer


def vector(values, length, nonnegative=False):
    if type(values) not in (list, tuple) or len(values) != length:
        raise ValueError('one exact rational per required coordinate')
    result = [rational(x) for x in values]
    if nonnegative and any(x < 0 for x in result):
        raise ValueError('nonnegative weights required')
    return result


def _tree_witness(I, a, r, selected_digits):
    state = I['states'][a]
    if r == 0:
        return {'state_index': a, 'state_id': state['id'], 'branching': 0,
                'internal_paths': [], 'leaf_paths': [], 'leaf_resources': []}
    stack = [()]
    internal = []
    leaves = []
    while stack:
        path = stack.pop()
        if len(path) == I['h']:
            leaves.append(path)
        else:
            internal.append(path)
            digits = selected_digits[path]
            if len(digits) != r:
                raise RuntimeError('witness did not select exactly r children')
            stack.extend(path + (d,) for d in reversed(digits))
    leaves.sort()
    return {'state_index': a, 'state_id': state['id'], 'branching': r,
            'internal_paths': [list(p) for p in sorted(internal, key=lambda p: (len(p), p))],
            'leaf_paths': [list(p) for p in leaves],
            'leaf_resources': [I['resources'][state['wiring'][p]] for p in leaves]}


def _value_state(I, a, available):
    state = I['states'][a]
    k = I['k']
    values = {}
    for path in reversed(state['nodes']):
        if path in state['wiring']:
            values[path] = k if state['wiring'][path] in available else 0
        else:
            ordered = sorted((values[path + (d,)] for d in state['children'][path]), reverse=True)
            values[path] = max([0] + [r for r, value in enumerate(ordered, 1) if value >= r])
    r = values[()]
    choices = {}
    if r:
        for path in state['children']:
            eligible = [d for d in state['children'][path] if values[path + (d,)] >= r]
            if len(eligible) >= r:
                choices[path] = eligible[:r]
    return r, _tree_witness(I, a, r, choices)


def _best_value(I, available):
    candidates = [_value_state(I, a, available) for a in range(len(I['states']))]
    return max(candidates, key=lambda entry: entry[0])


def value(data, subset):
    I = build_instance(data)
    available = subset_indices(I, subset)
    q, witness = _best_value(I, available)
    return {'source_claims': [SOURCE_CLAIMS[0]], 'mode': 'exact-value',
            'subset': [u for i, u in enumerate(I['resources']) if i in available],
            'value': q, 'witness': witness}


def _cost_tree(I, a, r, costs):
    state = I['states'][a]
    if r == 0:
        return F(0), _tree_witness(I, a, 0, {}), {}
    dp = {}
    choices = {}
    for path in reversed(state['nodes']):
        if path in state['wiring']:
            dp[path] = costs[state['wiring'][path]]
        else:
            ordered = sorted(state['children'][path], key=lambda d: (dp[path + (d,)], d))
            choices[path] = ordered[:r]
            dp[path] = sum((dp[path + (d,)] for d in choices[path]), F(0))
    witness = _tree_witness(I, a, r, choices)
    return dp[()], witness, dp


def _leaf_weights(I, a, leaf_weights):
    state = I['states'][a]
    weights = vector(leaf_weights, len(state['leaves']), nonnegative=True)
    costs = [F(0) for _ in I['resources']]
    for path, weight in zip(state['leaves'], weights):
        costs[state['wiring'][path]] = weight
    return weights, costs


def min_cost_subtree(data, state, branching, leaf_weights):
    I = build_instance(data)
    a = state_index(I, state)
    r = integer(branching)
    if r > I['k']:
        raise ValueError('branching must not exceed k')
    weights, costs = _leaf_weights(I, a, leaf_weights)
    cost, witness, _ = _cost_tree(I, a, r, costs)
    return {'source_claims': [SOURCE_CLAIMS[0], SOURCE_CLAIMS[2]],
            'mode': 'minimum-cost-subtree', 'state_index': a,
            'leaf_weights': weights, 'cost': cost, 'witness': witness}


def exact_demand(data, prices):
    I = build_instance(data)
    prices = vector(prices, len(I['resources']))
    negative = {i for i, price in enumerate(prices) if price < 0}
    credit = -sum((prices[i] for i in negative), F(0))
    costs = [max(F(0), p) for p in prices]
    best = None
    candidates = []
    for a in range(len(I['states'])):
        for r in range(I['k'] + 1):
            cost, tree, _ = _cost_tree(I, a, r, costs)
            score = credit + r - cost
            candidates.append({'state_index': a, 'branching': r, 'cost': cost, 'score': score})
            if best is None or score > best[0]:
                best = score, tree, cost
    target, selected_tree, cost = best
    chosen = negative | {I['resource_index'][u] for u in selected_tree['leaf_resources']}
    q, witness = _best_value(I, chosen)
    total_price = sum((prices[i] for i in chosen), F(0))
    objective = q - total_price
    if objective != target:
        raise RuntimeError('actual demand subset did not attain DP optimum')
    return {'source_claims': [SOURCE_CLAIMS[0]], 'mode': 'exact-demand',
            'prices': prices,
            'negative_resources': [u for i, u in enumerate(I['resources']) if i in negative],
            'negative_price_credit': credit,
            'subset': [u for i, u in enumerate(I['resources']) if i in chosen],
            'value': q, 'total_price': total_price, 'objective': objective,
            'witness': witness, 'minimum_cost_candidate_tree': selected_tree,
            'minimum_cost_candidate_cost': cost, 'candidate_scores': candidates}


def full_envelope(data, state=0):
    I = build_instance(data)
    a = state_index(I, state)
    k, h = I['k'], I['h']
    N = len(I['states'][a]['leaves'])
    D = N - (k - 1) ** h
    envelope = F(N, D)
    gap = F(k * D, N)
    if not F(min(k, h), 2) <= gap <= min(k, h):
        raise RuntimeError('proved envelope loss bound missed')
    return {'source_claims': [SOURCE_CLAIMS[1]], 'mode': 'full-envelope-formula',
            'state_index': a, 'k': k, 'h': h, 'N': N,
            'largest_q_le_t_leaf_counts': [N - (k - t) ** h for t in range(k + 1)],
            'uniform_leaf_weight': F(1, D), 'envelope_full': envelope,
            'q_full': k, 'multiplicative_loss': gap,
            'loss_lower_bound': F(min(k, h), 2), 'loss_upper_bound': min(k, h),
            'generic_LP_optimization_implemented': False}


def separate_minorant(data, state, leaf_weights):
    I = build_instance(data)
    a = state_index(I, state)
    weights, costs = _leaf_weights(I, a, leaf_weights)
    W = sum(weights, F(0))
    best = None
    candidates = []
    for s in range(I['k'] + 1):
        cost, blocker, _ = _cost_tree(I, a, s, costs)
        violation = W - cost - (I['k'] - s)
        candidates.append({'blocker_branching': s, 'cost': cost,
                           'threshold': I['k'] - s, 'violation': violation})
        if best is None or violation > best[0]:
            best = violation, blocker, cost
    maximum, blocker, blocker_cost = best
    occupied = {I['resource_index'][u] for u in blocker['leaf_resources']}
    state_resources = set(I['states'][a]['wiring'].values())
    available = state_resources - occupied
    q, witness = _value_state(I, a, available)
    actual_weight = sum((costs[i] for i in available), F(0))
    if actual_weight - q != maximum or maximum < 0:
        raise RuntimeError('actual complementary witness missed separation maximum')
    return {'source_claims': [SOURCE_CLAIMS[2]], 'mode': 'exact-minorant-separation',
            'state_index': a, 'leaf_weights': weights, 'weight_total': W,
            'feasible': maximum == 0, 'maximum_violation': maximum,
            'witness_subset': [I['resources'][i] for i in sorted(available)],
            'witness_value': q, 'witness_weight': actual_weight,
            'witness_tree': witness, 'dual_blocker': blocker,
            'dual_blocker_cost': blocker_cost, 'candidates': candidates,
            'dual_blocker_meaning': 'Combinatorial complementary branching-tree duality, not an LP dual solution.'}


def compact_minorant_lp(data, state=0, objective_subset=None):
    I = build_instance(data)
    a = state_index(I, state)
    tree = I['states'][a]
    leaves, nodes = tree['leaves'], tree['nodes']
    node_id = {p: i for i, p in enumerate(nodes)}
    w_names = {p: 'w:' + str(i) for i, p in enumerate(leaves)}
    variables = []
    constraints = []

    def variable(name, upper):
        variables.append({'name': name, 'lower': 0, 'upper': upper})

    def row(name, sense, coefficients, rhs):
        constraints.append({'name': name, 'sense': sense,
                            'coefficients': [[v, c] for v, c in coefficients if c], 'rhs': rhs})

    for name in w_names.values():
        variable(name, 1)
    row('full-set-bound', 'le', [(name, 1) for name in w_names.values()], I['k'])
    for s in range(1, I['k'] + 1):
        c_names = {p: 'c:' + str(node_id[p]) + ':' + str(s) for p in nodes}
        for p in nodes:
            variable(c_names[p], I['k'])
        for p in leaves:
            row('leaf:' + str(node_id[p]) + ':' + str(s), 'eq',
                [(c_names[p], 1), (w_names[p], -1)], 0)
        for p in nodes:
            if p not in tree['children']:
                continue
            z = 'z:' + str(node_id[p]) + ':' + str(s)
            variable(z, I['k'])
            t_names = []
            for d in tree['children'][p]:
                t = 't:' + str(node_id[p]) + ':' + str(s) + ':' + str(d)
                variable(t, I['k'])
                t_names.append(t)
                row('positive-part:' + t, 'ge',
                    [(t, 1), (z, -1), (c_names[p + (d,)], 1)], 0)
            row('smallest-sum:' + str(node_id[p]) + ':' + str(s), 'le',
                [(c_names[p], 1), (z, -s)] + [(t, 1) for t in t_names], 0)
        row('root-bound:' + str(s), 'ge',
            [(c_names[()], 1)] + [(name, -1) for name in w_names.values()], -I['k'] + s)
    permitted = set(tree['wiring'].values())
    target = permitted if objective_subset is None else subset_indices(I, objective_subset, permitted)
    objective = [[w_names[p], 1] for p in leaves if tree['wiring'][p] in target]
    return {'source_claims': [SOURCE_CLAIMS[2]], 'mode': 'compact-minorant-LP-data',
            'state_index': a, 'k': I['k'], 'h': I['h'],
            'leaf_coordinates': [{'variable': w_names[p], 'path': list(p),
                                  'resource': I['resources'][tree['wiring'][p]]} for p in leaves],
            'variables': variables, 'constraints': constraints,
            'objective': {'sense': 'maximize', 'coefficients': objective},
            'generic_LP_optimization_implemented': False, 'solver_used': None,
            'scope': 'Exact compact constraint data only; no generic LP optimum has been computed.'}


def minorant_extension(data, state, leaf_weights):
    """Give auxiliaries for an already verified minorant; no LP optimization."""
    I = build_instance(data)
    a = state_index(I, state)
    weights, costs = _leaf_weights(I, a, leaf_weights)
    if not separate_minorant(data, a, weights)['feasible']:
        raise ValueError('input weights are not an additive minorant')
    tree = I['states'][a]
    node_id = {p: i for i, p in enumerate(tree['nodes'])}
    assignment = {'w:' + str(i): weight for i, weight in enumerate(weights)}
    for s in range(1, I['k'] + 1):
        _, _, dp = _cost_tree(I, a, s, costs)
        for p in tree['nodes']:
            assignment['c:' + str(node_id[p]) + ':' + str(s)] = dp[p]
        for p in tree['children']:
            z = sorted(dp[p + (d,)] for d in tree['children'][p])[s - 1]
            assignment['z:' + str(node_id[p]) + ':' + str(s)] = z
            for d in tree['children'][p]:
                assignment['t:' + str(node_id[p]) + ':' + str(s) + ':' + str(d)] = max(F(0), z - dp[p + (d,)])
    return assignment


def encode(k, h, state_resources, resources=None):
    """Audit fixture only; production requires explicit complete leaf addresses."""
    paths = list(product(range(k), repeat=h))
    states = []
    ground = [] if resources is None else list(resources)
    for a, row in enumerate(state_resources):
        if len(row) != len(paths):
            raise ValueError('wrong explicit leaf count')
        states.append({'id': a, 'leaves': [{'path': list(p), 'resource': u} for p, u in zip(paths, row)]})
        if resources is None:
            for u in row:
                if u not in ground:
                    ground.append(u)
    return {'k': k, 'h': h, 'resources': ground, 'states': states}


def jsonable(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, dict):
        return {str(k): jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (tuple, list)):
        return [jsonable(v) for v in obj]
    return obj


def audit():
    """Small explicit exhaustive oracles, distinct from production recurrences."""
    from random import Random
    import hashlib
    import platform
    import time
    started = time.perf_counter()
    rng = Random(1111703)
    counts = Counter()
    certificates = []

    def all_subtree_masks(k, h, r):
        # Enumerate every child choice and Cartesian combination; no h-index
        # recurrence and no min-cost recurrence from the production code.
        if r == 0:
            return [0]
        def visit(prefix):
            if len(prefix) == h:
                index = 0
                for d in prefix:
                    index = index * k + d
                return [1 << index]
            children = [visit(prefix + (d,)) for d in range(k)]
            answer = []
            for digits in combinations(range(k), r):
                for masks in product(*(children[d] for d in digits)):
                    total = 0
                    for mask in masks:
                        total |= mask
                    answer.append(total)
            return answer
        return visit(())

    def brute_q(mask, families):
        return max(r for r, trees in enumerate(families)
                   if any(tree & mask == tree for tree in trees))

    def check_tree(data, tree):
        k, h = data['k'], data['h']
        r = tree['branching']
        state = data['states'][tree['state_index']]
        wiring = {tuple(leaf['path']): leaf['resource'] for leaf in state['leaves']}
        leaves = [tuple(p) for p in tree['leaf_paths']]
        if r == 0:
            assert not leaves and not tree['internal_paths'] and not tree['leaf_resources']
            return
        assert len(leaves) == len(set(leaves)) == r ** h
        assert all(p in wiring for p in leaves)
        assert tree['leaf_resources'] == [wiring[p] for p in leaves]
        children = {}
        for p in leaves:
            for depth in range(h):
                children.setdefault(p[:depth], set()).add(p[depth])
        assert all(len(ds) == r for ds in children.values())
        assert set(children) == {tuple(p) for p in tree['internal_paths']}
        counts['actual_branching_tree_certificates_checked'] += 1

    def check_lp_rows(lp, assignment):
        assert set(assignment) == {v['name'] for v in lp['variables']}
        for v in lp['variables']:
            assert v['lower'] <= assignment[v['name']] <= v['upper']
        for row in lp['constraints']:
            actual = sum((coefficient * assignment[name] for name, coefficient in row['coefficients']), F(0))
            if row['sense'] == 'le':
                assert actual <= row['rhs']
            elif row['sense'] == 'ge':
                assert actual >= row['rhs']
            else:
                assert row['sense'] == 'eq' and actual == row['rhs']
        counts['compact_LP_auxiliary_certificates_checked'] += 1

    for k, h in ((1, 1), (1, 7), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2)):
        N = k ** h
        data = encode(k, h, [list(range(N))])
        families = [all_subtree_masks(k, h, r) for r in range(k + 1)]
        truth = [brute_q(mask, families) for mask in range(1 << N)]
        formula = full_envelope(data)
        maxima = [max(mask.bit_count() for mask in range(1 << N) if truth[mask] <= t)
                  for t in range(k + 1)]
        assert maxima == formula['largest_q_le_t_leaf_counts']
        for mask, expected in enumerate(truth):
            subset = [u for u in range(N) if mask >> u & 1]
            result = value(data, subset)
            assert result['value'] == expected
            check_tree(data, result['witness'])
            assert set(result['witness']['leaf_resources']) <= set(subset)
            assert mask.bit_count() * formula['uniform_leaf_weight'] <= expected
            counts['all_explicit_leaf_subsets'] += 1
        counts['exact_full_envelope_formula_instances'] += 1
        uniform = [formula['uniform_leaf_weight']] * N
        assert separate_minorant(data, 0, uniform)['feasible']
        for r in range(k + 1):
            cost_result = min_cost_subtree(data, 0, r, uniform)
            check_tree(data, cost_result['witness'])
            exact_cost = min(sum((uniform[u] for u in range(N) if mask >> u & 1), F(0))
                             for mask in families[r])
            assert cost_result['cost'] == exact_cost
            assert sum((uniform[u] for u in cost_result['witness']['leaf_resources']), F(0)) == exact_cost
            counts['public_minimum_cost_subtree_queries'] += 1
        lp = compact_minorant_lp(data)
        check_lp_rows(lp, minorant_extension(data, 0, uniform))
        if N <= 4:
            pairs = product(range(1 << N), repeat=2)
        else:
            pairs = ((rng.randrange(1 << N), rng.randrange(1 << N)) for _ in range(32))
        for left, right in pairs:
            assert truth[left | right] <= truth[left] + truth[right]
            counts['subadditive_pairs_checked'] += 1
        weight_cases = list(product((F(0), F(1)), repeat=N)) if N <= 4 else [
            tuple(F(rng.randrange(7), rng.randrange(1, 6)) for _ in range(N)) for _ in range(10)]
        for weights in weight_cases:
            result = separate_minorant(data, 0, weights)
            exact = max(sum((weights[u] for u in range(N) if mask >> u & 1), F(0)) - truth[mask]
                        for mask in range(1 << N))
            assert result['maximum_violation'] == exact
            chosen = sum(1 << u for u in result['witness_subset'])
            assert result['witness_value'] == truth[chosen]
            assert result['witness_weight'] - result['witness_value'] == exact
            for candidate in result['candidates']:
                s_candidate = candidate['blocker_branching']
                exact_cost = min(sum((weights[u] for u in range(N) if mask >> u & 1), F(0))
                                 for mask in families[s_candidate])
                assert candidate['cost'] == exact_cost
                counts['all_cost_candidates_vs_subtree_enumeration'] += 1
            check_tree(data, result['dual_blocker'])
            s = result['dual_blocker']['branching']
            brute_cost = min(sum((weights[u] for u in range(N) if mask >> u & 1), F(0)) for mask in families[s])
            assert result['dual_blocker_cost'] == brute_cost
            assert set(result['dual_blocker']['leaf_resources']).isdisjoint(result['witness_subset'])
            assert set(result['dual_blocker']['leaf_resources']) | set(result['witness_subset']) == set(range(N))
            counts['exact_separation_vs_full_subset_OPT'] += 1

    # Two overlapping states plus a ground resource outside every state.
    data = encode(2, 2, [[0, 1, 2, 3], [0, 2, 4, 5]], resources=list(range(7)))
    families = [all_subtree_masks(2, 2, r) for r in range(3)]
    state_rows = ([0, 1, 2, 3], [0, 2, 4, 5])
    ground_values = []
    for mask in range(1 << 7):
        ground_values.append(max(brute_q(sum(1 << j for j, u in enumerate(row) if mask >> u & 1), families)
                                 for row in state_rows))
    signed = [[F(0)] * 7, [F(2)] * 6 + [F(-1, 3)],
              [F(-2, 3), F(1, 3), F(0), F(4, 3), F(-1, 3), F(1), F(-2, 3)],
              [F(1, 10 ** 100 + 151)] * 6 + [F(-1, 10 ** 100 + 151)]]
    for _ in range(20):
        signed.append([rng.choice((F(-2, 3), F(0), F(1, 3), F(4, 3))) for _ in range(7)])
    for t, prices in enumerate(signed):
        result = exact_demand(data, prices)
        optimum = max(F(ground_values[mask]) - sum((prices[u] for u in range(7) if mask >> u & 1), F(0))
                      for mask in range(1 << 7))
        chosen = sum(1 << u for u in result['subset'])
        actual = F(ground_values[chosen]) - sum((prices[u] for u in result['subset']), F(0))
        assert optimum == result['objective'] == actual
        assert all(u in result['subset'] for u, p in enumerate(prices) if p < 0)
        check_tree(data, result['witness'])
        check_tree(data, result['minimum_cost_candidate_tree'])
        counts['signed_price_vectors_vs_all_ground_subsets'] += 1
        if t < 4:
            certificates.append({'name': 'shared-states-signed-prices-' + str(t),
                                 'instance': data, 'prices': prices, 'result': result})
    # Explicit k=1 depth, mixed exact labels, and negative outside-ground image.
    unary = encode(1, 30, [[17], ['leaf']], resources=[17, 'leaf', 'unused'])
    result = exact_demand(unary, ['1/3', '2/3', '-5/7'])
    assert result['subset'] == [17, 'unused'] and result['objective'] == F(29, 21)
    check_tree(unary, result['witness'])
    counts['unary_deep_signed_boundary'] += 1
    certificates.append({'name': 'unary-deep-negative-unused-resource', 'instance': unary, 'result': result})

    nonxos = encode(3, 2, [list(range(9))])
    subset = [0, 1, 2, 3, 4, 5, 6]
    result = value(nonxos, subset)
    assert result['value'] == 2 and F(len(subset), 3) > 2
    formula = full_envelope(nonxos)
    assert formula['envelope_full'] == F(9, 5) < formula['q_full'] == 3
    violating = separate_minorant(nonxos, 0, [F(1, 3)] * 9)
    assert not violating['feasible'] and violating['maximum_violation'] == F(2, 3)
    counts['non_XOS_exact_certificate'] += 1
    certificates.append({'name': 'non-XOS-three-ary-height-two', 'instance': nonxos,
                         'subset': subset, 'value_result': result, 'full_envelope': formula,
                         'uniform-full-value-minorant-objection': violating,
                         'scope': 'Non-XOS uses the proved symmetry/full-envelope theorem, not an implemented generic LP solver.'})
    lp = compact_minorant_lp(nonxos, 0, subset)
    extension = minorant_extension(nonxos, 0, [F(1, 5)] * 9)
    check_lp_rows(lp, extension)
    certificates.append({'name': 'compact-LP-data-and-feasible-uniform-support',
                         'instance': nonxos, 'LP_data': lp, 'auxiliary_assignment': extension})

    base = encode(2, 1, [[0, 1]], resources=[0, 1, 2])
    invalid_instances = []
    def copied():
        return json.loads(json.dumps(base))
    bad = copied(); bad['states'][0]['leaves'][1]['resource'] = 0
    invalid_instances.append(bad)
    bad = copied(); bad['states'][0]['leaves'].pop()
    invalid_instances.append(bad)
    bad = copied(); bad['states'][0]['leaves'][0]['path'] = [True]
    invalid_instances.append(bad)
    bad = copied(); bad['states'][0]['leaves'][0]['resource'] = 99
    invalid_instances.append(bad)
    bad = copied(); bad['states'] = []
    invalid_instances.append(bad)
    bad = copied(); bad['resources'] = [0, 0, 2]
    invalid_instances.append(bad)
    bad = copied(); bad['k'] = 0
    invalid_instances.append(bad)
    bad = copied(); bad['h'] = 0
    invalid_instances.append(bad)
    bad = copied(); bad['k'] = 10 ** 100; bad['h'] = 10 ** 100
    invalid_instances.append(bad)
    for instance in invalid_instances:
        try:
            value(instance, [])
        except ValueError:
            counts['invalid_instances_rejected'] += 1
        else:
            raise AssertionError('invalid explicit tree accepted')
    invalid_calls = [lambda: exact_demand(base, [0, 0]),
                     lambda: exact_demand(base, [0.5, 0, 0]),
                     lambda: exact_demand(base, [True, 0, 0]),
                     lambda: exact_demand(base, ['NaN', 0, 0]),
                     lambda: exact_demand(base, ['1/0', 0, 0]),
                     lambda: value(base, [99]),
                     lambda: value(base, [0, 0]),
                     lambda: separate_minorant(base, 0, [-1, 1]),
                     lambda: separate_minorant(base, 0, [1]),
                     lambda: compact_minorant_lp(base, 0, [2]),
                     lambda: min_cost_subtree(base, 0, 3, [0, 0])]
    for call in invalid_calls:
        try:
            call()
        except ValueError:
            counts['invalid_queries_rejected'] += 1
        else:
            raise AssertionError('invalid exact query accepted')
    return {'status': 'passed', 'source_claims': SOURCE_CLAIMS,
            'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'seed': 1111703, 'python': platform.python_version(), 'counts': dict(counts),
            'actual_subset_and_blocker_certificates': certificates,
            'scope': 'Finite exact checks against independent subtree enumeration and full subset enumeration. '
                     'Production implements value/demand and single-state separation, plus compact LP data and given-support auxiliaries. '
                     'No generic LP optimization, no NP-hardness, no UM schedule or approximation breakthrough.',
            'elapsed_seconds': time.perf_counter() - started}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input')
    parser.add_argument('--output')
    parser.add_argument('--mode', choices=['value', 'demand', 'cost', 'minorant', 'formula', 'lp'], default='value')
    args = parser.parse_args()
    if args.input:
        payload = json.loads(Path(args.input).read_text())
        keys = {'value': {'instance', 'subset'}, 'demand': {'instance', 'prices'},
                'cost': {'instance', 'state', 'branching', 'leaf_weights'},
                'minorant': {'instance', 'state', 'leaf_weights'},
                'formula': {'instance', 'state'}, 'lp': {'instance', 'state'}}
        allowed = keys[args.mode]
        if type(payload) is not dict or (set(payload) != allowed and not
                (args.mode == 'lp' and set(payload) == allowed | {'objective_subset'})):
            raise ValueError('exact query payload keys required')
        if args.mode == 'value':
            result = value(payload['instance'], payload['subset'])
        elif args.mode == 'demand':
            result = exact_demand(payload['instance'], payload['prices'])
        elif args.mode == 'cost':
            result = min_cost_subtree(payload['instance'], payload['state'], payload['branching'], payload['leaf_weights'])
        elif args.mode == 'minorant':
            result = separate_minorant(payload['instance'], payload['state'], payload['leaf_weights'])
        elif args.mode == 'formula':
            result = full_envelope(payload['instance'], payload['state'])
        else:
            result = compact_minorant_lp(payload['instance'], payload['state'], payload.get('objective_subset'))
    else:
        result = audit()
    output = json.dumps(jsonable(result), ensure_ascii=False, indent=2) + '\n'
    if args.output:
        with Path(args.output).open('x') as handle:
            handle.write(output)
    else:
        sys.stdout.write(output)
