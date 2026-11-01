# R-44b24 full_tree 后三个源实读与处置建议

审查者：Boss6 子批次 full_tree-b。未修改共享 clone，未执行远端 clean done。

## 总结

三个冻结源均已用当前 `work.py clean show` 导出并全文阅读，SHA/字节与冻结 inventory 一致；两份 JSON 的原始输出与对应脚本在隔离目录重放后逐字段相等。它们的数学内容已经被当前结果树中的 canonical 对象和 evidence 目录完整吸收，建议三源均登记 `integrated`，而非 duplicate 或 needs-decision。

相关 canonical 去向：

- `archives/customer-attraction/subarchives/six-providers/state/审查/截断交集矩的有限差分重构与保策略压缩--审查.md`
- `archives/customer-attraction/subarchives/six-providers/state/资源/截断交集矩独立全收益审计与显式压缩--资源.md`
- `archives/customer-attraction/subarchives/six-providers/state/审查/计数势格循环的独立Floyd审计与冻结证据--审查.md`
- `archives/customer-attraction/subarchives/six-providers/state/引理/两层计数势端点配平的真实行双向支付--引理.md`
- `archives/customer-attraction/subarchives/six-providers/state/构造/十五客户完整策略的势循环严格扩大收益SCC空间--构造.md`

原件已在 evidence 的 `truncated-moments-independent-review-primary/related-original/<source-id>/...` 与 `lattice-independent-review-primary/related/...` 下按原路径保全；canonical frontmatter/source_refs 和 manifest 均直接引用这三个 source ID。

## 0d2f5d5b27d611918123 — lattice_circulation_audit.json

冻结路径：`research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/full_tree/lattice_circulation_audit.json`；SHA-256 `f8a705f2...`（clean show 报告完整值 `f8a705f20df3908518b9efe5517e9fcdeaf4ef5d7a2d9a0f63fa3ff6e012ab49`），6400 B。

全文字段实读：`status=passed`，范围明示“true SPE and strict circulation-space expansion only; not a half counterexample”；15 个单位客户、13 个有序历史、39 个真实行动比较、最小松弛 0，根路径 `(0,2,0)`，根三人支付 `(13/3,13/3,13/3)`，W=13，OPT=15；payoff SCC 秩 1、加根行秩 2，111 次 triangle regression。四条 zero-circulation rows 与 13 节点 complete strategy 也完整读取。

实读判断：这是三主题十五客户完整纯 SPE 的有限精确报告，显示势端点配平产生严格超出旧收益 SCC 的真实行方向；它不是六人 half 反例，不是一般 lineality 维数证明，也不等于完整策略枚举。当前 canonical lattice review/lemma/construction 已逐项保留其字段、四行、39 松弛、SCC 严格性及适用边界。

重放：从同 source 组导出 `audit_lattice_circulation.py`（source `b2cc74c6caa0cb212eb3`），标准 Python 运行 exit 0；stdout 解析为 `passed, unit_customers=15, ordered_histories=13, all_action_comparisons=39, minimum_slack=0, welfare=13, OPT=15, payoff_SCC_space_rank=1, SCC_plus_root_row_rank=2, triangle_regressions=111`。重放 JSON 与冻结 `lattice_circulation_audit.json` Python 对象逐字段相等（`lattice equal True`）。这是对冻结 source 的有限实现复核，不把 111 次回归升级为普遍证明。

处置：`integrated`。targets 为 lattice review、势端点配平引理、十五客户严格扩张构造，以及 evidence 的 related lattice originals。没有独有未去向内容。

## 072dd75667bbf82c9ea7 — truncated_intersection_moments.md

冻结路径：`research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/full_tree/truncated_intersection_moments.md`；SHA-256 `55651ea...`（完整值 `55651ea71ad4c40bd7005c8a5adc7e08013944d6e1cf41e9dea23101cd295eed`），10,911 B。

全文实读判断：自足给出固定 m,p 的终局收益函数 `f_{q,a}`、交集矩 `z_A`、`D_{m,p}=Σ_{s≤min(m,p)} C(p,s)`；通过积分展开和最高次有限差分系数证明全部收益行张成非空 Boolean 单项式空间；同低阶矩保持每一终局逐玩家收益、全部有序历史纯 SPE、W 和 OPT；通过有理列依赖压缩正类型数；给出 m+1 标签奇偶核、m=2,p=3 最小例、p=4/m=2 显式 15→8 正类型但客户 15→16；并明确非法矩与二次 cylinder 非负分解障碍、一般 half 仍 open。

重读比较：canonical `截断交集矩的有限差分重构与保策略压缩--审查.md` 对这些解析命题逐式自足重构，且将该原稿作为 related-original 保全；资源对象明确把它与发现审计/独审实现区分，不把其 10,911 B 视为独审程序的成功运行。source manifest 和 frontmatter 直接保留 source ID、commit/path/SHA。

处置：`integrated`。targets 为上述审查/资源对象和 `truncated-moments-independent-review-primary/related-original/072dd...`。无未吸收独有数学内容；“Q-CAG-HALF 仍 OPEN”、非空/重复/零客户/任意弱平局边界均已保留。

## ca8ec5094cab41041af7 — truncated_moments_audit.json

冻结路径：`research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/full_tree/truncated_moments_audit.json`；SHA-256 `e87fb8c...`（完整值 `e87fb8c0b48613b25fd6148f23ad4e60ada0978999f62e7cbc4812bd8960cd9a`），3275 B。

全文字段实读：`status=passed`，范围为 exact finite audits only；`payoff_rows_mobius_checked=1008`；24 个 rank cases（m=1..4,p=1..6）、4 个 parity games（(1,2),(2,3),(3,4),(4,5)，ordered leaves 2/9/64/625）、4 个 compression cases（before/after 15→4, 31→15, 63→21, 31→25），`infeasible_moment_excess=7/10`，二次非负点为 010/101。

重放：导出同源 `audit_truncated_moments.py`（source `3fd2ed1ea60aaf51a547`），标准 Python 运行 exit 0；stdout 与冻结 JSON 逐字段相等（`truncated equal True`），摘要为 `passed, 1008, 24, 4, 4, 7/10`。该程序使用 Fraction 的精确有限检查，但不替代任意 m,p 解析证明，不枚举完整策略 IC，不证明 half。

比较与去向：canonical 资源对象完整区分发现者 8252 B 程序/3275 B 报告与独审 4067 B 程序/2342 B 报告；当前三源已作为 related-original 原字节保全，且审查对象吸收其有限范围和边界。不存在需要另建对象的独有结论。

处置：`integrated`，targets 为截断交集矩审查/资源与 related-original evidence。

## 共同边界与接续

- 这些源分别提供有限精确实现与解析对象/势循环实例；都不证明当前恰六人 Q-CAG-HALF 对所有完整历史纯 SPE 成立。
- 不能把 15 客户三人严格扩张实例迁移成六人结论，也不能把 1008 行/111 回归/24 rank cases 当一般量词。
- canonical 文本已保留源版本差异（发现者与独审实现不混借）；有限审计字段不代替数学判断。
- 本批仅完成实读、比较、运行和处置建议；远端 source progress 仍待根 Boss 串行 `checkpoint`/`clean done`。
