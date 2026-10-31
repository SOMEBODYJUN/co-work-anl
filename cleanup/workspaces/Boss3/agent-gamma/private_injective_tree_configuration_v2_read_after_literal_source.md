# 私有注入树配置五三界：作者证明读后攻击记录

## 实读文件与来源层级

本稿在独立 Exact-first 稿冻结后才全文读取作者证明。原独立稿不作修改：

- `/workspace/scratch/038d9dcc4cac/private_tree_configuration_floor_v2_statement_first_review_literal.md`，SHA256 `13491bd3332d25c5b49dccc9812b3c5cc61f7e5b4e4ba3be3ef03b55a04d9ff7`。
- 先前 v1 Exact-first 稿 SHA256 `9f60a21914a49efab98beacfedd93494dd98ddbd2478afee7ff8453f20432a4b`。

本次实读全文：

1. `/workspace/scratch/038d9dcc4cac/private_tree_configuration_floor_v2_root_frozen_proof.md`，实际 SHA256 `e524ac4cf8df7310729477dc12f91c14842a90dff58953e66d3952397574a05a`，与发送者给值一致。
2. `/workspace/scratch/038d9dcc4cac/private_injective_tree_fractional_floor/private_injective_tree_fractional_floor_frozen_proof.md`，实际 SHA256 `f4900b3693d6242cd08f218cbc478bb1e40ee6f072fb3205a5619b21fd1f40c5`，与发送者给值一致。

绑定 v2 Exact SHA `ad33f6b2c42c184b943651e61437ece2d1372ee1445443017e62534d83487900`。本次读后审查不倒改为零信息盲审，不覆盖未读外部原论文全文、新颖性或生产代码。

## 结论

未发现 fatal objection。作者 v1/v2 的关键证明与本人的先行独立推导相符；作者 v2 的正部行、显式圆周区间分解和确定性 b-质量递归是本人 Exact-first 未读到的具体写法，已在本次单独核查。A/B/C 及完整原 P 回填均成立，算法范围没有越界。

## 1. 精确小型 CONFIG 行及充分性

对 1≤T<2，s=⌊d(T−1)⌋、a=d−s。incoming 边际 q、每 outgoing job 的 unit 边际 t_e，small 边际 A_e=1−t_e。必要性使用 Fréchet 下界：incoming 与 small 同时出现的概率至少 c_e=(q−t_e)_+；含 incoming 的配置最多 s 枚 small，因此 Σc_e≤sq。

作者的充分性是有效的：

- q>0 时，将各长度 c_e≤q 的区间串接到长度 L=Σc_e≤sq 的线段，再模 q 投到 incoming 概率圆周。每个原区间长度≤q，故对应 small job 不会在同一点重复计；对任一点的覆盖次数至多 ⌈L/q⌉≤s（L=0 时为零）。各 small 在 incoming 部分的概率确为 c_e。
- 非 incoming 区间长 1−q。所需剩余 small 概率 A_e−c_e 非负且≤1−q：t_e<q 时它等于 1−q，t_e≥q 时为 1−t_e≤1−q。各自用初始区间即可，允许重叠，因为无 incoming 时全部 d small 的总负载也仅为 1。
- q=0、q=1 分别省去零长区间；s=0 强迫全部 c_e=0，不发生除零或非法覆盖。

所以每个局部配置合法、每个 small 边际精确，incoming 边际 q 精确。外机在 T<2 的配置只有 empty 或 unit singleton；资源行 Σt_e≤1 正好充分。每内部 job 的父边际 1−t_e 和下端边际 t_e 精确合成 1，selector 在各根的边际和也为 1。不需要各机器配置来自一个整数调度的共同分布。

用辅助 z_e≥0、z_e≥q−t_e、Σz_e≤sq 的线性系统确与正部行等价，规模及整数系数位长按显式原 P 多项式。作者另称“阈值只在 1+j/d 改变”也成立：此模型所有有限处理时间为 1 或 1/d，每台机器的任一配置负载是整数／d；非空 selector 保证下界 1，全父置调度保证上界 2。可在 j=0,…,d 中按单调可行性二分，j=d 对应 T=2 的直接可行情形。这只计算配置阈值，不输出整数 σ。

“至少覆盖”改为“恰覆盖”的步骤也有效：配置族向下封闭，可对每个 excess job 的部分配置权重拆分并删除该 job，逐个使覆盖降到恰 1，不增加任何配置负载或改变其它 job 的覆盖。

## 2. 共同 b 子树流与真实单状态一致性

作者使用由局部行等价得到的

\[
 \sum_e\min(q_v,t_e)\ge a q_v.
\]

对任意 0<b≤q，有逐项不等式 `min(b,t)≥(b/q)min(q,t)`，分别对 t≤b、b<t≤q、t≥q 核对均成立。因此可选有理 b_e≤min(b,t_e) 且 Σb_e=ab；逐项贪心填容量正确，因为总容量至少 ab，且单项容量≤b。

