# 逐资源畸变完整菜单定理：首次完整作者证明实读审查

## 1. 对象、顺序与证据身份

审查人：`negation_logic`。本次实际全文读取的 canonical 是

`research/current/unrelated_machines/resource_distortion_flat_menu_rounding.md`

所读版本 SHA256：`3a863222725d5493f49691d5743425ecc1513c1e2d547bb161a0cd614409dbc7`。

这是我**首次读取作者的完整证明**。此前读过的 `source_promise_decoder_draft.md` 在当时仅有域、S1/S2 陈述与 PaperFact，没有作者证明，不能计为完整读后。更早的读前独立重构已冻结为 `resource_distortion_review_before_proof.md`，SHA256 `ea0619f9244d6e4a6e5fe97bdfc799bd1101fb533ba4af60fc7de09a57a01155`；root 明确在读过该重构后才写 canonical，故 canonical 不是与这份重构相互盲写。

后续我另核原始 Cheng–Mao α>4 后端，并冻结 `resource_distortion_backend_scope_review.md`，SHA256 `9509ab6f189202fa618a8963718d15ee7019eaf3a2a31f444127f3de78678791`。该文件不修改读前记录，也没有追认外部论文已被完整重新证明。

## 2. 审查结论

对 canonical 声明的精确完整 flat 域，没有发现 standing fatal。接受 Cheng–Mao 已发表 restricted Santa Claus Theorem 1 后，式 (2) 的确定性总位多项式实际分配结论可由正文所写转换成立。主目标 `UM-TARGET-v1` 的正反面状态仍 OPEN。

以下具体承重项已逐段实查。

### 2.1 域与零边界

G 非空、各 S_g 非空已写明；每组 selector 给 OPT≥1。全部 M_x 和 R_u 两两不同，消除了 private/resource 合并后的负载干扰。原 incidence 集可空，p=0 和 unused/all-zero resources 都合法；κ 的定义含 1，不作 0/0。空组集被明确排除在两段不等式链之外，空任务另返回零分配，正确。

### 2.2 baseline 版 V 与实际 OPT

正文式 (3) 使用的是 \(b_x+\sum p_{xu}\)，不是 W<1 时旧的无 baseline 菜单效用。由于 b_x+W_x=1，各 f_g 的值均在 [0,1]，有限菜单保证 maxima 达到。

正向给定两两不交 B_g，逐组选一个达到 f_g 的实际 state；其 private 负载恰 2−f_g，其余 private≤1，资源至多一枚 unit。即使导出某些零 p incidence，B_g 的不交性仍给资源峰≤1，因此全 jobs 调度合法。

反向仅在 C<2 下读 resource 独占，正确避免在 C=2 时把两件 unit 误当不可能。选中 private 给同一负载恒等式，推出 V≥2−C。OPT=2、V>0 时正向会给峰<2，矛盾，故 (4) 在 V=0 也闭合。没有额外输入最优调度或免费选择 V 见证。

### 2.3 restricted Santa 的两侧值界

每个原资源只建一件 real item，值 q_u=min positive p；并未按 incidence 克隆资源。每个 baseline 只被其原 state 感兴趣；每组 |S_g|−1 件 unit dummy 只被本组 state 感兴趣。这三类物品都严格是每件物品有固有值、玩家只决定零/非零资格的 restricted 域。

式 (5) 左侧：选中玩家的 baseline 与真实资源值向下比较损失至多 κ，其他玩家各拿一枚 dummy。κ≥1 支付 baseline 的比较，所有 auxiliary allocation 真实不交。

式 (5) 右侧：每组至少一名玩家没有本组 dummy；它的正效用至多 b_x+Σq≤b_x+Σp≤1。按组取这样的玩家，保留其正资格 real items，原 p≥q，因此得到 baseline 菜单分配，其最小值不低于当前 Santa allocation 的最小值。对最优 Santa allocation 应用即可得 V≥V_−。零价值或外组 dummy 不增加效用，忽略即可。

