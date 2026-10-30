---
id: "unrelated-machines/pi-simplex-tagged-line-proof-interfaces-and-review"
kind: "review"
type_tag: "审查"
title: "公共simplex仿射线菜单的证明接口与审查边界"
status: "five-historical-sources-integrated"
truth_status: "scoped-exact-family-rechecked; no-robust-hardness-or-general-algorithm"
review_level: "five-full-source-reads; full-canonical-and-existing-simplex-object-compared"
summary: "接回公共四维simplex/coset反例的原证明和独立审查；展开全pairs、helper目标点恢复、CSP值、投影重复state、稀疏/稠密规模、singleton矩形和删main即unit的准确边界。"
legacy_ids:
  - "UM-TAGGED-AFFINE-LINE-PI-SIMPLEX-TINY-VALUE-v1"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/tagged_affine_line_pairwise_independent_simplex_tiny_value_exact_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/tagged_affine_line_pairwise_independent_simplex_tiny_value_proof_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/tagged_affine_line_pairwise_independent_simplex_tiny_value_v1_independent_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/tagged_affine_line_pairwise_independent_simplex_tiny_value_v1_author_proof_read_after.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/tagged_affine_line_pairwise_independence_boundary_simplex_v1_final_scope_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/tagged_affine_line_pairwise_independence_boundary.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/tagged_affine_line_pairwise_independence_boundary_review.md"
---

# 已吸收的主对象与本批增量

本五源属于公共四维simplex、局部全pairs均匀的多primary反例。其主构造、V、完整普通OPT及CSP值已经在[仿射线单primary与单边际趋二双源审查](仿射线单primary与单边际趋二双源审查--审查.md)第3节展开，本批不复制第二份主定理。这里补回原始自足证明的关键接口、独立稿额外边界、精确规模和实际审查链。

这与刚另补的[每组Rstates单标签边际反例](../反例/单标签均匀边际仿射线菜单的趋零保留--反例.md)不同：本对象每组R⁴个states，全部变量pairs均匀，helper联合包含R+1个primary，$V=2/(R+1)$；后者每组Rstates、不具PI、$V=1/(R-1)$。PI反例逻辑上也否定更弱单边际充分性，但不能将来源构造和精确数值合并。

五源均实际全文读取；另用 `clean show` 全文读取当前合并canonical `272262722a54067c48fd` 及专门review `39a4d75750002384dde4`，并比较既有simplex正文和单边际对象。最终canonical SHA为 `0b94156ecd6552e8ab29961ce03a5d21ddfa75cb945ab802da7115bf781970bf`。原件五份共66797字节，完整ID、双冻结提交、SHA、blob及原字节路径见[manifest](../../tools/evidence/pi-simplex-history/manifest.json)。

# 准确对象与代码接口

域限odd prime $R\ge3$；选非平方 $\nu\in\mathbb F_R$，

\[
K=\mathbb F_R[\omega]/(\omega^2-\nu),\quad
\operatorname{Tr}(a+b\omega)=2a,\quad
\mathcal T=\{1+c\omega:c\in\mathbb F_R\}\cup\{\omega\}.
\]

T按给定顺序列出R+1个一维 $\mathbb F_R$ 方向。Blocks为 $\mathcal B=K\cup\{\infty\}$，$B=R^2+1$；parts为 $\Pi=\mathcal B\times\mathcal T$，共同arity $q=B(R+1)=(R^4-1)/(R-1)$。对 $\zeta=(u,v)\in K^2$，令

\[
w_a(\zeta)=u+av\ (a\in K),\qquad w_\infty(\zeta)=v,\qquad
E_{a,t}(\zeta)=\operatorname{Tr}(t w_a(\zeta)),
\quad C=E(K^2)\subseteq\mathbb F_R^q.
\]

每part一个primary $x_{a,t}$。Main参加全部q个primary，relation C；每个 $H_{a,j}$（$j\in\mathbb F_R^*$）在本block的R+1个parts参加相应primary，在其它每part参加只属于它的fresh变量。每组恰q个不同变量、每part一变量、全部K²的R⁴个indexed states保留。Helper完整relation为同一C的coset：本block减j、其它坐标不平移。Primary截距为main的0和本block各helper的非零j，degree R；fresh截距0、degree1。

每变量有完整tagged $\mathbb F_R^2$ 资源平面，每state给每个参加变量一条整线，全部qR点incidences保留。Main state指定 $\alpha=-u/v$（v≠0）或∞（v0），只在

