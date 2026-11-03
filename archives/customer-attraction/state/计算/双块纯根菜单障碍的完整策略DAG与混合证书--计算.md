---
id: customer-attraction/two-block-pure-root-menu-obstruction-full-strategy-dag-and-mixtures
kind: computation
type_tag: 计算
title: 双块纯根菜单障碍的完整策略DAG与混合证书
status: complete-finite-certificate-and-original-audit-contract; no-new-IC-run
summary: 保八人32单位客户、13872节点全部字段/边及原59496精确比较；每纯列cap37/10大于根13/4，但简单混合123/40和父审最优851/280均低于根，不反混合菜单或half。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/counterexample/build_pure_menu_dag.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/counterexample/build_pure_menu_dag.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/counterexample/pure_menu_two_block_dag.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/counterexample/pure_menu_two_block_dag.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/counterexample/verify_pure_menu_dag.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/counterexample/verify_pure_menu_dag.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/counterexample/pure_menu_two_block_audit.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/counterexample/pure_menu_two_block_audit.json
---

# 双块纯根菜单障碍的完整策略DAG与混合证书

4017B发现器、1443260B完整DAG、5277B直接核验器与1993B完整审计JSON四primary全文处理。DAG全部13872个节点的counts/target/action/children均读入无损字段表，不只根或统计；原件、完整字段索引及比较见[证据](../../tools/evidence/Boss7-resume-d22-menu/README.md)。本轮没有导入/运行发现器、原直接核验、父方独审、BI、LP或新IC程序。

## 有限模型与被否定命题

有限不同单位客户、共同有限非空目录、单位顺序提供者，原策略保所有有序历史及任意离轨平局；一般域仍允许空题、重复行动和零客户。具体m=8、k=8，标签顺序A0,B0,C0,D0,A1,B1,C1,D1。两个客户块互不相交，每块16名单位客户，局部类型及重数是

| 局部兴趣 | A | BD | AC | CD | ABCD |
|---|---:|---:|---:|---:|---:|
| 不同单位客户数 | 2 | 4 | 6 | 3 | 1 |

第二块标签加4。十个类型总32，非加权玩家/客户价值。令完整根强制b后的真实八槽列为Z(b)，原强制者收益d_b，actual根u=max_b d_b。独立额外查询a对该**包含强制根**的完整列得

$$K_{ab}=\sum_{x\in T_a}\frac1{1+c_x(Z(b))}.$$

本例反“存在一个纯真实根列同时给所有查询K_ab≤u”；反例所需量词是每列b都有某行a超过同一个actual u。它不需要一行对所有列都坏，更不等于混合菜单M_full=min_Q max_a(KQ)_a>u。

## 八根列、完整DAG和全历史展开

设b0=(2,1,1,0)，四局部列依A/B/C/D为c0=(2,0,1,1)、c1=(1,1,1,1)、c2=(1,0,2,1)、c3=(1,0,1,2)。前四根列(c_j,b0)，后四(b0,c_j)。actual根选D0，即3，target=(1,0,1,2,2,1,1,0)。原发现器先用ExactSPESolver求全部集合值续局及阈值13/4，再展开这一个指定策略；它不是依赖BI状态数来认证SPE。

每个DAG节点是(q,target)。非终端存规定action及八个按合法动作编号的children；对应孩子counts=q+e_a，规定孩子target保持原target。终端q=target、action=null、children空。缓存同一(q,target)可共享；同q不同target分开，并未宣称所有纯策略可净化成计数策略。任何具体有序历史沿自身动作序列走八叉边，仍得到明确动作，包括再次偏离；该指定策略恰在共享节点处作相同选择，属于允许的全历史策略。

原核验器不导入model/BI/canonical verifier，展开32个不同单位客户直接算Fraction份额；逐节点检查全部八边的真实孩子target、规定收益对每个偏离者在该孩子终局的收益。按剩余深度归纳：终端正确、孩子均SPE、当前规定动作对全部真实孩子最优，则整个展开是SPE。counts每边增加一保证终止，所有孩子存在并访问全部节点，故压缩比较覆盖全部2396745个有序决策历史，而不是只有13872个历史。核验只针对这一份给定完整策略，不穷尽所有SPE。

| depth | DAG节点 | 不同counts |
|---:|---:|---:|
| 0 | 1 | 1 |
| 1 | 8 | 8 |
| 2 | 58 | 36 |
| 3 | 201 | 120 |
| 4 | 514 | 330 |
| 5 | 1078 | 792 |
| 6 | 1999 | 1716 |
| 7 | 3578 | 3432 |
| 8 | 6435 | 6435 |

