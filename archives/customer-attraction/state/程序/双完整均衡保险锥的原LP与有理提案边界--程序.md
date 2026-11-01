---
id: customer-attraction/insurance-pair-fixed-cones-and-rational-proposals
kind: program
type_tag: 程序
title: 双完整均衡保险锥的原LP与有理提案边界
status: original-code-two-reports-and-runtime-sources-fully-read; no-LP-replay
truth_status: two-negative-rational-points; no-certified-LP-optimum-or-universal-insurance-bound
review_level: informed-source-and-analytic-point-accounting; no-new-independent-game-verification
scope: two-named-original-inputs-derived-full-policy-pairs; all-mask-reweighting-with-fixed-policy
summary: 实际源码从两来源SPE全集取多high/首low固定锥，双方保root及全historyIC，全部兴趣型权重/14或56支持数值LP；两负有理点全字段，不冒同根跨度/新菜单floor/对偶最优。
source_ids: [3f900cb2b58a9b7e2129, cba82764e1c24456332c, de3c477c8761be7fba26]
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/credible_attack/insurance_pair_attack.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/credible_attack/insurance_pair_attack.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/credible_attack/insurance_pair_eight_cce_welfare_gap.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/credible_attack/insurance_pair_eight_cce_welfare_gap.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/credible_attack/insurance_pair_root_tax_failure.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/credible_attack/insurance_pair_root_tax_failure.json
---

# 双完整均衡保险锥的原LP与有理提案边界

实际normalshow原三件共4129B：3328B代码及344B/457B两份报告，全部实读。此前[整尾势诊断入口](../资源/整尾势漂移与有限阈值诊断的停止边界--资源.md)只据MD保有限保险攻击、无对偶最优证书，本次补代码真实循环与两原点全部数据，不改写历史“当时未读程序”的身份。**本包原CLI/import、solver/策略生成、LP、IC、参数扫描及新数学实现均0。**

## 被攻击不等式与有效修复幅度不同

采用[单位客户共同目录完整历史纯SPE](../定义/共同目录完整历史模型--定义.md)。在同一人数/同一目录/同一客户权重实例，H、L是两份**完整根也最佳**的纯SPE策略，actual首人利润分别h、ell，高枝实际福利W_H，真实最优覆盖OPT_m。源候选为

\[
D:=2W_H-OPT_m\stackrel?\ge3(h-\ell).
\]

名称high/low先按原输入挑，不保证改变客户权重后仍是全体均衡的最大/最小根值。也**不要求H、L根动作相同**；两原报告恰都不同：八客户来源H首1/L首0，根税来源H首5/L首2。不能将它们说成固定同根A的两份suffix跨度，或借不交花瓣同根锐界替其一般交叠LP作证明。

[有效菜单引理](../引理/保险根菜单的有效幅度与调和后继保底--引理.md)中M是**全部完整根SPE**的最低首人利润，保险真正可修幅度e=h−M。对保持可信的选定L只知ell≥M，所以h−ell≤e。原代码重权后不重新求新M，所存ell也不是自动达到新floor；即使对全部选定pair证明D≥3(h−ell)，也不能据此给D≥3(h−M)。若将来得到h>ell、D<3(h−ell)的完整原模型点，它当然也击穿更强有效幅度界，但仍不自动搭配出旧主组件足够大的half缺陷。现在两点均为负目标，不给这个见证。

## 读哪些输入，生成哪些完整策略

主入口有guard；`main(name='root_tax_failure')`，可传一个bare name，`main(*sys.argv[1:])`多于一参数会TypeError，没有argparse、种子或输出路径选项。ROOT按脚本parents[5]定位原仓库；OUT为原脚本目录。导入NumPy、SciPy linprog以及项目Instance/ExactSPESolver；guard只阻main，普通import仍会导这些模块，本次未import。ROOT不自行注入sys.path，项目包和第三方依赖须原运行环境能解析，本包不捏造版本/安装状态。

