# 全局叶流与完整见证重组：独立重构、冻结攻击及真实输出

实际冻结正文 SHA256：`425af66b7eaa6c8317398f1806aceeae869459ffb57ee9b89c2a6fd2d029070f`。

结论：`UM-UNIT-READOUT-FIXED-HEIGHT-APPROX-v1` 和 `UM-UNIT-READOUT-SELECTOR-MIXING-v1` 在各自明确范围内没有尚成立 fatal objection。外审、全球新颖性和独立论文价值未认证，一般主目标及其反面仍 OPEN。以下记录实际发生的审查和运行，不用人数投票升级真值。

## 1. 独立性与实际顺序

1. `pcsp_occurrence` 先只收到 h1 任意密度三半 Claim 和能否推广固定 h 的问题，未读 root 新证明，独立推出共同 b 叶流、floor-root、真实祖先 DP 和比值 `1+2^(-1/h)`。其盲稿 SHA 为 `7fd13b3a43b357f7921a04f47a8c8b889afdc029b24649f5339446106e8b6d96`。随后实际读完整冻结正文，读前后 hash 均为上记值；第一项是真正先陈述重构，第二 mixing 项只标为读后数学攻击。
2. `cover_consistency` 只收到 p 份完整 YES / 指定 selector profile / N≥p 的精确陈述，独立推出 `d*≤pA`、指定轨槽与未指定轨父置，并独立找到每 p 的锐例。盲稿 SHA 为 `0b574dd865868f00f40d2cd77a57c1bc6a09b07106bae8d8221fbd18d54ec492`；先冻结后实际读上述正文，独立复核第一项，未冒称第一项同为其盲推导。
3. `hardness_route` 构造 mixing 候选并实现其规范程序，再读冻结全文核两个 Claim；这是构造者核查，不混记为独立 blind review。root 亲自重构两项证明，逐行亲读两个规范程序和独立 profile 矩阵程序，重新运行并从原边重新累计全部实际负载。

旧双轨/半密度/固定 D 合同已按精确账本去重；本页不重复登记它们，也不把经典流/Hall/ST 和既有叶命中式称为新技术。新内容限于两个完整全局合同及 mixing 的真实锐 profile。

## 2. 任意密度叶流：攻击点与处理

**流必须每变量饱和。** b 是共同整数供给，不是总流除变量数；只有流值 `b|V|` 才可行。每个实际叶 job 容量 1，保留 sign、路径和原 clause。最优 r_* 森林给每变量 r_*^h 枚不同叶，所以 `b≥r_*^h` 的必要方向成立。

**严格祖先门槛。** 多数轨已流叶数至少 m=ceil(b/2)，未标记数至多 N−m。q=floor((N−m)^(1/h)) 保证未标记数严格小于 (q+1)^h；当 r̂=k−q 时命中阈值恰是 (q+1)^h，off-by-one 正确。DP 只能从同一次流的实际标记叶中取子树，删除后外部共同注入仍合法。旧 64-open 障碍只输出 r1/C7/4，没有免费补成 r2。

**OPT 网格与比值。** OPT<2 时所有外部 unit 至多一 job，唯一 incoming 的树正规形使 OPT 精确为 2−r_*/k。f(x)=(1−x^h/2)^(1/h) 满足 f≥c=2^(-1/h)、−f'≤c，比值导数分子至少 1−c+cx>0，最大在 x1，值 1+c。h1 同样成立。固定 H 时系数统一，h 无界时余量趋 0；没有声称比值最优或一般调度突破。

**失败和退化。** b0 用任意 C<2 必产生每变量一条真实根叶路径来排除，故此分支 OPT2 并输出全父置最优；不是任意松弛失败都 sound。空变量先返回 0；k1 是显式深链；二进制大 A 截真实 arity，未用机器负载精确为零。算法中不计算无理近似系数，根比较用整数，复杂度按显式树和输入位长。

## 3. 多见证重组：攻击点与处理

**不是局部可用性。** p 份调度必须是同一 P 的全部任务、同一共同容量下的真实 C≤1。每个 selector 所选轨被迫全树外送，故指定轨每枚叶在至少一份完整见证外送，逐份计数给 d*≤pA。不同边界预载下的局部 YES 不能替代。

**未指定轨不进强 LP。** 另一轨全部任务直接固定父置，内部机负载 1，不占 clause；不能把这些 t0 行硬塞进要求 r−1 下传的旧全轨 given-witness API。只对指定轨建 x0=1 槽，selector 仅指定根正支持。每活动行分数任务数≤整数 L=k−r+1，incoming 只邻首槽；Hall 一次覆盖所有未固定任务，与固定轨合并守住每台机器。

