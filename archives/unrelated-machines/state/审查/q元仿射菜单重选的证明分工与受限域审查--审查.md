---
id: "unrelated-machines/qary-affine-recoupling-proof-and-domain-review"
kind: "review"
type_tag: "审查"
title: "q元仿射菜单重选的证明分工与受限域审查"
status: "six-historical-sources-integrated"
truth_status: "exact-values-in-stated-selector-domains; no-general-nonlinear-or-hardness-claim"
review_level: "six-full-source-reads; existing-proofs-and-later-scope-compared"
summary: "将q元循环/全部仿射/逐坐标三域精确值的原陈述、两种整数达界证明和分阶段审查接回既有正文；保留固定A的完整Hall公式、二元特例、实验归属及选择域非空修复。"
legacy_ids:
  - "UM-QARY-AFFINE-MENU-RECOUPLING-CONSISTENCY-v1"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/qary_affine_menu_recoupling_consistency_exact_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/qary_affine_menu_recoupling_consistency_proof_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/qary_affine_menu_recoupling_consistency_v1_independent_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/qary_affine_menu_recoupling_consistency_v1_proof_read_after.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/qary_affine_menu_recoupling_consistency_v1_canonical_scope_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/qary_affine_menu_recoupling_consistency_v1_canonical_final_scope_note.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/cartesian_menu_block_coherence_rank_and_deficit.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/qary_affine_menu_recoupling_consistency_review.md"
---

# 数学身份与已有吸收

六份历史文件属于同一Claim，其三域公式、固定A的秩公式和普通UM桥已由当前canonical `ea09d8d6b48b2a06d18f` 整理在[笛卡尔分块一致性与二度菜单联合取整双源审查](笛卡尔分块一致性与二度菜单联合取整双源审查--审查.md)一、1–3节。本页不再建立重复主定理；接回原始完整证明、独立稿的额外接口、作者读后与最终限定认证，并保留实际有限检查的执行归属。原六文件共40040字节，全部按冻结原字节保存；ID、大小、SHA及两个内容相同的冻结提交见[manifest](../../tools/evidence/qary-recoupling-history/manifest.json)。

本轮六源全部全文读取；另实际读汇总review `c5bceece4104f6baf428`、当前已修正双源审查相关段、[二元逐坐标配额定理](../定理/逐坐标一致菜单的整数资源配额--定理.md)和[裸菜单与配额的分域审查](裸菜单与逐坐标配额的分域审查--审查.md)。最终组合canonical已在本会话前批全文读取，本批复核其SHA仍为 `11dbb5c50317fada96a89d8cedd7ca1cdeeb13b8e5acc5f51c158902bf129e4f`，并按本Claim的章节比较。后续near-full v1/v2原证明也已在前批全读；这里仅比较它们如何推进无约束域，不把其认证移给本Claim审查者。

# 完整菜单与三种选择域

给定素数幂 $q\ge2$、其标准有限域 $\mathbb F_q$ 的显式表示及整数 $t\ge1$，令 $N=q^t$。组 $g$ 和每组的全部indexed states $\ell$ 遍历 $\mathbb F_q^t$；真实资源为 $(a,b)\in\mathbb F_q^t\times\mathbb F_q^t$。状态支持

\[
S_{g,\ell}=\{(a,b):b_i+g_i a_i=\ell_i\ \forall i\}
\]

恰有N项，每项private权为普通有理数 $1/N$。域运算不能与有理处理时间混淆，素数幂域也不自动是整数模q环。对选态函数 $\ell(g)$，可自由取跨组两两不交的 $B_g\subseteq S_{g,\ell(g)}$，允许资源不用，不要求 $B_g$ 为product。记最大共同整数配额为 $k(\ell)$、$V(\ell)=k(\ell)/N$。

| 选择域 | 对全部组同时施加的条件 | 本Claim精确值 |
| --- | --- | --- |
| cyclic | 固定 $\ell_i(g)=g_{i+1}$，下标循环 | $V_{\rm cyc}=1-\lceil(q-1)^t/q\rceil/q^t$。 |
| 全部affine | 优化所有 $\ell(g)=Ag+c$，无A的形状、秩或可对角化前提 | $V_{\rm aff}=V_{\rm cyc}$。 |
| coordinatewise | 优化所有 $\ell_i(g)=f_i(g_i)$，各 $f_i:\mathbb F_q\to\mathbb F_q$ 可非线性，但不能读取其它组坐标 | $V_{\rm sep}=\lfloor(q-1+1/q)^t\rfloor/q^t$。 |

