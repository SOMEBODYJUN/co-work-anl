---
id: unrelated-machines/original-token-m1-lift-and-global-context-capacity-psd
kind: proof
type_tag: 证明
title: 原任务标签提升的一阶PSD与全语境容量块
status: proved-conditional-moment-identities; necessary-block-not-sufficient
legacy_ids: [UM-ANONYMOUS-TOKEN-M1-LIFT-M2-NONEXTENSION-v1]
summary: 一共同degree4 functional下的形式不放回标签提升保M1，原身份共同M2另必须满足完整head乘context PSD；全局affine语境可含本组标签，不把单个交叉块称PSD。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/anonymous_token_label_lift_and_nonextension_review.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/anonymous_token_label_lift_and_nonextension_review.md
---

# 原任务标签提升的一阶PSD与全语境容量块

本页展开本批匿名标签review所实际核过的数学。已取并读当前canonical SHA dd3a012c9e24eb64a6ddc4f8e953ccc787aa27cc8a6945a454af2357d5689fb8的**§7、112–304行**，另全文读faa5abd3f4efc8e514a74750b9d7f31f858794e7af23b449b5a8c900a82a6c79的affine-context学习稿；旧前缀只核字节，不冒称本批重新审过。现有[根树流冻结审查](../审查/根树流环正规化与有向需求桥冻结审查--审查.md)§3.4已述这项结论；本页展开一般M1公式与完整SOS，不另称新发现。历史先验、精确非扩展点及软件范围另见[双Schur审查](../审查/匿名标签四次非扩展的双Schur证据与冻结范围--审查.md)。

## 一个共同functional与形式核

有限多个组$g$，显式整数$k_g\ge1$、$0\le r_g\le k_g$，$h_g=k_g-r_g$。Boolean活跃量$A_g$、匿名head $X_{g,w}$及不参与标签置换的Boolean contexts，共用**一个**次数至多四的线性functional $L$，$L1=1$，以次数$\le2$单项式为指标的共同$M_2\succeq0$。Boolean/one-hot等式及

$$X_{g,w}A_g=X_{g,w},\qquad \sum_wX_{g,w}=r_gA_g$$

均乘到总次数四。不同组/行分别可行的projection不够。

每组恢复$k_g$个不同原标签$a$，home变量$t_{g,a}$、head变量$x_{g,a,w}$。先Boolean化请求；同原任务被要求两个不同端、或两个原标签同占一个匿名head则该单项式取零。合法请求在一组含$t\ge1$个不同head/标签及$s$个另留home标签，替换为

$$\frac{(h_g)_s}{(k_g)_{s+t}}\prod_{w\ {\rm requested}}X_{g,w}.$$

若只有$s\ge1$个home请求则为$1-[1-(h_g)_s/(k_g)_s]A_g$，空请求为一。跨组相乘，context不动，再作用$L$得$L'$；下降阶乘分母不为零，因为合法不同标签总数$\le k_g$，分子可零。总次数不增。真Boolean law下它是均匀不放回注入标签；伪矩下不能由“像抽样”推出完全正性。

## 一般M1保持的标签平均与对比分解

省组下标。$k\ge2$时，除对角等于一阶矩外，

$$L'x_{a,w}=LX_w/k,\quad L't_a=1-rLA/k,$$
$$L'x_{a,w}x_{b,v}=LX_wX_v/[k(k-1)]\quad(a\ne b,w\ne v),$$
$$L'x_{a,w}x_{b,w}=L'x_{a,w}x_{a,v}=L't_ax_{a,w}=0\quad(a\ne b,w\ne v),$$
$$L't_ax_{b,w}=hLX_w/[k(k-1)]\ (a\ne b),$$
$$L't_at_b=1-LA+h(h-1)LA/[k(k-1)]\ (a\ne b).$$

$k=1$改用线性替换$t=1-rA,x_w=X_w$，不使用$k-1$分母。

