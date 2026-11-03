# Boss3 动态门槛与单位净变分方向审查

2026-10-24。仓库根为 `仓库根`，下列源码路径均相对此根。仓库只读；本轮只重放既有冻结范围并对一个既有族做确定性候选判别，没有随机扩样、发消息到研究公屏或提交。

## 结论

1. **THRESHOLD/TB 与 SM 仍是未证一般候选。** 本次检查的既有静态匹配反例、真实偏离匹配反例和集合值 BI 逻辑，都没有否定其所写的 `O−W` 预算。`u_i≥Theta_i` 与 `ΣTheta_i≤W` 正确，但不支付 TB 的缺口。
2. **UV 的条件蕴含成立；其原本标为 OPEN 的“每个完整 SPE 存在满足 UV 的最优元组排列”问题已有否定答案。** 既有 all-big 下界族在每个 `m≥4` 都使**所有**最优排列失败。这不否定 THRESHOLD、SM 或 Q-CAG-HALF。原稿没有把 UV 普遍存在当作已证，审查不应指控其虚报定理。
3. 有限运行有明确辅助候选对象，属于可接受的压力测试；其阴性结果没有新增全输入成立的支付关系。当前更有价值的动作是保留 THRESHOLD 的一般数学义务，并据下述精确分离处理 UV，停止增加阴性样本数。

## 读取依据与模型量词

- `AGENTS.md:3,9–15`：只研究一般共同目录、任意人数、每个完整历史纯 SPE；有限实例仅服务明确一般候选的判别，阴性计算不证明一般结论。
- `research/current/customer_attraction/model.md:8–32,34–55`：单位客户、单位提供者、共同目录、全部有序离轨历史；整数重数只压缩不同单位客户。
- `research/questions/customer_attraction_half_coverage.md:9–23`：主目标全量词及既有 all-big 文献下界族。以下反例复用第23行记录的族，不是新发现的游戏构造，也未独立核查论文优先权。
- 新稿主定义：`research/workspaces/customer-attraction/R-f399f831353446a49502f49d8abd2cb7/threshold_budget/README.md:7–41`；相同候选的根稿 `root_route/threshold_budget.md:7–30`。
- 新稿条件桥：同 actor 的 `probabilistic_route/variation_bridge.md:9–43,48–81,108–116`。
- 本次同时读了根 README、研究总入口、本题入口和数学地图；它们均保持一般 Q-CAG-HALF 为 OPEN。

令实际终局为 `z`，实际前缀为 `h_i`，`L_i(A)=min_{q∈R(h_i,A)}u_i(q)`，`Theta_i=max_A L_i(A)`。对每个 A，原完整策略的真实离轨终局 `z^sigma_{i,A}` 属于该孩子子博弈的全部 SPE 终局集，故

`u_i(z) ≥ u_i(z^sigma_{i,A}) ≥ L_i(A)`。

再对 A 取最大就得到 `u_i(z)≥Theta_i`。这也澄清了根稿第14行略写的推理：需要逐动作的原策略 IC，而不仅是“实际动作收益不低于自身动作的最小值”。

集合值 BI 的必要性/充分性已写在 `research/current/customer_attraction/exact_solver.md:26–28,32–64`，规范实现见 `customer_attraction/exact.py:51–83`。同计数历史的**可实现终局集合**相同，仍可在不同有序历史选择不同续局。因此用计数缓存准确计算 L 没有把策略限制成匿名策略。BI 不自动给 TB，也不因不同分支的极小续局互斥而使定义无效；孩子子树本来就可独立拼接。

## 旧匹配反例没有击中这两个新式子

必须区分三个右侧：遗漏数 `|Oset\Cset|`、福利差 `O−W=|Oset\Cset|−|Cset\Oset|`、以及静态查询和的上界 W。它们的方向、支付对象不同。

| 既有资产 | 被否定的精确桥 | 本轮 Fraction 反算 |
|---|---|---|
| `research/current/customer_attraction/portfolio_matching_counterexample.md:9–20,63–90` | 存在最优组合/排列使同一 sigma 下真实偏离收益和至少支付**遗漏数** | `W=44, OPT=45`，遗漏数42、两种最优排列偏离和均41；但 SM 右侧仅 `OPT−W=1`。该例最坏子 SPE 的 L 在 B/D 两列仍给 `19+22=41`，故两种最优排列都满足 SM；`ΣTheta=44`，TB slack43。 |
| `research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/optimal_static_matching_counterexample.md:7–11,42–56` | 存在最优组合/匹配使**冻结其他实际行动**的静态查询和 Q≤W | `W=47, OPT=52`；静态最小 Q=48>47。对同一实际路径重新计算全部子 SPE 的 L，24个最优排列的 L 和在 `[277/6,187/4]`，SM 右侧5；`ΣTheta=47`，TB slack42。 |

因此这些资产不能被引为 SM/TB 的已有反例。这里仅判别这两份具体资产；没有宣称所有仓库失败例均已穷尽。

另外，固定 sigma 的策略锥只装载该 sigma 实际选择的续局，而 L 在全部子 SPE 上取最小。新 actor 的 `dual_lp_route/README.md:35–41` 对此有正确提醒，二主题 tie 例中 L 确实可在边界跳变。但这只阻止把 L 当作一个固定线性行直接塞入该锥，不能推出 THRESHOLD 为假，也不能推出不存在分片或其他证明。

