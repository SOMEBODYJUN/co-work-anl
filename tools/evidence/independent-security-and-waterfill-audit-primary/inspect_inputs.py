"""Inspect all real frozen input fields and prepare a byte-exact local mirror.

This does not execute any primary auditor or any historical generator.
"""
from pathlib import Path
from fractions import Fraction
from collections import Counter
from itertools import product
import ast
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
E = ROOT / 'tools/evidence/independent-security-and-waterfill-audit-primary'
sources = json.loads((E / 'source-manifest.json').read_text())
deps = json.loads((E / 'dependency-manifest.json').read_text())
by_id = {x['id']: x for x in deps}
counts = Counter()

def walk(x):
    counts[type(x).__name__] += 1
    if isinstance(x, dict):
        for key, value in x.items():
            assert isinstance(key, str)
            walk(value)
    elif isinstance(x, list):
        for value in x:
            walk(value)
    else:
        assert type(x) in (str, int, float, bool, type(None))

packs = {}
for row in deps:
    data = (ROOT / row['saved_path']).read_bytes()
    assert len(data) == row['size'] and hashlib.sha256(data).hexdigest() == row['sha256']
    value = json.loads(data)
    walk(value)
    packs[row['id']] = value

game_rows = []
for ident in ['1384d853217106a4f948', '480334724777cf80164f', 'bc3a57d93d51b69d628c',
              '760c140a12ae10efa5c4', 'c00b6ac7a4b315507e33', '464b5462eddc2fab21e2']:
    d = packs[ident]
    game, sec = d['game'], d['security']
    n, m = game['players'], len(game['topics'])
    assert type(n) is int and n > 0 and len(set(game['topics'])) == m
    for customer in game['customers']:
        assert type(customer['multiplicity']) is int and customer['multiplicity'] > 0
        assert customer['topics'] and len(set(customer['topics'])) == len(customer['topics'])
        assert all(type(a) is int and 0 <= a < m for a in customer['topics'])
    policy = {tuple(row['history']): row['action'] for row in d['strategy']['actions']}
    assert len(policy) == len(d['strategy']['actions'])
    assert set(policy) == {h for depth in range(n) for h in product(range(m), repeat=depth)}
    assert all(type(a) is int and 0 <= a < m for a in policy.values())
    p = list(map(Fraction, sec['primary']))
    assert len(p) == m and min(p) >= 0 and sum(p) == 1
    for dual in sec['dual']:
        assert len(dual['rivals']) == n - 1
        assert all(type(a) is int and 0 <= a < m for a in dual['rivals'])
        assert Fraction(dual['probability']) >= 0
    assert sum(Fraction(r['probability']) for r in sec['dual']) == 1
    game_rows.append({'id': ident, 'players': n, 'topics': m,
                      'unit_customers': sum(c['multiplicity'] for c in game['customers']),
                      'policy_histories': len(policy), 'all_actual_input_actions_and_dual_backgrounds_legal': True})

cone = packs['7a48fb9d35ad4f79eb56']
cone_rows = []
lambda_terms = 0
for case in cone['cases']:
    n, m = case['players'], case['topics']
    assert type(n) is int and type(m) is int and n > 0 and m > 0
    pol = {tuple(r['history']): r['action'] for r in case['policy']}
    assert len(pol) == len(case['policy'])
    assert set(pol) == {h for depth in range(n) for h in product(range(m), repeat=depth)}
    assert all(type(a) is int and 0 <= a < m for a in pol.values())
    certs = []
    for cert in case['certificates']:
        assert cert['target'] == 'aggregate' or 0 <= int(cert['target']) < n
        assert len(cert['lambda']) == m
        for terms in cert['lambda']:
            for term in terms:
                assert set(term) == {'row', 'coefficient'}
                assert len(term['row']) == (1 << m) - 1
                for coordinate in term['row']:
                    Fraction(coordinate)
                assert Fraction(term['coefficient']) >= 0
                lambda_terms += 1
        assert cert['Q'] and sum(Fraction(q) for b, q in cert['Q']) == 1
        for b, q in cert['Q']:
            assert len(b) == n - 1 and all(type(a) is int and 0 <= a < m for a in b)
            assert Fraction(q) >= 0
        certs.append({'target': cert['target'], 'Q': cert['Q'],
                      'lambda_terms_per_query': [len(x) for x in cert['lambda']]})
    cone_rows.append({'name': case['name'], 'players': n, 'topics': m,
                      'histories': len(pol), 'certificates': certs})

mirror = E / 'replay-tree'
imports = []
for row in sources:
    raw = (ROOT / row['saved_path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == row['sha256']
    imported = []
    for node in ast.walk(ast.parse(raw)):
        if isinstance(node, ast.Import):
            imported.extend(alias.name.split('.')[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert node.level == 0
            imported.append(node.module.split('.')[0])
    assert set(imported) <= sys.stdlib_module_names
    imports.append({'id': row['id'], 'stdlib_imports': sorted(set(imported)), 'project_code_dependencies': []})
    dst = mirror / row['path']
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(raw)
for row in deps:
    if row['id'] in [r['id'] for r in game_rows] + ['7a48fb9d35ad4f79eb56']:
        dst = mirror / row['path']
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes((ROOT / row['saved_path']).read_bytes())

canonical = packs['1384d853217106a4f948']
budget34 = packs['bc3a57d93d51b69d628c']
p1 = {tuple(r['history']): r['action'] for r in canonical['strategy']['actions']}
p2 = {tuple(r['history']): r['action'] for r in budget34['strategy']['actions']}
assert canonical['game'] == budget34['game'] and canonical['security'] == budget34['security']
differences = [{'history': list(h), 'canonical': p1[h], 'budget_attainer': p2[h]}
               for h in sorted(p1, key=lambda h: (len(h), h)) if p1[h] != p2[h]]

report = {'status': 'passed-input-structure-and-readiness-only', 'all_twelve_JSON_fields_traversed': True,
          'all_value_types': dict(counts), 'game_inputs': game_rows, 'selected_cone_scope': cone['scope'],
          'selected_cones': cone_rows, 'lambda_terms_checked_structurally': lambda_terms,
          'primary_stdlib_imports': imports, 'canonical_vs_budget34_policy_differences': differences,
          'numeric_input_reading_scope': 'all keys/metadata/policies/Q read; all numeric vectors retained, parsed and subsequently checked by exact primary auditor; no claim of human word-for-word reading every numeric digit',
          'additional_primary_sources_done': 0, 'mathematical_auditors_run_by_this_script': 0}
(E / 'input-structure-and-readiness.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'inputs': len(deps), 'game_inputs': len(game_rows), 'cone_cases': len(cone_rows),
                  'cone_certificates': sum(len(r['certificates']) for r in cone_rows),
                  'lambda_terms': lambda_terms, 'policy_differences_34': differences}, ensure_ascii=False))
