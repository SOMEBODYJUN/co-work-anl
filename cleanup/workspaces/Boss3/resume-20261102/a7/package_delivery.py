from pathlib import Path
import json, hashlib, shutil
R=Path.cwd(); W=R/'cleanup/workspaces/Boss3/resume-20261102/a7'; E=R/'archives/customer-attraction/tools/evidence/trueH-fixed-and-bidirectional-resumed-boss3'; S=Path('/workspace/scratch/cd4305a146e6/boss3-session/source-root')
def save(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
M=json.loads((E/'source-manifest.json').read_text()); D={Path(x['path']).name:json.loads((E/'source-root'/x['path']).read_text()) for x in M if x['path'].endswith('.json')}
F=['archives/customer-attraction/state/程序/加权最大铰链的精确恢复与全断点分离--程序.md','archives/customer-attraction/state/程序/真实第三位固定查询闭包与双菜单替换定价--程序.md','archives/customer-attraction/state/资源/固定查询闭包与双菜单探索的三份浮点保存点--资源.md']
related=json.loads(Path('/workspace/scratch/cd4305a146e6/boss3-session/a7-requested-dependencies.json').read_text())
for m in related:
 p=S/m['path'];out=E/'comparison-source-root'/m['path'];out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,out);m['evidence_path']=str(out.relative_to(R));m['role']='comparison-only; no receipt/no extra done'
save(E/'comparison-source-manifest.json',related)
base=next(x['atoms'] for n,x in D.items() if n=='trueH_bidirectional_discovery.json')
comp={}
for m in related:
 if m['path'].endswith('.json'):
  d=json.loads((S/m['path']).read_text());comp[Path(m['path']).name]={'atoms_equal_primary_449':d['atoms']==base,'primal_nonzero':sum(v!=0 for v in d['primal_float']),'dual_entries':len(d['dual_multipliers_float']),'row_count':len(d['row_names']),'full_fields_read':True}
reports={}
for n,d in D.items():
 if 'atoms' not in d:continue
 reports[n]={'top_keys':list(d),'row_count':len(d['row_names']),'distinct_rows':len(set(d['row_names'])),'row_prefix_counts':{},'all_primal_nonzero':[[i,v] for i,v in enumerate(d['primal_float']) if v!=0],'all_primal_zero_indices':[i for i,v in enumerate(d['primal_float']) if v==0],'dual_multipliers_float':d['dual_multipliers_float'],'metadata':{k:v for k,v in d.items() if k not in ['atoms','row_names','primal_float','dual_multipliers_float','history']}}
 for row in d['row_names']:
  p=row.split(':')[0];reports[n]['row_prefix_counts'][p]=reports[n]['row_prefix_counts'].get(p,0)+1
 if 'history' in d:
  reports[n]['history_all_fields']=d['history']
  reports[n]['last_100_primal_all_zero']=all(v==0 for v in d['primal_float'][749:849])
  reports[n]['last_round_negative_states']=[z['maximum_state'] for z in d['history'][-1]['state_reports'] if z['minimum_scaled_residual']<0]
save(E/'data-reading-report.json',{'scope':'Full-field reading/serialization view; not LP, independent mathematical check or rerun. All atoms in lossless pool view; all named rows retained in original and report_other_fields.','main_report_data':reports,'comparison_atom_identity':comp,'original_math_program_runs':0,'new_math_checker_runs':0})
modules=[('certificate/max_indexed_coupling.py','full code; exact row reconstruction, parent interfaces, class reuse, pricing and frozen run contract'),('maxroot/price_indexed_hinges.py','full code; current 5d7cd5 source versus old report d9f193, target/modes/new zero columns'),('maxroot/trueH_payment_pricing.py','full code; P7 table, 24 rows, source mapping and family oracle'),('maxroot/indexed_hinge_pricing.py','full code; inherited indexed hinge histogram source domains')]
basepath='research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/'
reads=[]
for name,scope in modules:
 p=S/(basepath+name);reads.append({'path':str(p),'sha256':sha(p),'read_scope':scope,'role':'comparison-only'})
