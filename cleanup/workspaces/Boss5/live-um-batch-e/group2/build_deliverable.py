from pathlib import Path
import hashlib
import json
import shutil

BASE = Path('/workspace/scratch/9cf2a96299f5')
REPO = BASE / 'co-work-anl'
OUT = BASE / 'um-batch-e-resume/group2'
TARGET = 'archives/unrelated-machines/state/资料/不相关机历史工作区的身份与接续边界--资料.md'
EVIDENCE = 'archives/unrelated-machines/tools/evidence/historical-workspace-identities'
group = json.loads((BASE / 'boss5-resume-groups/group2.json').read_text())
inventory = {x['id']: x for x in map(json.loads, (REPO / 'cleanup/inventory.jsonl').read_text().splitlines())}

notes = {
    'a21bc98acb07d0da647e': (
        '完整149B/6行JSON实读：schema精确整数1、save=unrelated-machines、actor=R-6a2ecc2ee52f4c7c928ba97e2e2f266c、instance=d26349463a684c7e928509bb794187ec，恰四键，无数学内容。',
        '完整旁读配对26f47e228c82a6d76070 README并与1254模板替换精确actor后逐字相等；该README另批处置。三份本组JSON替换各自精确actor/instance后字节相同；实际阅读现行work.py 283–349的路径和恢复校验，以及两份既有恢复/身份资料相关合同。精确actor/instance全仓检索未见正式数学正文引用，inventory在该前缀仅两文件；不推论作者别处无成果。',
        'retained：复用已有四字段合同，仅新增此源的精确actor、instance、原字节与双冻结定位；不创建数学对象，不接管身份，不替配对README done。'),
    'e4f92e3bf0e2ad6240f5': (
        '完整1163B/15行README实读：历史boss9身份、UM-TARGET-v1与一般反面OPEN、Git/对外交流归历史boss9；唯一数学链接arbitrary_sink_private_group_price_cover_rounding.md；任意sink/逐件资格/无共同下包络而保唯一home/W/尺寸/rho；一般角色生成与绝对阈值decoder未解；BFS宽度、非单位反链gammoid、固定平均配置数未提升。',
        '完整读最终16556B主稿SHA6c23677…§1–9，与正式价格覆盖双源审查、共同占位最终审查、最终冻结读后审查、最终正文内部审计及独立有限MW计算逐项比较。已有对象保三个ID、空模式满秩修复、+b、真实cover回溯/共同宏/MW、poly(L,1/eta)、unknown-OPT promise和实现边界。纠正引用方向：主稿§7及内部审计明确OPT以下接受集合可非单调；另一读后审查“单调接受谓词”措辞不准。全仓精确草稿术语检索未定位这三份未提升稿，不补造结果。',
        'integrated：数学证明已由正确正式对象承载，仅在身份资料新增此README的历史导航、三ID精确域/界、非单调搜索区别、草稿未提升身份、一般结构生成与全调度decoder缺口。保留原件，不重复证明、不改变旧审查完成归属、无新软件运行或新颖性认证。'),
    'aac2a9a1a95b359cdd0d': (
        '完整149B/6行JSON实读：schema精确整数1、save=unrelated-machines、actor=R-6b0a5491cfe44e0695dface4a9262057、instance=38c027e7df5947f19e40a12d73ccbe59，恰四键。',
        '完整配对实质README e4f92e3bf0e2ad6240f5，actor/save一致；与另两JSON精确身份归一后字节同一结构；实读现行workspace_path/workspace_init相关完整校验代码、恢复资料及本历史身份资源合同。JSON不含README数学声明，不能据instance认证价格覆盖或推送完成。',
        'retained：原字节、blob/SHA、双冻结定位及精确配对身份单独保留，四字段共性复用；数学导航属于README及其已存在正式对象。'),
    'bafba4fbc000ed1f5b8c': (
        '完整978B/7行README实读：历史boss1当前环境恢复使用新actor，不接管旧boss1编号；唯一目标OPEN；唯一数学链接weighted_group_joint_slot_rounding.md；虚拟d_h/带home容量共同槽去Hall正W下界、实际3/2+delta与位多项式未知OPT搜索；一般矩阵结构未解，软件仅给token见证后的恢复。',
        '完整读12930B最终weighted主稿SHA95f329…§1–8，与正式加权出口算法及双实现/冻结范围全文比较；已有对象保两ID、共同资格/等端w/宏>T/2条件、出口不超d及home付离散误差、真正单调LP网格搜索、given-witness软件边界、zero-target域外fixture纠错及7708/八例证据归属。另与price最终主稿比较，禁止把price非单调搜索混入weighted或把逐件资格扩入共同E。',
        'integrated：已有完整证明不重抄，在身份资料新增旧作者接续、新旧编号边界、两ID准确域/界/失败机制、软件范围和一般任务身份联合容量缺口；原件独立保留，不升级一般UM、不新增程序运行或审查。'),
    'de47f5c6feb5ab4c7615': (
        '完整149B/6行JSON实读：schema精确整数1、save=unrelated-machines、actor=R-6fe15cbf717641d4ad88c25122f728aa、instance=de2ba7ab46ca4cbf8ed5dc5d24c10193，恰四键。',
        '完整配对bafba4fbc000ed1f5b8c README，actor/save一致；与另两JSON精确actor/instance替换后字节相同；已读现行恢复校验、工作区恢复资料和历史身份共性合同。没有数学版本、角色、任务完成或分支字段；不得从“当前环境恢复”反推旧编号接管或数学认证。',
        'retained：逐源保此instance及原件/指纹/双冻结出处，共性仅复用四字段恢复合同；配对README的实际算法导航另由本批分节承载。')
}

