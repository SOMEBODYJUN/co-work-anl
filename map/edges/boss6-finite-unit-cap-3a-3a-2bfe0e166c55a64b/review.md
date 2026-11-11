# 全有限单位 helper 反族：由既有 ∞ 像到新有限保证的整结果迁移

本任务为 `boss6-finite-unit-cap-3a-3a-2bfe0e166c55a64b`，owner 为 Boss6。核心 CF 为 M-d1467073db5b4c139d81c9483d98f1c0 v1；共享端 C 为 M-b6605b3864cb41e399d926496739f12d v1，H 为 M-b86375379821448d857231e8c38d8f46 v1。三个当前 registration_pin 分别为 `544e687681b5c59e7470cbb03e31736a1afb7dab9107067e93a4c60e0883b8dc`、`a4473d1389b5162ebfdada8c07211497ebd46ec7034fa7a58c716c57ea695df7`、`bd9217e58da09968a5580a321b9be8c46b109e3f20b184ff2468e4acb1ba3a30`，已以只读 metadata 核对。数学结论是 accepted、unconditional、transfers，保留单一必要来源 ALL{C}，终点为 CF 的完整有限实例保证。H 的有限边界另作已完成比较，不机械加入这条证明的前提。

## 1. 模型、完整实例与迁移映射

固定任意整数 n≥4，令 v=(n−1)/n、a=(2n−1)/n²，则 0<a<1/2<v<1。C 明确给出的 ∞ 像记 K∞。它有 n 位原玩家 i；每位 i 有自己的私有物品 r_i，只有主人值 a。每个共享索引 j∈{1,…,n−1} 有副本 c_{j,1},…,c_{j,n}；原玩家 i 仅在 c_{j,i} 值 v。helper h_{j,k}（1≤k≤n−1）仅在 c_{j,k},c_{j,k+1} 值 ∞，其余未列端全为零。

CF 的有限像记 K1。逐项保持同一 n、玩家身份、链索引 j、owner 索引 i、helper 索引 k；只作物品标签 r_i↦q_i、c_{j,i}↦e_{j,i}，并将每个 helper 的两条 ∞ 估值改为 1。故两个原矩阵的玩家—物品正支撑完全相同，原玩家全部估值完全相同；K1 独立于查询参数，非零值仅 a,v,1。它是新的全有限实例，不能把 CF 当作旧 C 的版本改写。

raw 整数分配的每件物品至多归一人，效用非负加性。raw CONFIG(s) 每行仅用原值达 s 的配置、行质量恰为一、每物品总边际至多一。cap M-LP 固定 λ=1，给每个有限 M>0 用 min(p,M) 分类：p≥M 为 big，p<M 为 small，等于 M 归 big。约束完整保留

\[
\sum_i x_{ij}\le1,\quad \sum_{j\in B_i}x_{ij}+z_i\ge1,\quad
\sum_{j\in S_i}p_{ij}x_{ij}\ge Mz_i,\quad
x_{ij}\le z_i\ (j\in S_i),\quad x,z\ge0.
\]

没有额外的行总 x=1。对 M>0，零端永远 small；先将所有零估值端 x 设零，列容量与逐 small 上界只变松，big 和、小端效用不变，非负性保持。下文转换均先这样清理。

## 2. ALL{C} 迁移为 CF 的全部 cap 正参数

C 已完整证明固定 K∞ 的 cap 正可行集恰 S_n=(0,a]∪(v,1]，尤其不存在 M>1 的可行点。

若 0<M≤1，K1 的 helper1端和 K∞ 的 helper∞端在 cap 后都恰为 big M；所有其余端的值、分类及索引相同。于是经上述标签映射，两者规范化矩阵与全部五类约束逐项相同。这不只保持可行性：这一参数区间里的两个 LP 系统相同。由 C 立即转得该区间内精确可行集 S_n；M=a 包含、M=v 排除、M=1 包含。

若 M>1，假设 K1 有可行证书 (x,z)，先去零。此时 K1 的全部正端均 small，故 helper h 没有任何 big 端，big+z≥1 迫 z_h≥1；其两条单位小端给

\[
x_{h,e_{j,k}}+x_{h,e_{j,k+1}}\ge Mz_h\ge M>1.
\]

把这份证书显式变为 K∞ 的证书：按标签对应保全部 x、保原玩家 z_i，只把每个 helper 改为 z'_h=0。逐类核对如下。

