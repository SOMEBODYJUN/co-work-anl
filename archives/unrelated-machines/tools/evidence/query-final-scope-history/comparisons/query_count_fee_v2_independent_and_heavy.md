# UM-TWO-WITNESS-QUERY-COUNT-FEE-v2：Exact-first 独立审查

审查者：boss11 内部 typed_edge_gap，2026-10-18。先只读 `two_witness_query_count_fee_v2_exact.md`，未读本计数合同的作者证明文件。使用此前已经独立核实的一般双见证固定 I>T/2 染色算法。

**结论：Exact v2 全部数量界与费用界成立；η=0 必须分开，本文按 v2 分开。** 下面另给一个从这些界独立推出的“绝大多数 query 必须初态近 unit”必要条件，明确不把它冒充原 Exact 字句。

## 1. 坏颜色注入 rich machines

设 c=β−1∈[1/2,1)，LQ_i 为全部 Q 在 σ0 机器 i 的原负荷，rich 集合 R={i:LQ_i>cT}，其大小为 Rβ。沿用一般定理得到的 owner 颜色及同一族 A_q、τ_q，不重新染色。

可直接选择

\[
 G=\{q\in Q:\text{没有 rich 机器的 owner 为 }q\}.
\]

每台机器只有一个 owner，故删去的 query 颜色数≤Rβ，|G|≥d−Rβ。对 q∈G：未标 q 的机器负荷≤3T/2≤βT；标 q 的机器都不 rich，其剩余其它 queries 原负荷≤LQ_i≤cT，故负荷≤T+cT=βT。因此 G 全部合格。也可算出所有 τ_q 的真实负荷以选取更大的合格集合，但不必这样做。

支持不交给 Σ_{q∈G}fee(τ_q)≤W。Rβ<d 时 G 非空，平均费≤W/|G|≤W/(d−Rβ)。这证明第一项，无须新增全局调度假设。

## 2. 单件 η 界、严格计数和整数界

η=0 时 LQ_i=0 全部 i 成立，所以 Rβ=0、所有 d 个 queries 合格，平均费≤W/d。不使用“严格多于d”。

以下设 0<η<c。每 rich 机器满足 LQ_i>cT，而全体 query 原质量总和≤dηT。因此

\[
 cTR_β<dηT,
 \quad R_β<(η/c)d.
\]

Rβ=0 时严格不等式仍成立，因为 η,d,T 为正。于是

\[
 |G|\ge d-R_β>(1-η/c)d>0,
\]

整数至少 floor((1−η/c)d)+1。用 Σfee≤W 平均，即得到 Exact 的非严格费用≤W/[(1−η/c)d]。W=0 时保持≤而不误写严格<。

令 s=floor(c/η)+1。每 rich 机器上的 query 数 n_i 满足 n_iηT≥LQ_i>cT，所以 n_i>c/η，整数 n_i≥s。不同机器的 queries 不交，因此 sRβ≤d，Rβ≤floor(d/s)，|G|≥d−floor(d/s)。因 η<c，s≥2，故后者≥ceil(d/2)。所有相应平均费用界成立。

## 3. 物理收费合同的准确推论

若合同确实要求每个 load≤βT 的合法单 query 模式都支付非 query 指定改派费至少 F>0，那么每个构造 τ_q（q∈G）都受该收费要求约束。故

\[
 W\ge\sum_{q\in G}fee(τ_q)\ge|G|F\ge(d-R_β)F,
\]

以及 (3) 的整数界。不能把相对 σ0 的改派/新增 unit 费 W 换成扣 baseline 退款后的净费用。也不能把别的实例的 strict 见证或未知 σ1 当作本合同输入。

## 4. 更直接的必要逃逸：多数初态 query 必须 > (β−1)T

这是本次独立追加的推论，非原 Exact 的另一个假设。令

\[
 H=\#\{q\in Q:p_{σ_0(q),q}>cT\},\qquad S=d-H.
\]

每台 rich 机器如果含初态 heavy query，可以归给其中一个 heavy（机器间不重复）；若不含 heavy，则它必须含至少两件 queries，否则质量≤cT。因而

\[
 R_β\le H+\lfloor S/2\rfloor,
 \qquad d-R_β\ge\lceil S/2\rceil.
\]

收费合同遂迫使

\[
 \boxed{W\ge\lceil(d-H)/2\rceil F.}
\]

若 all-on 的对应新增/改派费 W≤κF（κ≥0 为固定数），必要有

\[
 H\ge d-2\lfloor κ\rfloor.
\]

特别真正“一次F给任意多个查询共享”的 W≤F 合同，必须至少 d−2 枚 queries 在 strict off 状态的单件 old processing time 超过 (β−1)T。β=2−ε 时，这就是至少 d−2 枚 old size > (1−ε)T，已经不是单件 tiny 查询。这个必要条件不需要限制 query 在同机的 aggregate，也不依赖 home/单正端/unit 分类。

若统一单件界 η<c 已给定，则 H=0，W≥ceil(d/2)F；η 更小时 Exact 的 s 界更强，W≥[d−floor(d/s)]F。特别 d<s 时全部 d 个 queries 合格，W≥dF。

因此，在保持同一 P 的两 strict 见证、真实指定改派/新增费对象及 load 阈值 β≥3/2 的前提下，常数次 fixed-fee 共享必须让几乎全部被读 queries 的初态单件大小接近 T。否则只能退出这些具体前提之一；本推论并不排除其它费用对象、无同一 strict 见证、或初态近 unit 的机制。

## 5. 位复杂度与状态

已有染色算法是 det bitpoly。LQ_i、rich 标记、owner 筛选及有理费用平均均为多项式次有理加法/比较。s 由一次有理商取整计算，虽数值可大，但其位长为输入位长量级；不迭代 s 或 1/η。T>0 是本 count 合同的域，故除 T/c 的推导合法。没有读取本合同作者 proof，没有运行新代码审计，没有 Work/Git 写入。
