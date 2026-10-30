# Supplied Pro report: equal movable-weight flow selector

Received as the user-attached `粘贴的文本 (1).txt` on 2026-10-07.
The complete attached text and embedded code follow, with line endings normalized.
The original attachment SHA-256 is `31420663aa1fe11430ca912745522e9a3e81adb2ac417c23413f9988a43adee5`.
Its sandbox ZIP and linked separate code/report files were not attached or obtained.
Reported test counts below are source claims, not repository verification evidence.
The current reconstruction and independently generated implementation/evidence are
linked from `research/current/multi_facility/equal_light_flow.md`.
The claimed equal-light MF input class was already covered by
`SC-K-UNIFORM-LIGHT-FLOW-2`; the new proof removes the optimization lower bounds
and proves the additional home inequalities for every global optimizer.

---

**一般异权输入的位多项式总运行时间，本轮仍未闭合。** 我没有证明现有确定性规则具有多项式总步数，也没有得到覆盖一般异权输入的新构造。

本轮取得了一个新的、具有完整总成本证明的子类结果：

> **当所有未冻结的可移动客户等权时，对任意客户数、地点数、设施数及任意允许集合，可以通过最小费用流，在输入位长多项式时间内直接构造完整盒内精确 NE，并同时满足 \((H)\)。全过程恰好进行 \(n\) 次单位增广。**

这个结果不要求树宽、深度、出度或共同锚点受限；但**等权限制目前尚未去掉**。

我已按交接页读取公开 `main` 的状态、完整进展证明、规范代码和 BOX-TO-2 接口。交接页所列的一般异权总时间义务仍然保留，不能用本轮子类结果替代。你消息中的提交号为空，本轮也没有取得可核验的远端 SHA，因此不能称为锁定提交的检出；未修改仓库。([GitHub][1])

## 一、等权全局构造定理

设所有可移动客户的权重为同一个正有理数

$$
w_i=\delta,\qquad 0<\delta<1.
$$

其他条件完全不变：

$$
q_1\ge\cdots\ge q_m\ge1,\qquad
0\le c_t\le1,\qquad h_i=\min A_i.
$$

记

$$
H_t:=\#\{i:h_i=t\},\qquad
N_t(a):=\#\{i:a_i=t\},\qquad
b_t:=c_t-\delta H_t.
$$

于是

$$
X_t(a)=b_t+\delta N_t(a).
$$

这里 \(b_t\) 可以为负，算法不把它当成必须非负的实际负载。

考虑下面的目标函数：

$$
\boxed{
\Psi(a)=
\sum_{t=1}^m
\frac{b_tN_t(a)+\frac{\delta}{2}N_t(a)(N_t(a)-1)}{q_t}.
}
\tag{1}
$$

**优化域是全部合法分配 \(a_i\in A_i\)，不预先施加盒约束或 \((H)\)。**

### 定理

任意 \(\Psi\) 的全局最小者都满足

$$
0\le X_t\le1,
$$

$$
\frac{X_{a_i}-\delta}{q_{a_i}}
\le \frac{X_v}{q_v}
\qquad(i,\ v\in A_i),
$$

以及

$$
\frac{X_{a_i}-\delta}{q_{a_i}}
\le\frac{1-\delta}{q_{h_i}}.
$$

而且，\(\Psi\) 的一个全局最小者可通过一个多项式规模的最小费用流网络求出。

下面先证明“全局最小者自动落入盒”，再给出算法及**全过程**的复杂度界。

## 二、为什么无约束最小者自动满足完整盒与 NE

### 1. 所有 NE 不等式直接来自单客户移动

把一名客户从 \(s\) 移到 \(t\)，式（1）的变化恰为

$$
\boxed{
\Delta\Psi
=
\frac{X_t}{q_t}
-\frac{X_s-\delta}{q_s}.
}
\tag{2}
$$

因此，全局最小者不可能存在严格客户改善。

这里检查的是全部原始允许集合中的偏离，**没有删除“偏离后会越盒”的选项**。

剩下要证明的是：这个无约束最小者本身满足完整盒与 \((H)\)。

### 2. 下盒：沿归属有向路径同时归位

对每名不在归属的客户，画一条边

