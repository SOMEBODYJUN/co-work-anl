# 固定主玩家后的轻玩家阈值序势：独立重构与冻结攻击

## 精确审查对象和范围

审查 `WC-FIXED-HUB-LIGHT-THRESHOLD-RESPONSE-v1`：冻结任意全部 hub 动作；每条 side 仅一名 light、任意 hub 子集；每名 light 有唯一 source；hub/light 任意正实权；资源为同费二元副本和非负系数多项式，次数允许为零。不假设 UF。结论是冻结 hub 的 light 子游戏有符号精确保留的序势、全部严格 light 改善路径有限、势局部最小点恰为精确 light PNE，以及从全 aligned 状态有每名 light 至多一次严格移动的有序删除构造。

这不是整个原游戏的 exact/approximate PNE 结论，也不是跨不同 hub 向量的共同势。真实 hub 偏离保持 light 冻结；重新求 light 子游戏均衡是另一个动作合同。

作者临时候选：`fixed_hub_light_threshold.md`（冻结候选，现行稿为 `research/current/weighted_congestion/fixed_hub_light_threshold_response.md`）。本次先读精确陈述、MODEL 和规范 side 拓扑，自行重构下面的成本比较与势，之后才读作者候选。最初冻结无有序删除版本 SHA256 为 `4262bc8f2c8ce62d9404f4a9a8dde9c15e8ceff004fe4b62da4c11a5eccf9e67`；后置有序删除和 multi-light 边界所审版本 SHA256 为 `ac6a354e1d728a51ace67601908e168003fe459f893bd49fb270d370c7042898`。后续若修改正文，须以新 hash 记录差异复核。

最终冻结 SHA256 为 `4a071681b6ddbe0babafd6ea3ad03842f6a8da8dba262b4d1de93e2be1c3be60`。后置差异复核核对了命题状态、Dependencies、Evidence 及新增的文献精确应用，确认其已将存在性/FIP标为既知 Paper Fact 的重构接口；阈值式、势、删除构造及反边界数值不变。独立程序针对这个最终 hash 重跑通过。

## 读作者稿前的独立重构

固定 hub 后，每名 light 的 side 成本只依自己的动作：一条 side 的另一类战略用户都是已冻结的 hubs。因此每个 source 的 light 组独立。对某 source 重新命名其 hub 副本为 0，hub 权为 a>0，light 总权 W。令 S 为选 0 的 light 集、总权 L。

独立推导先使用包含偏离者的变量 y：对权 w_i 的玩家 i，比较其选 0 和选 1 的真实成本得到

    E_i(y)=F(a+y)−F(W−y+w_i)+q_i^0−q_i^1,
    y∈{w_i+Σ_{j∈T}w_j:T⊆I\{i}}.

若 F 非恒定，则其在非负半轴严格递增，所以 E_i 严格递增。选有限可达集合的符号切点 r_i，可构造

    Φ(S)=L²−Σ_{i∈S}w_i(2r_i−w_i).

加入 i 的变化是 `2w_i(L+w_i−r_i)`，删除 i 的变化是 `−2w_i(L−r_i)`。令 `t_i=r_i−w_i` 就是作者变量，作者势恰为该 Φ 的一半。完整成本差和势差有相同符号。平局时要使势差也为零，必须准确选平局点，不能随意在零集合外选阈值。

F 为常数时所有主资源项抵消，成本差为玩家私有动作常数。此时取线性势 `Σ_{i∈S}(q_i^0−q_i^1)`，而非强行使用二次式。因而常数和零费用也有平局保留的序势。

## 冻结稿逐项攻击

