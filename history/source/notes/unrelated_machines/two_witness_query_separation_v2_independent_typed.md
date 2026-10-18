# UM-TWO-WITNESS-QUERY-SEPARATION-v2：3/2 锐性独立构造

审查者：boss11 内部 typed_edge_gap，2026-10-18。先只读 root 的 `two_witness_query_separation_exact_v2.md` 精确陈述，**未读 root 作者证明**；随后独立构造如下。v1 上界已在另一份独立审查中重构通过。

**结论：v2 新增锐性成立，而且下面实例的 soundness 对所有实际 schedules 成立，不仅对 σ0/σ1 hybrid 子类。**

给任意有理 η∈(0,1/2]、B∈[1,3/2)。令

\[
 a=(B+1/2)/2.
\]

则 0<a<1，且 a+1/2=(B+3/2)/2>B。

## 显式实际 P 与两个严格见证

机器恰为 H,T1,T2,F,R。jobs 恰为 q1,q2,b1,b2,f。下表未列的端全为∞：

|job|唯一正小 home / time|另一有限 unit 端 / time|σ0|σ1|
|---|---|---|---|---|
|q1|R，η/2|T1，1|R|T1|
|q2|R，η/2|T2，1|R|T2|
|b1|H，1/2|T1，1|T1|H|
|b2|H，1/2|T2，1|T2|H|
|f|H，a|F，1|H|F|

Q={q1,q2}。所有 jobs 都恰二端、拥有唯一正小 home、其它有限端为 unit；所有有限时间≤1。baseline 的 b1,b2 已经预先 SU 导出，这正是旧 all-home baseline 合同未覆盖的情形。

σ0 各机负载为 H=a，T1=T2=1，F=0，R=η，故 Cmax=1。σ1 各机负载为 H=1，T1=T2=F=1，R=0，故 Cmax=1。每机 queries 的初始总量≤η（只有 R 非零，恰为η）。

## 每个 singleton 都必须开启同一 fee job

固定 i∈{1,2}，要求 q_i 使用其 σ1 unit 端 Ti，其余 query q_{3−i} 使用 σ0 的 R。考虑任何使 Cmax≤B 的实际 schedule；因每 job 只有表列二端，这也等于 Exact 要求的 hybrid 域。

q_i 在 Ti 的处理时间为1。如果 b_i 仍放 Ti，则该机负载为2>B，故 b_i 必须回 H，贡献1/2。如果 f 仍在 H，则 H 负载至少

\[
 a+1/2=(B+3/2)/2>B,
\]

故 f 必须移到 F 的 unit 端。此论证不依赖另一个 b job 的选择，且即使允许另一个 query 也导出，结论依然成立。

存在这样的 singleton strict schedule：q_i@Ti、b_i@H、f@F，另一个 b 留其 T 端，另一个 q 留 R。其峰值为1≤B；所以这里不是通过 singleton 不可行取得 vacuous soundness。

给非 query 权 w_f=1、w_b1=w_b2=0。baseline 物理收费恰0：f 在 small home；b_i 虽已 unit 导出但权0。每 singleton 都必须新开 f，费用恰1；all-Q 见证 σ1 也只新开 f 一次，费用1，无 baseline 退款抵销。两个 singleton 若都满足峰≤B，其 A_q 都包含 f，故不可能两两不交。

## 位复杂度与准确范围

实例规模恒定5机5 jobs；η/2 与 a 只做常数次有理加法、除2，编码长度为 O(bits(η)+bits(B))。B=1 同样成立（a=3/4）；当 B→3/2 取下方有理值时，a→1 但始终为严格正小端。

这证明一般双见证查询分离/费用合同的 3/2 常数不能统一降低，即便 query 初始 aggregate 任意 tiny。它不证明 ordinary UM 的任何近似下界：本实例 OPT≤1，而且所有 singleton 也各有 load1 见证，只是它们必须共享同一个 fee job。该 shared-fee 逃逸只发生于所测试 B<3/2，不是 near-2 gadget。

## Read-after 作者证明核对（独立稿冻结之后）

上述独立实例与证明已经先写入本文件，且已向 root 发出独立构造完成消息；随后才读取 `two_witness_query_separation_proof_v2.md`。该文件明确对应 UM-TWO-WITNESS-QUERY-SEPARATION-v2；未将 v1 上界冒充 v2 新增锐性。作者用六机、两个分开的 query homes，与本独立五机实例等价；本实例把两个 query homes 合并为 R，并将每个 query 旧时间设η/2，故 aggregate 恰η，严格模式与 singleton 可行性均保持。

作者一般证明以 I_i(q)>T/2 直接触发；我的先行独立证明以 baseline_load_i+I_i(q)>3T/2 触发。两者都是合法的闭包算法并给相同合同界；后者阈值可能更保守，但 owner 唯一与终止后的上界仍完整成立。未发现作者证明的域/量词偏移、基线付费混淆或 T=0 漏洞。

作者锐例取 γ∈(0,min(1/2,3/2−B)) 并令 fee small time=1−γ；我的参数 a=(B+1/2)/2 对有理 B 直接给同一严格不等式。Exact 声明 B 为有理输入时，两者字长均多项式。若另把 B 当实常数，仅需选区间 (B−1/2,1) 内任意有理 small time；不应把实 B 的公式当作有限二进制输入。

最终复核结论不变：3/2 是这项给定双见证查询分离/改派费合同的统一阈值锐性；不是一般 UM 近似比硬度，也没有产生 YES≤1/NO≥3/2 的 OPT gap。
