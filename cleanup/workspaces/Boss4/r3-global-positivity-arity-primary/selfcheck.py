from pathlib import Path
import hashlib,json,re
S=Path(__file__).resolve().parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=Path(__file__).parent
E=S/'archives/customer-attraction/tools/evidence/global-positivity-arity-primary'
errors=[];files=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 rel=str(p.relative_to(S));b=p.read_bytes()
 if p.suffix=='.json':
  try:json.loads(b)
  except Exception as e:errors.append([rel,'bad-json',str(e)])
 if p.suffix=='.md':
  try:s=b.decode('utf-8')
  except UnicodeDecodeError as e:errors.append([rel,'bad-utf8',str(e)]);continue
  bad=[(i,x) for i,x in enumerate(b) if x<32 and x not in (9,10,13)]
  if bad:errors.append([rel,'C0',bad[:10]])
  if re.search(r'\t(?:ag|ext)\b',s):errors.append([rel,'interpreted-TeX-tab'])
  if rel.startswith('archives/customer-attraction/state/'):
   for key in ('id:','kind:','type_tag:','title:','status:','summary:','source_refs:'):
    if key not in s:errors.append([rel,'missing-frontmatter',key])
  linkbase=p.parent
  try:original_rel=p.relative_to(E/'comparison');linkbase=(R/original_rel).parent
  except ValueError:pass
  for dest in re.findall(r'\]\(([^)]+)\)',s):
   if '://' in dest or dest.startswith('#'):continue
   dest=dest.split('#')[0]
   if not dest:continue
   st=(linkbase/dest).resolve()
   if st.exists():continue
   try:r=st.relative_to(S)
   except ValueError:errors.append([rel,'broken-link-original-location',dest]);continue
   if not (R/r).exists():errors.append([rel,'broken-link',dest])
 if p.name not in {'selfcheck.json','copy-files.json'}:files.append({'path':rel,'size':len(b),'sha256':hashlib.sha256(b).hexdigest()})
source=json.loads((E/'source-manifest.json').read_text())['rows']
for a in source:
 b=(S/a['evidence_path']).read_bytes()
 if len(b)!=a['size'] or hashlib.sha256(b).hexdigest()!=a['sha256']:errors.append([a['id'],'fingerprint'])
receipts=json.loads((W/'semantic-receipts.json').read_text());ids={a['id'] for a in receipts}
if len(receipts)!=3 or len(ids)!=3:errors.append(['receipt-count'])
for a in receipts:
 for key in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']:
  if a.get(key) is not True:errors.append([a['id'],key])
 for target in a['targets']:
  if not (S/target).is_file():errors.append([a['id'],'missing-target',target])
claim=json.loads((E/'actual-claim-full-7.json').read_text());binding=json.loads((W/'primary-owner-binding.json').read_text());pres=json.loads((E/'claim-sync-preservation-full.json').read_text())
if claim['status']!='pushed' or claim['actor']!='Boss4' or not ids<=set(claim['ids']) or set(binding['ids'])!=ids:errors.append(['owner-binding'])
if claim['local_sync']['status']!='needs-attention' or binding['raw_local_sync_status']!='needs-attention':errors.append(['raw-sync-state-was-rewritten'])
if pres['missing'] or pres['different'] or pres['unmerged'] or not pres['stash_kept'] or not all(x['same'] for x in pres['tracked']):errors.append(['claim-sync-preservation-not-clean'])
copy=sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
for name in ['selfcheck.json','copy-files.json']:
 rel=str((W/name).relative_to(S))
 if rel not in copy:copy.append(rel)
(W/'copy-files.json').write_text(json.dumps(sorted(copy),ensure_ascii=False,indent=2)+'\n')
result={'status':'passed' if not errors else 'failed','ordinary_file_check_only':True,'mathematical_execution':0,'primary_files':3,'semantic_receipts':3,'formal_objects':2,'copy_files':len(copy),'raw_claim_local_sync_status':'needs-attention, preserved unchanged; separate preservation evidence checked','errors':errors,'non_self_referential_files':files}
(W/'selfcheck.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='non_self_referential_files'},ensure_ascii=False))
if errors:raise SystemExit(1)
