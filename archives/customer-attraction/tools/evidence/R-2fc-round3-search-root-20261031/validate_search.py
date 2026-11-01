from pathlib import Path
from fractions import Fraction
from itertools import product
import json,hashlib,subprocess,sys
ROOT=Path(__file__).parent; SRC=ROOT/'source'; checks=[]
def ck(n,ok,d=''):
 checks.append({'name':n,'passed':bool(ok),'detail':d})
 if not ok: raise AssertionError(n+': '+d)
exp={'m5p7_pos1.best.json':('9c75460d08c374607940',331302),'m5p7_pos1.json':('de736e9d061300a93280',28503),'m5p7_pos2_multi.best.json':('089592c096af119504ad',331516),'m5p7_pos2_multi.json':('3f0db73541b98afb1119',51768),'m5p8_pos0_multi.best.json':('10f6ed4f50c00ddd45eb',554386),'m5p8_pos0_multi.json':('2a2166a3cfd559a80fac',19376),'unit_point_audit.json':('d6bc176f1ca2ecaedc20',5203)}
for n,(sid,size) in exp.items(): ck('source:'+sid,(SRC/n).stat().st_size==size)
def utility(inst,path,i):
 vals=[]
 for c in inst['customers']:
  if int(path[i]) in c['topics']:
   load=sum(int(a) in c['topics'] for a in path)
   vals.append(Fraction(c['multiplicity'],load))
 return sum(vals,Fraction(0))
def welfare(inst,path):
 return sum(c['multiplicity'] for c in inst['customers'] if any(int(a) in c['topics'] for a in path))
def verify_best(name,expected):
 x=json.load(open(SRC/name)); inst=x['instance']; q=len(inst['topics']); m=inst['players']; amap={tuple(a['history']):a['action'] for a in x['strategy']['actions']}
 ck(name+'-action-count',len(amap)==sum(q**d for d in range(m)))
 def finish(h):
  h=tuple(h)
  while len(h)<m: h=h+(amap[h],)
  return h
 strict=ties=comp=0; minslack=None
 for d in range(m):
  for h in product(range(q),repeat=d):
   on=utility(inst,finish(h),d)
   for a in range(q):
    off=utility(inst,finish(h+(a,)),d); s=on-off; ckval=s>=0
    if not ckval: raise AssertionError(f'{name} deviation {h} {a} {s}')
    strict+=s>0; ties+=s==0; comp+=1; minslack=s if minslack is None or s<minslack else minslack
 actual=finish(())
 opt=max(welfare(inst,h) for h in product(range(q),repeat=m))
 w=welfare(inst,actual)
 ck(name+'-exact-values',(w,opt,actual)==expected,f'{w},{opt},{actual}')
 ck(name+'-full-history',x.get('full_strategy_verified') is True and minslack>=0,f'comparisons={comp},strict={strict},ties={ties},min={minslack}')
 return {'name':name,'W':w,'OPT':opt,'actual':actual,'comparisons':comp,'strict':strict,'ties':ties,'minimum_slack':str(minslack)}
results=[]
results.append(verify_best('m5p7_pos1.best.json',(6,9,(0,2,0,0,0))))
results.append(verify_best('m5p7_pos2_multi.best.json',(5,9,(0,0,5,0,0))))
results.append(verify_best('m5p8_pos0_multi.best.json',(6,9,(0,7,2,2,0))))
for n,expected_records in [('m5p7_pos1.json',35),('m5p7_pos2_multi.json',65),('m5p8_pos0_multi.json',30)]:
 x=json.load(open(SRC/n)); ck(n+'-scan',x['finished_steps']==expected_records and x['best']=='9' and len(x['records'])>0 and 'absence of counterexample' in x['scope'])
unit=json.load(open(SRC/'unit_point_audit.json')); ck('unit-audit-shape',len(unit)==6 and all(r['full_history_SPE'] and not r['violations'] and 2*r['W']>=r['OPT'] for r in unit))
out={'passed':True,'checks':checks,'exact_best_replays':results,'scope':'fixed finite full-history SPE certificates and finite cone scans; no universal claim'}
(ROOT/'validation.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
