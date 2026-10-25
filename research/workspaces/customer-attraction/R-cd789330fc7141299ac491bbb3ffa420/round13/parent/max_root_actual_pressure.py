"""HALF5 template attack: actual path plus true largest-theme root child.
Full 10-bit/opt-multiplicity domain. Float discovery, no SPE-primal claim.
"""
import json
from itertools import product,combinations_with_replacement
from math import comb
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

def choose(n,k): return comb(n,k) if 0<=k<=n else 0

def main():
    bits=np.array(list(product((0,1),repeat=10)),dtype=np.int8)
    b=np.repeat(bits,6,axis=0); e=np.tile(np.arange(6),len(bits))
    n=len(e); act=list(range(5)); child=list(range(5,10))
    w=np.any(b[:,:5],axis=1).astype(float); o=(e>0).astype(float)
    rows=[]; names=[]
    def add(name,v): names.append(name); rows.append(v)
    def profits(path):
        load=b[:,path].sum(axis=1)
        return [np.divide(b[:,a],load,out=np.zeros(n),where=load>0) for a in path]
    ua=profits(act); uc=profits(child)
    for path,uu,tag,start in ((act,ua,'actual',0),(child,uc,'maxroot',1)):
        for j in range(start,5):
            pre=b[:,path[:j]].sum(axis=1); rem=5-j
            for q in range(10): add(f'{tag}:node{j+1}:floor{q}',uu[j]-b[:,q]/(pre+rem))
            add(f'{tag}:node{j+1}:sumopt',5*uu[j]-e/(pre+rem))
            if rem in (2,3,4):
                beta={2:1.5,3:5/3,4:1499/750}[rem]
                comp=np.zeros(n)
                for count in range(1,rem+1):
                    mult=np.array([choose(int(a),count)*choose(5-int(a),rem-count) for a in e])
                    comp+=mult*count/(pre+count)
                add(f'{tag}:tail{rem}:opt_profit',choose(5,rem)*beta*sum(uu[j:])-comp)
            if rem==2:
                tax=b[:,path[j]]/((pre+1)*(pre+2)); H=sum(uu[j:])+tax
                comp=np.zeros(n)
                for count in (1,2):
                    mult=np.array([choose(int(a),count)*choose(5-int(a),2-count) for a in e])
                    comp+=mult*count/(pre+count)
                add(f'{tag}:tail2:exact_tax_opt',10*H-comp)
                for q,r in combinations_with_replacement(range(10),2):
                    load=b[:,q]+b[:,r]
                    add(f'{tag}:tail2:exact_tax{q},{r}',H-load/(pre+load+(load==0)))
    add('root_IC_max',ua[0]-uc[0])
    for q in range(10): add(f'max_size{q}',b[:,5]-b[:,q])
    add('max_size_opt_average',5*b[:,5]-e)
    for i in range(5): add(f'actual{i+1}:global_size_cap',5*ua[i]-b[:,5])
    z=linprog(-o,A_ub=-np.array(rows),b_ub=np.zeros(len(rows)),A_eq=[w],b_eq=[1.],bounds=(0,None),method='highs')
    out={'status':'floating_template_only','types':n,'rows':len(rows),'success':bool(z.success),'message':z.message}
    if z.success:
        out.update({'O_over_W':float(-z.fun),'actual_utilities':[float(u@z.x) for u in ua],'max_size':float(b[:,5]@z.x),'rootmax_utilities':[float(u@z.x) for u in uc],'active_dual':{name:float(-v) for name,v in zip(names,z.ineqlin.marginals) if v<-1e-8},'support':[{'bits':''.join(map(str,b[i])),'opt_multiplicity':int(e[i]),'mass':float(v)} for i,v in enumerate(z.x) if v>1e-9]})
    path=Path(__file__).with_suffix('.json')
    with path.open('x') as f: json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k not in ('support','active_dual')},indent=2))
if __name__=='__main__': main()
