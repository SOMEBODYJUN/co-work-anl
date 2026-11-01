"""New exact selected-row check, not the unavailable historical audit.

Input is the already archived 64-atom 437-row certificate. This entry only
evaluates the AE last-node offdiagonal R-menu row from the printed lemma.
It does not re-audit the 437-row system, run an LP, or certify a strategy.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
E=Path(__file__).resolve().parent
out=E/'new-ae-menu-exclusion.json'
if out.exists():raise SystemExit('Selected-row check already completed; do not rerun')
source=E/'comparison/five_player_indexed_bound.json'
data=json.loads(source.read_text())
assert data['theme_order']==list('ABCDEUVWXY')
assert data['paths']['second']==list('AEUVW')
types=[tuple(x) for x in data['third_histogram_type_order']]
assert types==[(t,r,s) for t in range(2) for r in range(2) for s in range(2)]
atoms=data['primal']['atoms'];den=int(data['primal']['denominator'])
assert len(atoms)==64 and den>0
K=5;chosen=F(0);full=F(0);diag=F(0);off=F(0);welfare=F(0);comparison=F(0)
rows=[];direct_terms=0
for index,atom in enumerate(atoms):
 bits=[int(x) for x in atom['bits']];hist=atom['AE_hist']
 assert len(bits)==10 and len(hist)==8 and all(isinstance(x,int) and x>=0 for x in hist) and sum(hist)==K
 mass=F(atom['mass_numerator'],den);assert mass>0
 p=bits[0]+bits[4]
 expanded=[state for state,n in zip(types,hist) for _ in range(n)]
 R=sum(r for t,r,s in expanded)
 own=sum((F(s,p+t+r+s) if s else F(0) for t,r,s in expanded),F(0))
 all_queries=sum((F(R,p+t+r+1) for t,r,s in expanded),F(0))
 diagonal=sum((F(r,p+t+r+1) for t,r,s in expanded),F(0))
 off_direct=F(0)
 for i,(t,r,s) in enumerate(expanded):
  for j,(tt,rr,ss) in enumerate(expanded):
   if i!=j:off_direct+=F(rr,p+t+r+1);direct_terms+=1
 off_factored=R*sum((F(1,p+t+r+1) for t,r,s in expanded),F(0))-diagonal
 assert off_direct==off_factored==all_queries-diagonal
 slack=(K-1)*own-off_direct
 chosen+=mass*own;full+=mass*all_queries;diag+=mass*diagonal;off+=mass*off_direct
 welfare+=mass*int(any(bits[:5]))
 comparison+=mass*int(any(t for t,r,s in expanded))
 rows.append({'index':index,'bits':atom['bits'],'AE_hist':hist,'mass':mass,'prefix_p':p,'R_count':R,
  'sum_last_reply_payoffs':own,'full_R_queries':all_queries,'diagonal_R_queries':diagonal,
  'offdiagonal_direct':off_direct,'offdiagonal_factored':off_factored,'atom_slack':slack,
  'weighted_slack':mass*slack})
assert welfare==1 and comparison==F(data['primal']['comparison_cover'])
slack=4*chosen-off
assert slack==sum((x['weighted_slack'] for x in rows),F(0))
def enc(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,dict):return {str(k):enc(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [enc(y) for y in x]
 return x
result={'status':'selected-necessary-row-violated' if slack<0 else 'selected-row-not-negative',
 'new_definition_entry_runs':1,'original_program_entry_runs':0,'optimizer_calls':0,'timer_recorded':False,
 'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'input_bytes':source.stat().st_size,
 'input_atoms':len(atoms),'K':K,'expanded_offdiagonal_terms':direct_terms,
 'source_row':'menu_exclusion_lemma.md equation(5), AE background a+e, comparison C_j=R_j',
 'actual_template_welfare':welfare,'template_comparison_union':comparison,
 'sum_last_reply_payoffs':chosen,'four_times_reply_payoffs':4*chosen,'all_25_query_sum':full,
 'five_diagonal_query_sum':diag,'all_20_offdiagonal_query_sum':off,'necessary_row_slack':slack,
 'full_sum_row_slack':5*chosen-full,'diagonal_sum_row_slack':chosen-diag,
 'atom_records':rows,'scope':'Only selected AE_R coefficient factorization and total fixed-point diagnostic; no recheck of437 rows or their dual, no completeSPE, no enhanced-cone optimum.'}
out.write_text(json.dumps(enc(result),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(enc({k:v for k,v in result.items() if k!='atom_records'}),ensure_ascii=False))
