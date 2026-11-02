"""Diagnose exact candidate sum_i p^T K_i p <= W on existing full trees.

This is one finite candidate test, not an SPE search or proof. A positive
optimization witness is independently recomputed as Fraction.
"""
import itertools,json,pathlib
from fractions import Fraction as F
import numpy as np
from scipy.optimize import minimize

ROOT=pathlib.Path(__file__).resolve().parents[6]
OUT=pathlib.Path(__file__).resolve().parent

def main():
    rows=[]
    for ip in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
        cp=ROOT/'evidence/certificates/customer_attraction'/ip.name
        if not cp.exists():continue
        obj=json.loads(ip.read_text());cert=json.loads(cp.read_text())
        strategy=cert.get('strategy',{}) if isinstance(cert,dict) else {}
        if not isinstance(strategy,dict) or not strategy.get('actions'):continue
        acts={tuple(r['history']):r['action'] for r in strategy['actions']}
        m=obj['players'];k=len(obj['topics'])
        if len(acts)!=sum(k**i for i in range(m)):continue
        cs=[frozenset(c['topics']) for c in obj['customers'] for _ in range(c.get('multiplicity',1))]
        def end(h):
            while len(h)<m:h=h+(acts[h],)
            return h
        def payoff(a,z,extra=0):
            return sum((F(1,extra+sum(t in c for t in z)) for c in cs if a in c),F())
        for h in acts:
            assert payoff(acts[h],end(h))>=max(payoff(a,end(h+(a,))) for a in range(k))
        z=end(());W=sum(any(t in c for t in z) for c in cs)
        H=[[F() for a in range(k)] for t in range(k)]
        for i in range(m):
            Z=[end(z[:i]+(a,)) for a in range(k)]
            for t,a in itertools.product(range(k),repeat=2):H[t][a]+=payoff(t,Z[a],1)
        mat=np.array([[float(v) for v in row] for row in H])
        starts=[np.ones(k)/k]+[np.eye(k)[j] for j in range(k)]
        starts += [(np.eye(k)[a]+np.eye(k)[b])/2 for a,b in itertools.combinations(range(k),2)]
        best=None
        for p0 in starts:
            res=minimize(lambda p:-p@mat@p,p0,jac=lambda p:-(mat+mat.T)@p,
                bounds=[(0,1)]*k,constraints=[{'type':'eq','fun':lambda p:p.sum()-1,'jac':lambda p:np.ones(k)}],
                method='SLSQP',options={'ftol':1e-11,'maxiter':300})
            if best is None or res.fun<best.fun:best=res
        p=[max(F(),F(float(v)).limit_denominator(1000000)) for v in best.x];p=[v/sum(p) for v in p]
        value=sum((p[t]*H[t][a]*p[a] for t,a in itertools.product(range(k),repeat=2)),F())
        row={'instance':ip.name,'m':m,'W':W,'p':[str(v) for v in p],'value':str(value),'gap':str(value-W)}
        rows.append(row)
        print(ip.name,'gap',float(value-W))
    (OUT/'extra_slot_aggregate_diagnostic.json').write_text(json.dumps({'scope':'existing certificate diagnosis only; all-input candidate not proved','results':rows},indent=2)+'\n')

if __name__=='__main__':main()
