# 任意汇点价格覆盖与共同占位舍入的最终冻结稿读后审查

## 1. 冻结对象、读取方式与结论

被审正文：`/workspace/scratch/014c8decb8a6/co-work-anl-boss9/research/current/unrelated_machines/arbitrary_sink_private_group_price_cover_rounding.md`。

本次实际完整读取的 SHA256：

`6c23677ab25afb0db3f0c6ced6b1fb16bb8993a541c875d6b3ee2dfaf3d6e580`。

本次对当前文件先运行 sha256sum，再以 cat 实际完整读取§1–9和全部复现链接说明。没有用旧稿、独立+B证明或此前有限实验替代当前全文读取。随后重新核对三项身份、面维数/删行、价格覆盖、MW常数、未知OPT搜索、退化边界和位复杂度。

**结论：在三个声明的精确输入域内，本次未发现仍成立的实质数学异议；standing objections为零。** 首稿Q为空可能使秩下降的漏洞已经通过显式rank-preservation假设修复。这里的结论是内部完整读后核查，不是外部评审、全球新颖性认证、完整软件验收或一般UM目标完成。

本次未修改被审正文、根仓库、Git状态或冻结证据。所有新审查输出仅写独立scratch。

## 2. 修复轨迹保持独立

首稿路径为`/workspace/scratch/014c8decb8a6/price_cover_joint_rounding_draft.md`，其被审SHA是

`07e65d4798eece8159ba9c4cbad6631bf3b2c221013eba97c48e1c3cdd3c7d1f`。

首轮完整读后报告保留在`/workspace/scratch/014c8decb8a6/independent_selection/price_cover_v1_read_after_review.md`，该报告自身SHA为

`40dbb1168e0ea67374c85ce4140004e642b60b44a8a28dd377df35e3836299f1`。

旧稿的F1反例是单macro、单home、原图一条边，但该home无occupied模式：原图覆盖全部宏任务，实际模式拟阵却秩零。现稿明确要求非空模式类home集合H_Q仍覆盖全部B，并定义先限制到H_Q再作平行扩张。旧反例不满足新域，F1已关闭。结构算法成功记录的任意一轮共同宏匹配本身也证明生成菜单保住该秩。

此前实际读过的canonical准备稿SHA为`9fa1bb886e50b9393873366116fe6e58c120ad5e1617eac2d36c3849477c849f`。现稿进一步把eta复杂度说明精确为“不声称对eta的二进制编码长度为多项式”。这正确区分poly(L,1/eta)与关于bit(eta)的多项式。旧报告没有换号或替换哈希。

## 3. 第一身份：列预算单侧拟阵基舍入

`UM-UPPER-COLUMN-BUDGET-BASE-ROUNDING-v1`现在的域与结论一致。H_Q覆盖B保证基大小|B|。显式扩展保留每home的u_h≤1，正确表达home的平行类；直接复制宏邻接而省略home容量确实错误，正文与负控制都已指出。

投影顶点通过本轮逐x坐标lex最优化取得；临时lex等式下轮释放，只保留真实0/1固定。固定occupied模式不固定宏身份，宏流始终共同可调，最后才恢复实际宏匹配。删除零变量和收缩单位变量后，剩余基多面体的紧秩集合闭合并交；极大紧链分块不会被其他紧集切开，块质量是正整数，所以

`sum_e(1-x_e) <= d_face <= number_of_retained_resource_rows`。

非负列预算给全部行未来上增包络之和≤b sum(1−x)，因此可删一行上增≤b。永久0/1固定保证该行到最终最多增加删除当时的包络，不重开零元素，不再次计算固定贡献。无行时剩余基顶点整数。每轮LP系数只来自原矩阵删行加0/1约束；字典序所取顶点的统一行列式位长界、总LP次数和最终整数匹配均支撑确定性位多项式规格。

秩一k列的加性锐性例正确，只限制显式菜单接口；不推出原任务允许更多模式时仍有该误差。b=0、秩零和空资源行域也正确。

