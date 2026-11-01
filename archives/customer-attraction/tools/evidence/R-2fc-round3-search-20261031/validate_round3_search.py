from pathlib import Path
import json,hashlib,subprocess,sys
ROOT=Path(__file__).parent; SRC=ROOT/'source'; REP=ROOT/'replay'; checks=[]
def ck(n,ok,d=''):
 checks.append({'name':n,'passed':bool(ok),'detail':d})
 if not ok: raise AssertionError(n+': '+d)
exp={'audit_unit_points.py':('83a42a07eae9a400150d',3377,'183ee79f333a234d699492b91df7bd4685812afb11b054b5c7c89f1bea32dc31'),'early_floor_walk.py':('223f74fca6d37c18fdf9',8593,'8d38d60183300505b2856640d2b5111283a02890166db23896943bf2102c1f22'),'m4p6_pos0.best.json':('a8d5b27abbbcfae828e1',28184,'ce4c144f4a09b6c222922348ada830c1b90a213f8fc3a5c54e04a53f86f061bd'),'m4p6_pos0.json':('164ca0aa0fdcaaeb6af0',25251,'8550f8a6a0f9e3d70d89313bfb0af2e47c344f57bc5cdb608a2aff69ad8590ac'),'m4p6_pos0_multi.best.json':('1e45ceb2591765fa9584',28261,'84aae4b0477880fca968edaa9c692c8f892531b3ca020823eaa246018d8b2af7'),'m4p6_pos0_multi.json':('1608f33929033f9e4965',43191,'648bc279b0bfac439bf61c311bb28627e357a5aa1125bcaba438da55c5407b1d'),'m5p7_pos0_multi.best.json':('9b1eb844ff4eaeebcf18',331516,'227aa87f3c519727f5dcb90af09127e8d1073b0b0919eeee1c20625ef30b87fe'),'m5p7_pos0_multi.json':('43ed0717ee68eeba171c',46821,'ada1e1ba082fc7c94f9d301fddac99d782e47d469c7298eff285c4c821f03d1f')}
for n,(sid,size,sha) in exp.items():
 b=(SRC/n).read_bytes(); ck('source:'+sid,len(b)==size and hashlib.sha256(b).hexdigest()==sha,f'{n} {len(b)}')
for p in SRC.glob('*.py'):
 r=subprocess.run([sys.executable,'-m','py_compile',str(p)],capture_output=True,text=True); ck('compile:'+p.name,r.returncode==0,r.stderr)
for n,expected_steps,expected_cones,expected_best in [('m4p6_pos0.json',35,33,'7'),('m4p6_pos0_multi.json',65,54,'7'),('m5p7_pos0_multi.json',65,56,'9')]:
 x=json.load(open(SRC/n)); ck(n+'-search',x['scope'].startswith('finite full-history SPE cones') and x['finished_steps']==expected_steps and x['cones']==expected_cones and x['best']==expected_best and 'absence of counterexample is not proof' in x['scope'])
for n,players,ratio,W,O in [('m4p6_pos0.best.json',4,'7',5,7),('m4p6_pos0_multi.best.json',4,'7',5,7),('m5p7_pos0_multi.best.json',5,'9',6,9)]:
 x=json.load(open(SRC/n)); ck(n+'-exact-candidate',x['full_strategy_verified'] is True and x['ratio']==ratio and x['u']=='1' and x['W']==W and x['OPT']==O and x['scope'].startswith('one genuine complete-history pure SPE'))
ua=json.load(open(REP/'unit_points_audit.json')); ck('unit-point-audit',len(ua)==3 and all(x['full_history_SPE'] and x['minimum_slack']=='0' and x['half_gap']>0 for x in ua) and [(x['players'],x['W'],x['OPT'],x['individual_ratio']) for x in ua]==[(4,5,7,'7'),(4,5,7,'7'),(5,6,9,'9')])
ck('unit-point-clean',(REP/'unit_points.stderr').read_text()=='' and (REP/'unit_points.stdout').stat().st_size>0)
# early_floor_walk has frozen source dependencies outside this batch; source was read/compiled, so runtime is explicitly bounded.
ck('early-floor-dependency-boundary', not (SRC/'early_floor_walk.py').read_text().find("R-18e993ca519949aba29e030d3d7b15b3")<0)
out={'passed':True,'checks':checks,'scope':'finite full-history cone search and exact audits of recovered best points; no universal floor/half theorem','search_reports':{'m4p6':{'steps':35,'cones':33,'best':'7'},'m4p6_multi':{'steps':65,'cones':54,'best':'7'},'m5p7_multi':{'steps':65,'cones':56,'best':'9'}},'exact_candidates':[{'players':x['players'],'W':x['W'],'OPT':x['OPT'],'ratio':x['individual_ratio'],'half_gap':x['half_gap']} for x in ua], 'dependency_note':'early_floor_walk.py imports frozen R-18e993ca... engines absent from this batch; canonical best JSONs were independently audited.'}
(ROOT/'validation.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
