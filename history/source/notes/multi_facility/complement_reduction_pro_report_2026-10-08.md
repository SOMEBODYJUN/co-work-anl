# 来源留存：2026-10-08 共单例搜索归约附稿

来源为本次会话提供的完整 Markdown 附件；以下保留正文与内嵌代码。
原始附件 SHA-256：`b8b8d9bb47bb8b3670f22eba50b991e07660def0527fccd18b3eb1f5a4445a2e`。

正文链接的 ZIP、单独源码和报告未取得；来源自报审计次数不作为本仓库证据。
本仓库的新证明、规范实现、实际审计和适用边界另行登记。

---

**本轮证明了一条新的、保持原地点设施重数的位多项式搜索归约：即使所有合法分配都满足完整盒、所有可移动客户都严格满足** **`(H)`****、归位修复一次也不会触发，原题仍可精确包含任意异权、二选一、两种速度的相关机纯 NE 搜索。** 更一般地，归约保留一类加权共单例拥塞博弈的全部 NE、严格改善边和指定规则的完整运行。

**这不是你要求的一般 NE 求解器；一般异权的统一位多项式构造仍未完成。** 新结果的实质是：它不再依赖上一轮 `(E)` 中的微扰或设施数放大，并把仓库原来的“相关机公式不能直接替换”推进为一个正确、可执行、具有完整总成本证明的搜索接口。

