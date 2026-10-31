---
id: "unrelated-machines/affine-line-global-dummy-proof-and-version-review-lineage"
kind: "review"
type_tag: "审查"
title: "仿射线全局dummy的证明与版本审查链"
status: "historical-proof-and-review-evidence-integrated"
truth_status: "scoped-proof-rechecked; no-general-source-bridge-impossibility"
review_level: "full-six-source-read; canonical-and-related-objects-compared"
summary: "保留逐tuple分组、d=n-q枚共享dummy编译的完整半保留证明、unit双向提取、精确位长及独立输入与最终字节修正链；主数学身份接回已有双源审查。"
legacy_ids:
  - "UM-AFFINE-LINE-TUPLE-GROUP-GLOBAL-DUMMY-ESCAPE-v1"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/affine_line_tuple_groups_global_dummy_statement_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/affine_line_tuple_groups_global_dummy_proof_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/affine_line_tuple_groups_global_dummy_rank_exact_first_review_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/affine_line_tuple_groups_global_dummy_rank_author_read_after_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/affine_line_tuple_groups_global_dummy_final_canonical_scope_review_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/affine_line_tuple_groups_global_dummy_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/affine_line_tuple_groups_global_dummy_compilation_escape.md"
---

# 数学身份与本页增量

六份来源均已全文实读。其主数学身份已经由当前源 `b055f6c18bcbb55590a2` 整理进[仿射线全局dummy与任意汇点价格覆盖双源审查](仿射线全局dummy与任意汇点价格覆盖双源审查--审查.md)的第一部分。本页不是第二个半保留定理，而是该对象的证明和版本审查资源：保留精确规模、slot-Hall细节、先行独立输入与作者读后的区别，以及最终canonical字节的唯一排版修正。下文自足列出被核对的合同，避免仅凭“旧稿已吸收”丢失原论证。

六份原字节以及本次全文比较的canonical、旧constraint-as-group正文见[证据清单](../../tools/evidence/global-dummy-proof-history/manifest.json)。两份冻结提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 所列版本内容相同；本页source_refs取前者，manifest保留两条定位。下述“先读/后读”是冻结记录自述的审查路由，不把文件哈希当成独立时间戳证明。本次清洗者已读全部材料，所作比较也不冒称新的盲审。

# 完整合同及其证明

取素数 $R\ge2$、整数 $k\ge1$、有限变量集 $X$ 与indexed relations $G$。每个 $g$ 涉及 $k$ 个不同变量 $X_g$，每变量的relation-degree至多 $R$，并给注入 $j_x:G(x)\hookrightarrow\mathbb F_R$。显式允许表 $A_g\subseteq\mathbb F_R^{X_g}$ 可空。令

\[
n=\sum_g|A_g|,\quad m_0=|\{g:A_g\ne\varnothing\}|,\quad
1\le q\le m_0,\quad d=n-q,\quad D=kR.
\]

每个allowed indexed tuple $e=(g,s)$ 是不同group，原state的支持为

\[
S_e=\biguplus_{x\in X_g}\{(x,z,s(x)z+j_x(g)):z\in\mathbb F_R\}.
\]

资源有变量tag，故 $|S_e|=D$。另添与原资源 $U=\biguplus_x\{x\}\times\mathbb F_R^2$ 不交的 $d$ 枚global dummy $\delta_1,\ldots,\delta_d$；**同一dummy资源由全部groups共享**。每group的menu有一个原state $S_e$ 和每枚dummy的singleton state。每个indexed state各有独立private机；每资源各有资源机。每group有一件selector，时间1且只能去自己menu的private。每state-resource incidence是一件不同原job，只能在其private用 $1/D$（原state）或1（dummy state），或在对应资源机用1，其余资格为无穷。全部未选state的jobs仍存在，无预载或额外守卫。每state总private质量1，域内 $n\ge1$，每件job都有有限端。$d=0$ 时不生成任何dummy资源、state或job。

对**每份**上述显式输入，不给源赋值、OPT或full-set packing见证，可确定性按完整输入/输出总位长多项式构造全部原jobs的同一实际分配，使

\[
C_{\max}\le2-\frac{\lceil kR/2\rceil}{kR}\le\frac32.
\tag{1}
\]