共有7437非终端、6435终端；原direct报告59496项含自身比较=8×7437，其中严格50732、相等8764、最小差0。actual有序路径(3,0,2,3,4,4,5,6)，按位置收益(13/4,21/4,17/4,13/4,13/4,13/4,17/4,21/4)，和32；此叶覆盖全部32客户，故W=OPT8=32，绝非half坏点。discover字段的12870是canonical计数状态数，不能与DAG节点或展开历史混同。

## 完整额外查询矩阵及纯/混合分离

行/列均按0,…,7；列是根强制动作、行是独立额外查询。原8×8矩阵全部保留：

| a\b | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---:|---|---|---|---|---|---|---|---|
| 0 | 71/30 | 16/5 | 27/10 | 16/5 | 71/30 | 71/30 | 71/30 | 71/30 |
| 1 | 11/5 | 23/15 | 11/5 | 23/15 | 11/5 | 11/5 | 11/5 | 11/5 |
| 2 | 27/10 | 16/5 | 49/20 | 59/20 | 16/5 | 16/5 | 16/5 | 16/5 |
| 3 | 16/5 | 38/15 | 59/20 | 137/60 | 37/10 | 37/10 | 37/10 | 37/10 |
| 4 | 71/30 | 71/30 | 71/30 | 71/30 | 71/30 | 16/5 | 27/10 | 16/5 |
| 5 | 11/5 | 11/5 | 11/5 | 11/5 | 11/5 | 23/15 | 11/5 | 23/15 |
| 6 | 16/5 | 16/5 | 16/5 | 16/5 | 27/10 | 16/5 | 49/20 | 59/20 |
| 7 | 37/10 | 37/10 | 37/10 | 37/10 | 16/5 | 38/15 | 59/20 | 137/60 |

根列本人的d_b=(13/4,9/4,13/4,13/4)重复两遍，actual u13/4；不能用K_bb替d_b，因为K额外加一名查询。前四列查询D1、后四列查询D0均给37/10>13/4，差9/20；每列cap确37/10。因此任何标量选纯列（包括“好最大势列总存在”的普遍加强）都无法修此例的纯cap。

原direct报告用Q=(δ3+δ7)/2，八行值为(167/60,28/15,123/40,359/120)重复两遍，最大123/40<13/4，差7/40。这个Q是合法可行混合证书，未声称最优。原flags pure_menu_blocker_refuted=true、mixed_menu_blocker_refuted=false、half_coverage_refuted=false均有上述明确数学含义。

后续[父方独立证据合同](../资源/单位客户父审计与利润枚举的完整证据合同--资源.md)在**同一DAG/同一矩阵**给更优原始/对偶：Q=(0,0,1/14,3/7)重复两遍，p=(0,0,2/7,3/14)重复两遍；KQ=(577/210,67/35,851/280,851/280)重复两遍，pK=(443/140,443/140,851/280,851/280)重复两遍。归一非负且max KQ=min pK=851/280，有限零和对偶给精确M_full=851/280<u，差59/280。因此123/40与851/280是可行上界和更精确最优的区别，不是矛盾。父审硬编码32单位输入，不读取DAG.instance；本原direct从instance展开，两者的输入对应/矩阵与报告已全文比较。本轮不重跑任一审计，也不将父审脚本纳入本四primary重复done。

## 发现器、核验器与当前状态

build_pure_menu_dag.py无CLI；按最近含customer_attraction/__init__.py的祖先定位旧根，构造实例、选根列后，非根取首admissible动作，偏离孩子按(当前收益,终局计数)最小值选，独占x模式写同目录DAG。verify_pure_menu_dag.py有--input/--output，默认同目录DAG；逐节点正分母份额、全部边/目标、根列、实际路径、完整矩阵、混合及W/OPT均在写报告前核验，输出亦x模式。它无独立生产代码SHA/环境事件，不能凭报告格式回填实际运行argv；原结果仍完整保。

本次新增只是原件/全字段读取索引、两原审计来源比较和自足证书推理，无IC新PASS或新策略发现。[两人纯列](../引理/两名剩余完整终局菜单的纯列封顶--引理.md)仅r2，不与八人失败矛盾；[完整菜单资料](../资料/完整真实菜单的条件对偶与旧实例账本--资料.md)的普遍混合FM后来已由另一银行真例反驳，不能把本mixed未反驳误写为一般OPEN。新输入补齐了旧资源“八人DAG未取得”的来源范围，但没有自动新增运行、外审或新颖性。六人half仍是其完整有序历史独立问题。
