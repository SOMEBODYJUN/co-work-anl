# 一背景五尾：原 53 外射线加五个真实 Z 查询的共同重配锥

RUN：six-boss1-20261111；Boss1 子任务 background_reweight。

## 当前结论

本稿完成了原53个合法外乘子及五个 actual 尾位 Z 查询的共同重配，共58个全局非负乘子。GitHub Actions 已返回完整域精确证书，本地一次完整精确重放通过。局部 BG、PC、DEEP 的原源乘子与正确平移后的信用合同保持固定；MAXROOT 原源合同的背景费用也完整保留。

现在普遍有

\[
\boxed{R_Z\le2V+\varepsilon_{\rm new}E_Z,\qquad
\varepsilon_{\rm new}\approx0.045031284569913524<\frac{451}{10000}.}
\]

这是任意合法长度一历史、任意五尾纯SPE及任意五合法比较索引的全称结论；精确分数与全部外权见第七节和 actions_full/exact_upper_certificate.json。相对已证旧收费约0.04977021，费用下降约9.5216%。58锥另有47原子的精确下界约0.04497639859110952，上下界不同，**未宣称精确最优**。

并行的解析工作已经得到65原子的精确方法障碍：原53加五actual查询、MAX:Z及七个隐藏后继SAFE-Z的66行锥，收费都至少约0.0000793164968486。对这个65原子，在尾第一源、θ=1/2、初态(Z,Z)的完整19参数四态价格锥还有严格无分离界 >7/100。不能把这些方法障碍当作SPE反例；云端47原子与该65原子是两个不同测度。

早期本地384个旧极值见证 LP 的最优值曾为 ε=0，但将该新向量交给重新求极值的 oracle 后，仅所审计96个条件态就有44个负态，最小值为

\[
-\frac{1303719631171846354}{1006523287534683699}.
\]

这个早期小试只证明旧极值见证不足以验证重配后的乘子。后来的全锥障碍来自另外的精确对偶，不能从这44个负态反推。旧证书收费为

\[
\varepsilon_0=\frac{62212762317811658581}{1250000000000000000000}<\frac1{20}.
\]

原六人全模型 half 与一般零收费 BG5 继续 OPEN。

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

**本节请求已实际执行完成。** Main 已核推送提交、run43077553308、job130721374378及产物13881608606的输入与下载回执；本代理已逐文件保持字节复制到 actions_full，并完成下述独立/完整复核。命令保留为执行记录，不重复使用相同请求ID。

manifest：research/workspaces/six-boss1-20261111/background_reweight/computations.json。

experiment：six-boss1-background-reweight-58-full。

本次请求 ID：C-six-boss1-background-reweight-58-01。实际入口命令为：

```sh
python work.py compute request six-boss1-background-reweight-58-full --manifest research/workspaces/six-boss1-20261111/background_reweight/computations.json --request-id C-six-boss1-background-reweight-58-01 --timeout-minutes 60
```

该命令由 Main 在实读并冻结依赖后执行；本子任务没有写 request、Git、RUN 或 registry。manifest 声明 ubuntu-latest、固定 numpy/scipy 版本，算法预算3200秒、任务超时3480秒、60分钟作业窗口。全部源码及依赖已由请求绑定，本代理自冻结后没有修改原计算输入。

标准输出目录是 background_reweight/actions_full。重点读取 summary.json、iteration_history.json；如生成，读取 exact_upper_certificate.json 与 exact_upper_audit.json，或 exact_lower_certificate.json 与 exact_lower_audit.json。candidate_exact_upper 文件名本身不表示通过。

重放命令：

```sh
python research/workspaces/six-boss1-20261111/background_reweight/verify.py research/workspaces/six-boss1-20261111/background_reweight/actions_full
```

仅有有限对偶时可以添加 --lower-only。此重放不调用 LP 求解器，但上界复核仍使用同一已审计的完整域 oracle；字面行评估来自另一个逐索引实现，不将它夸称为第二套独立完整分离器。

每轮保存 actions_full/checkpoint.json，并同步到 RESEARCH_CHECKPOINT_DIR/background_reweight_checkpoint.json。后续新请求通过 --resume-from 的明确文件或计算系统的 RESEARCH_RESUME_FROM 恢复；程序实际读取完整已发现类型、迭代历史和下一迭代号。恢复文件也须由新请求绑定 SHA。旧请求 ID 不重复使用，修改旧请求不当作重跑。

## 七、云端完整域新收费及一次本地精确复核

云任务进行了46轮切平面，共耗算法时间约282.93秒。恢复出的上界是

\[
\varepsilon_{\rm new}=
\frac{328842728720307482565580732756366444109149317026355907082844719841487618552513076812153818154743019863525061705}
{7302539375925668608415480169685768567545568649303581418612668777977033735554976260554561247969122398994272212448}.
\]

