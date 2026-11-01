# 全续局门槛矩阵：精确量词与本轮检查点

2026-10-24。研究对象始终是任意人数、任意有限共同目录及每份完整有序历史纯 SPE。一般 Q-CAG-HALF、原门槛预算 TB、同序矩阵 SM、路径完整菜单桥均 **OPEN**。本目录没有得到新的跨枝支付不等式；阴性有限筛查到此停止。以下是可复核的量词澄清和未闭合义务，不能作为一般正面证据。

候选来源为 `../../../../R-f399f831353446a49502f49d8abd2cb7/threshold_budget/README.md`（从本目录回到 customer-attraction 工作区后读取该 actor）；规范模型及当前一般断点分别见 `research/current/customer_attraction/model.md`、`general_half_proof.md` §§6、8。

## 1. 候选的确切量词

固定完整 SPE `sigma` 的实际终局 `z=(S_1,...,S_m)` 和实际前缀 `h_i=(S_1,...,S_(i-1))`。令 `R(h_i,A)` 为该有序孩子以后全部完整纯 SPE 续局的可实现终局全集，不要求采用 sigma 原先指定的续局。记

```
L_i(A) = min_{y in R(h_i,A)} u_i(y),
Theta_i = max_A L_i(A).
```

原候选为：对每个合法有序比较 m 元组 `T=(T_1,...,T_m)`、`O=|union T_i|`，

```
SM:  sum_i L_i(T_i) >= O - W(z).
TB:  O <= W(z) + sum_i Theta_i.
```

SM 蕴含 TB；实际纯 SPE 最优性给 `u_i(z)>=Theta_i`，故两者都足以推出一般 half。原文将 SM 写成任意有序比较元组；“对每个最优比较支持至少存在一种排列成立”是严格更弱、同样充分的新候选，不能混写成已经证明的原 SM。

L_i 不是原固定 sigma 的一条偏离收益，也不是安全值 `v_r`、静态最坏背景或固定平局选择器。某个 `L_i(T_i)` 的极小续局来自另一份完整子 SPE，仍须保留全部后继历史的真实激励。

## 2. 同时实现全部真正离轨极小值

这是已有独立孩子拼合接口在实际路径上的直接应用，不宣称新的福利支付。

**路径离轨极小化。** 固定上面的 sigma 和 z。对每个 i 及每个 `A != S_i`，可以同时把有序孩子 `(h_i,A)` 后的完整续局替换为实现 `L_i(A)` 的子 SPE，得到另一份完整 SPE `sigma^-`，其实际终局仍为 z，且所有这些真正离轨偏离的收益同时恰为 `L_i(A)`。

**证明。** 这些有序孩子的子树两两不交：较早位置的孩子已经偏离了实际动作，而较晚孩子仍含该实际动作。每棵替换子树本身是完整子 SPE。实际节点 i 的规定行动及其实际终局均不改变；每个被替换的偏离收益只从原来的真实续局收益降低到 L_i(A)，所以该节点全部 IC 保留。其他节点不改变，或位于已替换且已是子 SPE 的子树中。于是全部有序历史 IC 同时成立。有限目录和树保证极小值达到。证毕。

这说明：**对于真正离轨列，分别取全部子 SPE 的最低值不会制造新的相容性障碍。** 难点仍是如何由这些完全可同时实现的真实树 IC 支付比较覆盖；不能把“能拼合”称为已完成预算。

## 3. 去掉没有必要的在轨极小化

定义在轨保留值

```
barL_i(T) = L_i(T),  T != S_i;
barL_i(S_i) = u_i(z).
SM*: sum_i barL_i(T_i) >= O-W(z).
```

SM* 仍充分 half，因为每项 `barL_i(T_i)<=u_i(z)`。对同一实例全体完整 SPE 的量化下，SM* 等价于以下选定真实续局预算：

```
SD: for every complete pure SPE sigma and every comparison tuple T,
    sum_i d_i^sigma(T_i) >= O-W(z),
```

其中 `d_i^sigma(T)` 是实际前缀处强制 T 后、所有后继继续按该同一份 sigma 的当前收益。

- SM* => SD：每个真正离轨收益至少 L_i(T)，在轨收益等于 u_i。
- SD => SM*：先用 §2 得到同实际 z 的 sigma^-，再对 sigma^- 使用 SD，便恰得到 SM*。

SD 正是既有 `../../../round3/credible/general_root_regret_working.md` §7 自由 matching 候选的逐元组加强方向：旧候选只要求存在比较索引排列通过，SD 要求每个给定有序元组通过。它属于已有候选族，不计作本轮新增预算。该等价只澄清缺口，不构造 SD 的非负历史乘子，也未证明 SD。原 SM 还要求支付被保留在轨列的续局租金

```
rho_i = u_i(z)-L_i(S_i) >= 0;
SM = SM* with the extra subtraction sum_{i:T_i=S_i} rho_i.
```

