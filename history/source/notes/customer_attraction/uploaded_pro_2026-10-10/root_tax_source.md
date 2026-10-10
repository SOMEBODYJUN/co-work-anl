**（RT）为假。四人、六个主题就存在严格反例。**

下面的实例有 `61` 名单位客户，并有一份定义在全部有序历史上的纯 SPE，满足

```math
\boxed{ \operatorname{OPT}_4=61,\qquad W=38,\qquad \tau=\frac{45}{2}. }
```

因此

```math
\boxed{ \operatorname{OPT}_4-W-\tau =61-38-\frac{45}{2} =\frac12>0. }
```

**这是空背景的根总税反例，不是半覆盖反例：**

```math
61<2\cdot38=76.
```

而且，这个反例不需要复杂的历史依赖平局：前三位在所有历史都选同一主题，只有末位执行带固定平局顺序的最佳回应。

## 一、单位客户实例

取四位相同、无权提供者，共同目录为

```math
\mathcal S=\{A,B,C,D,E,F\}.
```

按下表建立互不相交的客户组。“所属主题”表示客户**恰好**属于这些主题。例如，`AEF` 行的六名客户都属于 `A,E,F`，不属于 `B,C,D`。

| 所属主题不同单位客户数 |    |
| ----------- | -- |
| `A`         | 12 |
| `B`         | 8  |
| `C`         | 4  |
| `D`         | 8  |
| `AE`        | 6  |
| `AF`        | 6  |
| `CE`        | 3  |
| `CF`        | 3  |
| `AEF`       | 6  |
| `BEF`       | 2  |
| `CEF`       | 1  |
| `DEF`       | 2  |

这里的重数只是压缩表示不同的单位客户，**没有使用客户权重或提供者权重**。

主题大小为

```math
|A|=30,\quad |B|=10,\quad |C|=11,\quad |D|=10,\quad |E|=|F|=20.
```

特别地，`A,B,C,D` 两两不交，而且构成全部客户的一个分割：

```math
X=A\mathbin{\dot\cup}B\mathbin{\dot\cup}C\mathbin{\dot\cup}D.
```

所以四个提供者分别选择 `A,B,C,D`，就覆盖全部客户。因此

```math
\boxed{\operatorname{OPT}_4=|X|=61.}
```

## 二、完整策略：前三位恒选 `A`，末位取真实最佳回应

定义如下纯策略。

前三位提供者在其**每一个**合法有序历史上都选择 `A`：

```math
\sigma_1(\varnothing)=A,\qquad \sigma_2(P)=A,\qquad \sigma_3(P,Q)=A \quad(P,Q\in\mathcal S).
```

末位观察真实历史 `h=(P,Q,T)`。记该历史的负载为

```math
d_x(h)=\mathbf1_{x\in P}+\mathbf1_{x\in Q}+\mathbf1_{x\in T}.
```

末位选择使

```math
L(S\mid h)=\sum_{x\in S}\frac1{1+d_x(h)}
```

最大的主题；平局时按照固定优先序

```math
\boxed{F\succ E\succ D\succ C\succ B\succ A}
```

选择。将这个唯一确定的回复记为 `\rho(h)`。

这就定义了全部历史上的策略。特别是，早期玩家偏离后，末位执行的是 `\rho(\text{偏离后的真实历史})`，并不固定为原路径上的末位动作。

## 三、精确证明：这份策略在每个子博弈都最优

末位的最优性由其定义直接成立。下面验证前三位，包括所有离轨历史。

### 1. 把所有早期节点归约到同一个有限比较

对任意 `P,Q,T\in\mathcal S`，定义

```math
V(T;P,Q) = \sum_{x\in T} \frac1{ 1+\mathbf1_{x\in P} +\mathbf1_{x\in Q} +\mathbf1_{x\in\rho(P,Q,T)} }. \tag{1}
```

它表示：前三位中的一人选择 `T`，另外两人选择 `P,Q`，末位按上述真实最佳回应规则行动时，选择 `T` 者的终局收益。

由于**这份具体策略**的末位回复只依赖主题计数与固定标签优先序，

```math
V(T;P,Q)=V(T;Q,P).
```

我们将验证

```math
\boxed{ V(A;P,Q)\ge V(T;P,Q) \quad\text{对所有 }P,Q,T\in\mathcal S. } \tag{2}
```

