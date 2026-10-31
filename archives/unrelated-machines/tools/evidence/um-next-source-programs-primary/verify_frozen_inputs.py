#!/usr/bin/env python3
"""Independent data/formula/certificate check. No original imports or audit reruns.
Run in an empty directory. Old exhaustive counts are compared, not recomputed.
"""
import ast,hashlib,json,pathlib,platform
from fractions import Fraction as Q
E=pathlib.Path(__file__).resolve().parent; C=E/'comparison'
def load(p):return json.loads((C/p).read_text())
def encode(x):
 if isinstance(x,Q):return str(x)
 if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [encode(v) for v in x]
 return x
def save(p,x):pathlib.Path(p).write_text(json.dumps(encode(x),ensure_ascii=False,indent=2)+'\n')
def build(f,k,d):
 closed=f=='closed'; a=Q(k-1,k) if closed else 1-Q(1,2*k);delta=Q(k-1,k*k) if closed else Q(1,k);c=Q(1,k*k);D=d+k-1 if closed else d+2*k-1
 ms=['r' if closed else 'root'];root=ms[0];roots=[];locals=[];blocks=[]
 for b,h in enumerate([d]*k+[D] if closed else [D]+[d]*k):
  hs=[f'h{b}_{u}' if closed else f'chain{b}.home{u}' for u in range(h)];sink=root if closed else f'chain{b}.sink';ms+=hs+([] if closed else [sink]);g=f'g{b}';es=[f'e{b}_{u}' for u in range(h)]
  p=(a if b==k else delta+c/4 if b==0 else delta) if closed else Q(1) if b==0 else delta
  r=[g,root,hs[0],p,Q(1),b];ls=[[e,hs[u],hs[u+1] if u+1<h else sink,a,Q(1) if u+1<h or not closed else c/2 if b==0 else c,b] for u,e in enumerate(es)]
  roots.append(r);locals+=ls;blocks.append([r]+ls)
 jobs=[r for block in blocks for r in block] if closed else roots+locals
 tests={'s0':lambda b:b<k if closed else b>0,'s1':lambda b:b==k if closed else b==0,'bad':lambda b:b==0 if closed else b==1,'repair':lambda b:b in (0,1) if closed else b in (1,2)}
 st={name:{j:v if test(b) else u for j,u,v,p,t,b in jobs} for name,test in tests.items()};P={j:{u:p,v:t} for j,u,v,p,t,b in jobs};beta=Q(1,k)
 x={j:{i:beta*(st['s0'][j]==i)+(1-beta)*(st['s1'][j]==i) for i in P[j]} for j in P}
 L={name:{i:sum((P[j][i] for j in P if s[j]==i),Q(0)) for i in ms} for name,s in st.items()}
 B=2-Q(3,k)+Q(3,2*k*k) if closed else 2-Q(1,k);R=2-Q(4,k)+Q(7,2*k*k) if closed else 2-Q(2,k)
 assert max(L['s0'].values())==max(L['s1'].values())==1 and max(L['bad'].values())==B and max(L['repair'].values())==R
 assert all(sum(row.values())==1 and all(v>0 for v in row.values()) for row in x.values())
 assert all(sum((P[j].get(i,0)*x[j].get(i,0) for j in P),Q(0))<=1 for i in ms)
 changed=[j for j in P if st['bad'][j]!=st['repair'][j]];touched={i for j in changed for i in (st['bad'][j],st['repair'][j])};assert len(changed)==d+1 and len(touched)==d+(1 if closed else 2)
 assert max(sum(st['bad'][j]==i for j in changed) for i in ms)==1
 order=[j[0] for j in jobs];rootfirst=[r[0] for r in roots+locals];inter=[r[0] for block in blocks for r in block]
 orders={'closed_independent':order,'closed_reviewer':rootfirst} if closed else {'long_gap':order,'long_independent':order,'long_reviewer':inter}
 graphs={}
 for role,order in orders.items():
  idx={j:q for q,j in enumerate(order)};edges={j:[] for j in order};intervals={};counts={}
  for i in ms:
   at=Q(0)
   for j in sorted((j for j in order if x[j].get(i,0)),key=lambda j:(-P[j][i],idx[j])):
    end=at+x[j][i]
    if i==root:intervals[j]=[at,end]
    for s in range(at.numerator//at.denominator,-(-end.numerator//end.denominator)):
     if min(end,s+1)>max(at,s):edges[j].append([i,s])
    at=end
   counts[i]=-(-at.numerator//at.denominator)
  assert counts[root]==k+closed and all(v==1 for i,v in counts.items() if i!=root)
  graphs[role]=dict(edges=edges,counts=counts,root_intervals=intervals)
 b=1 if closed else 2;seq=[j for j,u,v,p,t,branch in jobs if branch==b];g=next(j for j in seq if j.startswith('g'));es=[j for j in seq if j!=g];path=[dict(st['bad'])]
 for j in list(reversed(es))+[g]:
  s=dict(path[-1]);s[j]=next(i for i in P[j] if i!=s[j]);path.append(s)
 peaks=[max(sum((P[j][i] for j in P if s[j]==i),Q(0)) for i in ms) for s in path]
 assert path[-1]==st['repair'] and max(peaks)==B+(c if closed else 0)
 if not closed:assert all(b<=a for a,b in zip(peaks,peaks[1:]))
 return dict(family=f,k=k,d=d,machines=ms,jobs=jobs,P=P,states=st,x=x,loads=L,B=B,R=R,source_job_orders=orders,slot_graphs=graphs,changed=changed,touched=sorted(touched),reverse_tail_path_to_repair=path,path_peaks=peaks)
def certificate(z):
 f=z['family'];closed=f=='closed';base=f'optimal_hull_{"closed_cycle" if closed else "long_chain"}_k3d1.json';inp=load(pathlib.Path('examples/unrelated_machines')/base);ce=load(pathlib.Path('evidence/certificates/unrelated_machines')/base);ms=z['machines'];P=z['P'];st=z['states'];role='closed_independent' if closed else 'long_gap';order=z['source_job_orders'][role]
 assert inp['machines']==ms
 if closed:
  assert inp['jobs']==order and {j:{i:Q(v) for i,v in row.items()} for j,row in inp['processing_times'].items()}==P
  assert ce['optimal_schedules']==[st['s0'],st['s1']] and ce['bad_schedule']==st['bad'] and ce['sharp_reassignment']==st['repair']
  assert {j:{i:Q(v) for i,v in row.items()} for j,row in ce['fractional_assignment'].items()}==z['x']
  match=ce['bad_slot_matching'];path=ce['one_job_escape_path'];actual=[]
  assert path[0]==st['bad'] and path[-1]==st['s0'] and len(path)-1==4
  for q,s in enumerate(path):
   if q:assert sum(path[q-1][j]!=s[j] for j in P)==1
   actual.append(max(sum((P[j][i] for j in P if s[j]==i),Q(0)) for i in ms))
  assert actual==list(map(Q,ce['path_makespans'])) and max(actual)==z['B']+Q(1,9)
 else:
  assert [[Q(v) if v is not None else None for v in row] for row in inp['processing_times']]==[[P[j].get(i) for j in order] for i in ms]
  owners=lambda s:[ms.index(s[j]) for j in order]
  assert ce['optimal_components']==[owners(st['s0']),owners(st['s1'])] and ce['bad_assignment']==owners(st['bad']) and ce['repair_assignment']==owners(st['repair'])
  assert [[Q(v) for v in row] for row in ce['x']]==[[z['x'][j].get(i,Q(0)) for j in order] for i in ms]
  match={j:[ms[i],s] for j,(i,s) in zip(order,ce['bad_slot_injection'])}
  for n in ['bad','repair']:assert list(map(Q,ce[n+'_loads']))==[z['loads'][n][i] for i in ms]
 assert len(match)==len(order) and len({tuple(s) for s in match.values()})==len(order)
 assert all(s in z['slot_graphs'][role]['edges'][j] and s[0]==st['bad'][j] for j,s in match.items())
 return dict(family=f,machines=len(ms),jobs=len(order),finite_edges=2*len(order),slot_injection_edges=len(match),PASS=True)
def main():
 ca=load(pathlib.Path('evidence/runs/unrelated_machines/optimal_hull_closed_cycle_audit.json'));la=load(pathlib.Path('evidence/runs/unrelated_machines/optimal_hull_long_chain_audit.json'));li=load(pathlib.Path('evidence/runs/unrelated_machines/optimal_hull_long_chain_independent.json'));lr=load(pathlib.Path('evidence/runs/unrelated_machines/optimal_hull_long_chain_reviewer.json'));bindings=[]
 for r in json.loads((E/'primary-inventory.json').read_text()):
  raw=(E/'original'/r['path']).read_bytes();assert len(raw)==r['size'] and hashlib.sha256(raw).hexdigest()==r['sha256'];tree=ast.parse(raw)
  imports=sorted({n.module.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and n.module}|{a.name.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names})
  assert set(imports)<={'__future__','collections','fractions','itertools','functools','json','pathlib','hashlib','platform'}
  name=pathlib.Path(r['path']).name;actual=ca['sha256'][r['path']] if 'closed_cycle' in name else la['source_sha256'] if name.endswith('_gap.py') else li['code_sha256'] if name.endswith('_independent.py') else lr['source_sha256'];assert actual==r['sha256'];bindings.append(dict(id=r['id'],sha256=actual,imports=imports,original_entry_run_here=False))
 ccases=[(3,1),(3,2),(4,1),(4,2),(5,1)];lcases=[(k,d) for k in range(3,9) for d in range(1,5)]+[(3,20),(16,1),(32,2)];zs=[build('closed',k,d) for k,d in ccases]+[build('long',k,d) for k,d in lcases];by={(z['family'],z['k'],z['d']):z for z in zs};certs=[certificate(by[f,3,1]) for f in ['closed','long']]
 ci=ca['independent_integer_owner_enumeration'];cr=ca['independent_subset_DP'];assert [(r['k'],r['d']) for r in ci['results']]==ccases and sum(r['assignments'] for r in ci['results'])==353280
 for r in ci['results']:
  z=by['closed',r['k'],r['d']];assert (r['m'],r['n'])==(len(z['machines']),len(z['jobs'])) and r['assignments']==2**len(z['jobs']) and Q(r['bad'])==z['B'] and r['minimum_changed_jobs']==r['minimum_touched_machines']==r['d']+1
 assert cr['total_schedules']==91136 and [(r['k'],r['d']) for r in cr['exhaustive_cases']]==[(3,1),(3,2),(4,1),(5,1)]
 for r in cr['exhaustive_cases']:
  z=by['closed',r['k'],r['d']];assert Q(r['mincost'])==sum(z['loads']['bad'].values()) and r['mincost_machine_assignments']==1
 assert [(r['k'],r['d'],r['all_equal_size_root_tie_orders']) for r in ci['tie_checks']]==[(3,1,12),(4,1,144)] and [(r['k'],r['d'],r['all_root_tie_orders']) for r in cr['all_tie_orders']]==[(3,1,12),(4,1,144)]
 assert [(r['k'],r['d']) for r in la['cases']+la['boundaries']]==lcases and len(la['cases'])==24 and len(la['boundaries'])==3 and la['invalid_rejections']==5
 for r in la['cases']+la['boundaries']:
  z=by['long',r['k'],r['d']];assert r['machines']==len(z['machines']) and r['jobs']==len(z['jobs']) and Q(r['bad'])==z['B'] and Q(r['repaired'])==z['R'] and Q(r['minimum_slot_cost'])==sum(z['loads']['bad'].values()) and Q(r['cost_margin'])==Q(1,2*r['k']) and r['mincost_optimized']==(r in la['cases'])
 assert li['total_enumerated_assignments']==270336
 for a,b,lex,slot in zip(li['runs'],lr['runs'],[76,144,378],[90,192,324]):
  assert (a['k'],a['d'])==(b['k'],b['d']);z=by['long',a['k'],a['d']];assert a['lex_improving_assignments']==b['strict_lex_improving_assignments']==lex and a['slot_covering_machine_assignments']==slot and b['minimum_cover_matchings']==a['mincost_slot_machine_assignments']==b['minimum_slot_owner_assignments']==1 and a['enumerated_assignments']==b['enumerated_assignments']==2**len(z['jobs'])
  scale=2*a['k'];js=[(z['machines'].index(u),z['machines'].index(v),int(p*scale),int(t*scale)) for j,u,v,p,t,branch in z['jobs']];assert hashlib.sha256(json.dumps({'k':a['k'],'d':a['d'],'scale':scale,'jobs':js},sort_keys=True).encode()).hexdigest()==a['instance_sha256']
 save('expanded-inputs.json',zs);save('result.json',dict(status='PASS',python=platform.python_version(),scope='source binding / full certificate / input formulas / old-field consistency only; old owner-enumeration and matching counts NOT recomputed',source_bindings=bindings,certificate_checks=certs,expanded_closed_instances=5,expanded_long_instances=27,original_program_entries_run=0,helper_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()))
 print('PASS: 5 SHA bindings; 32 explicit inputs; 2 complete certificates; original entries run 0')
if __name__=='__main__':main()
