---
id: "unrelated-machines/one-primary-pi-onehot-unit-escape-proof-and-review"
kind: "review"
type_tag: "审查"
title: "单primary条件化的单位逃逸与原态匹配证明"
status: "five-historical-sources-integrated"
truth_status: "scoped-unit-escape-proof-rechecked; no-general-PI-or-UM-conclusion"
review_level: "five-full-source-reads; full-canonical-and-related-objects-compared"
summary: "保留一primary/onehot接口的完整条件化—Hall—全原任务证明，展开不求λ的直接原态图与作者正流支持图的差别，并分开先陈述独审、作者读后和只审canonical§1–2的历史范围。"
legacy_ids:
  - "UM-TAGGED-AFFINE-LINE-ONE-PRIMARY-PI-ONEHOT-HELPER-UNIT-ESCAPE-v1"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/tagged_affine_line_one_primary_pi_onehot_helper_unit_escape_exact_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/tagged_affine_line_one_primary_pi_onehot_helper_unit_escape_proof_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/tagged_affine_line_one_primary_pi_onehot_helper_unit_escape_exact_first_review_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/tagged_affine_line_one_primary_pi_onehot_helper_unit_escape_author_read_after_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/tagged_affine_line_pairwise_independence_boundary_one_primary_canonical_scope_review_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/tagged_affine_line_pairwise_independence_boundary.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/tagged_affine_line_pairwise_independence_boundary_review.md"
---

本页将五份原始陈述、作者证明及分阶段审查接回已经整理的[仿射线单primary与单边际/多primary审查](仿射线单primary与单边际趋二双源审查--审查.md)第2节。这里完整展开单位逃逸证明及直接原态图的算法义务，并保留五源各自的独有证据；不是五个不同定理。旧双源页的单边际来源去向已经纠正，本批不改该页，也不用本五源认证其多primary simplex部分。

五源共53100字节均已全文实读，另全文比较合并canonical、专门review、单边际原正文、任意权并行关系原正文及相应已整理对象。原字节与双冻结提交、blob、SHA见[证据清单](../../tools/evidence/one-primary-unit-history/manifest.json)。本批没有程序、有限运行或参数扫描；结论依靠下面的自足证明。源记录的先陈述审查不转称本次清洗者的新盲审。

## 1. 完整接口：每helper恰一primary，所有原态均onehot

取任意素数 R≥2，在 F_R 运算。有限变量集分为不交的 primary 集 𝒫与 auxiliary 集 𝒜；𝒫非空，𝒜可空或含unused变量。每个变量x有独立tagged完整资源平面

\[
U_x=\{(x,z,y):z,y\in\mathbb F_R\}.
\]

Groups恰是唯一main M及有限helper集H（可空）。Main参加全部𝒫，不参加𝒜。每helper h的变量恰为 X_h={u(h)}∪A_h，其中唯一primary u(h)∈𝒫、A_h⊆𝒜可空且无重复；没有其它primary或额外groups。不同primary blocks的helpers可任意共享auxiliary。

每incidence(g,x)给固定截距 j_x(g)∈F_R，同一变量的不同groups截距互异。因此primary最多有R−1个helpers加main，auxiliary最多R个helpers；main截距不必0，算法不改编号。

每group给非空显式indexed-state表 S_g。原state s给每参加变量一个slope a_{g,s}(x)，完整支持是

\[
T_{g,s}=\bigsqcup_{x\in X_g}\{(x,z,a_{g,s}(x)z+j_x(g)):z\in\mathbb F_R\}.
\]

每个完整state-resource incidence给非负二进制有理私权 p_{g,s,r}，逐state总和恰1。Main权可随完整state任意变化、可有任意多个正点和零点。**每helper的每个原indexed state恰有一个权1正点 e_h(s)，其它完整line点均权0**，包括概率为0的states。正点可依赖完整state、所有labels、截距和全部输入，不预先绑定parking位置。重复label vectors不合并indexed identities。

每helper在原states上给非负有理分布λ_h，和1，可有零概率states，且对所有t,a∈F_R和x∈A_h有

