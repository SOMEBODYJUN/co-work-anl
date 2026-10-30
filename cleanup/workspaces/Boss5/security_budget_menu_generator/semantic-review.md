---
id: "customer-attraction/security-budget-menu-generator-review"
kind: "review"
type_tag: "审查"
title: "固定有限游戏的完整纯 SPE 菜单与预算极值生成器审查"
status: "draft-ready-for-checkpoint"
truth_status: "exact-finite-fixed-game-result; no-universal-half-claim"
review_level: "source-read-output-field-reconciliation"
scope: "budget_menu_generator.py 及其固定四游戏输出；不扩展到任意客户集、任意策略或六人半覆盖"
summary: "源程序按对称计数状态递归保留每个前缀可由完整纯 SPE 实现的终局计数菜单，并对每个有序实际路径逐个优化首次偏离分支的独立查询均值。精确 Fraction 输出四个固定游戏的最大 Σ_i C_i(p)−W 均为负；这关闭指定游戏和指定安全分布的 GB 接口，不是一般半覆盖反例。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/customer_attraction/security_gluing_2026-10-10/budget_menu_generator.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/customer_attraction/security_gluing_2026-10-10/budget_menu_generator.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/customer_attraction/onpath_budget_failure.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/customer_attraction/aggregate_theta_failure.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/customer_attraction/root_tax_failure.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/customer_attraction/global_decorrelation_failure.json"
---
# 固定有限游戏的完整纯 SPE 菜单与预算极值生成器

## 1. 来源身份与问题

冻结来源 `c87dddcc86c72255caea` 是
`history/source/notes/customer_attraction/security_gluing_2026-10-10/budget_menu_generator.py`，源字节 SHA-256 为
`51b775001f14b0e7b98de20e85d82ff9daeede9a1dd8d470014657cea8bbe2a2`，大小 5417 字节。它在同一内容的两个历史版本（`68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`）中均出现。

程序研究的是一个**固定**有限共同目录游戏、固定完整纯 SPE 的静态安全查询分布 (p)，并计算该固定游戏上所有完整纯 SPE 中可以达到的最大
\[
  G_B(\sigma,p):=\sum_i C_i(\sigma,p)-W(\sigma),
\]
其中 (C_i) 是玩家 (i) 所有首位偏离分支的独立查询平均值，(W) 是实际终局覆盖人数。若最大值仍为负，表示在该固定游戏和该 (p) 下，任何完整纯 SPE 的独立查询预算都小于实际福利；这只是一个固定接口的有限障碍。

程序不证明对任意客户类型、任意完整策略或任意安全分布均有某个符号，也不计算六人目标的 \(\operatorname{OPT}_6\le 2W\)。

## 2. 输入模型与精确量

游戏 JSON 给出 `players=n`、主题集合及客户类型。每个类型是兴趣主题集合 (L\subseteq[m]) 与整数重数 (w_L\)。重数可解释为单位客户复制。终局由主题计数向量 (q=(q_0,\ldots,q_{m-1})) 表示，\(|q|=n\)。对主题 (a) 的客户收益为
\[
 f_a(q)=\sum_{L\ni a}\frac{w_L}{\sum_{b\in L}q_b}.
\]
`utility(a,q)` 用 `Fraction` 逐类型求和；`coverage(q)` 为至少有一个被选主题的客户重数总和。安全查询分布 `p` 也是有理数，程序在初始化时断言 \(p_a\ge0\) 且 \(\sum_a p_a=1\)。

若玩家在自己的偏离主题 (b) 后，剩余竞争计数为
\[
 B=q-e_b,
\]
则 `query_mean(b,q)` 计算
\[
 g_b(q;p)=\sum_{a=0}^{m-1}p_a
       \sum_{L\ni a}\frac{w_L}{1+\sum_{x\in L}B_x}.
\]
这正是该首位偏离分支在查询主题 (a) 下的客户份额，再对固定 (p) 平均。程序只把第一个偏离玩家的行动从 (q) 中扣除；其余玩家按该分支的完整续局计数执行。

## 3. 菜单递归为何刻画固定计数对称游戏

