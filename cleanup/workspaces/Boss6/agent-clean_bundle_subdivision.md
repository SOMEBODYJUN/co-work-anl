---
id: "unrelated-machines/bundle-coupling-subdivision-pre-cross-reference-version-review"
kind: "review"
type_tag: "审查"
title: "成束耦合细分边界前置源版本核对"
status: "integrated-as-pre-cross-reference-version"
truth_status: "same-conditional-results-as-integrated-barrier-review; no-new-theorem"
review_level: "full-source-read-and-byte-level-version-comparison"
scope: "history/source/notes/unrelated_machines/bundle_subdivision_pre_cross_reference.md; comparison with later cross-referenced barrier source and integrated review"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/bundle_subdivision_pre_cross_reference.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/bundle_subdivision_pre_cross_reference.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/bundle_coupling_subdivision_barrier.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/bundle_coupling_subdivision_barrier.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/bundle_subdivision_review.md"
legacy_source_ids:
  - "0523719ad5957d736c5f"
  - "662f60ef16911ee431c3"
source_sha256:
  "0523719ad5957d736c5f": "f923212d74e42ac3b32c09d73e15382dd656e90e10b39ea22bc4fa29559cd894"
---

# 阅读与版本核对

本源 0523719ad5957d736c5f 已用冻结 clean show 全文读取，实际字节数 14,900，SHA-256 为 f923212d74e42ac3b32c09d73e15382dd656e90e10b39ea22bc4fa29559cd894。它是《成束任务的二阶相容性、计数传播与细分障碍》的前置版本；冻结来源在 legacy-cleanup 提交 68fad804ec5946cb296f77dc5b336308a66abf12 与 main 提交 aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c 均保留同一条历史路径。

为避免把现有正文误算为本源的独立新结果，将本源与其后带交叉引用的同题源 662f60ef16911ee431c3 做了冻结字节比较：

- 前置源：14,900 字节，SHA f923212d74e42ac3b32c09d73e15382dd656e90e10b39ea22bc4fa29559cd894。
- 后置源：15,254 字节，SHA bbbfb292f4ce3cd02eb87864524add850075f20b938f3b9aaef0a2e54b765222。
- 前 145 行及全部数学段落逐字相同；后置源只在末尾追加 UM-LONG-PATH-GAP-v1 与 UM-COALITION-PROJECTION-GAP-v1 交叉引用及“长度2重构不另报独立反例”的版本说明。前置源因此不含该后续关系信息，但不缺少二阶矩、闭包、pair coupling 或细分证明。

现有《双见证批量插值与成束耦合细分边界双源审查--审查》已经完整整合后置源 662f60ef16911ee431c3，并保留三身份的稳定合同。本源的数学内容应并入同一审查对象作为前置版本证据；不应创建另一个重复的 UM-* 身份。

# 数学内容实际承重

本源的三个稳定对象及其严格范围如下。

1. **UM-BUNDLE-MOMENT-v1（条件性实例族定理）**：对经典两树、每个末端父机和终端机之间的 k≥4 条平行任务束，父端时间 1/k、终端端时间 1，加入二阶互补恒等式
   E[binom(k-N_u,2)] = E[binom(N_v,2)].
   当 T<2−1/k 时终端配置最多含一条束任务，互补等式迫使父端正质量配置至少含 k−1 条，故 incoming 时间1不能同居；自底向上将根间任务两端均逼为0。T=2−1/k 的已知整数路径调度给出紧性。源还给出旧配置点被切除的聚合残差 (k−2)/2。该结论只针对该 k≥4 族，不是一般 hierarchy 强度定理，也没有给指数配置 LP 的多项式求解器。

2. **UM-CARDINALITY-CLOSURE-v1（安全但不完备的过滤器）**：对任意合法有理输入 P,T≥0，维护任务候选域，按单域强制负载、二域束余量和 p_ij+F_i^¬j+Σ_{v≠i}r_iv^¬j>T 同步删边。每轮删除保持所有 T-可行调度的边，单调闭包在输入位长多项式内终止；整数缩放后二分给出数值下界 B≤OPT。接受不代表可行、不输出调度。无平行任务的初态二域中所有 r=0，可能无第一条删除；这是明确不完备边界。

