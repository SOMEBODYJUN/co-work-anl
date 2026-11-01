---
id: customer-attraction/bank-upgrade-original-half-single-policy-and-round-ten-read-order
kind: resource
type_tag: 资源
title: 重复银行原HALF单策略构造与第十轮读序
status: 三primary570044B全文实读；源seed/整bankσ/38型和README时序闭合，0本次原入口/BI/LP
summary: 参数化重复银行+AAB只供每次需BI的策略种子；m5固定默认极小续局策略的全255型重数LP只交精确原始点，38端点唯一最优J不授对偶上界。README较早弱版OPEN由同页置顶全人数族更新，LAST压力严格必要条件与有限报告身份分开。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/credible/bank_upgrade_attempt.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/credible/bank_upgrade_attempt_m5.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/credible/README.md
---

# 原三件的实际范围

4211B程序、561628B完整JSON及4205B README共570044B均核size/SHA/blob。bank JSON是此前Root成功normal show的同SHA原字节精确复用，不虚称本次新show；此前只消费endpoint/path/J的related阅读，**本批才全文读完**旧source、全部source/endpoint利润、全38型/255克隆及完整4681处方。[完整输入及全部有序策略表](../计算/银行端点的完整五人策略与三十八型数据--计算.md)给自足数学数据。两篇正文承担数学，收据或原日志不替证明。

本轮0原入口、导入、BI、LP、MILP、扫描或新IC checker。没有找到/制造本批原生exit/argv事件；historical exact_primal与代码接受断言按其证据层保。后继59型StrongA原5026此前恰一次真实成功只属于那份输入，不能借给本38型或旧seed。0Git/start/claim/done/network/凭据，Root串行发布。

# 模型与参数化seed的准确合同

有限共同目录、不同单位客户、m个单位顺序行动者，策略对全部有序历史规定动作。兴趣型I重数n_I，终局x上c_I(x)=Σ_j1_(x_j∈I)，利润u_i(x)=Σ_(I:x_i∈I)n_I/c_I(x)，福利W(x)=Σ_(c_I(x)>0)n_I，OPT=max_(y∈目录^m)W(y)。不覆盖项不作分母；保空主题、重复行动、零客户和全部平局。实数重数只作优化辅助，最终须清分母成不同单位客户；不是加权行动者或私人目录。

original_seed(m)按整数m≥4使用（小于4直接ValueError），设p=m+3，标签0…p−1；正重数仅
\[
n_{\{0\}}=4,\ n_{\{1\}}=4,\ n_{\{2\}}=2,\ n_{\{2,3\}}=2,\ n_{\{2,4\}}=2,
\quad n_{\{0,3,4\}}=6,\ n_{\{1,3,4\}}=2,\ n_{\{5\}}=5(m-3).
\]
其余所有非空兴趣型为零。候选path=5重复m−3次，再0,0,1；比较J=(2,3,4,6,7,…,p−1)恰m个不同标签。程序逐输入先检查目标计数q∈R(0)，不成立就只返回seed_target_not_credible；只有成立才调用certificate(q,on_path=path)并canonical完整核验。存在名义参数m、padding形式或某次m5成功，都没有证明任意m此目标可信。

仅从seed叶可直接算：银行m−3角色均得5，随后为5,5,6；W=5m+1、总客户N=5m+7。四个主题0,1,2,5已覆盖全宇宙，m≥4可重复补到m槽，所以OPT=N；J在此seed只覆盖14。以上是叶/覆盖算术，**不证明这条叶对所有m有SPE实现**。默认main恰调用attempt(5)，没有参数CLI扫描或其它m报告；当前实例m5/W26/OPT32/J23467不能外推成通式认证。

原seed的6…p−1都是空覆盖标签；m5时6/7是两个重复空标签，属于可区分标签软件扩展域。集合目录中重复空集合须识别，不能把名义p当p个不同覆盖。完整m5表的规定动作从不取6/7，若使用原8标签seed的SPE合同，删除这两标签并限制历史给六非空互异覆盖SPE，逐节点原偏离完成叶保留。最终38型端点有私有6/7、八覆盖两两不同，不需要靠辅助seed重复空标签扩展才合法。