它**不读旧certificate JSON**。读`examples/customer_attraction/<name>.json`（若顶层instance则取其值），Instance解析正整数单位客户重数及合法标签，ExactSPESolver从该原实例求全纯SPE可实现终局。此次相关依赖包括完整model/exact/certificate/__init__四源、两个example，均从已发表同SHA缓存全文理解并保全，无新增done。

M_orig=`s.threshold((0,)*p)`。依已读精确求解器，给定计数k的每个行动孩子终局集E_a，门槛max_a min_(z∈E_a)u_a(z)，保所有达到门槛的合法子局终局；这恰是原根最低完整SPE首值。计数只缓存集合，不把所有同计数有序历史强制成同一回复。

高策略cases循环所有`s.outcomes()`终局计数t，再循环其`s.ordered_outcomes(t)`可实现有序路径z。若原h>M_orig，或cases还空，就生成`s.certificate(on_path=z)`；再按**(根动作z₀,终局计数t)**去重，保首次选中的完整profile与path。同根同counts的其他有序路径及其不同完整offpath策略不再入cases。首case可能只是h=M_orig，也会强保，因此不能写“每个case必严格高根”。

低策略lows另从原outcomes/ordered paths找首个根利润恰M_orig者，生成完整certificate，内外两层立即break，**只用这一份L**。原outcomes返回frozenset，首项遍历顺序没有稳定对外保证；它没有枚举所有最低根profile，亦无高/低完整策略数量日志。仅遍历所有可实现有序叶不等于遍历所有完整策略图。

certificate实际按指定on_path保该叶，离轨孩子选当前行动者最低的可信后继，默认取字典序首个min-counts及首个可选行动；所有有序子树展开完整。由此cases每个元素包含完整actions，但**最终报告只留high_path/low_path，不保存这两棵actions**。原代码未调用verify_certificate，不能将相关模块存在说成已单独做第二个验证器核验。旧入口“两来源派生固定策略”应按这段理解：两个名字各自有多个候选H配同一个L，而不是总共两个LP或各名字只有一张高树。

## 固定策略锥和全部客户类型

p为主题数，m为玩家数，变量w_b遍历全部非空兴趣mask b=1,…,2^p−1，包含原输入没有的类型。空兴趣客户不贡献任何目标/IC，省略；零权重类型允许。LP重新选择整个客户向量，原example仅供挑策略、m/p/标签，**输出weights不是原输入客户表**。

对固定H或L，`path(actions,h)`在当前有序h沿原actions补至无键叶。生成器给完整树时这恰为真实续局；path函数本身没有m深度/完整键验证，不能拿它独立验证任意坏actions。第i人在真叶z的单位mask利润系数为

\[
r_b(z,i)=\frac{\mathbf1\{z_i\in b\}}{\sum_j\mathbf1\{z_j\in b\}},
\]

分子0时直接返回0，当前覆盖时分母正。每个深度k的全部p^k有序历史、除规定动作外p−1个合法当前行动，加入IC系数r_b(规定真叶,k)−r_b(偏离真叶,k)。**根IC也保留，双方完整树均保留**，不是root-only删除根的四锥程序。

每个profile有(p−1)Σₖ₌₀ᵐ⁻¹p^k原始比较行，不去重，零行和相同行保留。八客户来源m3/p4每profile63行、每对126；根税来源m4/p6每profile1295行、每对2590。它们是代码结构解析计数，不是本包新IC通过数或实际总LP数量。没有把两份策略相同行合并后少计，也不加self行。

A=−ICrows的float数组，所有行A w≤0；w≥0，Σ_b w_b=1。人数m与p个目录标签保持原值，客户重数及兴趣支持则全放开。m3/p4用15个非空mask变量，m4/p6用63个。归一的是客户总质量，而非W_H=1；高福利可低于1。

## 比较支持与LP的目标方向

