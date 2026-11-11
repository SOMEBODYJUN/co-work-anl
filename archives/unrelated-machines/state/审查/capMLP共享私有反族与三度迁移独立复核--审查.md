# λ=1 cap M-LP 的共享—私有反族：独立核验与当前登记去重

本报告只读 `/workspace/scratch/62622ba39554/co-work-anl-boss6`，不修改该 clone、Git、队列或 `work.py`。所核主任务为 Boss6 已 claimed 的 `boss6-inf-chain-transfer-3b-ea6be0c00b1186cf`。这是独立纸面重构与当前正文去重；未运行旧数学程序、求解器或枚举。

**结论。** 对每个整数 n≥4，题给反族成立。原始整数最优值与原始 CONFIG 最高阈值均精确为 a=(2n−1)/n²；λ=1、逐端 cap 为 min(p,M) 的 (4)–(8) 松弛在正参数上的可行集合精确为 (0,a]∪(v,1]，其中 v=(n−1)/n。故最高可行参数为 1，按“最高可行参数/整数 OPT”定义的比值为 n²/(2n−1)=Θ(n)，n=4 已为 16/7>2。这同时给出该 cap 参数化可行性非前缀，以及无附加小物品界时 `cap-M-LP(I,M) feasible ⇒ raw-CONFIG(I,M/2) feasible` 的显式反例。

**去重结论。** 在下述实际搜索与实读范围内，未发现已经登记、能够精确承载本反族及上述两项边界的独立对象 ID。现有 InfDegree、DegreeThree、CONFIG gap、有限/∞ helper 对象均有不同实例或不同接口；不能以一个普通证明步骤的新 lemma 身份替代本反例。若主任务需要图中独立引用此否定边界，建议由 Boss 按既有登记流程为这个单一反例族安排身份；本报告不自行造 ID。若主任务仅需纠正 M-LP 接口，则可先完整挂入该接口正文，避免机械增点。

## 1. 精确模型与所否定的量词

原输入 I_n 有 n 名玩家，n−1 件共享物品 q_1,…,q_{n−1}，n 件私有物品 r_1,…,r_n。所有物品不可分、每件至多给一位玩家，估值非负加性：

- 每位玩家 i 对每件 q_j 的值均为 v=(n−1)/n。
- 玩家 i 对 r_i 的值为 a=(2n−1)/n²，对 r_k（k≠i）的值为 0。
- 没有其他物品或正端，未分配物品允许留空。

n≥4 时 0<a<1/2<v<1，特别是 a<v。均为有限显式二进制有理数。正边有 n(n−1)+n=n² 条，物品数 2n−1；分子分母的位长均为 O(log n)，因而稠密或稀疏输入编码均为 poly(n)。共享物品的正度为 n、私有物品为 1，原输入的物品侧 InfDegree 为 0；本例没有声称原输入 DegreeThree。

对每个 M>0 单独定义封顶后的端值 \(\widehat p_{ij}=R_M(p_{ij})=\min(p_{ij},M)\)。考虑严格按封顶值分类的 λ=1 系统：

\[
\begin{aligned}
&\sum_i x_{ij}\le1 &&\text{每件物品 j},\\
&\sum_{j:\widehat p_{ij}=M}x_{ij}+z_i\ge1 &&\text{每位玩家 i},\\
&\sum_{j:\widehat p_{ij}<M}\widehat p_{ij}x_{ij}\ge Mz_i &&\text{每位玩家 i},\\
&x_{ij}\le z_i &&\widehat p_{ij}<M,\\
&x_{ij},z_i\ge0.
\end{aligned}
\]

这就是本报告的 `cap-M-LP(I_n,M)`。特别地，等于 M 的端是 big；零估值端在每个 M>0 都是 small。正向构造将全部零端 x 置 0；反向不可行性允许这些零端有任意合法 x，它们仍不产生价值，也不进入 big 和式，故不能逃避下面的容量矛盾。

所否定的是对原估值 I 的 CONFIG 的无条件桥，即对所有有限非负加性 I 与所有 M>0，cap-M-LP(I,M) 可行都推出 raw-CONFIG(I,M/2) 可行。目标仍使用原 p，而非在中途把 [M/2,M) 端提升为 M 后的新估值。报告也否定把本参数 M 的 feasible oracle 直接当成一个前缀判定器的普遍假设。

