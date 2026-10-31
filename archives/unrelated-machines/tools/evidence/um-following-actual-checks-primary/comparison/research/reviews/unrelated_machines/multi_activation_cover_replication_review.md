# 多件共同激活与复制反放大：独立审查

## 审查对象

审查 `research/current/unrelated_machines/multi_activation_cover_and_replication_barriers.md` 的四个范围：

* `UM-MULTI-ACTIVATION-STATIC-COVER-v1` 的全程负载不变式；
* `UM-MULTI-ACTIVATION-HOLD-EDGE-RESTATEMENT-v1` 是否真的扩大静态接口；
* 给定目标的两机三任务反例与静态 cover 非必要的三机路径例；
* `UM-DISJOINT-BLOCK-NO-AMPLIFICATION-v1` 与 `UM-SHARED-CLONE-REPLICATION-COLLAPSE-v1` 的复制界。

## 先陈述重构

对任意已迁集合 `W`，机器 `i` 的负载确为

`S_i-D_i(W)+P_i(W)`。

若先迁 `R`，前缀受 `P_i(W)≤P_i(R)≤U−S_i` 控制；完成 `R` 后，`D_i(R)≥h_i` 给出

`S_i-D_i(R)+Q_i≤U`。

所以静态 cover 命题的两阶段顺序和所有机器的全程峰值证明成立。等端时间网络的下界 `ceil(h_i/q_i)` 与上界 `floor((U-S_k)/r_k)` 也与该命题逐项对应；带下界整数流的位复杂度是输入位长多项式。

## 独立攻击与修正

初稿曾把 hold-edge 说成静态命题的严格扩展。令 `A=R\\B` 后，若 `beta_k=0`，有 `P_k(A)=P_k(R)≤U−S_k`；若 `beta_k>0`，因 `R` 可能漏选一部分非保留目标任务，`beta_k>h_k` 给 `P_k(A)≤Q_k-beta_k<U−S_k`。因此 `A` 已满足静态 cover，hold-edge 只是在同一证书上的延迟执行重写，不能绕过静态 cover 失败。正文已改为 `RESTATEMENT` 并删除扩展性表述。等号 `beta_k=h_k>0` 也能给非严格 `≤U`，正文保留严格条件只是避免边界歧义。

两机三任务输入 `T=3/4,C=5/4,U=13/8` 的两个可能首步负载分别为 `7/4` 和 `2`，均严格超过 `U`；目标调度本身负载为 `3/4`，所以它确实反驳“任意给定 `sigma,tau` 都存在 `U`-峰值路径”。相反，三机六任务输入 `T=1,C=2,U=5/2` 的静态预算为 `1/2`，A 源只能通过 `3/5` 目标边，故任何静态 `R` 都失败；给定迁移次序的实际峰值为 `23/10`。这两个例子共同区分了“静态证书充分”“静态证书非必要”和“任意目标路径不总存在”。

复制界也通过独立重构。对共享同机 `k`-copy，任意整数调度按复制数除以 `k` 给 assignment-LP 下界 `O_k≥kF`；对 LP 最优 `x` 逐任务 floor/ceil 取整，机器 `i` 的额外量至多 `Σ_{j:p_{ij}<∞}p_{ij}`，故 `O_k≤kF+S`。该结论是固定实例的渐近身份；`k` 若二进制给出，显式展开本身有 `nk` 个任务，不能把超大复制直接当作位多项式归约。它不讨论阈值删边 configuration-LP，也不外推到任意 Kronecker/跨副本 gadget。

## 审查结论

当前稿在上述声明范围内没有尚成立的致命异议。可接受状态是：

* 静态 cover 是给定目标的位多项式充分桥；
* hold-edge 是同一桥的等价重排，不是新扩展；
* 两个显式例子给出必要性边界；
* disjoint union 与 shared-machine cloning 的反放大公式成立。

这些结果仍缺从任意 `P,T` 计算 `sigma,tau` 或 sound `FAIL=>OPT>T` 的机制，不能提升 `UM-TARGET-v1`。有限 `Fraction` 程序只核本页列出的输入和公式。
