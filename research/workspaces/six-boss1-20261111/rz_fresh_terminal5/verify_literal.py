"""Independent standard-library verification of the full five-cone completion.

Does not import the solver, the bridge auditor, or any prior program.
Reads the original frozen alpha/beta dictionaries; directly sums each true
row with literal named query indices; solves four two-state tail policies;
then checks every named i != j, old R/Z state, and all 16 x 16 hidden pairs.
"""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
POINT = REPO / 'research/workspaces/six-boss1-20261111/union_augmented_lp/augmented_lp_exact.json'
PACKAGE = REPO / 'research/workspaces/six-boss2-20261111-cross/coverage_bridge/selected_prefix_tail_5752.json'
PSHA = 'b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3'
KSHA = '595e7386cfacc591f513fe477453e94d9e2271e4cb63ce3f5c57a8dc34fabd50'
HIDDEN = tuple(product(range(2), repeat=4))


def digest(p):
    return sha256(p.read_bytes()).hexdigest()


def convert(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): convert(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [convert(v) for v in x]
    return x


def frac(n, d):
    if d == 0:
        assert n == 0
        return F(0)
    return F(n, d)


assert digest(POINT) == PSHA and digest(PACKAGE) == KSHA
point = json.loads(POINT.read_text())
package = json.loads(PACKAGE.read_text())
contracts = {}
for branch, number, scale in [('A', 2, 999), ('B', 13, 10000)]:
    row = package['cuts'][number - 1]
    assert row['source'] == 4 and row['k'] == 3 and F(row['delta']) == F(1, 2)
    aa = {name.replace('@Bj', '@Cj'): scale * F(weight) for name, weight in row['alpha'].items()}
    bb = {name: scale * F(weight) for name, weight in row['beta'].items()}
    assert all(weight >= 0 for weight in (*aa.values(), *bb.values()))
    assert not any('capacity' in key for key in (*aa, *bb))
    contracts[branch] = aa, bb


def static_queries(words, i, j, actual):
    return {'Ti': (words[i][0],), 'Tj': (words[j][0],),
            'Ci': (words[i][2],), 'Cj': (words[j][2],),
            'A6': (actual[5],), 'other_T': tuple(words[k][0] for k in range(6) if k != i and k != j)}


def raw_prefix(branch, p, D, initial, hidden, queries):
    alpha, _ = contracts[branch]
    b, c, j, v = hidden
    memberships = {'t': initial, 'b': b, 'c': c, 'j': j, 'v': v}
    first_total, second_total = p + initial + b + c, p + c + j + v
    out = F(0)
    for coordinate, weight in alpha.items():
        if coordinate == 'sourceT':
            feature = frac(initial, first_total)
        elif coordinate == 'sourceC':
            feature = frac(c, second_total)
        elif coordinate.startswith('price:'):
            feature = F(memberships[coordinate[6:]], D)
        else:
            operation, at, query_name = coordinate.partition('@')
            family, variables = operation.split(':')
            query_values = queries[query_name] if at else (None,)
            feature = F(0)
            for query_bit in query_values:
                mm = dict(memberships)
                if at:
                    mm['q'] = query_bit
                if family == 'last1':
                    term = F(mm[variables], p + initial + b + 1) - frac(c, first_total)
                elif family == 'last2':
                    term = F(mm[variables], p + c + j + 1) - frac(v, second_total)
                else:
                    assert family in ('pair1', 'pair2')
                    xx, yy = (mm[k] for k in variables.split(','))
                    background, first, last = (p + initial, b, c) if family == 'pair1' else (p + c, j, v)
                    term = F(xx + yy, background + 1)
                    term -= F(xx * yy + first, (background + 1) * (background + 2))
                    term -= frac(first + last, background + first + last)
                feature += term / len(query_values)
        out += weight * feature
    return out


@lru_cache(None)
def raw_tail(branch, p, D, Ti, Tj, others):
    _, beta = contracts[branch]
    queries = {'Ti': (Ti,), 'Tj': (Tj,), 'other_T': others}
    edges = {}
    for t, c in product(range(2), repeat=2):
        candidates = []
        for middle in range(2):
            load = p + t + middle + c
            val = beta['source'] * frac(t, load)
            val += (beta['alpha_mid'] * middle + beta['alpha_last'] * c) / D
            for name, weight in beta.items():
                if name.startswith('mu_'):
                    bits = queries[name[3:]]
                    val += sum((weight * (F(bit, p + t + middle + 1) - frac(c, load)) / len(bits) for bit in bits), F(0))
            candidates.append(val)
        edges[t, c] = min(candidates)
    choices = [[], []]
    for action0, action1 in product(range(2), repeat=2):
        a, b = F(1) - F(action0 == 0, 2), -F(action0 == 1, 2)
        c, d = -F(action1 == 0, 2), F(1) - F(action1 == 1, 2)
        determinant = a * d - b * c
        choices[0].append((d * edges[0, action0] - b * edges[1, action1]) / determinant)
        choices[1].append((a * edges[1, action1] - c * edges[0, action0]) / determinant)
    V = tuple(min(options) for options in choices)
    for t in range(2):
        assert V[t] == min(edges[t, c] + V[c] / 2 for c in range(2))
    return tuple(value / 2 for value in V)


def main():
    started = time.monotonic()
    saved = json.loads((HERE / 'local_tables_exact.json').read_text())
    completion = json.loads((HERE / 'completion_exact.json').read_text())
    knapsack = json.loads((HERE / 'knapsack_exact.json').read_text())
    assert completion['point_sha256'] == PSHA
    reference = {(s['hist_column'], tuple(s['wi']), tuple(s['wj']), tuple(s['old_state'])): s for s in saved['states']}
    chosen = {s['state_id']: s for s in completion['rows']}
    hist = {}
    group = defaultdict(dict)
    current = None
    word_types = tuple(product(range(2), repeat=3))
    for index, column in enumerate(point['columns'][:4849]):
        if column['kind'] == 'hist':
            current = index
            words = tuple(w for w, multiplicity in zip(word_types, column['hist']) for _ in range(multiplicity))
            hist[index] = (tuple(map(int, column['actual_bits'])), words, F(column['weight']))
        elif column['kind'] == 'joint-reply' and column['group'][:2] == [1, 0]:
            _, _, wi, wj = column['group']
            key = (current, tuple(wi), tuple(wj))
            group[key][tuple(column['state'])] = F(column['weight'])
    for key, distribution in group.items():
        distribution[0, 0] = hist[key[0]][2] - sum(distribution.values(), F(0))
        assert min(distribution.values()) >= 0
    income = [sum((mass * frac(actual[i], sum(actual)) for actual, words, mass in hist.values()), F(0)) for i in range(6)]
    assert sum(income, F(0)) == F(point['W'])
    source_budget, price_budget = {}, {}
    for branch, (alpha, beta) in contracts.items():
        source_budget[branch] = alpha['sourceT'] + alpha['sourceC'] + beta['source']
        price_budget[branch] = sum((weight for name, weight in alpha.items() if name.startswith('price:')), F(0)) + beta['alpha_mid'] + beta['alpha_last']
    assert source_budget == {'A': F(999), 'B': F(10000)}
    assert price_budget == {'A': F(139), 'B': F(1358)}
    budget = {b: source_budget[b] * income[3] + price_budget[b] * income[5] for b in ('A', 'B')}
    totals = dict.fromkeys(('A', 'B', 'Z', 'R_to_vB', 'Z_to_vA'), F(0))
    dual_values, unconstrained_queries = dict(A=F(0), B=F(0)), dict(A=F(0), B=F(0))
    count = dict(histograms=len(hist), zero_histograms=sum(m == 0 for a, w, m in hist.values()),
                 named_pairs=0, old_states=0, hidden_pairs=0, raw_prefix_values=0,
                 coefficientwise_dominance_checks=0, old_marginal_equalities=0,
                 nonzero_common_atoms=0, zero_old_states=0)
    seen = set()
    for hist_id, (actual, words, hist_mass) in hist.items():
        p, P, D, n = sum(actual[:3]), sum(actual[:4]), sum(actual[:5]) + 1, sum(w[0] for w in words)
        for i in range(6):
            for j in range(6):
                if i == j:
                    continue
                count['named_pairs'] += 1
                pair_mass = F(0)
                query = static_queries(words, i, j, actual)
                psis = {b: raw_tail(b, p, D, words[i][0], words[j][0], query['other_T']) for b in ('A', 'B')}
                for r, z in product(range(2), repeat=2):
                    key = (hist_id, words[i], words[j], (r, z))
                    ref = reference[key]
                    seen.add(ref['id'])
                    assert (i, j) in map(tuple, ref['named_pairs'])
                    mm = group[hist_id, words[i], words[j]][r, z]
                    assert mm == F(ref['old_group_mass'])
                    count['old_states'] += 1
                    count['zero_old_states'] += mm == 0
                    mass = mm / 30
                    dR, dZ = p + words[i][0] + words[j][2] + 1, P + r + 1
                    arrays = {b: [raw_prefix(b, p, D, r if b == 'A' else z, hh, query) + psis[b][hh[3]] for hh in HIDDEN] for b in ('A', 'B')}
                    count['raw_prefix_values'] += 32
                    for b in ('A', 'B'):
                        assert arrays[b] == list(map(F, ref[b + '_costs']))
                        minima = [min(arrays[b][k] for k, hh in enumerate(HIDDEN) if hh[3] == v) for v in range(2)]
                        assert minima == list(map(F, ref[b + '_min_by_v']))
                        eta = F(knapsack['solutions'][b]['dual_multiplier'])
                        anchor, denominator = (z, dZ) if b == 'A' else (r, dR)
                        dual_values[b] += mass * min(arrays[b][k] + eta * F(hh[3] - anchor, denominator) for k, hh in enumerate(HIDDEN))
                        canonical = min(range(16), key=lambda k: (arrays[b][k], k))
                        unconstrained_queries[b] += mass * F(HIDDEN[canonical][3] - anchor, denominator)
                    cond = chosen[ref['id']]
                    dist = [[F(0)] * 16 for _ in range(2)]
                    for k, b in enumerate(('A', 'B')):
                        theta = F(cond['probability_vA1' if b == 'A' else 'probability_vB1'])
                        assert 0 <= theta <= 1
                        for v in range(2):
                            ix = ref[b + '_argmin_by_v'][v]
                            assert HIDDEN[ix][3] == v
                            dist[k][ix] = theta if v else 1 - theta
                    cond_sum, mass_sum = F(0), F(0)
                    for ia, ib in product(range(16), repeat=2):
                        count['hidden_pairs'] += 1
                        # Replacing only (b,c,j) with a same-v minimizer
                        # changes precisely one source cost coordinate.
                        assert arrays['A'][ia] >= F(ref['A_min_by_v'][HIDDEN[ia][3]])
                        assert arrays['B'][ib] >= F(ref['B_min_by_v'][HIDDEN[ib][3]])
                        count['coefficientwise_dominance_checks'] += 2
                        probability = dist[0][ia] * dist[1][ib]
                        assert probability >= 0
                        cond_sum += probability
                        atom_mass = mass * probability
                        mass_sum += atom_mass
                        if atom_mass:
                            count['nonzero_common_atoms'] += 1
                            totals['A'] += atom_mass * arrays['A'][ia]
                            totals['B'] += atom_mass * arrays['B'][ib]
                            totals['Z'] += atom_mass * (F(n, 6) - z) / dZ
                            totals['R_to_vB'] += atom_mass * F(HIDDEN[ib][3] - r, dR)
                            totals['Z_to_vA'] += atom_mass * F(HIDDEN[ia][3] - z, dZ)
                    assert cond_sum == 1 and mass_sum == mass
                    assert sum((F(a['probability']) for a in cond['atoms']), F(0)) == 1
                    for atom in cond['atoms']:
                        ia, ib = atom['hA_index'], atom['hB_index']
                        prob = dist[0][ia] * dist[1][ib]
                        assert prob == F(atom['probability'])
                        assert mass * prob == F(atom['per_named_pair_mass'])
                        assert mass * prob * ref['orbit_count'] == F(atom['averaged_mass'])
                    count['old_marginal_equalities'] += 1
                    pair_mass += 30 * mass_sum
                assert pair_mass == hist_mass
    assert len(seen) == len(reference) == len(saved['states']) == 312
    assert count['named_pairs'] == 480 and count['old_states'] == 1920
    assert count['hidden_pairs'] == 491520 and count['raw_prefix_values'] == 61440
    assert count['coefficientwise_dominance_checks'] == 983040
    slacks = dict(alpha=budget['A'] - totals['A'], beta=budget['B'] - totals['B'],
                  lam=-totals['Z'], mu=-totals['R_to_vB'], nu=-totals['Z_to_vA'])
    assert slacks == {k: F(v) for k, v in completion['slacks'].items()}
    assert all(v >= 0 for v in slacks.values())
    for b in ('A', 'B'):
        assert dual_values[b] == totals[b] == F(knapsack['solutions'][b]['minimum_cost'])
        assert budget[b] - totals[b] == F(knapsack['solutions'][b]['exact_slack'])
    assert totals['R_to_vB'] == totals['Z_to_vA'] == 0
    report = dict(status='PASS', full_five_weight_cone_certificate=True,
                  source_zero_faces_included=True, identity_and_budget_check='PASS',
                  counts=count, budgets=budget, raw_cost_totals=totals, slacks=slacks,
                  slacks_float={k: float(v) for k, v in slacks.items()},
                  exact_knapsack_dual_values=dual_values,
                  unconstrained_canonical_minimizer_query_costs=unconstrained_queries,
                  unconstrained_canonical_minimizer_query_costs_float={b: float(v) for b, v in unconstrained_queries.items()},
                  inputs_sha256={str(path.relative_to(REPO)): digest(path) for path in (POINT, PACKAGE, HERE / 'inputs_exact.json', HERE / 'local_tables_exact.json', HERE / 'knapsack_exact.json', HERE / 'completion_exact.json')},
                  verifier_sha256=digest(Path(__file__)), elapsed_seconds=time.monotonic()-started,
                  scope='Only the specified frozen A/B, actual4, family1 off-diagonal R20--R22 cone on the pinned 19662 point. No full-SPE realization or universal half theorem.')
    (HERE / 'independent_verification.json').write_text(json.dumps(convert(report), ensure_ascii=False, indent=2)+'\n')
    print('PASS', report['slacks_float'], flush=True)
    print('literal counts', count, flush=True)
    print('unconstrained query costs', report['unconstrained_canonical_minimizer_query_costs_float'], flush=True)
    print('seconds', report['elapsed_seconds'], flush=True)


if __name__ == '__main__':
    main()
