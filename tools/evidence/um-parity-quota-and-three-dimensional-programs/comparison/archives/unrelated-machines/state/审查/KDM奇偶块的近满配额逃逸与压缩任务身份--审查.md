---
id: "unrelated-machines/kdm-parity-nearly-full-quota-escape-and-compressed-token-identity"
kind: "review"
type_tag: "审查"
title: "KDM奇偶块的近满配额逃逸与压缩任务身份"
status: "candidate-exact-family-reconstructed; source-wording-clarified; finite-resource-DFS-and-actual-certificates"
summary: "保偶d全匹配仅半而所有中间配额全覆盖的精确族、odd对照与实际OPT1+1/d；按原压缩token桥澄清x任务数量及根时间1/q。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/unrelated-machines/R-e3b3957c07cf4f32b420a8831ef1ebef/notes/kdm_parity_partial_escape.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/unrelated-machines/R-e3b3957c07cf4f32b420a8831ef1ebef/notes/kdm_parity_partial_escape.md"]
---

# 显式族与全部配额层

源ID `UM-KDM-PARITY-PARTIAL-ESCAPE-v1` 是候选/观察，未接受独立reviewer完整读后、外审或新颖性核查，不升级为canonical Claim。取偶d≥2、s≥1，q=2s个选择点x_(g,a)，g∈[s]、a∈{0,1}；资源(g,j,b)，j∈[d]、b∈{0,1}。不同块g完全不交。

x_(g,a)的合法标签为b∈{0,1}ᵈ满足a+Σbⱼ≡1 mod2，标签资源束S_(g,a,b)={(g,j,bⱼ):j∈[d]}。每个选择点2^(d−1)标签，共L=s2ᵈ标签，每束d个不同资源。ν_t为最多多少个**不同选择点**可各选一个合法标签并各领t个资源，全部领取彼此不交；不是任意挑若干标签、不付选择点唯一性。

四层简单DAG为根r→x→标签→资源，需求依次q、1、d、0。对包含r的朝外树，所有选中的正需求点（即使在输出成为叶）均按deg⁺/需求收费，评分b(H)还截断在1。根单点评分0。完整全层恒等式是
\[
b^*=\max_{1\le t\le d}\min\{\nu_t/q,t/d\}.
\]
从任意正评分b树，根至少bq个孩子，所选x至少一个标签；可各保一个标签而不降其x的比例到1以下。每保留标签至少ceil(db)个资源，单父性给不交子束，置t=ceil(db)得两项都≥b。反向ν_t个不同x各取一个标签及其t个不交资源，直接给评分min(ν_t/q,1,t/d)。不需有限枚举代替证明。

# 完整层半覆盖，中间层全覆盖

同块两完整d束不交，必在每个坐标取相反bit，即b′=1−b。偶d使Σb′≡Σb mod2，而a=0与a=1要求相反奇偶，故两点不可能同时全取。一块可任选一个合法完整束，块间不交，所以ν_d=s。

取任一固定j₀。a=0用只在j₀为1的向量b，a=1用全1向量b′。前者奇数和，后者偶数和，均合法；两束只在j₀资源相同，删掉该坐标就给两点各d−1个不交资源。对t≤d−1再取同样t个非j₀坐标即可。每块都做，故
\[
\nu_t=2s=q\ (1\le t\le d-1),\qquad \nu_d=s,
\quad b^*=(d-1)/d.
\]
d=2时中间项1/2与完整项1/2相等，边界仍成立。对照奇d≥3，取a=0任一合法b、a=1用其补向量，奇偶恰翻转，两个完整束不交，每块全取，b*=1；偶数条件真实承重。

# 真实UM必须按压缩桥造原任务

调用[有向需求压缩token桥](../定理/有向需求与调度的压缩双向任务桥--定理.md)。此DAG所有正需求≤原出度，故无filler；每DAG顶点一机器，全部原任务/资格为：

| 原任务数量及身份 | 全部有限端与时间 |
|---|---|
| 一件根g | 仅根机r:1 |
| q件互异根token | 每件在r:1/q，可到任意选择机x:1 |
| **每个x恰一枚**token | 自己x:1，可到该x任一合法标签机:1 |
| 每标签恰d枚互异token | 每件在自己标签机:1/d，可到该标签束内任一资源机:1 |