\[
\sum_{s:a_{h,s}(u(h))=t}\lambda_{h,s}=1/R,
\quad
\sum_{s:a_{h,s}(u(h))=t,\ a_{h,s}(x)=a}\lambda_{h,s}=1/R^2.
\tag{1}
\]

只要求primary均匀及其与**每一个**auxiliary分别pairwise均匀；auxiliary间可相关，不要求helper间独立、全局共同分布或源赋值。Main无需局部分布。也可仅承诺(1)有非负实解；第4节给不取出该实解的实际算法。

定义V：每组选一原state，领取其支持的任意资源子集，跨组资源不交，最大化最小所领私权质量。允许partial subsets及闲置，不要求完整几何supports不交。

精确结论量化**每份上述输入、main每一个预先指定的原state s_M**：确定性总位多项式选原helper states，给每helper其唯一正点、给main指定state的全部正点，所有所领正资源互异，每组质量恰1，故V=1。算法不改main labels/weights、不拼造输入表外的状态、不输出共同source-CSP标签解。

## 2. 只条件化一个primary，得逐点容量

固定指定main state，记 t_u=a_{M,s_M}(u)。对helper h只条件化其唯一primary label=t_{u(h)}，定义

\[
\mu_{h,s}=\begin{cases}R\lambda_{h,s},&a_{h,s}(u(h))=t_{u(h)},\\0,&\text{否则}.\end{cases}
\]

条件事件概率1/R，故μ_h和1。由(1)，对每x∈A_h、每a都有

\[
\Pr_{\mu_h}[a_{h,s}(x)=a]
=R\sum_{s:a_{h,s}(u(h))=t_{u(h)},\ a_{h,s}(x)=a}\lambda_{h,s}=1/R.
\tag{2}
\]

这里只固定一坐标；没有推断同时条件化多个primary后仍均匀。令

\[
f_{h,r}=\sum_{s:e_h(s)=r}\mu_{h,s}.
\]

每helper行和1。下面分别证明每原资源列和≤1，而且正流资源避开main全部正点。

**Primary平面。** 与u相关的每helper条件状态都使用斜率t_u、截距j_u(h)的同一条完整线。Main使用同斜率、不同截距j_u(M)；其它相关helpers的截距也互异。这些完整平行线两两不交，所以某primary点最多接一个helper的条件正流，贡献≤1；所有helper primary正点避开main整条线，强于只避开某一parking点。不同primary用不同tags，helper没有第二个primary入口。

**Auxiliary平面、z≠0。** 固定资源(x,z,y)，helper h的线经过它必须有唯一slope a=(y−j_x(h))/z。正点等于该资源的事件包含在线经过事件内；即使e_h(s)任意依赖整state，也由(2)得

\[
f_{h,(x,z,y)}\le1/R.
\]

同x最多R个helpers，列和≤1。不同primary blocks的helpers共享x不影响这个求和。

**Auxiliary平面、z=0。** 此时线经过资源当且仅当 y=j_x(h)，与slope无关，不能声称每helper贡献≤1/R。实际截距注入保证最多一个helper可贡献，其全部质量≤1，故列和仍≤1。Main不参加auxiliary，故这类资源也不与main正点冲突。

三个分支覆盖全部原资源；没有用auxiliary–auxiliary联合独立，也没有把独立选择helper states的随机实现当成满足容量的实际输出。

## 3. Hall给实际原态，不从各坐标拼标签

将helper作为二部图左点、原资源作为右点。作者Proof的图只取 f_{h,r}>0 的边；给定有理λ时可精确计算，并为每边找μ>0且e_h(s)=r的原state。

先陈述独立稿给更直接的图：**对每个原helper state，只要primary label等于所需t，就加 h→e_h(s) 边，储存完整原state作见证**；相同h/resource边可合并，仍保存一个原state index。可包含λ=0的states，无需计算λ或μ。这个图含作者正流图，故数学流f支持其中。对于任意helper子集B，