mod=R/'archives/customer-attraction/tools/evidence/weighted-source-contracts-resumed-boss3/comparison/modules'
for name,scope in [('exact_cross_primal.py','full code; evaluator and exact inherited setup'),('frozen_pair_reoptimization.py','only fraction_solve and independent_rows helper definitions, not whole source'),('max_menu_joint_pricing.py','only block_coeff/maximum_scores relevant definitions; maxnames zip prefix, not whole source'),('max_menu_tuple_pricing.py','full 46-line module; maxnames extension and block_coeff dispatch')]:
 p=mod/name;reads.append({'path':str(p.relative_to(R)),'sha256':sha(p),'read_scope':scope,'role':'comparison-only; published evidence reuse'})
for p in [R/'archives/customer-attraction/state/引理/任意背景加权近饱和交换与统一锚主题上界--引理.md',R/'archives/customer-attraction/state/引理/共同加权最大主题的双菜单铰链消元--引理.md',R/'archives/customer-attraction/state/引理/真实第三位投影的五人最大根包络--引理.md',R/'archives/customer-attraction/state/资源/共享最大铰链与十单位策略的原独立回放--资源.md',R/'archives/customer-attraction/state/资源/五人最大根与共享菜单原件的复现边界--资源.md',R/'archives/customer-attraction/state/引理/实际第三位十三行投影的两态铰链分解--引理.md',R/'archives/customer-attraction/state/程序/两种第三位历史的共同目录抬升与分离归因--程序.md']:
 reads.append({'path':str(p.relative_to(R)),'sha256':sha(p),'read_scope':'full mature prose; frozen original audits not rerun','role':'mathematical comparison'})
