"""NEW exact definition check reconstructed from the complete MD strategy.

The missing original fixed_rank_obstruction.py is NOT imported or executed.
Only stdlib Fractions, all constrained ordered nodes, and true completions.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from math import comb,lcm
import hashlib,json
E=Path(__file__).resolve().parent
source=E/'original/research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_tree/fixed_rank_proof.md'
def make(m,k):
 M=2**k;D=(m+M-1)//M;L=lcm(*range(1,D+1));den=[(m-i+M-1)//M for i in range(m)]+[1]*m
 sizes=[L//d for d in den];assert all(L%d==0 for d in den)
 @lru_cache(None)
 def state(h):
  plan=tuple(range(m));rank=0
  for pos,T in enumerate(h):
   if T==plan[pos]:continue
   rank+=1;past=h[:pos];r=m-pos;p=past.count(T);d=den[T]
   if rank<=k:
    a=2**(k-rank);q=max(p+1,(r+p+1)//(a*d+1));copies=q-p
    assert 1<=copies<=r
    fresh=tuple(B for B in range(m,2*m) if B not in past and B!=T)
    assert len(fresh)>=r-copies
    plan=past+(T,)*copies+fresh[:r-copies]
   else:plan=past+(T,)*r
  assert len(plan)==m and plan[:len(h)]==h
  return rank,plan
 return M,L,sizes,state
def enc(v):
 if isinstance(v,F):return str(v)
 if isinstance(v,dict):return {str(k):enc(x) for k,x in v.items()}
 if isinstance(v,(tuple,list)):return [enc(x) for x in v]
 return v
cases=[]
for m,k in [(5,0),(9,1),(6,2),(3,3)]:
 M,L,sizes,state=make(m,k);queue=[()];cursor=0;checks=nonself=zeros=0;minimum=None;digest=hashlib.sha256();bydepth=[0]*m
 while cursor<len(queue):
  h=queue[cursor];cursor+=1;rank,z=state(h);assert rank<=k;bydepth[len(h)]+=1
  a=z[len(h)];own=F(sizes[a],z.count(a))
  for b in range(2*m):
   child=h+(b,);newrank,zz=state(child);val=F(sizes[b],zz.count(b));slack=own-val
   assert slack>=0,(m,k,h,rank,a,b,own,val,z,zz)
   checks+=1;nonself+=b!=a;zeros+=slack==0;minimum=slack if minimum is None else min(minimum,slack)
   digest.update((json.dumps(enc([h,rank,a,b,z,zz,own,val,slack]),separators=(',',':'))+'\n').encode())
   if len(child)<m and newrank<=k:queue.append(child)
 expected_bydepth=[sum(comb(d,j)*(2*m-1)**j for j in range(min(k,d)+1)) for d in range(m)]
 assert bydepth==expected_bydepth and checks==len(queue)*2*m and nonself==len(queue)*(2*m-1)
 W=sum(sizes[:m]);OPT=m*L;assert F(W,L)==sum((F(1,(r+M-1)//M) for r in range(1,m+1)),F(0))
 cases.append({'m':m,'cutoff':k,'M':M,'L':L,'topic_sizes':sizes,'actual_path':list(range(m)),
  'W':W,'OPT':OPT,'OPT_minus_2W':OPT-2*W,'constrained_ordered_nodes':len(queue),
  'nodes_by_depth':bydepth,'including_self_comparisons':checks,'nonself_comparisons':nonself,
  'zero_comparisons':zeros,'minimum_slack':minimum,'comparison_rows_serialization_sha256':digest.hexdigest(),
  'rank_is_number_of_true_deviations_from_current_history_prescription':True,'full_SPE_claimed':k>=m-1})
parameter_checks=second_checks=0
for a in [1,2,4,8]:
 for d in range(1,9):
  for r in range(1,33):
   for p in range(7):
    q=max(p+1,(r+p+1)//(a*d+1));assert p+1<=q<=p+r and d*q>=(r+2*a-1)//(2*a)
    parameter_checks+=1
    if q>p+1:assert r-q+p+1>=a*d*q;second_checks+=1
witnesses=[]
for k in [0,1,2]:
 M=2**k;m0=4*M+(5*M)//18+1;M,L,sizes,state=make(m0,k)
 h=tuple(m0+j for j in range(k+1));rank,z=state(h);assert rank==k+1
 a=z[len(h)];b=m0+k+1;rank2,zz=state(h+(b,));assert rank2==k+2
 prescribed=F(sizes[a],z.count(a));alternative=F(sizes[b],zz.count(b))
 assert prescribed==F(L,m0-k) and alternative==F(L,m0-k-1)>prescribed
 W=sum(sizes[:m0]);assert m0*L>2*W
 witnesses.append({'cutoff':k,'m':m0,'L':L,'history':h,'rank':rank,'prescribed':a,'deviation':b,
  'prescribed_terminal':z,'deviation_terminal':zz,'prescribed_payoff':prescribed,'deviation_payoff':alternative,
  'strict_profit':alternative-prescribed,'W':W,'OPT':m0*L,'OPT_minus_2W':m0*L-2*W})
thresholds=[]
for k in range(9):
 M=2**k;m0=4*M+(5*M)//18+1
 def mass(m):return sum((F(1,(r+M-1)//M) for r in range(1,m+1)),F(0))
 assert m0>2*mass(m0) and m0-1<=2*mass(m0-1)
 thresholds.append({'cutoff':k,'M':M,'first_m_in_this_family':m0})
out={'status':'pass','new_definition_entry_runs':1,'timing_recorded':False,'original_program_runs':0,
 'optimizer_calls':0,'original_program_imported':False,'primary_proof_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'cases':cases,'parameter_lemma_finite_checks':parameter_checks,'last_copy_secondary_checks':second_checks,
 'threshold_examples':thresholds,'unconstrained_strict_deviation_witnesses':witnesses,
 'proof_scope':'Universal cutoff obstruction rests on MD parameter proof, not these finite checks. Formal strategy is not SPE when witness given.'}
(E/'reconstructed-rank-strategy-exact-check.json').write_text(json.dumps(enc(out),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(enc({k:v for k,v in out.items() if k not in ['cases','unconstrained_strict_deviation_witnesses','threshold_examples']})))
for c in cases:print(json.dumps(enc({k:v for k,v in c.items() if k not in ['topic_sizes','actual_path','comparison_rows_serialization_sha256']})))
