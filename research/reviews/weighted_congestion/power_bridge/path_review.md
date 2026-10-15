# 两尺度路径障碍：固定幂乘子的独立重构审查

审查人：`path_obstruction_review`。本报告先在未读取其他成员文件的情况下独立重构，再核对主对话发送的两 cohort 参数。两次尝试读取指定的 `path_obstruction.md` 时，该文件尚未出现；以下比较依据主对话明确给出的公式，不假称已审阅该文件。本报告只修改本文件，未执行 Git。

## 【数学审查】

### 1. 核心结论与精确量词

候选 NO 成立，而且不需要多层权重。对每个固定实数 (p\in[0,1)) 和每个有限 α≥1，都存在一个有限用户集 (I) 及恰好两种正权重，使得不存在任何集合函数 Φ:2^I→ℝ 同时满足

\[
w_i^p W(S\cup\{i\})
\le \Phi(S\cup\{i\})-\Phi(S)
\le \alpha w_i^p W(S\cup\{i\})
\quad(S\subseteq I,\ i\notin S),
\qquad W(S)=\sum_{j\in S}w_j.
\]

也就是

\[
\forall p\in[0,1)\ \forall\alpha\in[1,\infty)\
\exists I\text{ finite}\ \exists(w_i)_{i\in I}>0\
\forall\Phi:2^I\to\mathbb R\
\exists(S,i)\text{ violating an edge bound}.
\]

α<1 时任意非空实例的一条边已经不可能满足约束。允许统一正比例因子 λ>0、甚至允许该因子依赖整个实例，也不能避免障碍：把 Φ 除以 λ 后恢复上述规范化；两条路径预算之比不变。

关键不是限制 Φ 的形式，而是集合函数在两条具有相同起点和终点的添加路径上必须有同一总增量。

### 2. 独立重构：一个大用户已足够

固定 (p\in[0,1))，取整数 (n\ge2)，一个权重为 1 的用户和 (n) 个权重为

\[
\varepsilon=n^{-2/(1+p)}
\]

的用户。令

\[
\delta=\frac{1-p}{1+p}>0,
\qquad D_n=1+\frac{n(n+1)}2\varepsilon^{p+1}
=\frac32+\frac1{2n}.
\]

先添加所有小用户、最后添加大用户的预算为

\[
T_{LH}
=\varepsilon^{p+1}\frac{n(n+1)}2+(1+n\varepsilon)
=D_n+n^{-\delta}.
\]

先添加大用户、再添加所有小用户的预算为

\[
T_{HL}
=1+\sum_{k=1}^n\varepsilon^p(1+k\varepsilon)
=D_n+n^{\delta}.
\]

若所有边约束成立，则分别在 HL 路径累加下界、在 LH 路径累加上界，得到

\[
T_{HL}\le \Phi(I)-\Phi(\varnothing)\le\alpha T_{LH}.
\]

然而

\[
\frac{T_{HL}}{T_{LH}}
=\frac{\frac32+\frac1{2n}+n^\delta}
{\frac32+\frac1{2n}+n^{-\delta}}
\ge\frac{n^\delta}{3}\longrightarrow\infty.
\]

选取整数 (n>\max\{1,(3\alpha)^{1/\delta}\}) 即给出有限反证。对无理数 (p) 不需要舍入权重或把 (p) 有理化：正实权重原本就允许 (n^{-2/(1+p)})。这里的量词是先固定 (p<1)，再选择 (n=n(p,\alpha))，不是在 (p\uparrow1) 时要求统一有限人数。

### 3. 端点与范围

- **(p=0)**：上式完全适用，(ε=n^{-2})、(δ=1)、所有 (h_i=1)。预算比为 ((3/2+1/(2n)+n)/(3/2+1/(2n)+1/n))，仍无界。
- **(p=1)**：存在 α=1 的精确资源势
  \[
  \Psi(S)=\frac12\left(W(S)^2+\sum_{j\in S}w_j^2\right),
  \qquad \Psi(S+i)-\Psi(S)=w_iW(S+i).
  \]
  此时 δ=0，两条路径预算相等。不能把 NO 延伸到此边界。
- 结论否定的是**不依赖权重及人数的统一失真界**。对每个固定有限权重向量，仍可以把上述精确势适当缩放，得到依赖权重比的有限界。证明没有声称单个有限实例对所有有限 α 均不可行。

