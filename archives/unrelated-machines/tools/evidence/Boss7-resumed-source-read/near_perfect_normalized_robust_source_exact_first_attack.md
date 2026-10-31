# 近完美归一化 robust 源合同：仅 Exact 的独立攻击与三重等号重构

日期：2026-10-18。审者：near_two_reduction（boss11 内部研究 subagent）。本次只实际读取

`/workspace/scratch/038d9dcc4cac/negative_hardness_work/current_hardness_sources/near_perfect_normalized_robust_gap_exact.md`

未读它的作者 Proof，未改该 Exact、任何共同仓库或 git。本人已知并参与上一阶段一般福利 LP 的有理去随机化证明；因此本审查是基于公开共同前提的后续独立重构，**不是 blind 全研究审查**。下述重构先于作者 Proof 读取冻结，不追溯回填独立性。

## 1. 本次实际接受的精确合同

有限非空 n 个 groups，各有非空有限显式 indexed norm1 非负有理 states；distinct 原资源、真实不交 allocation、无额外coherence。参数作为binary输入：0≤η<1，0≤δ<1，0<γ_hi≤1，且

  (5/8)(1−η)≥γ_hi+(1−γ_hi)δ。                                    (E)

YES 是存在一个 allocation 的unit-quality组数至少(1−η)n；NO_≥ 是每个allocation的quality≥δ组数严格少于γ_hi n；另一个NO_>只改高端为>δ。LP用z每组和一、0≤x≤z、资源Σx≤1、目标L=Σp*x，不是positive-support FSLP。判别为L≥(1−η)n时YES，否则NO。

有限U虽未显式要求非空，但norm1非空state已经排除U为空的合法输入，没有真实域缺口。零incidences不产生正x，而零jobs的物理执行不属于此源decider的对象；不能将它误读成删物理jobs。

## 2. 独立重构：YES方向与无需unit witness的LP算法

对任意实际allocation，逐组选一个attaining原state，令对应z=1，并只对该state中实际收到的正资源置x=1。资源不交保证每resourceΣx≤1，x≤z保持；这个LP目标等于该allocation的原总福利。给质量一的k个组、其余质量非负时，L≥k。

YES有实际整数k≥(1−η)n（等价k≥ceil((1−η)n)），所以L≥(1−η)n，判为YES。算法不需要找到该allocation或知道k；它只解显式福利LP并与一个可计算binary rational阈值比较。

该LP只有S+I_+个变量、n个等式、I_+个x≤z链接、m个资源容量及非负约束。矩阵系数0/1，目标为输入p；标准确定性有理LP最优值计算与比较为总位多项式。阈值(1−η)n只需有理乘法，不依赖1/(1−η)、1/γ或1/δ的数值展开。z任意每组和一、x0即合法，因此LP总可行且有界L≤n。

## 3. 独立重构：NO方向及strict边界

反设NO输入被判YES，则L≥(1−η)n>0。使用共同前提的精确福利舍入：存在实际原allocation满足W=Σ_gr_g>(5/8)L；每r_g∈[0,1]。这只是用于证明LP不可能越过阈值；最终decider无需运行finder。

NO_≥中令h=#{g:r_g≥δ}，则h<γ_hi n，其余r_g<δ。NO_>中令h=#{g:r_g>δ}，则h<γ_hi n，其余r_g≤δ。两种分别按自身语义，都有

  W≤h+(n−h)δ
    =δn+(1−δ)h
    <[γ_hi+(1−γ_hi)δ]n，                                           (1)

最后strict用h<γ_hi n与1−δ>0；不需要γ_hi n整除。由舍入和(E)却有

  W>(5/8)L≥(5/8)(1−η)n
                 ≥[γ_hi+(1−γ_hi)δ]n，                            (2)

与(1)矛盾。因此NO两版均L<(1−η)n，判为NO。