\[
|B|=\sum_{h\in B,r}f_{h,r}
\le\sum_{r\in N(B)}1=|N(B)|.
\tag{3}
\]

因此Hall条件成立。按固定点/边顺序做增广路匹配，至多|H|次增广可覆盖全部helper：若最大匹配漏左点，交替可达左集合中至少一未匹配点，而所有可达右邻点均已匹配到该左集合，得到|N(B)|<|B|，与(3)矛盾。

每匹配边输出所储存的**整份原indexed state**，包括所有可能相关的auxiliary labels及其onehot点。不是分别选标签后假定这些labels能构成原state。每helper正点由匹配互异，所有图边的正点都避开main正点（primary同斜率不同截距，auxiliary tag absent from main）。把main全部正点和helper匹配点分配出去，每helper质量1，main质量1；state归一化给V≤1，故V=1。

图中使用λ0态合法：它仍是原菜单state，所有态onehot是显式前提；Hall只需证明图拥有一个可行分数支持，并不要求最终匹配每条边都有正λ。被选完整supports可在零权点相交，这些点既未作为正资源领取，也不靠分配它们获取质量。

## 4. 实λ承诺、可选LP及显式位长

仅承诺(1)有非负实解时，上述实μ/f用于存在性证明Hall；实际finder只读原state表、选main label、建全条件态图并做整数匹配，**不需要求λ，也不依赖不可计算实数**。这是独立重构相对作者正流图的明确实现差别，后来的作者读后与canonical已接纳；不改变精确域或结论。

若要先验证/寻找分布接口，可对每helper做显式有理可行性LP：|S_h|个非负λ变量、归一化、R条primary等式及|A_h|R²条pair等式。系数0/1、右侧1、1/R、1/R²；计费按完整states、labels及planes展开。实可行的有理有界多面体有多项式位长基本解：独立0/1子矩阵维数≤|S_h|，右侧共同分母R²，行列式界给分子/分母位长多项式。标准确定性有理LP可找到证书；也可精确核给定有理λ。LP不可行只表示这个额外边际接口失败，**不能据此宣布普通UM无unit调度**。

图边数≤Σ_h|S_h|，相关右点亦不超过该数；扫描完整权表即可找每state唯一正点，合并重复边时保留state见证。原states的标签重复、正点相同、概率零均不改变这个界。匹配和state查表按图规模多项式；field arithmetic按logR位长，R被承诺为素数，证明中非零z可求逆。给定λ时乘R只加O(logR)位长，有限有理和的位长受原编码控制；不复制概率分母或1/λ，不枚举R!。

完整planes、states和line权表必须显式给出或实际展开。这里只保证对这个总编码/输出长度多项式，不声称compact predicates、权oracle或仅二进制R可在poly(logR)时间免费展开R²平面与全部任务。

## 5. 完整ordinary P：所有原任务同时unit，且OPT恰1

每原indexed state一台不同private root，每tagged资源一台resource machine。每group**一枚**selector，在该组每state root的时间均1。每完整state-resource incidence是一枚不同原job，只可在自身private时间p_{g,s,r}或对应resource时间1，其余∞。没有额外machines/jobs、预载、外部锁模式、虚拟容量或免费外送。0私权端仍是有限资格。

给定main状态和匹配得到的原helper状态，实际schedule为：

1. 每group的selector放选中state root。
2. 选中state全部正incidence jobs放各自领取的resource；每个选中零私时job留原private。
3. 每个未选state的**全部**incidence jobs留各自原private，包含概率零states、所有正job及零job。

选中root负载是selector1加零，未选root负载为该完整state原私权总和1；所有导出的正job在resource用时1且目标互异，故resource负载≤1。Unused变量的完整planes仍是原机器，负载0。每原任务执行恰一次、所有原资格合法，得到Cmax=1。至少main selector存在且其全部合法端时间1，所以任意完整调度Cmax≥1，精确OPT(P)=1。这里直接核全部任务，不只援引V与OPT的抽象桥。

写n=1+|H|、S=Σ_g|S_g|、I=RΣ_g|S_g||X_g|，每state每变量的R个横坐标不同、不同变量tag不同，故完整P精确有

