"""Full field/byte readiness for exact reuse and two isolated original CLIs.

No primary math code, Git, source generator, network or identity is run here.
"""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import ast
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
E = ROOT / 'tools/evidence/search-and-facility-site-primary'
sources = json.loads((E / 'source-manifest.json').read_text())
deps = json.loads((E / 'dependency-manifest.json').read_text())
byid = {x['id']: x for x in sources + deps}
mirror = E / 'replay-tree'
types = Counter()

def walk(value):
    types[type(value).__name__] += 1
    if isinstance(value, dict):
        for k, v in value.items():
            assert isinstance(k, str)
            walk(v)
    elif isinstance(value, list):
        for v in value:
            walk(v)
    else:
        assert type(value) in (str, int, float, bool, type(None))

packs = {}
for row in sources + deps:
    data = (ROOT / row['saved_path']).read_bytes()
    assert len(data) == row['size'] and hashlib.sha256(data).hexdigest() == row['sha256']
    dest = mirror / row['path']
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    if row['path'].endswith('.json'):
        packs[row['id']] = json.loads(data)
        walk(packs[row['id']])

search = packs['912c92b9572c9c92ca11']
assert search['status'] == 'completed' and search['audit_script_sha256'] == byid['4a0a68157e801a180ce5']['sha256']
assert search['parameters']['confirm'] and search['parameters']['extended']
assert search['total_instance_count'] == 27136 and len(search['stages']) == 13
assert sum(s['instance_count'] for s in search['stages']) == 27136
assert all(s['welfare_half_violations'] == 0 and s['residual_lemma_violating_instances'] == 0 for s in search['stages'])
assert search['residual_lemma_counterexamples'] == []
assert Fraction(search['minimum_ratio']) == Fraction(5, 9)

four = packs['79d0b8c76eebaca202fa']
assert four['source_sha256']['tests/audits/four_site_fptas.py'] == byid['a4954c4665e08897643a']['sha256']
assert four['source_sha256']['facility_spe/shared/four_site_fptas_hardness.py'] == byid['9f32aa2a4194de92d3b6']['sha256']
assert len(four['results']) == four['source_instances'] == 32
assert four['yes'] == 8 and four['no'] == 24
assert sum(x['enumerated'] for x in four['results']) == four['enumerated'] == 886344
ind = packs['c26e8f18cc84a854a492']
assert ind['source_sha256']['tests/audits/four_site_fptas_independent.py'] == byid['f859371ea34882324c83']['sha256']
assert len(ind['cases']) == ind['counts']['sources'] == 19
assert ind['counts']['yes'] == 8 and ind['counts']['no'] == 11
assert all(Fraction(x['core_guard_lower_bound']) < Fraction(131, 100) for x in ind['cases'])

imports = []
for ident in ['aba4ae48ffacdaea5c90', '64fbe1e82a8a643c43b7', '68753e23b4abb3316644', 'b1d86a5bf34773a9de22']:
    text = (ROOT / byid[ident]['saved_path']).read_text()
    modules = []
    for node in ast.walk(ast.parse(text)):
        if isinstance(node, ast.Import):
            modules.extend(a.name.split('.')[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert not node.level
            modules.append(node.module.split('.')[0])
    assert set(modules) - {'facility_spe'} <= sys.stdlib_module_names
    imports.append({'id': ident, 'imports': sorted(set(modules))})

result = {'status': 'passed-real-byte-field-and-import-readiness', 'all_five_old_JSON_fields_traversed': True,
    'field_types': dict(types),
    'old_success_reused': [
        {'source_id': '4a0a68157e801a180ce5', 'same_code_SHA': True, 'instances': 27136,
         'parameters': search['parameters'], 'canonical_confirm_scope': '13 stage-worst roots matched; old report does not list canonical source hashes; no new-stack certification'},
        {'source_id': 'a4954c4665e08897643a', 'same_code_and_nontrivial_constructor_SHA': True, 'instances': 32,
         'coverage': 'all closed supports / ten unordered layouts and tag reflection'},
        {'source_id': 'f859371ea34882324c83', 'same_code_SHA': True, 'project_dependencies': [], 'instances': 19,
         'coverage': 'full core and five unique alternatives; analytic diagonal guards, not diagonal support enumeration'}],
    'new_run_plan': [
        {'source_id': 'aba4ae48ffacdaea5c90', 'original_CLI_invocations': 1, 'quick': False,
         'real_inputs': 'all original 1103 constant-domain probes/96 macro comparisons/14 specified source-target-factor cases'},
        {'source_id': '64fbe1e82a8a643c43b7', 'original_CLI_invocations': 1,
         'real_inputs': 'all nine specified source-target-factor cases and six bad sources',
         'runpy_identity': 'run_path default name <run_path> loads main-auditor definitions; does not execute its __main__; then edge main calls audit_case nine times'}],
    'new_run_code_imports': imports,
    'no_fake_stubs_or_Git_fixture': True, 'facility_shared_namespace': 'no shared/__init__.py inventory source exists; real root90B docstring retained, namespace child is valid',
    'additional_related_sources_done': 0}
(E / 'input-structure-and-run-readiness.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'old_same_SHA_successes_reused': 3, 'new_original_CLIs_planned': 2,
                  'new_Git_operations': 0, 'JSON_values_traversed': sum(types.values())}))
