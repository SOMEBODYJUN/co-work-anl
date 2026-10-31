from pathlib import Path
import json,hashlib,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'source'; REP=ROOT/'replay'; checks=[]
def chk(name,ok,detail=''):
 checks.append({'name':name,'passed':bool(ok),'detail':detail})
 if not ok: raise AssertionError(f'{name}: {detail}')
expected={
'root_potential_independent_audit.json':('831052265f6603650b50',626,'352231ee37526268bb365601877d6444cb43c81361c5d238de7292edef6294b9','10c0a5e7bccaf653921abd53b11cb98395a53b50'),
'root_potential_independent_audit.py':('aad3b319edcc95b5d6d7',4159,'dd3c639f46976685c9eae2512f1f0b381a54e23703d23c0acab0a3d6948bcddc','6e8869feeec2483b26b44734e367dcf8102b8bed'),
'truncated_potential_audit.json':('d7389f400d38f77ec31d',600,'ef5c669b9a751127707a71ec7e51175de2818978ca70344b13426299a38aa882','1813da2ab368689e906a7d95269b771c0f42f21e'),
'truncated_potential_probe.py':('900e8c0df5857ce636c5',3191,'3e1121b31d491c80d92592de0201e32ec4a4fb6890e261980ca3e6bcb8004f1d','e2825c17e9dd0050979758881418d39d1dc75711'),}
for n,(sid,size,sha,blob) in expected.items():
 p=SRC/n;b=p.read_bytes();chk('source:'+sid,len(b)==size and hashlib.sha256(b).hexdigest()==sha,f'{n} {len(b)} {hashlib.sha256(b).hexdigest()}')
for p in SRC.glob('*.py'):
 r=subprocess.run([sys.executable,'-m','py_compile',str(p)],capture_output=True,text=True);chk('py_compile:'+p.name,r.returncode==0,r.stderr)
root=json.loads((SRC/'root_potential_independent_audit.json').read_text())
tr=json.loads((SRC/'truncated_potential_audit.json').read_text())
rout=json.loads((REP/'root/root.stdout.json').read_text()); minout=json.loads((REP/'root/minimized.stdout.json').read_text())
chk('root-json-exact',root['N']==78 and root['terminal']==[1,5,5] and root['W']==54 and root['OPT']==75 and root['Phi']=='141/2' and root['Psi']=='141/2' and root['comparisons_including_self']==258 and root['nonself_comparisons']==215 and root['minimum_slack']=='0' and root['half_slack']==33)
chk('root-independent-replay',rout['N']==root['N'] and rout['terminal']==root['terminal'] and rout['W']==root['W'] and rout['OPT']==root['OPT'] and rout['Phi']==root['Phi'] and rout['Psi']==root['Psi'] and rout['comparisons_including_self']==root['comparisons_including_self'] and rout['nonself_comparisons']==root['nonself_comparisons'] and rout['minimum_slack']==root['minimum_slack'])
chk('minimized-replay',minout.get('status')=='passed' and minout['N']==11 and minout['terminal']==[1,5,5] and minout['W']==8 and minout['OPT']==11 and minout['Phi']=='21/2' and minout['comparisons']==258 and minout['min_slack']=='0')
chk('truncated-json-matches',tr['clients']==78 and tr['actual']==[1,5,5] and tr['W']==54 and tr['OPT']==75 and tr['Phi']=='141/2' and tr['truncated_Phi']=='141/2' and tr['difference']=='-9/2' and tr['comparisons']==258 and tr['minimum_slack']=='0')
chk('truncated-probe-smoke', (REP/'truncated/probe.stderr.txt').read_text()=='' and 'completed 3 q 6 r 3' in (REP/'truncated/probe.stdout.txt').read_text())
chk('no-half',2*root['W']>root['OPT'] and 2*tr['W']>tr['OPT'] and 2*minout['W']>minout['OPT'])
result={'passed':True,'checks':checks,'source_count':4,'root':{'N':root['N'],'W':root['W'],'OPT':root['OPT'],'Phi':root['Phi'],'Psi':root['Psi'],'half_slack':root['half_slack']},'minimized':{'N':minout['N'],'W':minout['W'],'OPT':minout['OPT'],'Phi':minout['Phi']},'truncated_audit':{'clients':tr['clients'],'W':tr['W'],'OPT':tr['OPT'],'Phi':tr['Phi'],'difference':tr['difference']},'scope':'exact fixed strategy/candidate replay; truncated probe finite floating discovery only; no general half theorem'}
(ROOT/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