这里的coordinatewise值是**优化整个函数族**的值；一般 $q>2$ 时并不声明每份固定非线性 $f_i$ 都同值。二元定理则对每个固定f给同一配额，因其所有两点函数均可由全局资源平移化为零标签。两域量词必须分开。取整作用于整个普通有理数幂，不能改成逐坐标先取整再相乘。

# 原证明与独立重构的实质分工

## 固定A的精确Hall公式

独立稿不是只确认三域的最后数值。它先对每个固定 $\ell(g)=Ag+c$ 定义

\[
\nu_a=\dim\ker(A-\operatorname{diag}(a)),\qquad
\Lambda(A)=\sum_{a\in\mathbb F_q^t}q^{-\nu_a},
\quad k(A,c)=\lfloor\Lambda(A)\rfloor.
\tag{1}
\]

最后一式是精确值且与c无关：对任意组集合F，每个a层的邻域为 $(A-\operatorname{diag}(a))F+c$，每个fiber大小至多 $q^{\nu_a}$，所以

\[
|N(F)|\ge\Lambda(A)|F|.
\]

这给每组 $\lfloor\Lambda\rfloor$ 的全部Hall子集条件及整数流。全体N组的union恰为 $N\Lambda(A)$，反给同一整数上界。不能只看全体组总资源就断言匹配充分；本证明先核所有F才得达到。

独立稿还明确：所有整数目标 $0\le h_g\le\lfloor\Lambda\rfloor$ 可从均匀达界分配删减得到，但没有把全union计数当成任意更大非均匀目标的充分判据。较大目标仍需完整Hall条件。这一可复用边界在旧摘要只列均匀最优时未展开，原稿与本页共同保留。

## 全部affine上界与cyclic奇异层

作者与独立稿都证明multiaffine网格事实：非零且逐变量次数至多1的r元多项式在 $\mathbb F_q^r$ 至少有 $(q-1)^r$ 个非零点。归纳写成末变量乘系数加常项；系数为零与非零分别处理。应用于 $\det(A-\operatorname{diag}(a))$ 的末变量系数，它的最高全乘积项系数为非零的正负1，至少有 $L=(q-1)^{t-1}$ 个前缀使其非零。每个这样的前缀有唯一末坐标令det为0，因而至少L个奇异层，每层在 $N-\Lambda$ 中损失至少 $1-1/q$：

\[
N-\Lambda(A)\ge L(1-1/q)=\frac{(q-1)^t}{q}.
\tag{2}
\]

cyclic核递推严格由原方程得到 $\delta_{i+1}=a_i\delta_i$；奇异恰当且仅当 $\prod_i a_i=1$，此时核维数恰1。这个事实对任意域特征成立，不需要特征不整除t，也不需要循环矩阵可对角化。若另写加号矩阵，须先作 $a\mapsto-a$ 换元，不能混用乘积条件。

cyclic恰有L个奇异a，所有好层每组各给一枚独占资源，共 $N-L$ 项。坏层真实图左度L、右度q，所有左子集邻域至少 $L|F|/q$，整数b-matching每组再给 $\lfloor L/q\rfloor$ 项，最终配额

\[
N-L+\lfloor L/q\rfloor=N-\lceil(q-1)^t/q\rceil.
\]

必须共同使用奇异层资源；完全丢掉奇异层只给较弱下界。t=1时空minor为1、循环矩阵为[1]、L=1，所有公式仍有效。上述内容已吸收到既有正文一、3；原始两份证明保留精确符号与边界。

## Coordinatewise达界的两种一致证明

任意固定f的第i维有q条不同斜率线；第一条有q点，每条后续线至少与第一条交一点，union至多 $q^2-q+1$。全部组遍历完整tuple，故selected-state union精确等于各维union的product，至多 $(q^2-q+1)^t$。任意全局partial若每组取m项便需Nm个不同资源，给

\[
m\le\lfloor(q-1+1/q)^t\rfloor.
\]

此处没有限制领取集合形状。两个原证明对达到给出不同而相容的接口：

| 证明来源 | 达到同一整数配额的真实步骤 |
| --- | --- |
| 作者Proof第4节 | 取所有 $f_i=0$，每维q条线concurrent，独占点分数1、共点分数 $1/q$。tensor的是**分数边量**，每组总量 $\alpha^t$、每资源容量至多1，其中 $\alpha=q-1+1/q$。缩放到整数需求 $\lfloor\alpha^t\rfloor$ 后，普通整数maxflow恢复真实全局不交子集。 |
| 独立稿第1、4节 | 同取 $A=0,c=0$，$\nu_a$ 为a的零坐标数，故 $\Lambda(0)=(q-1+1/q)^t$，直接用式(1)的所有Hall子集与整数流得到floor。 |

