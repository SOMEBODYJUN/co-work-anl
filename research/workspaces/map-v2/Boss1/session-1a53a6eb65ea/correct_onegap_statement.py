"""Correct one ambiguous registry-only slash using the unchanged source proof."""
from pathlib import Path
from fractions import Fraction as F
import copy
import hashlib
import json
import subprocess
import sys

R = Path.cwd()
O = R / 'research/workspaces/map-v2/Boss1/session-1a53a6eb65ea'
sys.path.insert(0, str(R / 'tools'))
import research_runtime as rr


def save(p, o):
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + '\n')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


oid = 'M-08ce8b5c16d149c9ab4816c34e89ffe0'
tid = 'customer-attraction-3a-3a-d9b971ecd9ba54c7'
reg = json.loads((R / 'research/registry.json').read_text())
obj = next(o for o in reg['objects'] if o['object_id'] == oid)
assert obj['version'] == 1
assert obj['statement'].count('u4/u5≥v5') == 1
task_refs = []
for p in (R / 'research/operations/map-v2/tasks').glob('*.json'):
    t = json.loads(p.read_text())
    if oid in t['definition'].get('input_pins', {}):
        task_refs.append(t)
assert len(task_refs) == 1 and task_refs[0]['definition']['task_id'] == tid
assert task_refs[0]['state'] == 'available' and task_refs[0].get('owner') is None
assert not any(oid in (R / p).read_text() for p in reg['edge_files'])

source_refs = [
    {'path': 'archives/customer-attraction/state/引理/固定两尾势缺口的三项真实比较--引理.md',
     'sha256': '953b090fd6d8771755c09fe53c36e358b9a5518841511ffab7e6eda23052bd7b'},
    obj['body'],
]
for ref in source_refs:
    assert sha(R / ref['path']) == ref['sha256']

before = copy.deepcopy(obj)
obj['statement'] = obj['statement'].replace('u4/u5≥v5', 'u4、u5各自≥v5')
obj['version'] = 2
obj['objections'] += ' 摘要原斜杠现正名为u4、u5分别达到v5；这不是两收益的比值保证。正文、模型、量词和原证据不变。合法保险族a=1,b=2给u4=9/4、u5=2、v5=8/5，二者各自保底但u4/u5=9/8<8/5。'
for key in ('model', 'quantifiers', 'assumptions', 'scope', 'truth_status', 'body', 'evidence', 'sources'):
    assert obj[key] == before[key]

u4, u5, v5 = F(9, 4), F(2), F(8, 5)
assert u4 >= v5 and u5 >= v5 and u4 / u5 < v5
proposal = O / 'onegap-statement-proposed.json'
save(proposal, reg)
proc = subprocess.run([sys.executable, 'work.py', 'research', 'register', '--record-file', str(proposal.relative_to(R))],
                      capture_output=True, text=True)
print(proc.stdout, end='')
print(proc.stderr, end='')
if proc.returncode:
    raise SystemExit(proc.returncode)
proposal.unlink()
audit = {
    'status_at_creation': 'registered-local-before-checkpoint',
    'reviewer': 'Boss1 and PREFIX7-REFRESH temporary ONEGAP 3D comparison',
    'object_id': oid, 'before': before, 'after': obj,
    'before_pin': rr.pin(before), 'after_pin': rr.pin(obj),
    'source_refs': source_refs,
    'unchanged_sources': True,
    'exact_witness': {'a': 1, 'b': 2, 'required_domain': 'positive integer a,b and b>=3a/2; full 20-label Cartesian directory, all-history BASE/PUNISH/EXIT',
                      'u4': str(u4), 'u5': str(u5), 'v5': str(v5), 'u4_over_u5': str(u4/u5),
                      'ratio_minus_v5': str(u4/u5-v5)},
    'scope': 'Registry summary punctuation/meaning correction only: separate lower bounds, never a ratio. ONEGAP stays open; no new object and no scientific program rerun.',
    'canonical_incident_edges': [],
    'unfinished_task_to_refresh': tid,
    'required_followup': 'Native repair-draft refresh of this sole available task before claim; no claimed task or old done receipt is affected.'
}
save(O / 'onegap-statement-correction.json', audit)
print(json.dumps({'object_id': oid, 'version': obj['version'], 'pin': rr.pin(obj), 'only_affected_task': tid}, ensure_ascii=False))
