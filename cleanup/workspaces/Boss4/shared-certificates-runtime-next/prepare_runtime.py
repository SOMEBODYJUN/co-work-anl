import json,hashlib,pathlib,shutil
root=pathlib.Path('tools/evidence/shared-certificates-runtime')
inv=list(map(json.loads,open('cleanup/inventory.jsonl')))
by_path={r['path']:r for r in inv}
primary=json.load(open('/workspace/scratch/37f0f9248cfc/boss4-next-cache/next40-groups.json'))['shared_certificates_runtime']
replay=root/'replay'
old=pathlib.Path('tools/evidence/shared-catalog-side-results/replay')
for p in old.rglob('*'):
    if p.is_file():
        dest=replay/p.relative_to(old);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
for base in ['original','related']:
    src=root/base
    for p in src.rglob('*'):
        if p.is_file():
            dest=replay/p.relative_to(src);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
certbase=pathlib.Path('archives/customer-attraction/tools/evidence/shared-certificates/original')
for name in ['tiny_phi.json','on_path_chord.json','sharp_lower_rational.json']:
    dest=replay/'evidence/certificates/shared'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(certbase/name,dest)
manifest=[]
ids={r['id'] for r in primary}
for p in sorted(replay.rglob('*')):
    if not p.is_file():continue
    rel=str(p.relative_to(replay));rec=by_path[rel]
    digest=hashlib.sha256(p.read_bytes()).hexdigest();assert digest==rec['sha256'],rel
    manifest.append({**rec,'role':'primary' if rec['id'] in ids else 'comparison-runtime-dependency','preserved_path':str(p)})
(root/'replay-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
primary_manifest=[]
for item in primary:
    rec=next(r for r in inv if r['id']==item['id']);p=root/'original'/rec['path']
    primary_manifest.append({**rec,'preserved_path':str(p),'read_method':'python3 work.py clean show '+rec['id'],'all_bytes_read':True})
(root/'source-manifest.json').write_text(json.dumps(primary_manifest,ensure_ascii=False,indent=2)+'\n')
print('canonical replay files',len(manifest),'primary files',len(primary_manifest),'primary bytes',sum(r['size'] for r in primary_manifest))