本轮核实到的公开 `main` 为 `38a94423f625684eafdd046982e8d88a83035676`，并按固定 SHA 读取了交接材料。Git 克隆仍因 DNS 失败未完成，远端未修改。该版本仍将一般输入的总运行时间列为待闭合项。([GitHub](https://github.com/SOMEBODYJUN/co-work-anl/commit/main.patch?audit=20261008 "https://github.com/SOMEBODYJUN/co-work-anl/commit/main.patch?audit=20261008"))

## 一、源问题与新定理

先定义归约的源游戏，避免把两种 NE 条件混用。

有 `m\ge1` 个资源，正整数速度 `q_t`，非负有理背景负载 `B_t`。客户 `i` 的权重为任意正有理数 `u_i`，允许集合为非空 `A_i`。

客户选择一个**排除地点** `a_i\in A_i`，实际使用其余资源 `A_i\setminus\{a_i\}`。资源负载和客户成本为

```math
Y_t(a)=B_t+\sum_{\substack{i:t\in A_i\\a_i\ne t}}u_i, \qquad C_i(a)=\sum_{t\in A_i\setminus\{a_i\}}\frac{Y_t(a)}{q_t}.
```

若客户从排除 `s` 改为排除 `t\ne s`，它开始使用 `s`、停止使用 `t`，其余使用情况不变。因此

```math
\boxed{ C_i(a^{i\to t})-C_i(a) = \frac{Y_s(a)+u_i}{q_s}-\frac{Y_t(a)}{q_t}. } \tag{1}
```

当每个 `A_i` 恰有两个元素时，客户实际只使用其中一个资源，**这就是通常的二选一相关机游戏**。解码成所选机器时，应取 `A_i\setminus\{a_i\}` 的唯一元素，而不是 `a_i`。

### 新定理

给定上述源实例和任意正有理数

```math
0<\eta\le\frac12,
```

可以构造一个符合原模型的真实共同目录设施实例，使得：

原地点的贪心设施重数恰为原来的 `q_t`，另外只增加一个独立地点及一家设施；最后插入得分为 `\gamma=1`。对源客户的**每个合法分配**，对应目标分配均满足完整盒与严格 `(H)`，并且每条单客户偏离的成本差都乘以同一个正常数。因此，纯 NE 集和严格改善有向图精确对应。

这个归约的全部编译、真实贪心执行和解码成本，均是显式客户、关联、设施及有理数编码长度的多项式。特别地，源速度只取 `1,2` 时，目标设施数

```math
k=1+\sum_tq_t\le2m+1,
```

所以在通常的源输入位长下也是多项式归约。

下面给出证明。

## 二、直接构造真实规范贪心实例

记

```math
T=\sum_i u_i,\qquad Q=\max_tq_t,\qquad M=\max_tB_t+T+1,
```

```math
\delta=\frac{\eta}{QM}, \qquad T_t=\sum_{i:t\in A_i}u_i.
```

保留原来的 `m` 个地点。对每位源客户 `i`，建立一名权重

```math
w_i=\delta u_i
```

的原子客户，其覆盖地点恰为 `A_i`。

在每个地点 `t`，再添加一名仅由该地点覆盖的私有客户，权重为

```math
\boxed{ P_t=q_t+\delta(q_tM-B_t-T_t). } \tag{2}
```

最后添加独立地点 `z`，仅覆盖一名权重为 `1` 的私有客户，并取

```math
k=1+\sum_tq_t.
```

这只使用原模型允许的正权原子客户、任意覆盖子集和共同目录，没有增加入口费、客户特有延迟或硬容量。原模型的条件成本仍是客户自身权重加上其他客户在所选设施上的期望负载。([GitHub](https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/main/research/current/multi_facility/model.md "https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/main/research/current/multi_facility/model.md"))

### 1. 所有权重都严格合法

因为 `B_t+T_t\le M-1`，

```math
q_tM-B_t-T_t\ge(q_t-1)M+1\ge1.
```

所以

```math
P_t\ge q_t+\delta>q_t\ge1.
```

而移动客户满足

```math
0<w_i=\delta u_i<\delta M=\frac{\eta}{Q}\le\frac12<1.
```

甚至其**总权重**也满足

```math
\sum_iw_i=\delta T<\frac{\eta}{Q}.
```

因此，全部可移动客户的总重可以任意小，仍然保留后面的精确战略对应。

### 2. 贪心重数恰为 `q_t`，不需要微扰

规范贪心对已开地点使用固定首开客户池，对未开地点使用当前未覆盖总重。([GitHub](https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/38a94423f625684eafdd046982e8d88a83035676/research/current/multi_facility/greedy_box_global_progress.md "https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/38a94423f625684eafdd046982e8d88a83035676/research/current/multi_facility/greedy_box_global_progress.md"))

地点 `t` 首次开设时，设其可达源客户中已经在更早地点被覆盖的总源权重为 `F_t`。它的固定首开池为

```math
G_t=P_t+\delta(T_t-F_t) =q_t+\delta(q_tM-B_t-F_t).
```

由于 `0\le F_t\le T_t`，

```math
\boxed{ q_t+\delta\le G_t\le q_t+\eta<q_t+1. } \tag{3}
```

于是，地点 `t` 的前 `q_t` 次插入得分都大于 `1`，下一次得分小于 `1`。每个未开原地点的得分也大于 `1`，而独立地点 `z` 的得分恒为 `1`。

所以贪心必先在每个原地点完成恰好 `q_t` 次插入，最后开设 `z`：

```math
\boxed{ q_t^{\mathrm{greedy}}=q_t,\qquad q_z=1,\qquad\gamma=1. } \tag{4}
```

这个证明允许重数并列。

还要验证归属次序。若两个未开地点满足 `q_u>q_v`，则 `u` 的分数大于 `q_u`，而 `v` 的分数不超过

```math
q_v+\eta<q_v+1\le q_u.
```

因此首次开设按 `q` 非增序发生；同重数内使用实际首次开设次序，便得到合法的

```math
q_1\ge\cdots\ge q_m,\qquad h_i=\min A_i.
```

**原地点的设施重数完全没有放大，平局也没有被微扰消除。**

## 三、全状态完整盒、严格 `(H)` 与 NE 对应

### 1. 完整盒对所有分配成立

把源客户的排除地点 `a_i` 作为对应目标客户的分配地点。原地点 `t` 的实际负载为

```math
\begin{aligned} W_t(a) &=P_t+\sum_{a_i=t}\delta u_i\\ &=q_t+\delta(q_tM-Y_t(a)). \end{aligned}
```

所以

```math
\boxed{X_t(a)=W_t(a)-q_t=\delta(q_tM-Y_t(a)).} \tag{5}
```

由于 `0\le Y_t(a)\le M-1`，

```math
\boxed{ \delta\le X_t(a)\le\delta q_tM =\frac{\eta q_t}{Q}\le\eta\le\frac12. } \tag{6}
```

原来的 `m` 个地点在**所有分配中都严格位于盒内**。新增独立地点 `z` 恒有 `W_z=q_z\gamma=1`，位于下边界；它没有跨地点客户偏离。整个实际实例对每个分配都满足完整盒。

### 2. 所有移动客户在所有分配中严格满足 `(H)`

由式（6），

```math
\frac{X_t}{q_t}\le\frac{\eta}{Q}\le\frac1{2Q}.
```

同时 `w_i<1/2`、`q_{h_i}\le Q`，故

```math
\frac{1-w_i}{q_{h_i}}>\frac1{2Q}.
```

因此

```math
\boxed{ \frac{X_{a_i}-w_i}{q_{a_i}} < \frac{X_{a_i}}{q_{a_i}} \le\frac1{2Q} < \frac{1-w_i}{q_{h_i}}. } \tag{7}
```

这不是运行中的归纳不变量，而是**整个合法状态空间的性质**。

仓库归位操作只返回严格违反 `(H)` 的外来客户。因此，在这个嵌入族上，归位修复始终不会触发；改善过程的全部成本都来自严格改善本身。([GitHub](https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/38a94423f625684eafdd046982e8d88a83035676/research/current/multi_facility/greedy_box_global_progress.md "https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/38a94423f625684eafdd046982e8d88a83035676/research/current/multi_facility/greedy_box_global_progress.md"))

### 3. 全部客户偏离精确对应

客户 `i` 在目标中从 `s` 改去 `t\ne s`，其条件成本变化为

```math
\begin{aligned} \Delta_i^T &=\frac{W_t}{q_t} -\frac{W_s-\delta u_i}{q_s}\\ &=\delta\left( \frac{Y_s+u_i}{q_s}-\frac{Y_t}{q_t} \right)\\ &=\delta\bigl(C_i(a^{i\to t})-C_i(a)\bigr). \end{aligned} \tag{8}
```

因为 `\delta>0`，所有严格改善、严格劣化和相等偏离都保留。没有删去任何原始允许选项，也没有把“偏离后仍在盒内”作为 NE 检查条件。

私有客户仅能访问一个占用地点；该地点各设施的条件成本相同，所以站内独立均匀选择是其精确最佳响应。

因此

```math
\boxed{ \text{源纯 NE} \quad\longleftrightarrow\quad \text{目标完整盒内、站纯且站内独立均匀的精确 NE}. } \tag{9}
```

对应的是这类站纯输出，不是目标游戏中所有任意混合 NE。

### 4. 原精确势与规范运行也保留

定义源加权仿射精确势

```math
\Psi_G(a)= \sum_t \frac{Y_t(a)^2+ \sum_{i:t\in A_i,\ a_i\ne t}u_i^2}{2q_t}.
```

令

```math
K_t=\sum_{i:t\in A_i}u_i^2,\qquad Y_{\rm tot}=\sum_tB_t+\sum_i(|A_i|-1)u_i.
```

展开式（5），目标原精确势满足

```math
\boxed{ \Phi_T(a)=\delta^2\left[ \Psi_G(a)+\frac{M^2}{2}\sum_tq_t -MY_{\rm tot}-\frac12\sum_t\frac{K_t}{q_t} \right]. } \tag{10}
```

括号内除 `\Psi_G(a)` 外全部与分配无关。

此外，记 `Q_i=\max_{t\in A_i}q_t=q_{h_i}`。目标的最小 `(r_i,i)` 优先级

```math
r_i=\frac{1-\delta u_i}{Q_i}
```

恰好等于源优先级

```math
\boxed{(-Q_i,-u_i,i).} \tag{11}
```

同 `Q_i` 时这一点直接成立。若 `Q_i>Q_j`，则

```math
\frac{1-\eta/Q}{Q_j}-\frac1{Q_i} = \frac{Q_i-Q_j-\eta Q_i/Q}{Q_iQ_j} \ge\frac{1-\eta}{Q_iQ_j}>0,
```

从而 `r_i<r_j`。

又因为

```math
\frac{W_t}{q_t}=1+\delta M-\delta\frac{Y_t}{q_t},
```

目标的最小价格目的地，正是源的最大归一化负载排除地点。使用相同物理标签破平局后，**规范运行逐步对应，客户移动总数完全相同，没有归位微步**。

这里没有把任意预先指定的源初态都冒充贪心初态：初态由实际首次覆盖归属确定。每个二选项对恰含一台快机和一台慢机时，初始排除快机，源客户初始全在慢机，优先级为权重降序。

## 四、归约全过程的时间和数值位长

令

```math
E=\sum_i|A_i|,\qquad k=1+\sum_tq_t.
```

输出含 `n+m+1` 名客户、`m+1` 个地点、`E+m+1` 条覆盖关联，以及全部 `k` 个带标签设施坐标。

预先建立地点关联后，每次字面贪心插入使用 `O(E+m)` 次有理运算，且**恰好执行** **`k`** **次插入**。加上集合规范化、排序及数据输出，总算术成本为

```math
\boxed{ O\!\left(k(E+m)+E\log(m+1)+n+m\right). } \tag{12}
```

给定目标分配后的 NE 核验和源解码另需 `O(n+m+E)` 次有理运算。

原模型明确按显式设施输出收费；不能把这个关于 `k` 的界写成关于任意紧凑 `\log k` 的界。源速度只取 `1,2` 时，`k\le2m+1`，因此没有这个表示问题。([GitHub](https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/main/research/current/multi_facility/model.md "https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/main/research/current/multi_facility/model.md"))

### 显式共同分母

取源 `B_t,u_i` 分母的公倍数 `D`，写

```math
B_t=\frac{V_t}{D},\qquad u_i=\frac{U_i}{D},\qquad\eta=\frac ae.
```

令

```math
N=D+\max_tV_t+\sum_iU_i.
```

则

```math
M=\frac ND,\qquad \delta=\frac{aD}{eQN},
```

并且目标权重具有形式

```math
\boxed{ w_i=\frac{aU_i}{eQN},\qquad P_t=q_t+ \frac{a\left(q_tN-V_t-\sum_{i:t\in A_i}U_i\right)}{eQN}. } \tag{13}
```

所有目标权重共有分母 `eQN`。`\log D` 不超过输入分母位长之和，`\log N` 和 `\log(eQN)` 均有输入位长多项式界。池负载是这些数的显式有限和；插入分数再除以不超过 `k` 的整数，仅增加 `O(\log k)` 位。

因此式（12）确实是归约全过程的位多项式界。没有按 `D`、`N`、`1/\delta`、最小权重倒数或最小价格间隔倒数循环。

**这个时间证明只覆盖编译和解码。尚未提供的 NE 求解器，其成本不能被当作零或单位时间。**

## 五、一般输入还有一个精确的正向导入接口

上述嵌入说明一般算法必须处理什么。反过来，对任意原抽象输入，也可以把真正待解的任务完整转成一个**带输出负载区间的共单例 NE 问题**。

令

```math
b_t=c_t-\sum_{h_i=t}w_i,\qquad T_t=\sum_{i:t\in A_i}w_i,
```

```math
M=1+\max_t\frac{b_t+T_t}{q_t}, \qquad B_t=q_tM-b_t-T_t. \tag{14}
```

因为

```math
b_t+T_t =c_t+\sum_{\substack{i:t\in A_i\\h_i\ne t}}w_i\ge0,
```

所以 `M\ge1`，并且 `B_t\ge q_t>0`。

取源权重 `u_i=w_i`、相同允许集合，以排除 `a_i` 表示原分配，就有

```math
\boxed{Y_t(a)=q_tM-X_t(a).} \tag{15}
```

因此

```math
\frac{Y_s+w_i}{q_s}-\frac{Y_t}{q_t} = \frac{X_t}{q_t}-\frac{X_s-w_i}{q_s}, \tag{16}
```

而完整盒恰好变成

```math
\boxed{q_tM-1\le Y_t(a)\le q_tM.} \tag{17}
```

这给出一个覆盖一般输入的、位多项式可计算的替代合同：

> 从已知可行的最高速度排除初态 `h_i=\min A_i` 出发，构造满足式（17）的加权共单例纯 NE；全部原始偏离仍必须检查，包括会离开这些区间的偏离。

这个变换自身不展开 `q`，连二进制大重数的强化抽象输入也可直接处理。反向取

```math
c_t=q_tM-Y_t(h)
```

即可恢复合法抽象输入，所以这两个**带约束搜索表述**具有直接的位多项式双向变换。

**不能把“满足区间的源 NE”换成“任意无区间源 NE”。** 完整研究记录中给出了一个精确证书说明这一量词区别。这里也没有把输出区间变成博弈硬容量。

这与仓库此前否定的直接 `q=\text{速度}` 替换不同：旧替换缺少客户自重在源、目的之间的位置转换；本次使用策略取补、负载反向仿射变换和正私有客户实现，式（8）、（16）才是成立的接口。([GitHub](https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/main/research/current/multi_facility/restricted_related_link_boundary.md "https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/main/research/current/multi_facility/restricted_related_link_boundary.md"))

## 六、完整实现与核验

下面是完整编译器，**不是 NE 求解器**。它输出真实设施实例、实际规范贪心序列和合法抽象数据；`decode_ne` 核验另行提供的目标解并解码，`to_bounded_complement` 实现一般输入的式（14）—（17）。没有隐藏的指数枚举兜底。

两个独立精确审计合计完成了 **12,008 次分配检查、83,740 次有向客户偏离检查**，另有 **11,515 次实际带标签设施条件成本比较**。还逐步对照了规范运行。计数包含尺度和破平局复测，不是互不重叠实例数；有限核验验证实现，普遍结论依据上述证明。

```python
"""Exact polynomial search reduction, NOT a general boxed-NE solver.

Source: player i excludes one site a_i in A_i and uses all other sites in A_i;
site t has background B_t and latency (B_t + selected weight)/q_t.
Target: an actual common-catalog facility instance on its canonical greedy layout.
Site/client indices are zero-based. Rational inputs must not be floats.
Runtime counts the explicitly output sum(q)+1 labeled facilities.
"""
from __future__ import annotations
from fractions import Fraction as F
from typing import Any, Sequence


def rational(x: Any) -> F:
    if isinstance(x, bool) or not isinstance(x, (int, str, F)):
        raise ValueError("Use integers, Fraction, or rational strings, not floats.")
    try:
        return F(x)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("Invalid rational input.") from exc


def normalize(q, B, u, A):
    q, B, u = tuple(q), tuple(map(rational, B)), tuple(map(rational, u))
    if not q or len(B) != len(q) or len(A) != len(u):
        raise ValueError("Nonempty resource list and matching dimensions required.")
    if any(type(x) is not int or x < 1 for x in q):
        raise ValueError("Speeds must be positive integers.")
    if any(x < 0 for x in B) or any(x <= 0 for x in u):
        raise ValueError("Backgrounds must be nonnegative; weights positive.")
    rows = []
    for row in A:
        row = tuple(row)
        if not row or any(type(t) is not int or not 0 <= t < len(q) for t in row):
            raise ValueError("Invalid or empty allowed set.")
        rows.append(tuple(sorted(set(row))))
    return q, B, u, tuple(rows)


def canonical_greedy(weights, allowed, sites: int, k: int, *, reverse_ties=False):
    """Literal fixed-first-pool greedy; returns labeled insertion order and pools."""
    cover = [[] for _ in range(sites)]
    for i, row in enumerate(allowed):
        for t in row:
            cover[t].append(i)
    owner = [None] * len(weights)
    count, pool, layout, scores, opening = [0] * sites, [F(0)] * sites, [], [], []
    for _ in range(k):
        values = [pool[t] / (count[t] + 1) if count[t] else
                  sum((weights[i] for i in cover[t] if owner[i] is None), F(0))
                  for t in range(sites)]
        best = max(values)
        candidates = [t for t, value in enumerate(values) if value == best]
        t = candidates[-1] if reverse_ties else candidates[0]
        if not count[t]:
            opening.append(t)
            for i in cover[t]:
                if owner[i] is None:
                    owner[i] = t
                    pool[t] += weights[i]
        count[t] += 1
        layout.append(t)
        scores.append(best)
    return count, pool, owner, layout, scores, opening


def compile_game(q, B, u, A, eta="1/2", *, reverse_ties=False) -> dict:
    """Compile source data. All target assignments satisfy full box and strict H."""
    q, B, u, A = normalize(q, B, u, A)
    eta = rational(eta)
    if not 0 < eta <= F(1, 2):
        raise ValueError("eta must lie in (0,1/2].")
    m, n, Q = len(q), len(u), max(q)
    M = max(B) + sum(u, F(0)) + 1
    delta = eta / (Q * M)
    eligible = [F(0)] * m
    for i, row in enumerate(A):
        for t in row:
            eligible[t] += u[i]
    private = [q[t] + delta * (q[t] * M - B[t] - eligible[t]) for t in range(m)]
    weights = [delta * x for x in u] + private + [F(1)]
    allowed = list(A) + [(t,) for t in range(m)] + [(m,)]
    k = sum(q) + 1
    count, pool, owner, layout, scores, opening = canonical_greedy(
        weights, allowed, m + 1, k, reverse_ties=reverse_ties)
    if count != list(q) + [1] or layout[-1] != m or scores[-1] != 1:
        raise AssertionError("Greedy multiplicity/last-score certificate failed.")
    if any(score <= 1 for score in scores[:-1]):
        raise AssertionError("A premature score at or below one occurred.")
    if any(not q[t] < pool[t] < q[t] + 1 for t in range(m)):
        raise AssertionError("First-opening pool certificate failed.")
    rank = {old: new for new, old in enumerate(opening)}
    aq = [count[t] for t in opening]
    ac = [pool[t] - count[t] for t in opening]
    aA = [sorted(rank[t] for t in row) for row in A]
    if any(aq[t] < aq[t + 1] for t in range(m)):
        raise AssertionError("First-opening order is not nonincreasing in q.")
    if any(rank[owner[i]] != min(aA[i]) for i in range(n)):
        raise AssertionError("Home-order certificate failed.")
    return {
        "kind": "search reduction; not a general NE solver",
        "source": {"q": list(q), "B": list(map(str, B)),
                   "u": list(map(str, u)), "A": [list(x) for x in A]},
        "eta": str(eta), "M": str(M), "delta": str(delta),
        "target": {"k": k, "site_count": m + 1,
                   "weights": list(map(str, weights)), "A": [list(x) for x in allowed]},
        "greedy": {"layout": layout, "multiplicities": count,
                   "pools": list(map(str, pool)), "owners": owner,
                   "insertion_scores": list(map(str, scores)), "gamma": "1"},
        "abstract": {"q": aq, "c": list(map(str, ac)),
                     "w": list(map(str, weights[:n])), "A": aA},
        "abstract_to_source_site": opening,
    }


def decode_ne(compiled: dict, abstract_assignment: Sequence[int]) -> list[int]:
    """Verify an oracle's station-pure output; return the source exclusions.

    The oracle is NOT provided by this module. No exponential fallback is used.
    For a two-choice source scheduling game, the selected machine is the other
    allowed site, not the returned exclusion.
    """
    source, target = compiled["source"], compiled["target"]
    q, B, u, A = normalize(**source)
    n, m = len(u), len(q)
    mapping = compiled["abstract_to_source_site"]
    if len(abstract_assignment) != n:
        raise ValueError("Oracle returned the wrong number of mobile clients.")
    a = []
    for i, v in enumerate(abstract_assignment):
        if type(v) is not int or not 0 <= v < len(mapping) or mapping[v] not in A[i]:
            raise ValueError("Oracle returned an illegal assignment.")
        a.append(mapping[v])
    weights = list(map(rational, target["weights"]))
    W = weights[n:n + m].copy()
    Y = list(B)
    for i, s in enumerate(a):
        W[s] += weights[i]
        for t in A[i]:
            if t != s:
                Y[t] += u[i]
    for t in range(m):
        if not q[t] <= W[t] <= q[t] + 1:
            raise ValueError("Oracle output fails the full box.")
    for i, s in enumerate(a):
        external = (W[s] - weights[i]) / q[s]
        for t in A[i]:
            if external > W[t] / q[t]:
                raise ValueError("Oracle output is not a target exact NE.")
            if t != s and (Y[s] + u[i]) / q[s] < Y[t] / q[t]:
                raise AssertionError("Source NE correspondence failed.")
    return a


def to_bounded_complement(q, c, w, A) -> dict:
    """General abstract F -> nonnegative co-singleton loads with exact bands.

    This is an import interface, not a solver: an oracle must return an NE
    satisfying the reported load bands, not just an arbitrary unbounded NE.
    The empty/zero-coverage case is handled directly, without this interface.
    """
    q, _, w, A = normalize(q, [0] * len(q), w, A)
    c = tuple(map(rational, c))
    if len(c) != len(q) or any(not 0 <= x <= 1 for x in c):
        raise ValueError("c must have one entry in [0,1] per site.")
    if any(q[t] < q[t + 1] for t in range(len(q) - 1)):
        raise ValueError("Abstract q must be nonincreasing.")
    if any(x >= 1 for x in w):
        raise ValueError("Abstract movable weights must be below one.")
    h, b, eligible = [row[0] for row in A], list(c), [F(0)] * len(q)
    for i, row in enumerate(A):
        b[h[i]] -= w[i]
        for t in row:
            eligible[t] += w[i]
    M = 1 + max((b[t] + eligible[t]) / q[t] for t in range(len(q)))
    B = [q[t] * M - b[t] - eligible[t] for t in range(len(q))]
    assert all(B[t] >= q[t] for t in range(len(q)))
    return {
        "kind": "bounded co-singleton import interface; not an NE solver",
        "source": {"q": list(q), "B": list(map(str, B)),
                   "u": list(map(str, w)), "A": [list(row) for row in A]},
        "M": str(M), "initial_exclusions": h,
        "lower_load": [str(qt * M - 1) for qt in q],
        "upper_load": [str(qt * M) for qt in q],
    }


if __name__ == "__main__":
    import json, sys
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python complement_reduction.py source.json")
    with open(sys.argv[1], encoding="utf-8") as stream:
        data = json.load(stream)
    result = compile_game(**data)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()
```

[完整研究包：证明、源码、独立审计、固定输入和结果](sandbox:/mnt/data/greedy_box_complement_embedding_2026-10-08.zip)

[完整证明记录](sandbox:/mnt/data/greedy_box_complement_embedding/research_note_zh.md) · [编译器源码](sandbox:/mnt/data/greedy_box_complement_embedding/complement_reduction.py) · [嵌入核验报告](sandbox:/mnt/data/greedy_box_complement_embedding/audit_results.json) · [一般带区间接口核验](sandbox:/mnt/data/greedy_box_complement_embedding/bounded_audit_results.json)

**本轮已闭合的是上述全状态搜索嵌入、规范运行对应及一般带区间等价接口。它们没有证明源问题困难，也没有证明现有规则存在超多项式轨迹；一般异权 NE 构造的多项式总时间仍未闭合。**