同时，完整实际峰值不超过1当且仅当原indexed full sets存在大小至少 $q$ 的两两不交packing。后者是unit可行性的等价，不表示式(1)的算法会找到unit调度。

## 不求源解的选择与所有Hall子族

按输入顺序选 $q$ 个不同非空relations，各取表内第一tuple，得到 $q$ 个原groups $F_0$。其余恰 $d$ 个groups与 $d$ 枚dummy作确定性双射。只对 $F_0$ 中的原states寻求部分导出；不在全部 $n$ 个tuple groups上套relation-degree界。

固定任意 $F\subseteq F_0$，对变量 $x$ 记其出现次数为 $r_x\le R$。由于每relation只选一个tuple，$j_x(g)$ 在这些lines间各异。同slope线平行不交，异slope线在素域恰交一点，因此两条线不重合且交点至多1。二阶容斥给

\[
\left|\bigcup\text{所选 }x\text{-lines}\right|
\ge r_xR-\binom{r_x}{2}
\ge\frac{R+1}{2}r_x.
\]

变量tag分离且 $\sum_xr_x=k|F|$，故对**每个**Hall子族都有

\[
|N(F)|\ge\frac{k(R+1)}2|F|
\ge b|F|,\qquad b=\lceil kR/2\rceil.
\tag{2}
\]

最后一步也含 $kR$ 奇数，因为 $\lceil kR/2\rceil\le kR/2+1/2\le k(R+1)/2$；空 $F$ 与 $r_x=0$ 自动成立。把每group复制成 $b$ 个同邻接slots，任意slot子集涉及某族 $F$，其大小至多 $b|F|$，邻域就是 $N(F)$，所以式(2)给普通Hall条件。整数matching或容量flow为每group构造恰 $b$ 枚真实资源 $B_e\subseteq S_e$，所有 $B_e$ 两两不交。算法不枚举Hall子族，$B_e$ 也无须由整条line组成。

## 全部原jobs的一次共同分配

选中原group的selector去原state private，只把 $B_e$ 对应的 $b$ 件incidences外送；选dummy的group把selector放对应singleton private，并外送它的唯一incidence。**其余全部incidences均留各自private**，包括选原group的所有dummy states、选dummy group的原state及其它dummy states。

选中原private负载为 $1+(D-b)/D=2-b/D$；选中dummy private只有selector1；未选private的总incidence质量是1。原资源因matching至多一件unit，dummy资源因双射至多一件unit。所有原jobs恰执行一次、只用原有限端，所有机器在同一分配中同时受控，得到式(1)。该证明的“完整”取决于回填全部未选states，而不是只给selected子实例的局部负载。

## Unit双向：覆盖任意实际调度

若有 $q$ 个不交原full sets，选择其原states，其余groups与dummy双射；把selected states的全部incidences外送、其余states全留private。原full sets不交，dummy各用一次且与 $U$ 分离，所以资源机负载至多1；selected private只有selector1，未选private质量1，得完整unit分配。

反向取任意完整峰值不超过1的实际调度。每selector在某个state private占时间1，该selected state每件incidence的private时间严格正，因此它的全部incidences必须外送。资源端时间为1，所有selected states所领资源必须全局不交；选择dummy的groups至多 $d$ 个，所以至少 $n-d=q$ 个groups选择原state，其完整 $S_e$ 两两不交。未选state可能另有外送，只会占用更多资源，不破坏提取。因此不必先把任意unit调度正规化。selector还给 $\mathrm{OPT}\ge1$。这一等价保留strict端的packing阈值，却不为weak partial端提供困难性soundness。

## 边界、精确规模与位长

$q=n$ 时，由 $q\le m_0\le n$ 得 $m_0=n$，每个非空relation恰一tuple，$d=0$，全部groups选原state；Hall、回填及unit提取都无需dummy且无除零。空relations不生成groups，也不改原注入。$m_0$ 仅用于本合同的域及选择数量，不能把源value的分母从 $|G|$ 改成 $m_0$，不能把near-perfect YES免费强化成perfect YES。$m_0=0$ 或 $q>m_0$ 在域外，需要覆盖它们的完整归约须另证合法分支。

写 $v=|X|$，完整矩阵规模为：

