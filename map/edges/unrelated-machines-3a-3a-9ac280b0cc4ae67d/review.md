# DegreeTwo 四近似的承重链与同域算法比较

## 任务、端点与判定

本包为 `unrelated-machines-3a-3a-9ac280b0cc4ae67d`，owner Boss6。当前核心 `M-e52574ff126d4b128f222053c97bf596` v3，pin `eff19fc84cf112c156c8fc3228f91b9cc55f928a88b6b3bc21fd9c5a2094130f`。追加只读端点为 `UM-VW2010-THEOREM12-BACKEND-PRECHECK-v1` v1，pin `16a2920abfebbaed76d2492aee350d1b801fcfe5eb40c65c9a4f33ddddb02584`，以及 `M-de7aec4bd7c24b0f9dc342c483c4a75e` v3，pin `dc433f81a5ec38885a9666f9dadbf2e7adf6f91d9422b60af76704fe9d0a4d24`。

结论是：原 DegreeTwo 的 M-LP/树舍入四近似有完整可用的承重链；同域组合二近似改进近似因子，但不证明那份指定 M-LP 算法的正确性；严格二硬度与四近似相容。本包保留一条 `supersedes/context`，核心覆盖用 `isolated-after-review`，不将语境边冒作完整逻辑支持，也没有未付清的算法正确性义务。

本次完整读取成熟 PCSP/MaxMin/平行重复三源正文，以及 VW 后端的完整成熟正文和其 evidence 中 Theorem 12 的完整节；MaxMin 原 PDF 实读物理/印刷第 6–12 页，并视觉核对第 7、10、11、12 页。第 8 页的 Thm2.3 打包论证和第 9 页的降度也已读，但四近似证明不调用 Thm2.3 的 promotion 减 z 步或任意 raw CONFIG(M/2) 桥。没有重读全部 49 页、重跑旧程序、证书或有限枚举。

## 原始阈值重估与 M-LP 的用途

玩家集合非空且有限，物品有限，物品不可分且至多分给一玩家；估值非负、加性，每件物品至多两个正价值玩家，两端正值允许不同。以下算法及位复杂度保证在显式有限非负二进制有理估值域陈述。未使用物品可由非负性任意补配；OPT=0 的实例直接输出合法完整分配。符号 ∞ 若在其他对象出现，不能据此改写本包二近似端点的有限值合同。

给 M>0、λ=4，按端点定义 big：原值 p_ij≥M/4。重估值 R_M(p)=M（p≥M/4），否则 R_M(p)=p；small/big 是玩家端标签，同一物品可一端 big、一端 small。原文 PDF 第 6 页采用“≥”，Figure 3 第 12 页写“bigger than”；阈值相等时两种归类都保持最终 M/4 保证，本稿统一用“≥”。

R_M 不要求点态不减：原值大于 M 时会封顶。真正需要的是两件事。第一，任何原 CONFIG(M) 配置若有 big 端，可删成一个该端物品，重估值恰为 M；若无 big，全部端为 small，原值和不变，仍至少 M。因此原 CONFIG(M) 可行推出此重估域的 M-LP 可行，尤其原整数 OPT≥M 时成立。第二，最后分给玩家的 big 物品在原估值下仍至少 M/4；small 分配的值不变。这正是阈值重估的可行性来源和解码合同，不需要任意参数下 M-LP 与 raw CONFIG 的等价。

使用 PDF 第 7 页式 (4)–(8)：物品容量 Σ_i x_ij≤1；big 质量加 z_i 至少 1；small 加权和至少 M z_i；每个 small x_ij≤z_i；变量非负。CONFIG 到 M-LP 的具体见证也可令 z_i 为 all-small 配置的总概率：small 边际不超过该概率，small 配置各自至少 M，big singleton 概率加该概率为 1。故不需借助 Thm2.3 从 M-LP 反向建立 CONFIG(M/2)。

## 半整数重排给出的真实不变量

可先把零估值端的 x 归零，再减少 small x 使 small 加权式取等。保留零支撑，把每个非零 fractional x 置为 1/2，并把 small 上原先为 1 的 x 也截为 1/2。因此每个正 small x 恰为 1/2；有 small 支撑的玩家舍去全部 big 边。