### 2.4 全部原任务的实际回译

§4 只导出选中玩家收到且有正价值的 real items 对应原 incidence；这些 items 全局不交，所以所有 resource 峰≤1。所有未导出的 incidence，包括未选 states 的全部 jobs 和 zero jobs，仍在原 private，各执行一次。baseline 没分给所选玩家也不造成缺口，因为可用上界是 a_x≤b_x+Σ收到的q，而非假定它必收到 baseline。式 (5) 还保证后端实际最小值 t≤V_−≤1，所以 2−t 同时覆盖资源和未选 private 的峰1。

第二段不等式差为 \(2(1-c)(O-1)\ge0\)，由 c∈(0,1)、O≥1 得到。若去掉非空 G，这段会失效；当前域已修正。

### 2.5 ≥ 型 NO 承诺及严格 ε

§6 的判别阈值为 τ=2−1/(ακ0)。YES 有 O≤1，而 selector 强制 O≥1，故实际输出峰≤τ。NO 有 O≥2−ε 且 ε<1/(ακ0)，于是任何实际调度峰≥O≥2−ε>τ。因此“输出峰≤τ”可靠地区分 ≥ 型 NO。

严格 ε 不可删除；在等号 ε=1/(ακ0) 时，NO 可能恰有 OPT=τ，会与 YES 允许的输出阈值接触。正文没有误用这一边界。随机归约也没有被升级成仅 P≠NP 的反证。

## 3. 位复杂度与外部 import：接受的准确读法

已直接核读 Cheng–Mao arXiv:1905.06084v1 原 PDF 的 restricted 定义、Theorem 1（物理第 2 页）、其后的未知目标搜索说明、§3 Build/Collapse、§4.3 Lemma 18 与 Appendix A 路径算法。原文给实际 4+δ 近似，固定 δ 时组合迭代为多项式；不是从积分间隙自行推导一个 finder，也不是沿用 DRZ 旧版错误的 4+ε。

组合状态只存实际资源子集、matching、层与路径。值比较是原输入值的有限子集和、固定有理参数倍和整数计数，确定性顺序足够；没有随迭代把分母相乘增长的新权值。正文有理清分母与辅助表大小说明正确，κ 只用于分析而不按数值循环。

正文 §4 的 `t≥V_−/a` 应按**直接导入完整的 Cheng–Mao Theorem 1 的 a 近似算法**理解；这个算法合同本身已经包含未知目标。该读法下 §4 的数值完整成立。

§5 又给了两种实现说明：单向成功目标例程或几何网格。若实际选择第二种，需把常数分层写清：先取固定 \(4<\beta<a<\alpha\)，选固定网格比 g>1 满足 βg≤a，以 β 后端输出 V_−/a；若还有近似配置误差，再在 β、a 之间支付。仅有 a<α 可以支付最终式 (2)，但若几何损失后仍逐字保留 `t≥V_−/a`，则应另选内部 β。这是实现文字的精化，不是当前直接 import 读法下的 fatal。

还有一种完全不损比率的标准补法，已在 `resource_distortion_backend_scope_review.md` 详细写出：清分母后真实 Santa 最优值 V_int 为整数；给整数目标 z 的组合算法加固定参数多项式时钟，精确验证实际输出。真实 V_int≥z 必成功，失败只能在 V_int<z。用 lo=0、hi=全部礼物值之和+1，成功增 lo、失败减 hi。只维护 hi>V_int，最后 lo=hi−1≥V_int，保留的实际输出给 V_int/a 保证；成功标签无需单调。这样不需要精确配置 oracle，也不会因错误目标而无限运行。

我已把上述精化通过 parent message 发给 root，未改 canonical。若 canonical 修改了搜索段，需另记录新全文 hash；本报告当前完整读取身份仅对应所列 `3a863...` 字节版本。

## 4. 独立有限审计的范围

