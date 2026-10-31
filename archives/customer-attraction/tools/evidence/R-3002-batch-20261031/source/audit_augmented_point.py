"""Replay old 3889 rows, then independently append five scalar root rows."""
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / 'R-c4f1ef099fad483c9f81283b61eb0b53/six_astra'
sys.path.insert(0, str(OLD))
import attractive_nested as old

path = HERE / 'research_5/root_rows_joint_point.json'
raw = path.read_bytes()
report = json.loads(raw)
point = report['certificate']
previous = old.verify(point)
assert previous['verified_rows'] == 3889
u1, capital, optimum = F(0), None, F(0)
for col in point['columns']:
    weight = F(col['weight'])
    if col['kind'] == 'K':
        capital = weight
    elif col['kind'] == 'hist':
        bits = list(map(int, col['actual_bits']))
        if bits[0]:
            u1 += weight / sum(bits)
        if col['d']:
            optimum += weight
assert optimum == 1
slacks = []
for cut in report['cuts']:
    certpath = HERE / 'research_4' / Path(cut['file']).name
    cert_raw = certpath.read_bytes()
    assert hashlib.sha256(cert_raw).hexdigest() == cut['sha256']
    cert = json.loads(cert_raw)
    nu, denominator = cert['multipliers_numerators'], cert['denominator']
    a = F(sum(v for k, v in nu.items() if k.startswith(('LASTO:', 'PAIRO:'))), denominator)
    b = F(cert['equality_numerator'] - sum(v for k, v in nu.items() if k.startswith('CAP:')), denominator)
    slack = u1 - a * optimum - b * capital
    assert slack >= 0
    slacks.append(str(slack))
assert slacks == report['exact_verification']['new_root_slacks']
result = dict(input_sha256=hashlib.sha256(raw).hexdigest(),
              old_generator_replay=previous, root_rows=len(slacks),
              exact_root_slacks=slacks, O=str(optimum), W=point['W'],
              status='exact feasible point for listed 3894 necessary relations; not SPE or target counterexample',
              scope='old canonical generator replay plus separate scalar-root reconstruction; not independent raw reconstruction of all 3889 rows')
(HERE / 'augmented_point_audit.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
