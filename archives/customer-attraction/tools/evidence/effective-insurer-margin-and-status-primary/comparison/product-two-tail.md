---
id: "customer-attraction/arbitrary-background-two-tail-product-threshold-and-credible-filter"
kind: "theorem"
type_tag: "定理"
title: "任意背景两尾产品门槛与可信叶过滤"
status: "proved-exact-two-tail-product-filter-with-explicit-L-nonadditivity"
summary: "任意整数背景/任意有限分量，末位BR和倒二最低门槛精确分解，完整SPE叶只需总倒二收益过滤；五客户双副本L=5/2<3并给不依原JSON的完整策略解析构造。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/dynamic_matching/README.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/dynamic_matching/README.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/harmonic_debt/product_transfer_independent_review.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/harmonic_debt/product_transfer_independent_review.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/independent_attack/product_transfer_independent_review.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/independent_attack/product_transfer_independent_review.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/source_reset/product_independent_review.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/source_reset/product_independent_review.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/dynamic_matching/product_transfer_lemma.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/dynamic_matching/product_transfer_lemma.md"]
source_ids: ["9826517b238bcb4e1b77", "2a7fefaf181c46e608ea", "cb41970a61296e3fa636", "34b184d5d1a61f83fc40", "30e8d20848c6519f641f"]
review_status: "五MD全文/原SHA与已有完整产品对象比较；原三独审实际section范围另保，知情重构不是新blind/原审计重演"
truth_status: "明示产品过滤/闭包/有限条件放大/同质对角边界已证；未提供SM严格种子或half反例，六人未解"
---

# 模型与两个尚未行动者

取[共同目录模型](../定义/共同目录完整历史模型--定义.md)有限正个q分量，单位客户集不交，有限非空目录S_k，共同玩家次序相同，联合目录为完整×S_k。固定合法有序过去，在分量k客户x有整数旧负载β_x≥0，仅剩p、p+1两位单位玩家。下式也定义任意外给非负整数β的两人辅助游戏；原模型应用只用合法固定过去。允许空主题、零客户、重复和任意历史依赖平局，分母β+1始终正。

\[
U_k(a,b)=\sum_{x\in a}\frac1{\beta_x+1+1_{x\in b}},\quad
V_k(a,b)=\sum_{x\in b}\frac1{\beta_x+1+1_{x\in a}}.
\]

BR_k(a)=argmax_b V_k(a,b)，λ_k(a)=min_(b∈BR_k(a))U_k(a,b)，θ_k=max_aλ_k(a)。θ保留末位最优性后倒二的最低可信门槛，不是任意尾部min_b保底、静态minimax或固定末位策略的最佳行动值。

# 精确分解与当且仅当FILTER

固定倒二向量a，末位总收益ΣV_k。完整Cartesian允许单改任一坐标，故末位BR**必须且只需**各坐标BR：BR_prod(a)=×BR_k(a_k)。因此λ_prod(a)=Σλ_k(a_k)，θ_prod=Σθ_k；有限性保证所有argmin/max达到。

候选向量叶(a,b)可成为这两人子博弈一份完整纯SPE的结果，当且仅当

\[
b\in\prod_kBR_k(a_k),\qquad
\sum_kU_k(a_k,b_k)\ge\sum_k\theta_k.\tag{FILTER}
\]

必要：末位必须BR；倒二可改成逐坐标达到max λ的向量，任一真实末位BR都付至少Σθ。充分：在选定a孩子用给定b；每个其他a′独立选择使U_k达到λ_k(a′_k)的末位BR，给其收益≤Σθ，不超过规定叶。各有序孩子均填末位BR，故全两层树可信，不把相同负载不同历史合并。坐标叶可以有U_k<θ_k，由别的坐标盈余支付；其坐标投影未必SPE。

