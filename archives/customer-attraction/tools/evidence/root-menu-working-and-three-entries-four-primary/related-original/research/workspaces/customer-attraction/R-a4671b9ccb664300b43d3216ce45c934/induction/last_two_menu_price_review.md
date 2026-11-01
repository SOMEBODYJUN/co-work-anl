# 末两人整张主题价格的盲重构：静态单槽支配与总缺陷预算

2026-10-25。Boss13 本轮一般归纳分支。本文是在只收到陈述、尚未收到证明时独立重构的解析核验；不是一般 half 证明。随后获知并核读旧 `R-e5d83af532dc495c966f99cf70cda2a2/parent_tail/penultimate_price_defect.md`：其组合 slack 去掉倒二当前 IC 后已有更强结论，本核验不认领新端点、新范围或新机制。所用单末位去相关是共享正文 `continuation_security_barriers.md` / `general_half_proof.md` 中已有关系。

## 精确陈述

固定任意合法旧前缀，客户负载为整数 `b_x>=0`，仅剩两名单位玩家。对每个合法主题 `T`，令 `D(T)` 为同一完整策略规定的末位真实最佳回复，并令

\[
 U_b(T,D)=\sum_{x\in T}\frac1{b_x+1+\mathbf1_{x\in D}},
 \qquad d(T)=U_b(T,D(T)).
\]

实际末两主题为 `A,B=D(A)`，实际末位利润为 `u_B=U_b(B,A)`；`W` 是旧前缀与 `A,B` 的完整总覆盖数。定义

\[
 g(T)=\sum_{x\in T}\frac1{(b_x+1)(b_x+2)},\qquad
 B_0=\sum_x\frac{b_x}{b_x+1},\qquad P=\{x:b_x>0\}.
\]

则存在同一客户向量 `0<=y_x<=1`，满足

\[
 \sum_{x\in T}y_x\le d(T)\quad\text{对所有合法主题 }T,
 \qquad \sum_x(1-y_x)\le W-g(A). \tag{1}
\]

因此，对任意实数 `z_T>=0`，不要求其总和、是否覆盖或是否整数，令

\[
 a_x=\sum_{T\ni x}z_T,\qquad F(z)=\sum_x\min(1,a_x),
\]

有

\[
 \sum_Tz_Td(T)\ge F(z)-W+g(A). \tag{2}
\]

这里只要求全部 `D(T)` 为末位最佳回复，不使用倒二玩家当前最优性。任意历史依赖平局均允许。

## 1. 同一整张菜单被一份静态单槽分布支配

写

\[
 f(T)=\sum_{x\in T}\frac1{b_x+1},\qquad
 h(T,D)=\sum_{x\in T\cap D}\frac1{(b_x+1)(b_x+2)},
\]

故 `U_b(T,D)=f(T)-h(T,D)`，且 `h` 对称。对任意目录分布 `p`、独立 `T,T'~p`，末位真实最优性给

\[
 U_b(D(T),T)\ge U_b(D(T'),T).
\]

求期望后两个 `f(D)` 项相消，得到

\[
 \mathbb E h(T,D(T))\le\mathbb E h(T,D(T')),
\]

即

\[
 \mathbb E_p d(T)\ge
 \mathbb E_{T,T'\sim p}U_b(T,D(T')). \tag{3}
\]

对每个 `p`，右端是一份静态末位主题分布的查询期望，所以

\[
 \min_Q\mathbb E_{T\sim p,\,D\sim Q}
       [U_b(T,D)-d(T)]\le0.
\]

有限 minimax 遂给出一份分布 `Q`，使

\[
 \mathbb E_{D\sim Q}U_b(T,D)\le d(T)
 \quad\text{同时对所有 }T. \tag{4}
\]

可以把 `Q` 的支持限制为真实回复集合 `{D(T):T in S}`。令

\[
 y_x=\mathbb E_{D\sim Q}\frac1{b_x+1+\mathbf1_{x\in D}}.
\]

则 `0<=y_x<=1`，且(4)就是(1)的全部主题约束。这是存在一个共同静态分布的代数结论，不是让顺序玩家隐藏执行混合承诺。

## 2. 总价格缺陷由实际覆盖支付

直接展开得

\[
 \sum_x(1-y_x)=B_0+\mathbb E_Qg(D). \tag{5}
\]

对任意合法 `D`，逐客户有

\[
 \frac{\mathbf1_{x\in D}}{(b_x+1)(b_x+2)}
 \le\frac{\mathbf1_{x\in D}}{2(b_x+1+\mathbf1_{x\in A})}
       +\frac14\mathbf1_{x\in A\setminus P}.
\]

当 `b=0,a=1` 时允许的额外四分之一恰支付差；其余情形第一项已足够。由于 `B` 在实际末位节点对 `D` 最优，故

\[
 g(D)\le\frac12 U_b(D,A)+\frac14|A\setminus P|
 \le\frac12u_B+\frac14|A\setminus P|. \tag{6}
\]

再逐客户比较

\[
 B_0+g(A)+\frac12u_B+\frac14|A\setminus P|\le W. \tag{7}
\]

`b=0` 时，实际 `A/B` 成员型 `00,10,01,11` 左端贡献依次是 `0,3/4,1/2,1`，均不超过覆盖指示。`b>=1` 时全部贡献随 `a=1_A,c=1_B` 非减，故只需取 `a=c=1`，此时贡献为

\[
 \frac b{b+1}+\frac1{(b+1)(b+2)}+\frac1{2(b+2)}
 =1-\frac1{2(b+2)}<1.
\]

(5)--(7)给 `sum(1-y)<=W-g(A)`，完成(1)。

## 3. 任意分数权与不可覆盖客户

对 `a>=0, 0<=y<=1`，逐客户均有

\[
 \min(1,a)-ay\le1-y.
\]

当 `a<=1` 时左端为 `a(1-y)`；当 `a>=1` 时左端为 `1-ay`。因此将(1)各主题约束乘 `z_T`，再求和，即得(2)。截断不能换成未截断的 `a_x`，但不要求 `a_x<=1`。

零客户、空主题、重复覆盖标签、不可覆盖客户均不出问题。若客户既无旧负载又不在任何主题，则上式构造给 `y_x=1`、`a_x=0`、总缺陷零。若旧负载为正，该客户已由旧前缀覆盖并计入 `W`。所有客户数有限，所以 LP / minimax 及求和无紧性问题。

## 准确用途与停止点

本核验给末两人菜单的同一主题敏感价格向量及一份共同预算；它仅复核已有末端机制。对三人以上，(3)中的一个末位行动不再代表整个后继团队的合法单一偏离，不能据此将共同价格直接迭代到更早节点。缺失的是不同根孩子整张价格表之间由真实后继 IC 支付的传递关系，而不是最后这一步 LP 对偶。
