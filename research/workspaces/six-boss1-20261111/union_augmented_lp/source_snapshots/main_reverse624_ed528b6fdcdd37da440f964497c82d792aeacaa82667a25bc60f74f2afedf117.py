"""Main independently rebuilds the peer's one reverse-terminal row.

No peer generator is imported.  Sixteen literal B/C/J/V states are evaluated
from true-history denominators and the stated sixteen global weights.  Every
original column, including zero-mass columns, is checked.
"""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
from itertools import product
from collections import defaultdict
import json

WS = Path(__file__).resolve().parent
REPO = WS.parents[2]
PEER = REPO/'research/workspaces/six-boss2-20261111-cross'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def share(n, den):
    assert den or not n
    return F(n, den) if n else F(0)


def main():
    package_path = PEER/'joint_requery/reverse_terminal_5799_one_v1.json'
    point_path = WS/'peer_augmented_lp/augmented_lp_exact.json'
    old_path = PEER/'master_cuts/dynamic_5799_exact.json'
    package = json.loads(package_path.read_bytes())
    cut = package['cuts'][0]
    assert (cut['i'], cut['k'], cut['member'], cut['orb']) == (3, 3, 0, [0, 0])
    assert digest(old_path) == package['source_sha256'] == '63edbafd53493a20ec64ced5f09a694ead3f894bfb6419cde425de0b3a1710c1'
    assert digest(point_path) == 'd70c26065d42fd73dedc94183e4533dd6f8608d5841f7a6018ff180dc77e2f9f'
    point, old = [json.loads(p.read_bytes()) for p in (point_path, old_path)]
    columns = point['columns'][:4849]
    assert [{k: v for k, v in c.items() if k != 'weight'} for c in columns] == [
        {k: v for k, v in c.items() if k != 'weight'} for c in old['columns']]
    weights = {name: F(value) for name, value in cut['weights'].items()}
    assert set(weights) == {'sourceT', 'sourceC', 'price:b', 'price:c', 'price:j', 'price:v', 'cap:v',
                            'last2:b', 'last1:q6', 'pair2:q6,b', 'last1:q8', 'last1:q10',
                            'last2:q10', 'pair2:q14,b', 'oldpair1:6,10:product', 'priorZ:v'}
    source_weight = weights['sourceT']+weights['sourceC']
    price_weight = sum(weights['price:'+x] for x in ('b', 'c', 'j', 'v'))
    cap_weight = weights['cap:v']
    assert (source_weight, price_weight, cap_weight) == tuple(F(cut[k]) for k in ('source_weight_sum', 'u6_coefficient', 'K_coefficient'))
    groups = defaultdict(dict)
    h = None
    for index, col in enumerate(columns):
        if col['kind'] == 'hist':
            h = index
        elif col['kind'] == 'joint-reply':
            f, diagonal, wi, wj = col['group']
            groups[h].setdefault((f, diagonal, tuple(wi), tuple(wj)), {})[tuple(col['state'])] = index
    words = list(product((0, 1), repeat=3))
    vector = [F(0)]*15593
    vector[0] = cap_weight
    cells = 0
    tables = []
    for h, gs in groups.items():
        col = columns[h]
        a = tuple(map(int, col['actual_bits']))
        p, ell, p4 = sum(a[:3]), sum(a[:5]), sum(a[:4])
        counts = dict(zip(words, col['hist']))
        vector[h] += source_weight*share(a[3], sum(a))+price_weight*share(a[5], sum(a))
        orbit_weight = F(0)
        for (family, diagonal, wi, wj), indices in gs.items():
            if (family, diagonal) != (0, 0):
                continue
            frequency = F(counts[wi]*(counts[wj]-int(wi == wj)), 30)
            assert frequency > 0
            orbit_weight += frequency
            ti, ci, bj = wi[0], wi[2], wj[1]
            mean_t = F(col['d']-wi[0]-wj[0], 4)
            psi = {}
            for r, z in product((0, 1), repeat=2):
                candidates = []
                for b, c, j, v in product((0, 1), repeat=4):
                    den1, den2 = p+r+b+c, p+c+j+v
                    beta1, beta2 = p+r, p+c
                    d1, d2 = (beta1+1)*(beta1+2), (beta2+1)*(beta2+2)
                    terminal1, terminal2 = share(c, den1), share(v, den2)
                    pair2 = lambda x, y: F(x+y, beta2+1)-F(x*y+j, d2)-share(j+v, den2)
                    feature = {'sourceT': share(r, den1), 'sourceC': share(c, den2),
                               'price:b': F(b, ell+1), 'price:c': F(c, ell+1),
                               'price:j': F(j, ell+1), 'price:v': F(v, ell+1), 'cap:v': F(v),
                               'last2:b': F(b, p+c+j+1)-terminal2,
                               'last1:q6': F(ti, p+r+b+1)-terminal1,
                               'last1:q8': F(ci, p+r+b+1)-terminal1,
                               'last1:q10': F(bj, p+r+b+1)-terminal1,
                               'last2:q10': F(bj, p+c+j+1)-terminal2,
                               'pair2:q6,b': pair2(ti, b),
                               'pair2:q14,b': pair2(mean_t, b),
                               'oldpair1:6,10:product': F(ti+bj, beta1+1)-F(ti*bj+b, d1)-share(b+c, den1),
                               'priorZ:v': F(v, p4+r+1)-share(z, p4+r+z)}
                    candidates.append(sum((weights[k]*feature[k] for k in weights), F(0)))
                    cells += 1
                psi[r, z] = min(candidates)
            vector[h] -= frequency*psi[0, 0]
            for state, index in indices.items():
                vector[index] -= frequency*(psi[state]-psi[0, 0])
            tables.append({'hist_column': h, 'word_i': list(wi), 'word_j': list(wj), 'orbit_probability': str(frequency),
                           'psi_00_01_10_11': [str(psi[state]) for state in product((0, 1), repeat=2)]})
        assert orbit_weight == 1
    saved = {int(j): F(v) for j, v in cut['sparse_row']}
    assert all(value == saved.get(j, F(0)) for j, value in enumerate(vector))
    new_slack = sum((v*F(c['weight']) for v, c in zip(vector, point['columns'])), F(0))
    old_slack = sum((v*F(c['weight']) for v, c in zip(vector, old['columns'])), F(0))
    assert old_slack == F(cut['exact_slack']) < 0
    report = {'scope': 'Independent literal sixteen-state reconstruction of one reviewed reverse-Z-to-V joint row; fixed-point evaluation, not strictness of whole cones or an SPE.',
              'original_columns_checked': 4849, 'zero_auxiliary_columns_checked': 10744,
              'literal_hidden_evaluations': cells, 'all_coefficients_equal': True,
              'source_weight': str(source_weight), 'actual_last_price_weight': str(price_weight), 'capacity_weight': str(cap_weight),
              'old_exact_slack': str(old_slack), 'new_exact_slack': str(new_slack), 'new_slack_float': float(new_slack),
              'point_sha256': digest(point_path), 'package_sha256': digest(package_path), 'source_sha256': digest(Path(__file__)),
              'tables': tables}
    (WS/'main_reverse624_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'tables'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