这足以同时验证前三位：

第三位在历史 `(P,Q)` 的全部偏离比较就是式 (2)。第二位在历史 `P` 偏离到 `T` 后，第三位按同一策略选择 `A`，所以比较的是 `V(T;P,A)`。第一位偏离到 `T` 后，第二、第三位均选择 `A`，所以比较的是 `V(T;A,A)`。

因此，只需验证式 (2)，而不是假定任何一般 SPE 具有计数不变性。

### 2. 全部比较的精确表

下表覆盖六个主题形成的全部 `21` 个无序二元组，包含重复主题。相同结果合并展示。

第二列是选 `A` 的收益；第三列是其他五个动作中的最大收益。所有数值均按式 (1) 和客户组表直接计算。

| 另外两人的主题 `P,QV(A;P,Q)\displaystyle\max_{T\ne A}V(T;P,Q)` |        |        |
| ------------------------------------------------------- | ------ | ------ |
| `AA`                                                    | `9`    | `9`    |
| `AB,\ AD`                                               | `13`   | `11`   |
| `AC`                                                    | `13`   | `10`   |
| `AE,\ AF`                                               | `23/2` | `9`    |
| `BB,\ DD`                                               | `15`   | `38/3` |
| `BC,\ CD`                                               | `15`   | `11`   |
| `BD`                                                    | `15`   | `12`   |
| `BE,\ BF,\ DE,\ DF`                                     | `13`   | `61/6` |
| `CC`                                                    | `15`   | `34/3` |
| `CE,\ CF`                                               | `13`   | `9`    |
| `EE,\ FF`                                               | `12`   | `55/6` |
| `EF`                                                    | `23/2` | `26/3` |

每一行第二列都不小于第三列，故式 (2) 成立。

为明确表中末位回复的计算方法，记客户类型 `M\subseteq\mathcal S` 的人数为 `m_M`。在历史 `(P,Q,T)`，末位选 `S` 的收益恰为

```math
L(S\mid P,Q,T) = \sum_{M:\,S\in M} \frac{m_M}{ 1+\mathbf1_{P\in M}+\mathbf1_{Q\in M}+\mathbf1_{T\in M} }. \tag{3}
```

先用式 (3) 及固定平局序确定 `\rho(P,Q,T)`，再代入式 (1)，就得到上表。

例如，`AA` 行实际上有更强的等式：

```math
V(A;A,A)=V(B;A,A)=\cdots=V(F;A,A)=9. \tag{4}
```

其中，第三位偏离到 `F` 后，末位的真实回复是 `E`，因此

```math
V(F;A,A) = 3+\frac63+\frac64+\frac22+\frac12+\frac22 =9.
```

这里六项分别来自 `CF,AF,AEF,BEF,CEF,DEF` 六类客户。

至此，前三位在每个历史的全部偏离，以及末位在每个历史的全部偏离，都已验证。每位提供者在一条实现分支上只行动一次，所以这些比较就是所需的全部子博弈最优性条件。

```math
\boxed{\text{上述完整纯策略是一份 SPE。}}
```

## 四、实际终局与根税的精确计算

前三位实际都选择 `A`。在末位历史 `AAA`，六个动作的收益为

```math
\begin{array}{c|rrrrrr} \text{动作}&A&B&C&D&E&F\\ \hline \text{末位收益}&15/2&10&11&10&11&11 . \end{array}
```

根据固定平局顺序，末位选择 `F`。实际终局是

```math
\boxed{(A,A,A,F).}
```

由客户组表，

```math
|A\cap F|=6+6=12,\qquad |A\setminus F|=18,\qquad |F\setminus A|=8.
```

因此前三位每人获得

```math
u_1=u_2=u_3 =\frac{18}{3}+\frac{12}{4} =9,
```

末位获得

```math
u_4=8+\frac{12}{4}=11.
```

总福利为

```math
\boxed{W=9+9+9+11=38.}
```

计算题目指定的税时，只计前三次行动。因此

```math
b_x= \begin{cases} 3,&x\in A,\\ 0,&x\notin A. \end{cases}
```

于是

```math
\boxed{ \tau=\sum_x\frac{b_x}{b_x+1} =30\cdot\frac34 =\frac{45}{2}. }
```

