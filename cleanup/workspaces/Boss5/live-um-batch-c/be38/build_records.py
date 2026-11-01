from pathlib import Path
import json,hashlib,re,shutil
out=Path('/workspace/scratch/9cf2a96299f5/um-batch-c/be38')
repo=Path('/workspace/scratch/9cf2a96299f5/co-work-anl')
manifest=json.loads((out/'manifest-additions.json').read_text())
target='archives/unrelated-machines/state/资料/不相关机历史工作区的身份与接续边界--资料.md'
common='已读AGENTS.md、cleanup/OBJECTS.md和receipt-example；全仓按精确actor、instance、来源路径及数学ID检索，并读共享身份资料的相关分节、当前workspace_init四键校验合同。'
notes={
'c6b6dd0142c5266f0445':(
'全文7行996B：boss24及actor身份，UM原目标/一般反面仍OPEN，完整clone §8精确Claim及专门后审链接，六内部研究方向且不以赞同作证明，真实近二源/任意低载完整调度绝对阈值decoder/固定误差位多项式规模义务，度二MaxMin仅还原3/2提醒。',
common+'全文读现完整clone定理及计算对象、冻结canonical§8和00c66c...专门后审；实读§9及现有界接线定理/计算对象比较操作差别，按字节定位旧审查绑定的§8与前缀。核U最短端、S_T含正整数、删空Λ三修复及后继2290累计177次DFS口径；未重跑代码。',
'以历史研究交接保留：原件、actor/profile、MC=min=liminf/最终gcd周期/指数首达的准确导航、审查先验与纠错、未解hardness义务完整进入资源分节。既有数学对象承担一般证明；MaxMin警示仅保历史范围，不另授新hardness或认领被引来源。'),
'a7c3291b2e31a2824c05':(
'全文6行149B；恰四键，schema精确整数1、save=unrelated-machines、actor=R-40bb9e2c2cb04c489d65ec3d7bf38331、instance=511ff8684704460b96f091e361cfd3d7；与配对README及冻结目录一致，无隐藏题目/分支/角色字段。',
common+'与c6b6... README配对；四键及32hex相容性与当前work.py第300–352行逐项比较，未调用恢复。精确actor/instance全仓检索仅定位路径索引/清点及本次相关后审的历史actor说明。',
'保留此独有容器身份及指纹到统一资料，不作调度instance、数学证书、推送回执或当前授权；不以profile为数学推导证据。'),
'5e2c25ff10dc5e0a5ab6':(
'全文15行653B：标题/存档/actor、未填写的当前研究占位、notes/experiments/candidates建议、成熟资产沿规范层链接、私聊及checkpoint确认pushed可见性合同；无实际研究问题、数学正文或实验链接，无OPEN/CLOSED声明。',
common+'与已保存1254c0254ceb82d8b6b7 README全文逐字比较，仅各自精确actor替换为<ACTOR>后字节完全一致。冻结inventory精确actor前缀仅两文件；全仓检索未定位该actor/instance在正式数学正文的引用。',
'模板共性并入既有说明，同时独立保存本原件、身份和真实未填写状态；不生成数学对象，不由目录建议或未命中推断作者没有其他研究。'),
'1405f78195b693c085f1':(
'全文6行149B；四键schema=整数1、save=unrelated-machines、actor=R-4347997ee7984447a7209e3470d522ac、instance=7848c8bb42c041cabc3c2eb2e4c1188d；无数学内容或状态字段。',
common+'与配对5e2c...空模板、其他两组本批JSON及既有四字段资料比较；当前workspace_init仅定向全文实读300–352行，未执行。源指纹与inventory大小/SHA逐项相同。',
'保此具体profile与模板配对，解释恢复相容性和字段非数学身份；不合并掉不同instance，不恢复旧actor。'),
'3dce7ba852326558ca3c':(
'全文11行1268B：UM反面入口和OPEN，固定r ordinary-YES/r-tuple-NO过滤、有界重数接线配置包络/共同循环真实OPT1见证、允许padding单一log字母表三入口及精确限制；旧审查/外审边界，真实整数NO/任意低载全任务decoder缺口，未成熟草稿留scratch。',
common+'完整比较canonical top_two §7及现最终审查/作者候选障碍，private_graft §9及现定理/计算，model_classical §8及专门review/现padding等价；区分固定r的B_r与总负载、某个c接线的存在性与全称、固定k padding次数与可变k。核unavailable=None字段纠错、q<c/零坐标修复及N=2^E旧表读数。',
'保留三种不同合同和历史交接到统一资源，不复制同义定理，不把后继审读倒授旧候选或把未物化padding称真实运行；三者均未闭合一般近二hardness/完整decoder。'),
'c99c0c32ac143736dea9':(
'全文6行149B；四键schema=整数1、save=unrelated-machines、actor=R-434a435edada4b1e8b69630114bc4556、instance=c6eaa3c43e514f849d36c6b23c069b5b；与README及冻结路径相符。',
common+'与3dce...数学交接README配对并比较另两组profile、现历史身份资料和work.py定向函数。完整actor/instance全仓检索未定位现正式正文对该精确容器的已有整合，只有冻结路径/清点索引。',
'独立保容器身份、原字节和来源定位，数学只由配对README导航到正式对象；不将instance等同数学输入、审查状态、pushed证据或当前Boss身份。')}
receipts=[]
for d in manifest['files']:
 a,b,c=notes[d['id']]
 receipts.append({'id':d['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a,'comparison_note':b,'decision_note':c,'disposition':'retained','targets':[target]})
(out/'receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
reads=[
('AGENTS.md','full','本仓当前规则与身份/阶段边界'),
('cleanup/OBJECTS.md','full','对象类型、资源处置及来源合同'),
('cleanup/receipt-example.json','full','receipt字段'),
('cleanup/inventory.jsonl','filtered exact six IDs and exact three actor prefixes','源指纹与每容器可见文件清点；未声明全文实读整个inventory'),
(target,'相关身份/模板/旧boss21、R-1c6、两占位及R-3bcf/R-3ca5分节；partial','已有资源的去重、空模板与未链接独立笔记的边界；未声称全文重新核证全部历史引用'),
('archives/unrelated-machines/tools/evidence/historical-workspace-identities/original/1254c0254ceb82d8b6b7/README.md','full','模板逐字比较'),
('work.py','lines 300-352 only','workspace_init，四键/32hex/显式resume/不覆盖README；未执行'),
('archives/unrelated-machines/问题--问题.md','full','主目标脚手架身份，不沿用其未完成脚手架为新证明'),
('archives/unrelated-machines/state/定义/不相关机器与两个调度松弛--定义.md','full','全部原任务、zero/empty、非负有理、统一epsilon与反面量词'),
('archives/unrelated-machines/state/定理/完整机器任务克隆的多重集与最终周期--定理.md','full','MC双向恢复、有限值域/半群/gcd最小周期、Sylvester及近二种子、三修复/审查先验/后继计数'),
('archives/unrelated-machines/state/计算/完整克隆的双Oracle与周期族核验--计算.md','full','DFS/DP不同接口，172+5=177次及2290节点，报告负载表与未展开大复制范围；未运行'),
('archives/unrelated-machines/state/定理/有界重数克隆接线与共同循环坍缩--定理.md','full','cap包络、星边分色补置换、q<c、严格层级、共同cycle与历史贡献、零坐标/总量修复'),
('archives/unrelated-machines/state/计算/有界接线的证书实现与有限穷举--计算.md','full','给定证书实现及非序列化见证、81/2448/256/22/8有限口径；未运行'),
('archives/unrelated-machines/state/等价/私有填充的对数字母表调度等价--等价.md','full','A_N、固定k padding、全合格输出decoder及E/logN读数'),
('archives/unrelated-machines/state/障碍/固定件数超载过滤与严格次二障碍--障碍.md','full','作者候选身份、固定r B_r与ordinary目标、局部严格次二障碍不同合同'),
('archives/unrelated-machines/state/审查/固定件数过滤最终证明与不可用端字段纠错--审查.md','full','最终canonical§7、big-only/短前缀误差和unavailable=true=None字段纠错'),
('archives/unrelated-machines/state/审查/不相关机研究状态总账与开放义务--审查.md','full','方法边界与去重导航；其总账概述不替换精确定义的存在统一epsilon量词'),
('archives/unrelated-machines/tools/evidence/pair-witness-audits/source/top_two_pair_witness_boundary.md','full lines 1-287','完整§1–7实际阅读：pair目标/3SAT三半、固定r总证明与反面promise'),
('tools/evidence/um-foundation-composition-configuration-reviews/related/research/current/unrelated_machines/private_graft_and_resource_repetition.md','§8 lines216–346 and §9 lines347–445; partial whole file','逐段实读两个直接链接数学节；不声称重审§1–7。读取全文件字节只用于prefix/section hash绑定。'),
('archives/unrelated-machines/tools/evidence/model-classical/original/research/current/unrelated_machines/model_and_classical_barriers.md','§8 lines202–EOF; partial whole file','完整padding正文与所有合格输出/位复杂度/有限审计边界'),
('archives/unrelated-machines/tools/evidence/model-classical/original/research/reviews/unrelated_machines/logarithmic_palette_padding_equivalence_review.md','full','固定k/实际N及审读边界'),
('archives/unrelated-machines/tools/evidence/research-state-20261031/original/research_state.md','rg matching snippets only, not full read','MaxMin/clone/反面导航检索；不认证整个112KB源'),
]
entries=[]
for rel,scope,purpose in reads:
 p=repo/rel;b=p.read_bytes()
 entries.append({'path':rel,'scope_actually_read':scope,'purpose':purpose,'size':len(b),'sha256':hashlib.sha256(b).hexdigest()})
# Separate exported dependency was fully read but is not part of these six receipts.
dep=Path('/workspace/scratch/9cf2a96299f5/um-workspace-next/00c66c414f8ee27aead1--complete_clone_multiset_periodicity_review.md')
b=dep.read_bytes();dest=out/'comparison-dependency'/'00c66c414f8ee27aead1--complete_clone_multiset_periodicity_review.md';dest.parent.mkdir(exist_ok=True);dest.write_bytes(b)
entries.append({'path':str(dep),'scope_actually_read':'full','purpose':'README直接链接的专门后审：提示/参与构造先验、§8精确绑定、三修复；仅比较依赖不登记done','size':len(b),'sha256':hashlib.sha256(b).hexdigest(),'local_copy':str(dest)})
for d in manifest['files']:
 entries.insert(0,{'id':d['id'],'path':d['local_original'],'scope_actually_read':'full','size':d['size'],'line_count':d['line_count'],'sha256':d['sha256'],'purpose':notes[d['id']][0]})
readlog={'scope':'Boss5内部Solver，仅六已认领源；没有Git/网络/clean，没有改共享正文，没有另登记身份或子代理。','new_mathematical_program_executions':0,'source_and_template_verification_script_executed':True,'reads':entries,'searches':[
'cleanup inventory按六源ID提取，并按三actor路径前缀清点',
'archives与tools下精确三actor及三instance检索；命中路径索引，新增后审依赖明确记录R-40bb历史actor',
'全仓按UM-COMPLETE-CLONE-MULTISET-PERIODICITY及clone/固定r/共同cycle/log palette等关键词检索，随后实读上列相应全文或明确节段',
'MaxMin/反向互补/degree-two/3/2等关键词查相关现对象及历史总账；没有以搜索片段冒充完整外部定理证明。'
]}
(out/'actual-reading-log.json').write_text(json.dumps(readlog,ensure_ascii=False,indent=2)+'\n')
canon=(repo/'tools/evidence/um-foundation-composition-configuration-reviews/related/research/current/unrelated_machines/private_graft_and_resource_repetition.md').read_bytes();s=canon.index('## 8. '.encode());e=canon.index('## 9. '.encode())
identity={'operation':'Current combined source has §9 appended; remove only one added separator newline immediately before §9, then hash prior prefix and §8 span.','prefix_before_section9_size':e-1,'prefix_before_section9_sha256':hashlib.sha256(canon[:e-1]).hexdigest(),'section8_size':e-s-1,'section8_sha256':hashlib.sha256(canon[s:e-1]).hexdigest(),'review_bound_prefix_sha256':'6afdec871fa9a209cfb15d169b2846548522d1805ee24f269ec7b97145012d5f','review_bound_section8_sha256':'963833e8093222662cfc161e81cca83bf3a89cb764ff967e931346183e8446c5'}
identity['prefix_matches']=identity['prefix_before_section9_sha256']==identity['review_bound_prefix_sha256'];identity['section_matches']=identity['section8_sha256']==identity['review_bound_section8_sha256'];assert identity['prefix_matches'] and identity['section_matches']
(out/'review-prefix-identity.json').write_text(json.dumps(identity,ensure_ascii=False,indent=2)+'\n')
# Resolve only local Markdown links against final intended resource location.
section=(out/'section.md').read_text();links=re.findall(r'\]\(([^)]+)\)',section);checked=[]
for href in links:
 p=(repo/target).parent/href
 assert p.exists(),str(p)
 checked.append({'href':href,'exists':True})
verification=json.loads((out/'verification.json').read_text());verification.update({'receipt_count':len(receipts),'receipt_ids_match_sources':set(r['id'] for r in receipts)==set(d['id'] for d in manifest['files']),'intended_target':target,'all_section_local_links_exist':True,'section_local_links':checked,'review_prefix_exact_identity':identity['prefix_matches'] and identity['section_matches'],'section_sha256':hashlib.sha256((out/'section.md').read_bytes()).hexdigest()});(out/'verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'receipts':len(receipts),'reading_records':len(entries),'links_checked':len(checked),'review_prefix_and_section_match':True,'section_bytes':len((out/'section.md').read_bytes())},ensure_ascii=False))
