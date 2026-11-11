"""Main records closed Stage18 packages and live successors, with lossless frozen text."""
from pathlib import Path
from hashlib import sha256
import gzip
import json
import subprocess

HERE=Path(__file__).resolve().parent;W=HERE.parent;REPO=HERE.parents[3]
RUN='six-boss1-20261111';PREFIX='research/workspaces/'+RUN+'/'
assert not (HERE/'stage18-save-receipts.json').exists()
for name,status in [
 ('main_visible_c_v4_certificate_check.json','PASS_MAIN_FULL1586_RAW513_DUAL_FULL_FACE_TRUE_BRANCH_AND_SIX_UNIVERSAL_CUTS'),
 ('main_ordered_cells_check.json','PASS_MAIN_COMPLETE181_CELL_GEOMETRY_AND_ALL513_COLUMNS'),
 ('main_cap_coupled_complete_check.json','PASS_MAIN_COMPLETE_NONPRODUCT_DOMAIN28_TRUE_COSTS_AND_COLUMNS')]:
    assert json.loads((W/name).read_text())['status']==status

checks=[]
for folder in ['visible_maximum_joint_v4','visible_maximum_joint_v4_solve','all_source_ordered_joint_menu','all_source_ordered_menu_cells','source2_cap_coupled_internal_safe']:
    base=W/folder;count=0
    for line in (base/'SHA256SUMS').read_text().splitlines():
        wanted,rel=line.split('  ',1)
        p=REPO/rel if rel.startswith('research/') else base/rel
        assert sha256(p.read_bytes()).hexdigest()==wanted,(folder,rel)
        count+=1
    checks.append({'package':folder,'checksums_verified':count,'manifest_sha256':sha256((base/'freeze_manifest.json').read_bytes()).hexdigest()})
(HERE/'stage18-closed-checksums.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')

target=W/'visible_maximum_joint_v4/row_catalog.tsv';raw=target.read_bytes()
archdir=W/'portable_frozen_text_stage18';archdir.mkdir(exist_ok=False)
archive=archdir/'visible_c_v4_row_catalog.tsv.gz';archive.write_bytes(gzip.compress(raw,mtime=0))
assert gzip.decompress(archive.read_bytes())==raw
manifest={'scope':'Lossless publication of frozen1586 raw catalogue; trailing empty TSV fields preserved byte-for-byte. Original source and manifest unchanged.',
 'files':[{'target':'visible_maximum_joint_v4/row_catalog.tsv','archive':'portable_frozen_text_stage18/visible_c_v4_row_catalog.tsv.gz',
 'sha256':sha256(raw).hexdigest(),'archive_sha256':sha256(archive.read_bytes()).hexdigest(),'original_bytes':len(raw),
 'freeze_manifest_sha256':sha256((W/'visible_maximum_joint_v4/freeze_manifest.json').read_bytes()).hexdigest()}]}
(archdir/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

note=(W/'stage18-current.md').read_text()
main=W/'main.md';old=main.read_text();headline='# Boss1：六人共同目录跨真实分支研究\n\n'
assert old.startswith(headline) and not old[len(headline):].startswith('# Stage18：')
main.write_text(headline+note+'\n## 此前阶段的历史入口\n\n'+old[len(headline):])
(REPO/'archives/customer-attraction/subarchives/six-providers/workspaces/Boss1/README.md').write_text('# Boss1：恰六人半覆盖\n\n'+note)
(W/'assignments/stage18.md').write_text(note)
tasks=[
 ('visible_maximum_joint_v4','visible_maximum_joint_v4.md','closed','/root/visible_maximum_joint','完整1586原输入已明确消费恰一次；所有原行/零行/尺度保留，严禁重跑。'),
 ('visible_maximum_joint_v4_solve','visible_maximum_joint_v4_solve.md','closed','/root/visible_maximum_joint_solve','精确alpha约.4411521416736506、全13秩20零列面及真实内部SAFE整面排除，Main全重放。'),
 ('all_source_ordered_joint_menu','all_source_ordered_joint_menu.md','closed','/root/early_shared_x_source_audit','完整连续G与损失项已证，67样本已冻；后继181cell义务也闭合。'),
 ('all_source_ordered_menu_cells','all_source_ordered_menu_cells.md','closed','/root/visible_maximum_joint','14cell181点完整有限化；Main重建全部32448边界及92853系数。'),
 ('source2_cap_coupled_internal_safe','source2_cap_coupled_internal_safe.md','closed','/root/early_shared_x_source_audit','11面28顶点非product域已冻；Main另核3584余项与14364列，26行严格分离完整1586最优面。'),
 ('source2_minimal_cap_safe','assignments/stage18.md','working','/root/early_shared_x_source_audit','任意tau及最小匹配中间帽，完整源2参数域与C行；0优化/不读点，保自由Ceq乘子可负。'),
 ('all_source_minimal_cap_safe','assignments/stage18.md','working','/root/visible_maximum_joint_solve','同一直接付款推广源1/3/4/5；保H=t/min(D,5)，核完整域或明确子族；0优化。'),
 ('ordered181_on_1586_diagnostic','assignments/stage18.md','working','/root/visible_maximum_joint','已明确释放固定1586点/面只读；核181全部面表达与119根完整正支付，0优化。'),
 ('main','main.md','working','/root','确认本阶段pushed，正式回流独有连续付款与全域精确界；核更一般帽族后准备下一完整输入，half仍开放。')]
receipts=[]
for solver,nn,state,agent,nxt in tasks:
    cmd=['python','work.py','research','save',RUN,'--solver',solver,'--profile','full','--note',PREFIX+nn,'--state',state,'--agent-id',agent,'--next',nxt]
    r=subprocess.run(cmd,cwd=REPO,capture_output=True,text=True)
    (HERE/f'stage18-save-{solver}.stdout.json').write_text(r.stdout)
    (HERE/f'stage18-save-{solver}.stderr.txt').write_text(r.stderr)
    assert r.returncode==0,(solver,r.stderr)
    receipts.append({'solver':solver,'state':state,'agent':agent,'receipt':json.loads(r.stdout)})
    print(solver+':'+state,flush=True)
(HERE/'stage18-save-receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'closed_checksums':checks,'lossless_original_sha256':manifest['files'][0]['sha256']},ensure_ascii=False))
