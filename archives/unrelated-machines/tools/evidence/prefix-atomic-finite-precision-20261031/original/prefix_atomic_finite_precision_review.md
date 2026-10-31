# 有限精度前缀原子解码的独立重构与冻结全文攻击

对象：`UM-PREFIX-ATOMIC-FINITE-PRECISION-v1`，原精确查询身份不变。
下文保留先只收精确陈述的独立重构，随后记录对最终正文的实际全文攻击。
原始局部文件名是审查产生时的名称；可复现规范入口如下：

| 原局部名称 | 仓库规范路径 |
| --- | --- |
| prefix_oracle_exact_first_audit.py | tests/audits/unrelated_machines/prefix_atomic_finite_precision_independent.py |
| prefix_oracle_gram_read_after_audit.py | tests/audits/unrelated_machines/prefix_atomic_relative_gram_independent.py |

两份独立脚本按原字节收入，root实际重跑；结果保存在 evidence/runs/unrelated_machines/ 下同数学对象的 audit.json。
作者侧脚本由root删去本阶段未采用的条件势/稀坏分布实验，并补空任务/不可用端fixtures后，规范为
`tests/audits/unrelated_machines/prefix_atomic_finite_precision.py`；root实际读码并重跑，
其冻结结果记录代码与正文SHA。三个审计均为有限证据，不充当一般证明或全承诺验证器。

# 守恒前缀 law 的近似查询解码：Exact-first 独立常数审查

审查对象只取 root 发来的 Exact Statement。未读 agent_prefix 稿或作者证明。下文先独立推导，再做 Fraction 核验；没有查问题开放状态或导入外部结果。

## 1. 精确合同与结论

固定 n 个 job 的顺序；第 j 件有 d_j>=1 个显式有限端，N=product_j d_j，空乘积为1。所有完整合法 assignments 是叶，非负前缀 law pi 满足 root=1 及每父的值恰等于全部孩子值之和。给定同一 pi 的 promise oracle：对被查询前缀 v，返回 hat_pi(v)，满足 |hat_pi(v)-pi(v)|<=alpha。无需估计值本身非负或守恒；alpha>=0 为有理数。每层查询全部 d_j 个孩子并选择最大估计，ties 用固定次序。

**审查结论 A。** 输出完整叶 sigma 的真实质量满足

    pi(sigma) >= max(0, [1-2*alpha*(N-1)]/N).

这是对每个固定分支向量 (d_1,...,d_n)、每个 alpha>=0 的精确最坏界。若不加 max，原拟定不等式仍真，但其右端为负时不能称锐。N=1 的值恒为1，包含 n=0 和全部 d_j=1。

## 2. 独立推导与等号构造

某父真实质量为 x，孩子数 d，所选孩子真实质量为 y。其余每个孩子 z 的估计不高于所选，故真实质量至多 y+2alpha。利用真实守恒，

    x <= d*y + 2alpha*(d-1),
    y >= [x-2alpha*(d-1)]/d.

写 D_j=product_{h<=j}d_h，q_j 为所选深 j 前缀真实质量，D_0=q_0=1。逐层乘 D_j 得

    D_j*q_j >= D_(j-1)*q_(j-1) - 2alpha*(D_j-D_(j-1)).

望远镜求和即 D_j*q_j>=1-2alpha*(D_j-1)，j=n 得结论；另用非负性截断。

N>1 且 alpha<=1/[2(N-1)] 时，沿固定 tie 分支设

    q_j=(1+2alpha)/D_j-2alpha.

其余 d_j-1 个兄弟各赋质量 q_j+2alpha=(1+2alpha)/D_j。所有质量非负，总和为 q_(j-1)。被选孩子的估计取 q_j+alpha，兄弟估计也取 q_j+alpha，故它们分别达到 +alpha/-alpha 误差并按固定 tie 分支继续。其他兄弟以下可任意非负守恒展开。由此输出恰等下界。alpha 较大时，沿用 alpha_0=1/[2(N-1)] 的构造，所有误差仍<=alpha，输出恰0。N=1 仅有一个完整叶，质量必为1。

这个 sharp 构造使用确定性 tie 选择；若要求唯一最大值，可以任意接近下界，通常只能称下确界。若算法含随机 tie，则逐次已发生的选中路线仍适用下界，但“某一预先固定路径恰等号”的措辞要另定 adversary 合同。

