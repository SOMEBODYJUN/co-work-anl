# Boss7 第二阶段交接：仅本地，尚未共享

本轮已沿用 Boss7 身份、cleaner 角色、repository-cleanup 存档，在独立 clone 恢复。结果分支 rebuild/research-v2，公屏 wcg/board-cleanup-20261028。

## 真实运行边界

用户提交授权一直有效。当前 work.py start --actor Boss7 --resume 的实际 receive-pack 写验证返回：`GitHub rejected the credential/write permission. Stop retrying this credential.` 身份绑定可恢复，但本次写端点验证失败；没有将其误称为自动审批拒绝。失败后未同凭据重试、未换凭据、未新认领、未执行远端 done。

12 个本人原有 in-progress 来源全部实读、比较并形成 8 份正文；六个 gpt-6.1-sol/ultra 完整清洗代理均已交付，Boss本人完成三源重构并审阅全部八份正文。所有新产物只作 checkpoint --local-only；不声称 pushed 或 done。原恢复快照的七条本人 completed 记录仍在远端，未改写。

程序 clean handoff 没有 local-only 选项，且会重新验证同一写端点。为遵守认证失败后不重试的用户要求，本轮未再调用其远端写入。本文和给 Boss32 的报告仅保存在本地，未共享；十二项远端占用未能释放，需协调 Boss32 据此处理。不能将本文件当作已经成功的 clean handoff。

## 十二个来源与准确去向

| 来源 ID | 冻结路径 | 待登记正文 |
|---|---|---|
| `c2eec47b68e75da94236` | `history/source/notes/unrelated_machines/sol_true_hardness_raw_sh3_inclusion_entry_cut_exact_first_attack.md` | `archives/unrelated-machines/state/审查/集合包含入口切陈述先行重构与实阈值边界--审查.md` |
| `bec6c70d5f39c03bdd81` | `history/source/notes/unrelated_machines/ternary_palette_tensor_obstruction_v1_exact_objection_retained_source.md` | `archives/unrelated-machines/state/审查/三叉调色板张量v1常量分支与高度修正--审查.md` |
| `95ac41c9f9ef7aac8977` | `history/source/notes/unrelated_machines/ternary_palette_tensor_obstruction_v1_independent_literal_source.md` | `archives/unrelated-machines/state/审查/三叉调色板张量v1常量分支与高度修正--审查.md` |
| `d0fcf01aa8bd6952ea25` | `history/source/literature/unrelated_machines/feder_fanout_limitations_author_original.ps` | `archives/unrelated-machines/state/文献/Feder--扇出受限约束系统与广义拟阵--文献.md` |
| `6409efb7883ecf36d337` | `history/source/literature/unrelated_machines/karp_1972_reprinted_2010_reducibility.pdf` | `archives/unrelated-machines/state/文献/Karp归约框架与完全问题--文献.md` |
| `533900faa02356c5f2df` | `history/source/literature/unrelated_machines/manurangsi_minrep_degree_1807_00936v1.pdf` | `archives/unrelated-machines/state/文献/MinRep度数与字母表逼近困难--文献.md` |
| `6cfd61c7a86bbe0e41b9` | `history/source/literature/unrelated_machines/potechin_2019_symmetric_sos_knapsack.pdf` | `archives/unrelated-machines/state/文献/对称平方和背包下界--文献.md` |
| `e367617bfd1e98dfb971` | `history/source/literature/unrelated_machines/vontobel_koetter_2005_graph_cover_decoding_v1.pdf` | `archives/unrelated-machines/state/文献/图覆盖译码与基本多面体--文献.md` |
| `93808197dd001b8ac118` | `history/source/notes/unrelated_machines/fractional_rematching_extension_statement_only_v4.md.gz` | `archives/unrelated-machines/state/审查/分数重匹配显式XOS-v4-v5增量--审查.md` |
| `b50f2d64238493b723a0` | `history/source/notes/unrelated_machines/fractional_rematching_extension_statement_only_v5.md.gz` | `archives/unrelated-machines/state/审查/分数重匹配显式XOS-v4-v5增量--审查.md` |
| `dc1a1b0e22af277523e9` | `history/source/notes/unrelated_machines/fractional_rematching_extension_v4_coauthor_validation_and_provenance.md` | `archives/unrelated-machines/state/审查/分数重匹配显式XOS-v4-v5增量--审查.md` |
| `8e013b1a8d17a54eba9a` | `history/source/notes/unrelated_machines/fractional_rematching_extension_v5_coauthor_validation_and_provenance.md` | `archives/unrelated-machines/state/审查/分数重匹配显式XOS-v4-v5增量--审查.md` |

## 数学边界及新增纠错

- Feder：基族、独立集族和 cube 图独立禁止点分别保留；二元相等不单独判 NP 完全，promise/物理复制尚须另证。
- Karp：完整判定/二进制归约合同、Steiner 和 MaxCut 原式缺陷、明确替代及未认证自动机方向；不把带权 MaxCut 偷换成无权。
- MinRep：δ、pDn、N 基准与精确下尾修复；后续文献的参数缺口和正规化义务单列。
- Potechin：等式背包、索引次数/普通次数、good-story 证明依赖、n=1 小参数例外与真实分布界限。
- Vontobel–Koetter：有理覆盖实现与 LP 最优值合同；原 Lemma24 整数锥等式给奇偶反例，信道/平局/覆盖规模均保留。
- fractional v4/v5：原 Q 数值收费与残余归一化/局部格点的位长强化；协作验证和后续证明身份分开；γ 高低比例互补勘误不被旧 PASS 覆盖。
- 三叉 v1：常量 (A,B,C) 与正高度缺口；raw SH3：原矩次数、共同 terminal 预算、floor 及实阈值界限。

## 恢复与下一步

恢复基点：`3c7e0e6ab81d05b8eb69c4658673012f86dd688c`。本轮本地提交及所有新证据将保存在恢复包，最终提交头见包内 RESTORE.json。不得把恢复包或 receipt 文件视为远端完成回执。

恢复有效写凭据后：先核对最新远端和 owner self，并保留本地提交；使用 start --actor Boss7 --resume（不是另借编号或重绑其他 clone）。恢复包应先导入独立 clone 比较，冲突保留双方内容。

随后以本工作区及全部八份正文、Boss7-*-restored 证据目录为显式 checkpoint 范围，覆盖本轮全部未发布祖先；确认 status=pushed 后，才把 receipts-pending-push.json 中仍需登记的逐源记录提交 clean done。先检查各来源是否已由协调者处理，不盲目覆盖状态。

若此后仍暂停，再执行 clean handoff --all --reason 实际原因 --draft-note 本文路径及已共享状态，并分别确认远端成功。全仓仍有大量未处置来源，当前六人任意完整历史 SPE 半覆盖目标未由本批解决。

最终核对：final-local-validation.json；逐源回执：receipts-pending-push.json；认证记录：write-boundary.json。没有后台继续清洗的数学代理。
