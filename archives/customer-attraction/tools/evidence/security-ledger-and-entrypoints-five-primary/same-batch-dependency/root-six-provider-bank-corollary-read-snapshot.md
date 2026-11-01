---
id: customer-attraction/joint-terminal-push-uniform-query-six-provider-bank-obstruction
kind: corollary
type_tag: 推论
title: 联合推送全查询上界的六人银行障碍
status: complete-analytic-corollary-of-established-complete-SPE-family
truth_status: proved
summary: 既有笛卡尔银行完整SPE族在六人十六客户三十主题时，对均匀查询及任意合法终局平均背景均有F≥31/22>6/5；因而同查询联合推送的普遍逐根上界已被否定，原half目标仍满足。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round5_general/security/global_extra_individual_counterfamily.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-977d3dbff13346b3b7c0f5a4caa6168e/security/push_joint_probe.py
---

# 联合推送全查询上界的六人银行障碍

本页是将已经完整证明的[笛卡尔银行反族](../反例/笛卡尔银行目录的逐人分数门槛反族--反例.md)代入[同查询联合推送合同](../资源/真实终局平均负载的同查询联合浮点攻击合同--资源.md)所得的直接解析推论。既有反族承担全有序历史、全部再次偏离及任意平局的SPE证明，本页明确计算此前两对象之间的关系。没有新增游戏搜索、原程序运行或全树数值认证；不主张银行构造或其逐人失败的新颖性。

## 被否定的准确合同

采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)，零过去负载，真实剩余玩家为 $m$。对同一份完整策略 $\sigma$，强制根标签 $a$ 后完成的 $m$ 槽终局计数为 $T_a$，其中含强制根本人。查询分布 $p$ 同时用于查询以及平均这些真实终局，置

\[
q_\sigma(p)=\frac1m\sum_a p_aT_a,\qquad
F_\sigma(p)=\sum_x\frac{\alpha_x(p)}{1+m\alpha_x(q_\sigma(p))}.
\]

每个 $T_a$ 都是合法非负整数计数、总和为 $m$，所以 $q_\sigma(p)$ 是目录上的概率分布。分母的额外一是另一个静态查询槽；它不把真实游戏改成 $m+1$ 人。待判合同为：每份完整SPE在根都满足 $F_\sigma(p)\le u_1$ 对**所有**查询 $p$ 成立。

该合同确实充分推出自由 extra 分数安全值 $t_{m+1}(0)\le u_1$：$H(p,q)$ 对 $p$ 线性、对 $q$ 凸，紧凸域上的极小极大与逐点 $\min_q H(p,q)\le H(p,q_\sigma(p))$ 给出充分方向。这里没有否定该逻辑。下面证明其普遍前提本身为假，而且给一个固定查询的显式严格缺口。

## 同一银行族的固定均匀查询

银行族有 $m$ 个经济客户 $e_i$、$m-1$ 个互不相交的两客户块 $B_j$；标签为所有配对 $(i,j)$，每个主题覆盖 $\{e_i\}\cup B_j$。既有完整BASE／PUNISH／EXIT策略给

\[
u_1=1+\frac1{m-1},\quad W=2m,\quad \operatorname{OPT}_m=3m-2.
\]

取全部 $m(m-1)$ 个主题上的均匀查询 $p^*$。其经济边际为 $1/m$，银行边际为 $1/(m-1)$。对**任意**目录分布 $q$，记经济边际为 $x_i$、银行边际为 $y_j$，二者各自非负、和为一。于是

\[
H(p^*,q)=\frac1m\sum_{i=0}^{m-1}\frac1{1+mx_i}
 +\frac2{m-1}\sum_{j=0}^{m-2}\frac1{1+my_j}
 \ge \frac12+\frac{2(m-1)}{2m-1}
 =\frac32-\frac1{2m-1}.
\tag{1}
\]

两项分别是函数 $z\mapsto(1+mz)^{-1}$ 的Jensen不等式。均匀配对背景 $q$ 同时达到两边际均匀，故(1)的下界可取等；这也恢复既有 $t_{m+1}(0)$ 的双边值。但否定联合推送只需下界：对实际 $q=q_\sigma(p^*)$ 仍成立，根本不必列出所有根孩子的终局表，也不必假设它们有某种独立或对称结构。

因此

\[
F_\sigma(p^*)-u_1\ge
\frac{2m^2-9m+5}{2(2m-1)(m-1)}>0\qquad(m\ge4).
\tag{2}
\]

这对所给银行SPE的所有合法终局平均推送都有效；不是只在局部优化中找到某个浮点正点。它也不声称该游戏的每份SPE具有同一根收益。

## 六人精确代入及程序归一

取 $m=6$，共有16名不同单位客户、30个共同主题，完整SPE满足

\[
u_1=\frac65,\qquad W=12,\qquad\operatorname{OPT}_6=16.
\]

式(1)给所有 $q$ 的值至少 $31/22$，故

\[
\boxed{F_\sigma(p^*)-u_1\ge\frac{23}{110}>0.}
\]

联合浮点入口将客户质量缩放到根收益一，而不是总客户质量一或福利一。按该归一同时缩放 $F,u_1$，缺口至少为

\[
\frac{31/22}{6/5}-1=\frac{23}{132}>0.
\]

这只是解释同一数学目标在程序坐标中的量纲，不宣称原150条有限报告含该30主题游戏、该完整策略或这条解析点，也不宣称运行过这个输入。原报告的全部负最佳值可与本推论并存。

## 用途与接续边界

普遍“同查询真实终局平均负载可由根利润支付”在六人原模型已失败。原程序作为发现器、每个特定实例的条件上界，或合适受限类的研究仍有明确用途；任何保留的正命题都须写出额外假设，并检查银行族是否被排除。

这不反驳真正聚合安全值、不是六人half反例，也没有解决六人half：本游戏 $W=12>\operatorname{OPT}_6/2=8$。单次特定推送失败通常不能推出自由安全值失败；此处之所以两者都失败，是另有(1)对**所有**自由背景 $q$ 的解析下界。后续关系图应分别记录“联合推送充分推出逐人extra”“银行族否定逐人extra”“均匀查询直接否定联合推送”三条有证据的关系，不把它们合并成对聚合或half的反驳。
