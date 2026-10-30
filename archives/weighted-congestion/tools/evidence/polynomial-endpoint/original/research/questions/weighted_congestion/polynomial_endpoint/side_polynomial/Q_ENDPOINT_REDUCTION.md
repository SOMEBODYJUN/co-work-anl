# 保守两攻击证书：副资源多项式的端点还原

## Claim identity

- **ID/version:** WC-R1-Q-ENDPOINT v1.
- **Exact Statement:** 固定整数 $d\ge1,n\ge1$、实数 $0<w\le1$、实数 $\alpha>1$，以及非负系数、次数至多 $d$ 的主资源多项式 $P$。若存在同类副资源多项式 $Q$，使下列两条严格证书成立，则存在 $\beta>0$，使 $Q'(x)=\beta x^d$ 仍使两条证书严格成立。
- **Objects/Domain:** 对称两列 gadget 的费用 $P,Q$；玩家权重为重玩家 $1$、$n$ 个轻玩家 $w$。费用采用 MODEL.md 的不乘玩家权重约定。
- **Quantifiers:** 上述每个 $d,n,w,\alpha,P$；对每个严格可行 $Q$，下文给出显式 $Q'$。$P$ 保持不变。
- **Assumptions/Definitions:** $P,Q\in\mathbb R_{\ge0}[x]$，degree 至多 $d$。证书指
  \[
  P(1)+nQ(1+w)>\alpha\bigl(P(1+nw)+nQ(1)\bigr),\tag{H}
  \]
  \[
  P(1+w)+Q(w)>\alpha\bigl(P(nw)+Q(1+w)\bigr).\tag{L}
  \]
- **Scope/Conclusion:** 扩展副资源为任意非负系数多项式，不会扩大这两条保守证书的严格可行倍率集合。此命题只比较这两条证书；不宣称它们必要于整个 gadget 无近似均衡。
- **Dependencies:** 两条证书来自 arXiv:2002.07466v3 §3 Theorem 1 的两类状态论证，其重建公式由父 agent 提供。端点归约证明独立如下。
- **Evidence:** 完整一般证明；独立内部 agent 对边界、分母、显式系数与权重互换接口进行了复核。另有 exact-rational sanity checker，不替代证明。
- **Counterevidence/Objections:** $w>1$ 时本证明的凸弦方向反转，不能直接沿用本归约；见末尾接口。原文 $\beta\le1$ 与主资源单项式归约不包含在本 claim 中，须由父 agent 另外证明。
- **Status:** 完整内部证明；独立内部复核通过。外部 peer review 与新颖性未认证。
- **Related Files:** `check_q_endpoint.py`；父 agent 的主资源消元资产。

## 显式构造

记 $s=1+w>1$、$A=s^d$。把
\[
Q(x)=\sum_{j=0}^{d}b_jx^j,\qquad b_j\ge0
\]
替换为
\[
\widetilde Q(x)=C+Dx^d,
\]
其中
\[
C=\frac{A Q(1)-Q(s)}{A-1}
 =\sum_{j=0}^{d}b_j\frac{A-s^j}{A-1}\ge0,
\]
\[
D=\frac{Q(s)-Q(1)}{A-1}
 =\sum_{j=0}^{d}b_j\frac{s^j-1}{A-1}\ge0.\tag{1}
\]
因此
\[
\widetilde Q(1)=Q(1),\qquad \widetilde Q(s)=Q(s).\tag{2}
\]
下面证明
\[
\widetilde Q(w)\ge Q(w).\tag{3}
\]

## 三点端点不等式

对 $0<w\le1$，设
\[
\rho=\frac{\log(s/w)}{\log s}\ge1.
\]
对任意 $0\le j\le d$，令 $u_j=s^{-j}$。则
\[
\left(\frac{w}{s}\right)^j=u_j^{\rho}.
\]
函数 $u\mapsto u^{\rho}$ 在正实数上凸，且 $u_j\in[u_d,1]$。因此它在该区间上不高于连接两端点的弦。令
\[
\lambda_j=\frac{u_j-u_d}{1-u_d}\in[0,1].
\]
便有
\[
\left(\frac ws\right)^j
\le\lambda_j+(1-\lambda_j)\left(\frac ws\right)^d.
\]
两边乘以 $b_js^j$，得到
\[
b_jw^j
\le b_j\frac{A-s^j}{A-1}
 +b_j\frac{s^j-1}{A-1}w^d.
\]
对 $j$ 求和即为 $3$。在 $j=0,d$ 处等号成立；$w=1$ 时 $\rho=1$，所有 $j$ 都取等号。故 $d=1$ 与 $w=1$ 边界无须特殊修改。