写类别计数$n_0=k-rA$、$n_w=X_w$，$\sum_c n_c=k$。任意恢复后单变量线性多项式按标签分成平均与contrasts，后者系数$d_{a,c}$满足$\sum_a d_{a,c}=0$。平均为原聚合变量的线性式，平方由共同$M_1$非负；跨组contrast及contrast与平均/未动context的交叉项按均匀系数相消。单组contrast平方为

$$\frac1{k(k-1)}\sum_a
\left[k\sum_c d_{a,c}^2Ln_c-L\left(\sum_cd_{a,c}n_c\right)^2\right]
=\frac1{k(k-1)}\sum_a\sum_{c<e}(d_{a,c}-d_{a,e})^2L(n_cn_e)\ge0.$$

不同head有$LX_wX_v=L[(X_wX_v)^2]\ge0$；home/head有$L(n_0X_w)=hLX_w\ge0$。等式只用共同计数/Boolean ideal到四次，不假定隐藏真实条件law。因此$L'$在常数、所有恢复原单变量和未动context单变量上的$M_1$ PSD，涵盖多组、$r=0,r=k,k=1$。

若另有native行的活跃量等于incoming-unit总和、head容量零对矩，则原行一阶/同行二阶还可由inactive全home、active按incoming边缘并均匀选$h$个home的真实行law实现。抽象组等式本身不定义全部原机器CONFIG；指数行分布表也不是免费多项式输出。**M1保持不说明M2保持。**

## 任意原任务共同M2必须有完整语境块

这是更广的必要条件，独立于上一段同菜单或固定$r$形式核。给任意显式$k$个原任务；每任务类别端指标$x_{a,i}$满足

$$x_{a,i}^2=x_{a,i},\qquad x_{a,i}x_{a,j}=0\quad(i\ne j)$$

到总次数四。类别可为互斥端的和、不可用端为零，不需覆盖全部端。置$X_i=\sum_a x_{a,i}$，**不要求$X_i$ Boolean**。

任取固定全局affine基$z_0=1,z_1,\ldots,z_s$，可含本组个别原标签。共同原$M_2$必须使一个整体矩阵

$$K_{(i,\ell),(j,t)}
=k\,\mathbf1_{i=j}L(X_i z_\ell z_t)-L(X_iX_j z_\ell z_t)\succeq0.$$

证明对任意$c_{i,\ell}$令$t_i=\sum_\ell c_{i,\ell}z_\ell$、$B=\sum_iX_it_i$、$q_a=\sum_ix_{a,i}t_i-B/k$。$q_a$至多二次，同任务排斥/Boolean ideal给

$$c^TKc
=k\sum_iL(X_it_i^2)-L(B^2)
=k\sum_{a=1}^kL(q_a^2)\ge0.$$

全部矩次数至多四，不需degree六、新条件law、标签平均或$X_i$ Boolean。$k=1$时整个$K$由原ideal恒零。

必须同时以head和context为索引。对固定**不同**$z_\ell,z_t$取出的非对角交叉块未必PSD，甚至不单独是Gram；正确断言是整个$K$及其主子矩阵。旧作者Proof措辞曾需此澄清，原字节不改。context置换不变时可称standard-label contrast块至正常数；含个别标签时仍必要，却不能只称standard表示。

## 计算身份与用途

对给定多项式长的显式任务组/类别/context列表，$K$维数$|I|(s+1)$，是四次矩的有理线性矩阵，SOS可精确核。完整原$M_2$中它冗余，投影掉任务身份后不一定冗余。它未证足以重构全部原$M_2$，枚举所有组/context也不免费；没有generic exact SDP finder或由一个坏点推出原实例FAIL。

形式核只计算至多四阶下降阶乘，位长受显式变量/矩编码控制；若$k$仅二进制需求且尚无这些任务，不能免费展开$k$标签。需另回到实际任务桥的压缩构造，而不能把两个不同身份系统混为同一输入。

[非扩展审查](../审查/匿名标签四次非扩展的双Schur证据与冻结范围--审查.md)给一个aggregate共同M2通过但此必要块负的精确点，说明保M1不能升M2；它拒绝给定点扩展，不是调度不可行、near2 gap或算法。读域/原件/历史证据见[本批证据](../../../../tools/evidence/um-review-contracts/README.md)。
