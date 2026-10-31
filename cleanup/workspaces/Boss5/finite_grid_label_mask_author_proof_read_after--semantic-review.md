# 有限格点 label-mask 对数势作者 Proof read-after：语义清洗草稿

- **来源 ID**：`dfc2aa730b7a1fc9a905`
- **冻结路径**：`history/source/notes/unrelated_machines/finite_grid_label_mask_log_potential_derandomization_v1_author_proof_read_after.md`
- **来源 SHA-256**：`8e863fc1772ac2d7c32ea0fab83e2373b7d69f79f93b1646c6513f5bf8c87a59`
- **来源大小**：6671 bytes
- **来源版本**：`68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 内容相同
- **清洗角色**：Boss5 / cleaner；本稿是独立草稿，尚未写入正式 `archives/` 对象
- **建议处置**：`integrated`（作者 Proof 的 read-after 审查）；与同题 Exact-only 独立审查、statement-only 和作者 Proof 保持四个稳定来源身份

## 实际阅读和来源关系

本源是对 `finite_grid_label_mask_log_potential_derandomization_author_proof_v1.md` 的作者 Proof read-after 审查，明确说明先行独立记录已被完整读取，因此它不是 blind 独立审查。清洗时完整读取本源，并回读同题两个直接关联来源：

1. statement-only Exact：`aee57c40a59da7343ff1`，SHA-256 `b6056384c47ed7b201a5666ac0750492fe717d7692aa23d6d775f225fb331165`；
2. Exact-only 独立重构：`c7285e5c3cc4ad1716ec`，SHA-256 `25448b56a0ed6022cfe340c5c1b647f3d7bdbdc7726fd2aa673e601e01ab3633`；
3. 作者 Proof：`c05060b2330f0a8d6978`，SHA-256 `8a20ac9d1d0a9381621ff7560e1c3f985db072dba4aafae8125c4c846d54fbad`。

本源报告与 Exact-only 重构一致，结论为 **PASS**：在给定有限格点、显式有理概率和权重、正偏置，以及明确的固定标签类内不交前提下，没有发现致命的数学、误差、位复杂度或全局物理不交错误。`PASS` 只表示这条工具接口的范围核对通过，不是对下游 NSW、常数、来源归约或一般 unrelated-machines 比率的认证。

## 模型域和合法退化分支

设显式 item 集为 (U)，item 数 (m)，agent 数 (a)，标签为 (0,1,ldots,L)（(L\ge1)）。每个 item (j) 的标签概率 (pi_{j,t}) 是非负有理数，和为 1，item 之间独立。agent (i) 有目标标签 (t_i\in[L])、集合 (S_i\subseteq U)、正有理 (V_i,\nu_i)，以及非负权 (w_{i,j})，其中每个权是 (1/Q) 的整数倍且行和不超过 1。令 (h_{i,j}=Qw_{i,j})，则 (h_{i,j}) 是非负整数、行和至多 (Q)，所有剩余质量索引都在 (0,ldots,Q)。

(V_i,\nu_i>0) 保证对数有定义；(pi=0,1)、零权、空 (S_i) 都合法。(m=0) 时返回空标签，势与期望相等；(a=0) 时每 item 取输入顺序中的第一个正概率标签，势恒为 0。非空普通分支不依赖 (
u)、(pi) 或权的数值倒数。

原势可写成

\[
\Phi(r)=\sum_i\ln V_i+\Psi(r),\qquad
\Psi(r)=\sum_i -\ln\left(\nu_i+\frac1Q\sum_jh_{i,j}{\bf1}[r_j=t_i]\right).
\]

第一项与 labels 无关，因此只需控制 (Psi)；不能把这一化简误读为假设 (V_i) 或期望本身有理。

## 作者 Proof 的关键核验

### 精确 conditional-expectation DP

固定一个已选 prefix，要求每一步只在原输入概率为正的 labels 中选择。prefix 事件因此有正概率，未决 items 仍保持原独立分布，无需除以小的 prefix 概率。对 agent (i)，已固定整数质量为 (b_i)，未决质量 (Z_i) 的生成多项式是

\[
\prod_{j\in J}\big((1-\pi_{j,t_i})+\pi_{j,t_i}z^{h_{i,j}}\big),
\]

次数不超过 (Q)。若 (pi=P/D)，用整数分子数组递推

\[
N'_k=(D-P)N_k+P N_{k-h},
\]

共同分母乘以 (D)。系数非负且总和等于分母，故分子位长由实际输入概率分母位长总和控制；(h=0)、(pi=0,1) 和零质量自然覆盖。不同 agent 之间不要求独立，因为势是各 agent 条件期望的线性和。

对下一 item 的每个正概率候选 label，先把其真实 (h_{i,j}) 贡献加入 (b_i)，再对剩余 item 做 DP，得到 child 条件期望。只在 DP 的实际正 support 上求和；`base + k` 永不超过 (Q)，不访问表外索引，也不把零概率项当成需要近似的对数。

### 近似误差和全局 ε 界

取

\[
\alpha=\frac{\varepsilon}{2am},
\]

为每个 (i,kin\{0,\ldots,Q\}) 预计算 (-\ln(\nu_i+k/Q)) 的有理近似，绝对误差不超过 (alpha)。每个 child 条件期望的总误差至多 (a\alpha)。由全期望，至少存在一个正概率 label 的真实 child 期望不大于 parent 期望；选最小有理估计的 label 后，真实 child 至多比该最小真实 child 多 (2a\alpha)。(m) 步累计为 (2am\alpha=\varepsilon)。

这里不需要任何正概率下界，不用近似值判断 (pi>0)，也不会因某个 (pi) 极小而引入 (1/\pi) 循环。ties 可按固定输入顺序处理；无需判定一般无理数对数的精确相等。恢复 (sum_i\ln V_i) 只是语义等式，不需计算无理期望。

### 对数近似和位复杂度

对任意正有理 (x)，写 (x=2^h y)，(1\le y<2)，再令 (z=(y-1)/(y+1)\in[0,1/3))。使用

\[
\ln y=2\sum_{n\ge0}\frac{z^{2n+1}}{2n+1},
\]

并用同一展开近似 (ln2)。截断尾界可取 (9^{-N})，选择 ((|h|+1)9^{-N}\le\alpha) 即得绝对误差 (alpha)。(h) 的大小由分子、分母 bit length 控制；幂、分母和有限有理求和的位长均为输入位长与 (N) 的多项式。对 (
u_i+k/Q>0) 的所有 (a(Q+1)) 个表项，这不展开 (1/\nu)、(1/\pi) 或 (1/\varepsilon) 个对象。

总计算量是显式输入位长、(a,m,L,Q)（按 **Q 的数值**收费）及 (log(1+1/\varepsilon)) 的固定多项式。因而任意二进制超大 (Q) 时只是 pseudo-polynomial 格点 DP；只有应用前提 (Q=4m) 且 (m\ge1) 时，才可把该工具写成总输入位多项式。此处没有软件实现、数值回归或下游应用的认证。

## 物理全局不交的真实前提

工具自身的势下降只给 label assignment，不自动给所有 agent 的物品不交。若对每个固定真实目标标签 (t\in[L])，所有 (t_i=t) 的 (S_i) 两两不交，则对同一个完整 assignment 定义

\[
T_i=\{j\in S_i:r_j=t_i\}.
\]

若 item (j\) 同时属于 (T_i,T_h)，同一个单一 label (r_j) 迫使 (t_i=t_h)，随后 (j\in S_i\cap S_h) 违反该 fixed-label 类内不交假设。因此 (T_i) 跨全部 agents 两两不交，包括零权 items、空集合和退化分支。没有该额外前提时，不能从 potential guarantee 推出 physical allocation disjointness；也不能为不同 agent 复制或独立重抽 item label。

## 与全仓对象的比较和边界

全仓已有的《显式 XOS 与福利舍入三源边界》已把 DLRV 随机 NSW 框架、Feng–Li 对数势先例和 Feige 福利舍入摘要分开归类。本源补的是有限 label-mask 工具的作者 Proof read-after，而不是新的 NSW 定理。应保持以下边界：

- 本源认证的是有限显式 item-label 概率、(1/Q) 格点权、正 offsets 的 conditional-expectation/DP 工具；
- 全局不交是另加 fixed-label 类内 (S_i) 两两不交的条件推论；
- 不可直接外推至 demand-oracle、任意 subadditive/weighted XOS、一般 unrelated-machines 近似比、NSW 常数、source hardness、六人纯 SPE 或 Q-CAG-HALF；
- 不能用“作者 Proof 与独立 Exact-only 一致”改写成“软件已实现并通过有限实验”，因为本源和关联三份材料均没有实现认证；
- 不能把 Q 按 (log Q) 收费，也不能省略 (Q=4m) 的下游真实输入核验。

建议 mapper 将本源登记为 `author-proof-read-after` 资料/审查对象，关系指向：

1. Exact-only 独立重构（方法一致性审查）；
2. 作者 Proof（来源审查与边界）；
3. 全仓 XOS/NSW 资料（方法接口，非主线均衡结论）；
4. 任何下游 NSW 或调度对象（仅在实际核对 Q、概率、权和不交前提后建立实现/迁移关系）。

## 未完成义务

尚未由本稿证明下游 source reduction、NSW 常数或一般机器模型的近二界；尚未运行实现或有限数值实验；也没有将作者 Proof 的 `PASS` 当成外部新颖性、发表优先权或全仓数学主命题。正式入库前应由 Boss5 串行 checkpoint 该草稿/正式对象，再提交本源的完整语义回执。
