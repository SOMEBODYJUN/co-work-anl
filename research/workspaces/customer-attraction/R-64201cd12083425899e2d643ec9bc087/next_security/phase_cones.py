"""Screen all two-group phase strings, including two early same-group actors.
Only numerical candidate generation; all ordered-history rows are retained.
"""
from pathlib import Path
import argparse,importlib.util,json,sys,time
sys.dont_write_bytecode=True
import numpy as np
from scipy.optimize import linprog
spec=importlib.util.spec_from_file_location('pa',Path(__file__).with_name('pair_attack.py'));pa=importlib.util.module_from_spec(spec);spec.loader.exec_module(pa)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=4);ap.add_argument('--k',type=int,default=8);ap.add_argument('--iterations',type=int,default=16);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    s=pa.residual_space(a.n,a.k,());groups=(tuple(range(a.k//2)),tuple(range(a.k//2,a.k)));gi={x:i for i,G in enumerate(groups) for x in G};rng=np.random.default_rng(8976027);best=None;done=[];started=time.time()
    for ref in ('first','last'):
      for bits in range(1<<(a.n-1)):
       for pick in ('fresh','cycle','repeat'):
        def action(h):
            if not h:return 0
            d=len(h);g=gi[h[0] if ref=='first' else h[-1]] ^ ((bits>>(d-1))&1);G=groups[g]
            if pick=='fresh':return min(G,key=lambda x:(h.count(x),x))
            if pick=='cycle':return G[sum(gi[x]==g for x in h)%len(G)]
            return G[0]
        cone=s.full_policy({h:action(h) for h in s.histories});G=cone['gamma']/s.L;bounds=[(0,None)]*s.k;bounds[-1]=(0,0)
        extreme=linprog(rng.normal(size=s.k),A_ub=-G,b_ub=np.zeros(len(G)),A_eq=[np.ones(s.k)],b_eq=[1],bounds=bounds,method='highs')
        if not extreme.success:
            done.append(dict(ref=ref,bits=bits,pick=pick,feasible_without_universal=False));continue
        path=[]
        for _ in range(a.n):path.append(action(tuple(path)))
        ans=pa.attack(s,cone,tuple(path[:2]),extreme.x,rng,a.iterations)
        done.append(dict(ref=ref,bits=bits,pick=pick,path=path,gap=ans['gap']))
        if best is None or ans['gap']<best['gap']-1e-10:
            best=ans;best['phase']=done[-1];print(json.dumps(dict(phase=done[-1],elapsed=time.time()-started)),flush=True)
        if ans['gap'] < -1e-8:break
       if best and best['gap'] < -1e-8:break
      if best and best['gap'] < -1e-8:break
    a.output.write_text(json.dumps(dict(status='numerical screening only',n=a.n,k=a.k,completed=len(done),elapsed=time.time()-started,phases=done,best=best),indent=2)+'\n')

if __name__=='__main__':main()
