"""HALF(5) discovery: genuine root menus + binary-tail credit + AP rows.

Imports existing row contracts without changing upstream sources. Floating
column generation is discovery only; a final bound needs rational recovery
and exhaustive exact pricing. No finite-game sweep is performed.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from itertools import product
import sys, json, time, hashlib, platform
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').exists())
PEER=ROOT/'research/workspaces/customer-attraction/R-febfdd131cde4128882ca0edd4d712ba/template'
sys.path.insert(0,str(PEER))
import aligned_root_pricing as aligned
from _aligned_rows_safe import aligned_rows_safe
aligned.aligned_rows = aligned_rows_safe
base=aligned.base
RPOS,TYPES,sc,q,PATHS=base.RPOS,base.TYPES,base.sc,base.q,base.PATHS
START=base.START
LABELS=base.LABELS

def alpha2(k):return 8*(k-1)+k*k

def fixed_rows(bits,exact=True):
    Q=base.EX['q'] if exact else base.VE['q']
    b=dict(zip(LABELS,bits));out={}
    for pn,path in PATHS.items():
        for i in range(START[pn],4):
            k=5-i;p=sum(b[x] for x in path[:i]);aa=alpha2(k)
            u=Q(b[path[i]],sum(b[x] for x in path))
            for c in LABELS:
                for d in LABELS:
                    cv,dv=b[c],b[d]
                    out[f'Root:APfixed:{pn}:{i}:{c}:{d}']=aa*u-Q((aa-2)*cv+2*cv*dv,p+k)-Q(2*dv*(1-cv),p+1)
    return out

def root_ap_rows(hist,bits,exact=True):
    Q=base.EX['q'] if exact else base.VE['q']
    def sm(fn):return sum((n*fn(*map(int,t)) for n,t in zip(hist,TYPES)),F(0) if exact else 0)
    b=dict(zip(LABELS,bits));out={}
    for i in (1,2,3):
        k=5-i;aa=alpha2(k)
        us=sm(lambda *tt:Q(tt[i],sum(tt)))
        worst=sm(lambda *tt:Q(1,sum(tt[:i])+k))
        immediate=sm(lambda *tt:Q(1,sum(tt[:i])+1))
        for c in LABELS:
            for d in LABELS:
                cv,dv=b[c],b[d]
                out[f'Root:AProot:{i}:{c}:{d}']=aa*us-((aa-2)*cv+2*cv*dv)*worst-2*dv*(1-cv)*immediate
        for ci,c in enumerate(RPOS):
            for di,d in enumerate(RPOS):
                out[f'Root:APown:{i}:{c}:{d}']=aa*us-sm(lambda *tt:Q((aa-2)*tt[ci]+2*tt[ci]*tt[di],sum(tt[:i])+k)+Q(2*tt[di]*(1-tt[ci]),sum(tt[:i])+1))
    return out

class Universe(aligned.Universe):
    def __init__(self):
        super().__init__()
        self.fixnames=list(fixed_rows([0]*10));self.fixidx={n:i for i,n in enumerate(self.fixnames)}
        self.apbits={tuple(map(int,b)):i for i,b in enumerate(self.bits)}
        self.fixvalues=np.array([[int(sc(v)) for v in fixed_rows(tuple(map(int,b))).values()] for b in self.bits],dtype=np.int64)
        self.names+=self.fixnames
        for i in (1,2,3):
            k=5-i
            self.local[f'APshare:{i}']=self.rh@sc([q(int(t[i]),int(sum(t))) for t in TYPES])
            self.local[f'APworst:{i}']=self.rh@sc([q(1,int(sum(t[:i]))+k) for t in TYPES])
            self.local[f'APinstant:{i}']=self.rh@sc([q(1,int(sum(t[:i]))+1) for t in TYPES])
        rr=root_ap_rows(self.rh.T,[0]*10,False)
        self.apnames=list(rr);self.names+=self.apnames
        for n,v in rr.items():
            if n.startswith('Root:APown:'):self.local[n]=sc(v)
        print(json.dumps({'AP_fixed_rows':len(self.fixnames),'AP_root_rows':len(self.apnames),'total_rows':len(self.names)}),flush=True)
    def atom_rows(self,a):
        rr=super().atom_rows(a);bits=tuple(map(int,a['bits']))
        rr.update(fixed_rows(bits));rr.update(root_ap_rows(a['root_hist'],bits));return rr
    def root_score(self,bits,weights,integer=False):
        ap=[(n,v) for n,v in weights if n.startswith(('Root:APfixed:','Root:AProot:','Root:APown:'))]
        rest=[(n,v) for n,v in weights if not n.startswith(('Root:APfixed:','Root:AProot:','Root:APown:'))]
        _,const,co,E,H=super().root_score(bits,rest,integer)
        b=dict(zip(LABELS,map(int,bits)));bi=self.apbits[tuple(map(int,bits))]
        for n,v in ap:
            tag=n.split(':')[1]
            if tag=='APfixed':const+=v*int(self.fixvalues[bi,self.fixidx[n]])
            elif tag=='APown':co[n]+=v
            else:
                _,_,ii,c,d=n.split(':');i=int(ii);aa=alpha2(5-i);cv,dv=b[c],b[d]
                co[f'APshare:{i}']+=v*aa
                co[f'APworst:{i}']-=v*((aa-2)*cv+2*cv*dv)
                co[f'APinstant:{i}']-=v*2*dv*(1-cv)
        key=tuple(sorted((n,v) for n,v in co.items() if v))
        return key,const,co,E,H

def fast_rows(a):
    rr=aligned.float_atom_rows(a);bits=tuple(map(int,a['bits']))
    rr.update(fixed_rows(bits,False));rr.update(root_ap_rows(a['root_hist'],bits,False));return rr

def run(maxiter=80,target_name="ap_binary_discovery.json",warm_path=None):
    U=Universe();source=PEER/'aligned_root_cg.json';target=HERE/target_name
    warm=json.loads((target if target.exists() else Path(warm_path) if warm_path is not None else source).read_text())
    atoms=[];cols=[];keys=set();ws=[];os=[]
    def add(a):
        key=base.rkey(a)
        if key in keys:return 0
        rr=fast_rows(a);cols.append([float(rr[n]) for n in U.names]);atoms.append(a);keys.add(key)
        ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])));return 1
    pp=warm['primal_float'];keep=[i for i,w in enumerate(pp) if w>1e-10]
    keep+=list(range(max(0,len(warm['atoms'])-240),len(warm['atoms'])))
    for i in sorted(set(keep)):add(warm['atoms'][i])
    for d in (0,5):
        h3=[0]*8;h3[3 if d==0 else 7]=5;h4=[0]*16;h4[7 if d==0 else 15]=5;h5=[0]*32;h5[15 if d==0 else 31]=5
        add({'bits':'1111111111','AB_hist':h3,'AE_hist':h3,'second_hist':h4,'root_hist':h5,'menus_lh':[(5,d)]*3})
    for a in atoms[::max(1,len(atoms)//10)]+atoms[-2:]:
        exact=U.atom_rows(a);fast=fast_rows(a)
        assert max(abs(float(exact[n])-float(fast[n])) for n in U.names)<1e-9
    print(json.dumps({'initial_columns':len(atoms),'row_crosscheck':'passed'}),flush=True)
    hist=[]
    for it in range(maxiter):
        t=time.time();mat=np.asarray(cols).T
        out=linprog(-np.asarray(os,float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[ws],b_eq=[1.],bounds=(0,None),method='highs')
        if not out.success:raise RuntimeError(out.message)
        beta=-out.fun;lam=-out.ineqlin.marginals
        minimum,new,contexts=U.price(lam,beta)
        n=sum(add(a) for _,a in new)
        rec={'iteration':it,'columns':len(atoms),'beta':beta,'minimum_scaled_residual':minimum,'new_columns':n,'pricing_contexts':contexts,'seconds':time.time()-t}
        hist.append(rec);print(json.dumps(rec),flush=True)
        report={'scope':'Floating all-type necessary-condition discovery. Not a proved bound or game.','target':'Q-CAG-HALF-5','row_names':U.names,'atoms':atoms,'primal_float':out.x.tolist()+[0.]*n,'dual_beta_float':beta,'dual_multipliers_float':{name:float(v) for name,v in zip(U.names,lam) if v>1e-10},'history':hist,'sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(aligned.__file__),Path(base.__file__),PEER/'aligned_root_cg.json']},'python':platform.python_version()}
        target.write_text(json.dumps(report,indent=2)+'\n')
        if n==0:break
    return U,out,atoms

if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 80)
