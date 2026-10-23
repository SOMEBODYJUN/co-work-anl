"""Probe the full cross-support joining-gradient relaxation.

The finite supporting-potential extension encodes every directed cycle, not
merely pairwise monotonicity.  Floating optimization is exploratory only.
No abstract payoff vector produced here is claimed to have customer weights.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import importlib.util
import json
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SOURCE = ROOT / 'research/workspaces/customer-attraction/R-fa8dd4ddea574a74a634ebc71e6f9ccb/continue_coupling/verify_all_pair_obstruction.py'


def data():
    spec = importlib.util.spec_from_file_location('inherited_exact_data', SOURCE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.reconstruct()


def setup():
    obj,m,p,actions,histories,terminal,qs,vs,y,types,cover = data()
    bs = sorted({tuple(q[i] - (i == a) for i in range(p)) for q,a in vs})
    vid = {v:i for i,v in enumerate(vs)}
    nv,nb = len(vs),len(bs)
    nn = nv+nb
    def unit(q,a):
        r = np.zeros(nn)
        r[vid[q,a]] = 1
        return r
    covers = {}
    for q in qs:
        A = tuple(a for a in range(p) if q[a])
        covers.setdefault(A, sum((q[a]*unit(q,a) for a in A), np.zeros(nn)))
    ub,eq = [],[]
    for h in histories:
        a = actions[h]
        for b in range(p):
            ub.append(unit(terminal(h+(b,)),b)-unit(terminal(h),a))
    for q,a in vs:
        for r,b in vs:
            if a != b or q == r:
                continue
            kappa = max(Q(sum(r[c] for c in range(p) if B>>c&1),sum(q[c] for c in range(p) if B>>c&1)) for B in types if B>>a&1)
            ub.append(unit(q,a)-float(kappa)*unit(r,a))
    for q,a in vs:
        A = tuple(c for c in range(p) if q[c])
        eq.append(sum((q[c]*unit(q,c) for c in A),np.zeros(nn))-covers[A])
        if len(A) == 2:
            b = next(c for c in A if c != a)
            r,s = q[a],q[b]
            eq.append(m*r*unit(q,a)-r*covers[(a,)]-s*(covers[A]-covers[(b,)]))
    # All arbitrary-length cycles iff these finite supergradient inequalities
    # admit real potential labels L_b (difference-constraints theorem).
    for i,b in enumerate(bs):
        for j,d in enumerate(bs):
            if i == j:
                continue
            row = np.zeros(nn)
            row[nv+j] += 1
            row[nv+i] -= 1
            for a in range(p):
                q = tuple(b[c]+(c==a) for c in range(p))
                row -= (d[a]-b[a])*unit(q,a)
            ub.append(row)
    root = covers[tuple(a for a in range(p) if terminal(())[a])]
    eq.append(root)
    rhs = np.zeros(len(eq));rhs[-1] = 1
    return obj,m,p,vs,bs,np.array(ub),np.array(eq),rhs,covers


def main():
    obj,m,p,vs,bs,ub,eq,rhs,covers = setup()
    results = []
    best = None
    for target in combinations(range(p),m):
        objective = covers[target]
        sol = linprog(-objective,A_ub=ub,b_ub=np.zeros(len(ub)),A_eq=eq,b_eq=rhs,
                      bounds=[(0,None)]*len(vs)+[(None,None)]*len(bs),method='highs')
        rec = {'target':list(target),'success':sol.success,'value':float(-sol.fun) if sol.success else None}
        results.append(rec)
        if sol.success and (best is None or -sol.fun > best['value']+1e-8):
            best = rec | {'y':[{'q':list(q),'a':a,'value':str(Q(float(sol.x[i])).limit_denominator(10000000))} for i,(q,a) in enumerate(vs)],
                          'potential':[{'b':list(b),'value':str(Q(float(sol.x[len(vs)+i])).limit_denominator(10000000))} for i,b in enumerate(bs)]}
    out = {'scope':'Fixed inherited three-player strategy; abstract all-cross-support CG relaxation, not a customer game or SPE counterexample',
           'players':m,'topics':p,'payoff_vertices':len(vs),'gradient_states':len(bs),
           'ub_rows':len(ub),'eq_rows':len(eq),'strategy_actions':obj['strategy_actions'],
           'results':results,'best':best}
    (HERE/'cross_support_gradient_probe.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('strategy_actions','results','best')} | {'best_target':best['target'],'best_value':best['value']},indent=2))


if __name__ == '__main__':
    main()
