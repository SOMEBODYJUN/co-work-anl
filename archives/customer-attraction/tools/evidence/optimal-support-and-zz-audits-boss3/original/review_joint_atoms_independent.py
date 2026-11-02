#!/usr/bin/env python3
"""Independent literal-label review of closure/joint_atoms_exact.json.
Does not import joint_atoms.py or its verifier/audit. The 60 ZZ rows are rebuilt
from 66 actual reply labels and the literal utility difference, without using
its polynomial compiler. Old 1083 raw rows use the frozen preceding library.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
from collections import Counter,defaultdict
import json,hashlib,sys
BASE=Path(__file__).resolve().parent
WORK=BASE.parent
ROOT=next(p for p in BASE.parents if (p/'work.py').exists())
SOURCE=ROOT/'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra'
INPUT=WORK/'closure/joint_atoms_exact.json'
SCHEMA=WORK/'closure/joint_atoms_old_schema.json'
d=json.loads(INPUT.read_text());old=json.loads(SCHEMA.read_text())
PAT=tuple(product((0,1),repeat=3))
def groupkey(g):return (g[0],g[1],tuple(g[2]),tuple(g[3]))
def canon(xs):
 values={};out=[]
 for x in xs:
  if x not in values:values[x]=len(values)
  out.append(values[x])
 return tuple(out)
PARTS=tuple(sorted({canon(z) for z in product(range(4),repeat=4)}))
ROWS=tuple((f,g,p) for f,g,p in product(range(2),range(2),PARTS))
labels=tuple((f,i,j) for f,i,j in product(range(2),range(6),range(6)) if f==1 or i!=j)
assert len(labels)==66 and len(ROWS)==60
paircounts=Counter((e[0],v[0],canon((e[1],e[2],v[1],v[2]))) for e in labels for v in labels)

histmass=[F() for _ in d['histograms']]
four=[defaultdict(F) for _ in d['histograms']]
rr=[defaultdict(F) for _ in d['histograms']]
zz={r:F() for r in ROWS}
W=F();O=F();paircomparisons=0;semantic_polynomial_matches=0
for atom in d['atoms']:
 hi=atom['hist_index'];hist=d['histograms'][hi];w=F(atom['weight'])
 assert w>0 and 0<=hi<len(histmass)
 groups=tuple(map(groupkey,d['groups'][hi]));R=atom['R'];Z=atom['Z']
 assert len(R)==len(Z)==len(groups) and len(groups)==len(set(groups))
 assert all(type(b) is int and b in (0,1) for b in R+Z)
 histmass[hi]+=w;W+=w*int(any(int(x) for x in hist['actual_bits']));O+=w*int(hist['d']>0)
 words=tuple(t for t,n in zip(PAT,hist['hist']) for _ in range(n))
 assert len(words)==6 and len(hist['actual_bits'])==6
 lookup={g:i for i,g in enumerate(groups)}
 # Directly assign both bits to each of the 66 distinct labels. Orbit equality
 # is this witness's chosen restriction, never assumed for every valid model.
 edgegroup={e:(e[0],int(e[1]==e[2]),words[e[1]],words[e[2]]) for e in labels}
 assert set(edgegroup.values())==set(groups)
 bits={e:(R[lookup[edgegroup[e]]],Z[lookup[edgegroup[e]]]) for e in labels}
 for i,g in enumerate(groups):four[hi][g,(R[i],Z[i])]+=w
 for i,g in enumerate(groups):
  for j,h in enumerate(groups):rr[hi][g,h]+=w*R[i]*R[j]
 pa=sum(map(int,hist['actual_bits'][:4]));nums=defaultdict(int)
 for e in labels:
  re,ze=bits[e]
  for v in labels:
   _,zv=bits[v];row=(e[0],v[0],canon((e[1],e[2],v[1],v[2])))
   # Literally u6(Z_e)-u6(Z_v), with the same R_e in both comparisons.
   # For binary z: z/(pa+R_e+z) = z/(pa+R_e+1).
   nums[row,pa+re+1]+=ze-zv
   paircomparisons+=1
   # Check the source's multilinear denominator expansion independently.
   assert (ze-zv)*(pa+2-re)*(pa+re+1)==(ze-zv)*(pa+1)*(pa+2)
   semantic_polynomial_matches+=1
 for (row,den),num in nums.items():zz[row]+=w*F(num,den)

assert F(d['K'])>=0 and O==1 and W==F(d['W']) and W<F(1,2)
assert 1-2*W==F(d['strict_half_gap'])
# All four states, including the implicit 00 state, and every RR marginal
# upper bound follow from the same assignments rather than separate marginals.
fourbounds=0;rrbounds=0;minfour=None;minrr=None
for hi,groups_json in enumerate(d['groups']):
 groups=tuple(map(groupkey,groups_json));mass=histmass[hi]
 for g in groups:
  vals=[four[hi][g,(r,z)] for r,z in product((0,1),repeat=2)]
  assert sum(vals)==mass and min(vals)>=0
  upper=mass-sum(four[hi][g,s] for s in ((0,1),(1,0),(1,1)))
  assert upper==four[hi][g,(0,0)]
  minfour=upper if minfour is None else min(minfour,upper);fourbounds+=1
  for h in groups:
   rg=sum(four[hi][g,s] for s in ((1,0),(1,1)))
   rh=sum(four[hi][h,s] for s in ((1,0),(1,1)))
   x=rr[hi][g,h]
   assert 0<=x<=rg and x<=rh
   minrr=min(rg-x,rh-x) if minrr is None else min(minrr,rg-x,rh-x)
   rrbounds+=2
# Recover the complete frozen old-column schema directly from the atoms.
cols=old['columns'];histpositions={};current=None;generated=[];nhi=0
for j,c in enumerate(cols):
 kind=c['kind']
 if kind=='K':value=F(d['K'])
 elif kind=='hist':
  current=nhi;nhi+=1;histpositions[j]=current
  assert {k:v for k,v in c.items() if k!='weight'}==d['histograms'][current]
  value=histmass[current]
 elif kind=='joint-reply':value=four[current][groupkey(c['group']),tuple(c['state'])]
 elif kind=='overlap':
  hi=histpositions[c['hist_column']];g,h=map(groupkey,c['groups']);value=rr[hi][g,h]
 else:raise AssertionError(kind)
 assert value==F(c['weight']),(j,kind,value,c['weight'])
 generated.append(value)
assert nhi==len(histmass)
# Check all preceding raw rows using their frozen exact definitions. This is
# shared-library replay, not an independently rederived audit of all 1083.
sys.path.insert(0,str(SOURCE))
import attractive_nested as at
hc=[h for h in d['histograms']]
libcols,names,m,obj,norm=at.build(hc)
assert len(libcols)==len(cols)
assert json.dumps(libcols)==json.dumps([{k:v for k,v in c.items() if k!='weight'} for c in cols])
active=[(j,v) for j,v in enumerate(generated) if v]
raw=[];bound=[]
for name,row in zip(names,m):
 val=sum((row[j]*v for j,v in active if row[j]),F())
 assert val>=0,(name,val)
 if name.startswith(('joint-state-upper:','overlap-upper:')):bound.append((name,val))
 else:raw.append((name,val))
assert len(raw)==1083 and len(raw)+len(zz)==1143
assert min(zz.values())>=0
report={'status':'PASS_EXACT_SPECIFIED_ROW_OBSTRUCTION_ONLY','scope':'27 positive joint atoms on 16 frozen histograms; 60 ZZ rows rebuilt independently from 66x66 literal labels; preceding raw rows shared-library exact replay; not a game/SPE or general half result','input_sha256':hashlib.sha256(INPUT.read_bytes()).hexdigest(),'old_schema_sha256':hashlib.sha256(SCHEMA.read_bytes()).hexdigest(),'atoms':len(d['atoms']),'histograms':len(histmass),'reply_labels_per_atom':len(labels),'literal_pair_comparisons':paircomparisons,'denominator_identity_checks':semantic_polynomial_matches,'four_state_bounds_checked':fourbounds,'RR_upper_bounds_checked_including_diagonal_and_both_orders':rrbounds,'minimum_implicit_00_mass':str(minfour),'minimum_RR_upper_slack':str(minrr),'matched_old_schema_columns':len(cols),'prior_raw_rows_shared_library_replayed':len(raw),'prior_bound_rows_replayed':len(bound),'new_ZZ_rows_independently_rebuilt':len(zz),'raw_rows_total':len(raw)+len(zz),'minimum_prior_raw_slack':str(min(v for _,v in raw)),'minimum_ZZ_slack':str(min(zz.values())),'K':str(F(d['K'])),'O':str(O),'W':str(W),'W_decimal':float(W),'strict_half_gap':str(1-2*W),'ZZ_rows':[{'f':f,'g':g,'partition':p,'literal_label_pairs':paircounts[f,g,p],'value':str(zz[f,g,p])} for f,g,p in ROWS]}
(BASE/'closure_independent_review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='ZZ_rows'},indent=2))
