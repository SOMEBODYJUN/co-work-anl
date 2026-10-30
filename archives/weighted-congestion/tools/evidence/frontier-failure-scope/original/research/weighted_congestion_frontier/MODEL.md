# WC-TARGET v1：精确模型

## 对象与定义域

d∈Z_{≥0}。G_d 包含所有有限加权原子拥塞博弈：非空有限 E、N；每个玩家有任意实数正权 w_i>0 和非空有限策略族 S_i⊆2^E；每个资源费用为 c_e(x)=Σ_{k=0}^d a_{e,k}x^k，a_{e,k}≥0。允许空策略、零费用、不同玩家策略族不同、多资源策略。权重不依资源变化。

纯状态 s∈Π_i S_i，负载 x_e(s)=Σ_{i:e∈s_i}w_i，成本 C_i(s)=Σ_{e∈s_i}c_e(x_e(s))。采用核心来源的“不乘 w_i”成本约定；固定玩家整体乘正 w_i 不改变近似均衡集合。实验的有理权/系数是全类的子域，不得偷换一般存在命题。

α≥1 的 α-PNE 定义为：对每个 i、每个 t_i∈S_i，

    C_i(s) ≤ α C_i(t_i,s_{−i}).

边界取 ≤；非存在证明必须对每个 s 找到严格 > 的偏离。偏离后重新计算全部受影响资源的负载。偏离成本零而当前成本正时，所有有限 α 均失效；两个成本都零时满足不等式，禁止直接计算 0/0。

## 普遍阈值

    a_*(d) = inf {α≥1 : 对每个 G∈G_d，存在 s∈Π_i S_i 是 α-PNE}。

使用 inf，不预设端点在所有博弈中均取得。有限单个游戏的最佳因子、全类阈值、可计算性和社会福利近似是不同对象。

## 主目标的量词

上界：给出显式 f(d)≥1、f(d)/d→0，并证明对每个整数 d≥d_0 和每个 G∈G_d 都存在 f(d)-PNE；有限小 d 可用已知保证补齐。只有子类、固定人数或实验范围不满足主目标。

下界：给出显式可增长族 G_d∈G_d 和 L(d)，证明对每个目标 d、每个纯状态 s，存在 i,t_i 使 C_i(s)>α C_i(t_i,s_{−i})，适用于全部 α<L(d)。明确 L 与核实过的已知下界相比改善哪里；必须保留玩家数随 d 增长的可能。仅发现一个改善循环不能证明非存在，因为循环之外可能仍有均衡。

终极目标是确定 a_*(d) 的增长阶或更精确的前沿。首个 o(d) 上界/严格新无限下界是重要阶段突破，不等同于上下界已匹配。

## Claim 身份与外部定理

新 claim 必须列 ID/version、Exact Statement、Objects、Domain、Quantifiers、Assumptions、Definitions、Scope、Conclusion、Dependencies、Evidence、Counterevidence/Objections、Status、Related Files。变更任一量词、模型或范围建立新版本。外部定理逐项检查适用条件；工具失败没有数学真值含义。

## 端点的后续已证性质（定义不变）

[WC-UNIVERSAL-THRESHOLD-ENDPOINT-v1](../current/weighted_congestion/template_certificates/integer_counterexample_normal_form.md)在原inf定义下证明：全类可行倍率集是[a_*(d),∞)，因此端点对每个游戏分别可行。该结论不预设某个有限游戏取得全类上确界，也没有解决其增长阶；[严格反例规范形](../current/weighted_congestion/template_certificates/integer_counterexample_normal_form.md)另给逐固定倍率的整数单项式子类等价。