manifest = []
receipts = []
for item in group:
    ident = item['id']
    meta = inventory[ident]
    original = BASE / 'um-workspace-next' / f"{ident}--{Path(item['path']).name}"
    data = original.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    assert digest == meta['sha256'] and len(data) == meta['size']
    target = OUT / 'original' / ident / Path(item['path']).name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    manifest.append({**meta, 'line_count': data.count(b'\n'), 'full_file_reviewed': True,
        'outside_repo_original': str(target),
        'proposed_evidence_original': f"{EVIDENCE}/original/{ident}/{target.name}"})
    read, compare, decision = notes[ident]
    receipt = {'id': ident, 'full_file_reviewed': True, 'related_material_checked': True,
        'unique_content_accounted_for': True, 'read_note': read,
        'comparison_note': compare, 'decision_note': decision,
        'disposition': 'integrated' if item['path'].endswith('README.md') else 'retained',
        'targets': [TARGET]}
    receipts.append(receipt)
    (OUT / f'receipt-{ident}.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')

(OUT/'receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
(OUT/'source-manifest.json').write_text(json.dumps({'schema':1,'batch':'Boss5 internal resume group2',
    'target':TARGET,'sources':manifest,'no_git_network_clean_or_shared_text_mutation':True},ensure_ascii=False,indent=2)+'\n')
refs=[]
for m in manifest:
    refs += [f"- source:{s['commit']}:{s['path']}" for s in m['sources']]
(OUT/'frontmatter-source-refs.txt').write_text('\n'.join(refs)+'\n')

full_files = [
    ('AGENTS.md','任务及数学保全合同'),
    ('cleanup/OBJECTS.md','正式对象命名/身份/状态/来源合同'),
    ('cleanup/receipt-example.json','逐源语义receipt字段'),
    ('archives/unrelated-machines/state/资料/个人工作区恢复规则与旧题路由边界--资料.md','通用四字段/恢复/旧题路由合同'),
    ('archives/unrelated-machines/state/问题/任务级共同容量的算法义务--问题.md','一般UM统一epsilon、全机/原任务/可靠FAIL/位复杂度义务'),
    ('archives/unrelated-machines/tools/evidence/um-next-four-audit-primary/comparison/research/current/unrelated_machines/arbitrary_sink_private_group_price_cover_rounding.md','boss9唯一链接的最终主稿全文§1–9；最终SHA6c23677…'),
    ('archives/unrelated-machines/tools/evidence/weighted-joint/original/research/current/unrelated_machines/weighted_group_joint_slot_rounding.md','boss1唯一链接的最终主稿全文§1–8；最终SHA95f329…'),
    ('archives/unrelated-machines/state/算法/共同资格组的加权出口联合槽--算法.md','完整weighted证明/搜索/软件及fixture域'),
    ('archives/unrelated-machines/state/审查/共同资格组的双实现与冻结范围--审查.md','两个实现、真正运行与输入/版本/zero-target边界'),
    ('archives/unrelated-machines/state/审查/仿射线全局dummy与任意汇点价格覆盖双源审查--审查.md','全部正文；本组使用其中price精确接口与证明承载'),
    ('archives/unrelated-machines/state/审查/任意汇点价格覆盖与共同占位联合舍入最终审查--审查.md','全部正文；空模式修复/三个合同/审查顺序/有限证据'),
    ('archives/unrelated-machines/state/审查/任意汇点价格覆盖最终冻结读后审查--审查.md','全部正文；发现unknown-OPT接受谓词单调措辞不准确'),
    ('archives/unrelated-machines/state/审查/任意汇点私有组价格覆盖最终正文内部审计--审查.md','全部正文；准确保OPT以下可非单调，及最终证明/边界'),
    ('archives/unrelated-machines/state/计算/任意汇点价格覆盖与共同MW的独立有限审计--计算.md','全部正文；112例/1876query/full-vs-prefix/final-matroid未执行'),
    ('archives/unrelated-machines/tools/evidence/historical-workspace-identities/original/1254c0254ceb82d8b6b7/README.md','653B模板全文与R6a README精确actor归一逐字比较')
]
reading=[]
for rel,purpose in full_files:
    data=(REPO/rel).read_bytes()
    reading.append({'path':rel,'full_file_read':True,'purpose':purpose,'size':len(data),
        'sha256':hashlib.sha256(data).hexdigest(),'new_execution':False})
reading.extend([
    {'path':'archives/unrelated-machines/state/资料/不相关机历史工作区的身份与接续边界--资料.md',
     'full_file_read':False,'read_scope':'开头四字段/空模板/既有历史接续的实际相关部分；本资料有并行增量，未宣称整份历史数学引用全部重审。','purpose':'确定复用资源目标及共性合同；检索确认本组精确身份尚未整合'},
    {'path':'work.py','full_file_read':False,'read_scope':'283–349行，workspace_path尾部及workspace_init完整四键/instance/resume/README/回执代码','purpose':'比较当前恢复字段语义；只阅读未调用'},
    {'path':str(BASE/'um-workspace-next/26f47e228c82a6d76070--README.md'),
     'full_file_read':True,'source_id':'26f47e228c82a6d76070','size':653,
     'sha256':'a9458d27e0fb5dee93acdb80363b1d93122e3e63a3b44b85177bf47cb2d72107',
     'purpose':'R6a配对模板；仅比较不receipt/不done'},
    {'path':'cleanup/inventory.jsonl','full_file_read':False,'read_scope':'精确本组5源与配对26f47的6行；三个actor完整前缀检索；相关草稿关键词检索','purpose':'原件双冻结定位/前缀范围；不把清单当数学证明'}
])
for m in manifest:
    reading.append({'path':m['outside_repo_original'],'source_id':m['id'],'full_file_read':True,
        'size':m['size'],'sha256':m['sha256'],'purpose':notes[m['id']][0]})
(OUT/'actual-reading-list.json').write_text(json.dumps(reading,ensure_ascii=False,indent=2)+'\n')

profiles=[]
for m in manifest:
    if m['path'].endswith('workspace.json'):
        s=Path(m['outside_repo_original']).read_text(); p=json.loads(s)
        profiles.append(s.replace(p['actor'],'<ACTOR>').replace(p['instance'],'<INSTANCE>'))
assert len(set(profiles))==1
a=(BASE/'um-workspace-next/26f47e228c82a6d76070--README.md').read_text().replace('R-6a2ecc2ee52f4c7c928ba97e2e2f266c','<ACTOR>')
b=(REPO/'archives/unrelated-machines/tools/evidence/historical-workspace-identities/original/1254c0254ceb82d8b6b7/README.md').read_text().replace('R-0aebcce9ae5842fdb1be78207a977265','<ACTOR>')
assert a==b
(OUT/'comparison-checks.json').write_text(json.dumps({'profiles_compared':3,'exact_four_keys':True,
    'profiles_equal_after_exact_actor_instance_substitution':True,
    'R6a_compared_readme_id':'26f47e228c82a6d76070','template_comparison_id':'1254c0254ceb82d8b6b7',
    'readmes_equal_after_exact_actor_substitution':True,'source_fingerprints_match_frozen_inventory':True,
    'new_math_program_runs':0,'only_read_local_sources_and_wrote_outside_repo':True},ensure_ascii=False,indent=2)+'\n')

# Keep the two exact canonical dependencies used to distinguish their searches.
for ident,rel in [
    ('price-cover-final','archives/unrelated-machines/tools/evidence/um-next-four-audit-primary/comparison/research/current/unrelated_machines/arbitrary_sink_private_group_price_cover_rounding.md'),
    ('weighted-joint-final','archives/unrelated-machines/tools/evidence/weighted-joint/original/research/current/unrelated_machines/weighted_group_joint_slot_rounding.md')]:
    dst=OUT/'comparison-snapshots'/f'{ident}.md';dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(REPO/rel,dst)

print(json.dumps({'source_count':len(manifest),'receipt_count':len(receipts),'output':str(OUT),
    'all_original_fingerprints_match_inventory':True,'new_math_runs':0},ensure_ascii=False))
