# v2 独立重构：无 FSLP 前提的一般福利 LP 与门控全类比例

2026-10-18。收到 root 对 v2 的口头目标“general LP→random claims→balanced→13/8、无 FSLP 假设”后独立构造本稿；尚未读取正式 v2 Exact 或作者 Proof，也未查看 root 发给作者的有理反算。v1 的实读结论不冒作 v2 审查。

## 1. 猜测并独立构造的一般显式 LP

沿 v1 全部 norm1/非负/显式菜单定义。设 state 变量 lambda_gs≥0，列出 incidence 变量 z_gsu≥0。最大化

L=sum_g,s,u p_gsu*z_gsu，

约束为 sum_s lambda_gs≤1（每组），z_gsu≤lambda_gs（每 incidence），sum_g,s z_gsu≤1（每 resource）。零 incidence 的 z 可直接置 0，未列项没有变量。此 LP 规模 O(S+I)、系数有理、显式；零解合法，最优值 0≤L≤n，且有标准多项式位长 rational optimum。

令 v1 balanced optimum 为 B=beta*。从其最大见证 H、states、bundles 取 H 上相应 lambda=1，其导出 positive incidences z=1，余下均0，可得 LP 可行，且

L≥sum_{g∈H}v_g(B_g)≥|H|*B≥n B²。

这里从 balanced witness 嵌入 LP，未假设 unit 正支撑 FSLP。若 B=0，同一不等式显然成立。

## 2. 两级有限 claims，资源竞争与 welfare

每组独立：按 lambda_gs 选 state s，剩余概率 1−sum_s lambda_gs 选 null。条件于 state s 且 lambda_gs>0，对每原 positive incidence u 独立抛 claim coin，成功概率 z_gsu/lambda_gs；null 无 claims。组间独立，组内不同资源相关只来自共同 state。

令 Y_gu 为该组在 u 上成功 claim 时的原 p_gsu，否则 0。则

Pr[Y_gu>0]=sum_{s:p_gsu>0}z_gsu，sum_g Pr[Y_gu>0]≤1，

sum_g,u E Y_gu=sum_g,s,u p_gsu*z_gsu=L。

沿 v1 的单资源 tail proof，独立性只在组间使用：E sum_u max_gY_gu≥aL，a=1−1/e。给资源的成功 claimant 中原系数最大者（tie 固定），得到每组一个原 state 上的不交实际 bundle，selected-state 质量 r_g∈[0,1]，总和≥aL。null 组质量0且可输出任意原 state。

### 确定性 bit-poly

先依次固定每组 state/null，比较精确条件期望。每资源每原正 threshold t 的 group tail probability 是：未固定组为 sum_{s:p_gsu≥t}z_gsu；已固定非null state 为 1[p_gsu≥t]*z_gsu/lambda_gs；null 为0。全部 rational；候选的原概率是 lambda 或 null 剩余概率，当前期望为候选条件期望加权平均。只选正概率候选，故未支付极小概率倒数循环。

所有 states 固定后再逐个固定被选 states 的 incidence claim coin，用同一 CDF 精确条件期望公式；资源维度只涉有限原 p levels。最后所有 randomness 均消除，福利 W≥aL≥a nB²。比值 z/lambda 的位长是两者描述长度之和；总乘积/有限求和位长仍多项式。**条件化后逐资源 positive probability 可能超过1，但此时仅计算真实条件期望，不再重用初始 tail 下界；这不是缺口。**

## 3. Balanced 提取与一般 13/8 ratio

将得到的原实际质量 r_g 排序 r_(1)≥...≥r_(n)，计算

b_alg=max_{1≤k≤n}min{k/n,r_(k)}。

选 maximizing k 的 top-k groups，v1 的完整原作业回填给 C≤2−b_alg。算法不知道 B、a 或 OPT。

证明 13/8 ratio：若 B≤10/13，则 C≤2≤(13/8)(2−B)。若 B>10/13，定义仅供分析的有理目标 b=(13B−10)/8∈(0,3/8]。设 h=#{g:r_g≥b}。若 h≤bn，则 W≤h+(n−h)b≤(2b−b²)n。另一方面 W≥a B²n>(5/8)B²n，而且

(5/8)B²−(2b−b²)=(209B²−468B+260)/64≥1/64>0。

最后一步因该二次式在 [0,1] 单调下降（导数418B−468<0），在 B=1 处为1。因此必 h>bn，所列 top-h 前缀给 b_alg≥b。于是

C≤2−b_alg≤2−b=(13/8)(2−B)=(13/8)OPT(P_gate)。

在 B=10/13、B=1、n=1、zero lambda/null/zero incidence 和资源未用情况下均无除零；13/8 是整个明示 P_gate 类的相对 OPT 比例，不再仅是 FSLP-feasible 子类的绝对峰。

## 4. 可选更强常数（不当作已审 v2 合同）

由 W≥a nB² 的同一数量论证有 b_alg≥1−sqrt(1−aB²)，所以 C≤1+sqrt(1−aB²)。对 a=1−1/e<3/4，R(B)=[1+sqrt(1−aB²)]/(2−B) 在 [0,1] 单调非减：其导数符号等于 sqrt(1−aB²)+1−2aB，后者≥sqrt(1−a)+1−2a>0。故 C≤(1+e^(-1/2))OPT，数值约1.606531。

严格有理版本更简单且不含算法超越比较：13/8 的以上二次式证明已足够。本文不认证更强比例的全球新颖性，也不把 whole-class 结果外推原 flat 或 general UM。

## 5. 仍须实际比对 v2 Exact

上面是本人独立选择的 LP 和算法。若作者正式 Exact 的变量、状态/null 机制、资源 claim 分布、组可用端、zero jobs 或 ratio 量词不同，需逐项另核，不能因为本独立方案可证便自动判作者方案通过。下一步才读正式 v2 Exact。
