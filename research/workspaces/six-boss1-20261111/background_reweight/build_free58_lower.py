"""Exact 65-atom positive-fee obstruction for all 58 free outside rays.

Reuse the mature archived 64-atom projection, add one exclusive zero type,
and pay all positive K columns with one common scalar. No numerical search.
"""
from fractions import Fraction as F
import hashlib
import json
from cone import HERE, ROOT, NAMES, literal_vector, target, exclusive

SOURCE = ROOT/'archives/customer-attraction/tools/evidence/five-full-actual-extension-primary/original/certificate/exact_full_actual_extension_known_v1.json'


def main():
    source = json.loads(SOURCE.read_text())
    atoms = []
    value = [F(0)]*58
    V = R = F(0)
    k = None
    for old in source['atoms']:
        d = sum(old['AB_hist'][4:])
        w = {'background': 0, 'bits': old['bits'], 'd': d, 'menus': old['menus_lh'],
             'histograms': {'AB': old['AB_hist'], 'AE': old['AE_hist'], 'Sbranch': old['second_hist']}}
        mass = F(old['exact_mass'])
        assert mass > 0
        a, kk = literal_vector(w)
        k = kk if k is None else k
        assert k == kk
        value = [v+mass*x for v, x in zip(value, a)]
        V += mass*int(any(map(int, w['bits'][:5])))
        R += mass*int(d > 0)
        atoms.append({'mass': str(mass), 'witness': w})
    assert len(atoms) == 64 and V == 1 and R == F(source['comparison_cover'])
    assert R-2*V == F(source['gap_above_two']) > 0
    assert all(value[j] >= 0 for j in range(53) if k[j] == 0)
    mr = NAMES.index('MAXROOT-NEW')
    assert [j for j in range(58) if k[j] < 0] == [mr]
    capacity = max([F(0)]+[-value[j]/k[j] for j in range(58) if k[j] > 0])
    z = {'background': 1, 'bits': '0000000000', 'd': 0, 'menus': [[0, 0]]*3,
         'histograms': {'AB': [5]+[0]*7, 'AE': [5]+[0]*7, 'Sbranch': [5]+[0]*15}}
    za, zk = literal_vector(z)
    assert zk == k and exclusive(z) == 1 and target(z) == 0
    assert za[mr] == F(1983898, 10**6)
    background_mass = (-value[mr]-capacity*k[mr])/za[mr]
    assert background_mass > 0
    slacks = [(v+capacity*kk)/background_mass+zv for v, kk, zv in zip(value, k, za)]
    assert all(v >= 0 for v in slacks)
    assert all(v > 0 for v in slacks[53:])
    lower = (R-2*V)/background_mass
    cert_atoms = [{'mass': str(F(a['mass'])/background_mass), 'witness': a['witness']} for a in atoms]
    cert_atoms.append({'mass': '1', 'witness': z})
    cert = {'schema': 1, 'cone': 'shifted-53-plus-five-actual-Z-safe-queries',
            'scope': 'All 58 global nonnegative outside multipliers with unchanged shifted local contracts and nonnegative customer and K remainders.',
            'lower_bound': str(lower), 'capacity_mass': str(capacity/background_mass), 'atoms': cert_atoms,
            'source_point': str(SOURCE.relative_to(ROOT)), 'source_point_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            'not_an_SPE_counterexample': True, 'not_claimed_optimal': True}
    (HERE/'free58_lower_certificate.json').write_text(json.dumps(cert, indent=2)+'\n')
    audit = {'status': 'EXACT-FREE-58-LOWER-BOUND-CONSTRUCTED', 'old_atoms': len(atoms),
             'new_dual_atoms': len(cert_atoms), 'old_V': str(V), 'old_R': str(R), 'old_gap': str(R-2*V),
             'old_35_zero_K_slacks': {NAMES[j]: str(value[j]) for j in range(53) if k[j] == 0},
             'unscaled_capacity': str(capacity), 'capacity_binding_rows': [NAMES[j] for j in range(58) if k[j] > 0 and -value[j]/k[j] == capacity],
             'unscaled_exclusive_mass': str(background_mass), 'exclusive_mass': '1',
             'capacity_mass': cert['capacity_mass'], 'epsilon_lower_bound': str(lower), 'epsilon_lower_float': float(lower),
             'all_58_slacks': {n: str(v) for n, v in zip(NAMES, slacks)},
             'five_query_slacks': {n: str(v) for n, v in zip(NAMES[53:], slacks[53:])},
             'MAX_Z_slack_if_added': str(capacity/background_mass-1),
             'source_point_sha256': cert['source_point_sha256'], 'not_an_SPE_counterexample': True}
    (HERE/'free58_lower_construction.json').write_text(json.dumps(audit, indent=2)+'\n')
    print(json.dumps({k: v for k, v in audit.items() if k not in ('old_35_zero_K_slacks', 'all_58_slacks')}, indent=2))


if __name__ == '__main__':
    main()
