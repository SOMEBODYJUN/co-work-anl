---
id: customer-attraction/r486-same-query-clique-redundancy-2396-boundary-review
kind: review
type_tag: 审查
title: R-486 相同查询完全图冗余与 2396 点边界
status: exact-local-comparison-complete; no-new-cut
truth_status: identical-query-families-redundant; frozen-2396-clique-no-cut; Q-CAG-HALF-open
summary: 当三族前置查询逐索引完全相同，完全图 O 行逐边退化为已有族内 O 行；对冻结 2396 点的三族 exact 重建中全部原子 k=1，八种有向完全图方向的新行余量均严格为正，因此该完全图模板没有新增切割。若改用 L 菜单，所需真实回复未记录，不能代入。
source_refs:
  - clean:d617e7539b4cb8b4efcf
  - clean:409aa69f6b84a54a907a
  - clean:53a50187718922aebd9c
  - clean:3f010c4e1926933c3335
  - clean:667dc37261628075aedc
related_objects:
  - customer-attraction/signed-menu-graph-common-customer-envelope
  - cag-enhanced-five-provider-index-identities-and-2396-review-boundary
---

## 1. 相同前置查询族时的完全图退化

固定 q 个索引、L 个族和同一份完整历史纯 SPE。若所有族的前置菜单逐索引相同，
即 (Z_i^r=T_i)，则每个客户的命中集合 (S_r={i:xin T_i}) 相同，故
(K_r=k)、(C_{rs}=k)。令
[
 \ell=\max(0,2k-q),\qquad d=k-\ell.
]
对有向边 (r\to s)，源族的异索引真实行仍是
[
 O_{rs}=(q-1)A_r-(q-1)a_rK_s+g_r(K_rK_s-C_{rs}).
]
代入共同 (K,C) 得 (O_{rs}=O_{rr})：目标族的背景、边方向和目标标签不再提供新的查询集合；该边只是源族已有的族内 O 行。

对任意固定于全部客户的非负边权 (lambda_e)，设 (w_e=lambda_e g_{\mathrm{src}(e)})，(omega=min_e w_e)，(chi) 为完全图共同索引容量扣除。完全图表达可写为
[
 \sum_e\lambda_eE_e-\omega\chi
 =\sum_e\lambda_eO_{\mathrm{src}(e),\mathrm{src}(e)}
 +\Bigl[\sum_e w_ed-\omega\chi\Bigr].
]
共同命中集合给出 (chi\le |E|d)，而 (sum_e w_ed\ge\omega |E|d)，所以方括号逐客户非负。真实族内 O 行的全客户和已非负，因而完全图式被既有族内行逐项支配。这个结论允许不同 (b_r)、任意方向和任意固定非负 (lambda)，但只适用于 (Z_i^r=T_i) 的同查询情形；不同背景不等于不同前置查询族。

这与已有“带符号真实菜单图的共同客户扣除与精确包络”相容：后者给任意 D/O 图的普遍必要式和精确重排放松，本源进一步识别在同查询特例中每条 O 边的独有信息为零。

## 2. 冻结 2396 点的定义级重建

冻结对象 `enhanced_2396_exact_obstruction.json`（source `clean:667dc37261628075aedc`，
SHA-256 `ce1f9d8b1036256b7e40e1eb5c990fdcc4f33c7fed3f2aa796bdf8245b9d0c4f`）给出
38 个正质量原子和三族可用真实菜单
[
H_0=(A,B,C),quad H_1=(A,E,U),quad H_2=(A,B,E),
\qquad Z_i^r=T_i,quad F_i^r=L_i^r.
]
这里 (q=5)。对每个原子，三族 (K_r) 都等于同一个 (k)，而 `mass_by_K` 显示该冻结点的全部质量集中在 (k=1)。一般 (q=5) 的完全图扣除 (chi) 只在 (k=2,3) 时可能为 1；本点因此逐原子 (chi=0)。

独立读取并实际运行 `evaluate_2396_clique.py` 一次。脚本不导入原 2396 行生成器，而从冻结原子中的 `AB_hist`、`bits` 和 `(ell,h)` 直接重建 (A_r,a_r,g_r)，逐客户检查每个方向的非负余项，并将八种有向三边选择的有理结果与冻结 `evaluation_2396_clique.json` 比较。运行状态为 `exact_evaluation_passed_no_cut`；独立重放的数值字段与冻结 JSON 相同（环境相关的 source 路径字符串除外）。

三条既有族内 O 行的总 slack 约为
[
0.7662514079159392,quad 1.5977558427757625,quad 0.9045431503613814.
]
八种方向的完全图单位权新行 slack 全部严格为正，最小值为
(4.713989929899356)，最大值为 (6.383809335069987)。因此该完全图模板在此冻结点没有切掉任何质量；这只说明同查询完全图没有额外信息，不能把点改造为 SPE 证书，也不能推出福利或 half 结论。原审查指出该冻结点另由同索引 (L_i^2) 查询 (L_i^1) 的真实末位行排除；本源不重复声称新的排除机制。

## 3. 不能把未记录的 L 回复补成新查询族

若把前置查询改为 (Z_i^r=L_i^r)，真实末位回复应是
[
F_i^{\prime r}=\sigma_5(H_r+L_i^r),
]
而不是已保存的 (L_i^r=\sigma_5(H_r+T_i))。冻结 2396 数据没有 (F_i^{\prime r}) 的会员和收益字段，因此不能把旧 (L_i^r) 冒充新回复来应用完全图定理。要走该路线，必须新增这些真实节点的回复、共享客户约束和最终根福利结算。

## 4. 处置与边界

本源新增的是“同查询完全图退化”的一般支配说明，以及冻结 2396 点的 exact no-cut 重建；`evaluation_2396_clique.json` 是有限点结果，`evaluate_2396_clique.py` 是重建程序，工作区身份文件不承载数学信息。与已有 2396 行审查相比，本轮不重新认证 2396 全行质量、38 原子是否为全局最优、完整有序历史策略或 2396 行外的福利界；也不把任何局部负 slack/正 slack提升为真实 SPE/OPT 结论。六人 Q-CAG-HALF 仍开放。
