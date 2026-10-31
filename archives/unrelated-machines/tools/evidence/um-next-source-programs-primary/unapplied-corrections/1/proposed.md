---
id: "unrelated-machines/optimal-hull-long-chain-and-private-sink-two-source-review"
kind: "review"
type_tag: "审查"
title: "最优凸包长链与私有汇点边界两源精读"
status: "restricted-convex-hull-barrier-read"
summary: "两份 optimal-hull review 确认不同受限障碍：长链族在显式最优凸包点上对严格 lex 改善需改变 Ω(d) 任务/机器，但存在 Cmax 非增修复；私有汇点族在常数行负载/计数合同下 supremum 精确为2，并在固定边际与同 sink pairwise 条件下给期望/尾界。两者都不提供一般 UM hardness 或算法。"
source_refs:
  - "clean:704e41e5911efe317744"
  - "clean:d7ea60675d8f563250cd"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/optimal_hull_long_chain_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/optimal_hull_marginal_review.md"
---

# 来源与范围

`704e41e5911efe317744`（SHA `62bbfd90f4accc6693e19fac024e2031baf530b7dd00a3305aa5b4988d000393`）审 `UM-OPT-HULL-LONG-CHAIN-LOCAL-GAP-v1` 的第10节、规范/独立代码与完整有限枚举；`d7ea60675d8f563250cd`（SHA `7789909f4c9ac7f3e3c718a747d19d321ecfc8a92920c4d565a53806804c744c`）审私有汇点 row-contract 与 marginal/pairwise 负相关边界。两源均 clean show 全文实读，原件与 manifest 在 `archives/unrelated-machines/tools/evidence/optimal-hull-20261031/`，receipt 草稿在 `cleanup/workspaces/Boss2/optimal-hull-receipts-20261031.json`。

# 1. Long-chain local convex-hull lex barrier

对任意 `k≥3,d≥1`，显式 UM 子族每个 job 恰有两台可用机器，两个最优调度 `S0,S1` 的凸分解 `x=δS0+(1−δ)S1` 为真实 optimal-hull 点，`δ=1/k`、链长度 d、macro/tiny 任务均正有理，OPT=1。ST 槽交定义采用正交长，平局次序固定，输入规模显式多项式。

每个 root/chain home 负载由 `a=1−1/(2k)` 构成；若实际输出 `Cmax≤2−δ`，下传比特只能形成后缀，rootjob 离根则强制整条链下传。没有新 rootjob 离根时，旧 active 链不能返回 root；其它链仅可迁移后缀，排序向量不减，故严格 lex 改善至少激活一条新链。该链改变至少 `d+1` 个任务和 `d+2` 台机器；另有一条 tiny 链可达到该下界。该证明覆盖任意合法实际重分配，不能缩成净负载变化计数。

最优槽/成本分解表明全部最低成本 cover matching 诱导唯一实际机器分配：至少一个 rootjob 离根，tiny activation cost `c_t=(d+2k−2)/(2k)>0`，macro cost 更大；因而最低成本输出激活恰一条 tiny 链。此局部 lex 障碍不排除其它初始化或直接返回 optimal 分量。

同一族存在 weak-Cmax 非增修复：沿 inactive tiny 链从 sink 逆序下传，前 d 步峰值不增但 lex 变坏，最后一步峰值下降 δ；依次激活其余链得到 S0。因此该障碍只针对严格 lex 局部改进，不是 Cmax 单调路径困难性或一般近二 hardness。

规范与独立代码采用 Fraction，完整读跑；规范覆盖 k=3…8,d=1…4 与边界案例，独立脚本逐合法 assignment 计数，第三份 reviewer enumeration 直接核 ST cover matching。有限枚举支持已列参数，不替代一般证明或实现全域。

# 2. Private-sink marginal row-contract barrier

对 a,b≥1 的逐行合同 `L_i≤a ell_i+b M_i`，一般 ST 槽匹配给所有真实最优凸包点 x 一个 assignment：每机槽数 `ceil(N_i)`、负载≤`ell_i+M_i≤2OPT`，因此域非空且普遍比率上界2。计数合同 `count_i≤ceil(N_i)+b0` 同样非空、上界2。

下界族：一个 big job B 只能去 r 个 home `H_i`，每组 k 个 small 只能在 `H_i` 或私有 sink `Z_i`、两端时间1/k。最优调度把 B 放某 home、整组 small 移 sink，OPT=1；均匀平均 x 是真实 optimal-hull 点。若 B 位于 `H_h`，row 合同至多允许 `q=min(k,floor(ak/r+b))` 个该组 small 去 `Z_h`，故实际最优 makespan恰 `2−q/k`。取 `r=k²`、k→∞，任意固定 a,b≥1 的 supremum 精确为2；计数合同类似 `q=min(k,1+b0)`。

任意 `C≤2−ε` 输出必须将至少 `ceil(εk)` 个 h 组 small 集中到 `Z_h`，因而 `L_Zh` 相对其均值 `1/r` 获得无界倍率；但这是输出必要条件，不排除换 x、正相关集中迁移或其它算法。有限枚举核对小 `(r,k)` 全 assignment、行/计数合同和集中迁移条件，不能替代一般证明。

固定 x 的 pairwise-negative marginal 条件下，若同一 sink 不同 small 满足 `E[Y_itY_iu]≤1/r²`，则

`E C≥2−1/k−(k−1)/(2r)`，

且 `Pr(C≤2−ε)≤k(k−1)/(r q(q−1))`，其中 `q=ceil(εk)≥2`。显式对称联合分布达到相应期望/尾界（分别 sharp），但不排除具有正相关集中迁移的最优混合。

# 3. 关系、实现和来源边界

长链障碍控制最优凸包中严格 lex 的局部支持变化；私有汇点障碍控制已给边际/行合同下的实际集中迁移和真实 OPT。二者的输出空间、量词和负载合同不同，不能合并成一个一般 UM lower bound。与 ST/SV 经典例比较时，本文明确凸包点有真实最优分解，并保留私有 sink/相关迁移差异；不作全球优先权认证。

本批实际重跑了指定 Fraction/整数审计和有限全分配枚举，未声称生产实现。外审、全球新颖性、一般 UM `2−ε` 算法/硬度、最优凸包点求解与当前六人 SPE 目标均未解决。引用时须保留 strict lex vs weak Cmax、a,b≥1、row/计数合同、固定边际 pairwise 条件和私有 sink 完整邻域等前提。