(E)的**等号**不影响：(2)第一步仍strict，且(1)最后一步也strict。不能将它误记成需要(E)留正slack。原NO若恰卡integer boundary，h<γ_hi n仍按有理严格比较处理：等价h≤ceil(γ_hi n)−1；没有四舍五入例外。

本证明未交换NO_≥与NO_>；它只是对两个各自的h分别重建同一上界。虽然给定共同前提的strict舍入还可承担某些更弱NO，本次不升级作者未声明的源版本。

## 4. 统一子域及三重等号，精确算术

在0<γ_hi≤δ≤3/8中，1−δ>0给

  γ_hi+(1−γ_hi)δ
    =δ+γ_hi(1−δ)
    ≤δ+δ(1−δ)=2δ−δ²
    ≤2(3/8)−(3/8)²=39/64。                                        (3)

第二函数在δ∈[0,3/8]严格递增（2−2δ>0）。η≤1/40给

  (5/8)(1−η)≥(5/8)(39/40)=195/320=39/64。                          (4)

因此全子域满足(E)。当η=1/40、δ=γ_hi=3/8，(3)与(4)同时取等，确为允许的三重等号，不是漏掉的边界。

在该角点，假设LP≥39n/40，则舍入W>39n/64；NO高组h<3n/8则W<39n/64。对所有整数n≥1均矛盾。譬如n40时YES需要至少39组unit，高NO需h<15；n1时YES需要1组unit，高NO需h<3/8即h0；无需将n限制为40或8的倍数。

## 5. 退化与尝试的fatal objection

* δ0/NO_≥：全部n组均有r_g≥0，且γ_hi≤1，所以NO为空。这是作者明确保留的退化语义，不反驳decider。NO_>是另一个promise，按h=#{r>0}再用(1)处理，不把它同NO_≥合并。
* η接近1：只要η<1，阈值(1−η)n仍严格正；binary有理比较不需按倒数枚举。若η1才可能失去这一步，但η1被明排。
* δ接近1：1−δ仍正，严格count上界仍传递；若δ1就不能沿用该strict项，但δ1被明排。
* γ_hi1：若(E)合法，则其右侧为1而左侧≤5/8，不可能；所以该端点没有满足(E)的输入，不产生未处理分支。
* YES/NO交叠：由(E)知(5/8)(1−η)≥γ_hi，因此1−η>γ_hi（γ_hi>0）；YES的unit组都高于δ<1，直接排NO交叠。
* 将福利LP偷偷换成FSLP：失败。近完美YES只保证福利目标阈值，不保证全部groups有disjoint full supports，故不接受这种替换。作者Exact明确没有这样做。
* 只控制完整sets/固定source labels：不够调用(1)，因为舍入输出可能重选原state并仅分配资源子集。作者NO明确量化全部实际allocation，故当前合同没有这一缺口。
* 非norm1或额外coherence：将失去r≤1或使舍入输出不属于源合法allocation，确为致命越域；作者已明排。本审查不据当前结论否定这些域。

**本次结论：** 在上述精确显式域及共同福利前提下，未发现standing fatal；decider、strict两版、binary参数和三重等号均独立闭合。此结论是Exact先读后的陈述范围内审查，不是作者Proof读后审查，也不是该福利前提的又一次blind重证。

## 6. 复杂度后果及证据限度

若NP完全语言确定性Karp-reduces到这个promise，复合上述LP decider给P=NP。随机归约必须逐其YES/NO成功事件讨论，只可得到实际合同支持的NP⊆BPP等；当前Exact没有伪造这种源归约。没有得到一般UM算法/困难性或一般Santa Claus常数结果。

本次未新增实验规模、未读作者Proof、未审canonical最终code。所有结论来自上面的有限有理式和共同福利引理；后续code22k实际读取须另冻记录，不能用本文件代记。作者Proof一旦允许读取，将按实际路径/版本另写读后攻击，不修改这份冻结记录。
