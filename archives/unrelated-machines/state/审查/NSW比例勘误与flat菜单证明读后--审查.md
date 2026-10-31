# NSW 高低组比例勘误与 flat-menu 度三路径证明读后

- **稳定归档 ID**：`nsw-gamma-complement-flat-proof-followup-20261031`
- **角色**：第二阶段 cleaner，Boss2
- **来源**：`2635332457d793f7982c`、`fe652aee7fad810f7a52`、`9f0ba5ca993e687e4fa4`
- **证据目录**：`archives/unrelated-machines/tools/evidence/retired-nsw-flat-followup-20261031/`
- **处置类型**：前两源是对已归档显式 XOS/NSW 内部规格的实质勘误链，第三源是已归档 normalized-flat 度三对象的作者 Proof read-after。三源都没有生成一般 unrelated-machines 算法、hardness 或六人 SPE 定理。

## 1. NSW 比例勘误：必须区分高端上限和低端下限

`263533...` 是对既有 `显式 XOS 的分数 NSW、几乎所有组质量与共享修复 LP 边界` 的实际 read-after 审查；它明确撤回旧 §F 中把 robust NO 的高质量组比例与 C–D 低质量组比例当作同一 `γ` 的错误。`fe652...` 是同一修正的 gzip diff，已用 `gzip -dc` 完整展开并逐行核对，保留文本 diff 与二进制原件。

设一个实际 allocation 的组质量为 `r_g`，阈值为 `δ`。若 robust NO 写作

\[
\#\{g:r_g\ge δ\}<γ_{hi}n,
\]

则准确互补是

\[
\#\{g:r_g<δ\}>(1-γ_{hi})n,
\]

不是 `γ_hi n`。相应地，弱版本的四种边界为：

| 高端条件 | 低端等价 |
|---|---|
| `#{r≥δ}<γn` | `#{r<δ}>(1−γ)n` |
| `#{r≥δ}≤γn` | `#{r<δ}≥(1−γ)n` |
| `#{r>δ}<γn` | `#{r≤δ}>(1−γ)n` |
| `#{r>δ}≤γn` | `#{r≤δ}≥(1−γ)n` |

这不是符号润色：旧 §F 用 `γ_hi≤δ` 推出低端必要界，实质上比较了错误比例。应撤回的旧结论是“C–D 不覆盖典型 `γ≤δ_q` 小常数域”。正确的直接适用条件是：C.4 的输出满足 `#{r_g<q_η}<ηn`；当 `δ≤q_η` 且 `γ_hi≤1−η` 时，同一输出有 `#{r_g≥δ}>(1−η)n≥γ_hi n`，因此违反该 robust NO。`δ=q_η` 和 `γ_hi=1−η` 的等号也被严格计数覆盖；不需要 `ηn` 为整数。

如果高端改成 `r_g>δ`，就必须使用低端 `r_g≤δ` 的控制，不能直接套用只证明 `<q_η` 的 C.4。独立从严格 NSW 下界另证 `#{r_g≤q_η}<ηn` 是可能的，但不能把这个加强假装是 C.4 原句自身。`263533...` 保留了这一边界区分，也明确没有重审 A/B 的全部作者证明、软件枚举或新颖性。

**处置**：这两个来源更新的是已有内部 XOS/NSW 资料的关系证据和适用参数域；它们没有新增一个独立 NSW 算法，也没有证明全部正参数域都被排除。当前资料中的 residual LP、显式 XOS deterministic fractional guarantee、shared singleton REPAIR 计数和完整 ordinary schedule 仍保留原对象身份与未实现边界。

## 2. Flat-menu 度三路径降度 Proof read-after

`9f0ba...` 完整读取作者 Proof v1 的六节，并与先前已归档的 Exact-only independent reconstruction 逐项对照。结论 PASS 表示作者 Proof 与独立重构及所有端点一致；这不是软件运行或外部审稿认证。

对象是 `UM-FLAT-MENU-RESOURCE-DEGREE-THREE-PATH-REDUCTION-v1`，范围固定为显式 flat menu。Proof 保留每个 helper 的 hole-a 端口选择：对 `j<a` 使用端口 `j`，其余使用 `j+1`；每个 helper 的 selector、选中 incidence 和未选状态 incidence 都在其 private machine 上形成实际负载一。旧 group 的每个 indexed state 沿同一 port，外部旧 job 的身份和 eligibility 全部保留。

逆向方向使用 `C<2` 强迫选中的 helper singleton job 离开 private machine；`d−1` 个 helper 导出的端口互异，其他可能的 helper exports 只会减少给旧 jobs 的可用端口。于是任意目标部分调度都能投影回原实例，每个原 resource 至多承载一个旧外部 unit job。作者明确不在 `C=2` 时错误使用 exclusivity，而是用完整 private schedule 处理 OPT=2 的上端点。

正值方向另外证明：helper 的 singleton 必须实际出现在 bundle 中，旧 selected state 及其整个分配子集可以保持；`V=0` 情形由正向逆向矛盾处理，而不是从 normalized scheduling identity 猜出。完整 menu 的 group membership 计数包括零 private-time 的原 incidence，得到目标 resource degree 至多三；每个 helper 增加两台 private machines、三个 jobs 和六个 finite eligibility entries。证明保持原 jobs 全部存在，不把 helper 重标为 mixed group，也不声称保持 group interaction `M`。

边界情况包括 `d=0`、`d=1`、empty states、zero private times、重复 indexed states 和 unused resources。复杂度按实际显式 jobs、paths、旧二进制有理值与常数一计，不按未知状态选择或逆参数展开。作者 Proof 只声明 source `C<2` 方向的 private-choice preservation；`C≥2` 时另一实例的 all-private schedule 提供负载二的 fallback，因而 exact optimal-value equality 没有遗漏端点。

**处置**：该 read-after 作为同一 normalized-flat 度三对象的证明 provenance，与已有 Exact/Proof/independent review 合并；不创建第二个 theorem，不扩展到一般 UM、source hardness、near-two 或当前六人 SPE。

## 3. 与主线的关系和未解决问题

这批纠错和 read-after 对当前六人共同目录、完整有序历史、终局价值均分和半主题覆盖目标的作用是边界检查：

- 高端“至少多少高质量组”和低端“多少低质量组”必须逐历史、逐策略保持互补量词；不能把摘要中的比例直接当成 SPE 偏离条件。
- Flat-menu 度三路径降度保留 ordinary jobs/eligibility 的做法，可作为未来编码历史对象时的证书格式参考；它没有证明提供者偏离、纯 SPE 或任意平局。
- NSW internal correction 不构造 source reduction，也没有把 `C<2` 的调度端点转成六个提供者的价值上界。

因此本批分类为：

- **勘误**：`263533...` 与 `fe652...` 撤回旧比例混用结论，精确给出可保留的新参数域。
- **条件证明读后**：`9f0ba...` 在 normalized-flat 度三对象中确认作者证明与 Exact 一致。
- **障碍**：不得把高端 `γ_hi`、低端 `γ_lo` 或 `C<2` 端点偷换成一般 UM/SPE 量词。
- **未解决**：没有从本批得到六人纯 SPE 的半最大覆盖下界，也没有得到一般 unrelated-machines 的近二算法或 hardness。

三份源文件、解压 diff、manifest、`validate_sources.py` 与 PASS 的 `validation.json` 均在证据目录；后续 mapper 应将前两源连到显式 XOS/NSW 资料的勘误边，第三源连到 normalized-flat 度三对象的 proof-provenance 边。
