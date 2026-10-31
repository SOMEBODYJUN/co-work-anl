---
agent: Boss6/clean_complete_clone
source_id: "070e4cdfdd9cc682b2dc"
source_sha256: "92b582ad618cee1465b206490ec5fae1faa3670b15bf2f816affed4b393dbc81"
source_path: "history/source/notes/unrelated_machines/complete_clone_exact_reconstruction.md"
review_status: "full-source-read-and-related-material-checked"
recommended_disposition: "integrated"
---

# 来源 070e4cdfdd9cc682b2dc：完整机器任务克隆陈述先行推导（处置草稿）

## 1. 实际读取与来源身份

已通过 `clean show 070e4cdfdd9cc682b2dc` 完整读取冻结源，共 3482 字节；仓库冻结元数据给出的 SHA-256 为 `92b582ad618cee1465b206490ec5fae1faa3670b15bf2f816affed4b393dbc81`。来源自述为 boss24 本轮实际推导的事后整理，明确它不是推导开始前已冻结的原件，也不是完整子代理聊天记录。因此本源应作为**形成过程/来源追溯记录**，不应另立一份与现行定理重复的数学结论。

已核对：

- `archives/unrelated-machines/state/定理/完整机器任务克隆的多重集与最终周期--定理.md`（legacy ID `UM-COMPLETE-CLONE-MULTISET-PERIODICITY-v1`）；
- `archives/unrelated-machines/state/计算/完整克隆的双Oracle与周期族核验--计算.md`；
- `tools/evidence/private-tree/complete-clone/complete_clone_multiset_periodicity.py`（10337 字节，Fraction 双 oracle 与三类构造）；
- `tools/evidence/source-migration-crosswalk/original/research/source_crosswalk.md` 对本源的行（明确目标为 `research/current/unrelated_machines/private_graft_and_resource_repetition.md`，语义为完整 q² 交叉端的 MC/真实调度双向、最终周期、指数首次达到；“主目标未解”）；
- `cleanup/workspaces/Boss6/CLAIMS.md` 中 `UM-COMPLETE-CLONE-MULTISET-PERIODICITY-v1` 条目及其证据/边界。

源交叉表、CLAIMS 和 canonical theorem 一致把本文件视为现行对象的历史/来源记录，而非新的对象。

## 2. 来源的数学内容（逐项归并）

### 2.1 明确的克隆操作与配置接口

对每台原机器和每种原任务各复制 q 份，并把每条原有限端扩为全部 q² 条交叉端；允许同类型任务副本在一个机器副本共居。这与 incidence 置换 cover、同机任务复制、Kronecker 等操作不同。删除有零端的原任务类型后，余下机器负载在有限的多重集配置中描述。

真实配置计数的约束为
[
\sum_a z_{ia}=q,qquad \sum_{i,a} a_j z_{ia}=q .
]
归一化 (y_{ia}=z_{ia}/q) 给每类机器配置质量 1、每类任务平均质量 1 的多重集配置 LP；有理 LP 证书乘共同分母可恢复所有带标签副本。这个双向恢复是可复用的核心内容，已在 canonical theorem §8.2 写成正式证明。

### 2.2 阈值、周期与极限结论

对每个固定阈值 T，正可行复制数集合对加法封闭。有限值域与加法半群余数论证给出：若该集合非空，则从某处起恰为 gcd 的倍数；最优阈值处的 gcd 是 O_q 的最小正最终周期。由此：

- (t_+=\min_q O_q=\liminf_q O_q)，并由有限有理配置 LP 取得；
- O_q 一般不相邻单调，也不保证普通极限存在；
- 最终周期是 (d_* = \gcd(S_{t_+}\setminus\{0\}))；
- 收敛当且仅当 (d_*=1)；
- limsup 可从有限负载集合中选择最终 gcd 为 1 的最小阈值。

来源中的“阈值半群/最终周期”方向与 canonical §8.3 的正式有限半群证明一致；来源本身是推导记录，不单独承担证明。

### 2.3 任意周期族与指数首次达到族

来源给出两类构造，canonical theorem §8.4–8.5 已纳入并明确限制：

1. 任意最小周期：m 台机器，一件全资格 unit，每台 m−1 件仅能在该机运行、时间 1/m 的私有任务。真实 (O_q=1+d(m,q)/m)，(S_1) 的正元素恰为 m 的倍数，最小最终周期恰 m；原种子 OPT 为 (2-1/m)，但 q=m 时克隆值降为 1，说明完整 q² 交叉端不自动保持原 gap。

2. 指数首次达到：Sylvester 分母
(e_1=2, e_{s+1}=1+\prod_{h\le s}e_h)，(R_k=\prod_{s\le k} e_s)，k+1 台机器、k 件全资格 unit、每机一件私有 (1/D_i)（分母为 (e_1,\ldots,e_k,R_k)）。有 (O_q=1) 当且仅当 (R_k\mid q)，故首次达到数和最小周期可为 (R_k=2^{\Theta(L)})（L 为输入位长）。这是实际输出规模障碍，不是复杂度归约或 LP gap 证明。

