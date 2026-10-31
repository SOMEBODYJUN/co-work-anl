#!/usr/bin/env python3
"""Independent formula/membership check; no missing original audit imported/run.
Six-group finite checks do not constitute a full SPE or global 1100-row point.
Polynomial arrays below are formal in z=m-3, not interpolation.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement,product
import json,hashlib,pathlib

def family(m):
 X=4*(m-1)**3;Y=2*m*(m-1)*(m-3);Z=m*(m-3)*(m*m-3*m+4);ff=4*(m-3)
 return [(frozenset({0,1}),X),(frozenset({2,3}),X),(frozenset({0,2}),Y),(frozenset({1,3}),Y),(frozenset({0,1,2}),Z),(frozenset({3}),ff)]
def payoff(groups,path,i):return sum((F(n,sum(a in B for a in path)) for B,n in groups if path[i] in B),F(0))
def main():
 rows=[]
 for m in range(3,101):
  groups=family(m);K=sum(n for B,n in groups if 0 in B);branch=(0,)*(m-2)+(1,2);v=payoff(groups,branch,0);p=payoff(groups,branch,m-2);t=payoff(groups,branch,m-1);e=m*v-K;H=3*m*m-7*m+2;cm=F((m-1)**2)-F(m*m*(m-3)**2,2*H)
  assert e==2*H>0 and all(sum(n for B,n in groups if a in B)<=K for a in range(4))
  Q=m*sum(n for B,n in groups if 3 in B and 0 not in B)+sum(n for B,n in groups if 3 in B and 0 in B);assert F(Q-K,e)==cm
  for a in range(4):
   floor=sum((F(n,(m-2)*(0 in B)+2) for B,n in groups if a in B),F(0));assert p>=floor
   alt=branch[:-1]+(a,);assert t>=payoff(groups,alt,m-1)
  assert cm==1+F(m*(m-1),2)+F(m*(m-3)*(m-1)**2,H)
  if m>=4:assert cm<(m-1)**2
  rows.append(dict(m=m,K=K,e=str(e),cm=str(cm),root_branch_payoff=str(v),penultimate_payoff=str(p),terminal_payoff=str(t)))
 # Genuine penultimate deviation D at m4: evaluate every final response from membership.
 groups=family(4);after=(0,0,3);reply=[payoff(groups,after+(a,),3) for a in range(4)];assert reply.index(max(reply))==2 and reply.count(max(reply))==1;dev=payoff(groups,after+(2,),2);assert dev==82 and payoff(groups,(0,0,1,2),2)==68
 # Formal integer polynomial arithmetic in z=m-3.
 def add(*ps):
  if not ps:return [0]
  out=[0]*max(map(len,ps))
  for p in ps:
   for i,v in enumerate(p):out[i]+=v
  while len(out)>1 and out[-1]==0:out.pop()
  return out
 def mul(a,b):
  out=[0]*(len(a)+len(b)-1)
  for i,x in enumerate(a):
   for j,y in enumerate(b):out[i+j]+=x*y
  return out
 def scale(p,c):return [c*x for x in p]
 m=[3,1];mm=[2,1];z=[0,1];X=scale(mul(mul(mm,mm),mm),4);Y=scale(mul(mul(m,mm),z),2);Z=mul(mul(m,z),add(mul(m,m),scale(m,-3),[4]));ff=scale(z,4)
 gs=[({0,1},X),({2,3},X),({0,2},Y),({1,3},Y),({0,1,2},Z),({3},ff)]
 base=add(scale(mul(mul(m,m),add(X,Y)),2),scale(mul(mm,Z),4),scale(add(X,Z),2),mul(mul(m,mm),Y))
 def sf(a):return add(*[mul(scale(m,2) if 0 in B else scale(mul(m,mm),2),N) for B,N in gs if a in B])
 def sg(a,b):return add(*[mul([2] if 0 in B else mul(m,mm),N) for B,N in gs if a in B and b in B])
 expected=[[320,904,984,522,136,14],[320,808,808,402,100,10],[64,264,344,202,56,6],[64,168,204,124,36,4],[320,808,772,360,84,8],[64,168,168,82,20,2],[64,168,168,82,20,2],[64,168,168,82,20,2],[64,72,28,4],[64,120,74,20,2]];polys=[]
 for (a,b),want in zip(combinations_with_replacement(range(4),2),expected):
  coeff=add(base,scale(sf(a),-1),scale(sf(b),-1),sg(a,b));assert coeff==want and all(x>=0 for x in coeff) and coeff[0]>0;polys.append(dict(pair=[a,b],coefficients=coeff))
 # Two-label symmetry examples from the independent orbit review.
 k=(1,0);c=(2,1);cp=(1,2);swap=lambda v:v[::-1];assert swap(c)==cp and c[0]>k[0] and not cp[0]>k[0];assert F(1,c[0])==F(1,2) and F(1,cp[0])==1
 # Complete m2 policy realizes fixed q=(1,1), despite no swap-fixed root action.
 sigma={():0,(0,):1,(1,):0}
 def terminal(h):
  while len(h)<2:h=h+(sigma[h],)
  return h
 comparisons=0
 for depth in range(2):
  for h in product(range(2),repeat=depth):
   out=terminal(h);u=F(1,out.count(out[depth]))
   for action in range(2):assert u>=F(1,terminal(h+(action,)).count(action));comparisons+=1
 assert terminal(())==(0,1) and swap((1,1))==(1,1) and all(a!=1-a for a in range(2))
 result=dict(status='PASS',scope=__doc__,finite_family_cases=len(rows),finite_family_rows=rows,m4_credible_deviation=dict(old=68,new=82,unique_final_reply=2,final_reply_payoffs=list(map(str,reply))),formal_tax_polynomials=polys,orbit_alignment=dict(k=k,c=c,c_prime=cp,u_A=['1/2','1']),non_equivariant_selector_example=dict(players=2,topics=[[0],[1]],root_target=[1,1],complete_policy=[dict(history=list(h),action=a) for h,a in sigma.items()],actual=[0,1],all_action_comparisons=comparisons),global_1100_row_projection='NOT reconstructed: exact mass input/code absent locally',original_audit_runs=0,helper_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest())
 pathlib.Path('result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('PASS: 98 membership cases; 10 formal polynomial identities; m4 profitable deviation; orbit examples. Original runs 0; global point unverified.')
if __name__=='__main__':main()
