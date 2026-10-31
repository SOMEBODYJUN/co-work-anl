"""Full literal-domain column generation for max-root same-source requery.

Only a discovery program. Reduced-cost separation visits every expanded
customer membership type. Neither numeric feasibility nor a type point is
a game/SPE counterexample.
"""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
PATHS=['TABCDE','TEFGHI','TAEJKL','TABEMN','TIUVWX']
FIRST=[1,2,3,4,2]
COPIES=[(0,1,1),(0,2,2),(0,3,3),(0,1,4)]
NAMES=''.join(dict.fromkeys(''.join(PATHS)))


def raw(codes):
    b={a:((codes>>i)&1).astype(float) for i,a in enumerate(NAMES)}
    def load(path):return sum((b[a] for a in path),np.zeros(len(codes)))
    def sh(n,d):return np.divide(n,d,out=np.zeros_like(d),where=n!=0)
    def pay(path,i):return sh(b[path[i]],load(path))
    rows=[]; labels=[]; typ=[]
    def add(label,v,rhs=0):labels.append(label);rows.append(v);typ.append(rhs)
    for a in NAMES:
        if a!='T':add('CAP:'+a,b[a],1)
    for src,i,dst in COPIES:
        add(f'COPY:{src}:{i}:{dst}',pay(PATHS[dst],i)-pay(PATHS[src],i))
    for tag,path in enumerate(PATHS):
        first=FIRST[tag]
        for i in range(first,6):
            p=load(path[:i])
            for q in NAMES:add(f'SAFE:{tag}:{i}:{q}',sh(b[q],p+6-i)-pay(path,i))
        p=load(path[:5])
        add(f'LASTO:{tag}',-6*pay(path,5)-p/(p+1),-1)
        if first<=4:
            p=load(path[:4]);h=pay(path,4)+pay(path,5)+b[path[4]]/((p+1)*(p+2))
            add(f'PAIRO:{tag}',-3*h-p/(p+1),-1)
    return np.array(rows),np.array(typ),b['T'],pay(PATHS[0],0),labels


def main():
    global PATHS,FIRST,COPIES,NAMES
    p=argparse.ArgumentParser();p.add_argument('--o',type=float,default=4.2)
    p.add_argument('--variant',choices=['second_I','third_L','third_I','branch_D','baseline','I_L','L_D'],default='second_I')
    p.add_argument('--max-iterations',type=int,default=100);args=p.parse_args()
    if args.variant!='second_I':
        PATHS=PATHS[:4];FIRST=FIRST[:4];COPIES=COPIES[:3]
        if args.variant=='third_L':
            PATHS+=['TALUVW'];FIRST+=[3];COPIES+=[(0,2,4)]
        elif args.variant=='third_I':
            PATHS+=['TAIUVW'];FIRST+=[3];COPIES+=[(0,2,4)]
        elif args.variant=='branch_D':
            PATHS+=['TEDUVW'];FIRST+=[3];COPIES+=[(1,2,4)]
        elif args.variant=='I_L':
            PATHS+=['TIUVWX','TALYZQ'];FIRST+=[2,3];COPIES+=[(0,1,4),(0,2,5)]
        elif args.variant=='L_D':
            PATHS+=['TALUVW','TEDXYZ'];FIRST+=[3,3];COPIES+=[(0,2,4),(1,2,5)]
        NAMES=''.join(dict.fromkeys(''.join(PATHS)))
    rng=np.random.default_rng(31971)
    initial=np.r_[np.arange(1,1<<12,dtype=np.uint32),
                  rng.integers(1,1<<len(NAMES),size=12000,dtype=np.uint32),
                  np.arange((1<<len(NAMES))-1024,1<<len(NAMES),dtype=np.uint32)]
    codes=np.unique(initial)
    record=[]
    for it in range(args.max_iterations):
        A,typ,E,c,labels=raw(codes)
        rhs=np.where(typ==1,1,np.where(typ==-1,-args.o,0))
        out=linprog(c,A_ub=A,b_ub=rhs,A_eq=E[None,:],b_eq=[1],bounds=(0,None),method='highs')
        if not out.success: print(out.message,flush=True);break
        y=out.ineqlin.marginals;z=float(out.eqlin.marginals[0])
        negative=[];low=0
        for start in range(1,1<<len(NAMES),32768):
            batch=np.arange(start,min(start+32768,1<<len(NAMES)),dtype=np.uint32)
            B,_,EE,cc,_=raw(batch)
            reduced=cc-y@B-z*EE
            low=min(low,float(reduced.min()))
            select=np.flatnonzero(reduced < -1e-8)
            if len(select):
                # Keep 64 extreme columns per batch, then globally 512.
                idx=select[np.argsort(reduced[select])[:64]]
                negative.extend(zip(reduced[idx].tolist(),batch[idx].tolist()))
        item={'iteration':it,'types':len(codes),'r_over_K':out.fun,'min_reduced_cost':low}
        print(json.dumps(item),flush=True);record.append(item)
        if low>=-1e-8:
            result={'evidence':'floating full-literal-domain necessary-row LP only',
                    'paths':PATHS,'first_genuine':FIRST,'copy_edges':COPIES,
                    'names':NAMES,'O_over_K':args.o,'trace':record,
                    'active_dual':{k:float(-v) for k,v in zip(labels,y) if abs(v)>1e-9},
                    'eq_dual':z,
                    'primal':{str(int(q)):float(v) for q,v in zip(codes,out.x) if v>1e-9}}
            (HERE/f'root_requery_{args.variant}_o{args.o:g}.json').write_text(json.dumps(result,indent=2))
            break
        new=[q for _,q in sorted(negative)[:512]]
        codes=np.unique(np.r_[codes,np.array(new,dtype=np.uint32)])


if __name__=='__main__':main()