\[
\mathcal D_\alpha=\{(x_{\alpha,t},1,0):t\in\mathcal T\}
\]

的R+1点各给 $1/(R+1)$；helper只在本block某个 $\mathcal D_a$ 点给权1。其它所有完整incidences，包括fresh lines，权0。Helper目标方向为有序T中第一个满足 $\operatorname{Tr}(t w_a(\zeta))=0$ 的 $t_0$。

以下证明接口说明这些对象全部合法；它们不是额外source假设或不透明code oracle。

## 全pairs均匀包括fresh variables

Trace配对为 $\operatorname{Tr}((A+B\omega)(C+D\omega))=2(AC+\nu BD)$，矩阵diag(2,2ν)在odd域非退化。Block0与∞的t=1、ω坐标分别恢复u、v，故E单射、C维数恰4，R⁴个完整tuples互异。

作者Proof分同block与异block证明pairs：同block的不同projective t给独立trace forms；不同finite blocks a≠b时 $(u,v)\mapsto(u+av,u+bv)$ 是可逆K-linear map，finite/∞同理。独立稿另统一看系数向量 $(t,ta)$ 与 $(0,t)$：它们恰列尽 $\mathbb F_R^4$ 的全部不同一维方向，任意两forms秩2。Uniform ζ的每个pair取值有R²个原像，每个单坐标有R³个原像。

Helper只是固定coset平移，故所有实际变量pairs——primary/primary、primary/fresh、fresh/fresh——均精确uniform。Fresh**私权为0**不表示其labels恒0；仍须使用完整E-coordinates。不能只核primary边际后声称全pair PI，也不能删fresh后仍称同一padded code。

## t0存在及任意helper正点的显式恢复

非零w的trace-kernel是一维，T中恰一个代表令trace0；w0时所有代表可用，first规则合法。Main选定block的w为0，所以其中labels全0，截距0的线在z1经过y0。Helper在t0处实际slope−j、截距j，同样经过该原资源；所有state的权总1，无v0/ζ0缺口。

原独立稿还给确定目标点的显式公式：对 $t=A+B\omega\in\mathcal T$，取

\[
w_t=\nu B-A\omega\ne0,\qquad\operatorname{Tr}(t w_t)=0.
\]

其唯一零方向就是t。Finite block a用原state $\zeta=(w_t,0)$，∞用 $(0,w_t)$，helper的onehot即可落在指定 $\mathcal D_a$ 点。作者Proof以非退化配对求非零正交w给同一finder，两种论证均保留。给定w_a其实有R²个原ζ；完整fresh labels区分它们，不能因本block投影重复而合并states或漏其zero jobs。

# 已有精确值的证明去向与完整任务

已有第3节的精确值在原五源中由以下独立义务联合闭合：

| 义务 | 实际论证，不可省略的量词 |
| --- | --- |
| 全partial上界 | 若某helper质量0，min已≤2/(R+1)；否则每helper必须领取其state唯一unit正点。每block R−1 helpers占R+1个D_a点中的R−1个不同点，任意main所选state的D_α至多剩两点。因此对所有states/任意partial，$V\le2/(R+1)$。 |
| 达界分配 | Main用ζ0、在D∞预留两点；每个block的helpers各取R−1个不同点，通过上述finder返回真实原states。所有helpers质量1、main质量2/(R+1)，全部blocks同时分配、真实tags不交。 |
| 完整ordinary上界 | 每group selector放所选private；main外送两正jobs、helper外送唯一正job；其它全部incidences留自身private，包括所有未选states、fresh和zero。Selected main负载2−2/(R+1)，selected helpers/unselected private/resource≤1。 |
| 任意完整actual下界 | C≥2分支平凡；C<2时实际selector确定state，helper正job若留private会与selector成2，故必须外送。Resource unit容量迫每block占R−1不同D_a点，selected main至多外送两正jobs，其private至少2−2/(R+1)。未选states额外exports只占容量，不假设其不存在。 |

故原主值准确为

\[
V=\frac2{R+1},\qquad\operatorname{OPT}_{\rm UM}=2-\frac2{R+1}.
\]

普通P编码依合并canonical第1.3节通用norm-one定义：每indexed state一private、每tagged资源一resource、每group一unit selector、每完整incidence一private p/resource1的原job，其余无穷。该定义依赖没有把one-primary特殊前提带给simplex；所有zero和未选state jobs始终存在。R3给1/2与3/2，R2不在trace构造域，不能从one-primary允许R2推过来。