**参数与锐界。** k≥p 取 r=floor(k/p)，递推 x_h≤r/k≤1/p；k<p,N≥p 时 r1、x_h=1/N≤1/p。k≤pr+p−1≤(2p−1)r 给统一余量。p1 直接返回原 YES 模式；k1 非空且 N≥p 强制 p1。N<p 的 k1 两变量交换 clause 例确有指定模式真 OPT2，不能删前提。

独立审查者还用每指定轨恒定下传 t=r/k 重构大 k 分支：根 row=L，非根 row≤L；与正文递推不同但均合法。这个替代推导不是另一个新 Claim。

正文 shared-positive/private-negative 锐族和独立程序的双共享 clause 锐族都给每 p 的精确指定 profile 值 `2−1/(2p−1)`，全局 OPT 均为 1。前者与后者机器数不同，不能混抄。独立较小族 p1..4 的机器/jobs 为 (3,3),(10,14),(21,33),(36,60)，值 1,5/3,9/5,13/7。下界是原根至少两枚外送与原 shared 容量 `2p>2p−1` 的一般计数，未冒称全调度枚举。

**对近二归约的限制。** 只能对 covered Cartesian hull 中的禁止模式给实际低调度；NO 源输出可能没有任何完整 YES，因此不能据此否定所有归约。实际 C≤S 只自动反驳严格高于 S 的 NO 下界，等号合同另核。这些前提已经写在正文，没有剩余越界应用。

## 4. 软件字节、来源与实际运行

| 文件 | 最终 SHA256 | 实际身份 |
| --- | --- | --- |
| `tests/audits/unrelated_machines/unit_readout_leaf_flow.py` | `43dbf6749b993871cfe8363b3da280d82590147a352f95e46c2eb0eb88a3284f` | 独立写整数流、b 二分、整数根和祖先提取；原 P builder/finish/load 核复用旧校准程序 |
| `tests/audits/unrelated_machines/unit_readout_selector_mixing.py` | `ddc7714e3718f39a08da091394c72b3145c8e1b3f0613690ab36c5459be1ce9f` | 指定轨槽新实现；旧 builder/load/Hall 复用，未指定轨明确固定父置 |
| `tests/audits/unrelated_machines/unit_readout_selector_profile_independent.py` | `3c54c73591d723818bfbc35660ee61167190a24b73a0003bb331aff54654aa1a` | 不 import 仓库核，独立构造并读回 nullable 完整原矩阵、全部 σ、所有机器负载 |

规范两程序不是独立于旧物理模型核的全栈实现；旧核 SHA 为 `039ac7dbbfc0858aa9f51086ad8debb2b2f403b282e6a516ada328e2ebf175c4`。生产入口没有 OPT/LP oracle 或森林枚举。

root 实际重跑两个规范 audit，退出码 0。叶流仅 7 个关键构造：h1 真 OPT1 例输出 3/2 且另验 C1；b0 真 OPT2；A0；64-open 祖先负控；unary 深80；5001 位十进制容量；空变量早于巨大二进制高度。重组仅 7 个关键构造（含 empty），6 个非法输入拒绝，包含 p2/p3 锐族、全局无密度的永不选死轨、k<p、p1 原大编号 unit 重命名和 unary。均没有全调度枚举。

root 另不 import 规范构造，从序列化原资格逐任务重算 26 份完整调度（含 13 份给定 YES）、1359 项实际 job 归属、603 条机器负载记录，并从原网络重建 5 个最大 b 的割证书。独立锐族另亲跑并回算 3002 原矩阵项、1166 有限边、480 job 归属、300 个全机器负载；符号下界不由这些有限运行承担。

两个 `--input` CLI 均实际输出并重算：叶流 5 jobs、C3/2；重组 14 jobs、C5/3。外围 JSON 重读曾因 Python 默认 4300 位十进制上限失败，随后显式解除上限才重读通过；规范 CLI 和旧核从起始就解除，未改数学前提或冻结源码来掩盖外围读取错误。

冻结输出：[有限运行](../../../evidence/runs/unrelated_machines/unit_readout_global_leaf_flow_and_selector_mixing_audit.json)；[独立完整锐矩阵/σ](../../../examples/unrelated_machines/unit_readout_selector_mixing_sharp_profiles.json)。旧冻结证据不覆盖、不修改。复现时运行上述三个程序到新输出路径，JSON 读取端同样需允许大整数文本。

## 5. 最终层级

证明完成：上述限定两合同；内部审查：先陈述重构与实际冻结全文攻击；实现：两个无通用 LP 的实际构造和独立锐证书；外审：未记录；新颖性与论文价值：未认证。固定高度、给定完整 YES 和私有同成本树均承重。没有一般统一 ε，没有近二 NP-hardness，没有关闭 UM-TARGET-v1 的任何正反面结论。
