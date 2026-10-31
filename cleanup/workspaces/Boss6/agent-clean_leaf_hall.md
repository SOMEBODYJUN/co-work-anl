---
id: unrelated-machines/conditional-leaf-hall-v3-author-transport-proof-read
kind: review
type_tag: 审查
title: 条件叶 Hall v3 作者运输证明读后（Boss6）
status: integrated-into-canonical-review-pending-root-checkpoint
truth_status: restricted-R-cons-projection-proof-read-after
review_level: full-5886-byte-source-read-and-cross-archive-comparison
scope: v3 §9 MC transport, path matching mixtures, exact projection, Q_t boundary; no all-core joint law or generic UM hardness
summary: 完整实读冻结作者推导：以共同 hole law 的列边际和 z 下界构造每个 core-state 的运输表，得到 R_cons 的同一 global edge marginals；证明只在指定 core/path-leaf partition 下成立，并保留 matching mixture、zero/beta/d 边界与 Q_t 近二障碍的限制。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/conditional_leaf_hall_consistent_marginals_author_proof_v3.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/conditional_leaf_hall_consistent_marginals_author_proof_v3.md
  - clean:2c9423076f733f78f201
source_sha256: 730c5ef3af3861f123466d7e561111b363f5effb51c839efc0d6d284591d14c9
source_size: 5886
related_objects:
  - ../../state/审查/条件叶Hall投影与一致边际四源证明读后--审查.md
  - ../../state/审查/条件叶Hallv3新MC独立重构--审查.md
  - ../../state/障碍/一致条件叶边际仍无福利下界--障碍.md
evidence_paths:
  - archives/unrelated-machines/tools/evidence/conditional-leaf-hall-v3-author-proof-20261031/original/conditional_leaf_hall_consistent_marginals_author_proof_v3.md
---

# 来源身份与读取声明

clean ID 2c9423076f733f78f201 的冻结源为 history/source/notes/unrelated_machines/conditional_leaf_hall_consistent_marginals_author_proof_v3.md，5886 字节，源 SHA-256 为 730c5ef3af3861f123466d7e561111b363f5effb51c839efc0d6d284591d14c9。两个 source refs 是 legacy-cleanup commit 68fad804ec5946cb296f77dc5b336308a66abf12 与 main commit aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c 的同路径冻结版本。全文已用 clean show 导出并逐段读取。本源只证明冻结 Exact v3 的第 9 节（源中引用的 Exact v3 SHA 为 34244f9737bbbe7baa858482d31f8154f0e4146be0f1464c9e0598a402bfb38b）；第 1--8 节不被本源重写。来源是作者推导，不是 blind 独立重构，也没有声称运行 checker。

# 1. 作者运输构造

对每个旧资源 u，按正邻居 group 的固定顺序 c_1,...,c_d 写 b_i=sum_s z_(c_i,s,u)，b=sum_i b_i<=1。选共同 hole 分布 pi_i>=b_i，sum pi_i=1，例如将全部 slack 放入第一个 hole。hole i 的 one-hole path matching M_i 令 leaf j 在 j<i 时走 port j，否则走 port j+1（d=1 无新增 leaf，d=0 保留 unused resource）。令 y0=sum_i pi_i M_i；每个 leaf row 为 1，port i 的 leaf load 为 1-pi_i，加上 core load b_i 后不超过 1。不同旧资源路径不共享端点，故可逐资源拼接。

固定 core c=c_i 和 state s，记 lambda_s=lambda_cs、z_s=z_csu。构造非负运输表 w_(s,h)，满足 sum_h w_(s,h)=lambda_s，sum_s w_(s,h)=pi_h，且 w_(s,i)>=z_s。先置 w_(s,i)=z_s；残余行 lambda_s-z_s 与残余列 pi_i-b_i、pi_h（h 不等于 i）的总量均为 1-b_i；按固定次序以 min(row residual,column residual) 贪心填满，每步清空一行或一列。若 c 不是 u 的正邻居，则无 z 下界，直接取 w_(s,h)=lambda_s pi_h。该版本不除以 lambda 或 b_i，所以 lambda=0 与 b_i=1 自然闭合。

令 y_cs=sum_h w_(s,h)M_h。每个 conditional leaf row 总量是 lambda_s；own port 的 load 为 lambda_s-w_(s,i)，加 z_s 后不超过 lambda_s，其他 port 的 z 为 0。对状态求和得到 sum_s y_cs=sum_h (sum_s w_(s,h))M_h=sum_h pi_h M_h=y0，故 MC 逐 core/leaf-edge 等式成立。不同 core 可以有不同运输表；证明只共享 pi 的 edge-column marginals，不声称所有 core/state 共享一份完整 matching joint law。

每个 y_cs 是 lambda_s 倍的完整 one-hole matching 的有理混合，通常不是单一 integral matching。该点与已有独立 v3 重构一致，并说明不能把 v2 的单 matching 条款升级到 R_cons。作者明确 d=1 无 leaf rows、d=0 无 path flow；显式 zero incidence 仍保留在 private time-0 端点，不进入 z 或正值约束。