因此作者的tensor证书不是最终bundle的product约束，也不是允许拆分资源的执行；独立稿的统一秩公式也不是用总union直接推整数可行。这两种证明分工和独立中间公式由本页保留，已有主干第2–3节承接其数值与算法结论。

# 完整普通UM、事后修复与后续域边界

完整普通P为每state一private、每真实资源一resource、每组一件selector1；每incidence独立原job仅在自身private用 $1/N$ 或对应resource用1，其余无穷，全部未选状态jobs仍存在。给不交B，只外送所选状态中B对应jobs，其余全部停车，负载为：selected $2-|B_g|/N$、unselected 1、resource至多1。

反向任意完整峰 $C<2$ 时，按每个selector真实目的地取所选状态真实exports。资源unit容量使这些B不交，即使未选状态另有exports也不解除约束。selected private精确负载为 $1+(N-|B_g|)/N$，$C\ge2$ 时下界平凡。因此每个**非空**选态域 $\mathcal L$ 的受限实际最优恰

\[
C_{\mathcal L}=2-V_{\mathcal L}.
\tag{3}
\]

普通P自身没有跨组强制affine或coordinatewise的资格；尤其 $C_{\rm sep}$ 不能用作普通无约束OPT的下界。所有原jobs各执行一次，不以所选子实例替代全部矩阵。

固定q时

\[
V_{\rm cyc}\longrightarrow1,\qquad
0\le V_{\rm sep}\le(1-1/q+1/q^2)^t\longrightarrow0.
\]

于是任意常数c>0，充分大t的cyclic达界输入都没有同菜单的coordinatewise输出能保留c倍最小质量。这是在存在性层面否定特定事后修复合同，不依赖算法效率；它不否定改变资源/任务/模型、其它一致性、直接处理nonlinear重选或仅处理额外physical结构的compiler image。

独立稿另给q=2任意nonlinear域的自足上界：取补组 $g,g+\mathbf1$，其所选支持任意标签下必交一点，所以不能每组全取N项；整数配额至多N−1，cyclic达到。t=1时三个域均值 $(q-1)/q$，q=2,t=1为1/2、实际3/2。不能将一般q>2的determinant证明搬给任意nonlinear函数。

历史Exact和本六源审查都说一般q>2无约束最优未由本Claim证明。这不与后来near-full新证明冲突：最终canonical第7–8节另用并发投影/H/K必要界关闭 $q=3,t=2$ 的7/9及 $q=3,t=3$ 的8/9全域端点，范围及完整actual见[near-full版本审查](任意非线性仿射菜单缺项的版本推进与审查边界--审查.md)。这些新证明不是本recoupling审查者对context的默认认证，也未证明所有q,t的cyclic全域最优。

# 原件、审查顺序及非空域修订

| 完整读取的来源 | 独有内容及去向 |
| --- | --- |
| `012990e36aa61607d60d`，[Exact](../../tools/evidence/qary-recoupling-history/original/qary_affine_menu_recoupling_consistency_exact_v1.md) | 第1–4节冻结三域量词、自由partial、精确floor/ceil、完整actual、修复不可能的准确否定范围及显式编码。其陈述已被旧正文吸收，本页保留原始未附Proof身份和域差异。 |
| `88b461d9d2572eb0860b`，[作者Proof](../../tools/evidence/qary-recoupling-history/original/qary_affine_menu_recoupling_consistency_proof_v1.md) | 第1–6节给全affine union/det上界、cyclic坏层b-matching、任意f上界、分数tensor后整数flow达到、全jobs双向桥与极限。两种达界证明的作者分支由本页明确保留。 |
| `4352f1423f2ac4ce5c0e`，[独立重构](../../tools/evidence/qary-recoupling-history/original/qary_affine_menu_recoupling_consistency_v1_independent_review.md) | 第1–9节另增固定A精确floorΛ、c不变性、非均匀目标 caveat、q2全nonlinear证明、任意特征/t1、显式图大小与有限检查自述。这些不因主值相同而被当成无增量。 |
| `002e1bbca5b80bd51a69`，[作者读后](../../tools/evidence/qary-recoupling-history/original/qary_affine_menu_recoupling_consistency_v1_proof_read_after.md) | 首次实读作者Proof后逐节比较其tensor-flow与先行rank/Hall证明，核符号、奇异层、全jobs和实验执行归属，并说明真实source编译仍需物理一致性。本页分开保留“先行重构”与“作者稿读后”。 |
| `a915728913f18cae2af5`，[首次canonical scope](../../tools/evidence/qary-recoupling-history/original/qary_affine_menu_recoupling_consistency_v1_canonical_scope_review.md) | 全文读16914字节b859版本，但正式认证仅第1–4节及第9节对应qary内容；第5–8节仅context。核定理式、算法、实验归属和OPEN边界，旧审查保持其历史版本。 |
| `8f8e6c3965904ba31a39`，[final scope](../../tools/evidence/qary-recoupling-history/original/qary_affine_menu_recoupling_consistency_v1_canonical_final_scope_note.md) | 另读16920字节11db final，确认唯一非空域修订和逆hash，正式范围不扩张。本页接回当前最终源，不以旧hash预认证后来改动。 |

