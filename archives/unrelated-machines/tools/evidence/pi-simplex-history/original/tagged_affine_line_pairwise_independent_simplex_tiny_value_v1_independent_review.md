# PI simplex-coset tagged LINE：独立 Exact-only 全文重构

Reviewer：bicriteria_set_packing_bridge，2026-10-18。只读本次指定 Exact，未读作者 Proof（收到任务时尚未冻结）、作者其它新推导或 root 策略。仅 clone 外 scratch，不修改 repo、Git、Work 或任何旧源。

实际全文读取的唯一作者文件：

`/workspace/scratch/038d9dcc4cac/tagged_affine_line_pairwise_independent_simplex_tiny_value_exact_v1.md`

SHA256 `670bd2deb41f4b5fc9df6ca3f0ed460ca2daaa3a9cca38604561bfff3d7b10d2`。

Claim ID：`UM-TAGGED-AFFINE-LINE-PI-SIMPLEX-TINY-VALUE-v1`。

结论：**PASS，全部精确值及结构/位复杂度合同可独立重构，未发现 fatal。** 下文自足证明 extension field 与 common simplex code、每组所有 pair 的 uniformity、所有 states 与 onehot 权的合法性、任意 partial allocation 上界、任意完整 ordinary 调度下界、共同 part/arity 的真实 fresh padding、CSP exact value 和显式规模。O(R^11 polylog R) 的规模按本 Exact 明定的 sparse finite-options、其它资格默认为 infinity 的表示理解；若额外要求 dense 矩阵则为 O(R^19 polylog R)，仍为该展开输入的多项式。

## 1. 二次域、trace pairing 与 projective representatives

R 是任意 odd prime、R>=3。非平方 ν 非零，X²−ν 在 F_R 上不可约，因此 K=F_R[ω]/(ω²−ν) 是 R² 元域。用 a+bω 的两坐标精确表示。乘法矩阵为 [[a,bν],[b,a]]，其线性迹为 2a，故给定 Tr 正是 extension trace。R odd 保证 2 可逆。

配对 (t,w)↦Tr(tw) 非退化：若 w!=0，可取 t=w^{-1}，得到 Tr(tw)=Tr(1)=2!=0。同理对 t!=0 的线性 functional w↦Tr(tw) 非零。取 t=A+Bω、w=C+Dω 时，配对明确为 2(AC+νBD)。

T={1+cω:c∈F_R}∪{ω} 恰是 K 中所有一维 F_R 子空间的不同代表。非零 A+Bω 若 A!=0，可唯一写成 A(1+(B/A)ω)；若 A=0，则为 Bω。任意两个不同 T 元素不成 F_R^* 倍数，|T|=R+1。

这些论证含 R=3，无隐藏“大素数”条件。R=2 不属于本域；不能把 trace=2a 的构造外推到 R=2。

## 2. Common code 的 dimension、full simplex 与全部 pair uniform

把 ζ=(u,v)∈K² 视为四维 F_R 向量。有限 block a 的 coordinate 是

\[
E_{a,t}(u,v)=\operatorname{Tr}(tu+tav),
\]

其 trace-pairing coefficient vector 为 (t,ta)∈K²；infinity block 的 coefficient vector为 (0,t)。这些都是非零 F_R 线性 forms。

任意两个不同 parts 给出的 forms 不成 F_R 倍数：

- 两个 finite blocks 若 `(t,ta)=λ(s,sb)`，λ∈F_R^*，则 t=λs 使其 projective reps t=s、λ=1，再有 a=b。因此相同只可能是同一 part。
- finite 和 infinity block 的第一分量分别非零和0，不能成比例。
- 两个 infinity parts 若比例，则 t=λs，同样强迫同一个 rep。

配对非退化保证 forms 的比例等价于 coefficient vectors 的比例。因此任意两不同 coordinates 的 F_R-linear map `ζ↦(E_i(ζ),E_j(ζ))` 秩为2。均匀 ζ∈F_R^4 的每个 pair 取值恰有 R² 个原像，故 pair probability精确1/R²；单坐标有R³个原像，概率1/R。

code map 本身单射。a=0 的 t=1、ω 两个 coordinates 给 Tr(u)、Tr(ωu)，可恢复 u；a=∞ 的同两 coordinates可恢复 v。具体若 u=A+Bω，二者为2A、2νB，均可反解。因此 code dimension恰4，|C|=R^4，均匀 indexed ζ 与均匀 codeword 分布相同。

所有一维 F_R coefficient directions 的总数为 `(R^4−1)/(R−1)=R³+R²+R+1=(R²+1)(R+1)=q`。上面 q 个 directions 两两不同，因而列尽它们；此具体表示确为四维 full projective simplex code。

