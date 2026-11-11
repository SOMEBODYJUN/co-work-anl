"""Literal 28-row old-B/new-early-tail interface, exact standard library.

Indices are common OPT labels. The old word (t,b,c) and new five-bit tail
share t at each index. Rows are full same/off S6 orbit averages, with fixed
normalizers 6 and 30. Safe queries retain the real source payoff, while the
deviation denominator bounds the true, unfrozen continuation.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
PIN = 'd70c26065d42fd73dedc94183e4533dd6f8608d5841f7a6018ff180dc77e2f9f'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def q(n, d):
    return F(n, d) if n else F(0)


def bits(w, n):
    return tuple(map(int, f'{w:0{n}b}'))


def names():
    return ([('B-to-Y', l, rel) for l in range(5) for rel in ('same', 'off')]
          + [('Y-to-old', k, v, rel) for k in range(4) for v in ('B', 'C')
             for rel in ('same', 'off')]
          + [('Y5-to-B', rel) for rel in ('same', 'off')])


def coefficients(actual, old, new):
    assert len(old) == len(new) == 6
    p = sum(map(int, actual[:3]))
    ow = [bits(w, 3) for w in old]
    nw = [bits(w, 5) for w in new]
    out = {name: F(0) for name in names()}
    for i, (t, b, c) in enumerate(ow):
        oldpay = q(b, p+t+b+c)
        for j, e in enumerate(nw):
            s = ow[j][0]
            rel = 'same' if i == j else 'off'
            scale = 6 if i == j else 30
            for l in range(5):
                out['B-to-Y', l, rel] += (oldpay-F(e[l], p+t+2))/scale
            for k in range(4):
                den = s+sum(e[:k])+5-k
                ownpay = q(e[k], s+sum(e))
                out['Y-to-old', k, 'B', rel] += (ownpay-F(b, den))/scale
                out['Y-to-old', k, 'C', rel] += (ownpay-F(c, den))/scale
            out['Y5-to-B', rel] += (q(e[4], s+sum(e))
                                   - F(b, s+sum(e[:4])+1))/scale
    return out


def main():
    source = BASE/'root_old_tail_joint/joint_completion_exact.json'
    cert = json.loads(source.read_text())
    assert sha(BASE/'peer_augmented_lp/augmented_lp_exact.json') == cert['point_sha256'] == PIN
    totals = {name: F(0) for name in names()}
    for atom in cert['atoms']:
        vals = coefficients(atom['actual'], atom['old_words'], atom['new_words'])
        for name, value in vals.items():
            totals[name] += F(atom['mass'])*value
    report = {
        'status': 'EXACT PREVIOUS-WITNESS EVALUATION',
        'scope': 'Only the 28 specified orbit rows on the previous 17-atom measure; not SPE.',
        'point_sha256': PIN,
        'previous_certificate_sha256': sha(source),
        'script_sha256': sha(__file__),
        'actual_argv': [sys.executable, *sys.argv],
        'rows': [{'row': list(n), 'slack': str(v), 'float': float(v)} for n, v in totals.items()],
        'negative_rows': [list(n) for n, v in totals.items() if v < 0],
        'zero_rows': [list(n) for n, v in totals.items() if v == 0],
        'minimum_slack': str(min(totals.values())),
    }
    (HERE/'previous_witness_28_exact.json').write_text(json.dumps(report, indent=2)+'\n')
    for n, v in totals.items():
        print(n, str(v), float(v))
    print('NEGATIVE', len(report['negative_rows']), 'ZERO', len(report['zero_rows']))


if __name__ == '__main__':
    main()