$$
h_i\longrightarrow a_i.
$$

由于 \(h_i=\min A_i\)，每条边都严格指向更大的地点编号。

假设某个全局最小者在地点 \(s\) 满足 \(X_s<0\)。记 \(\operatorname{in}(s)\)、\(\operatorname{out}(s)\) 分别为外来客户数和离乡客户数，则

$$
X_s=c_s+\delta\bigl(\operatorname{in}(s)-\operatorname{out}(s)\bigr).
$$

因为 \(c_s\ge0\)，地点 \(s\) 必有出边。

沿出边继续走，直到一个没有出边的地点 \(z\)。编号严格递增，所以这条路径有限。终点至少有一条入边，故

$$
X_z=c_z+\delta\operatorname{in}(z)\ge\delta.
$$

现在把路径上的客户**同时送回各自归属**。每个中间地点都失去一名、得到一名等权客户，因此人数和负载完全不变。只有两个端点改变：

$$
X_s\mapsto X_s+\delta,\qquad
X_z\mapsto X_z-\delta.
$$

所以

$$
\Delta\Psi
=\frac{X_s}{q_s}-\frac{X_z-\delta}{q_z}<0,
$$

与全局最小性矛盾。

因此

$$
\boxed{X_t\ge0\quad\forall t.}
\tag{3}
$$

### 3. 外来客户的 \((H)\)：反向追溯归属路径

假设外来客户 \(i\) 位于 \(t\)，并且违反 \((H)\)：

$$
e_i:=\frac{X_t-\delta}{q_t}
>
\frac{1-\delta}{q_{h_i}}.
\tag{4}
$$

从 \(u=h_i\) 开始向较小编号追溯。

若 \(X_u\le1-\delta\)，立即停止。否则，\(u\) 已经有一名离乡客户。若它没有外来客户，就有

$$
X_u=c_u-\delta\operatorname{out}(u)\le1-\delta,
$$

矛盾。因此，可以选一名当前分配在 \(u\) 的外来客户，继续追溯到该客户的归属。

每一步编号严格减小，所以最终到达某个地点 \(z\)，满足

$$
X_z\le1-\delta,\qquad q_z\ge q_{h_i}.
$$

把这条反向路径上选出的客户同时归位。中间地点仍然是等权抵消，只剩

$$
X_t\mapsto X_t-\delta,\qquad
X_z\mapsto X_z+\delta.
$$

目标变化为

$$
\begin{aligned}
\Delta\Psi
&=\frac{X_z}{q_z}-e_i\\
&\le\frac{1-\delta}{q_z}-e_i\\
&\le\frac{1-\delta}{q_{h_i}}-e_i
<0,
\end{aligned}
$$

再次矛盾。

所以，所有外来客户都满足 \((H)\)。

### 4. 上盒与归属客户的 \((H)\)

若某地点 \(t\) 满足 \(X_t>1\)，由 \(c_t\le1\)，它必有外来客户 \(j\)。于是

$$
\frac{X_t-\delta}{q_t}
>
\frac{1-\delta}{q_t}
\ge
\frac{1-\delta}{q_{h_j}},
$$

违反刚刚证明的外来客户 \((H)\)。

因此

$$
\boxed{X_t\le1\quad\forall t.}
\tag{5}
$$

在归属的客户，其 \((H)\) 随即由 \(X_{h_i}\le1\) 得到。结合式（2）、（3）、（5），定理的正确性部分完成。

**这里起决定作用的不是有限改善势，而是等权交换路径的内部负载完全抵消。**

## 三、直接求终点的最小费用流算法

构造网络

$$
S\longrightarrow i\longrightarrow t\longrightarrow T.
$$

源点到每名客户的边容量为 \(1\)、费用为 \(0\)。客户 \(i\) 到每个 \(t\in A_i\) 的边容量为 \(1\)、费用为 \(0\)。

令

$$
M_t:=\#\{i:t\in A_i\}.
$$

地点 \(t\) 到汇点建立 \(M_t\) 条平行的单位容量“槽边”，第 \(\ell\) 条费用为

$$
\boxed{
d_{t,\ell}
=\frac{b_t+(\ell-1)\delta}{q_t},
\qquad 1\le\ell\le M_t.
}
\tag{6}
$$