# CSP精确值及两种block常量排除证明

对应ordinary additive-CSP每group一个q-ary约束，接受本组的common C coset，全局变量是实际primary和fresh变量。定义二维block code $F(w)=(\operatorname{Tr}(tw))_{t\in T}$。作者Proof证明每个F(w)至少有一个零坐标（非零w有kernel方向，w0显然），故不含非零常量。独立稿另比较t=1与1+ω再用t=ω，若F(w)=c·1则先得Tr(ωw)=0、再得c0；同样排除非零常量。

因此各 $-j\mathbf1+C_{\rm block}$ cosets两两不交。Main满足时每block在j0 coset，没有helper满足；main不满足时每block至多一helper，总数至多B。给全部primary label−1，各block选 $H_{a,1}$ 的ζ0并把其专属fresh设0，B个helpers同时满足；其它fresh可任意（也可全0）。Main不能接受非零常量primary tuple。由此

\[
\operatorname{val}_{\rm CSP}=\frac{B}{1+B(R-1)}.
\]

Fresh completion不冲突是它们专属每helper的结果；local PI分布不是全局赋值，local certificate不替代这份全局证明。这个小CSP值也不是计算困难性源。

# 原摘要未展开的三个结构边界

**只有singleton Cartesian rectangles。** 独立稿的额外观察：固定非零ζ，零trace的coefficient directions组成三维超平面的projective directions，恰R²+R+1个；全部q个方向中，非零codeword恰有R³个非零坐标。因此C不含weight1向量。若某coset含一条side有至少两个元素的Cartesian rectangle，固定其它坐标取两vectors之差就得到C中的weight1向量，矛盾。所以各side只能singleton。本观察独立于V/OPT/CSP主证明，不是作者Proof§9的前提，也不是软件检查；它准确解释全pair PI不带来宽坐标矩形自由度。

**删去唯一main后全unit。** 此处删除的是整个main group：其selector、全部main-state incjobs和private roots，不是只删一件任务。保留所有helpers及resources，每block R−1 helpers可注入R+1个D_a点，选中onehot外送、其余全部helper jobs停车，含未选/zero，得V1与完整峰1；剩余selector给OPT≥1。这说明tiny minimum由一个diffuse main瓶颈承担，不提供删除预算/dummy-budget稳健性或许多groups同时低质量的结论；也无需引用one-primary unit theorem作证明前提。

**去padding只保值，不保所有结构标签。** 删除fresh变量、它们的zero incjobs及资源planes，辅助未填充模型的main arity q、helper arity R+1，已不是共同arity对象。保留全部R⁴ indexed states/private/selector，helper的投影tuples可能重复；不合并它们。Partial删/补空zero点质量不变，任意unpadded调度将删去的零jobs补回自己的private不增峰，反向投影不增负载，故V和OPT双向不变。Fresh labels承担原common C/partiteness/全pair声明，不能因权0而免费丢掉后仍称同一完整关系。

# 规模：完整有限资格表与dense矩阵是两种计量

记 $H=B(R-1),G=1+H,q=B(R+1)$，精确

\[
N_{\rm var}=q+H(q-(R+1)),\quad N_{\rm state}=GR^4,\quad
I=GqR^5,\quad N_{\rm resource}=N_{\rm var}R^2,
\]
\[
N_{\rm machine}=GR^4+N_{\rm var}R^2,\quad
N_{\rm job}=G+I,\quad N_{\rm finite}=2I+GR^4.
\]

Private0也占一有限端，local probability $1/R^4$ 只是certificate、不是额外处理时间。q/G为O(R³)，变量O(R⁶)、states O(R⁷)、machines/resources O(R⁸)、jobs/incidences O(R¹¹)，所以完整**sparse finite-options**、state/label/line表和local certificates为 $O(R^{11}\operatorname{polylog}R)$。若物化所有infinity端的dense job×machine矩阵，则有 $O(R^{19})$ 项，编码再乘polylogR。

Exact的O11按其已定义的有限端表示解释；作者Proof、先行独立稿及读后/final均明确区分O19 dense，并非改V或普通矩阵。不能把“完整”误写成O11 dense。所有finite数值仅0、1/(R+1)、1；查非平方、field/trace、finder、CSP达到赋值、全jobs assignment按实际展开总位长多项式，不声称binary R输入下poly(logR)免费输出，也不按隐藏reciprocal复制对象。

