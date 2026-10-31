"""Necessary new bounded representation/metadata/format checks; no old suite."""
from pathlib import Path
import hashlib, json, re
E=Path(__file__).resolve().parent
S=E.parents[2]
W=S/'cleanup/workspaces/Boss4/r3-assets-review-files-ledger-next'
checks=[]
F=chr(96)*3
def check(name,ok):
    checks.append({'check':name,'passed':bool(ok)})
    if not ok:raise AssertionError(name)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for row in read(E/'source-manifest.json'):
    p=S/row['saved_path']
    check('primary bytes '+row['id'],p.stat().st_size==row['size'])
    check('primary SHA '+row['id'],sha(p)==row['sha256'])
assets=read(E/'original/research/assets.json')['entries']
reviews=read(E/'original/research/review_status.json')['entries']
am=read(E/'asset-record-destinations.json')
rm=read(E/'review-record-destinations.json')
formal=read(E/'formal-pages.json')
cache={}
for p in formal:
    raw=(S/p).read_text()
    cache[p]=[json.loads(z) for z in re.findall('^'+F+r'json\n(.*?)\n'+F+'$',raw,re.M|re.S)]
    check('forbidden C0 '+p,not any(ord(c)<32 and c not in '\t\n\r' for c in raw))
    check('trailing whitespace '+p,all(l==l.rstrip() for l in raw.splitlines()))
    check('flat frontmatter '+p,raw.startswith('---\n') and all(k+':' in raw.split('---',2)[1] for k in ['id','kind','type_tag','title','status','summary','source_refs']))
check('formal count',len(formal)==11)
actualassets={z['id']:z for p in {z['target'] for z in am} for z in cache[p]}
actualreviews={z['id']:z for p in {z['target'] for z in rm} for z in cache[p]}
check('all351 exact object identities',len(actualassets)==351 and set(actualassets)=={z['id'] for z in assets})
check('all640 exact review identities',len(actualreviews)==640 and set(actualreviews)=={z['id'] for z in reviews})
doccache={p:(S/p).read_text() for p in formal}
for i,z in enumerate(assets):
    check('asset complete source fields '+str(i),actualassets[z['id']]==z and am[i]['source_record']==z and am[i]['index']==i)
    check('asset heading '+str(i),am[i]['heading'] in doccache[am[i]['target']])
for i,z in enumerate(reviews):
    check('review complete source fields '+str(i),actualreviews[z['id']]==z and rm[i]['source_record']==z and rm[i]['index']==i)
    check('review heading '+str(i),rm[i]['heading'] in doccache[rm[i]['target']])
cat=read(E/'related/catalog/original/research/catalog.json')
rows=[(i,z) for i,z in enumerate(cat['entries']) if z['topic']=='weighted_congestion']
fm=read(E/'files-record-destinations.json')
check('FILES501 full original catalog fields',len(fm)==501 and [(z['catalog_index'],z['source_record']) for z in fm]==rows)
filedoc=doccache[fm[0]['target']]
block=re.search('^'+F+r'text\n(.*?)\n'+F+'$',filedoc,re.S|re.M).group(1)+'\n'
check('FILES formal full text equal',block.encode()==(E/'original/research/weighted_congestion_frontier/FILES.md').read_bytes())
binding=read(E/'full-files-binding.json')
check('actual independent whole FILES binding',binding['entire_file_equal'] and binding['bytes']==534265 and binding['expected_sha256']==binding['sha256'])
check('54 package values includes empty',len({z.get('package','') for _,z in rows})==54 and '' in {z.get('package','') for _,z in rows})
meta=read(E/'metadata-analysis.json')
check('five actual malformed condition arrays',[z['index'] for z in meta['character_arrays']]==[22,27,28,29,30])
check('640 external not recorded',meta['axes']['external_review']=={'not_recorded':640})
check('actual identity differences',meta['asset_ids_without_review']==['Q-CAG-HALF'] and meta['review_ids_without_asset']==['CERT-SOUND'])
check('620 graph claim coverage',meta['graph_claims']==620 and not meta['graph_claims_without_asset'] and not meta['graph_claims_without_review'])
for z in read(E/'dependency-manifest.json'):
    p=S/z['saved_path']
    check('dependency byte SHA '+z['saved_path'],p.stat().st_size==z['bytes'] and sha(p)==z['sha256'])
progress=read(E/'reading-progress.json')
check('read all351 asset indices',progress['assets_complete_indices']==list(range(351)))
check('read all640 review indices',progress['review_complete_indices']==list(range(640)))
check('read all FILES semantic scope',progress['FILES_all_shell_and501_shared_semantics_read'] and progress['FILES_entire534265bytes_static_binding'])
receipts=read(W/'semantic-receipts.json')
check('3 exact primary receipts',{z['id'] for z in receipts}=={z['id'] for z in read(E/'source-manifest.json')})
for z in receipts:
    check('full semantic receipt '+z['id'],all(z[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all(z[k] for k in ['read_note','comparison_note','decision_note']) and z['disposition']=='integrated' and z['targets'] and all((S/p).is_file() for p in z['targets']))
result={'scope':'new exact object representation, metadata identity and format only; no old code/suite or mathematical proof certification','checks':len(checks),'passed':all(z['passed'] for z in checks),'formal_forbidden_C0':0,'details':checks}
for p in [E/'self-check.json',W/'self-check.json']:p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='details'},ensure_ascii=False))
