---
agent: Boss6/clean_true_hardness_author_read
source_id: "b4c80a82aa43c9ebe976"
source_sha256: "d55514ae36989bf3990bd0294bb31498731d267f32dffca8599de1fe764629a4"
source_path: "history/source/notes/unrelated_machines/sol_true_hardness_actual_allocation_v4_author_read_after_by_nsw.md"
review_status: "full-source-read-and-related-candidate-comparison"
recommended_disposition: "integrated"
---

# 来源 b4c80a82aa43c9ebe976：v4 actual-allocation 势算法读后攻击

## 1. 来源身份与实际读取

已通过 `clean show b4c80a82aa43c9ebe976` 完整读取冻结源，共 13,225 字节，源 SHA-256 为 `d55514ae36989bf3990bd0294bb31498731d267f32dffca8599de1fe764629a4`，legacy-cleanup 与 main 两个冻结提交指向同一 blob `7993009a21f4de8901492c96809bcef4c45c810d`。源标题说明它是审者对新 v4 actual-allocation 势算法的全文读后攻击，而不是 Exact-first、作者原稿或软件运行；它自述已知前序来源和送审提示，因此不能标为本路线的 blind 独立证明。

源中实际新算法背景稿为 `sol_true_hardness_shared_ud_tiny_home_k2_v4_exact_first_attack.md`（149 行，源 SHA `69036ac605760a193093869fc2af26b6fed35d76ed1c49f776185d17e9089f10`），本次票逐段读取作者攻击的算法/证明内容，但没有重新认证其历史阅读顺序，也没有读取 O(1/k) 草稿、软件、运行产物或外部链接。对应原件已导出到 `archives/unrelated-machines/tools/evidence/shared-ud-tiny-home-actual-allocation-v4-20261031/original/`，manifest 记录来源 SHA、读取层级和未运行边界。

## 2. 精确 typed 域和输出分支

输入域沿用 shared-UD tiny-home v4b：k≥1 个 single-state outer；所有正 home 全局互异；每个 home 有唯一 unit-own helper；任意 normalized B-only fallback states；B-only exact-threshold-UD leaves（ε=15/16）；原 zero、indexed duplicate、inactive、unused resource 与所有普通 jobs 保留。k=1 不设 tiny 上界；k≥2 要求 `ν=max w_j≤1/(16384 k²)`。完整普通矩阵满足 `OPT=2−V∈[1,2]`，其中 V 是真实 normalized-menu max-min value。

算法的硬阈值为 `r=18/19`、`a=r²=324/361`、`t=1/10`、成功福利门槛 `ℓ=19/100`。它有两条可靠输出分支：

1. 若所有 outer 的实际福利 `L_i≥19/100`，保留 Good helpers 并用同一叶匹配/拟阵独立集恢复全部原 jobs，得到 `C≤19/10`。
2. 若停止时福利门槛失败，则证明 `V≤18/19`，把所有原 incidences 留 private 得到 `C≤2`；等号也安全，因为 `(19/10)(2−18/19)=2`。

不把旧算法的严格 FAIL gap 写入本路线；`V=18/19` 属于可靠失败分支，k=1 另用线性势证明。

## 3. 实际 matroid 状态与候选更新

叶完整匹配存在时，resource-side transversal matroid A 的对偶 M 表示可保留的 B 资源；所有正 fallback incidence 是 M 中的带标签平行 copy。状态为每个有 fallback helper 的一个当前 state 和一个独立实际 incidence 集 I；每轮只在 `I_{−j}` 加候选 helper j/state 的正 copies 上做 weighted matroid greedy，旧 I 保证 `δ_j≥0`，无 fallback helper 的 δ 为零。候选、排序和 matching oracle 均在显式 ground 上计算；不把未知最优 profile、fractional optimum、FW 或 SDP 当输入 oracle。

关键比较式用完整标签 ground 的 weighted matroid rank F：对任意共同参考 `I*`，每 helper 至多一个 state，次模性和候选增益给出

`Σ_i h_i L_i* ≤ 2 Σ_i h_i L_i + Σ_j δ_j`。

