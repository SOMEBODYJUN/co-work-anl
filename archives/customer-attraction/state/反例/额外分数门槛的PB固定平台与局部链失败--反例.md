---
id: customer-attraction/pb-extra-fractional-fixed-plateau-and-local-chain-failure
kind: counterexample
type_tag: 反例
title: 额外分数门槛的PB固定平台与局部链失败
status: exact-arbitrary-legal-background-local-helper-refuted; aggregate-survives-on-this-instance
summary: 旧PB完整子SPE在竞争质量r的额外分数门槛上给δ_(r+1)(b)=δ_r(b+F)>u，局部链失败但全部r人利润仍大于rδ；全目录KKT与singletons、子混合及根可达性边界完整保留。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round11/aggregate/extra_fractional_local_plateau.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round11/aggregate/check_extra_fractional_plateau.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round11/aggregate/extra_fractional_plateau_check.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round11/parent/extra_local_scalar_independent.json
---

# 精确域：静态分数背景与真实子SPE分开

采用有限单位客户、有限非空共同目录和全部有序历史完整纯SPE模型，允许空主题、重复行动、同覆盖标签、零客户及任意平局。固定合法旧历史的客户负载b。为消除原稿δ下标歧义，定义
\[
 \mathcal K_s=s\operatorname{conv}\{\mathbf1_A:A\in\mathcal S\},
 \quad \delta_{s+1}(b)=\min_{z\in\mathcal K_s}
       \max_{T\in\mathcal S}\sum_{x\in T}\frac1{b_x+1+z_x}. \tag{DEF}
\]
下标s+1表示**静态竞争质量s**，查询者另有自身一份；不是s+1名顺序玩家，也不是随机整数背景的倒数期望。它就是[自由分数门槛](../定义/自由分数背景安全门槛--定义.md)的t_{s+1}。r名真实剩余玩家的extra门槛是δ_(r+1)，竞争质量r。

本源否定的局部助手量化**任意合法背景及其完整子SPE**：当前实际动作S、收益u应满足
\[
 u+(r-1)\delta_r(b+\mathbf1_S)\ \stackrel?\ge\ r\delta_{r+1}(b).
 \tag{EXTRA-LOCAL}
\]
若在某份策略全部实际节点都成立，它会沿同一条实际路径望远镜：势为rδ_(r+1)(b)，下一项为(r−1)δ_r(b+S)，末端剩余人数0的势定为0。因此根会有W≥mδ_(m+1)(0)，与静态OPT_m≤2mδ_(m+1)(0)一起给half。**本反例只否任意合法背景的全称版本**；下文这个精确背景不能成为原根实际SPE前缀，故不能拿它反驳只限原根实际节点的版本。

# 复用的PB输入与全历史身份

不是新游戏。使用已证[PB完整子SPE](任意合法背景的前两人额外槽安全值--反例.md)，参数
\[
 k=3,\ d=20,\ q=12,\ t=10,\ r=2475,\ Q=2063,
 \ H=100000,\ M=10^9.
\]
客户分20段。每段Q个真实R块，各12位不同单位客户；另两个dummy D块，各Hq=1200000位单位客户。regular主题在每段选ℓ∈{1,2,3}个不同R块和前3−ℓ个D块；各段选择完全Cartesian。再加所有客户的singleton。共48495120位不同单位客户，原价值/均分规则未变。

每个R块11位客户背景M、1位背景M+1；每个D客户背景HM。重复合法singleton有限次可实现b，且b已覆盖全部客户。记正有理函数
\[
 f(c)=\frac{11}{M+c}+\frac1{M+c+1},
 \qquad g(c)=\frac{1200000}{HM+c}.
\]
F在每段取固定R块1,2,3，无D。原完整策略无偏离时前三人F；之后Greedy每段取一个最低负载R和两个D。第一次早期regular偏离会触发至多180次Punish：每次在一个未达10的目标段加偏离者热点，其余段用空R，且取两个D；第二次偏离或处罚结束后永久Greedy。Greedy平局先照顾最近偏离者所选块，再按最近使用者，最后固定标签。首次singleton后的每棵互不交子树另用有限逆向归纳的完整SPE补齐。

