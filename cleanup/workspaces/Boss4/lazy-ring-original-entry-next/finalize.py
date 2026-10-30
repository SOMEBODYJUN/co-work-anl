from pathlib import Path
import json,hashlib,ast,re
repo=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
root=repo/'tools/evidence/lazy-ring-original-entry';ws=repo/'cleanup/workspaces/Boss4/lazy-ring-original-entry-next'
resource='archives/facility-games/state/资料/双设施规范代码入口与证书格式的精确导航--资料.md';computation='archives/facility-games/state/计算/惰性最大最小回应环的原入口与有限回归--计算.md'
notes=[
('279ea752f2177f6e76ce','全文读2341字节README，九程序职责、短证书/普遍界/复杂度/最优分离及迁移/增长链接全部保留。','比较MITM、单交叠、异址正规形、DP、强弦、异构、硬度对象；全文跟进USAGE/path_migration/GROWTH，实际USAGE已为CAG流程而非所指双设施示例。','保存九行完整资源职责，明确表非穷尽、不同参数与五种证书格式；不由README继承普遍phi或四种子一般因子二。','integrated',[resource]),
('b1d86a5bf34773a9de22','全文读90字节根包init，只有研究范围和旧claims路径的docstring。','与cli/local及已清洗exact init逐字与SHA相同；AST无import/函数/类/重导出，真实原件保留供包路径恢复。','内容重复、路径角色保留；无独有数学内容，不把claims链接当定理认证，也未用空stub替代。','duplicate',[resource]),
('508bc42ce26940ad7cfa','全文读90字节cli init，仅相同研究范围docstring，无命令或检查函数。','与root/local/exact init同SHA e9632a5a…ff9ea0；原CLI的真实package bytes已用于隔离入口。','文档内容重复但保原路径，不创造额外算法/运行计数，不丢独有数学。','duplicate',[resource]),
('d3b4a7b1ea0d51306dce','全文读90字节local init，仅相同docstring；无pure/strong_chord重导出或自动执行。','四init同字节，比较pure/strong_chord独立模块职责；本组lazy不导入local求解器。','保原件与路径，范围说明去重；没有独有定理、不能把一个包标记当额外数学结果。','duplicate',[resource]),
('355e5949795947d67a09','全文读610字节CLI：必填input、精确小数token读取、lazy调用、计时/stdout；原tiny入口一次exit0。','全文读MITM273行/日志与半表/闭核后纠错；核全目录d剪枝、环内目标、相对概率、无default接口、弱输入解析与assert边界。','保存完整输出：[0,4,3]路径/[4,3]环，alpha1，6calls/12pruned/3visited；与冻结仅elapsed异。新独立25布局核验另列，不升级待审phi。','integrated',[computation]),
('25f41f7983570a1f5be7','全文读751字节测试；seed33221、30个8客户6地点输入，显式只核访问d相等与full alpha<=lazy；原样一次exit0、350剪枝。','比较历史lazy报告及共享optimize_pair核心；响应平局可不同，测试不比环/概率/证书逐字，不是独立局部实现。','保存真实报告，区分两显式断言与内部assert；新25布局条件成本/16默认补全是另一个新脚本，非原suite已有核验。','integrated',[computation])]
rows=[{'id':sid,'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':read,'comparison_note':comparison,'decision_note':decision,'disposition':disp,'targets':targets} for sid,read,comparison,decision,disp,targets in notes]
# Do not create a replacement directory during a shared synchronization window.
if not ws.is_dir() or not root.is_dir():raise RuntimeError('Shared synchronization window has not restored the owned paths yet')
(ws/'receipts.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
validation=[]
for fn in [resource,computation]:
    p=repo/fn;s=p.read_text();assert s.startswith('---\n')
    for m in re.finditer(r'\]\(([^)]+)\)',s):
        link=m[1]
        if '://' in link or link.startswith('#'):continue
        assert (p.parent/link.split('#')[0]).resolve().exists(),(fn,link)
    validation.append({'path':fn,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':p.stat().st_size,'links':'all targets exist'})
for mf in ['source-manifest.json','related-manifest.json','replay-manifest.json']:
    for rec in json.load(open(root/mf)):
        p=repo/rec['preserved_path'];assert p.stat().st_size==rec['size'];assert hashlib.sha256(p.read_bytes()).hexdigest()==rec['sha256']
for p in root.rglob('*.json'):json.load(open(p))
for p in root.rglob('*.py'):ast.parse(p.read_text(),str(p))
for rec in rows:assert all((repo/t).is_file() for t in rec['targets'])
assert len(rows)==6 and {r['id'] for r in rows}=={r['id'] for r in json.load(open(root/'source-manifest.json'))}
inc=list(map(json.loads,open(repo/'cleanup/increments/local-20261029.jsonl')));paths={r['path'] for r in json.load(open(root/'source-manifest.json'))};assert not any(r['path'] in paths for r in inc)
(root/'integrity.json').write_text(json.dumps({'primary_sources':6,'primary_bytes':3972,'all_canonical_hashes':'matched','JSON_and_Python_AST':'passed','formal_objects':validation,'receipt_dispositions':{'integrated':3,'duplicate':3},'independent_read_only_review':'Underlying source contracts checked by one temporary reviewer; findings: shared core, no default API, relative probabilities, asserts, weak input limits and non-exhaustive README.'},ensure_ascii=False,indent=2)+'\n')
(ws/'delivery.json').write_text(json.dumps({'source_count':6,'formal_paths':[resource,computation],'evidence_directory':str(root.relative_to(repo)),'receipt_file':str((ws/'receipts.json').relative_to(repo)),'execution':'Two original entrypoints once each, exit0; saved-output direct checker once, exit0; no passed original suite repeated','ready_for_boss_checkpoint':True,'relationship_assessment':'Navigation, MITM+greedy joint pruning and attainment; explicit closed kernel limits optimum transfer; finite checks stay checks; phase-3 edges deferred.'},ensure_ascii=False,indent=2)+'\n')
print('6 receipts, 2 formal objects; canonical hashes, JSON, AST and links passed')
