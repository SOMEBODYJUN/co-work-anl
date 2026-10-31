---
id: "unrelated-machines/tiny-paired-slot-proof-and-heavy-medium-scoped-review"
kind: "review"
type_tag: "审查"
title: "tiny配对槽独立证明与重中端胶合的分域审查"
status: "three-review-and-proof-sources-integrated"
truth_status: "existing-scoped-gluing-proofs-retained; no-general-solver"
summary: "保存tiny原job配对槽费用流这一独立证明、uniform/tiny两条审核路线和heavy新域的完整界与最终字节修正，不把旧基础先验或旧枚举移给新Claim。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/unit_presence_two_witness_gluing_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/tiny_presence_gluing_independent_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/heavy_medium_strict_witness_presence_gluing_review.md"
---

# 三件原资源与已有数学

来源ad2（4591B）、127a（4851B）、377a（2364B）均全文实读，原件见[manifest](../../tools/evidence/uniform-audits-reviews/manifest.json)。成熟主数学已在[近单位PCSP与单位presence胶合双源审查](近单位PCSP与单位presence胶合双源审查--审查.md)第3节。本页不是再建三条胶合定理；补齐原tiny独立证明的**原job配对槽**路线，以及uniform/tiny/heavy三域各自的实际先验、证明与最终认证范围。另全文比较当前presence20393B及heavy五份Exact/Proof/独立/作者读后/canonical读后。

# Tiny：直接对原jobs配对槽，不靠virtual任务证明

`UM-TWO-MEASUREMENT-TINY-PRESENCE-GLUING-v1`输入同一显式P的两完整实际见证，有限时间在$\{1\}\cup[0,a]$、有理$0\le a<1$，两峰≤$T=1+a$。两不同测量机v/w在前见证均无unit、后见证均有unit。任务允许任意arity、tiny成本不同/为0、tiny↔unit切换。要输出两位任意profile、全部原jobs各一次的实际分配，峰≤3T/2；不是寻找两见证的程序。

127a的独立路线此前已有uniform count-flow经验，并曾给较弱tiny界$T+1/2+a$；仅读加强Exact后把额外a降成a/2。这是对新陈述先行、**有旧基础先验**的独立重构，不称零背景盲审。它与canonical的matching+virtual-item二染色证明是不同的实际证明资源。

先把两见证目的机相同的原job固定，记该机固定tiny负荷$F_i$或固定unit数；同一job同一原机时间固定，不会暗藏tiny/unit切换。其余每job有两个不同机器端，各半流。每机把其tiny incidences按真实时间$t_1\ge t_2\ge\cdots$相邻配对，每对一个容量1槽，至多一个单尾槽；两枚job各半流入槽。unit端进入该机unit节点，容量为1减固定unit数。job源边容量1，槽/unit节点通汇，原half点是一份分数满流。槽是组合变量，不是新原机或新增执行任务。

实现10：把$\sigma_1$在v执行的unit job $j_v$从half改为整枚固定v。它不是原先同机固定job，v-unit由1/2增1合法，另端只减half，不增加tiny槽流。w的unit流仍1/2：$j_v$在$\sigma_1$端是v，而$\sigma_0$在w没有unit；另端即使是w也只能tiny。删已固定job并扣容量，仅给进入w-unit的边费用1，其余0。已有分数满流费1/2；整数最小费用满流的费为非负整数且≤1/2，故0。恢复固定jobs，恰得v1/w0，另一mixed交换，00/11用原见证。

每配对槽至多选一tiny，故一次共同整数解在每机的tiny负荷≤

\[
F_i+t_1+t_3+\cdots\le F_i+\tfrac12\sum t_j+t_1/2
\le\mathrm{averageTiny}_i+a/2.
\]

降序交错差≤$t_1$，奇尾/M0同样成立；固定$ j_v $只删别处half tiny，因此仍由原均值控制。两原见证的平均unit数$q_i\in\{0,1/2,1\}$，tiny均值≤$T-q_i$。q_i0时保留端本无unit，负荷≤T+a/2；q_i1/2时至多一unit给$1+T-1/2+a/2=3T/2$；q_i1时给T+a/2。所有机器同时成立，每job原端恰一次，无切片执行。

