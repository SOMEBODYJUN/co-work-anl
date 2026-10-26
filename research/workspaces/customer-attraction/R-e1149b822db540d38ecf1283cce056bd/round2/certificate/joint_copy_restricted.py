"""Add genuinely new common-catalogue ICs across distinct real copies.
Discovery restricted LP only; never a game counterexample or theorem.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,time
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
REPO=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').exists())
SOURCE=REPO/'research/workspaces/customer-attraction/R-bfbfe64dd5f94fa09d36b75198633f2b/five_only'
sys.path.insert(0,str(SOURCE))
import actual_root_copies as c
# Scalar-only restricted evaluation; discovery, with later exact independent audit.
def scalar_q(n,d): return n/d if n else 0.0
c.old.VE['q']=scalar_q
c.fixed_rows.__globals__['base'].VE['q']=scalar_q

def cross_rows(a,exact=False,sources=None):
    q=c.old.EX['q'] if exact else c.old.VE['q']
    b=dict(zip(c.LABELS,map(int,a['bits'])))
    chosen=c.ROOTS if sources is None else sources
    rr={}
    for s in chosen:
        pre,forced=c.SPECS[s];path=tuple(b[x] for x in pre)+(b[forced],*a['copies'][s])
        for t in chosen:
            if s==t: continue
            for i in range(c.FIRST[s],5):
                v=q(path[i],sum(path));den=sum(path[:i])+5-i
                for j,x in enumerate(a['copies'][t]):
                    rr[f'Joint:{s}:{i}:{t}:{j}']=v-q(x,den)
    return rr

def run(which='all'):
    stamp=time.time();U=object.__new__(c.Universe)
    src=SOURCE/'penultimate_branch_half_search.json'
    warm=json.loads(src.read_text());atoms=warm['atoms']
    U.names=list(U.atom_rows(atoms[0],False))
    sources=None if which=='all' else tuple(which.split(','))
    newnames=list(cross_rows(atoms[0],sources=sources));names=U.names+newnames
    print(json.dumps({'old_rows':len(U.names),'new_rows':len(newnames),'columns':len(atoms)}),flush=True)
    cols=[];ws=[];os=[]
    for j,a in enumerate(atoms):
        rr=U.atom_rows(a,False);rr.update(cross_rows(a,sources=sources))
        cols.append([float(rr[n]) for n in names])
        ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])))
        if j%1000==0: print(json.dumps({'built':j,'seconds':time.time()-stamp}),flush=True)
    mat=np.asarray(cols);scale=np.maximum(1.,np.max(np.abs(mat),axis=0))
    result=linprog(np.r_[np.zeros(len(names)),1.],A_ub=np.c_[mat/scale,-np.asarray(ws)],b_ub=-np.asarray(os),bounds=[(0,None)]*(len(names)+1),method='highs')
    out={'scope':'Finite restricted necessary-row LP only. Neither a universal bound nor a SPE counterexample.','status':result.message,'new_relation':'Cross-new-branch ICs in one common catalogue, including exact terminal ICs','old_rows':len(U.names),'new_rows':len(newnames),'columns':len(atoms),'seconds':time.time()-stamp}
    if result.success:
        out['restricted_beta_float']=float(result.x[-1]);out['positive_new_multipliers']={n:float(v) for n,v in zip(newnames,result.x[len(U.names):-1]/scale[len(U.names):]) if v>1e-10}
        out['dual_multipliers_float']={n:float(v) for n,v in zip(names,result.x[:-1]/scale) if v>1e-10}
        weights=-result.ineqlin.marginals
        out['primal_positive_count']=int(np.sum(weights>1e-9))
        out['primal_atoms']=[{'weight':float(v),'atom':a} for a,v in zip(atoms,weights) if v>1e-9]
        print(json.dumps({k:v for k,v in out.items() if k not in ('primal_atoms','dual_multipliers_float','positive_new_multipliers')}),flush=True)
    (HERE/f'joint_copy_restricted_{which.replace(",","_")}.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':run(sys.argv[1] if len(sys.argv)>1 else 'all')
