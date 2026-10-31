"""Independent adversarial audit of the equal-light unconstrained flow theorem.

Run from any directory:
  python3 tests/audits/kfac_equal_light_flow_adversary.py --output NEW.json
Existing evidence is never overwritten. The independent exhaustive oracle uses
sum_t (X_t^2 - sum_{i:a_i=t} w_i^2)/(2q_t), not a production certificate.
Both the canonical solver and the exact, SHA-256-pinned, already reviewed code
embedded in the archived USER ATTACHMENT are checked against that oracle.
Only the latter is instrumented for residual-graph checks. No arbitrary code
path, external module, or network source is accepted. Changing the code pin
requires reading and reviewing the new embedded code first.

Finite tests support implementations and concrete counterexamples; they do not
prove the universal theorem, polynomial complexity, or literature priority.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path
from random import Random
import re
import sys
import types

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
SOURCE_NOTE = 'history/source/notes/multi_facility/equal_light_flow_pro_report_2026-10-07.md'
REVIEWED_EMBEDDED_CODE_SHA256 = '340ee161a21e3384091b2461c666bda73fe3e96cc838e3c88cb7b45335186a50'
LOCAL_FIXTURE = 'examples/multi_facility/equal_light_flow_local_ne.json'
UNEQUAL_FIXTURE = 'examples/multi_facility/greedy_two_light_potential.json'
SEED = 2026100719


def values(q, c, w, menus, assignment):
    """Definition-level weighted potential and loads; works for unequal w too."""
    x = list(c)
    for i, destination in enumerate(assignment):
        assert destination in menus[i]
        x[min(menus[i])] -= w[i]
        x[destination] += w[i]
    phi = sum(((x[t] ** 2 - sum(w[i] ** 2 for i, s in enumerate(assignment)
                              if s == t)) / (2 * q[t]) for t in range(len(q))), F(0))
    return x, phi


def properties(q, w, menus, assignment, x):
    return dict(
        full_box=all(0 <= z <= 1 for z in x),
        exact_ne=all((x[s] - w[i]) / q[s] <= x[t] / q[t]
                     for i, s in enumerate(assignment) for t in menus[i]),
        home_inequality=all((x[s] - w[i]) / q[s] <= (1 - w[i]) / q[min(menus[i])]
                            for i, s in enumerate(assignment)))


class Audit:
    def __init__(self):
        from multi_facility_spe.equal_light_flow import equal_weight_box_ne
        self.canonical = equal_weight_box_ne
        self.counts = Counter()
        self.check_residual = False
        note = (ROOT / SOURCE_NOTE).read_text(encoding='utf-8')
        blocks = re.findall(r'^```python\n(.*?)^```', note, re.MULTILINE | re.DOTALL)
        assert len(blocks) == 1, 'Expected one archived embedded Python block'
        code = blocks[0]
        digest = hashlib.sha256(code.encode()).hexdigest()
        assert digest == REVIEWED_EMBEDDED_CODE_SHA256, 'Unreviewed source code: refusing execution'
        anchor = '    a = []\n'
        assert code.count(anchor) == 1, 'Instrumentation anchor changed'
        instrumented = code.replace(anchor,
            '        audit_residual(graph, source, sink, total_cost)\n\n' + anchor)
        # A fresh in-memory temporary module; __main__ is false, so no I/O entrypoint runs.
        module = types.ModuleType('reviewed_archived_equal_light_flow')
        module.audit_residual = self.residual
        exec(compile(instrumented, SOURCE_NOTE + ':reviewed-code-block', 'exec'), module.__dict__)
        self.archived = module.equal_weight_box_ne
        self.code_hash = digest
        self.instrumented_hash = hashlib.sha256(instrumented.encode()).hexdigest()

    def residual(self, graph, source, sink, total_cost):
        """Floyd check of the ARCHIVED source constructor, not canonical internals."""
        if not self.check_residual:
            return
        self.counts['archived_residual_graphs_checked'] += 1
        n = len(graph)
        distance = [[None] * n for _ in range(n)]
        for u in range(n):
            distance[u][u] = 0
            for v, _reverse, cap, cost in graph[u]:
                if cap and (distance[u][v] is None or cost < distance[u][v]):
                    distance[u][v] = cost
        for k in range(n):
            for u in range(n):
                if distance[u][k] is None:
                    continue
                for v in range(n):
                    if distance[k][v] is not None:
                        candidate = distance[u][k] + distance[k][v]
                        if distance[u][v] is None or candidate < distance[u][v]:
                            distance[u][v] = candidate
        assert all(distance[u][u] == 0 for u in range(n)), 'Negative residual cycle'
        if any(cap and distance[v][u] is not None and cost + distance[v][u] == 0
               for u in range(n) for v, _rev, cap, cost in graph[u]):
            self.counts['archived_residual_graphs_with_zero_cost_cycles'] += 1

    def instance(self, q, c, delta, A, residual=False):
        self.check_residual = residual
        c, delta = list(map(F, c)), F(delta)
        menus = [tuple(sorted(set(row))) for row in A]
        n, m = len(menus), len(q)
        w = [delta] * n
        base = [c[t] - sum(w[i] for i, row in enumerate(menus) if min(row) == t)
                for t in range(m)]
        self.counts['negative_baseline_instances'] += any(b < 0 for b in base)
        best, minimizers = None, []
        for assignment in product(*menus):
            x, phi = values(q, c, w, menus, assignment)
            self.counts['enumerated_assignments'] += 1
            if best is None or phi < best:
                best, minimizers = phi, [(assignment, x)]
            elif phi == best:
                minimizers.append((assignment, x))
        self.counts['all_global_minima_checked'] += len(minimizers)
        self.counts['tied_minimum_instances'] += len(minimizers) > 1
        self.counts['zero_or_one_optimal_load_instances'] += any(
            any(z in (0, 1) for z in x) for _, x in minimizers)
        for assignment, x in minimizers:
            assert all(properties(q, w, menus, assignment, x).values()), (
                q, c, w, menus, assignment, x)
        optimal_assignments = {a for a, _ in minimizers}
        for label, solver in (('canonical', self.canonical), ('archived', self.archived)):
            output = solver(q, c, w, A)
            assignment = tuple(output['assignment'])
            assert assignment in optimal_assignments, (label, output)
            x, phi = values(q, c, w, menus, assignment)
            assert tuple(map(F, output['X'])) == tuple(x)
            assert F(output['objective']) * delta + sum(
                (b * b / (2 * q[t]) for t, b in enumerate(base)), F(0)) == phi == best
            assert output['augmentations'] == n
            self.counts[label + '_global_oracle_instances'] += 1
        self.counts['instances'] += 1


def strict_greedy(data):
    """Independent implementation of the canonical new-coverage/add-seat rule."""
    sites = data['sites']
    clients = data['clients']
    weights = [F(row['weight']) for row in clients]
    q = {site: 0 for site in sites}
    assignment = [None] * len(clients)
    trace = []
    for _ in range(data['k']):
        scores = {}
        for site in sites:
            if q[site]:
                scores[site] = sum(weights[i] for i, s in enumerate(assignment)
                                   if s == site) / (q[site] + 1)
            else:
                scores[site] = sum((weights[i] for i, row in enumerate(clients)
                                    if assignment[i] is None and site in row['sites']), F(0))
        maximum = max(scores.values())
        winners = [site for site in sites if scores[site] == maximum]
        assert len(winners) == 1, ('Greedy witness is not strict', scores)
        chosen = winners[0]
        if not q[chosen]:
            for i, row in enumerate(clients):
                if assignment[i] is None and chosen in row['sites']:
                    assignment[i] = chosen
        q[chosen] += 1
        trace.append((chosen, maximum))
    assert all(s is not None for s in assignment)
    opening_order = list(dict.fromkeys(s for s, _ in trace))
    normalized_order = sorted(opening_order, key=lambda s: (-q[s], opening_order.index(s)))
    gamma = trace[-1][1]
    totals = {s: sum(weights[i] for i, t in enumerate(assignment) if t == s) for s in sites}
    movable = [i for i, row in enumerate(clients) if weights[i] < gamma
               and sum(q[s] > 0 for s in row['sites']) > 1]
    normalized = dict(
        q=[q[s] for s in normalized_order],
        c=[totals[s] / gamma - q[s] for s in normalized_order],
        w=[weights[i] / gamma for i in movable],
        menus=[tuple(sorted(normalized_order.index(s) for s in clients[i]['sites'] if q[s]))
               for i in movable])
    assert all(min(normalized['menus'][j]) == normalized_order.index(assignment[i])
               for j, i in enumerate(movable))
    return q, assignment, trace, gamma, movable, normalized_order, normalized


def original_ne(data, q, assignment):
    weights = [F(row['weight']) for row in data['clients']]
    totals = {s: sum(weights[i] for i, t in enumerate(assignment) if t == s)
              for s in data['sites']}
    assert all((totals[s] - weights[i]) / q[s] <= totals[t] / q[t]
               for i, s in enumerate(assignment) for t in data['clients'][i]['sites'] if q[t])
    return totals


def local_ne_counterexample(audit):
    data = json.loads((ROOT / LOCAL_FIXTURE).read_text())
    q, homes, trace, gamma, indices, order, normalized = strict_greedy(data)
    expected = data['expected']
    assert [s for s, _ in trace] == expected['strict_greedy_order']
    assert [str(score) for _, score in trace] == expected['greedy_scores']
    assert [q[s] for s in order] == expected['q']
    assert gamma == F(expected['gamma'])
    assert normalized['c'] == list(map(F, expected['normalized_c']))
    assert normalized['w'] == list(map(F, expected['normalized_w']))
    assert indices == expected['movable_indices']
    assignment = tuple(order.index(s) for s in expected['local_ne_movable_assignment'])
    x, phi = values(**normalized, assignment=assignment)
    verdict = properties(normalized['q'], normalized['w'], normalized['menus'], assignment, x)
    assert verdict == dict(full_box=False, exact_ne=True, home_inequality=True)
    assert x == list(map(F, expected['local_ne_X']))
    base = [normalized['c'][t] - sum(normalized['w'][i] for i, row in
            enumerate(normalized['menus']) if min(row) == t) for t in range(len(order))]
    constant = sum(b * b / (2 * normalized['q'][t]) for t, b in enumerate(base))
    psi = (phi - constant) / normalized['w'][0]
    assert psi == F(expected['local_ne_Psi'])
    full_assignment = homes[:]
    for j, i in enumerate(indices):
        full_assignment[i] = order[assignment[j]]
    totals = original_ne(data, q, full_assignment)
    comparisons = []
    for i, s in enumerate(assignment):
        for t in normalized['menus'][i]:
            if t != s:
                left, right = (x[s] - normalized['w'][i]) / normalized['q'][s], x[t] / normalized['q'][t]
                assert left < right
                comparisons.append(dict(client=indices[i], source=order[s], target=order[t],
                                        source_external=str(left), target_price=str(right)))
    all_states = []
    for a in product(*normalized['menus']):
        y, candidate = values(**normalized, assignment=a)
        all_states.append(dict(assignment=list(a), X=list(map(str, y)),
                               Psi=str((candidate - constant) / normalized['w'][0]),
                               **properties(normalized['q'], normalized['w'], normalized['menus'], a, y)))
    minimum = min(F(record['Psi']) for record in all_states)
    minima = [record for record in all_states if F(record['Psi']) == minimum]
    assert len(minima) == 1 and minimum == F(expected['global_Psi'])
    assert [order[t] for t in minima[0]['assignment']] == expected['unique_global_movable_assignment']
    audit.instance(normalized['q'], normalized['c'], normalized['w'][0], normalized['menus'], True)
    return dict(fixture=LOCAL_FIXTURE, strict_greedy_order=[s for s, _ in trace],
                strict_greedy_scores=[str(v) for _, v in trace], gamma=str(gamma),
                site_order=order, original_ne_totals={s: str(v) for s, v in totals.items()},
                all_four_states=all_states, strict_original_menu_comparisons=comparisons,
                conclusion='Exact NE and H do not imply the lower box, even with equal movable weights and a strict real greedy origin.')


def unequal_counterexample():
    data = json.loads((ROOT / UNEQUAL_FIXTURE).read_text())
    q, homes, trace, gamma, indices, order, normalized = strict_greedy(data)
    assert order == ['H', 'M', 'L', 'R'] and gamma == 45
    assert normalized['q'] == [3, 2, 1, 1]
    assert normalized['c'] == [F(44, 45), F(44, 45), F(2, 45), F(0)]
    assert normalized['w'] == [F(4, 5), F(44, 45)]
    states = []
    for a in product(*normalized['menus']):
        x, phi = values(**normalized, assignment=a)
        states.append(dict(assignment=list(a), X=list(map(str, x)), Phi=str(phi),
                           **properties(normalized['q'], normalized['w'], normalized['menus'], a, x)))
    minimum = min(F(row['Phi']) for row in states)
    minima = [row for row in states if F(row['Phi']) == minimum]
    assert len(minima) == 1 and minima[0]['assignment'] == [1, 2]
    assert minima[0]['X'] == ['8/45', '4/5', '46/45', '0']
    assert minima[0]['exact_ne'] and not minima[0]['full_box'] and not minima[0]['home_inequality']
    actual = homes[:]
    for i, site in zip(indices, ['M', 'L']):
        actual[i] = site
    original_ne(data, q, actual)
    # Return Y: L->M (44/45), X: M->H (4/5); all values are before the batch.
    w0, w1 = F(44, 45), F(4, 5)
    start, middle, end = F(46, 45), F(4, 5), F(8, 45)
    terms = [-w0 * (start - w0), (w0 - w1) * (middle - w1) / 2, w1 * end / 3]
    assert terms == [F(-88, 2025), F(0), F(32, 675)]
    home_phi = next(F(row['Phi']) for row in states if row['assignment'] == [0, 1])
    assert sum(terms) == home_phi - minimum == F(8, 2025) > 0
    assert start - w0 == F(2, 45) > (1 - w0) / 2 == F(1, 90)
    assert end > 1 - w0 and end <= 1 - w1
    return dict(fixture=UNEQUAL_FIXTURE, strict_greedy_order=[s for s, _ in trace],
                strict_greedy_scores=[str(score) for _, score in trace], gamma=str(gamma),
                all_four_states=states, reverse_path=['L', 'M', 'H'],
                reverse_path_weights=[str(w0), str(w1)], path_terms=list(map(str, terms)),
                return_potential_change=str(sum(terms)), violated_H=['2/45', '1/90'],
                conclusion='Unequal endpoint weights and the failed common return threshold matter even when the entire internal potential term is zero. This refutes this selector extension, not existence or all polynomial algorithms.')


def run(random_cases=4500, identity_cases=1000):
    audit = Audit()
    for q in ((1, 1), (2, 1), (3, 2)):
        for c in product((F(0), F(1, 2), F(1)), repeat=2):
            for delta in (F(1, 3), F(1, 2), F(2, 3)):
                for menus in product(((0,), (1,), (0, 1)), repeat=3):
                    audit.instance(q, c, delta, menus, True)
    rng = Random(SEED)
    for z in range(random_cases):
        m, n = rng.randint(1, 5), rng.randint(0, 6)
        q = sorted([rng.randint(1, 8) for _ in range(m)], reverse=True)
        c = [rng.choice([F(0), F(1), F(rng.randint(0, 5), 5)]) for _ in range(m)]
        delta = rng.choice([F(1, 2), F(1, 3), F(2, 3), F(1, 101), F(100, 101)])
        menus = [tuple(t for t in range(m) if rng.randrange(2)) or (rng.randrange(m),)
                 for _ in range(n)]
        audit.instance(q, c, delta, menus, z < 80)
    audit.instance([10 ** 90 + 3, 10 ** 80 + 7], [0, 1], F(1, 10 ** 70 + 33), [(0, 1)] * 8, True)
    audit.instance([], [], F(1, 2), [], True)
    audit.instance([2, 1], [0, 1], F(1, 2), [[1, 0, 1], [0, 1, 0]], True)
    local_witness = local_ne_counterexample(audit)
    unequal_witness = unequal_counterexample()
    invalid = [([1], [0], [F(1, 2), F(1, 3)], [[0], [0]]),
               ([1, 2], [0, 0], [], []), ([True], [0], [], []), ([1], [1.0], [], []),
               ([1], [0], [F(1, 2)], [[]]), ([1], [0], [F(1, 2)], [[True]]),
               ([1], [0], [0], [[0]]), ([1], [0], [1], [[0]])]
    for label, solver in (('canonical', audit.canonical), ('archived', audit.archived)):
        for args in invalid:
            try:
                solver(*args)
            except ValueError:
                audit.counts[label + '_invalid_inputs_rejected'] += 1
            else:
                raise AssertionError((label, 'Invalid input accepted', args))
    for _ in range(identity_cases):
        ell = rng.randint(0, 5)
        weights = [F(rng.randint(1, 9), 10) for _ in range(ell + 1)]
        x = [F(rng.randint(-10, 30), 10) for _ in range(ell + 2)]
        q = [rng.randint(1, 8) for _ in x]
        y = x[:]
        before, after = [F(0)] * len(x), [F(0)] * len(x)
        for j, weight in enumerate(weights):
            y[j] -= weight
            y[j + 1] += weight
            before[j] += weight ** 2
            after[j + 1] += weight ** 2
        actual = sum((y[j] ** 2 - x[j] ** 2 - after[j] + before[j]) / (2 * q[j])
                     for j in range(len(x)))
        expected = -weights[0] * (x[0] - weights[0]) / q[0] + weights[-1] * x[-1] / q[-1]
        expected += sum((weights[j - 1] - weights[j]) * (x[j] - weights[j]) / q[j]
                        for j in range(1, ell + 1))
        assert actual == expected
        audit.counts['nonuniform_path_identities_checked'] += 1
    paths = ['multi_facility_spe/equal_light_flow.py',
             'tests/audits/kfac_equal_light_flow_adversary.py', SOURCE_NOTE,
             LOCAL_FIXTURE, UNEQUAL_FIXTURE]
    return dict(
        schema_version=1, audit='independent_equal_light_flow_adversary', status='all_passed',
        seed=SEED, parameters=dict(random_cases=random_cases, identity_cases=identity_cases,
            exhaustive_grid=dict(q=[[1, 1], [2, 1], [3, 2]], c_values=['0', '1/2', '1'],
                delta_values=['1/3', '1/2', '2/3'], n=3,
                menus='Every labeled tuple of nonempty subsets of two sites'),
            random_generator=dict(m=[1, 5], n=[0, 6], q=[1, 8],
                c='choose 0, 1, or randint(0,5)/5',
                delta=['1/2', '1/3', '2/3', '1/101', '100/101'],
                menus='Independent fair site inclusion; empty replaced by random singleton'),
            archived_residual_scope='All exhaustive grid cases, first 80 random cases, and special fixtures',
            optimization_domain='All legal assignments without box or H prefiltering'),
        counts=dict(audit.counts),
        source_sha256={path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in paths},
        archived_code_sha256=audit.code_hash, instrumented_archived_code_sha256=audit.instrumented_hash,
        instrumentation='Only the hash-pinned archived embedded constructor is instrumented; canonical outputs are independently globally verified. No canonical internal residual-state claim.',
        local_ne_counterexample=local_witness, unequal_counterexample=unequal_witness,
        primary_source_boundaries=[
            dict(url='https://www.ijcai.org/proceedings/2024/0315.pdf',
                statement='Theorem 2/Algorithm 1 gives polynomial fixed-placement favoring client equilibria for all-equal clients. Theorem 3/Algorithm 2 gives arbitrary-k exact SPE existence; its total iteration count is expressly open. The present frozen-heterogeneous-client factor-two interface is a different scope and target.'),
            dict(url='https://courses.csail.mit.edu/6.854/20/Notes/n09-mincostflow.html',
                statement='Negative costs, no-negative-residual-cycle optimality and shortest augmentations are standard tools.'),
            dict(url='https://cgi.csc.liv.ac.uk/~gairing/publications/2004-stoc.pdf',
                statement='The imported exact restricted Nashification theorem concerns identical links. With mixed q, site-uniform source own-weight subtraction is not related-link target insertion.')],
        limitations=[
            'Finite enumeration and random checks do not establish the universal theorem or bit-polynomial complexity.',
            'The original attached ZIP was unavailable; these are newly reproduced checks, not adopted source counts.',
            'Residual graph checks refer to the reviewed embedded attachment implementation only.',
            'SC-K-UNIFORM-LIGHT-FLOW-2 already covered the original-model input class and N unit augmentations.',
            'The additional mathematical property is automatic full box and H for every unconstrained global minimizer.',
            'Unequal-weight and local-NE examples refute the specified stronger selectors, not general boxed NE existence.',
            'No external peer review or comprehensive literature priority certification.'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--random-cases', type=int, default=4500)
    parser.add_argument('--identity-cases', type=int, default=1000)
    args = parser.parse_args()
    if args.random_cases < 0 or args.identity_cases < 0:
        parser.error('Case counts must be nonnegative')
    if args.output and args.output.exists():
        parser.error('Refusing to overwrite existing frozen evidence')
    report = run(args.random_cases, args.identity_cases)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x', encoding='utf-8') as stream:
            json.dump(report, stream, indent=2)
            stream.write('\n')
    print(json.dumps(report['counts'], indent=2))


if __name__ == '__main__':
    main()
