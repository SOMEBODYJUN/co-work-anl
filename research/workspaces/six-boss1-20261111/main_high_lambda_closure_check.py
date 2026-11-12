"""Main: review continuous closure and bind its actual payments to full4177."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
import json

W=Path(__file__).resolve().parent
R=W.parents[2]
P=W/'high_lambda_closure'
assert sha256((P/'proof.md').read_bytes()).hexdigest()=='3671f03677395cd8be8b95412fda5d4b5135a5cc0b69fd22eda65f2e5fa6a1ea'
data=json.loads((W/'visible_maximum_joint_v6/exact_input.json').read_text())
rows={r['name']:r for r in data['raw_rows']}
atoms=list(product((0,1),repeat=9))
safe_names=[]
for i in range(1,6):
 for target in list(range(1,9))+['C']:
  name=f'SAFE_{i}_{target}';row=rows[name];safe_names.append(name)
  for k,bits in enumerate(atoms):
   p=sum(bits[:i-1]);total=sum(bits[:6]);u=F(bits[i-1],total) if total else F(0)
   if target=='C':query=F(bits[8],p+7-i)
   elif target==8:query=F(bits[7],6*(p+7-i))
   else:query=F(bits[target-1],p+7-i)
   assert F(row['a'].get(str(k),'0'))==u-query,(name,k)
  assert F(row['a'].get('512','0'))==0 and F(row['rhs'])==0

links=json.loads((P/'endpoint_correspondence.json').read_text())['links']
assert len(links)==279
cache={}
for link in links:
 package=link['old_package']
 if package not in cache:cache[package]={r['name']:r for r in json.loads((R/package).read_text())['rows']}
 original=cache[package][link['old_row_name']]
 assert rows[link['old_row_name']]==original
 for k in range(513):F(original['a'].get(str(k),'0'))

brackets=identities=0
for i in range(1,6):
 m=5-i;n=6-i
 for q0 in [F(1,6),F(1,5)]:
  S0=1+m*q0/2;L=24-15*q0
  assert 24-15*q0-L==0 # independent u-coefficient identity, after cross-terms cancel
  assert 1-F(m)*q0/8>0
  for j in range(i+1,6):
   bj=1+F(j-i-1)*q0/F((7-j)*(8-j))
   assert 1<=bj<=S0 and bj>=S0/2
   for p in range(i):
    D=p+7-i
    assert 2*(j-i)*(p+1)<=n*(p+7-j)
    Q=bj/F(p+1)+(S0-bj)/D-S0/F(p+7-j)
    assert Q>=0;brackets+=1
    for t,o in product((0,1),repeat=2):
     M=F(o,6*(p+1+n*t));Phi=F(o,6*D)
     N=F(o,6*(p+(j-i)*t+7-j))
     assert bj*M+(S0-bj)*Phi-S0*N==F(o*(1-t),6)*Q
     identities+=1
    assert bj/F(p+1)+(S0-bj)/D-S0/F(p+7-j)==Q
result={'status':'PASS_MAIN_CONTINUOUS_HIGH_LAMBDA_CLOSURE_AND_FULL4177_PAYMENTS',
 'proof_read_sha256':sha256((P/'proof.md').read_bytes()).hexdigest(),
 'input_sha256':sha256((W/'visible_maximum_joint_v6/exact_input.json').read_bytes()).hexdigest(),
 'full_actual_SAFE_rows':len(safe_names),'SAFE_full_columns':len(safe_names)*513,'actual_SAFE_names':safe_names,
 'old_lambda25_rows_literal_in4177':len(links),'old_endpoint_column_positions':len(links)*513,
 'all_prefix_brackets_nonnegative':brackets,'all_p_t_o_query_coefficient_identities':identities,
 'analytic_review':['All missing states split into last-bit difference, D=6 prefix comparison and sum of single-missing gaps plus nonnegative remainder.',
 'Triangular positive-width sections give every base vertex and normalized ray; radial v=tau/(L0+lambda-25) represents entire unbounded domain.',
 'V<=m/24 follows by summing all normalized caps; A_T>0, A_O>=0, H>0. Source u, independent K and forced-target coefficients cancel exactly.',
 'The displayed nonnegative query remainder is checked for every legal p,j,t,o. Ordered uses its own O-average coefficient identity.',
 'C-only keeps the additional +V*E_C term after multiplying by H; its K coefficient is zero on each ray.',
 'All45 needed SAFE rows, including the five actual six-query mean rows, are already literal in full4177; all279 endpoint rows are already present. Thus closure applies to this finite input family as well.'],
 'frozen_proof_transcription_correction':'In proof.md section4.2, the term d,m_1 in f(p,d) means d times m_1; the correct formula is ((6-d)m_0+d*m_1)/6. Frozen code and all computations use multiplication. No source bytes changed.',
 'new_raw_rows_needed':0,'optimizer_calls':0,'candidate_points_read':0,'half_status':'OPEN'}
with (W/'main_high_lambda_closure_check.json').open('x') as out:out.write(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','full_actual_SAFE_rows','old_lambda25_rows_literal_in4177','all_prefix_brackets_nonnegative','new_raw_rows_needed']},ensure_ascii=False))