a0同算法实际峰≤1（所有tiny零、unit数≤1），强于统一3/2界。奇k≥3、a=1/k的四机uniform族mixed真OPT=$3/2+3/(2k)=3T/2$，所以统一系数不可降，但不称每个固定a都锐；k3/a1/3 mixed2说明绝对次二需要严格a<1/3。节点/边/槽O(m+n)，仅原两端、整数容量≤n、费用0/1，排序/有理运算总位多项式，不按1/a或分母值造槽。原稿无软件或有限测试。

# Uniform/tiny review实际覆盖什么

ad2记录uniform先陈述独立count-flow，后读作者8757证明，再读39e canonical，root纳入第二证明；uniform原matching/virtual-flow不被改写。k2/3/4共21504份scratch枚举仅是其历史有限补证，未有通用生产软件。tiny另以新Exact先审，127a独立配对槽证明后才读含uniform countflow+tiny的92b canonical；另一名审者也仅读新Exact独立做槽流、另构odd reciprocal锐族，再读相同92b。不能把uniform旧审查算tiny新量词的审查，也不能把另一审者路线的先验回填127a。

review攻击的关键包括unit匹配来自两actual和T<2、machine路径不同测量端、virtual只是方向编码、直接流同时控制unit与tiny/总count、固定$j_v$只用half余量、费用整数性迫w0、同机不同成本选廉、两匹配配对图只能路径/交替偶环。这些都针对原任务完整输出，不是逐机各取一个不同见证。ad2绑定的是当时39e/92b whole版本，其uniform/tiny认证不能自动覆盖后来新§8；新heavy由377a及其五件原链限定认证。源中部分statement/初稿/独立稿hash在inventory未取得原件，按历史自述保留；本批没有重演这些枚举/盲审。

# Heavy–medium：改变见证容量和时间规则的新ID

377a正式review对应 `UM-HEAVY-MEDIUM-STRICT-WITNESS-PRESENCE-GLUING-v1`。输入正有理T、$0\le\epsilon<1/2$、$0\le a<1-\epsilon$，两完整actual峰≤T；**仅两见证用过的端**须在medium $[0,aT]$ 或heavy $[(1-\epsilon)T,T]$，未用有限端任意。输出只用每job两原见证端，保两机heavy-presence，界为

\[
[3/2+(\epsilon+a)/2]T=[2-((1-\epsilon)-a)/2]T<2T.
\]

两heavy不能同机，故matching分量仍合法，但heavy时间不再相等。单job–machine翻转必须同时计内部heavy替换最多$\epsilon T$及唯一新增medium≤aT，允许叠在同机，总≤$(1+\epsilon+a)T$。其它分支全job–machine active，真实medium及job–job virtual items半流≤两原medium均值；按成本降序相邻配对，与item对二染色，全部机同时多≤aT/2，再恢复原jobs。三类完整机器的界是：

| 两原见证heavy-presence | medium均值 | 全部负荷/T |
| --- | --- | --- |
| 11 | ≤εT | ≤1+ε+a/2 |
| 01/10 | ≤(1+ε)T/2 | ≤3/2+(ε+a)/2 |
| 00 | ≤T且不会新接heavy | ≤1+a/2 |

三行均≤目标，a0/ε0、静止job、同机不同成本virtual均合法，不按参数倒数展开。gap≥κ时界≤$(2-\kappa/2)T$。T0明确域外，不能说旧正容量unit/tiny身份自动处理；不声明新域全参数锐性、指定job身份/其它边界或源解码。

general的先行输入是新Exact加**获准旧unit/tiny基础**，未读新作者Proof，再作者读后及最终canonical§8读后。五原hash表均与本批已读比较原件一致，最终wholeSHA `0b9ab7d50bba3b4b7c5825c6208e51d23d20cdb5460d8e7478a6ef866f986e00`。实际[字节检查](../../tools/evidence/uniform-audits-reviews/version-byte-checks.json)确认当前除LF无ASCII控制字节，且§8前去两个追加LF的旧§1–7前缀SHA为 `1d5d27a9a80c64dbcca319531da735f23b1d65e29d1ef1f16a011a85a4adf4ba`。历史首稿的TAB/FF/VT/CR转义和T0误指已修；本次没有旧坏draft，不假称重构其字节。修正不改变正T数学，也不能把旧uniform枚举认证给heavy新域。

三主源integrated：原tiny完整不同证明、review读序/先验、heavy最终分域和修正都有去向；成熟主定理不重复授予。关系分同合同另一证明、条件推广、来源及内部复核，未重建阶段三图。两strict见证由输入给，不计算未知解，无新胶合软件/一般UM算法、hardness、外审/全球新颖性或六人SPE结论。