\[
N_{\rm machine}=S+(|\mathcal P|+|\mathcal A|)R^2,
\quad N_{\rm job}=n+I,
\quad N_{\rm finite}=S+2I.
\]

S是全部selector有限端数，不是selector任务数；私权0也占一个private有限端。若物化dense矩阵，其项数为前两项乘积。完整输出扫描S+I和planes便可；未选state、零job和unused plane不被静默删去。

H空时匹配空，main全部正点即可；𝒜空时直接靠primary平行线，允许auxiliary unused；R=2、main非零截距、零main权、λ0态及任意整state决定的onehot点均覆盖。𝒫非空及main存在保证下界1，不使用空实例OPT0的错误延伸。

## 6. 全仓比较：单边际、多primary与并行半保留分别接续

| 对象 | 本质前提与结论 | 与本对象的关系 |
| --- | --- | --- |
| 本单primary合同 | 每helper恰一primary、所有态onehot；primary与各auxiliary的条件pair边际；main无aux；V=OPT=1 | 一次条件化保持各auxiliary均匀，逐点容量后Hall。 |
| [单标签边际反例](../反例/单标签均匀边际仿射线菜单的趋零保留--反例.md) | 每组R态、helper仍一primary但aux label与primary恒差常数；V=1/(R−1)，完整OPT=2−1/(R−1) | 标签单边际均匀不满足(1)：两坐标只支持R对而非R²对，故不反驳本定理。原构造与精确值有独立正文，不能错接simplex。 |
| [公共simplex多primary族](公共simplex仿射线菜单的证明接口与审查边界--审查.md) | odd R≥3、每组R⁴态、helper含R+1个primary；所有局部pairs均匀，V=2/(R+1)，OPT=2−2/(R+1) | 同时条件化多个primary不由pairwise推出aux均匀。该族超出本域，one-primary reviewer没有认证其原证明；不由本合同推到“恰两个primary已有同例”。 |
| [任意状态权并行关系半保留](任意状态权仿射并行线的证明与审查链--审查.md) | 完整sum关系、k≥2、R组、任意归一化state权；寻找一个affine-in-group选态，V≥1/2、完整峰≤3/2 | 条件化整个已选state后做损失平均/唯一例外回填；它不需要本onehot/单primary合同，本定理也不覆盖其完整关系域。共同使用有限域和条件化是方法比较，不是推导依赖。 |

本定理另外不覆盖diffuse helper、main接auxiliary、额外非onehot groups、缺pair边际、外部预载或输入改截距；也未声称selected完整supports不交、source CSP满足、Chan/LST hard image、一般identity复制不可能或一般UM算法/困难性。只给单primary、给定物理接口的actual unit escape。条件化、线几何和Hall是标准技术，本批不认领新匹配后端或全球新颖性。

## 7. 五份原件的独有内容、先验与实际审查范围

五源的冻结hash和原字节见[manifest](../../tools/evidence/one-primary-unit-history/manifest.json)；Exact为59e71…、作者Proof为2b4d…、独立重构为f535…、作者读后为30a76…、最终scope为d7bb…。它们在两冻结提交中字节相同，各只计一个源版本。

