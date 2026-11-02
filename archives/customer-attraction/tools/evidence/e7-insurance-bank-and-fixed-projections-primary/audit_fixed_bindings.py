"""Fixed projection and stored-query binding only; no equilibrium/LP imports.

Checks no saved ell minimum, no IC, no complete outcome set, no LP optimality.
All returned policy qualification is reused from mature same-input evidence.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,product
from collections import defaultdict,Counter
from math import comb
from functools import lru_cache
import argparse,hashlib,json,time

HERE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);args=ap.parse_args();start=time.monotonic()
 ms=json.loads((HERE/'source-manifest.json').read_text());deps=json.loads((HERE/'fixed-input-manifest.json').read_text());data={};hashes={};inputs={}
 for x in ms:
  p=HERE/'original'/x['id']/Path(x['path']).name;assert p.stat().st_size==x['size'] and sha(p)==x['sha256'];hashes[str(p)]=sha(p)
  if p.suffix=='.json':data[x['id']]=json.loads(p.read_text())
 for x in deps:
  p=args.repo/x['path'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256'];hashes[str(p)]=sha(p);inputs[x['name']]=json.loads(p.read_text())
 report={'scope':'two explicit indexed projections and five original-weight stored-query menus; no ell reoptimization, no IC, no LP/BI/RNG or original entry call','input_sha256':hashes,'projection_checks':[],'fixed_query_menu_checks':[]}
 primal=inputs['indexed_primal']['primal'];atoms=primal['atoms'];assert len(atoms)==64 and primal['row_count']==437
 pointdep=next(x for x in deps if x['name']=='indexed_primal');assert pointdep['sha256']=='18e074ba51357dfa03090fe9b97b8ff868b9c83b2687c7da7ff6f7b39489abe1'
 projected=[];copies=0;ell_count=0;last_count=0
 for fixed,sid in [(5,'bc0513e16e1f9fdc04ff'),(10,'c61bcd8adfb7846feb72')]:
  saved=data[sid];scale=10*primal['denominator'];assert scale==saved['scale'] and saved['source_sha256']==pointdep['sha256']
  p=fixed+5;rows=defaultdict(int);js=[]
  for at in atoms:
   bits=at['bits'];assert len(bits)==10 and set(bits)<={'0','1'}
   j=sum(at['AB_hist'][4:]);assert j==sum(at['AE_hist'][4:])==sum(at['second_hist'][8:]);assert 0<=j<=5 and 10%comb(5,j)==0
   mass=int(at['mass_numerator']);assert mass>0
   actual=sum((1<<i) for i,c in enumerate(bits[:fixed]) if c=='1');each=mass*10//comb(5,j)
   for J in combinations(range(fixed,p),j):rows[actual|sum(1<<a for a in J)]+=each;copies+=1
   js.append(j)
  assert set(js)=={1} and len(rows)==saved['types']==(60 if fixed==5 else 155)
  w={b:F(n,scale) for b,n in rows.items()};path=tuple(range(5))
  def payoff(z,a):return sum((v/F(sum(bool(b>>c&1) for c in z)) for b,v in w.items() if b>>a&1),F(0))
  u=[payoff(path,a) for a in path];W=sum(v for b,v in w.items() if b&31);total=sum(w.values(),F(0))
  assert W==F(saved['W'])==1 and u==list(map(F,saved['u'])) and sum(u)==W
  # j=1 means exactly one comparison label covers each customer: five Ts cover all.
  assert all((b>>fixed).bit_count()==1 for b in rows)
  OPT=total;assert OPT==F(saved['OPT']);B=2*W-OPT;assert B==F(saved['B'])
  last=[payoff(path[:-1]+(a,),a) for a in range(p)];last_count+=p;assert max(last)==u[-1] and saved['last_br']
  ell=[list(map(F,row)) for row in saved['ell']];assert len(ell)==4 and all(len(row)==p for row in ell);ell_count+=sum(map(len,ell))
  M=list(map(max,ell));g=[v-uu for v,uu in zip(M,u)];P=sum((max(v,0) for v in g),F(0));N=sum((max(-v,0) for v in g),F(0));pp=max([F(0)]+g);nn=max([F(0)]+[-v for v in g]);C=2*P-N+pp+nn
  assert M==list(map(F,saved['M'])) and g==list(map(F,saved['g'])) and C==F(saved['C']) and B+C==F(saved['B_plus_C'])>0
  sizes=[sum(v for b,v in w.items() if b>>a&1) for a in range(p)]
  CD=[sum(v for b,v in w.items() if b>>a&1 and not b>>other&1) for a,other in [(2,3),(3,2)]]
  assert sizes[2]==sizes[3]==5*u[0] and min(CD)>0
  distinct=[]
  for a,b in combinations(range(p),2):
   d=sum(v for mask,v in w.items() if bool(mask>>a&1)!=bool(mask>>b&1));assert d>0;distinct.append(str(d))
  projected.append({'source_id':sid,'topic_count':p,'scale':scale,'clients':[{'interest_mask':b,'unit_customer_multiplicity':str(n)} for b,n in sorted(rows.items())]})
  report['projection_checks'].append({'source_id':sid,'fixed_count':fixed,'topic_count':p,'input_atoms':len(atoms),'j_values':sorted(set(js)),'positive_types':len(rows),'scale':scale,'integer_clients':str(sum(rows.values())),'W':str(W),'u':list(map(str,u)),'OPT_from_five_disjoint_comparison_labels':str(OPT),'B':str(B),'last_action_payoffs':list(map(str,last)),'last_br':True,'saved_ell_entries_only_algebra_checked':sum(map(len,ell)),'saved_M':list(map(str,M)),'saved_g':list(map(str,g)),'C_from_saved_ell':str(C),'B_plus_C_from_saved_ell':str(B+C),'C_size':str(sizes[2]),'D_size':str(sizes[3]),'five_root_payoff':str(5*u[0]),'C_minus_D':str(CD[0]),'D_minus_C':str(CD[1]),'all_labels_positive_coverage_separation':True,'new_ell_minimum_or_BI_checks':0})
 finite=data['9b7a0cf12c9e1f5aca15'];nkeys=branches=entries=0;fieldcounts=[]
 for r in finite['original_weight_tests']:
  n=r['game'];game=inputs[n+':game'];cert=inputs[n+':policy'];m=game['players'];p=len(game['topics']);policy={}
  for row in cert['strategy']['actions']:
   h=tuple(row['history']);a=row['action'];assert h not in policy and type(a)==int and 0<=a<p;policy[h]=a
  assert set(policy)=={h for d in range(m) for h in product(range(p),repeat=d)};nkeys+=len(policy)
  assert max(policy.values())+1==p
  @lru_cache(None)
  def end(h):return h if len(h)==m else end(h+(policy[h],))
  z=end(());assert list(z)==r['outcome']
  customers=[]
  for c in game['customers']:
   B=frozenset(c['topics']);w=c['multiplicity'];assert all(type(a)==int and 0<=a<p for a in B) and type(w)==int and w>=0;customers.append((B,w))
  W=sum(w for B,w in customers if any(a in B for a in z));assert W==r['W']
  dist=list(map(F,r['p']));assert len(dist)==p and min(dist)>=0 and sum(dist)==1
  matrices=[];R=[];argmins=[];childs=[]
  for i in range(m):
   matrix=[];child=[]
   for a in range(p):
    y=end(z[:i]+(a,));child.append(list(y));branches+=1
    row=[]
    for t in range(p):
     row.append(sum((F(w,1+sum(b in B for b in y)) for B,w in customers if t in B),F(0)));entries+=1
    matrix.append(row)
   vals=[sum((dist[t]*row[t] for t in range(p)),F(0)) for row in matrix];R.append(min(vals));argmins.append([a for a,v in enumerate(vals) if v==min(vals)]);matrices.append([[str(v) for v in row] for row in matrix]);childs.append(child)
  assert R==list(map(F,r['R'])) and sum(R)-W==F(r['sum_R_minus_W'])
  # Bind the recorded discovery inputs; the onpath certificate is intentionally paired with aggregate_theta game.
  for suffix in [':game',':policy']:
   dd=next(x for x in deps if x['name']==n+suffix)
   srcpath=('examples/customer_attraction/'+n+'.json') if suffix==':game' else ('evidence/certificates/customer_attraction/'+('onpath_budget_failure' if n=='aggregate_theta_failure' else n)+'.json')
   assert finite['source_sha256'][srcpath]==dd['sha256']
  report['fixed_query_menu_checks'].append({'game':n,'m':m,'p':p,'ordered_action_keys_read_and_bound':len(policy),'root_path':list(z),'W':W,'stored_query':list(map(str,dist)),'R':list(map(str,R)),'sum_R_minus_W':str(sum(R)-W),'argmin_forced_actions':argmins,'all_forced_terminal_paths':childs,'K_matrices_by_position_forced_query':matrices,'new_IC_or_LP_optimality_checks':0})
 assert len(report['fixed_query_menu_checks'])==5
 for p,h in hashes.items():assert sha(Path(p))==h
 report['actual_operations']={'projection_atom_visits':2*len(atoms),'integer_type_emissions_before_aggregation':copies,'projection_last_BR_comparisons_including_self':last_count,'stored_ell_scalars_algebra_only':ell_count,'original_weight_policy_keys_structurally_bound':nkeys,'forced_branches_evaluated':branches,'full_terminal_extra_query_matrix_entries':entries,'new_ell_or_SPE_outcome_BI':0,'new_IC':0,'LP':0,'RNG':0,'original_entry_or_import':0}
 report['elapsed_seconds']=time.monotonic()-start
 (HERE/'fixed-binding-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(HERE/'projected-unit-client-types.json').write_text(json.dumps(projected,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'projections':[{k:v for k,v in x.items() if k not in ('last_action_payoffs','saved_M','saved_g')} for x in report['projection_checks']],'menus':[{k:v for k,v in x.items() if k not in ('K_matrices_by_position_forced_query','all_forced_terminal_paths')} for x in report['fixed_query_menu_checks']],'actual_operations':report['actual_operations'],'elapsed_seconds':report['elapsed_seconds']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
