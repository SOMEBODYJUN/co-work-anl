## 本轮结论

**本轮尚未证明或反驳（BR）。** 得到了两个可以严格核验的结果：

1. **一个新的、合法的四人完整 SPE 证书：即使把所有玩家的去相关差额相加，总差额仍可为负。** 因而“早期玩家的负去相关差额会自动被后继玩家的正去相关差额补偿”这条全局路线也不成立。这个实例有 **89 名单位客户、6 个不同主题**。
2. **一个不限制竞争组合、使用整棵真实策略树的精确对偶证书定理。** 它把普遍（BR）无损转换为一族明确的线性证书存在性问题；对固定完整策略和固定有理混合分布，证书若不存在，可以提取真正的单位客户反例，而不是缺少后继理性的松弛点。

下面先给出总预算恒等式和新障碍，再给出这个全局证书定理及其完整证明。

---

# 一、应该保留的总预算：激励松弛与去相关差额必须一起计算

固定完整纯 SPE `\sigma`，实际终局为 `z`，实际第 `i` 位玩家行动前的历史为 `h_i`。

记

```math
B_i(a)
```

为该玩家在 `h_i` 改选 `a` 后，**同一份** **`\sigma`** 所产生的全部竞争主题：包括固定过去和真实后继，共 `n-1` 个。