| 本批全文实读来源 | 数学内容与证据角色 |
| --- | --- |
| `2e109cdd36dcec65d4f6` [statement-only Exact](../../tools/evidence/one-primary-unit-history/original/tagged_affine_line_one_primary_pi_onehot_helper_unit_escape_exact_v1.md) | 首次冻结域、λ有理/实可行两接口、main任意指定state、全部indexed/zero/all-jobs、精确counts和全部排除域。本页第1、4–6节逐项保留；原时点仅scratch且不附作者Proof，root此前看过策略而非blind。 |
| `92a1fcf7e3397136d164` [作者Proof](../../tools/evidence/one-primary-unit-history/original/tagged_affine_line_one_primary_pi_onehot_helper_unit_escape_proof_v1.md) | 第1–7节条件化、primary隔离、aux z≠0与z0两论证、正流图/Hall/整state恢复、全原任务与LP位长；本页第2–5节。其“root报告独立稿完成后才冻结Proof、只交root”是原作者provenance自述，不作为本轮可独立认证的外部时间戳。 |
| `b875db0e37f7a33dfd5e` [Exact-first独立重构](../../tools/evidence/one-primary-unit-history/original/tagged_affine_line_one_primary_pi_onehot_helper_unit_escape_exact_first_review_v1.md) | 第1–10节仅据指定Exact自足构证，未读作者Proof/root推导/他人新rainbow策略；特别新增全条件态图可含λ0状态、无需求λ的real-existence finder、显式增广路证明、精确S+2I有限端和重复态边界。本页第3–5节保这些细节，不能因作者Proof同结论就丢弃。 |
| `6233d7c07a3039428d79` [作者读后](../../tools/evidence/one-primary-unit-history/original/tagged_affine_line_one_primary_pi_onehot_helper_unit_escape_author_read_after_v1.md) | 独立稿冻结且root实读后，才收到许可并全文读作者Proof§1–7；比较正流图与全条件态图两个合法实现，不回填为先行已读作者。明确未读full-PI simplex候选/别的rainbow推导，也不提前认证未来canonical或软件。 |
| `08a640687b72fc7deb78` [最终canonical scope](../../tools/evidence/one-primary-unit-history/original/tagged_affine_line_pairwise_independence_boundary_one_primary_canonical_scope_review_v1.md) | 记录**整个文件hash**0b941…，实际工具只输出shared header及全部§1–2，止于§3之前；其数学认证仅one-primary范围，含§1.3 V/full-P定义。不是全文实际阅读§3–8 simplex，更不是认证另一reviewer的读史。核直接图变体与先前独立稿一致，保原scope而不按wholeSHA扩大。 |

合并canonical确为SHA `0b94156ecd6552e8ab29961ce03a5d21ddfa75cb945ab802da7115bf781970bf`。本批清洗者已全文读其§1–8与专门review，但不改变原scope reviewer只实读header/§1–2的历史事实。专门review分别归属general的一primary链和bicriteria的simplex链；typed合稿者依据所读材料编排，不是第三次独立数学审查。Root先参与策略讨论，后来的亲读/核对不记盲审。

各冻结文件互相引用hash一致，支持这份内部来源链；它不提供独立带时间戳的外部审计、软件运行、同行外审或全球新颖性认证。独立稿/作者读后均没有fatal或requested correction，不等于仅凭投票证明真值；本页重新核对的具体数学义务已在第1–5节展开。

## 8. 处置、自查与关系判断

五源均integrated到本页和原字节。全域、任意main态、实λ承诺的直接算法、z0、概率零态、原indexed身份、所有未选/zero任务、精确counts/位长和历史先验均有明确去向；不以“旧来源”退休，也不重复done当前canonical、专门review或PI五源。

本次自查逐项核：条件事件概率1/R；pair式给每aux条件uniform；primary平行线避main；aux两类横坐标容量；Hall与λ0大图；匹配整state恢复；main归一化与helper一正点给V；选中/未选/private/resource逐机负载；selector下界1；S+2I计数；实λ与显式位长；各reviewer实际先后及partial-read范围。没有新增数学运行；文件指纹、链接与receipt结构检查只作交付核验。

可解释关系为：精确one-primary结构+(1)局部边际→条件化及逐点容量→Hall原态匹配→V1与全部原任务OPT1；直接图是对同一结论的实现规格加强，作者/独立/读后/scope文件是来源及内部复核关系，不是额外数学假设。与单边际、多primary及并行关系的联系仅为第6节分别注明的前提边界/方法比较。阶段二此处完成关系判断，正式三级图仍待第三阶段按这些条件建立；本批不改旧图或其它正文。

仍需另证的是真实hard image、全局source decoder、扩到多primary或diffuse helpers、预载/额外组、一般UM共同容量算法及近二困难性。当前UM-TARGET-v1和六人共同目录纯SPE半覆盖目标均不由本限定接口解决。