## 2. 原始整数和 CONFIG 的阈值精确相同

每位玩家得到自己的私有物品即可达到 a，所以整数 OPT≥a。若某整数分配的最小值 s>a，则每位玩家必须得到至少一件共享物品：没有共享物品的玩家，其全部正值只可能来自自己的 r_i，价值至多 a。n 位玩家因而需要 n 件互不相同的共享物品，然而只有 n−1 件。矛盾。故整数 OPT=a，且对所有 s>0，整数 s-可行当且仅当 s≤a。

配置 LP 用全部原始值和达到 s 的有效物品集合，每玩家配置质量和为 1，每物品全体边际容量至多 1。s≤a 时，每位玩家选 singleton {r_i}、质量 1，给出可行点。若 s>a，玩家 i 的每个有效配置都必须含至少一件共享物品，因此对任意候选点 y：

\[
\sum_{j=1}^{n-1}\sum_i\sum_{C\ni q_j} y_{iC}
\;\ge\;\sum_i\sum_C y_{iC}=n.
\]

另一方面逐共享物品容量给同一左端≤n−1。矛盾。这里没有假定各玩家配置能联合采样为整数分配，只使用各玩家的独立配置质量和单物品容量。因此 raw-CONFIG(I_n,s) 可行当且仅当 0<s≤a，ConfigOPT=a。

## 3. cap-M-LP 的全部正参数分类

### 3.1 低区间 0<M≤a：可行

每个自己的私有端与所有共享端封顶后都等于 M，因而为 big。令 x_{i,r_i}=1、z_i=0，其他 x 全部为 0。每件私有物品只被自己的玩家使用；每行 big 和为 1；small 价值行右端为 0；全部 small x≤z 为 0≤0。故 (0,a] 全部可行，含端点 M=a。

### 3.2 中间区间 a<M≤v：不可行

每个共享端封顶为 M，是 big；每个自己的私有端值仍为 a<M，是 small，其他 private 端值为 0。第 (6)、(7) 行对玩家 i 给出

\[
Mz_i\le a x_{i,r_i}\le a z_i.
\]

因 M>a 且 z_i≥0，必有 z_i=0。第 (5) 行遂要求每位玩家的共享 big 边际和至少 1。对 n 行求和，共享总使用≥n；对 n−1 件共享物品用列容量求和又给总使用≤n−1。矛盾。端点 M=v 仍然把共享端归为 big，故 M=v 也不可行；这是开区间 (v,1] 左端不能写闭的原因。

### 3.3 高区间 v<M≤1：可行

所有正端现在都严格小于 M，故均为 small；不存在 big 端。令每位玩家 i 对每件共享物品 q_j 使用 x_{i,q_j}=1/n，对自己的私有物品使用 x_{i,r_i}=1，其他 private 使用 0，并令 z_i=1。

每件共享物品列和为 n·(1/n)=1，每件私有物品列和为 1。所有 x≤1=z，(5) 由 z=1 满足。每行小物品价值精确为

\[
(n-1)v\frac1n+a
=\frac{(n-1)^2}{n^2}+\frac{2n-1}{n^2}
=1\ge Mz_i.
\]

因此 (v,1] 全部可行，M=1 时每行价值刚好等于 1。该点的所有端值都已低于 1，cap 不改变原输入的任何估值。

### 3.4 M>1：不可行

此时同样全部端为 small，所以 (5) 强制每位 z_i≥1。逐行求 (6) 之和得到

\[
\sum_{i,j} p_{ij}x_{ij}\ge M\sum_i z_i\ge Mn>n.
\]

但逐物品容量和非负性给出

\[
\sum_{i,j}p_{ij}x_{ij}
\le \sum_j\max_i p_{ij}
=(n-1)v+na
=\frac{(n-1)^2+2n-1}{n}=n.
\]

矛盾。因此不存在更高的可行 M。

合并四个区间，精确得到

\[
\{M>0:\mathrm{cap\text{-}M\text{-}LP}(I_n,M)\text{ feasible}\}
=(0,a]\cup(v,1].
\]

本报告没有涉及 M=0，因为原系统的大/小分类及 helper 消耗论证的正阈值语义均应单独处理零端点。

## 4. 被否定的两个接口及保留边界

最高 cap-M-LP 可行参数精确为 1，而整数 OPT=a，故比值

\[
\frac{1}{a}=\frac{n^2}{2n-1}=\Theta(n).
\]

