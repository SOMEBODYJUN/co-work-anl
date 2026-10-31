"""New independent definition check; no imports of original/canonical solvers.
Exact customer-incidence payoffs, arbitrary-history set-valued backward induction,
and complete affine IC for fixed policies in the assigned Markdown.
"""
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from functools import lru_cache
from pathlib import Path
import json,sys
BASE=Path(__file__).resolve().parent
I=json.loads((BASE/'input.json').read_text());T=I['customer_types'];P=I['m2_policy'];Q=I['m3_policy'];LABEL=I['topics']
def fmt(x):return str(x)
def u(a,z,w):
 return sum((F(c,sum(LABEL[b] in typ for b in z)) for typ,c in zip(T,w) if LABEL[a] in typ),F(0))
def cov(z,w):return sum(c for typ,c in zip(T,w) if any(LABEL[a] in typ for a in z))
def counts(z):return [z.count(a) for a in range(4)]
def action(h,m):
 if not h:return P['root'] if m==2 else Q['root']
 if m==2:return P['last'][h[0]]
 if len(h)==1:return Q['second'][h[0]]
 return Q['last'][h[0]][h[1]]
def leaf(h,m):
 while len(h)<m:h=h+(action(h,m),)
 return h
def fixed(m,w):
 rows=[]
 for d in range(m):
  for h in product(range(4),repeat=d):
   a=action(h,m);z=leaf(h,m);v=u(a,z,w);alt=[u(b,leaf(h+(b,),m),w) for b in range(4)];g=[v-alt[b] for b in range(4) if b!=a]
   assert all(x>0 for x in g)
   rows.append(dict(history=''.join(LABEL[i] for i in h),action=LABEL[a],true_payoffs=[fmt(x) for x in alt],min_nonself_slack=fmt(min(g))))
 z=leaf((),m);return dict(rows=rows,path=''.join(LABEL[i] for i in z),payoffs=[fmt(u(a,z,w)) for a in z],W=cov(z,w),OPT=max(cov(z,w) for z in product(range(4),repeat=m)),decision_nodes=len(rows),nonself_IC=sum(3 for _ in rows),min_nonself_slack=fmt(min(F(r['min_nonself_slack']) for r in rows)))
def all_spe(m,w):
 @lru_cache(None)
 def solve(h):
  if len(h)==m:return frozenset([h])
  children=[solve(h+(a,)) for a in range(4)]
  floor=max(min(u(a,z,w) for z in children[a]) for a in range(4))
  return frozenset(z for a in range(4) for z in children[a] if u(a,z,w)>=floor)
 zs=sorted(solve(()));co=sorted(set(tuple(counts(z)) for z in zs))
 return dict(paths=[''.join(LABEL[a] for a in z) for z in zs],terminal_counts=[list(x) for x in co],W_values=sorted(set(cov(z,w) for z in zs)),minimum_W=min(cov(z,w) for z in zs),OPT=max(cov(z,w) for z in product(range(4),repeat=m)),recurrence='exists child outcome for chosen action, independent minimizing SPE children off-action; compares to max_a min_child U_current(a,child)',cached_ordered_prefixes=solve.cache_info().currsize)
def q_policy(m):
 w=[22*a+b for a,b in I['strict_q_affine']];pol={}
 def rec(h):
  if len(h)==m:return h
  children=[rec(h+(a,)) for a in range(4)];v=[u(a,children[a],w) for a in range(4)]
  best=[a for a in range(4) if v[a]==max(v)];assert len(best)==1
  a=best[0];pol[h]=a;return children[a]
 rec(());return pol
def affine(m):
 aa=[x[0] for x in I['strict_q_affine']];bb=[x[1] for x in I['strict_q_affine']];rows=[];thresholds=[];pol=q_policy(m)
 def lf(h):
  while len(h)<m:h=h+(pol[h],)
  return h
 for d in range(m):
  for h in product(range(4),repeat=d):
   a=pol[h];z=lf(h);gaps=[]
   for b in range(4):
    if a==b:continue
    zz=lf(h+(b,));al=u(a,z,aa)-u(b,zz,aa);be=u(a,z,bb)-u(b,zz,bb)
    assert al>=0 and (al>0 or be>0) and 22*al+be>0
    if al>0:thresholds.append(-be/al)
    gaps.append(dict(alternative=LABEL[b],alpha=fmt(al),beta=fmt(be),q22_value=fmt(22*al+be)))
   rows.append(dict(history=''.join(LABEL[x] for x in h),action=LABEL[a],gaps=gaps))
 z=lf(())
 return dict(policy={''.join(LABEL[a] for a in h):LABEL[a] for h,a in sorted(pol.items())},rows=rows,nonself_IC=3*len(rows),max_strict_threshold=fmt(max(thresholds)),all_alpha_nonnegative=True,all_zero_alpha_beta_positive=True,all_q22_values_positive=True,path=''.join(LABEL[a] for a in z),W_affine=[cov(z,aa),cov(z,bb)],OPT_witness='AC',OPT_affine=[sum(aa),sum(bb)])
R={'kind':'new definition-level exact audit; not original program or report','thirteen':{str(m):all_spe(m,I['thirteen']) for m in [2,3]},'forty':{str(m):fixed(m,I['forty']) for m in [2,3]},'strict_q':{str(m):affine(m) for m in [2,3]}}
assert R['thirteen']['2']['paths']==['AC']
assert R['thirteen']['3']['terminal_counts']==[[0,1,1,1],[0,2,0,1],[1,1,1,0]]
assert R['thirteen']['3']['minimum_W']==12
assert R['forty']['2']['path']=='AC' and R['forty']['2']['W']==40 and R['forty']['2']['min_nonself_slack']=='1/2'
assert R['forty']['3']['path']=='DBB' and R['forty']['3']['W']==39 and R['forty']['3']['min_nonself_slack']=='1/6'
assert R['strict_q']['2']['W_affine']==[13,-50] and R['strict_q']['3']['W_affine']==[12,-40]
assert R['strict_q']['2']['max_strict_threshold']=='18' and R['strict_q']['3']['max_strict_threshold']=='21'
(BASE/'output.json').write_text(json.dumps(R,indent=2)+'\n')
print(json.dumps({'result':'all assertions passed','thirteen_root_paths':{m:R['thirteen'][m]['paths'] for m in ['2','3']},'forty_min_slacks':{m:R['forty'][m]['min_nonself_slack'] for m in ['2','3']},'affine_rows':78,'thresholds':['18','21'],'original_CLI':False}))
