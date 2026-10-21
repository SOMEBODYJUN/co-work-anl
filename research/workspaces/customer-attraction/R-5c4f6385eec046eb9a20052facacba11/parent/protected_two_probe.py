"""Fixed two-player strategy cones; exploratory LP, never a proof oracle.

Background loads b are realized by bmax nested prefix topics only if those
topics are in the common catalog: here these are arbitrary external legal
backgrounds for a tail game, without claiming a full root SPE embedding.
"""
import argparse
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


def scan(p=4, bmax=3):
    atoms = [(mask, b) for mask in range(1, 1 << p) for b in range(bmax+1)]
    def row(a, q):
        return np.array([float(F(bool(mask & (1 << a)), b + sum(bool(mask & (1 << j)) for j in q)))
                         if mask & (1 << a) else 0 for mask, b in atoms])
    W = row(0, (0, 1)) + row(1, (0, 1))
    D = np.array([int(b == 0 and not mask & 3 and mask & 12 != 0) for mask, b in atoms])
    best = {"value": None}
    for tail in itertools.product(range(p), repeat=p-1):
        reply = (1,) + tail
        constraints = []
        for a, r in enumerate(reply):
            constraints.extend(row(r, (a, r)) - row(t, (a, t)) for t in range(p) if t != r)
        constraints.extend(row(0, (0, 1)) - row(a, (a, reply[a])) for a in range(1, p))
        mat = np.array(constraints)
        result = linprog(-D, A_ub=-mat, b_ub=np.zeros(len(mat)), A_eq=[W], b_eq=[1],
                         bounds=(0,None), method='highs')
        if not result.success:
            continue
        value = -result.fun
        if best['value'] is None or value > best['value'] + 1e-8:
            best = {'value': value, 'reply': reply, 'support': [
                {'mask': mask, 'b': b, 'mass': str(F(float(w)).limit_denominator(10**7))}
                for (mask,b),w in zip(atoms, result.x) if w > 1e-8],
                'min_slack_float': float(min(mat @ result.x))}
    return {'p': p, 'bmax': bmax, 'objective': 'protected_union_TQ / actual_tail_profit', 'best': best}


if __name__ == '__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--p',type=int,default=4)
    ap.add_argument('--bmax',type=int,default=3); ap.add_argument('--output')
    args=ap.parse_args(); result=scan(args.p,args.bmax)
    blob=json.dumps(result,ensure_ascii=False,indent=2)
    if args.output: Path(args.output).write_text(blob+'\n')
    print(blob)