1. **真实负载。** 作者式(1)中的 `W−x` 必须包含偏离者 w_i；独立 literal 实现确实使用全部资源用户重新求和，不把它写成 `W−w_i−x`。与上述 E_i 代换一致。
2. **离散阈值。** `X_i` 永远非空，至少含 0。非常数 F 使 D_i 严格递增，至多一个可达零点；存在两种符号时最大负点小于最小正点，阈值可在两者之间。仅有正值/负值时可以选可达区间外；单名 light 的单点集合也覆盖。
3. **零区间。** 非恒定非负多项式不存在让 D_i 在不同 x 处同时为零的区间。恒定 F 下 D_i 可处处为零，作者单独的线性势使所有这些边恰好为平局。因此没有漏掉零区间，也没有伪造严格下降。
4. **边界和支配。** 端点零恰令对应真实边和势边打平；严格支配动作对应阈值在可达范围外。任意实权造成的重复子集和只合并 x 值，不改变成本比较。
5. **结论强弱。** 势不仅在每条严格 light 改善上下降，还对每条单方边保留全符号，故每个 light PNE 恰为势局部最小点；有限状态严格下降证明全部严格 light 路径终止。它不意味着原成本差等于势差，不能称 exact potential。
6. **source 分离。** 两个 source 的主副本互异；side 仅含一名 light，冻结 hubs 后无法重新耦合两组 lights。各 source 的势相加合法。若放宽为多 light side，该分离机制实际失败，见下面反例。

## 有序删除：先独立重构，再核作者新节

从全 0 开始，按 t_i 非降扫描。若 `L−w_i>t_i` 则删除 i。这是合法实际严格改善，因为当时 `L−w_i∈X_i`。被保留者满足 `L−w_i≤t_i`，以后 L 只下降，最终仍不愿离开。删除者 i 在删除后满足 `L>t_i`；后来若删除 j，则新 L 满足 `L>t_j≥t_i`。因此全部此前删除者一直不愿回到 0。最终每名 light 精确稳定。平阈值的任意顺序和弱边界均成立。

此构造每名 light 至多一次实际严格移动。它不证明任意起点至多一次，也不证明总输入位复杂度多项式：有限可达阈值的直接构造可以枚举指数多子集，任意实系数输入下的计算模型并未指定。作者新节明确保留这些限制。

## 独立 Fraction 审计与 multi-light 反边界

独立程序 `independent_fixed_hub_light_threshold.py` 不导入作者程序，不使用作者成本核心。它显式为全部玩家建立两个资源子集，逐资源汇总包括冻结 hubs 的真实总负载；阈值直接从 literal 两端成本差重建，势用成对项 `Σ_{i<j∈S}w_iw_j−Σ_{i∈S}w_it_i` 实现。逐状态检查全符号、PNE 与势局部最小一致、严格改善图 DAG，并运行两种阈值打平次序的有序删除。

独立 seed 为 930411；515 个固定 hub 实例，8976 完整 light 状态，19729 条严格改善边，6876 条平局边和 737 个可达阈值零样本全部通过。含零/常数主费、空 light/side、空 side hub 集、异权 hubs、多 source、source 自己参加 side 以及全部固定 hub 位。最大测试规模为 3 hubs、6 lights、费用次数 4。完整实际输入、Python/源码/候选 hash 和统计写入配套 JSON，全部算术为 Fraction；有限证据不替代实参数证明。

另独立重建作者复用的 multi-light side 反边界：light 权 `(1,2,3)`；side light 集 `{1,2},{1,3},{2,3}`，费用 `2100x²,1130x²,499x²`；新增固定 source hub 的主费为零，且不参加 side。四个补位代表状态的真实结果为：

| 状态 | 三玩家成本 | 一条严格出口 |
| --- | --- | --- |
| 000 | (36980,31375,30555) | 1:36980→3230 |
| 001 | (20030,20896,14661) | 2:20896→20875 |
| 010 | (20180,10396,22571) | 1:20180→20030 |
| 011 | (3230,20875,22645) | 3:22645→22571 |

补位对称覆盖全部八态。最优纯状态因子为 `20896/20875>1`，无精确 PNE。反例原先已在 `heterogeneous_hub_sorted_side_review.md`§4登记，因此新接口应引用并重标该既有资产，不称新反例或全类下界进展。独立 JSON 包含全部八态偏离成本及实际参数。

