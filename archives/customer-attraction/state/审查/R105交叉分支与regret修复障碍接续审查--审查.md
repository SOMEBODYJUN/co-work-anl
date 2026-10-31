---
id: customer-attraction/R105-cross-branch-and-regret-repair-boundary-review-20261031
kind: review
type_tag: 审查
title: R105 交叉分支与 regret 修复障碍接续审查
status: complete-source-read-integrated-as-boundary-not-general-result
truth_status: Q-CAG-HALF remains open; zero-regret repair bridge refuted; factor-two regret coefficient attempt leaves C>=1 lower bound only
review_level: full-source-read-cross-comparison-with-existing-CAG-objects
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/independent_general/independent_reconstruction.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/independent_general/independent_reconstruction.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_cross_branch/zero_regret_welfare_repair_obstruction.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_cross_branch/zero_regret_welfare_repair_obstruction.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_induction_repair/factor_two_regret_attempt.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/new_induction_repair/factor_two_regret_attempt.md
evidence_paths:
  - archives/customer-attraction/tools/evidence/R105-cross-branch-boundaries-20261031/manifest.json
  - archives/customer-attraction/tools/evidence/R105-cross-branch-boundaries-20261031/independent_reconstruction.md
  - archives/customer-attraction/tools/evidence/R105-cross-branch-boundaries-20261031/zero_regret_welfare_repair_obstruction.md
  - archives/customer-attraction/tools/evidence/R105-cross-branch-boundaries-20261031/factor_two_regret_attempt.md
related_objects:
  - ../问题--问题.md
  - ../审查/一般半覆盖问题接口与异构趋二下界跨模型审查--审查.md
  - ../审查/上传精确SPE脚本与个体安全压缩生成接续审查--审查.md
  - ../推论/尾部利润界向任意总人数的合法提升--推论.md

# R105 交叉分支与 regret 修复障碍接续审查

本审查完整读取 R-105 工作区的三份研究文档。三份来源都围绕顺序客户吸引的一般 `Q-CAG-HALF` 目标：有限单位客户、有限共同目录、单位提供者、所有有序历史上的完整纯 SPE。它们的共同结论是保持开放状态并精确记录失败桥，不构成一般 half 证明或完整反例。

## 1. 原件身份

| source ID | 路径 | blob | 字节 | SHA-256 |
| --- | --- | --- | ---: | --- |
| `aeed4a9e3eff72fe8f56` | `.../independent_general/independent_reconstruction.md` | `89456ebd8658c62620b70eae48f65dccb4ffc59a` | 8505 | `30c2023da8fbb73288fbce795d9cfeeba62269e20376f3828fc38840e9dad42e` |
| `1ee4950f653a57911a9b` | `.../new_cross_branch/zero_regret_welfare_repair_obstruction.md` | `86b24508984b9b74f4e5abccdf65481db7e7c711` | 7570 | `bb9e62d08d8419a98389b0a792427b3518b9383430d1d6b8d4070f16dd1d9576` |
| `06627fd33b7bef833233` | `.../new_induction_repair/factor_two_regret_attempt.md` | `8555caeb81cd9d88add52e047fedcf9c7b482c4d` | 6969 | `8982b2831ad5a7b7e53bf4a135ae081d575008090c6e44ed313751036c8bb2f8` |

完整路径、双提交 source refs 和证据副本记录在 `archives/customer-attraction/tools/evidence/R105-cross-branch-boundaries-20261031/manifest.json`。

## 2. `independent_reconstruction.md`：交叉分支义务与已知候选

该文档独立重构了一般证明的真实义务：固定完整纯 SPE `sigma` 和比较主题后，强制某个玩家改选主题产生的终局由**真实离轨分支**决定，后继玩家可以改变行动。因而任何静态 smoothness 交换都不能把离轨后继替换成一个共同实际对手多重集。即使使用调和势

\[
\Phi(z)=\sum_x H_{c_x(z)},
\]

也会出现“完整终局势差减去删除当前玩家后的势差”；丢掉删除势差正是冻结后继的错误。

文档重写了匿名计数终局对应集：对前缀计数 `b` 和动作 `A`，若 `R(b+e_A)` 是所有完整纯 SPE 终局集合，令 `ell_A(b)` 为该分支行动者收益最小值、`M(b)=max_A ell_A(b)`，则

\[
R(b)=\bigcup_A\{q\in R(b+e_A):U_A(q)\ge M(b)\}.
\]

不同有序节点即使计数相同，也可独立选择对应集合中的不同终局；这不是 Markov 选择器定理。

它重新发现了既有 full-terminal-tax/OCC-CAP 候选

