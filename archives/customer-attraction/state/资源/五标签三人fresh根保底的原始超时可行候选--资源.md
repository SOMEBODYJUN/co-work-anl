---
id: customer-attraction/p5m3-fresh-root-floor-original-timeout-floating-incumbent
kind: resource
type_tag: 资源
title: 五标签三人fresh根保底的原始超时可行候选
status: complete-all-fields-and-policy-read; original-time-limit-with-primal-not-optimality
truth_status: numerical-zero-incumbent; no-positive-rational-counterexample-or-general-floor-result
review_level: exact-primary-SHA-prior-normal-fullread-reused; all15coefficients-and26policy-actions-accounted
scope: R731的p5/m3联合完整fresh政策MILP；45秒原限时记录；不包含原CAG客户实例
summary: 全部14字段、15浮点系数及26合法历史动作完整保全；有primal候选而非无解报告，约2.86e−13不作严格正例，精确常数−1点仅解释零差不认证原求解。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-731efdb50dd844178e597d804bdd4596/root_fresh/README.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-731efdb50dd844178e597d804bdd4596/root_fresh/joint_fresh_floor.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-731efdb50dd844178e597d804bdd4596/root_fresh/joint_p5m3.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-731efdb50dd844178e597d804bdd4596/root_fresh/joint_p5m3.json
---

## 原报告全部标量和状态

1081B JSON原字节在[证据](../../tools/evidence/root-fresh-MILP-original-and-timeout-three-primary/README.md)，本次对同SHA priornormal/fullread准确复用，无新show或求解。[程序完整对象](../程序/无重复二次根保底的联合策略MILP与大M合同--程序.md)给辅助模型、变量顺序、全部大M/真实IC/θ见证和261/1116解析来源；不是泛称“有限搜索”后只保一个目标数字。

|字段|完整原值及含义|
|---|---|
|scope|`finite auxiliary full ordered-history signed fresh quadratic search`|
|p / m|5 / 3|
|seconds|45.005815471000005；源码从milp调用前计时，不含建矩阵|
|status|1|
|message|`Time limit reached. (HiGHS Status 13: Time limit reached)`|
|variables / rows|261 / 1116|
|objective|2.859934511434403e−13；报告是SciPy最小目标取负后的τ−根收益|
|universal_result|false|
|theta_lower|−2.999999999999714|
|root_payoff|−3.0|
|coefficients / policy|下面完整15数与26动作；这两个复合字段连同上表共14字段|

原报告**有浮点primal候选**，所以不能改称无可用解。入口明确这个约2.86e−13属于数值零、没有正反例、没有全局上界或一般结论。它不是精确infeasible、全局最优0、排除所有同p,m根反例或普遍fresh floor证明。原message没有说primal_status None，不能挪另一171/591报告的错误文本或缺solution状态来覆盖。

`theta_lower`只对应原求解器浮点向量的见证下界变量，未另精确枚举所有H确认其等于真正θ；root_payoff也是传播变量的原值。全部V/z/y未保存，当前JSON不足以独立核1116行残差。保留一个policy并不恢复缺失原浮点向量。

## 十五个系数的完整顺序和值

源码先5个α，再按无序对01,02,03,04,12,13,14,23,24,34存β。没有用四舍五入值取代原15数。

|序号|系数|原浮点文本|
|---:|---|---:|
|0|α₀|−1.0000000000002855|
|1|α₁|−1.000000000000286|
|2|α₂|−1.0|
|3|α₃|−0.9999999999988436|
|4|α₄|−1.0|
|5|β₀₁|−0.9999999999985572|
|6|β₀₂|−0.9999999999988431|
|7|β₀₃|−1.0000000000008713|
|8|β₀₄|−1.0000000000000009|
|9|β₁₂|−1.0|
|10|β₁₃|−1.0000000000011569|
|11|β₁₄|−1.0|
|12|β₂₃|−1.0|
|13|β₂₄|−0.999999999999714|
|14|β₃₄|−0.9999999999999991|

