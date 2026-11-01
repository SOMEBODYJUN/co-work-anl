---
id: customer-attraction/third-topic-background-seven-payoff-compensation-identity
kind: lemma
type_tag: 引理
title: 第三主题占位的七收益补偿恒等式
status: proved-by-seven-membership-cases;no-global-payment-construction
summary: 固定第三主题人数时二支持回路需保该主题三个收益补偿项；给r≥s≥1、t≥1完整有理身份及唯一可能负系数的移项域。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-fa8dd4ddea574a74a634ebc71e6f9ccb/tree_coupling/three_support_background_circuit.md
---

# 第三主题占位的七收益补偿恒等式

主题a,b,c为不同标签，允许覆盖交叠或同覆盖。对计数q，U_a(q)是一名选a玩家的最终收益。取整数r≥s≥1、t≥1，m=r+s+t、D=r+s+2t，令
\[
q=(r,s,t),\quad q'=(s,r,t),\quad q^0=(0,r+s,t).
\]
共同客户资料可以有符号；不需要SPE，也没有把q/q′/q⁰声称为某一策略的可达终局。精确恒等式为
\[
\begin{aligned}
rsD U_a(q)+r(r-s)D U_b(q')+st(s+t)U_c(q)
={}&s^2D U_a(q')+(r^2-s^2)D U_b(q^0)\\
&+t[s^2+(2s-r)t]U_c(q')+(r-s)t^2U_c(q^0).
\end{aligned}\tag{7}
\]
除ζ=t[s²+(2s−r)t]外各系数非负；ζ≥0 iff(r−2s)t≤s²，若ζ<0移到左侧成为全非负系数身份。r=s退化、部分零系数；r>s时其余六系数严格正，不误写全部参数七项都正。

## 从七类客户直接推导

不命中a/b/c者全零。无c的a-only/b-only/ab三模式，前四a/b项系数比例先由两支持身份定为rs:r(r−s):−s²:−(r²−s²)。暂不乘D，设三个c收益在左边系数A,B,G；c-only要求G=−A−B，ac/bc模式分别要求
\[
Ar(s+t)+Bs(r+t)=t^2s(r-s),
\]
\[
Ar(r+t)+Bs(s+t)=ts(r-s)(s+t).
\]
r>s时相减并除r−s得Ar−Bs=ts²，解为
\[
A=ts(s+t)/D,\ B=t[(r-2s)t-s^2]/D,\ G=-t^2(r-s)/D.
\]
abc模式各分母同m，系数总和为0，故也成立。乘D移项得(7)；r=s直接代入验证，无须除0。逐客户相加即证任意共同有符号资料，非负性未参与。

## 一组全正参数及原二支持系数为何不能原样提升

取r=2s、t=k并把(7)除s，m3s+k、D3s+2k，得到
\[
\begin{aligned}
2sD U_a(q)+2sD U_b(q')+k(k+s)U_c(q)
={}&sD U_a(q')+3sD U_b(q^0)\\
&+ks U_c(q')+k^2U_c(q^0).
\end{aligned}\tag{P}
\]
全部系数正。七兴趣模式的两侧共同值为a:D，b:D，c:k+s，ab:4D/3，ac:3s+k，bc:3s+k+ks/(2s+k)，abc:[4sD+k(k+s)]/(3s+k)。这些是单客户单位贡献，不是已经给实际策略的共同预算。

例如s=k1时(P)为10Ua(2a+b+c)+10Ub(a+2b+c)+2Uc(2a+b+c)=5Ua(a+2b+c)+15Ub(3b+c)+Uc(a+2b+c)+Uc(3b+c)。旧无c的2Ua(2a+b)+2Ub(a+2b)=Ua(a+2b)+3Ub(3b)若原系数统一加kc，对ac型要求2/(2+k)=1/(1+k)，每k>0均假；(P)正是合法补偿而非“无法提升”的总体不可能性。

任意背景多个主题时每客户看到的背景人数不同，不能统一合成一个c后直接套(7)。恒等式可用任意有符号乘子，真实SPE比较和非负客户不等式则须合法非负乘子；有正项形式不提供在任意策略图上的可实现非负运输，也未把全树成本付到2W。

原verify_background_circuit.py声称形式多项式全部系数检查，但本批未新读/执行该代码。这里按七模式与上述求解完整重构，不称新的盲审、原代码复跑或一般half结论。[同支持全环障碍](../障碍/同支持全部梯度环不能替代共同客户表示--障碍.md)需要不同支持间信息，(7)给一类真实共同表示约束；它与另一个27/13抽象点失败的三不同标签覆盖身份不混为同一式。

原件、逐项指纹、真实读取范围和本批运行事件见[本批证据](../../../../tools/evidence/cag-maxroot-terminal-share-and-direction-primary/README.md)。