1. 列容量：清零时只下降；此后全部 x 不变，故仍≤1。
2. 原玩家行：其原值、big/small 分类、小端系数、x 和 z_i 全部不变，故 big+z、小端效用、逐 small x≤z 及非负性原样保持。
3. helper 的 big+z：在 K∞ 中两条正端均为 big M，质量和≥M>1，加 z'_h=0 仍≥1。
4. helper 的小端效用：其余端全为零，所以左边为 0，右边 Mz'_h=0。
5. helper 的逐 small 上界：K∞ 中 helper 的 small 端恰为零估值端，已清成 x=0，所以每条为 0≤z'_h=0。两条正端已转为 big，不再受此上界。所有变量非负。

这给出同一 M 的 K∞ 可行证书，与 C 的 M>1 不可行性矛盾。因此 K1 不会额外产生任何高参数可行点。结合低区间相同系统，得到全部有限正 M 上

\[
\{M>0:\mathrm{cap}\text{-}\mathrm M\text{-}\mathrm{LP}(K1,M)\text{ 可行}\}
=(0,a]\cup(v,1].
\]

这里没有使用一般 M-LP 的估值单调性。M>1 时有限与 ∞ 的 helper 分类确实不同；成立的是本构造上的上述特殊证书转换。也不需要 C 中源 I_n 到 ∞ 像的桥在本边再作为独立端点：当前 C 本身已经包含 K∞ 的整条成熟结论。

为直接核对正端点，M=1 取原玩家 z_i=1、private x=1、每个专属副本 x=1/n；helper z_h=0、左右 x=(n−k)/n,k/n。原玩家小端值为 a+(n−1)v/n=1，所有 x≤z；helper big 质量为一；每件副本 helper 合计 1−1/n，加 owner 1/n 恰一。这个见证在 v<M≤1 都有效。0<M≤a 则用私有和每位 helper 的左副本作 big 匹配，全部 z=0。正向可行见证与 C 的完整参数结论一致。

## 3. raw 两种精确值及全部正阈值

这里可只用 C 的成熟 raw 值，加一个独立于 M-LP 的原值配置包含关系。逐端有 p(K1)≤p(K∞)，因此任何 K1 上达有限正 s 的实际分配，在 K∞ 上仍达 s；任何 K1 的 raw 有效配置也在 K∞ 上有效，保持原配置质量和、单物品边际即可得到 K∞ 的 raw CONFIG(s) 证书。故两种 raw 最优值在 K1 上都≤C 的 a。这只是原值分配/配置的单向包含，不是 cap M-LP 单调性。

下界为明确实际分配：q_i 给原玩家 i；每条链将 e_{j,k} 给 h_{j,k}（k=1,…,n−1），剩余 e_{j,n} 任意安置。所用物品互异，原玩家值 a，helper 值 1≥a。故 raw 整数和确定性 CONFIG 在 a 可行，也在全部 0<s≤a 可行。与上界合并，raw OPT=raw ConfigOPT=a，两个正可行集均恰(0,a]。

另直接核过正式正文的独立容量上界，未把原值矩阵的单调包含当作唯一审读：任取 s>a，每个 helper 的达 s 配置至少含一件相邻副本（s>0，其他端全零），每链 helper 归一质量合计至少占 n−1 副本边际；n 个副本总容量≤n，原玩家所获正副本边际至多一。每个原玩家的达 s 配置至少含一份专属副本，因为其余正值只有 private a；n 行至少要 n 副本边际，n−1 链却至多给 n−1，矛盾。论证对 s>1 也有效：helper 可能需两件只会增加消耗；没有把 CONFIG 误当联合整数采样。

## 4. 全部计数、度、位长与完整终点

仅改 helper 值、无增删玩家、物品或正端，故 C 的同一支撑给

\[
N=n+(n-1)^2=n^2-n+1,\quad m=n+n(n-1)=n^2,
\]
\[
E=n+n(n-1)+2(n-1)^2=3n^2-4n+2.
\]

每件私有物品正度一，每链端点副本正度二、内部副本正度三；每位 helper 正度二，原玩家正度 n。K1 两侧原 ∞ 度都为零，所有估值在[0,1]。有限正值 a,v,1 的位长 O(log n)，正端表规模 O(n²)，稠密表示也为 poly(n)，亦为 poly(N)。构造是显式输出，没有 poly(log n) 压缩承诺。

在 M=1，只有 helper1端为 big，故物品 big 度≤2、玩家 big 度≤2；原玩家 big 度零、helper big 度二。低目标 M≤v 时旧 v 端亦可能 big，内部副本可有三个 big 端，不能把 M=1 的二度声明外推到所有 M，也不能把玩家总正度写成三。

由 cap 最高参数恰一及 raw 两值恰 a，两个比均恰 n²/(2n−1)。n²/2≤N≤n² 且 n/2<n²/(2n−1)<n（n≥4），故为本族的 Θ(√N)。n=4 时 v=3/4、a=7/16、N=13、m=16、E=34，值域为{0,7/16,3/4,1}，cap(1) 可行，raw CONFIG(1/2) 因 1/2>a 而不可行，比16/7>2。1 可行而 (a+v)/2 不可行，排除 cap 可行域必为前缀的普遍假设。

