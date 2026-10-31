#!/usr/bin/env python3
"""Independent bounded BNS/AP formula checks, not original eight-certificate audit.
The two old fixtures' full SPE validity is reused from DG; only new weighted
rows are evaluated here. One 3-customer control has 14 new IC comparisons.
"""
import json,hashlib,pathlib,re
from fractions import Fraction as F
from itertools import product
E=pathlib.Path(__file__).resolve().parent;C=E/'comparison'
def old(name):
 inp=json.loads((C/'examples/customer_attraction'/f'{name}.json').read_text());ce=json.loads((C/'evidence/certificates/customer_attraction'/f'{name}.json').read_text());return inp,ce['strategy'],'DG old IC success reused; no new IC enumeration'
def check(inp,strategy,mode):
 p=len(inp['topics']);m=inp['players'];clients=[frozenset(r['topics']) for r in inp['customers'] for _ in range(r['multiplicity'])];sig={tuple(r['history']):r['action'] for r in strategy['actions']};expected={h for d in range(m) for h in product(range(p),repeat=d)};assert set(sig)==expected
 def terminal(h):
  while len(h)<m:h=h+(sig[h],)
  return h
 def pay(z,i):return sum((F(1,sum(a in B for a in z)) for B in clients if z[i] in B),F(0))
 newic=0
 if mode=='new control':
  for h in expected:
   z=terminal(h);u=pay(z,len(h))
   for a in range(p):assert u>=pay(terminal(h+(a,)),len(h));newic+=1
 else:
  data=json.loads((E/'reused-DG-check/result.json').read_text());g=next(x for x in data['games'] if x['customers']==len(clients));assert g['complete_policy']==[dict(history=list(h),action=sig[h]) for h in sorted(expected,key=lambda h:(len(h),h))] and g['IC_minimum']=='0' and g['comparisons']==258
 sizes=[];ap=bn=empty=0;min_ap1=min_ap2=min_b1=min_b2=None;strict=[]
 for h in sorted(expected,key=lambda h:(len(h),h)):
  k=m-len(h)
  if k<2:continue
  b=[sum(a in B for a in h) for B in clients];w=[F(1,bx+k) for bx in b];u=pay(terminal(h),len(h));M=k+max(b,default=0);s=[sum((wx for B,wx in zip(clients,w) if a in B),F(0)) for a in range(p)];K=max(s)
  for a in range(p):
   MC=k+max((bx for B,bx in zip(clients,b) if a in B),default=0);assert MC<=M and MC>=k;e=u-s[a];assert e>=0
   for d in range(p):
    lhs=sum((F(1,bx+k) if a in B else F(1,bx+1) for B,bx in zip(clients,b) if d in B),F(0));r1=s[a]+((k-1)*(M-1)+F(k*k,2))*e;r2=s[a]+((k-1)*(MC-1)+F(k*k,2))*e;assert lhs<=r2<=r1;ap+=1;min_ap1=r1-lhs if min_ap1 is None else min(min_ap1,r1-lhs);min_ap2=r2-lhs if min_ap2 is None else min(min_ap2,r2-lhs)
    if MC<M and r2<r1:strict.append(dict(history=list(h),C=a,D=d,k=k,M=M,MC=MC,e=str(e),v1_rhs=str(r1),v2_rhs=str(r2)))
    if s[a]==K:
     b1=K+(k-1)*(M-1)*(u-K);b2=K+(k-1)*(MC-1)*(u-K);assert lhs<=b2<=b1;bn+=1;min_b1=b1-lhs if min_b1 is None else min(min_b1,b1-lhs);min_b2=b2-lhs if min_b2 is None else min(min_b2,b2-lhs)
  # C=empty direct formula, without adding a new empty label or asserting its SPE.
  MC=k;coef=(k-1)*(MC-1)+F(k*k,2);assert coef>=k
  for d in range(p):
   lhs=sum((F(1,bx+1) for B,bx in zip(clients,b) if d in B),F(0));assert lhs<=k*s[d]<=k*u<=coef*u;empty+=1
 return dict(customers=len(clients),players=m,topics=p,policy=[dict(history=list(h),action=sig[h]) for h in sorted(expected,key=lambda h:(len(h),h))],mode=mode,new_IC_comparisons=newic,AP_pairs_each_version=ap,BNS_pairs_each_version=bn,empty_C_direct_rows=empty,min_AP_v1_slack=str(min_ap1),min_AP_v2_slack=str(min_ap2),min_BNS_v1_slack=str(min_b1),min_BNS_v2_slack=str(min_b2),strict_MC_examples=strict)
def main():
 games=[check(*old(n)) for n in ['individual_security_failure','aggregate_theta_failure']]
 control=dict(players=3,topics=['A','B'],customers=[dict(topics=[0],multiplicity=2),dict(topics=[1],multiplicity=1)]);sig={():0,(0,):0,(1,):0,(0,0):1,(0,1):0,(1,0):0,(1,1):0};strategy=dict(actions=[dict(history=list(h),action=a) for h,a in sig.items()]);g=check(control,strategy,'new control');assert g['new_IC_comparisons']==14 and g['strict_MC_examples'];games.append(g)
 scalar=0
 for b in [0,1,2,10,10**40]:
  for k in range(2,9):
   assert k*(b+1)*(b+2)-2*(b+k)==b*(k*b+3*k-2)>=0
   for z in range(0,k):
    diff=F(1,b+z+1)-F(1,b+1)+F(z,(b+1)*(b+2));assert diff==F(z*(z-1),(b+1)*(b+2)*(b+z+1))>=0;scalar+=1
 assert [F((k-1)*4)+F(k*k,2) for k in [5,4,3,2]]==[F(57,2),F(20),F(25,2),F(6)]
 inv=json.loads((E/'primary-inventory.json').read_text());claims=next(r for r in inv if r['id']=='577c036ceeac0040c7e9');text=(E.parents[3]/claims['preserved_repo_path']).read_text() if False else (E/'original'/claims['path']).read_text();fracs=[F(int(a),int(b)) for a,b in re.findall(r'(\d{20,})/(\d{20,})',text)];assert len(fracs)==2 and all(v>2 for v in fracs)
 out=dict(status='PASS',scope=__doc__,games=games,new_control_input=control,new_control_strategy=strategy,scalar_kernel_cases=scalar,reported_projection_fractions_arithmetic=[dict(value=str(v),excess_over_two=str(v-2)) for v in fracs],projection_feasibility='NOT checked: original supports/rows/programs absent; rational value>2 alone does not certify a feasible point',original_program_runs=0,reused_DG_new_runs=0,helper_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest());pathlib.Path('result.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('PASS: new BNS/AP v1/v2 weighted rows, empty-C direct inequalities, strict MC control and scalar kernels; no 1867-row feasibility or original audit claim.')
if __name__=='__main__':main()