路由按冻结文件自述为：原独立审查者只读Exact重构，后才实际读作者Proof并另冻；再全文读组合canonical但只认证本Claim对应章节，最后另冻final scope。当前汇总review称该审查者bicriteria，文件hash链相符；这些路由不是本次新组织的盲审，也不当外部时间戳认证。

最终canonical的“对任意选择域”只加“非空”，两字为6个UTF-8字节，从16914到16920。当前final SHA为 `11dbb5c50317fada96a89d8cedd7ca1cdeeb13b8e5acc5f51c158902bf129e4f`；将唯一新短语逆替换后准确恢复 `b859a872faf453265f3a4d0b99439df104ae7fac4af1dca92ca969e39f6e8b30`，见[核对记录](../../tools/evidence/qary-recoupling-history/canonical-nonempty-replacement-check.json)。本会话已实际验证此逆替换，本批针对同一最终源复核；没有把生成的逆替换字节冒称另行取回的旧canonical原件。

所有具体三域从来非空，所以修复使通用最大值/受限最优表述有定义而未改变三公式。near-full和binary-block审查各有自己的认证范围，不能因为它们在同一文件就合并成一次全篇数学认证。

# 有限检查归属、显式复杂度与关系判断

独立稿第9节报告的有限辅助检查保留如下，不能抹成“从未做实验”，也不能记为本轮或root执行：

| 原审查者自述检查 | 参数及结果范围 | 当前证据强度 |
| --- | --- | --- |
| 1504个矩阵、24664次rank | 枚举全部A的参数为(2,1),(2,2),(2,3),(3,1),(3,2),(4,1),(4,2),(5,1),(5,2)；GF4用 $x^2+x+1$。记录称所有A满足奇异数/Λ上界，域最大整数配额吻合cyclic。 | 六源提供文字记录和证明，没有随附这些计算的程序/完整日志；本批不认证逐项执行输出，也未复跑。 |
| 3412个一维函数 | q=2,3,4,5的全部函数，记录称union均至多 $q^2-q+1$ 且最大值达到。 | 仅归该reviewer的有限辅助证据，不是所有q,t的证明前提、作者运行或root亲自核验。 |

一般结论依赖有限域线性代数、multiaffine计数与全部Hall子集的自足证明。作者读后及两个canonical范围记录明确重申这些执行归属；没有软件实现、外审或全球新颖性认证。

完整规模是N组、$N^2$ private、$N^2$ resources、$N^3+N$ jobs、$2N^3+N^2$有限条目、dense $2N^2(N^3+N)$；标签和 $1/N$ 有理时间位长 $O(t\log q)$。达界不枚举全部 $q^{t^2}$ 个A或所有函数，直接取cyclic或f=0；所选状态图N组、至多 $N^2$ 资源、$N^2$ 邻边，整数容量流完成后输出全部 $N^3+N$ 原任务。给定A的式(1)只需N个对角扰动rank。复杂度按完整展开输入计，不是 $\operatorname{poly}(t,\log q)$ 输出指数对象。

六源均以 `integrated` 处置：已存在主定理不再新建，原证明/独立中间接口/审查范围与实验归属在本页及原字节中有明确去向。本批没有新增数值扫描。关系判断是：固定A公式支撑affine与f=0达界；全affine上界和cyclic见证共同给精确三域值；两条渐近比较共同否定限定事后repair。来源、作者读后、scope支持另作证据关系，不当数学前提。与二元固定f定理是特化/量词比较，与near-full新证明是后续无约束推进，不能混域。本次未改阶段三图或其他已交付正文。

尚未实现的义务仍是普通矩阵内真实的选择一致性和任意低峰调度解码，或另找可用困难性源。这里无一般UM近二算法/困难性、无免费coherence，也没有与六人共同目录纯SPE半覆盖的推导关系。