save(E/'related-reading-scope.json',reads)
relations=[{'object':F[0],'compared_to':'background BNS + A5 HM + A6 exact57 report and independent t1 audit','decision':'same mother relation for k=2/3/4; bind author 3d4428 recovery to891c and all18; do not recredit independent stored5421 values as rederived'}, {'object':F[1],'compared_to':'mature P7 full 144 coefficient theorem + payment/source-last/indexed source code','decision':'D arbitrary legal five-menu, same-family substitutions94 and fixed15query60; preserve actual/second/max/indexed sources and120float'}, {'object':F[2],'compared_to':'payment mother/source_last449 and current generic price code','decision':'same columns not inherited row_names; all128 logs; final10negative andlast100zero not reoptimized; d9f193 vs5d7cd5'}, {'object':F[2],'compared_to':'published actual13 and shared catalog lifts','decision':'53 source-last actual V cap+Kenv explains failure without new joint coupling;50fixed float lift not SPE;63actual13 separate point/row family'}]
save(W/'relationship-decisions.json',relations)
save(W/'read-and-run-record.json',{'identity':'Boss3 cleaner_a','primary_sources':8,'primary_bytes':sum(m['size'] for m in M),'all_primary_full_read':True,'read_details':{'main_python':'4 full source files, 3 implementations and267B wrapper','main_json':'4 complete reports:18negative all long fractions;3large all keys/all atoms including zero/all row names and sparse duals/all128 history states','atom_lossless_view':'849 distinct atoms,1747 stored records;7field pools andall849 index tuples full read;other_fields unchanged','comparison_sources':'3 parent-exported comparison-only files full read;449atoms byte-content identity reused,all distinct fields/primal/duals/history read','helpers':'precise partial/full scopes in related-reading-scope.json'},'normal_clean_show_calls':8,'normal_clean_show_exit0':8,'primary_size_sha_verified':8,'original_math_program_runs':0,'new_math_checker_runs':0,'LP_BI_random_runs':0,'source_code_imports':0,'scope_boundary':'all numerical mathematics is frozen historical output or analytic derivation; current packaging serialization/hashes/AST do not execute original programs','correction':'earlier informal9negative-state message superseded byfull10 states0,1,2,4,8,23,27,29,30,31','tool_dispatch_notes':'3 initial long apply_patch requests aborted before dispatch byincoming agent messages; no file mutation from those; successful sequential patches subsequently written'})
Eread='archives/customer-attraction/tools/evidence/trueH-fixed-and-bidirectional-resumed-boss3/README.md'
notes={
'exact_all_hinge_breakpoints.json':('全文3010B scope/count/sourceSHA和18个name/全部长有理负值，逐i/菜单/c读；7条max1、11条max2、0max3。','保287名义断点域和仅保存18负输出；sourceSHA绑定A6的891c57点，t1同值，不升格SPE反例。',[F[0]]),
'exact_projected_hinge.py':('全文5448B imports、breaks/coefficient/atom映射、浮点QR候选支持、Fraction恢复/全部5421原式重构、双h系数比对、输出和main。','原作者重构5421与A6独立只读保存值不同，k2/3/4共同BNS及分段仿射完整解释；没有重跑。',[F[0]]),
'price_trueH_fixed_closure.py':('全文267B docstring、两import和main的4轮/Universe/两文件名完整调用。','保wrapper与实际generic入口不同SHA，当前target存在优先续跑、末批零填充及旧报告字段差异。',[F[1],F[2]]),
 'trueH_bidirectional_pricing.py':('全文4300B SPECS全部94行域、任意D/J行、fixed与indexed真节点、全hist缓存/120浮点oracle、母atoms重算LP及全输出。','P7的D不需opt；同族94不发明新机制或跨族完整σ；保精确行与非整数oracle不同层。',[F[1]]),
 'trueH_fixed_closure_pricing.py':('全文5012B 15合法标签、45fixed+15indexed、row公式/三源/fixed_block、全部缓存键/family接口、run母列重算及输出。','准确写任意15查询重复五次及13395系数；背景真indexed不平均化；新增60只补合法查询类。',[F[1]]),
 'trueH_bidirectional_discovery.json':('全文520452B全部顶层、6659行名、449个全部字段atoms含398零权列、全部449primal、50非零dual、scope/code/beta/minslack；无损视图复原。','保存51正质量和449原子不同；与fixed449列相同而行/对偶不同，母payment旧名不可当现行行定义。',[F[2]]),
 'trueH_fixed_closure_discovery.json':('全文522907B全部顶层、6747行名、449全字段atoms含399零权列、全部449primal、49非零dual、scope/code/beta/minslack；无损视图复原。','50正质量有限列LP数值，beta<2不是全域证书；codeSHA绑定当前fixed实现。',[F[2]]),
 'trueH_fixed_closure_fullpricing.json':('全文818396B全部顶层、6747行名、849全字段atoms含786零权列、全部primal/61duals、四轮全部128state余量/context/seconds、旧codeSHA。','保末100列未重优、末轮10负state、受限beta不作half证书，旧d9f193不等当前5d7cd5；所有零权列和旧exact_mass注释保留。',[F[2]])}
