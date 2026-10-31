---
id: um-normalized-xos-threshold-menu-size-obstruction-v2-source-review
kind: source-review
type_tag: semantic-review
title: 同宇宙归一化 XOS 阈值菜单最小规模（Exact v2）来源清洗
status: integrated-candidate
summary: 完整读取 Exact v2；其有限组合恒等式、两个锐端点和固定 eta 的输出规模界与现行正文一致，范围严格限于同资源宇宙、逐玩家、非负 norm-1 显式 clauses。
source_refs:
  - source:a4946858cc8b88c116a5:history/source/notes/unrelated_machines/normalized_xos_menu_threshold_size_exact_v2.md
  - sha256:6208afa100822520502e368c1cf3814d6d5bd520e3fdaec363efc33961eb2d3d
  - object:UM-NORMALIZED-XOS-THRESHOLD-MENU-SIZE-OBSTRUCTION-v2
---

# 清洗结论

本次用 `clean show a4946858cc8b88c116a5` 完整读取了 3155 字节、44 行的冻结原件；原件 SHA-256 为 `6208afa100822520502e368c1cf3814d6d5bd520e3fdaec363efc33961eb2d3d`。来源是 `UM-NORMALIZED-XOS-THRESHOLD-MENU-SIZE-OBSTRUCTION-v2` 的 Exact-only 陈述，明确要求把它和 v1、作者 Proof、其它审查及同档的 SC 值桥分开保存。它不是运行日志，也没有软件或枚举输出。

来源的独有内容是把 v1 的 `r=d+1` 支撑下界提升为精确的有限组合量 `K_min=Theta(2t,t,k)`，并明确列出 `d=0` 与 `eta t` 为正整数时的真正锐端点。该内容已经由现行对象“归一化菜单的 Santa Claus 精确值桥与状态数量锐界”的第 4–6 节承接；本来源应以 `integrated` 处置，原始字节仍在 evidence 中保留，不能只用现行正文替代来源指纹。

## 模型和量词

参数为有理 `0<eta<1`、整数 `t>=1`，资源宇宙 `U` 有 `2t` 个显式资源。令

\[
d=\lfloor eta t\rfloor,\qquad k=\max\{1,\lceil d/eta\rceil\}.
\]

因此 `0<=d<t` 且 `1<=k<=t`。菜单有 `K>=1` 个 indexed additive clauses；每个 clause 的系数在 `U` 上非负、有理、总和恰为 1，允许零系数和重复 indexed clauses。令

\[
f(B)=\max_s\sum_{u\in B}w_{s,u}.
\]

承重条件是全量词：每个 `|T|=t` 的集合有 `f(T)=1`，每个 `|B|<=d` 的集合有 `f(B)<=eta`。`K_min` 是固定参数下满足这两个条件的最小 indexed clause 数；来源没有声称求 `K_min` 的算法复杂度。

## 独有数学结论及推导

对任意 clause，记严格正支撑大小为 `h`。若 `d>=1` 且 `h<=d`，取 `B` 为整个支撑，则该 clause 在 `B` 上质量为 1，违反 `f(B)<=eta<1`。若从支撑取权重最大的 `d` 项，则它们的总质量至少为 `d/h`，而小集合条件把它限制为 `eta`；故 `h>=ceil(d/eta)=k`。`d=0` 时 norm-1 直接给出非空支撑，仍有 `h>=1=k`。这一步使用了非负性、逐 clause 恰 norm-1 和全部小集合量词。

令 `Theta(2t,t,k)` 为最小 family `F`（`F` 是 `k`-子集的集合），使每个 `t`-子集 `T` 都包含某个 `F`。这里方向是“大集合含一个指定小集合”，不能误称相反方向的 covering design。

给定任一可行菜单，对每个 clause 的支撑任选一个 `k`-子集并在其上均匀赋权 `1/k`。因为每个 unit `T` 上的有限最大值等于 1，某个 clause 在 `T` 上的质量恰为 1；非负且总和为 1 强迫其整个支撑包含在 `T`，所以抽出的 `k`-子集也包含在 `T`。替换后的菜单仍使每个 unit 集合值为 1，而任意 `|B|<=d` 的新 clause 值至多 `d/k<=eta`。去除重复 `k`-子集后得到大小不增的 family，因此 `Theta<=K`。

