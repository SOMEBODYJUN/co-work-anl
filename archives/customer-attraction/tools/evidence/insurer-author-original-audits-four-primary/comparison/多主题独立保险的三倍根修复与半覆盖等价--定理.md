---
id: "customer-attraction/multi-theme-independent-insurer-three-regret-repair-and-half-equivalence"
kind: "theorem"
type_tag: "定理"
title: "多主题独立保险的三倍根修复与半覆盖等价"
status: "padded-compiler-and-fixed-m-half-root-regret-equivalence-proved; no-bad-old-plan-exhibited"
summary: "m个不交保险块保旧actual并修完整根，half缺陷只稀释3s；固定m的half等价全部正深度SPE计划OPT−2W≤3Δ。客户成本/实际福利/稀释三对象与盲审边界分开。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/compiler/padded_insurer_repair.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/compiler/disjoint_insurer_spread.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/independent/insurer_blind_review.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/compiler/disjoint_insurer_three_sharp.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/independent/insurer_three_sharp_review.md"]
---

# 多主题独立保险的三倍根修复与半覆盖等价

7608B作者主稿本次正式primary完整处理。此前[fresh缺陷页](../引理/笛卡尔目录的最优查询缺陷与三倍根修复--引理.md)已有同padded组件；这里完整保作者全部历史策略和**原half本身**的等价R4，以及实际盲审先验和三个成本对象，不认领组件首次发现。

## 原输入、正有理记账与结论

固定m≥2，有限单位客户共同非空目录，完整计划τ在每个正深度子博弈为纯SPE，根指定A可非最佳。u是actual根收益，d_B是强制旧根B后按τ真实后继的收益，Δ=max_Bd_B−u≥0（含不偏离）。不得只核actual后缀。

取有理s>0、s≥Δ。与旧客户及彼此不交的保险块X,Y,Z1…Z_(m−2)大小为2s、(m−1)s、s。保险目录恰这m主题；新共同目录为全部旧B与保险T的Cartesian并集B∪T，最多mp联合覆盖（旧p主题），不是“原目录加两个总主题”。m2无Z。

若s非整数，以下先作有理记账；将**全部旧、新**客户同乘正整数L清分母，才得到单位客户实例，所有收益/福利/Δ也同乘L。选择s=Δ>0时，单位旧游戏所有收益分母整除lcm(1,…,m)，取该L可使LΔ整数。不能只缩新保险而保持旧单位收益不变。

存在完整纯SPE保旧坐标actual路径，保险actual为X,Y^(m−1)，根利润u+2s，并有

\[
W_{new}=W_{old}+(m+1)s,
\quad OPT_{new,m}=OPT_{old,m}+(2m-1)s,
\quad OPT_{new,m}-2W_{new}=OPT_{old,m}-2W_{old}-3s.\tag{C}
\]

这些式为清分母前的记账；实际复制单位实例整体再乘L。新策略不冻结旧根偏离后继。

## 所有保险历史的H、L_X、L_Y、L_Z

先s1。提到BI退出时，在该**确切保险前缀**整个子树固定一份有限逆向归纳完整纯SPE，之后永久执行，不随旧坐标或未来事件换模式。

H：根X后每个历史均规定Y。若已有a≥1次X、c次Z类动作，当前规定Y后最终Y数m−a−c≥1，利润(m−1)/(m−a−c)≥1；改X得2/(a+1)≤1，改任意Z最多1。它覆盖重复X和含Z离轨历史，根保险收益2。

L_X：根X后第二人规定X，从深度2起每个历史均全Y（含第二人改Y/Z的分支）。第二人依从X得1，改Y终局X,Y^(m−1)也1，改Z至多1；深层已有根X，由H同算。首人保险收益1。

