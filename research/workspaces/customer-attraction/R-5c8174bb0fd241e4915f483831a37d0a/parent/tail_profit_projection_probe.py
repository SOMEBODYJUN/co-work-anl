"""Attack a new projected true-tail-profit row on a frozen necessary point.

No SPE or optimality assertion is made about the frozen point.  Float LP only
selects two parameters; every reported row is subsequently evaluated in Fraction.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import hashlib
import json
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
SOURCE = ROOT / 'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/attractive_nested_exact.json'


def share(n, d):
    return F(n, d) if n else F()


def hyp_profit(b, d, r):
    """Uniform r-subset of six optimal indices, independently of forced index."""
    return sum((F(comb(d, q) * comb(6-d, r-q), comb(6, r)) * share(q, b+q)
                for q in range(max(0, r-(6-d)), min(d, r)+1)), F())


def row_value(cols, i, r, beta, alpha, gamma):
    value = F()
    for col, mass in cols:
        a = tuple(map(int, col['actual_bits']))
        b, ell, d = sum(a[:i]), sum(a[:5]), col['d']
        for t in (0, 1):
            prob = F(d if t else 6-d, 6)
            if not prob:
                continue
            local = min(share(t, b+t+z) - gamma*beta*share(z, b+t+z)
                        + alpha*F(z, ell+1) for z in range(r+1))
            value += mass*prob*(local+gamma*hyp_profit(b+t, d, r))
    u = sum((mass*share(int(col['actual_bits'][i]), sum(map(int,col['actual_bits'])))
             for col,mass in cols), F())
    last = sum((mass*share(int(col['actual_bits'][5]), sum(map(int,col['actual_bits'])))
                for col,mass in cols), F())
    return u + r*alpha*last - value


def optimize(cols, i, r, beta):
    # variables alpha >=0, gamma >=0 and free per-column, per-t minimum values
    cells = []
    for col, mass in cols:
        a = tuple(map(int, col['actual_bits']))
        b, ell, d = sum(a[:i]), sum(a[:5]), col['d']
        for t in (0, 1):
            prob = F(d if t else 6-d, 6)
            if prob:
                cells.append((mass*prob,b,ell,d,t))
    n = 2+len(cells)
    objective = np.zeros(n)
    last = sum((mass*share(int(col['actual_bits'][5]), sum(map(int,col['actual_bits'])))
                for col,mass in cols), F())
    objective[0] = float(r*last)
    matrix, rhs = [], []
    for j,(weight,b,ell,d,t) in enumerate(cells):
        objective[j+2] = -float(weight)
        objective[1] -= float(weight*hyp_profit(b+t,d,r))
        for z in range(r+1):
            rr = np.zeros(n)
            rr[j+2] = 1
            rr[0] = -float(F(z,ell+1))
            rr[1] = float(beta*share(z,b+t+z))
            matrix.append(rr)
            rhs.append(float(share(t,b+t+z)))
    lp = linprog(objective, A_ub=np.array(matrix), b_ub=rhs,
                 bounds=[(0,None),(0,None)]+[(None,None)]*len(cells), method='highs')
    assert lp.success, lp.message
    alpha,gamma = (F(float(lp.x[j])).limit_denominator(10**8) for j in (0,1))
    slack = row_value(cols,i,r,beta,alpha,gamma)
    return dict(position=i+1,tail=r,beta=str(beta),alpha=str(alpha),gamma=str(gamma),
                exact_slack=str(slack),slack_float=float(slack),
                scope='one exact valid row selected by a floating LP, not an exact optimum claim')


def main():
    raw=SOURCE.read_bytes()
    data=json.loads(raw)
    cols=[(c,F(c['weight'])) for c in data['columns']
          if c['kind']=='hist' and F(c['weight'])]
    results=[optimize(cols,i,5-i,beta) for i,beta in
             ((1,F(1499,750)),(2,F(5,3)),(3,F(3,2)),(4,F(1)))]
    report=dict(status='OPEN',source=str(SOURCE.relative_to(ROOT)),
                source_sha256=hashlib.sha256(raw).hexdigest(),histogram_count=len(cols),results=results)
    print(json.dumps(report,indent=2))
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__ == '__main__':
    main()
