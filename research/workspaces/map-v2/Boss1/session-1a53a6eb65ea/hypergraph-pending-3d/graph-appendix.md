# 同一3D包补充：v4 exact4 → 八色 → 三色的窄审查

**判定：两条当前canonical边的 whole / accepted / unconditional 维持；当前v4源delta没有侵入成熟两条全目标推导。** 结合已交主超图审查，本补充支持清除此前 `M-d007675a9ed240898c90e831af80b092` 及 `M-ab4a576ed0be482b89d4a646ffc102b9` 在此v4修复包中的3D义务。末次实际见到的integration已经是 `object_ids:[]`、`edge_ids:[]`，仅有 `archive_scopes:["archives/unrelated-machines"]`；这是观测，不是本worker进行了清写。整个archive范围及其他未指派比较不由此补充替代。

本补充按Root指派在同一worker继续，只写clone外的本文件与 `graph-bindings.json`。既有 `review.md` 与 `current-bindings.json` 保持冻结；主报告中“本worker尚未读两共享图边，保留三色pending”的阅读边界，是它生成时的真实状态，此附录用新完成的实际阅读补上，不倒改历史记录。

## 实际读取与成熟复用

本次完整读了当前source `M-ab4a576ed0be482b89d4a646ffc102b9`、八色target `M-922feb7b429f49d4b5f13ca51b34aae7`、三色target `M-d007675a9ed240898c90e831af80b092` 的完整记录，以及以下两条边全部字段：

1. `map/edges/boss5-localfix-repair-8c728e95a224313d/exact-four-to-one-v4-to-eight-color-independent-set-8c728e95a224313d.json`
2. `map/edges/boss5-localfix-repair-8c728e95a224313d/eight-color-independent-set-v4-to-three-color-gap-8c728e95a224313d.json`

同目录 `comparison-proof.md` 全文已实读，SHA是 `d1634e6dfcd5402be4adfe9b238df6a06dd1c7bdc96a1ea9f98b945be15896fe`；8c task的状态、当前input pins及receipt的coverage/数学说明已读。共享正文已在主审查全文读取，本次按同SHA复用且核其引用章节唯一。当前两边的所有evidence SHA均逐范围验证。

复用的成熟外部合同明确是：FMW perfect exact4硬度（主审查已新核定义、Theorem1.6和Appendix B）；GS20 §2.1的exact d-to-1到d-to-d induced-list桥、Theorem7、Theorem9/Lemma10与Lemma8。GS20的全文深审由正式8c证明与其原冻结证据承载，本次没有重审整篇GS20或DMR09，也没有把它们记作本次新证明。没有科研重跑或新枚举。

## v4实际delta

三对象当前版本都是4，共享正文SHA为 `d0273adacbf4ccbb9d6cd954cdfd44dddb5f8a8e969067107f63c77bdaaf4b78`。当前完整记录明确说明：v4撤回MZ印18页商数倒置的文本抽取误诊，保留事件句概率修正与一般k的floor分组补充；FMW四对象仅因共享body字节更新，其数学合同不变。本次另外对照abad历史ledger保存的v3记录快照，三对象statement与evidence逐项相同。该快照没有保存所有旧metadata字段，所以不把它夸成对旧完整登记记录的逐字段diff。

对本补充真正承重的当前完整字段，已直接核：exact4源仍是先固定任意ε、再取常数字母表、YES严格1；八色目标仍是先固定任意δ、完整八色YES、最大独立集比例严格小于δ的NO；三色目标仍是每个固定整数k≥3、完整三色YES、非k色NO。两条图证明均从FMW/GS20合同进入，未引用MZ的Claim3.2、一般projection、近完美YES或实际字母表幂次soundness。因此共享body中的上述MZ变化没有改变它们的前提、完备性、解码或参数顺序。

## exact4到八色：全目标接口闭合

源perfect exact4的左右域比4、每右标签4个原像、任意小固定NO soundness、常数字母表和带身份多重约束，完整支付GS20 d=4的输入。Appendix B增加平行约束并保perfect的部分已在主报告独立核算，不以“同一图”偷掉约束重数。