该完整有序历史身份由已读PB正式证明与[四份审查读序](../审查/PB背景反例的全历史审查与版本--审查.md)承担，不靠本源的9个标量布尔值：Greedy任意水位证明付单块/多块偏离，G/P/F三个严格比较付各模式，regular在任意真实后继下收益大于singleton，允许整块结构破坏后的子树补齐。遵循Punish所用后继人数上界与偏离后下界分别正确；不能把旧Copy尾冻结。当前没有重新展开巨量客户或策略树。

实际前三人均得u=3df(3)。2472个Greedy动作先填2060个空R块，再将其中412个升到2，不碰原F的三个3负载热点。整个后文只重用这份已经证明的完整子SPE，不改变离轨平局。

# 竞争质量r的精确鞍点：包括singleton目录

置
\[
 L=3r/Q=7425/2063\quad(1<L<4),
 \quad a=f(1+L),\quad h=g(1),
 \quad\Delta_+=d(a+2h).
\]
查询p在每段均匀取一个R块和两个D；背景分布q在每段均匀取三个不同R块、无D。各段独立组合仍是合法regular主题。竞争质量r乘q的边际给每个R块负载L，每个D客户负载0。于是R整块查询价a，D块价h。

因为
\[
 a<\frac{12}{M+1+L}<\frac{12}{M+1/H}=h,
\]
任一regular查询在每段ℓa+(3−ℓ)h，以ℓ=1最大。singleton查询不超过1/(M+1)，而Δ_+>2dh>1/(M+1)。所以q给全目录上界δ_(r+1)(b)≤Δ_+，不能只检查regular主题就省略singleton。

为核全局下界，固定同一p，F_p(z)=Σ_xρ_x/(b_x+1+z_x)为凸函数。每个R块在负梯度中贡献
\[
 H_R=\frac1Q\left[\frac{11}{(M+1+L)^2}
                         +\frac1{(M+2+L)^2}\right],
 \quad H_D=\frac{1200000}{(HM+1)^2}
\]
是每D块贡献。这里R查询边际是1/Q、D是1。原程序断H_R>H_D；该正性也可直接看出，无浮点容差：M>6、L<4，故
\[
 H_R>\frac{12}{Q(M+6)^2}>\frac{12}{4QM^2}
       >\frac{12}{HM^2}>H_D
\]
（H=100000>4Q=8252）。每个regular背景主题最大线性负梯度为3dH_R，恰在各段ℓ=3的q支持上达到。任何R-singleton的贡献≤1/[Q(M+1+L)^2]<3dH_R；任何D-singleton的贡献1/(HM+1)^2也严格小于3dH_R，因为H_R>H_D。原代码的singleton_gradient正是这两类最大值的联合比较。

因此q支持最大化该负梯度，凸一阶条件给其负载全局最小化F_p，且值F_p=Δ_+。任何别的竞争负载z有max_T查询价≥F_p(z)≥Δ_+。结合前面的全目录上界，得到真正静态minimax证书
\[
 \boxed{\delta_{r+1}(b)=\Delta_+.}              \tag{ROOT-STATIC}
\]
这是一份合法查询/竞争分布，不假定SPE实现静态分数承诺；也不把整数静态安全值v_(r+1)与δ_(r+1)置等。

# 子背景恰恢复相同的全部分母

先实际选F，再给静态子竞争者总质量r−1。每段三个热点已多背景1，期望后续负载需要热点L−1、外部R块L。令
\[
 \theta=\frac{3(L-1)}{r-1}=8043/2551931\in(0,1).
\]
在每段以概率θ取一个均匀热点和两个不同均匀外部R块；以概率1−θ取三个不同均匀外部R块。总是ℓ=3、无D，是原目录合法动作；Q−3=2060足够。完全Cartesian给整主题分布。各热点及外部边际分别满足
\[
 1+(r-1)\theta/3=L,
 \qquad (r-1)(3-\theta)/(Q-3)=L.
\]
第二式由QL=3r直接化简。于是子背景b+F加其竞争负载与(ROOT-STATIC)的b加负载逐客户相同，所有查询分母都恢复，子值≤Δ_+。

