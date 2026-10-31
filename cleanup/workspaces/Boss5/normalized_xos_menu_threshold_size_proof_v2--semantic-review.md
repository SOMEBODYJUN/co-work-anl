---
source_id: "6624c132790212150bac"
source_path: "history/source/notes/unrelated_machines/normalized_xos_menu_threshold_size_proof_v2.md"
source_sha256: "6208afa100822520502e368c1cf3814d6d5bd520e3fdaec363efc33961eb2d3d"
kind: "semantic-review-draft"
status: "read-compared-ready-for-integration"
---

# Proof v2 语义清洗稿：归一化 XOS 菜单的精确覆盖等价

## 来源与实读范围

这是 UM-NORMALIZED-XOS-THRESHOLD-MENU-SIZE-OBSTRUCTION-v2 的作者 Proof v2；来源明确没有实现或有限测试。本次用 clean show 完整读取，并与现有障碍对象、独立 Exact v1 审查、canonical v2 §4–6 和相邻分数重匹配对象比较。未运行程序，未读取二进制，也没有把作者稿当作一般 Santa Claus/UM hardness 证书。

## 精确模型

资源宇宙 U 有 2t 个资源，t≥1；固定 0<η<1，d=floor(ηt)，k=max(1,ceil(d/η))。菜单有 K 个 indexed 加性 clause，系数非负且每条 clause 在整个 U 上总和为 1，f(B) 是这些 clause 值的最大值。要求对全部 |T|=t 的集合有 f(T)=1，对全部 |B|≤d 的集合有 f(B)≤η。允许零系数与重复 clause；不引入辅助资源、玩家或全局耦合。

## 证明主线

令 A_s 为第 s 条 clause 的严格正 support，h_s=|A_s|。若某个 t 集由该 clause 达到值 1，因为总质量为 1 且系数非负，必有 A_s 包含于该 t 集。反向，包含 A_s 的 t 集使该 clause 取值 1。

tiny 条件强制 h_s≥k。d=0 时归一化直接给 h_s≥1。d>0 时若 h_s≤d，A_s 本身就是 tiny 集而 clause 值为 1，矛盾；若 h_s>d，取最大 d 个正系数，它们的总和至少 d/h_s，而 tiny 条件给出该和≤η，所以 h_s≥ceil(d/η)。不要求原权重 uniform，也不需要逐项权重上界。

对每条原 clause 从 A_s 选任意 k 子集 F_s，替换成 F_s 上均匀的 1/k。任何原来被它覆盖的 t 集包含 A_s，也就包含 F_s，故 unit 条件保持；h_s>t 的 clause 原来覆盖不到 unit t 集，可删去而不增加 K。新 clause 在任意 tiny 集上的值至多 d/k≤η，仍归一化。因此任意合法菜单可变为不增大小的均匀 k 子集菜单。

反向地，任意用 k 子集覆盖全部 t 子集的族 F，都可在每个 F 上放置一条均匀 1/k clause；每个 t 集得到值 1，每个 tiny 集的每条 clause 值至多 d/k≤η。因此最小菜单数恰等于覆盖数 Θ(2t,t,k)，即用 k 子集覆盖所有 t 子集的最小族大小。这个双向等价是表示定理，不是求覆盖族的多项式算法。

## 计数与端点

固定 k 集包含于 C(2t-k,t-k) 个 t 集，待覆盖的 t 集总数是 C(2t,t)，所以 K≥C(2t,t)/C(2t-k,t-k)。重叠、重复 support、重复 indexed clause 和全零 clause 只会浪费覆盖，不能改进下界。

d=0 时 k=1，精确覆盖数为 t+1：至多 t 个 singleton 留下至少 t 个资源，可组成未覆盖 t 集；t+1 个 singleton 则保证任意 t 集命中一个。若 ηt 为正整数，则 k=t，每个 t 集只能由自身 support 覆盖，精确值是 C(2t,t)，均匀 1/t clause 在 tiny 边界取等号。可行性不空：列出全部 t 集并各放一条均匀 1/t clause 即可。

## 固定 η 的输出边界

令 θ=ηt-d∈[0,1)。对 d>0，t-k=floor(θ/η)≤ceil(1/η)-1=c。于是分母 C(2t-k,t-k)=C(t+t-k,t-k)≤(2t)^c；中心二项式满足 C(2t,t)≥4^t/(2t+1)，从而 K≥4^t/((2t+1)(2t)^c)。原加性玩家可用 2t 个资源、每项 1/t 的 O(t log(t+1)) 位输入描述；固定 η 时显式列出 indexed clauses 仍超多项式。这里没有把资源数指数误写成输入 bitlength 上的 2^(Ω(L))，也不把 η 变化时的常数偷换成固定常数。

## 与既有对象比较和独有内容

这不是新模型，而是现有 归一化 XOS 菜单阈值规模下界 障碍对象的作者 Proof v2 来源。现有对象已记录 r=d+1 的基础 covering bound、k=ceil(d/η) 的精度修正、余数分析、端点和 bitlength 边界，并有独立 reviewer 重构。该源最适合作为同一对象的版本 provenance，不应新建第二个 theorem。

可补入既有障碍正文的独有内容是：逐 clause 选 k 支持并保持 unit/tiny 的双向均匀化等价；支持大于 t 的 clause 可删除；原权重无需 uniform；显式可行菜单构造；以及“覆盖等价不是算法”的明示。原文件与本语义稿应进入同一 normalized-xos evidence 目录，正式对象链接保持唯一。

## 严格范围

结论只针对同一资源宇宙、逐玩家、非负、每 clause 总质量为 1、对全部 unit/tiny 集合保真的显式 XOS。它不推出一般 Santa Claus 或不相关机 NP-hardness、近二下界、UM-TARGET 反例、六人客户 SPE 结论，也不覆盖辅助资源/玩家、reachable-only 保真、unit 有损、未归一化 clause 或另有证明的隐式表示。

## 处置

语义状态为 integrated（已完整实读、全仓比较、独有内容定位）。数学对象沿用既有障碍；由 Boss 先把正文和本稿及原件 evidence checkpoint 推送，再提交该源的 done。本代理不执行 Git 或 done。
