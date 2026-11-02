---
id: customer-attraction/equal-solitary-payoff-two-player-root-dominates-iid
kind: lemma
type_tag: 引理
title: 等单独收益目录的两人首位与任意iid人数比较
status: proved-for-equal-solitary-payoffs;general-extra-iid-not-inferred
summary: 同一固定背景下所有合法主题的单独收益相等时，任意完整两人纯SPE首位恰得全局最小交叠损失后的共同收益，支配任意至少两人同分布独立抽样的单人期望。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-75bfd8f0f91740408bf08f0c9f5e2aa1/iid_extra_slot/child/README.md#已证：两人、等单独收益背景子类
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-75bfd8f0f91740408bf08f0c9f5e2aa1/iid_extra_slot/child/README.md
---

# 等单独收益目录的两人首位与任意iid人数比较

固定[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)的一个合法有序前缀，客户有限、提供者和客户单位权、共同目录有限非空。前缀给客户负载 $b_x\in\mathbb Z_{\ge0}$，之后**恰有两名真实顺序玩家**。完整纯SPE在每个合法首动作后都规定真实末位最佳回复；重复、空主题、同覆盖不同标签、零客户与任意历史平局均保留。以下甚至只需非负背景，但不借此改变原模型。

令
\[
 f_b(A)=\sum_{x\in A}\frac1{b_x+1},\qquad
 h_b(A,B)=\sum_{x\in A\cap B}\frac1{(b_x+1)(b_x+2)}.
\]
增加两个真实行动 $A,B$ 后，两人的终局利润分别为
\[
 U_b(A,B)=f_b(A)-h_b(A,B),\qquad
 U_b(B,A)=f_b(B)-h_b(A,B). \tag{1}
\]
这是[固定背景两人税界](固定背景两人税界--引理.md)中相同的逐客户身份；此处增加的关键假设是
\[
 f_b(A)=K\quad\hbox{对全部合法主题 }A. \tag{E}
\]
不是只要求实际两题或某个查询分布的支持满足(E)。

## 全部完整两人SPE的首位值

有限目录使 $h_*:=\min_{A,B}h_b(A,B)$ 达到。取达到它的一对 $A_*,B_*$。在首位选 $A_*$ 的真实末节点，由(E)和(1)，所有末位最佳回复都最小化 $h_b(A_*,B)$，故都给首位 $K-h_*$。这一保证不依赖末位如何在最优行动间平局选择。

所给SPE的首位可以偏离为 $A_*$，所以其实际终局收益 $u\ge K-h_*$。另一方面，任意两人终局的首位收益都为 $K-h_b(A,B)\le K-h_*$。因此更准确地
\[
 \boxed{u=K-h_*\quad\text{对每份完整两人纯SPE成立}.} \tag{2}
\]
原README写出所需的下界；(2)的另一方向只是同一全局最小值定义给的上界，不增加任何策略选择假设。

## 与任意至少两人iid抽样的比较

固定**任意**主题分布 $q$，不先假设它是Nash。辅助静态 $n\ge2$ 人各独立同分布抽题，令 $V_n(q;b)$ 为任意一位的期望均分利润。耦合全部抽样，删掉第3至第n位后，每个客户的分母逐点不增加，所以
\[
 V_n(q;b)\le V_2(q;b)
 =\mathbb E_{A,B\,\mathrm{iid}\,q}[K-h_b(A,B)]
 \le K-h_* =u. \tag{3}
\]
这里只比较同一个 $q$ 的不同静态人数，不声称不同人数的Nash分布相同。特别地，对辅助静态n人游戏的任一对称iid Nash分布，(3)给 $u\ge\lambda_n(b)$。其存在与共同值良定来自[合法背景iid值](../定理/合法前缀残余独立同分布价值与租金--定理.md)；本引理的比较本身无需求解它。真实两人对应额外一人的目标是 $u\ge\lambda_3(b)$。

另保原README的一人边界：余一名真实玩家在任意合法背景得 $\max_Af_b(A)$；任意两人iid分布的单人期望不超过同q的单独收益平均，故不超过该最大值。这个 $r=1$ 结论无需(E)。零客户或全空目录给全部量0；如果目录包含空主题而(E)成立，则 $K=0$，同样无例外。

## 不等单独收益、后续纠错与复用

一般目录末位最大化的是 $f_b(B)-h_b(A,B)$，不同 $B$ 的第一项不能消掉。因此不能把本证明的“最小交叠”替换成一般最佳回复，也不能只从一个两人静态PNE推出额外人数的iid封顶。

同一README的262单位客户hub例已完整保于[支持外枢轴分离族](../反例/支持外枢轴修复与静态查询平均的两人分离族--反例.md)：$\lambda_3=997/24>\theta_2=83/2$，但真实根可选H保证 $105/2$，所以它只否定 “$\lambda_3\le\theta_2$” 和支持查询直接平均的辅助桥。此例H的单独收益70、每周边主题59，不满足(E)。README另指向循环静态PNE族，其准确原对象是源 `3d55722d798eb4bff9df`；该族给低于$\lambda_3$的静态PNE，未给低根的完整两人SPE，不能据导航把它当作本引理反例。

README在2026-10-23写一般extra-slot仍OPEN仅属当时状态。一般全背景、全剩余人数的EI后来已被[七客户三人银行根](../反例/额外一人iid收益桥的七客户银行根反例--反例.md)及较大银行族否定；本引理的等f子类与一人边界仍成立。本三源没有解决一般不等f的两人EI，也没有证明六人half。

本批完整阅读README与其两个原程序；程序的有限核验不承担(2)或(3)的全称证明，详[实现合同](../程序/子集枢轴两人族的组合计数与逐客户有理审计--程序.md)。原件、来源指纹、实际运行及关系判断见[证据目录](../../tools/evidence/extra-iid-two-player-child-primary/README.md)。
