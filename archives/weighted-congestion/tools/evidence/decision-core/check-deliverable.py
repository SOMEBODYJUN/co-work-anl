#!/usr/bin/env python3
"""Check the owned decision-core deliverable only; no source execution or Git."""
import hashlib,json,re
from pathlib import Path
import yaml
r=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
e=r/'archives/weighted-congestion/tools/evidence/decision-core'
cache=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache')
receipts=json.loads((r/'cleanup/workspaces/Boss4/decision-core-receipts.json').read_text())
sources=json.loads((e/'provenance.json').read_text())['sources']
owned=sorted({Path(t) for x in receipts for t in x['targets'] if '唯一精确均衡' not in t})
errors=[];links=0;ids={}
# Only read stable-ID header lines elsewhere. Unrelated YAML is not parsed.
for p in (r/'archives/weighted-congestion/state').rglob('*.md'):
 m=re.search(r'^id:\s*["\']?([^\n"\']+)',p.read_text(),re.M)
 if m:ids.setdefault(m.group(1),[]).append(str(p.relative_to(r)))
for q in owned:
 p=r/q;t=p.read_text();m=re.match(r'^---\n(.*?)\n---',t,re.S)
 if not m:errors.append(str(q)+' missing YAML');continue
 x=yaml.safe_load(m.group(1))
 for k in ['id','kind','type_tag','title','status','summary','source_refs']:
  if not x.get(k):errors.append(str(q)+' missing '+k)
 if len(ids.get(x['id'],[]))!=1:errors.append(str(q)+' duplicate id')
 for ref in x['source_refs']:
  if not re.match(r'^source:[0-9a-f]{40}:.+',ref):errors.append(str(q)+' malformed ref '+ref)
 for target in re.findall(r'\]\(([^)]+)\)',t):
  if re.match(r'\w+://',target) or target.startswith('#'):continue
  links+=1
  if not (p.parent/target.split('#')[0]).exists():errors.append(str(q)+' broken '+target)
for s in sources:
 for root in [e/'original',cache]:
  if hashlib.sha256((root/s['path']).read_bytes()).hexdigest()!=s['sha256']:errors.append(s['id']+' source hash')
related=json.loads((e/'related-provenance.json').read_text())['sources']
for s in related:
 if hashlib.sha256((e/'related'/s['path']).read_bytes()).hexdigest()!=s['sha256']:errors.append(s['id']+' related hash')
if len(receipts)!=20 or {x['id'] for x in receipts}!={s['id'] for s in sources}:errors.append('receipt coverage')
for x in receipts:
 if any(x.get(k) is not True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']):errors.append(x['id']+' false semantic field')
 for t in x['targets']:
  if not (r/t).is_file():errors.append(x['id']+' missing target '+t)
 if x['id']=='7a622b6e381cd0e3104e' and ('二次资源1+2x²' not in x['read_note'] or '线性资源' in x['read_note']):errors.append('single-player read_note coefficient description')
comp=json.loads((e/'replay-comparison.json').read_text())
if not all(x['exit_code']==0 and x['all_fields_equal'] and not x['differences'] for x in comp['runs']):errors.append('replay comparison')
for n in ['related-search.json','primary-source-check-attempt.json']:
 json.loads((e/n).read_text())
out={'status':'passed' if not errors else 'failed','owned_objects':len(owned),'owned_sources':len(sources),'receipt_count':len(receipts),'local_links_checked':links,'source_hashes_checked':2*len(sources),'related_hashes_checked':len(related),'replay_runs_equal':len(comp['runs']),'scope':'Owned mathematical/source/receipt deliverable; no expansion of unrelated YAML scan and no repetition of already passed source audits.','errors':errors}
(e/'self-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