论文中的 SPE 定义正是比较这样的真实续局收益，而不是把实际终局的其他行动冻结。([arXiv](https://arxiv.org/html/2307.07174v2 "https://arxiv.org/html/2307.07174v2"))

对任意主题分布 `p`，定义

```math
D_i(p)=\sum_a p_a f_{B_i(a)}(a),
```

以及

```math
C_i(p)=\sum_{a,b}p_ap_b f_{B_i(b)}(a).
```

`D_i` 是公开随机偏离的期望收益：先抽中 `a`，后继观察 `a`，再执行原策略。

`C_i` 则只是一个比较量：独立抽取 `a,b`，用 `b` 索引真实竞争组合，再用 `a` 查询该组合。**这里没有声称游戏中存在隐藏承诺。**

再定义

```math
e_i(p)=u_i-D_i(p)\ge0, \qquad \kappa_i(p)=D_i(p)-C_i(p).
```

其中，`e_i` 是实际节点的激励松弛，`\kappa_i` 是去相关差额。直接相加得到精确恒等式

```math
\boxed{ W-\sum_{i=1}^n C_i(p) = \sum_{i=1}^n e_i(p)+\sum_{i=1}^n\kappa_i(p). } \tag{1}
```

另一方面，令

```math
\underline v_n(p)=\min_B\mathbb E_{a\sim p}f_B(a).
```

由于 `C_i(p)` 是若干合法静态竞争组合查询值的平均，

```math
C_i(p)\ge \underline v_n(p). \tag{2}
```

因此，下列**允许局部负余额的全局预算引理**足以推出（BR）：

```math
\boxed{ \forall p,\qquad \sum_i e_i(p)+\sum_i\kappa_i(p)\ge0. } \tag{GB}
```

取安全值最优分布 `p^*`，由 (1)、(2) 即得

```math
W\ge\sum_i C_i(p^*)\ge nv_n.
```

必须区分两件事：

- 要求 `\sum_i\kappa_i(p)\ge0`，仍然过强；下面给出完整反例。
- 要求包含 `e_i` 的（GB），本轮没有证明，也没有得到反例。它仍比（BR）更强，因为它指定了一个特殊的竞争组合混合规则。

已有仓库障碍已经说明，逐节点去相关和根真实菜单的自由混合都不能直接完成证明。这里的新证书进一步排除了“只把去相关差额跨玩家相加”这一补救。

---

# 二、89 客户完整 SPE：总去相关差额为负，且后继差额全部为零

## 2.1 合法单位客户与共同目录

主题标为 `0,1,\ldots,5`。

用整数 mask `t` 编码客户的兴趣集合：第 `a` 个二进制位为 `1`，表示主题 `a` 覆盖这个客户。下表每一行的重数均表示**不同的单位客户**，不是加权客户。

| mask客户数mask客户数 |    |    |    |
| -------------- | -- | -- | -- |
| 5              | 16 | 35 | 5  |
| 10             | 1  | 40 | 4  |
| 11             | 11 | 46 | 2  |
| 15             | 8  | 52 | 1  |
| 22             | 1  | 53 | 4  |
| 23             | 2  | 54 | 14 |
| 24             | 2  | 56 | 2  |
| 26             | 1  | 61 | 10 |
| 33             | 1  | 62 | 4  |

总计 `89` 名客户，六个主题的覆盖集合两两不同。

## 2.2 完整策略及 SPE 认证

完整策略在文末核验代码的 `POLICY` 中给出。编码顺序为：

先按历史长度排列，再在同一长度内按主题标签的字典序排列；每一位数字指定相应历史上的行动。

它明确指定全部

```math
1+6+6^2+6^3=259
```

个有序决策历史。核验器逐历史重放原行动与全部备选行动后的原策略续局，用有理数检查全部

```math
259\cdot6=1554
```

项动作比较，包含原动作与自身的比较。

实际路径为

```math
z=(2,5,0,0),
```

实际收益为

```math
\boxed{ (u_1,u_2,u_3,u_4) = \left(\frac{71}{3},\,22,\,\frac{59}{3},\,\frac{59}{3}\right), \qquad W=85. } \tag{3}
```

这里没有把相同计数、不同顺序的历史绑定为同一回复。

## 2.3 总去相关失败

取用于检验去相关的分布

```math
\widehat p_1=\widehat p_2=\frac12, \qquad \widehat p_a=0\quad(a\notin\{1,2\}).
```

逐玩家的精确结果为：

| 玩家 `iD_i(\widehat p)C_i(\widehat p)\kappa_i=D_i-C_ie_i=u_i-D_i` |          |           |         |         |
| --------------------------------------------------------------- | -------- | --------- | ------- | ------- |
| 1                                                               | `43/2`   | `1033/48` | `-1/48` | `13/6`  |
| 2                                                               | `247/12` | `247/12`  | `0`     | `17/12` |
| 3                                                               | `59/3`   | `59/3`    | `0`     | `0`     |
| 4                                                               | `59/3`   | `59/3`    | `0`     | `0`     |

于是

```math
\boxed{\sum_{i=1}^4\kappa_i(\widehat p)=-\frac1{48}<0.} \tag{4}
```

这个失败比“某个早期节点去相关失败”更明确：

> **唯一的负去相关差额没有被任何后继节点的正去相关差额抵消，因为后三项恰好全为零。**

但真实激励松弛没有消失：

```math
\sum_i e_i(\widehat p)=\frac{43}{12}.
```

因此完整预算仍然为正：

```math
W-\sum_i C_i(\widehat p) = \frac{43}{12}-\frac1{48} = \boxed{\frac{57}{16}>0}. \tag{5}
```

所以，若继续攻击（GB），必须真正利用 `e_i`，不能仅以“全局去相关”代替它。

## 2.4 精确安全值：这个例子不是（BR）的反例

此实例的真正安全值为

```math
\boxed{v_4=\frac{508643}{26546}.} \tag{6}
```

匹配的原始证书为

```math
p^* = \frac1{331825} (44245,\ 49133,\ 120795,\ 77367,\ 0,\ 40285). \tag{7}
```

匹配的对偶证书 `Q^*` 如下；未列竞争组合概率为零：

| 竞争主题三元组 `B13273\,Q^*(B)` |      |
| ------------------------ | ---- |
| `(0,1,2)`                | 1635 |
| `(0,2,2)`                | 5550 |
| `(0,2,3)`                | 3365 |
| `(0,2,5)`                | 1123 |
| `(2,2,3)`                | 1600 |

独立有理数核验给出

```math
\min_B\mathbb E_{a\sim p^*}f_B(a) = \max_a\mathbb E_{B\sim Q^*}f_B(a) = \frac{508643}{26546}. \tag{8}
```

特别地，

```math
\boxed{ W-4v_4 = \frac{110919}{13273}>0. } \tag{9}
```

**因此，这个证书否定的是总去相关引理，不是否定（BR）。** 用于 (4) 的 `\widehat p` 也不是这里用于认证安全值的 `p^*`。

---

# 三、完整树—不受限静态对偶的精确证书定理

下面给出本轮对优先目标最有用的无损转换。它允许所有历史的激励约束共同支付总预算，也允许对偶使用任意竞争组合。

## 3.1 固定完整策略，把客户重数作为变量

固定主题数 `m`、人数 `n`，以及一份定义在全部有序历史上的纯策略 `\sigma`。

暂时不固定客户数量。对每个非空兴趣类型

```math
T\subseteq[m]
```

设重数变量 `w_T\ge0`。整数重数就是原模型中的单位客户实例；非负有理重数可以清除共同分母后展开。

记：

```math
z_h=\text{从历史 }h\text{ 开始执行 }\sigma\text{ 的完整终局},
```

```math
z_{ha}=\text{在 }h\text{ 选择 }a\text{ 后执行原策略的完整终局}.
```

对兴趣类型 `T`，定义单个该类型客户给选择主题 `a` 的玩家支付的份额

```math
\rho_T(a,z)= \begin{cases} \displaystyle\frac1{\#\{j:z_j\in T\}},&a\in T,\\[6pt] 0,&a\notin T. \end{cases} \tag{10}
```

出现第一种情况时，该终局包含该玩家选择的 `a`，分母不会为零。

为每个历史 `h` 和备选行动 `a` 建立一行

```math
\Gamma_{h,a;T} = \rho_T(\sigma(h),z_h) - \rho_T(a,z_{ha}). \tag{11}
```

于是

```math
\boxed{ \sigma\text{ 是该客户实例的完整纯 SPE} \iff w\ge0,\qquad \Gamma_\sigma w\ge0. } \tag{12}
```

这不是松弛：每行就是原模型的一项真实子博弈偏离比较。

定义实际覆盖系数

```math
c_T=\mathbf1\{z_{\varnothing}\text{ 中至少一个主题属于 }T\},
```

因此

```math
W=c\cdot w. \tag{13}
```

再固定一个有理分布 `p\in\Delta([m])`。对每个合法竞争元组 `B\in[m]^{n-1}`，定义向量

```math
\beta_B(p)_T = \frac{\sum_{a\in T}p_a} {1+\#\{j:B_j\in T\}}. \tag{14}
```

则

```math
\beta_B(p)\cdot w = \mathbb E_{a\sim p}f_B(a). \tag{15}
```

## 3.2 定理：全局总预算的精确线性证书

令

```math
\mathcal K_\sigma = \{w\ge0:\Gamma_\sigma w\ge0\}.
```

对固定的 `\sigma,p`，以下两件事等价。

**人口一致的总预算：**

```math
\forall w\in\mathcal K_\sigma,\qquad c\cdot w \ge n\min_B\beta_B(p)\cdot w. \tag{16}
```

**完整树线性证书：** 存在

```math
Q\in\Delta([m]^{n-1}),\qquad \lambda_{h,a}\ge0,\qquad r_T\ge0,
```

使逐客户类型恒等式成立：

```math
\boxed{ c-n\sum_BQ_B\beta_B(p) = \Gamma_\sigma^{\mathsf T}\lambda+r. } \tag{T}
```

这里没有逐人支付要求，也没有把 `Q` 限制在根菜单、实际删人组合或其他局部菜单中。

### 证明：证书推出总预算

将（T）与任意 `w\in\mathcal K_\sigma` 内积：

```math
c\cdot w - n\sum_BQ_B\beta_B(p)\cdot w = \lambda^{\mathsf T}\Gamma_\sigma w+r\cdot w \ge0.
```

又因为平均值不小于最小值，

```math
c\cdot w \ge n\sum_BQ_B\beta_B(p)\cdot w \ge n\min_B\beta_B(p)\cdot w.
```

得到 (16)。

### 证明：总预算推出证书

零重数向量无须处理。对非零重数按齐次性归一化，令

```math
K= \left\{ w\ge0: \Gamma_\sigma w\ge0,\quad \sum_Tw_T=1 \right\}.
```

这是非空紧凸多面体。非空性也可直接看出：只放一单位“对所有主题感兴趣”的客户，所有动作收益相同，任意策略均满足激励约束。

由 (16)，

```math
\max_{w\in K}\min_Q \left(n\sum_BQ_B\beta_B(p)-c\right)\cdot w \le0.
```

表达式对 `w,Q` 双线性，有限维 minimax 给

```math
\min_Q\max_{w\in K} \left(n\sum_BQ_B\beta_B(p)-c\right)\cdot w \le0.
```

所以存在 `Q`，使

```math
\left(c-n\sum_BQ_B\beta_B(p)\right)\cdot w\ge0 \qquad\forall w\in\mathcal K_\sigma.
```

多面体锥的对偶形式为

```math
\mathcal K_\sigma^* = \left\{ \Gamma_\sigma^{\mathsf T}\lambda+r: \lambda\ge0,\ r\ge0 \right\}.
```

故得到（T）。证毕。

---

# 四、为什么这个证书问题与原模型之间没有隐藏的放松

## 4.1 它与普遍（BR）的量词关系

称一份形式策略 `\sigma` **可实现**，若至少存在一个原模型的合法单位客户实例，其主题覆盖两两不同，且 `\sigma` 是完整纯 SPE。

那么普遍（BR）等价于：

```math
\boxed{ \begin{gathered} \text{对任意 }m,n,\text{ 任意可实现的完整策略 }\sigma,\\ \text{任意有理 }p\in\Delta([m]), \text{ 证书（T）存在。} \end{gathered} } \tag{GL}
```

正向需要一个技术细节：`\mathcal K_\sigma` 中可能有些重数使不同主题变成相同覆盖，不能直接把它们算作原模型的不同主题。

这个问题可以精确处理。固定一个实现 `\sigma` 且主题两两不同的重数向量 `w^0`。对任意 `w\in\mathcal K_\sigma`，

```math
w+\varepsilon w^0\in\mathcal K_\sigma\qquad(\varepsilon>0),
```

且主题重新两两不同。利用有理近似、整数缩放和有限最小值的连续性，原模型上的（BR）可以延拓到整个锥上的 (16)。

反向更直接：对任何原模型实例及其完整 SPE，把实际客户重数代入（T），然后对 `p` 取安全值最优分布，即得 `W\ge nv_n`。有理实例的有限安全值线性规划具有有理最优解，因此只要求有理 `p` 已足够。

**这一步是无损的全局转换，不是（BR）的证明。** 未完成的部分恰好是证明（GL）的普遍证书存在性。

## 4.2 证书不存在时，如何提取真正的反例

对固定完整 `\sigma` 和固定有理 `p`，考虑线性规划

```math
\begin{array}{ll} \text{最大化}&nt-c\cdot w\\ \text{满足}&w\ge0,\quad \Gamma_\sigma w\ge0,\\ &\sum_Tw_T=1,\\ &t\le\beta_B(p)\cdot w \quad\text{对所有 }B\in[m]^{n-1}. \end{array} \tag{LP}
```

若最优值严格为正，便有

```math
c\cdot w < n\min_B\beta_B(p)\cdot w \le nv_n(w). \tag{17}
```

由于数据有理，可以取有理可行见证。如果需要修复主题覆盖重合，加入足够小的有理 `\varepsilon w^0`：所有 SPE 行继续成立，而严格差距保留。最后清除共同分母，就得到有限单位客户实例。

因此，这里的正有理见证可以转换为真正反例，其原因不是“线性规划找到了一个点”，而是：

```math
\Gamma_\sigma w\ge0
```

已经包含了**固定完整策略的全部真实子博弈激励约束**。

相比之下，只约束部分历史、任意填写惩罚回复，或把后继冻结后得到的可行点，都没有这个性质。

---

# 五、准确剩余缺口与研究优先级

目前最精确的剩余引理是（GL），也就是：

> 对每份可实现的完整纯策略和每个混合查询分布，能否用所有真实节点的非负激励乘子，构造一个不受菜单限制的静态竞争分布，使逐客户类型恒等式（T）成立？

它把“谁为适应性付费”明确写成了

```math
\Gamma_\sigma^{\mathsf T}\lambda.
```

这些行可以来自不同深度、不同偏离分支；单行在某些客户类型上可以为负，只要求全部收费后的剩余向量非负。

本轮得到的具体障碍是：**不能把这笔跨节点收费简化为** **`\sum_i\kappa_i\ge0`**。89 客户证书已经否定了这种简化，而且失败时所有后继去相关差额都为零。保留实际激励松弛的（GB）仍值得攻击，但它限定了竞争分布的构造方式；（T）则没有这个额外限制。

与已证（SB）结合的结论仍然只能写成条件式：

```math
\text{若（BR）成立，则 } \operatorname{OPT}_n\le(2-1/n)W.
```

（SB）本身并不填补上述全局证书存在性的缺口。([GitHub](https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/main/research/current/customer_attraction/oblivious_security.md "https://raw.githubusercontent.com/SOMEBODYJUN/co-work-anl/main/research/current/customer_attraction/oblivious_security.md"))

---

# 六、可复现证书与完整核验代码

[下载独立有理数核验器](sandbox:/mnt/data/customer_attraction_global_budget_obstruction_89.py)
[下载客户、完整策略及原始／对偶证书 JSON](sandbox:/mnt/data/customer_attraction_global_budget_obstruction_89.json)

以下代码不调用优化器。它展开单位客户，验证完整 SPE，核验负的总去相关差额，并认证真正的 `v_4`。另外检查单人、全零客户、两主题边界，并确认一个故意错误的策略会被拒绝。

```python
"""Exact certificate: aggregate decorrelation fails; BR is NOT refuted."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json

WEIGHTS = {
    5: 16, 10: 1, 11: 11, 15: 8, 22: 1, 23: 2,
    24: 2, 26: 1, 33: 1, 35: 5, 40: 4, 46: 2,
    52: 1, 53: 4, 54: 14, 56: 2, 61: 10, 62: 4,
}
POLICY = (
    "222500222522222020250000022020220000022020022522222322253323"
    "022222222322222022222322222020230000022020220000022020053323"
    "030000030000020000030000000000022222222020220000022020220000"
    "022020222322220000030000020000020000020000022022222020000000"
    "0220202200000200200"
)
PRIMARY = [
    F(z, 331825)
    for z in (44245, 49133, 120795, 77367, 0, 40285)
]
DUAL = {
    (0, 1, 2): F(1635, 13273),
    (0, 2, 2): F(5550, 13273),
    (0, 2, 3): F(3365, 13273),
    (0, 2, 5): F(1123, 13273),
    (2, 2, 3): F(1600, 13273),
}


def audit(m, n, weights, encoded):
    """Expand unit customers; check every ordered-history deviation."""
    assert m >= 1 and n >= 1
    assert all(
        0 < t < 2**m and isinstance(k, int) and k > 0
        for t, k in weights.items()
    )
    customers = tuple(
        t for t, k in weights.items() for _ in range(k)
    )
    topics = tuple(
        frozenset(
            x for x, t in enumerate(customers) if t >> a & 1
        )
        for a in range(m)
    )
    assert len(set(topics)) == m

    histories = [
        h
        for k in range(n)
        for h in product(range(m), repeat=k)
    ]
    assert len(encoded) == len(histories)
    policy = dict(zip(histories, map(int, encoded)))
    assert all(0 <= a < m for a in policy.values())

    @lru_cache(None)
    def terminal(h):
        if len(h) == n:
            return h
        return terminal(h + (policy[h],))

    @lru_cache(None)
    def utilities(z):
        loads = [
            sum(x in topics[a] for a in z)
            for x in range(len(customers))
        ]
        return tuple(
            sum((F(1, loads[x]) for x in topics[a]), F(0))
            for a in z
        )

    comparisons = 0
    for h in histories:
        i = len(h)
        current = utilities(terminal(h))[i]
        for a in range(m):
            deviated = utilities(terminal(h + (a,)))[i]
            assert current >= deviated, (h, a)
            comparisons += 1

    def f(a, rivals):
        return utilities((a,) + tuple(rivals))[0]

    return (
        customers, topics, policy, terminal,
        utilities, f, comparisons
    )


def main():
    # Boundary cases and a deliberately non-equilibrium policy.
    audit(1, 1, {1: 1}, "0")
    audit(1, 3, {}, "000")
    audit(2, 2, {1: 1, 2: 1}, "110")

    rejected = False
    try:
        audit(2, 2, {1: 1, 2: 1}, "000")
    except AssertionError:
        rejected = True
    assert rejected

    (
        customers, topics, policy, terminal,
        utilities, f, comparisons
    ) = audit(6, 4, WEIGHTS, POLICY)

    z = terminal(())
    u = utilities(z)
    W = len(frozenset().union(*(topics[a] for a in z)))

    assert len(customers) == 89
    assert len(policy) == 259
    assert comparisons == 1554
    assert z == (2, 5, 0, 0)
    assert u == (F(71, 3), F(22), F(59, 3), F(59, 3))
    assert sum(u) == W == 85

    # Independent comparison variables, not hidden randomized play.
    p = {1: F(1, 2), 2: F(1, 2)}
    rows, h = [], ()

    for i in range(4):
        def rivals(a):
            zz = terminal(h + (a,))
            return zz[:i] + zz[i + 1:]

        D = sum(
            (p[a] * f(a, rivals(a)) for a in p), F(0)
        )
        C = sum(
            (
                p[a] * p[b] * f(a, rivals(b))
                for a in p for b in p
            ),
            F(0),
        )
        rows.append((D, C, D - C, u[i] - D))
        h += (policy[h],)

    assert [r[2] for r in rows] == [
        F(-1, 48), F(0), F(0), F(0)
    ]
    assert sum(r[0] for r in rows) == F(977, 12)
    assert sum(r[1] for r in rows) == F(1303, 16)
    assert sum(r[3] for r in rows) == F(43, 12)
    assert W - sum(r[1] for r in rows) == F(57, 16)

    # Exact certificates over all ordered competitor tuples.
    assert sum(PRIMARY) == sum(DUAL.values()) == 1
    assert min(PRIMARY) >= 0
    assert min(DUAL.values()) >= 0

    lower = min(
        sum(
            (PRIMARY[a] * f(a, B) for a in range(6)),
            F(0),
        )
        for B in product(range(6), repeat=3)
    )
    upper = max(
        sum(
            (q * f(a, B) for B, q in DUAL.items()),
            F(0),
        )
        for a in range(6)
    )

    assert lower == upper == F(508643, 26546)
    assert W - 4 * lower == F(110919, 13273) > 0

    return {
        "claim": (
            "sum_i(D_i-C_i) >= 0 is false; "
            "BR is NOT refuted"
        ),
        "unit_customers": len(customers),
        "ordered_decision_histories": len(policy),
        "exact_incentive_comparisons": comparisons,
        "outcome": list(z),
        "utilities": list(map(str, u)),
        "W": W,
        "v_4": str(lower),
        "W_minus_4v_4": str(W - 4 * lower),
        "aggregate_decorrelation": str(
            sum(r[2] for r in rows)
        ),
        "aggregate_on_path_slack": str(
            sum(r[3] for r in rows)
        ),
        "compensated_budget": str(
            W - sum(r[1] for r in rows)
        ),
        "rows_D_C_kappa_slack": [
            list(map(str, r)) for r in rows
        ],
        "boundary_tests": (
            "passed; non-SPE policy rejected"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, indent=2))
```

**可登记的结论是：完整树对偶证书的等价定理，以及总去相关非负性的合法反例。不可登记为已证的是（GB）、（BR）或原半覆盖目标。**