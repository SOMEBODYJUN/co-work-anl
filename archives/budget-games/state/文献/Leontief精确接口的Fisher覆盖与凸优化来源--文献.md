---
id: budget-games/leontief-fisher-exact-interface-historical-primary-coverage
kind: literature-resource
type_tag: 文献
title: Leontief精确接口的Fisher覆盖与凸优化来源
status: historical-source-audit; known-interface; no-current-external-verification
summary: 保存2026年10月20日核查的具体版本、定理拼接和实际阅读范围；原文仍称open不抵消具体数学覆盖，不继承为最新文献调查。
legacy_ids: [NA02, NE-FISHER-TRANSFER-v1]
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/notes/leontief_fisher_known_interface.md#独立来源核查
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/multi_lane/research/topic_selection/notes/leontief_fisher_known_interface.md
---

# Leontief精确接口的Fisher覆盖与凸优化来源

这是**历史来源核查资源**。本批全文读取242行主源，包括后半份独立核查，重构[矩阵等价](../等价/Leontief贡献矩阵与线性Fisher支出的精确对应--等价.md)和[坐标恢复](../证明/Leontief对数规划的有理坐标恢复接口--证明.md)。下面“已读/已核”均指原2026-10-20核查所报告的外部读取；本批没有重新打开外部论文、确认当前最新版本、完成其全部证明或认证新颖性。外部链接是精确来源定位，不冒充本批浏览记录。

## P1：原问题确实存在于指定版本

