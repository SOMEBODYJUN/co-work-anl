"""Targeted exact attack on the old path/Hamming/tail-depth obstruction family.
All new outputs stay outside the repository until the run completes.
"""
import json,math,sys,time
from fractions import Fraction as F
from pathlib import Path
REPO=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(REPO))
sys.path.insert(0,str(REPO/'research/workspaces/customer-attraction/R-977d3dbff13346b3b7c0f5a4caa6168e/background'))
from customer_attraction.model import Instance,CustomerType
from interval_ceiling_dp import IntervalCeilingFloor,MaterializedInterval

def instance(m,k,h):
 n=m-k;d=n-h;L=math.lcm(*range(1,d+1))
 sizes=[L//max(n-i-h+1,1) for i in range(1,n+1)]+[L]*m
 ins=Instance(tuple(['A'+str(i) for i in range(1,n+1)]+['B'+str(i) for i in range(1,m+1)]),tuple(CustomerType(frozenset({i}),s) for i,s in enumerate(sizes)),m)
 return ins,sizes,L,d

def one(m,k,h,explicit=False):
 start=time.time();ins,sizes,L,d=instance(m,k,h);dp=IntervalCeilingFloor(ins);G=dp.root();q=ins.topic_count
 lo,hi=dp.bounds((0,)*q)
 checked=0
 for b,l in dp.level.items():
  assert l==L,(m,k,h,b,l,L)
  expected=tuple(a for a in range(q) if b[a]==0 and sizes[a]==L)
  assert dp.allowed[b]==expected,(m,k,h,b,dp.allowed[b],expected)
  checked+=1
 assert G==m*L
 if explicit:
  ref=MaterializedInterval(ins);H=ref.terminals((0,)*q)
  expected_count=math.comb(sum(s==L for s in sizes),m)
  assert len(H)==expected_count
  for z in H:
   assert all(z[a] in [0,1] and (not z[a] or sizes[a]==L) for a in range(q))
  for b in ref.level:
   assert ref.level[b]==dp.level[b] and ref.allowed[b]==dp.allowed[b]
 W=sum(sizes[:m-k])+k*L
 ans={'m':m,'tail_depth':k,'hamming_radius':h,'d':d,'q':q,'L':L,'unit_customers':sum(sizes),'sizes':sizes,'old_path_W':W,'OPT':m*L,'old_path_half_violation':W*2<m*L,'interval_G':str(G),'interval_root_L':str(dp.level[(0,)*q]),'interval_root_E':[ins.topics[a] for a in dp.allowed[(0,)*q]],'all_nonterminal_states_checked':checked,'explicit_H_compared':explicit,'elapsed_seconds':time.time()-start}
 return ans

if __name__=='__main__':
 out=[]
 for m in range(2,6):
  for k in range(1,m):
   for h in range(m-k):
    out.append(one(m,k,h,explicit=m<=4))
 print('small_done',len(out),sum(r['all_nonterminal_states_checked'] for r in out),flush=True)
 out.append(one(7,1,0))
 print('first_old_half_failure',json.dumps(out[-1]),flush=True)
 ans={'status':'exact targeted family audit; no SPE or general-half counterexample','small_parameters':'all 2<=m<=5, 1<=k<m, 0<=h<m-k','small_instances':len(out)-1,'total_nonterminal_states_checked':sum(r['all_nonterminal_states_checked'] for r in out),'results':out}
 Path(__file__).with_name('interval_tail_family_audit.json').write_text(json.dumps(ans,indent=2)+'\n')
