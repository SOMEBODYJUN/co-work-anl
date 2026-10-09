# Customer attraction：顺序福利猜想的文献桥梁审查

审查日期：2026-10-09。这里只登记一手来源及导入边界；没有声称解决猜想。
本轮对象与仓库原有“设施先同时选址、战略客户随后作负载均衡”的模型不同。

## 目标与原文范围

**Conjecture（本轮精确版本）**：有限单位客户集 \(N\)，\(m\) 名单位权玩家共享有限主题目录 \(\mathcal S\subseteq2^N\)，按固定顺序各选一次。每个已覆盖客户在其覆盖者间均分；
\[
u_i(a)=\sum_{q\in a_i}\frac1{c_q(a)},\qquad
W(a)=\left|\bigcup_i a_i\right|.
\]
任取纯 SPE 的完整历史依赖策略，允许每个历史独立选择并列最优行动，欲证
\(W(a)\ge\mathrm{OPT}_m/2\)。

**Paper Fact**：[Deng 等，arXiv:2307.07174v2](https://arxiv.org/html/2307.07174v2)
§2 定义模型，§5 Definition 4 对所有前缀定义 SPE；Theorem 5.2 给两名单位权玩家的 \(sPoA=3/2\)，Example 2 给共同目录下界 \(2-1/m\)。§6 提出超过两人时上界 2 的猜想。

**Interpretation**：§6 那一句没有重新写出目录相同的限制；Theorem 5.2 的 “i.e.” 也只列玩家数与单位权。本页研究的是上面明确的共同目录子类版本，不能把对异构目录的证据直接当作其反例。

## 真正相关的定理及其导入条件

| 一手来源与位置 | Paper Fact：精确条件与结论 | Interpretation：本轮能否导入 |
| --- | --- | --- |
| [Vetta, FOCS 2002](https://web.mit.edu/6.454/www/www_fall_2004/gametheory/VettaNashEquilibria.pdf)，§2 的 valid utility 条件，§3 Theorem 5（PDF 第 5 页） | 社会效用为单调次模集合函数；个人效用至少等于移除该玩家的社会损失；个人效用之和至多社会效用。**静态** Nash 均衡满足 \(\mathrm{OPT}\le(1+\delta)W\le2W\)。 | 单位权 CAG 的行动博弈满足这些条件；但顺序 SPE 的终局可能不是该行动博弈的 NE。下面的四客户证书已排除此桥梁。 |
| [Brethouwer, UT master thesis, 2018](https://essay.utwente.nl/76986/1/Brethouwer_MA_EEMCS.pdf)，§6.2 Definition 6.15（印刷页 33），§7 Theorem 7.6（页 41） | 文中 generalized market sharing games 要求目录 downward-closed；equal-sharing covering games 去掉该要求。后者允许任意玩家目录。Theorem 7.6 只对**对称 singleton congestion**，且资源收益匿名、随人数非增，给出每个 SPE 终局为 NE。 | 一名玩家“选一个主题”不等于“只选一个客户资源”。覆盖多个客户的主题不满足 singleton 条件。不能用该定理证明任意主题目录的上界。 |
| [Ben-Porat–Tennenholtz, Shapley Facility Location Games, 2017](https://arxiv.org/pdf/1709.10278)，§2 Definition 1、§4.3 Theorem 3（PDF 第 10 页） | 模型为紧用户空间 \(U\)、总质量 1 的密度、取值 \([0,1]\) 的 Riemann 可积相似度、所有玩家共同位置空间 \(U\) 及 Shapley attraction；纯静态 PoA 上界为 \((2m-1)/m\)。 | 二元“感兴趣/不感兴趣”的均分是覆盖合作博弈的 Shapley 分配，见下述直接推导。该文给的是静态均衡定理，不能由 Shapley 名称推出任意 SPE 的福利保证。 |
| [de Jong–Uetz, WINE 2014](https://marcuetz.personalweb.utwente.nl/Preprints/wine2014.pdf)，§1，§3 Theorems 1–2 | 原子拥塞、非负仿射成本 \(d_r+w_r k\)、各玩家最小化资源成本总和；两人 \(sPoA=3/2\)，三人 \(2+63/488\)。 | CAG 的利润项 \(1/k\) 不是非负仿射成本。改符号、加常数也不保持福利比值，见下文。数值相似不构成模型归约。 |

### 四人超过 2 的文献报告：只可作导入警示

**Paper Fact**：Brethouwer §6.2.4 Theorem 6.22（印刷页 38）报告 equal-sharing covering games 的四人下界
\(sPoA\ge2.0558498235\ldots\)，28 个资源，各玩家策略数按 \(2,3,4,5\) 构造；未展示资源—行动矩阵。
公开的 [WINE 2018 一页摘要](https://ris.utwente.nl/ws/files/101071923/Abstract.pdf)
也没有该矩阵；[官方成果记录](https://research.utwente.nl/en/publications/analysis-of-equilibria-for-generalized-market-sharing-games/)
将其列为 poster。

**Interpretation**：这不是共同目录反例，也不是本轮独立复现的数值证书。
没有原矩阵，无法重算其全部 SPE，更无法检验将所有玩家目录合并后的新偏离。
本文不以这个报告提升或降低本轮猜想的真值状态。

## 可独立复核的桥梁失败证书

### 共同目录 SPE 终局可以不是 PNE

Claim ID：`CA-SPE-NON-PNE`。状态为本轮直接构造、精确独立核验的反例；
没有外部同行评审记录。它攻击的是 SPE→PNE 的桥梁，不攻击 `Q-CAG-HALF`。

**Interpretation / exact calculation**：以下是单位客户版的小证书，受到 Brethouwer Example 6.5（印刷页 28）的并列延续机制启发，所有行动与收益在本轮重新计算。

令 \(N=\{a,b,c,d\}\)，共同主题为
\[
X=\{a,b\},\quad Y=\{c,d\},\quad Z=\{b,c,d\}.
\]
两名玩家依次行动。第二名玩家的完整规则为
\(\sigma_2(X)=Z,\ \sigma_2(Y)=X,\ \sigma_2(Z)=Z\)。

| 首人行动 | 次人选择 | 次人的该选择收益 / 最优收益 | 首人最终收益 |
| --- | --- | --- | --- |
| \(X\) | \(Z\) | \(5/2\) / \(5/2\) | \(3/2\) |
| \(Y\) | \(X\) | \(2\) / \(2\) | \(2\) |
| \(Z\) | \(Z\) | \(3/2\) / \(3/2\) | \(3/2\) |

第二人每个历史均选最优；第一人严格偏好 \(Y\)，因此这是完整纯 SPE。
终局 \((Y,X)\) 下，若固定次人的终局行动 \(X\)，第一人改选 \(Z\) 得
\(u_1(Z,X)=5/2>2=u_1(Y,X)\)。终局不是 PNE。
此例 \(W=\mathrm{OPT}_2=4\)，**没有**否定福利猜想。

两处 ties 对上面的规则有用：在 \(Y\) 后，\(X,Z\) 都给第二人收益 2；在 \(Z\) 后，\(X,Z\) 都给收益 \(3/2\)。同一静态并列关系的选择随历史改变。

### Shared misery 的收益保证条件失效

Brethouwer Definition 7.2 要求：后来者一旦降低早先玩家收益，该早先玩家的新收益至少为后来者的即时收益。
本证书历史 \((Y,Z)\) 给
\[
u_1(Y)=2>u_1(Y,Z)=1<2=u_2(Y,Z).
\]
因此该共同目录 CAG 不是 shared misery game，不能套其 Lemma 7.4 的 payoff guarantee。

### 合并目录不保留原 SPE

这是另一项独立计算。两名玩家原目录分别只有 \(A=\{a\}\) 和
\(B=\{b,c,d\}\)，原 SPE 唯一终局为 \((A,B)\)。合并为共同目录 \(\{A,B\}\) 后，
第一人若选 \(B\)，第二人严格偏好 \(B\)（收益 \(3/2>1\)）；
第一人因而也严格偏好 \(B\)（\(3/2>1\)）。原终局不能保留为 SPE。
所以四人异构例即使补齐数据，也仍需重新验证对称化，不能只统一策略标签。

## 结构匹配为何还不够

**Interpretation / direct derivation**：固定主题行动 \(a\) 后，给每个客户定义合作价值
\(v_q(T)=\mathbf1\{T\cap\{i:q\in a_i\}\ne\varnothing\}\)。在随机玩家排列中，覆盖者 \(i\) 成为第一个覆盖者的概率为 \(1/c_q(a)\)，因此该客户的 Shapley 分配恰为 CAG 均分。
此外
\[
u_i(a)\ge W(a)-W(a_{-i}),\qquad \sum_i u_i(a)=W(a),
\]
覆盖福利单调次模。这只核实静态结构。

静态有效效用论证需要固定 \(a_{-i}\) 比较
\(u_i(a)\ge u_i(a_i^*,a_{-i})\)。SPE 给的是
\(u_i(a)\ge u_i(h_i,a_i^*,\text{该历史下的后续策略})\)，后续行动可随偏离改变。
上面的四客户证书正好显示前一种不等式不能由后一种推出。
把完整策略列表当作静态行动也没有自动修复：一张列表变动会改变后来者实际执行的主题，
不能直接沿用“每个行动固定对应一个资源子集”的有效效用验证。

拥塞成本变换也需检查目标。取 \(d_q(k)=M-1/k\) 时，玩家成本为
\(M|a_i|-u_i(a)\)，主题大小不同时连行动偏好都可能改变。
即使所有主题等大小 \(K\)，总成本为 \(mMK-W\)，成本近似倍率 \(R\) 只给
\[
W_{\mathrm{SPE}}\ge R\,\mathrm{OPT}_m-(R-1)mMK,
\]
不能自动给 \(W_{\mathrm{SPE}}\ge\mathrm{OPT}_m/2\)。

## 本轮核验与仍开放的义务

- Python `fractions.Fraction` 独立计算了四客户证书的全部九个终局收益；核验每个历史的次人最优性、首人的三种延续收益及静态改善 \(2\to5/2\)。这验证一个桥梁失败证书，不是普遍福利证明。
- 已核对 §6.2.4 公开材料的目录条件和缺失数据。未重建四人 LP，未认证其浮点下界，更未认证对称化。
- 本轮没有找到可直接覆盖“任意 \(m\)、任意共同主题目录、所有历史依赖纯 SPE”的文献定理。未找到不等于证明不存在；目标仍须新的延续收益论证或直接反例。

可重算四客户证书的最小代码：

```python
from fractions import Fraction as F
S = [{0, 1}, {2, 3}, {1, 2, 3}]  # X, Y, Z
reply = [2, 0, 2]
def u(x, y):
    return sum((F(1, 2) if q in y else F(1)) for q in x)
for a, x in enumerate(S):
    assert u(S[reply[a]], x) == max(u(y, x) for y in S)
assert [u(x, S[reply[a]]) for a, x in enumerate(S)] == [F(3, 2), F(2), F(3, 2)]
assert u(S[2], S[0]) == F(5, 2) > u(S[1], S[0])
```