| 对象 | 精确数量 | 原因 |
| --- | --- | --- |
| private机器 | $n(d+1)$ | 每group一个原state及 $d$ 个dummy states |
| resource机器 | $vR^2+d$ | tagged原资源加共享dummy |
| 原jobs | $n(D+d+1)$ | $n(D+d)$ 件incidences与 $n$ 件selectors |
| finite条目 | $n(2D+3d+1)$ | $2n(D+d)$ 个incidence端及 $n(d+1)$ 个selector端 |
| dense条目 | $[n(d+1)+vR^2+d]\,n(D+d+1)$ | 全机器数乘全部job数 |

原时间 $1/D$ 的位长是 $O(\log D)$，其余有限时间为1。选表首项、枚举lines、至多 $qD$ 条selected支持边的flow、$qb\le qD\le nD$ 个slots、dummy双射及全部job输出均对完整显式总编码长多项式；不按更大隐藏分母复制对象。任意二进制 $R$ 的 $vR^2$ 资源和 $nD$ incidences展开必须收费，不承诺succinct的 $\mathrm{poly}(\log R)$。固定source的 $k,R$ 时才直接成为原source输入上的多项式编译。

# 六源各自贡献及输入顺序

以下来源都不是六个新数学结果。作者Proof和独立重构给同一完整证明；其余材料固定精确量词与审核对象。原件路径和完整哈希均在manifest中。

| 来源及证据角色 | 独有内容与去向 | 必须保留的界限 |
| --- | --- | --- |
| statement `199e244b6a608b893d14`，[原字节](../../tools/evidence/global-dummy-proof-history/original/affine_line_tuple_groups_global_dummy_statement_v1.md) | 冻结完整ordinary UM、两个Exact结论、counts与显式位长；数学合同在既有双源审查第一部分，本页补齐slot-Hall及精确规模。 | 它自述正式文件在先行独立记录后才冻结，不能倒称reviewer先读此文件；本statement不附证明策略。 |
| 作者Proof `f50994241118db0fad7b`，[原字节](../../tools/evidence/global-dummy-proof-history/original/affine_line_tuple_groups_global_dummy_proof_v1.md) | 给不同relation选择、所有子族容斥、容量Hall、全任务回填、任意unit提取、边界及counts；上文逐项自足重述并与canonical核对。 | 不求source/OPT/packing见证；不把给定 $q$ 的packing困难性当成近二NO。 |
| Exact-first `7063b9c26d336e4df22f`，[原字节](../../tools/evidence/global-dummy-proof-history/original/affine_line_tuple_groups_global_dummy_rank_exact_first_review_v1.md) | rank报告只据root的完整消息Exact和旧current第1–27行source定义，未读该页后续Hall或新作者Proof，独立重构完整矩阵、slot-Hall、actual与unit双向；特别点明不对全部tuple groups误用degree。 | 正式statement当时尚未创建。它是“消息陈述先行的独立重构”，不是“正式文件先行审查”；冻结自述不等于独立时间戳。 |
| 作者读后 `6b6f07d801c08d64495d`，[原字节](../../tools/evidence/global-dummy-proof-history/original/affine_line_tuple_groups_global_dummy_rank_author_read_after_v1.md) | rank在独立稿冻结、root实际读后才全文读正式statement与作者Proof，逐项核对域、所有Hall子族、全部jobs、任意unit调度、边界与counts，并核原独立稿hash不变。 | 这是同一人的作者读后核对，不是第二份独立盲重构；不能改写原先读取范围。 |
| 最终scope `06a57d5a9ed4705ed7c9`，[原字节](../../tools/evidence/global-dummy-proof-history/original/affine_line_tuple_groups_global_dummy_final_canonical_scope_review_v1.md) | 全文读canonical初稿与修正后字节，发现并跟踪dense式逗号排版错误；最终认证绑定 $\texttt{edc0c843…c2c65}$，覆盖全部第1–5节。完整数学核查与上文一致。 | 认证不扩大到任意dummy数量、任意权、不同阈值或真正guard；scope文件没有新增软件/有限实验。 |
| 短review `edae0497c74a32c31e48`，[原字节](../../tools/evidence/global-dummy-proof-history/original/affine_line_tuple_groups_global_dummy_review.md) | 把前五件原字节、root实际亲核、先行与读后顺序以及最终canonical范围汇成正式入口；五个完整SHA与本次导出一致。 | 它是审查入口，不是另一个外审、独立实现或全球新颖性认证。 |