## 4. 第二身份：私有原矩阵生成真实模式

`UM-ARBITRARY-SINK-PRIVATE-GROUP-PRICE-COVER-v1`的唯一home、私有组不交、W_h≤T、a_j≤delta T、sink逐边上界p_zj≤rho a_j、宏只在homes且全有限宏边>T/2均承重。它允许无界sink数量、任意逐件资格和没有接收时间下包络，仍是给定结构的限域接口。

需求D_h=(W_h−tau T)_+。D>0的inclusion-minimal覆盖中，每件a_j>0，且总home工作量<D+delta T；因此每个实际occupied模式的总出口≤rho(D+delta T)≤b0T。D=0使用零出口模式。empty模式把全部私有任务留home，W_h≤T保证合法，资源恒零。

真实T调度在每home至多一宏。其实际private留量<T/2≤tau T，所以从原出口集合删冗余并把被删任务搬回自己的home，仍保private留量≤tau T；各sink负载逐坐标不增。这只是证明共同见证存在，算法不获取真实最优调度。

价格查询按每件任务实际合法sink的pi_z p_zj最小值构造覆盖成本，FPTAS保持真实a覆盖而仅缩放成本。零成本预处理、正最大成本猜测和不可复用回溯均支持(1+epsilon)乘性界；删冗余不增成本并保列预算。全部宏边使用同一home成本，因此最小成本宏匹配真实地共同选择occupation，不冻结某个历史宏身份。原共同见证的价格总成本≤T，故oracle在OPT≤T时不会因无匹配或成本>(1+epsilon)T而FAIL。

## 5. MW常数、全部实际任务和位复杂度

epsilon=gamma=eta/4，R=max(1,|H|b0)，g_z=ell_z/(RT)∈[0,1]。总权重的log增长与单行权重的log增长给出正文平均式。N≥16RK/eta²并使用logK≤K，得到

`R logK/(gamma N) <= eta/4`，

故`(1+epsilon+R logK/(gamma N))/(1-gamma) <= (1+eta/2)/(1-eta/4) <= 1+eta`，最后一式的交叉相乘余量正是eta(1−eta)/4≥0。eta=1的端点也成立。算法无需计算log或近似实数。

平均N份实际方案的模式指标和宏流量，给出了正确平行扩张的显式分数基。每列≤b0T，+b舍入后每sink≤(1+eta+b0)T。每selected home执行其唯一所选实际私有模式，再重新匹配一个时间≤T的真实宏任务，故home≤(1+tau)T；未选home全部私有任务回home，负载≤T。私有组互不交且与宏任务集不交，每件原任务恰执行一次，端点均合法；不靠保持给定边际或槽计数。

R≤max(1,|H|)保证N不按rho数值增长。实际负载是原处理时间的子集和；权重乘子仅含这种子集和与原参数，N次乘积的位长相加，价格、FPTAS和下一步LP数据位长均多项式。运行规格为poly(L,1/eta)；eta作为固定常数时是总位多项式，eta作为二进制可变输入时没有被误称为关于其编码长度的多项式。

K=0采用禁止正D occupied home再匹配的正确分支；无宏任务直接全部回home。T=0在任何除法前完整检查零边，全部任务存在零边时返回零调度。空任务、空组、零a、零sink时间、单端、无出口和极大分母没有被归一化步骤遗漏。

## 6. 第三身份：未知OPT的one-sided搜索

`UM-ARBITRARY-SINK-PRIVATE-GROUP-PROMISE-APPROX-v1`只在真实OPT处要求结构promise；它没有声称能验证该promise或从一般P提取分组。

阈值程序明确取消“宏边>当前T/2”检查，只保宏时间≤T剪枝和W_h、a_j前置检查。对所有T≥OPT，原最优调度因promise仍是每home至多一宏，private留量<OPT/2≤tau T，故共同见证仍成立，不要求较大T上重获宏下界。任何成功的实际负载界则只使用宏时间≤T。因此每次FAIL都发生在T<OPT。

