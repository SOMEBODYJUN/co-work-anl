# Direct cohabiting canonical actual-read-after：typed_edge_gap，正式仅B

审查者 typed_edge_gap，2026-10-18。仅scratch记录，不修改repo/Work/Git。

## 实际读取与正式范围

已实际全文通读canonical：
/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/direct_cohabiting_query_return_strict_sat_and_sharp_escape.md
实核SHA256 3e6ac499c73cf5c084ed5623ede2cb921214192c8f5e3aa9f859ecdc80147607。

正式actual canonical-read-after只认证共同域§1及B的§2–3，即ID UM-WEIGHTED-DIRECT-COHABITING-QUERY-RETURN-ALL-FORMULA-FAILURE-v1。§4按授权实际读取为上下文，但不代审C的sharp Claim，不认证其最优值/阈值或有限运行声明；没有读取C对应其它作者Proof/独立推导/审查文件，也没有运行其audit。

## 原始先行证据与真实先后归属

B Exact实读SHA076561e78796927d6792f6dfb3c581c11afd263752b9098abd9f35d58df2ddfb。
B独立Exact-only记录先冻：weighted_direct_cohabiting_query_return_all_formula_failure_exact_only_review_typed_edge_gap_v1.md，SHA6d853646c525a26a0776c4dc393650f95d2c3ae6de882ab64a001a8ed5a40c00。
B作者Proof后实读SHA82783900de69ccb3e14aa187c7aa8a2e2146934d404686f2d67d0dcedbc1b571。
B作者Proof read-after另冻：weighted_direct_cohabiting_query_return_all_formula_failure_read_after_typed_edge_gap_v1.md，SHAb91adadb3d917a7826ea96ac1effab755ea669cbabe26d91bd753379f5c93253。

canonical所记“作者一次向reviewer简述策略发生在独立记录已冻结之后”真实对应：作者rainbow发来本B新candidate的简述及active virtual共同matching策略时，6d853...独立记录已经写完并取得SHA；该摘要随后到达。它不是本B独立重构的先行证据。再后才经root授权实际全文读B作者Proof。这个顺序已在给root的即时消息及独立后的read-after记录如实区分，没有反向改写原独立文件。

既有保护环/matching技巧本来是背景，B Exact也明示技术来源；没有把“通用旧技巧已知”冒称“本B新异权矩阵的作者策略先给了独立审查者”。独立性针对本B的具体P/异权/混合分支推导，不宣称matching技术原创。

## §1共同域核对

- 原P与B Exact完全一致：每i两台M_i,C_i及q_i,b_i；q三个端M_i:ρ、M_i+:1、C_i:x_i；b两个端pin:ρ/C_i:1；每clause u仅对自身真实occurrences的C_i有y_i端。没有D/h、真实公共R或额外免费状态。
- ρ∈(1/2,1)，真实x/y正且和≤1，dummy x1；全部finite≤1从这些条件自动成立。只保出现变量，显式环padding≥3。每occ唯一属于一个clause，重复literal/变量不合并任务。
- 空公式一idle机零jobs的合法UM域明确，OPT0不借非空下界。非空2N机、2N+m jobs、5N+L finite与dense 2N(2N+m)计数正确。额外长dummy列表按实际N计，无隐藏指数展开。

## §2严格SAT双向身份核对

正向同满足赋值方向z，每clause仅选一枚真文字，q+u在C真共居x+y≤1，b返回pin替代同向q槽，其余q含dummy沿环、b留C；每原job一次，每M恰一件，全部负载≤1。

反向E⊆R使用正x，内部M全是>1/2的q/b使N−|E|+|R|≤N，故E=R且M恰一件。正y使u不能读unit b，只能读同编号q；有效环任务方程给整变量环同方向，返回s=z给clause真文字。额外真实exports/returns与dummy全部仍在计数中，没有免费同编号关系，也未用未知SAT赋值构造反向。

此部分与6d853...的全槽饱和独立推导及作者E/R计数均相合，canonical没有扩域到零x/零y、unit/empty clauses或ρ=1/2。

## §3共同active匹配及全部原jobs核对

baseline是有某y≤1/2，active的全部y>1/2迫全部x<1/2；没有从异权中错误抽取单个公共e。辅助图包含全部q/b及仅active u，右侧全部M/C及每active一个virtual V。无q→C图边。baseline/dummy C的唯一邻居b强制它们留C，q必须内部；所以active不能偷用baseline返回容量。

θ_i=1/k_c≤1/2保证fractional边非负；q的pin扣θ由同编号b补回；各M/C/V列和与q/b/u行和同时1。一个共同整数perfect matching给全局互异返回pins，不是分clause拼局部见证。每active V唯一q_j，每active u占C_r且仅该b_r返回；允许j/r错配是结论而非附加身份。

恢复时每q→V确实改成同一原q→自身原C，保输入真实x；全部其它图jobs保原端及真实ρ/1/y；所有暂未入图的baseline u逐件加入。最终没有virtual目的地、没有分数执行或额外分析jobs。

实际负载表覆盖全机：M一原job≤1；baseline C为b+可选u≤1.5且无q；dummy C仅b；active留b的C可能加本编号q为1+x<1.5且无u；active返回b的C有原u、可再加本编号q，总≤x+y≤1。每occ独属一个clause，故不同u不会叠加。该分配确实同时执行全部2N+m原jobs。

active集合空仍有合法q/b环perfect matching，之后加入全部baseline u；空公式另行idle返回。全部cases未遗漏。

## 位复杂度、状态与最终认证

baseline比较为精确输入有理数与1/2比较；辅助图显式多项式规模，θ仅1/k_c，位长O(logL)。实际算法整数matching不按1/x、1/y、1/ρ或分母数值循环；输出全部原job编号与原端，实际负载回算位长多项式。dense P成本已计，implementation none符合本次仅数学审查事实；本审查没有跑软件或有限优化。

正式PASS：canonical共同域§1及B异权§2–3与已审Exact/Proof相符，无fatal或无授权量词扩张；strict SAT双向身份合同及所有公式actual≤3/2均完整。历史oldstrategybrief到达顺序的归属准确。

本记录不认证§4的sharp Claim，不把B的上界升级为sharp、固定gap困难性或一般medium复制不可能。未读取C的其它推导或运行其测试，UM-TARGET与真正tiny-gap源没有在本审查中推进为已解。