源记录的实际先后关系是：root先发消息Exact；rank仅读消息和旧source定义作先行重构；root实际读该记录后建立正式statement及作者Proof；rank再全文读后二者并另冻读后；最后rank全文读取canonical并跟踪排版修正，短review汇总。没有把当时未存在的正式文件倒填为先行输入。作者Proof、独立重构与canonical在上面列明的所有承重数学步骤相合；本次未见改变此限定结论的后续数学纠错。

# 最终字节修正：只恢复历史，不改原件

最终scope报告，canonical初稿wholeSHA为

`22c9377c33b1167827d3d89636d91820de94808fe9ded724273f6768bb162f36`。

初稿dense公式把机器数与jobs数之间误写为逗号。root改为显式乘号后，最终wholeSHA为

`edc0c8437260085bfcb408099f724306531a88b360d27811b0a8e70762fc2c65`。

本次实际全文读取的canonical就是后一SHA，并在内存把唯一的

`[n(d+1)+vR^2+d]\cdot n(D+d+1).`

逆替换为

`[n(d+1)+vR^2+d],n(D+d+1).`

重算后精确恢复前一SHA。该检查支持“两个版本只相差这一处排版字节”，而不是数学定理变更；没有重写旧canonical或其它原件。复算方法及实际结果见[完整性检查脚本](../../tools/evidence/global-dummy-proof-history/verify_integrity.py)与[输出](../../tools/evidence/global-dummy-proof-history/integrity-check.json)。这只是源字节和单处修正的复核，不是新调度软件、flow实现、优化枚举或独立数学实验。

# 与先有对象的比较、否定范围与接续

本次已全文比较旧 `5181ee7a09c56933cfcd` [constraint-as-group正文](../../tools/evidence/global-dummy-proof-history/comparisons/line_set_packing_and_take_continue_compilation_obstructions.md)、当前 [canonical](../../tools/evidence/global-dummy-proof-history/comparisons/affine_line_tuple_groups_global_dummy_compilation_escape.md)、既有[直线集合打包与统一端口停车审查](直线集合打包与统一端口停车双源审查--审查.md)及[任意状态权仿射并行线审查链](任意状态权仿射并行线的证明与审查链--审查.md)。旧constraint-as-group合同对每relation一个group、非空任意表、均匀权及**任意完整local state选择**给半保留；它明确没处理tuple另成groups的compiler，因为全部tuple groups不再自动满足原relation-degree或line不重合。这里用恰 $d=n-q$ 枚global dummy，只让 $q\le m_0$ 个不同relations采用原state，重新恢复用于partial matching的真实不变量，因而是另一个被精确关闭的合同，与旧稿当时的未排范围无矛盾。

任意状态权的完整并行sum关系则依赖全tuple菜单及 $k\ge2$，寻找某个affine state选择并处理state-dependent权；这里是任意关系、均匀权、$k\ge1$，用dummy计数选择不同relations。不能把那一对象的任意权结论迁移到此处，也不能把此处结论改成对全部tuple groups的任意state选择成立。

本结论精确排除：保留上述关系与资源、uniform private权、$d=n-q$ 枚共享dummy及 $1\le q\le m_0$ 这一完整编译时，试图靠该桥强制接近2的NO峰值。它不排除其它grouping、资源权、任务、阈值、dummy数量、实际shared guard或其它source-to-UM桥。unit等价没有证明原full-set packing容易；外部整set困难性也没有提供这里缺失的partial-set soundness。本页只使用自足几何合同，没有重新认证外部论文完整困难性证明或全球新颖性。

关系判断是：六件历史资源分别给已有双源审查第一部分提供精确陈述、作者证明、独立重构、读后与最终范围证据；旧constraint-as-group对象提供几何方法背景及不同的已排范围。证据支持关系与数学推广关系分开，不能由此连出一般UM算法、一般归约不可能或六人SPE边。此次第二阶段登记这一判断，未重建第三阶段图。

六源均作为 `integrated` 处理：完整证明和独有版本链都有正式去向，原字节完整保留。源材料无软件实现、有限优化实验或外部同行评审，本次亦未把字节检查升级为这些证据。标准容斥、Hall与flat回填不是新matching理论，`UM-TARGET-v1`及六人共同目录纯SPE半覆盖目标均不因本对象而闭合。