# 五来源的实读与认证范围

| 全文读取来源 | 独有内容及本页去向 |
| --- | --- |
| `8f33d3aa3779f9f3f9af`，[Exact](../../tools/evidence/pi-simplex-history/original/tagged_affine_line_pairwise_independent_simplex_tiny_value_exact_v1.md) | 第1–7节完整二次域/一个公共C、实际fresh/parts、全部R⁴ states、state-dependent权、全V/actual/CSP、精确counts及scope；原为statement-only且root先参与讨论，不具blind。主体已有旧第3节，本页保细化接口与证据身份。 |
| `2ff118e6f21b95d1e0e2`，[作者Proof](../../tools/evidence/pi-simplex-history/original/tagged_affine_line_pairwise_independent_simplex_tiny_value_proof_v1.md) | 第1–9节trace与projective方向、全pairs、所有正点/任意目标可达、全partial/full-UM、CSP零坐标论证、O11/O19区别、唯一main删除和source参数边界。其自述未读reviewer记录不提升为reviewer可独立观察的事实。 |
| `721c319202cfcbc4aec4`，[独立重构](../../tools/evidence/pi-simplex-history/original/tagged_affine_line_pairwise_independent_simplex_tiny_value_v1_independent_review.md) | 第1–10节从唯一Exact重构全证明，另给显式w_t、统一系数forms的pair证明、常量的另一排除法、unpadded重复tuples/双向保值、min-distance R³→singleton矩形。全部独有增量在本页对应段展开，不因主值已吸收丢弃。 |
| `43a7fe838c67f7259d29`，[作者读后](../../tools/evidence/pi-simplex-history/original/tagged_affine_line_pairwise_independent_simplex_tiny_value_v1_author_proof_read_after.md) | 第1–8节核作者全部九节，与先行独立构证比较；明确未读one-primary Claim，后续尚未给canonical时不预认证，唯一main删除/固定arity与source参数边界保留。 |
| `25f7f1cebf213af8166c`，[最终scope](../../tools/evidence/pi-simplex-history/original/tagged_affine_line_pairwise_independence_boundary_simplex_v1_final_scope_review.md) | 第1–8节实际全文读精确0b941版本，只认证simplex shared header+第3–8节；实际核第1.3通用V/full-P及line定义依赖，第1–2仅context，不代general审one-primary。原hash链不改，不预认证未来字节。 |

真实顺序是bicriteria只读Exact先独立冻结（当时作者Proof尚未冻结），root实际读后才取得/解封作者Proof，reviewer再读作者全文，最后读指定canonical。作者Proof称未接触reviewer推导属于作者provenance自述，读后稿明确不把它当reviewer可独立观察的附加事实。Root在Exact前参与构造讨论，typed合并页只是据已读材料编排，不是第三次独立审查。

最终scope认证simplex与§1.3定义，不认证one-primary特殊条件化/LP/unit定理，亦未读它的原raw。反过来one-primary的general审查不能自动覆盖本多primary族。同一个合并文件SHA并不合并各审查者的数学身份；本批清洗者已读整个canonical，也不自称又做盲审。

# 处置与后续用途

五源全部 `integrated` 到已有simplex主干、本页证明接口和精确原字节。没有把五份材料计成五个新定理；没有复制已充分陈述的主V/OPT反例。数学比较未发现新fatal，当前canonical已吸收原证明与明确scope，原件总66797字节保留。

关系判断是：trace/projective/common code给全pair边际与正点可达；资源占位及finder联合给V，全部原jobs上下界给实际OPT；block常量排除与fresh completion给CSP值；删除和unpadding为各自明确对象上的保值/反例边界；min-distance观察阻断宽矩形假设的迁移。Exact/独立/读后/scope另是来源与内部复核证据，不作新数学前提。本次未改其他正文或阶段三图。

本五源及当前canonical没有软件实现/有限运行交付，本轮未新增数学扫描。C与arity q随R变化且q约R³，不是先前固定arity、R相对arity充分大的既核LST参数域；没有Chan/LST困难像声明、任意源NO decoder、NP-hard promise、删除稳健困难性、一般UM算法或近二计算困难性。单边际族、one-primary正面接口和本多primary PI族应分别接续，不能用其中一个的证据替另一个闭合义务；六人共同目录纯SPE也不由此解决。
