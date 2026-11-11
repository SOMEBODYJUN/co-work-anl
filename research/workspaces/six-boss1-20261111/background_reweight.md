# 一背景五尾：原 53 外射线加五个真实 Z 查询的共同重配锥

RUN：six-boss1-20261111；Boss1 子任务 background_reweight。

## 当前交付与不能提前宣称的结论

本稿给出一个可直接由既有 GitHub Actions 执行的完整域切平面程序。它同时重配原 53 个合法外乘子，并允许五尾每一位对合法前置主题 Z 的一个安全查询，共 58 个全局非负乘子。局部 BG、PC、DEEP 的原源乘子与正确平移后的信用合同保持固定；MAXROOT 原源合同的背景费用也完整保留。

**目前尚无新的全域上界或正的精确锥下界。** 本地仅完成约五秒的 384 个旧极值见证 LP、96 条件态的小域算术审计，以及四轮小域切平面接线检查。384 个旧见证上的最优值为 ε=0，但将该新向量交给重新求极值的 oracle 后，仅所审计 96 个条件态就有 44 个负态，最小值为

\[
-\frac{1303719631171846354}{1006523287534683699}.
\]

这只证明旧极值见证不足以验证重配后的乘子，既不反零收费 BG5，也不说明全部 58 射线锥不能做到零收费。原已证收费仍为

\[
\varepsilon_0=\frac{62212762317811658581}{1250000000000000000000}<\frac1{20}.
\]

原六人全模型 half 继续 OPEN。

## 一、对象与固定来源

先运行 research search 查询“背景 五人”“background free 53”“one-prefix-five-profit”，并实读当前 bridge 稿、平移程序、固定 53 利润整表及冻结证书/核验器。最邻近的已登记对象是：

- customer-attraction/five-remaining-background-profit-scope-and-index-interface：一般合法背景五尾半利润仍为候选。
- customer-attraction/one-prefix-player-physical-share-obstruction-and-local-repair：零背景行不能逐字移植。
- customer-attraction/one-prefix-five-profit-exclusive-charge v2：正确平移合同、固定 53 外权的已证独占费用，以及单加末位 Z 查询不能修复该**固定外权**向量。

这些查询没有定位到已登记的“全部 53 外权自由重配、同时处理 b=0/1”的免费证书。本稿没有将未检索到理解为全仓不存在；本次新增工作是具体完整域锥、代码及可复算接口。

输入表 inputs.json 精确锁定十五份既有依赖的 SHA-256。三个最核心数据 pin 为：

| 输入 | SHA-256 |
|---|---|
| half5-exact/certificate.json | 395e056b218d237abe8b85db894f0b1c37d2e14d55c74b1dca723abeceb6a44e |
| half5-exact/verify_certificate.py | 6ff64ab6d1e412227fd70a75f5892e5d768c97529600d194c1147d50c723556f |
| background_five_bridge/shifted_local_tables.json | 8fe319e0bfe86a54e562d3d671cda1a527853de43d94e84ad2ec6c435af2c87d |

完整十五项与本轮源码、manifest、烟雾审计输出的指纹另列于 background_reweight/freeze_manifest.json。输入内容若改变，程序的 check_inputs 会拒绝执行。

## 二、实际数学问题

沿固定合法历史 (Z) 后的五人纯 SPE，实际尾主题为 A,B,C,D,E。单客户有

\[
b=\mathbf1_Z\in\{0,1\},\qquad c=\sum_{Q\in\{A,B,C,D,E\}}\mathbf1_Q,
\qquad d=\sum_{j=1}^5\mathbf1_{T_j}.
\]

比较索引保留重复，所有主题来自同一共同目录；零分子分式定义为零。定义

\[
V=\sum_x\frac{c_x}{b_x+c_x},\quad
R_Z=\sum_x\frac{d_x}{b_x+d_x},\quad
E_Z=\sum_x\mathbf1_{\{b_x=1,c_x=0\}}.
\]

目标是寻找最小非负 ε，使所选证明锥推出

\[
R_Z\le2V+\varepsilon E_Z.
\]

V 始终为后五人的真实总利润，不换成新覆盖；R_Z 始终为五比较的背景利润，不当作 OPT6。b 是客户级变量，同一游戏同时可有 b=0 与 b=1，因此两类客户必须使用**同一个**外乘子向量。

### 2.1 原 53 行的精确范围

