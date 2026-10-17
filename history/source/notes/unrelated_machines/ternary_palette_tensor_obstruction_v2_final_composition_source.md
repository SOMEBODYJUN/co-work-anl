# 三叉张量／纯收缩附节：最终组合字节核对

本次为最终 canonical 的读后组合审查，不是盲审。旧 v1/v2 Exact-first 与作者读后稿保持原字节：`fb59cbb90a782f7e8b7452a6046e89f6b12689431ba0779014f8fead74016cc2`、`950164f0ce3c2d9f32096bd3f80b58857243865761f51d70f94a81152b5c493a`、`8a6c1b5b3f027d8329a8847030a8da6a83daffcc8172ff1ca54831f362ce89d3`。

实际全文读取新 Claim 及 T1–T7：

`/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/ternary_rainbow_subtree_exact_hardness.md`

实际 SHA256：`3f3075ec56543f2e2b1f909614c853762b66232c0081d311e9c3d1f58d8b1903`，与 root 提供值一致。

实际读取对应 review 新增 tensor 段及上下文：

`/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/reviews/unrelated_machines/ternary_rainbow_subtree_exact_hardness_review.md`

实际 SHA256：`4e7d5309156ce444f379619eba260b81098d0206db4f4169ab6c9484e651b4e5`。

## 组合数学结论

无 fatal objection，没有引入未审新 Claim 或扩大操作范围。新精确合同、全部 P 端与任务、OPT=2−q/d、末层palette张量界、YES乘积见证、严格递减G_k及纯收缩界均与已审 v2 Exact／proof 相符。

常量规范已明确 A≠B，并区分“旧v1未指定、旧v2已指定”：仅断言规范输出族满足前提，不倒称旧v1任意合法常量已被核过。高度H≥1保证pin定义。T4、T5引用明确为本附节T2，不误指旧SAT证明的编号。

T7已将作者冻结旁注的错误包含方向修为 NP⊆QP，排除假设明确 NP⊄QP；与缺少实际gap时不能靠更强复杂度假设补齐的数学结论一致。没有扩大成所有tensor／改色／padding／跨副本归约不可能；没有声称可按binary k多项式输出显式张量。

## 实际字节比对

用只读脚本将 canonical 的 T1–T7 标题还原为作者 proof 的1–7编号，与已实读冻结作者 proof `b2b7afdcdd362c8b8b087d97f9ba90e5bcf657d592857a7bbf9308293bc65aaa` 的正文作逐行差异。除常量历史说明、两处本附节T2引用、NP⊆QP／NP⊄QP修正外，证明正文没有其它变化。这些差异逐项核清，不静默认证未知变更。

再取新 tensor 附节之前的旧 canonical 前缀，恢复原文件单一末尾换行，SHA256 精确为

`9314ea1777df138b047587a391bba7ddf487ab5a3ecc94ef928425ed23e654c0`。

因此旧 v1/v2 数学和文字原字节保持；review保留该值为历史冻结版本，而非当前整页hash，正确。

review新增段如实保留 v1 原字节异议、v2修正、独立先行→作者读后顺序及方向勘误，六份原始来源 SHA 与本人记录一致。root另记录自己已实际全文读作者proof和全部审查并亲核q/P及代数；本审查不将其行为倒称本人新增运行。

无新代码或有限实验认证；作者的有限 Fraction 排印回算不作一般证明。外审、新颖性、论文价值及一般UM正反面状态不变。上述 canonical／review SHA 可作为已核最终字节保存。