每个固定H/L对，枚举大小s=1,…,min(p,m)的所有**不同主题支持**S，覆盖行o_b(S)=1{b与S相交}，高福利行c_b(H)=1{b被high_path覆盖}，高低根利润行分别hr/lr。最大化

\[
J_S(w)=\sum_b[3(hr_b-lr_b)-2c_b+o_b(S)]w_b
=3(h-\ell)-2W_H+|\cup S|.\tag{OBJ}
\]

所有支持是合法≤m主题比较，补重复槽不改覆盖。每H的支持数在m3/p4为4+6+4=14，m4/p6为6+15+20+15=56；实际H数/失败LP数未存，不能把14/56或乘某猜测策略数当原运行次数。

不必在LP里另最大化真实OPT：任意支持覆盖≤OPT_m，若某个J_S>0且有理w确非负、两profile全IC有效，则真实3(h−ell)−2W_H+OPT也>0。反之，一个支持的负点不是同实例最优覆盖下仍负的证明；没有对所有支持/策略锥的精确对偶，数值最优非正也不证一般候选。源码既没加新h−ell>0约束，也未重求新M；旧按原h>M_orig挑策略不能在新权重下替代这些条件。

## 浮点发现、有理原始点与写出合同

`linprog`用method highs、最大化目标取负送入，A_eq一行全1、b_eq1、非负bounds；返回success为false则跳过。每成功数值value=−res.fun，只有best为空或value>best.float_objective+1e−9才更新。这个容差是发现/记录阈值，**不是精确最优认证**；比旧best略好但差≤1e−9的点不会被有理检查，不能把最终best说成全部求解的无容差最大值。

只有更新时才逐坐标`Fraction(float(x)).limit_denominator(100000)`。源码不再归一、不检查有理权重的和或非负性；从浮点非负约束而来的提案必须在将来证书化时确认真正w≥0。所有IC与目标都是齐次，若有理w≥0且总量>0，即便舍入后和不等1，清分母仍得有限不同单位客户；不能因没重归一就宣称原始点必坏，也不能只信float success。

`min_exact_ic`是该固定L/H**全部原有理IC行**点积最小值；exact_objective是(OBJ)系数与舍入w的Fraction点积。它只在记录此提案，不是有理最优目标/对偶。若exact_ic≥0且obj>0，写固定`insurance_pair_candidate.json`并立即return（不再写按名字报告）。否则继续，最终写`insurance_pair_<name>.json`为best，若从无成功LP则可写null。所有输出固定覆盖；早期候选返回可能留下旧按名报告。每次best更新会print一条紧凑JSON并flush，但没有保存完整stdout/argv/solver版本/耗时/退出码/输入及代码hash。

报告不存low/high完整actions、IC逐行松弛、总cases/LP/失败数量、对偶乘子、原M或重权后的h/ell/W/OPT。因此两文件能保留精确原始点，但单个min_exact_ic字符串不能让本包独立重验两棵SPE，或认证所有其它LP的上界。原入口/LP/solver/IC均不重跑，未制作虚构新日志。

## 两份原报告的全部字段

每个原JSON恰八键，下表逐个完整保存；weights所有非零mask另表展开，未列的mask权重为0（源码省略零项）。原float字面值与Fraction字符串均保留，不把float换成有理最优性证书。

|字段|eight_cce_welfare_gap原报告|root_tax_failure原报告|
|---|---|---|
|float_objective|-0.19999999999999996|-0.043478260869565244|
|exact_objective|-1/5|-1/23|
|min_exact_ic|0|0|
|high_path|1,2,3|5,0,0,0|
|low_path|0,1,1|2,0,0,4|
|comparison|0,1,2|0,1,2,3|
|weights|下表全部4项|下表全部9项|
|source|eight_cce_welfare_gap|root_tax_failure|