这支付 CF v1 的整个 statement 和量词，包括固定有限输出上的全部正 s/M、raw 精确值、规模、各度、最高 cap、分离与 n=4 反例；方向为 C 的成熟 ∞ 像保证，经本文显式值替换与证书映射，得到 CF 的新全有限保证。没有仅得到解码桥再把它冒作完整目标。

## 5. H 精确引用对的完成比较与边界

已实际读取 H 完整 record、正文全篇；承重比较使用其§1五类约束、§2主合同及直接证书公式、完整§4“有限 helper：整数、CONFIG 与 M-LP 的边界不同”。§4 的一般有限 H>0 合同是：M≤λH 时 helper 为 big，hole/prefix 正向仍适用；反向对全部 M>0 成立。M>λH 时 helper 全为 small、z_h≥1，相邻两端和≥Mz_h/H>λ≥1，故每链原 owner 总副本边际≤1，可投影回源。一般正向超过 cutoff 不成立；其一条四副本链的 H=1、cap最高4/3 例明确表明不能直接把 raw s>H 不可行套给 M-LP。

本族是 λ=H=1，C 给 I_n 的全部 cap 可行参数 S_n⊆(0,1]。故用 H§4，可将所有源可行点正向送到 K1；有限 H 全 M 反向又排除额外点。它给同一 cap 集的另一条完整解释。可是§2已由 C 的 K∞ 成熟保证加局部逐约束转换完成全部 cap 迁移，§3/4又付 raw 和结构，不需要 H 的一般有限桥作额外前提。故不发布冗余 ALL{C,H} 边，也不为同一个已解决问题另造3B后续。

两个 task 中指定的 in-packet 对均已闭合：CF—C 是本条整结果迁移；CF—H 是有限正向截止/全 M 反向的适用域比较，得到“本源可行集落在截止内，H 可作替代解释、非本条必要 premise”。不存在待发布的具体缺口或 follow-up。

本反例仅否定无 small 上界前件的 λ=1 cap→raw CONFIG(M/2)，以及 cap 参数必为前缀。M=1 的旧小端最大值 v≥3/4>M/2，未满足安全 small 接口；λ≥2 的重估合同与 λ=4 DegreeTwo 四近似均不受本迁移否定。raw CONFIG 与整数的向下闭性保持。Θ只刻画本族，不推出整个 DegreeThree 类 tight 界、hardness 或全局新颖性。

## 6. 精确证据与阅读边界

- CF 正文全文169行：`archives/unrelated-machines/state/反例/全有限单位helper三度族的capMLP非前缀与根号人数分离--反例.md`，SHA256 `1a7a9b07f378abf3fd3c659ec35297fd774b47c004952773b01896feae133939`。
- CF 独立审查全文37行：`archives/unrelated-machines/state/审查/全有限单位helper三度cap反族独立复核--审查.md`，SHA256 `60532563e85816541e45ebe42681eedf5720ef18df7b0a5a5a4edcd25401a7e9`。
- C 正文全文220行：`archives/unrelated-machines/state/反例/三度二无限度内capMLP非前缀与根号人数分离--反例.md`，SHA256 `b3454530c3cfff2700e16d39114ade01a645526863d5130efcc61e5253c3fece`。
- H 正文分段读完281行：`archives/unrelated-machines/state/定理/无限helper链对阈值规范化MLP的全正阈值双向保持--定理.md`，SHA256 `f07cd5f7128a9e8ac0f4667b8e69f5d89905b8d4e4d999edd090612cb95a9dfb`。本包承重比较限于上述模型、主合同与完整§4；余段记录了实际附带阅读，并未把其所有外部证据或端点纳入本包。
- 三个 registry 对象记录完整读取；`research/registry.json`仅选取这三个对象，未声称全文审读总表。只读 `research show` 确认三 pin 与 binding_status=current。
- 已读根 AGENTS.md、worker 提示词、IMPLEMENTATION.md 和实际 claimed task；旧 `joint-to-cap-family.json`仅作边字段格式参考，不复用其外部 evidence 或把旧边列为本条来源。

未读取或重导出原 PDF，未读取 C/H 所列其他外部证据正文，未运行求解器、枚举、旧科学程序或历史证书。正文中的“原作者已读 PDF”等是被审读材料的来源说明，不代表本 worker 重做。此稿仅写指定 staging 的任务 write_paths 镜像；无 clone/Git/queue/native-binding 写入。