## 3. 实际负载与有理网格

对同一个 pi 的每个完整叶、每机器 i，额外承诺真实不等式

    (T-L_i(sigma))*pi(sigma) >= -tau,

其中 tau>=0。若解码保证的 b>0，则输出叶逐机 L_i<=T+tau/b。这是除以真实正质量，不把 hat_pi 当分母。

取 Q 为输入全部有限 p_ij 的正整数分母与 T 的正整数分母之积；允许未约分分母，Q 仍可作共同分母。处理时间非负、T>=0。任一合法叶均有 Q*(L_i-T) 为整数。取

    alpha=1/(4N),
    b=(N+1)/(2N^2)>1/(2N),
    tau=1/(4QN),

得到精确

    tau/b=N/[2Q(N+1)]<1/(2Q).

故 Q*(L_i-T)<1/2，与整数性合用给 L_i<=T。即使只保留较松的 <=1/(2Q) 也足够。一般充分条件是 tau/b<1/Q；等号不能免费扩成 <=，因为一个质量为 b、负载违反量恰1/Q 的叶可在 tau=b/Q 时满足其 localizer。

若给的是 dyadic-precision oracle，取 k_pi=ceil(log2(4N)) 即保证 2^(-k_pi)<=alpha；k_loc=ceil(log2(4QN)) 对 tau 同理。它们是精度位数，不是按 1/alpha 或 1/tau 展开的循环。若 oracle 只承诺 poly(input length,k) 查询时间，则整个 decoder 查询数 sum_j d_j、精度与工作位长均为多项式。**给出精度位数不证明存在这样的 oracle。**

## 4. 边界与必要假设

* n=0：N=1，输出空调度，质量1；m>=1 时每负载0。若 T>=0 自然满足。无需构造不存在的 job 子节点。
* N=1：所有选择强制，真实叶质量1；可省全部查询。公式仍给 b=1 与 tau=1/(4Q)。
* T=0：网格证明强制所有机器真实负载为0，不退化成“很小正负载”。
* infinity：只枚举原有限资格，Q 不含 infinity。每 job 至少一条有限边是合法输入合同；若 d_j=0 必须可靠拒绝，不可令 N=0 再除。
* 大分母：log Q 等于输入分母位数之和的量级，因而多项式；log N=sum log d_j<=sum d_j，受显式资格表大小控制。Q、N 的数值可指数大，其二进制位长仍多项式。
* 同一 law：所有前缀答复及全叶 localizer 必须指向同一个非负守恒 pi。每次查询各自能被不同 law 延伸，不能替代此合同。
* 假 localizer：若只检查有误差的数值是否 >=-tau，必须另计检查误差；本结论按 root Exact 的真实全叶不等式 promise。没有枚举并验证指数多个叶。

## 5. 绝对 localizer 的 dilution 与相对误差

取两台机器 a,z，T=0，一枚只能在 a 执行且耗时 d>0 的原任务；另有 k 枚零任务，每枚在 a,z 均为0。所有原任务不可拆分，但零任务有两个实际选择。N=2^k，任一完整调度都有 L_a=d，故没有 T 调度。

令 pi 为 N 个完整叶均匀分布，所有前缀质量由守恒定义，则每叶

    (T-L_a)*pi=-d/N.

所有其他机器 localizer 为0。因此允许绝对容差 tau>=d/N 就能让一个完全无 T 调度的实例满足全部真实全叶不等式。该例没有改变实际过载量，只指数稀释了每叶质量。它不反驳本页 tau=1/(4QN)：若 d 的分母整除 Q，d>=1/Q，故 d/N>=1/(QN)>tau。

若承诺改为

    (T-L_i)*pi >= -Delta*pi,

则任一正质量叶均等价于 L_i<=T+Delta，均匀叶数 N 不出现。上述强制过载例通过当且仅当 d<=Delta，无法靠增加零任务稀释。相对容差本身不自动保证 T：还需 Delta<1/Q 才能用网格。零质量叶没有任何负载信息，解码必须保证输出正质量。

## 6. 审查意见

Exact Statement 的数学主链成立，建议仅把“锐界”非负截断及 oracle/真实 localizer 合同写清。alpha 与 tau 的拟定常数安全，特殊情况和 polynomial-bit 精度均成立。不可从本结果宣称已经生成/验证一个适用于一般 UM 的 oracle，也不可把其承诺本身当可高效检验条件。它是给定 promise oracle 的确定性真实调度解码器。

