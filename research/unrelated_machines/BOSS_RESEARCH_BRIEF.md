> 保留的调度存档入口：当前全仓主攻为Q-CAG-HALF（customer-attraction），见[当前入口](../customer_attraction/README.md)。下文仅用于显式选择unrelated-machines的旧题对话，不是新会话默认任务。

# Boss 研究总览：一般不相关并行机的路线分诊

【当前方向：反面主攻】用户已决定主攻UM-TARGET-v1的否定，争取对每个固定ε>0建立真实近二困难性。下面的UM-TARGET-v1仍是固定待否定命题，不改其量词或OPEN状态。明确区分复杂度假设下的不可近似性与无条件否定；只排一个固定比率、配置gap或局部舍入不够。当前承重是任意低负载完整调度的可靠源解码、全ε量词和固定参数总位复杂度。

**快照日期：2026-10-18；下文计数是原阶段快照，不是实时计数。** 本页属于研究存档 `unrelated-machines`，是进入研究的短入口，不替代精确 Claim、正文、审查或冻结证据。它的作用是让新 boss 在几分钟内选对承重义务，而不是通读全部资产。短期实际调度见[当前活跃路线](ACTIVE_ROUTES.md)，填写格式见[Route Card 模板](ROUTE_CARD_TEMPLATE.md)。

## 先看结论

**当前用户决定：全体直接主攻 `UM-TARGET-v1` 的否定。** 以下原命题保持其数学身份，作为待否定对象。研究全 ε 的真实近二 gap 与绝对阈值解码，逐条声明复杂度假设；既有正面资产作为工具保留。下文旧路线分诊和规模快照不构成新的配额或审批。一般反面仍 OPEN。

唯一主目标是 `UM-TARGET-v1`：对一般 `R∥C_max`，机器数和任务数都可增长，寻找统一常数 `ε>0` 和确定性总位长多项式算法，对每个合法输入输出完整分配并满足

\[
C_{\max}(A(P))\le (2-\varepsilon)\operatorname{OPT}(P).
\]

**当前状态仍是 `OPEN`。** 仓库没有一般输入的统一 `(2−ε)` 算法，也没有在 `P\ne NP` 等明确假设下排除所有这类算法的完整困难性证明。已有结果主要改变了我们对方法边界和可恢复结构的认识。

不要把下面任何一种结果当成主目标完成：固定机器数的 PTAS、`2−1/m`、配置 LP 间隙、特殊可用性图、给定分组/给定矩证书、有限枚举、实验最优或某个舍入反例。

## 当前方向：优先否定全部统一改善量

**当前研究方向：反面主攻。** 用户已决定优先争取在明确标准复杂度假设下否定 `UM-TARGET-v1`：排除每一个固定 ε>0 的确定性位多项式实际调度算法，包括任意极小常数。原命题身份和 OPEN 状态保持；这是研究方向，不是已证不存在。反面以每个固定参数的真实整数 OPT gap、全部低负载调度的源解码及总位复杂度为承重；正面资产用于攻击归约和寻找逃逸，不预设结论。

反面按每个固定 k 的真实近二 gap 分流；一般 PCSP 源与物理 copy/decoder 分开。已有正面结构结果作为归约攻击材料，不能为了符合方向而删去实际逃逸。详见 [ACTIVE_ROUTES](ACTIVE_ROUTES.md)。

## 当前资产规模与可信状态

这是结构检查得到的仓库快照，不是数学真值计数：

| 资产 | 数量 | 应如何理解 |
| --- | ---: | --- |
| 当前不相关机正文 | 102 | 其中许多是严格受限接口或方法边界 |
| 精确账本中的专题条目 | 212 个小节 | 不能按小节数等同于 212 个一般结果 |
| 独立审查文件 | 116 | 主要是内部 statement-first/read-after 或 exact attack |
| 精确审计程序 | 201 | 证明有限构造、枚举或反例，不替代一般证明 |
| 冻结运行记录 | 155 | 可复现证据，范围由各记录确定 |
| 原始文献/来源文件 | 36 | 以 manifest 的取得状态和定位为准 |
| 全仓命题状态记录 | 505 条 | 覆盖多个旧/新模型；外部评审字段当前均未记录 |
| 关系图 | 932 节点、1069 条超边 | `checks/attacks/limits` 不得读成 `derives` |

