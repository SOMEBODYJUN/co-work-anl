from pathlib import Path
import hashlib, json, subprocess, sys
B=Path(__file__).resolve().parent; S=B/'source'; R=B/'replay'; checks=[]
def ck(n,o,d=''):
 checks.append({'name':n,'passed':bool(o),'detail':d})
 if not o: raise AssertionError(n+': '+d)
meta={
'audit_augmented_point.py':('91e6874d112b7fecbc5b','c7f46bba871c665d4a93a4bc8f76b6f2d8247467fbbaeee3c9aa19b11f6f6d4f',2180),
'audit_baseline_point.py':('2b1d51906cf8c5b3a3e8','a9fa5883aea1e10af289ce9fe3c74ffdd19640152a4a6953f0d542d997bc3ef1',2803),
'audit_root_rows.py':('9c64d4a4e9e9090f65bd','d6611270ec219682f0aced72390229023742b7a56cff2244f76b8c9ba6b5b16d',5642),
'augmented_point_audit.json':('83aa52e83fb6154f7c32','5f271cc5ea8d8588d47d1e4dd267b95f314ea4ca831f7a1df43f7840d37947ca',1054),
'baseline_point_audit.json':('ee5dad02516d63bef17d','29f974506a3aa9fea7f40b3ef7d5f11563577e2ff287a964361dc41c384a185d',395),
'audit_requery_merged.py':('68c7fb5f7e72d2c38f91','76dee096a03fb3bf4a06392ed241b91b20be8381ae7a52141c19302522536091',4533),
'requery_merged_audit.json':('20fb4ceedac54695e997','5b1f613fede0032abb90ac1251bb87deda7bb45f7be717a15d75ca2c29fa9c45',2211),
'baseline_exact_primal.json':('588745a747a28a0b4030','942b6946d6d0ee746f0c386e1634cd525ae8fdf4c4d7396d32c3057b1c238e87',2811)}
for n,(i,h,z) in meta.items():
 p=S/n; raw=p.read_bytes(); g=hashlib.sha256(raw).hexdigest(); ck('source:'+i,g==h and len(raw)==z,f'{n} sha={g} size={len(raw)}')
for n in ['audit_augmented_point.py','audit_baseline_point.py','audit_root_rows.py','audit_requery_merged.py']:
 q=subprocess.run([sys.executable,'-m','py_compile',str(S/n)],capture_output=True,text=True); ck('compile:'+n,q.returncode==0,q.stderr)
b=json.loads((S/'baseline_point_audit.json').read_text()); ck('baseline-status',b['old_rows']==235 and b['min_old_slack']=='0' and b['QL_margin'].startswith('-'),'235 old rows nonnegative with negative QL margin')
a=json.loads((S/'augmented_point_audit.json').read_text()); ck('augmented-status',a['old_generator_replay']['verified_rows']==3889 and a['root_rows']==5 and a['status'].startswith('exact feasible point'),'3889 replay + 5 root rows')
rr=json.loads((R/'root_rows_audit.json').read_text()); ck('root-row-audit',len(rr)==5 and all(x['min_residual']==0 and x['separates_old_point'] for x in rr),'five coefficient certificates independently checked')
qm=json.loads((R/'requery_merged_audit.json').read_text()); ck('merged-audit',len(qm['checks'])==4 and all(x['min_integer_residual']==0 and x['min_nonzero_type_integer_residual']>0 for x in qm['checks']),'four full-cube audits')
err=(R/'augmented_point_audit.stderr').read_text(); ck('augmented-boundary','FileNotFoundError' in err,'old canonical generator dependency tree outside claimed batch; source JSON retained')
out={'passed':True,'checks':checks,'scope':'exact necessary-row and scalar separation audits only; no SPE or six-player half theorem','boundary':'augmented old-generator replay attempted; missing frozen six_maxroot/query_closure/general_payment tree recorded, so no rerun claimed'}
(B/'validation.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
