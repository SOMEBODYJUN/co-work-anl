---
id: "customer-attraction/fractional-extra-mass-interpolation-half-bound"
kind: "theorem"
type_tag: "定理"
title: "额外分数竞争质量插值及其静态 half 界"
status: "proved-static-and-conditional"
truth_status: "delta-family-static-theorem-extra-one-leader-refuted-general-rge3"
review_level: "full-source-read-and-algebraic-reconstruction"
scope: "有限共同目录静态比较；顺序应用仅作条件推论，delta=1逐人候选已被一般银行族在m≥4否定"
summary: "将额外一槽推广为质量r−1+δ、δ∈[0,1]，证明OPT_m≤(2m−1+δ)t_{m,δ}及合法前缀嵌入；若实际每节点支付t_{r,δ}则half成立。δ=1最弱而仍足够half，但不是一般SPE定理。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/security/extra_mass_interface.md#为什么这个更弱门槛仍足够half"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/security/extra_mass_interface.md#已可直接确认的小尾部"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-077c0cacfba24288be91dee1acf6d484/security/free_fractional_security.md#2-根下界与合法前缀嵌入"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/security/extra_mass_interface.md"
---

# 额外分数竞争质量插值及其静态 half 界

## 质量参数和下标

固定合法客户负载b及共同目录 $\mathcal S$。对剩余人数r≥1和 $0\le\delta\le1$，定义分数竞争质量

$$s_{r,\delta}=r-1+\delta,$$
$$t_{r,\delta}(b)=\min_{q\in\Delta(\mathcal S)}\max_{A\in\mathcal S}
\sum_{x\in A}\frac1{b_x+1+s_{r,\delta}\alpha_x(q)}.$$

这不是把真实玩家数改成非整数；它是静态背景分母中的总质量。端点 $\delta=0$ 是标准 $t_r(b)$，$\delta=1$ 是旧 EXTRA-ONE 的 $t_{r+1}(b)$。下标始终表示真实剩余r，括号内质量才是 $r-1+\delta$；不可把“额外一”解释为多了一名顺序玩家。

目录可保留空主题、重复标签及同覆盖标签，q可用全目录。用于原模型时b仍须由合法过去主题实现；外生任意实负载只属于静态函数接口。

## 静态覆盖不等式

根处有m名真实玩家。固定任意q，令 $L_x=mq_x$、

$$M(q)=\max_{A\in\mathcal S}\sum_{x\in A}\frac1{1+L_x}.$$

若比较m个主题的客户覆盖重数为d_x，则逐客户

$$\mathbf1_{d_x>0}\le\frac{d_x+L_x}{1+L_x}.$$

求和，d项是m个合法主题查询值之和，至多mM；L项是q的混合查询值乘m，也至多mM。因此 $OPT_m\le2m\min_qM(q)$。这只是δ=1的宽松版本。

对任意 $0\le\delta\le1$，令 $L_x=(m-1+\delta)\alpha_x(q)$。同一逐客户不等式给

$$OPT_m\le mM(q)+(m-1+\delta)M(q)
=(2m-1+\delta)M(q).$$

取q最小得

$$\boxed{OPT_m\le(2m-1+\delta)t_{m,\delta}(0).}\tag{S}
$$

主题质量预算不能漏掉；同样证明对标准最大覆盖LP有效，把左侧换成 $\min(1,d_x)$。

## 前缀嵌入和条件half

对当前合法主题A、剩余r≥2，若未来使用分布q，则

$$\mathbf1_A+(r-2+\delta)\alpha(q)
$$

是根质量 $r-1+\delta$ 允许的背景负载。故可行域包含给出

$$\boxed{t_{r-1,\delta}(b+\mathbf1_A)ge t_{r,\delta}(b).}\tag{E_\delta}
$$

若一份完整有序历史纯SPE在其实际路径每个节点都满足真实最终收益

$$u_i\ge t_{r_i,\delta}(b_i),\qquad r_i=m-i+1,$$

则反复(Eδ)给每人 $u_i\ge t_{m,\delta}(0)$，从而 $W\ge m t_{m,\delta}(0)$。与(S)合并：

$$OPT_m\le(2m-1+\delta)t_{m,\delta}(0)
\le\left(2-\frac{1-\delta}{m}\right)W\le2W.$$

所以整个δ族都是**条件half机制**；δ=1最弱而仍够half。它没有把静态门槛变成一般SPE合同，也没有移除全部离轨历史量词。

## 小尾部确实支付整个δ族

剩一人时最佳回应值为 $\max_A\sum_{x\in A}1/(b_x+1)=t_{1,0}(b)$，而质量增加会使t非增，所以 $u\ge t_{1,\delta}(b)$。

剩两人时，已有末两人真实最佳回复保底给每人 $u\ge\theta_2(b)\ge v_2(b)\ge t_{2,0}(b)$；因此同样 $u\ge t_{2,\delta}(b)$。这只证明r≤2，不是把三人以上的失败扫描改称证明。

## 当前真值和与银行反族的关系

原稿把δ=1写为 EXTRA-ONE-LEADER，并称对所有r开放。该状态已被[笛卡尔银行逐人反族](../反例/笛卡尔银行目录的逐人分数门槛反族--反例.md)纠正：其一份完整m人SPE在m≥4有 $u_1<t_{m,1}(0)=\delta_{m+1}(0)$。因此本页的条件half和静态(S)/(Eδ)保留，但无条件逐人合同只在r≤2有普遍证明，r≥3不能从本页推出。

与标准自由分数定义的关系是 $t_{r,0}=t_r$；与响应债务定理的 $t_{r+1}$ 是δ=1同一质量，但响应条件给出的是特定真实分支上的充分支付条件，亦不保证一般SPE。

本页不把扫描中未找到分离的数值记录当作证明；真实全历史策略、合法过去和任意平局仍须独立保留。无外审或新颖性认证。