n=4 时有 v=3/4、a=7/16，可行集合为 (0,7/16]∪(3/4,1]，比值 16/7>2。在 M=1 处 cap-M-LP 可行，而原 CONFIG(1/2) 不可行，因为 a<1/2。因此不存在对本完整输入类、无额外条件的二倍回原 CONFIG 桥。

若把“可行阈值必构成从 0 开始的前缀”作为直接二分的逻辑依据，本例也已反驳：1 可行，但 (a+v)/2 不可行。这里否定的是前缀单调性这一接口前提；没有声称所有利用断点、分段搜索或其他信息的算法都不可能。

该反例不否定已证明的 ∞ helper M-LP 保持接口：保持同一个松弛不等于把该松弛变成原始 CONFIG，反例的缺口可以被保留下来。它也不把任意 DegreeThree 或 InfDegree gap 结论自动搬到此 cap 家族；若要降度，须实用相应的 M-LP 见证桥，并重新计数新增玩家。

原论文的 revaluation 与小端控制必须显式保留。maxmin.txt 的 Theorem 2.3 证明开头先把值≥M/2 的端重估为 M，之后才使用 p_max≤M/2 的小物品分解。这改变了本例在 M=1 的共享端分类。若先已在 λ≥2 的 revaluation 模型上工作，也要说明其 CONFIG 结论属于哪个估值实例，以及返回原值时付出的 λ 因子；不能把那段证明去掉估值变化后直接读成本报告所否定的 raw-CONFIG(M/2) 合同。本报告没有把 λ=1 cap 反例称作原论文指定 revaluation 适用域的反例。

## 5. 实际登记搜索、实读与接口差异

本次当前 `research/registry.json` 的 SHA-256 为 `8275b367cb9eed28da87cfa8c90ea65434bb75dd330eab951a076ec34630a5bb`。先对全 registry 的 object_id、title、model、statement、scope、assumptions、objections 做 M-LP/naturalLP/自然LP 与 MaxMin 搜索，再检索 cap/nonprefix/非前缀/可行集合不连通以及共享—private 的 MaxMin 组合词；正文另检索 unrelated-machines/state 下的相同术语。MLP/naturalLP metadata 共命中 13 项，UM 相关精确身份如下；其余项属于预算配置、背包或 online CRS 模型，无法当作本 MaxMin 同一对象。非前缀/cap 公式模式未命中独立对象。搜索本身不是数学证明，也不宣称全文仓库或外部文献全球新颖性。

| 已有精确 ID | 实际主正文/模型 | 与本例的接口差异 |
| --- | --- | --- |
| M-90610eea6c6447188c03208eaa549254 | PCSP 三文整理 §2；maxmin.txt §4/Lemma 4.1 | {0,1,∞} 的 H_T、多复制 distinguished-root 家族；M-LP 与 CONFIG 同有 Ω(n^(1/6)) gap。没有 cap λ=1 对 raw-CONFIG 的分离，也没有本共享—私有实例。 |
| M-b126c4b3ff29400589f7f38abdca4d85 | 同主正文；原 maxmin.txt 页 13 脚注 2 | InfDegreeTwo 的 Ω(n^(1/4)) CONFIG/M-LP gap 声明；完整透明构造现由下一条主正文承载。不是本例的阈值集合。 |
| M-7bc9eab74ecd475db7df33c3f4b75e61 | 无限helper全阈值降度与三度二无限度配置间隙--定理.md §8–9 | T 个 H_T block，T−1 外部 B 链，随后只降 w 的度；ConfigOPT=T、OPT=floor√T，N=T³+T。其 CONFIG 本身有 gap，与本例 ConfigOPT=OPT、cap-M-LP 额外失真不同。 |
| M-16209762a32e42e48ec20b76381b5e9d | 同主正文 §1–7 | 同一 ∞ helper 输出全正阈值保持 actual 与 CONFIG，正文明确不声称一般 M-LP 变量原样映射。本反例不重复该保持定理，也不否定它。 |
| M-080d9b22ae87408f9a673a898c7a6dc3 | 规范化平菜单的CONFIG与正支撑LP双向保持--定理.md §4 | finite unit-helper 的 actual/CONFIG 路径双向保持；正向阈值≤1。可复用 helper 技术，不承载 cap-M-LP 非前缀反例。 |
| M-e52574ff126d4b128f222053c97bf596 | PCSP 三文整理 §2 | DegreeTwo、λ=4、实际四近似后端。n≥4 时本共享物品正度 n，且 λ=1 cap 不等同其 revaluation 域。 |
| UM-SPARSE-CONDITIONED-CONFIG-GAP-v1、UM-CONTRACTED-SPARSE-CONFIG-GAP-v1 | 三选稀疏条件配置与资源星转移有限审查--审查.md 全文 | 普通不相关机 makespan；有身份原任务、逐边独立 machine-CONFIG、深树与共享 z、OPT=2−1/k。目标方向、配置含义和实例全部不同。 |

