#!/usr/bin/env python3
"""Independent exact recomputation for shared-z+dilution, no submitted checkers."""
from pathlib import Path
from fractions import Fraction as Q
import argparse,hashlib,importlib.util,json,platform,random
parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,default=Path.cwd());args=parser.parse_args()
ROOT=args.repo.resolve()
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);a=importlib.util.module_from_spec(s);s.loader.exec_module(a);return a
basepath=ROOT/'tests/audits/unrelated_machines/diluted_sink_probe_gap.py'
extpath=ROOT/'tests/audits/unrelated_machines/diluted_escape_probe_gap.py'
peerpath=ROOT/'tests/audits/unrelated_machines/heavy_matching_residual.py'
b=load(basepath,'candidate_base');e=load(extpath,'candidate_extension')
d=e.extend_instance(b,4)
M=len(d['configs']);J=len(d['edges']);z=d['escape'];T=d['T']
assert z==M-1 and d['configs'][z]==[(Q(1),())]
assert len(d['blockers'])==sum(len(g['blockers']) for g in d['gadgets'])
assert all(d['edges'][j].get(z)==Q(1,2) for j in d['blockers'])
assert all(z not in ed for j,ed in enumerate(d['edges']) if j not in d['blockers'])
coverage=[Q(0)]*J;columns=0
for i,choices in enumerate(d['configs']):
 assert sum((w for w,S in choices),Q(0))==1
 for w,S in choices:
  assert w>=0 and len(set(S))==len(S)
  assert all(i in d['edges'][j] for j in S)
  assert sum((d['edges'][j][i] for j in S),Q(0))<=T
  for j in S:coverage[j]+=w
  columns+=1
assert all(v==1 for v in coverage)

def checkactual(x,jfix,ifix):
 assert set(x)==set(range(J));load=[Q(0)]*M
 for j in range(J):
  assert sum(x[j].values(),Q(0))==1
  for i,v in x[j].items():
   assert isinstance(v,Q) and v>=0 and i in d['edges'][j]
   assert d['edges'][j][i]<=T
   load[i]+=d['edges'][j][i]*v
 assert x[jfix].get(ifix,Q(0))==1
 assert max(load)<=T
 return max(load)

rng=random.Random(20261016)
oldpairs=[(j,i) for j,ed in enumerate(d['edges']) for i in ed if i!=z]
newpairs=[(j,z) for j in d['blockers']]
chosenold={(d['bridge'],i) for i in d['roots']}
g=d['gadgets'][0]
for j in g['ordinary']:chosenold.update((j,i) for i in d['edges'][j])
chosenold.update((g['blockers'][0],i) for i in g['terminals'])
seen=set()
for j,i in oldpairs:
 key=tuple(d['roles'][j])+(d['edges'][j][i],)
 if key not in seen:chosenold.add((j,i));seen.add(key)
chosenold.update(rng.sample(oldpairs,32))
chosennew={(g['blockers'][0],z) for g in d['gadgets']}
chosennew.update(rng.sample(newpairs,12))
maxold=max(checkactual(e.escape_probe_certificate(b,d,j,i),j,i) for j,i in sorted(chosenold))
maxnew=max(checkactual(e.escape_probe_certificate(b,d,j,i),j,i) for j,i in sorted(chosennew))
small=[{i for i,p in ed.items() if 2*p<=T} for ed in d['edges']]
big=[{i for i,p in ed.items() if 2*p>T} for ed in d['edges']]
mandatory={j for j,S in enumerate(small) if not S}
unique=[{j for j,S in enumerate(small) if S=={i}} for i in range(M)]
assert mandatory=={d['bridge']} and unique[z]==d['blockers']
assert not any(z in H for H in big)
queries=0;maxmatching=0
for j,H in enumerate(big):
 for i in H:
  # Independently build an actual matching saturating all optional U_i,
  # then place mandatory bridge at a remaining root. Full saturation proves
  # its weight is globally maximal because all optional weights are >=0.
  match={j:i};used={i}
  for ell in sorted(unique[i]):
   assert ell!=j
   choices=big[ell]-used
   assert choices
   r=min(choices);match[ell]=r;used.add(r)
  for ell in sorted(mandatory-set(match)):
   choices=big[ell]-used
   assert choices
   r=min(choices);match[ell]=r;used.add(r)
  assert mandatory|{j}|unique[i] <= set(match)
  assert len(set(match.values()))==len(match)
  assert all(r in big[ell] for ell,r in match.items())
  assert match[j]==i
  F=sum((d['edges'][ell][i] for ell in unique[i]),Q(0))
  W=sum((d['edges'][ell][i] for ell in unique[i] if ell in match),Q(0))
  assert W==F and d['edges'][j][i]+F-W<=T
  queries+=1;maxmatching=max(maxmatching,len(match))
