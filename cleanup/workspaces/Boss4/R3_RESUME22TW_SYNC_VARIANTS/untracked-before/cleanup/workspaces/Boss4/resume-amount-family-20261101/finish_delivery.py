from pathlib import Path
import json,hashlib,re
root=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
ws=root/'cleanup/workspaces/Boss4/resume-amount-family-20261101'
ev=root/'archives/customer-attraction/subarchives/six-providers/tools/evidence/amount-cap-one-family-primary'
obj='archives/customer-attraction/subarchives/six-providers/state/程序/金额cap1完整策略锐族的原程序与四百动作证书--程序.md'
oldmath='archives/customer-attraction/state/定理/末层多孩子金额预算的锐两倍列容量--定理.md'
inv=[json.loads(s) for s in (root/'cleanup/inventory.jsonl').read_text().splitlines()]
related_ids=['49d812c22c050d9a42b7','22b85da39da11d287947','703238e69005f7fcdf08','152b3f738a1113eea03e','3692e7c1ef305f2d24a5','bb36885d5dad09bb0b25','6dc2912b1c12b620cad5']
related=[next(x for x in inv if x['id']==sid) for sid in related_ids]
(ev/'related-source-manifest.json').write_text(json.dumps(related,ensure_ascii=False,indent=2)+'\n')
p=root/obj
s=p.read_text()
related_refs=['source:'+t['commit']+':'+t['path'] for r in related for t in r['sources']]
s=s.replace('---\n\n# 金额cap1', 'related_source_refs:\n'+''.join('  - '+json.dumps(x,ensure_ascii=False)+'\n' for x in related_refs)+'---\n\n# 金额cap1',1)
s += '\n详细后续审查定位：`703238e69005f7fcdf08`，`source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-b6d636d360e14c11aeb4b76415ed422b/direction_review/continued_exchange_2026_10_24/audits/wallet_review.md#二、末层cap2的独立重构与它没有购买的资金`及`#三、深层cap2真正要新增什么`；两冻结版本定位均在related_source_refs。原文所述其它五人旧界后来已被正式五人定理超越，本对象只用其对金额合同的解析复核，未继承那些历史数值作为现状。\n'
p.write_text(s)
(ev/'README.md').write_text('''# 金额cap1完整策略族的五源证据

正式说明见[原程序与四百动作证书](../../state/程序/金额cap1完整策略锐族的原程序与四百动作证书--程序.md)。五件均为实际冻结源原字节，合计54013B；源ID、大小、SHA、blob和两提交路径在source-manifest.json。

- [全n原稿](original/coupling/amount_cap1_family.md)：6880B，完整SPE与列比2−3/(n+1)。
- [原3332B生成器](original/coupling/audit_amount_cap1_family.py)：标准库Fraction；顶层执行并写同目录JSON，import也执行。当前未运行或import。
- [原36652B n3证书](original/coupling/amount_cap1_family_n3.json)：全部400有序决策前缀动作，原报告2800含自身比较；n3是四人，非六人证书。
- [credible原审查](original/credible/review_amount_cap1_family.md)：3622B，解析逐类型重构，无独立代码运行声明。
- [independent原审查](original/independent/amount_cap1_family_review.md)：3527B，明示先重构后对照；历史复跑为原样脚本，不是独立实现。

另保两份实读后续原稿：[deep精确交接](related/deep_amount_handoff.md)、[deep粗界](related/deep_amount_bound_check.md)。它们仅为相关比较，不在本批五源receipts里，也未冒新done。

prior-certificate-structural-readout.json与prior-execution-and-review-scope.json来自本地此前同SHA缓存：原件现已全字节对等核实；前者只是键域、标签、顺序和实际链的结构PASS，后者明确原入口/import/payoff/IC全部0。复用报告不算当前重新验证2800项IC，更不算当前原程序运行。当前运行边界见execution-scope.json。

源码内嵌单位likes，不依赖项目Instance。一般结论由正式说明完整解析证明及父档锐cap2定理承担；六人n5取值由公式代入，不需新全树运行。JSON的optimum字段来自全覆盖上界达到，不来自独立最优搜索。原JSON无argv/环境/代码SHA/exit日志，未倒填。
''')
# README depth: evidence -> tools -> six-providers, so ../../state is correct.
(ev/'execution-scope.json').write_text(json.dumps({'current_frozen_source_show_reads':5,'current_exported_primary_files':5,'current_original_entry_runs':0,'current_imports':0,'current_payoff_or_IC_replays':0,'new_mathematical_implementation_runs':0,'new_solver_or_SPE_search_runs':0,'current_original_byte_hash_and_old_cache_byte_equality_checks':5,'prior_same_SHA_structural_readout_reused':True,'current_repeated_400_action_structural_scans':0,'current_complete_certificate_human_read':'all 16 fields, three requests and all 400 ordered action records read after compact lossless output','n5_six_person_values':'analytic substitution only','frozen_n3_original_runs':'historical reports only; no raw execution log available','prior_cache_location':'boss4-next-cache/r3-amount-cap-one-family-certificate-and-reviews-primary','scope':'retrieval, full reading, comparison, byte identity and delivery checks; no mathematical code run'},ensure_ascii=False,indent=2)+'\n')
notes={
'44ac5a996de190a8da48':('6880B全文：精确多cut/多forced主题AMOUNT及CAP1量词、单位块构造、全部fresh与非fresh有序历史策略、末位D平局、未用A/重复A/T/非根D/根D五类偏离及真实末位理性、全覆盖与q/λ/列比、统一二锐性和deep未付。','与现父档锐cap2定理逐式比较，确认本稿全n主数学已完整作related整合；另全文读程序、全部400动作JSON、双原review、deep_amount_handoff、deep_amount_bound_check及wallet_review中对同一合同的复核。','主数学重复于现定理而非未成熟或错误；原稿字节仍保。本程序对象补正式原证书/双review身份及n5六人解析特化，保同cut多孩子及λ>1；不重认新定理、half反例或固定六人二锐。','duplicate'),
'110a1ed1af682948ed17':('36652B完整JSON：16根字段、三个sender/cut/forced主题/parent与child利润/λ/q请求、全部400条history/action；全有序深度0/1/2/3均读。保原零起始主题与一起始角色混用、actual0,1,2,3、W=OPT18、输出15/4及5/4。','逐项对原3332B生成器输出字段与原稿n3代入；比较父方check_amount_cap输入门槛，发现本JSON无terminal_counts且不在其glob原位置，不冒父筛查已接受。原件与旧结构PASS所绑定缓存同SHA全字节一致，复用其键域/动作范围/排序/链readout，不再重算IC。','保完整原动作表及数据和无代码SHA/argv/环境/exit日志的边界。它是n3四人有限证据；不是全n证明、六人证书或本次2800项IC复验。','retained'),
'c98e8355f192f5614a31':('3332B全文：顶层parse_args --n≥3、m/k标签、不同单位客户likes、Fraction pay、build先递归全部真实孩子再fresh override/BI和断言、全有序历史第二遍IC含自身、q与金额/覆盖断言、JSON写同目录及stdout去actions。无main guard，import也执行。','与6880B全n稿和400动作JSON完全对应；对照父方4626B check_amount_cap发现本程序是自带输入的单族生成审计，父程序是过滤项目证书的固定输入最坏列评价，目标/依赖/IO不同。旧同SHA缓存execution明示数学运行0，故当前也未运行/import或伪造输出。','原代码完整保留，正式对象解释输入、真实后继、两遍检查、400内部前缀与2401叶区分及副作用。一般证明仍解析承担；源码读懂不自动等于本次运行。','retained'),
'a4a99bb614912c545bd9':('3622B全文：独立解析重构、非fresh封闭性、末位D与A平局、五类偏离及根D真实末位BR、全部金额重算、forced T合法而非须最优、同cut多孩子及λ>1、全n统一二锐与W=OPT/deep未证。','与原稿及现父档定理逐项比较无冲突；与independent原review比对审查先后与运行声明，本稿未陈述严格盲读顺序或程序运行，不能由标题独立推断独立实现。后续wallet_review仍确认末层容量且保deep/初始化未付。','保内部解析攻击审查的实质和真实边界，未升级为外审、新颖性、代码独立实现或一般half审查。','retained'),
'877bcf0bef8f85435968':('3527B全文：明示先独立重构一般证明后对照原稿，完整模型/全历史递归/五类偏离/根D关键理性/金额及W=OPT；历史n3原样复制重放400/2800、(5,5,5,3)、18和15/4，以及删除冗余副本后指回coupling入口。','与原稿、credible逐段重构及实际3332B代码/36652B完整JSON比较。严格区别一般解析重构与同一实现历史复跑；原稿自身不称独立实现，未有原argv/环境/exit日志，当前不补造或重复运行。','保明示读序和同实现复跑的作者记录，完整证明细节留正式对象；不误称严格盲审或独立实现，不把n3运行替代全n，保deep未证和half未被反驳。','retained')}
receipts=[]
manifest=json.loads((ev/'source-manifest.json').read_text())
for r in manifest:
    read,compare,decision,disp=notes[r['id']]
    targets=[obj,r['local_path']]
    if disp=='duplicate': targets.insert(0,oldmath)
    receipts.append({'id':r['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':read,'comparison_note':compare,'decision_note':decision,'disposition':disp,'targets':targets})
(ws/'semantic-receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
relations=[
{'type':'definition-scope','source':'customer-attraction/common-catalog-full-history-model','target':'customer-attraction/amount-cap1-family-400-node-certificate-and-review-reading-order','reason':'完整有序策略、真实偏离后继、单位客户/共同目录为全n构造共同条件；存在构造不升级成所有平局产生同一路径。','evidence':'正式正文精确候选及全n证明；现模型定义全文'},
{'type':'sharpness-not-new-upper-bound','source':'customer-attraction/amount-cap1-family-400-node-certificate-and-review-reading-order','target':'customer-attraction/terminal-multichild-amount-normalized-sharp-column-cap-two','reason':'同AMOUNT合同的全n列比趋2提供统一锐性；上界独立由末位逐客户代数证明，不需SPE。','evidence':'44ac5a996de190a8da48 §§3–5；父定理全文'},
{'type':'implementation','source':'44ac5a996de190a8da48','target':'c98e8355f192f5614a31','reason':'代码逐单位客户实现fresh override和封闭非fresh BI，第二遍核每个有序历史当前角色的全部合法动作。','evidence':'3332B源码全文；未运行'},
{'type':'historical-finite-certificate','source':'c98e8355f192f5614a31','target':'110a1ed1af682948ed17','reason':'JSON字段及全动作表符合该源码n3格式；历史复跑按原审稿报告，不造当前执行绑定。','evidence':'全部JSON及源码；同SHA旧结构readout、双review'},
{'type':'internal-analytic-review','source':['a4a99bb614912c545bd9','877bcf0bef8f85435968'],'target':'44ac5a996de190a8da48','reason':'两稿均实质重构全部全n激励类型及金额，独立稿明示先重构后对照；都不审一般half或deep。','evidence':'两review全文'},
{'type':'specialization','source':'44ac5a996de190a8da48','target':'customer-attraction/six-providers/problem','reason':'n5透明代入给六人辅助CAP1反例，W=OPT50，非half反例；只联系所需付款合同的边界。','evidence':'正式正文六人代入：11主题、利润9^5/5、列15/2'},
{'type':'unproved-extension-boundary','source':['49d812c22c050d9a42b7','22b85da39da11d287947'],'target':'customer-attraction/amount-cap1-family-400-node-certificate-and-review-reading-order','reason':'深层真实后继变化不能套末层负载+1和c−1；粗界仅prefix总利润半数，不证一般deep cap2。','evidence':'两related原稿全文及wallet_review §§2–3'}]
(ws/'relation-evidence.json').write_text(json.dumps({'stage':'phase2-human-relationship-assessment','map_projection_modified':False,'reason':'本批只新增独立正文和证据，父Boss串行决定登记；全量阶段三超图尚未执行，不能由链接自动造边。','relations':relations,'nonrelations':'WA、同context净券、其它退款合同不因付款同名获得蕴含；原程序与父glob筛查也不互为已执行认证。'},ensure_ascii=False,indent=2)+'\n')
(ws/'mathematical-self-check.md').write_text('''# 本次完整数学自查

1. 全n参数为n≥3,m=n+1；likes重数是不同单位客户，2n²客户、2n+1主题，无权客户或权玩家变模。
2. 非fresh永久封闭；root D偏离使用同一σ真实末位严格支配T<A，而非冻结后继；末位fresh的D是非严格BR。所有有序历史由归纳/BI覆盖，构造只证存在。
3. AMOUNT同sender跨孩子总额≤同一parent利润；λ可>1，同cut多主题不可删。sender与recipient索引条件j<i≤l完整保。
4. parent2n−1，child n+1，q1，λ=(2n−1)/(n+1)，末列比2−3/(n+1)>1；实际W=OPT2n²。统一二锐不推固定六人二锐。
5. 六人n5解析特化：50客户、11主题、利润9五份及5、child6、λ3/2、输出15/2；没有新n5运行。
6. 全n证明是一般数学；原n3 JSON是四人400决策前缀而非含2401终叶的全部树。原2800含自身比较只是有限报告，不给一般量词。
7. 原脚本顶层执行及同目录写文件，未import/执行；原JSON无terminal_counts，不能冒父方glob已接受。同实现历史重放不叫独立实现。
8. 字节同SHA缓存及既有结构PASS已读并复用；本次五件show/导出和原件字节核实，不重跑已成功400结构或2800算术。一般deep、AMOUNT覆盖初始化、已有支出兼容均留未证。
9. 双review完整实读，明示与未明示先后分别记；无外审或新颖性认证。后续wallet_review读取仅用于金额合同比较，不继承已过时五人界。
''')
nexts=[{'id':sid,'path':next(x for x in inv if x['id']==sid)['path'],'reason':reason} for sid,reason in [('49d812c22c050d9a42b7','已作related全文读，完整精确DEEP义务及提前复制T失败尝试值得独立语义清洗。'),('22b85da39da11d287947','已作related全文读，一般不需SPE的半prefix粗界及充分条件应与deep开放候选分别保。'),('2f4c09a6069876368efe','旧CLAIMS登记仍需逐对象比较，不能靠本族五源完成代替。'),('364c1e03baa75080b24a','一般工作稿中AMOUNT初始化、深层容量、已有支出兼容的完整止点值得核全稿。')]]
(ws/'next-candidates.json').write_text(json.dumps(nexts,ensure_ascii=False,indent=2)+'\n')
files=[str(q.relative_to(root)) for q in ev.rglob('*') if q.is_file()]+[obj]
# delivery file itself is a coordination handoff, no claims of checkpoint/done.
(ws/'delivery.json').write_text(json.dumps({'status':'ready-for-parent-review-and-serial-checkpoint','source_ids':[r['id'] for r in manifest],'formal_files':[obj],'evidence_root':str(ev.relative_to(root)),'primary_sources':5,'primary_bytes':54013,'receipts':str((ws/'semantic-receipts.json').relative_to(root)),'actual_math_runs':0,'current_IC_or_payoff_replays':0,'all_written_paths':sorted(files+[str(q.relative_to(root)) for q in ws.iterdir() if q.is_file()]),'no_git_or_clean_mutations':True,'next_candidates':str((ws/'next-candidates.json').relative_to(root))},ensure_ascii=False,indent=2)+'\n')
print('wrote receipts=5, relations=7, math runs=0')