实际全文读取的当前 Markdown 为：

1. `archives/unrelated-machines/state/文献/PCSP最大最小分配与投影博弈平行重复三篇文献整理--文献.md`，SHA `a0d8bb0b5261e46ef6843a1e2c9bb812393f22953129ffba03313e0c16b5fb36`。
2. `archives/unrelated-machines/state/定理/无限helper全阈值降度与三度二无限度配置间隙--定理.md`，SHA `9d56eff7715d695c85f6e45707b899633faef71dd1388c86bea1ac4fc721dbca`。
3. `archives/unrelated-machines/state/定理/规范化平菜单的CONFIG与正支撑LP双向保持--定理.md`，SHA `8bfbaa80b98546b6d1320e9760bb9491165e26a6cef1b6cd35eb86116c822f66`。
4. `archives/unrelated-machines/state/审查/三选稀疏条件配置与资源星转移有限审查--审查.md`，SHA `5dcc341353986d1f9631b932f9f115e05de0433253cf1fe54c34fc634bc31e53`。

另实际读取原文的 `maxmin.txt` §2 从 Definition 2.1 到 Theorem 2.3 的关键证明（印刷页 6–8），以及 §4 前言、Lemma 4.1、InfDegreeTwo 脚注和后续模型定义（印刷页 12–14）。原 PDF 路径为 `archives/unrelated-machines/tools/evidence/retired-literature-pcsp-20261031/maxmin.pdf`，SHA `7f7b21ff08b37e8489e9f60527e9aa9458dc5cf4cd6cc6804869665c24d51f7f`；本次以其现有 text 提取核公式，没有声称新做整篇 PDF 视觉复核。

原文页 6 “natural LP unbounded gap” 只是一般背景；页 7 删除 (7) 称 S-LP 的语句只界定松弛关系。它们没有在上述当前独立对象中给出本 n−1 共享+private 的显式参数、cap 断点或非前缀性质。因此可作背景引用，不能当作已经去重成功的 exactID。

## 6. 交接建议

主 worker 的 M-LP 接口正文应完整保留 §1 的 cap 定义及 §3 的端点分类，尤其 M=v 为不可行、M=a 为可行。`M-LP feasible ⇒ CONFIG(M/2)` 必须指明估值实例与 small≤M/2 前件；不能把源论文中间重估当成原值不变。最高 feasible cap 参数仍可定义并精确为 1，但不能以传统单调可行域直觉直接二分。

本反族的两个否定后果和精确阈值来自同一个输入族，应作为一个可复用边界对象处理。没有必要把行值恒等式、全局总价值 n、单独 n=4 数值或参数集合的每一段另造 ordinary lemma。登记身份由 Boss 决定；本 worker 不写 clone、不领新包、不制造注册 ID。

## 7. 同一反族经 D∞ 后的 DegreeThree∩InfDegreeTwo 版本

这是沿同一已认领任务追加的直接关联核验，不是另领任务或另建议普通引理。令 \(K_n=D_\infty(I_n)\)，其中只对原族 n−1 件共享物品降度；每件共享物品总正度 n>3，n 件私有物品保持不变。这里同时使用两个不同的保持接口：

- 已登记结论 A，即 `M-16209762a32e42e48ec20b76381b5e9d`，保持 raw 整数和 raw CONFIG 的全部有限正阈值。
- 待登记新桥 `M-b86375379821448d857231e8c38d8f46`，保持同一 D∞ 输出在每个有限 M>0、有限 λ≥1 下的规范化 M-LP 可行性；此处只用 λ=1。该 M-LP 保持不属于 A 的既有结论，不能只引 A 而省略新桥。

