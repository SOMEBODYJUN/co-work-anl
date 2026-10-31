---
source_id: "c357f938944fbee92d56"
source_path: "history/source/notes/unrelated_machines/sol_general_repair_shared_ud_O1k_v5_final_actual_read_v1.md"
source_sha256: "7492f4151f292456dda4612f73afa704bac2e710d873cae542667f65268e0360"
source_size_bytes: 6344
status: "integrated-version-read-after; no-new-software"
disposition: "integrated"
targets:
  - "archives/unrelated-machines/state/审查/全局行基数过滤与多外层单态小home双源审查--审查.md"
  - "archives/unrelated-machines/tools/evidence/multi-outer-tiny-home-author-proof-v1-20261031/"
---

# 来源身份与实读范围

`clean show c357f938944fbee92d56` 完整读取 6344 字节的 v5 final actual-read 记录。该文件是对 `multi_outer_single_state_tiny_home_rounding.md` 第 21–27 节（原文件 52640 字节、486 行；整篇 SHA `f91b32aba8da447fb0838849fb1a63a1d48296b96e5bb156646eb01c67c27aec`）的知情作者后置复核，新增后缀 104 行/11122 字节，后缀 SHA `b424b1bc66afac3913fa8e1e39bdd160b4e91bf677de4bc9202a9337a9a1d65f`。旧 1–382 行只作哈希确认，不构成本源的重新全文审查。

作者说明此票是作者读后 final-read，不是 fresh/blind，也没有在本轮打开新链接、软件、运行 JSON、NSW 437c 或其他未读材料。正确证据等级是“限定域后置数学核验”，不能写成独立实现、端到端运行或外审。

# v5 的限定域与精确结论

v5 另立 `UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v5` 身份。输入是 normalized-flat typed 域：每个 outer 只有一个 state，home 全局物理互异，每 home 有一个 own-unit helper；允许 shared B-only fallback 和额外 exact-threshold UD 叶。k≥2 时最大正 home 权重满足 \(\nu\le1/(1024k)\)，k=1 另有不设 tiny 的实际-I 分支。不存在一般 UM、multi-state outer、home 重合或任意 non-UD extra groups 的扩展。

算法目标是确定性位多项式、输出全部原 jobs 的 \(19/10\) 实际 makespan。固定叶阈值 ε=15/16；可靠 FAIL 使用 \(r=18/19\)，二者不混用。无叶 matching 时只推出 \(V<\epsilon<r\)；终点某坐标过低只推出 \(V\le r\)，该弱等号已足够使 baseline 峰值 2 满足 \((19/10)(2-r)=2\)。成功阈值 q=19/100 给 Good mass 至少 1/10。C<2 的 normalized-flat OPT=2−V decoder 与 C≥2 的平凡 baseline 分支均沿用既有合同，不扩域。

## 证明承重内容

1. **实际 I 与 matroid 候选。** vacancy \(M\) 定义为 \(D\subseteq B\) 当且仅当 \(B\setminus D\) 可匹配全部叶；positive incidences 作为 parallel copies，检查 resource 不重复。每个 helper 至多一个原 fallback state，其他 helper 只丢旧项，不换原 state。
2. **全局共同参考。** weighted-rank 次模求和给出 \(hL^*\le 2hL+\sum\delta_j\)。参考 allocation 同时提取给全部 outer，因此各 \(L_i^*\ge V^2\) 可共存；没有把每个 outer 的 bundle 复制成不同全局见证。
3. **相对余项与势。** §24 分别付倒数/线性 reciprocal remainder、tangent dominate、线性→倒数二次余项和零余项；\(m^2\le2k\)、\(\nu h_{max}\le1/8\) 保证每个实际候选步合法。停止求和每 helper 付 \(\tau/N\)，总和为 \(\tau\)；\(\sum w_j^2\le\nu\) 和 h 上界用于 Cauchy 余量。文件给出净系数 `2334307/102921100`、最小余量 `59552417/20584220`、势范围 `808k²/25`、每步增量 >1/(100N)，接受次数 <3232k²N。
4. **k=1 分支。** h=1、\(\Phi=L\)，不使用相对二次界或 prefix loss；接受步 <100N，终点比较 `(A−τ)/2=32039/72200>q`，覆盖 \(\nu=1\)。
5. **全任务回填。** Good 的 I 子集仍 M-independent，补一次共同完整叶 matching；非Good helpers 回 own，所有 zero/inactive/duplicate jobs、selector、selected-state 和其他 incidence 保留且每个 job 恰执行一次。成功时 home ≤19/10、inactive ≤1；失败时全 private baseline ≤2。counts 为 S+U、G+I、S+2I。
6. **source 边界。** 只针对整个像均在 typed 域的 NP reduction 给固定 γ∈(0,.1) 的 1.9/2 区分；multi-state outer、home overlap、non-UD extras、general normalized-menu 和一般 UM 仍 OPEN。

# 与已有对象和证据的比较

现有《全局行基数过滤与多外层单态小 home 双源审查》已承接 row-count filter、紧凑趋二反例族和 v1/v4/v5 版本；本源独有的是 v5 新增 §21–27 的实际-I、matroid rank、relative reciprocal 势、O(1/k) home 常数、k=1 分支及完整回填/位复杂度说明。它与早期 v1/v4 的证明身份不能合并：v1 是 1/(4096k⁴) CDF/MW 域，v4 是 1/(16384k²) shared-UD/FW 域，v5 是 1/(1024k) actual-I 域。

本轮没有运行算法、matching backend、LP、profile search、prefix-flow 或全 jobs end-to-end；不能把作者的 PASS 写成软件证书。`UM-TARGET-v1` 仍 OPEN，也不与六人 Q-CAG-HALF/SPE 模型相连。

# 处置建议

将本源 `integrated` 到已有多外层审查对象，保留本文件作为版本 read-after 证据；原件指纹与新增后缀 hash 进入对应 evidence manifest。后续第三阶段应把“作者读后核验→v5 限定算法”作为 provenance/审查边，不把它误连成一般近二算法或六人 SPE 结论。