### 4. 主对话两 cohort 极限：成立且量词可落实到有限人数

主对话参数为 (M) 个权重 1 的用户和 (N) 个权重 ε∈(0,1) 的用户，(q=\varepsilon^p)。令

\[
K=\frac{M(M+1)}2+q\varepsilon\frac{N(N+1)}2,
\quad D=\frac q\varepsilon>1,
\quad s=\sqrt D.
\]

两预算确为

\[
T_{HL}=K+MNq,
\qquad T_{LH}=K+MN\varepsilon.
\]

对每个有限 (M,N\ge1)，AM–GM 给出

\[
K>\frac12(M^2+q\varepsilon N^2)
\ge\sqrt{q\varepsilon}\,MN=s\varepsilon MN,
\]

从而

\[
T_{HL}-sT_{LH}
=(s-1)(s\varepsilon MN-K)<0.
\]

另一方面，令 (N_M=\lfloor M/\sqrt{q\varepsilon}\rfloor)，则 (N_M/M\to1/\sqrt{q\varepsilon})，且

\[
\frac{T_{HL}}{T_{LH}}
\longrightarrow
\frac{1+\sqrt D}{1+1/\sqrt D}=\sqrt D=s.
\]

因此，这两条路径在**固定权重对、允许所有有限正整数人数**时，其预算比的上确界恰为 (s)。若 α<s，极限定义保证存在有限 (M,N) 使路径比大于 α；不需要无限用户实例。若 α=s，这两条路径不产生矛盾。仅凭该路径论证尚不能声称整个势约束的最优统一界等于 (s)；下面给出独立上界证书，补足这一点。

### 5. 固定两类型的 sharp 统一界：一般 (a,b,h_A,h_B)

这部分是另一个独立推导，未依赖其他成员的分片公式。设类型 A 的权重、乘子为 (a,h_A>0)，类型 B 为 (b,h_B>0)。按乘子与权重之比标号，使

\[
\rho_A=\frac{h_A}{a}\le\rho_B=\frac{h_B}{b},
\quad D=\frac{\rho_B}{\rho_A},
\quad s=\sqrt D.
\]

注意 A 未必是权重较大的类型；一般形式的排序依据是 ρ，不能直接按权重大小标号。对 (h=w^p)、(p<1)，较大权重的类型恰为较小 ρ 的 A。

给定集合中的人数 (m,n)，令物理负载 (x=am, y=bn)。定义连续函数

\[
F(x,y)=\frac{\rho_A}{2}
\begin{cases}
x^2+2Dxy+Dy^2,&x\ge sy,\\
s x^2+2sxy+sD y^2,&x\le sy.
\end{cases}
\]

两式在 (x=sy) 上的值及两个偏导数均相同，因此 (F) 在非负象限内为 (C^1)。对所有 (x,y\ge0)，逐区间检查得到

\[
\rho_A(x+y)\le F_x(x,y)\le s\rho_A(x+y),
\]

\[
\rho_B(x+y)\le F_y(x,y)\le s\rho_B(x+y).
\]

例如，在 (x\ge sy) 区间，(F_y=\rho_AD(x+y)=\rho_B(x+y))，且

\[
F_x=\rho_A(x+Dy)
\le s\rho_A(x+y)
\iff (s-1)(x-sy)\ge0.
\]

在另一区间，(F_x=s\rho_A(x+y))；(F_y\ge\rho_B(x+y)) 等价于 ((s-1)(sy-x)\ge0)，上界直接成立。上述界在原点也以连续性成立。

对离散用户集合定义

\[
\Phi(S)=F(am(S),bn(S))
+\frac12\sum_{i\in S}h_iw_i.
\]

添加任一类型的用户 (i)，沿对应坐标线积分偏导数。令原负载为 (W)，则

\[
h_i\left(W+\frac{w_i}{2}\right)
\le F(S+i)-F(S)
\le s h_i\left(W+\frac{w_i}{2}\right).
\]

跨越分片边界时上述积分仍成立，因为 (F\in C^1) 且偏导数界沿整段有效。再加自项 (h_iw_i/2)，得到

\[
h_i(W+w_i)\le\Phi(S+i)-\Phi(S)
\le s h_i(W+w_i),
\]

其中上界使用 (1\le s)。这是一份针对**所有集合、所有加入边、所有有限人数**的构造性上界证书；因而其他循环约束不能迫使统一界超过 (s)。当 (D=1)，两分片合并为通常的精确势。

