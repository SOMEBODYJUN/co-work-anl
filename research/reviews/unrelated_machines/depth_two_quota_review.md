# 两层异质需求半配额贪心的独立重构与冻结审查

## 审查对象与边界

审查身份：本轮boss9内部独立研究者 depth_two_reconstruct；不是独立持久Work身份，不对外发言，不操作Git。先收到精确候选问题r→U→W及b(H)定义，未获主研究者的证明路线。先阅读一般桥梁合同以固定输出树和原需求计分，再独立将阈值问题重构为异质完整配额的互异叶星包装；独立提出最小半配额贪心及按首次失效收费的证明。此后才收到主研究者独立得到的同一候选和证明摘要。

最终冻结审查对象：

- 正文 `research/current/unrelated_machines/rooted_dag_degree_token_bridge.md` 全文件SHA256：`824d69df9dd1ba2730433a5bc3e9f88bd97a6908a51947a7ebc35c2e6e7e659b`。本次实质审查范围是§7；§1—6的一般桥梁只作为已另行审查的依赖，没有把本次审查冒称为其从零全量复审。末次复核确认：从先前受审哈希`c5f79d8a4754fcaa6ba07d47eaae55d606fa1c08e5008f9c38060fe2aa83b94f`到当前版本，只将首段“不是新的近似算法或困难性”限缩为“不是一般不相关机的新近似算法或困难性；第7节另给浅层正面构造”。以反向替换后重算SHA256独立核对了这个单处文字变更；§7数学内容和规范代码均未改变，原审查结论保持。
- 规范实现 `tests/audits/unrelated_machines/depth_two_quota_greedy.py` SHA256：`dd160d6977fb395992f81cfbe92208e6404648a4dbc6844d4d24357f022a663e`。核对half_stars、depth_two_half，以及其调用的validate、candidate_thresholds、score、tree_to_schedule、loads实现。
- 独立核验 `tests/audits/unrelated_machines/depth_two_quota_independent.py`，SHA256：`c5f5f32f59fb65607e3ecd81b3c37e7d25385e8cea99a93d618e2b32fe7fdc4b`；结果 `evidence/runs/unrelated_machines/depth_two_quota_independent.json`。不导入规范greedy。
- 规范构造交叉审计 `tests/audits/unrelated_machines/depth_two_quota_conformance.py`，SHA256：`1adbcfc8620ed2462829a5b5e148382be05411b3921df0506676b3561858d5a7`；结果 `evidence/runs/unrelated_machines/depth_two_quota_conformance.json`。它仅导入被测规范模块，独立oracle自含。`--repo`可显式指定仓库根；放于上述规范路径时默认从脚本位置恢复仓库根，不依赖某个scratch路径。

## 一般证明的独立攻击

1. **可选中心和真实树。** 只有根邻居能计入根度；规范代码以out[root]建neighbors，正确忽略不可达正需求中心。每个W最多分给一个中心，所有选中U都连根，所以输出是D的实际根树，不只是度向量。正需求但零出度U不能作为免费终端，算法不会选它。
2. **完整配额到半配额。** d_u=ceil(τk_u)为正整数，a_u=ceil(d_u/2)=ceil(τk_u/2)。完整基准S_u至少有d_u叶；u首次失效时至少丢d_u−a_u+1≥a_u个基准叶。即使实际邻域大于S_u，此下界仍成立。
3. **收费的候选资格。** 只对O\G中心的最先a_u个被占基准叶收费。这些占用不晚于首次失效，步骤开始时u仍未选且可行；故最小配额规则确实给a_x≤a_u。若对失效后全部叶继续收费，此推理会失效；最终正文明确排除了这一错误。
4. **全球资源唯一性。** 基准S_u两两不交，一个实际占用叶最多被一个基准中心收费。每步占用a_x叶，每次费≤1/a_x，总费≤1。所得是|O\G|≤|G|，再加|O∩G|≤|G|，不是错误地声称|O|≤|G|。
5. **根需求和截断。** τ=b*那次有K≥τk_r和2G≥K，从而G/k_r≥τ/2，无需根满需承诺。可选剪根到min(k_r,G)时，由τ≤1仍保留≥τk_r/2。每个U比例也≥τ/2，截断项1足够。b*=0、空U/空W、死根默认均覆盖；根为终端由原桥梁另行精确处理。
6. **未知b*和阈值枚举。** Γ含最优树的承重整数度比，或截断值1，因此b*>0时必有b*∈Γ。程序调用通用candidate_thresholds还可能多列不可达U的比值；这些额外迭代不影响正确性，仍至多1+|E|。程序只保留实际评分最好的树，没有将失败迭代用作不可行证书。
7. **总位复杂度。** 所有quota在比较显式残余度之后才分配资源，选中时quota≤|W|；循环次数至多|U|，实际占叶总数至多|W|。Γ总规模由显式边数控制。大二进制需求只进入整数乘除和位多项式比较；没有按需求值建立槽或枚举1,…,k。
8. **实际调度和近似比。** 代码真正调用tree_to_schedule并返回具体assignment；独立读取jobs的可用端及Fraction处理时间重算负载，未只比较一条公式。使用原桥梁OPT=2−b*，有3OPT/2−(2−b*/2)=1−b*≥0。此范围只覆盖深度二的桥梁输入族，不能升级UM-TARGET-v1。

