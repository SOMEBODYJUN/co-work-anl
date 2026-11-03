from pathlib import Path
import shutil,json,hashlib
R=Path.cwd();E=R/'archives/customer-attraction/tools/evidence/copy-tax-domain-correction-resumed-boss3';W=R/'cleanup/workspaces/Boss3/resume-20261102/a8'
formal=[Path('archives/customer-attraction/state/审查/R286链式重查询与R291复制税边界--审查.md'),Path('archives/customer-attraction/state/程序/复制税的固定策略锥与全SPE最小税递推--程序.md')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
for p in formal:
 snap=E/'before'/p;snap.parent.mkdir(parents=True,exist_ok=True);assert not snap.exists();shutil.copyfile(R/p,snap)
ids={'4567df5291710117cab5','6844b47df933ffb8a9a4','8a16e7b20cd8ca84ecbb','d58b5436694f50d196ef','2436b89c5cc92115ecb5','0d2a6223816aaebe7801'}
metas=[]
for line in (R/'cleanup/inventory.jsonl').read_text().splitlines():
 d=json.loads(line)
 if d.get('id') in ids:metas.append(d)
old=R/'archives/customer-attraction/tools/evidence/R286-chain-R291-copy-tax-20261031';ad=R/'archives/customer-attraction/tools/evidence/four-topic-exhaustive-and-maxima-scope-primary/original'
for m in metas:
 p=(ad if 'R-ad571' in m['path'] else old)/Path(m['path']).name
 assert p.stat().st_size==m['size'] and sha(p)==m['sha256'];out=E/'frozen-source-root'/m['path'];out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,out);m.update({'evidence_path':str(out.relative_to(R)),'copied_from':str(p.relative_to(R)),'role':'existing-done-source-comparison;no-claim/no-done'})
save(E/'source-manifest.json',metas)
extra=[old/'runs/exhaust_copy_tax_three_topics.stdout',old/'runs/exhaust_copy_tax_three_topics.stderr',old/'runs/counterexample_search_m6.stdout',old/'runs/counterexample_search_m6.stderr',old/'README.md',old/'source-manifest.md',old/'comparison-notes.md',R/'cleanup/progress/4567df5291710117cab5.json',R/'cleanup/progress/6844b47df933ffb8a9a4.json',R/'archives/customer-attraction/tools/evidence/half-restart-and-copy-tax-boundary-primary/original/research/workspaces/customer-attraction/R-291a34e2dbf4451aa0115fed89a7729b/README.md']
extra_meta=[]
for p in extra:
 out=E/'saved-records'/p.relative_to(R);out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,out);extra_meta.append({'from':str(p.relative_to(R)),'evidence_path':str(out.relative_to(R)),'size':p.stat().st_size,'sha256':sha(p),'role':'historical-log-or-cleaning-record;not-new-source'})
save(E/'saved-record-manifest.json',extra_meta)
save(W/'formal-before-after.json',[{'path':str(f),'before_path':str((E/'before'/f).relative_to(R)),'before_sha256':sha(E/'before'/f)} for f in formal])
print('Preserved 2 before snapshots, 6 original sources, 10 historical records; no mutation of formal or original sources.')