|source|mask|全部喜欢标签（零基）|原weight字符串|
|---|---:|---|---|
|eight_cce_welfare_gap|1|0|1/5|
|eight_cce_welfare_gap|2|1|2/5|
|eight_cce_welfare_gap|4|2|1/5|
|eight_cce_welfare_gap|8|3|1/5|
|root_tax_failure|1|0|10/23|
|root_tax_failure|2|1|7/69|
|root_tax_failure|4|2|5/69|
|root_tax_failure|8|3|7/69|
|root_tax_failure|20|2,4|2/69|
|root_tax_failure|36|2,5|2/69|
|root_tax_failure|50|1,4,5|2/23|
|root_tax_failure|52|2,4,5|4/69|
|root_tax_failure|56|3,4,5|2/23|

## 有理点自身的自足算术，不冒新SPE认证

下面只按已读路径/权重手工展开单位份额与覆盖，解释两个存储exact_objective。它不调用原LP/solver，不重算两棵完整树全部IC；报道的min_exact_ic=0仍按原记录身份保存。

**四标签点。** 仅单例mask1/2/4/8，权重依标签为(1,2,1,1)/5，总1。H=123时根标签1得h=2/5，覆盖W_H=4/5；L=011时根0单占得ell=1/5。比较012覆盖4/5，也等真正OPT₃：任取三标签至多覆盖最大的2/5与两个1/5。故

\[
3(h-\ell)-2W_H+OPT_3=3/5-8/5+4/5=-1/5.
\]

清分母5是5名单位客户的新点，非原例8名客户。这个点的δ=h−ell=1/5>0、D=4/5，D−3δ=1/5>0，没有击穿候选；不据此证明整个三人四主题策略锥最优。

**六标签点。** 把原权重统一为分母69，非零mask及分子是

\[
(1,2,4,8,20,36,50,52,56):
(30,7,5,7,2,2,6,4,6),
\]

总分子69。标签0..5按源名A..F。H=FAAA：根F覆盖CF、BEF、CEF、DEF，共18/69，三名A共享A私有30/69，所以h=18/69、W_H=48/69。L=CAAE：根C份额为C私有5、CE的1、CF的2、CEF的2，共ell=10/69。比较ABCD覆盖所有九类，故其覆盖及真正OPT₄均为69/69=1。于是

\[
3(h-\ell)-2W_H+OPT_4=(24-96+69)/69=-1/23.
\]

这里δ=8/69>0，D=(96−69)/69=27/69=9/23，3δ=24/69=8/23，缺口1/23。清分母69给69名单位客户；原root_tax输入是61名，不能把新w点的W_H48/69与原例实际W38等混用。两点w均恰非负且和1，这是表本身的有理事实，不替代其它未存提案的非负性检查，也不是本次新运行验证。

## 全仓比较、当前未决与逐源去向

本程序保两份策略的**根**IC并最大化保险pair目标，与[根修复有限锥](../资源/根修复有限判别与全深度工作区的接续边界--资源.md)删除单个root、以Δ≥最大根偏离并攻击O−3Δ的合同不同；四锥旧原始/对偶严格吻合及7/4等值不能移来认证本两个负点。

[三倍根修复定理](../定理/多主题独立保险的三倍根修复与半覆盖等价--定理.md)的通用构造和固定m的half⇔root-regret上界已有完整解析证明，本有限LP阴性不证该等价右端。当前一般交叠/根后联动的有效幅度界仍按自己的真正菜单量词接续；本单low、去重high固定锥既非全部完整策略，也未给对偶。原README说“没找到正目标、随后停止扩样转全深度编译”只保历史研究顺序，不视作再次执行授权或停止当前清洗。

三primary均retained到本程序页与[原字节/依赖/比较证据](../../tools/evidence/insurance-pair-fixed-cones-and-rational-proposals-primary/README.md)。六相关源全文与五正式对象/一旧MD均闭包保全，不额外done，不因导入工具属于已有来源就重复处置。11WQ原全11ID claim pushed/raw synced保留，本包仅核本3subset Boss4/sourceSHA，未Git/claim/done/外发。没有新数学程序、盲审、外审、最优性或新颖性认证；只有源理解、有理点定义级算术和准确证据边界。