Becker–Fries–Greger–Segal-Halevi，*Efficiently Computing Equilibria in Budget-Aggregation Games*，[2509.08767v3](https://arxiv.org/html/2509.08767v3)（2026-02-24），[AAMAS2026正式PDF](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/CCMB1463.pdf)，DOI10.65109/CCMB1463。原审计核查§§5、8，正式版printed p1311/PDF第8页。

§8 Definition8.1将有理权重$q_i/D$克隆为$D$个equal-share者；Lemma8.2恢复NE；Theorem8.3时间$\operatorname{poly}(m,D)$，是伪多项式。末段明确问weighted、特别Leontief能否普通多项式计算，正式版仍保留。故不能说原候选误读了问题。

但原句“polynomial in n,m”没有完整规定bit model，也没有strongly polynomial字样。对比克隆的$D$和§5二进制估值算法，消除数值分母依赖是合理语义；整理时自行明确$\operatorname{poly}(n,m,L)$，不能将略写$n,m$当成已精确定义所有复杂度细节。§5 Lemma5.4的短有理表示、Lemma5.5引用Jain2007 Thm13，场景为equal-share，不能直接升成一般weighted精确位多项式定理。

## P2：weighted NSW与NE/Lindahl桥梁

Brandt–Greger–Segal-Halevi–Suksompong，*Coordinating Charitable Donations with Leontief Preferences*，JET230:106096(2025)，DOI10.1016/j.jet.2025.106096，[2305.10286v3](https://arxiv.org/html/2305.10286v3)、[v4](https://arxiv.org/html/2305.10286v4)（2025-10-10）、[作者journal PDF](https://pub.dss.in.tum.de/brandt-research/balanced_journal.pdf)。

原审计核查§3模型、§4.3 Theorem1及B.2、§4.4 Proposition1、相应计算讨论（作者PDF printed p12）：任意贡献$C_i\ge0$，public效用$\min_{j:v_{ij}>0}\delta_j/v_{ij}$，与当前模型完全对齐。

- §4.3的weighted Nash welfare最大化给唯一均衡总量；这不是本轮发明的log规划。
- rational估值和贡献给rational最优总量；临界集已知时可用LP。该段对一般贡献仍述pseudo-poly，equal contributions才有binary-input poly，不能凭摘要的efficient继承更强算法。
- §4.4 Proposition1对非均匀预算给public Leontief NE distribution iff Lindahl equilibrium，是接下一篇的桥。

§7的“binary weights”指$v_{ij}\in\{0,1\}$，不是预算的二进制编码。作者[slides](https://pub.dss.in.tum.de/brandt-research/donor_slides.pdf)第33页笼统写rational/poly computation，但该页没有一般weighted新算法证明；宽泛演示文字不能替代上述精确命题。

## P3：决定性的同矩阵public Leontief / private linear对偶

Tao–Zheng，*Fisher Meets Lindahl: A Unified Duality Framework for Market Equilibrium*，[2511.04572v2](https://arxiv.org/html/2511.04572v2)（2025-12-04，初稿2025-11-06）。原审计另记录[STOC2026目录](https://acm-stoc.org/stoc2026/toc.html)，此为历史观测。

原审计实际读§2假设、§3双向utility公式、Theorem2完整statement和主证明、Remark1、相关§4.1 CES例子及§5.1 Theorem5后Leontief PRD说明；**没有审完51页所有dynamics/chores应用**。

§2的private Fisher每good供给一、public Lindahl单位生产成本、预算$B_i>0$；Assumption1要求连续、非递减、局部非饱和、拟凹。每行非空的Leontief满足；零预算、全零列须预处理，不能略掉。

§3 Theorem1后、Example1前明确给：
线性$\sum_j a_{ij}x_j$的dual是$(1/B_i)\min_jx_j/a_{ij}$；
反方向Leontief $\min_jx_j/a_{ij}$的dual是$(1/B_i)\sum_j a_{ij}x_j$。
逐agent正倍乘不改变均衡，所以本题对应**同系数矩阵的private linear**，不是系数取倒数，也不是private Leontief（后者可能有无理均衡）。

§3 Theorem2与Remark1保持agents/goods/budgets，交换public allocation和private equilibrium price，并交换public personalized prices和private allocations。因此$p_j=\delta_j$、$X_{ij}=p_jy_{ij}$是该已知一般定理的特例。§5.1还指出Leontief Lindahl PRD与linear Fisher PRD一致。§1.1 warmup着重public linear↔private Leontief，仅读warmup容易看反方向；本覆盖用的是§3明确反向公式及定理。

## P4：精确linear Fisher求解器及实际输出

Orlin，*Improved Algorithms for Computing Fisher's Market Clearing Prices*，STOC2010 pp291–300，DOI10.1145/1806689.1806731；[19页作者版本](https://drops.dagstuhl.de/storage/16dagstuhl-seminar-proceedings/dsp-vol10171/DagSemProc.10171.2/DagSemProc.10171.2.pdf)、[MIT入口](https://dspace.mit.edu/entities/publication/aeca65f4-08b6-4649-8a19-e123eda7614c)。

原审计核§1.1 money-spending模型、§2 BasicSolution和强多项式版本。其变量$x_{ij}$本就为钱，不是货物比例；行和预算、列和价格、正支出走最大$U_{ij}/p_j$边，逐式匹配本题临界支持。算法返回actual exact equilibrium，并非仅$\varepsilon$价格。原报告复杂度$O(N^4\log N)$，$N$为buyers+goods，另有稀疏改进；本页没有独立重证该复杂度。

原论文用整数预算/估值；[等价正文](../等价/Leontief贡献矩阵与线性Fisher支出的精确对应--等价.md)明确清分母、控制位长、缩回price和spending。必须导入强多项式版本及中间数位长合同，不能以早期依赖$e_{\max}$数值的版本或克隆展开代替。

## 覆盖的四步和判断层次

| 本题需要的接口 | 历史核查定位 | 本轮角色 |
|---|---|---|
| public Leontief NE总量对应Lindahl | Brandt §4.4 Proposition1 | 既有模型桥 |
| 同预算、同$v$转private linear Fisher | Tao–Zheng §3公式、Theorem2/Remark1 | 既有一般对偶 |
| 精确价格及支出/货物分配 | Orlin §1.1及强多项式算法 | 外部算法导入 |
| $\delta=p,\ X=p\odot y$恢复实际public行 | 对偶交换及临界支持 | 本文自足重构，非新工具 |

指定版本P1仍称open与另文具体覆盖可以同时属实。前者不抵消后三步逐式归约；不能据此推断作者沟通、引用遗漏动机或最新版本是否更改。内部独立推导正确，也不等可原创发表。NA02“首次weighted exact bit-poly算法”按此审计退休，保留清楚接口与来源资产，不发送“解决开放题”声明。

## 凸优化备线的精确来源边界

Jiang，*Minimizing Convex Functions with Rational Minimizers*，[2007.01445v5](https://arxiv.org/pdf/2007.01445)（2022-09-20）：原审计读Definition1.1、Theorem1.6、Definitions2.6–2.7。所需oracle对任意查询返回最优YES或非零向量严格分离所有minimizers；minimizer集合需bounded rational polyhedron及有界LCM vertex complexity。“unique rational optimum”五字不足以满足此合同；还需domain扩展、total oracle和位界。本页的弱优化备线不用偷换这一exact oracle。

Vazirani2012，*The Notion of a Rational Convex Program, and an Algorithm for the Arrow-Debreu Nash Bargaining Game*，JACM59(2):7，[作者PDF](https://ics.uci.edu/~vazirani/NBalg.pdf)，[预印本](https://arxiv.org/pdf/1010.4280)：原审计仅§§1、2。RCP定义本身要求polybit rational最优；log加线性约束并不自动保证。其主要算法对象ADNB，不是本题public donor游戏。

Jain2007，*A Polynomial Time Algorithm for Computing an Arrow–Debreu Market Equilibrium for Linear Utilities*，SICOMP37(1):303–318，DOI10.1137/S0097539705447384：原审计只读publisher摘要，Theorem13通过P1 Lemma5.5转述核查，**未直接读其原Theorem13完整证明**。

[GLS书](https://link.springer.com/book/10.1007/978-3-642-97881-4)及Dadush–Hojny–Huiberts–Weltge2024[oracle-model论文](https://link.springer.com/article/10.1007/s10107-023-02005-8)§1，仅作为标准ellipsoid界背景；不能将本题的位多项式后端归作后文新算法已经专门实现。

主源还用两个各预算$1/2$、估值$(1,0),(2,2)$的例子指出：有理效用$(1/2,1/4)$的几何均值无理，故P1 Thm5.3末段“有理坐标使精确目标也短有理、二分命中”的推理不足。该局部论证缺口不否定结论；坐标恢复和Fisher转移均可绕过。

## 搜索历程只作历史反例

原核查记录两套引擎检索weighted Leontief/budget aggregation/donor coordination、Nash welfare rational convex、public-private Fisher/Lindahl；先只见pseudo-poly描述，改变接口关键词后才找到P3并修正判断。因此早期“没找到”不是仍open证明，也不能将一次历史检索当全局查重完成。本批保全其检索边界和结论修正，不扩称实际读完被链接论文。[完整原件、阅读日志与逐段去向](../../../../tools/evidence/cloning-leontief-potential/README.md)可复核。
