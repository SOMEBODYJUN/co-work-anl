"""New stdlib check of the complete 13-unit Markdown strategy.

Not the unavailable author audit/JSON, not a new rank-one or38atom audit.
Run only after actualclaim+owner verification; output refuses overwrite.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib,json
E=Path(__file__).resolve().parent
out=E/'new-thinning-definition-check.json'
if out.exists():raise SystemExit('Definition check already completed; do not rerun')
types=[([0,1],2),([2],2),([0,2],1),([0,1,2],3),([3],2),([1,3],3)]
units=[frozenset(x) for x,n in types for _ in range(n)]
assert len(units)==13
actions={():1,**{(a,):b for a,b in enumerate([1,2,1,1])},
 **{h:a for h,a in zip(product(range(4),repeat=2),[3,2,1,1,2,2,3,2,1,3,1,1,1,2,1,2])}}
histories=[(),*((a,) for a in range(4)),*product(range(4),repeat=2)]
table=[['5/2','5','9/2','7/2'],['3','5','7/2','7/2'],['5/2','7/2','9/2','7/2'],['5/2','5','5/2','7/2'],['7/2','5','9/2','5/2'],
 ['2','14/3','10/3','5'],['13/6','19/6','7/2','7/2'],['7/3','5','7/3','5'],['3','4','4','5/2'],
 ['13/6','19/6','7/2','7/2'],['8/3','8/3','4','3'],['5/2','7/2','5/2','7/2'],['7/2','7/2','9/2','2'],
 ['7/3','5','7/3','5'],['5/2','7/2','5/2','7/2'],['10/3','6','2','5'],['4','5','3','5/2'],
 ['3','4','4','5/2'],['7/2','7/2','9/2','2'],['4','5','3','5/2'],['6','6','6','5/3']]
def follow(h):
 while len(h)<3:h+=(actions[h],)
 return h
def polynomial(z,i):
 coefficients=[0,0,0]
 for likes in units:
  if z[i] in likes:
   load=sum(a in likes for a in z);coefficients[load-1]+=1
 return coefficients
def integrate(coeff):return sum((F(n,j+1) for j,n in enumerate(coeff)),F(0))
def coverage(z):return sum(any(a in likes for a in z) for likes in units)
rows=[];lookup={}
for h,expected in zip(histories,table):
 z=follow(h);i=len(h);poly=polynomial(z,i);u=integrate(poly);alternatives=[]
 for a in range(4):
  zz=follow(h+(a,));pp=polynomial(zz,i);v=integrate(pp);delta=[x-y for x,y in zip(poly,pp)]
  assert v==F(expected[a]) and u>=v and integrate(delta)==u-v
  row={'action':a,'terminal':zz,'harmonic_value':v,'component_polynomial':pp,
    'harmonic_slack':u-v,'component_slack_coefficients':delta}
  alternatives.append(row);lookup[h,a]=row
 rows.append({'history':h,'chosen':actions[h],'terminal':z,'harmonic_value':u,'component_polynomial':poly,'alternatives':alternatives})
special=[((1,0),3,[0,-2,3]),((3,0),2,[-2,4,0]),((3,3),1,[1,0,-3])]
specials=[]
for h,a,expected in special:
 row=lookup[h,a];assert row['component_slack_coefficients']==expected and row['harmonic_slack']==0
 specials.append({'history':h,'chosen':actions[h],'alternative':a,'coefficients':expected,'integral':0})
assert F(4,9)>F(1,3)
actual=follow(());profit=[integrate(polynomial(actual,i)) for i in range(3)]
W=coverage(actual);terminals=[{'terminal':z,'coverage':coverage(z)} for z in product(range(4),repeat=3)];OPT=max(x['coverage'] for x in terminals)
assert actual==(1,2,3) and profit==[5,F(9,2),F(7,2)] and W==OPT==13
def enc(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,dict):return {str(k):enc(v) for k,v in x.items()}
 if isinstance(x,(tuple,list)):return [enc(z) for z in x]
 return x
result={'status':'pass','new_definition_entry_runs':1,'original_entries':0,'external_solver_calls':0,'timing_recorded':False,
 'unit_customers':13,'types':types,'labels':['A','B','C','D'],'full_policy_actions':[{'history':h,'action':actions[h]} for h in histories],
 'nodes':21,'including_self_comparisons':84,'nonself_comparisons':63,'all_rows':rows,'all64_terminal_coverages':terminals,
 'actual':actual,'profits':profit,'W':W,'OPT':OPT,'half_slack':2*W-OPT,'three_zero_integral_obstructions':specials,
 'no_common_t':'DAforces t>=1/2; BAthen t>=2/3; DDforces t²<=1/3; 4/9>1/3 exact.',
 'source_md_hashes_full_paths':{str(p.relative_to(E/'original')):hashlib.sha256(p.read_bytes()).hexdigest() for p in (E/'original').rglob('*.md')},
 'not_run':['originalthinningaudit','rankoneexistingrun','2396/38mass','root92/96/9770coupling','uniformfloatcones','EF/ER/FBentries'],
 'scope':'Only explicit13customer harmonicSPE/no commonparameter. Allm graft andmomentbounds areanalyticproofs, not finitecomputerclaims.'}
out.write_text(json.dumps(enc(result),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(enc({k:result[k] for k in ['status','nodes','including_self_comparisons','nonself_comparisons','actual','profits','W','OPT','half_slack','new_definition_entry_runs','original_entries','external_solver_calls']})))