# z's all-optional matching is not a GHMR query, but verify the explicit
# extra claim too. Do not use z as an available big destination.
zmatch={};used=set()
for g in d['gadgets']:
 for ell,r in zip(g['blockers'],g['terminals']):
  assert r in big[ell] and r not in used
  zmatch[ell]=r;used.add(r)
assert set(zmatch)==unique[z]
starqueries=0
for j,ed in enumerate(d['edges']):
 for i in ed:
  Fstar=[ell for ell,domains in enumerate(d['edges']) if ell!=j and i in domains
         and all(2*p>T for r,p in domains.items() if r!=i)]
  used=set();match={}
  for ell in sorted(Fstar,key=lambda ell:len(d['edges'][ell])):
   candidates=set(d['edges'][ell])-{i}-used
   assert candidates
   r=min(candidates);used.add(r);match[ell]=r
  assert len(used)==len(Fstar)
  assert all(r!=i and r in d['edges'][ell] for ell,r in match.items())
  assert d['edges'][j][i]<=T # full saturation makes B precisely p_ij
  starqueries+=1
# Independent upper schedule, unused z: small ends plus one down path.
sigma={d['bridge']:d['roots'][0]}
for j,ed in enumerate(d['edges']):
 smallend=[i for i,p in ed.items() if p==Q(1,d['k'])]
 if smallend:sigma[j]=smallend[0]
v=d['roots'][0]
while True:
 outgoing=[j for j,ed in enumerate(d['edges']) if ed.get(v)==Q(1,d['k'])]
 if not outgoing:break
 j=min(outgoing);v=next(i for i in d['edges'][j] if i!=v);sigma[j]=v
for g in d['gadgets']:
 occupied=set(sigma[j] for j in g['ordinary'])&set(g['terminals'])
 for j,i in zip(g['blockers'],sorted(set(g['terminals'])-occupied)):sigma[j]=i
assert set(sigma)==set(range(J)) and z not in sigma.values()
loads=[Q(0)]*M
for j,i in sigma.items():loads[i]+=d['edges'][j][i]
assert max(loads)==2-Q(1,d['k'])
print(json.dumps({'title':'稀释终端共享小端组合的独立证书重算','python':platform.python_version(),
 'arithmetic':'Fraction exact','seed':20261016,'submitted_base_sha256':hashlib.sha256(basepath.read_bytes()).hexdigest(),
 'submitted_extension_sha256':hashlib.sha256(extpath.read_bytes()).hexdigest(),
 'peer_GHMR_sha256':hashlib.sha256(peerpath.read_bytes()).hexdigest(),
 'audit_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'k':4,'machines':M,'jobs':J,'old_edges':len(oldpairs),'added_edges':len(newpairs),
 'all_config_columns_checked':columns,'old_actual_points_checked':len(chosenold),
 'new_actual_points_checked':len(chosennew),'max_old_probe_load':str(maxold),'max_new_probe_load':str(maxnew),
 'all_GHMR_big_queries_with_independent_full_matching':queries,'largest_matching_size':maxmatching,
 'independent_z_optional_matching_size':len(zmatch),'all_star_queries_with_independent_full_matching':starqueries,
 'independent_unused_z_schedule_value':str(max(loads)),
 'limitations':['Only k=4 expanded; general proof reviewed separately.',
 'Instance/point generators imported; no submitted numerical checker, GHMR certificate, optimizer or filter called.',
 'Actual point sample covers all bottom groups at z but does not cover all finite edges.',
 'No full integer assignment enumeration for this large instance; no global approximation result.']},ensure_ascii=False,indent=2))