这里必须保留成熟induced-list桥的两个量词：每个先固定列表上界t、每个先固定诱导比例a0；其NO排除在足够大的顶点子集中用每点至多t标签满足全部诱导约束。当前边和proof都没有由普通低满足率直接跳过此桥。

固定 `0<a<min(δ,1/8)`。GS20 q=2d的构图在d=4给q=8，perfect源标签指定码字坐标，Markov支持两对应d元组的不交性使每条输出边异色，保完整八色。若有比例≥a的独立集，密度≥a/2的码块对应源点集Z满足 `|Z|/|V|≥a/2`。每条诱导constraint-ID各自零相关测试，Theorem7使用严格均值阈值a/4，Lemma6给对应d块中的两侧影响坐标。

统一列表取 `L(w)={i:I_i^(≤dh)(g_w)≥η/d}`，由总低度影响≤dh，有安全界 `|L(w)|≤d²h/η`，故t=ceil(d²h/η)是固定常数。当前proof已经支付比原印刷计数更保守的d因子，不需要新增假设。固定列表对每个诱导ID给对应块里的两侧标签，故统一列表满足Z内全部诱导约束，包括同端点不同关系。取a0=a/4与Z≥a/2矛盾。于是NO最大独立集比例<a<δ；输出重复普通图边可去重，源constraint-ID不可去重。

常数顺序是δ→a→影响阈值/低度→t、a0→induced-list桥要求的源soundness→FMW常数字母表。码块与支持展开随后为确定性多项式。完整八色目标已付清，边是whole而非仅局部contribution。

## 八色到三色：固定k的整条有限链

先固定目标整数k≥3，令 `t4=2^(2^k)`、`b(n)=C(n,floor(n/2))`、`C=b(b(t4))`，再取独立集阈值δ<1/C。源NO若C可着色，至少一个颜色类占比≥1/C>δ，违反独立集NO；YES仍八色，所以确实得到GraphColoring(C,8)源合同，而未把同一输入图直接称为三色。

调用成熟Lemma8的一般步骤 `GraphColoring(b(t),b(c))≤pGraphColoring(t,c)`：八色YES可视作二十色，b(6)=20、b(4)=6使两步成为六色、四色YES；NO对应从非C色依次变为非b(t4)色、非t4色。再按Lemma8给的两次arc构造，四色YES成为三色YES；若最终图k可着色，标准子集着色反推界两次给四色阶段至多 `2^(2^k)=t4` 色，与NO矛盾。

参数顺序 `最终k→t4→C→δ→源gap/字母表` 在输入规模前固定，C虽大但为常数，每段确定性多项式，复合仍多项式。对所有固定k≥3的全目标与当前三色对象的model、statement、quantifiers、scope完全相符；没有把k当随输入免费增长参数，也没有额外最大度要求。

## 绑定与3D处置

source/八色target/三色target的当前pins依次为：

- `e2f4d171f9174665027371524263e60473a991292495c0041683392feaa38077`
- `551be6c145cf6c5ee53f5828c71aeef6fbd22f50a958928a01a802fe2b213aed`
- `99d7c06058a4c711748cbebb1e385f2fe1ce667604d22407eda463831c1f8edb`

两条图边当前raw SHA依次为 `2154e7f238a0764c054b871cab7fb3ecf47bc02d57a23851d8a3dc9e98a5d27a`、`7fcb8fcc3c8612224e9a3af03f9cc5111e89de3e13159a0b8520ee646af56c13`。边仍canonical，endpoint pins与当前登记和8c task input pins一致；两边native pin与integration一致；8c receipt的native pin与任务内嵌收据、integration一致。精确快照、当前HEAD及所有本范围refs见 `graph-bindings.json`。

可以采用本补充解除此前三色target的“尚未由本worker读当前共享链”限制；结合主超图报告，source本次v4 delta在指派的两个图应用与超图应用均已闭合。八色target是已核的共享中间全结果，无须新增pending。当前object/edge pending为空，与本补充结论相容；仍存在的UM archive范围不能仅凭这三个FMW应用清空。

无新错误、缺步或正式repair需求。仍保留成熟合同的原适用范围：带身份多重约束、固定参数、完整YES、不免费得到R幂次soundness、最大度约束或UM/SPE迁移。本补充没有修改任何仓库资产或主报告。
