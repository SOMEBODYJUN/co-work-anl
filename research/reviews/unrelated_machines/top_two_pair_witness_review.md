# 双件证据三半边界：独立重构、实读与软件范围

本记录覆盖三个精确身份：`UM-TOP-TWO-MATCHING-APPROX-v1`、`UM-PAIR-WITNESS-HARDNESS-BARRIER-v1`、`UM-TOP-TWO-THREE-HALVES-HARDNESS-v1`。判定：在所列最终正文范围内未发现仍成立的 fatal objection；完整自足限域证明可内部使用。外审、全球原创性未认证，普通 UM 主目标及其一般反面保持 OPEN。审查不是投票。

## 冻结文件

| 实际路径 | SHA-256 |
|---|---|
| research/current/unrelated_machines/top_two_pair_witness_boundary.md | `75a08a63fbfa2096731f49323b5134dc2df79c2d6705d8b9ba1e505640b49a8e` |
| tests/audits/unrelated_machines/top_two_pair_witness_audit.py | `e307943d7a4f2d1013a4524209806fa02807b609624a3418f75ad50e44b84ef3` |
| tests/audits/unrelated_machines/top_two_pair_witness_independent.py | `0d4749f6896508c0422a166c6c0cd63811a640da2baa764b5562c7507aad23a9` |
| evidence/runs/unrelated_machines/top_two_pair_witness_audit.json | `8fa37fd25837d71a9935295925895e7a0ea1a632d82a61e88e7ae0d2241874fa` |
| evidence/runs/unrelated_machines/top_two_pair_witness_independent.json | `343ccb0fe2afb63d66484acc9bb72b690930b2bf5fdabb098862ebc87dd59c65` |

## 实际独立性与阅读顺序

1. root先收到一般pair匹配机制，独立推出更强的O₂目标与完整断点搜索。`negation_bitcomplexity`只收到该加强陈述，未读作者proof便重构q_j、strict重集、覆盖matching、FAIL健全性、端点规则、零/空与位复杂度；之后实际读作者完整英文proof，未发现数学fatal。
2. `near_two_gadgets`先只收到sharpness陈述，独立构造出现位置unit/filler/clause全矩阵，证明任意pair-safe分配迫环同值并解码源赋值，逐机核YES及三半上界；之后读作者literal-copy证明。它此前读过仓库旧query/return障碍，所以不把本次记录夸成完全不知领域机制的blind review。
3. `lp_gap_to_hardness`另从陈述重构匹配与源decoder，再实际读最终中文正文全篇及作者BFS软件。第一次所读中文正文哈希c95b7da84e717755a7e2a56a60f4cfb2677bc3d30a43d3e7f1abc75f72388f91，主BFS原稿a42be6b0fd286945775514d06ac4e7d5b6ed446cdd476732d2e56dccb126552c。独立重放原软件并查Hall oracle、长路径及大分母边界，未发现fatal。实际软件阅读与数学重构分别发生，不以测试代审查。
4. root核读作者完整稿、全部BFS审计及全部独立枚举源码，重写最终中文自足正文；实际读本页冻结版本全部章节。最终§5的表示说明由审查纠正：两实现的cycle方向相反，须逐变量反转循环顺序后识别文字端口，而非在固定循环/原文字不变时仅重命名端口。所有数学陈述及证明不变。该实质表示差别如实记录，不虚报字节相同。

## 逐项攻击

- B₂含singleton及空机零值；不能漏掉单件超阈值。H_T用2q_j>T，保留端用p≤T；等号属于轻件与可用端。匹配失败严格推出O₂>T，成功只给B₂≤3T/2。
- 断点仅原finite时间和二倍minimum，谓词单调且首次成功闭合；输入的巨大分母不会制造按数值时间迭代。空任务先返回，避免按巨大二进制m展开无用输出。
- pair-NO量化所有保留端实际分配，成功输出直接反驳NO；只对canonical分配说明冲突不足。两choices的2SAT只适用于pair约束，不冒充总容量判定。
- 源归约每个出现单独复制；每副本文字至多两次，unit与half都是原job，所有机资格度≤3。每个任意B₂<3/2输出的half目的地给真文字，环迫副本一致；ρ=3/2不能继续使用strict NO。重复文字、singleton与两元素环均闭合。
- 完整任务执行与全部机器负载在YES中分别核对。top2输出的普通负载可无界差，因此不把该上界升级为UM-TARGET-v1算法；三半下界不升级为趋二下界。

## 实际软件修复与有限范围

主审计原稿递归增广可能受Python递归深度影响；发布前改为迭代BFS并重新运行。输出改为必选新路径、exclusive create，避免覆盖冻结证据。独立代码旧pair评分未计singleton；所选实例数值因unit下界不变，但发布前明确改为完整B₂，并查singleton边界。独立代码移入tests后默认repo定位曾错误；root修为parents[3]，失败没有生成输出，随后在canonical路径实际重跑通过。

主canonical代码实际运行检查85,219个编码矩阵，其中68,201个合法（另外17,018个无有限端的编码只测拒绝）；全分配oracle比较O₂、输出及断点单调，含2,401个零值例、10,993个三半等号例。256个指定两变量unit/binary CNF模板（95 SAT、161 UNSAT）枚举50,625份unit放置；不是穷尽全部3CNF。另有100位分母的Fraction边界。

独立canonical代码枚举四个具体出现位置矩阵的全部37,440份完整原assignment，包含36,864份UNSAT例；全部机器总负载、B₂和每份低pair分配decoder都实际核对。其余为三组各192份边界。源码不导入主舍入核心。一般证明不依赖这些计数。

root另用不持久化的独立小oracle查2机、n=0..3的3,616份合法矩阵及seed25的400份有理随机矩阵，均通过；此临时核验未列为完整可复现资产，不作为Evidence主链。发布后的迭代实现另实际走1,100任务交替路径，避免只改源码未测深路径。

重放（输出换成全新scratch路径，不覆盖evidence）：

```sh
python3 tests/audits/unrelated_machines/top_two_pair_witness_audit.py --base-commit 22b3f24bc34bf0545b45a411829bb41a520f1758 --output /workspace/scratch/03110e73ccb8/pair-replay.json
python3 tests/audits/unrelated_machines/top_two_pair_witness_independent.py --output /workspace/scratch/03110e73ccb8/pair-independent-replay.json
```

这些程序是audit_only。没有验证任意位长的具体Python运行上界、全球文献优先权、普通makespan最优求解或任何近二NP归约。全称位复杂度由正文的显式匹配与有理比较证明，而非有限Python执行认证。