## SM 必须先冻结量词

`threshold_budget/README.md:29–41` 开头写“任意 m 元组”，随后又说“目前只需要某个固定顺序”。应明确列出不同版本：

- **SM-all**：对每个合法有序 m 元组成立。
- **SM-opt-all**：对每个最优有序 m 元组成立。
- **SM-opt-exists**：对给定实例和给定 SPE，至少存在一个最优有序 m 元组成立。

三者都足以推出 TB，但不是同一命题。对一个最优排列的失败只能否定全称版本；要否定存在版本，必须使所有最优元组及其排列都失败。TB 自身只涉及 OPT 和 Theta，即使 SM-opt-exists 失败，也可能继续成立，因为 Theta 每行可由比较最优元组之外的动作取得。

## UV存在性已有精确否定

全参数证明、严格作用范围及同族SM/TB分离见[UV链障碍](uv_chain_obstruction.md)。它复用已知all-big族，不另认领新客户游戏。

## 审计文件与已有有限记录的实际范围

本轮自足脚本为 `uv_all_big_audit.py`，冻结输出为同目录 `uv_all_big_audit.json`。命令：

```bash
python uv_all_big_audit.py
```

脚本以七个独立单位客户的 Fraction 份额核验全部85个有序决策历史、340个含自行动比较（255个非自行动偏离），枚举全部256终局证明最优元组恰24个，并记录全部24条前缀链的每客户份额。随后独立调用规范 `ExactSPESolver` 的完整子 SPE 终局集计算每个 L，保存所有孩子终局及其当前收益；L 全1。脚本不使用作者的审计函数，确定性验证上述 m=4 判别；全 m 结论由前述解析证明给出，没有逐 m 扩样。

已有记录核对：

- `root_route/experiments/check_threshold_candidate.py:35–44` 对全部可实现有序路径逐前缀取规范 threshold，计算 TB slack，量词与代码一致。重放现有 `p=3,m=5` 二值全集，确为128实例、3288路径、全体最小 slack0、正实例最小 slack1。500随机输入的冻结 JSON 报2969路径；本轮未再随机扩样。
- `threshold_budget/README.md:47–48` 额外声称 SM 多范围通过；`threshold_budget/test_summary.py:1–8` 只是注释占位，实际根脚本只检查 TB，没有检查最优元组及 SM 的循环。因此这些 SM 历史运行在现有文件中缺少足够可重放脚本；不能把“注释称检查过”计为本轮独立核验通过。
- `counterexample_attack/owner_tax_exhaustive.py:48–77`：重放确得127非空二值支持、3984项和最大 gap `−1`。但第62–64行对每个**终局计数**只选一份默认 canonical 完整证书和一个有序路径，再枚举全部最优 tuple。它没有枚举每份完整策略，也没有枚举同计数的全部实际有序路径。`counterexample_attack/README.md:11` 的有限对象应据此精确描述；根稿 `root_route/threshold_budget.md:70` 不能被读成3984份任意完整 SPE 的穷尽。
- 随机脚本 `counterexample_attack/owner_tax_search_random.py:54–67` 只看最差福利计数、各取默认证书和一个实际路径、最多前20个最优元组。它是一个有边界的辅助候选攻击器；没有所有策略/所有最优元组保证，本轮未运行。
- `counterexample_attack/README.md:3–13` 与根稿 `root_route/threshold_budget.md:42–55` 检查的 `R_min≤|I|+2|G|` 只是税诊断。由 `|U|≤W+R_min`，即使该诊断一般成立，也不能推出 half；不能把这批阴性结果当 THRESHOLD 的证明进度。`recursive_state/mixed_owner_lp.md:65–83` 的 `Tax≤|G|+Q_C` 才是其另一个真正充分支付义务，尚未证明。

小勘误：`recursive_state/README.md:29` 的 `O=|C\actual|+|U|` 将遗漏集数了两次；应为 `O=|C∩actual|+|U|≤W+|U|`。最终带税不等式仍可按更正后的式子推出。根稿第70行“阴性记录否定加强桥”的表述也应改为“在该有限范围未找到该诊断的反例”。

## 下一项具体有价值的判别

立即把 UV 的一般存在问题由 OPEN 改为上述精确 FALSE，并保留条件引理；无需再为它寻找更多失败样本。单纯优化同一条最优链的非负 IC 权重已被这个族排除，接续需真正引入链外的合法全树关系，或者转到仍未被击中的 THRESHOLD。

对 THRESHOLD 保留一般推导任务；若接续 SM，先明确采用 **SM-opt-exists**，将反例判别写为

`max_{T∈S^m: W(T)=OPT_m} Σ_i L_i(T_i) < OPT_m−W(z)`。

这才否定全部最优组合/排列的存在式。若只失败某个排列，应仅报告相应全称版本失败。一个有价值的后续结果应是对全部输入建立一个支付这项最大匹配预算的真实全树不等式，或给出满足上式的完整 SPE；再做更多 p=3/p=4 阴性运行不会解决该数学义务。直接攻击 TB 则应检查严格 `OPT_m>W+ΣTheta_i`，仍须与 SM 的反例分开。
