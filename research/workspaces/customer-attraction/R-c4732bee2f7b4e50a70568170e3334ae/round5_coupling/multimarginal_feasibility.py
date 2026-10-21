"""One three-family customer coupling for all selected genuine menu rows.

Fixed-marginal finite discovery. Each client's joint histogram is allowed
fractionally; no SPE or globally welfare-optimal conclusion is claimed.
"""
from pathlib import Path
import sys,json,hashlib
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix,csr_matrix,hstack
HERE=Path(__file__).resolve().parent;ACTOR=HERE.parent
sys.path.insert(0,str(ACTOR/'round4_coupling'))
from pair_transport import LM,ORBITS,row as pair_envelope,specs as pair_specs
from joint_transport import family,joint_row
FAMILIES=('AB','AE','second')

def terminal_specs():
    for s,t in product(FAMILIES,repeat=2):
        if s==t:continue
        for p in range(1,4 if t=='second' else 3):
            for k in ('D','O'):yield f'{s}:{t}:terminal{p}{k}',s,t,p,k

def state(atom,source,s):
    a,b,c,d,e,*_=map(int,atom['bits'])
    prefix=a+(b if source=='AB' else e) if source!='second' else a
    p=prefix+sum(s[:-2]);first,last=s[-2:]
    H=F(first+last,p+first+last) if first+last else F(0);H+=F(first,(p+1)*(p+2))
    den=prefix+sum(s[:-1])+1
    return p,H,F(last,den),F(1,den)

def solve(path,mode='pair_positive_terminal'):
    atoms=json.loads(path.read_text())['atoms'];masses=[F(a['exact_mass']) for a in atoms]
    ps=list(pair_specs());ts=list(terminal_specs());slacks={}
    for name,s,t,p,k in ts:
        slacks[name]=sum((m*joint_row(a,s,t,((p,k,F(1)),)) for a,m in zip(atoms,masses)),F(0))
    if mode=='pair':ts=[]
    elif mode=='pair_positive_terminal':ts=[z for z in ts if slacks[z[0]]>=0]
    rows=[('pair',)+z for z in ps]+[('terminal',)+z for z in ts]
    rc=[];marg=[];vars=[]
    for ai,(atom,mass) in enumerate(zip(atoms,masses)):
        data={s:family(atom,s) for s in FAMILIES};q=5
        for tbit in (0,1):
            supports={s:sorted(set(z for z in data[s] if z[0]==tbit)) for s in FAMILIES}
            vi=[]
            for triple in product(*(supports[s] for s in FAMILIES)):
                slot=dict(zip(FAMILIES,triple));idx=len(vars);vars.append((ai,triple));vi.append((idx,slot));coeff=[]
                for spec in rows:
                    typ,name,source,target,*rest=spec
                    s=slot[source];z=slot[target];p,H,own,inv=state(atom,source,s)
                    tar=data[target]
                    if typ=='pair':
                        (u,v),o=rest;B=sum(w[u] for w in tar);C=sum(w[v] for w in tar);K=sum(w[u]*w[v] for w in tar)
                        n,L,M=LM(q,z[u],z[v],B,C,K)[o]
                        coeff.append(n*H-F(L,p+1)+F(M,(p+1)*(p+2)))
                    else:
                        pos,kind=rest
                        coeff.append(own-inv*z[pos] if kind=='D' else (q-1)*own-inv*(sum(w[pos] for w in tar)-z[pos]))
                rc.append(coeff)
            for s in FAMILIES:
                for z in supports[s]:marg.append(([(idx,1) for idx,slot in vi if slot[s]==z],mass*data[s].count(z)))
    Aeq=lil_matrix((len(marg),len(vars)));b=[]
    for i,(entries,rhs) in enumerate(marg):
        for j,v in entries:Aeq[i,j]=v
        b.append(float(rhs))
    R=np.asarray([[float(c) for c in col] for col in rc]).T
    norms=[]
    for spec in rows:
        if spec[0]=='pair':o=spec[-1];norms.append(1 if o==0 else 4 if o<4 else 12)
        else:norms.append(1 if spec[-1]=='D' else 4)
    Au=csr_matrix(np.column_stack((-R,norms)));Ae=hstack((Aeq.tocsr(),csr_matrix((len(marg),1)))).tocsr()
    c=np.zeros(len(vars)+1);c[-1]=-1
    res=linprog(c,A_ub=Au,b_ub=np.zeros(len(rows)),A_eq=Ae,b_eq=np.asarray(b),bounds=[(0,None)]*len(vars)+[(None,None)],method='highs')
    out={'scope':'Numerical convex three-family necessary-condition relaxation only','source_path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'mode':mode,'variables':len(vars),'marginal_equalities':len(marg),'rows':len(rows),'success':res.success,'message':res.message,'negative_single_terminal_envelopes':{n:str(v) for n,v in slacks.items() if v<0}}
    if res.success:
        lam=-res.ineqlin.marginals
        out.update({'max_common_normalized_margin':float(res.x[-1]),'joint_weights':{spec[1]:float(v) for spec,v in zip(rows,lam) if v>1e-9}})
    return out

if __name__=='__main__':
    path=Path(sys.argv[1]) if len(sys.argv)>1 else ACTOR/'round5_pricing/exact_optimum_primal_cross_pair.json'
    reports=[solve(path,mode) for mode in ('pair','pair_positive_terminal','all')]
    (HERE/f'multimarginal_{path.stem}.json').write_text(json.dumps(reports,indent=2)+'\n')
    print(json.dumps(reports,indent=2))
