"""Exact set-valued BI of one targeted 18-label integer-customer seed.

The recurrence is the canonical ExactSPESolver recurrence, with common share
scale 60 and int64 arithmetic after explicit no-overflow bounds. This computes
all history-dependent pure SPE terminal counts, not only count selectors.
No failed finite seed test is evidence for the universal conjecture.
"""
from full18_cone_attack import Attack,HERE
from fractions import Fraction as F
import json,time,numpy as np
start=time.time();seed=json.loads((HERE.parent/'research_6/seed_full18.json').read_text());C=Attack(seed)
w=np.array([q['multiplicity'] for q in seed['customers']],dtype=np.int64)
assert int(w.sum())*60<2**63
U=(C.inv.astype(np.int64)*w[None,:])@C.inc.astype(np.int64)
W=C.cover.astype(np.int64)@w
optvals=C.opts.astype(np.int64)@w;opt=int(optvals.max());optid=int(optvals.argmax())
out=[None]*(C.m+1);out[-1]=[np.array([j],dtype=np.int32) for j in range(len(C.term))]
stats=[]
for r in range(C.m-1,-1,-1):
 cur=[];largest=0;ret=0
 for ids in C.child[r]:
  children=[out[r+1][j] for j in ids]
  floor=max(int(U[child,a].min()) for a,child in enumerate(children))
  accepted=[child[U[child,a]>=floor] for a,child in enumerate(children)]
  vals=np.unique(np.concatenate(accepted));assert len(vals)
  cur.append(vals);largest=max(largest,len(vals));ret+=len(vals)
 out[r]=cur;rec={'depth':r,'states':len(cur),'retained':ret,'largest_set':largest,'seconds':time.time()-start};stats.append(rec);print(rec,flush=True)
root=out[0][0];worst=int(root[np.argmin(W[root])]);value=F(opt,int(W[worst]))
report={'status':'one finite targeted instance, full exact set-valued SPE BI','topics':len(seed['topics']),'customer_types':len(seed['customers']),'count_states':sum(len(x) for x in C.levels),'terminal_states':len(C.term),'root_outcome_count':len(root),'minimum_SPE_welfare':int(W[worst]),'OPT6':opt,'ratio':str(value),'strict_target_counterexample':value>2,'worst_terminal_counts':C.term[worst].tolist(),'optimum_support':C.opt_supports[optid],'stages':stats,'share_scale':60,'arithmetic':'int64 exact; 60*total_customer_count <2^63 checked'}
(HERE/'full18_exact_bi.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