结构检查当前通过：入口 30 个、显式本地链接 867 个；`check_assets.py` 还验证了 1435 个命名资产和 272 个本题范围条目。**这些数字说明保存和追踪能力很强，也说明随机阅读已经不经济。**

状态轴必须分开：

- **Truth：** 很多受限命题已有完整正文和精确内部核验。
- **Value：** 已经得到大量可复用的障碍、边界和受限联合构造。
- **Novelty：** 绝大多数尚未完成外部新颖性核验，不能把内部审查写成已发表贡献。
- **Mechanism：** 主瓶颈已从“再找一个局部舍入”收窄到“任意输入的共同容量桥”。
- **Ambition：** 主目标仍未推进到一般算法或一般困难性结论。

## 唯一主轴：四个必须同时闭合的义务

对任意输入 `P` 和候选阈值 `T`，下一条真正推进主目标的路线至少要闭合下列四项；少一项就只能登记为局部资产：

1. **共同容量状态：** 从输入本身产生可验证的 big/medium/tiny 或等价联合状态，不能把最优分配、支撑、矩、home/sink 分组当作 oracle。
2. **全机实际输出：** 同时给出所有机器上的完整整数任务分配，并逐机证明负载界；分数存在性不够。
3. **可靠失败语义：** 若路线输出 `FAIL`，必须有独立可检验的证书推出 `OPT(P)>T`，不能把 LP 不可行或有限搜索没找到当作失败证明。
4. **统一余量与位复杂度：** `ε` 不随 `m,n,K,q,r` 退化，阈值搜索、分母增长、循环次数和输出长度都按输入总位长多项式控制。

标准分解仍是最清楚的测试台：固定 `β<1`，若能从任意输入找到 big 分配 `μ` 和 tiny 分数补全 `x`，有序槽舍入给出 `(1+β)T`。真正的难点是联合找 `μ,x` 以及把相对 `T` 的保证转换成可靠的相对 `OPT` 保证。

## 路线分诊表

| 优先级 | 路线类别 | canonical 入口 | 已得到的认识 | 现在应做什么 |
| --- | --- | --- | --- | --- |
| P0 | 任意输入共同容量桥 | `questions/unrelated_machines/barrier_escape_obligations.md`；`current/unrelated_machines/joint_matching_completion_and_block_cuts.md` | 逐机探针、固定 big 匹配和局部补全会被共享容量/选择耦合击穿 | 只接受能直接产出共同状态、实际输出或 sound `FAIL` 的新机制 |
| P1 | 受限正面接口 | `current/unrelated_machines/weighted_group_joint_slot_rounding.md`、`heterogeneous_macro_uniform_residual_st_rounding.md`、`shared_sink_joint_macro_assignment.md` | 唯一 home、共同资格、固定分组或宏承诺下可达 `3/2+δ` 甚至更好 | 攻“任意输入如何提取这些结构”；不要把 promise 算法包装成一般算法 |
| P1 | 共同迁移/repair | `current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md`、`strict_sub2_batch_barrier.md` | 逐坐标、单目的地和固定小批量 repair 在近二族遇到锐障碍 | 若没有多目的地共同容量和统一势，停止同类局部微调 |
| P1 | 证书、矩与需求树 | `current/unrelated_machines/succinct_prefix_atomic_decoding_bridge.md`、`global_assignment_moment_rounding.md`、`rooted_dag_degree_token_bridge.md` | 给定证书可以解码真实调度；从任意 `P` 生成证书仍开放，固定阶贪心有线性损失 | 只攻“证书生成/可靠失败”这一具体缺口，不再重复固定阶 probe |
| P1 | 反向困难性 | `current/unrelated_machines/general_weighted_private_clause_exchange_and_shared_outside_boundary.md`、`private_graft_and_resource_repetition.md`、`k_uniform_bundle_matching_floor.md`、`santa_conditional_reverse_barrier_v2.md` | 私有异权子句辅助网络若保单query/单return及全索引局部strict可选，整条真实变量环仍实际≤3/2；共享外端多query接口尚缺源一致性。私有复制、资源池和Santa桥另有地板 | 攻退出该精确模板的真实共同容量及源NO全局decoder；只有真实整数近二OPT gap、YES/NO解码和位多项式soundness全闭合才升级 |
| P2 | 经典共同前提 | `current/unrelated_machines/model_and_classical_barriers.md`、`reviews/unrelated_machines/classical_foundation_review.md` | LST/ST 给 2；配置 LP 的一般 gap 可达 2；低于 3/2 的一般算法受 NP-hardness 阻挡 | 读一次后作为前提引用，避免重新证明或把 gap 当一般 hardness |
| P2 | 新菜单/Cartesian/局部结构边界 | `current/unrelated_machines/cartesian_menu_*`、`degree_*_menu_*` | 许多精确边界和受限 `≤3/2` 构造已闭合，但尚无一般 decoder | 只有能改变跨机器一致性或源解码的结果才继续；否则做 honest salvage |

