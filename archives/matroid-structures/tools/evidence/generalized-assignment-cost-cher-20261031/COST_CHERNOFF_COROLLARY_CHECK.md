# 成本保留Chernoff舍入：2026框架的直接推论核查

2026-10-20，状态：**LIKELY_STANDARD_COROLLARY_PENDING_CHECK**。这是一条应先淘汰假创新的查重路线，不是我们声称的新定理或对原公开问题已获认证的解决。若下述核查成立，GA-01无需作为独立选题。

来源：Swamy–Traub–Vargas Koch–Zenklusen，SOSA2026，*Unsplittable Cost Flows from Unweighted Error-Bounded Variants*，§2 Algorithm1及Theorem2.2。https://arxiv.org/html/2510.21287v1 ，https://doi.org/10.1137/1.9781611978964.42 。本次web：turn152view0。母问题为Rohwedder–Rouhani–Wennmann，ICALP2025 §4末段的cost-preserving matroid Chernoff rounding问题，https://arxiv.org/abs/2502.08267 ，web turn37view2。

## 拟推论的精确合同

M任意matroid，Q=P(M)为base polytope；x∈Q；c为任意有理线性cost；a_1,…,a_k∈[0,1]^E。希望随机多项式时间返回basis B，使每次成功输出c(B)≤c·x，以常数成功概率同时有

|a_r(B)−a_r·x|≤O(L+sqrt((a_r·x)L)), L=ceil(log_2(2k))。

不要求精确marginals；它与所有输出均cost≤c·x通常不相容。

## 自洽误差体消除均值依赖

设μ_r=a_r·x，s_r=L+sqrt(μ_r L)，r_r=K s_r，其中K为足够大的绝对常数。令

R={v: |a_r·v|≤r_r for all r}。

先解 min{c·y: y∈Q∩(x−R)}，得到y*。该LP可行且Q有界，所以最优值达到。对每r有ν_r=a_r·y*≤μ_r+r_r。

标准matroid SwapRounding（或同类已知face-preserving Chernoff rounding）以常数概率同时满足

|a_r(B)−ν_r|≤C(L+sqrt(ν_r L))。

注意sqrt(r_r L)≤sqrt(K)s_r，因为 L≤s_r。因此

C(L+sqrt((μ_r+r_r)L))
≤C(s_r+sqrt(r_r L))
≤C(1+sqrt(K))s_r≤K s_r=r_r，

只需固定K≥C(1+sqrt(K))。于是一次满足普通Chernoff界的SwapRounding输出，就位于y*+R，且位于y*在Q中的最小面。

SOSA成本论证实际上只用当前y*这一点的face-preserving与误差包含，不要求我们已经给出对整个Q都适用的相同R。因此其同一个局部论证可直接使用：令z=1_B；face-preserving给某λ>0使ybar=y*+λ(y*−z)∈Q，而z−y*∈R；取yhat=(λx+ybar)/(1+λ)，则yhat∈Q∩(x−R)。y*最优意味着c·y*≤c·yhat，代入yhat=y*+λ(x−z)/(1+λ)得到c·z≤c·x。又z−x∈R−R=2R，得到目标误差。

这一步解释了为何仅以“Chernoff半径依赖μ，SOSA要求固定R”来保留GA-01是不充分的：在x−R内均值只增加一个r，选足够大的常数K便自洽吸收。

## 需要复核的技术门

1. SwapRounding的面保持：y*的所有正系数basis分解均在该最小面，合并交换须保持该面；也可显式限制到该face对应的matroid minors。需引用/核对标准实现的oracle与位复杂度。
2. 精确LP不应输入不受控无理平方根。可将sqrt(μ_r L)替换为整数上界ceil(sqrt(μ_r L))，只增加≤1，被L≥1吸收；再增常数K。这样误差体的所有系数为有理，半径比目标量级至多常数。
3. 标准Chernoff联合成功概率需选择L中常数，使所有k行成功概率≥1/2。失败可识别（逐行核差与cost），重复至成功期望多项式。最终cost保证只对已验证的成功输出承诺。
4. 本推论只保O(·)误差，不保母文某个精确常数、精确尾分布、marginals或多预算。若原公开问题实质要求更强分布合同，须重新逐字对照，不能扩大本推论。

当前判断：该路线非常可能是2026通用工具的标准组合，而非值得独立押注的创新。报告和JSON降级，不宣称已解决原问题。


代码与冻结输出：`tests/audits/topic_selection/generalized_assignment/`、`evidence/runs/topic_selection/generalized_assignment/`；见[复现说明](../VERIFICATION.md)。