0/1/7/8/10五坐标略低于名义下界−1，是原浮点容差现象的直接文本证据，不能把原向量当精确盒内有理点。不能仅把每数转换Fraction就宣布精确可行或把微小正目标认证成严格floor反例；对近零候选必须重核原定义。

## 二十六个完整fresh历史政策

空字符串是根，其余逗号串是有序历史，a∉h。全26键为1根、5个一步、20个二步，不是26份SPE或原CAG全重复历史。

|有序历史h|原动作σ(h)|有序历史h|原动作σ(h)|
|---|---:|---|---:|
|∅|0|0|2|
|1|0|2|3|
|3|1|4|1|
|0,1|4|0,2|3|
|0,3|1|0,4|1|
|1,0|3|1,2|3|
|1,3|0|1,4|0|
|2,0|3|2,1|4|
|2,3|1|2,4|1|
|3,0|1|3,1|2|
|3,2|0|3,4|0|
|4,0|1|4,1|3|
|4,2|0|4,3|2|

完整键/合法动作的结构可从原JSON直接核；根路径按该字典是(0,2,3)。这不等于已将原微扰系数下所有节点逐定义理性化。源码用每节点z浮点最大值输出动作，不输出所有binary值或断言其整数残差；打印policy的合法性和完整性只是必要结构条件。

### 精确常数点为何只有零差

把所有α、β精确设为−1时，任何三元终局中每名所选标签利润都为−3，不依后继政策；所有fresh动作都平局，任意完整合法policy都是纯SPE。每个二元H的每个未用query也为−3，故θ₅,₃=−3，根差为0。该定义级等式只解释原候选靠近哪个零差面，**不是**原浮点输出的精确重构或旧MILP最优性审计，也不排除其它系数的正点。本轮没有执行数值/分数程序来检验这个直接代数观察。

## 新入口全部内容与可接续义务

847B README说辅助对象沿旧R-3d6f的quadratic_graph_compiler.md、不是原CAG；联合选全部有序政策、对称系数和每θ背景的max见证，有别旧固定策略锥；正数必须有理化/定义级全历史审计。它准确列p5/m3、系数[−1,1]、45秒、261/1116、超时及数值零，并将本JSON仅作运行边界复现，拒绝一般结论及同规模重复扫描，下一步偏向解析交换/更紧根松弛结构。这些是作者研究时态，不是本worker已执行新搜索或接续要求必须先解决floor。

本次必要6513B引用原稿已normal/fullread。其符号A₀=max|α|、L=max|β|，K=1+ceil(6A₀+6L(m−1)+2L)，pair重数r_ab=K−2β_ab，D_a=Σ_(b≠a)r_ab，δ_a=α_a−D_a，E=max|δ|、D=maxD_a；充分C=1+ceil(3E+2D)、private重数r_a=C+δ_a、B=C−(m−1)K/2。它解释选择足够偏置后收益/θ同加B并补全部原重复前缀，但同时给OPT<2W。因此辅助根保底的真假与原half比率必须分开；本次不重授该作者待审候选为新的canonical证明，也不跑其已充分成功的2288旧回归。

已读并比较当前辅助候选、完整fresh嵌入/均匀偏置障碍、频率二候选、旧171/591超时无primal资源以及[工作区根入口](包含前缀证书的来源映射与背景回路工作区入口--资源.md)。旧根已正确概述本两related而当时未primarydone；本次把实际联合变量/约束、齐次归一化、所有报告字段/15数/26动作完整提升为单独程序资源，不以旧摘要代原件，也不虚构第二次运行。

三源为入口integrated、代码retained、JSONretained，每源receipt三项true及实质read/comparison/decision/targets齐。7ZT claim已pushed c8da98edfbe9483c455f65966a085fb5d9e233bd，raw local_sync为synced原样保，完整7ID捕获不改但只本3done。0新MILP/数学运行、0原import、0R修改/Git/start/claim/done/adopt；阶段二来源清洗已足够成熟，未把开放floor、当前六人目标或全仓任务称完成。
