"""Target U for all pure SPE via independently selectable full off-path children.
Finite separation only: no successful run proves a universal inequality.
"""
from pathlib import Path
import json,sys, numpy as np
from fractions import Fraction as F
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix
from customer_attraction.model import Instance
from customer_attraction.exact import ExactSPESolver, _increment


def K(ins,q):
    return tuple(sum((F(c.multiplicity,1+sum(q[a] for a in c.topics)) for c in ins.customers if t in c.topics),F()) for t in range(ins.topic_count))


def optimize_path(ins,sol,path,time_limit=5):
    n,m=ins.topic_count,ins.players; q=ins.counts(path,terminal=True)
    payoff=ins.player_payoffs(path); welfare=ins.welfare(q)
    kval={z:K(ins,z) for z in sol.outcomes()}
    # Every possible child terminal is a full-game terminal too, but may not be a root SPE.
    choices={}; k=(0,)*n
    for i,a0 in enumerate(path):
        for a in range(n):
            if a==a0:continue
            cand=tuple(z for z in sol.outcomes(_increment(k,a)) if ins.topic_payoff(a,z)<=payoff[i])
            assert cand
            choices[i,a]=cand
            for z in cand:
                if z not in kval:kval[z]=K(ins,z)
        k=_increment(k,a0)
    bins={}; nextv=n+m
    for key,cand in choices.items():
        for z in cand:bins[key,z]=nextv;nextv+=1
    rows=[]; low=[]; high=[]
    def add(row,l=-np.inf,h=np.inf):rows.append(row);low.append(l);high.append(h)
    add({t:1 for t in range(n)},1,1)
    actual=K(ins,q)
    for i in range(m):add({**{t:-float(actual[t]) for t in range(n)},n+i:1},h=0)
    big=max(float(x) for vals in kval.values() for x in vals)+1
    for key,cand in choices.items():
        i,a=key;add({bins[key,z]:1 for z in cand},1,1)
        for z in cand:
            row={t:-float(kval[z][t]) for t in range(n)};row[n+i]=1;row[bins[key,z]]=big
            add(row,h=big)
    A=lil_matrix((len(rows),nextv))
    for r,row in enumerate(rows):
        for j,v in row.items():A[r,j]=v
    obj=np.zeros(nextv);obj[n:n+m]=-1
    ub=np.ones(nextv);ub[n:n+m]=big
    integ=np.zeros(nextv);integ[n+m:]=1
    res=milp(obj,integrality=integ,bounds=Bounds(np.zeros(nextv),ub),constraints=LinearConstraint(A.tocsr(),low,high),options={'time_limit':time_limit,'mip_rel_gap':1e-8})
    if res.x is None:return {'status':str(res.message)}
    p=tuple(F(float(v)).limit_denominator(100000) for v in res.x[:n]);p=tuple(v/sum(p) for v in p)
    selected={key:max(cand,key=lambda z:res.x[bins[key,z]]) for key,cand in choices.items()}
    vals=[]
    for i in range(m):
        cols=[q]+[z for (ii,a),z in selected.items() if ii==i]
        vals.append(min(sum((p[t]*K(ins,z)[t] for t in range(n)),F()) for z in cols))
    gap=sum(vals,F())-welfare
    return {'status':str(res.message),'path':list(path),'W':welfare,'payoffs':list(map(str,payoff)),'p':list(map(str,p)),'psi':list(map(str,vals)),'gap':str(gap),'numeric_gap':float(gap),'choices':{f'{i},{a}':list(z) for (i,a),z in selected.items()}}

if __name__=='__main__':
    source=Path(sys.argv[1]);obj=json.loads(source.read_text());ins=Instance.from_dict(obj.get('instance',obj));sol=ExactSPESolver(ins)
    # Candidate U is specified above; stop at first actual separating full-menu strategy.
    best=None;done=0
    for path in sol.ordered_outcomes():
        ans=optimize_path(ins,sol,path);done+=1
        if 'numeric_gap' in ans and (best is None or ans['numeric_gap']>best['numeric_gap']):
            best=ans;print(json.dumps({'done':done,'new_best':best}),flush=True)
        if best is not None and best['numeric_gap']>1e-7:break
    print(json.dumps({'candidate':'U: sum_i min_A G_p(Z_i(A)) <= W for every full-history pure SPE and every p','source':str(source),'paths_checked':done,'best':best,'scope':'Finite full-continuation separation diagnostic; nonseparation is not general evidence.'}),flush=True)
