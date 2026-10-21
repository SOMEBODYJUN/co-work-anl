"""Sample unrestricted fresh-label policies, then optimize their whole cones.

Every sample is first checked on uniform positive customer types. The
numerical optimization does not assert any universal bound.
"""
import json
import math
import random
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from customer_attraction import Instance, CustomerType, StrategyCertificate, verify_certificate
from cone_static_allowance import matrix


def main():
    rng = random.Random(202610213)
    best = 0
    record = []
    for m, k, runs in [(3, 6, 80), (4, 7, 50), (5, 7, 30)]:
        uniform = Instance(tuple(map(str, range(k))), tuple(
            CustomerType(frozenset(a for a in range(k) if mask >> a & 1), 1)
            for mask in range(1, 1 << k)), m)
        for trial in range(runs):
            actions = {}
            def fill(h):
                if len(h) == m:
                    return
                fresh = [a for a in range(k) if a not in h]
                actions[h] = rng.choice(fresh)
                for a in range(k):
                    fill(h+(a,))
            fill(())
            h = ()
            while len(h) < m:
                h += (actions[h],)
            q = tuple(h.count(a) for a in range(k))
            cert = StrategyCertificate(actions, q)
            verify_certificate(uniform, cert).assert_valid()
            G, cover, ds, scale = matrix(cert, k, m)
            for a, d in enumerate(ds):
                result = linprog(-d, A_ub=-G, b_ub=np.zeros(len(G)),
                                 A_eq=cover[None, :], b_eq=[1], bounds=(0, None), method='highs')
                if not result.success:
                    raise RuntimeError(result.message)
                ratio = -result.fun/scale
                if ratio > best+1e-8:
                    best = ratio
                    record.append({'m': m, 'k': k, 'trial': trial, 'a': a,
                                   'ratio': ratio, 'certificate': cert.to_dict()})
                    Path(__file__).with_name('fresh_policy_checkpoints.json').write_text(
                        json.dumps(record, indent=2)+'\n')
                    print(json.dumps({'m': m, 'k': k, 'trial': trial, 'a': a,
                                      'ratio': ratio}), flush=True)
                if ratio > (m+1)/m + 1e-7:
                    rr = [Fraction(float(x)).limit_denominator(100000) for x in result.x]
                    denom = math.lcm(*(x.denominator for x in rr))
                    vv = [int(x*denom) for x in rr]
                    ins = Instance(tuple(map(str, range(k))), tuple(
                        CustomerType(frozenset(b for b in range(k) if mask >> b & 1), v)
                        for mask, v in enumerate(vv, start=1) if v), m)
                    check = verify_certificate(ins, cert)
                    if not check.valid:
                        print('RATIONAL_RECONSTRUCTION_FAILED', flush=True)
                        continue
                    dd = Fraction(sum(int(x)*v for x, v in zip(d, vv)), scale)
                    ww = sum(int(x)*v for x, v in zip(cover, vv))
                    if dd <= Fraction(m+1, m)*ww:
                        continue
                    out = Path(__file__).with_name('fresh_static_allowance_failure.json')
                    out.write_text(json.dumps({'instance': ins.to_dict(), 'certificate': cert.to_dict(),
                                               'a': a, 'D': str(dd), 'W': ww,
                                               'D_over_W': str(dd/ww)}, indent=2)+'\n')
                    print('EXACT_FAILURE', out, flush=True)
                    return
    print('COMPLETE', best, flush=True)


if __name__ == '__main__':
    main()
