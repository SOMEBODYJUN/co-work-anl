"""Targeted attack on a new, explicitly stronger net-refund floor.

Candidate: for fixed optimal O and D=O\\C, each actual player at remaining
r has u_i+e_i >= f_D(r)-f_D(r-1), e_i=profit on B_i\\O.  Only a positive
floating discovery is retained; it requires a separate exact full-tree audit.
This is not an attack on HALF and no negative-search table is a deliverable.
"""
from pathlib import Path
from itertools import combinations
from functools import lru_cache
import json
import sys
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]

def attack(m,k,actions,name):
    masks=np.arange(1,1<<k)
    n=len(masks)
    bit=np.array([[(int(q)>>a)&1 for q in masks] for a in range(k)])
    @lru_cache(None)
    def leaf(h):
        return h if len(h)==m else leaf(h+(actions[h],))
    def pay(h,a):
        z=leaf(h+(a,)); load=sum(bit[b] for b in z)
        return np.divide(bit[a],load,out=np.zeros(n),where=load>0)
    base=leaf(())
    W=np.minimum(1,sum(bit[a] for a in base))
    rows=[]
    for h,a in actions.items():
        prescribed=pay(h,a)
        for b in range(k):
            if b!=a: rows.append(np.r_[pay(h,b)-prescribed,0])
    frees=[a for a in range(k) if a not in base]
    unions=[np.minimum(1,sum((bit[a] for a in z),start=np.zeros(n)))
            for z in combinations(range(k),min(m,k))]
    for opt in combinations(range(k),min(m,k)):
        O=np.minimum(1,sum(bit[a] for a in opt))
        D=O*(1-W)
        optimum=[np.r_[z-O,0] for z in unions]
        for i in range(m):
            r=m-i
            if r>len(frees): continue
            ui=pay(base[:i],base[i]); ei=ui*(1-O)
            for top in combinations(frees,r):
                covered=D*np.minimum(1,sum(bit[a] for a in top))
                extra=[]
                for small in combinations(frees,r-1):
                    z=D*np.minimum(1,sum((bit[a] for a in small),start=np.zeros(n)))
                    extra.append(np.r_[z-covered,1])
                matrix=np.array(rows+optimum+extra)
                res=linprog(np.r_[ui+ei,-1],A_ub=matrix,
                    b_ub=np.zeros(len(matrix)),A_eq=np.r_[W,0][None,:],
                    b_eq=[1],bounds=[(0,None)]*(n+1),method='highs')
                if res.success and res.fun < -1e-8:
                    out={'candidate':'u_i+e_i >= f_D(r)-f_D(r-1)',
                         'identity':'new strong sufficient bridge, not HALF',
                         'strategy_source':name,'m':m,'k':k,'path':base,
                         'optimal_topics':opt,'bad_position':i+1,'top':top,
                         'floating_violation':-res.fun,
                         'weights':{str(q):float(w) for q,w in zip(masks,res.x[:-1]) if w>1e-8},
                         'd':float(res.x[-1]),
                         'actions':[{'history':h,'action':a} for h,a in actions.items()]}
                    Path(__file__).with_name('refund_floor_floating.json').write_text(json.dumps(out,indent=2))
                    print(json.dumps(out,indent=2)); return True
    print(name,': no positive witness in this fixed cone; no inference')
    return False

if __name__=='__main__':
    actions={():0,**{(i,):a for i,a in enumerate([1,4,4,4,5,4])}}
    if attack(2,6,actions,'known 71-customer response graph'):sys.exit()
    for name in ['individual_security_failure','prefix_balance_failure','root_tax_failure']:
        obj=json.loads((ROOT/f'evidence/certificates/customer_attraction/{name}.json').read_text())
        strategy=obj.get('strategy',obj)
        inst=json.loads((ROOT/f'examples/customer_attraction/{name}.json').read_text())
        ad={tuple(x['history']):x['action'] for x in strategy['actions']}
        k=max([*ad.values(),*(a for h in ad for a in h)])+1;m=max(map(len,ad))+1
        if attack(m,k,ad,name):break
