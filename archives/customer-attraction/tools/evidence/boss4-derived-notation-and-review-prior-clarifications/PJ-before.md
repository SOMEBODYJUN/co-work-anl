---
id: customer-attraction/small-outsider-relative-core-capacity-induction-and-automatic-half
kind: theorem
type_tag: 定理
title: 小外部主题闭合的相对核心容量归纳与自动半覆盖
status: 只合规前缀的全SPE容量归纳成立；cap和=m自动严格half，不要求G覆盖全客户
summary: outside<λ严格排除污染，允许相对G私有核心；统一非负真实偏离给W≥mλ及OPT<(Kcap+m)λ，Kcap=m时half，不能替换为outside≤λ。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-ab183d14fb74403091d09db766b05f73/global/small_outsider_capacity_half.md
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-ab183d14fb74403091d09db766b05f73/independent/capacity_core_outside_audit.md
---

# 小外部主题闭合的相对核心容量归纳与自动半覆盖

5693B作者及4985B独立稿逐份全部实读。PJ5实际完整24项claim 36bea7b95047e83d4ca011ddff3f1266ebff278a pushed/synced，本5subset/owner/sourceSHA/size/blob核；当前只封语义清单，不预称正文已推/done。作者最终版已吸收独审加强；4985明确只接精确statement、未读作者正文或实现先重构，与其它读后guard审查区分，不将当前知情比较称新盲审/外审。

## 原模型与精确条件

有限单位客户、有限非空共同目录S、m≥1单位玩家，固定任意完整有序历史纯SPE σ，允许空/重复题和任意历史依赖ties。非空G⊆S、各T正整数cap k_T，Kcap=Σ_Gk_T≥m。a_T为T里只被G中T覆盖的客户数，**可**被任意outside S∖G覆盖，不要求全S私有。λ>0，要求每guard
\[
 a_T/k_T+(|T|-a_T)/m≥λ,\qquad |T|<(k_T+1)λ,\tag{1}
\]
每outside题U严格有|U|<λ。称有序前缀合规若只含G且各count≤cap。结论：每合规前缀后的原σ续局仍只选G、不超cap，每个**剩余**玩家在该真实终局的利润≥λ。根合规，故actual全利润≥λ、W≥mλ。不声称此前已有outside/超cap的不合规前缀也享同下界。

## 不删原目录的完整有序子局归纳

按剩余深度逆向，量化所有合规有序前缀而不识别同计数历史。长度t<m时不可能全部G已满，否则t≥Σcap≥m，故有未满Q。当前真改Q后前缀仍合规；所有更深合规节点的归纳保证后继只G/不超cap，因此该真实偏离终局中Q份数≤k_Q，核心a_Q不被其它实际G题分享，各给≥1/k_Q，其余Q每客户给≥1/m，故改Q收益≥λ。

任何outside无论什么后继都给当前≤|U|<λ；任何已满T在当前再选后终局至少k_T+1个T玩家，当前收益≤|T|/(k_T+1)<λ。这两个无条件上界不需其非合规孩子有结构；原完整σ在那些孩子的行为完整保留。SPE最优性使规定收益≥λ，故规定只在G选未满题，孩子合规，完成逆归纳。末位即同一无后继基例。

outside虽然相对核心污染，严格小题使其不在任何合规续局中被选；把实际路径“没有outside”当先验则循环，以上证明没有这么做。任意tie都保，因为排除条件是严格差。

## 容量和等于m时自动严格half

取任意至多m个比较题，删重复后G内子集H、outside数t，|H|+t≤m。并集≤大小和，若非空比较集合，由严格大小条件
\[
 |\cup\text{比较题}|<λ(\sum_{T\in H}k_T+|H|+t)
 ≤λ(Kcap+m).\tag{2}
\]
空比较集/全空主题覆盖0也严格小于正右端。有限目录使OPT达到且保严格，
\[
 OPT_m<(Kcap+m)λ,
\quad OPT_m/W<1+Kcap/m.\tag{3}
\]
根W≥mλ>0所以此比率合法。特别Kcap=m时OPT<2mλ≤2W，**不需G覆盖所有客户**；outside可包含G并集以外的客户。|G|≤m已由cap≥1/总和m自动推出。Kcap>m的(3)本身不保half，也可另给OPT≤2mλ或宇宙覆盖数≤2mλ作充分证书。

4985独立稿记载，原先G覆盖全部可覆盖客户的子类被它加强成上面自动half；5693作者最终版已吸收。这里保两原稿的版本报告，不声称本次另取了未提供的初稿，也不把它们记作两项不同新定理。存在λ/cap/G证书是一项可核对输入条件，不是说任意原实例都有这种证书。

## 无全目录私有、无界极大题数量的全m例

每m≥2，G为m个不交3客户块B_i、cap1、λ3，outside取全部跨两不同块的二客户题，可再添全部单客户题。每客户都在outside出现，没有全S私有核；相对G仍a=3。outside大小≤2<3、guard3<6、总capm，故actual必须m个不同B_i，WOPT3m。

所有跨块二客户题都不包含于任何B_i，不同二题也互不包含，极大题数m+9·binom(m,2)无界。原最优覆盖的分数覆盖数恰m：m个B_i给上界，每客户对偶1/3使guard权1/outside≤2/3给下界。它不要求分数覆盖数≤7/2，也不声称排掉所有其它定理的间接证明。

## 严格性与另一全历史污染定理

若只改outside≤λ，[十一客户及每m完整反族](../反例/外部主题等号边界的全历史收益保底反族--反例.md)给W<mλ，因此不能复用本中间归纳；那些实例half仍真，不判弱条件全类half。若改guard大小≤(k+1)λ也可能满题平局，此proof不能沿用。

[有限污染整数guard](有限核心污染守卫的整数平衡信用与全历史归纳--定理.md)是另一正面合同：用outside与核心最大交β/整数平衡信用，在所有合法前缀给≥λ且可实际选大outside。它与本定理不同历史域，不能抹去严格小题条件便冒相同结论。零客户或空guard若不满足正λ只表示证书不适用；所有原模型零/空/重复边界仍允许。
