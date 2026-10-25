"""Read-only independent reconstruction of imported HALF5 local components.

All histories are FULL five-role paths. No proof-package Python is imported.
Only exact JSON data is read; output stays in this actor's direct workspace.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import ceil,floor
import json,hashlib
HERE=Path(__file__).resolve().parent
PKG=Path.cwd()/'customer_attraction/proofs/half5_exact_v1'
COM=PKG/'components'
REPORT=[];HASH={};CHECKS=0

def read(name):
 data=(COM/name).read_bytes();HASH[name]=hashlib.sha256(data).hexdigest();return json.loads(data)
def sh(n,d):return F(n,d) if n else F(0)
def each(names):
 for v in product((0,1),repeat=len(names)):yield dict(zip(names,v))
def code(b,names):
 x=0
 for q in names:x=2*x+b[q]
 return x
def payoff(b,path,i):return sh(b[path[i]],sum(b[q] for q in path))
def floor_query(b,path,i,query):return sh(b[query],sum(b[q] for q in path[:i])+5-i)
def raw_ic(b,path,i,query,first):
 assert len(path)==5 and first<=i<=4
 return floor_query(b,path,i,query)-payoff(b,path,i)
def true_switch(b,source,child,i,first):
 assert source[:i]==child[:i] and i>=first
 return payoff(b,child,i)-payoff(b,source,i)
def tax_raw(b,path,query):
 assert len(query)==2
 p=sum(b[q] for q in path[:3]);n=sum(b[q] for q in query)
 H=payoff(b,path,3)+payoff(b,path,4)+sh(b[path[3]],(p+1)*(p+2))
 return sh(n,p+n)-H

def multipliers(c):
 lam={k:F(v) for k,v in c.get('multipliers',c.get('weights')).items()}
 assert lam and min(lam.values())>=0
 return lam

def basic_external(c,lam,beta):
 assert sum((v for k,v in lam.items() if k.startswith('CAP:')),F(0))==F(c[beta])

def run_family(family,data,names,paths,first,source_i,bits_name,gamma_name,beta_name):
 global CHECKS
 for ci,c in enumerate(data):
  lam=multipliers(c);basic_external(c,lam,beta_name)
  if family=='BG2':gam=[F(0)]+list(map(F,c[gamma_name]))
  else:gam=list(map(F,c[gamma_name]))
  def raw(b,key):
   z=key.split(':')
   if z[0]=='CAP':return F(b[z[1]])
   if family=='BG2':
    if key=='TRUE3':return true_switch(b,paths['base'],paths['query'],2,first['base'])
    if key=='TRUE4':return true_switch(b,paths['base'],paths['copy'],3,first['base'])
    if z[0]=='IC':
     pref,own,q=z[1:];p=next(x for x in paths.values() if x[1:].startswith(pref+own));i=1+len(pref)
     return raw_ic(b,p,i,q,first[next(t for t,x in paths.items() if x==p)])
   if family=='BG3':
    if key=='TRUE4-Q':return true_switch(b,paths['base'],paths['query'],3,first['base'])
    if key=='TRUE4-D':return true_switch(b,paths['base'],paths['copy'],3,first['base'])
    if z[0]=='IC':
     pref,own,q=z[1:];tag={'T':'base','TC':'base','TQ':'query','TD':'copy'}[pref];i=2+len(pref)
     assert paths[tag][i]==own
     return raw_ic(b,paths[tag],i,q,first[tag])
    if z[0]=='TAX':return tax_raw(b,paths['base'],z[1])
   if family in ('PC2','PC3'):
    if z[0]=='ACTUAL':
     i=int(z[1])-1;assert 0<=i<=4
     return sh(b[z[2]],sum(b[q] for q in 'ABCD'[:i])+5-i)
    if z[0]=='IC':
     tag={'init':'base','third':'query','fourth':'copy'}.get(z[1],z[1]);tag={'init':'base'}.get(tag,tag)
     i=int(z[2])+(1 if family=='PC2' else 2)
     return raw_ic(b,paths[tag],i,z[3],first[tag])
    if family=='PC2':
     if key=='TRUE3':return true_switch(b,paths['base'],paths['query'],2,first['base'])
     if key=='TRUE4':return true_switch(b,paths['base'],paths['copy'],3,first['base'])
     if z[0]=='TAX':
      tag={'init':'base','third':'query','fourth':'copy'}[z[1]]
      assert first[tag]<=3
      return tax_raw(b,paths[tag],z[2])
    else:
     if key=='TRUE4-F':return true_switch(b,paths['base'],paths['copy'],3,first['base'])
     if key=='TRUE4-Q':return true_switch(b,paths['base'],paths['query'],3,first['base'])
   raise AssertionError((family,key))
  if family in ('PC2','PC3'):
   expected=list(map(F,c['u_coefs' if family=='PC2' else 'u_coefficients']))
   for i in range(5):
    actual=sum((v for k,v in lam.items() if k.startswith('ACTUAL:'+str(i+1)+':')),F(0))
    if family=='PC3':actual+=int(i==2)
    assert actual==expected[i]
  mini=None;zeros=0;count=0
  for b in each(names):
   r=payoff(b,paths['base'],source_i)+sum((v*raw(b,k) for k,v in lam.items()),F(0))-gam[code(b,bits_name)]
   assert r>=0,(family,ci,b,r)
   mini=r if mini is None else min(mini,r);zeros+=not r;count+=1
  if 'zero_types' in c:assert zeros==c['zero_types']
  REPORT.append({'family':family,'index':ci,'states':count,'minimum':str(mini),'zeros':zeros});CHECKS+=count

deep=read('deep_root_query.json')
Dpaths={'base':'TABCD','query2':'TQHIJ','query3':'TAQEF','query4':'TABQG'}
Dfirst={'base':1,'query2':2,'query3':3,'query4':4}
for ci,c in enumerate(deep):
 lam=multipliers(c);basic_external(c,lam,'beta');assert lam['ROOT']==F(c['alpha'])>0
 def rawdeep(b,key):
  z=key.split(':')
  if z[0]=='CAP':return F(b[z[1]])
  if key=='ROOT':return payoff(b,Dpaths['base'],0)
  if z[0]=='IC':
   pref,own,q=z[1:];tag=next(t for t,p in Dpaths.items() if p.startswith(pref+own));i=len(pref)
   return raw_ic(b,Dpaths[tag],i,q,Dfirst[tag])
  if key.startswith('TRUE'):
   i=int(key[-1])-1
   return true_switch(b,Dpaths['base'],Dpaths['query'+key[-1]],i,Dfirst['base'])
  if z[0]=='TAX':
   pref,q=z[1:];assert len(pref)==3
   tag=next(t for t,p in Dpaths.items() if p.startswith(pref));assert 3>=Dfirst[tag]
   return tax_raw(b,Dpaths[tag],q)
  raise AssertionError(key)
 zs=0
 for b in each('TABCDEFGQHIJ'):
  r=sum((v*rawdeep(b,k) for k,v in lam.items()),F(0))+F(c['gamma'])*b['T']+F(c['zeta'])*b['T']*b['Q']-b['Q']*(1-b['T'])
  assert r>=0,('DEEP',ci,b,r);zs+=not r
 assert zs==c['zero_types'];REPORT.append({'family':'DEEP','index':ci,'states':4096,'minimum':'0','zeros':zs});CHECKS+=4096

bg2=read('background_player2.json');bg3=read('background_player3.json')
pc2=read('priced_player2.json');pc3=read('priced_player3.json')
run_family('BG2',bg2,'ATQBCDEFG',{'base':'ATBCD','query':'ATQEF','copy':'ATBQG'},{'base':2,'query':3,'copy':4},1,'ATQ','margin_coefs','Kcoef')
run_family('BG3',bg3,'ABTQCDEF',{'base':'ABTCD','query':'ABTQE','copy':'ABTDF'},{'base':3,'query':4,'copy':4},2,'ABTQ','gamma_ABTQ','beta_K')
run_family('PC2',pc2,'ABCDTQEFGHIJ',{'base':'ATEFG','query':'ATQHI','copy':'ATEQJ'},{'base':2,'query':3,'copy':4},1,'ABCDTQ','gamma','Kcoef')
run_family('PC3',pc3,'ABCDTQEFGH',{'base':'ABTEF','query':'ABTQG','copy':'ABTFH'},{'base':3,'query':4,'copy':4},2,'ABCDTQ','gamma_ABCDTQ','Kcoef')

maxroots=read('maxroot_four_copy.json')
Mpaths={'actual':'TABCD','root':'TDQRS','second':'TADXY'};Mfirst={'actual':1,'root':2,'second':3}
for ci,c in enumerate(maxroots):
 lam=multipliers(c);B,C=F(c['B']),F(c['C']);assert B>0
 assert sum((v for k,v in lam.items() if k.endswith(':pairO') or k.endswith(':lastO')),F(0))==1
 def rm(b,key,o):
  z=key.split(':')
  if z[0]=='CAP':return F(b['T']-b[z[1]])
  if z[0]=='copy':
   i={'root':1,'second':2}[z[1]]
   return -true_switch(b,Mpaths['actual'],Mpaths[z[1]],i,Mfirst['actual'])
  path=Mpaths[z[0]]
  if z[1].isdigit():return -raw_ic(b,path,int(z[1])+1,z[3],Mfirst[z[0]])
  if z[1]=='pairO':
   p=sum(b[q] for q in path[:3]);H=payoff(b,path,3)+payoff(b,path,4)+sh(b[path[3]],(p+1)*(p+2))
   return F(5,2)*H+sh(p,p+1)-o
  if z[1]=='lastO':
   p=sum(b[q] for q in path[:4]);return 5*payoff(b,path,4)+sh(p,p+1)-o
  raise AssertionError(key)
 zs=0
 for b in each('TABCDQRSXY'):
  r=B*payoff(b,'TABCD',0)+C*b['T']-sum((v*rm(b,k,0) for k,v in lam.items()),F(0))
  r1=B*payoff(b,'TABCD',0)+C*b['T']-1-sum((v*rm(b,k,1) for k,v in lam.items()),F(0))
  assert r>=0 and r==r1 and (r*245803508760).denominator==1
  zs+=not r
 assert zs==56;REPORT.append({'family':'MAXROOT','index':ci,'states':1024,'minimum':'0','zeros':zs,'legacy_JSON_states':c['states'],'legacy_JSON_zeros':c['zero_types']});CHECKS+=1024

mb=read('max_background_player2.json');lam=multipliers(mb)
B,C,ga,gt=map(F,(mb['B'],mb['C'],mb['gammaA'],mb['gammaT']))
assert B==lam['FORCED'] and F(mb['Acoef'])==ga
assert C==gt+sum(v for k,v in lam.items() if k.startswith('CAP:'))
P={'init':'ATBCD','third':'ATDEF'};first={'init':2,'third':3}
def rmb(b,key,d):
 z=key.split(':')
 if z[0]=='CAP':return F(b[z[1]])
 if key=='FORCED':return payoff(b,P['init'],1)
 if key=='TRUE3':return true_switch(b,P['init'],P['third'],2,first['init'])
 if z[0] in ('IC','OPT'):
  path=P[z[1]];i=int(z[2])+1;assert i>=first[z[1]]
  if z[0]=='IC':return raw_ic(b,path,i,z[3],first[z[1]])
  return sh(d,sum(b[q] for q in path[:i])+5-i)-5*payoff(b,path,i)
 if z[:2]==['PAIR','OPT']:
  path=P[z[2]];p=sum(b[q] for q in path[:3]);H=payoff(b,path,3)+payoff(b,path,4)+sh(b[path[3]],(p+1)*(p+2))
  return sh(d*(5-d),p+1)+sh(d*(d-1),p+2)-10*H
 raise AssertionError(key)
zs=0
for b in each('ATBCDEF'):
 for d in range(6):
  r=sum((v*rmb(b,k,d) for k,v in lam.items()),F(0))+gt*b['T']+ga*b['A']-int(d>0)
  assert r>=0;zs+=not r
assert zs*2==mb['zero_types'];REPORT.append({'family':'MAX-BG2','index':0,'states':768,'minimum':'0','zeros':zs});CHECKS+=768

# Independently rebuild every outward-rounded frozen source table.
S=10**6;manifest=json.loads((PKG/'row_manifest.json').read_text())
BG=[]
for i in (0,1,3,5,11,12):
 c=bg2[i];BG.append([ceil(S*F(c['Kcoef'])),[0]+[floor(S*F(x)) for x in c['margin_coefs']],1])
for c in bg3[:3]:BG.append([ceil(S*F(c['beta_K'])),[floor(S*F(x)) for x in c['gamma_ABTQ']],2])
PC=[]
for i,c in enumerate(pc2+pc3):
 g=list(map(F,c['gamma'] if i<5 else c['gamma_ABCDTQ']));u=list(map(F,c['u_coefs'] if i<5 else c['u_coefficients']))
 if i<5:u[1]+=1
 PC.append([ceil(S*F(c['Kcoef'])),[floor(S*x) for x in g],[ceil(S*x) for x in u]])
DEEP=[[ceil(S*F(c[x])) for x in ('alpha','beta','gamma')]+[S,ceil(S*F(c['zeta']))] for c in deep]
assert BG==manifest['BG'] and PC==manifest['PC'] and DEEP==manifest['DEEP']
assert [ceil(S*F(maxroots[0][x])) for x in ('B','C')]==[46313177,-7412362]
for key,record in manifest['sources'].items():
 assert record['sha256']==HASH[Path(record['path']).name]
assert len(REPORT)==36 and CHECKS==47872
out={'status':'PASS_independent_global_path_local_reconstruction','components':len(REPORT),'coefficient_states':CHECKS,'frozen_outward_tables':'BG9_PC8_DEEP3_MAXROOT_match','input_sha256':HASH,'checks':REPORT,'scope':'Local components and rounding only; global integer identity is reviewed separately by other seats.'}
(HERE/'audit_imported_half5_local_independent.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('checks','input_sha256')},indent=2))