每个 padded group 的完整 q 个 label positions恰对应所有 parts；helper只是自己 block 上减去固定j，其余coordinates仍是同一 E。加固定coset向量不改变single/pair uniformity，也不破坏ζ到完整tuple的单射。因此**每个group、每对不同实际变量**（包括fresh/fresh、primary/fresh、同block primary/primary）均恰为uniform F_R²，每个individual label均uniform F_R。fresh的私权为零不表示它的label固定零；其真实labels仍随ζ变化，这一点保证PI与common C声明成立。

均匀local certificate给每个indexed state权1/R^4，完全显式，无须有全局满足赋值。不同helpers可用不同ζ，不存在免费global一致性承诺。

## 3. 真正的变量、partiteness、degrees 与 fixed intercepts

主group M拥有q个primary变量x_(a,t)，每part一枚。每helper H_(a,j) 在自身block的R+1 parts使用对应primary，在其它每part使用其专属fresh变量d_(a,j;b,t)。fresh names带完整helper和part索引，彼此不同且不与任何primary同名。

所以每group恰有q个不同变量、一part一个、共同part集Π、共同arity q。main relation为C，helper关系为在自身block整体减j的coset b_g+C；完整每组R^4 indexed states全部保留。每个primary只出现在main及本block的R−1 helpers，degree恰R，intercepts为0和所有非零j；每个fresh只出现一次，degree1、intercept0。故同变量不同组固定intercepts确实单射，最大degree R，算法和证明均不修改这些编号。

变量数精确为 `q+H(q−(R+1))`，H=(R²+1)(R−1)，groups G=1+H。fresh padding是实际新变量及其完整状态/line/jobs，不是把helper缺少的parts口头补齐。

## 4. 全部 state 权与 t0 的合法性

每state在每变量有R个不同资源，不同变量tag分离，因此完整state恰qR个不同incidences。D_a的R+1个点在不同primary变量上，彼此不同。

对main ζ=(u,v)：若v!=0，α=−u/v使w_α=u+αv=0；若v=0，α=∞使w_∞=v=0，包括ζ=(0,0)。所以在α block的每t都有E_(α,t)=0，intercept0的完整line在z=1确含(x_(α,t),1,0)。主state给予这R+1个真实点各1/(R+1)，其余qR−(R+1)点零权，恰norm1。没有遗漏v=0或全零state。

固定w∈K。若w=0，全部T元素trace值零，t0定义为首个t=1。若w!=0，t↦Tr(tw)是非零F_R-linear functional，其kernel是一维子空间；T恰有一个代表在kernel中。因此t0存在且唯一（非零w情形），定义的“first”没有歧义。

helper H_(a,j) 任意state ζ 的w=w_a(ζ)满足Tr(t0(w)w)=0。该primary的实际slope是−j，intercept是j，故z=1时y=−j+j=0，所指D_a资源确在该state完整line上。helper在这一真实incidence私权1，其余全部0，恰norm1。其它helper states同样合法；并未只为某些ζ定义权。

还需能使helper onehot选择任意一个D_a点。任取t=A+Bω∈T，令

\[
w_t=\nu B-A\omega.
\]

w_t!=0且Tr(tw_t)=0，所以t0(w_t)=t。若a finite，取ζ=(w_t,0)使w_a=w_t；若a=∞，取ζ=(0,w_t)。这些均是保留在完整K²菜单中的真实states。因此每个helper能将onehot置于D_a的任一t，而不删除其它states。

## 5. 任意 partial allocation 的精确 V

写ρ=2/(R+1)。首先证明覆盖**每个indexed state choice、每组任意资源子集**的上界。若某helper质量为0，则minquality=0<=ρ。否则全部helpers必须各领取自身state的唯一正权点，否则它们质量就是0。对固定block a有R−1个helpers，每个正权点都在仅有R+1资源的D_a中。资源两两不交要求这R−1个helper正点互异。因此每个block至少R−1个D_a点被helpers占用。

任取main所选state，其所有正权位于某D_α，等权1/(R+1)。该block给main最多剩2个正点，故main质量<=ρ，minquality亦<=ρ。选取任意zero资源不增加质量，fresh资源对全体state权也为0，不能逃避此计数。因此V<=ρ，且不把full-set packing当作partial。

给出达到ρ的确定构造。按T显示顺序，取前R−1个不同t，分派给j=1,...,R−1，记t_j。对每个block a的helper H_(a,j)，按§4选一个onehot在t_j的真实state，并只领取该唯一正点。每block的helpers留下T中最后两个点空闲。main取ζ=(0,0)，其α=∞，只领取D_∞中这两个空点。所有领取点按variable tags/各block互异；helpers质量1、main质量ρ。所有其它资源可不领取。故

