"""Discovery: all local client types for one true root-max branch and last BR.
Floating LP is not a proof; feasible kernels are not SPE certificates.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

def build(k=5,mode='last'):
    types=[b for b in product((0,1),repeat=k+1) if any(b)]
    csize=np.array([b[0] for b in types],dtype=float)
    root=np.array([b[0]/(b[0]+sum(b[2:])) if b[0] else 0 for b in types])
    target=np.array([b[1]/(k if b[0] else 1) for b in types],dtype=float)
    rows=[]; names=[]
    for q in range(1,k+1):
        rows.append(np.array([b[q]-b[0] for b in types],dtype=float))
        names.append(f'size_{q}<=size_C')
    last=np.array([b[-1]/(b[0]+sum(b[2:])) if b[-1] else 0 for b in types])
    for q in range(k):
        dev=np.array([b[q]/(b[0]+sum(b[2:-1])+1) if b[q] else 0 for b in types])
        rows.append(dev-last); names.append(f'last_BR_{q}')
    if mode!='last':
        actions=[0]+list(range(2,k+1))
        for j in range(1,k-1):
            prefix=actions[:j]; rem=k-j; cur=actions[j]
            profit=np.array([b[cur]/sum(b[q] for q in actions) if b[cur] else 0 for b in types])
            for q in range(k+1):
                guar=np.array([b[q]/(sum(b[a] for a in prefix)+rem) for b in types])
                rows.append(guar-profit); names.append(f'node{j+1}_floor_{q}')
        if mode=='tail':
            for rem,beta in ((3,F(5,3)),(4,F(1499,750))):
                prefix=actions[:k-rem]; tail=actions[k-rem:]
                actual=np.array([sum(b[a] for a in tail)/sum(b[a] for a in actions) if any(b[a] for a in tail) else 0 for b in types])
                for qs in combinations_with_replacement(range(k+1),rem):
                    comp=np.array([sum(b[q] for q in qs)/(sum(b[a] for a in prefix)+sum(b[q] for q in qs)) if any(b[q] for q in qs) else 0 for b in types])
                    rows.append(comp-float(beta)*actual); names.append(f'tail{rem}_profit_{qs}')
    return types,csize,root,target,rows,names

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--mode',choices=('last','node','tail'),default='last'); args=parser.parse_args()
    types,csize,root,target,rows,names=build(mode=args.mode)
    out={'status':'floating_discovery_only','k':5,'mode':args.mode,'types':len(types),'rows':len(rows),'points':[]}
    for ratio in (F(1,5),F(21,100),F(11,50),F(6,25),F(1,4),F(3,10),F(1,3),F(2,5)):
        z=linprog(-target,A_ub=np.array(rows+[root]),b_ub=[0.]*len(rows)+[float(ratio)],A_eq=[csize],b_eq=[1.],bounds=(0,None),method='highs')
        q={'root_cap':str(ratio),'success':bool(z.success),'message':z.message}
        if z.success:
            q.update({'F':float(-z.fun),'dual_root':float(-z.ineqlin.marginals[-1]),'dual_C':float(-z.eqlin.marginals[0]),'active_multipliers':{n:float(-v) for n,v in zip(names,z.ineqlin.marginals[:-1]) if abs(v)>1e-9},'support':[{'bits':''.join(map(str,types[i])),'mass':float(v)} for i,v in enumerate(z.x) if v>1e-9]})
        out['points'].append(q)
    path=Path(__file__).with_suffix('.json') if args.mode=='last' else Path(__file__).with_name('max_theme_local_envelope_'+args.mode+'.json')
    with path.open('x') as f: json.dump(out,f,indent=2)
    print(json.dumps({'path':str(path),'points':[{k:v for k,v in q.items() if k not in ('support','active_multipliers','message')} for q in out['points']]},indent=2))
if __name__=='__main__': main()