亦可完全避免对数：对 $0<w<1$ 与 $1\le j\le d$，
\[
\frac{1-w^j}{s^j-1}
=\frac{1-w}{w}\,
\frac{\sum_{i=0}^{j-1}w^i}{\sum_{i=0}^{j-1}s^i}
\ge\frac{1-w^d}{s^d-1}.
\]
最后不等式来自 $w^i/s^i=(w/s)^i$ 严格递减：加入后续项只会减小这个按 $s^i$ 加权的均值。整理后得到相同的单项式不等式。

## 删去常数项

设 $\Delta=\widetilde Q(w)-Q(w)\ge0$。用 $\widetilde Q$ 替换 $Q$ 后，由 $2$，$H$ 的左右两边完全不变，而 $L$ 的左边增大 $\Delta$。然后删去常数 $C$，令
\[
Q'(x)=Dx^d.
\]
若把两条证书的「左边减去 $\alpha$ 倍括号」称为对应 margin，则
\[
M_H(P,Q')=M_H(P,Q)+n(\alpha-1)C,
\]
\[
M_L(P,Q')=M_L(P,Q)+\Delta+(\alpha-1)C.
\]
因为 $\alpha>1,C\ge0,\Delta\ge0$，原来为正的两个 margin 仍然为正。证明完成。

严格可行同时保证构造非退化：由 $P(1+nw)\ge P(1)$ 和 $H$，
\[
n\bigl(Q(s)-\alpha Q(1)\bigr)
>\alpha P(1+nw)-P(1)\ge0,
\]
所以 $Q(s)>Q(1)$，从 $1$ 得到 $D>0$。若 $P\equiv0$，$L$ 将要求 $Q(w)>\alpha Q(s)$，与非负系数的单调性矛盾，故 $P\not\equiv0$。于是在正负载上 $P$ 为正，两种证书的分母在构造前后都严格为正。若需要使用比值 $H,L$，不涉及 $0/0$。

对固定 $P,n,w$，若初始两比值都大于 $1$，该构造实际上使 $H,L$ 各自不减：保持 $Q(1),Q(s)$ 并升 $Q(w)$ 时如此；随后从分子、分母分别删去相同非负量，亦会提高一个大于 $1$ 的比值。严格倍率可行性是本 claim 采用的量词形式。

## 父证明的权重接口（独立核对通过）

本 claim 范围仅为 $0<w\le1$。若父证明还允许 $w>1$，可先处理如下。

不能把「固定原 $P$，直接把原 $Q$ 改为最高次单项式」扩大到 $w>1$：一个精确反例是
\[
n=1,\quad w=2,\quad d=2,\quad P(x)=\frac9{40}x^2,\quad Q(x)=x.
\]
此时 $H=129/121$、$L=161/156$，均严格大于 $51/50$。但若改成 $Q(x)=\beta x^2$，则 $H>1$ 要求 $\beta>9/40$，而 $L>1$ 要求 $\beta<9/40$，故不可同时成立。以下交换接口正是该范围差别的处理。

- $n\ge2$ 时，$nw\ge1+w$，因此 $P(nw)\ge P(1+w)$、$Q(1+w)\ge Q(w)$，$L$ 不可能对任何 $\alpha>1$ 成立。
- $n=1,w>1$ 时，交换两玩家、互换主/副资源费用，并把两权重同除以 $w$。代数上设
  \[
  w'=1/w,\qquad P_{\rm new}(x)=Q(wx),\qquad Q_{\rm new}(x)=P(wx).
  \]
  则 $0<w'<1$，费用仍有非负系数、degree 至多 $d$，而新证书满足
  \[
  H_{\rm new}=L_{\rm old},\qquad L_{\rm new}=H_{\rm old}.
  \]
  因而可先作此变换，再应用上面的 $w\le1$ 归约；这一步会互换 $P,Q$，所以不属于「固定主资源 $P$」的 claim v1。

## 证明意义的限制

此结果是一个精确的失败路线回收：在这两条保守证书内，把副资源扩大到全部非负系数多项式无法得到新倍率。它没有排除利用各状态更紧的偏离倍率、非对称资源、不同轻玩家权重、更多策略、负系数但负载区间非负的费用，或其他 gadget 改善全类下界。


---
整理来源与当前文件用途见[逐文件登记](../../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。
