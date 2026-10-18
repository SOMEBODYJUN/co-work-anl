# 七态 affine Boolean / Gram-owner 分类：Exact-first 独立重构记录

身份与范围：本轮实际只读获释 Exact `/workspace/scratch/038d9dcc4cac/sol_seven_state_affine_boolean_owner_boundary_exact_v1.md`，SHA256 `a38dfcf05158f38d93f1a26c54591944b8a662174018ece9f81388d499bef250`；实读 header、§1–7 全部 94 行 / 5752 bytes，工具完整返回 1462 tokens、无截断。未读 identity 此候选作者 Proof、策略稿或有关新分类的其它记录。此前已读 global 七态 learning §1–7，故此处只对新函数分类 / 共同 M3 Gram-extension / owner scope 作 Exact-first，不冒七态零背景 blind。

结论：PASS，按下述独立证明未见 fatal。只核此 Exact 的数学合同，不作新颖性、一般 UM 难度、算法或软件认证。没有写 repo、Git、Work 或外部服务。

## A. 先核原支持与退化端点

由 d,s 正偶且 2≤s≤d/2，得 d≥4，h=s/2 为整数，1≤h≤d/4；特别 h≤d−1。p=(s/d)^3/1000>0，u0=4p(1−eta)>0；eta≤1/2 给 p≤1/8000，e=4/5−p−u0>0。因此 Ω0={0,1}×({0^d,1^d}∪h-slice) 的每点确有正质量，且七态中其它点不影响以下分类。h=1 与 d=4,s=2 将单独覆盖；不使用 h≥2 的未述前提。

## B. 独立函数分类证明

令 f=a+bC+Σc_iY_i，在 Ω0 上 Boolean。

(1) 在 Y=0、C=0/1 处，a,a+b∈{0,1}，故 b∈{−1,0,1}。若 b=1，则每个允许 Y 上 f(0,Y),f(1,Y) 相差 1 且均 Boolean，所以恒为 0,1。由 h-subset sums 恒定，交换两个坐标得各 c_i 相等，再用 h>0 得 c_i=0；a=0，f=C。b=−1 同理 f=1−C。

(2) 余下 b=0。用 1−f 可把 a=1 化归 a=0，故只需证明 a=0 时 f∈{0,Y_i}。记 D=Σc_i，由 Y=1^d 得 D∈{0,1}。

若 h=1，则每 c_i∈{0,1}；总和 D 为 0 或 1，直接给所需清单。现设 h≥2。

给任意 i≠j，能选不含 i,j 的 (h−1)-subset T（d−2≥h−1）。两个 h-subset 的 Boolean 值之差给 c_i−c_j∈{−1,0,1}。所以要么各系数同值 t，要么恰有两个水平 t,t+1。

同值情形：ht,dt∈{0,1}，且 d/h≥4。ht=1 会迫 dt=d/h≥4，矛盾；故 t=0。

双水平情形：设高水平个数为 r，1≤r≤d−1。一个 h-subset 中的高水平数 k 逐一覆盖整数区间

 [max(0,h−d+r), min(h,r)]。

其 f 值为 ht+k。因所有这些值只取 0,1，该区间长度至多 1。若 2≤r≤d−2，则 h,d−h,r,d−r 均至少 2，区间长度至少 2，矛盾。因此 r=1 或 d−1。

r=1 时 k=0,1，故 ht=0，t=0，恰有一个系数 1，其余 0。

r=d−1 时 k=h−1,h，故 ht+h−1=0，即 t=−1+1/h；总和 D=dt+(d−1)=d/h−1≥3，与 D∈{0,1} 矛盾。

因此 a=0 只给 0 或 Y_i；取补后 a=1 给 1 或 1−Y_i。合并 (1) 正是 Exact §2 清单。证明不靠系数符号、整数性或有理性，也不靠附加 d/2-slice。

## C. 共同 M3 的 Gram-null 提升

固定 e，简写 X=X_e，f=f_e，D=X−f。D 次数≤1 且 Lhat(D²)=0。共同 M3 PSD 表明 D 是该 Gram 空间的 null vector，因此

 Lhat(D r)=0，任意次数≤3 的多项式 r。

特别令 B=X+f−1（次数≤1），取 r=D B²（次数≤3），得

 Lhat[(DB)²]=Lhat[D·(DB²)]=0。                                  (C1)