反向是合法前缀嵌入：1_F加任意r−1份分数目录负载属于r份分数目录负载，故对子域取min只能较大，δ_r(b+F)≥δ_(r+1)(b)。得
\[
 \boxed{\delta_r(b+F)=\delta_{r+1}(b)=\Delta_+.} \tag{PLATEAU}
\]
此处子竞争质量是r−1；原稿所引先前标准分数平台使用3(r−1)/Q，不能沿用那个负载而忘掉extra索引。本页root负载始终3r/Q，原PB整数安全下界s的Jensen式同样使用3r/Q。

# 局部确实失败，全r人聚合在同例仍为正

原PB查询下界为s=d[f(1+L)+2g(r+1)]>u。g严格递减，故Δ_+>s>u。由(PLATEAU)，(EXTRA-LOCAL)左减右精确为u−Δ_+<0，两份原报告完整保存同一个有理数：
\[
 u-\Delta_+=-
 \frac{2650802775393752098848146156885170657595}
 {2418164246133683536467300136600764904723600072166563356}.
\]
这是旧PB的静态索引推论，不是新全历史构造。

另一方面，U是**剩余r玩家的利润总和**，不是含已走旧玩家的覆盖福利。每段前三F的R总份额9f(3)；随后1648个R块一人用、412个R块两人用，共1648f(1)+824f(2)；两个D块各被2472人用，给4944g(2472)。因此
\[
 U=d[9f(3)+1648f(1)+824f(2)+4944g(2472)].
\]
把上面固定参数代入的精确差为
\[
 U-r\Delta_+=
 \frac{37931603069518962951597320888331420013681724109394305258011476365542645}
 {19912419741830972497105030928065975446562337451885019926043244867711247019506545556}>0.
\]
正分子/正分母和明确有理公式给固定点正性，不从报告中一个true推广一般定理。它只说明本例后继可共同补偿早期债务；没有反驳、也没有证明任意合法背景的聚合U≥rδ_(r+1)(b)。该差原报告身份及两实现边界见[计算对象](../计算/额外分数平台原标量与父方报告的证据边界--计算.md)。本批没有执行上述标量程序。

# 根可达性及与其他平台的区别

原稿写b“未必在根实际路径”。现有更强[实际前缀关联预算审查](../审查/实际前缀的关联预算与PB背景可达性复核--审查.md)对原目录、精确b和余2475位已排除所有合法实现成为实际SPE前缀：R总关联I=495120000041260、β=M+1、D最低背景B=HM，取α=1、a=q=240，有aB>I及qB>β+I+r+1。最后D-singleton可在任意真后继下严格偏离到regular主题。这个后续结论不改变合法离轨子SPE；变目录、背景或人数必须重新核条件。

b本就覆盖全部客户，若只把这背景放进整个原游戏，覆盖福利已OPT；U只计剩余利润，不能拿它和全覆盖W混算。因此本结果不反根half，不是恰六人反例，也没有排除跨节点信用或实际根路径的局部弱化。

[五客户全B平台](合法背景安全值平台的局部斜率障碍--反例.md)是另一输入：11主题、余4人、整数安全v4=v3、长5B旧前缀。这里是48495120客户、2475人、自由分数额外质量δ_(r+1)=δ_r。二者都显示局部平台可有当前亏损及总聚合补偿，但不得把各自输入、r槽/分数槽或程序成功互相替代。

2971B原稿、1203B代码、两完整报告及2348B入口都实际normal全文。原稿引用同行`pb_fractional_saddle_plateau.md`作为先前出处，本批未声称新取或全文读那个raw文件；本页直接用已读PB正式定理、自由分数定义及原稿给出的全部数据重构上述静态证明。没有新程序、旧参数扫描、全树枚举、盲审、外审或新颖性认证。来源和精确全26claim/恢复证据见[本批证据](../../tools/evidence/round11-extra-fractional-plateau-primary/README.md)。