## 文献事实与新颖性边界

独立检索首先核对 MFCS 2007 的作者 PDF *Congestion Games with Player-Specific Constants*（https://econ.biu.ac.il/sites/econ/files/shared/staff/u36/papers/constants.pdf），其 pp635–636 明确区分 weighted 与 player-specific 及三链改善环；不能将任意资源 singleton 存在定理直接用于两种变化同时存在的模型。

随后检得并直接阅读 Milchtaich, *Congestion Games with Player-Specific Payoff Functions*, Games and Economic Behavior 13 (1996), 111–124（https://www.cs.cornell.edu/courses/cs684/2005fa/milchtaich.pdf）。其 §4 Theorem 1（p114）证明两策略 FIP；§8（p121）明确说明该证明对正权玩家仍成立，p123 表格也明确列 weighted/two strategies 为 FIP。

固定 source 的子游戏是该已知类的直接特例：资源 0/1 上玩家 i 的收益分别为 `−F(a+x)−q_i^0` 与 `−F(y)−q_i^1`，均随资源总 light 权非增。故 FIP 与精确 PNE 的存在本身是已知 Paper Fact 的直接应用，不能称新颖定理。当前可复用价值是将它具体接入本仓库 unique-light 模型，给平局精确保留的显式阈值势和有序删除响应，并明确阻止 hub 重置误用。此次未检索到完全同式的阈值势或同一删除程序，但这一有限检索不认证其新颖性。自足证明无需导入该文献结果。

## 结论

在所述冻结 hub、unique-light side 范围内，未发现 fatal objection；符号精确保留序势、FIP、精确 light PNE 与有序删除构造均成立。multi-light 反边界与不能自动 lift hub 响应的限制应保留。该 lemma 只闭合固定外场的 light 响应义务；跨 hub 变动的势变化和真实冻结 light 偏离预算尚未闭合，全类主问题不升级。

正式路径整合只更改临时身份、相对链接、状态和审计入口，未更改已审数学正文；独立程序的稿件读取路径现指向规范正文，不再依赖原scratch位置。完整运行和输入冻结到正文所列两份JSON，数学适用范围不因此扩大。

## 规范整合的独立逐字节复核

独立审查者将正式正文 `research/current/weighted_congestion/fixed_hub_light_threshold_response.md` 与最终冻结 `4a071681b6ddbe0babafd6ea3ad03842f6a8da8dba262b4d1de93e2be1c3be60` 作只读 diff，并用 Python 核对从“精确陈述与证明概览”至原“复验”末尾的数学正文：去掉尾部空白后全部 8300 字节相同，该正文片段 SHA256 为 `b4c527a0137d5ba015e12bf2fd6013b98303cd6a23bd17458382755c3a7ac8c8`。实际改动限于删除临时候选身份、修正共享侧正文相对链接、将 Evidence/Status 改为已经完成的内部重构与审计状态、Related Files 接入正式入口，以及追加规范审查和复验路径；精确对象、量词、假设、成本式、阈值势、删除证明、反边界数值和文献应用均未改。

正式正文 SHA256 为 `511432133cd538344629caaa3376be4fc18f122ad288df41cc41bec8f1d6f700`。独立程序的正式版本只将稿件路径从临时绝对路径改成仓库相对路径，并将输出字段 `candidate_sha256` 改为 `canonical_sha256`；literal 成本、阈值、势、DAG、有序删除和多 light 反边界核心均逐字节未变。正式源码 SHA256 为 `1ea5e5d926cded51254bc27c7d6985dae2ba5fa574494e49144e897950c6d865`。

独立审查者已再次实际运行正式程序，并逐项比较其 seed、实例数、全部统计、全部实际输入、multi-light 八态证书、正文 hash 和源码 hash 与规范冻结 `evidence/runs/weighted_congestion/fixed_hub_light_response/independent.json` 一致；515 个实例全部通过。此次仅更新本审查记录，没有改正文、冻结证据、共同账本或 Git。
