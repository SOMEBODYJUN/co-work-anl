from fractions import Fraction as F
from itertools import product,permutations
import json

def enc(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,dict):return {str(k):enc(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [enc(v) for v in x]
 return x

def routing(rho,edges):
 n=len(rho);v=[F(0)]*n;u=[F(0)]*n;policy={}
 for i in reversed(range(n)):
  c=1+len(edges[i]);v[i]=rho[i]/c;u[i]=rho[i]/c
  if edges[i]:
   j=min(edges[i],key=lambda j:(v[j],j));policy[i]=j
   v[i]+=F(c-1,c)*v[j];u[i]+=sum((u[j] for j in edges[i]),F(0))/c
 assert all(v[i]>=1 and u[i]>=v[i] for i in range(n))
 choices=[edges[i] for i in range(n) if edges[i]];branch=[i for i in range(n) if edges[i]]
 vals=[]
 for selected in product(*choices):
  p=dict(zip(branch,selected));z=[F(0)]*n
  for i in reversed(range(n)):
   c=1+len(edges[i]);z[i]=rho[i]/c+(F(c-1,c)*z[p[i]] if edges[i] else 0)
  vals.append(z)
 assert all(min(z[i] for z in vals)==v[i] for i in range(n))
 # One argmin rule simultaneously attains any nonnegative source mixture.
 mixtures=[[F(1)]*n,[F(i+1,3) for i in range(n)]]
 for source in mixtures:
  inflow=list(source);absorbed=F(0);cost=F(0)
  for i in range(n):
   c=1+len(edges[i]);a=inflow[i]/c;absorbed+=a;cost+=rho[i]*a
   if edges[i]:inflow[policy[i]]+=inflow[i]-a
  assert absorbed==sum(source,F(0)) and cost==sum((source[i]*v[i] for i in range(n)),F(0))
 return dict(nodes=n,rho=rho,edges=edges,bellman=v,uniform=u,deterministic_policies=len(vals),shared_argmin_source_mixtures=2)

def initialization(m,eligible,prices):
 best=None;records=0;formula=[]
 for pi in permutations(range(m)):
  val=sum((min(prices[x][pi[j]][j] for j in eligible[x]) for x in range(len(eligible))),F(0));formula.append(val)
  for owner in product(*eligible):
   cost=sum((prices[x][pi[j]][j] for x,j in enumerate(owner)),F(0));records+=1
   best=cost if best is None else min(best,cost)
 assert min(formula)==best
 illegal=sum((min(prices[x][i][j] for i in range(m) for j in eligible[x]) for x in range(len(eligible))),F(0))
 assert illegal<=best
 return dict(m=m,customers=len(eligible),permutations=len(formula),owner_permutation_choices=records,Copt=best,illegal_customerwise_pi_lower_bound=illegal,strict_coupling_gap=best-illegal)

def main():
 gs=[]
 for n in range(1,6):
  for pattern in range(3):
   edges=[]
   for i in range(n):
    after=list(range(i+1,n));edges.append(after if pattern==0 else (after[:1] if pattern==1 else after[::2]))
   rho=[F(1)+F((3*i+n+pattern)%7,3) for i in range(n)]
   gs.append(routing(rho,edges))
 strict=routing([F(3),F(3,2),F(1),F(4)],[[1,2,3],[2,3],[3],[]]);assert strict['bellman'][0]<strict['uniform'][0]
 gs.append(strict)
 p2=[[[F(1),F(1)],[F(100),F(100)]] for _ in range(2)]
 i2=initialization(2,[[0],[1]],p2);assert i2['Copt']==101 and i2['illegal_customerwise_pi_lower_bound']==2
 p3=[[[F(1)+F(((i+1)*(j+2)+x)%7,2) for j in range(3)] for i in range(3)] for x in range(3)]
 i3=initialization(3,[[0,1],[1,2],[0,2]],p3)
 rc=0
 for a,b,k in product(range(4),repeat=3):
  delta=F(1,a+1+k)-F(1,b+1+k);rhs=F(b-a,(a+1+k)*(b+1+k));assert delta==rhs and abs(delta)<=1
  if a==0 and b>=1:assert delta>0
  rc+=1
 V=[[F(19),F(19)],[F(22),F(22)]];W=F(44);OPT=F(45);R=F(42);G=F(41);u=[F(22),F(22)]
 match=[sum((V[i][p[i]] for i in range(2)),F(0)) for p in permutations(range(2))]
 allq=sum((sum(row,F(0)) for row in V),F(0));e=[u[i]-sum(V[i],F(0))/2 for i in range(2)]
 first=W-OPT+allq/2;assert OPT-W==R-G==1 and match==[41,41] and max(match)<R and allq>=2*(OPT-W)
 assert 2*W-OPT==first+sum(e,F(0))==43
 return dict(status='PASS',arithmetic='standard-library-Fraction',new_definition_check_runs=1,original_program_entries=0,old_full_strategy_replays=0,abstract_dags=len(gs),deterministic_route_policy_instances=sum(g['deterministic_policies'] for g in gs),simultaneous_source_mixtures=sum(g['shared_argmin_source_mixtures'] for g in gs),routing_cases=gs,initialization_cases=[i2,i3],total_joint_owner_permutation_choices=i2['owner_permutation_choices']+i3['owner_permutation_choices'],fixed_tail_reset_cases=rc,existing86matrix=dict(matrix=V,W=W,OPT=OPT,R=R,G=G,matchings=match,total_query=allq,WA_target=2*(OPT-W),ic_slack=e,WA_bracket=first,half_slack=2*W-OPT,credibility='existing-canonical-complete-proof;matrix-arithmetic-only'),scope='abstractrecipientDAGsandinitialpricearraysnotclaimedSPE;existing86matrixonly;noprogramorfloatreportinputavailable')

if __name__=='__main__':print(json.dumps(enc(main()),ensure_ascii=False,indent=2))
