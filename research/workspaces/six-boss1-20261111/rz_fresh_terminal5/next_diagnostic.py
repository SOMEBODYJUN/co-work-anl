"""Evaluate possible new queries on this one completion; no optimization."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
table = json.loads((HERE / 'local_tables_exact.json').read_text())['states']
completion = json.loads((HERE / 'completion_exact.json').read_text())['rows']
hidden = tuple(product((0, 1), repeat=4))
costs = {k: F(0) for k in ('cA_to_vB', 'vA_to_vB', 'cB_to_vA', 'vB_to_vA')}
for state, row in zip(table, completion):
    assert state['id'] == row['state_id']
    p = state['p']
    r, z = state['old_state']
    for atom in row['atoms']:
        mass = F(atom['averaged_mass'])
        bA, cA, jA, vA = hidden[atom['hA_index']]
        bB, cB, jB, vB = hidden[atom['hB_index']]
        costs['cA_to_vB'] += mass * F(vB - cA, p + r + bA + 1)
        costs['vA_to_vB'] += mass * F(vB - vA, p + cA + jA + 1)
        costs['cB_to_vA'] += mass * F(vA - cB, p + z + bB + 1)
        costs['vB_to_vA'] += mass * F(vA - vB, p + cB + jB + 1)
report = dict(scope='Read-only evaluation of four possible follow-up true-terminal queries on the one completed measure; no new optimization or separation claim.',
              costs={k: str(v) for k, v in costs.items()},
              costs_float={k: float(v) for k, v in costs.items()})
(HERE / 'next_interface_diagnostic.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report['costs_float'], ensure_ascii=False, indent=2))
