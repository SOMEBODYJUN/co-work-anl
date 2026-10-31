#!/usr/bin/env python3
"""New readonly archived-byte binding; does not execute archived programs."""
from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parent
R=B.parent.parent/'boss4-research'
x=json.loads((B/'research/branch_cleanup.json').read_text())
rows=[json.loads(l) for l in (R/'cleanup/inventory.jsonl').read_text().splitlines()]
idx={r['path']:r for r in rows if any(s['commit']=='68fad804ec5946cb296f77dc5b336308a66abf12' for s in r['sources'])}
out=[]
for i,row in enumerate(x['archived_sources']):
 record={'index':i,**row,'scope':'byte binding only; neither mathematical proof review nor current remote branch audit'}
 for label,spec in [('original',row['commit']+':'+row['original_path']),('frozen_archive',idx[row['archived_path']]['blob'])]:
  proc=subprocess.run(['git','cat-file','blob',spec],cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  if proc.returncode:record[label]={'available':False,'returncode':proc.returncode,'stderr':proc.stderr.decode(errors='replace')[:1000]}
  else:record[label]={'available':True,'bytes':len(proc.stdout),'sha256':hashlib.sha256(proc.stdout).hexdigest(),'equals_record':len(proc.stdout)==row['bytes'] and hashlib.sha256(proc.stdout).hexdigest()==row['sha256']}
 out.append(record)
report={'scope':'new readonly Git object byte hashes for141declared archived routes; no old program, ancestry, remote or mathematical suite repeated','records':out,'count':len(out),'all_original_and_archive_bytes_match_record':all(r[k].get('equals_record') for r in out for k in ['original','frozen_archive'])}
(B/'archived-blob-bindings.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'records':len(out),'unavailable':sum(not r[k]['available'] for r in out for k in ['original','frozen_archive']),'all_original_and_archive_bytes_match_record':report['all_original_and_archive_bytes_match_record']},ensure_ascii=False))
