"""Main independently rebuilds cap3 costs, full weak intervals and186 raw rows."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
from functools import lru_cache
import json

W=Path(__file__).resolve().parent
P=W/'source2_cap3_tradeoff'
TAILS=list(product((0,1),repeat=4))
ATOMS=list(product((0,1),repeat=9))


def params(delta,s,q0,h):
 x=F(5977,6912)-delta;y=F(43,48)+delta;a=25+x+y-s
 b0=[q0*(F(1,2)+x/12+y/6),q0/2+x+q0*y/6,q0/2+y]
 b=[b0[0]-h,b0[1],b0[2]]
 return x,y,a,b0,b,1+sum(b)


def cost(delta,s,q0,h,p,t,q,tail):
 x,y,a,b0,b,S=params(delta,s,q0,h);r3,r4,r5,z=tail;L=p+t+r3+r4+r5+z
 num=a*t-z-x*r4-y*r5
 assert L or num==0
 return (num/L if L else F(0))+sum(bb*r for bb,r in zip(b,tail[:3]))+z+q/F(p+t+r3+r4+r5+1)+x*q/F(p+t+r3+3)+y*q/F(p+t+r3+r4+2)


@lru_cache(None)
def minimum(delta,s,q0,h,p,t,q):
 return min(cost(delta,s,q0,h,p,t,q,r) for r in TAILS)


def fvalues(delta,s,q0,h,p):
 out=[minimum(delta,s,q0,h,p,0,F(0))]
 for d in range(1,7):
  v=d*minimum(delta,s,q0,h,p,1,F(d-1,5))
  if d<6:v+=(6-d)*minimum(delta,s,q0,h,p,0,F(d,5))
  out.append(v/6)
 return out


def row_vector(row,h=None):
 delta,s,q0=map(F,[row['delta'],row['s'],row['q0']]);h=F(row['h']) if h is None else h
 x,y,a,b0,b,S=params(delta,s,q0,h)
 mu=S-s/5 if row['row_kind']=='C-only' else F(0)
 values=[]
 for bits in ATOMS:
  total=sum(bits[:6]);u=F(bits[1],total) if total else F(0);p,o,c=bits[0],bits[7],bits[8]
  if row['mode']=='ordered':
   fs=fvalues(delta,s,q0,h,p);G=min(fs[1:]);assert G==fs[1]
   val=a*u-o*G
  else:
   name=row['target'];j=int(name[1:])-1 if name.startswith('A') else 6 if name=='X' else 8
   val=a*u-minimum(delta,s,q0,h,p,bits[j],F(o,6))+mu*c
  values.append(val)
 values.append(S-mu)
 return values


def main():
 proof=P/'proof.md'
 assert sha256(proof.read_bytes()).hexdigest()=='d5645c90f0b2f1f3a0eea8b713f02eef70760c46b2f79ba73de5692e2fc316d1'
 env=json.loads((P/'exact_envelopes.json').read_text())['slices']
 family=json.loads((P/'exact_family.json').read_text())['rows']
 segments=json.loads((P/'affine_family.json').read_text())['rows']
 assert len(env)==12 and len(family)==186 and len(segments)==126
 states=zero_intervals=intervals=conditions=multiplicity_pairs=0
 for sl in env:
  delta,s,q0=map(F,[sl['delta'],sl['s'],sl['q0']]);x,y,a,b0,b,S=params(delta,s,q0,F(0));B=b0[0]
  assert [F(v) for v in sl['h_domain']]==[F(0),B]
  all_breaks={F(0),B}
  for cond in sl['conditions']:
   p,t,q=cond['p'],cond['t'],F(cond['q']);conditions+=1
   lines=[(cost(delta,s,q0,F(0),p,t,q,r),F(-r[0])) for r in TAILS]
   U=min(z[0] for z,r in zip(lines,TAILS) if r[0]==0)
   V=min(z[0] for z,r in zip(lines,TAILS) if r[0]==1)
   assert [U,V]==list(map(F,cond['group_min_at_zero']))
   assert F(cond['kappa'])==max(F(0),V-U)
   for idx,(record,(aa,bb)) in enumerate(zip(cond['tails'],lines)):
    assert record['tail']==''.join(map(str,TAILS[idx]))
    assert [F(record['intercept']),F(record['slope'])]==[aa,bb];states+=1
    lo,hi=F(0),B;empty=False
    for cc,dd in lines:
     gap,slope=aa-cc,bb-dd
     if slope>0:hi=min(hi,-gap/slope)
     elif slope<0:lo=max(lo,-gap/slope)
     elif gap>0:empty=True
    if lo>hi:empty=True
    got=None if empty else [str(lo),str(hi)]
    assert record['weak_minimum_interval']==got
    assert record['zero_length']==(not empty and lo==hi)
    if not empty:
     all_breaks.update((lo,hi));intervals+=1;zero_intervals+=int(lo==hi)
   if t:
    assert V<U, (sl['id'],cond['key'])
   else:
    Z=q*(F(1,p+1)+x/F(p+3)+y/F(p+2))
    J=B+q*(F(1,p+2)+x/F(p+4)+y/F(p+3))
    # The two groups contain all sixteen tails. Their minima need not be
    # represented by the same tail, but their lower envelope is exactly Z/J.
    for h in [F(0),B,max(F(0),min(B,J-Z))]:
     assert minimum(delta,s,q0,h,p,t,q)==min(Z,J-h)
  assert sorted(all_breaks)==list(map(F,sl['common_breaks']))
  if sl['mode']=='ordered':
   for h in sorted(all_breaks):
    for p in [0,1]:
     fs=fvalues(delta,s,q0,h,p)
     assert fs[0]==0 and min(fs[1:])==fs[1]
     for d in range(2,7):
      assert fs[d]-fs[1]>=F(d-1)*F(146807,414720)
      multiplicity_pairs+=1
 for row in family:
  assert row_vector(row)==list(map(F,row['a'])),row['id']
  delta,s,q0,h=map(F,[row['delta'],row['s'],row['q0'],row['h']]);x,y,a,b0,b,S=params(delta,s,q0,h)
  assert F(row['real_budget']['source_IC'])==a and a>0 and all(v>=0 for v in b)
  assert list(map(F,row['beta_original'].values()))==b0
  assert list(map(F,row['beta_actual'].values()))==b
  assert F(row['raw_K'])==S
  mu=S-s/5 if row['row_kind']=='C-only' else F(0)
  assert F(row['free_EC'])==mu and F(row['K'])==S-mu
  base=row_vector(row,F(0));got=row_vector(row)
  threshold=q0*(F(1,3)+x/30+y/12)
  for j,bits in enumerate(ATOMS):
   p,o,c=bits[0],bits[7],bits[8]
   if row['mode']=='ordered':
    diff=o*(h if not p else h/6+F(5,6)*max(F(0),h-threshold))
   else:
    target=row['target'];t=bits[int(target[1:])-1] if target.startswith('A') else bits[6] if target=='X' else c
    diff=h*t+h*o*(1-t)*(1-p)+max(F(0),h-threshold)*o*(1-t)*p
    if row['row_kind']=='C-only':diff-=h*c
   assert got[j]-base[j]==diff,(row['id'],j)
  assert got[512]-base[512]==(F(0) if row['row_kind']=='C-only' else -h)
 byid={r['id']:r for r in family}
 for seg in segments:
  lo,hi=F(seg['lo']),F(seg['hi']);left=byid[seg['left_row_id']];right=byid[seg['right_row_id']]
  lvec,rvec=row_vector(left),row_vector(right)
  intercept,slope=list(map(F,seg['intercept'])),list(map(F,seg['slope']))
  for j in range(513):
   assert slope[j]==(rvec[j]-lvec[j])/(hi-lo)
   assert intercept[j]==lvec[j]-lo*slope[j]
  mid=(lo+hi)/2
  assert row_vector(left,mid)==[aa+mid*bb for aa,bb in zip(intercept,slope)]
 result={'status':'PASS_MAIN_CAP3_FULL192_CONDITIONS_WEAK_INTERVALS_186_RAW_AND126_SEGMENTS',
  'proof_read_sha256':sha256(proof.read_bytes()).hexdigest(),'source_family_sha256':sha256((P/'exact_family.json').read_bytes()).hexdigest(),
  'conditions':conditions,'true_affine_tail_states':states,'nonempty_weak_intervals':intervals,'zero_length_weak_intervals':zero_intervals,
  'complete_endpoint_columns':186*513,'complete_affine_coefficients':126*513*2,'segment_midpoint_columns':126*513,
  'strict_ordered_endpoint_comparisons':multiplicity_pairs,'exact_general_C_only_and_ordered_tradeoff_columns':186*513,
  'C_only_entire_continuum_redundant':True,'other_new_information':'Only literal differences proved; no whole-cone independence or current-point separation claimed.',
  'optimizer_calls':0,'candidate_points_read':0,'half_status':'OPEN'}
 with (W/'main_cap3_tradeoff_check.json').open('x') as out:out.write(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