与最优覆盖比较，

```math
W+\tau =38+\frac{45}{2} =\frac{121}{2} <61 =\operatorname{OPT}_4.
```

严格违背量为

```math
\boxed{\frac12.}
```

等价地，实际未覆盖的客户共有

```math
61-38=23
```

人，而根税只有 `45/2`，比这部分覆盖损失少了 `1/2`。

## 五、后继理性为什么没有救回（RT）

这个例子直接展示了你强调的“早期偏离收益如何被真实续局稀释”。

在实际终局 `AAAF`，末位选择 `F` 能获得 `11`。但是，第一位不能通过提前选择 `F` 获得这个收益。第一位偏离到 `F` 后，同一份策略产生

```math
\boxed{(F,A,A,E),}
```

而不是保留原末位动作的冻结终局。

这个真实分支的收益为

```math
\boxed{ \left(9,\frac{23}{2},\frac{23}{2},9\right). }
```

这里没有不可信的惩罚：

两位中间提供者选 `A` 都能获得 `23/2`，而改选其他主题至多获得 `9`，对应上表的 `AF` 行。末位在真实历史 `FAA` 的六个动作收益为

```math
(9,9,9,9,9,7),
```

所以按固定优先序选择 `E`，确实是最佳回应。最初选择 `F` 的偏离者最终只获得 `9`，没有改善。

**因此，后继理性仍允许“末位可得** **`11`****”在提前选择后降为** **`9`****。** 这个可信稀释已经足以破坏根税候选。

还可以把题目中的末位接口缺口精确定位。设

```math
f_b(T)=\sum_{x\in T}\frac1{b_x+1}.
```

对本例的最优分割 `A,B,C,D`，

```math
\bigl(f_b(A),f_b(B),f_b(C),f_b(D)\bigr) = \left(\frac{15}{2},10,11,10\right).
```

其和为

```math
\sum_{T\in\{A,B,C,D\}}f_b(T) =\frac{77}{2} =W+\frac12. \tag{5}
```

相对于末位收益 `u_4=11`，四个最佳回应松弛之和为

```math
\left(11-\frac{15}{2}\right)+(11-10)+(11-11)+(11-10) =\frac{11}{2},
```

但

```math
4u_4-W=44-38=6.
```

两者正好相差 `1/2`。

所以，已有接口

```math
\operatorname{OPT}_4\le4u_4+\tau=\frac{133}{2}
```

