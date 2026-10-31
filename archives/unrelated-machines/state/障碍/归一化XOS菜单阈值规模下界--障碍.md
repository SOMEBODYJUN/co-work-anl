---
id: "unrelated-machines/normalized-xos-threshold-menu-size"
kind: "obstruction"
type_tag: "障碍"
title: "归一化 XOS 菜单阈值规模下界"
status: "proved-with-scope-and-version-boundary"
summary: "同一资源宇宙、逐玩家非负归一化显式 XOS 若同时保持全部 t 集合值 1 与全部至多 floor(eta t) 集合值不超过 eta，则 indexed clause 数至少为 binom(2t,t)/binom(2t-r,t-r) 且至少 2^r；该障碍只针对全集合 unit/tiny 保真接口，不是一般 Santa Claus、UM 或 hardness 结论。"
source_refs:
  - "clean:1b969bd94717c6572e45"
  - "clean:3edd3c1c1176185ac70e"
  - "clean:a521e9e84c5c1249c770"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/normalized_xos_menu_threshold_size_exact_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/normalized_xos_menu_threshold_size_author_read_after_v2.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/normalized_xos_menu_threshold_size_canonical_read_after_v2.md"
---

# 对象身份、版本与证据层级

本页完整读取三份同一数学对象的冻结来源：独立 Exact v1、作者 Proof v2 read-after、canonical §4–6 read-after v2。三源都只讨论“在同一资源宇宙、逐玩家显式非负归一化 XOS 菜单中，同时保留全部 unit (t)-集和全部 tiny 集”的菜单规模；它们没有研究一般 Santa Claus/不相关机、source hardness 或全局 SC 值桥。

| clean ID | 原路径 | SHA-256 | 大小 | 实读层级 | 本页处置 |
|---|---|---|---:|---|---|
| `1b969bd94717c6572e45` | `history/source/notes/unrelated_machines/normalized_xos_menu_threshold_size_exact_v1.md` | `f10774625ddc30e09db98088a8c4cee579da027c8ae2512f6baba3ed5203bb44` | 2,992 B | 独立精确陈述，无作者证明 | 保存为主对象、量词和边界 |
| `3edd3c1c1176185ac70e` | `history/source/notes/unrelated_machines/normalized_xos_menu_threshold_size_author_read_after_v2.md` | `a00b5d40f88915754f2aa1e021997ceb2784a35e68518d218d6f00367fd926e3` | 3,157 B | 作者 Proof v2 实际 read-after；与独立推导逐项核对 | 记录作者证明的条件和退化点，结论为有效但未作软件枚举 |
| `a521e9e84c5c1249c770` | `history/source/notes/unrelated_machines/normalized_xos_menu_threshold_size_canonical_read_after_v2.md` | `83739c8d639ce808977741c0fcb2b366b183cb3be137fc3e80da9400edf62569` | 4,638 B | canonical 全文实际 read-after，但认证范围仅 §4–6 | 保存其精度修正和明确排除范围，不把 §1–3 SC 值桥带入 |

原件导出、manifest 和哈希复核位于 `archives/unrelated-machines/tools/evidence/normalized-xos-menu-threshold-20261031/`。

# 精确模型与量词

固定有理常数 (0<\eta<1)，取整数 (t\ge1)，资源宇宙 (U) 有 (2t) 个不同资源。令

\[
 d=\lfloor\eta t\rfloor,\qquad r=d+1.
\]

因此 (0\le d\le t-1)、(1\le r\le t)；特别是 \(\eta t<1\) 时 (d=0,r=1)，不应把退化情形误写为需要两个资源。

显式菜单有 (K\ge1) 个 indexed 加性 clauses，系数 (w_{s,u}\in\mathbb Q_{\ge0}) 满足每个 clause 在**整个** (U) 上总量恰为一：

\[
 \sum_{u\in U}w_{s,u}=1,\qquad
 f(B)=\max_{s\in[K]}\sum_{u\in B}w_{s,u}.
\]

允许零系数和重复 indexed clauses。需要同时满足两个逐集合条件：

