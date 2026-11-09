---
id: "M-4bfb99ccca4f4f77a6aaee6882ef1170"
kind: "theorem"
type_tag: "定理"
title: "CONFIG保真低峰解码的私有树参数障碍"
status: "proved-with-stated-scope"
summary: "Q_D的CONFIG(1)与完整实际值2−1/D结合私有均匀菜单树的配置上界，证明峰不增低峰解码必须满足D ceil(d/(μ+2))≤d，故d≥D、μ≥D−2；无须正向调度映射或算法性。"
source_refs:
  - "archives/unrelated-machines/state/定理/规范化平菜单的CONFIG与正支撑LP双向保持--定理.md"
  - "archives/unrelated-machines/state/定理/私有菜单树有界叶重数配置界--定理.md"
  - "research/workspaces/map-v2/Boss5/qd-private-tree-decoder-obstruction-474257b8.md"
---

# CONFIG保真低峰解码的私有树参数障碍

本结果把显式 $Q_D$ 族的实际整数值与完全私有均匀菜单树的已证配置上界共同用于一条具体编译路线。它给出解码所必需的参数增长；不需要假定存在正向实际调度映射，也不把配置可行性当作源的实际低峰调度。

## 1. 两侧的完整模型

源 $P_D$ 是 $Q_D$ 的完整归一化 flat 普通不相关机实例，(D\ge2) 为整数。资源为 $g_{a,j}$ 和 $A_a$，其中 $a,j\in[D]$。main 组有 $D$ 个 indexed states，第 $a$ 态含 $g_{a,1},\ldots,g_{a,D}$，每项 private 权 $1/D$。每对 $(a,j)$ 有一 helper 组，恰有两个 singleton states：资源 $g_{a,j}$ 或 $A_a$，private 权均为 $1$。

完整 flat 规则是：每 state 一台独立 private 机；每资源一台资源机；每组一件 unit selector，其有限端恰为本组全部 state 机；每个 state-resource incidence 是不同的原任务，只能在该 state private 机按其 private 权运行，或在命名资源机按时间 $1$ 运行。所有未选 states 的任务也存在。无额外任务、预载或资格。

目标 $P'$ 严格采用 `UM-Q-PRIVATE-TREE-BOUNDED-MULTIPLICITY-CONFIGURATION-FLOOR-v3` 的模型：全局整数 $d,h\ge1$，非空有限 root 集合，每 root 有非空有限 state 菜单，每 state 为满 $d$ 叉、高 $h$ 的完全私有树；不同 states 的内部机器互异。每 root 一件 unit selector，有限端恰为其全部 state 根。每内部 edge job 只有父端 $1/d$、子端 $1$；每 leaf job 只有父端 $1/d$ 和显式叶映射指定的唯一单位外端。无其它任务、预载或资格。全部 states、树和叶端显式存在。

令实际最大完整 state 叶资源重数为
\[
\mu=\max_{u,s,z}|f_{us}^{-1}(z)|\ge1.
\]
外部资源可以跨 roots 或 states 共享；完全私有的要求作用于内部机器。这里的 $d$ 同时规定满树分支和父端处理时间，不能只从某个图的二叉形状认定 $d=2$。

两侧 CONFIG(1) 均为全部原任务的通常 machine 配置 LP：每台机器在合法、负载至多 $1$ 的任务子集上给概率分布，每件原任务覆盖恰 $1$。本结论使用目标 CONFIG(1) 的可行性；不要求某个前向程序逐项转送源的特定配置证书。

## 2. 精确结论

设目标 $P'$ 满足 CONFIG(1) 可行，并且满足以下低峰解码合同：

> 对每份峰 $C<2$ 的 $P'$ 完整实际调度，存在一份包含全部原任务的 $P_D$ 合法调度，其峰不超过 $C$。

不要求这个解码可计算，也不要求处理峰至少 $2$ 的目标调度。令
\[
r=\left\lceil\frac d{\mu+2}\right\rceil.
\]
则必有
\[
\boxed{D r\le d},\qquad d\ge D,\qquad \mu\ge D-2.
\]