L_Y：根Y后检查首个非Y行动。尚无非Y时当前规定X；首个非Y为X后全Y；首个非Y为任意Z后**永久BI退出**。纯Y前缀当前选X独占得2；改Y且还有后继，下一人会选X，其后全Y，使偏离者得1；若已末位，改Y得(m−1)/m<1。改Z不论BI出口选择如何最多1。已有X的区域用H比较；Z出口用其完整BI。实际Y,X,Y^(m−2)，固定首人收益1。不能在无X却已有很多Z的历史仍强制X。

L_Z：根任意Z_j后任选完整BI；固定首人自身块总大小1，所以其收益≤1。无需断言后继常值。m2时H仅下一Y、L_X仅第二X、L_Y仅第二X，没有Z出口，上述仍合法。

## 完整联合偏离与根修复

新根规定(A,X)。各联合根后一次固定：该指定根用τ_A与H；(B≠A,X)用τ_B与L_X；任意(B,Y)用τ_B与L_Y；任意(B,Z_j)用τ_B与L_Z。旧坐标此后只读旧历史，保险坐标只读保险历史，模式已由根固定，不能因以后旧行动更改。

每个正深度节点，两坐标分别是完整suffix SPE。任意同时改两坐标的合法动作，其收益差是两个非正差之和，故不盈利。完整Cartesian目录承重；缺边目录不能直接套该分解。根实际u+2s，任何其它联合根旧收益≤u+Δ、保险≤s，合≤u+Δ+s≤u+2s。根也BR，得到完整纯SPE，含全部离轨/重复/平局。

实际保险覆盖X∪Y给(m+1)s，总保险并集含m块为(2m−1)s；m角色各选一次可全覆盖。旧最优m元组与保险最优m元组任意按位置配对合法，客户不交使OPT准确相加，故(C)。不能把总新增客户数当actual福利。

## 固定人数的精确等价攻击接口

令G(τ)=OPT_m−2W(τ)。对每个固定m≥2，原单位模型“每份完整有序历史纯SPE均half”等价于

\[
\boxed{\text{每个正深度为完整SPE的计划}\ \tau\text{均满足 }G(\tau)\le3\Delta(\tau).}\tag{R4}
\]

正向：Δ>0取s=Δ，必要时整体清分母；新完整SPE若half，(C)给L[G−3Δ]≤0，除L即R4。Δ0时τ根本已BR、整计划为完整SPE，直接G≤0，不往正s构造塞s0。

反向：任意完整SPE取Δ0，R4恰G≤0。故这是保同人数、单位客户、全历史和平局量词的等价接口，不更换或解决原目标。若Δ>0，严格G>3Δ当且仅当本s=Δ编译产生half反例；尚未展示这样的旧计划。Δ0且G>0时旧计划自己已是反例，无需新增零大小重复空主题。

[53固定私有支架](../引理/私有最优遗漏计划的单根缺陷与尾部席位界--引理.md)解析排其全部可行重数的G>3Δ，但条件只私有遗漏/固定τ；[本批原审计](../计算/固定私有尾策略的七根原审计与类型证书--计算.md)的七负margin也不构成一般R4证明。更强的正深度-only half只是源提出的另问题，不由有限诊断确认。

## 三种成本不可替换，常数锐性不得跨审查

本padded实际值：总新增客户C_ins=(2m−1)s，actual福利W_ins=(m+1)s，half稀释2W_ins−OPT_ins=3s。旧独立两主题构造C=W=OPT=(m+1)s，稀释(m+1)s。新加m−2个未actual覆盖叶块，actual不变、OPT增(m−2)s，使稀释减少(m−2)s；不是把总C成本也降到3s。

[两主题成本定理](两主题笛卡尔根修复及成本下界--定理.md)已给C≥(m+1)Δ。相关10996B多花瓣稿本次全文读：在删共同核后的不交极大花瓣类（允许任意内部子主题），固定同保险根A的suffix SPE收益跨度≤C/(m+1)，所以独立坐标修根也需C≥(m+1)Δ。其证明用singleton剩余阈值席位、SPE终局PNE及占用差至多1，再动态删严格子主题；这是**总客户数**下界，不是half稀释下界。padded在sΔ时总C=(2m−1)Δ≥(m+1)Δ，完全相容。

