# wc493 恢复：锚定门、社会下降与联合转移复核

本轮为父 worker 的局部数学复核；不修改公共正文、registry、边或收据，不进行 Git、网络或队列操作。

## 实际实读范围

- 完整 `AGENTS.md` 与 `prompts/03-map-worker.md`。
- 全文 `archives/weighted-congestion/state/定理/完整锚定门的稳定集合与有限修复--定理.md`（100行）。
- 全文 `archives/weighted-congestion/state/定理/锚定门的社会费用分解与最优压缩--定理.md`（100行）。
- 全文 `archives/weighted-congestion/state/定理/正则化核心的稳定与社会质量联合转移--定理.md`（95行）。
- 当前 registry 中 `WC-FRONT-CORE-STABLE-SET-TRANSFER-v1` v2、`WC-SOCIALLY-DESCENDING-REPAIR-v1` v3、`WC-REGULARIZED-CORE-REPAIR-QUALITY-v1` v3 的完整对象记录。
- 全文边 `anchor-repair-pays-trigger-contribution.json` 与 `regularization-rt-sd-joint-front-guarantee.json`。
- 任务收据中上述两个核心（社会下降、联合转移）的完整 coverage，以及三条相关 closed_overlaps；稳定集合对象为共享 read 端点，不是本包 coverage 核心。

本轮未读 `research/IMPLEMENTATION.md` 正文（仅查看文件大小），未读完整任务、共同尺度源正文、历史审查/计算/连续稿/账本或它们的附件；因此不把本轮当作这些范围已支付，也不验证共同尺度源对象本身。父 worker 已要求不再扩大读取，接回余项。

## 数学复核结论

1. RT 的模型与量词一致：有限二动作基体、每类内部等权、完整锚定三元且门与基体/其他门资源不交，全部真实单方偏离。前沿并非动作笛卡尔积。非法态最早异位修复后，含 mover 的门全部不触发，至少一门原触发；RD 排除非法稳定点。前沿保域边上 mover 在每个关联门的两端都处于二人侧，门费恰为 u，所以容差 `(alpha-1) r_i u` 的符号与方向正确。alpha>1 不能把受限基体稳定集包含关系改为相等。调度步数只针对指定修复，不保证任意改善路。

2. 社会结构贡献正确且必须保留为 contribution。逐门社会费为未触发 `w(2u+z)`、触发 `3wv`，故全状态分解与 K 正确。指定修复严格减少触发数而不增加其他触发；在无 SD 时只能得结构结论，不能声称完整社会成本严格降或 OPT 在前沿。非负非递减门值使 d=3v-2u-z>=0；SD 提供严格下降所需正余量。

3. 真实社会外部性界正确：对进入资源旧 x、新 y=x+w，`y^(k+1)-x^(k+1)<= (k+1)w y^k`；退出资源不增、保留资源不变，故 `Delta W_B <= (p+1)w_i C_i^B(new)`，其中计入所有必用/背景用户。只有 SD 支付此项后才能压完整 OPT。RD⇒SD 的链使用 alpha>=1、L>=1、z<=u 以及 3alpha>=p+1，严格性来自 RD 首步。六玩家反例与正向三人例的合同边界一致。

4. 联合转移目标正文的自足证明成立。在相同共同 h_i 插入合同下，社会插入边际给新共同尺度 h_i+eta w_i 和 beta_eta。对两端都在前沿的真实偏离，把删/增/保留成本记 A/B/H，严格 beta 改善推出 A>beta B，势差严格负，故前沿全局最小点受限稳定；RT 在新 beta 的 RD 下提升完整稳定。前沿全局双点比较给 lambda=(M+eta)/(m+eta)；SD 给完整 OPT=K+min_F W_B，K>=0，再得完整 lambda 质量。无需把前沿称子游戏，不除 OPT，覆盖零费用。局部最小和加性 gap 不能自动给同一联合合同。

5. 目前两边的方向与 whole/contribution 分界准确：RT→SD 只作结构 contribution；共同正则化+RT+SD 的三源 ALL 指向联合转移 whole_result。共同尺度源的全域 PNE 不能直接限制到非积前沿；现边已逐式给域桥，目标正文也自足给出该桥。基体 p 与新增门次数分开，原门 alpha=1 的 RD 与新 beta=3/2 所需门参数分开，现边/正文没有混用两个游戏的 K、次数或 OPT。

## 修改与未付义务

在上述实际实读范围内未发现需要修改正文、registry 或这两条边的数学错误。相关三条 closed_overlaps 均有具体已解决理由，可以保留；不存在由本局部复核新增的 follow-up。

父 worker 仍须自行核对本轮未读的共同尺度源及全任务其它材料，并核收据既有较大“完整实读”范围是否有真实历史/本轮付款证据；此局部记录不能替代它们。最终 pins/bind/checkpoint/done 由父 Boss 串行完成。
