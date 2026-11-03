---
id: customer-attraction/fifty-three-unit-four-player-complete-strategy-endogenous-waterfill-benchmark
kind: construction
type_tag: 构造
title: 五十三单位四人完整策略与内生水位基准
status: fixed-input-complete-SPE-proved-by-reused-sameSHA-tail-and-root-evidence; constructor-reproduced
truth_status: finite-four-player-unit-example-not-half-counterexample; work-entry-claims-separated-from-current-checks
review_level: full1549B-instance35766B-all400-actions-and2437B-README-primary-reading; sufficient-prior-exact-validation-reused-without-repeat
scope: 四单位提供者、七共同主题、53不同单位客户、400全部有序历史固定纯策略；同一输入v4证书另独立核，不改变一般六人问题
summary: 旧34客户加P私有19，actual P,X0,Y0,Y1利润19,29/3,67/6,67/6，W51/OPT53。完整策略的399非空节点及7根比较按同输入SHA复用；静态v4=28481/2924使第二人略低于t，rootP仍为19。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/tail/endogenous_53_instance.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/tail/endogenous_53_strategy.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/tail/README.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/tail/build_endogenous_example.py
---

# 五十三单位四人完整策略与内生水位基准

## 完整单位输入及实际路径

有限单位客户共同目录，所有四位提供者权重一，客户在最终覆盖者间均分。主题顺序$(X_0,X_1,X_2,Y_0,Y_1,Y_2,P)$用索引0…6，允许重复行动和所有有序离轨历史。输入有下列14兴趣类，每个重数都是不同单位客户，非不可分加权客户。

|精确喜欢主题索引|单位数|精确喜欢主题索引|单位数|
|---|---:|---|---:|
|2|1|0134|4|
|0234|3|1234|3|
|01234|2|5|1|
|0135|3|0235|3|
|1235|3|0145|3|
|0245|3|1245|3|
|01345|2|6=P|19|

总53，主题覆盖两两不同。完整策略定义是[35766B全400动作原表](../../tools/evidence/endogenous-padding-and-security-primary/original/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/tail/endogenous_53_strategy.json)这个有限函数；输入[1549B原件](../../tools/evidence/endogenous-padding-and-security-primary/original/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/tail/endogenous_53_instance.json)同时保留。没有用“任选末BR”替代早期所依赖的特定离轨平局。

动作键恰$1+7+49+343=400$个所有长度<4的有序历史，无缺失/重复。root6=P，actual$(6,0,3,4)$，声明终局计数$(1,0,0,1,1,0,1)$。多个P和其它离轨节点由字面表定义；不将同计数历史或原34三人规则无声合并。

## 完整SPE验证的真实证据分解

前批DL在**相同实例SHA与策略SHA**上已有足够定义级校验，本批复用，未再扫描2800条或重跑旧作者3624B程序。原作者税入口按每个固定第一动作核全部57个tail历史×7动作，七根共399非空历史、2793含self比较；该原成功执行optimize0、exit0，对每偏离都计算原完整σ的真实后继并assert单位收益IC。它不核空根。

当时另有独立data-only补核七根。原强制根叶/根收益为

|根|真实完整叶|原单位根收益|
|---|---|---:|
|0|0,6,3,4|29/3|
|1|1,6,3,4|29/3|
|2|2,6,3,4|29/3|
|3|3,6,0,1|29/3|
|4|4,6,0,1|29/3|
|5|5,6,0,1|29/3|
|6=P|6,0,3,4|19|

故指定P最佳。399非空节点加根节点才覆盖完整400历史（逻辑合计2800含self比较）；**2793是旧原入口，根7是另补核**，不混成原程序已查全根。它们联同有限每人只动一次的逆向归纳证明给定σ为完整纯SPE。

[复用清单](../../tools/evidence/endogenous-padding-and-security-primary/reused-SPE-validation-manifest.json)保输入/策略两SHA、原3624B代码/成功执行/2075B报告、原root补核代码及结果六个字节载体；2394-node/path的大原trace在[原存档](../../tools/evidence/mixed-pi-and-uniform-tree-tax-primary/replay/tree-tax/passive-observation.json)保全，本次读/hash核定而不重复复制或执行。现构造器一次新运行也逐字节产生同两输入/策略，因此没有策略漂移使旧验证失效。构造与完整SPE证据的责任分开，详[生成资源](../计算/私有主题补齐构造器的单次生成与依赖--计算.md)。