在这里完全正确；失败的是试图进一步把它收紧为 `W+\tau`。这也不影响论文的两人结论或仓库的固定背景两人税界，因为反例发生在四人根局。([arXiv](https://arxiv.org/html/2307.07174v2?utm_source=chatgpt.com "Equilibrium Analysis of Customer Attraction Games"))

## 六、完整精确核验代码

下面的代码把客户组展开成不同的单位客户，使用 `Fraction`，核验全部

```math
1+6+6^2+6^3=259
```

个有序决策历史，以及全部 `1295` 个非平凡行动偏离。偏离后始终执行同一份策略的真实续局。

已运行通过；另含单人、空主题、同覆盖不同标签和不交主题的边界测试。

[下载完整核验脚本](sandbox:/mnt/data/rt_counterexample.py)

```python
"""Exact certificate for a four-player root-tax counterexample."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import product

GROUPS = {
    "A": 12, "B": 8, "C": 4, "D": 8,
    "AE": 6, "AF": 6, "CE": 3, "CF": 3,
    "AEF": 6, "BEF": 2, "CEF": 1, "DEF": 2,
}


def expand_groups(groups, labels="ABCDEF"):
    """Each customer is a distinct unit customer."""
    topics = {a: set() for a in labels}
    next_id = 0

    for membership, multiplicity in groups.items():
        if multiplicity < 0 or not set(membership) <= set(labels):
            raise ValueError("Invalid customer group.")

        for x in range(next_id, next_id + multiplicity):
            for a in membership:
                topics[a].add(x)

        next_id += multiplicity

    return topics


def certify(n, topics, early="A"):
    """First n-1 players choose early; last-player ties favor larger labels."""
    if n < 1 or not topics or early not in topics:
        raise ValueError("Invalid game.")

    actions = tuple(sorted(topics))
    universe = set().union(*topics.values())

    @lru_cache(None)
    def payoffs(profile):
        loads = Counter(x for a in profile for x in topics[a])
        return tuple(
            sum(
                (Fraction(1, loads[x]) for x in topics[a]),
                Fraction(0),
            )
            for a in profile
        )

    @lru_cache(None)
    def last_reply(history):
        return max(
            actions,
            key=lambda a: (payoffs(history + (a,))[-1], a),
        )

    def strategy(history):
        if not 0 <= len(history) < n:
            raise ValueError("Expected a nonterminal history.")
        return early if len(history) < n - 1 else last_reply(history)

    def follow(history):
        while len(history) < n:
            history += (strategy(history),)
        return history

    nodes = deviations = 0

    for depth in range(n):
        for history in product(actions, repeat=depth):
            chosen = strategy(history)
            actual = payoffs(follow(history))[depth]
            nodes += 1

            for alternative in actions:
                if alternative == chosen:
                    continue

                # Execute the SAME strategy after the actual deviation.
                changed = follow(history + (alternative,))
                deviation_payoff = payoffs(changed)[depth]

                if deviation_payoff > actual:
                    raise AssertionError(
                        (
                            history, chosen, alternative,
                            actual, deviation_payoff,
                        )
                    )

                deviations += 1

    outcome = follow(())
    W = len(set().union(*(topics[a] for a in outcome)))

    OPT = max(
        len(set().union(*(topics[a] for a in profile)))
        for profile in product(actions, repeat=n)
    )

    prefix_load = Counter(
        x for a in outcome[:-1] for x in topics[a]
    )
    tau = sum(
        (
            Fraction(prefix_load[x], prefix_load[x] + 1)
            for x in universe
        ),
        Fraction(0),
    )

    assert sum(payoffs(outcome)) == W

    return (
        outcome, payoffs(outcome), W, OPT, tau,
        nodes, deviations,
    )


def main():
    # Boundary tests.
    assert certify(
        1, {"A": set(), "B": {0}}
    )[0] == ("B",)

    assert certify(
        4, {"A": set()}
    )[2:5] == (0, 0, Fraction(0))

    assert certify(
        3, {"A": {0}, "B": {0}}
    )[2:5] == (1, 1, Fraction(2, 3))

    assert certify(
        2, {"A": {0}, "B": {1}}
    )[2:5] == (2, 2, Fraction(1, 2))

    topics = expand_groups(GROUPS)
    result = certify(4, topics)

    expected = (
        tuple("AAAF"),
        tuple(map(Fraction, (9, 9, 9, 11))),
        38, 61, Fraction(45, 2),
        259, 1295,
    )
    assert result == expected

    outcome, utilities, W, OPT, tau, nodes, deviations = result

    assert OPT - W - tau == Fraction(1, 2)
    assert W + tau + Fraction(1, 2) == OPT
    assert OPT <= 2 * W

    # A, B, C, D partition all customers.
    assert sum(len(topics[a]) for a in "ABCD") == OPT
    assert len(
        set().union(*(topics[a] for a in "ABCD"))
    ) == OPT

    print("Boundary tests: passed")
    print("Outcome:", "".join(outcome))
    print("Payoffs:", ", ".join(map(str, utilities)))
    print(f"W = {W}; OPT_4 = {OPT}; tau = {tau}")
    print("OPT_4 - W - tau =", OPT - W - tau)
    print(
        f"Verified all {nodes} ordered decision histories "
        f"and {deviations} deviations."
    )


if __name__ == "__main__":
    main()
```

实际输出为：

```text
Boundary tests: passed
Outcome: AAAF
Payoffs: 9, 9, 9, 11
W = 38; OPT_4 = 61; tau = 45/2
OPT_4 - W - tau = 1/2
Verified all 259 ordered decision histories and 1295 deviations.
```

**结论：应当否定（RT）的全称版本。** 这个实例同时满足

```math
\operatorname{OPT}_4=61 < \left(2-\frac14\right)W=\frac{133}{2} < 2W=76,
```

所以它既不反驳半覆盖目标，也不反驳 `2-1/n` 的福利上界；它严格排除的是以题目中这项实际前缀总税 `\tau` 支付全部覆盖损失的全局引理。