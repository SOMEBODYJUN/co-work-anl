"""NEW stdlib definition checks from complete MD formulas/customer tables.

Not the missing original prefix_absence_audit/independent_partition_audit.
No canonical game implementation, discovery LP, or optimizer is imported.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,permutations
import hashlib,json
E=Path(__file__).resolve().parent
output=E/'new-definition-check.json'
if output.exists():raise SystemExit('New mathematical entry already completed; do not rerun')
H=[F(0)]
for j in range(1,101):H.append(H[-1]+F(1,j))
patterns=0;pattern_minimum_checks=0
for m in range(1,13):
 for k in range(1,m+1):
  d=m-k;mins={}
  for pattern in product([0,1],repeat=d):
   missed=0;value=F(0)
   for covers in pattern:
    value+=F(1,m-missed)
    if not covers:missed+=1
   r=sum(pattern);lower=F(r,m)+H[m]-H[k+r]
   assert value>=lower,(m,k,pattern,value,lower)
   mins[r]=min(mins.get(r,value),value);patterns+=1
  for r,value in mins.items():assert value==F(r,m)+H[m]-H[k+r];pattern_minimum_checks+=1

cases=[];coefficient_checks=polynomial_lower_checks=0;old_inclusions=new_inclusions=polynomial_certifications=0
gamma_lookup={}
for m in range(1,101):
 for k in range(1,m+1):
  d=m-k;a=F(d+2,d+1);N=2*m*d*(d+2)+(d+2)*k-2*m*m
  L=F(N,2*m*m*(d+1));Q=F((d+2)*k,2*m*m*(d+1));coeff=[]
  for t in range(k,m+1):
   r=t-k;q=m-t;Ar=F(r,m)+H[m]-H[t]-F(r,t)
   assert Ar>=F(k*(m-t),m*t)>=0
   Ct=t+a*(t*(H[m]-H[t])-F((t-k)*(m-t),m))
   assert Ct==t*(1+a*Ar)
   assert Ct>=m-L*q+Q*q*q
   coeff.append((t,Ct));coefficient_checks+=1;polynomial_lower_checks+=1
  gamma=min(x[1] for x in coeff);argmins=[t for t,c in coeff if c==gamma]
  old_square=d*d<=m;old_residual=m*(2*d+1)>=d*d*(d+2);new=gamma>=m-1
  polynomial=max(N,0)**2<=8*m*m*(d+1)*(d+2)*k
  if old_square:assert old_residual;old_inclusions+=1
  if old_residual:assert new;new_inclusions+=1
  if polynomial:assert new;polynomial_certifications+=1
  gamma_lookup[(m,d)]=(gamma,argmins)
  cases.append({'m':m,'k':k,'d':d,'gamma':gamma,'argmin_t':argmins,'old_square':old_square,
    'old_residual':old_residual,'harmonic_certifies':new,'polynomial_certifies':polynomial})

relaxation_checks=0
for m in range(1,61):
 for d in range(m):
  g=m-d
  for h in range(d,m):
   endpoint=g+F((h+2)*g*d,m*(h+1))
   assert m*(h+1)*(endpoint-(m-1))==m*(h+d+1)-d*d*(h+2)
   if d*d<=m:assert m*(h+d+1)>=d*d*(h+2)
   relaxation_checks+=1
table_inputs=[(6,2,3,F(85,16)),(8,3,4,F(1233,175)),(12,4,5,F(265349,23760)),
 (20,5,7,F(27649297,1447040)),(50,9,12,F(4212909271547,85846896135)),
 (100,13,17,F(38598461531924449,389208642094272))]
table=[]
for m,oldmax,d,reported in table_inputs:
 actual,args=gamma_lookup[(m,d)];computed_oldmax=max(dd for dd in range(m) if m*(2*dd+1)>=dd*dd*(dd+2))
 table.append({'m':m,'d':d,'reported_gamma':reported,'computed_gamma':actual,'argmin_t':args,
  'reported_old_largest_d':oldmax,'computed_old_largest_d':computed_oldmax,
  'gamma_equal':reported==actual,'old_largest_equal':computed_oldmax==oldmax})
assert all(gamma_lookup[(6,6-k)][0]>=5 for k in range(3,7))
assert all(gamma_lookup[(5,5-k)][0]<4 for k in [1,2])

# Complete fourteen-unit-customer point from the 5054B comparison Markdown.
types=[([3],2),([3,4],1),([2],2),([2,5],1),([1],2),([1,5],1),([1,4],1),([0,3,4,5],2),([0,2,4,5],2)]
units=[frozenset(likes) for likes,n in types for _ in range(n)];assert len(units)==14
topics=[frozenset(i for i,likes in enumerate(units) if a in likes) for a in range(6)]
assert len(set(topics))==6 and list(map(len,topics))==[4,4,5,5,6,6]
replies=[1,4,4,5,5,4];actions={():0,**{(a,):b for a,b in enumerate(replies)}}
def follow(h):
 while len(h)<2:h+=(actions[h],)
 return h
def pay(z,i):return sum((F(1,sum(a in likes for a in z)) for likes in units if z[i] in likes),F(0))
def covered(z):return frozenset(i for i,likes in enumerate(units) if any(a in likes for a in z))
node_rows=[]
for h in [(),*((a,) for a in range(6))]:
 z=follow(h);i=len(h);u=pay(z,i);alts=[]
 for b in range(6):
  zz=follow(h+(b,));v=pay(zz,i);assert u>=v;alts.append({'action':b,'terminal':zz,'payoff':v,'slack':u-v})
 node_rows.append({'history':h,'chosen':actions[h],'terminal':z,'payoff':u,'alternatives':alts})
actual=follow(());actual_set=covered(actual);Welfare=len(actual_set)
all_ordered=[{'tuple':z,'coverage':len(covered(z))} for z in product(range(6),repeat=2)]
OPT=max(x['coverage'] for x in all_ordered);opts=[x['tuple'] for x in all_ordered if x['coverage']==OPT]
assert actual==(0,1) and (pay(actual,0),pay(actual,1))==(4,4) and Welfare==8 and OPT==10
assert opts==[(2,3),(3,2)]
matchings=[]
for opt in opts:
 O=covered(opt);owners={}
 for x in O:
  eligible=[j for j,T in enumerate(opt) if T in units[x]];assert len(eligible)==1;owners[x]=eligible[0]
 for assignment in permutations(range(2)):
  rows=[];value=F(0)
  for x,j in sorted(owners.items()):
   i=assignment.index(j);cx=sum(a in units[x] for a in actual);den=cx+1-int(actual[i] in units[x]);cost=F(1,den)
   rows.append({'customer':x,'eligible_occurrence':j,'actual_slot':i,'actual_load':cx,'cost':cost});value+=cost
  assert value==9
  matchings.append({'ordered_optimum':opt,'actual_slot_to_optimal_occurrence':assignment,'R':value,'customer_rows':rows})
assert sum((F(1,1+sum(a in likes for a in actual)) for x,likes in enumerate(units) if x in covered((2,3))),F(0))==8
source_md=E/'original/research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_terminal/prefix_absence_repeated_last.md'
point_md=E/'comparison-original/research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_boss/partition_attack/optimal_partition_counterexample.md'
def enc(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,dict):return {str(k):enc(v) for k,v in x.items()}
 if isinstance(x,(tuple,list)):return [enc(v) for v in x]
 return x
table_ok=all(x['gamma_equal'] and x['old_largest_equal'] for x in table)
out={'status':'pass' if table_ok else 'source-table-difference','new_definition_entry_runs':1,'timing_recorded':False,
 'original_program_runs':0,'optimizer_calls':0,'source_md_sha256':hashlib.sha256(source_md.read_bytes()).hexdigest(),
 'comparison_point_md_sha256':hashlib.sha256(point_md.read_bytes()).hexdigest(),
 'prefix_pattern_checks_m_le_12':patterns,'prefix_minimum_by_r_checks':pattern_minimum_checks,
 'coefficient_checks_m_le_100':coefficient_checks,'polynomial_lower_checks':polynomial_lower_checks,
 'old_square_inclusions':old_inclusions,'old_residual_to_harmonic_inclusions':new_inclusions,
 'polynomial_certified_cases':polynomial_certifications,'relaxed_d_h_endpoint_checks_m_le_60':relaxation_checks,
 'all_m_k_cases':cases,'reported_six_row_table_comparison':table,
 'six_player_k_ge_three_certified':True,'five_k_one_two_not_certified_by_this_interface':True,
 'fourteen_customer_point':{'types':types,'distinct_themes':6,'unit_customers':14,'actual':actual,'utilities':[4,4],
   'W':Welfare,'OPT':OPT,'half_slack':2*Welfare-OPT,'node_count':7,'including_self_comparisons':42,
   'nonself_comparisons':35,'all_node_comparisons':node_rows,'all_36_ordered_comparison_tuples':all_ordered,
   'only_optimal_ordered_tuples':opts,'partition_eligibility_is_unique_for_each_customer':True,
   'all_four_order_matching_checks':matchings,'all_R_equal_9':True,'full_terminal_tax':F(4),'addition_query_A':F(8)},
 'universal_scope':'Analytic proofs, not finite checks, establish the all-parameter theorem and asymptotic. Old audits not rerun.'}
output.write_text(json.dumps(enc(out),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(enc({k:v for k,v in out.items() if k not in ['all_m_k_cases','reported_six_row_table_comparison','fourteen_customer_point']})))
print(json.dumps(enc(table)))
print('fourteen_unit_customer_exact_SPE_OPT_partition_PASS')
