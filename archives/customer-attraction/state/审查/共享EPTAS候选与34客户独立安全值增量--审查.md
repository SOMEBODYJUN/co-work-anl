---
id: "customer-attraction/shared-eptas-and-individual-security-increment-20261030"
kind: "review"
type_tag: "审查"
title: "共享 EPTAS 候选与 34 客户独立安全值增量审查"
status: "finite-audits-classified"
truth_status: "exact-fraction-finite-cag-replay-with-duplicate-source-boundary"
review_level: "full-source-read-and-cross-archive-comparison"
scope: "shared_eptas_candidate finite four-site probes plus independent exact replay of the 34-customer individual-security counterexample"
source_refs:
  - "source:d027eeb6603c80ef3c5a:evidence/runs/2026-10-09/shared_eptas_candidate.json"
  - "source:d84b4339b784d8c9a9ea:evidence/runs/2026-10-10/individual_security_independent_replay/report.md"
  - "source:78e8551ac6447ffc0f70:evidence/runs/2026-10-10/individual_security_independent_replay/results.json"
evidence_manifest: "../../tools/evidence/cag-eptas-individual-20261030/source-manifest.json"
---

# 1. 阅读范围与模型身份

本批三项来源都属于 customer-attraction/CAG 证据线。第一项是共享 EPTAS 候选的四设施有限 probe；后两项是 34 客户、三玩家、六主题逐人静态安全值反例的独立 exact replay（一个 Markdown 报告加一个完整结果 JSON）。本批没有改变当前六人 Q-CAG-HALF-6 的目标，也没有把三人反例改写为六人结论。

旧档案已经有《三人逐人混合安全值击穿》正文和《后继安全值与完整树精确审计》计算资源。后两项因此属于**独立运行增量**：它们重新核验同一输入的策略、全历史偏离、静态 primal/dual 与预算恒等式，不能再计作一个新的 34 客户反例。第一项则是另一个共享 EPTAS candidate finite audit，单独保留其四设施 probe 量词。

# 2. 共享 EPTAS candidate：186 个有限输入

## 2.1 领域与计数

`d027eeb6603c80ef3c5a` 的状态为 `all assertions passed; finite audit only`，使用 Fraction、无浮点；seed=20261009003，Python 3.12.14，重放命令是 `python3 tests/audits/shared_eptas_candidate.py`。参数说明为：180 个 seed-random four-site inputs，至多六个 clients，显式有理权重和随机 coverage；另有三个 gap-family 输入和三个 zero/tiny-denominator 输入；
\(η\in\{1/8,1/4,1/2\}\)。总计字段为：

- instances=186，layouts=2976；
- full cells examined=73304；
- far patterns=14590，near patterns=7295；
- conditional-cost comparisons=166968；
- facility deviations=1116。

这些数值说明脚本确实覆盖了列明的有限四设施样本和近/远模式比较，但不是所有客户数、设施数、coverage 结构或 η 的全称量词。源的 limitations 明确写出“finite preliminary audit only”“samples may overlap other audits”“no canonical EPTAS implementation or general theorem certified”。

## 2.2 精确结果和异常行

186 行中绝大多数满足 `optimal_alpha=menu_bound=actual_alpha=1`。非平凡的精确行包括：

| η | optimal alpha | menu bound = actual alpha | 解释 |
|---:|---:|---:|---|
| 1/8 | 85/81 | 85/81 | 有限 gap-family 行 |
| 1/8 | 16/15 | 16/15 | 有限 gap-family 行 |
| 1/2 | 34/31 | 34/31 | 有限 gap-family 行 |
| 1/2 | 1 | 47/46 | menu/actual 边界超过1 |
| 1/2 | 8589934592/8291672987 | 同值 | 大分母 exact 行 |
| 1/4 | 13/10 | 2301/1760 | 菜单上界与实际值分离 |
| 1/4 | 2124/1625 | 2275/1728 | 有限菜单/实际误差 |
| 1/8 | 144508/110895 | 5135/3888 | 有限大分母误差 |

这些行只说明在脚本生成的具体 input/layout 上，三种 alpha 字段的 exact 比较结果。`menu_bound` 高于 `optimal_alpha` 的行不能被解释成一个通用 EPTAS 近似比；`actual_alpha` 与 menu bound 相同也不能证明菜单构造对所有输入都可实现。它们的用途是回归候选和边界定位：后续若要形成正式算法命题，必须给出输入编码、菜单生成、近/远分类的全称定义和误差随 η 的证明。

## 2.3 与 CAG 六人目标的边界

共享 EPTAS candidate 不是当前有限单位客户、完整有序历史或纯 SPE 模型：它采用 four-site/client/coverage 的候选接口，最多六客户，并且 source 自己没有 canonical EPTAS implementation。因而它不支持六人目录最大覆盖人数的一半，也不替代六人终局覆盖者均分。归档为 CAG 相关的有限候选/障碍，保持其模型身份。

# 3. 34 客户独立安全值复核

