---
id: "unrelated-machines/fixed-sink-occupation-base-review-final-contracts"
kind: review
type_tag: 审查
title: "固定汇点占位基面与未知OPT承诺的最终审查"
status: complete-primary-read-and-scoped-mathematical-reconstruction
summary: "任意K侧约束2K非单值引理、固定K真实3T/2算法、含OPT宏边promise搜索三身份分开，保base而非独立集和软件缺口。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/fixed_sink_occupation_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/fixed_sink_occupation_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/fixed_sink_occupation_rounding.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/fixed_sink_occupation_rounding.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/fixed_sink_occupation_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/fixed_sink_occupation_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/occupation_base_face_independent_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/occupation_base_face_independent_audit.json"
evidence_manifest: ../../../../tools/evidence/um-next-available-reviews/source-manifest.json
---

# 三个量词不同的正式身份

主源1fdb08ccd3717fa2ad9c全文8637B/73行已读；当前82af0ae2f147b7c28726全文224行、SHA5d41fe7e8530a7cc17f633e15498b58080f405835c6659ca18ab7ce2ff34aae9，与最终审查一致。原文和OPT-promise增量均实际受审，不以同步/提交状态代证。以下为三个独立合同，不能合为一般UM算法。

| 身份 | 输入/量词 | 输出 |
|---|---|---|
| UM-OCCUPATION-MODE-SIDE-CONSTRAINT-v1 | 任意K≥0、覆盖宏匹配图、有限0/1占位模式、任意K条线性侧不等式 | 交切投影顶点≤2K个非单值home；支持恢复不保证预算 |
| UM-FIXED-SINK-PRIVATE-GROUP-THREE-HALVES-v1 | 每固定K≥1，给T≥0及显式home/sink与唯一home私有分组，所有宏有限边>T/2 | FAIL⇒普通OPT>T；成功真实全任务峰≤3T/2 |
| UM-FIXED-SINK-MACRO-PROMISE-APPROX-v1 | 不给T，但每有限宏边>OPT/2的额外promise | 固定K下真实峰≤3OPT/2 |

H与K个sink Z不交，宏B只可在H，私有J_h互不交、每非宏恰一组，只可去h及Z子集（可在h不可用、可非tiny）。允许零/∞、空组、无宏和大分母。给T先空任务/零端检查，再剪p>T，剪后无端或宏无法全覆盖可可靠失败。所有边均保原身份。

# 真实模式与共同取整误差

T>0且有私有任务，N=max(1,Σ|J_h|)、s=T/(4N)。只将sink时间向上取整ceil(p/s)，home成本存原有理数。每组DP的K维坐标≤floor(T/s)+n_h≤5N，每profile仅保最小真实home负载与完整任务回溯。empty标签允许home≤T，occupied允许home≤T/2；同一分配可有两个标签，但不是执行两次。

原T调度因宏>T/2每home至多一宏，故有这些模式；同profile替换只降home，sink上界不增。全体组每sink取整总量≤T+Ns=5T/4，不能每home分别花T/4。菜单总量≤2|H|(5N+1)^K；固定K位多项式，可变K不统一。

共同宏可用home集构成transversal matroid，秩b=|B|；真正occupation向量必须落在**base**多面体B(M)，大小b且覆盖全部宏。不是只要求独立集。定义P(Q)为每home模式和1、x_h=occupied质量且x∈B(M)。给定随机base分解，条件于占位按对应正模式比例挑选，证明P(Q)恰是实际匹配及兼容模式的凸包；不要求算法生成长分解。LP用z_bh行和1、列和x_h的匹配扩展。

# 2K核心面引理的自足证明

y正支持每home a_h项，F={0<x_h<1}混合home，G为x在B(M)的最小face。每i∈F存在最优基A、B使i∈A\B，各取全覆盖宏匹配。同一交替路径从i止于某j∈B\A，同时交换得到A−i+j、B−j+i；两个最优性方向才得权w_i=w_j，两新基都在G。交换图覆盖F且每块≥2顶点，其生成森林方向给dimG≥|F|/2。单向可交换不足以推等权。

模式最小face投影整个G；保持每标签内正比例即可lift任意x'∈G。纤维维数Σ_h(a_h−1)−|F|，所以d_P=dimG+Σ(a_h−1)−|F|≥R/2，其中R为a_h≥2的home数。K活跃侧行若压出顶点则d_P≤K，否则可找同时消掉活跃侧行的非零双向小移动。故R≤2K；K0还原积分性，系数无需非负。