本次实际读到新桥 staging 稿 `staging-inf-chain-transfer-3b/mlp-interface-complete-proof.md` 的 §2，逐项核了去零、helper z=0、hole/prefix 容量和反向投影；下面为本族把需要的具体构造和证明再付清。此引用仅使用其 §2 的直接桥，不为该稿仍在纠正的不同松弛接口措辞背书。

### 7.1 逐项输入、计数与结构度

对每件共享物品 q_j，建立 n 份副本 c_{j,1},…,c_{j,n}。原玩家 i 只在 c_{j,i} 保留有限值 v；其他原玩家在该副本上取 0。建立 n−1 位新玩家 h_{j,1},…,h_{j,n−1}，其中 h_{j,k} 仅在 c_{j,k}、c_{j,k+1} 上取符号 ∞。不同共享物品使用独立的副本及 helper 身份。原私有物品 r_i 与其值 a 保持不变；未列端为 0。

每件共享物品新增 n−1 位 helper，原族有 n−1 件共享物品，故

\[
S=(n-1)^2,\qquad
N=n+S=n^2-n+1,
\]
\[
m(K_n)=(2n-1)+S=n^2,
\]
\[
E(K_n)=n^2+2S=3n^2-4n+2.
\]

最后一式计全部正端：原 n² 个有限正端按副本重命名后仍是 n² 个，每位新 helper 恰增加两条 ∞ 端。所有新玩家和新物品均已计入；n 仍是原族参数，不能把 gap 的 n 误称为新玩家人数。

| 输出物品 | 旧玩家有限正端 | helper ∞ 端 | 总正度 | ∞ 度 |
| --- | --- | --- | --- | --- |
| 每条链端点 c_{j,1}、c_{j,n} | 1 | 1 | 2 | 1 |
| 内部 c_{j,i}，1<i<n | 1 | 2 | 3 | 2 |
| 私有物品 r_i | 1 | 0 | 1 | 0 |

因此 K_n 的物品侧总正度≤3、∞度≤2。原玩家没有任何 ∞ 端；每位 helper 恰有两条 ∞ 端，所以此具体族的玩家侧∞度也≤2。玩家侧总正度未被压为三，原玩家仍有 n−1 件专属共享副本加一件 private，总正度为 n。原值域精确包含于 {0,a,v,∞}，不是 {0,1,∞} 的原论文简化族。∞按常数长度符号编码，有限值位长 O(log n)，总输入长度仍为 poly(n)，也为 poly(N)。

InfDegreeTwo 在这里首先是原估值矩阵的符号∞度。λ=1 在某些低目标 M 上会把有限旧端封顶为 big，不能把“∞度≤2”未经检查就写成“所有目标规范化后 big 端度≤2”。在本报告用于否定二倍桥的 M=1 处，旧有限值 a、v 都小于 1，故只有 helper ∞ 端是 big，此点甚至满足对应的物品 big 端度≤2。

### 7.2 raw 整数与 CONFIG 精确值仍为 a

由 A 的全正阈值保持及 §2，直接得到

\[
\operatorname{OPT}(K_n)=\operatorname{ConfigOPT}(K_n)=a.
\]

也可对该具体输出直接核完上下界：在每条共享链任意留一份副本为空，其余 n−1 份按路径匹配一一给 n−1 位 helper，使其均得∞；原玩家各取自己的 private，达到 a。因此 raw 整数和 CONFIG 在 a 都可行，后者取上述完整整数分配的每玩家 singleton 或所得 bundle 质量 1 即可。

反向任一正阈值整数分配中，每条链的 n−1 位 helper 各至少取得一件相邻副本，所以每条链至多有一份副本正值服务原玩家。若全部原玩家达到 s>a，每位至少需要一件专属共享副本，n 位原玩家却只能从 n−1 条链取得至多 n−1 份服务，矛盾。

raw CONFIG 的上界不用联合整数实现。每位 helper 的每份有效配置至少含一件相邻副本，所以该链全部 helper 边际占用至少 n−1；n 件副本的容量总和为 n，留给全部原玩家的正值边际至多 1。若目标 s>a，每位原玩家的有效配置必须含专属共享副本，n 位原玩家总共需要至少 n 的这类边际；n−1 条链又只提供至多 n−1。矛盾。因此 raw 整数和 raw CONFIG 对全部正 s 恰在 (0,a] 可行，未出现由 ∞ helper 本身引入的新 raw gap。

