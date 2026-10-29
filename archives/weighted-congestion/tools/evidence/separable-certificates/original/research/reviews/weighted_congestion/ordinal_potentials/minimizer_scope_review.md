# 依游戏资源可分最小点选择：量词边界审查

审查基线：commit `ec827a977d6e800073b031959016a04509aca986` 的三个候选；新增 `WC-GAME-SPECIFIC-MINIMIZER-EQUIVALENCE-v1` 位于 `research/current/weighted_congestion/separable_ordinal_obstruction.md` 第四节。该新引理与原障碍分别记录状态，未提升全类目标。

新增引理所审现行稿 SHA-256：`dd881b2f38eb34b6bee395a5119ac4b5fe9778d19791fbedbe4946c604fd2654`。审查仅将该文件第四节的新引理与原障碍分开核对。

## 独立性及精确范围

子审查者先从 MODEL 重构了共同玩家乘子、闭路可积性、改善图无环和存在汇点的区别，随后读取三篇候选并逐步重算。未在读稿前独立发现其多尺度构造，因此这些旧障碍的核对属于 informed reconstruction。独立新发现的是：在任意固定游戏中，以入射对称差可唯一选择任意合法状态，故“依游戏可分目标的全部最小点为近似均衡”与均衡存在本身等价。主研究者随后独立重算双重计数及逆向最小值存在论证。

## 新引理的攻击

F_e(U)=|U△S_e(s*)| 合法定义于每个玩家子集，不要求该子集是任何玩家的策略。双重计数得 Σ_eF_e(S_e(s))=Σ_i|s_i△s_i*|。目标是合法状态，故零值可达；不同合法状态至少有一个入射位不同，唯一性成立。MODEL 的策略族是资源子集的集合，没有多个不同标签却同一资源子集的漏洞。空策略、全零费用、不同策略族和任意实权均不影响证明。

反向只需有限非空状态集上最小值存在。该结论没有假定目标函数对所有改善下降，也没有假定资源函数单调、可局部构造或跨游戏固定。若用此构造证明新的倍率保证，就把所需均衡放进了输入，论证循环；因此这里只是准确范围澄清。

## 三项旧障碍的 informed 核查

- `arbitrary_multipliers.md`（SHA256 `7c1b3046da1da452aa528f8d16f9dfc276fabffc14c262bb0b074e3d628fd7ac`）：同时平均 F 和 h、两路径比的负导数、有限 Riemann 和、相邻与首尾类乘子冲突均可重算。所有克隆在一个先选定的有限向量内，未见原范围 fatal objection。不是纯均衡非存在证明。
- `universal_additive_ordinal_bridge.md`（SHA256 `c11a5edb36b2a93296261a399d456b012ae8195b84a1e494b8a04b4eca155574`）：有理复制比较用的是跨游戏同一规则；固定参考正比值保证 inf>0；两状态限制要求规则独立策略族。依整个游戏重新选 F_e 时不能使用该推理。
- `game_specific_separable_ordinal_barrier.md` 的原稿（SHA256 `099fe036a70194c4daaaa66abe176b1c250e1b3cf8f5cf9630f838723cd6fd3d`）：先固定有限资源数再量化任意 F_e；资源置换确为同一个游戏的自同构，平均保留严格性。有限复制包给 R 夹逼，故只排除“全部 alpha 改善严格下降”的可分势；不排除本次最小点目标。此旧稿审查不覆盖今后未见修订。

这些核对未发现实质反驳，但不冒称读稿前独立重建原构造。旧命题仍沿原账本的审查级别记录，本文件不以 informed 核查代替其所要求的独立攻击。

## 精确实现核对

本次规范审计 `tests/audits/weighted_congestion/template_certificates/verify_template_certificates.py` 的资源成本 oracle 直接重建真实负载；输入 `examples/weighted_congestion/template_certificates/exact_fixtures.json` 含空策略、零资源、未使用资源、常数、多项式混合、单动作及异质策略族。对每个目标状态和每个状态，逐一核对上述双重计数及零值唯一性；冻结输出记录实际数量和源码/input hash。该有限检查不提供新的近似上界。新引理的一般证明不依赖外部定理，外部评审及新颖性没有认证。
