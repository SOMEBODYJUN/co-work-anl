from pathlib import Path
from collections import Counter
import json,hashlib
REPO=Path('/workspace/scratch/cd4305a146e6/co-work-anl-boss3');W=REPO/'cleanup/workspaces/Boss3/resume-20261102/c';BASE=REPO/'archives/customer-attraction/tools/evidence/boss3-c16-resumed';PFX='research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/'
items=json.loads((BASE/'source-manifest.json').read_text());objs=json.loads((W/'object-index.json').read_text());paths={}
for rel,meta in objs.items():
 for src in meta['sources']:paths.setdefault(src.split('#')[0],[]).append('archives/customer-attraction/state/'+rel)
# Each note describes that particular primary file, rather than a directory label.
notes={
'CLAIMS.md':'全文读取B8-REFINED-ACTUAL-TAX-NO-v1全部量词/定义域/依赖/证据/反证范围/状态，m13与任意k未证分明。',
'README.md':'全文读取旧Boss8/R-c50身份、恢复基线、任意人数目标、六目录地图、税桥后续与直接padding的额外core分支缺口。',
'workspace.json':'完整读取schema1/save customer-attraction/actor R-c50/instance4aa4四字段，仅来源身份信息。',
'background/exchangeable_probe.py':'1738B全源码；choose/miss/超几何leader、orbit总质量、两根收益≤1、逐r覆盖LP、m2…15循环及有理化/写出。',
'background/exchangeable_probe.json':'全部14组L=m2…15、每组全部m+1个值、best r/value/support均消费；与明确有理可行公式逐项比较，非精确最优认证。',
'credible/audit_reciprocal_tail.py':'1404B全源码；t1…100系数恒等式、x7/a11、逐单位末位2对5/2与全部输出；本次原样一次exit0。',
'credible/reciprocal_tail_obstruction.md':'全文三个指定真实路径、根/末位必要式、a≤(3−t)x/[2(t+1)]、t≥2严格末位偏离及未排除变化，解析逐式重推。',
'credible/audit_refined_tax_blind.py':'6856B全文；硬编码36单位/LCM、全部counts集合值BI、(counts,target,active)自动机、每真偏离、历史重数与税；未读packet的实现边界。',
'credible/refined_tax_blind_audit.json':'全部BI27132/8568/root11、27244/18675/93375、14层状态/历史重数、13步路径准入、g/G/gap及旧seconds均读取。',
'credible/audit_security_packet.py':'4727B全文；gzip/SHA、逐单位Fraction、完全忽略desired、真child逆推、93375非自比较、14层6^d重数和可达性。',
'credible/security_packet_audit.json':'全部输入路径/SHA、27243/18675/93375/min0、14层重数/总历史、actual/counts/g/G/gap和三个声明布尔读取。',
'credible/count_joint.py':'6287B全文；w/U/z变量、条件m、path/c归一/目录界/效率、浮点MILP、全历史展开与精确固定锥后处理、output guard及依赖。',
'credible/count_joint_7_5_00112.json':'381649B全部字段、2801动作及127克隆消费；330count态/actual00112，一全兴趣客户，45秒时限、ratio1、无精确dual。',
'credible/count_joint_selftest.json':'1185B全部m2/p2、三动作/三克隆、status0/38行/15变量、ratio3/2/dual row0均读；直接解码(1/2,−1,0)与β3/2证书。',
'global/additive_terminal_search.py':'2471B全文；随机整数种子、全有序树与float平局、真IC固定锥、O−2W+ulast、正gap浮点输出/早停；没有随批运行结果。',
'global/last_player_probe.py':'1075B全文；两人默认k4、全reply函数、根0/末位BR、两主题比较与LP/正或无界早停；批内没有其stdout。',
'independent/README.md':'2228B全文；22客户资产、残余覆盖/Markov两停止理由、最优私有区cardinality未付款、产品非NE及tree他人审查进行中。',
'independent/markov_root_probe.py':'3568B全文；reverse count DAG统一后继/同终局取商、found等全outcomes提前停/cap跳过、随机类型及规范solver比较。',
'independent/markov_3x3.json':'192B全字段：1000 samples/checked、skipped0、max232、p3/m3、seed816/cap1000000；仅有限阴性。',
'independent/population_audit.py':'3320B全文；22单位Fraction、完整有序R(h)递推、106节点全部表项、21/85动作证书真实比较；原样一次exit0。',
'independent/population_audit.json':'154564B全字段含106节点每history/floor/四孩子min/max/counts/outcomes，与本次原程序新全报告整体JSON相等。',
'independent/population_nonmonotonicity.md':'3411B全文；九型22客户、全部三/四人终局/根收益、全集递推必要充分及审查层次，证明独立重构。',
'independent/population_probe.json':'1323B全文：11型共27客户、players5/sample52/topics4、m1…5最差福利[16,25,26,25,26]，与22客户版区别。',
'independent/population_small.json':'12178B全部九型22客户/minimum/all_outcomes、21+85动作及声明终局读取；动作原审计全核，声明计数另与实际follow核同。',
'independent/product_nonNE.json':'1187B全部四主题/四型7客户、q/静态2→3/五动作/终局计数；按定义解析列出全部末位和根收益，无附属程序冒称。',
'root_audits/check_automaton.py':'7137B全文；输入合法/真边递归/desired可选核/全可达/单位效率/OPT子集/税；零客、一人与盈利/错误边负控。',
'root_audits/refined_tax_root.json':'1232B全字段：packet/checker SHA、四自检及audit36/13/6/27243/18675/112050/路径/收益/税/half；旧事件不当新PASS。',
'security/README.md':'2064B全文；精确税反例域、六资源链接、两违量/真安全列、三角色内部审查与任意k停点。',
'security/build_refined_tax_packet.py':'2798B全文；旧11客户fixture/k偶数/P质量5k/2、(counts,promise)全行动闭包、最低偏离孩子/priority、硬编码gzip输出/stats。',
'security/padding_probe.py':'1607B全文；core翻2/P质量5k、默认六k、目标存在及逐路径floor、g/G/min_u打印；无一般闭包或随批各k输出。',
'security/refined_tax_k10_packet.json.gz':'372216B全gzip解压消费27243节点全部counts/action/children/desired/terminal及scope/instance/root/expected/stats；成熟同SHA资格复用，0新IC。',
'security/audit_refined_tax_packet.py':'4371B全文；36单位/LCM、每边递增/可达、逆推真终局/desired、112050比较、税/OPT/static安全列全部理解。',
'security/refined_tax_k10_audit.json':'1369B所有字段：27132counts/19164ties/112050含self、两违量、12槽安全背景/六查询/1/2余额；保旧成熟认证。',
 'tree/all_support_shapley_circuits.md':'4948B全文；正积分/交错λ、最高支持β、三角恢复与v−d独立身份signed充要、双支持/等计数交换；逐式证明重构。',
 'tree/verify_all_support_shapley.py':'3347B全文；逐类型边际、三角身份零化/Fraction秩、等计数theta及五参数main；本次原样一次全部成功。',
 'tree/verify_signed_obstruction.py':'3934B全源码；85320恢复后全259动作/336收益/1554 IC/18480稀释/效率/比较/原子及双输出；原样一次成功。',
 'tree/signed_obstruction_exact.json':'26641B全部56型signed Fraction和259常2动作、scope/n/p/target/actual/coverage全读，与本次原恢复器输出逐字节相同。',
 'tree/signed_obstruction_report.json':'697B全字段：259/1554/18480/336、三最小值、W1/160/79、97负原子与最小支持/模式，与本次输出同字节。',
 'tree/signed_policy_search.py':'5227B全文；全收益/锐稀释float round、完整有序policy、signed warm/RNG、比较LP、有理近似/>2早停/写出；main不用exact=True。',
 'tree/signed_policy_n3_p6_best.json':'6061B全部43动作/41 signed分数、seed2802/trial10/target012/float1.8333，恢复路径353、22正19负；未赋新IC证书。',
 'tree/signed_policy_n3_p6_run.json':'2569B全部12轮trial/value/target/root/elapsed消费；无null、最大trial10、末旧秒数1.0172843933105469。',
 'tree/signed_policy_n4_p6_b_best.json':'26886B全259常2动作/56权重及seed2804/trial0/target/value、额外四型非负seed；逐项按85320恢复对比。',
 'tree/signed_policy_n4_p6_b_run.json':'227B单轮trial0/target/root/value2.0253164556963204/elapsed全读，与>2早停及best一致，不是全策略穷尽。',
 'tree/signed_policy_n5_p6_best.json':'159483B全部1555合法完整动作/62 signed Fraction，seed2801/trial0，路径54444、30正32负；未恢复全IC/稀释资格。',
 'tree/signed_policy_n5_p6_run.json':'13776B全部60轮trial0…59的value/target/root/elapsed消费，无null、最大trial0、末400.94562792778015秒。',
 'tree/symmetric_hub_probe.py':'1955B全源码；固定4/5/hub0、九per-type轨道、allhub各count IC、锐稀释/非负收益、可选≤4投影原子、双LP，无main guard。',
 'tree/symmetric_hub_local0.json':'831B全部九轨道分数及m4/p5/hub0/objective2.0253164556965357/local false；与六标签exact点不同。',
 'tree/symmetric_hub_local1.json':'786B全部九轨道分数及m4/p5/hub0/objective2/local true；hub-only −1/3，局部≤4非负不自动给全局非负实现。'
}
assert len(notes)==48
comp={
'十三人精确税证书的构造与三重内部审计--资源.md':'全文比较成熟实际弱付款桥反例、分数负载全历史核验、同题删位十三人推论；当前各套审计/构造/盲BI源码和报告逐项区分，同SHA资格复用。',
'固定人数全支持Shapley的三角身份基与等计数交换--定理.md':'全文比较成熟共同客户正边际+BC表示与固定二主题秩三纠错；共同公式一致，本源新增固定m层三角消元基与等计数交换。',
'重复互惠尾惩罚的最后位置闭包--障碍.md':'对照共同单位客户完整历史模型及本批原审计；逐式重推任意t，而非从100个例子外推，三路径合同不扩大成所有惩罚。',
'双单例直积目录的动态平局与静态偏离--反例.md':'直接逐单位求全部五历史收益；与成熟历史/计数净化分离及本批人口例区别：静态冻结获利与真实偏离后继不同。',
'四主题二十二客户的人数福利下降--反例.md':'全文比较成熟12客户三主题全部SPE人口下降及本源27→22客户版本；对应原程序新106表与冻结JSON全字段相等。',
'共同有符号客户的四人超二福利与局部负原子--障碍.md':'全文比较共同signed表示、三标签全局耦合缺口及单调Shapley互补边界；本源负原子/固定比较不同，原exact两输出本次同字节。',
'计数联合MILP的完整历史展开与限时证据--程序.md':'全文比较成熟历史/计数严格分离及仓内StrategyCone源码合同；解析解码二人dual、五人一全兴趣客户直接常收益，不重跑LP。',
'一般半覆盖旧工作区的有限探针与版本边界--资源.md':'实读成熟三人五主题历史/计数严格分离、12客户人口反例、共同signed表示及本批相应全部程序/记录；有限阴性和未恢复点不扩大。'
}
comp={k:v.replace('当前各套','当前各套') for k,v in comp.items()}
retained={'workspace.json','background/exchangeable_probe.json','credible/refined_tax_blind_audit.json','credible/security_packet_audit.json','independent/markov_3x3.json','independent/population_probe.json','root_audits/refined_tax_root.json','security/refined_tax_k10_packet.json.gz','security/refined_tax_k10_audit.json','tree/signed_policy_n3_p6_best.json','tree/signed_policy_n3_p6_run.json','tree/signed_policy_n5_p6_best.json','tree/signed_policy_n5_p6_run.json','tree/symmetric_hub_local0.json','tree/symmetric_hub_local1.json'}
receipts=[]
for x in items:
 rel=x['path'][len(PFX):];targets=list(dict.fromkeys(paths[rel]));assert rel in notes and targets
 for t in targets:assert (REPO/t).is_file()
 primary=Path(targets[0]).name
 decision=('原字节完整保留为可接续资源，正式对象解释其独有版本/有限范围；' if rel in retained else '独有数学/程序合同已写入自足正式对象并链接完整原件；')+'该源具体内容按read_note及正文对应段保全，真值/审查/执行与开放缺口分别标级；本次仅四个必要有限原入口，不扩大成熟审计。'
 receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':notes[rel],'comparison_note':comp[primary],'decision_note':decision,'disposition':'retained' if rel in retained else 'integrated','targets':targets})
(W/'receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n')
(W/'delivery-paths.json').write_text(json.dumps(['archives/customer-attraction/state/'+p for p in objs]+[str(BASE.relative_to(REPO)),str(W.relative_to(REPO))],ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'receipts':len(receipts),'objects':len(objs),'dispositions':dict(Counter(r['disposition'] for r in receipts))},ensure_ascii=False))