这些槽费用严格递增。因此，在一个最小费用流中，某地点使用 \(N_t\) 条槽边时，必使用费用最低的前 \(N_t\) 条。它们的费用和正好为

$$
\sum_{\ell=1}^{N_t}d_{t,\ell}
=
\frac{b_tN_t+\delta N_t(N_t-1)/2}{q_t}.
$$

所以：

$$
\boxed{
\text{流量为 }n\text{ 的最小费用整数流}
\quad\Longleftrightarrow\quad
\Psi\text{ 的一个全局最小合法分配}.
}
\tag{7}
$$

每条客户出边承载的是**一整名客户**，不是一个权重单位。没有把原子客户拆开。

### 总增广次数不是势值范围，而是客户数

记

$$
E=\sum_i|A_i|,\qquad V=n+m+2.
$$

网络有 \(V\) 个节点、\(n+2E\) 条正向边。

初始网络是有向无环图，因此即使有负槽费用，也没有负环。从零流开始，反复沿最短费用增广路发送一个单位。最短路增广保持残量网络没有负环，从而每个流量阶段都保持最小费用；这是标准最短增广路算法的最优性依据。([MIT课程][2])

由于源点恰有 \(n\) 条单位容量客户边，

$$
\boxed{\text{全过程恰好执行 }n\text{ 次单位增广。}}
\tag{8}
$$

使用 Bellman–Ford，每次增广需要

$$
O\bigl(V(n+E)\bigr)
$$

次整数加法与比较。包括建图在内，总算术操作数为

$$
\boxed{
O\bigl(m+n(n+m+2)(n+E)\bigr),
}
\tag{9}
$$

另加多项式时间的输入及有理数预处理。

### 位复杂度

令

$$
D=\operatorname{lcm}\bigl(
\operatorname{den}(c_1),\ldots,\operatorname{den}(c_m),
\operatorname{den}(\delta)
\bigr),
$$

$$
L=D\operatorname{lcm}(q_1,\ldots,q_m).
$$

把所有费用乘以 \(L\)，便得到整数费用。

\(D,L\) 的位长至多为相应输入位长的和。槽费用、最短路标签、总流费用均保持多项式位长。因此式（9）确实给出**输入位长多项式总时间**，而不是分母数值意义上的伪多项式时间。

这个结论甚至不需要显式展开 \(q_t\) 家设施。没有客户时，算法零次增广并直接返回 \(X=c\)。

该子类结果也不依赖仓库中局部权重 DP 所需的固定树宽条件；它允许任意覆盖图。([GitHub][3])

## 四、一般异权推广还缺哪一步

等权证明与原精确势之间有恒等式

$$
\Phi(a)
=
\sum_t\frac{b_t^2}{2q_t}+\delta\Psi(a).
$$

但不能据此把上述选择器直接推广到一般异权。仓库已经记录了一般异权下全盒势最小者不必是 NE 的边界。([GitHub][4])

下面可以把推广障碍写成一条精确公式，而不是笼统地说“交换会影响别人”。

设一条归位路径为

$$
u_0=t,u_1,\ldots,u_{\ell+1}=z,
$$

其中第 \(j\) 名客户权重为 \(w_j\)，从 \(u_j\) 返回 \(u_{j+1}\)。所有 \(X\) 都取同时归位之前的值。

中间地点 \(u_j\) 的负载变化为

$$
\boxed{\Delta X_{u_j}=w_{j-1}-w_j.}
\tag{10}
$$

对原精确势，同时归位的变化恰为

$$
\boxed{
\begin{aligned}
\Delta\Phi={}&
-w_0\frac{X_{u_0}-w_0}{q_{u_0}}\\
&+\sum_{j=1}^{\ell}
(w_{j-1}-w_j)
\frac{X_{u_j}-w_j}{q_{u_j}}\\
&+w_\ell\frac{X_{u_{\ell+1}}}{q_{u_{\ell+1}}}.
\end{aligned}
}
\tag{11}
$$

内部项来自恒等式

$$
\frac{(X+x-y)^2-X^2-(x^2-y^2)}{2q}
=
(x-y)\frac{X-y}{q}.
$$

