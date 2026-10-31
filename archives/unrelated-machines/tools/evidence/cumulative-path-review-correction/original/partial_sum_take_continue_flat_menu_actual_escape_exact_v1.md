# partial-sum 路径的 take／continue：完整普通矩阵中的 AND 逃逸

候选边界 ID：`UM-PARTIAL-SUM-TAKE-CONTINUE-FLAT-MENU-ACTUAL-ESCAPE-v1`。

Scratch freeze，2026-10-18。对象是下面**明确定义的局部 take/continue 编译候选**，不是所有 DAG compiler 的不可能性定理，也不是已通过 selector-tree 正规形的反例。不主张本例在所有可能编码中机器数最小。

已实际读取真实 selector-tree 接口：`degree_three_weighted_menu_cube_embedding.md` §8–9，SHA256 `5e3f12dff54e770ff4afeae4201ef7f5c21536f0243858708fc24e3449439b41`。该接口的正值链只选择一个已经存在的原 normalized state；它本身不承诺把一条路径上多个 items 合成 AND。本例检查在 take 边上用一个 additive state 同时装“item 质量”和“继续信号”的自然扩展。

## 1. 原 Santa Claus 矩阵：两 items、三 agents

有 agents `a=1,2,3` 和不同 items `u_1,u_2`。每名 agent 对每件 item 的原 value 都是 `3/5`，因此每行总值为 `6/5>1`。

一名 agent 要达到 unit value，必须取得两件 items。按逐 item 累计、把累计值 cap 在 1 的记账，唯一 unit bundle 的 take path 是

\[
0\xrightarrow{\text{take }u_1,\ \text{credit }3/5}3/5
\xrightarrow{\text{take }u_2,\ \text{credit }2/5}1.
\]

第二步 credit `2/5` 不超过该 item 原 value `3/5`。这是有效的 partial-sum unit 路径，不涉及数值近似、舍入误差或 DAG merging。全源只有两件不可拆 items，三名 agents 的任何合法 allocation 必有一名拿不到 item，所以真实 `OPT_SC=0`。

## 2. 被攻击的精确 take/continue 规则

当路径一步给 item u 的 credit 为 `c in (0,1)` 时，用一个质量恰 1 的 normalized additive state 表示它：

- 原 item resource u 的 private weight 为 c；
- 下一个 node 的 own-resource 的 private weight 为 `1-c`。

下一节点有通常的 own singleton/off state；达到 partial sum 1 的末节点有一个使用 fresh accept-resource 的 singleton accept state。每节点是一个真实 group，有一件 unit selector；每 state 各有独立 private machine 和全部 incidence jobs；每资源只有一台 global unit resource machine。

这个规则在 full value 1 时要求同时领取 item 和 continuation，似乎实现 AND；但在 positive partial value 时可能只领取 continuation。本例给出其全部原 jobs 的实际逃逸矩阵和精确最优值。

这条规则是本页独立列出的候选，不从既有 selector-tree 定理推出来。若改用其它 AND、守卫、共享结构或完整 leaf state，须另立实际矩阵分析。

## 3. 完整目标 normalized-flat ordinary P

除两件共享原 item resources `u_1,u_2`，为每 a 加不同 fresh resources `x_a,y_a,z_a`，全部身份互异。目标有三个真实 groups：`r_a,m_a,l_a`。其完整 state 菜单为：

| Group | Indexed state | 资源及其 private weights |
|---|---|---|
| `r_a` | `take1` | `u_1:3/5`, `x_a:2/5` |
| `m_a` | `off` | `x_a:1` |
| `m_a` | `take2` | `u_2:2/5`, `y_a:3/5` |
| `l_a` | `off` | `y_a:1` |
| `l_a` | `accept` | `z_a:1` |

对 `a=1,2,3` 全部复制这些 **private groups/states**，但原 items 始终用相同的两个 global resource identities。每 state 内资源互异、权非负且总和恰为 1。

完整普通 UM 实例逐 job 定义：

1. 每个上表 indexed state 一台独立 private machine；每个列出的不同 resource 一台 resource machine；两种 namespace 不交。
2. 每个 group 恰一件 selector，时间 1，eligible machines 恰为它自己的全部 state private machines。
3. 每个 state-resource incidence 恰一件不同 job，时间为表内 private weight 或其 indexed resource machine 上的 1。
4. 所有其它时间为 infinity，没有额外资格、预载、拒绝、免费约束或删除的 jobs。所有 off/unselected states 的 jobs 都保留。