DegreeTwo 的用途是物品容量：每件物品正支撑至多两个。如果没有保留 x=1 的 big 端，至多两个 1/2；若有 x=1，另一端原为零且仍为零。因此容量保持。对于原 z_i>0 的玩家，由 x*_ij≤z*_i 与 Σ_small p_ij x*_ij≥M z*_i 得

\[
\sum_{j\in S_i}p_{ij}\ge M,
\qquad S_i=\{j:\text{small 且 }x^*_{ij}>0\}.
\]

所以新 small 价值为 (1/2)Σ_{S_i}p_ij≥M/2。令新 z_i=(2/M)Σ_small p_ij x_ij，则 z_i≥1，覆盖式成立且 small x≤z_i。该论证按权重求和，对任意异值 small 端成立；不要求 small 值都是 1，不要求 M 是物品数量。

原 z_i=0 的玩家没有正价值 small 使用，其 big 总质量至少 1。若唯一正 big 支撑，它的质量必为 1；否则重排后至少两个 1/2。因此每个 big-only 玩家仍有 big 总质量至少 1。可仅在 big-only 行删减支撑至总质量恰 1，不损其他玩家及容量；质量为 1 的 big 物品可直接固定给该玩家并移除该玩家，其物品另一端当前 x 为零。

这里真正使用的是“small-only 玩家值≥M/2，big-only 玩家 big 质量≥1，small 正边为 1/2，物品容量合法”四个不变量。原文 SP3 所谓 value M/2 应在保留端标签的归一化覆盖意义理解：若要按 Definition 2.2 的字面形式重写，big 代表值应同步重标 M/2（并相应调整 small/big gap 参数），不能把原 big 数值 M 与新阈值 M/2 的字面等号条件混用。后续证明直接使用上述不变量，无须重新分类物品。

## 大边旋转、树叶替换与实际解码

在 big-only 玩家与其正 big 使用物品之间作二部图。沿偶环交替加减 ε，取至至少一个边权为零（或为 1）的位置。玩家行和与物品使用量均保持，small 外部使用不变，正边数减少。big 行预先归一为 1，因此出现质量 1 的边时该玩家其余 big 边为零，且物品其他端为零，可按前述固定删除。有限次后剩余分量为树，每个玩家度至少 2，故所有叶都是物品。

每个内部物品在树中连接两名玩家；因为总正度≤2，它不能另有树外正值玩家。一棵树有 n_t 名玩家、k_t 片物品叶，内部物品数恰为 n_t−1。任选一片叶作根，把根物品及每个内部物品交给其下一名玩家，就给全部 n_t 玩家各一 big 物品，并留下其余 k_t−1 片叶。此处“恰好用一片叶”是存在的规范化选择；不能字面扩张成任意分配都恰用一片叶。

如果有一片叶没有外部正 small 使用，可直接将它保留为根，全部其他叶照原 small 使用进入舍入。余下非平凡情形中，每片叶对应至多一名树外 small 玩家，使用质量为 1/2；该叶的外部端价值<M/4。将 k_t 片叶配为相邻对，以 ceil(k_t/2) 个虚拟 small 物品替换：若两叶外部玩家不同，虚拟物品在两端沿用相应原叶价值，各用 1/2；若同为一玩家，虚拟物品的值取两个叶值的 max，使用质量设为 1，贡献不小于原来两份 1/2 贡献；奇数叶的最后一个虚拟物品仅有一外部端，使用 1/2。容量均≤1，small 玩家值不减，最大正使用端仍<M/4。

忽略 big-only 玩家，对这些虚拟物品以及其余真实 small 物品应用原文第 11 页 Theorem 3.2（Bezáková–Dani 的 LP-Round）。其合同是：从值至少 L 的自然指派分数解，按正使用端的最大物品值 p_max 舍入，得到实际整数分配且每玩家至少 L−p_max。本处 L=M/2，p_max≤M/4，故 small 玩家至少 M/4。它是 MaxMin 目标下的外引舍入定理；不能用 makespan 的 LST 上界句直接替代它。

一个虚拟物品分给其正价值端时，选择该端对应的原叶即可解码；同端配对取 max 的那片叶。每棵非平凡树最多因此消耗 ceil(k_t/2)≤k_t−1 片叶（k_t≥2），至少留下一片叶作根，按上一段规则满足整棵树。没有外部使用的叶保留为根的情形也已付清。全部真实物品都至多使用一次，big 玩家每人原值≥M/4，small 玩家原值不变也≥M/4。big-only 全覆盖时可直接做树分配，无需空的 small 子程序。