\[
F(c)=\sum_{x:c_x>0}\left(2-\frac1{c_x+1}\right)=W+E(c),
\quad E(c)=\sum_{x:c_x>0}\frac{c_x}{c_x+1},
\]

并给出静态分解 `G_c(T)=sum_{x in T}1/(c_x+1)`。候选比较并集的逐客户不等式需要保留重复比较客户、实际客户在比较并集外的 slack；简单桥 `m max_T G_c(T)<=W` 已被已有 14 客户完整 SPE 击穿。文档也记录多 punisher amplification 只是 OCC-CAP 已有诊断的重复，不形成新不可能性定理。

有限 Fraction 评估、800 个随机小实例和 154 个策略采样均未找到该候选的反例，但没有回收精确 dual，也没有形成一般 theorem；故本源增量是“独立推导和 stop point”，不是新正面结果。

## 3. `zero_regret_welfare_repair_obstruction.md`：零 regret 不能保证无损重选

该文档给出精确两人尾部 CAG 输入：主题 `A,B,C,D`，18 名单位客户，合法背景为一位过去玩家选 `A`，尾部有两位提供者。原尾部完整纯 SPE 的唯一菜单是首位 `C`、末位在首位 A/B/C/D 后选 C/C/B/C；实际尾叶为 `(C,B)`，福利 `W=17`。

在保留旧策略、删除背景 `A` 后，实际两个节点的全部真实单步 regret 均为 0；但删除后的完整 SPE 逐行收益表严格固定唯一菜单 `(C,D,B,B)`，因此删除后唯一完整 SPE 是 `(D,B)`，福利仅 16。复制全部客户 `t` 次会使原福利/修复损失变为 `17t`/`16t`，regret 仍为 `(0,0)`。这排除了任何仅由 `n` 和实际 regret 向量决定、在零向量处有限的无损修复误差函数：若存在，则要求 `t<=F_2(0,0)` 对任意正整数 `t`。

该障碍只否定“冻结旧实际分支 + 零 regret ⇒ 可重选同福利 SPE”的桥；它不否定带新枝信用、被删者利润或完整离轨菜单信息的修复定理，也不构成 half 反例。文档明确和已有五客户 suffix-blind 例区分：后者删后仍能维持原福利，本例才证明任意重选都损失客户。

## 4. `factor_two_regret_attempt.md`：保留全历史 factor-two 后仍只得 C≥1

该文档不再假设 SPE，而测试更强合同：完整历史 forced payoff 对 prescribed payoff 至多 2 倍，定义全深度 regret 总额 `B=sum_i max_h R(h)`，试图证明

\[
OPT_m-2W\le C B.
\]

它构造任意 `m>=2` 的不交主题族：大主题 `A` 有 `L=ceil((m-1)/2)` 名客户，其余 `m-1` 主题为单例；形式策略前 `m-1` 位都选 A，末位选真实最佳单例。该策略满足完整历史 factor-two 条件，实际福利 `W=L+1`，最优 `OPT_m=L+m-1`，且

\[
B=m-1-L,\qquad OPT_m-2W=B-2.
\]

因此任何绝对系数合同至少要求 `C>=1`，但没有否定 `C=1`，也没有证明合同。对 `m=5` 得 `L=2,W=3,OPT=6,B=2`，只是 half 等号的非-SPE形式策略例。

文档进一步说明把逐节点 factor-two regret 和静态税行直接相乘会得到随 `m/H_m` 增长的弱系数，不能自动给常数 2；真正缺口是不同 forced continuation 之间的动态关系。`B=0` 正是完整 SPE 情形，因此若证明 `C=1`，就会直接解决 Q-CAG-HALF，不能把它当已有桥。

## 5. 与现有对象的关系和边界

| R105 内容 | 现有对象 | 处置 |
| --- | --- | --- |
| 真实离轨对应集合、full-terminal-tax 候选、静态桥失败 | `一般半覆盖问题接口`、现有 OCC-CAP/税审查 | 作为独立重构和 stop point；不新造 theorem |
| 零 regret 重选必损福利 | CAG repair/suffix-blind 障碍对象 | 新增更强的合法背景障碍；不升级为 half 反例 |
| factor-two regret 系数尝试 | 尾部 regret/完整历史安全合同 | 只证明任何绝对系数至少 1，合同仍 OPEN |

本批确认的共同状态是 `Q-CAG-HALF OPEN`。可继续使用的证明义务是：真实离轨分支的共同支付、保留比较并集外客户的 slack、或新的动态信用；不能再把零实际 regret 当作无损重选证据，也不能把形式 factor-two 策略当作 SPE。所有文档和哈希已保全；本批未执行 Git commit、push 或 `clean done`。