源逐式核对了同-outer 被挤出 helper 的损失，不把 `I_j` 删除误当免费；二次势 `Φ(L)=Σ_i[-(γ−L_i)_+²+bL_i]` 的 2-Lipschitz 曲率、停止阈值 `τ/N` 和 `ν≤1/(16384k²)` 给出 `Σδ_j≤E+τ`，并以 Fraction 重算保守常数，证明 `V>18/19` 时不可能停在某 `L_i<19/100`。k=1 走 `Φ=L_1` 的线性分支，无 tiny 假设。

真实参考 `I*` 只在反证中从一个达到 V 的完整 allocation 提取：home 质量≥V 的 outer helper 必为 B-fallback，保留其 B bundle；每个 leaf 取一个达到 ε 的代表资源，彼此不交且与保留 B bundles 不交，故同一 physical B 上整体 independent。算法不取得 V 或参考 allocation；它只用当前状态和显式 matroid greedy。

## 4. 全 jobs 回填、复杂度与证据边界

成功回填先保 Good helper 的实际 B bundle 和全局互异 homes；非 Good helper 回 own state；selector 只导出 selected-state 的正 incidence jobs，所有其它 indexed/zero/inactive/duplicate/unselected jobs 留在各自 private 端，保证每个普通 job 恰执行一次、所有端点仍有限。完整 leaf matching 再逐叶选择一个系数至少 ε 的原 state。算法声明固定 typed 域上的 deterministic total-bit polynomial；势、候选、matching、排序与有理分母在显式输入位长内计算，未依赖 OPT/target witness、configuration/profile oracle、随机时间或 exact SDP。

本源没有实现或运行该 actual-allocation 算法，没有全程 scheduler backend、NSW greedy、matching search 或外部同行/新颖性认证。它支持的是工作候选的数学读后攻击票；不支持一般 unrelated-machines、multi-state outer、重合 homes、non-UD extras、任意 UM、NP-hardness 或 UM-TARGET-v1 结论。当前对象与既有 O(1/k) working candidate review 属同一后续 v4 候选的互补 read-after 角色，不与早期 k⁴/k² 算法、FW 作者 Proof 或独立 Exact-first 合并为多个独立定理。

## 5. 与现有对象的比较和建议去向

已核对 `archives/unrelated-machines/state/审查/相对曲率O1k候选三源精读与19比10范围--审查.md`、`archives/unrelated-machines/state/证明/共享UD tiny状态势与19比10回填--证明.md`、`cleanup/workspaces/Boss6/CLAIMS.md` 中 v4 Claim，以及 `archives/unrelated-machines/tools/evidence/relative-curvature-o1k-working-sources-20261031/` 的四源 manifest。现有 review 已登记 v4 的 candidate domain、作者 reciprocal-gradient Proof、independent Exact-first 和 informed read-after；本源是后续 actual-allocation 势算法的 primary read-after 攻击，新增内容是完整 actual-allocation 状态、same-outer 损失、等号可靠 FAIL、k=1 分支、全 jobs 回填和 bit-polynomial 量词核对。

建议将本源标记为 `integrated`，补入上述 O(1/k) working review 的 source_refs、source_sha256 与“actual-allocation read-after”表格，并保留 raw source/manifest。不要新建第二个 19/10 theorem，也不要把 informed read-after 改写成作者原 Proof、软件运行或一般 UM 结论。

## 建议 receipt

```json
{
  "id": "b4c80a82aa43c9ebe976",
  "full_file_reviewed": true,
  "related_material_checked": true,
  "unique_content_accounted_for": true,
  "read_note": "完整读取13225字节 v4 actual-allocation 势算法读后攻击；核对 typed single-state/互异home/UD叶域、matroid 状态、2×当前福利比较、same-outer 损失、二次曲率、r=18/19 等号 FAIL、k=1 分支、全jobs回填与位复杂度。",
  "comparison_note": "与相对曲率 O(1/k) working review、共享UD tiny 证明、v4 Claim、relative-curvature manifest 及早期 k4/k2 版本比较；本源是后续 actual-allocation 路线的互补 read-after，不是 blind Proof、软件运行或独立 Exact。",
  "decision_note": "整合到现有 O(1/k) working candidate review 的 actual-allocation read-after 层，保留 candidate/author-proof/read-after 角色分离、有限常数核验和无实现/无一般UM边界；不新建重复 theorem。",
  "disposition": "integrated",
  "targets": ["archives/unrelated-machines/state/审查/相对曲率O1k候选三源精读与19比10范围--审查.md"]
}
```\n