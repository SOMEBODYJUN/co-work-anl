---
id: "customer-attraction/weak-and-partitioned-matching-exact-audit"
kind: "computation"
type_tag: "计算"
title: "弱匹配与分区查询的精确核验"
status: "complete"
truth_status: "exact-algebra-and-fixed-policy-certificate; universal-bridge-open"
review_level: "本次全文实读六冻结源、全仓比较、Fraction 系数复核与有理对偶残差复核；无外部同行评审"
scope: "有限共同目录、单位客户、完整有序历史纯 SPE；冻结终局查询、分区一次收费和固定策略锥"
summary: "Q 的随机匹配恒等式、R 的超几何分区公式和一个固定 52 客户策略的有理对偶证书均精确成立；PFR-OPT-v1 及 A≤W 等一般支付桥仍未证明。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/weak_matching/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/weak_matching/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/weak_matching/algebra_audit.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-27557809587746c9eb07/weak_matching/algebra_audit.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/weak_matching/algebra_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/weak_matching/algebra_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/weak_matching/dual_probe.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/weak_matching/dual_probe.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/weak_matching/partitioned_queries.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/weak_matching/partitioned_queries.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/weak_matching/source_partition_dual.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/weak_matching/source_partition_dual.json"
---

# 弱匹配与分区查询的精确核验

## 对象和三个不同的查询量

采用共同目录完整历史模型：有限单位客户、有限非空共同主题目录，\(m\) 名单位提供者按完整有序历史行动；允许空主题、重复行动、零客户、离轨历史和任意平局。固定实际终局 \(S=(S_1,\ldots,S_m)\)，令 \(c_x\) 为客户 \(x\) 被实际终局覆盖的次数。固定一个长度为 \(m\) 的比较组合，比较主题作为有序出现次数保留，令 \(k_x\) 为出现次数、\(O\) 为其并集。三种量必须分开：

1. 冻结全主题查询 \(Q(\pi)\) 将每个比较主题的全部客户 incidences 分派给实际槽排列 \(\pi\)，重复出现重复收费：
   \[
   Q(\pi)=\sum_i\sum_{x\in T_{\pi(i)}}
      \frac{1}{c_x+1-\mathbf1_{x\in S_i}}.
   \]
2. 分区一次收费 \(R(\pi,P)\) 将每个比较出现 \(T_j\) 切成块 \(P_j\subseteq T_j\)，每名客户只留在第一次覆盖它的块；这是冻结账目，不是合法动作或真实后继。
3. 真实偏离收益 \(V\) 沿同一完整策略在改变前缀后的真实后继计算。它可因后继动作变化而与 \(Q\) 或 \(R\) 不同。

把三者混写会把静态后缀/一次收费桥误读成顺序 SPE 证明。既有《最优组合真实偏离匹配不足》已给 86 客户实例，其中真实 \(V\) 的两种最优组合指派均为 41，而遗漏最优客户数为 42；它否定的是普遍真实匹配接口，不是否定下面的静态恒等式或分区候选。

## 全主题冻结查询的精确恒等式

定义
\[
 A=\sum_x \frac{k_x}{c_x+1},\qquad
 D=\sum_{x:c_x=0}k_x,
\]
并令 \(B(\pi)\) 为被分派到实际覆盖槽时的修正项。对 \(c_x>0\)，某比较出现若匹配到覆盖 \(x\) 的槽，分母从 \(c_x+1\) 降为 \(c_x\)，每次修正为 \(1/[c_x(c_x+1)]\)。因此
\[
 Q(\pi)=A+B(\pi).
\]
均匀随机排列把一个比较出现送到 \(x\) 的 \(c_x\) 个覆盖槽之一的概率设为 \(c_x/m\)，从而
\[
 \mathbb E_\pi B(\pi)=\frac{A-D}{m},\qquad
 \min_\pi Q(\pi)\le \frac{m+1}{m}A-\frac{D}{m}.
\]
这给出一个明确的条件：若某个最优长度-\(m\) 比较组合满足 \(A\le W+D/(m+1)\)，则存在排列使 \(Q\le(1+1/m)W\)。若再有静态客户账目
\[
 \operatorname{OPT}_m\le Q+(1-1/m)W,
\]
便得到 \(\operatorname{OPT}_m\le2W\)。两条不等式都不是完整 SPE 的普遍结论；特别是 \(A\le W\) 的添加查询桥在来源中仍标为开放。

## 分区一次收费与超几何公式

