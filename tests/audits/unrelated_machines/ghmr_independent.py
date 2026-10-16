#!/usr/bin/env python3
"""独立核验大边匹配残余过滤与共享备用机反例。

Arithmetic is exact. The optimizer oracle exhaustively enumerates assignments.
The family builder and compressed DP are independently reconstructed; they do
not import the production construction or its mathematical verification code.
Only weighted_cover_matching and filter_domains are imported for testing.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import platform

def construct(k):
    h, a = 1, F(1, k - 1)
    while a < F(1, 2):
        h += 1
        a *= F(k, k - 1)
    jobs, configs, kind = [], [], []

    def node(label):
        configs.append([])
        kind.append(label)
        return len(configs) - 1

    def edge(u, v, pu, pv):
        jobs.append({u: F(pu), v: F(pv)})
        return len(jobs) - 1

    roots = [node('root'), node('root')]
    bridge = edge(*roots, 1, 1)
    metadata = []

    def subtree(u, depth, incoming):
        if depth == 1:
            terminals = [node('terminal') for _ in range(k)]
            outgoing = [edge(u, v, F(1, k), 1) for v in terminals]
            reserves = [edge(terminals[t-1], terminals[t], 1, 1)
                        for t in range(1, k)]
            for ell, v in enumerate(terminals, 1):
                choices = [(F(1, k), (outgoing[ell-1],))]
                if ell > 1:
                    choices.append((F(ell-1, k), (reserves[ell-2],)))
                if ell < k:
                    choices.append((F(k-ell, k), (reserves[ell-1],)))
                configs[v] = choices
            alpha = F(1, k - 1)
            metadata.append((u, terminals, outgoing, reserves))
        else:
            outgoing = []
            for _ in range(k):
                v = node('internal')
                e = edge(u, v, F(1, k), 1)
                outgoing.append(e)
                child_alpha = subtree(v, depth - 1, e)
            alpha = child_alpha * F(k, k-1)
        configs[u] = [(1-alpha, tuple(outgoing))]
        configs[u] += [(alpha / k, (incoming, e)) for e in outgoing]
        return alpha

    for root in roots:
        alpha = subtree(root, h, bridge)
        thinned = []
        for weight, conf in configs[root]:
            if bridge in conf:
                thinned.append((weight / (2*alpha), conf))
                thinned.append((weight*(1-1/(2*alpha)),
                                tuple(e for e in conf if e != bridge)))
            else:
                thinned.append((weight, conf))
        configs[root] = [(w, c) for w, c in thinned if w]
    return jobs, configs, kind, h, metadata

def validate_configuration(jobs, configs, T):
    coverage = [F(0) for _ in jobs]
    for i, choices in enumerate(configs):
        assert sum(w for w, _ in choices) == 1
        for weight, conf in choices:
            assert weight >= 0
            assert len(conf) == len(set(conf))
            assert sum(jobs[e][i] for e in conf) <= T
            for e in conf:
                coverage[e] += weight
    assert coverage == [F(1)] * len(jobs)

def full_weight_matching(jobs, targets, threshold, forced=None):
    """Find matching covering every target. Success certifies W=F_i."""
    mate = {}
    if forced is not None:
        fixed_job, fixed_machine = forced
        assert fixed_machine in jobs[fixed_job]
        assert jobs[fixed_job][fixed_machine] > threshold/2
        mate[fixed_machine] = fixed_job
    else:
        fixed_job, fixed_machine = None, None

    def augment(j, seen):
        for i, p in jobs[j].items():
            if p <= threshold/2 or i == fixed_machine or i in seen:
                continue
            seen.add(i)
            if i not in mate or augment(mate[i], seen):
                mate[i] = j
                return True
        return False

    for j in sorted(set(targets)):
        if j != fixed_job and not augment(j, set()):
            return False
    assigned = {j: i for i, j in mate.items()}
    assert set(targets).issubset(assigned)
    if forced:
        assert assigned[fixed_job] == fixed_machine
    assert all(jobs[j][i] > threshold/2 for j, i in assigned.items())
    return True

def min_reserves_to_z(k, h, B):
    """Exact DP for B in [1,2): minimum integer reserve count routed to z.

    If d stars enter a bottom path gadget, deleting max(d-1,0) reserves
    is necessary and sufficient to orient remaining reserves away from
    those occupied vertices. Bottom stars can be selected freely.
    """
    assert 1 <= B < 2
    costs = {}
    for incoming in (0, 1):
        choices = [max(k-r-1, 0) for r in range(k+1)
                   if incoming+F(r, k) <= B]
        costs[incoming] = min(choices) if choices else None
    for _ in range(1, h):
        old = costs
        costs = {}
        for incoming in (0, 1):
            choices = []
            for r in range(k+1):
                if incoming+F(r, k) > B:
                    continue
                if (r and old[0] is None) or (r < k and old[1] is None):
                    continue
                choices.append(r*(old[0] or 0)+(k-r)*(old[1] or 0))
            costs[incoming] = min(choices) if choices else None
    if None in costs.values():
        return None
    return costs[0]+costs[1]

def optimum_with_z(k):
    h, alpha = 1, F(1, k-1)
    while alpha < F(1, 2):
        h += 1
        alpha *= F(k, k-1)
    for units in range(2*k, 4*k):
        B = F(units, 2*k)
        cost = min_reserves_to_z(k, h, B)
        if cost is not None and F(cost, 2) <= B:
            return h, B, cost
    return h, F(2), None


def exhaustive_matching(neighbors, mandatory, weights, forced=None):
    """Exponential independent oracle; at most three jobs in this audit."""
    required = set(mandatory)
    rewards = dict(weights)
    if forced is not None:
        required.add(forced[0])
        rewards.pop(forced[0], None)
    relevant = sorted(required | rewards.keys())
    best = None
    for sigma in product(*[(None, *neighbors[j]) for j in relevant]):
        used = [i for i in sigma if i is not None]
        if len(used) != len(set(used)):
            continue
        assignment = dict(zip(relevant, sigma))
        if any(assignment[j] is None for j in required):
            continue
        if forced is not None and assignment[forced[0]] != forced[1]:
            continue
        value = sum((rewards.get(j, F(0)) for j in relevant
                     if assignment[j] is not None), F(0))
        if best is None or value > best:
            best = value
    return best


def audit_matching(production):
    checked = 0
    for masks in product(range(4), repeat=3):
        neighbors = {j: [i for i in range(2) if masks[j] & (1 << i)]
                     for j in range(3)}
        # For each job: mandatory, optional absent, weight 1/2, or weight 1.
        for roles in product(range(4), repeat=3):
            mandatory = {j for j in range(3) if roles[j] == 0}
            weights = {j: F(roles[j]-1, 2) for j in range(3) if roles[j] >= 2}
            # Include forced jobs initially absent/optional and nonexistent
            # forced edges: the API must add the former and reject the latter.
            probes = [None]+[(j, i) for j in range(3) for i in range(2)]
            for forced in probes:
                oracle = exhaustive_matching(neighbors, mandatory, weights, forced)
                actual = production.weighted_cover_matching(neighbors, mandatory,
                                                            weights, forced)
                assert (actual is None) == (oracle is None), (
                    neighbors, mandatory, weights, forced, oracle, actual)
                if actual is not None:
                    assert actual['weight'] == oracle
                    assigned = actual['assignment']
                    assert mandatory <= assigned.keys()
                    assert len(set(assigned.values())) == len(assigned)
                    assert all(i in neighbors[j] for j, i in assigned.items())
                    if forced is not None:
                        assert assigned[forced[0]] == forced[1]
                    certificate_weights = dict(weights)
                    if forced is not None:
                        certificate_weights.pop(forced[0], None)
                    assert actual['weight'] == sum(
                        (certificate_weights.get(j, F(0)) for j in assigned), F(0))
                checked += 1
    return checked


def schedules_with_value(matrix):
    n, m = len(matrix[0]), len(matrix)
    choices = [[i for i in range(m) if matrix[i][j] is not None]
               for j in range(n)]
    if any(not c for c in choices):
        return []
    return [(sigma, max((sum((matrix[i][j] for j in range(n) if sigma[j] == i),
                            F(0)) for i in range(m)), default=F(0)))
            for sigma in product(*choices)]


def audit_edge_preservation(production):
    matrices = schedules = 0
    # Exhaustive all 2-machine/3-job matrices from this exact finite alphabet.
    # Values 3/2 test initial p>T pruning, and 1/2 tests the small/big boundary.
    alphabet = (None, F(0), F(1, 2), F(1), F(3, 2))
    for flat in product(alphabet, repeat=6):
        matrix = [list(flat[:3]), list(flat[3:])]
        available = [[i for i in range(2) if matrix[i][j] is not None]
                     for j in range(3)]
        if any(not c for c in available):
            continue
        matrices += 1
        viable = [(s, v) for s, v in schedules_with_value(matrix) if v <= 1]
        actual = production.filter_domains(matrix, F(1))
        for sigma, _ in viable:
            assert actual['feasible']
            assert all(sigma[j] in actual['domains'][j] for j in range(3))
            schedules += 1
    boundaries = [([[]], F(0)),
                  ([[F(0)]], F(0)),
                  ([[F(0), F(0)], [None, F(0)]], F(0)),
                  ([[F(1, 10**90+7)]], F(1, 10**90+7)),
                  ([[None, F(0)], [F(7, 3), None]], F(7, 3)),
                  ([[F(1, 2), F(1, 2)]], F(1)),
                  ([[F(1), F(1)]], F(1))]
    for matrix, target in boundaries:
        actual = production.filter_domains(matrix, target)
        for sigma, value in schedules_with_value(matrix):
            if value <= target:
                assert actual['feasible']
                assert all(sigma[j] in actual['domains'][j] for j in range(len(sigma)))
    # Invalid inputs must be rejected by the input contract rather than used.
    invalid = [([], 1), ([[F(-1)]], 1), ([[None]], 1),
               ([[0.5]], 1), ([[True]], 1), ([[0]], -1)]
    for matrix, target in invalid:
        try:
            production.filter_domains(matrix, target)
        except (ValueError, TypeError):
            pass
        else:
            raise AssertionError(('accepted invalid input', matrix, target))
    return dict(matrices=matrices, feasible_schedules=schedules,
                threshold='1', boundary_cases=len(boundaries),
                rejected_invalid_cases=len(invalid))


def audit_family(production):
    expanded = []
    for k in (2, 3, 4):
        jobs, configs, kind, h, bundles = construct(k)
        T = 1+F(1, k)
        z = len(configs)
        configs.append([(F(1), ())])
        for _, _, _, reserves in bundles:
            for e in reserves:
                jobs[e][z] = F(1, 2)
        validate_configuration(jobs, configs, T)
        small = [{i for i, p in choices.items() if p <= T/2}
                 for choices in jobs]
        mandatory = {e for e, choices in enumerate(small) if not choices}
        assert mandatory == {0}
        unique = [{e for e, choices in enumerate(small) if choices == {i}}
                  for i in range(len(configs))]
        probes = 0
        for e, choices in enumerate(jobs):
            for i, p in choices.items():
                if p <= T/2:
                    continue
                assert full_weight_matching(jobs, mandatory | {e} | unique[i],
                                            T, (e, i))
                probes += 1
        assert all(full_weight_matching(jobs, mandatory | optional, T)
                   for optional in unique)
        matrix = [[choices.get(i) for choices in jobs]
                  for i in range(len(configs))]
        result = production.filter_domains(matrix, T)
        assert result['feasible'] and not result['trace'] and result['rounds'] == 1
        assert result['domains'] == [set(p) for p in jobs]
        row = dict(k=k, height=h, machines=len(configs), jobs=len(jobs),
                   all_optional_matching_witnesses=probes,
                   production_deleted_edges=len(result['trace']),
                   configuration_target=str(T))
        if k in (2, 3):
            # Explicit boundary cases: the asymptotic theorem excludes h=1.
            opt = min(value for _, value in schedules_with_value(matrix))
            assert opt == 1
            row['exhaustive_optimum'] = str(opt)
        expanded.append(row)
    compressed = []
    for k in (4, 5, 8, 16, 32, 64):
        h, optimum, reserve_count = optimum_with_z(k)
        assert h >= 3 and optimum == 2-F(1, k)
        lower = optimum-F(1, 2*k)
        lower_reserves = min_reserves_to_z(k, h, lower)
        assert lower_reserves >= 2**(h-1) >= 4
        assert F(lower_reserves, 2) > lower
        assert optimum/(1+F(1, k)) == 2-F(3, k+1)
        compressed.append(dict(k=k, height=h, optimum=str(optimum),
                               configuration_target=str(1+F(1, k)),
                               ratio=str(optimum/(1+F(1, k))),
                               optimal_z_reserves=reserve_count,
                               immediately_lower_grid=str(lower),
                               lower_grid_min_reserves=str(lower_reserves)))
    return dict(expanded=expanded, compressed=compressed,
                scope='Compressed exact DP only for this symmetric family; not a general OPT oracle')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--module', type=Path,
                        default=Path(__file__).with_name('heavy_matching_residual.py'))
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('ghmr_production', args.module)
    production = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(production)
    output = dict(arithmetic='fractions.Fraction', python=platform.python_version(),
                  independent_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  production_sha256=hashlib.sha256(args.module.read_bytes()).hexdigest(),
                  exhaustive_weighted_matching_cases=audit_matching(production),
                  edge_preservation=audit_edge_preservation(production),
                  family=audit_family(production))
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
