# 私有树全阈值配置界与承诺判定：v2 扩展陈述先行审查

审查者：boss11 内部 cover_consistency。实际只读 Exact `private_tree_configuration_floor_v2_exact_statement.md`，SHA256 `ad33f6b2c42c184b943651e61437ece2d1372ee1445443017e62534d83487900`。本稿冻结前尚未读作者 v1 proof 或任何 v2 proof，也未询作者思路。已知本人 v1 独立 hitting/Haxell 证明，允许作为背景，但A/B/C新增量词在此重新核验，不能把旧审查直接升级覆盖。

结论：A/B/C均独立闭合，未发现standing fatal objection。关键新增B使用CONFIG配置的**联合条件行分布**，而不是只用总load或粗边际和。C仅为判定器；没有把有限匹配存在性升级为一般参数位多项式输出σ。

## 1. 完整CONFIG(T)的精确小型行系统

先任取T∈[1,2)，写s=floor(d(T−1))，a=d−s，故0≤s≤d−1、1≤a≤d。

每个私有内部机器恰有一个可在此取unit的输入job（根是本root的selector，其它节点为父edge job），及d个可在此取small=1/d的出job。设输入unit边际为x，出job在其child/外机的unit边际为z_j；因每job恰两个合法端，留父边际为1−z_j。全部x,z∈[0,1]。

行配置不含输入unit时可含任意small子集（总和≤1≤T）；含输入unit时最多s个small，因此至少a个出job不在父机。故必要条件为

 Σ_j min(x,z_j) ≥ a x。             (1)

这有多项式线性扩展：引入q_j，要求0≤q_j≤x、q_j≤z_j，Σq_j≥a x。根输入边际λ_us再满足每u的Σ_sλ_us=1；每external z的所有leaf-unit边际总和≤1，因为T<2时external配置至多一枚unit job。变量/约束按显式原P为线性量级。

(1)也充分，而非只是松弛。取q_j=min(x,z_j)。若x>0，q/x在[0,1]^d中且坐标和≥a，故是大小至少a的子集的incidence convex hull（uniform-matroid complement的整数polytope）。在输入unit出现的mass x上，抽一个如此分布的“未留父”子集，其small数≤s；在unit不出现的mass1−x上，以剩余未留父边际(z_j−q_j)/(1−x)选任意子集，各坐标落[0,1]，可独立抽。此时父端small边际恰1−z_j。x=0或1时只保留有正mass分支，同样成立。external按leaf-unit marginals配置singleton/empty分布。每原job两个端覆盖恰1，故所得是真正完整CONFIG(T)。

等价地，可以从真实CONFIG witness直接定义q_j=Pr(input-unit在本机且出job不在本机)，它满足q_j≤min(x,z_j)、Σq_j≥a x。这里不需要把每job在不同机器的随机配置耦合成实际全局调度；配置LP只要机器分布和覆盖边际一致。

切勿把(1)换成Σz_j≥a x：例如d=4,a=3,x=1/10,z=(3/10,0,0,0)通过粗总和却不通过(1)，不能支撑下一节的分数a树。这是B证明的一个实质审查点。

T≥2时原P有全父置、任取selector根的实际C≤2，因而CONFIG(T)可行；T<1时非空selector无合法配置，CONFIG不可行。空U另作零值处理。usual“至少覆盖”版可在向下封闭配置中逐job稀释至覆盖恰1，因此不改变本系统。

## 2. A：CONFIG(1)与共同full-bundle λ

T=1给s=0、a=d，(1)迫使每个out-unit边际z_j≥x。根input的λ_us之和为1；向下逐层可知每个state全部leaf-unit边际至少λ_us。每external的unit边际总和≤1，故

 Σ_(u,s)λ_us |f_us^−1(z)|≤1。

这给所声称的共同λ。反向给λ后，可显式构造CONFIG(1)：每state每machine以massλ_us放输入unit单件，以mass1−λ_us放全部d个父端small（负载1）；每external对每个真实leaf job放权重λ_us的singleton，加空配置补足1。所有edge/leaf两个端覆盖λ+(1−λ)=1，selector各根覆盖之和1。external不超1由λ系统保证。

于是A成立。此等价自身的必要性/充分性实际上也能保留multiplicity而用于非注入f；但本v2仅在注入域陈述A，并不据此把非注入CONFIG整数gap也升级。λ系统包含每个显式state一变量和每个external一行，系数可由显式leaf资格统计，数目和编码位长均多项式。它不是“λ可行⇒实际C1”的声称。

## 3. B：从CONFIG(T)抽出共同分数满a叉子树

从给定CONFIG witness，在每root先按λ_us选择一个state。每state内部node的input-unit边际记x_v。归纳保持该node被抽入a树的概率α_v≤x_v，根处等号为λ。

当node被抽入且x_v>0，在它含input-unit的条件配置分布下，至少a个出job不在父机。按一个固定次序从这些缺席出job中选恰a个，激活相应child（末层则选leaf）。对某出job e，其被选入的无条件概率至多

 (α_v/x_v)·Pr(input-unit在node且e不在node)
 ≤ z_e。