给定排列 \(\pi\)，每个客户在所有覆盖它的比较出现中选最便宜的冻结份额，且每个客户只计一次。令比较出现含 \(x\) 的次数为 \(k_x\)，实际覆盖次数为 \(c_x\)。则
\[
 R(\pi)=|O\setminus C|+\sum_{x\in O\cap C}
 \left(\frac{1}{c_x+1}+
 \frac{\mathbf 1\{\text{所有含 }x\text{ 的比较出现均被分派到实际含 }x\text{ 的槽}\}}
 {c_x(c_x+1)}\right).
\]
当 \(c_x=0\) 时该客户贡献 1；当事件不成立时至少有一个比较出现落在不含 \(x\) 的槽，最小分母为 \(c_x+1\)；事件成立时所有候选份额为 \(1/c_x\)，产生上式修正。事件在 \(k_x>c_x\) 时自动不可能。

对均匀随机排列，\(k_x\) 个出现落入 \(m\) 个槽的均匀子集，故
\[
 \mathbb E R=|O\setminus C|+\sum_{x\in O\cap C}
 \left(\frac{1}{c_x+1}+
 \frac{\binom{c_x}{k_x}}{\binom{m}{k_x}c_x(c_x+1)}\right),
\]
其中 \(\binom{c_x}{k_x}=0\)（当 \(k_x>c_x\)）。这和 \(Q\) 的重复收费是不同对象。

来源提出候选 PFR-OPT-v1：每份完整历史纯 SPE 都存在达到 \(\operatorname{OPT}_m\) 的比较组合和排列，使 \(R\le W\)。该候选仍开放。若成立，则遗漏客户贡献 1、已覆盖客户贡献至少 \(1/m\)，给出
\[
 \operatorname{OPT}_m\le(2-1/m)W;
\]
也可用逐客户 \(1/(c_x+1)\) 下界得到
\[
 \operatorname{OPT}_m\le W+\sum_{x:c_x>0}\frac{c_x}{c_x+1}.
\]
来源中的尖锐族（主题 0 有 \(m\) 个私有客户，其余 \(m-1\) 个主题各有 1 个私有客户，所有玩家选主题 0）给 \(W=m,\operatorname{OPT}=2m-1,R=m\)，所以候选不可能统一加强为 \(R<(1-\varepsilon)W\)。

## 精确审计和固定策略锥证书

本次从冻结源导出并全文读取 algebra_audit.py、其 JSON 和 dual_probe.py；对不依赖原研究树的系数部分用 Fraction 独立重算，\(m=1,\ldots,5\) 共 1302 个 (actual incidence, comparison incidence) 组合全部通过恒等式、超几何期望和 \(\min R\ge1/m\) 断言。冻结 algebra_audit.json 的 52 客户固定策略输出为：

| 项 | 精确值 |
|---|---:|
| 完整 SPE 有序历史 | 259 |
| 完整 SPE 比较数 | 1295 |
| \(A\) | \(611/15\) |
| \(D\) | \(10\) |
| \(W\) | \(47\) |
| \(\min Q\) | \(48\) |
| \(\mathbb E Q\) | \(581/12\) |
| \(\min R\) | \(263/12\) |
| \(\mathbb E R\) | \(815/36\) |

独立读取 source_partition_dual.json 并用 Fraction 重核 63 个 residual：最小值为 0，全部非负；target=(0,1,4,5)，actual=(3,3,2,2)，
\[
 R_{(4,5,0,1)}\le \frac{281295}{345586}W
\]
对所有使这份固定策略仍为 SPE 且使该 target 弱最优的非负客户重数成立。此是固定策略/固定匹配证书，没有最优性乘子，不能提升为所有实例、所有完整 SPE 或六人 half 结论。

旧 52 客户固定策略的强全主题冻结查询最低值 48 大于 \(W=47\)，而分区一次收费最低值 \(263/12\) 小于 \(W\)；这正是“整主题 \(Q\)”与“重复去除后的 \(R\)”不能互换的精确边界。既有无环真实替换引理的 \(R_{\rm first}=277/12\)、真实预算 \(140/3\)、\(W=47\) 与这里一致而对象不同；不要把分区证书当作真实后继支付。

来源中有限数值搜索（p6m4：196 个策略、588 个策略/目标对；p7m5：99 个策略、297 个策略/目标对）均未找到浮点分离，但搜索不是全量策略枚举；浮点点不构成精确 SPE 或一般不存在性证明。

## 处置与接续

六个来源共同写入本对象：README 提供量词分层与开放状态，partitioned_queries 给出分区公式和有限搜索范围，algebra_audit.py/JSON 给出 1302 组合与 52 客户数值，dual_probe.py 及其 JSON 给出固定策略有理对偶。它们与现有无环引理、86 客户真实匹配反例、循环污染/补位核对象按“条件推导—固定证书—普遍存在性缺口”关系接续。

不能从本批推出：一般 \(A\le W\)、一般 PFR-OPT-v1、六人 Q-CAG-HALF，或真实 \(V\) 的静态替代。后续若要推进，必须同时处理：最优组合选择、完整有序历史的真实后继、任意重复/空主题和平局，以及把有限浮点搜索转成全量有理证书。