不能通过 §2 免费消去这份租金，因为在轨孩子包含后来实际历史，替换它一般改变 z。这里“额外强化”是固定实例/实际路径上的量词比较；没有断言两个全实例候选在加入重复标签等模型变换后仍严格分离。

### 在轨极小化确实能改变实际终局

两位玩家、三个共同主题：A 有五名客户；B 含其中两名及另外两名私有客户；C 有三名与 A、B 不交的客户。A、B、C 单独大小为 5、4、3，且 A∩B 大小 2。

在 A 后，末位选 B 或 C 都得 3；在 B 后，末位唯一选 A 得 4；在 C 后，末位唯一选 A 得 5。指定 A 后选 C，根选 A 得 5，而偏离 B、C 各得 3，故构成完整纯 SPE，实际 z=(A,C)、W=8。但 `L_1(A)=4`，由 A 后改选 B 实现。故 `rho_1=1`。该极小续局无法同时保留原实际 z。这个例子不否定 SM、SM*、TB 或 half，只说明额外在轨极小化的范围。

## 4. 本轮有限筛查：只是反例尝试

`probe_existing.py` 与 `existing_results.json` 对下表 **19 个已存在的具体输入**做了精确 Fraction 检查，没有扩展新固定人数正面专题。实际一般候选固定为原 SM；另外记录仅限最优比较覆盖的版本。

每个输入：先用规范 `ExactSPESolver` 得到全部根可实现终局 q；对每个 q，动态规划状态为 `(实际前缀计数 k, 比较主题支持 mask)`。沿每个可实现有序实际路径推进，同时在每个位置允许比较主题任取目录行动。代价是相应 `L_i(T_i)`。最后减比较联合覆盖、加该 q 的实际福利。故检查该输入的全部有序 SPE 实际路径以及全部有序比较 m 元组；列举比较元组的数量为 `p^m`，未将其限制为某一排列或只含互异主题。

计数缓存只压缩全部可实现结果集及值，不承诺同计数历史采取同一续局。动态规划使用 `q in R(k+e_a)` 与 `u_a(q)>=Theta(k)` 判定当前动作可实现；每个有序孩子仍可独立拼合。实现导入规范求解器，不是对该求解器的独立审计。

表中为 `W+sum L-O` 的最小值，右栏只保留比较覆盖等于 OPT 的元组。

| 既有输入 | p | m | 全比较最小余量 | 最优比较最小余量 |
| --- | ---: | ---: | ---: | ---: |
| aggregate_theta_failure.json | 6 | 3 | 79/3 | 79/3 |
| collision_free_occupancy.json | 4 | 2 | 5/2 | 5/2 |
| coverage_opportunity_failure.json | 5 | 3 | 11/3 | 11/3 |
| dynamic_iid_local.json | 7 | 5 | 127/3 | 127/3 |
| eight_cce_welfare_gap.json | 4 | 3 | 4 | 4 |
| empirical_iid_kernel.json | 4 | 3 | 11/3 | 11/3 |
| fractional_actual_load_failure.json | 4 | 4 | 55/6 | 55/6 |
| global_decorrelation_failure.json | 6 | 4 | 367/6 | 379/6 |
| individual_security_failure.json | 6 | 3 | 26 | 26 |
| local_security_increment.json | 6 | 3 | 83 | 83 |
| optimal_last_query_failure.json | 7 | 4 | 1271 | 1271 |
| portfolio_matching_failure.json | 5 | 2 | 59/2 | 30 |
| prefix_balance_failure.json | 6 | 4 | 59/12 | 59/12 |
| residual_counterexample.json | 5 | 2 | 11/2 | 11/2 |
| root_stationary_kernel.json | 6 | 3 | 21/2 | 21/2 |
| root_tax_failure.json | 6 | 4 | 23/2 | 23/2 |
| tax_bridge_failure.json | 4 | 3 | 3 | 3 |
| worst_cce_welfare_failure.json | 5 | 3 | 6 | 6 |
| worst_pne_welfare_failure.json | 4 | 3 | 35/3 | 35/3 |

以上阴性结果不支持任意 p,m 的真值，不是 half 的证明。未做独立盲审。禁止把19个实例通过改写为“全范围证据”。

## 5. 真正剩余的义务

目前没有从完整真实 SPE 激励导出 SM、SM*、TB 或 Mpath 的一般单步不等式。把

```
F(h;remaining comparisons)
 = min_{actual SPE continuation} [W(final)+sum_future L_i(T_i)]
```

写成递推，只是精确重述：实现 F 极小的实际孩子与实现当前 `L_i(T_i)` 极小的离轨孩子可以不同；未来动作又必须由相应真实子 SPE 支撑。未构造一个共同的逐客户信用池或非循环势函数，可以把这些不同孩子的选择差支付给实际 W。当前应继续寻找这种真实支付，而不是增加阴性扫描、静态运输或重复 DP 恒等式。