分母乘积D位长至多输入分母位长之和，实际makespan及OPT在1/D网格。任选合法调度的C给整数U=DC≥DOPT，U/D必成功。非单调接受集合也无碍：lo<DOPT且hi保存成功，FAIL只把lo推进到仍小于DOPT的整数；结束hi=lo+1≤DOPT，输出≤alpha OPT。零最优值先精确返回，delta=0不做除法。

平衡参数tau=[rho(1+delta)+eta]/(1+rho)满足b0=tau−eta、alpha=1+tau=1+eta+b0；rho delta+eta<1给tau<1、alpha<2，rho≥1给tau≥1/2。此统一余量只在固定rho、delta、eta的声明结构域成立，不是UM-TARGET-v1的一般算法。

## 7. 文献与价值边界

正文已明确扣除cover FPTAS、匹配、MW和upper-only degree-bounded matroid计数的新颖性；其有理加权+b结论在正文自足证明，不依赖把未读外部定理当oracle。旧工具的结构性组合可以作为当前价值，但全球新颖性与独立论文价值没有被认证。

本次没有独立取得并完整重读所列三份外文来源，故不以此报告认证其作者元数据、印刷页或定理编号；root的primary-source定位记录应与本数学读后审分开保留。该限制不构成当前自足证明的standing数学异议。

主目标仍缺任意P生成共同角色、唯一home分组、接收边及统一rho/delta余量的算法。显式菜单舍入与本结构输入的菜单生成均不能替代这一全输入桥。

## 8. 两份迁移代码的实际核对与重新运行

实际核对文件及当前SHA：

- `tests/audits/unrelated_machines/upper_column_budget_base_audit.py`：`498ab45976ed27d264f5c20527ab88af70d80d44a7e1e809a5c30f0a2c7a6269`。
- `tests/audits/unrelated_machines/occupation_vertex_audit_core.py`：`8c5464edfd9990c98ee7bc4901544f108e31ae1c89fe5411119f6899bf93beba`。

源diff与AST检查确认核心的8个函数、审计的5个非main数学函数均与本独立稿相同。main差别仅为import/依赖文件名、Python与范围元数据、移除默认改写结果文件；没有数学核心或scope漂移。顶点核心无独立运行入口，通过upper审计实际执行。

本次重新运行命令：`python -B tests/audits/unrelated_machines/upper_column_budget_base_audit.py`，stdout保存到`/workspace/scratch/014c8decb8a6/independent_selection/final_canonical_upper_budget_rerun.json`。

实际结果：187例（180随机）、283次面检查、1062个扩展顶点候选、380个整数选择、96条删行，全部断言通过；27例原预算没有整数选择。包含home容量遗漏的负控制及10^95量级分母。另核一个Q_h为空但H_Q仍覆盖B的合法实例，成功恢复正确模式和宏匹配。

补充精确有限核验输出`/workspace/scratch/014c8decb8a6/independent_selection/final_source_and_parameter_checks.json`：64组MW参数、32组平衡系数和2546个任意非单调one-sided接受谓词全部通过。这些仅作有限algebra/搜索审计，不是一般证明替代，也没有执行极小eta下的全部MW迭代。

本次未审读或运行另一个独立MW审计程序`arbitrary_sink_price_cover_mw_audit.py`；该程序及原矩阵完整MW回放应依它自己的审查与运行记录判断。没有集成生产级有理LP后端，指数顶点枚举仍只是有限审计。

## 9. 最终standing状态

F1空模式秩漏洞已关闭。投影顶点、本轮lex释放、home容量、宏身份不冻结、MW常数、one-sided未知OPT、零值和位长方面没有新的standing objection。

可以按三个精确限域身份登记为有自足数学证明并经内部完整读后攻击的资产；软件实现、有限验证、外审和新颖性状态仍须分别记录。UM-TARGET-v1保持OPEN。
