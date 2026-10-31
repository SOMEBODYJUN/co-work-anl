---
id: unrelated-machines/normalized-flat-menu-degree3-normal-form-v1
kind: review
type_tag: 审查
title: 归一化 flat 菜单三态资源度三正规形三源审查
status: candidate-domain-proof-refinement-independent-review-integrated
truth_status: restricted-normal-form-contract; internal proof; independent Exact-first review
review_level: full-source-read
summary: "完整读取 normalized-flat three-state/degree-three Exact、作者 Proof 与 Exact-first 独立审查；保留树展开、路径降度、partial/actual/OPT2 双向量词和规模账，明确只适用于显式 normalized-flat 域。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/flat_normalized_menu_three_state_degree_three_normal_form_exact_v1.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/flat_normalized_menu_three_state_degree_three_normal_form_proof_v1.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/flat_normalized_menu_three_state_degree_three_normal_form_independent_review_v1.md
source_ids: [33cd8669fd7a6a7c9d86, e84bc7ad6b6b9e64e72f, 57454c431b001ccfb960]
source_sha256:
  - 33094582e9804d6a0a7aaa78122b5eac90e2fb65e5d9089aa939b7b618092a29
  - 079dfbfd274eb503db6e1e7410a251fa146f15be0c12941f235e6224591d9b28
  - 642049e4d872554efad0d8ebb5398713a922ca0524a80f1a33070407e8e9fa3d
source_blobs: [13c9064430490f75508639708c39896a23dcb03c, 3be28bd36b5b4e2d945782302c41de6ff8a5a77a, 6df92ae10fa683422df8f6535ce2681097d243d1]
source_commits: [68fad804ec5946cb296f77dc5b336308a66abf12 (legacy-cleanup), aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c (main)]
evidence_manifest: ../../tools/evidence/retired-flat-menu-degree3-normal-form-20261031/manifest.json
---

# Exact 域

输入是完整 normalized-flat ordinary P：每 group 有非空 indexed states，每 state 是 distinct resource 集合和非负二进制有理权，权重和严格为 1；每 state 一台 private machine、每个 incidence 一枚原 job、每 group 一个 unit selector，其他资格为无穷。Claim 允许任意 K_g、support、resource 跨 group degree 与 interaction，但目标先把每 group 菜单正规化为至多 3 states、每 resource degree 至多 3，同时保持 value、OPT 与完整实际 jobs 的可解码性。

Exact 构造：每个原 group 的 K-state 集合替换为满二叉树。非 root 顶点新增 own resource。root/internal 菜单是 child-own singleton；非root/internal 是 own、left、right 三个 singleton；非root leaf 是 own singleton 或原 indexed state；K=1 root-leaf 保持原 state。新增所有 singleton、selector、incidence、own resource 均为显式 physical objects，不能使用抽象 OR 或免费激活。

Exact Statements 要求对每个正阈值 v，源 whole-state partial allocation value≥v 当且仅当树中间实例和最终 degree-3 实例均有 value≥v；要求 deterministic bit-polynomial 双向 actual decoder；要求 V(P*)=V(P)，并对任意完整 actual schedule 保持 Cmax 不增、OPT 包括 OPT=2 端点；最终输出大小随源显式输入位长多项式。

# Proof 与独立重证

作者 Proof 的正向路径：源 group 选 leaf state 和资源子集后，root 到 leaf 的内部节点选择 child-own singleton，leaf 选择原 state，off-path nodes 选择 own singleton。own resources 在路径上由 parent 使用、off-path 由自身使用，因而互不冲突。逆向不预设只有一条活路径：target root 选择的 child-own resource 阻塞 child 的 own state，递归下降直到实际选择原 leaf；额外 off-path leaves 可丢弃，只提取一条 root path。

对完整 C<2 actual，selector private load 1 加未导出 incidence 的负载会超过 2，因此 selected singleton 的 incidence 必须导出；逆映射沿实际 selected path 解码原 leaf，删除新增 tree selector/资源并把原 selector 重定位到原合法 leaf，全部旧 jobs 恰一次。正向则保留原 jobs/资源导出并为新增 singleton 安排 unit export。该证明明确处理未选 states 的原 incidence jobs、zero weights、duplicate states、idle machines，而不是只映射资源子集。

路径降度必须在树展开之后执行：对每个真实资源的 d 个 incident groups 建 d ports 和 d-1 helpers，每个 helper 只能选相邻 port singleton。完整正向/逆向 mapping 保持原资源子集不交和 C<2；最终每 group 至多 3 states、每 resource 至多 3 groups。树规模：每 K 个原 states 有 2K-1 vertices、2K-2 own resources；总中间 groups 2S-m、states 5S-4m，新增 singleton incidences 4S-4m，仍为显式输入位长多项式。

Exact-first 独立审查在声明的 normalized flat 域重证正值 partial witness、任意中间 target actual C<2、V0/OPT2 端点与完整 ordinary jobs，报告无 fatal。它强调 K=1、未选 state jobs、多个 off-path leaves、先树后 path 的顺序和 resource degree 的真实 membership；这些是适用域的承重条件，不是一般 UM 自动正规化。

# 处置与范围

- `33cd8669fd7a6a7c9d86`：`retained-candidate-exact-domain`，保留三态/度三 Exact 量词和全 job/OPT 要求。
- `e84bc7ad6b6b9e64e72f`：`integrated-internal-proof-refinement`，保留树路径、actual decoder、path reduction、规模和端点证明。
- `57454c431b001ccfb960`：`integrated-independent-exact-first-review`，保留独立重证与无 fatal 结论，明确不等于外审/新颖性。

正规形只适用于显式 normalized-flat source；不覆盖未归一化 Sigma p>1、一般 UM 识别、M 保持、source hardness 或全局新颖性。它可以作为后续 restricted-UM reduction 的桥接对象，但不能直接写成 unrelated-machines 一般 19/10 算法。
