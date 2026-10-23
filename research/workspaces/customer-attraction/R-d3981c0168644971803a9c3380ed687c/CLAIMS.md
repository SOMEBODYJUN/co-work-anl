# 精确命题身份（个人区）

## ROOT-ONLY-REPAIR-3-v1

- Objects/domain/quantifiers：每个原CAG-MODEL实例、每个m>=2、每个完整纯计划tau，其在每个正深度子局已为SPE；根A不必最优。全部有序历史、重复/空主题、任意历史平局保留。
- Definition：u为实际根收益，d_B为按原tau完整后继的真实根偏离收益，Delta=max_B d_B−u>=0。给定有理s>=Delta且s>0。
- Conclusion：存在同m单位提供者、合法新共同Cartesian目录的完整纯SPE，旧坐标实际路径不变；W_new=W_old+(m+1)s、OPT_new=OPT_old+(2m−1)s、gap_new=gap_old−3s。有理账面数共同整数缩放成单位客户。Delta=0时旧计划已经SPE，无需修复。
- Dependencies：分支后独立Cartesian收益可加，H/L_X/L_Y/leaf-BI完整续局，最优组合可按位置同时配对。
- Evidence/status：自足一般证明及作者Fraction联合全树核验；independent/insurer_blind_review.md独立盲重构与定义级回放未发现致命异议。内部解析可靠，未外审/未认证新颖性；非Q-CAG-HALF解答。
- Related：compiler/padded_insurer_{statement,repair}.md、audit_padded_insurer.py/.json、independent/insurer_blind_*。

## ROBUST-ROOT-ONLY-3-EQUIV-v1

原Q-CAG-HALF（对所有共同目录，固定任意m>=2）等价于：每个上述root-only计划均满足OPT_old<=2W_old+3Delta。正向对Delta>0应用ROOT-ONLY-REPAIR-3-v1、取s=Delta并清分母；Delta=0直接用原命题。反向在完整SPE取Delta=0。该等价不证明任一边；当前状态OPEN等价重述，不冒充新half机制。

## 其他待独立审查对象

compiler/disjoint_insurer_three_sharp.md（准确架构三系数锐下界）、shared_omission/credible_degree_two_negative_flux.md（真实完整SPE无条件驻留负flux）各以正文量词为准，审查未完成时保持作者结果身份。