## 新 boss 的最短读取路径

1. 读本页，再读[数学地图](../current/unrelated_machines/README.md)开头的模型和 `UM-TARGET-v1`。
2. 只选上表一行，写一个承重义务 `O`：共同容量、实际整数输出、sound `FAIL`、统一余量或位复杂度。
3. 读该行的一个 canonical 正文、对应审查和一个审计程序；不要先通读 1391 个资产。
4. 开始研究前写清：相比 LST/ST/configuration-LP 新增了什么信息；最小边界输入是什么；若失败会回收什么。
5. Builder 和 blind red-team 分离。red-team 先只读 Claim 与 `O`，攻击零值、不可用边、单端任务、`m,n` 增长、极大分母、`FAIL` 语义和输出合法性。
6. 连续两轮只增加样本、换参数或重复同一局部 probe/slot/repair，且没有减少 `O`，就停止该微调并记录失败范围。

## 当前运行协议

所有 boss 可以直接探索，路线表和 Route Card 只提供可选导航，不是审批、名额或排他认领。P0-F 和 R0-R 是当前最值得优先尝试的路线，但可以自由改用全局交换、局部修复、矩、需求树或新的非 LP 表示。blind red-team 只在成熟候选、路线合并或 Claim 晋级时后置使用；探索中的想法不因尚未审查而停下。详细可选模板在[ACTIVE_ROUTES](ACTIVE_ROUTES.md)和[Route Card 模板](ROUTE_CARD_TEMPLATE.md)。

## 维护规则

- 新工作先查本页和 `CLAIMS.md`；同一数学内容修订原资产，不按 boss/日期复制。
- 新命题只在改变对象、量词、假设、结论或范围时建立新版本。
- `current/` 放自足正文，`questions/` 放未闭合候选，`reviews/` 放独立审查，`tests/audits/` 和 `evidence/runs/` 放可复现核验。
- 内部审查通过不等于外部评审或新颖性成立；有限计算不等于一般证明。
- 每次有真实数学增量才更新本页的路线表；普通聊天和重复日志不入库。

## 权威入口

- [精确 Claim 账本](CLAIMS.md)
- [当前研究前沿](RESEARCH_STATE.md)
- [失败路线与回收](FAILED_ROUTES.md)
- [数学地图](../current/unrelated_machines/README.md)
- [启动提示词](BOSS_START.md)
- [操作手册](RUNBOOK.md)