以上未发现仍成立的fatal objection。

## 有限可复现核验

独立代码以Python 3.12.14、整数及fractions.Fraction运行；没有误差阈值，没有外部优化器。

以下命令从仓库根运行，默认只向stdout输出，可将新复现写到scratch；不得覆盖冻结证据。

规范构造审计：`python3 tests/audits/unrelated_machines/depth_two_quota_greedy.py`；冻结结果 `evidence/runs/unrelated_machines/depth_two_quota_audit.json`。

- 枚举(U,W)∈{(0,0),(1,2),(2,2)}、全部允许的根边/两层边子集，以及根和全部U需求在{1,2,3}中任取，共1803个输入。其独立oracle枚举全部边子集、检查入度和根可达性并自行计算瓶颈值。
- 另有seed=916202610的250个随机实例、4个退化/大需求/非零根/不可达中心边界，以及3个非法层状合同拒绝检查。
- 这一份会调用规范构造及实际树→调度接口，有限核对调度负载；它不证明一般算法保证。

独立全选择审计：`python3 tests/audits/unrelated_machines/depth_two_quota_independent.py`；冻结结果 `evidence/runs/unrelated_machines/depth_two_quota_independent.json`。

- 完整星包装oracle用逐中心跳过/选取所有完整d_u叶子集的动态规划；greedy oracle枚举所有最小配额中心并列以及全部可用叶子集，取最坏最终中心数。不是只核对某一种恰好表现好的并列规则。
- U=0,…,3，W=0,…,4，全部二分图，全部d_u∈{1,2,3}，共129554个输入均满足2G≥O。输入数另由Σ_{u=0}^3Σ_{w=0}^4(3·2^w)^u反算核对。
- 用“每个叶的目的中心或未用”的独立枚举重构b*，核对4006个深度二实例：6个明确退化/共享/大需求边界，加seed=940327的4000个样本，U≤4、W≤5，需求来自{1,2,3,5,7,2^100+267,2^100+269}。均2b_alg≥b*且2C≤3OPT。这里b_alg是独立确定性实现的输出，不冒称已经运行规范实现。
- 6728组有理参数/需求核对嵌套ceil恒等；一般恒等和一般保证仍由正文证明承担。

冻结规范代码与自含独立oracle另做直接对照，命令：

`python3 tests/audits/unrelated_machines/depth_two_quota_conformance.py`；冻结结果 `evidence/runs/unrelated_machines/depth_two_quota_conformance.json`。

其脚本SHA256为`1adbcfc8620ed2462829a5b5e148382be05411b3921df0506676b3561858d5a7`。开头记录正文/规范代码哈希，结束检查文件未变，本冻结运行记录为上述受审哈希。使用seed=197604919生成1000个U≤4、W≤5实例，随机根编号、随机缺少根边、任意共享资源、需求来自{1,2,3,5,2^130+33}；其中631个含不可达中心，758个根编号非零，464个含131位需求。全部通过自含独立每叶目的地枚举的b*比较、实际树合法性检查、逐job可用性与实际有理负载重算，以及3/2调度界。

以上是有限实现证据，不覆盖所有输入，也不作为一般证明。审查本身没有调用穷举oracle作为算法子程序。

## 非致命限制与结论

- 算法的最小配额规则承重，改成任意可行中心不能复用该证明。
- 单次贪心半根度例仅说明此规则允许的坏选择；配额为1时最大匹配即可修复，所以不构成该问题的不可改善性或计算困难性。
- Bamas2025原始PDF只作为新颖性线索重读：其printed p3的递归greedy叙述对均匀k_u=k给O(ℓ)近似并有n^{O(ℓ)}时间；这不能直接认证本异质位模型的精确常数2新颖性。当前合理定位为标准charging的局部primitive；未认证独立论文价值，没有外审。
- 本轮不声称一般深度DAG有常数根树近似，也不声称已跨过一般不相关机调度2壁垒。

结论：冻结正文§7的一般证明与规范构造无未处理fatal objection；有限独立oracle与规范代码对照均通过。建议按“有自足证明、内部独立重构通过、实现有限核验通过、外审未做、新颖性未认证、UM-TARGET-v1仍OPEN”分轴登记。