其余端∞，所有未选标签的全部任务保留。源末段“每个x→标签任务”不能按**每条弧造一件unit job**读；P(D,k)中k_x=1，所以只有一枚可选择全部孩子的原token。标签token也保原来的任意孩子资格，不能暗中替换成固定一资源的不同矩阵。

源另称时间只含{1,1/d,1−1/d}，在这个固定q=2s特化里不准确：根token确有1/q，此处没有filler；实际时间集是{1,1/q,1/d}的子集。以下统一按原桥的精确P解释，原note字节保留，不用错误简写生成另一矩阵。显式计数为
\[
m=1+2s+L+2ds,\quad n=1+4s+dL,
\]
\[
\#\text{finite}=1+q(q+1)+q(1+2^{d-1})+dL(d+1),\quad L=s2^d.
\]
算法按展开标签/原矩阵总编码多项式；d固定当然也是输入多项式，但不称对succinct二进制d的poly(log d)归约。

# 全部原任务的实际值

偶d：根g留r，将q根token一一送全部x；每x唯一token送前述选定合法标签。选中标签d枚token中，任选d−1枚分别送非j₀坐标的对应不同资源，余一枚留home；未选标签所有d枚留home。全部任务一次合法：根/x峰1，未选标签负载1，所选标签有incoming unit加留home的1/d，资源至多一unit。因此完整Cmax=1+1/d，不需要源见证。

反向任何C<2完整调度中，资源/标签/x每机至多一件外来unit；根g供unit，沿实际外送token从根取可达弧，DAG及入流唯一保证真实根树。已选正需求v的负载精确为2−s_v/k_v，其中s_v是本地token实际外送数，故解码b(H)≥2−C。若C<1+1/d，则b(H)>1−1/d，与b*=(d−1)/d矛盾。故
\[
\operatorname{OPT}(P)=1+1/d.
\]
这下界针对任意实际完整分配，不只是所造上界或某LP点。奇d互补束全外送，给完整峰1；根g迫OPT≥1，故该对照实际OPT1。

# 旧程序、一次新复跑与范围

原 `parity_block_check.py` 39行仅导入itertools和Fraction，枚举合法标签，对所选x子集递归遍历标签及t子资源，精确算ν_t，再有理代入全层式。它没有生成P、枚举调度或验证任意低峰decoder。主源的有限表为d∈{2,4,6}、s∈{1,2}，值分别

| d | s=1的ν₁…ν_d | s=2的ν₁…ν_d | b* | 实际OPT（由证明） |
|---|---|---|---|---|
| 2 | (2,1) | (4,2) | 1/2 | 3/2 |
| 4 | (2,2,2,1) | (4,4,4,2) | 3/4 | 5/4 |
| 6 | (2,2,2,2,2,1) | (4,4,4,4,4,2) | 5/6 | 7/6 |

本批在新空目录执行原入口恰一次，exit0/stderr空，六行**数值及行序**与源表一致；真实stdout保其空格，不称Markdown代码块逐字一致。独立wrapper另按上表的压缩资格生成六个even完整P证书和odd d3/5、s1对照，核每件原任务一次、原资格及同时负载；最大fixture157机/777任务/5529有限端。没有遍历这些P的全部调度，八证书的下界仍来自上面解析证明。[原程序](../../../../tools/evidence/um-weighted-partial-parity-and-route-primary/support/parity_block_check.py)、[复跑与新证书报告](../../../../tools/evidence/um-weighted-partial-parity-and-route-primary/run-parity-and-certificates/report.json)分清两种证据。

# 正确否定范围与下一义务

完整匹配比例ν_d/q=1/2，但近满层d−1已全覆盖，真实OPT→1。它反驳“只用完整KDM层soundness，提高K/需求就能从直接bundle桥得到近二NO”的黑盒推论；不是NP-hardness，也没证明这个易判奇偶族属于LST或任何指定hard image。[已有全层/低配额边界](KDM配额与原地拟阵指数边界两源精读--审查.md)强调同一逻辑，原笔记独有的是**近满**配额逃逸及精确odd对照，不是只重复t=1逃逸。

要接近二归约，仍需对每固定ε>0控制NO中所有t>εd的可分离领取，并从任意完整C<2−ε实际调度给真实源见证。完整匹配gap、有限程序、显式OPT或把d增加都不替代该decoder。[128行原笔记](../../../../tools/evidence/um-weighted-partial-parity-and-route-primary/original/371e4302c248eaf14f86.md)保持候选及未审状态。