3. **UM-PAIR-SUBDIVISION-GAP-v1（局部 pair 松弛的障碍）**：机器图简单二部、每任务恰两台可选机时，逐机器对的配置联合约束不能形成全局联合分布；单共享任务时乘积拼接足够。把每个原任务细分为两个旧端子任务并接入一个容量 H 的中间机，满足 min{OPT(P),2H}≤OPT(P′)≤max{OPT(P),H}。对经典两树取 H=1、T_k=1+1/k，提升原配置证书而得到 OPT/T_PAIR≥(2−1/k)/(1+1/k)=2−3/(k+1)→2。细分后的计数闭包在该阈值初态无首删。未声称 T_PAIR=T_k、一般 hardness 或对 UM-TARGET-v1 的否定。

这三条内容与后置源和现有审查正文数学相同；唯一独有信息是它保留了没有长链/coalition 交叉引用的历史版本状态。长链对象由后置版本及独立审查承接，不从本源倒填。

# 与既有对象、证据和后续工作的关系

- 正式数学去向：现有 archives/unrelated-machines/state/审查/双见证批量插值与成束耦合细分边界双源审查--审查.md 已包含后置同题源的完整承重证明；本源可在其 frontmatter/source table 中作为前置版本补充，或由本文件作为版本核对附件链接。不要复制三条 UM-* 身份。
- 账本去向：cleanup/workspaces/Boss6/CLAIMS.md 的 UM-BUNDLE-MOMENT-v1、UM-CARDINALITY-CLOSURE-v1、UM-PAIR-SUBDIVISION-GAP-v1 已记录正确量词和障碍；本源只需作为 legacy_ids/version evidence，不能再增加结论。
- 证据去向：evidence/runs/unrelated_machines/bundle_subdivision_audit.json（inventory id 528f36466ffc7a22d79e）和 tests/audits/unrelated_machines/pair_coupling_subdivision.py（inventory id e285a5c5428b9f209e67）只支持有限证书/穷举回归；一般结论仍由上述数学推导承担。独立审查 research/reviews/unrelated_machines/bundle_subdivision_review.md（inventory id d5e1b5b40e6c407f5b41）用于版本、范围与异议。
- 交叉关系：后置源追加的长链/固定 coalition 交叉引用由 UM-LONG-PATH-GAP-v1 与 UM-COALITION-PROJECTION-GAP-v1 正式对象承接；本源本身没有该追加文字，不应伪造其原始来源已读到后续对象。
- 主目标边界：本源及其后置版本都没有提供未知见证搜索器、一般近二算法、一般 NP-hardness、三机全局联合分布或 UM-TARGET-v1 的结论。下一步义务仍是跨容量一中间机保留多端信息、或给出全局一致性/消元/相对 OPT 分析。

# 建议处置与回执

建议将该源标记为 integrated（不是 duplicate）：它是后置源的前置历史版本，完整数学内容已进入同一稳定审查对象，但其 SHA 与版本关系仍应记录。receipt 建议：

- source_id: 0523719ad5957d736c5f
- source_sha256: f923212d74e42ac3b32c09d73e15382dd656e90e10b39ea22bc4fa29559cd894
- disposition: integrated
- read: full
- compared: full
- unique_content_accounted_for: true（独有为前置版本/无长链追加；数学段落与后置源重复）
- target_objects:
  - unrelated-machines/bulk-witness-interpolation-and-bundle-coupling-subdivision-review
  - unrelated-machines/bundle-coupling-subdivision-pre-cross-reference-version-review
- evidence_paths:
  - archives/unrelated-machines/state/审查/双见证批量插值与成束耦合细分边界双源审查--审查.md
  - archives/unrelated-machines/state/审查/成束耦合细分边界前置源版本核对--审查.md
  - archives/unrelated-machines/tools/evidence/long-path-marginal-20261030/source-manifest.json（for later cross-reference only; do not attribute to pre-cross-reference source）
- notes: 完全实读；与 662f60ef16911ee431c3 逐字比较，前 145 行/全部数学相同，唯一版本增量是后置长链/coalition 交叉引用；不新建 UM-* 身份；未将有限 audit 升格为一般结论。

# 未完成/接续

本源清洗的完成仅表示版本和数学处置准确；UM-TARGET-v1 仍开放。第三阶段应把“前置源 -> 后置源 -> 长链/coalition 对象”的版本关系作为证据边，不能把前置源直接当作独立第二个 gap 反例。