作者末段提“不交保险常数3锐性”未在本7608证明中展开；第一份7442B盲审**明确排除sunflower-insurer稀释下界/锐性**。不能由已读总C下界或3s达到值自行推出架构的half稀释下界。为核清这条后续，本次另完整读取7242B锐性作者稿、1827B仅陈述和7382B后续独审，全部作为[相关原文](../../tools/evidence/root-audit-restricted-graphs-and-insurer-primary/context-manifest.json)保全，未提前计它们primary done。

后续的准确类是：K为**全部合法主题**的交集，删除K后不同包含极大花瓣两两不交；允许内部子主题/同覆盖标签/任意有序平局，固定根A也可能只是花瓣内部主题。不能换成“仅极大主题交集”后允许内部根漏掉核心，否则逐人恒定|K|/m无法相消。对同一A后的两份真实完整suffix SPE，若首人u_H>u_L、δ=u_H−u_L，则高分支实际覆盖W_H与同实例OPT_m满足

\[
2W_H-OPT_m\ge |K|+3\delta.
\]

这里根自身无需BR。后续证明用已读spread的动态删除/PNE工具：无核时令A⊆极大花瓣B、a=|A|>0,w=|B|，B后继函数a/(t+1)+(w−a)/t，其它花瓣w_j/t。两PNE的B后继数至多差1，高/低可记k−1/k，δ=a/[k(k+1)]。高分支最低后继利润μ>0；k≥2时已用花瓣都完整覆盖，O≤W+(m−ell)μ、W≥(m−1)μ+a/k，故2W−O≥a/k≥3δ。k1时高分支无后继触B，W=a+P，μ≥w−a/2，P≥(m−1)μ，且O≤P+max(w,μ)+(m−r−1)μ，得2W−O≥3a/2=3δ。加回核心给|K|。严格内部根的w−a项保留，未把根直接扩张。

后续还证明任意固定根/任意真实suffix都基线2W−O≥|K|≥0（包括残余根空的δ0边界）。因此任意多个客户不交、根以下每分支按坐标独立执行真实suffix的Cartesian坐标，允许δ_l异号：D_l对δ_l>0至少3δ_l，对δ_l≤0至少0，故ΣD_l≥3Σ_(δ_l>0)δ_l≥3Σ_lδ_l。与旧最大偏离**保持同一联合保险根**比较，修复需Σδ_l≥Δ，所以本精确架构稀释≥3Δ，padded取等。这是后续另一个真正成本定理，不与总C下界混同。

这不证明R4中的3对任意旧计划最佳，也不排根后继续跨坐标切换续局、共享客户或一般交叠极大覆盖。第一份盲审的“不审锐性”先验不变；后续7382独审才核本精确类及其3下界。本次已读证明后核对，不新增blind或外审身份。

## 独立先验与本批程序边界

相关1679B仅陈述稿、7442B盲审稿及10996B成本稿均完整context保存，不附带primary done。盲审先收到root消息的精确statement，独立重构与审计时未读作者证明；完成后才读statement文件和当前作者稿。它先按整数s陈述、对有理Δ共同复制L，特别澄清m2 punitive XX只覆盖2s而compliant XY才3s。其补全策略较作者H更繁，但同根高/低收益和联合模式一样正确；本页已完整核对作者更简H与永久Z出口。

原作者audit_padded_insurer.py及盲insurer_blind_audit.py不属本五源，本批入口均0；盲稿所报m2…6保险120552节点-动作、m4旧三主题L2联合22620比较只作历史审计范围，不算本次新调用。当前实际原程序只有6714 root与2920 graph各一次；它们没有检查保险H/L_X/L_Y/L_Z或R4。任意m/任意旧τ结论由上面完整解析证明承担，无新blind/外审/新颖性认证。
