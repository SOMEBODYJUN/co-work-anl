---
id: customer-attraction/pb-counterexample-extension-to-fractional-extra-slot-floor
kind: corollary
type_tag: 推论
title: 任意背景分数额外槽门槛的PB分离
status: proved-extension-of-existing-background-counterexample
summary: 同一PB子SPE的Jensen查询对任意连续合法分数负载仍给s大于实际前三人收益；不只是较强整数门槛失败的逻辑外推，不是根或六人half反例。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/potential_dual/fractional_background_floor_corollary.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/potential_dual/README.md
---

# 任意背景分数额外槽门槛的PB分离

有限单位客户、有限非空共同目录，b为**合法有序前缀**的整数负载，余r人完整历史纯SPE，允许重复主题及任意离轨平局。定义静态质量r的
\[
 f_r(b)=\min_{q\in\Delta(S)}\max_{T\in S}\sum_{x\in T}\frac1{1+b_x+r q_x}
       =t_{r+1}(b).
\]
被反驳的是任意合法b及任意上述子SPE首位均有u≥f_r(b)。f_r不大于真正r槽整数混合值v_(r+1)，由倒数凸性得到；但较强u≥v失败不能逻辑上推出本弱式失败，以下给独立于这种错误蕴含的全分数下界。

## 继承的完整策略与本页实际扩展

采用[PB完整背景构造](../反例/任意合法背景的前两人额外槽安全值--反例.md)：k=3、d=20、q₀=12、r=2475、Q=2063、H=100000、M=10⁹。每段Q个real块（各q₀客户），另有k−1个dummy块（各Hq₀客户）。real块中q₀−1客户背景M、一客户M+1，dummy背景HM；全singletons使此背景可由合法前缀实现。每个regular主题在每段选ℓ∈{1,2,3}个real块及前k−ℓ个dummy块，各段Cartesian组合。

前述正式证明给Greedy/Fill/Copy/Punish及首次singleton后的完整子树拼合，核任意有序历史全部再次偏离；前三人的真实收益各为u=dkF(k)，其中
\[
 F(c)=\frac{q_0-1}{M+c}+\frac1{M+c+1},\qquad
 G(c)=\frac{Hq_0}{HM+c}.
\]
本页不重授新策略或声称再次展开巨量树；继承这一已证完整SPE，扩展的是静态查询对全部连续分数背景的保证。

## 对每个分数分布都成立的容量与Jensen

查询p在每段均匀选一个real块并取全部k−1个dummy块，是合法regular主题分布。任取背景分布q，令ℓ_x=rq_x。固定段及固定real客户层（每块各一个同背景客户），任一regular主题覆盖至多k个该层客户，任一singleton至多一个。因此线性平均后仍有
\[
 \sum_{j=1}^{Q}\ell_j\le rk.\tag{L}
\]
这直接量化q，不需要ℓ是整数元组或随机整数负载的实现。对q₀−1个M背景层及一个M+1层分别用倒数凸性和单调性，查询real收益至少F(1+rk/Q)。每个dummy客户ℓ_x≤r，故每段dummy收益至少(k−1)G(r+1)。于是同一个合法查询分布对全部q满足
\[
 \max_T\sum_{x\in T}\frac1{1+b_x+\ell_x}
 \ge E_{T\sim p}\sum_{x\in T}\frac1{1+b_x+\ell_x}
 \ge s:=d[F(1+rk/Q)+(k-1)G(r+1)].
\]
取min_q，得到f_r(b)≥s。固定参数有
\[
 u=\frac{180000000705}{250000001750000003},\qquad
 s-u=\frac{655518746053822970420433555247437051305}
 {604541061548383275389777051408169916255944671102717364}>0.
\]
所以前三人每人u<f_r(b)，也否其前三人中任一、前两人平均等加强。原源只重算这两个标量，没有重做旧PB全历史证明；[后继标准平台](../反例/PB标准分数鞍点的真实前三步平台--反例.md)甚至给竞争质量r−1下的精确鞍点与三步平台，不能倒填成原源已完成的工作。

## 准确保留的条件用途与边界

若上述普遍逐人式本来成立，沿m人实际位置取余人数r=m−i+1，b_i+r q是m槽合法分数负载，故f_r(b_i)≥f_m(0)。逐人求和与[静态覆盖界](../等价/空根分数安全值的齐次平方根表示--等价.md)会给W≥mf_m(0)≥OPT_m/2。这是正确条件推导，但第一前提已假。

PB背景已经覆盖所有客户，未保证是原根SPE的实际前缀；经过它时福利本来就是全客户数。此分离不否根聚合W≥mf_m(0)、不能将r2475代成六人，也不产生半覆盖反例。源中“本例没有反驳某根逐人合同”只说本构造的边界；后继银行族是否另有逐人反证必须独立查证，不能维持过时OPEN。

主源5842B和1256B入口全部实读、比较旧PB完整证明及标准平台后继，原字节保全见[证据](../../tools/evidence/fractional-root-and-layer-current-primary/README.md)。新意限于来源所述的连续负载扩展，没有外审或新颖性认证；(L)是该扩展的关键，不能用Jensen口号代替。