\[
V=\rho=\frac2{R+1}.
\]

这一分配显式、无需枚举所有state组合或求解未知最优值。R=3时每block两个helpers占四点中的两个，给ρ=1/2，边界完全正常；随odd primes趋于无穷ρ趋于0。

## 6. 完整ordinary UM：上界与任意完整调度下界

实例的所有private、resource、selector及incidence jobs严格按Exact。相同variable资源给所有states共享同一machine，但不同variable tags分离；private只服务自己state的incidences和本group可能放入的一枚selector。zero私时仍保留真实job，resource端时间仍为1。

由§5的attaining allocation：每selector放在该组选中state private；只导出分配到的正权incidences；其余每件incidence留自身private，包括全部未选states、完整fresh-variable行和全部zero jobs。每resource至多一个unitjob；未选private行和1；选中helper private只剩selector1；main selected private负载`1+(R−1)/(R+1)=2−ρ`。因此全部原jobs给actual Cmax<=2−ρ。

反向取任意合法完整调度σ，记峰值C。若C>=2，已经C>=2−ρ。只需考虑C<2。每group selector所在的private机器确定一个真实indexed state，称为该组选中state；不存在假定σ预先按我们的attaining构造选态。

每个selected helper state的唯一私时1正job必须导出，否则它和selector使该private负载至少2。它只能导出到自身D_a onehot资源。C<2使每台resource最多容纳一件unitjob，因此同block的R−1件selected-helper正jobs占用R−1个不同D_a点。任何未选states的额外exports或zero exports只会再占资源，不能增加空闲容量。

selected main state的R+1个正incidences全在其D_α中，最多2个可导出（其它R−1个资源已被本block selected helpers占据）。每个未导出的正job只能留自己的selected main private，故该private负载至少

\[
1+\frac{R+1-2}{R+1}=2-\rho.
\]

得到所有完整σ均C>=2−ρ，与attaining上界一致：

\[
\operatorname{OPT}_{UM}=2-\frac2{R+1}.
\]

此论证没有假定其它未选jobs留private，没有只审某些partial模式，也没有删零jobs。阈值C=2单独已覆盖；C=2−ρ由完整witness达到，等号不被错误排除。selector给OPT>=1亦一致。本族closed-form optimum趋于2不蕴含NP-hard approximation gap。

## 7. Associated CSP 的精确 value

记二维block map `F(w)=(Tr(tw))_(t∈T)`。一个关键代数事实是：其image不含任何非零constant vector。若F(w)=c·1_T，比较t=1与t=1+ω，线性性给Tr(ωw)=0；但t=ω坐标又等于c，故c=0。再由t=1、ω的配对非退化可知w=0。尤其c!=0时不可能。

固定block a。若两个不同j,k的helpers同时被一个globalassignment接受，shared primary tuple必须同时等于F(w_j)−j·1和F(w_k)−k·1。相减给F(w_j−w_k)=(j−k)·1，其中j−k!=0，矛盾。因此每block至多一个helper可满足，总helpers至多B。

如果main也被接受，primary全tuple为某个E(ζ_M)，其block a为F(w_a(ζ_M))。任何helper H_(a,j)被接受将要求F(w_H)−j·1等于该block，因此F(w_H−w_a(ζ_M))=j·1，j非零，矛盾。所以main满足时没有helper满足，满足总数恰1；main不满足时最多B。B=R²+1>1，故总满足数<=B。

该上界可达到。给全部primary variables label −1，给全部fresh variables label0。每block的H_(a,1)正好接受其ζ=(0,0) state：自身block primary labels是0−1，其余fresh labels是0。每helper的fresh variables专属该helper，所以这些赋值相容，全部B个H_(a,1)同时满足。main不满足，因为其任何block若为constant−1都违背上述事实；j!=1的同blockhelper不能同时满足。故exactlyB个constraints被满足，

\[
\operatorname{val}_{CSP}=\frac{B}{1+B(R-1)}.
\]

这里fresh在某个attaining globalassignment中取0；这不表示其local state labels为常数0。CSP的accepting relation确为同一common C的coset，其完整tuple与indexed state一一对应；计算没有用外部globalwitness或把local PI 分布当成joint satisfying assignment。

## 8. 显式计数、构造与总位复杂度

B=R²+1、q=B(R+1)=O(R³)、H=B(R−1)=O(R³)、G=1+H=O(R³)。逐项核对：