一般类型的路径预算也有完全对应的下界。令

\[
K_{M,N}=h_Aa\frac{M(M+1)}2+h_Bb\frac{N(N+1)}2.
\]

A 后 B 的预算为 (K_{M,N}+ah_BMN)，B 后 A 为 (K_{M,N}+bh_AMN)。若 (D>1)，取

\[
N_M=\left\lfloor\frac{a}{sb}M\right\rfloor,
\]

则两预算之比从有限实例趋近 (s)。因此可准确表述为：

> 固定两个正权重和两个正乘子，对于 (c(W)=W)，在全部有限两类型人数实例上，满足上述边际夹逼的最小统一 α 恰为 (√{(\max h/w)/(\min h/w)})。这是跨全部有限人数的统一最优界，不是每一个固定有限权重向量的最优值。

单个有限实例可能有更小最优值。这里的构造有 (s) 的上界、密集路径族有趋近 (s) 的下界，两者正好核准上述量词。

### 6. 非负仿射延迟的推广与例外

对 (c(W)=\ell W+\beta)、(ℓ,β\ge0)，令

\[
\Phi_{\ell,\beta}(S)
=\ell\left(F(am(S),bn(S))+\frac12\sum_{i\in S}h_iw_i\right)
+\beta\sum_{i\in S}h_i.
\]

常数部分的边际恰为 β(h_i)，因此同样得到 ([1,s]) 夹逼。

- 若 ℓ>0，固定 β 后，密集路径预算中的线性负载项是 (\Theta(M^2))，常数延迟项为 (O(M))，路径比仍趋近 (s)。跨全部有限人数的最优统一界仍是 (s)。
- 若 ℓ=0，精确势为 β(\sum_{i\in S}h_i)，最优统一界为 1；零延迟情形也可取 α=1。不能把 (s>1) 的 sharp 下界声称用于纯常数延迟。
- 上述推广明确要求非负系数。负 β 时，“常数部分可被 (s) 倍吸收”的上界步骤不能直接使用；本报告不作该推广。

### 7. 与纯纳什均衡存在性的关系：不能读成非存在结果

在有限标准加权拥塞游戏中，设玩家 i 的总成本为

\[
C_i^{(p)}(s)=w_i^p\sum_{e\in s_i}c_e(W_e(s)).
\]

则

\[
C_i^{(p)}(s)=w_i^{p-1}C_i^{(1)}(s).
\]

乘子是正数，并且与玩家的策略、资源、其他玩家的行动无关，所以每一玩家的严格改善和最佳反应不变，纯纳什均衡集合相同。对 (c_e(W)=\ell_eW+\beta_e)，标准 (p=1) 模型的精确势为

\[
\Psi(s)=\sum_e\left[
\frac{\ell_e}{2}\left(W_e(s)^2+\sum_{j:e\in s_j}w_j^2\right)
+\beta_eW_e(s)\right].
\]

一个玩家的偏离满足

