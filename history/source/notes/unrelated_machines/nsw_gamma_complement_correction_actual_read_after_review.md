# NSW §F 集合互补纠错：实际读后限定审查

Reviewer: `/root/sol_literal_budget_attack`, 2026-10-18. 这是 root 指出错误并释放纠正文稿后的定向审查，非盲审。结论：**本次集合互补及所列新适用范围 PASS；旧 §F 的“不覆盖”结论有实质错误，须撤回。** 本记录不回填为旧审查早已发现该错，也不重新认证 A/B 的证明、历史阅读或来源。

## 1. 实际字节与阅读范围

- 用 root 明确授权的只读 `git show 44aa:research/current/unrelated_machines/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary.md` 还原旧页至 scratch；实际 SHA256 为 `2365f54091786596e75cac20456caaf61cdf607664ba5cf2bd995de6963c6c81`，651 行。实际读旧 header 和完整 §F，并完整读其对下述 pending 的 unified diff；未重新全文审旧 A/B。
- Pending `/workspace/scratch/038d9dcc4cac/nsw_gamma_complement_corrected_canonical_pending_review.md`，实际 SHA256 `bfd9a2c452aff3d5ab1b5813b7afe9a2fb388196384efe686d4aa73356b29ae5`，648 行。实际独立显示并读 header 和完整 C、D、E、F（未截断）。首次大段输出有截断，故不以该次输出声称全页阅读。
- 完整 diff 的变化仅为 header 加入勘误及 §F 两段撤回/替换；本次不将其余保留文字升级为新审查、新颖性或软件证据。没有修改 repo、旧 Exact、旧 Proof 或旧审查。我也没有创建 `negative_hardness_work/` 或 `boss11_robust_gamma_complement_objection.txt`，不推测其作者。

## 2. 互补及新结论

对同一 allocation、同一个原组数 n，令 H 为质量至少 δ 的组数。恒等式是

\[
\#\{r_g<\delta\}=n-\#\{r_g\ge\delta\}.
\]

因此 robust NO `# {r_g≥δ} < γ_hi n` 精确等价于 `# {r_g<δ} > (1−γ_hi)n`。C–D 中低质量计数使用的是后者的比例，而不是 γ_hi。旧 §F 把这两个比例当成同一个 γ，并以 γ_hi≤δ 推出低端必要界自动成立；这个推理不能成立，旧“不覆盖典型 regime”的结论必须撤回。旧最终审查未捕捉这项实质错误，不能由本次纠错追溯升级。

C.4 的同一实际输出满足 `# {r_g<q_eta}<ηn`。若 δ≤q_eta，则

\[
\#\{r_g<\delta\}\le\#\{r_g<q_\eta\}<\eta n,
\quad
\#\{r_g\ge\delta\}>(1-\eta)n\ge\gamma_{\rm hi}n
\]

只要 γ_hi≤1−η。这直接违反该 robust NO。**δ=q_eta 和 γ_hi=1−η 同时成立也可；不需要额外严格 slack。** 不依赖 ηn 为整数。δ=0 时由非负质量更直接成立；通常 §F 的条件域为 0<δ<1。

“γ_hi≤δ 的充分小常数域被排除”也准确。例如固定 η=1/2，则 q_eta=ρ^−2=2^−48；取 0<δ≤2^−48 及 0≤γ_hi≤δ 即满足上述两个条件。没有声称全部正参数域被排除，也没有让 δ 随源规模趋零。

## 3. 严格和弱边界

准确的四种互补为：

| 高端 NO | 低端等价条件 |
| --- | --- |
| `# {r≥δ}<γn` | `# {r<δ}>(1−γ)n` |
| `# {r≥δ}≤γn` | `# {r<δ}≥(1−γ)n` |
| `# {r>δ}<γn` | `# {r≤δ}>(1−γ)n` |
| `# {r>δ}≤γn` | `# {r≤δ}≥(1−γ)n` |

上节直接使用 C.4 的第一项，所以高端采用 ≥δ 是关键的准确写法；它同时能反驳表中第二行的弱计数版本。若改用高端 >δ，必须控制低端 ≤δ。仅引用 C.4 第一项时，δ<q_eta 足够，而 δ=q_eta 不能直接靠集合包含。当前 pending 只提醒这种边界区分，没有作这个无依据的互换，故准确。

实际上若另行从 C.2 的严格 NSW 下界推导，可加强到 `# {r_g≤q_eta}<ηn`：若 k≥ηn 个值≤q_eta，其余≤1，则 NSW≤ρ^(−Kk/n)≤ρ^−1，与 C.2 的 NSW>ρ^−1 矛盾。这说明 >δ 在等号阈值处亦可另证，但该加强不应假装是 C.4 第一项文字本身；本次 PASS 不要求添加它。

## 4. 保留范围

F.1 对其明示的“至少 γ_lo n 组质量≤δ”前提仍正确。若高端 NO 给出低端严格 <δ 的互补，可先放宽成≤δ，再用低端比例 1−γ_hi（而非 γ_hi）比较；这正是旧数值比较失效的原因。C–D 原精确低端定理、同组 singleton REPAIR 的计数和 E 的全部 jobs 排程不被该集合恒等式反驳；本次不重审其作者证明。

新适用结论是原 C 定理在同一 norm1 显式菜单、unit-FSLP 前提下的直接 corollary，应与旧 v1 低端定理保留独立版本身份。它不提供所有原 machines 的统一 2−ε makespan，不构造任何 source reduction，不认证未来 gated 构造，也不解决共享内部/多层或不保正 support LP 的对象。当前 pending 的范围限制与这些结论一致。