receipts=[]
for m in M:
 n=Path(m['path']).name;rd,de,ts=notes[n]
 receipts.append({'id':m['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':rd,'comparison_note':'完整对照成熟BNS/HM/P7/A6恢复点及root实际十三行/共同目录抬升；实读payment、source_last母点和代码以及current price_indexed版本，精确范围见related-reading-scope.json/relationship-decisions.json。成功审计不重复运行。','decision_note':de+' 本批原数学程序/新数学checker/LP/BI/随机运行均0；原件size/SHA逐项核同。','disposition':'integrated','targets':ts+[Eread]})
save(W/'semantic-receipts.json',receipts)
save(W/'delivery.json',{'source_count':8,'source_bytes':sum(m['size'] for m in M),'claim_remote_tip':'e8f7b5f750865345324e8671fb967ee23d60e3e2','formal_objects':F,'checkpoint_paths':F+[str(E.relative_to(R)),str(W.relative_to(R))],'receipt_file':str((W/'semantic-receipts.json').relative_to(R)),'original_clean_show_calls':8,'original_clean_show_successes':8,'original_math_program_runs':0,'new_math_checker_runs':0,'LP_BI_random_runs':0,'remaining_in_assigned_scope':0,'comparison_only_extra_sources':[m['id'] for m in related],'parent_actions':'Review3objects/8receipts; checkpoint/pushed beforedone; internal agent noGitwrite/claim/done.'})
rows='\n'.join('|'+Path(m['path']).name+'|'+m['id']+'|'+str(m['size'])+'|'+m['sha256']+'|' for m in M)
(E/'README.md').write_text('''# 真实H固定查询与双菜单原始证据

本目录完整保全8主源1,879,792B；Boss3已实际领取，原子claim pushed e8f7b5f750865345324e8671fb967ee23d60e3e2。clean show只读导出8次全部exit0并核size/SHA；未读取凭据、未执行Git写入或claim/done。两个冻结commit路由同字节详见source-manifest.json。

|原文件|主源ID|字节|SHA-256|
|---|---|---:|---|
'''+rows+'''

`source-root/<原相对路径>` 保原字节；`comparison-source-root/` 的3原件1,060,230B仅比较依赖，非本批新增主源，不额外done。comparison-source-manifest.json保精确ID/路由/指纹，相关母文件由B6另实质处置。

## 正文与可使用范围

- [精确恢复和287名义断点/18负分离](../../../state/程序/加权最大铰链的精确恢复与全断点分离--程序.md)：k=2/3/4共同最大BNS；绑定作者3d4428恢复器与A6的891c57点，区分重构5421旧行和独立只读旧余量。
- [94双菜单和60固定查询](../../../state/程序/真实第三位固定查询闭包与双菜单替换定价--程序.md)：七行定理、任意合法D/J、精确源和120浮点oracle、四轮wrapper。
- [三浮点保存点](../../../state/资源/固定查询闭包与双菜单探索的三份浮点保存点--资源.md)：全字段、全部零权、128日志、末100零未重优、10负state、旧/新generic入口SHA差异。

## 完整数据读法

三大报告atoms共1747条存储、849条不同完整记录。complete-data-reading-view.json的7字段值池/849索引元组、original_record_maps、report_other_fields无损保存并恢复原JSON内容；缺键−1区别于空值，不能将旧exact_mass当当前浮点primal。全部池和元组、所有primal/dual、全部128日志都已实读，不只读摘要/正支持。原始JSON保最终字节，data-reading-report.json另列所有非零primal、所有零索引、对偶、metadata、全部history及母点449列相同的比较。解析/序列化不是数学可行性复现。

related-reading-scope.json逐项注明整份或定点范围：fraction_solve只读精确消元helper，max_menu_joint只读相关block/score，不能冒称整源；其它所列实现及成熟正文为全文阅读。父方后来发布actual13/两历史抬升已经链接，未重复审其原件。source-tree依赖旧research路径，归档不等于无依赖可导入包。

本批原数学程序、独立数学checker、LP/BI/随机/定价、原模块导入执行均0。已有充分成功的144项P7、1512条件HM及t1点回放不无因重跑。当前只作全文数学推导、全部数据阅读、指纹/无损视图/资产检查。精确恢复成功、18负值、四轮浮点日志都是历史冻结结果；没有SPE实现、一般half新证书或closed fullpricing声明。

工作记录和8逐源receipt在cleanup/workspaces/Boss3/resume-20261102/a7；父方负责实读复核、checkpoint/pushed和done。本目录不包含秘密或认证材料。
''')
print(json.dumps({'primary_count':len(M),'primary_bytes':sum(m['size'] for m in M),'receipts':len(receipts),'formal_objects':len(F),'comparison_bytes':sum(m['size'] for m in related),'math_runs':0},ensure_ascii=False))
