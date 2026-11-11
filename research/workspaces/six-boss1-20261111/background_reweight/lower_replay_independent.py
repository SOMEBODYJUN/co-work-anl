"""Standard-library replay of a finite dual; no cone/oracle/LP imports.

The row implementation is the bridge's independent literal-index evaluator,
not the transformed frozen verifier used by full-domain separation. This new
file is not a dependency of the already frozen Actions request.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BRIDGE = HERE.parent/'background_five_bridge'
sys.path.insert(0, str(BRIDGE))
from verify_literal_and_bridge import literal_row


def q(n, d):
    return F(n, d) if n else F(0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('certificate', type=Path)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    inputs = json.loads((HERE/'inputs.json').read_text())
    for name, expected in inputs['source_sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected, name
    c = json.loads(args.certificate.read_text())
    names = inputs['row_names']
    assert len(names) == 58 and names[-5:] == [f'actual:{i}:query-Z' for i in range(1, 6)]
    if c['cone'] == 'shifted-53-fixed-source-contracts':
        names = names[:53]
    else:
        assert c['cone'] == 'shifted-53-plus-five-actual-Z-safe-queries'
    cap = F(c['capacity_mass'])
    assert cap >= 0
    totals = {n: F(0) for n in names}
    kappas = None
    E = F(0)
    rhs = F(0)
    mass_total = F(0)
    positive = 0
    for atom in c['atoms']:
        mass = F(atom['mass'])
        assert mass >= 0
        positive += int(mass > 0)
        mass_total += mass
        w = atom['witness']
        b, d = w['background'], w['d']
        assert b in (0, 1) and isinstance(d, int) and 0 <= d <= 5
        assert len(w['bits']) == 10 and set(w['bits']) <= {'0', '1'}
        bits = dict(zip('ABCDEUVWXY', map(int, w['bits'])))
        branches = {}
        assert set(w['histograms']) == {'AB', 'AE', 'Sbranch'}
        for tag, h in w['histograms'].items():
            k = 4 if tag == 'Sbranch' else 3
            assert len(h) == 2**k and sum(h) == 5
            assert all(isinstance(v, int) and v >= 0 for v in h)
            branch = [ty for ty, count in zip(product((0, 1), repeat=k), h) for _ in range(count)]
            assert len(branch) == 5 and sum(t[0] for t in branch) == d
            branches[tag] = branch
        assert len(w['menus']) == 3
        for ell, h in w['menus']:
            assert isinstance(ell, int) and isinstance(h, int)
            assert 0 <= h <= d and 0 <= ell-h <= 5-d
        a = [bits[s] for s in 'ABCDE']
        V, R = q(sum(a), b+sum(a)), q(d, b+d)
        E += mass*int(b == 1 and sum(a) == 0)
        rhs += mass*(R-2*V)
        local_k = {}
        for name in names[:53]:
            val, kap = literal_row(name, bits, d, w['menus'], branches, b, 'profit')
            totals[name] += mass*val
            local_k[name] = F(kap)
        for i, name in enumerate(names[53:]):
            val = q(a[i], b+sum(a))-q(b, b+sum(a[:i])+5-i)
            totals[name] += mass*val
            local_k[name] = F(0)
        if kappas is None:
            kappas = local_k
        assert local_k == kappas
    assert positive > 0
    assert E <= 1
    for name in names:
        totals[name] += cap*kappas[name]
    assert all(v >= 0 for v in totals.values()), {n: str(v) for n, v in totals.items() if v < 0}
    assert rhs == F(c['lower_bound'])
    report = {'status': 'EXACT-LITERAL-DUAL-REPLAY-PASSED',
              'certificate_sha256': hashlib.sha256(args.certificate.read_bytes()).hexdigest(),
              'lower_bound': str(rhs), 'positive_lower_bound': rhs > 0,
              'positive_atoms': positive, 'total_atom_mass': str(mass_total),
              'exclusive_mass': str(E), 'capacity_mass': str(cap),
              'cone_row_count': len(names), 'raw_row_slacks': {n: str(v) for n, v in totals.items()},
              'source_sha256': inputs['source_sha256'], 'not_an_SPE_counterexample': True,
              'scope': f'Whole identified {len(names)}-ray coefficient-domain cone lower bound from a finite exact dual.'}
    output = args.output or args.certificate.with_name('independent_lower_replay.json')
    output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('raw_row_slacks', 'source_sha256')}, indent=2))


if __name__ == '__main__':
    main()