若模式依赖具体宏任务大小/身份，则所有occupied模式不再同等兼容原home，凸包不是该base扩展；长交替环可一维改变任意多home，不能套2K。该结构性边界不能由重新命名任务消除。

# 大贡献分支、投影顶点与完整回填

取γ=1/4、β=1/(8K)。原参考取整模式总出口≤5KT/4，因此总出口>βT的heavy homes少于10K²。枚举至多10K² homes及同一实际模式，固定后删除其他heavy模式；原T见证至少保在一支。空模式库仅使该支不可行。

每支LP加各sink预算5T/4，逐全部y坐标lex精确优化并固定，得到唯一y投影顶点。扩展z无需唯一；扩展LP basic point的任意投影不足以套引理。每步是原有界扩展LP的face，固定坐标是原顶点坐标，Cramer统一位界防止逐轮数值放大。

正支持只有occupied的home强制被覆盖、只有empty的禁止，混合自由。原z给带下界分数匹配可行，整数流覆盖全部宏及强制home。按匹配标签选任一支持模式，只有≤2K个非单值home改变，heavy固定home不变。每改变模式总出口≤βT，原LP成本非负，所以每sink实际≤(1+γ+2Kβ)T=3T/2；empty home≤T，occupied private≤T/2加实际宏≤T，亦≤3T/2。没有叠加第二份tiny流，私有组互不交确保每原job恰一次。

DP、模式回溯、有理LP、lex次数和匹配按显式总位长多项式，次数依K；粗枚举指数O(K³)。不按分母数值或1/p_min展开。K0另可直接残余匹配求T可行，但主算法身份K≥1；无私有任务直接宏匹配。

# 未知OPT：不需接受谓词单调

先全零端检查处理OPT0。有限分母乘积D的bits为输入分母bits之和，q*=D OPT正整数。宏非空令a为最小有限宏边，promise a>OPT/2给整数U=2aD−1≥q*，所有q≤U目标T=q/D<2a满足宏>T/2；p>T边仍可剪。宏空时以任意合法调度C取U=DC，不引用a。

初始U目标必须成功并保存σ；维持lo<q*、hi成功，FAIL只更新lo，成功只更新hi。终止hi=lo+1≤q*，返回≤3hi/(2D)≤3OPT/2。不需success集合单调，更不能把成功当T可行。调用O(log(U+1))、每目标bits多项式。宏非空a0、U<1或初始失败时返回未认证，promise内不会发生；promise外不保证近似。不可免费验证的含OPT条件、给定分区和唯一home均承重。

# 历史独立性、有限证据与软件边界

一审者先获精确合同，独立占位基/多维DP；另一内部研究者独立重构核心面维数/支持恢复，之后才对照冻结正文。boss9逐式核链及代码边界。修正包括T0前置、剪宏p>T、空库分支、home存真有理而非重复取整、以匹配双向交换代一般拟阵面黑箱；后加promise外明确返回分支未改变三正式保证。没有新盲审、外审或新颖性认证。

本轮全文读两冻结JSON，不运行：b1c932…为Python3.12.14/seed910217/Fraction，112局部组、997原分配、378模式、468保留见证；4454零目标矩阵/33910分配；26交切案例、6659活跃约束组、58顶点、88支持舍入、12实际恢复，K1/2分别达2/4非单值。16380接受表、1024宏网格只核阈值逻辑；参数K1/2/3/10/100对应heavy10/40/90/1000/100000，不是一般规模scheduler运行。

37cf25…独立不导规范核心，homes1..4、宏0..min(2,h)，所有可全覆盖0/1表示共304，权−1/0/1的20760个带重数暴露面，7002非平凡、5190正维等号、0违反。只测base面核心，不测DP、大贡献枚举、预算LP或输出scheduler。规范活约束顶点枚举是指数审计oracle，绝非数学算法的有理LP后端实现；通用LP及完整枚举软件均未交付。

既有双源页将occupation简写独立集的句子需以本页base合同解释，不能给未覆盖全部宏的向量补充算法保证。无界K、多home私有任务、动态宏/微角色和具体宏边模式仍是缺口；固定K受限正面构造不改变一般UM及六人SPE对象的开放状态。
