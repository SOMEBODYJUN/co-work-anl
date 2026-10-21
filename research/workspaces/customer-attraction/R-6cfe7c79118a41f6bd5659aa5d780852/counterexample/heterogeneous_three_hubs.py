"""Directed inverse design with disjoint optimum petals and three lures.
All floats are proposals; every accepted strategy is expanded and exact verified.
The seed families deliberately vary private-core heterogeneity to escape guard.
"""
from pathlib import Path
import sys,json,random,time,math
from fractions import Fraction as F
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4]
sys.path.insert(0,str(ROOT))
OTHER=ROOT/'research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/counterexample_search'
sys.path.insert(0,str(OTHER))
from cone_walk import Engine
from customer_attraction import Instance,CustomerType,StrategyCertificate,verify_certificate

def main():
    rng=random.Random(6212026);m=5;hubs=3;p=m+hubs
    # Every client belongs to exactly one petal, optionally to a subset of hubs.
    masks=[(1<<(hubs+i))+s for i in range(m) for s in range(1<<hubs)]
    eng=Engine(m,p,rng,masks=masks);seeds=[]
    # Concentrated private mass, then two levels; no random input sweep.
    for large in [2,4,8,16]:
      for partition in [[large,1,1,1,1],[large,large,1,1,1],[large,large,large,1,1]]:
       for orientation in range(3):
        r=np.zeros(len(masks))
        for i,a in enumerate(partition):
          r[i*8]=a
          # Put overlap onto petals with different private sizes.
          r[i*8+(1<<((i+orientation)%3))]=large if i>=2 else 1
          r[i*8+7]=1
        seeds.append(r.tolist())
    # One giant lure with tiny petals gives the exact 2-1/m boundary.
    r=np.zeros(len(masks))
    for i in range(m):r[i*8]=1;r[i*8+1]=m
    seeds.insert(0,r.tolist())
    records=[];best=F(0);seen=set();start=time.monotonic();endpoints=[]
    for step in range(60):
      if seeds:r=seeds.pop(0)
      else:
        r=list(endpoints[step%len(endpoints)])
        # Cross a private/overlap face in one specified petal.
        a=step%len(r);r[a]+=0.02
      target,ratio=eng.solve(r,diverse=step%3!=0)
      actions,G=eng.strategy(target)
      key=G.tobytes()+eng.cov[target].tobytes()
      if key in seen:continue
      seen.add(key)
      # The m petals cover every customer, hence always the exact optimum.
      jid=eng.portfolios.index(tuple(range(hubs,p)))
      ans=eng.optimize(target,G,jid)
      if ans is None:continue
      x,value=ans;endpoints.append(x.tolist())
      rec={'step':step,'input_ratio_proposal':ratio,'optimized_ratio_proposal':value,'root':eng.terminal[target].tolist(),'rows':len(G)};records.append(rec)
      if value>float(best)+1e-9:
        clones=eng.exact_recover(G,target,x)
        if clones is not None:
          inst=Instance(tuple(['B','C','D']+[f'T{i+1}' for i in range(m)]),tuple(CustomerType(frozenset(a for a in range(p) if mask&(1<<a)),n) for mask,n in zip(masks,clones) if n),m)
          cert=StrategyCertificate(dict(actions),tuple(map(int,eng.terminal[target])))
          check=verify_certificate(inst,cert);check.assert_valid()
          exact=F(inst.optimal_welfare(),inst.welfare(cert.terminal_counts))
          if exact>best:
            best=exact
            report={'scope':'One actual finite CAG with all ordered-history actions certified; not a universal bound.','ratio':str(best),'instance':inst.to_dict(),'strategy':cert.to_dict(),'checked_histories':check.checked_histories,'checked_deviations':check.checked_deviations}
            (HERE/'heterogeneous_three_hubs_best.json').write_text(json.dumps(report,indent=2)+'\n')
            print(json.dumps({'step':step,'best_exact':str(best),'root':rec['root'],'elapsed':round(time.monotonic()-start,2)}),flush=True)
      if step%10==0:print(json.dumps({'step':step,'cones':len(seen),'best':str(best),'elapsed':round(time.monotonic()-start,2)}),flush=True)
      if best>2:break
    report={'scope':'Directed finite fixed-policy cone search in disjoint-petal/three-lure catalogs; zero counterexamples is not a theorem.','best_exact_ratio':str(best),'cones':len(seen),'records':records,'elapsed':round(time.monotonic()-start,3)}
    (HERE/'heterogeneous_three_hubs_run.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'best':str(best),'cones':len(seen),'elapsed':report['elapsed']}),flush=True)
if __name__=='__main__':main()