计数：9 groups/selectors；15 indexed states/private machines；11 resource machines；21 incidence jobs；总计 **26 machines、30 jobs**。每项时间只为 `1,3/5,2/5` 或 infinity。

## 4. 任意解码都无法恢复正 SC 效用的实际 witness

选择每个 `r_a` 的 `take1`、每个 `m_a` 的 `take2`、每个 `l_a` 的 `accept`。领取

\[
B_{r_a}=\{x_a\},\qquad B_{m_a}=\{y_a\},\qquad B_{l_a}=\{z_a\}.
\]

所有这些 resources 不交，各组导出 private 质量分别为 `2/5,3/5,1`。所以该 normalized-flat allocation 的最小质量为

\[
\delta=2/5.
\]

两个原 item resources 完全没有使用。它不是“路径选错”：所有 agents 都沿同一条、且确实累计到 unit 的 take1/take2/accept 路径激活；失败在于每步 additive partial 领取允许只付 continuation，不付原 item。

完整实际调度如下，不只列 partial 子集：

- 每 selector 放在上述所选 state 的 private machine；
- 每所选 state 对应 `x_a,y_a,z_a` 的 incidence job 导出；
- **所有**其它 incidence jobs 留在自己的 private machine，包括两个 off states 的全部 jobs及所选 states 的原 item jobs。

每个 `r_a` private load 为 `1+3/5=8/5`；每个 `m_a` 的 selected `take2` private load 为 `1+2/5=7/5`；每个 `l_a` selected private load 为 1；每个未选 off-state private load 为 1。被占辅助 resource load 为 1；两个原 item resources load 为 0。每一原目标 job 恰执行一次、端合法。因此

\[
\tag{1}C_{\max}(P)\le8/5.
\]

事实上这是精确最优：若 `C<8/5`，每个根 group 的 selector 强制在其唯一 `take1` private；该 private 中的 `u_1` incidence job 私时 `3/5` 不能留下。三个这样的 jobs 全部必须导出到同一个 `R_{u_1}`。而 `C<8/5<2` 只允许一个 unit job，矛盾。故

\[
\boxed{\operatorname{OPT}(P)=8/5,\qquad V(P)=2/5.}
\]

V 的独立上界也直接成立：`u_1` 最多供一个 root 领取，其余 roots 的所选 state 质量至多 `2/5`；上面的 allocation 达到。

因为原 SC 的任何 allocation 最小效用都是 0，所以即使允许 decoder 任意重新分配原 items，而不要求只输出目标已领取的原 items，也不可能使每名原 agent 得到 `c delta` 效用，对任何 `c>0` 都失败。这里不是计算效率问题。

## 5. 证明了什么，没证明什么

本例否定精确规则§2的以下合同：对其任意正 partial normalized-flat allocation，总能提取所有原 SC agents 的 Omega(delta) 效用。它甚至不用共享 DAG nodes、非线性 recoupling、舍入误差或 exponentially many paths；单路径的 AND 已逃逸。

在 full threshold 1 下，take1 和 take2 的两个正权项确实必须全部领取，因此这类候选可以保住某些 unit witness。但这不构成 positive-partial soundness：unit AND 与 arbitrarily-small-partial AND 是不同义务。一个 normalized additive state 的两个正质量部分，在 partial threshold 小于等于其中一个部分时，本来就能由一部分单独满足。

本页没有排除所有 possible partial-sum DAG compilers。完整配置 leaf、其它共享守卫、多条相互依赖的 activation obligations 或不同实际 processing times 都不在§2的精确规则中。它也不否定已经通过的 selector-tree 正规形：那个定理的 leaf 必须是已有的真正 normalized original state；把 leaf 换成 fresh accept singleton、把其 bundle 分散成路径上的 additive take states，是本例所攻击的**新增、尚未证明的**步骤。

因此实际 source bridge 仍需一个新的、可对任意 partial allocation 解码的 AND/activation 合同，不能只压缩 partial-sum reachability 或复用 root-to-leaf 的 OR 接口。原 source tiny-hardness 仍是另一个独立义务。

## 6. 位复杂度与证据状态

此矩阵常数规模、所有数为固定小有理数，足以给出有效完全显式的反例。正文定义已能直接逐 job 生成矩阵及(1)的 assignment；没有调用求解器或有限搜索来声称普适不可能性。无 repo/Git/Work 修改、无其它模型或软件实现认证。
