# v2 正式 Exact 的独立重构后攻击

2026-10-18。先冻本人 `independent_general_lp_v2_reconstruction.md` SHA256 `7beb7a1f4a75414758942e2a87378ccb6ecb1ad81fd5fe8af5fcdeb01a329113`，随后同一工具调用才实际全文读 `../near_two_reduction/gated_weighted_menu_general_ratio_exact_v2.md` SHA `4dd1cff4786ffbccda5ee1bdedc18a34ba9b5c6408829c57e70ba4f92609c04a`。未读 v2 作者 Proof，未查看 root 的有理反算。

结论：§1–6 未发现 fatal。正式 LP 与本人先行构造的区别仅为组 state 质量等式而非≤1；将本人 null 质量改放任意原 state、其所有 claims 为零即可，目标与可行 x 不变。本稿不能冒称此前已读此等式版本，现差异已实际核对。

## 1. W*≤L 与 LP 全可行

任取实际 welfare allocation，为每组取一个 attaining state，使该 state 的 z=1，其余 z=0；该组 bundle 内所列正 incidence 的 x=1，余下0。各资源最多一个 owner，故满足容量，且 LP objective 恰为该 allocation 的福利。故 W*≤L。各组可任取一个 state z=1、全部 x=0，给明确总可行基线。归一化与 x≤z 给 L≤n。零 incidence 固定 x0 不影响实际 welfare 或物理 job。

## 2. 不依赖 FSLP 的随机 claims 与位长

正式分布每组按 z 抽一 state，正 incidence conditional probability x/z；初始每资源被正 claim 的概率和是 sum x≤1，而非 sum z。期望的 selected-state 福利 contribution 是 sum p*x=L。组内 claims 共享 state 不损害跨组独立。

实际 CDF 公式中未固定组 tail 是 sum_{s:p≥t}x；固定 state 的 tail 是 1[p≥t]x/z。全部状态固定后再将当前 selected incidence coin 变为0/1，逐步条件期望不降。初始的 Σtail≤1 不必在每个 conditional prefix 成立；算法仅在初始下界使用它。所有原 thresholds、z、x、x/z 都有多项式有理位长；候选总数 O(S+I)，不枚举指数个 subset 配置。正式 Exact 正确包含 z=0⇒x=0 和不作0/0。

## 3. 任意 allocation 的 balanced bound

w=W/n∈[0,1]。w=0 时结论显然；w=1 时所有 r=1、取全部组得 β_hat=1。其余取 b=1−sqrt(1−w)∈(0,1)。若 h=#{r≥b}≤bn，则因剩余组严格小于b，W<h+(n−h)b≤(2b−b²)n=wn=W，矛盾。所以 h>bn，该 top-h candidate 给 β_hat≥b。无比例整除或有理比较问题，b仅分析使用。

最优 balanced witness 只在 H 上收质量≥β*，其数≥β*n；向空余组给空 bundle 构成全 allocation，故 W*≥n(β*)²。这个补空步骤不可解释成删除其物理 jobs；真正排程稍后全回填，Exact 已明确。

## 4. 13/8 全类比例与全部 jobs

本人先行稿给纯有理反算：B=β*≤10/13 时 baseline C≤2够；B>10/13 时 b=(13B−10)/8，

(5/8)B²−(2b−b²)=(209B²−468B+260)/64≥1/64。

配 W>(5/8)nB² 迫 h_b>bn，因此 β_hat≥b，C≤2−β_hat≤(13/8)(2−B)。算法从未读 B。等式价值 OPT=2−B 的任意低调度 decoder 已在 v1 正式范围内独立核对，v2 没有改矩阵，故可在 v2 中明示沿用，而非冒称独立审过另一矩阵。

原 connector 固定自己的 gate；对 top-k 恰移动其自身 C_g，其 selector 去新 attaining state。资源重选仍只用该组原 B_g，跨组不交；所有未选 states/未激活 groups/零 incidence 全留原 private，root 负载2−k/n，gates1，所选 private2−r_g，其余 private1，resource≤1。所以全机证据保留。

## 5. 归属与尚待证据

本 LP 是显式 XOS configuration welfare LP 的 polynomial lift；state-dependent系数最大值舍入已在 DNS 作者稿§3.2 Theorem3.2/Lemma3.3 出现。这里不以‘一般LP新变量’宣称新的福利机制；具体 gated 类 whole-instance ratio、完整作业身份、旧γ纠错仍须与公开文献比对，未认证 novelty。

正式 Exact 的未运行声明诚实；通用 rational LP solver 未实施不妨碍数学 bit-poly 算法合同，但有限实现不能冒称已执行该 optimizer。本次仅一般证明审查，未跑有限测试，尚未读 v2 作者 Proof。