于是对每个成功的此 λ=4 M-LP 阈值 M，指定重排/树算法均构造原实例的实际 M/4 分配；这是核心中“指定算法”部分的独立原证链，不是由新二近似推出的。

## 重复猜测不需要假设 M-LP 成功前缀

以下仅补足原 Figure 3 “repeated guessing”的位复杂度接口，不宣称任意 cap 扩展都有单调成功谓词。把全部有限有理 p_ij 乘共同分母变为整数，分母乘积位长受输入总位长控制。令 U=min_i Σ_j p_ij，整数 OPT≤U；U=0 单列。M-LP 不可行能推出原 OPT<M，因为原 OPT≥M 时前述原整数配置到重估 M-LP 的映射成立。成功则按本节原算法输出实际值≥M/4，成功本身不能被解释为原 OPT≥M。

可设 low=0 并保存任意完整分配，high=4U+1。在给出 U 的最小总价值玩家那一行，所有原值≤U<high/4，故无 big；其 small 总价值≤U<high，而覆盖式又要求 z_i≥1，所以 high 的 M-LP 必不可行。二分整数 mid；成功便运行上述舍入、保存该实际分配并提高 low，失败便降低 high。始终 high>OPT；终止 high=low+1 时整数性给 low≥OPT，因此保存的实际最小值≥low/4≥OPT/4。所有猜测的系数及LP见证可按多项式位长处理，轮数 O(log(U+1))；无需在 OPT 以上假设 success 单调，更不需要额外 λ=1 promotion 或 raw CONFIG(M/2) 定理。这些接口义务已由此直接证明，不登记为新的开放问题。

## 同域二近似只作算法改进语境

`UM-VW2010-THEOREM12-BACKEND-PRECHECK-v1` 的完整成熟正文 §2–5，和其 evidence 的“Theorem 12”节，给同一共同有限非负有理、每物品至多双正端、允许异值、实际完整分配域的确定性总位多项式二近似。forced-largest 的逻辑是：删去当前最大双端物品后，某玩家即使拿其余全部物品仍达不到 T，则该最大物品在任意 T 分配中必归他；强制后从两端全局删除。同物品配对和逐玩家降序相邻配对的并图是交替偶环/路径，二染色使每个 local pair 至少取一件，给 value(B_i)+value(A_i去最大)/2≥T/2。拒绝才证明 OPT<T；成功只给实际 T/2 分配。整数化后二分高端 U+1，拒绝保持 high>OPT，结束保存分配≥OPT/2，无需 success 在 OPT 以上单调。

与旧四近似的差别具有数学意义：旧算法显式求阈值重估 M-LP，用半整数重排、big 树和 small LP-Round；新算法不用那条结构链，通过强制最大物品和双配对直接输出整数分配。因此新结果在共同域将保证从 OPT/4 改进为 OPT/2，可写 `supersedes/context`；它不会推出“那份 M-LP/树算法正确”这一目标整句。纯粹的 OPT/4 实际分配存在性虽为 OPT/2 的直接弱化，但在本包不另造一条会掩盖算法差异的 whole-result 边，也不将已由上文独立原证付清的指定算法义务假写为 open。

该比较不声称 VW 是截至当前日历日期的世界最佳算法；只比较当前总表中已实读的两个结果。没有把平方时间 O(|I|²) 作为本包已经重建的实现收费，也未重跑后端程序或引用未读的 weighted-menu 全定理作为新前提。

## 严格二硬度、降度与其他候选的处置

`M-de7aec4bd7c24b0f9dc342c483c4a75e` v3：同源完整成熟body和 PDF 第 10 页 Theorem 3.1 的构造已读。每变量两名文字玩家共享一件两端值 2 的物品；每 clause 有私有值 1 物品，并对每个文字 occurrence 有一件文字/clause 两端值 1 的共享物品；文字不足两次的部分以私有值 1 填足。每件共享物品至多两个正端且两端值相同。SAT 可满足时真文字拿值 2、假文字拿两件小物品、各 clause 拿私有加一个真 occurrence；反向最小值≥2 时，未拿大件的假文字必须占满其两件 small 物品，各 clause 所拿 occurrence 因而来自真文字。整数值下 NO 最小值≤1。因此 P≠NP 时排除任意固定 c<2，而 c=4 上界和 c=2 上界都完全相容；没有 refutes 关系，也没有硬度→四近似的算法推导。

