# 宽标签矩形下，仿射线的重资源与细资源可共同避冲突

## 精确身份与读取目的

- **ID/version**：`UM-TAGGED-AFFINE-LINE-WIDE-RECTANGLE-JOINT-ESCAPE-v2`。v1只冻两个推论，v2给统一marked/unmarked合同；只登记成熟v2，不把原v1倒改成已审v2。
- **Objects / Domain / Definitions**：prime R≥2；显式非空groups、每group非空变量集及indexed-state菜单；每变量独立tagged F_R²完整资源块，各incident group的固定intercepts单射。每state在每变量上有一条完整line，所有非负有理private权总1，包含zero。每group给Cartesian标签矩形，所有矩形vectors均在菜单中出现。
- **Quantifiers / Exact Statement / Conclusion**：对下述所有完整输入，若每条line给≤b个marked点，其余每点权≤β，且最小矩形边长L>b(D−1)，可det-bit-poly共同选择indexed states及互不相交的B_g，包含所有selected marks与全部selected独占点，每组质量≥v=max(0,1−Mβ)。同一完整原UM矩阵可输出全部原jobs实际峰值≤2−v。这里M=max_gΣ_(x∈X_g)(d_x−1)≤q(D−1)。
- **Assumptions / Dependencies**：无复杂度假设；`UM-MODEL-v1`和下述完整显式矩阵/rectangle/marks承诺。有限域计数与全调度自足，不调用CONFIG、未知actualYES或概率分布。
- **Scope / 额外信息**：真正新增信息是每组可独立选坐标的足够宽Cartesian状态自由度。Marks可依赖整个indexed state及所有权；不是分别找重、细两份allocation后相加。结论对所有合法固定intercepts成立。仅此宽矩形子域，不宣称所有LST/Chan hard images有该自由度。
- **Evidence / Objections**：bicriteria先仅据v2 Exact独立全文重构，root实际全文读后才解封作者Proof，再实际作者读后及最终canonical指定scope审；root先听口头策略不记盲审。原v1仅历史Exact，不虚构v1 Proof或v1审查。来源见[审查](../../reviews/unrelated_machines/tagged_affine_line_wide_rectangle_joint_escape_review.md)。
- **Status**：限定共同构造证明完整；独立先行、作者读后与最终正文审查各按实际范围记录。无软件、有限实验、外审或全球新颖性认证；`UM-TARGET-v1`仍OPEN。
- **Related Files**：[uniform单边际的反例](tagged_affine_line_uniform_marginal_gap.md)、[任意权下完整并行关系的半保留](weighted_affine_parallel_relation_reweighting_obstruction.md)、[审查](../../reviews/unrelated_machines/tagged_affine_line_wide_rectangle_joint_escape_review.md)。

## 1. 完整对象与统一合同

变量集X可含unused variables。G非空；每X_g⊆X非空且无重复变量，S_g非空且indexed。令q=max|X_g|，d_x为使用x的groups数，D=max_x d_x≥1。每(g,x)给固定j_x(g)∈F_R，同一x的不同groups取不同intercepts，所以d_x≤R。不同变量的资源块U_x={x}×F_R²带不同tag。

State s给slopes a_(g,s)(x)及完整资源集

\[
T_{g,s}=\bigsqcup_{x\in X_g}\{(x,z,a_{g,s}(x)z+j_x(g)):z\in\mathbb F_R\}.
\]

每个真实incidence有权p_(g,s,u)≥0，且Σ_(u∈T)p=1。不同indexed states可有相同label vector但任意不同权；没有与label唯一绑定的定价承诺。全部line的zero cells均保留。

输入给非空显式A_(g,x)⊆F_R，使∏_(x∈X_g)A_(g,x)包含于菜单label vectors集合；菜单可比此rectangle更大，重复vectors仍保留为不同states。令L=min|A_(g,x)|。每条state-variable line给显式marked子集E_(g,s,x)，|E|≤b，b≥0为二进制整数。所有unmarked点权≤β，β≥0为二进制有理数。Marks允许含zero，亦允许依赖整个state。

令M_g=Σ_(x∈X_g)(d_x−1)，M=max_g M_g≤q(D−1)。在L>b(D−1)时，下文算法输出s(g)及互不相交的B_g⊆T_(g,s(g))，使

\[
E_g:=\bigcup_xE_{g,s(g),x}\subseteq B_g,
\quad T_g\setminus\bigcup_{h\ne g}T_h\subseteq B_g,
\quad p_g(B_g)\ge\max(0,1-M\beta).
\]

这是同一整数解对所有groups同时成立，未声称完整T_g互不相交。

完整普通UM每indexed state一private、每resource一机器；每group一selector，在本组任意private用时1；每state-resource incidence是一不同job，只能在自身private耗p或对应resource耗1，其余∞。全部selectors、未选states的全部jobs、zero jobs均必须调度。

## 2. 避开旧marks后再读取新state

按任意固定顺序处理groups。当前g在变量x上每个较早selected marked点(x,z,y)对新line y=az+j_x(g)至多禁止一个slope：z≠0时唯一可能a=(y−j_x(g))/z；z=0时y等于旧intercept，因其不同于j_x(g)，禁止零个slope。算法不修改intercepts。

