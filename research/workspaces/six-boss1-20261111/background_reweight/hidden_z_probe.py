"""Seven Z-safe rows at genuine hidden successors, on the exact 65 atoms.

AB/AE: seats 4,5 only. Sbranch: seats 3,4,5 only. The forced T_i seat is
never treated as an optimizer. Each own payoff is its own hidden path share.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
from cone import HERE, LABELS, build

ROWS = [('AB', 4), ('AB', 5), ('AE', 4), ('AE', 5),
        ('Sbranch', 3), ('Sbranch', 4), ('Sbranch', 5)]


def q(n, d):
    return F(n, d) if n else F(0)


def hidden_z_value(w, tag, seat):
    b = w['background']
    bits = dict(zip(LABELS, map(int, w['bits'])))
    k = 4 if tag == 'Sbranch' else 3
    pos = seat-(6-k)
    assert 1 <= pos < k
    p = b+bits['A']+(bits['B'] if tag == 'AB' else bits['E'] if tag == 'AE' else 0)
    branch = [t for t, count in zip(product((0, 1), repeat=k), w['histograms'][tag]) for _ in range(count)]
    return sum(q(t[pos], p+sum(t))-q(b, p+sum(t[:pos])+k-pos) for t in branch)


def main():
    source = HERE/'free58_lower_certificate.json'
    cert = json.loads(source.read_text())
    domains = {b: build(b, 'profit')[:2] for b in (0, 1)}
    histids = {(b, k): {tuple(h): i for i, h in enumerate(dom.hist[k])}
               for b, (ns, dom) in domains.items() for k in (3, 4)}
    totals = {f'{tag}:{seat}:K:Z': F(0) for tag, seat in ROWS}
    by_atom = []
    for atom in cert['atoms']:
        w = atom['witness']
        mass = F(atom['mass'])
        b = w['background']
        ns, dom = domains[b]
        bits = dict(zip(LABELS, map(int, w['bits']))) | {'Z': b}
        row = {}
        for tag, seat in ROWS:
            name = f'{tag}:{seat}:K:Z'
            val = hidden_z_value(w, tag, seat)
            (k, p, terms), const, kap = dom.family_parts(tag, bits, {name: 1})
            ix = histids[b, k][tuple(w['histograms'][tag])]
            feature = F(const+sum(v*int(dom.features[k, p][f][ix]) for f, v in terms), 120)
            assert kap == 0 and feature == val, (name, feature, val)
            totals[name] += mass*val
            row[name] = str(val)
        by_atom.append({'mass': str(mass), 'witness': w, 'rows': row})
    out = {'status': 'EXACT-SEVEN-HIDDEN-Z-QUERY-AUDIT', 'source_certificate_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
           'roles': [{'family': tag, 'actual_global_tail_seat': seat, 'forced_comparison_seat_excluded': 2 if tag == 'Sbranch' else 3} for tag, seat in ROWS],
           'direct_and_feature_evaluations': len(cert['atoms'])*7,
           'row_values': {n: str(v) for n, v in totals.items()},
           'row_values_float': {n: float(v) for n, v in totals.items()},
           'negative_rows': [n for n, v in totals.items() if v < 0],
           'zero_K_budget': True, 'not_actual_payoff_substitution': True,
           'atom_values': by_atom, 'not_an_SPE_counterexample': True}
    (HERE/'hidden_z_probe.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'atom_values'}, indent=2))


if __name__ == '__main__':
    main()