在本页的目标域及 CONFIG(1) 前件下，低峰解码合同等价于标量条件 $\operatorname{OPT}(P_D)\le\operatorname{OPT}(P')$：v3保证目标最优峰严格小于2且有限实例最优值达到，故解码目标最优调度给该不等式；反向可对每份目标低峰调度取同一份源最优调度，峰仍不增。这个等价没有算法性要求，尤其适用于精确保实际 OPT 的编译。以上参数结论均为必要条件，不声称充分，也不构造满足边界的编译。

若只知道目标重数至多某个整数 $\mu_0\ge1$，则可用该上界代入，得到
\[
D\left\lceil\frac d{\mu_0+2}\right\rceil\le d.
\]
因此 $D>\mu_0+2$ 时不存在满足这些条件的目标及解码。若 $D=\mu_0+2$，这一必要条件还要求 $D\mid d$，但不能据此声称存在目标或解码。固定分支数上界 $d_0$ 时，任何 $D>d_0$ 也被排除，即使允许重数随输入增长。

## 3. 源的整数值与全部任务配置证书

先考虑同一 normalized 菜单的 one-state partial 分配：每组选一个 state、领取其任意资源子集，跨组领取不交，目标是最大化最小 private 质量，记为 $V$。

main 若在同一行 $a$ 领取 $r_0\ge2$ 个 $g_{a,j}$，对应的 $r_0$ 个 helper 都不能领取自己的 $g_{a,j}$。要取得任何正值，这些 helper 只能领取同一个 $A_a$，违反不交性。因此任何正值分配中 main 至多领取一个 $g$，故 $V\le1/D$。反向让 main 领取任一 $g_{a,j_0}$，对应 helper 领取 $A_a$，其余 helpers 各领取自己的 $g$，得到 $V=1/D$。

这里的完整 flat 实际值为
\[
\operatorname{OPT}(P_D)=2-V=2-\frac1D.
\]
全任务桥可直接核验：从阈值 $v$ 的 partial 分配，将各组 selector 放在选中 state，把领取的 incidences 外送，其余全部 incidences 留各自 private。选中 private 负载至多 $2-v$，未选 states 的全部任务总负载为 $1$，资源机至多接一个 unit job。反向对任意完整实际峰 $C<2$ 调度，每组 selector 所在 state 的原 private 总质量为 $1$，故该 state 实际外送质量至少 $2-C$；每资源机至多接一件 unit job。这些实际外送给出原 one-state partial 不交分配。因此 $C\ge2-V$。峰至少 $2$ 的分支本来不小于 $2-1/D$。

源的共同 FSLP 证书为：main 每态概率 $1/D$；每 helper 以 $1-1/D$ 选自己的 $g$，以 $1/D$ 选 $A_a$。每个 $g$ 的容量和为 $1/D+(1-1/D)=1$，每个 $A_a$ 的容量和为 $D(1/D)=1$。

该证书给完整 machine CONFIG(1)：在任一 state private 机，以本 state 概率 $\lambda$ 取 selector singleton，以 $1-\lambda$ 取该 state 的全部 incidences；后者总 private 负载为 $1$。资源机以相应 $\lambda$ 取各 incidence 的 unit singleton，余量给空配置。每 selector 的覆盖为本组 $\sum_s\lambda_s=1$，每一件 incidence（包括所有未选态任务）的 private 与资源覆盖恰为 $1-\lambda+\lambda=1$。这不是只对 selected subinstance 给证书。

源实例有 $D^2+1$ 个组、(2D^2+D) 个 states、(3D^2) 个 incidences、(D^2+D) 个资源；构造与证书大小按显式 $D$ 多项式，而非按 $\log D$ 多项式。

## 4. 目标配置界与解码方向

由私有菜单树 v3 的完整 CONFIG(T) 实际存在定理，在 $T=1$ 时有 $a=d$。取上面的 $r$，默认参数证明给
\[
d-\mu(r-1)\ge2r-1\ge1,
\qquad(2r-1)^h\ge2r^h-1.
\]
因此其 rainbow/Haxell 条件满足，存在目标全部原任务的一份实际调度，峰满足
\[
C'\le2-\frac rd<2.
\]
这里引用的是已证存在性及全部原 $d$ 叉任务回填；不需要把 Haxell 的存在证明改造成位多项式输出算法。

对这份实际低峰调度调用本页假设的解码，即得
\[
2-\frac1D=\operatorname{OPT}(P_D)
\le C'\le2-\frac rd.
\]
所以 $Dr\le d$。因为 $r\ge1$，有 $d\ge D$；因为 $r\ge d/(\mu+2)$，有 $D\le\mu+2$。若使用上界 $\mu_0$，同一 v3 定理在较大重数上界下仍适用，给相应的必要条件。边界 $D=\mu_0+2$ 时，(D\lceil d/D\rceil\le d) 当且仅当 $D\mid d$。

这条证明只需要目标向源的低峰实际解码。源向目标的实际调度扩展、完整 OPT 等式、映射的统一性及计算复杂度均没有用于反证。

## 5. 编译路线的准确边界

对任意固定 $\mu_0\ge1$，不存在覆盖全部 $D\ge2$ 的一族映射，同时提供目标 CONFIG(1)、上述完全私有均匀树域和峰不增低峰解码，并使每完整 state 重数至多 $\mu_0$。注入 state 是 $\mu_0=1$；取 $D\ge4$ 已排除此合同。固定 $d_0$ 也不能覆盖任意大的 $D$。

这不排除无界分支与重数、不同目标结构、有损解码或不保 CONFIG(1) 的路线。共享内部机器、异构树、非均匀处理时间、多单位叶端、额外任务和预载均不在所调用的 v3 结构域内。

已证的 normalized binary-selector-tree、state-dummy 与真实 port-path 正规化不与本结论冲突：其中每个树顶点可有自己的 unit selector，singleton 与 port 处理时间和共享方式也不同。图上二叉不等于全局父端 $1/2$ 的 v3 完全私有二叉树。那些正规形保值及保证书的结论仍按各自完整输入域成立。

此为两个已登记结果共同支付的精确结构障碍，不是一般 UM 困难性定理，不是一般近二近似不可能，也没有宣称上述参数必要条件锐利。证据来源为 [Q_D 及其完整配置桥](规范化平菜单的CONFIG与正支撑LP双向保持--定理.md) 的“平坦不相关机与 FSLP 的双向证书”“自足的 $Q_D$ 障碍与规模”，以及 [私有菜单树 v3](私有菜单树有界叶重数配置界--定理.md) 的完整模型、全配置实际存在界和默认 $r$ 证明。本次为第三阶段跨包推导和独立复核，没有新增有限枚举。