恢复秩47包含46个正外权及ε。五个新增actual查询中，只有**尾第一位**对Z的安全查询活跃；没有误称它为真实末位查询。原53条的局部合同与MAXROOT费用仍保持既有精确版本。

全域审计同时覆盖b=0/1、十位全部1024掩码及d=0,…,5，计12288个条件态；每一条件态仍在完整792、792、15504直方图族与三套完整菜单四角上组合后求极值。全部客户余项非负，精确最小值0；共同K余项恰为0。该结论直接代入第三节的恒等式，给出开头普遍收费，不依赖有限游戏抽样。

本代理将已下载的 actions_full 逐文件校验SHA并保持字节复制，回执为 actions_full_copy_receipt.json；没有覆盖云端输出。随后仅做一次本地完整精确上界重放，返回同样12288个条件态、最小值0、共同K余项0及完全相同的整数公分母。另存 actions_upper_local_replay.json。上界证书SHA：3df20bd623a3490906e3d1f3511e6503758679860650e3eaf35ff475b8b1aa6a。

因为E_Z≤r_Z，也同时有 R_Z≤2V+εnew r_Z；Z⊆实际尾并集时则仍给零费用 R_Z≤2V。没有把五比较改成OPT6。

## 八、47原子58锥下界及确实失败的新行

云端保存的47原子精确对偶给

\[
\varepsilon_{58}^*\ge
\frac{10716559432928893649596892185860770028136784380485115967798812693359525779907864076530375263890017901426572403513030}
{238270732398018949328712391806061148414014451382227452534439762233332602034163421154910513789882857824559246840269883}
\approx0.04497639859110952.
\]

本代理用不导入oracle/优化器的字面五索引实现独立重算全部58行、独占质量1与唯一共享K，全部通过。结果为 actions_lower_independent_replay.json，证书SHA为 e1ec47c735f7a2501e89aa85856d560c93981687c46cd839b2c0b23e2d49a1a9。

上下界差约0.00005488597880399918，因而目前只得到这个精确夹逼区间；云任务的旧轮精确下界不能被说成最终上界的相等对偶。

进一步对该**47原子**只做一次小型精确新行检查，不重新优化任何价格参数，结果如下：

| 新合法关系 | 47原子上的精确符号与十进制展示 |
|---|---:|
| K−card(Z)≥0 | **负**，−0.14643898168435043 |
| AB第四/第五位隐藏SAFE-Z | 正，0.7146391405 / 0.2194371212 |
| AE第四/第五位隐藏SAFE-Z | 正，0.5993542662 / 0.1209878227 |
| Sbranch第三/第四/第五位隐藏SAFE-Z | 正，0.7405730148 / 0.4925887064 / 0.1442116100 |
| 已冻结尾第一源、半折扣、初态ZZ的有理价格行 | **负**，−0.0026617112286304555 |

最后一行使用在旧65原子上得到的同一固定权：整数比例为(σ,αm,βm,μV,μW,μmean)=(3228,40,5,5,5,425)，分母3708；本次未重做19参数锥优化。以独立路径/环实现重算23个合并可见类型、1472个字面中间位Bellman比较，确认负号。完整有理值与输入绑定保存在 probe_actions47.py / actions47_new_row_audit.json。

因此47原子的58锥下界**不能**自动推广到含MAX:Z或这个重复Z价格行的更大锥，更不能当作真实SPE反例。它准确指出了可以削弱当前58方法障碍的两个已有合法关系。

## 九、不同于47点的65原子方法边界

free58_66_lower_bound.md 及其冻结清单给一般解析拼接：从既有64原子零背景点、一个独占零会员客户型及一份共同容量构成65原子。这个点通过58原行、MAX:Z及七个隐藏后继SAFE-Z，故66射线锥仍有严格正下界约0.00007931649684860619。

repeated_z_price/contract.md 给另一个完整结论：在**这个65原子**上，actual尾第一源、θ=1/2、初态(Z,Z)、静态十题/比较均值/Z的整个19参数锥严格无分离，统一有理下界 >7/100。独立审计按字面三中间位检查2368个Bellman比较、148个占用流方程及全部19坐标。这里不是只检查返回权，也未据此推广到其他初态或来源。

65点对本固定价格行余量正，47点对相同行余量负，没有矛盾；两者的会员质量与容量质量不同。原58输入、65点冻结子目录和19参数单案冻结子目录都保持不变。

## 下一问题

初始义务已得到严格更小的普遍收费和明确的全锥方法障碍。当前58锥不可能零费；单加MAX:Z或固定重复Z价格可切其47点，却仍被另一个65点挡住零费。继续追求零费需提出真正改变后者性质的合同，例如让新末题与旧共同目录互查时保留同客户联合会员和对应来源预算；不能把原19参数内的反复调权或65点的SAFE追加当作新方向。本稿没有启动这种新外层优化。
