# 五份GB报告与selected-cones的符号实核及最小修正

结论：旧《固定安全预算锥的五个精确失败实例》确实把**正预算核验**写成预算失败。这里不是仅从字段名推断；已全文读原生成器和原selected-cones研究稿，并新作独立Fraction检查：五份保存策略3882项完整IC、全部540有序静态背景上的p/Q匹配、实际C/W重算，及selected-cones全部13证书4914个坐标/真实Γ行归属/非负乘子和余项，全通过。详见同目录verify_saved_budget_and_cones.py与verification.json。该检查没有重新运行原生成器或旧审计，不新增primary receipt/done。

## 1. 目标定义与max/min方向来自真实代码

真实原文件为 archives/customer-attraction/tools/evidence/security-gluing-boss5/original/budget_menu_generator.py，SHA 51b775001f14b0e7b98de20e85d82ff9daeede9a1dd8d470014657cea8bbe2a2。

- 第26–30行：menus递归，floor=max_a min_{q∈child_a}utility(a,q)，保留当前收益至少floor的可实现终局；这层max-min是完整SPE续局可实现门槛。
- 第32–34行：query_mean(own,q)先从终局减去当前own槽，再对查询主题按同一个固定p平均，精确计算F_p(B_i(own))。
- 第59–62行：偏离分支必须满足utility(b,r)≤实际u，再用max(eligible,key=query_mean)选择最大的独立查询值；外层C+=p[b]·query_mean，即C_i的两次独立p抽样。
- 第66行明确 gb=C−coverage(q)。
- 第67行用 gb>best[0]更新，因此预算目标是**最大化**ΣC−W，不是最小化、不是最大化W−ΣC，也不是最大化n·v−W。
- 第75–78行把该最大值写入GB_violation_sumC_minus_W；W与sum_C原样另存。
- 第81–90行直接运行四游戏original36/individual360/root_tax_failure/global_decorrelation_failure；individual34不是这个原入口直接输出，不能倒填第五次原run。

形式上，该固定游戏与固定p的目标为

\[
 V(G,p)=\max_{\sigma\in\operatorname{SPE}(G)}
            [\sum_iC_i(\sigma,p)-W(\sigma)].
\]

因此V<0意味着对该固定G、指定p的全部完整纯SPE，都有

\[
 W(\sigma)-\sum_iC_i(\sigma,p)\ge -V>0.
\]

这确实阻止在这些固定游戏/指定p里通过调整完整SPE平局寻找GB反例；它**不**表示GB付款接口失败。字段包含violation一词也不改变这个方向。原研究稿selected_cones_source.md第64、72、76–86行直接说“最大ΣC−W/最小W−ΣC”“所有值严格正”“改变这些固定游戏的完整SPE平局仍不能破坏给定最优p的GB”。

另一个准确性细节：生成器第49行仅先按根终局计数菜单筛选，随后第55–65行仍有每位置eligible/valid检查。不能只凭终局计数在根菜单，就断言该计数的任意有序排列都可实现；枚举算法本身保留了必要的后续检查。

## 2. 原报告准确字段、行和新重算

原字节在 archives/customer-attraction/tools/evidence/security-cones-new/original/，各SHA和全部行号另记verification.json。下面行号以这些未修改原字节为准。

| JSON文件 | GB_violation行 | W行 | sum_C行 | W | C | 最大C−W/对应最小W−C |
|---|---:|---:|---:|---:|---:|---|
| all_SPE_GB_original36.json | 218 | 224 | 225 | 34 | 187/6 | −17/6 / 17/6 |
| all_SPE_GB_individual34.json | 187 | 193 | 194 | 32 | 1252/41 | −60/41 / 60/41 |
| all_SPE_GB_individual360.json | 220 | 226 | 227 | 336 | 1191500603/3710088 | −55088965/3710088 / 55088965/3710088 |
| all_SPE_GB_root_tax_failure.json | 124 | 131 | 132 | 38 | 73/2 | −3/2 / 3/2 |
| all_SPE_GB_global_decorrelation_failure.json | 220 | 227 | 228 | 85 | 828050154289/10570351740 | −70429743611/10570351740 / 70429743611/10570351740 |