1. 对每个 (T\subseteq U) 且 (|T|=t)，有 (f(T)=1)（全部 unit (t)-sets）；
2. 对每个 (B\subseteq U) 且 (|B|\le d)，有 (f(B)\le\eta)（全部 tiny sets）。

这些量词作用于整个资源宇宙，不是只对某个 reachable bundle、某个实际 allocation 或某个抽样集合成立。归一化是 clause 级总和恰为一；它不允许把额外资源、额外玩家、全局耦合或另一种隐式表示悄悄塞入同一接口。

# 精确规模定理

对任何满足上面条件的菜单，

\[
 K\ \ge\ \frac{\binom{2t}{t}}{\binom{2t-r}{t-r}}\ \ge\ 2^r. \tag{1}
\]

这里的第一项来自每个 (t)-set 必须包含某个 clause 的正 support，第二项是所有 (r)-子集的基本计数界。重复 clause、零系数和额外冗余全零 clause 都不能降低由非零归一化 clauses 产生的下界。

对固定正 \(\eta\)，有 (r\ge\lfloor\eta t\rfloor+1)，故随着显式资源数 (2t) 增长，(K\ge2^{\lfloor\eta t\rfloor+1})。这排除同一宇宙上的普适显式多项式大小归一化 shortcut。若 \(\eta\) 随输入变化，则指数常数也变化；来源没有声称统一的固定多项式分母。

## 1. 支撑包含与 (K\)-family 等价

由于 clause 系数非负且总和为一，对任意 (t)-set (T)，(f(T)=1) 意味着存在一个 clause (s) 的全部正 support 包含于 (T)。否则该 clause 在 (T) 上遗漏至少一个正系数，值严格小于一；所有 clauses 都如此则最大值不可能为一。

若某个 clause 的正 support 大小 (h\le d)，则 tiny 条件直接给 (h)-support 的 clause 值一，违反 (f(B)\le\eta<1)。因此每个能见证 unit set 的 clause 有 (h\ge r=d+1)。从每个 clause support 任取一个 (r)-子集，得到一个 (r)-family。所有 (t)-set 都必须包含该 family 中至少一个 (r)-集；否则其不包含任何 clause 的完整 support，不能满足 unit 值一。

反向地，给定一个覆盖全部 (t)-sets 的 (r)-family，每个 (r)-集上均匀置质量 (1/r) 的 clause，即得一个归一化 XOS 菜单：包含该 (r)-集的 (t)-set 值一，任意至多 (d)-set 的任一 clause 值至多 (d/r\le d/\lceil d/\eta\rceil\le\eta)。因此最小菜单数等于相应 covering family 的最小大小；来源用 (\Theta\) 记号时没有把它误称为短输入可计算的 oracle。

## 2. 计数下界

一个固定 (r)-集恰好包含

\[
 \binom{2t-r}{t-r}
\]

个 (t)-集。所有 (t)-集数为 \(\binom{2t}{t}\)。即使不同 (r)-集覆盖完全不重叠，仍需至少

\[
 \frac{\binom{2t}{t}}{\binom{2t-r}{t-r}}
\]

个。重叠只会减少有效覆盖数，不能改善下界；来源没有把该比值声称为所有参数都可达到的精确值。

由于每个 (r)-集的每个 (t)-superset 都被一条 unit 覆盖，亦有基本指数界 (K\ge2^r)（来源 Exact/Proof 版本均保留该边界）。当 (d=0) 时，单项 support 必须 hit 全部 (t)-sets，等价于其补集至多 (t-1)，最少需要 (t+1) 个 singleton clauses；(t=1) 时正确值为二。若 \(\eta t\) 是正整数，(r=t)，每个 (t)-set 只能由自身覆盖，最少需要 \(\binom{2t}{t}\) 个 clauses；其均匀 clause 在 support 内任意至多 (d) 项上的和达到上界 (d/t=\eta)，允许 low 条件的等号。

## 3. 锐点、浮动余数与输入规模

对 (d\ge1)，令 (k=\lceil d/\eta\rceil)（canonical 版本写为 (k=\max(1,\lceil d/\eta\rceil)) 以覆盖 (d=0)）。由于 support 大小小于等于 (d) 已排除，取 clause 中最重的 (d) 项，其质量至少为 (d/h)。tiny 条件迫使 (h\ge\lceil d/\eta\rceil=k)。结合 (h\le t)，有

