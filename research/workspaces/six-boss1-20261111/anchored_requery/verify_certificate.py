#!/usr/bin/env python3
"""Fraction-only replay of the finite full-cone nonseparation certificate.

No optimizer, discovery function, or certificate-generator module is used.
The saved flows are checked against the actual point and original descriptors.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
POINT = RUN/'discounted_augmented_lp/augmented_lp_exact.json'
MATRIX = RUN/'discounted_augmented_lp/exact_matrix.json.gz'
CERT = HERE/'sampled_cones_exact_certificate_19578.json'
POINT_SHA = 'a4e48a91f0e2c7b65725178d042b515c6bedf11562afdeeea2ae69b815e8f505'
MATRIX_SHA = 'a95bd72e0fdc2b0b93af79b1a0e8b324b6bd1fc8f62abe8a3ce642be4bcc3936'
WORDS = tuple(product((0, 1), repeat=3))
FIXED = [f'A{i+1}' for i in range(6)]+['Ti', 'Bi', 'Ci', 'Tj', 'Bj', 'Cj', 'R', 'Z', 'mean_T', 'mean_B', 'mean_C']


def ratio(n, d):
    assert d or not n
    return F(n, d) if d else F(0)


def expected_atoms(data, source, orbit):
    histograms = {}
    current = None
    for i, col in enumerate(data['columns'][:4849]):
        if col['kind'] == 'hist':
            current = i
            histograms[i] = (col, defaultdict(dict))
        elif col['kind'] == 'joint-reply':
            f, diag, wi, wj = col['group']
            histograms[current][1][f, diag, tuple(wi), tuple(wj)][tuple(col['state'])] = F(col['weight'])
    atoms = defaultdict(F)
    src = F(0); last = F(0)
    for col, groups in histograms.values():
        bits = tuple(map(int, col['actual_bits']))
        hist = col['hist']; mass = F(col['weight'])
        last += mass*ratio(bits[5], sum(bits))
        if source == 'actual5':
            src += mass*ratio(bits[4], sum(bits))
        else:
            src += mass*sum((F(n, 6)*ratio(w[1], sum(bits[:3])+sum(w)) for w, n in zip(WORDS, hist)), F(0))
        for (f, diag, wi, wj), states in groups.items():
            if (f, diag) != orbit:
                continue
            ni, nj = hist[WORDS.index(wi)], hist[WORDS.index(wj)]
            count = (ni if wi == wj else 0) if diag else ni*nj-(ni if wi == wj else 0)
            denominator = 6 if diag else 30
            assert count > 0
            assert set(states) == {(0, 1), (1, 0), (1, 1)}
            states[0, 0] = mass-sum(states.values(), F(0))
            assert min(states.values()) >= 0
            for (r, z), state_mass in states.items():
                values = list(map(F, bits+wi+wj+(r, z)))
                values.extend(F(sum(n*w[k] for w, n in zip(WORDS, hist)), 6) for k in range(3))
                named = tuple(sorted(zip(FIXED, values)))
                if source == 'actual5':
                    p, t0, t1 = sum(bits[:4]), r, z
                else:
                    p, t0, t1 = sum(bits[:3])+wi[0], wj[1+f], r
                key = p, sum(bits[:5]), bits[5], t0, t1, named
                atoms[key] += F(count, denominator)*state_mass
    atoms = {k: m for k, m in atoms.items() if m}
    K = sum((F(c['weight']) for c in data['columns'][:4849] if c['kind'] == 'K'), F(0))
    return atoms, {'source': src, 'alpha_last': last, 'beta_last': K}


def costs(key, previous, current, next_bit, names):
    p, ell, _, _, _, named = key
    query = dict(named)
    query['current'] = F(current)
    query['previous'] = F(previous)
    divisor = p+current+next_bit
    answer = []
    for name in names:
        if name == 'source':
            answer.append(ratio(current, divisor))
        elif name == 'alpha_last':
            answer.append(F(next_bit, ell+1))
        elif name == 'beta_last':
            answer.append(F(next_bit))
        else:
            assert name.startswith('mu_')
            answer.append(query[name[3:]]/(p+current+1)-ratio(next_bit, divisor))
    return answer


def main():
    assert sha256(POINT.read_bytes()).hexdigest() == POINT_SHA
    assert sha256(MATRIX.read_bytes()).hexdigest() == MATRIX_SHA
    data = json.loads(POINT.read_text())
    certificate = json.loads(CERT.read_text())
    assert certificate['point_sha256'] == POINT_SHA
    for item in certificate['inputs']:
        assert sha256((HERE/item['path']).read_bytes()).hexdigest() == item['sha256']
    expected_cases = set(product(('offpath5', 'actual5'), ((0, 0), (1, 0), (1, 1)), (F(0), F(1, 2), F(3, 4)), (2, 4)))
    seen = set()
    results = []
    total_flows = 0
    total_equations = 0
    for case in certificate['cases']:
        source = case['source']; orbit = tuple(case['orbit']); theta = F(case['theta']); memory = case['memory']
        case_key = source, orbit, theta, memory
        assert case_key in expected_cases and case_key not in seen
        seen.add(case_key)
        names = ['source', 'alpha_last', 'beta_last']+['mu_'+q for q in FIXED]+['mu_current']
        if memory == 4:
            names.append('mu_previous')
        assert names == case['parameter_names']
        atoms, external = expected_atoms(data, source, orbit)
        residue = [external.get(n, F(0)) for n in names]
        first = residue.copy()
        observed = {}
        state_list = ((0, 0), (0, 1)) if memory == 2 else ((0, 0), (0, 1), (1, 0), (1, 1))
        for witness in case['occupation_witnesses']:
            v = witness['visible']
            key = tuple(v[:5])+(tuple((n, F(x)) for n, x in v[5]),)
            mass = F(witness['mass'])
            assert key in atoms and key not in observed and atoms[key] == mass > 0
            observed[key] = mass
            prob = list(map(F, witness['probability_next_one']))
            flow = list(map(F, witness['discounted_state_flow']))
            assert len(prob) == len(flow) == memory
            assert all(0 <= p <= 1 for p in prob) and min(flow) >= 0 and sum(flow, F(0)) == 1
            incoming = [F(0)]*memory
            for s, (a, t) in enumerate(state_list):
                for c in (0, 1):
                    transition_mass = flow[s]*(prob[s] if c else 1-prob[s])
                    target = c if memory == 2 else 2*t+c
                    incoming[target] += transition_mass
                    vals = costs(key, a, t, c, names)
                    for j, val in enumerate(vals):
                        residue[j] -= mass*transition_mass*val
            start = key[4] if memory == 2 else 2*key[3]+key[4]
            for s in range(memory):
                assert flow[s]-theta*incoming[s] == (1-theta)*F(s == start)
            vals = costs(key, key[2], key[3], key[4], names)
            for j, val in enumerate(vals):
                first[j] -= mass*val
            total_flows += 1
            total_equations += memory
        assert observed == atoms
        assert {n: str(r) for n, r in zip(names, residue)} == case['all_parameter_residuals']
        assert {n: str(r) for n, r in zip(names, first)} == case['first_edge_parameter_residuals']
        bound = min(residue)
        first_bound = min(first)
        assert bound == F(case['exact_cone_lower_bound'])
        assert first_bound == F(case['first_edge_min_parameter_residual']) >= 0
        assert (1-theta)*first_bound+theta*bound == F(case['anchored_cone_lower_bound'])
        simple_bound = F(1, 400) if source == 'offpath5' else F(1, 2000)
        assert bound > simple_bound
        results.append({'source': source, 'orbit': list(orbit), 'theta': str(theta), 'memory': memory,
                        'exact_lower_bound': str(bound), 'simple_strict_lower_bound': str(simple_bound),
                        'first_edge_nonnegative_for_all_weights': True, 'all_parameter_residuals_equal': True})
    assert seen == expected_cases
    report = {'scope': 'Independent Fraction-only replay; full weight cones at 3 fixed discounts only; necessary point is not an SPE.',
              'point_sha256': POINT_SHA, 'matrix_sha256': MATRIX_SHA,
              'certificate_sha256': sha256(CERT.read_bytes()).hexdigest(),
              'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'cases': len(results), 'rational_occupation_flows': total_flows, 'exact_flow_equations': total_equations,
              'all_literals_and_masses_reconstructed': True, 'all_coordinate_residuals_exact': True,
              'offpath5_uniform_strict_lower_bound': '1/400', 'actual5_uniform_strict_lower_bound': '1/2000',
              'all_first_edge_coordinate_slacks_nonnegative': True, 'results': results}
    output = HERE/'independent_certificate_audit_19578.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'results'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
