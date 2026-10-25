"""Independent coefficient/projection and frozen-atom hinge replay.

Standard library only. Does not import the author's coefficient, menu-count,
row, discovery, or exact-recovery code. It does not reprove all 5421 old rows.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
source = HERE.parent / 'certificate' / 'exact_projected_hinge.json'
obj = json.loads(source.read_text())

def independent_coefficient(u, p, d, j, t=F(1)):
    cap = (35 - 2 * t) / 5
    return (40 * u - cap * F(j, p + 3) - F(d, p + 1)
            + 2 * max(F(0), d - t * (p + 1)) / ((p + 1) * (p + 3)))

# Every coefficient breakpoint of the stated t interval, exactly.
breaks = sorted({F(0), F(35, 2)}
                | {F(d, p + 1) for p in range(3) for d in range(6)})
projection_checks = 0
for p, d, j, t in product(range(3), range(6), range(6), breaks):
    cap = (35 - 2 * t) / 5
    scores = [(-cap * F(j, p + 3) - F(d, p + 1)
               + h * 2 * (d - t * (p + 1)) / ((p + 1) * (p + 3)))
              for h in (0, 1)]
    assert max(scores) == independent_coefficient(F(0), p, d, j, t)
    projection_checks += 1

hist_types3 = list(product((0, 1), repeat=3))
hist_types4 = list(product((0, 1), repeat=4))
mass_sum = F(0)
W = F(0)
O = F(0)
slack = F(0)
atom_records = []
for atom in obj['atoms']:
    mass = F(atom['exact_mass'])
    assert mass > 0
    bits = tuple(map(int, atom['bits']))
    mb = tuple(map(int, atom['max_bits']))
    assert len(bits) == 10 and len(mb) == 5
    assert len(atom['AB_hist']) == 8 and sum(atom['AB_hist']) == 5
    assert len(atom['second_hist']) == 16 and sum(atom['second_hist']) == 5
    # The first coordinate of each family is the same optimal membership.
    d = sum(n * z[0] for n, z in zip(atom['AB_hist'], hist_types3))
    assert d == sum(n * z[0] for n, z in zip(atom['second_hist'], hist_types4))
    # Sbranch menus are U,V,W: mW is coordinate 3 in (T,U,V,W).
    j = sum(n * z[3] for n, z in zip(atom['second_hist'], hist_types4))
    p = sum(mb[:2])
    u = F(mb[2], sum(mb)) if mb[2] else F(0)
    coeff = independent_coefficient(u, p, d, j)
    assert coeff == F(atom['hinge_coefficient'])
    mass_sum += mass
    W += mass * int(any(bits[:5]))
    O += mass * int(d > 0)
    slack += mass * coeff
    atom_records.append({'p': p, 'd': d, 'j': j, 'u': str(u),
                         'coefficient': str(coeff)})
assert W == 1 and O == F(obj['comparison_cover'])
assert slack < 0 and slack == F(obj['exact_hinge_slack'])
assert 5 * slack == F(obj['exact_hinge_slack_scaled_by_5'])
old_slacks = list(map(F, obj['source_row_slacks'].values()))
assert len(old_slacks) == obj['source_rows'] == 5421
assert min(old_slacks) == F(obj['minimum_source_exact_slack']) == 0
report = {
    'independence': 'Standard library only; no author module imported.',
    'proof_scope': 'Coefficient/projection and frozen 57-atom hinge only; old row values are schema-checked, not independently rederived.',
    'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'stated_t_breakpoints': list(map(str, breaks)),
    'projection_state_checks': projection_checks,
    'positive_atoms': len(atom_records),
    'mass_sum': str(mass_sum),
    'actual_cover_W': str(W),
    'comparison_cover': str(O),
    'exact_hinge_slack': str(slack),
    'exact_hinge_slack_times_5': str(5 * slack),
    'stored_old_rows_schema_checked': len(old_slacks),
    'stored_old_minimum': str(min(old_slacks)),
    'atom_projection_records': atom_records,
}
(HERE / 'hinge_independent_audit.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: v for k, v in report.items() if k != 'atom_projection_records'}, indent=2))