`menus(c)` 返回在给定有序前缀计数 (c) 后，某个完整纯 SPE 续局可以产生的所有终局计数向量。递归基为 \(|c|=n\)，此时唯一终局是 (c)。对非终局状态，先递归所有下一行动 (a) 的子菜单
\[
 M_a=M(c+e_a).
\]
对每个动作取该分支最坏可实现收益
\[
 \ell_a=\min_{q\in M_a} f_a(q),
 \qquad
 \ell(c)=\max_a\ell_a.
\]
保留的菜单是
\[
 M(c)=\bigcup_{a=0}^{m-1}\{q\in M_a:f_a(q)\ge\ell(c)\}.
\tag{M}
\]

递归的充分性来自完整纯 SPE 的单节点序贯理性：当前动作 (a) 的后继终局可以从 (M_a) 取任一项；对每个其他动作 (b)，该偏离分支是另一个有序历史，其续局可独立选择为 (M_b) 中的任一项。因此存在某个动作达到 (q) 且所有动作的最坏续局收益不超过 (f_a(q))，恰好等价于 (M)。必要性则由任一完整 SPE 的实际后继逐分支属于相应 (M_a)，并满足当前动作收益不小于每个分支的最小值。

计数压缩只利用客户收益对同一主题计数的对称性；它没有把有序历史的策略合并成一个不完整对象。`generic_policy` 从目标终局计数递归选择一个合法动作，并对每个动作的离轨子树递归选择一个合法菜单终局，最终给出所有长度小于 (n) 的有序历史的行动表。断言
\[
|\text{policy}|=\sum_{i=0}^{n-1}m^i
\]
保证策略覆盖了全部有序历史。

## 4. 固定有序路径上的精确预算优化

程序遍历所有主题序列 (z=(z_1,\ldots,z_n)\in[m]^n)。令其终局计数 (q_z) 属于根菜单 (M(0))，则该路径至少有一个完整 SPE 实现。对第 (i) 位的实际主题 `own=z[i]`，记真实玩家收益为 (u_i=f_{z_i}(q_z))。在真实前缀计数 (c_i) 后，对每个首次偏离主题 (b)：

* 若 (b=z_i)，分支仍取 (q_z)。
* 若 (b\ne z_i)，从 (M(c_i+e_b)) 中只保留满足 (f_b(r)\le u_i) 的终局 (r)。这些 (r) 正好是不会让该玩家通过首位偏离获得严格更高收益的续局。
* 在剩余候选中，按 ((g_b(r;p),r)) 字典序最大化，得到该偏离分支能给总查询预算的最大值。

不同真实节点的不同首次偏离历史互不相交；因此可以分别选择这些分支的续局，并把它们装配到同一份完整策略中。对路径 (z)，程序累加
\[
 C(z,p)=\sum_{i=1}^{n}\sum_{b=0}^{m-1}p_b\,g_b(r_{i,b};p),
\]
其中 (r_{i,b}) 是上述分支选择。随后计算
\[
 G_B(z,p)=C(z,p)-\operatorname{coverage}(q_z),
\]
并在所有根菜单允许的有序路径中取最大值。`possible_ordered_SPE_paths` 只计数满足根菜单的有序终局路径；它不是完整策略数量，也不是所有离轨回复组合数量。程序为每个达到最大值的路径构造一份见证策略，但不声称保存了所有等价策略。

该路径级优化是精确的：菜单递归给出每个分支可实现终局的全集，SPE 只要求偏离分支收益不超过真实收益，且分支选择独立；故任一完整 SPE 的 (C(z,p)) 不超过程序对该路径的取值，而程序选择的各分支可由 `generic_policy` 合成为完整纯 SPE，达到该取值。

## 5. 源程序直接覆盖的四个固定游戏

`run()` 的源字节明确读取四个名称：

1. `original36`：`aggregate_theta_failure.json` 游戏，安全证书取 `onpath_budget_failure.json` 的 `security.primary`；
2. `individual360`：由外部 `security_cone_attack/individual_security_failure_360.json` 提供 `game` 与 `security`；
3. `root_tax_failure`：根税输入和证书；
4. `global_decorrelation_failure`：总去相关输入和证书。