已有[三人笛卡尔精确菜单](三人笛卡尔可信菜单与根门槛凸化极限--定理.md)在三人/首行动后给同一过滤。本源source_reset明确保**任意已有整数背景、任意有限分量数、恰两剩余**的公式，归位为该接口的背景版本；不是声称任意长后缀θ都可加。一般全m只有[产品上界](../资料/全续局产品转移与全部最优元组攻击--资料.md)。

# 五客户单组件与双副本：精确L而非一个上界叶

三人单组件主题A,B,C，五名不同单位客户兴趣B、AB、C、AC、AC。强制首B，余两人的全部末位BR叶为：

|第二行动|末位BR|首收益d|第二收益v|
|---|---|---:|---:|
|A|C|3/2|3/2|
|B|C|1|1|
|C|A|3/2|2|
|C|C|2|3/2|

各第二行动最低可信收益(3/2,1,3/2)，θ=3/2。FILTER删第二行，其他三行可实现，所以L₁(B)=3/2。全部四行满足d≥v/2+1/2；第二/第三行各半混合有Ev3/2、Ed5/4并达到该共同下界，故单步barL₁(B)=5/4。

两个客户不交副本、九向量主题，强制首BB后末位BR叶恰4²=16对，FILTER只保v₁+v₂≥3的11对。任一可行叶有d₁+d₂≥(v₁+v₂)/2+1≥5/2。取第二/第三行组合，即完整叶(BB,BC,CA)，收益(5/2,3,9/2)，达到下界。因此

\[
L^{prod}_1(BB)=5/2<3=2L_1(B).
\]

这是对“全部可信续局极小L可加”的严格反例，不反指定坐标策略的收益相加，不反SM或half。人数仍三，客户只是十个不同单位，不是分数玩家或混合策略。

# 本次知情解析补全整棵根策略

原MD报告原JSON有91节点/819含自身比较与actual(CC,AA,BB)。本批未读取或重跑原JSON/代码，另用FILTER给同一已知十客户输入的一份**明确递归完整策略**；不声称字面等于原91动作表，不称新游戏实例。为保证根补全，另按客户定义核单组件强制首A、C的全部末BR叶(d,v)：

- 首A：(A,C;7/6,7/6)、(B,C;3/2,3/2)、(C,B;3/2,2)，故θ(A)2、L₁(A)3/2（叶ACB）。
- 首C：(A,B;2,3/2)、(B,A;2,3/2)、(B,C;3/2,2)、(C,B;3/2,3/2)，故θ(C)3/2、L₁(C)3/2（可取CCB）。首B如上L₁(B)3/2（可取BAC）。

每行末位BR由V式在A/B/C三个主题直接比较；FILTER给L下界及达到叶，不是浮点min声明。

构造：根规定CC。该孩子规定第二AA、末BB，每坐标CAB，收益(4,3,3)；第二门槛3，故FILTER给全子SPE。根BB孩子规定第二BC、末CA，门槛3亦达，首收益5/2。其余七个根动作孩子，每坐标按首主题分别选达到L的ACB、BAC或CCB，再作产品，首收益3。所有选定孩子的其他第二行动向量都按FILTER充分性规则：末位逐坐标取其BR中使第二人收益最小者；选定第二行动采用所指定末位。用固定标签序打破需要的argmin平局即可给每个有序历史唯一动作。

末位在全部81历史为BR，第二位在全部9历史比较全部9联合动作均满足FILTER，根CC的4大于所有其他根收益≤3。此为完整1+9+81=91节点纯SPE的解析定义/证明，没有程序运行。actualW10，三主题A/B/C在每分量可全覆盖，OPT10；half余量10。选定BB离轨子博弈保最低L见证，不是一条无法扩展的孤立尾路径。

三原独立审计各有自身读取/计算scope，见[审查边界](../审查/产品可信最低收益的原始审查范围与后加边界--审查.md)。本次新的是知情解析完整policy构造（同旧输入），原数学CLI/JSON replay0，不冒新增独立审稿人或原运行成功次数。
