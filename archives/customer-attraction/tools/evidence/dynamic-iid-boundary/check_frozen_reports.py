"""Bind the four frozen historical files to the existing exact evidence.

The two historical JSON reports are compared in full, as bytes and as parsed
values, against both the preceding cleanup replay and a fresh read-only run of
each original audit. Residual states are additionally rebuilt from binomial
definitions here. This script proves no arbitrary-population welfare bound.
"""
from fractions import Fraction as F
from hashlib import sha256
from math import comb
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / 'frozen-four-provenance.json').read_text())
for row in manifest['sources']:
    raw = (ROOT / row['retained_at']).read_bytes()
    assert len(raw) == row['bytes'] and sha256(raw).hexdigest() == row['sha256']

comparisons = []
for frozen_name, replay_name, script in (
    ('dynamic_iid.json', 'dynamic.json', 'customer_attraction_dynamic_iid.py'),
    ('dynamic_iid_independent.json', 'dynamic-independent.json', 'customer_attraction_dynamic_iid_independent.py'),
):
    frozen = (ROOT / 'original/evidence/runs/2026-10-10' / frozen_name).read_bytes()
    previous = (ROOT / 'replay' / replay_name).read_bytes()
    fresh = subprocess.run(
        [sys.executable, str(ROOT / 'original/tests/audits' / script)],
        check=True, capture_output=True,
    ).stdout
    assert frozen == previous == fresh
    assert json.loads(frozen) == json.loads(previous) == json.loads(fresh)
    comparisons.append({
        'historical_report': frozen_name,
        'sha256': sha256(frozen).hexdigest(),
        'bytes': len(frozen),
        'all_fields_and_bytes_equal_previous_replay': True,
        'all_fields_and_bytes_equal_fresh_read_only_run': True,
    })

game = json.loads((ROOT / 'original/examples/customer_attraction/dynamic_iid_local.json').read_text())
w = {tuple(row['topics']): row['multiplicity'] for row in game['customers']}
historical = json.loads((ROOT / 'original/evidence/runs/2026-10-10/dynamic_iid_independent.json').read_text())


def exact_state(prefix, q):
    r = game['players'] - len(prefix)
    alpha = [F(0) for _ in q]
    potential = Z = rent = coverage = F(0)
    for T, weight in w.items():
        p = sum(a in T for a in prefix)
        t = sum((q[a] for a in T), F(0))
        g = sum((F(comb(r - 1, k)) * t**k * (1-t)**(r-1-k)
                 / (p+1+k) for k in range(r)), F(0))
        for a in T:
            alpha[a] += weight * g
        for k in range(r+1):
            probability = F(comb(r,k)) * t**k * (1-t)**(r-k)
            potential += weight * probability * sum((F(1,p+j) for j in range(1,k+1)), F(0))
            if p+k:
                Z += weight * probability * F(k,p+k)
                rent += weight * probability * F(p,p+k)
                coverage += weight * probability
    assert coverage == Z + rent
    assert Z == r * sum((q[a]*alpha[a] for a in range(len(q))), F(0))
    return {
        'alpha': list(map(str,alpha)), 'potential': str(potential), 'Z': str(Z),
        'rent': str(rent), 'coverage': str(coverage),
    }


states = []
for row in historical['residual_states']:
    q = list(map(F,row['q']))
    assert all(x >= 0 for x in q) and sum(q) == 1
    assert row['support_equalities'] == [a for a,x in enumerate(q) if x]
    state = exact_state(row['prefix'], q)
    assert state['alpha'] == row['all_query_alpha']
    for key, old_key in (
        ('potential','expected_residual_harmonic_potential'), ('Z','Z'),
        ('rent','prefix_rent'), ('coverage','complete_expected_coverage'),
    ):
        assert F(state[key]) == F(row[old_key])
    v = F(row['KKT_multiplier'])
    assert all(F(value) <= v for value in state['alpha'])
    assert all(F(state['alpha'][a]) == v for a in row['support_equalities'])
    assert v - F(state['alpha'][6]) == F(row['outside_P_strict_slack'])
    states.append({'prefix':row['prefix'], 'q':row['q'], **state})

uniform_child = exact_state((6,6,0), [F(1,6)]*6 + [F(0)])
assert F(uniform_child['Z']) == F(194,9) > 21
assert F(uniform_child['potential']) < 27
assert states[1]['potential'] == '27'

print(json.dumps({
    'status':'PASS',
    'historical_files_hash_checked':len(manifest['sources']),
    'frozen_report_comparisons':comparisons,
    'residual_states_independently_rebuilt':states,
    'uniform_old_distribution_at_PPX0':uniform_child,
    'scope':'Historical provenance, complete report equality, and these finite residual states only; no root Z5 evaluation, universal iid bridge, aggregate-security result, or six-player half result.',
}, ensure_ascii=False, indent=2))