actual收益$(19,29/3,67/6,67/6)$，总W51，恰漏旧单例2和5各一客户。主题$(P,2,4,5)$覆盖全部53客户，故OPT53，无需再做新OPT穷举；$2W-OPT=49>0$，不是half反例。加七共同核心会把单位每人收益加7/4、W增7，但那是前批税回归的60单位派生域，不是此1549B输入本身。

## 真正内生t及其可用范围

本批另完整核了[静态鞍点证书](../计算/五十三单位静态安全值的有理鞍点--计算.md)：$t=v_4=28481/2924$，其中4包含query本人，竞争者为其余3个静态单位主题，全部84整数多重集，而非四竞争槽或分数背景。

当前固定SPE第二人实际$u_2=29/3<t$，差$647/8772$；actual第一人P收益19>t。这个相同输入的t不是任意自由阈值，却也不自动成为每个实际玩家的逐人收益下界。总体$W-4t=8800/731>0$，此例没有否定聚合或half。

\[
 \lambda=(29/3)/t=84796/85443
\]

解释了先前统一树税回归的第三个字面质量：用的是六个强制旧主题的低根值/actual第二人低值，不是把actual首位19误写成低于t。静态证书是非适应竞争者的查询保证；原顺序玩家的真实后继观察该行动，不能直接套其逐人结论。

## 原tail README保存的完整工作入口

2437B README本次primary全文读，保以下每个导航的作用与证据责任，不把它列的审查或程序都算本五源执行：

|原导航|原文陈述/用途|本批去向与边界|
|---|---|---|
|waterfill_common_credit.md|任意人数分数水位化、共同查询信用H≤低尾缺口、质量利润守恒；真正v4/完整SPE常数1锐性族及最小r聚合归约|一般静态核心另在既有[水位引理](../引理/分数尾水位的共同查询信用与利润守恒--引理.md)；本批只这份53输入/σ/t证书，不以固定点证明整族锐性或归约|
|audit_waterfill.py / waterfill_exact.json|原文记录53单位、400节点2800比较、84静态背景及严格有理区间|不是本1189构造器，也不是旧3624税回归；本批未作为primary读取/执行该5640B审计或4775B报告，不借README摘要提前done|
|builder / instance / strategy|构造和最终核验分离|本五源正式完整读，原构造一次、完整σ按上述同SHA证据复用|
|endogenous_53_security.json|真正v4的原始/对偶匹配数据|本批全84竞争多重集/7query有理核完，最优性不从旧声明继承|
|uniform_shrink_full_tree_tax.md / global review / uniform_tree_tax_exact.json|规定路径局部regret同叶税预算、实际翻转；不能跨多次偏离望远镜|前批[作者定理](../定理/统一缩尾的规定信用与非核心精确保真--定理.md)及回归已完整处理；不在本批重跑|
|VAR盲重构/最终独审及variational_blind_exact.json|原文报告KKT、CC、FE/JOINT、唯一/连续性、同多重集交换、Debt，14证书和根信用非单调导数|这里仅保原导航和其明示范围；本批未把那些源/程序/14份证书作为primary或再独审，不从一个53证书推VAR全义务|
|zero_pool_switch_debt.md|原文记旧34完整SPE、κ0时所有真实分支H0仍有正虚拟交换Debt，阻H-only接口而非half|该未领源只是准确导航，Debt未在本批另重定义/计算；不能把“H-only失败”泛化成聚合桥或half反例|

为使水位术语自足：对一个固定根/尾多重集，$w_j\in[0,1]$是辅助质量，正质量者的**密度**$U_j(w)\ge t$，实际利润为$w_jU_j(w)$，并非每个利润都≥t。初始高者在单遍水位构造保持权1；统一缩尾则给全部tail同λ，是不同合同。同一w的全客户池H同时界全部query变化且$H\le D=\sum(t-u_j)_+$，不是每条query各领一笔D。根Γ及其它背景返还须从同一尾质量利润扣，$V(w)=V(1)-\Gamma-\Delta B$。这些已证静态关系不使辅助profile成为单位SPE。

README最后定位的共同缺口仍准确：统一税Rec只在规定叶共用终局；VAR的同多重集比较在真实换子树时会重置基线/单位集/支撑，需一次真实IC与高尾剩余利润共同耦合，不能重复花原尾利润。原“本轮收束”是历史工作交接，不是当前清洗停工；原Q-CAG-HALF/GAP-r/聚合OPEN标签不作本批新的真假结论。当前五人half有其它定理，恰六人未由本有限基准解决。

原所称shared独立盲重构及mixed锐性独审是其历史导航身份，不从README连带认证全部后续或外审/新颖性。本批只完整处置实际五主源，其他数学来源仍须各自完整primary清洗。