原 certificate.json 的全部 53 个名字构成固定列表，均允许外权降至零。局部组件仍使用 shift_local.py 从原源乘子重算出的合同；新优化不改变内部源权，不取每客户独立的 IC 权。

共同容量为 K=max_Q |Q|。尤其保留

\[
46313177u_A-7412362K-10^6R_Z+1983898|Z|\ge0.
\]

该行背景收费的客户系数为 +1983898b；不能删去它或令 MAXROOT 免费提供负 K。lastO 的聚合税始终为内部前缀 p/(b+p+1)，分子不含 b。相同固定源码也承担局部 gamma 向下、收益/容量向上取整至百万分之一的安全合同。

### 2.2 五个新增行合法且预算明确

令 i=1,…,5，p_i 是该客户在实际尾前 i−1 个主题中的负载。实际第 i 位的合法 Z 查询给

\[
S_i^Z=u_i-\sum_x\frac{b_x}{b_x+p_{i,x}+6-i}\ge0.\tag{Z-i}
\]

证明：从同一实际有序历史偏离至 Z 后，当前及未来共 6−i 人，每个 Z 客户的终局分母至多 b+p_i+6−i。实际完整 SPE 的真偏离 IC 先比较同一策略的后继收益，再下界为上式。末位 i=5 的查询是真正精确末位报价；前四行只使用安全下界，不假装后继最优。

所有五行各有一个全局非负外权，不带 K，不另引入隐藏会员位，也不借用其他根的利润。相同 IC 可以作为非负线性组合的源；不存在额外“按客户挑其中一位”的许可。

## 三、完整域 LP 与正确的极大化次序

设 a_j(ω) 为第 j 行客户系数，k_j 为共同 K 系数，令

\[
t(\omega)=2\frac c{b+c}-\frac d{b+d},\quad
e(\omega)=\mathbf1_{\{b=1,c=0\}}.
\]

定义非负全局外权 λ_1,…,λ_58，求解

\[
\begin{aligned}
\min\quad&\varepsilon\\
\text{s.t.}\quad&\sum_j\lambda_j a_j(\omega)-\varepsilon e(\omega)\le t(\omega)
&&\text{每个完整客户类型 }\omega,\\
&\sum_j\lambda_jk_j\le0,\qquad \lambda_j\ge0,\quad\varepsilon\ge0.
\end{aligned}\tag{P}
\]

任意可行解给出恒等式

\[
2V-R_Z+\varepsilon E_Z
=\sum_j\lambda_jS_j-\Bigl(\sum_j\lambda_jk_j\Bigr)K
+\sum_x\left[t(\omega_x)+\varepsilon e(\omega_x)-\sum_j\lambda_ja_j(\omega_x)\right]\ge0.
\]

数值变量仅作正尺度换元 x_j=s_jλ_j：BG、PC、DEEP、MAXROOT 行 s_j=10^6，其余 s_j=1。没有额外上下界，也未缩窄允许的外权。

完整域含 b=0/1、ABCDEUVWXY 十位的全部 1024 掩码、共享比较重数 d=0,…,5，共 12288 个条件态。固定该条件态后：

- AB 与 AE 各有完整 792 个三位五索引直方图；
- Sbranch 有完整 15504 个四位五索引直方图；
- 每族只取该同一个 d 对应的直方图子集；
- 三个菜单各在完整多边形 0≤h≤d、0≤ell−h≤5−d 的四角 (0,0)、(d,d)、(5−d,0)、(5,d) 上求最大。

代码先将**当前全局外权组合成一个该族目标**，再对其全部合法直方图求最大；没有先逐行最大后相加，也没有冻结原 53 外权的旧极值直方图。三族与三个菜单之间的可分性，正是冻结核验器的客户类型松弛结构。这个结构扩大真实可实现类型域，因此上界合法；反过来，松弛原子不自动可实现为 SPE。

## 四、算法与精确认证

初始仅采用两种背景各 192 个已保存的极值见证。每轮：

1. 用 HiGHS 求当前有限约束的共同外权。
2. 在全部 12288 条件态及全部隐藏族域上重新分离。
3. 将违反最严重的至多 2048 个**完整新类型**加入同一个 LP。
4. 数值分离不再产生明显新违反时，按活跃约束以 Fraction 恢复有理候选，再作全部域的整数算术分离。

完整精确分离取所有实际 λ 与 ε 分母的公倍数 D，使用原收益尺度 120；直方图分值、菜单四角和最终余项均为 Python 大整数。只有余项全部非负、共同 K 系数非正、所有外权非负且扫描范围确为完整域，输出才标记 UNIVERSAL-CONE-CERTIFICATE。数值 epsilon=0、有限旧见证通过或小域通过均不会触发该状态。

