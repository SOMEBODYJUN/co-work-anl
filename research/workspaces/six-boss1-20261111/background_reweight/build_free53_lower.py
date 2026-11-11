"""Exact positive fee obstruction for the ENTIRE free 53-ray cone.

Reuse one archived 76-atom point, audit its 35 zero-K rows anew, and add one
background-exclusive zero-membership atom plus one shared capacity column.
No optimization, grid, or SPE-realizability assertion occurs here.
"""
from fractions import Fraction as F
import hashlib
import json
from cone import HERE, ROOT, NAMES, SCALES, literal_vector, target, exclusive


SOURCE = ROOT/'archives/customer-attraction/tools/evidence/dual-terminal-exact-resumed-boss2/original/exact_optimum_primal_dual_terminal.json'


def main():
    src = json.loads(SOURCE.read_text())
    atoms = []
    values = [F(0)]*58
    V = F(0)
    R = F(0)
    k = None
    for old in src['atoms']:
        d = sum(old['AB_hist'][4:])
        w = {'background': 0, 'bits': old['bits'], 'd': d, 'menus': old['menus_lh'],
             'histograms': {'AB': old['AB_hist'], 'AE': old['AE_hist'], 'Sbranch': old['second_hist']}}
        mass = F(old['exact_mass'])
        assert mass > 0
        a, kk = literal_vector(w)
        k = kk if k is None else k
        assert kk == k
        values = [v+mass*a_j for v, a_j in zip(values, a)]
        V += mass*int(any(map(int, w['bits'][:5])))
        R += mass*int(d > 0)
        atoms.append({'mass': str(mass), 'witness': w})
    assert len(atoms) == 76 and V == 1 and R == F(src['comparison_cover']) and R > 2
    assert sum(k[j] == 0 for j in range(53)) == 35
    assert all(values[j] >= 0 for j in range(53) if k[j] == 0)
    mr = NAMES.index('MAXROOT-NEW')
    assert [j for j in range(53) if k[j] < 0] == [mr]
    assert sum(k[j] > 0 for j in range(53)) == 17
    capacity = max([F(0)] + [-values[j]/k[j] for j in range(53) if k[j] > 0])
    z = {'background': 1, 'bits': '0000000000', 'd': 0, 'menus': [[0, 0]]*3,
         'histograms': {'AB': [5]+[0]*7, 'AE': [5]+[0]*7, 'Sbranch': [5]+[0]*15}}
    za, zk = literal_vector(z)
    assert zk == k and exclusive(z) == 1 and target(z) == 0
    assert za[mr] == F(1983898, 10**6)
    assert all(za[j] == 0 for j in range(53) if j != mr)
    background_mass = (-values[mr]-capacity*k[mr])/za[mr]
    assert background_mass > 0
    # Normalize total exclusive mass to exactly one.
    cert_atoms = [{'mass': str(F(a['mass'])/background_mass), 'witness': a['witness']} for a in atoms]
    cert_atoms.append({'mass': '1', 'witness': z})
    cap = capacity/background_mass
    row_slacks = [(v+capacity*kk)/background_mass+zv for v, kk, zv in zip(values, k, za)]
    assert all(v >= 0 for v in row_slacks[:53])
    lower = (R-2*V)/background_mass
    cert = {'schema': 1, 'cone': 'shifted-53-fixed-source-contracts',
            'scope': 'All 53 global nonnegative outside multipliers, unchanged shifted local contracts, pointwise nonnegative customer and K remainders. No Z query or extra MAX:Z ray.',
            'lower_bound': str(lower), 'capacity_mass': str(cap), 'atoms': cert_atoms,
            'source_point': str(SOURCE.relative_to(ROOT)),
            'source_point_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            'not_an_SPE_counterexample': True, 'not_claimed_optimal': True}
    (HERE/'free53_lower_certificate.json').write_text(json.dumps(cert, indent=2)+'\n')
    audit = {'status': 'EXACT-FREE-53-LOWER-BOUND-CONSTRUCTED', 'old_atoms': len(atoms),
             'new_dual_atoms': len(cert_atoms), 'old_V': str(V), 'old_R': str(R), 'old_gap': str(R-2*V),
             'old_35_zero_K_slacks': {NAMES[j]: str(values[j]) for j in range(53) if k[j] == 0},
             'unscaled_capacity': str(capacity), 'capacity_binding_rows': [NAMES[j] for j in range(53) if k[j] > 0 and -values[j]/k[j] == capacity],
             'unscaled_exclusive_mass': str(background_mass), 'capacity_mass': str(cap), 'exclusive_mass': '1',
             'epsilon_lower_bound': str(lower), 'epsilon_lower_float': float(lower),
             'all_53_slacks': {n: str(v) for n, v in zip(NAMES[:53], row_slacks[:53])},
             'excluded_new_query_slacks': {n: str(v) for n, v in zip(NAMES[53:], row_slacks[53:])},
             'MAX_Z_slack_if_added': str(cap-1),
             'source_point_sha256': cert['source_point_sha256'], 'not_an_SPE_counterexample': True}
    assert all(v < 0 for v in row_slacks[53:]), 'This particular construction is only a 53-ray obstruction.'
    (HERE/'free53_lower_construction.json').write_text(json.dumps(audit, indent=2)+'\n')
    print(json.dumps({k: v for k, v in audit.items() if k not in ('old_35_zero_K_slacks', 'all_53_slacks')}, indent=2))


if __name__ == '__main__':
    main()