# 默认证书：完整BI终局集合不等于全策略枚举

设R(k)为计数k后所有完整纯子SPE终局计数集合，u_a(q)=Σ_(I:a∈I)n_I/Σ_(b∈I)q_b。分子非零时q_a>0，分母正。终局R(k)={k}，并令
\[
\ell_a(k)=\min_{d\in R(k+e_a)}u_a(d),\quad M(k)=\max_a\ell_a(k),\quad
R(k)=\bigcup_a\{q\in R(k+e_a):u_a(q)\ge M(k)\}.
\]
任一真实SPE当前利润必须≥各孩子最小值；反向给偏离孩子选最小值子SPE，当前选达到门槛的动作，即可拼出目标q。完整[可信菜单算法](../算法/可信续局菜单与完整策略重构--算法.md)已证明该集合递推，包括零收益/任意平局。

这里certificate没有传选择callback：沿指定path前缀强制path下一动作并核可行；其它历史取admissible中最小标签。规定孩子继续desired；每个其它b只在argmin_(d∈R(k+e_b))u_b(d)中取**终局计数字典序最小者**。递归基例核目标一致，动作键保原h；同计数历史不合并动作，终局缓存不改变完整IC域。按子树归纳，选中的真实孩子均SPE且偏离收益≤当前收益，故构造合法。

该默认规则足够实现每个可信终局，却没有覆盖同终局的所有完整动作图。bank只取一份固定图σ_B，不是均匀抽完整策略、求最差福利终局或全sigma扫描。后继repeated改用全部可信菜单，在合法上限内优先异题拥挤，不是此处argmin规则；二者实际553处方不同，不能用相同path/counts把新旧合并成同σ。

# 固定bank图的全型重数LP与精确接受

对完整图σ_B，令z_σ(h,a)为在h强制a再跟原σ到终局，i=|h|+1。每型系数定义
\[
\sum_I\Gamma_{h,a,I}r_I=u_i(z_\sigma(h,\sigma(h)))-u_i(z_\sigma(h,a)).
\]
所以使该固定σ成为SPE的重数恰r≥0、Γr≥0；每个有序历史及真实偏离都在内，非只在轨、固定后继或静态PNE。自身/全零行与完全重复的有理行可去除。m5p8原报告4681节点、32767非自身比较去重为3078个不同非零IC行，255列是全部非空客户兴趣型，不是只让seed原八型重权。

设actual计数q固定，w_I=1_(Σ_(a∈I)q_a>0)，v^J_I=1_(I∩J≠∅)。helper.optimize(J)解
\[
\max v^Jr\quad\text{s.t. }r\ge0,\ \Gamma r\ge0,\ wr=1.
\]
这归一化的是实际福利W，不是总客户质量Σr，也没有把J预设为所有输入最优。全型自由是同σ内，不是同时改变动作图。[完整锥定理](../定理/固定完整策略的客户重数锥--定理.md)给其精确含义和同覆盖标签的边界。

float解先逐坐标limit_denominator(10⁷)，再用Fraction精确验Γ/非负/W1；不通过才取浮点正支持>10⁻⁸及近紧IC行误差<10⁻⁷作有理消元恢复，恢复后仍完整精确复查。integer_clones以分母LCM放大、除公共gcd；全为零不可能满足W1。程序再以直接Fraction逐历史/逐替代比利润及canonical verifier两路完整验收；direct路独立于canonical，但共享helper按同σ造的终局缓存，不是完全独立树重建或盲审。

只有这些断言通过，才写整数endpoint、全255克隆、完整strategy、五利润/W/OPT/ratio和refutes_HALF。外部helper导入NumPy/SciPy，canonical四文件及helper20567B按真实原source-root布局保留、同SHA全文上下文复用；本轮没有import、环境安装/测试、selftest、helper扫描或它main中的Git元数据命令。

精确对偶须有μ≥0、βw−Γᵀμ≥v^J逐255列成立；helper另检查β≥0。只有成立才给dual_bound，且β=v^Jr才dual_optimal。原38报告null/false/[]，因此只是按原接受代码交付的精确可行原始声明，没有精确上界，不把HiGHS成功或exact_primal冒锥最优。38表每型touch J并由私有2/3/6/7及04∩45迫唯一最优J，使此点OPT/W恰原目标321176/229141；没有把这个点上的事实扩成全部锥或任意目录上界。