`M-a9534c70ffa74fca9a91cd270468de3f` v3 只作为已读候选记录和同源 PDF 第 8–9 页 Theorem 2.4 的边界检查：链式 helper 输出总正度≤3，不是≤2。链内部副本可以有原玩家加两个 helper 的三个正端。因此不能把 DegreeTwo 算法接到任意该降度输出，反向得到一般 MaxMin 四近似。此候选未被用作边端点或承重依赖，未要求追加 read-add。

同源body中的 InfDegreeOne/InfDegreeTwo 只限制物品无限价值端数，不能替代总正度≤2；本文不重审它们的配置间隙对象，也不从其正文概要制造与本核心的逻辑边。检索中 VW 一般半整数/给最优类型信息的外引声明只读了当前记录与资源页末节，输出或假设合同不同，且记录明确缺完整算法，未用作本包推导。PCSP 和投影博弈章节虽在同一成熟body中完整读取，其模型与目标无实际证明映射，不按同页或同模型名称造 hub。

## 局部原文澄清与最小处置

1. PDF 第 11 页 SP3 论证中的“at least M different positive”对一般加权值不宜字面使用。可执行最小替换是上述 `Σ_{positive small support} p_ij≥M`，再得新值≥M/2。随后“z_i=1”改为“z_i≥1”。这两处只需数学审读说明，不改变核心 statement、对象身份或共享 PCSP 成熟body。
2. 同页 SP3 “M-LP solution of value M/2”保留 inherited big 标签解释；严谨引用用本稿四个明确不变量，或在文字中同步重标 big 代表值。不将按 M 建的 big 等号误套到新阈值的字面 M-LP 定义。
3. 第 11 页“没有玩家叶”之前先归一 big-only 行并移除可直接满足的质量 1 边；第 12 页“any solution uses exactly one leaf”改读为存在一个只用一片叶、足以满足该树的规范化分配。两者是省略的预处理/措辞澄清，已在本稿补全，不构成算法反例。
4. 第 7 页 Thm2.3 开头 promotion 减 z/截 x 的任意 cap 域适用问题不在本包新造依赖；本核心已用自己的 λ=4 可行性映射和树舍入证明闭合。原 PDF 保持冻结，不修改共享 PCSP 全体对象，也不将原文概括“能力相当”升级为任意 cap 点到 raw CONFIG(M/2) 的无条件边。

## 证据精确引用

- `archives/unrelated-machines/state/文献/PCSP最大最小分配与投影博弈平行重复三篇文献整理--文献.md`，全文 SHA256 `a0d8bb0b5261e46ef6843a1e2c9bb812393f22953129ffba03313e0c16b5fb36`，本次完整读完。
- `archives/unrelated-machines/tools/evidence/retired-literature-pcsp-20261031/maxmin.pdf`，全文 SHA256 `7f7b21ff08b37e8489e9f60527e9aa9458dc5cf4cd6cc6804869665c24d51f7f`，本次实际读取第 6–12 页；第 7、10、11、12 页有额外视觉核对。maxmin.txt 仅作定位，不代替 primary。
- `archives/unrelated-machines/state/审查/VW2010 Theorem12双端价值后端与新桥接口预核--审查.md`，全文 SHA256 `fbbe4ca060d00910f3679c128355a9427adc6e887bdfa0890ad51d2ba023bb81`，本次完整读完。
- `archives/unrelated-machines/state/资源/配置LP在图平衡及不相关机中的间隙--资源.md`，全文 SHA256 `0fcfc44edf52bb6f1d0bf459c9847540342f55c9f4d681588f32670d1c64de26`，本次实际读第 101–145 行，包含“二度MaxMin的组合二近似：Theorem 12”完整节及后续外引边界；没有读或声称复证该资源的全部 makespan 定理。

无 declared follow-up overlap 对，因此不填写任何伪造的 closed_overlaps；上述 peer 比较写入 additional_comparisons。无需要新派任务才能闭合的实际关系义务。