而z_e恰是该child的input-unit边际，故归纳成立。x_v=0时node被抽中概率0，任填条件规则即可。由此每root得到一棵真实state中的满a叉高度h子树的有限分布，其所有leaf-resource expected multiplicities不超过原CONFIG的external-unit marginals，故总和≤1。每root所选state/树的总权仍是1，是同一份共同分数证书。

有限分布可以有指数个完整a树；本证明只需存在。CONFIG有有理系数和有限配置时可取有理witness，条件抽样得到有理有限分布；无需声称写出它有多项式长度。

原f_us注入保证每个被抽出的满a树的叶外机也互异。把这些a树视作combinatorial candidates，对每个candidate的全部满r子树作Haxell资源超边。任一资源hitting集命中某个candidate全部r子树，至少含(a−r+1)^h个candidate叶。以上共同分布和资源cap1给每I的τ_I≥(a−r+1)^h|I|。每资源超边大小R=r^h、总边大小R+1；若(a−r+1)^h≥2R−1，则Haxell严格条件成立，得到每root一个真实r子树且全部外机不同。

这里虚拟candidate a树可以同属一个原state，内部节点因而可能相同；这不损害实际结论，因为最终每个root只选一个candidate/r树，原来不同roots的机器全私有。没有把虚拟candidate当成原P中新造的机器。

外部定理参数已在本人v1独立稿实际核 primary：Annamalai arXiv1509.07007v2 PDF2/印1 Thm1.1复述Haxell，uniform总edge size k给2k−3；本处k=R+1，确为2R−1。本文不声称另读过作者引用的1995原证明或其算法实现。

## 4. B的原P负载、算术和全部T

最终选定r树内机器收一unit、r个出job下送、d−r个原small留父，负载2−r/d。相同原state的非r分枝无unit incoming，全部d个出job留父负载1；所有未选state同样全父置负载1；external至多一个unit。每个原job仍恰一次，仅用原资格。注意实际保留的是d−r个small，不能把负载分母误换成a。

取r=floor((a+2)/3)=ceil(a/3)，有a−r+1≥2r−1，且(2r−1)^h≥2r^h−1，所以条件对全部h成立。又3r≥a=d−s，故

 2−r/d ≤ 5/3+s/(3d)
           ≤ (5/3)(1+s/d)
           ≤ (5/3)T。

因此Exact给的较松链正确。T∈[1,2)给a≥1；r≥1且r≤a≤d，没有隐藏空子树。T≥2时全父置/任选selector的实际C≤2也满足5T/3。

非空结构的配置阈值≥1。T<2时可行性只随整数s=floor(d(T−1))变化，2时必可行，因此最小配置阈值在有限网格{1,1+1/d,...,2}上取得；即使不使用此网格，也可对一列可行阈值取极限得到实际整数gap上界。有限调度集合保证OPT为最小值。故全部CONFIG阈值的量词确给结构类gap≤5/3，没有仅证明CONFIG(1)后偷升到全T。

## 5. C：安全过滤、原jobs保留、判定边界

若原P有实际C≤1，selector把某state根塞满1，该机的所有出job都必须下送；逐层unit塞满迫使该选state整棵d叉树全部下送至external。若该state有两枚leaf同外机，则外机收≥2，矛盾。所以任何真实C1调度每root所选state必是单射state；跨root所选全bundles外机也必须互异。

因此排除非注入state作selector候选安全：若某root无候选，原OPT>1；否则任何C1调度给过滤菜单上一个integral λ certificate。过滤λ LP不可行必原OPT>1。

反向若过滤λ LP可行，所有保留states注入，应用v1或A+B在T1的存在性得保留树上的实际C≤5/3。把每个被排除state的所有原port/edge job全部留父，其机器私有、没有selector投来，每机负载1，亦不增加external负载。它们的原jobs和原机器始终保留，故得到原完整P上的C≤5/3，而不是另一个删任务实例。

按每个显式f_us检查重复外机是确定性多项式；过滤λ LP规模及有理编码多项式，可用标准精确有理LP可行性算法判定。因此C的输出YES/NO为总位多项式。它没有必要找到Haxell匹配或输出实际σ：

- YES承诺OPT≤1的输入必通过过滤LP；
- NO承诺OPT>5/3的输入必过滤LP不可行；
- 中间1<OPT≤5/3两种回答均允许。

LP失败只保证OPT>1，不保证OPT>5/3；LP成功只保证存在C≤5/3，不保证OPT≤1。没有把判定器误写成一般变参算法构造，也没有声称非注入原P的CONFIG gap≤5/3。

## 6. 退化与范围

d=1时a=r=1，所有state单叶天然注入，Haxell退化Hall，条件和全部负载公式有效；任意h的显式链无额外困难。零λ/x节点如上跳过条件抽样；未选原states不能漏。U空时模型没有selector和树jobs，OPT=Tconf=0、空σ合法，应单独答YES而不套非空下界1。非空模型中Z为空和有效f不兼容，不构成合法反例。

本报告只审新增A/B/C数学与算法层级，未读任何作者proof、未运行程序或有限实例、未认证外部新颖性。结果限于此完全私有、unit selector、父1/d/子或外端1、每leaf唯一外端的模型，不能推广到其它资格、共享内部机器或任意一般UM。