## 3.1 输入、全历史和纯 SPE 核验

`d84b4339b784d8c9a9ea` 是 independent exact review 的 Markdown 报告，声明只读取 self-contained JSON，不导入作者 solver/verification code，所有收益和预算直接用 Python Fraction。输入为 3 players、6 topics、34 个 distinct unit customers（13 customer types），完整策略有 43 个有序非终端历史；216 个 ordered terminal profiles、258 个 one-action continuations、215 个非处方偏离，其中 144 严格更差、71 平局。21 个无序静态 rival backgrounds（等价36个有序背景）、126 个纯查询、1548 个 continuation-background query entry 全部逐项计算。

报告结论与已有反例一致：实际 profile 为 ((0,3,4))，收益
[
(u_1,u_2,u_3)=(29/3,67/6,67/6),
\qquad W=32,
\qquad \operatorname{OPT}_3=34.
]
所有策略节点最优，故这是完整历史纯 SPE 的独立复核；全终局收益和覆盖恒等式也逐行通过。

## 3.2 静态安全值的精确 primal/dual

结果 JSON 的 summary 给出：

[
\min_B E_p[f_B(a)]
=\max_a E_Q[f_B(a)]
=\frac{2411}{246}.
]

六个 dual queries 全部等于 (2411/246)，dual slacks 全部为零；positive dual support matrix determinant 为 (-12055/48)，uniqueness rank=6，primary distribution 因而唯一。报告进一步保存了 6 行唯一性方程和所有 policy-node query matrices。它不是数值 LP 近似，而是 exact rational primal/dual witness。

实际路径的逐人安全差为
[
(u_1-v_3,u_2-v_3,u_3-v_3)=(-11/82,56/41,56/41),
]
所以根玩家的逐人不等式失败，normalized gap 为 (11/2788)。同时
[
W-3v_3=213/82>0,
\qquad W-\operatorname{OPT}_3/2=15>0,
\qquad GB=60/41>0.
]
这三条正量必须与根的负逐人边界分开记录：独立复核再次确认逐人安全值桥失败，但聚合预算和 half 在此例仍成立。

## 3.3 预算分解和与旧证书的关系

结果 JSON 的三个 actual budget nodes 给出

| history | D | C | e | kappa |
|---|---:|---:|---:|---:|
| (()) | 29/3 | 2411/246 | 0 | -11/82 |
| ((0,)) | 5311/492 | 1252/123 | 61/164 | 101/164 |
| ((0,3)) | 2597/246 | 2597/246 | 25/41 | 0 |

所以 (sum e=161/164)、(sumkappa=79/164)，两者合成 (GB=60/41)。这与旧正文中的 (p^*=(10,10,21,10,10,21)/82)、六个正对偶支持、43 历史/258 比较完全吻合；新增内容是独立代码路径、结果 JSON 的完整 all-policy/all-terminal 数据和唯一性 determinant 的重新保存。

本批独立复核没有证明 34 客户最小性，也没有排除其他策略/客户数的更强反例。它只证实已有反例的定义域、全历史量词、精确安全值和预算层级。

# 4. 与已有数学对象和后续纠错的关系

1. **与已有 34 客户反例：** d84 报告和 78 结果应合并进既有反例的“独立 replay 证据”层，保留其独立输入 SHA、43 节点、216 终局、determinant 和完整结果数组；不重复建立同名反例。
2. **与 CAG 2026-10-21 CCE/分数负载批：** CCE 福利替换和实际 load 查询是不同量词；34 客户复核再次确认 (v_3=2411/246) 的静态混合安全值不能被 actual-load (M) 取代。不能用 shared EPTAS candidate 的 alpha 行去填补这条模型差异。
3. **与当前六人 half 目标：** 34 客户例只有三位玩家；它只否定逐人 (u_i\ge v_n) 的早期桥，不否定六人聚合 half。共享 EPTAS candidate 也没有共同目录/完整历史语义，不能承担六人覆盖结论。
4. **与未来修复：** 若继续处理共享 EPTAS 方向，应先把 menu bound、actual alpha 和 optimal alpha 的定义写成同一输入对象，并对异常行给出可复核的近/远分类证明。若继续处理逐人安全值，已有反例的重点是聚合补偿和后继预算，不应再次尝试未经条件的逐人桥。

# 5. 逐源处置

- `d027...`：集成为共享 EPTAS 候选的有限回归/边界证据，保留 186 instances、2976 layouts、166968 comparisons 和全部非平凡 alpha 行；分类为 retained finite candidate，不称 EPTAS 定理。
- `d84...`：集成为 34 客户反例的独立 exact review 报告，保留报告中的全历史、primal/dual、预算与复现命令；分类为 integrated 独立复核。
- `78e...`：集成为同一独立复核的完整结果 JSON，保留 all-policy/all-terminal、topic differences、uniqueness equations 和 exact matrices；分类为 integrated 证据副本。

本批没有新增六人半覆盖证明，也没有把任何有限候选、独立重放或重复输入升级为一般 theorem。