### 4.1 锥下界也有独立精确合同

有限 LP 的对偶可恢复为非负客户型质量 μ_ω 和非负容量质量 q，要求

\[
\sum_\omega\mu_\omega a_j(\omega)+qk_j\ge0\quad(\text{全部58行}),
\qquad \sum_\omega\mu_\omega e(\omega)\le1.
\]

则该完整锥的任何可行 ε 均满足

\[
\varepsilon\ge-\sum_\omega\mu_\omega t(\omega).
\]

因此，一个正的精确有限对偶即足以排除整个所定义 58 射线锥的零收费证书；这一步不需要把尚未枚举的类型忽略成可行约束，也不需要先得到完整上界。对偶证书的每个类型都重新检查共同 d、直方图总数、菜单可行性及全部 58 行。它只构成明确证明锥的方法下界，绝不构成 BG5 或六人 half 的 SPE 反例。

恢复失败时保存原浮点输出、错误原因与 checkpoint，不把数值最优值当作有理认证结果。

## 五、本地实际检验及边界

local_seed 保存 384 见证 LP 的输入、数值向量和状态。local_smoke.json 保存八个十位掩码、两个背景及六个 d，共 96 个条件态的实际算术结果：

- 原固定向量的 96 个重新极大化余项与既有整表逐项完全相等；
- 原向量与新向量共 11136 次独立字面逐行计算；每一条可变外权行的系数与 oracle 单独单位外权提取的值完全相等，组合值也相等；
- 原 K 列恢复为 −226487/10^21；
- 新的有限 LP 向量在这 96 条件态中有 44 个违反，故没有宣称 ε=0。

local_loop 另外只对相同八掩码运行四次切平面，用于确认加行和检查点接线。其行数从 384 增为 540，仍未有全域新上界。它不是扩大的数学扫描，不与主 Actions 的完整结果混写。

## 六、Main 可执行交接

manifest：research/workspaces/six-boss1-20261111/background_reweight/computations.json。

experiment：six-boss1-background-reweight-58-full。

建议新请求 ID：C-six-boss1-background-reweight-58-01。入口命令为：

```sh
python work.py compute request six-boss1-background-reweight-58-full --manifest research/workspaces/six-boss1-20261111/background_reweight/computations.json --request-id C-six-boss1-background-reweight-58-01 --timeout-minutes 60
```

该命令由 Main 在实读并冻结依赖后执行；本子任务没有写 request、Git、RUN 或 registry。manifest 声明 ubuntu-latest、固定 numpy/scipy 版本，算法预算 3200 秒、任务超时 3480 秒、60 分钟作业窗口。应推送源码、inputs.json、computations.json 及实际生成的请求；所有既有依赖均在 inputs/checkouts 中按精确路径列出。

标准输出目录是 background_reweight/actions_full。重点读取 summary.json、iteration_history.json；如生成，读取 exact_upper_certificate.json 与 exact_upper_audit.json，或 exact_lower_certificate.json 与 exact_lower_audit.json。candidate_exact_upper 文件名本身不表示通过。

重放命令：

```sh
python research/workspaces/six-boss1-20261111/background_reweight/verify.py research/workspaces/six-boss1-20261111/background_reweight/actions_full
```

仅有有限对偶时可以添加 --lower-only。此重放不调用 LP 求解器，但上界复核仍使用同一已审计的完整域 oracle；字面行评估来自另一个逐索引实现，不将它夸称为第二套独立完整分离器。

每轮保存 actions_full/checkpoint.json，并同步到 RESEARCH_CHECKPOINT_DIR/background_reweight_checkpoint.json。后续新请求通过 --resume-from 的明确文件或计算系统的 RESEARCH_RESUME_FROM 恢复；程序实际读取完整已发现类型、迭代历史和下一迭代号。恢复文件也须由新请求绑定 SHA。旧请求 ID 不重复使用，修改旧请求不当作重跑。

## 下一问题

首先等待完整域任务区分：这个 58 射线锥能否给 ε=0；若不能，能否同时给严格小于 ε0 的全域有理上界和正的精确锥下界。只有两端精确值相同，才称该明示锥的精确最佳收费。若数值分离收敛但有理恢复失败，下一步是保存活跃基上的精确恢复，而不是扩大网格或宣称普遍失败。