\[
 t-k=\left\lfloor\frac{\{\eta t\}}{\eta}\right\rfloor
 \le\lceil1/\eta\rceil-1,
\]

边界 \(1/\eta\in\mathbb Z) 时余数严格小于一，恰好给出减一。于是覆盖分母至多为 \((2t)^c\)，而中央二项式满足 \(\binom{2t}{t}\ge4^t/(2t+1))，得到固定 \(\eta) 时的指数增长。来源还指出，一名加性玩家若有 (2t) 个资源、每项原值 (1/t)，输入长度仅 (O(t\log(t+1)))，但同一宇宙的显式归一化菜单仍需指数多个 indexed supports；这不是 (2^{\Omega(\text{source total bit length})}) 的更强断言，也不适用于变化的 \(\eta) 而不重算常数。

# 三源比较与数学边界

| 内容 | 1b969 Exact v1 | 3edd 作者 Proof v2 read-after | a521 canonical §4–6 read-after v2 | 处置 |
|---|---|---|---|---|
| 模型、unit/tiny 全量词 | 精确给出 | 逐项确认 support、(d=0)、重复 clauses | 再核对全部集合而非 reachable bundles | 保留为定理前提 |
| (K\) 的 covering/计数下界 | 给出完整结论 | 说明一般 ratio 仅为下界，不声称总可达 | 核对 (\binom{2t-k}{t-k}) 和中心项 | 标为已证明有限对象 |
| (d=0)、(\eta t\in\mathbb Z) 边界 | 给出退化说明 | 确认 (t+1) 与中央二项式端点 | 重新核对 low 条件允许等号 | 作为精确边界保留 |
| 版本/精度 | v1 独立陈述 | 作者 Proof v2 与独立推导一致，无 fatal | canonical 首稿措辞曾把 uniform 质量写成等式，后来修为“至多 (d/t)，support 内达到”；最终 v2 已重读 | 仅认证 canonical §4–6，记录修正 |
| 额外对象 | 不含 | 明确排除额外资源/玩家、全局耦合、隐式表示 | 明确不认证 §1–3 SC 值桥 | 不扩张用途 |

作者 Proof v2 的结论“有效”来自来源中的逐项 read-after 记录，不等同于本轮运行程序或第三方外审。canonical v2 的整文件哈希仅作读取字节标识；数学认证范围仍限于其 §4–6，不能把 source 中未审查的 §1–3 迁入本页。

# 与现有 XOS/NSW 资料的关系

本障碍与 `显式XOS分数NSW与确定性范围--资料.md` 的对象不同但相邻：后者给定有限 clause-list 后研究分数 NSW rematching 与未实现的确定性舍入；本页证明某类**从短逐玩家加性描述直接生成同宇宙、全 unit/tiny 保真的显式 clause-list** 不可能保持多项式大小。它不能反向否定显式 XOS NSW 算法，也不能将 NSW 的 (1/1{,}125{,}000) 规格改写成 menu-size hardness。

特别要保留以下开放接口：

- 允许额外资源或额外玩家的全局归约，不受本页计数直接阻断；
- 只在 reachable allocations 上保真、放宽全部 unit sets、允许 unit YES 损失，或使用未归一化 clauses/可证明的隐式表示，均是不同模型；
- 本页没有提供 normalized YES (V=1) / NO (V\le\eta) 的 hardness source，也没有证明一般 Santa Claus 或 UM 的 NP-hardness；
- canonical 的 SC 值桥引用仅是接口提示，本页规模证明不依赖其数值恒等式。

# 本轮实际处置

三源均完整实读，逐项比较定义域、量词、支撑包含、covering-family 方向、计数下界、退化参数、输入长度和版本修正；没有重复扫描同路径的其他副本。1b969 的独立定理、3edd 的作者 Proof v2 read-after 和 a521 的 canonical §4–6 read-after 各自独有内容均写入本页；canonical §1–3 未认证内容明确排除。没有脚本或有限实验需要运行，二进制转换不适用。原件、manifest 和哈希位于 evidence 目录；本页归档为障碍，不写入 papers，不改写主 near-two 结论。