另一方面完整原端点 Boolean 矩等式给 Q=X²−X 的二范数为零：

 Lhat(Q²)=Lhat(X^4−2X^3+X²)=0。                                (C2)

这里仅用到总次数 4 的 Boolean 支付，已由 Exact 更强的总次数≤6 假设覆盖。

恒等式

 f²−f = Q−DB

两边均次数≤2。在 M3 Gram 中 Q 与 DB 都为 null，故 f²−f 也为 null：

 Lhat[(f²−f)²]=0。                                             (C3)

此多项式仅含 C,Y 且次数≤4，所以由基础矩匹配等于 E_P[(f²−f)²]。真实 P 每支持点权重为正，非负平方期望零迫 f 在全部正支持上 Boolean。B 节分类遂适用。

这不是只靠一阶相等；也没有将线性 Gram-null 自动乘任意高次数。唯一关键乘法 C1 的测试多项式次数恰≤3，因此共同 M3 足够，未暗加 M4 或真实联合 assignment law。

首、pair 的转移更低阶：D_e 与常数、X_e'、f_e' 的 Gram inner product 均为零，故

 Lhat X_e=E_P f_e，
 Lhat(X_eX_e')−Lhat(f_ef_e')
   =Lhat[(X_e−f_e)X_e']+Lhat[f_e(X_e'−f_e')]=0。

基础二次矩再给 Lhat(X_eX_e')=E_P[f_ef_e']。允许两个端点相同或与基础变量重合，不影响这些等式。

## D. 物理同行 owner 的分类

清单中的非零函数在 P 下均有正一阶。两个非零 functions 的 product 期望为零，当且仅当它们为同一 bit 的互补 literals。检查如下：

* 常数 1 与任意非零函数都有正 product；相同 literal 也有正 product。
* Y_i,Y_j 可同取 1 于 Y=1^d；它们的补可同取 1 于 Y=0^d。
* i≠j 时，h-slice 中存在含 i 不含 j 的点，故 Y_i 与 1−Y_j product 有正质量。
* C 或 1−C 可与任意指定 Y-literal 同取 1，因为 Ω0 在 C 上完整笛卡尔积。

同行不同 job 的 unit endpoints pair 零，由 C 节化为上述非负 Boolean product 期望零。因此一旦有两个正 owners，必为 t,1−t；第三个非零函数不能同时与它们不相交。若某 owner 常数 1，则其它全部 0。总正 owner 数≤2。

CONFIG(B<2) 每个合法配置至多容一枚 unit job，所以 matching row first/pair 确强制不同 unit-job pair 为零。即使该行还含其它 tiny/zero jobs，也不改变这个必要条件。这里只计 A_w；未纳入仿射 Gram 合同的 endpoints 完全未被限制。零一阶端点多、原资格度大均非矛盾。

## E. 背景与高物理入度例子

Exact §5 的前提不可省：条件点必须另外满足自己的 full Ω0 支持与共同矩/Gram/pair 条件；不能从未条件化 M3 自动免费条件化。对真实 law 的逐背景 affine Boolean endpoints，B/D 节则是逐点真实函数论证。

§6 例子逐项成立。固定 β，只有 J_β 在 w 的端点为 C；其它 w 端点为 0。每枚 J_alpha 的两个端点逐样本和为 1；w load 为 C≤1，各私有 u_alpha load≤1。跨均匀独立 β 后，每个 w 端点 first 为 E_P C/N=(1/10+p)/N>0；不同 jobs 的 w-pair 始终为零。N=1 亦成立。所有新增 jobs 都实际执行；没有 near-two NO。这个例子确否定把逐背景 owner≤2 扩为无条件原物理入度≤2。

## F. 最终边界

未见需要改 Exact 的 fatal 或漏边界。该结论是‘full Ω0 + 固定背景 + 同一个 M3 Gram-affine endpoint 合同 + 同行 pair 零’的条件分类；允许跨背景换 identity，允许互补两个 owners，且不免费给一般新接线 full global localizers。它既不证明所有 high-indegree gluing 不可行，也不构造 finder、调度或 hardness。此前七态作者背景在开头已披露；仅新分类与 Gram-extension 在作者 Proof 未读时完成上述独立重构。
