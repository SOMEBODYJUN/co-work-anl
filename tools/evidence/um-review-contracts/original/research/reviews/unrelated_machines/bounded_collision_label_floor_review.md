# 低重数标签资源的冻结独立审查

审查者为 boss11 内部子研究者 hardness_route，无独立 Work 身份。此记录只报告实际检查，不认证全球新颖性、外审或一般 UM 主目标。

首次冻结正文：research/current/unrelated_machines/bounded_collision_label_resource_floor.md。

实际先读取整篇版本 SHA256=1afdde037582bb42aa075116a2a669bf28b0f2d6584aff6314152829f67a0e20。随后核对最终修正版 SHA256=3ac04f5eb7780d31a5baf1220b3fd396a69d037c1d516787f801a868fdf4dd8c，实际检查 eta域为0<eta<1且Delta_G在空资源集时用并入{0}的最大值定义。并核查既有 rooted_dag_degree_token_bridge.md §1–5 的实际树到全部任务调度，包括 alpha=0 和根终端分支。

## Statement-first 重构与收到正文后的检查

审查先仅收到精确的有界所给资源碰撞地板，独立从资源独立拥有者和二项尾概率重构了1/Delta下界，随后才收到另一研究者的确定性颜色证明。对新增 UM-GROUP-DEGREE-LABEL-APPROX-v1，也先仅收到陈述，独立构造各组最大局部密度 a_x，降序上界 U=max_s min(s/q,a_(s))，再用所选组资源着色给 U/Delta 的实际树；主研究者随后采用该简化证明。审查不是赞成票：以下核查每个实际义务。

**所给完整束地板。** 每个所给 B_x 大小等于所选正需求，单个资源的所给组关联分别染不同颜色。每组至少在一种颜色取得 ceil(K_x/Delta) 个资源；某颜色的达标组数至少 ceil(q/Delta)。选出这些组后，同色资源单父、标签专属组且各层边仅向下一层，因此是真实根树。根、组、标签三类正需求同时受控，输出叶并未豁免原正需求。Delta由真实所给重数计算，1<=Delta<=q，无巨大二进制循环。非所给标签不必满足重数界。

**二重锐性。** 任意K>=1、两两组共享私有K集合：b>1/2时每选中标签要严格多于K/2资源，所以每对最多一组，与根比>1/2冲突；每对只选一组达到。一般Delta锐性仅用K=1，不能升级为每个K的同一族锐性。

**无见证全局近似。** 全局Delta_G计不同变量组，不能换成同一资源标签入度。在任意实际正评分树中每个选中组至少有一个原标签，故本地最大密度>=树评分；按选中组数得b*<=U。选择达到U的前s组不要求任何源问题见证。每组选择达到其a_x的标签，B_x=min(K,|S|)满足 |B_x|/K=a_x；临时需求仅用于获得本地分配数>=|B_x|/Delta'，最终按原需求评分。Delta'<=Delta_G、s/q>=U、a_x>=U，故所有原比例同时>=U/Delta_G。没有通过私自降低原需求声称更好原评分。

**调度翻译。** 既有桥梁允许任意真实树，包含评分0。其输出包含全部不可拆任务且负载<=2-b(H)，OPT=2-b*。实际代数为

(2-1/Delta_G)(2-b*)-(2-b*/Delta_G)=2(1-1/Delta_G)(1-b*)>=0。

该式只针对桥梁输出族，未声称一般矩阵可逆表示。Delta_G=0且q>=1时没有任何标签资源边，正评分树不存在，根单点与桥梁给真实最优负载2。q=0则根为零需求原终端，根单点评分1、桥梁最优负载1；此分支不除以Delta。

**精度修正已核实。** 首次冻结正文§4的“b*<=eta<1，则ceil(1/eta)”现已将参数域明定0<eta<1；eta=0与所给局部完整选择矛盾，不能在未定义的1/0表达式中默省。最终版另把Delta_G定义为资源组度集合并入{0}后的最大值，使R空时的Delta_G=0分支良定义。两项已在上述最终hash版本实际复核，不影响三项核心命题或证明。

## 有限独立核验

脚本 tests/audits/unrelated_machines/bounded_collision_bundle_independent.py 不 import 规范核心。其实际树 oracle 穷举原资源的全部父标签或 absent，不假定每变量只能保留一个标签；每个正评分树都由其资源父点和祖先唯一恢复。独立构造保留完整Gamma阈值枚举而非主稿的排序生产算法：Gamma={1}并上所有 d/K_e (1<=d<=min(K_e,|S_e|))，全体合格组、首个合格标签、取 ceil(tau K_e) 资源，并按逆组顺序赋色。逐个核对其实际见证、评分、U包络、b*上界、b>=U/Delta_G和桥梁比例代数。

实际运行命令：

python3 tests/audits/unrelated_machines/bounded_collision_bundle_independent.py > /workspace/scratch/038d9dcc4cac/bounded_collision_bundle_independent_run.json

Python3.12.14，seed2026101711。最终脚本 SHA256=b2232aee8aa706bdd755353c9645b51bd4d8120db6cbcef22221a1d614e605d7。

所给束部分：240个全菜单DAG、1056个所给逐组标签证书、500个随机全菜单DAG、9个K=1..9标签对、4个K=1..4双标签对、12个Delta=1..12单资源锐族、3个退化例；421839个实际资源父点选择。

无见证近似部分：4666个DAG，489061个实际资源父点选择。包括六种标签（可行、K>|S|、死端）全部64种局部菜单（含空菜单）在q=1,2的完整乘积；前述500随机例；根终端、缺组、死标签、200位需求、同组多标签单资源及缺组与异质需求混合例。实际见证均逐组、逐资源回算，没有将仅一个数值指标当作树证书。

这些运行均通过。有限运行不替代颜色、排序上界或桥梁的一般证明；规范生产实现还应单独核验。

## 最接近资产与文献

既有 k_uniform_bundle_matching_floor.md 提供t-of-K层匹配恒等，单资源层天然带1/K；当前增加独立于束宽的1/Delta碰撞地板及给定全局组关联度的无承诺比例近似。既有深二层半比例贪心少一个标签选择层；当前不假装消除了该层的一般难度。所有新增结构限定均承重。

在线已实际核实 Bateni–Charikar–Guruswami 作者技术稿 https://mhbateni.com/academic/pubs/maxmin-tech09.pdf §7，Definition7.1/Lemma7.2（实际PDF页47–48、印页47–48）。其三物品Santa-Claus duplication-gadget限制与本文对象不同；当前没有将该旧Paper Fact转记为本团队成果，也不承重调用其算法结论。未开展可认证全球新颖性的完整检索。

## 结论

最终hash版本的两项精度修正均已实际复核，没有仍成立的fatal objection。内部审查支持三项精确定义的地板、锐性及受限类近似；不支持一般近2困难性、不支持UM-TARGET-v1正反结论、不认证外审或新颖性。


## 实现者攻击及主研究者复核

规范构造者另行攻击冻结正文，核实三个Claim和代码一致性；其实现者身份没有被当作独立代码审查。两处定义精度修补已由构造者和独立审查者实读最终hash确认。主研究者亲读一般证明、规范API、独立原父点oracle，并实际重跑两份最终脚本，退出码均零；同时独立枚举小资源集合核着色和成对锐性。

主研究者还实读同期main9fdf36e新增的single_layer_quota_hypergraph_obstruction.md、affine_complement_cardinality_boundary.md和其审查：它们分别管逐t层完整公式和仿射基数解码，与本页低重数的随束宽无关界及全组度算法不同；保留全部原量词和待审限制，未作为本证明前提。