本地 Fraction 程序 prefix_oracle_exact_first_audit.py 核等号构造、局部极端误差、网格常数与 dilution；实际输出另存同目录。独立推导先于软件与作者稿。未外审、新颖性未认证。


# 有限精度前缀解码的读后攻击与相对 Gram 条件核对

## 1. 实际读取、先后次序与冻结身份

先完成 Exact-only 独立推导、写文件并运行 Fraction 审计，之后才实际读取 canonical 正文。独立文件与哈希如下：

* prefix_oracle_exact_first_review.md：`99017e92ef4bb1cf855844111f98f12b9547d967b40feb0b3bd6278361ca6d00`。
* prefix_oracle_exact_first_audit.py：`19180aa9322c8d05cbb8e04aef8d3d29095d82414303d778b663df23f4f5d77c`。
* prefix_oracle_exact_first_audit.json：`e826c557f836bd38b94333d6893856f179221c1a92589bc31a76835185a84c74`。

实际读到的完整 canonical 为
`co-work-anl-boss3/research/current/unrelated_machines/succinct_prefix_atomic_decoding_bridge.md`，SHA256
`a17bde448cd58ab9b637a6050837153006423cf8097b078621bcb302031ff02b`，与 root 指定一致。
读取了新增有限精度扩展 §1–6 及其前面的原精确定义；另实际读取依赖
`full_degree_moment_localizer_decoding_bridge.md`。

审查限给定 promise oracle、真实全叶不等式和满行秩 Gram 恒等。未审任何不存在的一般生成器或验证器；不把缺少生成器列为本定理缺陷。

## 2. FP1–FP2 的全参数锐性攻击

canonical 已使用 max(0,...)，恰修正独立审查中所需非负截断。其“一个特殊叶质量 u，其他全部叶质量 v”构造，与独立的逐层质量构造完全等价。实际核对：深 k 目标前缀有 N/D_k 个叶，所以其质量为

    u+(N/D_k-1)*v = (1+2a)/D_k-2a.

同父的每个其他孩子有 N/D_k 枚普通叶，质量 (N/D_k)*v，二者之差恰 v-u=2a。目标估计+a，其余估计-a，故按固定 tie 规则精确选择。d_k=1 时没有兄弟，公式仍真；N=1 时唯一叶质量1。超过临界误差预算时沿用临界零叶例，故整个 a>=0 范围确实 sharp。§1 的查询合同只需 a>0；a=0 是精确查询边界例，没有必要调用一个未承诺的有限精度接口。

FP2 分层精度的系数也正确：第 k 层误差成本为 2*a_k*(D_k-D_(k-1))，不是 2*a_k*(d_k-1) 或未加权误差和。它不声称任意近似器必出最坏值。

若 tie 规则含前缀/历史依赖但确定，可先按其全平局行为确定目标路径，再布置特殊叶。只要重复查询同一前缀应属于同一误差保证；本算法只用树中的不同节点，不需通过重复查询削减 adversarial error。

## 3. FP3–FP6 的 grid、dilution 与位复杂度

FP4 是真实正质量除法，未拿近似查询值作分母；条件 2a(N-1)<1 在 N=1 时自动成立。a<=1/(4N)、tau_i<=Delta_i/(2N) 给出的容量界正确，虽然常数有余量。

canonical dilution 例中 A 上两枚强制任务各3/4，T1，所有正端已<=T；新增零任务只在 B、C 各有原资格。因此 N=2^k，每叶 A 负载3/2，localizer -1/(2N)，真实没有 T1 调度。它比独立两机 T0 例额外避开了剪枝异议。两例不是调度 gap hardness，只表明绝对原子残差的质量稀释。

Q 采用全部约分后分母的乘积，确为每个实际负载与 T 的共同分母；不要求它最小。log Q 不超过输入各分母位数总和；log N=sum log d_j 被显式有限资格表控制。可计算 N、Q 的二进制表示而不展开其数值规模。a、tau 的分母位数均多项式。

FP6 实际给 pi>=b=(N+1)/(2N^2)，tau/b<=N/[2Q(N+1)]<1/(2Q)，canonical 只用 <=1/(2Q)<1/Q 已足够。若正过载则至少1/Q，矛盾。n0、N1、T0、零端和 infinity 边均正确处理。对于非法 d_j=0，合法 UM 合同已排除；不得代入 N0。

