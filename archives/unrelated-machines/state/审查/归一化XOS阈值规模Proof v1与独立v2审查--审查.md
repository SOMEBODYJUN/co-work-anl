---
id: unrelated-machines/normalized-xos-threshold-proof-v1-and-independent-v2-review
kind: review
type_tag: 审查
title: 归一化XOS阈值规模Proof v1与独立v2审查
status: version-read-integrated-with-exact-boundary
truth_status: normalized-xos-menu-size-obstruction-reconciled-r-strengthened
review_level: full-proof-v1-and-independent-v2-read-comparison
scope: UM-NORMALIZED-XOS-THRESHOLD-MENU-SIZE-OBSTRUCTION versions Proof v1 and Exact-first independent v2
summary: 完整实读作者Proof v1与独立Exact-first v2，和已有Exact v1、作者/canonical read-after、障碍对象逐项比较。Proof v1正确给r=d+1的support/cover计数；独立v2强化为k=max(1,ceil(d/eta))并给Theta(2t,t,k)精确family等价、端点和4^t/poly界。两者均只适用同一资源宇宙、norm1、全部unit/tiny集合的显式菜单接口。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/notes/unrelated_machines/normalized_xos_menu_threshold_size_proof_v1.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/notes/unrelated_machines/normalized_xos_menu_threshold_size_proof_v1.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/notes/unrelated_machines/normalized_xos_menu_threshold_size_independent_review_v2.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/notes/unrelated_machines/normalized_xos_menu_threshold_size_independent_review_v2.md
related_objects:
  - ../障碍/归一化XOS菜单阈值规模下界--障碍.md
  - ../审查/归一化XOS阈值规模独立Exact审查续页--审查.md
  - ../审查/规范化平菜单v1v3的独立与作者核验--审查.md
  - ../定理/分数重匹配与归一化XOS稳健缺口边界--定理.md

# 归一化 XOS 阈值规模 Proof v1 与独立 v2 审查

## 来源身份和读取范围

作者 Proof v1 大小3,167字节，SHA-256 ff9fa6969168077ac7d43aea711daa31054ec6d393100b6d908ff92dd6bfd88b；独立 Exact-first v2 大小6,500字节，SHA-256 8cf66cfa4c3845080d3323053bedb07d87922f42b03f8094c2c30931d8a6cc5c。两个版本在 legacy-cleanup 与 main 内容相同。本批完整实读 Proof v1 与独立 v2，并与已有 Exact v1、作者/canonical read-after 和正式障碍对象逐项比较。

它们共同研究同一接口：资源宇宙 U 大小 2t，显式有限 indexed XOS clauses，每个 clause 非负且在整个 U 上总量恰为1；每个 t-subset 的值恰为1，每个大小至多 d=floor(eta t) 的 subset 值至多 eta。这些是全资源宇宙的量词，不是 reachable bundle、实际 allocation 或抽样域。

## Proof v1：support/cover 计数完整性

作者 Proof v1 的每个正 support S_s 非空。若 |S_s|<=d，取 B=S_s，该 clause 在 B 上值1，违反 tiny 上界；故 |S_s|>=r=d+1，且 d=0 时只使用 support 非空，不错误要求 support至少2。

每个 unit t-set T 的 max 值1必须由某个 clause 达到；由于系数非负且 clause 总量恰1，该 clause 的正 support必须包含于T。一个 support 大小k覆盖的t-sets至多 C(2t-k,t-k) 个，于是
\[
K\ge\frac{\binom{2t}{t}}{\binom{2t-r}{t-r}}\ge2^r.
\]
因子分解
\[
\frac{\binom{2t}{t}}{\binom{2t-r}{t-r}}
=\prod_{j=0}^{r-1}\frac{2t-j}{t-j}\ge2^r
\]
合法；Proof v1 还正确处理 t=1、d=0、零系数、重复 clause、显式输入长度和一个逐t-set均匀 clause的非空性。它没有声称覆盖比值对全部参数达到，也没有推出 Santa Claus/UM hardness、source-NO解码或变化eta的统一指数常数。

## Independent v2：support strengthening 与 exact family

独立 v2 在不读取旧 Proof 的情况下重新构造。设正 support 大小为 L。若 L<=d 仍直接违反 tiny 条件；若 L>d，取 support 中权最大的 d 项，质量至少为 d/L。tiny 上界给
\[
d/L\le\eta,\qquad L\ge d/\eta,\qquad L\ge k=\max(1,\lceil d/\eta\rceil).
\]
这比 Proof v1 的 r=d+1 可能更强，且保留 eta t 为整数时 k=t 的等号。

v2 进一步对每个 clause 抽取任意 k-subset F_s 并均匀放置 1/k。每个 unit t-set 原本由某个 clause 的整个 support 包含，因此也包含 F_s；每个 tiny set 的新值至多 d/k<=eta。于是可行菜单等价于一个 k-subset family，使全部 t-subsets各自包含至少一个 family member：
\[
K_{\min}=\Theta(2t,t,k).
\]
该 family 等价只保持 unit/tiny 合同，不保持原 XOS 在中间大小 bundles 的完整函数值，也不声称最小 family 可多项式求出。覆盖计数给
\[
K\ge\frac{\binom{2t}{t}}{\binom{2t-k}{t-k}}.
\]

v2 精确处理两个端点：d=0、k=1 时 K_min=t+1（t=1时为2）；eta t为正整数时 k=t、每个t-set必须自身出现，K_min=binom(2t,t)。固定eta时 t-k有常数上界，因中央二项式得到 4^t/poly_eta(t) 下界；输入一个玩家的2t资源、每项1/t只有O(t log t)位，但显式菜单仍需指数indexed clauses。eta随输入变化时不宣称同一固定指数常数。

## 版本关系、修正和边界

Proof v1 的 r=d+1 结论是 v2 k强化的较弱但正确推论；不应把两个 r,k 记号混为同一个最优下界。已有独立 Exact v1/author/canonical read-after和正式障碍对象已经保存 v1合同与canonical §4–6精度修正。本对象补充作者 Proof v1 的逐步证明、独立 v2 的 exact family 等价、k强化、d=0/整数端点和4^t/poly输入解释。

两版本都明确不处理额外资源/玩家、全局耦合、只保 reachable bundles、放宽 unit completeness、未归一化 clauses、隐式可处理表示、一般 Santa Claus/UM hardness 或 normalized YES/NO source。其规模障碍不反向否定显式XOS的rematching/NSW算法，也不自动推出一般UM困难性。

## 处置

两源均 integrated 到本版本审查；正式数学主对象仍为归一化XOS菜单阈值规模下界，已有Exact v1 independent review继续作为独立proof provenance。没有运行新程序、没有外部同行评议或新颖性认证；第三阶段可标作者Proof、independent Exact、canonical read-after、版本强化和范围边界，不能重复造一般不可能性对象。

