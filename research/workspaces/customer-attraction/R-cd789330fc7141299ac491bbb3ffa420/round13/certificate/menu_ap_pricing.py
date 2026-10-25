"""Full-domain discovery with true-history AP applied to existing menus.

The AP theorem allows every legal C,D.  Old implementations applied it to
fixed labels and new-root own labels but not the older indexed reply menus.
Summing over both query indices uses only same-family count products, so
the original full histogram oracle remains exact.  Float discovery only.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import sys,json,time,hashlib
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').exists())
OLD=ROOT/'research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_pricing'
sys.path.insert(0,str(OLD))
from full_pricing import Universe as BaseUniverse, atom_key, sc, LABELS, PATHS, START, q
from cross_pair_pricing import CrossUniverse

NODES=[(pn,i) for pn,path in PATHS.items() for i in range(START[pn],4)]
MENUS={'AB':('mX','mY'),'AE':('mX','mY'),'Sbranch':('mU','mV','mW')}
FIELDS={'AB':'AB_hist','AE':'AE_hist','Sbranch':'second_hist'}
TYPES={k:list(product((0,1),repeat=k)) for k in (3,4)}
def aa(k):return 8*(k-1)+k*k
def source(bits,node):
    pn,i=node;path=PATHS[pn];p=sum(bits[LABELS.index(t)] for t in path[:i]);k=5-i
    return p,k,q(bits[LABELS.index(path[i])],sum(bits[LABELS.index(t)] for t in path))
def ap_value(u,p,k,c,d,nc,nd):
    a=aa(k);return nc*nd*a*u-q((a-2)*nd*c+2*c*d,p+k)-q(2*(nc*d-c*d),p+1)
def fixed_rows(bits,d):
    out={}
    for pn,i in NODES:
        p,k,u=source(bits,(pn,i))
        for c in LABELS:
            for e in LABELS:
                out[f'APfixed:{pn}:{i}:{c}:{e}']=ap_value(u,p,k,bits[LABELS.index(c)],bits[LABELS.index(e)],1,1)
        out[f'APfixed:{pn}:{i}:opt:opt']=ap_value(u,p,k,d,d,5,5)
    return out
def menu_specs():
    specs=[]
    for tag,menus in MENUS.items():
        pairs=[(c,e) for c in menus for e in LABELS]+[(c,e) for c in LABELS for e in menus]
        pairs += [(c,'opt') for c in menus]+[('opt',e) for e in menus]
        pairs += [(c,e) for c in menus for e in menus]
        for pn,i in NODES:
            for c,e in pairs:specs.append((f'{tag}:APmenu:{pn}:{i}:{c}:{e}',tag,(pn,i),c,e))
    return specs

class Universe(CrossUniverse):
    def __init__(self):
        super().__init__();self.nbase=len(self.names);assert self.nbase==717
        self.specs=menu_specs();self.specmap={z[0]:z for z in self.specs}
        self.fixednames=list(fixed_rows((0,)*10,0));self.names+=self.fixednames+[z[0] for z in self.specs]
        # Add fixed-state rows to the original base tensor and leave old-menu
        # affine coefficients zero. The original price() will then use them.
        extra=np.asarray([[[int(sc(v)) for v in fixed_rows(bits,d).values()] for d in range(6)] for bits in self.bits],dtype=np.int64)
        self.base=np.concatenate((self.base,extra),axis=2)
        zeros=np.zeros((1024,6,3,len(self.fixednames)),dtype=np.int64)
        self.ec=np.concatenate((self.ec,zeros),axis=3);self.hc=np.concatenate((self.hc,zeros),axis=3)
        self.oldids+=list(range(self.nbase,self.nbase+len(self.fixednames)))
        self.countarr={tag:{'opt':self.d[4 if tag=='Sbranch' else 3],**{'m'+n:v for n,v in self.count[4 if tag=='Sbranch' else 3].items()}} for tag in MENUS}
        print(json.dumps({'new_fixed_AP_rows':len(self.fixednames),'new_menu_AP_rows':len(self.specs),'total_rows':len(self.names)}),flush=True)
    def atom_rows(self,atom):
        rr=CrossUniverse.atom_rows(self,atom);bits=tuple(map(int,atom['bits']));d=sum(atom['AB_hist'][4:]);rr.update(fixed_rows(bits,d))
        counts={}
        for tag,field in FIELDS.items():
            k=4 if tag=='Sbranch' else 3;ty=TYPES[k];hist=atom[field]
            counts[tag]={'opt':d,**{t:sum(n*z[j] for n,z in zip(hist,ty)) for j,t in enumerate(MENUS[tag],1)}}
        for n,tag,node,c,e in self.specs:
            p,k,u=source(bits,node);cc=counts[tag][c] if c in counts[tag] else bits[LABELS.index(c)];dd=counts[tag][e] if e in counts[tag] else bits[LABELS.index(e)]
            rr[n]=ap_value(u,p,k,cc,dd,5 if c in counts[tag] else 1,5 if e in counts[tag] else 1)
        return rr
    def family_score(self,bits,tag,weights,integer=False):
        extra=[(n,v) for n,v in weights if ':APmenu:' in n];rest=[(n,v) for n,v in weights if ':APmenu:' not in n]
        key,const,vec,me,mh=super().family_score(bits,tag,rest,integer=integer)
        co=defaultdict(int if integer else float);arr=self.countarr[tag]
        # Each term is an affine/quadratic function of one family's counts.
        # Coefficients are scaled by 120, matching the original oracle.
        for n,v in extra:
            _,_,node,c,e=self.specmap[n];p,k,u=source(bits,node);a=aa(k)
            nc=5 if c in arr else 1;nd=5 if e in arr else 1
            const+=v*int(sc(nc*nd*a*u))
            cv=None if c in arr else bits[LABELS.index(c)];dv=None if e in arr else bits[LABELS.index(e)]
            def add_term(factor,variables):
                nonlocal const
                variables=tuple(sorted(variables))
                if not variables:const+=v*int(sc(factor))
                else:co[variables]+=v*int(sc(factor))
            if cv is None:add_term(-q((a-2)*nd,p+k),(c,))
            else:add_term(-q((a-2)*nd*cv,p+k),())
            if dv is None:add_term(-q(2*nc,p+1),(e,))
            else:add_term(-q(2*nc*dv,p+1),())
            factor=-q(2,p+k)+q(2,p+1)
            if cv is None and dv is None:add_term(factor,(c,e))
            elif cv is None:add_term(factor*dv,(c,))
            elif dv is None:add_term(factor*cv,(e,))
            else:add_term(factor*cv*dv,())
        for variables,v in co.items():
            ar=np.ones(len(self.hist[key[0]]),dtype=np.int64)
            for t in variables:ar=ar*arr[t]
            vec.append((v,ar))
        return (key[0],key,tuple(sorted(co.items()))),const,vec,me,mh
    def price(self,lam,beta,**kw):
        integer=kw.get('integer',False)
        self.crossweights=[(*row,int(w) if integer else float(w)) for row,w in zip(self.cross,lam[557:717]) if abs(w)>1e-11];self.extra_cache={}
        return BaseUniverse.price(self,lam,beta,**kw)

def run(maxiter=60):
    U=Universe();target=HERE/'menu_ap_discovery.json'
    src=json.loads((target if target.exists() else OLD/'cg_cross_pair_final.json').read_text())
    atoms=[];keys=set();cols=[];ws=[];os=[]
    def add(a):
        key=atom_key(a)
        if key in keys:return 0
        rr=U.atom_rows(a);cols.append([float(rr[n]) for n in U.names]);atoms.append(a);keys.add(key);ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])));return 1
    pp=src.get('primal_float');keep=list(range(len(src['atoms']))) if pp is None else [i for i,w in enumerate(pp) if w>1e-9]+list(range(max(0,len(src['atoms'])-150),len(src['atoms'])))
    for i in sorted(set(keep)):add(src['atoms'][i])
    for d in (0,5):
        h3=[0]*8;h3[3 if d==0 else 7]=5;h4=[0]*16;h4[7 if d==0 else 15]=5
        add({'bits':'1111111111','AB_hist':h3,'AE_hist':h3,'second_hist':h4,'menus_lh':[(5,d)]*3})
    history=src.get('history',[]) if target.exists() else []
    for it in range(maxiter):
        t=time.time();mat=np.asarray(cols).T
        out=linprog(-np.asarray(os,float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[ws],b_eq=[1.],bounds=(0,None),method='highs');assert out.success,out.message
        beta=-out.fun;lam=-out.ineqlin.marginals
        minimum,new,contexts=U.price(lam,beta,batch=100)
        n=sum(add(a) for _,a in new);rec={'iteration':len(history),'columns':len(atoms),'beta':beta,'minimum_scaled_residual':float(minimum),'new_columns':n,'pricing_contexts':contexts,'seconds':time.time()-t};history.append(rec);print(json.dumps(rec),flush=True)
        report={'scope':'Floating full-type AP closure discovery. Not a theorem, SPE, actual OPT, or template exact optimum.','target':'HALF(5)','row_names':U.names,'atoms':atoms,'primal_float':out.x.tolist()+[0.]*n,'dual_beta_float':beta,'dual_multipliers_float':{name:float(v) for name,v in zip(U.names,lam) if v>1e-10},'history':history,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()};target.write_text(json.dumps(report,indent=2)+'\n')
        if n==0:break
    return U,out,atoms
if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 60)