# 2. 反向投影、必要性和复杂度

R_cons 新行是旧 R1--R2 的子系统；对每个 path block 求和 d 个 global resource columns，再扣 d-1 个完整 leaf rows，恢复旧 basic column sum_(c,s) z_csu<=1，因此反向 projection 仍成立。实际 epsilon allocation 的 deterministic witness 每个 core 只保留一个 state；该 state 用 y0，其他状态流为 0，故 MC 不削弱必要性。

新增 MC 等式至多 |C| E_L 条，系数为 0/±1。每张运输表的 greedy 填充至多 O(|S_c|+d) 个非零格，坐标和比较在 supplied rational point 的多项式 bit-length 内完成；把各 path 的分割端点并集放入 [0,lambda_s]，可在多项式数量片段中拼出完整 matching mixture。来源只声称显式 rational LP/Farkas 证书的位多项式边界；没有 full CONFIG/PSD exact backend，也没有以 log(t) 计的 succinct output 结论。

自动 threshold 分区仍需原 groups 满足既有 non-threshold-original-group 前提；本构造没有偷偷重分区，D_+ 正邻居列表也不把 zero-only neighbor 加入 z。该限定必须保留。

# 3. Q_t 族与不能外推的边界

作者把运输表接回同一 Q_t 的 lambda,z=lambda basic point：epsilon=1 时，且固定 epsilon>0 取 t>1/epsilon 时，R_cons 仍可行；既有 Q_t 的 V(Q_t)=1/t 与 OPT=2-1/t 由先前 v2 对象承担，本页没有重做完整 schedule/value proof。因此本源支持“MC 不修复既有 Q_t 松弛障碍”的版本关系，但不单独认证任意 t 的福利公式。

作者明确缺少：所有 core 选择与完整 leaf matching 的共同 law；joint-core 条件 value/capacity；其他高阶矩约束；一般算法/硬度或 actual-OPT 近似下界；UM-TARGET-v1 结论。不能把 MC edge-marginal 一致性写成 all-core joint matching oracle，也不能将 t=2 有限审计或既有 JSON 计数外推为一般证明。

# 4. 与现有对象比较

现有《条件叶Hallv3新MC独立重构》已独立给出比例运输表、beta=1 分支和有限 fixture；现有《条件叶Hall投影与一致边际四源证明读后》已把另一份作者 read-after、canonical review 和独立证据合并。当前来源的独有价值是原始作者证明本身：先填 z_s 再按 min 贪心残余运输的无除法实现；明确 pi_i-b_i 与 1-b_i 守恒；非邻居 core 的 lambda*pi 表；直接由列边际 pi 证明 MC；zero incidence 的 private time-0、d=0/1、MC 行数和 Farkas/bit-length 范围；以及 Q_t 结论与旧 value proof 的版本分离。

该内容应作为 canonical review 的补充来源并保留原字节，不宜另造与现有审查重复的“已证明一般定理”。建议将原文件复制到 evidence_paths，并在 canonical review 的 source_refs、source_sha256、manifest 与四源比较表中新增本 clean ID；原障碍页保留历史 status，但增加作者证明 read-after/canonical review 已补充的关系说明，不能覆盖 source-only 的原始状态。

# 5. 建议处置与 receipt

建议 disposition 为 integrated（作者证明完整读取，写入 canonical review 的 restricted projection proof layer），而不是 duplicate、retired 或 needs-decision。它与已有独立重构/作者读后同一对象，但本源是 primary derivation，不能标 duplicate；数学结论只限 R_cons 指定 partition。

建议 receipt 语义：
- read_note：完整读取5886字节作者证明；核对 pi/hole matching、w transport、MC 求和、d=0/1、zero incidence、反向 projection、bit complexity 和 Q_t 版本边界。
- comparison_note：与 clean IDs e3bf2fef1967903a2e65、980f7d9ca13ea7f9a0b4、4c1d42084dbf3e593f 及现有障碍/审查对象逐项比较；独有 primary greedy transport，结论与 canonical review 相容。
- decision_note：integrated 到 canonical restricted-R_cons proof layer；保留不提供 all-core joint law、actual-YES hardness、full CONFIG/PSD 或一般 UM 算法的限制；不改写 v3 source-only 原始障碍。
- objects：unrelated-machines/conditional-leaf-hall-v3-author-transport-proof-read；unrelated-machines/conditional-leaf-hall-proof-canonical-read-after-20261031
- evidence：archives/unrelated-machines/tools/evidence/conditional-leaf-hall-v3-author-proof-20261031/original/conditional_leaf_hall_consistent_marginals_author_proof_v3.md

# 6. 复现/接续

作者来源本身没有附 checker 或可执行程序；复现依赖应只引用现有 independent-review evidence 和既有 finite JSON，不能声称本次重跑。第三阶段可从 canonical review 建立 author primary transport -> independent MC reconstruction -> restricted projection 关系；不得建立 MC -> common joint law 或 R_cons feasible -> actual scheduling approximation 关系。