\[
\Psi(s'_i,s_{-i})-\Psi(s)
=C_i^{(1)}(s'_i,s_{-i})-C_i^{(1)}(s)
=w_i^{1-p}\bigl(C_i^{(p)}(s'_i,s_{-i})-C_i^{(p)}(s)\bigr).
\]

因而 Ψ 也是 (p) 模型的加权势／改善势。有限策略空间的全局极小点给出精确纯纳什均衡。资源边际按预先指定 (h_i) 和同一全局比例夹逼失败，并不意味着没有其他势或没有精确 PNE；这里恰有后者。

一手事实核查：Harks、Klimm、Möhring 的 [SAGT 2009 论文正式出版页面](https://link.springer.com/chapter/10.1007/978-3-642-04645-2_10) 摘要明确给出标准 weighted congestion games 对 affine costs 具有 exact potential；作者所属机构的 [2011 正式论文记录](https://www3.math.tu-berlin.de/disco/research/publications/?author=Max+Klimm) 列出 *Theory of Computing Systems* 49(1):46–70，DOI [10.1007/s00224-011-9315-x](https://doi.org/10.1007/s00224-011-9315-x)，并给出同一结论。文中公式的成本约定由本报告的边际恒等式独立核验，不仅凭摘要推断。尝试读取机构 PDF 链接未成功；因此没有声称核验了该 PDF 的某页公式。

### 8. 精确 Fraction 复验

对 (p=1/2)，取整数 (k\ge2)，令 (n=k^3)、(ε=k^{-4})，则 (h_\varepsilon=k^{-2})，所有权重、乘子、预算都是有理数。独立逐步添加计算与闭式完全一致：

\[
T_{LH}=\frac32+\frac1{2k^3}+\frac1k,
\qquad T_{HL}=\frac32+\frac1{2k^3}+k,
\qquad \frac{T_{HL}}{T_{LH}}\ge\frac k3.
\]

| (k) | 小用户数 | 小权重 | (T_{LH}) | (T_{HL}) | 比值 |
|---:|---:|---:|---:|---:|---:|
| 2 | 8 | 1/16 | 33/16 | 57/16 | 19/11 |
| 3 | 27 | 1/81 | 50/27 | 122/27 | 61/25 |
| 4 | 64 | 1/256 | 225/128 | 705/128 | 47/15 |
| 8 | 512 | 1/4096 | 1665/1024 | 9729/1024 | 1081/185 |
| 16 | 4096 | 1/65536 | 12801/8192 | 143361/8192 | 2811/251 |

此外，在 (k=2,3,4,8)、(0\le m\le8)、(0\le n\le2k^3+3) 的网格上，精确检查了分片势的 **22,284 条加入边**，包括分片边界两侧及跨界加入，全部通过。另用四个非同型有理权重检查了标准 affine exact potential 的全部 **32 条布尔格加入边**，全部通过。数值枚举作为公式复验；全实数 (p) 的结论依据解析证明。

## 【修改建议】

1. NO 命题可直接采用第 2 节的一个大用户族；它覆盖整个实数区间 (0\le p<1)，不需要多层参数或分开处理无理 (p)。
2. 候选原本两 cohort 公式无需修改；应将“极限给出反例”改成“若 α<s，存在足够大的有限人数使路径比大于 α”，并显式给出 (N_M=\lfloor M/\sqrt{q\varepsilon}\rfloor)。
3. 若采用 `WC-R2-AFFINE-TWO-TYPE v1`，建议把 sharp 命题量词固定为“固定权重和乘子类型、允许任意有限 multiplicities 的最小统一界”；不要写成每个固定向量的最优 α 都等于 (s)。
4. 一般 (a,b,h_A,h_B) 的分片应按 (h/w) 标号，以**物理负载** (x=am,y=bn) 为变量；把人数直接当负载将漏掉 (a,b) 因子。分片修正项是 1/2(\sum h_iw_i)，不是 1/2(\sum h_i)。
5. 仿射版本保留 ℓ,β≥0 的假设，并把 ℓ=0 的 sharp 值 1 单独列出。
6. 在原 PNE 问题旁明确写出正比例策略不变性与 (p=1) 精确势；该障碍只否定特定资源边际夹逼，不能作为 d1 纯均衡非存在结论。

## 【论文版本】

**命题（线性资源的统一边际夹逼障碍）。** 设资源延迟 (c(x)=x)，玩家权重为正实数，且给定 (h_i=w_i^p)。对于每个 (p\in[0,1))，不存在只依赖 (p) 的有限常数 α，使得对任意有限用户集及任意正权重向量，均存在集合函数 Φ 满足

\[
h_i c(W(S\cup\{i\}))\le
\Phi(S\cup\{i\})-\Phi(S)\le
\alpha h_i c(W(S\cup\{i\}))
\quad(S\subseteq I,\ i\notin S).
\]

**证明。** 固定 (p\in[0,1))，记 (δ=(1-p)/(1+p)>0)。对整数 (n\ge2)，取一个权重 1 的用户及 (n) 个权重 (ε=n^{-2/(1+p)}) 的用户。从空集到全体用户集合，先大后小和先小后大的两条添加路径的预算分别为

\[
T_{HL}=\frac32+\frac1{2n}+n^\delta,
\qquad T_{LH}=\frac32+\frac1{2n}+n^{-\delta}.
\]

若上述夹逼成立，则路径累加给出 (T_{HL}\le\alpha T_{LH})。但 (T_{HL}/T_{LH}\ge n^\delta/3\to\infty)，与任何固定有限 α 矛盾。证毕。

**推论（固定两类型的仿射统一界）。** 固定 (a,b,h_A,h_B>0)，令 (ρ_A=h_A/a)、(ρ_B=h_B/b)，并按 (ρ_A\le\rho_B) 标号。对 (c(W)=\ell W+\beta)、(ℓ>0,β\ge0)，在全部有限两类型人数实例上，上述边际夹逼的最小统一常数恰为

\[
\sqrt{\rho_B/\rho_A}.
\]

下界由 (N_M/M\to a/(b\sqrt{\rho_B/\rho_A})) 的两条添加路径给出；上界由第 5、6 节的 (C^1) 分片二次势及离散自项修正给出。若 ℓ=0，则精确势为 β(\sum h_i)，统一常数可取 1。该推论的 sharp 值指跨全部有限人数的统一界。

**说明。** 以上命题不否定线性或仿射加权拥塞游戏的精确纯纳什均衡存在性。成本 (C_i^{(p)}=w_i^{p-1}C_i^{(1)}) 与标准加权成本具有相同改善关系，而后者有精确势。(p=1) 时资源边际夹逼本身也可取 α=1。

### 可直接执行的复验代码

```python
from fractions import Fraction as Q


def path_budget(k, heavy_first):
    small = (Q(1, k**4), Q(1, k**2))
    items = [small] * k**3
    items = ([(Q(1), Q(1))] + items
             if heavy_first else items + [(Q(1), Q(1))])
    load, budget = Q(0), Q(0)
    for weight, multiplier in items:
        load += weight
        budget += multiplier * load
    return budget


def two_type_potential(m, n, eps, q, s):
    d, y = q / eps, eps * n
    if m >= s * y:
        continuous = (m*m + 2*d*m*y + d*y*y) / 2
    else:
        continuous = (s*m*m + 2*s*m*y + s*d*y*y) / 2
    return continuous + (m + q*eps*n) / 2


for k in (2, 3, 4, 8, 16):
    diagonal = Q(3, 2) + Q(1, 2*k**3)
    low, high = diagonal + Q(1, k), diagonal + k
    assert path_budget(k, False) == low
    assert path_budget(k, True) == high
    assert high / low >= Q(k, 3)
    print(k, k**3, low, high, high / low)

edges = 0
for k in (2, 3, 4, 8):
    eps, q, s = Q(1, k**4), Q(1, k**2), Q(k)
    for m in range(9):
        for n in range(2*k**3 + 4):
            phi = two_type_potential(m, n, eps, q, s)
            heavy_delta = two_type_potential(m+1, n, eps, q, s) - phi
            small_delta = two_type_potential(m, n+1, eps, q, s) - phi
            heavy_cost = m + 1 + eps*n
            small_cost = q * (m + eps*(n+1))
            assert heavy_cost <= heavy_delta <= s*heavy_cost
            assert small_cost <= small_delta <= s*small_cost
            edges += 2
    for M in (1, 10, 100, 1000):
        N = M * k**3
        diagonal = Q(M*(M+1), 2) + q*eps*Q(N*(N+1), 2)
        low = diagonal + M*N*eps
        high = diagonal + M*N*q
        assert high / low < s
    print("fixed pair", k, "last dense ratio", high / low)
assert edges == 22284
print("piecewise potential edges:", edges)

weights = (Q(1, 9), Q(2, 3), Q(5, 2), Q(7, 4))
slope, intercept = Q(3, 7), Q(5, 11)


def exact_affine_potential(users):
    load = sum((weights[i] for i in users), Q(0))
    squares = sum((weights[i]**2 for i in users), Q(0))
    return slope * (load*load + squares) / 2 + intercept*load


edges = 0
for mask in range(1 << len(weights)):
    users = {i for i in range(len(weights)) if mask >> i & 1}
    for i, weight in enumerate(weights):
        if i in users:
            continue
        final_load = sum((weights[j] for j in users), Q(0)) + weight
        delta = exact_affine_potential(users | {i}) - exact_affine_potential(users)
        assert delta == weight * (slope*final_load + intercept)
        edges += 1
assert edges == 32
print("exact affine edges:", edges)
```

独立检查贡献：单个大用户的全实数 (p) 反例重构；两 cohort 有限量词与严格有限比值界；一般 (h/w) 排序下的分片势推导及跨边界积分检查；sharp 命题范围与纯常数仿射例外；资源障碍与 PNE 存在的逻辑分离；有理数逐边复验与一手出版事实核查。


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
