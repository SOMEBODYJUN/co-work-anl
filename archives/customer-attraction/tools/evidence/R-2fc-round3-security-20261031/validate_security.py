from pathlib import Path
import json,hashlib,subprocess,sys
ROOT=Path(__file__).parent; SRC=ROOT/'source'; REP=ROOT/'replay'; checks=[]
def ck(n,ok,d=''):
 checks.append({'name':n,'passed':bool(ok),'detail':d})
 if not ok: raise AssertionError(n+': '+d)
exp={'rank_seed_n4k6.json':('fbcf94d7d56d7caa5194',431,'9c11f9bbd6cbb8c30d8a0f0d1786636aafb29eaf08ae4a1940be29d13f182431'),'support_budget_probe.py':('8f75516e0d666eaec162',7156,'8f99e7fa7bb3f13263a072fb575a1e50e9cd967d14cbcbe16a7e2ffa1bd2b369'),'support_groups_n3k6.json':('871d0ff222c2d25860ea',2904,'6e000b82d08e9b4bce9cd7f774da2172d997fc2f9d85dd0630dbb1007faeb234'),'support_submod_alternating_n4k6.json':('2447b78ca867b0cb4499',443,'a0e14bf8c2d7d76762ee1d0467341ca2a81517827eec8e59a4b230369338d59d'),'support_submod_groups_n3k6.json':('d7a108152b68d2f4c2bb',440,'c0e2c763ccb2688ed548d098e1810445a9d18d581d79dbfc74d6e8ef1a2971f1'),'support_submod_n5k6.json':('fee9e4d7bfc43dae6fe2',432,'b771bd4df6a179028e8b23f227ac3c76169022dda1a09867fc45da07070aa13b')}
for n,(sid,size,sha) in exp.items():
 b=(SRC/n).read_bytes(); ck('source:'+sid,len(b)==size and hashlib.sha256(b).hexdigest()==sha,f'{n} {len(b)}')
r=subprocess.run([sys.executable,'-m','py_compile',str(SRC/'support_budget_probe.py')],capture_output=True,text=True); ck('compile',r.returncode==0,r.stderr)
for n in ['rank_seed_n4k6.json','support_groups_n3k6.json','support_submod_alternating_n4k6.json','support_submod_groups_n3k6.json','support_submod_n5k6.json']:
 x=json.load(open(SRC/n)); ck(n+'-scope',x['status']=='EXPLORATORY_LARGER_MODEL_NOT_CAG' and int(x['completed'])>0)
rank=json.load(open(SRC/'rank_seed_n4k6.json')); ck('rank-finite',rank['best']==0.0 and rank['completed']==100)
group=json.load(open(SRC/'support_groups_n3k6.json')); ck('group-witness-finite',group['best']<0 and group['completed']==1 and 'witness' in group, f"best={group['best']}")
for n in ['submod_smoke.stderr','groups_smoke.stderr']:
 ck('smoke-clean:'+n,(REP/n).read_text()=='')
for n in ['submod_smoke.json','groups_smoke.json']:
 x=json.load(open(REP/n)); ck('smoke:'+n,x['status']=='EXPLORATORY_LARGER_MODEL_NOT_CAG' and x['completed']==1)
out={'passed':True,'checks':checks,'scope':'larger support-budget DR exploratory LP class, explicitly outside CAG; finite reports and smoke only','reports':{'rank_best':rank['best'],'group_best':group['best'],'group_witness_present':True},'migration':'none; no CAG/SPE/half conclusion'}
(ROOT/'validation.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