### 7.3 精确 cap 可行集合由待登记新桥保持

使用 `M-b86375379821448d857231e8c38d8f46` 的 λ=1 特例，可得每个 M>0 上

\[
\mathrm{cap\text{-}M\text{-}LP}(K_n,M)\text{ feasible}
\iff
\mathrm{cap\text{-}M\text{-}LP}(I_n,M)\text{ feasible}.
\]

此处可以直接展开全部关键步骤。给去零后的原可行点，对固定共享 q_j 记 \(q_i=x_{i,q_j}\)、\(\sum_iq_i\le1\)。选 \(w_i\ge q_i\)、\(\sum_iw_i=1\)，令 \(W_k=\sum_{i\le k}w_i\)。将原 x_{i,q_j} 放在 c_{j,i}，原 z_i 保留；给 helper h_{j,k} 设 z=0，两条 ∞ 大端的 x 分别为 1−W_k 与 W_k。helper 大端质量和为 1、全部 small 坐标为 0；副本 c_{j,i} 的 helper 总使用恰为 1−w_i，加旧使用 q_i 后不超过 1。旧玩家的 finite 端值、分类和 (5)–(7) 完全保留。因此得到 K_n 的同目标可行点。

反向给 K_n 的 cap 可行点，先去零。每位 helper 没有任何正值 small 端，(6) 与 M>0 强制其 z=0；(5) 遂要求它的两条 ∞ 大端边际和至少 1。对一条链的 n 件副本容量求和，扣除 n−1 位 helper 的至少 n−1 使用后，原玩家在自己的副本上的总边际至多 1。把这些坐标投影回旧共享物品，原 private 与原玩家 z 保留，恢复所有原列容量；旧行的分类及 small 系数逐项相同，恢复 (5)–(8)。这正是新桥的直接 M-LP 证明，而不是借 CONFIG 证明更名。

结合 §3 已付清的原族全部四个区间，故新族也有精确集合

\[
\{M>0:\mathrm{cap\text{-}M\text{-}LP}(K_n,M)\text{ feasible}\}
=(0,a]\cup(v,1].
\]

M=1 的显式新点尤其简单：原玩家每个专属共享副本 x=1/n、自己的 private x=1、z=1；每条链取 w_i=1/n，因此 helper h_{j,k} 在左、右端分别取 (n−k)/n、k/n，z=0。每份副本原玩家使用 1/n、helper 合计 1−1/n，容量恰一；旧玩家 small 值和恰一，helper big 质量和恰一，所有 (4)–(8) 成立。

### 7.4 新人数下的间隙、同一对象与超边接口

因为新族最高 cap 可行参数仍为 1、raw OPT 与 raw ConfigOPT 仍为 a，其精确比值仍是

\[
\frac{n^2}{2n-1}.
\]

但新玩家数为 N=n²−n+1，故这是 Θ(√N)，不是 Θ(N)。例如对全部 n≥4，\(n^2/2\le N\le n^2\) 且 \(n/2<n^2/(2n-1)<n\)，已给出所需固定上下常数。原族的线性人数 gap 与新族的根号人数 gap 应分别注明计数基准。

n=4 的新族有 N=13 名玩家、16 件物品、34 条正端；raw OPT=raw ConfigOPT=7/16，cap-M-LP(1) 可行而 raw-CONFIG(1/2) 不可行，比值 16/7。于是同一个 cap 二倍桥失败和参数非前缀边界确实可以置于物品 DegreeThree∩InfDegreeTwo 内，并且该具体族还满足玩家∞度≤2。该结论不声称该类的全局 tight gap、外部新颖性、困难性或近似算法下界。

若整个反族对象同时承载 I_n 与 K_n，则可发布真实联合前提关系

`ALL{M-16209762a32e42e48ec20b76381b5e9d, M-b86375379821448d857231e8c38d8f46} → 整个 cap 反族对象`。

其中 A 负责 raw actual/CONFIG；新桥负责精确 cap feasible 集合；原族的实例、四区间、raw 精确值与二倍桥失败已由本文 §1–4 自足证明。结论中的原参数证据在目标正文内已付清，不能说两个抽象保持定理凭空创造原反例。这里不另拆 helper 计数、Θ(√N) 算术或 M=1 证书为普通 lemma，也不把本反族并入既有 M-7bc… 的 T-block CONFIG gap 对象。
