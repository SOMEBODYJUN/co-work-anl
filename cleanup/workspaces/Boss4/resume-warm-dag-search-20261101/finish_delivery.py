from pathlib import Path
import json
B=Path('/workspace/scratch/37f0f9248cfc/warm-dag-search-stage');W=B/'cleanup/workspaces/Boss4/resume-warm-dag-search-20261101';E=B/'archives/customer-attraction/subarchives/six-providers/tools/evidence/warm-dag-discovery-primary'
b='archives/customer-attraction/subarchives/six-providers/state/'
prog=b+'程序/完整终局见证的热启动向量与受限搜索合同--程序.md';calc=b+'计算/两人两主题热启动原始对偶证书与版本边界--计算.md'
p=B/prog;s=p.read_text();s=s.replace('原status字符串、实测solver秒','原status字符串、实测solver秒');s=s.replace('h.run()后取solution/info/model status。','adapter未沿用传入options字典作设置，而是以上述自身参数直接设HiGHS；h.run()后取solution/info/model status。')
s=s.replace('本批未取得20a37…源码，不能补造差异发生在何行','本批未取得20a37…源码，不能补造差异发生在何行');s=s.replace('文件内容可作为历史运行及独立可算证书保留，而非当前9844B脚本的已验证运行。','文件内容可作为历史运行及独立可算证书保留，而非当前9844B脚本的已验证运行。报告也未记helper/model/exact/certificate源码哈希，旧DAG哈希相同并不绑定旧运行整个导入闭包。')
s=s.replace('parameters完整CLI配置；','parameters完整CLI配置（objective_floor记录原args.floor，因此null不等于build未施加默认seed比率下界）；')
p.write_text(s)
p=B/calc;s=p.read_text();s=s.replace('原norm seed的两个根可实现终局','parameters.objective_floor=null只记录未显式给--floor；本冻结现代码在此配置会自动把seed比率1.5作为build下界，不能由null反称原运行无floor，旧版本实际实现仍须其源码。原报告只有warm/旧DAG两个代码哈希，未绑定helper和规范模型的旧执行版本。\n\n原norm seed的两个根可实现终局');p.write_text(s)
M=json.loads((E/'source-manifest.json').read_text())
notes={
'0cce6d9347944260698c':('9844B全文：原布局动态DAG依赖、全部12CLI参数、seed singleton/seed-file输入、oracle R(k)/threshold正福利校验、完整同序y/z/x/t向量、WarmSolver菜单上界/float残差/Hamming行/私有HiGHS全部选项与API状态、cold仍构造seed、完整展开0.9、固定policy精确恢复、两段stdout及覆盖写最终JSON/代码hash。','全文读9778B底层DAG、20567B策略锥helper、model/exact/certificate/init、6193BREADME、3471B审计源码，与已归档终局见证等价/原成功有限审计比较，不重复60个旧MIP等。核小报告warm hash20a37…与当前6e419…不同，旧DAG c7d550…匹配；未知旧版本不猜diff或以新run覆盖。','完整原代码与8件related/依赖原布局保留，正式程序对象自足证明合法seed编码和限制域，逐项分开浮点搜索、固定policy有理原始/对偶和全SPE目标；当前版本未借旧报告冒已执行，原CLI/import/优化/oracle/策略复跑0。','retained'),
'23a9decde7450d02d501':('2491B完整9根字段组：scope/universal false/seed；全部环境及两代码哈希；m2p2参数含null floor/coldfalse/无限制；seed两个根/6计数3叶8retained与构造时间；所有solver/milp字段和实测float数；exact3/2、克隆2,1,0、对偶row0系数1、W2/OPT3/3节点3非self及全部三动作。','与当前warm/旧DAG/helper逐字段比较；current warm SHA不匹配原environment，不能认证当前脚本。原明确策略和整数客户可直接解析三比较，固定锥两行排序、β3/2/μ0=1余项0,0,1/2完整重构；与现两主题一般回归基准一致，但不冒MIP全域精确最优。','整合为自足小证书计算对象并保全部原记录/环境时间身份和版本断口。未知旧20a37源码不影响显式数学点的直接证明，但不绑定当前9844B adapter；JSON状态不升级为普遍half或六人结论，未重跑实验。','integrated'),
'29d0b0997f32f56dd8cf':('150B全部四字段实读：schema1、save customer-attraction、actor R-44b24f3962bd4f68a4b6913610c0d417、instance47c2dd9a35e747ea9286ade9660b79c1。','与R44已归档入口/true_counterexample README及两实际数学主源比对，确认这是旧协作工作区身份/路由，不含客户、主题、策略、DAG变量或数学断言，也非当前Boss4身份。','按历史来源元数据retained：原字节和程序对象四字段说明完整保留，不用其instance键推断客户输入，不激活旧身份或另造数学对象；无独有数学论证被丢弃。','retained')}
records=[]
for r in M:
 if not r['primary']:continue
 a,b,c,d=notes[r['id']];targets=[prog,r['local_path']]
 if r['id']=='23a9decde7450d02d501':targets=[calc]+targets
 records.append({'id':r['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a,'comparison_note':b,'decision_note':c,'disposition':d,'targets':targets})
(W/'semantic-receipts.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
rels=[{'type':'implementation-of-existence-encoding','from':'cag-outcome-witness-dag-full-history-realizability','to':'customer-attraction/warm-start-outcome-witness-DAG-adapter-contract','reason':'完整R(k)和共同阈值为全部y/z/x/t给精确可行起点；同计数不同desired可异动作，非Markov净化。','evidence':'initial_vector全代码及程序对象四步构造证明'},
{'type':'exact-fixed-policy-certification','from':'customer-attraction/warm-start-outcome-witness-DAG-adapter-contract','to':'customer-attraction/two-player-two-topic-warm-start-fixed-policy-certificate-version-boundary','reason':'DAG展开一张完整动作表后固定锥LP可恢复有理原始/对偶；小点三历史直接重构，β3/2只属该policy锥。','evidence':'23a9…全部JSON；9778B exact_optimize；20567B StrategyCone'},
{'type':'historical-source-version-boundary','from':'23a9decde7450d02d501','to':'0cce6d9347944260698c','reason':'旧样本warm代码hash20a37…与当前6e419…不同，不能连成当前已执行认证；只共享旧DAGc7d550…版本及可算数学点。','evidence':'version-and-execution-scope.json；两原件SHA'},
{'type':'metadata-provenance','from':'29d0b0997f32f56dd8cf','to':'customer-attraction/warm-start-outcome-witness-DAG-adapter-contract','reason':'四字段保旧工作区身份，instance键非数学输入，不切换当前actor。','evidence':'150B全文、程序对象元资料段'},
{'type':'implementation-followup-not-new-welfare-bound','from':'cag-outcome-witness-dag-audit-and-fixed-cone-budget','to':'customer-attraction/warm-start-outcome-witness-DAG-adapter-contract','reason':'原自由重数DAG启动瓶颈可用可行向量改善，原成功审计不证明warm现版本或全MIP全局最优。','evidence':'既有计算资源全文、6193B工作区README；当前零旧实验复跑'}]
(W/'relation-evidence.json').write_text(json.dumps({'stage':'phase2-human-relation-review','map_modified':False,'reason':'只写自身独立新对象和证据，Boss串行发布，阶段三超图不由链接自动造边。','relations':rels,'nonimplications':'两人样本不迁移六人；float kOptimal/gap0不推出精确MIP全局界；固定policy锥对偶不覆盖其它策略；未知旧warm hash不靠重跑现版本消除。'},ensure_ascii=False,indent=2)+'\n')
(W/'mathematical-self-check.md').write_text('''# 数学与实现自查

1. 合法seed是非负整数类型客户、m/p正、q在完整SPE终局R(0)且W(q)>0；归一化每主题≤W、bigM1来自原SPE实际角色保证，不是float residual证明。
2. y集合除root仅q外全R(k)，终局自身；z为每desired选择合格行动，x为每行动最小利润孩子，t=M(k)/W。索引逐states y/t后再z/x，完全配旧DAG。非Markov目标不被删。
3. restrict只冻结seed0的y上界；radius行恰二元Hamming≤R，连续客户/t不受半径。float残差在加radius前，adapter本身无独立整性核；cold仍构造seed。
4. fixed root/portfolio客户重数自由，不是固定seed；显式portfolio不验范围/重复/≤m且helper bit求和会进位，默认合法，小点合法。参数floor null不表示无默认seed下界。
5. 私有HiGHS passModel/setSolution和float kOptimal/gap0只生成见证；expand≥0.9后仍需精确policy核。
6. fixedpolicy精确恢复先limitdenominator再active-row精确消元、严格verify、清分母/gcd、全有序直接Fraction比较。βw−Γᵀμ≥objective及μ≥0才给固定policy上界，certified primal不保证dual optimal，更不保证MIP全局。
7. 小点allA三历史真实偏离松弛0/0/3/2，W2OPT3；去重Γ0=(1/2,−1,0)、Γ1=(1,−1/2,0)，原始(1,1/2,0)，β3/2和μ0=1余项(0,0,1/2)。全部解析重构，无新数学代码执行。
8. warm报告hash20a37…≠当前6e419…；旧DAGc7d550…相同，不绑定未记录hash的helper/model旧版本。未知旧warm代码未取得，不猜差异，不借新run认证旧run。
9. 150B workspace四字段仅旧路由身份，无数学输入，不切换Boss4。3源12485B与8related/依赖全SHA保，related不额外done。
10. 0原CLI/import/MIP/LP/oracle/策略复跑；旧成功有限实验不重复，大报告/42输出未读不冒已认证。一般五人后续别证与六人OPEN保持各自范围。
''')
(W/'next-candidates.json').write_text(json.dumps([{'id':'a607df1fe2b98e17868c','reason':'本批related全文读README，全部大证书/性能/受限菜单引用需各自逐源清洗，不自动done。'},{'id':'c18e27c5f56908a85700','reason':'本批related审计源码全文读，有限42域/拒绝/非Markov依赖及版本尚应结合其原输出独立处理；不建议重跑成功原实验。'},{'id':'23c8f24257358e43f87d','reason':'原14009B warm_seed_audit输出本批未读，不因3471B源码或README作者声明而done。'}],ensure_ascii=False,indent=2)+'\n')
(W/'delivery.json').write_text(json.dumps({'status':'ready-for-parent-review-and-serial-checkpoint','external_stage_root':str(B),'source_ids':[r['id'] for r in records],'primary_files':3,'primary_bytes':12485,'formal_paths':[prog,calc],'evidence_root':str(E.relative_to(B)),'receipt_file':str((W/'semantic-receipts.json').relative_to(B)),'owner_snapshot':str((W/'owner-snapshot.json').relative_to(B)),'math_runs':0,'clone_mutations':0,'version_gap':'old sample warm20a37… not matching current9844B warm6e419…; same old9778B DAGc7d550…','all_written_paths':sorted(str(p.relative_to(B)) for p in B.rglob('*') if p.is_file())},ensure_ascii=False,indent=2)+'\n')
print('wrote 3 receipts, 5 relations, 0 math runs')
