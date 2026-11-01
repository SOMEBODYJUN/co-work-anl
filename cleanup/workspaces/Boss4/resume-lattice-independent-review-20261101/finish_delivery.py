from pathlib import Path
import json
B=Path('/workspace/scratch/37f0f9248cfc/lattice-independent-review-staging')
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=B/'cleanup/workspaces/Boss4/resume-lattice-independent-review-20261101'
E=B/'archives/customer-attraction/subarchives/six-providers/tools/evidence/lattice-independent-review-primary'
base='archives/customer-attraction/subarchives/six-providers/state/'
lemma=base+'引理/两层计数势端点配平的真实行双向支付--引理.md'
construct=base+'构造/十五客户完整策略的势循环严格扩大收益SCC空间--构造.md'
review=base+'审查/计数势格循环的独立Floyd审计与冻结证据--审查.md'
probe=base+'程序/真实行锥额外双向空间的两种发现探针--程序.md'
manifest=json.loads((E/'source-manifest.json').read_text())
notes={
'9e3fb9dac56e91215d76':('940B全部11根字段实读：原status、15客户/13有序历史/39含自身比较/min0、唯一非平凡SCC两个(q,a)端点、四条完整七维分数行、AB坐标分离文本、W13/OPT15及general_half历史OPEN。','与4138B源码返回结构、2948B成文审查、7624B发现稿及6400B全动作/39松弛输出全文比较；独立报告无complete_strategy/all_exact_slacks/rank/triangle字段，不能继承发现审计111回归或秩/势端点检查。全仓未见同SHA当前成功运行日志，冻结本件为已有成功记录且无新数学疑点，不重复有限程序。','完整原JSON保字节并在审查对象逐字段保存；它是单个三人实例的历史独立实现报告，不是当前运行绑定/全n证明/六人证书；无源码SHA、argv、环境、exit日志不倒填。','retained'),
'1c9328ee2dd9c1421567':('2948B全文：明示独立重建谐势差分后读稿；F=P−P删除式、势端点非负配平与负行非负移项、旧SCC包含及不穷尽lineality、三标签背景m−2六边源真实嵌入限制、15单位七类型/13完整历史/四真实节点/AB坐标严格扩张、独立Floyd有限审计及half未付。','实读7624B发现稿、5825B发现审计与6400B完整39松弛报告；现父档只有R44导航和全树势表示边界，没有完整势配平/严格扩张正文。与共同删除势全域效率对象比对，固定两层线性恒等式不需全域DR/效率；signed span也不等于非负真实锥lineality。','一般机制整合成自足引理；严格合法SPE整合为构造，含完整动作表/39松弛/18端点邻接/四行及严格性；审查资源保先验与实现范围。仅证明存在三人严格扩张，不声称穷尽完整lineality或给一般half付款，无外审/新颖性认证。','integrated'),
'76307e651db964a863ac':('4138B源码全文：main guard、run内独立13有序动作及单位客户、follow/utility/endpoint/type_row、39真实IC比较、收益图Floyd闭包/SCC、四行零和和AB坐标分离、实际13/3/覆盖13与27叶求OPT15、stdout和--output open(x)排他新建行为。','与5825B发现审计逐节点DFS/精确rank/显式势incidence/111三角回归逐段区分；本独立实现不用其代码或规范包，核相同固定真实策略而不枚举全SPE。940B报告全部返回字段对照一致但未冒本次字节重生成，源码未import/执行。','完整独立程序保留；审查对象解释全部输入/指标/副作用和真实独立代码路径。普遍机制由解析证明，有限成功原件已充分且无新疑点，当前原CLI/import/39算术/新实现/搜索均0，不为重复成功制造新运行。','retained')}
receipts=[]
for r in manifest:
 if r['role']!='primary':continue
 a,b,c,d=notes[r['id']]
 targets=[review,r['local_path']]
 if r['id']=='1c9328ee2dd9c1421567':targets=[lemma,construct]+targets
 receipts.append({'id':r['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a,'comparison_note':b,'decision_note':c,'disposition':d,'targets':targets})
(W/'semantic-receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
rels=[
{'type':'definition-scope','from':'customer-attraction/common-catalog-full-history-model','to':['customer-attraction/potential-lattice-circulation-signed-real-row-payment','customer-attraction/fifteen-customer-SPE-potential-circulation-strict-SCC-expansion'],'reason':'所有比较源自同一完整有序策略真实完成；一般引理只用形式策略，严格构造才给非负单位客户SPE。','evidence':'引理论域；构造全部13动作与39比较'},
{'type':'deduction','from':'customer-attraction/potential-lattice-circulation-signed-real-row-payment','to':'customer-attraction/fifteen-customer-SPE-potential-circulation-strict-SCC-expansion','reason':'四真实行以系数1作势端点零和，所以每行负向可由其它三行非负支付；根AB坐标再分离旧SCC像空间。','evidence':'g0…g3及背景r=eA/标签(C,A,B)三角源；完整18端点图'},
{'type':'internal-review','from':'1c9328ee2dd9c1421567','to':['customer-attraction/potential-lattice-circulation-signed-real-row-payment','customer-attraction/fifteen-customer-SPE-potential-circulation-strict-SCC-expansion'],'reason':'先重建差分后读稿，实质核全部机制、真实节点和边界；不扩为外审/新颖性。','evidence':'2948B全文'},
{'type':'independent-implementation-and-historical-finite-check','from':'76307e651db964a863ac','to':'9e3fb9dac56e91215d76','reason':'自带单位客户/策略、Floyd闭包不同于发现DFS；固定输入的有限报告字段与源码一致，未造当前run。','evidence':'4138B源码、940B全部11字段'},
{'type':'discovery-provenance','from':'customer-attraction/two-discovery-probes-extra-cone-lineality','to':'customer-attraction/fifteen-customer-SPE-potential-circulation-strict-SCC-expansion','reason':'探针只找候选；合法三主题实例由完整精确后验与解析构造承担，二主题同覆盖退化不承担此严格类。','evidence':'3fb17764a6930667e3a2 §5；Root分工probe对象，非新运行'},
{'type':'shared-representation-not-implication','from':['cag-full-tree-payoff-flow-potential-attacks-common-representation-boundary','cag-common-deletion-potential-global-efficiency-submodular-lift'],'to':'customer-attraction/potential-lattice-circulation-signed-real-row-payment','reason':'共享删除势表示，但本机制只需两层未映射端点平衡，不推出共同非负客户/全域DR/一般half，也不由这些背景对象自动解出非负行锥。','evidence':'两现有正式对象全文及引理限制'}]
(W/'relation-evidence.json').write_text(json.dumps({'stage':'phase2-explicit-human-relation-review','map_modified':False,'reason':'只写独立新对象/原件，父Boss串行发布；阶段三投影不由链接自动生成。','relations':rels,'negative_scope':'三人构造不自动迁移六人；覆盖矩signed span不等于lineality；额外有符号空间不自动给2c−o非负余项；未声称所有lineality维数恰2。'},ensure_ascii=False,indent=2)+'\n')
(W/'mathematical-self-check.md').write_text('''# 完整数学自查

1. F(q,a)只在q_a>0定义；含a的兴趣类型分母正，不含a直接零；H0合法，m1一般机制有效，三角源另需m≥2,p≥3。
2. 势端点e_q−e_(q−ea)属于m/m−1两层；映射到P后才是型向量。收益顶点配平→势配平→类型零和，逆向不自动，P自身依赖可能产生更多lineality。
3. 所有行来自原完整有序σ真实后继；λ≥0势平衡且λ_j>0才可除该λ移项。形式机制不预设SPE；合法实例逐39比较另证。
4. 客户重数3,2,3,2,3,1,1总15，各主题正私有；actual ACA三人各13/3，漏B私有2，W13/OPT15，2W−OPT11。只有存在这份策略，不声称严格/唯一。
5. 完整13历史保根、三第二层及九末位；39松弛均是原完整输出无损表式，不是新run。全部真实后继而非静态冻结。
6. g0…g3端点分别ACA/BAA、ACA/AAC、BAA/BCA、CAB/CAA；相加为背景eA标签(C,A,B)六边源。g0_AB1/6而g3_AB0，g3_A−1/2非零。
7. 手工18收益端点邻接列完39边的合并非自环；只有201:A与111:B互达，外出到汇点，其他非汇点无回路。旧像空间恰span(g3)一维，根行负向由其余三行支付，严格扩张；未求完整lineality维数。
8. 独立源码Floyd不同于发现DFS，main guard/--output排他创建明确；未import/运行。其报告11字段没有完整39表、rank、势端点或111三角回归。源码读完不等于本次执行。
9. 本次只3主源receipt；3个related原件全文读和保留但不额外done。源码/冻结JSON无raw argv、代码SHA、环境/exit日志，未倒填。没有新疑点，不重复原成功有限审计。
10. 原发现稿独审待回执已由后续2948B内部审查补足，外审/新颖性未认证；一般half未由机制证明，旧任意人数OPEN不覆盖当前另有五人定理的状态。
''')
# Completed source navigation says this is related only; suggest it without claiming availability.
next_ids=['3fb17764a6930667e3a2','b2cc74c6caa0cb212eb3','0d2f5d5b27d611918123','279a9b74712bc014f2ab']
inv=[json.loads(x) for x in (R/'cleanup/inventory.jsonl').read_text().splitlines()]
(W/'next-candidates.json').write_text(json.dumps([{'id':i,'path':next(x for x in inv if x['id']==i)['path'],'note':'本批已related全文读并保全或入口已读；如最新状态尚未完成，可按实际对象去向单独处理，不把本三主源done当这些源done。'} for i in next_ids],ensure_ascii=False,indent=2)+'\n')
(W/'delivery.json').write_text(json.dumps({'status':'ready-for-parent-review-and-serial-publish','source_ids':[r['id'] for r in receipts],'primary_bytes':8026,'formal_paths':[lemma,construct,review],'evidence_root':str(E.relative_to(B)),'receipt_file':str((W/'semantic-receipts.json').relative_to(B)),'owner_snapshot':str((W/'owner-snapshot.json').relative_to(B)),'actual_original_runs':0,'actual_new_math_runs':0,'external_stage_root':str(B),'clone_changes':0,'pending_cross_group_file':probe,'all_written_paths':sorted(str(p.relative_to(B)) for p in B.rglob('*') if p.is_file())},ensure_ascii=False,indent=2)+'\n')
print('receipts=3; relations=6; original/math runs=0')
