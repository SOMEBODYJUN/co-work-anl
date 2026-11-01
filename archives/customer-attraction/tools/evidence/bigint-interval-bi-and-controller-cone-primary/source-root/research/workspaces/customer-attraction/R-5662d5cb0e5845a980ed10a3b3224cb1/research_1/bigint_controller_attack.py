"""Exact big-integer interval BI plus history-dependent controller cone attack.

Payoff lower bounds use exact floor rounding to a 10^12 grid. Comparisons whose
integer intervals overlap are resolved by cached Python-bigint dot products;
all BI comparisons are exact. The later cone LP remains discovery only.
"""
from full18_cone_attack import Attack,HERE
from fractions import Fraction as F
import argparse,json,time,numpy as np

class ExactPayoffs:
 def __init__(self,C,weights):
  self.C=C;self.w=list(map(int,weights));total=sum(self.w);scale=10**12
  low=np.array([v*scale//total for v in self.w],dtype=np.int64)
  inc=C.inc.astype(np.int64);self.L=np.empty((len(C.term),C.k),dtype=np.int64);self.E=np.empty_like(self.L)
  for start in range(0,len(C.term),2048):
   inv=C.inv[start:start+2048].astype(np.int64);self.L[start:start+2048]=(inv*low[None,:])@inc;self.E[start:start+2048]=inv@inc
  self.cache={};self.action_indices=[np.flatnonzero(C.inc[:,a]).tolist() for a in range(C.k)]
  assert 60*sum(map(int,low))<2**63
 def val(self,t,a):
  key=(int(t),int(a));v=self.cache.get(key)
  if v is None:
   v=sum(int(self.C.inv[t,j])*self.w[j] for j in self.action_indices[a]);self.cache[key]=v
  return v
 def cmp(self,t,a,s,b):
  if self.L[t,a]>self.L[s,b]+self.E[s,b]:return 1
  if self.L[t,a]+self.E[t,a]<self.L[s,b]:return -1
  aa=self.val(t,a);bb=self.val(s,b);return (aa>bb)-(aa<bb)
 def argmin(self,ts,a):
  limit=np.min(self.L[ts,a]+self.E[ts,a]);cand=ts[self.L[ts,a]<=limit]
  if len(cand)==1:return int(cand[0])
  return int(min(cand,key=lambda t:self.val(t,a)))
 def minima(self,ts,a,chosen):
  lo=self.L[chosen,a];hi=lo+self.E[chosen,a];cand=ts[(self.L[ts,a]<=hi)&(self.L[ts,a]+self.E[ts,a]>=lo)]
  return [int(t) for t in cand if self.cmp(t,a,chosen,a)==0]

def solve(C,P):
 out=[None]*7;out[6]=[np.array([i],dtype=np.int32) for i in range(len(C.term))];mins=[None]*6;floor=[None]*6
 for r in range(5,-1,-1):
  cur=[];mn=[];fl=[]
  for ids in C.child[r]:
   children=[out[r+1][j] for j in ids];mt=np.array([P.argmin(child,a) for a,child in enumerate(children)],dtype=np.int32)
   lo=np.array([P.L[t,a] for a,t in enumerate(mt)]);up=np.array([P.L[t,a]+P.E[t,a] for a,t in enumerate(mt)]);cand=np.flatnonzero(up>=lo.max())
   a=int(cand[0])
   for b in cand[1:]:
    if P.cmp(mt[b],int(b),mt[a],a)>0:a=int(b)
   ft=int(mt[a]);vals=[]
   for b,child in enumerate(children):vals.extend(int(t) for t in child if P.cmp(int(t),b,ft,a)>=0)
   accepted=np.unique(np.array(vals,dtype=np.int32));assert len(accepted);cur.append(accepted);mn.append(mt);fl.append((ft,a))
  out[r]=cur;mins[r]=np.array(mn);floor[r]=fl
  print('EXACT_DEPTH',r,'retained',sum(map(len,cur)),'max',max(map(len,cur)),'cached_exact_payoffs',len(P.cache),flush=True)
 return out,mins,floor

def controller(C,P,W,out,mins,floor,target,rng):
 current={(0,int(target))};keys=[];policy=[];sizes=[]
 for r in range(6):
  nxt=set();lv=[]
  for q,t in sorted(current):
   ids=C.child[r][q];ft,fa=floor[r][q];adm=[a for a,j in enumerate(ids) if t in out[r+1][j] and P.cmp(t,a,ft,fa)>=0];assert adm;a=int(rng.choice(adm));dest=[]
   for b,j in enumerate(ids):
    if b==a:tb=t
    else:
     cand=P.minima(out[r+1][j],b,int(mins[r][q,b]));assert cand
     if rng.random()<.7:
      wm=min(W[z] for z in cand);cand=[z for z in cand if W[z]==wm]
     tb=int(rng.choice(cand));keys.append((t,a,tb,b))
    dest.append(tb)
    if r<5:nxt.add((int(j),tb))
    else:assert int(j)==tb
   lv.append((q,t,a,dest))
  policy.append(lv);sizes.append(len(current));current=nxt
  print('CONTROLLER',r,sizes[-1],flush=True)
 return np.unique(np.array(keys,dtype=np.int32),axis=0),policy,sizes

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',type=str,default='full18_vertex_seed.json');ap.add_argument('--prefix',type=str,default='bigint_controller');ap.add_argument('--trials',type=int,default=8);ap.add_argument('--seed',type=int,default=664193);a=ap.parse_args();start=time.time();rng=np.random.default_rng(a.seed)
 seed=json.loads((HERE/a.input).read_text());C=Attack(seed);weights=[q['multiplicity'] for q in seed['customers']];P=ExactPayoffs(C,weights);out,mins,floor=solve(C,P)
 W=[sum(v for v,c in zip(weights,row) if c) for row in C.cover];optvals=[sum(v for v,c in zip(weights,row) if c) for row in C.opts];opt=max(optvals);worst=int(min(out[0][0],key=lambda t:W[t]));ratio=F(opt,W[worst]);print('EXACT_ROOT',len(out[0][0]),'ratio',str(ratio),float(ratio),'seconds',time.time()-start,flush=True)
 records=[];best=0
 for trial in range(a.trials):
  target=worst if trial%3==0 else int(rng.choice(out[0][0]));keys,pol,sizes=controller(C,P,W,out,mins,floor,target,rng);ans,oid,root,nc,nr,viol=C.optimize(None,[np.array([target])],keys,C.initial,rng)
  if ans is None or not ans.success:print('FAIL',trial,None if ans is None else ans.message,flush=True);continue
  v=float(C.opts[oid]@ans.x);rec={'trial':trial,'ratio':v,'nodes_by_depth':sizes,'IC_keys':len(keys),'maximum_float_IC_violation':viol,'seconds':time.time()-start};records.append(rec);print('TRIAL',json.dumps(rec),flush=True)
  if v>best+1e-8:
   best=v;(HERE/(a.prefix+'_best_float.json')).write_text(json.dumps({'status':'float full-history controller cone candidate, exact recovery required','support_customers':C.cust,'weights':ans.x.tolist(),'comparison':C.opt_supports[oid],'ratio':v,'terminal_counts':C.term[target].tolist(),'policy_by_depth':pol,'discovery':rec},indent=2)+'\n')
  if v>2+1e-6:print('STRICT_TARGET_CANDIDATE',flush=True);break
 (HERE/(a.prefix+'_report.json')).write_text(json.dumps({'status':'targeted finite BI and controller discovery only','exact_input_root_outcome_count':len(out[0][0]),'exact_input_worst_ratio':str(ratio),'best_floating_cone_ratio':best,'trials':records},indent=2)+'\n');print('END',best,'seconds',time.time()-start,flush=True)
if __name__=='__main__':main()