等权时，式（11）的内部和为零，整个交换由两个端点控制。异权时，内部项一般没有确定符号。

因此，**本轮没有完成的证明义务**是：找到一种一般异权的批量交换或全局优化机制，能够控制这些内部项，同时给出多项式总次数。按权重类分别调用等权流算法，也尚未解决类间反复破坏已有 NE 不等式的问题。

这不是一般多项式构造不可能的证据。它只说明，本轮这个直接流构造还没有越过等权边界。

对满足等权条件的实际贪心输出，本算法可以直接供应 BOX-TO-2 所需的多项式盒内 NE；但不能据此登记一般异权多项式构造。后续数学接口不要求额外保留 \((H)\)，只是本算法自动给出了它。([GitHub][5])

## 五、精确核验与完整实现

独立核验器没有调用上一轮的 NE 检查代码。本轮完成了 **13,910 个合法分配**的穷举比较，检查了其中全部 **5,496 个全局最小者**；构造器在 **4,982 个有效实例**上通过了精确检查。另行检查了空输入、单地点、并列、盒边界、大分母、大 \(q\)、非法输入，以及式（11）的精确恒等式。

这些检查验证实现；定理依据的是前面的交换证明和总增广次数证明。

下面是完整构造器。输入中的地点编号从零开始，有理数使用字符串或 `Fraction`；**一般异权输入会被明确拒绝，不会悄悄回退到指数算法。**

```python
"""Exact polynomial constructor for equal movable weights; sites are zero-based."""
from fractions import Fraction
from math import lcm
from typing import Sequence

Rational = int | str | Fraction

def equal_weight_box_ne(
    q: Sequence[int], c: Sequence[Rational], w: Sequence[Rational],
    A: Sequence[Sequence[int]],
) -> dict:
    """Return a boxed exact NE with H. Reject nonuniform movable weights."""
    def rational(x: Rational) -> Fraction:
        if isinstance(x, bool) or not isinstance(x, (int, str, Fraction)):
            raise ValueError("Use integers, Fraction, or rational strings, not floats.")
        try:
            return Fraction(x)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError("Invalid rational input.") from exc

    q, c, w = tuple(q), tuple(map(rational, c)), tuple(map(rational, w))
    m, n = len(q), len(w)
    if len(c) != m or len(A) != n:
        raise ValueError("Dimension mismatch.")
    if any(type(x) is not int or x < 1 for x in q):
        raise ValueError("q must contain positive integers.")
    if any(q[t] < q[t + 1] for t in range(m - 1)):
        raise ValueError("q must be nonincreasing.")
    if any(not 0 <= x <= 1 for x in c):
        raise ValueError("c must lie in [0,1].")
    if any(not 0 < x < 1 for x in w):
        raise ValueError("Each weight must lie in (0,1).")
    if n and any(x != w[0] for x in w):
        raise ValueError("This constructor requires equal movable weights.")
    choices = []
    for row in A:
        row = tuple(row)
        if not row or any(type(t) is not int or not 0 <= t < m for t in row):
            raise ValueError("Each allowed set must be nonempty and valid.")
        choices.append(tuple(sorted(set(row))))
    A = tuple(choices)
    delta = w[0] if n else Fraction(1, 2)
    h = tuple(row[0] for row in A)
    home_count, degree = [0] * m, [0] * m
    for i, row in enumerate(A):
        home_count[h[i]] += 1
        for t in row:
            degree[t] += 1
    b = [c[t] - delta * home_count[t] for t in range(m)]

    # Scale costs, never capacities, to integers. No denominator-sized loops.
    D = lcm(delta.denominator, *(x.denominator for x in c))
    scale = D * lcm(1, *q)
    source, sink, V = n + m, n + m + 1, n + m + 2
    graph: list[list[list[int]]] = [[] for _ in range(V)]

    def add(u: int, v: int, cost: int) -> int:
        j, k = len(graph[u]), len(graph[v])
        graph[u].append([v, k, 1, cost])
        graph[v].append([u, j, 0, -cost])
        return j

    assignment_edges = []
    for i, row in enumerate(A):
        add(source, i, 0)
        assignment_edges.append([(t, add(i, n + t, 0)) for t in row])
    for t in range(m):
        for ell in range(degree[t]):
            z = (b[t] + ell * delta) * scale / q[t]
            if z.denominator != 1:
                raise RuntimeError("Cost scaling failed.")
            add(n + t, sink, z.numerator)

    # Exactly n unit augmentations; Bellman-Ford handles negative slot costs.
    total_cost = 0
    for _ in range(n):
        dist: list[int | None] = [None] * V
        parent: list[tuple[int, int] | None] = [None] * V
        dist[source] = 0
        for _pass in range(V - 1):
            changed = False
            for u in range(V):
                if dist[u] is None:
                    continue
                for j, (v, _rev, cap, cost) in enumerate(graph[u]):
                    candidate = dist[u] + cost
                    if cap and (dist[v] is None or candidate < dist[v]):
                        dist[v], parent[v] = candidate, (u, j)
                        changed = True
            if not changed:
                break
        if dist[sink] is None:
            raise RuntimeError("Unexpected infeasibility.")
        path, seen, v = [], set(), sink
        while v != source:
            if v in seen or parent[v] is None:
                raise RuntimeError("Invalid shortest-path predecessor chain.")
            seen.add(v)
            u, j = parent[v]
            path.append((u, j))
            v = u
        for u, j in path:
            v, rev, cap, cost = graph[u][j]
            graph[u][j][2] = cap - 1
            graph[v][rev][2] += 1
            total_cost += cost

    a = []
    for i, refs in enumerate(assignment_edges):
        selected = [t for t, j in refs if graph[i][j][2] == 0]
        if len(selected) != 1:
            raise RuntimeError("Nonintegral or incomplete assignment.")
        a.append(selected[0])
    count = [0] * m
    for t in a:
        count[t] += 1
    X = [b[t] + delta * count[t] for t in range(m)]
    if any(not 0 <= x <= 1 for x in X):
        raise RuntimeError("Full-box certificate failed.")
    for i, s in enumerate(a):
        external = (X[s] - delta) / q[s]
        if external > (1 - delta) / q[h[i]]:
            raise RuntimeError("H certificate failed.")
        if any(external > X[t] / q[t] for t in A[i]):
            raise RuntimeError("Exact NE certificate failed.")
    objective = sum(
        (b[t] * count[t] + delta * count[t] * (count[t] - 1) / 2) / q[t]
        for t in range(m)
    )
    if Fraction(total_cost, scale) != objective:
        raise RuntimeError("Flow/objective identity failed.")
    return {"assignment": a, "X": list(map(str, X)),
            "objective": str(objective), "augmentations": n}

if __name__ == "__main__":
    import json
    import sys
    data = json.load(sys.stdin)
    result = equal_weight_box_ne(**{key: data[key] for key in ("q", "c", "w", "A")})
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()
```