### 2.4 失败机制和不应外推的边界

来源明确失败机制：完整交叉资格让同一原私有类型在同一机器副本共居，0/1 配置被多重集配置取代，并在某些复制数实现有理混合；整除条件保留真实周期。因此：

- 不可把此操作的阈值写成原始 0/1 CONFIG、assignment-LP 或 incidence-置换 cover；
- 不可把 (O_q) 说成相邻 q 单调或普通极限必存在；
- 不可将有限双 oracle/有限构造当作一般 MC 求解器、周期识别器、近似算法或 NP-hard 证据；
- 不可由本文推出一般 UM-TARGET-v1 的正面/反面，也未排除精选 hard-image、物理一致性或附加资格限制可能阻止共居；
- 指数首次达到只说明显式 B_d 的输出规模可指数大，不表示输入位长本身指数，也不构成 P≠NP 结论。

## 3. 与既有正文/证据的比较

- **与 canonical theorem 的关系：** 内容是同一稳定 ID 的形成来源。canonical 已补充零端删除、空情形 \\(\Lambda=\\{0\\}\\)、最短端上界 U、S_T “含正整数”、Cramer/Hadamard 分母界和最小周期必要性等勘误/证明细节；本源没有独有且需要另立对象的定理。
- **与 computation 对象的关系：** `完整克隆的双Oracle与周期族核验--计算.md` 负责有限代码、冻结运行与本轮重放（86 矩阵×q=1,2 双 oracle 172 次；奇偶 q=1..5 双 oracle；m=1..9,q=1..40 的 360 组；Sylvester 前 5 族 500 次容量核验）。本源只描述这些对象如何产生和应如何分层，不能替代计算对象。
- **与 bounded-multiplicity 对象的关系：** `有界重数克隆接线与共同循环坍缩--定理.md` 处理有限重数 c 的扩展联系；c=1 的原 CONFIG 与本文允许任意重数的 MC 区别需保留。本源只提供“共同循环坍缩/多重集接口”的形成背景。
- **与旧研究路径的关系：** crosswalk 的目标路径是 `research/current/unrelated_machines/private_graft_and_resource_repetition.md`，结果分支已将该结论重写为 `archives/unrelated-machines/state/定理/完整机器任务克隆的多重集与最终周期--定理.md`。源路径本身保留在 history/source 中，不需复制到 archives 成为重复正文。

## 4. 建议正式处置与对象链接

建议将本源登记为 `integrated`，目标仅链接既有稳定对象：

1. `archives/unrelated-machines/state/定理/完整机器任务克隆的多重集与最终周期--定理.md`（主目标；来源形成记录、定理陈述、证明和边界已在其中分层）；
2. `archives/unrelated-machines/state/计算/完整克隆的双Oracle与周期族核验--计算.md`（有限程序/证据去向；本源不声称自身包含全部代码运行）。

不建议新建“complete_clone_exact_reconstruction--定理”或“--审查”文件：这会重复同一数学对象并把事后形成记录误报为独立证明/外审。

推荐 receipt（完成前先确认上述两个目标已在远端）：

```json
{
  "id": "070e4cdfdd9cc682b2dc",
  "full_file_reviewed": true,
  "related_material_checked": true,
  "unique_content_accounted_for": true,
  "read_note": "完整读取3482字节事后推导记录；逐项核对完整q²交叉端、配置LP双向恢复、阈值半群最终周期、任意周期族和Sylvester指数首次达到构造；标明其不是预冻结原件或完整聊天记录。",
  "comparison_note": "与完整机器任务克隆的多重集与最终周期--定理、完整克隆的双Oracle与周期族核验、CLAIMS及source_crosswalk核对；canonical 已含正式证明、勘误和边界，计算对象独立保存有限运行。",
  "decision_note": "将来源形成过程整合到既有定理/计算对象的source_refs与交叉表；不新建重复对象，不把事后记录升级为外审、新颖性或通用算法证明；保留UM-TARGET-v1和一般hardness为未解。",
  "disposition": "integrated",
  "targets": [
    "archives/unrelated-machines/state/定理/完整机器任务克隆的多重集与最终周期--定理.md",
    "archives/unrelated-machines/state/计算/完整克隆的双Oracle与周期族核验--计算.md"
  ]
}
```

## 5. 待根代理执行的检查

- 在 root 的串行窗口确认两个目标文件已 checkpoint pushed；
- 用上述 receipt 文件提交 `clean done`，由程序检查目标已存在远端；
- done 回执中保留源 SHA 与本次阅读范围；不要改动冻结来源字节；
- 后续第三阶段只需把该来源与稳定 ID 建边，不应将其当新的数学节点。