# README的先后段与各个数学对象

4205B README不是独立证书实现。它先置顶更新：“existential最优元组/指派版本也已被root全人数族否定”，正文末仍保早阶段“弱版OPEN”；当前必须读置顶更新，后者只历史，原冻结JSON不改。同页讲原HALF及较宽弱K未由此否定，不能只取旧OPEN也不能把相邻预算失败扩成这些不同命题。

准确分层如下：

| 对象 | 当前本3可据的身份 |
|---|---|
|bank38与repeated42两个原HALF端点|321176/229141、63464208590/44924837031均<2，仅不同固定策略的有限原始点，无普遍正面界|
|59型StrongA|同σ_R另一次有符号目标重权，正差2714689114258275/归一化3143/835942；旧raw、5026一次真实核验及tree全矩阵另已完整封包，不是本次再run|
|compact三人十客户|真实完整SPE有Q11−W9−C1=1；最小最优匹配(D,D,A)给Q6，弱版差−4，不能因某个坏最优排列反所有/存在量词|
|同59型的最优指派|有便宜840最优tuple；后tree解析更得**全部**最优指派都在相邻预算内，StrongA与每query加强失败不传存在弱版|
|后继全人数族|[唯一最优支持反族](../反例/唯一最优支持下相邻钱包的固定倍数反族--反例.md)在m≥7反存在最优相邻预算及任意固定倍数；m6边界等号，非六人half反例|

compact细节已有[十客户正式反例](../反例/十客户重复实际行的相邻钱包失败--反例.md)；原发现链见[发现/简化实现](反复异题拥挤重构与StrongA发现简化的原实现合同--资源.md)；59型全部最优指派的窄解析见[tree全矩阵资源](五人相邻钱包原证书的tree全矩阵独审与最优选择界--资源.md)。这些已有充分全读/实际证据不再扫大包或重复入口，本三不重认新StrongA。

## last-profit段是必要条件压力，不是一般付款

README另报告last_profit_pressure：原bank锥某精确点比率223145/161892、必要行等号；refitted锥某输出HiGHS Unknown/primal Infeasible，不称精确不可行。本三**仅全文读了README这段**，未新取/读那份3209代码、558504整数点或459失败JSON；不能冒这些原件的SHA绑定或独立数值审计，后续自然三源可单独闭合。

其数学语境可自足核清：任意真实完整SPE末位对前m−1行动的插入价g(T)=Σ_(x∈T)1/(1+L_x)全列最佳回复，故g(T)≤u_m。取最优m槽负载d，对每客户有1_(d_x>0)≤(d_x+L_x)/(1+L_x)。求和≤m u_m+(m−1)u_m=(2m−1)u_m，所以OPT≤(2m−1)u_m。若真half坏OPT>2W，则必须**严格**(2m−1)u_m>2W。压力LP若仅加≥2W是坏点必要条件的闭包放松；等号可筛掉真坏点而非认证坏点。这个[LAST既有引理](../引理/可信相邻换位与固定计数坏点正常形--引理.md)不控制共同跨枝付款，不由浮点不可行补全全σ证明。

# 本批保存和边界

全部3主源、5必要代码依赖、可逆两视图、553处方字面差、size/SHA/blob、normal捕获、actual19WY fullclaim及独立同步保全完整保。3逐源收据及自查反映本批才全读bank；旧发现5中“当时只needed-field reading”保持其历史范围，不静默改旧冻件。

19WY实际claim已pushed41c2e223127cbe5c48fcaa1f571cbb10fac8f45a，raw local_sync原needs-attention；另38untracked/2tracked同字节、missing/different/unmerged为空且stash保留，二者并列，不伪synced。源码main有guard且拒覆盖同名输出；未用README的历史“无git”当当前执行证据。原主目标全人数状态/当前六人前沿/五人别证、程序有限点及作者自述先验分别保留；没有外审、新颖性或普遍HALF成功认证。