已有归档输出 `archives/customer-attraction/tools/evidence/security-cones-new/original/` 的五个 JSON 中，`individual34` 是另一批固定游戏扩展产生的结果，不是本 92 行源程序 `run()` 的直接四项循环；不能把它或 61 客户结果倒填为本源代码输出。它们可以作为相关独立对象引用，但应保留来源边界。

## 6. 冻结输出字段与数值

对源程序直接覆盖的四项，归档 JSON 的关键字段如下。`GB_violation_sumC_minus_W` 是程序最大化后的 (C-W)，负值表示该固定 (p) 下所有完整 SPE 的 (C-W) 都为负。

| 游戏 | 根菜单数 | 有序终局路径数 | 达到路径 | (W) | \(\sum_iC_i\) | 最大 (C-W) | 完整策略动作数 |
|---|---:|---:|---|---:|---:|---:|---:|
| original36 | 20 | 48 | (0,3,4) | 34 | 187/6 | −17/6 | 43 |
| individual360 | 15 | 23 | (0,4,3) | 336 | 1191500603/3710088 | −55088965/3710088 | 43 |
| root_tax_failure | 12 | 102 | (0,0,0,4) | 38 | 73/2 | −3/2 | 259 |
| global_decorrelation_failure | 2 | 6 | (5,0,0,2) | 85 | 828050154289/10570351740 | −70429743611/10570351740 | 259 |

这些字段与已有《固定安全预算锥的五个精确失败实例》及《总安全预算的完整策略、静态证书与全表独立核验》一致。它们应读成“在四个指定游戏、四个指定安全分布上，完整纯 SPE 菜单搜索未找到非负 (C-W)”；不能读成所有完整 SPE 或所有 (p) 的统一支付定理。

## 7. 证据边界与可复验性

源程序中的 `BASE=/workspace/scratch/4fa21fc3d3cc`、`OUT=BASE/security_cone_attack`、`ROOT=BASE/co-work-anl` 是原运行环境绝对路径。当前仓库没有那个目录，因此直接执行原文件前需将输入路径映射到冻结副本，并为 `individual_security_failure_360.json` 准备其原始 `game/security` 文件。现有五个输出、`security-cones-new/source-manifest.json` 及独立 Fraction 审计已保存输出字节和 SHA；这些可用于复核字段和策略动作，但不能冒称“在当前 clone 直接重跑原路径”。

已有独立审查把计数递归与不使用计数压缩的有序历史验证分开；其固定游戏结论是同一组有限数值，且每例均保留完整策略动作表、客户类型和安全分布。复验时应至少：

```sh
# 将原程序的 BASE/ROOT/OUT 改为冻结输入副本后
python budget_menu_generator.py
# 对四份 all_SPE_GB_*.json 逐字段重算 Fraction，并核 strategy.actions 覆盖全部历史
```

这类重放是有限计算证据，不是数学普遍性证明。尤其不能从 `possible_ordered_SPE_paths` 的有限计数推出任意客户集或六人 half；也不能用 `GB_violation_sumC_minus_W<0` 反向断言存在 (W<nv_n) 或 \(\operatorname{OPT}_6>2W\)。

## 8. 处置与接续

本源独有内容是“菜单递归 + 首次偏离分支独立极值”的精确算法和四个固定游戏上的最大 (C-W) 数值；已有障碍正文承载其数学解释与五个固定游戏扩展。建议：

* 将本稿与冻结源、四个输出的 manifest 一起 checkpoint；
* 对源 `c87dddcc86c72255caea` 记 `integrated`，source_refs 指向本稿及四输出，不创建重复的“六人反例”对象；
* 将 `individual34` 与 61 客户结果继续保留在其各自来源对象中，注明它们不是本源 `run()` 四项循环；
* 第三阶段建立“固定游戏完整 SPE 菜单枚举 → 固定预算障碍”关系边，并与“逐人安全失败”“全局预算桥仍开放/已被指定例纠正”分开；
* 若要攻击六人 half，必须改变完整策略/客户游戏或构造安全最优分布的全称反例，不能在这四个已经穷举的固定游戏上重复调平局。
