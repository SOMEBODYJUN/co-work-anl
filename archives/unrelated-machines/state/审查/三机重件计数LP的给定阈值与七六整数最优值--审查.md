---
id: "unrelated-machines/three-machine-heavy-count-given-threshold-and-seven-sixths-optimum"
kind: "review"
type_tag: "审查"
title: "三机重件计数LP的给定阈值与七六整数最优值"
status: "workspace-counterexample-reconstructed; exact-finite-QA; LP-optimum-not-computed"
summary: "保全T=1强化指派LP证书和真实OPT=7/6，补全对全部调度的两件任务下界，不误称T为最优LP阈值。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/unrelated-machines/R-3bcf9ec8b38a45c3b115183a4e41350b/notes/tiny_heavy_count_lp_gap_3machines.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/unrelated-machines/R-3bcf9ec8b38a45c3b115183a4e41350b/notes/tiny_heavy_count_lp_gap_3machines.md"]
---

# 对象、量词和给定的LP点

这是普通不相关机 makespan 的一个四任务、三机器小例，全部有限时间严格正。源是工作室笔记，不是一般算法或困难性结论。固定阈值 T=1，考察指派约束
\[
\sum_i x_{ij}=1,\quad x\ge0,\quad
\sum_jp_{ij}x_{ij}\le1,\quad
\sum_{j:p_{ij}>1/2}x_{ij}\le1\quad(\forall i).
\]
严格大于半才算 heavy；等于半的端仍为轻端。时间表及实际提供的分数点为：

| 机器 | p₁ | p₂ | p₃ | p₄ | (x₁,x₂,x₃,x₄) |
|---|---|---|---|---|---|
| A | 3/4 | 1 | 2/3 | 1/2 | (2/3,0,0,1) |
| B | 2/3 | 1 | 3/4 | 2/3 | (0,0,1,0) |
| C | 1/2 | 2/3 | 2/3 | 3/4 | (1/3,1,0,0) |

四列各和为一。三行分数工作量依次为 1、3/4、5/6，严格 heavy 分数质量依次为 2/3、1、1，因此这个强化LP在给定阈值1确实可行。任务1的分数跨了 A 上的 heavy 端与 C 上的轻端；不能把“任务是否heavy”当成与机器无关的类型。

# 完整整数最优值

任何不可拆分分配将四件任务放在三台机器上，必有一台执行至少两件。各机器最短两件的时间和是
\[
\min_{j\ne k}(p_{Aj}+p_{Ak})=7/6,\quad
\min_{j\ne k}(p_{Bj}+p_{Bk})=4/3,\quad
\min_{j\ne k}(p_{Cj}+p_{Ck})=7/6.
\]
任务非负，执行更多件也不会减少负载。所以每份完整整数分配的峰值至少7/6。这补全原笔记从“不能做到1”转到“不能严格低于7/6”时需要的统一下界，不只列1阈值上的排斥。

取任务1→B、任务2→C、任务3及4→A，三机实际负载为 (7/6,2/3,2/3)。故
\[
\operatorname{OPT}_{\rm integer}=7/6>1.
\]
这反驳了“加入每行至多一份严格heavy分数质量后，LP在T可行就有实际T调度”。它给出相对于**所提供可行阈值**的7/6差距；本批没有求这个阈值依赖LP的全局最优值，不能写成“最优LP值恰1”。若将LP最优值记为L，本例只直接给 L≤1，因此OPT/L至少7/6，而非已算出精确比值。

# 相关数学、有限证据与接续

[逐机跨度≤2的联合槽舍入](联合选择槽舍入三源精读--审查.md)另有 `>T/3` 等整数前缀约束和一次全局匹配，不能把本例只加 `>T/2` 的较弱LP当成那个完整算法；本例各行跨度本身也不反驳受限算法。[整数前缀证书草稿](整数前缀槽预算的共同证书与搜索缺口--审查.md)进一步区分行内分数负载与完整槽包络。

本批从零写的 [Fraction小审计](../../../../tools/evidence/um-missing-one-pin-kernel-primary/independent-small-audit.py)在新空目录执行恰一次，枚举全部3⁴=81份实际分配，核对上面的最优值、给定x、严格heavy量和成对下界。输出见[精确报告](../../../../tools/evidence/um-missing-one-pin-kernel-primary/run-small-exact/report.json)。没有LP求解、浮点容差、旧程序重跑或近二下界认证。

源全文74行的身份、正时间矩阵、分数可行点、实际不可行性/7/6见证、局部强化失效用途均保全；未把它升级为当前canonical、一般UM算法、NP难性或新颖性。可接续研究哪些共同约束有必要，但不能只凭这个小例断言所有强化都会失败。完整原件见[原文](../../../../tools/evidence/um-missing-one-pin-kernel-primary/original/dfb63d624df20561d5c2.md)。
