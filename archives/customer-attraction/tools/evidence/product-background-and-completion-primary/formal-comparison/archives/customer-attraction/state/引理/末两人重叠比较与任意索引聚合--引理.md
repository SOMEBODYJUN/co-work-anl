---
id: "customer-attraction/two-tail-overlap-and-index-aggregation"
kind: "lemma"
type_tag: "引理"
title: "末两人重叠比较与任意索引聚合"
status: "complete"
truth_status: "proved"
review_level: "internal-semantic-review-and-exact-replay"
scope: "任意总人数；任意合法背景；真末两人子局；M个任意可重复比较索引"
summary: "三条真IC保留一份交叠，推出任意比较索引的二阶重数及背景覆盖包络。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:customer_attraction/proofs/half5_exact_v1/PROOF_ZH.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:customer_attraction/proofs/half5_exact_v1/PROOF_ZH.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/customer_attraction/five_player_half_local.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/customer_attraction/five_player_half_local.md"
---

# 末两人保留重叠的强比较与任意索引聚合

## 真节点、量词与强式

采用[完整历史模型](../定义/共同目录完整历史模型--定义.md)。固定任意合法有序历史，之后恰余两人；背景负载$b_x\ge0$。总提供者人数不限，所给完整纯SPE的实际尾部是$(C,D)$。对所有合法$T,Q$（允许相同或为空），定义

$$f(X)=\sum_{x\in X}\frac1{b_x+1},\quad g(X,Y)=\sum_{x\in X\cap Y}\frac1{(b_x+1)(b_x+2)},\quad U(X,Y)=f(X)-g(X,Y),$$

$$H=U(C,D)+U(D,C)+g(C,C).$$

则

$$\boxed{H\ge f(T)+f(Q)-g(T,Q).}\tag{PAIR}$$

它比[普通两人税界](固定背景两人税界--引理.md)的$H\ge f(T)+f(Q)-2g(T,Q)$保留多一份非负交叠信用，强式并不依赖五人定理成立。

## 自足证明

令$R$是同一策略在当前玩家强制$T$后的真实末位回复。三条真IC是

$$I_1=U(C,D)-U(T,R)\ge0,\quad I_2=U(R,T)-U(Q,T)\ge0,\quad I_3=U(D,C)-U(R,C)\ge0.$$

原末位只把$R$作为共同目录的合法查询，没有冻结偏离后的末位主题。直接展开并用$g$对称性得

$$H-f(T)-f(Q)+g(T,Q)=I_1+I_2+I_3+g(C,C)-g(C,R).$$

最后一项是$C\setminus R$上正权求和，故非负。全部IC用弱不等式，覆盖任意离轨平局；零客户时各和为零。

## 任意数量比较索引的精确聚合

取任意整数$M\ge2$和任意合法比较主题$T_1,\ldots,T_M$。索引不去重；令$d_x=\sum_i\mathbf1_{x\in T_i}$。把PAIR对每个$i<j$求和：每个$f(T_i)$出现$M-1$次，每个客户的交叠出现$\binom{d_x}{2}$次，因此

$$\boxed{\binom M2H\ge\sum_x\left[\frac{(M-1)d_x}{b_x+1}-\frac{d_x(d_x-1)}{2(b_x+1)(b_x+2)}\right].}\tag{P-M}$$

这比先换为普通两利润再求和精确强$\sum_x\binom{d_x}{2}/((b_x+1)(b_x+2))$。当$d\ge1$，方括号作为$d\in[1,M]$的凹二次式，其最小值在端点。$d=1$为$(M-1)/(b+1)$；$d=M$与此差为

$$\frac{(M-1)((M-1)(b+2)-M/2)}{(b+1)(b+2)}\ge0.$$

故(P-M)还推出

$$\frac M2H\ge\sum_{x:d_x>0}\frac1{b_x+1},\qquad
\boxed{\frac M2H+\sum_x\frac{b_x}{b_x+1}\ge\left|\bigcup_iT_i\right|.}\tag{COVER}$$

未被比较并集覆盖的客户只给非负背景项。$M=1$应另用真正末位查询，不能除以$M-1$。

## 用途和关系证据

五人主证书的三条`query_equal`PAIR行保留同一菜单索引$i\ne j$上的交叠，不能把$\sum t_ir_i$换成边际乘积。MAXROOT中的$M=5$覆盖包络只需较弱普通两人税，也可由上述强式推出；这两个使用位置的强度应区分。保留强式不代表早期分支利润已经由实际福利共同支付。

后续`research/current/customer_attraction/priced_hidden_reply_projection.md`再次自足提取(P-M)，并把实际末位报价用于任意尾长投影；其一般性不依赖五人主定理。该后续源为相关比较，本批未勾。完整历史、同一策略及背景量词是这些关系的共同前提；阶段三可据此分别记录“强式蕴含普通税”“强式参与五人证书”“一般索引求和”的关系，不按人数排递推链。
