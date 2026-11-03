---
id: "customer-attraction/d1-safe-local-renormalization-and-terminal-component-information-boundary"
kind: "obstruction"
type_tag: "障碍"
title: "SAFE局部归一化、末端组件信息与递归加载模板的停界"
status: "proved-local-identities-and-template-obstructions;global-capacity-open"
summary: "SAFE改分母只改变路由不产生库存；固定价格的参数选择在端点，末端四税本身不认证早位IC；加载补偿模板被原始B保底吞掉有效幅度。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/flow/normalization_slack_and_capacity_checkpoint.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/flow/normalization_slack_and_capacity_checkpoint.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/flow_continue/terminal_branch_elimination_checkpoint.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/flow_continue/terminal_branch_elimination_checkpoint.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/credible/recursive_loader_failed_attempt.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/credible/recursive_loader_failed_attempt.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/flow_continue/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d1dc7a18aded4304a25a87486681fb21/flow_continue/README.md"
---

# 固定自然 SAFE 的局部归一化

这里先是抽象非负流量账本，不把所有量自动当原游戏可兑现收益。一个自然 SAFE 源有 v>0、后继接收量 q_j≥0，P=Σ_jq_j<v，L=v−P>0，外来需求 h≥0。选择 0≤χ<L，并把分母改成 ν=v−χ，当前吸收和后继流量分别为
\[
h\frac{L-\chi}{v-\chi},\qquad h\frac{q_j}{v-\chi}.
\]
它们非负且和为 h。局部守恒不需要 χ≤某个离轨超额 ℓ，也没有改变原真实 IC；它只是控制流量路线。不能保持旧 β/旧 coupon 系数不变，又另把降低的分母当新钱。如果 P>0，可取端点 χ=L，此时 ν=P、当前吸收零；P=0 时该端点 ν=0 非法，而所有合法 χ 都把全部 h 吸收在当前。

冻结非负当前价格 z_i 和各后继单位成本 C_j，则每单位源成本为
\[
C_i(\chi)=\frac{z_i(L-\chi)+\sum_jq_jC_j}{v-\chi},
\quad
C_i'(\chi)=\frac{\sum_jq_j(C_j-z_i)}{(v-\chi)^2}.
\]
导数分子与 χ 无关。因此固定延续的最优点是合法端点、端点极限或全区间平坦，不出现凭局部调参制造的严格内点最优。若要倒推选择未来成本，仍须证明所选路由在同一原路径的共同容量可行；这个导数不提供容量。所有终端价格为 1 时，逐层成本仍为 1，改 ν 不会把总源需求降低到原 W 以下。

原 checkpoint 还比较四个真实叶：B=finish(g,a)、A=finish(actual-prefix,a)、V=finish(g,S_i)、Z=actual。真实 IC 给 v_B≥v_V、u_i≥D_A，可组成 rectangle 的非负 ℓ+e，但不推出 v_B≤原实际钱包。V、Z 的“fresh”标签不使互斥分支收益成为共同库存。下一义务是实际多源总容量，不是更换局部分母。

## 末端非负税不独立认证早位 SPE

取五名玩家，七个不交主题：C 有 1 名客户，A₁,…,A₆ 各 3 名。完整有序历史策略前 3 位恒 C；最后两位各选此前尚未用的最早 A 标签。因为至多已有 4 个行动，六个 A 中总有新鲜主题；最后两位在全部历史选择裸收益 3 的 BR。

对于任意上下文和任意基准标签 B，若尾路径有最后不同于 B 的行动，它总落在这两个末位之一。因此[四项税恒等式](../引理/稳定B的末异标签四项税与全历史重置刻画--引理.md)需要的当前 IC 和真实 B-child 保底都成立，全部 A,E,γ,ζ 非负。若 B 是实际最后 A，则最后非 B 是倒二 A；设所考察尾长为 n≥2，后缀仅最后一个 B，直接有
\[
\alpha=3,\quad\beta=3/n,\quad
A=0,\ E=3/2-3/n,\ \gamma=0,\ \zeta=3/2.
\]
它们仍逐项非负。这里只宣告末点组件信息满足其约束，不声称全游戏早位 IC。

actual 是 C,C,C,A₁,A₂，W=7；五个不同 A 可覆盖 15，故 2W<OPT₅。可是每个早位 C 只得 1/3，改选一个新鲜 A 并执行原后继可得 3；该策略明显**不是 SPE**。因此这是末点组件单独不足的反模型，绝不是五人或六人完整 SPE 的 half 反例，也不排除“组件加全部原 IC”能有更强结论。保留早位资格是这个例子的用途。

## 一次共享加载—末尾补偿模板为何无正有效幅度

固定 m=n+1，n≥3。客户块 X（大小 a>0）、B=Q∪R∪S（q,ρ,s，互不交）、Y（大小 y）彼此独立，目录含
\[
X,\ B,\ T=X\cup(B\setminus Q),\ U=Y\cup(B\setminus R).
\]
可以另有主题，Q∩R=∅。试图在同根 X 后实现两个真实 suffix-SPE：高叶 X,B^n；低叶 X,T^r,U,B^(n−r−1)，2≤r≤n−1。高根 h=a；有效幅度应是 h−M，M 为**所有完整根 SPE**的首位最低利润，不是高低两指定叶的差。

高叶末位 B 改 T、U 的 BR 必要条件是
\[
q\ge na/2,\qquad y\le\rho/n.\tag{1}
\]
低叶最后非 B 的 U，真实改 B 保底给反向不等式，故 y=ρ/n。低叶最后一个 T 实际利润为
\[
a/(r+1)+\rho/(n-1)+s/n.
\]
它真实改 B 后，无论原完整策略怎样续，每个 B 客户最多被所有剩余者覆盖，故当前至少得
\[
q/(n-r+1)+\rho/n+s/n.
\]
这个分母上界无需冻结原未来 U。必要 IC 为
\[
\frac a{r+1}+\frac\rho{n(n-1)}\ge\frac q{n-r+1}.\tag{2}
\]
结合 (1)、r≥2 及相应函数随 r 单调，
\[
y=\rho/n\ge(n-1)\left[\frac q{n-r+1}-\frac a{r+1}\right]
\ge a(n+2)/6.
\]
因此
\[
|B|\ge na(n+5)/6\ge(n+1)a,
\]
末步等价 (n−3)(n+2)≥0。任意完整根 SPE 都能在根改 B 并取得至少 |B|/(n+1)≥a，故 M≥a，h−M≤0。即使两个指定 suffix 能补完整，仍不能用跨度 a−a/(r+1) 修正正缺陷。加入额外主题不降低这个裸 B 下界；给所有主题加 κ 名共同核客户只使 h、M 同加 κ/m，仍不能挽救。

这是所列重复单 T、最后 U 补偿模板的必要行障碍；没有声称所有跨深度补偿不可能，也没有为已被必要条件排除的模板造全树。原两个有限 insurer/cone 诊断只作为旁证，真实能力范围见[程序合同](../程序/R-d1有限保险与背景聚合探针的真实目标--程序.md)。

## 证据与后续

三份 checkpoint/失败稿及 flow_continue 入口全文保留于[原件证据](../../tools/evidence/d1-stable-reset-and-shared-rent-primary/README.md)。本轮无枚举、BI、LP 或新数学程序调用。可复用的是局部守恒/导数、组件不足机制和加载模板的必要 IC；一般同路径共同付款仍缺容量证明，不因这些障碍而弃置其他补偿路线。