b_e/b 位于 uniform-matroid base polytope `{x∈[0,1]^d:Σx=a}`，可分解为恰 a 个不同 children 的子集分布。根质量 b=y_us，先按根 y 选一个真实 state；每活跃节点按其固定子集分布继续，所有节点有唯一私有 parent，故该递归的无条件活跃质量确为预先给定 b_e。每 child 质量≤t_e=q_child，每 leaf 的实际抽样活跃概率≤原 LP 的 unit 边际。作者称 b_e 可取有理数时，可先在第 1 节可行的有理系数有限 LP 中无损选择一份有理可行点，再递归作有理贪心；无需假定任意初始配置分布本来有理。

这种递归只构造每 root 的局部树分布；它没有声称原机器 LP 具有全局整数调度耦合。不同 root 的资源冲突仍留给 Haxell。每 root 从头到尾选的是同一真实 state，而不是不同路径自由改标签。菜单可能指数大，但仅为存在性辅助 states。

## 3. blocker 与 Haxell

作者 v1 的完整 d 树 blocker 归纳与作者 v2 的 a 树 blocker 归纳均正确，精确数分别为 `(d−r+1)^h`、`(a−r+1)^h`。高度零作为归纳辅助、h=1 原始叶层和 r=1 均正确。状态内完整 leafmap 注入保证同一辅助 a-tree 的叶资源互异，所以 blocker 个数可从叶数转换为实际资源数。

v2 仅以正权 a-tree 作辅助状态，并对每棵树的全部 r 子树建超边，足够：任何 hitting set 都要命中每个正权辅助树内的全部 r 子树；按同一每 root 概率分布加权，得到 τ(H_I)≥B_h|I|。不需要加入零权或从未生成的 a-tree。本人先行稿曾用包含更多原状态 r 子树的超图；两种构造各自都给相同存在结论。

超边包含一个 root tag 及 R=r^h 个不同资源，总均匀度 R+1。独立亲核的 Annamalai arXiv:1509.07007v2 Theorem 1.1 使用该总均匀度，所以所需常数确为 `2(R+1)−3=2R−1`。B_h≥2R−1 使每非空 I 的严格差至少 2R−1>0；空 I 的右侧负数，条件自动。R=1 时为普通 Hall。重复边去重并保留 witness 不改变匹配或 blocker。

本审查以自己已亲读的 Annamalai 原研究论文中的明确 Haxell 复述为依据；没有冒称亲读作者另列的 AFS2008 Theorem 2 或 Haxell1995 原全文。作者写出的“至多 rank”版本在本次应用只用到恰好 R 个资源，因此本人已核的均匀版本完全够用。

## 4. 所有原 jobs 的实际回填

作者 v1/v2 都将 selector 放在匹配选出的原状态根；选中真实 r-subtree 的 jobs 下送，其余 jobs 全父置。逐类负载无遗漏：

- 活跃根有且只有 selector unit；活跃非根有且只有其父 job unit；两者均另留 d−r 个 small jobs，负载 2−r/d。
- 非活跃内部节点、同一 state 的未选 d-branches、其它所有未选／零权 states，无 incoming unit，其全部 d small jobs 父置，负载 1。
- 每外机最多一个匹配叶 unit。

辅助 a-tree 不是新增物理机器或任务；作者明确回填原完整 d 树，故没有通过删去辅助树之外的 jobs 人为降低负载。不同状态内部机器完全私有在这一步实质使用。

默认 r=⌈a/3⌉ 的 blocker 数值条件及比值链正确。作者采用 x=a/d，把实际界写为 `2−x/3≤(5/3)(2−x)`，该不等式等价于 x≤1；T≥2 的直接调度覆盖剩余阈值。d=1,a=1,r=1,h=1、零 λ、T 恰为阈值均不产生例外。

## 5. C 的过滤及判定器 scope

严格 actual C≤1 时 selector 强迫选中状态的全部正 small ports 逐层下送，最终全叶 unit 外置，所以所选 state 的完整 leafmap 必单射，且所有 root 的选中全叶像互不冲突。过滤后共同 λ 至少有该 0/1 证书，故空菜单或 LP 不可行确实排除原 OPT≤1。

过滤后的共同 λ 可行时，对保留部分应用五三存在性；被过滤 states 的所有原 jobs 全父置，内部负载 1，没有 selector 放入，且不使用外机，因而可无冲突地回填原完整 P。原 selector 使用保留资格仍合法。

可行返回 YES 保证原 OPT≤5/3，不可行返回 NO 保证原 OPT>1；这正好给严格 (1,5/3) 承诺判定，不能把任意 NO 回答改写为 OPT>5/3。检测注入性及解共同 λ 的 0/1 矩阵有理 LP 均按显式 P 位多项式。σ 的存在通过 Haxell 得到，判定器不输出它；没有把这一步称为一般 approximation algorithm。

v2 也明确没有推出非注入原 P 的 CONFIG gap≤5/3。只有过滤后 LP 可行才获得原完整实例的调度存在性。非注入近二配置族因此不在 B 的否定范围内。

Status：v1/v2 作者全文读后攻击完成；实际 SHA 均匹配；无 fatal；旧独立 Exact-first 稿保持原字节；无新增软件实现、有限实验、新颖性或一般 UM 结论认证。