[下载完整研究包：证明、构造器、独立核验器、输入和结果](sandbox:/mnt/data/greedy_box_equal_weight_flow_2026-10-07.zip)

[完整证明记录](sandbox:/mnt/data/greedy_box_equal_weight_flow/research_note_zh.md) · [构造代码](sandbox:/mnt/data/greedy_box_equal_weight_flow/equal_weight_box_ne.py) · [精确核验报告](sandbox:/mnt/data/greedy_box_equal_weight_flow/audit_results.json)

**本轮可登记的是：等权可移动客户、任意覆盖图与任意设施数的统一位多项式完整盒 NE 构造。一般异权输入的统一位多项式总时间仍未证明。**

[1]: https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/main/research/questions/greedy_box_polytime.md "https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/main/research/questions/greedy_box_polytime.md"
[2]: https://courses.csail.mit.edu/6.854/20/Notes/n09-mincostflow.html "https://courses.csail.mit.edu/6.854/20/Notes/n09-mincostflow.html"
[3]: https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/main/research/current/multi_facility/local_weight_box_dp.md "https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/main/research/current/multi_facility/local_weight_box_dp.md"
[4]: https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/main/research/current/multi_facility/depth_three_box_boundary.md "https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/main/research/current/multi_facility/depth_three_box_boundary.md"
[5]: https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/main/research/current/multi_facility/polytime_frontier.md "https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/main/research/current/multi_facility/polytime_frontier.md"
