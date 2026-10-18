# 直线集合打包与累计路径编译中的部分导出障碍

读取目的：直接攻击真实 source 到普通 UM 的两条具体桥，核对 source soundness 能否承受所有 partial exports。第一条是已发表大 gap 集合打包源的均匀菜单编译，第二条是将一个 SC unit bundle 压成 take/continue 路径的候选。两条都已给实际完整矩阵中的逃逸，不否定其它编译或一般主目标。

## 1. 真实 primary 与其证明了什么

**Paper Fact。** Lee、Svensson、Thiery，*Asymptotically Optimal Hardness for k-Set Packing and k-Matroid Intersection*，[arXiv:2409.17831v1](https://arxiv.org/abs/2409.17831v1)。root实际下载14页原PDF（237437 bytes，SHA256 `75c9acd3432958383ffb21b12dd4baf2dacec97e8a183962cde4460dd7884ee2`），亲读§2 Definition2.1、§3 Theorem3.1/Claim3.3及构造证明、§4 Theorem4.1；fee亦独立实际核在线同版原文，不冒认其下载了root本地字节。

原构造取 prime \(R\)、alphabet \(R\)、变量 constraint-degree 至多 \(R\)，用 label 作直线 slope、变量的 constraint incidence 编号作 intercept。每个 constraint 的 allowed tuple 产生一个 \(kR\) 元 set，**完整 sets** 的最大 matching 大小等于可同时满足的 constraints 数。Theorem4.1 的 stated hardness 为固定 \(k\ge4,\epsilon>0\)、充分大 prime \(R\)，YES value \(\ge1-\epsilon\)，NO value \(\le k(1+\epsilon)/((k-3)R)\)，除非 \(\mathrm{NP}\subseteq\mathrm{BPP}\)。不是 perfect YES，也未给 partial-set tiny-retention soundness。

以下 source-specific 障碍的数学是既有 pair-overlap/Hall 的直接应用；不把下载、原论文摘要或标准匹配包装成新主定理。外部原文的证明状态与本页自足的编译分析分开。

## 2. Constraint-as-group 的完整均匀菜单

**ID / Version：`UM-LST2025-AFFINE-LINE-SOURCE-UNIFORM-COMPILATION-OBSTRUCTION-v1`。**

**Objects / Domain / Definitions / Quantifiers。** 任意 prime \(R\ge2\)、\(k\ge1\)、有限变量集 \(X\)、非空 indexed constraints 集 \(G\)。每 \(g\) 恰含 \(k\) 个不同变量 \(X_g\)，每变量属于至多 \(R\) 个 indexed constraints；给注入 \(j_x:G(x)\hookrightarrow\mathbb F_R\)。每 constraint 的显式 allowed tuple 表 \(A_g\subseteq\mathbb F_R^k\) **非空**，state 就是其中一个 tuple。重复 indexed constraints 允许，但 incidence 编号仍不同。

资源为带变量tag的 \(U=\biguplus_x\{x\}\times\mathbb F_R^2\)。定义

\[
 E_{x,g,a}=\{(x,z,az+j_x(g)):z\in\mathbb F_R\},\qquad
 S_{g,s}=\biguplus_{x\in X_g}E_{x,g,s(x)}.
\]

每 state 恰 \(D=kR\) 个 distinct resources，各 private 权 \(1/D\)。构造完整普通 UM：每 indexed state 一台 private \(M_{g,s}\)，每资源一台 \(R_u\)；每 group 一件 selector1，仅本组所有 private 有资格；每 state-resource 一件不同 incidence，只在自身 private 用 \(1/D\) 或该唯一资源机用1，余端 \(\infty\)。全部未选 states 的 jobs 保留，无其它预载或逻辑。

**Exact Statement / Conclusion。** 对每个这种输入、**每一任意完整 local state 选择** \(s(g)\in A_g\)，可确定性总位多项式给全局不交 \(B_g\subseteq S_{g,s(g)}\)，每组恰 \(b=\lceil kR/2\rceil\) 项。因而不输入源 witness 或 OPT，就能输出全部原 jobs 的具体调度，满足

\[
 C_{\max}\le2-\frac{\lceil kR/2\rceil}{kR}\le\frac32. \tag{1}
\]

该 b 不声称逐输入最优；结论不依赖 local labels 来自共同 CSP assignment。

## 3. 所有 Hall 子集与全部原任务的证明

固定任意所选 states、任意 group 子族 \(F\subseteq G\)。对变量 \(x\) 令 \(r_x=|F\cap G(x)|\le R\)。其 \(r_x\) 条 selected lines 各 \(R\) 点，因不同 indexed constraints 的 intercept 注入，不会重合；同 slope 不交，异 slope 恰交1点。二阶容斥给

\[
 |\bigcup_{g\in F\cap G(x)}E_{x,g,s(g)(x)}|
 \ge r_xR-\binom{r_x}{2}\ge\frac{R+1}{2}r_x.
\]

多线共点只使这个下界更松。变量资源有tag，\(\sum_xr_x=k|F|\)，故**每个** \(F\) 都满足

\[
 |N(F)|\ge\frac{k(R+1)}2|F|\ge\lceil kR/2\rceil|F|.
\]

最后一步也含 \(kR\) 奇数，因为 \(\lceil kR/2\rceil\le kR/2+1/2\le k(R+1)/2\)。整数容量 flow 或每组 b 槽的 Hall matching 给每组 b 枚真实资源，不要求 bundles 按变量/line分解。

每 selector 放所选 private，仅将该 state 的 \(B_g\) 原 incidence 导出；所有其它 incidence，包括每个未选 state 的全部 jobs，留自身 private。Selected 负载 \(2-b/D\)，未选为1，资源至多1，所有原任务恰一次，得(1)。\(G\ne\varnothing\) 使 selector 给 OPT\(\ge1\)，所以也给该精确结构类至多3/2的实际近似比。

若另给真正全满足的源赋值，同变量所选 lines 的 slope相同、intercept不同，所以全部所选资源 sets 不交，得 OPT=1。但 primary 的 near-perfect YES不自动提供这个更强见证。更改 grouping 为每个 allowed tuple 自成 group 再加 global dummy 后，不再自动保证 \(r_x\le R\) 与直线不重合，须重证这些不变量；**本页不排那个不同 compiler**。

**Assumptions / Scope / Dependencies。** 非空 relation、degree上界、intercept注入、不同变量tag、均匀权与此完整矩阵均承重。若 \(A_g=\varnothing\)，保 selector 会无合法端，不能静默称为普通UM输入；删除 constraint、加 dummy 或其它编码须另证源promise。对同 constraint重复变量、非uniform权、加入其它实际jobs亦不免费延伸。依赖显式构造及普通容斥/Hall，不依赖 source hardness 本身。

**Complexity / Evidence / Counterevidence / Status / Related Files。** 令 \(v=|X|,m=|G|,a=\sum_g|A_g|,L=kRa\)。机器数 \(vR^2+a\)、原jobs \(m+L\)、finite条目 \(2L+a\)、dense条目 \((vR^2+a)(m+L)\)。按这份显式总输入/输出编码长度计，构造、flow及所有job输出位多项式；不称对 \(\log R\) 的 succinct编译，固定 source \(k,R\) 时才直接为其源输入上的多项式。作者Proof、fee Exact-first/作者读后与最终正文实读见[审查](../../reviews/unrelated_machines/lst2025_affine_line_uniform_compilation_review.md)；root亲读原PDF并独核全部Hall子集。无 standing fatal，无软件/优化枚举，标准技巧非原创，外审/全球新颖性未认证；主目标未解。

## 4. 累计路径 take/continue 规则的明确反候选

**ID / Version：`UM-PARTIAL-SUM-TAKE-CONTINUE-FLAT-MENU-ACTUAL-ESCAPE-v1`。**

**Objects / Domain / Definitions。** 源 SC 有3 agents及2件不同不可拆 items \(u_1,u_2\)，每名agent对每item值均 \(3/5\)，row总 \(6/5\)。考察把一条 unit累计路径的 take credit \(c\) 写成 normalized additive state \(\{\text{原item}:c,\text{下节点own}:1-c\}\)，下一节点有 own/off，终点 fresh accept 的**明示规则**。本源的单agent unit路径 credits 为 \(3/5,2/5\)，第二个credit不超过原值。

目标共享资源 \(u_1,u_2\)，每个 \(a=1,2,3\) 另有互异 \(x_a,y_a,z_a\)。每agent产生3个真实groups，全部菜单如下：

| group | state | 资源与 private 权 |
| --- | --- | --- |
| \(r_a\) | take1 | \(u_1:3/5,x_a:2/5\) |
| \(m_a\) | off | \(x_a:1\) |
| \(m_a\) | take2 | \(u_2:2/5,y_a:3/5\) |
| \(l_a\) | off | \(y_a:1\) |
| \(l_a\) | accept | \(z_a:1\) |

每state独立private、每资源独立global resource机；每group一件unit selector仅本组所有private；每state-resource一件原incidence仅private表内权或resource1，余端∞。没有其它资格/任务/约束，**未选off jobs也全部存在**。共26机器、30jobs（9selector、21incidence）、57finite条目。\(V\) 为每group选一state并领取任意全局不交资源子集的最小private质量最大值。

**Exact Statement / Quantifiers / Conclusion。** 此常数显式对象精确有

\[
 \operatorname{OPT}_{SC}=0,\qquad V=2/5,\qquad \operatorname{OPT}_{UM}=8/5. \tag{2}
\]

因此此规则不存在把任意目标正 partial值 \(\delta\) 总能解码为每个原agent \(c\delta\) 效用的合同，任意统一 \(c>0\) 都不行，即使允许重新安排全部原items。否定的是此具体新增AND步骤，不否定所有DAG compiler或既有[selector-tree](degree_three_weighted_menu_cube_embedding.md)的原normalized leaf合同。

## 5. 全部30 jobs的达界与任意调度下界

源只有两不可拆items、三agents，至少一人无item，所以SC最优恰0。目标选择各 \(r\) 的take1、\(m\) 的take2、\(l\) 的accept，分别领取 \(x_a,y_a,z_a\)，质量 \(2/5,3/5,1\)，全局不交；两个原items完全不用。任意 min质量\(>2/5\)的分配则迫三个 roots 都领取唯一 \(u_1\)，矛盾，故 \(V=2/5\)。

完整actual把9selectors放上述states，导出9件对应own/accept的incidences，其余12件incidences均留自身private，含全部未选off jobs。每agent五台private的负载为 \(8/5,1,7/5,1,1\)，九台辅助资源负载1，\(R_{u_1},R_{u_2}\) 为0。全部30 jobs恰一次、原端合法，峰8/5。

若任意完整实际调度有 \(C<8/5\)，每个root selector只有唯一take1端，\(u_1\)-incidence若留private就与selector给8/5，所以三件不同的root原jobs都必须去同一 \(R_{u_1}\)，其总负载3，矛盾。不限制其它selectors或未选state的额外exports。这是所有完整实际调度的下界，闭合(2)。

该目标正值 \(\delta=2/5\)，但源根本没有让三人都正值的allocation，正常数decoder连存在性都失败。Full target质量1时一个state的两正权部分须同时领取，不意味着小partial阈值也强制AND；本例连DAG共享或错误路径都不需要。完整 leaf、其它守卫、耦合activation或不同实际矩阵均需另分析，不能引用本反例否定。

**Assumptions / Scope / Dependencies / Evidence / Counterevidence / Status / Related Files。** 常数显式矩阵及不可拆items为全部前提，不假设源复杂性、不给通用counterexample最小性。原名含Exact的作者完整来源本身已含证明；general先读它所做的是实际构造/证明与Fraction核验，不能算盲审，原标签已另冻结纠正，旧字节不改。root另冻真正statement-only，fee仅据它独立给出30job证书和任意调度lower，之后才读含证明来源，补全真正陈述先行审查。root亲读所有记录，并从本页五行state表独立重建26机30job全部57条有限资格，与general证书逐项相等，再按Fraction回算全部任务的实际端、每机负载及不交bundles；[固定证书审计](../../../tests/audits/unrelated_machines/audit_query_return_source_fixed_certificates.py)与[冻结输出](../../../evidence/runs/unrelated_machines/query_return_source_obstructions_v1/root_full_matrix_verification.json)仅核达界证书，不进行此实例优化枚举。对应[实际审查](../../reviews/unrelated_machines/partial_sum_take_continue_actual_escape_review.md)把两人的证据归属分开。数学完整，无 standing fatal；有限证书只作checks、不承担一般compiler不可能证明，外审/全球新颖性未认证；UM-TARGET-v1仍OPEN。
