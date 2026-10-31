---
id: "customer-attraction/selected-spe-branch-minimum-below-threshold"
kind: "counterexample"
type_tag: "反例"
title: "选中SPE分支的最小续局值可低于节点门槛"
status: "proved-exact-two-player-common-catalog-counterexample"
summary: "两人四单位客户的完整SPE实际收益2，而选中枝最低可信续局值1小于节点maxmin门槛3/2；只纠正中间桥，不反驳实际门槛下界或half。"
source_ids: ["0abe71e0f3a6d2e380b7"]
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/route5/README.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-1740705e79f14baba6326b951a52152f/route5/README.md"]
---

## 否定的断言和原语境

R174 route5原记录在L_h(A)=min_{z∈R_h(A)}u_i(z)、Θ_h=max_A L_h(A)后，把一份SPE选中a时的L_h(a)也写成至少Θ_h。下面是在同一单位客户、共同目录、完整历史纯SPE模型内的显式反例。它是本批读源后重构的纠错见证，不伪称原稿已给此例，也不认证全球新颖性。

## 全部客户、动作和策略

两名顺序提供者，四名单位客户a,b,c,d，共同目录
\[
A=\{a,b\},\quad B=\{a,b,c\},\quad C=\{c,d\}.
\]
完整策略：首人选A；末人在前缀A/B/C后分别选C/B/B。末位三种动作收益表是

|首人历史|末位A|末位B|末位C|指定末位|
|---|---:|---:|---:|---|
|A|1|2|2|C|
|B|1|3/2|3/2|B|
|C|2|5/2|1|B|

均为最佳回应。按此固定策略，首人强制A/B/C的真实收益分别2、3/2、3/2，故首人A严格最优。全部四个决策节点都给出并满足每个行动比较，是完整纯SPE。实际(A,C)双方收益均2，覆盖4；最优两主题也覆盖4，因此W=OPT2=4。

## 强制孩子全集与最低值

强制首人A后末位B/C均最佳，故R(A)={(A,B),(A,C)}，首人收益分别1、2，L(A)=1。强制B后末位B/C均最佳，首人收益3/2、5/2，L(B)=3/2。强制C后末位唯一B，首人收益3/2，L(C)=3/2。因此
\[
L(A)=1<\Theta=\max\{1,3/2,3/2\}=3/2<2=u_1(A,C).
\]
当前SPE可以选择下包络较差的A，因为自己的实际后继是有利的C；压住其它动作只需实际收益2，不需A的最坏续局值也压住门槛。正确普遍结论仍是actual_u≥Θ≥L(selected)。

## 实际精确核验及范围

[新Fraction定义级自查](../../../../tools/evidence/r174-workspace-and-bridge-primary/README.md)不导入已有solver，枚举3^(1+3)=81份完整两人策略映射，每份4节点的3个强制动作收益均算出，合972个收益条目；有效性按节点最大值判定，已知失败的策略不再重复判定其后节点，不能把字段名中的972解读为972次独立标量IC调用。恰5份SPE、4个不同根有序终局(A,C),(B,B),(B,C),(C,B)。另按孩子BR集合加阈值筛选得到同一根集合；两路共用单位客户收益函数，不冒称两套独立实现。报告保存全部5份完整策略、所用四节点收益表与全部精确L值，原程序入口执行0。

一般R(h)递归的充分/必要证明没有被否定，实际u≥Θ和Σ实际路径Θ≤W也不受影响。此反例只排除“选中枝最低值≥门槛”，没有满足或否定一般half条件接口的未证需求下界，尤其不是六人half反例。