我实际执行的 `resource_distortion_independent_audit.py` 不导入 canonical 或作者脚本。它独立枚举 1296 份二组/各二 states/二资源、p∈{0,1/2,1}、W≤1 的完整矩阵，并加 5 份零值/空资源/异分母边界，总计1301份。

共枚举1,328,275份原完整调度求真实OPT，20,798份辅助实际 allocation，并逐个回填原全部 jobs。α=41/10与7分别有10,770份满足近似前提的allocation，全部满足本接口；观察最大比率3/2。巨大分母样本也通过。脚本与JSON的SHA256已在后端scope文件登记。

这些有限数据只检查值比较、dummy-free读出和原job负载；没有实现 Cheng–Mao/DRZ 后端，没有证明外部算法、一般数学结论、全球新颖性或近二复杂度困难性。canonical 在§7保持了这些层次的分离。

## 5. 最终状态

**限定数学转换：** 实读后无 standing fatal。**外部算法：** 接受已发表 restricted Santa 定理，适用域和固定参数位复杂度接口已核，未独立重证全文。**实现：** 只有独立 finite audit，无完整后端。**复杂度推论：** 仅为固定κ完整flat像类的源筛选，P≠NP等假设按归约种类保留。**主目标、新颖性、外审：** 均未升级。

## 6. 实际重读实现措辞修补后的版本

root 修补 §5 后，我实际重读了 §4、§5 全段、§6 promise 段及相邻上下文。修补后 canonical 的 SHA256 为

`0da64ce52e3d85666aed7c3a156f68c09a699418e584512d851d82a02c3b05c5`。

两段变化已核：其一明确 §4 使用完整 a 近似算法合同，不再额外损失；若改用几何网格，先选内部 a0<a，再令 a0·g≤a。其二完整写出清分母后的整数目标、固定多项式时钟、失败方向、lo/hi 不变式、无需标签单调及 O(log U) 调用数。与本审查第 3 节的精化一致，没有留下 standing 实现措辞异议。

这次修改是实现合同说明的修补，不改变主定理、输入域、α>4 后端来源或 promise 分离阈值。第 1 节的 `3a863...` 对应首次全文实读，第 6 节的 `0da64...` 对应本次明确增量重读；不把两者混成同一版本。

另据 root 报告，独立 audit 复制到规范 tests 后删去了把 JSON 写在脚本同目录的两行，其余保留，并由 root 全文实读及 fresh run。该复制版代码的新 hash 由 root 单独登记；我未将本工作区原脚本 `7f90a...` 的 hash 冒充规范复制文件的 hash，也没有在本次只读审查中自行核读那份复制文件。

## 7. 实际重读固定实常数的有理 separator 修补

另一位读后审查者指出：α、κ0 的域允许固定实数，不能让判源程序直接对可能不可计算的 \(2-1/(\alpha\kappa_0)\) 作精确实数比较。这个实现边界此前并非由我指出，不追认为本审查先行发现。

root 修补后，我实际重读了 §6 全段及相邻的 §5 末段。最新 canonical SHA256 为

`983480e2db1676add57db68cbfd0f7eed4521cddc9c3152ef1de9fe6a283615b`。

新段固定一个有理 θ，满足

\[
2-1/(\alpha\kappa_0)<\theta<2-\varepsilon,
\]

比较实际有理峰与硬编码 θ。严格 ε 条件保证该开区间非空，有理稠密性保证存在这种 θ；θ 只依赖固定常数，不是输入参数，因此无需算法计算、编码或比较给定的实数 α、κ0、ε。YES 峰小于 θ，NO 的任何峰严格大于 θ，≥ 型 NO 的分离仍成立。

这关闭了固定实常数的比较实现缺口，未改动限定主定理、近似常数、结构域或严格 gap 数值条件。第 1、6 节各自记录的首次全文实读与前一次增量重读保持历史事实，不以本次最新 hash 覆盖它们。当前无 standing fatal。
