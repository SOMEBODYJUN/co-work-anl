---
id: "unrelated-machines/bcg-degree-path-primary-read-scope-increment-20261031"
kind: "review"
type_tag: "审查"
title: "BCG 度路径 primary 实际读取范围增量"
status: "integrated-primary-scope-provenance"
truth_status: "full-source-read-of-target-log-with-limited-web-excerpts"
review_level: "clean-show-full-read-cross-archive-comparison"
scope: "Bateni–Charikar–Guruswami STOC'09 degree reduction target log and its relation to K2 path topology"
source_refs:
  - "source:1eb8eafb5246cc60a6f0:history/source/notes/unrelated_machines/sol_bcg2009_degree_path_primary_target_read.md"
source_sha256: "fc3d12e17f058a648c5bf513b13e126c862e5e0c63b4aa14558e5cd5014bd95b"
evidence_paths:
  - "../../tools/evidence/bcg-degree-path-primary-read-20261031/original/sol_bcg2009_degree_path_primary_target_read.md"
related_objects:
  - "../文献/PCSP最大最小分配与投影博弈平行重复三篇文献整理--文献.md"
  - "../定理/完整菜单的资源度三路径归约--定理.md"
  - "归一化菜单的三态资源度三正规形--定理.md"
---

# BCG 度路径 primary 实际读取范围增量

## 1. 这份来源记录了什么

本次完整读取 `history/source/notes/unrelated_machines/sol_bcg2009_degree_path_primary_target_read.md`。
来源 ID 为 `1eb8eafb5246cc60a6f0`，大小 3,107 字节，SHA-256
`fc3d12e17f058a648c5bf513b13e126c862e5e0c63b4aa14558e5cd5014bd95b`。它是对 MohammadHossein
Bateni、Moses Charikar、Venkatesan Guruswami, *MaxMin Allocation via Degree
Lower-bounded Arborescences* (STOC'09 extended abstract) 的 primary 阅读范围账，
不是全文文献审查，也不是 K2 新颖性证明。原文在 evidence 目录保全。

该来源的获取方式和范围必须原样保留：作者站 PDF 通过 web reader 读取，没有在该次
记录中下载本地 PDF，因此这份账**没有本地原 PDF SHA**，不能把 web excerpt hash 当
PDF hash，也不能声称读取了全文十页。实际读到的连续 text-extraction 区段是 lines
0–407、367–783，并在 canonical 审查后再次读到 Theorem 3 的 lines 188–609，覆盖
Figure 1 caption、Theorem 3/proof、caveat 和 MinMax footnote。find snippets 不计成
额外全文。

## 2. 对 K2 路径装置的来源作用

读到的 Theorem 3 给出 degree reduction：将一个旧 item 按邻居拆为 d 份，并用 d−1
个相邻 dummy players 连成路径，使至多一份服务旧 taker；footnote 还讨论 MinMax
情形和 better-than-two 阈值。该历史装置与本仓库完整 flat-menu 资源度三路径归约的
底层形态相同，因此本对象必须把“d 个副本 + d−1 个相邻 helper/dummy 的 path topology”
登记为已有 BCG 先例，不把路径本身写成仓库原创。

但是，primary 目标段落没有给本仓库 K2 合同的全部义务：

- 完整 ordinary flat jobs 与 zero/inactive routing；
- 给定 degree-four rational functional 和全局 resource machine；
- 每机 CONFIG first/pair、global-affine physical load localizers；
- 全部旧 moments 的双向保持；
- 当前正文对 `C<2` 全任务调度、`OPT` 端点和 normalized partial `V` 的具体证明。

因此 BCG primary 只承担历史归属和底层 topology 对照；K2 的真实 helper 矩阵、任意
完整调度的双向映射、资源度三、全任务保留和边界仍由本仓库的自足正文承重。不能由
“BCG 具有相似路径”推出 BCG 已证明本仓库的完整 ordinary UM 接口，也不能把 BCG 的
MaxMin allocation theorem、hardness 或近二讨论自动移植。

## 3. 与现有文献和定理档案的关系

现有《PCSP 最大最小分配与投影博弈平行重复三篇文献整理》已经保存 BCG PDF 的另一条
完整证据路径（本地 PDF SHA `7f7b21ff08b37e8489e9f60527e9aa9458dc5cf4cd6cc6804869665c24d51f7f`）
以及 MaxMin 模型、DegreeTwo/DegreeThree、arborescence 与 hardness 边界。该文献页
承重完整文献数学；本源不重复复制 PDF，而补充一次实际 primary target log 的读取时序、
web reader 区段和 K2 topology 对应关系。

现有《完整菜单的资源度三路径归约》已给本仓库构造的数学证明：真实 port 机器、每个
helper 的两态 selector/incidences、C<2 正向扩展、任意目标调度逆投影、全 private
`OPT<=2` 基线、normalized partial `V` 和 `V=0` 端点。该定理的 source refs 已将
BCG 文献作为 attribution，但本页不把 primary target log 的有限阅读范围扩大为该
定理的证明。

## 4. 时间顺序、未认证项与处置

来源明确说明：Theorem 3 的 primary 阅读发生在 K2 Exact-first 重构与作者 proof
read-after 冻结之后，早于本次 canonical append 审查；因此不能把该文献知识倒填为
Exact-first 阶段的先验来源。来源作者没有打开 BCG full technical report，没有审全部
引用，也没有认证其他代理此前读过什么。

处置为 **integrated-primary-scope-provenance**：原记录保全，文献归属和 K2 topology
关系写入本页，完整 MaxMin 结论仍只引用已有文献页，K2 数学仍只引用完整菜单定理。
该来源不产生代码、有限实验或新颖性结论；第三阶段应把它标作
“primary excerpt scope → historical topology attribution”，而不能标作全文重审、
全球新颖性认证、一般 UM hardness 或六人 SPE 结果。