较早marked点至多b(d_x−1)个，故禁止的不同slopes少于L。扫描A_(g,x)选一个合法slope，每坐标独立选择。Rectangle containment保证所获完整vector对应至少一个真实indexed state。查表固定该index后，才读取它自己的完整权和marks，并用于后续groups的禁表。相同labelvector的另一state的权或marks不能替代它。

新整个line避开全部旧marks，因此新marks也避开旧marks。归纳可选完所有states，使E_g两两不交。新marked点仍可能撞到旧unmarked点；下面在同一allocation内计入这部分实际损失。

## 3. 共同分配与全部原jobs

选态完成后取

\[
Q_g=T_g\setminus\bigcup_{h\ne g}T_h,
\qquad B_g=E_g\cup Q_g.
\]

E_g两两不交，Q_g不属于任何其它selected support，所以全部B_g两两不交。某点若在g中marked而在h中unmarked，只归g，不在Q_h或E_h；只以unmarked身份被多个groups共享的点可以全部不领取。

固定g在变量x上的line，与每个其它同变量group的line至多交一点：intercepts不同且slopes相同时平行；slopes不同时恰交一点。不同变量资源带tag。因此g的全部共享点数至多M_g。任何没被g领取的点都是它自己的unmarked共享点，权≤β，故

\[
p_g(B_g)\ge1-M_g\beta\ge1-M\beta.
\]

质量非负，得到v=max(0,1−Mβ)。这里已经为marked夺取旧unmarked点同时付过账，没有把两份各自可行但相互冲突的分配叠加。

调度把selector放在selected private，把selected state中B_g的incidence jobs导出到resource，所有其它incidences留自身private。每个原job恰一次，全部资格为原finite端；zero导出仍按真实resource时间1收费。每resource≤1；每未选private负载恰1；每selected private负载2−p_g(B_g)≤2−v。v∈[0,1]，故全机峰值≤2−v，包括v0端点。每合法调度至少执行一枚unit selector，OPT≥1；v1时输出峰值与OPT均恰1。

## 4. 两个推论与边界

**稀疏正点。** 每条line至多b个正点时，全部正点marked、β=0。在L>b(D−1)下每组取得质量1，完整原UM实际OPT=1。b=0且β0时norm1非空域无实例；这不需对0求逆。

**任意权半保留。** D>1且L>2q(D−1)²时，取K=2q(D−1)、β=1/K、b=K；将每state所有p>β的点标记。因state总权1，严格超过1/K的正点总数小于K，逐line当然≤b。阈值等号点留作unmarked，仍满足权≤β。现在L>b(D−1)，Mβ≤1/2，所以每组≥1/2，完整实际峰值≤3/2。只扫描真实大点列表，不按K数值复制任务。

**M0/D1。** M=0等价于每个出现变量degree1：否则任一使用degree≥2变量的group有M_g≥1。不同groups资源块因此分离，任取states可全领取，实际OPT=1，不除以D−1。unused变量资源空置。主合同的β0、b0及R2、q1、单group均由原证明覆盖。

严格条件不能在所有输入上直接改成≥：R2单变量，两singleton-state groups的intercepts0/1、slopes0/1，唯一共同点(x,1,0)在两state中各权1并marked，其余完整line权0。各A singleton给L1=b(D−1)、b1/D2/β0，但无法同时领取marked点，V0、完整实际OPT2。此只核严格界必要的一个边界例，不证明该门槛对所有参数全局锐利。

## 5. 显式位复杂度与否定范围

全部planes、完整state label/line权表、marks及rectangles显式给出或实际展开。Rectangle containment可先核：计算菜单中落入rectangle的distinct label vectors数c_g，与binary整数∏|A_(g,x)|比较。所数vectors是rectangle子集，等数当且仅当containment；product位长≤Σlog|A|加常数，不枚举超过输入的巨大product。同vector的实际states不合并，只在此计数时去重。

禁slope与选label扫描真实列表，查出真实indexed state，再扫描selected完整supports构造Q/B并输出全部jobs。b巨大、β极小或0均仅做binary比较及有理数运算，不迭代b、1/β或分母数值。非零场元素求逆按O(log R)位输入进行，z0单独处理。标准精确有理求和的位长受输入总位长的多项式控制。

设n=Σ|S_g|，m=RΣ|S_g||X_g|，u=|X|R²，h=|G|。实际机器n+u、jobs m+h、finite entries2m+n；zero private端仍计一个finite entry。Dense矩阵与全部assignment输出均为完整展开输入大小的多项式，不声称仅binary R/compact CSP/权oracle的poly(log R)。

本合同对所有合法固定intercepts成立，不只是存在可重编号的一份source。但要应用于某困难源，仍须验证该源确有给定rectangles及所需R/D/q/b不等式；不能由‘可扩大alphabet’推断所有compilers必在域内，也不把标签pairwise independence自动当作宽矩形。Code-coset菜单可能没有非平凡矩形。源perfect completeness、hardness、实际NO decoder均非本定理已关闭的义务；主目标仍OPEN。