反向地，任何满足“每个 `t`-集包含一个 family 成员”的 `k`-子集 family，在每个成员上取均匀权 `1/k`，就同时满足两个阈值条件。因此

\[
K_{\min}=\Theta(2t,t,k).
\]

固定的 `k`-子集恰被 `binom(2t-k,t-k)` 个 `t`-子集包含；并集计数给出

\[
K\ge\frac{\binom{2t}{t}}{\binom{2t-k}{t-k}}.
\]

该比值是下界，不被来源声称对所有参数都达到。

## 两个精确锐端点和增长界

当 `d=0` 时 `k=1`。family 是一组 singletons；每个 `t`-集必须命中所选点，等价于未选点不能再组成 `t`-集。因此恰需 `t+1` 个 clauses，包含 `t=1` 时的 `K_min=2`。

当 `eta t` 是正整数时，`d=eta t`、`k=t`。一个 `t`-集只能包含自身作为 `t`-子集，所以必须列出全部 `binom(2t,t)` 个 `t`-集；每个集上的均匀 clause 达到该值。固定有理 `eta=p/q` 时，`t` 取 `q` 的正倍数给出这条锐端点。

固定 `eta` 且 `d>=1`，写 `r=eta t-d`，则 `0<=r<1`，并有 `t-k=floor(r/eta)<=c`，其中 `c=ceil(1/eta)-1`。于是

\[
K\ge\frac{\binom{2t}{t}}{(2t)^c}
\ge\frac{4^t}{(2t+1)(2t)^c}.
\]

同一资源宇宙中的单个 additive 玩家（每个资源值 `1/t`）只需显式列出 `2t` 个资源和这些有理值，编码长度为 `O(t log(t+1))`；所以固定 `eta` 下，保持该全量词接口的显式逐玩家 norm-1 菜单需超多项式输出。这个比较是按资源参数的输出规模，不能改写成 `2^{Omega(源总位长)}`；当 `eta` 随输入变化时，常数 `c` 也不固定。

## 全仓比较和边界

* 与 v1 Exact、v1 Proof、v1 independent review 比较：v1 只给 `r=d+1` 的支撑/覆盖下界，未给 `Theta` 恒等式或两个锐端点；v1 的“固定 eta 指数”不能代替 v2 的 exact-support 强化。
* 与 v2 Exact-first independent review 比较：该审查只读 v2 Exact，独立重构确认支持下界、均匀化、family 方向、`d=0`、`eta t` 整数端点和固定 `eta` 规模界均无 fatal；没有软件枚举或外审声明。
* 与现行正文及综合范围审查比较：正文只认证同资源宇宙、非负、逐 clause norm-1、有限显式 max、全部 `t`-集和全部至多 `d`-集阈值。SC 值桥是同档另一个对象，不能把本来源读成一般 Santa Claus/UM 困难性或全局归约不可能性。
* 支撑均匀化只保持两个阈值合同，不声称新函数在所有中间子集上逐点不大于原 `f`。辅助资源/玩家、全局耦合、只保可达集合、放松 unit completeness、未归一化 clauses 或另证可处理的隐式表示，均不在本障碍范围内。

## 建议处置

`integrated`。正式数学去向为现行对象 `UM-NORMALIZED-XOS-THRESHOLD-MENU-SIZE-OBSTRUCTION-v2`（现行正文第 4–6 节），证据去向为 `archives/unrelated-machines/tools/evidence/normalized-xos-threshold-20261031/` 的源 manifest/原件副本；不要新建与现行对象重复的定理。逐源回执应说明：完整读取原件；对比 v1、v2 独立审查和现行对象；独有内容是 `Theta` 精确表示、两个锐端点和固定 `eta` 输出界；保留的限制是不扩展至一般 hardness 或全局归约。