新检查不使用字段名认定含义：直接读每份game、完整strategy.actions和security.primary，逐历史核IC，沿每个实际前缀和每个强制主题补全同一策略，删除当前槽，再独立求期望C。计算出的W/C/C−W逐项完全等于上表。

还对全部合法有序静态背景核查询p保证，并对保存的对偶Q核六个纯查询封顶，精确匹配安全值分别10、2411/246、93177/908、9、508643/26546。因此指定p确为各自固定游戏的安全最优分布，不是用一个任意低保证p制造预算正值。

新检查仅重算保存的达到策略，并未重新枚举五游戏全部SPE。全SPE极值的算法方向/可实现性由上述全文读取的原生成器及selected_cones_source.md第66–86行的独立枚举说明承担。individual34的全SPE记录来自该五游戏研究稿/相应冻结JSON，不谎称是本四游戏入口的第五输出。

## 3. selected-cones的正λ实际证明什么

真实研究稿 archives/customer-attraction/tools/evidence/security-gluing-boss5/original/selected_cones_source.md：

- 第38行定义完整SPE锥w≥0、Γw≥0；
- 第40–46行给逐类型恒等式

\[
 d-\sum_BQ_Bf_B(a)=\Gamma^{T}\lambda_a+r_a,\qquad
 Q\ge0,\ \sum Q=1,\ \lambda_a,r_a\ge0.
\]

- d=d_i给整个该固定策略锥的u_i≥v_n；d=c/n给整个该固定策略锥的W≥n·v_n。
- 第48行记13证书/4914坐标；第50–60行给三固定策略的明确正向结论及边界。

实际原common_q_generator.py第16–18行把ΣQ·f+Γ^Tλ放在≤target约束左侧；第25行残差=target−ΣQ·f−ΣλΓ，第26行精确要求Q归一、所有变量非负和全部残差非负。因此其正λ是**可付款的真实激励行正组合**，并非“固定策略锥的负余项反例”。

新Fraction检查直接从selected_security_cones.json每份完整policy重建全部真实Γ行，再核每个保存row属于真实Γ、每个coefficient≥0、Q合法、63类型×6查询的残差≥0，13套共4914坐标通过。aggregate_theta_failure有target1/2/aggregate三证；其余两份各target0/1/2/3/aggregate五证。数字target按零起点玩家索引。aggregate目标真的是根实际福利系数c/n。

这三份固定策略、任意质量锥的结论，与前面的五固定游戏、指定p、全部SPE极值是**不同量词**，不能用“固定五个锥”合并。甚至global_decorrelation的selected-cones策略根动作2，而all-SPE预算达到策略根动作5；文件沿用实例名不使二者成为同一完整策略证书。

## 4. 可立即使用的最小修正方案

同目录proposed-existing-budget-page.md为旧障碍页的完整可替换正文，保原稳定id/源列表/原表数值/路径，不改冻结JSON或重done。将“失败”准确改为“在指定固定搜索空间无法攻击GB”的有限障碍，明确五固定游戏正预算与三固定策略锥正证书是不同对象，并接现有《指定完整策略锥安全证书与预算边界》。

同目录generator-review-wording.patch只修相邻生成器审查中的反向标签和根菜单成员身份的过强句子，保全部算法/数值/运行历史。若Boss先只紧急纠正已知反向结论，可先替换旧障碍页，再应用这些有限措辞修改；无需新增对象或改旧源done。

本次只读现有冻结证据和正式对象，未改共享页。尝试读取原规范selected预算审计脚本时，本地GIT_NO_LAZY_FETCH的git show返回“fatal: bad object 68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/customer_attraction_selected_security_budgets.py”（exit128），没有401/403或凭据挑战，未重试/换凭据。这里没有冒称读到或运行那份缺失blob；实际核查由现有完整原生成器、研究稿、原JSON及本次自写Fraction检查完成，证据闭合不依赖该脚本。

执行身份补记：自写检查先核保存策略与13套λ，随后增加五组完整静态p/Q检查后再次执行，两次均通过；当前verification.json来自补全后的版本。不将其称为旧原审计的一次重跑。
