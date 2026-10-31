from pathlib import Path
from fractions import Fraction as F
from itertools import product
import argparse,json,hashlib
if not __debug__:raise RuntimeError('assertions required')
a=argparse.ArgumentParser();a.add_argument('--input',required=True);a.add_argument('--output',required=True);a=a.parse_args()
ip=Path(a.input);raw=ip.read_bytes();d=json.loads(raw);assert d['schema']=='new-MD-transcription-not-original-JSON' and d['players']==3 and d['topics']==7
units=[t['mask'] for t in d['types'] for _ in range(t['count'])];assert len(units)==24 and len(d['types'])==15 and all(0<m<64 for m in units)
def policy(h):
 if len(h)==0:return d['policy']['root']
 if len(h)==1:return d['policy']['second_after_first'][h[0]]
 assert len(h)==2
 present=[x for x in h if x<6]
 if len(present)==0:return d['policy']['two_empty_reply']
 if len(present)==1:return d['policy']['one_nonempty_reply'][present[0]]
 start=0 if h[1]<3 else 3
 return min(x for x in range(start,start+3) if x not in h)
def leaf(h):
 h=tuple(h)
 while len(h)<3:h=h+(policy(h),)
 return h
def load(mask,z):return sum(bool(mask&(1<<x)) for x in z)
def payoff(z,i):return sum((F(1,load(m,z)) for m in units if m&(1<<z[i])),F(0))
def query(z,t):return sum((F(1,1+load(m,z)) for m in units if m&(1<<t)),F(0))
def potential(z):return sum((sum((F(1,j) for j in range(1,load(m,z)+1)),F(0)) for m in units),F(0))
def coverage(z):return sum(load(m,z)>0 for m in units)
rows=[];nodes=[]
for depth in range(3):
 for h in product(range(7),repeat=depth):
  prescribed=policy(h);assert 0<=prescribed<7
  z=leaf(h);val=payoff(z,depth);nodes.append({'history':list(h),'action':prescribed,'terminal':list(z),'payoff':str(val)})
  for alt in range(7):
   y=leaf(h+(alt,));other=payoff(y,depth);slack=val-other;assert slack>=0,(h,prescribed,alt,z,y,val,other)
   rows.append({'history':list(h),'prescribed':prescribed,'alternative':alt,'prescribed_terminal':list(z),'alternative_terminal':list(y),'prescribed_payoff':str(val),'alternative_payoff':str(other),'slack':str(slack)})
assert len(nodes)==57 and len(rows)==399
Z=[leaf((b,)) for b in range(7)];D=[payoff(z,0) for z in Z];U=max(D);PHI=[potential(z) for z in Z];K=[[query(z,t) for z in Z] for t in range(7)];caps=[max(K[t][b] for t in range(7)) for b in range(7)]
assert Z==[(0,3,4),(1,3,4),(2,3,4),(3,0,1),(4,0,1),(5,0,1),(6,0,1)]
assert D==[F(35,6)]*6+[F(0)] and PHI==[F(143,6)]*6+[F(18)]
assert caps==[F(11,2),F(73,12),F(16,3),F(11,2),F(73,12),F(16,3),F(41,6)]
assert K[2][4]==F(73,12) and K[2][4]-U==F(1,4) and PHI[2]==PHI[4]==max(PHI)
assert [K[t][0] for t in range(7)]==[F(43,12),F(11,2),F(21,4),F(47,12),F(43,12),F(11,2),F(0)]
actual=leaf(());pay=[payoff(actual,i) for i in range(3)];assert actual==(0,3,4) and pay==[F(35,6),F(41,6),F(19,3)] and coverage(actual)==19 and sum(pay)==19
result={'run_kind':'new independent definition-level24unit check, not originalCLI or replay','source_id':d['source_id'],'source_sha256':d['source_sha256'],'derived_input_sha256':hashlib.sha256(raw).hexdigest(),'expanded_unit_clients':len(units),'complete_policy_nodes':len(nodes),'IC_including_self':len(rows),'IC_nonself':sum(r['prescribed']!=r['alternative'] for r in rows),'minimum_slack':str(min(F(r['slack']) for r in rows)),'policy':nodes,'all_IC':rows,'root_columns':[{'root':b,'terminal':list(Z[b]),'original_root_payoff':str(D[b]),'Phi':str(PHI[b]),'query_cap':str(caps[b])} for b in range(7)],'K_rows_query_columns_root':[[str(v) for v in row] for row in K],'actual':list(actual),'actual_payoffs':[str(v) for v in pay],'actual_W':19,'root_u':str(U),'bad_maxPhi_column':{'column':4,'query':2,'K':str(K[2][4]),'u_gap':str(K[2][4]-U),'Phi_source':str(PHI[4]),'Phi_query_source':str(PHI[2])},'good_maxPhi_column':{'column':0,'query_vector':[str(K[t][0]) for t in range(7)],'cap':str(caps[0]),'strict_margin':str(U-caps[0])},'not_checked':['791sourceinstance','originalcode/output bytes or CLI','genericpotentialordering or generalCAG','OPT enumeration/globalminimality/externalreview'],'status':'PASS all actual24policy IC and statedK/Phi/root numbers'}
op=Path(a.output)
with op.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'status':result['status'],'nodes':len(nodes),'IC':len(rows),'root_u':str(U),'actual_W':19,'bad_gap':'1/4','good_margin':'1/3','report':str(op)},ensure_ascii=False))
