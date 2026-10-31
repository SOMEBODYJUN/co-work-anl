---
id: facility-games/history-search-and-eptas-editorial-v1
kind: review
type_tag: 审查
title: 设施历史搜索与 EPTAS 出版决定三源处置
status: historical-finite-search-and-editorial-record-retained
truth_status: finite-search-records; internal research/editorial status; no-external-certification
review_level: full-source-read
summary: "完整读取 3×3 kappa<=2 搜索记录、双设施 EPTAS 方向辩驳笔记和期刊拆分编辑决定；保留搜索量词、模型/算法候选与未完成门槛，明确历史记录不等同定理、同行评审或录用预测。"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/searches/three_by_three.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/publication/facility_eptas_direction_debate_2026-10-09.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/publication/facility_journal_decision_2026-10-02.md
source_ids: [abdb7a32555a7481a2aa, 6c7e74f7583107fb4931, f609a4cfb8d618273a20]
source_sha256:
  - 93f130d6cd664b6b14f8103690c89b47633119bfd287bea4bfbd78cebbe5bba4
  - a3835b7b3d89f6f9fde2583d1bf70b87867ba48446f3f8728808ae3e7a743a13
  - cdadfa6bd8cbf21e9308ebe5e527e95bd2cabef55ea65f4b67fb681d309b70b9
source_blobs: [18fbc58055fb27abaf29f8c95d015570dc25ad3c, 8a5b6e0b5c4e79a6571d2ad0107f4bf111fe5ae6, 6d3ee69c4cca9b90b4f1fce922a83e64798d77c7]
source_commits: [68fad804ec5946cb296f77dc5b336308a66abf12 (legacy-cleanup), aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c (main)]
evidence_manifest: ../../tools/evidence/retired-facility-history-20261031/manifest.json
---

# 历史记录与数学身份

三源均是 facility-games 双设施/异质 overlap 研究线的历史文档，不是当前 CAG-SPE 六提供者模型。第一源是 MILP 搜索日志；第二源是内部 EPTAS 方向辩驳；第三源是两篇论文拆分与投稿门槛。它们的 `integrated` 状态仅表示历史内容已按语义保存，不表示定理已完成或文章已录用。原件、SHA、manifest 和校验在 [retired-facility-history-20261031](../../tools/evidence/retired-facility-history-20261031/)。

# 1. 3×3、κ≤2 后续反例搜索

`three_by_three.md` source ID `abdb7a32555a7481a2aa`，大小 1590 bytes，SHA `93f130d6cd664b6b14f8103690c89b47633119bfd287bea4bfbd78cebbe5bba4`。研究对象是双方各三位置、每交叉对至多两名共有客户的严格唯一 NE 子类；最多 98 个候选类型槽、每交叉对至多两名，私有客户由 reach 减去跨色客户重数获得。20 个行内/列内排序的全局 interleaving 被编码为 MILP，严格改善因子阈值 2.001，每例限时 8 秒。

结果是全部 `time limit / no incumbent`，而不是 infeasible certificate；早先 (10^{-6}) margin 的伪可行零收益状态经 bounded_overlap.py 精确 oracle 检查后全部只有 factor 1，已拒绝。搜索未覆盖允许多个客户 NE 的一般 κ≤2，因此不能推出 κ≤2 的一般 2 上界或不存在反例。正确处置：`integrated-finite-search-history`，保留“搜索边界/伪可行纠正/非证书”三层。

# 2. 双设施 EPTAS 方向辩驳与未完成门槛

`facility_eptas_direction_debate_2026-10-09.md` source ID `6c7e74f7583107fb4931`，大小 10372 bytes，SHA `a3835b7b3d89f6f9fde2583d1bf70b87867ba48446f3f8728808ae3e7a743a13`。它保持原模型：共同目录、两设施、显式正有理原子权、强制服务、精确独立混合客户 NE、完整带标签续局；目标是倍率 (le\alpha^*+\varepsilon)，运行 (f(1/\varepsilon)\operatorname{poly}(L))，争取 (2^{O(1/\varepsilon)}\operatorname{poly}(L))。

笔记记录了具体近带路线：严格外带 (|\Delta|>\eta W) 时轻客纯选低侧，自由重客户至多 (1/\eta)；固定重支持后近带补全输出 (|\Delta|\le H) 的精确 NE；外带闭谱与近带代表组成候选 NE 菜单；零/极小收益坐标精确保留。内部有限攻击包括 1322 个固定重支持（388 可行）、另一审查者 2004 局部输入/8000 重支持，以及 186 四地点全局原型/2976 标签布局/1116 实际偏离；这些样本未发现实质反驳，但来源明确写着完整 EPTAS 算法、全局证明、位复杂度和独立证书核验**尚未交付**。

笔记还纠正了“递减列表较高侧必有最小轻客”的适用域：只在 (|D|\le S) 且剩余差非零时使用；(|D|>S) 时较高侧可能没有轻客。精度编码应写 (2^{O(1/\varepsilon)}\operatorname{poly}(L+\ell(\varepsilon))) 或整数 (p) 版本，以计入 (\varepsilonarepsilon) 读取位长。正确处置：`retained-internal-eptas-research-history`；它保存候选机制与缺口，不升级成已完成 EPTAS 定理。

# 3. 两篇论文拆分与出版门槛

`facility_journal_decision_2026-10-02.md` source ID `f609a4cfb8d618273a20`，大小 7415 bytes，SHA `cdadfa6bd8cbf21e9308ebe5e527e95bd2cabef55ea65f4b67fb681d309b70b9`。编辑决定是写两篇：

- **A shared catalogs**：两设施、共同目录的构造性 sharp (\varepsilonarphi) 上界与 polynomial bit-time certificate，目标先投 Algorithmica，需完成固定菜单覆盖、local chord exchange 计数、位复杂度和优先权核查；
- **B heterogeneous overlap**：nested incidence threshold (kappa=0\mapsto1)、(kappa\le1\mapsto\rho)、(kappa\le K\mapsto2)（(
ho=2\cos(\pi/7))）的结构分类，优先 SIDMA，需 `HC-2` sign-off、模型优先权审计和新英文稿。

该决定明确要求把 exact methods 作为短 companion，避免合并文章继承两条过长 proof chain；SICOMP/MOR 需要更广泛可迁移定理，当前只是高风险候选。它同时记录 precise continuation caveat：共同客户的预定一致 reach/priority 规则才能给稀疏 (
ho) 结论；任意混合纯 NE 选择可能没有有限稳定倍率。IJCAI 2024 的 lower bound 与 full-version SAT reduction 的模型范围也需准确归属，不能把多设施异质 reduction 当两设施 shared-catalog hardness。

此文档是内部 editorial assessment，明确不是 external peer review、priority certification 或 acceptance forecast。处置：`retained-editorial-publication-history`。

# 4. 三源关系与交接

三源共同说明 facility-games 研究线的实际状态：有限搜索未给一般反例证书；EPTAS 路线有具体近带机制但正式算法/位复杂度未完成；论文拆分决定将 shared-catalog 构造与 heterogeneous-overlap 分类分开。第三阶段可建立“搜索边界”“方法候选”“编辑组织”关系，但不能把出版决定当数学真值，也不能把未完成 EPTAS 候选写成主定理。