\[
\begin{aligned}
N_{var}&=q+H(q-(R+1))=O(R^6),\\
N_{state}&=GR^4=O(R^7),\\
I_{line}&=GR^4qR=O(R^{11}),\\
N_{resource}&=N_{var}R^2=O(R^8),\\
N_{machine}&=N_{state}+N_{resource}=O(R^8),\\
N_{job}&=G+I_{line}=O(R^{11}).
\end{aligned}
\]

每incidence恰两个不同namespace的finite options，含zero私时；全部selectors finite options之和是GR^4。因此finite eligibility entries恰`2I_line+GR^4`。真实processing times仅0、1/(R+1)、1。索引和各field元素/私时的bitlength为O(logR)，因而完整sparse finite-options表示连同全部planes、states、labels、完整line权表、jobs和默认infinity资格为O(R^11 polylogR)。没有把一个implicitstate oracle当显式表。

若把ordinary矩阵额外物化为dense，entries数为N_machine·N_job=O(R^19)，这是更大但仍polynomial expanded-size的输出；O(R^11)数值适用于Exact已经明定的完整sparse finite-option定义。该表示区别不影响精确OPT或det total-bit-poly Claim。

common code表需要R^4q=O(R^7)个field值；所有groups完整label表为GR^4q=O(R^10)；uniform local certificates总GR^4个rational 1/R^4，其位长亦poly。ν可给定并扫描平方验证，或从1,...,R−1扫描寻找非平方：odd field的非零square数量为(R−1)/2（平方的原像恰±r），故必有非平方，O(R²)朴素扫描也在expanded-size多项式内。

用a+bω arithmetic、模R运算及非零inverse即可展开全部E、cosets、lines与权。Tr kernel的t0可以扫描实际T，也可直接用两坐标；即使对每state逐项扫描也是固定次polynomial。每个变量、group、state、resource、job索引位长O(logR)，全部 rational计算均为精确binary运算。attaining allocation和完整schedule由§5–6的明确索引构造生成，再逐项输出全部N_job任务的machine；无未知OPT或sourceYES witness输入。

这是output-sensitive/expanded-input的位多项式保证，不是R仅有O(logR)位时免费写出R^11对象。没有按隐藏reciprocal weight展开指数次对象：weights倒数R+1已被实际T和完整input规模控制，ζ菜单大小固定R^4，全部循环次数由明确展开对象数的固定多项式界定。

## 9. Fresh zero padding 的辅助 unpadded 结论

删去所有fresh变量及其zero-private-time incidences/resource planes，只得到helper arity R+1、main arity q的辅助菜单，不能仍称共同arity q。其helpers保留R^4 indexed states时可能有重复的投影labeltuple；原padded tuple唯一性不应外推到这个辅助版本。

但actual V和OPT不变。删除的全部资源私权为0，且variable tags为fresh专属：partial allocation删去或补空这些点不改变任何组质量。每件被删job在自己的private为0，任何unpadded完整schedule都可将它们全补回自身private而不增加任何负载；反过来删除它们和仅服务这些jobs的fresh资源机器不可能破坏原jobs的剩余调度。完整padded/private states和selectors没有被合并。故这两种辅助操作保留exact V与UM optimum，亦说明padding没有暗藏正质量或漏掉zero任务。

## 10. Scope、先前接口与独立性身份

本族确给全local-pair-uniform、common-coset、q-partite、degree<=R的normalized tagged-LINE菜单，但实际export value为2/(R+1)趋于0，actual UM optimum趋于2。它反驳仅依靠这些local PI分布就能推出常数actual-export的普遍下界。

每helper共同涉及R+1个primary，而非一个；main diffuse、helpers onehot且state-dependent。fresh的完整labels仍承担common code与PI，只有其私权为零。arity q和common code随R变化。可选态和exact values均显式易算，不提供NP-hard promise gap、hard primary image typing或对任意sourceNO的decoder。

也没有与wide rectangle合同相冲突。作为独立额外核对：full projective simplex的任意非零codeword有恰R³个非零coordinates，因为固定非零ζ上为零的coefficient directions是一三维hyperplane的projective directions，数为R²+R+1，而q−(R²+R+1)=R³。故C不含weight1向量。若某coset内Cartesian rectangle有一条side大小>=2，固定其它coordinates取两个vectors相减便会得到C中的weight1向量，矛盾。因此本族rectangle所有side只能singleton，无法从local PI偷偷取得wide-coordinate freedom。此辅助观察不用于上述V/OPT/CSP精确值证明，也不作新hardness主张。

本次未读作者Proof或其它新推导，未运行有限数值扫描或实现认证。root按任务描述已先与作者讨论构造，不能记root为本候选的blind reviewer。本记录是独立Exact-only重构；未来作者Proof read-after或canonical scope review必须另冻，不改本记录及本次读取的Exact原字节。
