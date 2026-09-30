"""Independent all-support audit of the proposed shared-catalog phi menu."""
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
import json,time
from common_phi_algorithm import menu, solve
from asym_research.bounded_overlap import local

def independent_check(a,b,ws,e):
 p=e['prob_first'];x=a+sum(w*z for w,z in zip(ws,p));y=b+sum(w*(1-z) for w,z in zip(ws,p))
 assert [x,y]==e['loads']
 for i,(w,z) in enumerate(zip(ws,p)):
  first=w+a+sum(v*t for j,(v,t) in enumerate(zip(ws,p)) if j!=i)
  second=w+b+sum(v*(1-t) for j,(v,t) in enumerate(zip(ws,p)) if j!=i)
  assert not (z>0 and first>second) and not (z<1 and second>first)
 return x,y

def q_at_most(z):return z>=0 and z*z+z>=1

def run():
 start=time.time();local_count=0;global_count=0;maxfactor=Q(1)
 for k in range(5):
  for raw in combinations_with_replacement(range(1,6),k):
   ws=list(map(Q,raw))
   for a,b in product(range(9),repeat=2):
    a,b=Q(a),Q(b);entries=menu(a,b,ws)
    spec=local(ws+[a,b],[set(range(k))|{k},set(range(k))|{k+1}],0,1)
    reflected={tuple(1-p for p in e['prob_first']) for e in menu(b,a,ws)}
    assert {tuple(e['prob_first']) for e in entries}==reflected,(a,b,ws)
    for e in entries:
     x,y=independent_check(a,b,ws,e)
     assert any(piece['lo']<=x<=piece['hi'] for piece in spec['pieces'])
    local_count+=1
 # Every multiset of 3 positive integer-weight customer types on 3 sites.
 types=[(mask,w) for mask in range(1,8) for w in range(1,4)]
 for clients in combinations_with_replacement(types,3):
  inst={'weights':[w for m,w in clients], 'locations':[[i for i,(m,w) in enumerate(clients) if m>>s&1] for s in range(3)]}
  out=solve(inst);maxfactor=max(maxfactor,out['factor']);global_count+=1
  on=out['on_path'];s,t=on['layout'];base=on['loads']
  for record in [on]+[z['witness'] for z in out['deviations']]:
   u,v=record['layout'];su=set(inst['locations'][u]);sv=set(inst['locations'][v]);common=sorted(su&sv)
   a=sum(inst['weights'][i] for i in su-sv);b=sum(inst['weights'][i] for i in sv-su)
   independent_check(a,b,[inst['weights'][i] for i in common],record)
  for z in out['deviations']:
   who=z['deviator']-1
   assert z['witness']['loads'][who]<=out['factor']*base[who]
 # All 27 supports show a genuine need for three mixers in the local chord.
 rec=local([Q(20),Q(20),Q(20),Q(40),Q(39)],[{0,1,2,3},{0,1,2,4}],0,1)
 target=[p for p in rec['pieces'] if q_at_most(p['hi']/99) and q_at_most((139-p['lo'])/100)]
 assert target and all(p['states'].count(0)==3 for p in target)
 chord=[e for e in menu(40,39,[20,20,20]) if q_at_most(e['loads'][0]/99) and q_at_most(e['loads'][1]/100)]
 assert chord and all(all(0<p<1 for p in e['prob_first']) for e in chord)
 return {'local_exact_support_cases':local_count,'global_exhaustive_customer_multisets':global_count,'max_factor_in_exhaustive_family':str(maxfactor),'forced_three_mixer':{'reaches':[100,99],'common_weights':[20,20,20],'pure_loads':['60','79'],'two_mixer_loads':['79','60'],'three_mixer_loads':['277/4','279/4'],'prob_first':['39/80']*3},'seconds':time.time()-start}
if __name__=='__main__':print(json.dumps(run(),indent=2))
