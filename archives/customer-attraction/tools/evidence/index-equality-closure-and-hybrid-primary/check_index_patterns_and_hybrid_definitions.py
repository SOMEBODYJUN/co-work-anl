"""One NEW stdlib definition entry: fixed64 closure rows and hybrid policy.

No missing original audit/LP implementation is imported. The already verified
ER AE/R row is loaded without recomputation. No old437,42point orrestricted
optimization certificate is re-audited; no formalbadpolicy is called SPE.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from functools import lru_cache
from math import lcm
import hashlib,json
E=Path(__file__).resolve().parent;out=E/'new-index-pattern-and-hybrid-check.json'
if out.exists():raise SystemExit('Definition entry already completed; do not rerun')
point=E/'comparison/five_player_indexed_bound.json';data=json.loads(point.read_text())
assert hashlib.sha256(point.read_bytes()).hexdigest()=='18e074ba51357dfa03090fe9b97b8ff868b9c83b2687c7da7ff6f7b39489abe1'
atoms=data['primal']['atoms'];mass=[F(x['mass_numerator'],data['primal']['denominator']) for x in atoms]
assert len(atoms)==64 and all(x>0 for x in mass)
old=json.loads((E/'comparison/reused-ER-AE-row.json').read_text());assert old['input_sha256']==hashlib.sha256(point.read_bytes()).hexdigest()
q=5;patterns=['all_equal','query_equal_not_branch','first_query_equals_branch','second_query_equals_branch','all_distinct']
family_spec=[('AB','AB_hist',3,(0,1)),('AE','AE_hist',3,(0,4)),('Sbranch','second_hist',4,(0,))]
terminal={};pairs={};terminal_new_literal_terms=0;pair_literal_triples=0;pair_coefficient_equalities=0
for family,key,dim,fixed_positions in family_spec:
 states=list(product(range(2),repeat=dim))
 for menu in range(dim):terminal[family,menu]={'family':family,'query_position':menu,'atom_coefficients':[],'total_slack':F(0),'reused_ER_row':family=='AE' and menu==1}
 for M,N in combinations_with_replacement(range(dim),2):
  for overlap in [1,2]:
   for pattern in patterns:pairs[family,M,N,overlap,pattern]={'family':family,'M_position':M,'N_position':N,'overlap_coefficient':overlap,'index_pattern':pattern,'atom_coefficients':[],'total_slack':F(0)}
 for atom_index,(atom,w) in enumerate(zip(atoms,mass)):
  hist=atom[key];assert len(hist)==2**dim and sum(hist)==q
  expanded=[s for s,n in zip(states,hist) for _ in range(n)]
  fixed=sum(int(atom['bits'][i]) for i in fixed_positions)
  for menu in range(dim):
   row=terminal[family,menu]
   if row['reused_ER_row']:
    er=old['atom_records'][atom_index]
    assert er['index']==atom_index and er['bits']==atom['bits'] and er['AE_hist']==hist
    coefficient=F(er['atom_slack'])
   else:
    B=sum(s[menu] for s in expanded);compact=F(0);literal=F(0)
    for i,s in enumerate(expanded):
     den=fixed+sum(s[:-1])+1
     compact+=F((q-1)*s[-1]-B+s[menu],den)
     for j,t in enumerate(expanded):
      if i!=j:literal+=F(s[-1]-t[menu],den);terminal_new_literal_terms+=1
    assert literal==compact;coefficient=compact
   row['atom_coefficients'].append(coefficient)
   if not row['reused_ER_row']:row['total_slack']+=w*coefficient
  for M,N in combinations_with_replacement(range(dim),2):
   B=sum(s[M] for s in expanded);C=sum(s[N] for s in expanded);K=sum(s[M]*s[N] for s in expanded)
   compact=[[F(0) for _ in patterns] for _ in [1,2]]
   literal=[[F(0) for _ in patterns] for _ in [1,2]]
   for i,s in enumerate(expanded):
    p=fixed+sum(s[:-2]);v,z=s[-2:];h=(F(v+z,p+v+z) if v+z else F(0))+F(v,(p+1)*(p+2))
    b,c=s[M],s[N];D=(p+1)*(p+2)
    quantities=[(1,b+c,b*c),(q-1,B-b+C-c,K-b*c),
      (q-1,(q-1)*b+C-c,b*(C-c)),(q-1,B-b+(q-1)*c,(B-b)*c),
      ((q-1)*(q-2),(q-2)*(B-b+C-c),(B-b)*(C-c)-(K-b*c))]
    for orb,(n,L,T) in enumerate(quantities):
     for r_index,r in enumerate([1,2]):compact[r_index][orb]+=n*h-F(L,p+1)+F(r*T,D)
    for j,t in enumerate(expanded):
     for k,u in enumerate(expanded):
      orb=0 if i==j==k else 1 if j==k else 2 if i==j else 3 if i==k else 4
      base=h-F(t[M]+u[N],p+1);cross=F(t[M]*u[N],D)
      literal[0][orb]+=base+cross;literal[1][orb]+=base+2*cross;pair_literal_triples+=1
   assert literal==compact
   for r_index,r in enumerate([1,2]):
    for orb,pattern in enumerate(patterns):
     row=pairs[family,M,N,r,pattern];coefficient=compact[r_index][orb]
     row['atom_coefficients'].append(coefficient);row['total_slack']+=w*coefficient;pair_coefficient_equalities+=1
terminal['AE',1]['total_slack']=F(old['necessary_row_slack'])
terminal_rows=list(terminal.values());pair_rows=list(pairs.values())
new_terminal_violations=[x for x in terminal_rows if x['total_slack']<0]
weak=[x for x in pair_rows if x['overlap_coefficient']==2 and x['total_slack']<0]
strong=[x for x in pair_rows if x['overlap_coefficient']==1 and x['total_slack']<0]
reported_strongest=F(-472389383909475144797520617350241251969,908679097461847926994104235006019918544)
source_comparison={'ten_terminal_rows':len(terminal_rows)==10,'terminal_violations_four':len(new_terminal_violations)==4,
 'Sbranch_J_vs_I_exact':terminal['Sbranch',2]['total_slack']==reported_strongest,
 'weak_pair_violations_24':len(weak)==24,'strong_pair_violations_38':len(strong)==38}

def hybrid_case(m,k,exhaust_terminal):
 n=m-k;assert n>=1 and k>=1
 L=lcm(*range(1,n+1));sizes=[L//(n-i) for i in range(n)]+[L]*(m+k);labels=range(len(sizes))
 def action(h):
  if len(h)>=n:return next(a for a in range(n,len(sizes)) if a not in h)
  first=next((j for j,a in enumerate(h) if a!=j),None)
  return len(h) if first is None else h[first]
 def follow(h):
  while len(h)<m:h+=(action(h),)
  return h
 def pay(z,i):return F(sizes[z[i]],z.count(z[i]))
 actual=follow(());W=sum(sizes[a] for a in set(actual));OPT=m*L
 actual_rows=[]
 for i in range(m):
  h=actual[:i];u=pay(actual,i);vals=[]
  for a in labels:
   zz=follow(h+(a,));v=pay(zz,i);assert u>=v;vals.append({'action':a,'payoff':v,'slack':u-v,'terminal':zz})
  actual_rows.append({'history':h,'chosen':action(h),'payoff':u,'alternatives':vals})
 terminal_records=[];terminal_comp=0
 if exhaust_terminal:
  for depth in range(n,m):
   for h in product(labels,repeat=depth):
    zz=follow(h);u=pay(zz,depth);vals=[];assert u==L
    for a in labels:
     v=pay(follow(h+(a,)),depth);assert u>=v;vals.append(v);terminal_comp+=1
    terminal_records.append({'history':h,'chosen':action(h),'payoff':u,'all_action_values':vals})
 missing=None
 if n>=2:
  h=(n+k,);chosen=action(h);alternative=n+k+1
  prescribed=follow(h);deviated=follow(h+(alternative,));u=pay(prescribed,1);v=pay(deviated,1)
  assert chosen==h[0] and u==F(L,n) and v==L and u<v and m-1>k
  missing={'history':h,'remaining':m-1,'chosen':chosen,'deviation':alternative,'prescribed_terminal':prescribed,'deviation_terminal':deviated,'chosen_payoff':u,'deviation_payoff':v,'slack':u-v,'outside_both_retained_classes':True}
 return {'m':m,'k':k,'n':n,'L':L,'theme_sizes':sizes,'unit_customers':sum(sizes),'actual':actual,'W':W,'OPT':OPT,'ratio':F(OPT,W),
  'actual_path_nodes':m,'actual_path_comparisons_including_self':m*len(sizes),'actual_path_comparisons_nonself':m*(len(sizes)-1),'actual_path_rows':actual_rows,
  'terminal_histories_exhausted':exhaust_terminal,'terminal_nodes':len(terminal_records),'terminal_comparisons_including_self':terminal_comp,'terminal_rows':terminal_records,'missing_offpath_row':missing,
  'full_SPE_claimed':False,'all_m_k_proof':'Analytic MD proof, not this finite audit.'}
hybrids=[hybrid_case(10,2,False),hybrid_case(3,1,True),hybrid_case(4,2,True)]
assert (hybrids[0]['L'],hybrids[0]['W'],hybrids[0]['OPT'],hybrids[0]['ratio'])==(840,3963,8400,F(2800,1321))
assert hybrids[0]['missing_offpath_row']['slack']==-735
assert [x['terminal_nodes'] for x in hybrids[1:]]==[36,576]
def enc(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,dict):return {str(k):enc(v) for k,v in x.items()}
 if isinstance(x,(tuple,list)):return [enc(y) for y in x]
 return x
result={'status':'pass' if all(source_comparison.values()) else 'source-count-or-value-disagreement','new_definition_entry_runs':1,'original_entries':0,'external_solver_calls':0,'timing_recorded':False,
 'input64_sha256':hashlib.sha256(point.read_bytes()).hexdigest(),'input_atoms':64,'q':5,
 'terminal_rows':terminal_rows,'new_terminal_row_count':9,'reused_ER_row_count':1,'new_terminal_literal_terms':terminal_new_literal_terms,
 'pair_rows':pair_rows,'pair_rows_per_overlap':110,'pair_atom_compact_literal_equalities':pair_coefficient_equalities,'literal_branch_query_triples':pair_literal_triples,
 'weak_violations':len(weak),'strong_violations':len(strong),'source_comparison':source_comparison,
 'hybrid_cases':hybrids,'not_run':['old437systemor57dual','42atompoint','restricted64LPprimaldualFarkascertificates','6648oldgenericcaseaudit','combinedrankKandtailkimplementation','ERsuccessfulAE_Rrow','EF/FB/FP/FXmath'],
 'source_md_hashes_full_paths':{str(p.relative_to(E/'original')):hashlib.sha256(p.read_bytes()).hexdigest() for p in (E/'original').rglob('*.md')},
 'scope':'Universalindexpattern/hybridclaims proved analytically; fixed64numbers andfinitehybridactions exactchecks only. NoSPEbadpointorhalfproof.'}
out.write_text(json.dumps(enc(result),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(enc({'status':result['status'],'terminal_rows':10,'new_terminal_rows':9,'reused_ER_rows':1,'terminal_violations':len(new_terminal_violations),'Sbranch_J_vs_I':terminal['Sbranch',2]['total_slack'],'pair_rows':len(pair_rows),'weak_violations':len(weak),'strong_violations':len(strong),'pair_atom_equalities':pair_coefficient_equalities,'literal_triples':pair_literal_triples,'hybrid10_W':hybrids[0]['W'],'hybrid10_OPT':hybrids[0]['OPT'],'hybrid10_missing':hybrids[0]['missing_offpath_row']['slack'],'small_terminal_nodes':[x['terminal_nodes'] for x in hybrids[1:]],'new_entries':1,'original_entries':0,'external_solver_calls':0}),ensure_ascii=False))
