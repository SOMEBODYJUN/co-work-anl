---
id: customer-attraction/r2fc-root-potential-independent-replay-and-truncated-probe
kind: computation
type_tag: 计算
title: R-2fc 根势独立复放与截断势探针
status: fixed-candidate-replayed
truth_status: finite-evidence-retained; no-general-half-conclusion
review_level: source-level-read-and-independent-replay
scope: 3名顺序提供者、6主题、有限单位客户、完整有序历史纯SPE；给定策略/候选的精确证书与固定q/r浮点探针
summary: 四个global_proof源均已全文读取。78客户固定策略的Fraction复放得到W=54、OPT=75、Phi=Psi=141/2；脚本的minimized分支得到同策略11客户点W=8、OPT=11、Phi=21/2。截断势LP探针仅是固定Markov策略锥中的有限浮点发现器。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/root_potential_independent_audit.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/root_potential_independent_audit.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/truncated_potential_audit.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/truncated_potential_probe.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/root_potential_independent_audit.py
related_objects:
  - ../反例/三人均衡调和势低于最优覆盖的十一客户证书--反例.md
  - ../资源/无拥挤完整均衡族原稿与有限探索的准确范围--资源.md
  - R-2fc全局证明八源的精确核查与工具边界--计算.md
evidence_packet: ../../tools/evidence/R-2fc-global-proof-c-20261031/
---

# 对象与量词

对象是给定六主题目录、给定 3 人完整策略和给定客户类型权重下的终局覆盖与离轨单步偏离。根脚本把每个掩码类型展开成单位客户，按全部有序历史 h，深度为 0、1、2 检查当前策略动作与每个替代动作的真实均分收益。它不搜索策略空间，也不把一个固定候选的证书当作全部纯 SPE 的分类。

截断势记为：对每个主题负载 c，先取调和数 H_c=1+1/2+…+1/c，再分别求和得到普通势 Phi 和截断势 Psi，其中 Psi 的每项为 min(2,H_c)。
给定候选的 `root_potential_independent_audit.py` 同时核验普通势和截断势；`truncated_potential_probe.py` 只在随机权重和 Markov 逆向策略形成的有限锥中用浮点 LP 寻找 Psi−OPT 负点。

# 78客户固定候选的精确证书

权重支持为：mask 1 重复 7 次，3 重复 3 次，4 重复 12 次，6 重复 3 次，9 重复 5 次，18 重复 3 次，19 重复 6 次，22 重复 1 次，30 重复 5 次，32 重复 15 次，56 重复 18 次，共 78 个单位客户。策略规则给出根动作 1、见首动作 5 的次动作 1、其它首动作的次动作 5，并在末位对排序后的前缀 `(0,5),(2,5),(3,5),(4,5),(5,5)` 使用回复 (4,4,1,2,1)，其余回复 5。固定候选的实际终局为 (1,5,5)。

独立 Fraction 复放逐层检查 43 个有序历史、258 个含自身动作比较，其中 215 个是真正偏离，最小余量为 0。终局收益为 (21, 33/2, 33/2)，负载直方图为 24 个零负载、21 个一负载、33 个二负载。因此 W=54，OPT_3=75，Phi=Psi=141/2，Phi−OPT=−9/2，2W−OPT=33。
最优覆盖由有序元组 (0,2,5) 达到。这个结果精确否定“该固定候选的普通或截断调和势必支付最优覆盖”的桥；由于 (2W>OPT)，它没有否定六人 half 命题。

# minimized 分支与既有11客户对象

同一脚本的 `--minimized` 分支将权重压为 11 个客户，保留终局 (1,5,5)，逐历史 258 项比较仍全部通过，得到 W=8，OPT_3=11，Phi=21/2。这与既有[三人均衡调和势低于最优覆盖的十一客户证书](../反例/三人均衡调和势低于最优覆盖的十一客户证书--反例.md)的客户表和数值一致；当前源只负责独立复放和最小化输入分支，不能据此声称独立发现、最小客户数或外部认证。该点仍满足 2W−OPT=5。

# 探针用途与缺口

`truncated_potential_probe.py` 由随机非空掩码权重、有限 Markov 状态、逆向选优和 `linprog` 约束组成；对每个随机候选只抽最多 12 个比较主题，浮点目标为实际终局截断势的单位基线减去候选主题 fresh 覆盖。3 次 smoke run 为 `best=0`、退出码 0、无 stderr。该有限无命中不能推出所有策略、所有输入或所有纯 SPE 的势不等式；线性规划的浮点 incumbent 也不能替代 Fraction 全历史证书。

本对象的接续用途是：把 78 客户候选和 11 客户压缩点作为调和/截断势路线的固定障碍，和碰撞自由五客户/任意 k 族、背景首步及 52 客户整体反例分开比较。任何试图证明 Q-CAG-HALF-6 的后续工作必须另行支付真实离轨历史、重复客户和任意平局，不能由本批四源的有限复放代替。