承诺中“所有完整叶、所有机器”是同一个 pi 的真实不等式。一个只返回近似 localizer 数值的工具，若没有真实残差保证，不能按同一 tau 原样认证；正文未作此偷换。按精度编码位数多项式的运行时间是明示查询器假设，不由数值小自动推出。

## 4. FP7–FP8 的 Gram 满行秩复核及反例

取支撑数 s，函数数 r，F in R^(s*r)，行是原子、列是函数值；w_sigma>0。则

    K_i+Delta_i*M
      = F^T diag((T+Delta_i-L_i(sigma))*w_sigma) F.

若右端各原子系数非负则矩阵 PSD。反向在 rank(F)=s 时，对每原子 sigma 存在系数向量 c_sigma，使 F*c_sigma=e_sigma；将其代入二次型得到

    (T+Delta_i-L_i(sigma))*w_sigma >= 0.

除以正 w 即原子容量界。M 可奇异（例如 r>s），无需误加 M 可逆或 F 方阵条件。故 canonical 的满行秩措辞恰当。

**不可省 rank 的精确反例。** 两个支撑原子，权各1/2，T1，机器 A 的两原子负载分别0、2；只保留常数函数 F=(1,1)^T，rank1<2。则 M=[1]、K_A=[0]，Delta0 下 K_A PSD，但第二原子真实负载2>T。该例可用两件原 job 在 A 各耗1、B各耗0，取“全在A”与“全在B”的各半分布实现，全部有限 p<=T；不是抽象符号负载。换完整原子指示基 F=I_2，K_A=diag(1/2,-1/2) 立即拒绝。

**绝对 I 容差不保函数基。** 对同一例 F=I_2、tau1/2，K_A>=-tau I 成立；改用可逆基变换 G=diag(1,2)，K'_A=G^T*K_A*G=diag(1/2,-2)，同一绝对 tau 失败。相对条件连 M 一起变换，K'+Delta*M'=G^T*(K+Delta*M)*G，恰保等价。只有可逆变换属于这里的函数基变换；丢列、截断或低阶投影不能借此保持原子结论。

以上反例均被正文的 rank / relative 限制明确排除，不构成 standing objection。新增 Fraction Gram 审计验证这些矩阵及多组满行秩、矩形和可逆换基实例；有限检查不取代线性代数证明。

## 5. 原精确桥与全阶矩依赖的核对

原精确桥的 Eval(S) 可查询任意相容部分分配，新扩展只需固定顺序的前缀，不能反过来声称它免费实现全部任意 S 的查询。新证明实际仅使用沿选中路线的子前缀、归一化、非负、守恒以及完整原子 localizer，未额外调用 Gram oracle。

实际依赖正文把 L 定义在次数<=2n+1，并要求 q 次数<=n 的平方正性与 K_i*q^2 局部化。对前缀 m_S：m_S^2=m_S、次数<=2n，故 L(m_S)>=0；one-hot 理想给 L(m_S)=sum_e L(m_S*x_e)。对完整 m_sigma，其次数n，K_i*m_sigma^2 次数<=2n+1，利用 Boolean/one-hot 得

    L(K_i*m_sigma^2)=(T-L_i(sigma))*L(m_sigma).

所以原依赖提供正确的 exact law 与零残差条件，但其显式高阶大小可指数大，也不自动提供有限精度压缩查询器。原全阶文件开头的“次数2n”概述必须按其精确 §1 的 2n+1 及负载 localizer 理解；canonical 已使用正确 2n+1，未发生依赖阶数不足。

## 6. 结论与证据分级

目标 SHA 的有限精度 §1–6 无尚成立的数学 fatal objection。全 alpha sharpness、统一 law、全叶残差、网格恢复与相对 Gram 满行秩条件均闭合。审查通过范围仅此给定承诺的 decoder 及其线性代数边界；不认证一般 oracle 生成/验证、一般 UM 新近似、困难性升级或全球新颖性。

先独立后读后的历史由本页记录的实际 SHA 固定。独立 Fraction 审计已经通过；读后 Gram 与原构造等价检查由 prefix_oracle_gram_read_after_audit.py 及对应 JSON 记录。
