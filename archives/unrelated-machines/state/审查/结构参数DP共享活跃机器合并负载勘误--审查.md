# Dual / incidence 合并式遗漏父活跃负载：独立勘误审计

## 源版本、实际阅读与适用范围

审计对象为 Jansen–Maack–Solis-Oba, *Structural Parameters for Scheduling with Assignment Restrictions*, `arXiv:1701.07242v1`，仓库 PDF：

`archives/unrelated-machines/tools/evidence/registration-Boss5-0111-literature/structural-parameters.pdf`

SHA256：`4b47eaccfcffe81f6713522269b6afa2124bec3d619d6ef3a1b5341db7e48bae`，19 页，550316 bytes。worker 在本轮导出并连续实读页 1–11，亲自渲染及视觉核对页 4、5、7、9、10、11；本审计直接使用页 4、9、10、11 的定义、公式和证明，不声称重审页 12–19。Root 另独立阅读页 9–11 并视觉核对页 10，确认下面两个反例和修正。没有运行数值/科学程序。

这是两个 join 公式的目标值遗漏，不是对 Theorem 2 的反例。参数合同、`L^{O(k)} O(nm)` 复杂度、精确最优调度输出和非负整数模型不变。当前中文正文已经纠正的 nearly-inactive machine、incidence 任务拆分及父负载匹配缺漏，均按它们的正确语义使用；本审计是另外一处问题。

## 一、原定义确实包含活跃机器

PDF 页 4：对调度集合 S，`OPT(S)=min_{sigma in S} Cmax(sigma)`；Cmax 是所有机器真实负载的最大值，不是只计 inactive machines 的另一个目标。

PDF 页 9，dual 情况：

`S(t)=S(I[check J_t,check M_t union M_t])`，

`tilde S(t)=S(I[check J_t union tilde J_t,check M_t union M_t])`。

S(t,lambda) 和 tilde S(t,lambda') 只是上述调度中满足袋内活跃机器 M_t 给定负载的子集。因此其 OPT 包含活跃机器负载。

PDF 页 10 Lemma 13 原式为

`OPT(S(t,lambda)) = min_{(lambda_l,lambda_r) in Xi(lambda)} max_s OPT(tilde S(s(t),lambda_s))`。

该页证明还明确写了 `Cmax(sigma*)=max_s Cmax(sigma_s*)`。若同一活跃机器从两个子树接收任务，其父负载是两个部分负载之和，这个等式一般不成立。

PDF 页 11 的 incidence S(t,J,lambda) 同样是完整 Cmax 的调度子类；Lemma 15 的 join 以任务集拆分和左右负载向量合并，却同样只取两个子 OPT 的最大值。它存在同一遗漏，即使已经加上正确的父负载投影相加约束，仍须修正目标项。

## 二、同一明确小矩阵

取两个任务 x,y 和三台机器 a,i,b，全部有限加工时间为正整数：

| 机器 / 任务 | x | y |
| --- | ---: | ---: |
| a | 2 | infinity |
| i | 1 | 1 |
| b | infinity | 2 |

所以 x 仅能到 {a,i}，y 仅能到 {b,i}。dual 图是路径 a–i–b，incidence 图的边是 ax,ix,iy,by。下面两个反例都使用这一完整矩阵，未删除任何原任务或合法端。

## 三、dual Lemma 13 的完整分解及唯一拆分

树分解取如下有根树。空袋根 r0 有唯一孩子空袋 u；u 的孩子为 t={i} 和空叶 e；t 的两个孩子为 l={i,a} 和 r={i,b}；l,r 各有两个空叶。根 r0 在原无根树中是叶，其他内部节点各有两个孩子，全部叶袋为空，与源文的习惯一致。

dual 的两条边分别被 l 和 r 覆盖；i 的出现袋 {l,t,r} 连通，a 只在 l，b 只在 r。因此这是宽 1 的合法分解。

以下使用“在 parent 失活”的正确 nearly-inactive 定义 `tilde M_s=M_s\M_parent(s)`；原 PDF 对该定义的另外一处排版缺漏不作为本反例的前提。

* l：`check M_l=empty`、`M_l={i,a}`、`tilde M_l={a}`，所以 `check J_l=empty,tilde J_l={x}`。tilde S(l) 正是把 x 分配到 {i,a} 的全部调度。
* r：对称得到 `check M_r=empty,M_r={i,b},tilde M_r={b}`，`check J_r=empty,tilde J_r={y}`。tilde S(r) 正是把 y 分配到 {i,b} 的全部调度。
* t：`check M_t={a,b},M_t={i},check J_t={x,y}`。S(t) 是把两个任务分配到三台机器的全部调度。

固定父负载 `lambda(i)=2`。左子负载在 i 上只能是 0 或 1，右子也只能是 0 或 1；Xi 的投影守恒要求它们相加为 2。所以唯一可行拆分强制

`lambda_l(i)=1,lambda_l(a)=0`，`lambda_r(i)=1,lambda_r(b)=0`。

左边只能 x→i，其子 OPT=1；右边只能 y→i，其子 OPT=1。因此印式右端的 min 无法选择其他向量而改变结果，右端就是 1。父负载 2 又强制 x,y 都到 i，所以左端 OPT=2。由此严格反驳该印式。

## 四、incidence Lemma 15 的完整分解及唯一拆分

取同样的根 r0、u、t 和空叶结构，改两个孩子为

`l={i,a,x}`，`r={i,b,y}`；l,r 仍各有两个空叶，父 t={i}。

四条 incidence 边 ax,ix 分别在 l 中被覆盖，iy,by 在 r 中被覆盖；i 的出现袋连通，其他顶点各只在一个非空袋。因此是宽 2 的合法 incidence 分解。

在 l，`check J_l=empty,J_l={x},tilde J_l={x}`，`check M_l=empty,M_l={i,a},tilde M_l={a}`；取活跃而非 nearly-inactive 的附加任务集 `J'_l=empty`。故 tilde S(l,empty) 仍是把 x 分配到 {i,a} 的全部调度。右边对应 y，`J'_r=empty`。

在父 t，`J_t=empty,check J_t={x,y},M_t={i},check M_t={a,b}`，父状态的任务子集 J=empty。任务子集的左右分拆因此唯一为空/空。固定 `lambda(i)=2` 后，即使使用已经补全的 Xi 负载守恒，左右机器负载在 i 各为 1 仍是唯一可行拆分；子完整 Cmax 各为 1，父完整 Cmax 为 2。所以 Lemma 15 原目标右端也为 1 而左端为 2。

## 五、最小正确公式

若保留原文的完整 Cmax / OPT 定义，dual Lemma 13 应改为

`OPT(S(t,lambda)) = min_{(lambda_l,lambda_r) in Xi(lambda)} max({OPT(tilde S(l(t),lambda_l)),OPT(tilde S(r(t),lambda_r))} union {lambda_i:i in M_t})`。

incidence Lemma 15 同理改为

`OPT(S(t,J,lambda)) = min_{(J_l,J_r),(lambda_l,lambda_r)} max({OPT(tilde S(l(t),J_l,lambda_l)),OPT(tilde S(r(t),J_r,lambda_r))} union {lambda_i:i in M_t})`，

其中任务恰一次分拆和投影负载相加等于父 lambda 的约束都照常保留。M_t 为空时该额外最大值按 0 处理。

修正式充分，理由如下。固定一对可以合并的子调度 sigma_l、sigma_r，任务集合不交且全部覆盖父实例。任何已经在父处失活的机器只可能存在于一个子树，否则其出现袋的连通性会迫使它仍在父袋；所以该机器的完整负载已在相应子 Cmax 中。任何父活跃机器 i 的完整父负载恰为 lambda_i，是左右部分负载的投影之和。因此

`Cmax(sigma_l union sigma_r) = max(Cmax(sigma_l),Cmax(sigma_r),max_{i in M_t}lambda_i)`。

一方面，右端覆盖父的全部机器；另一方面，非负性使任一子调度在父活跃机器上的部分负载不超过父 lambda_i，而父失活机器不共享，所以右端没有超过真实父峰值的额外量。双向比较均成立。

对固定接口，lambda_i 是常量。可任取左右各自达到其状态最优值的调度合并，保持任务分拆、资格和负载约束；反向限制任一父最优调度得到可行子状态。因此对上述精确等式再取 min 即得两条修正递推，不需要增加状态维度。

## 六、closed-max 语义的完整等价替代

也可以重新定义表值为：“满足当前接口、所有已忘任务恰一次分配时，已遗忘机器最大负载的最小值”。活跃机器只保存 lambda，不立即计入该表值。introduce-edge 选择任务端并加负载；forget-machine 时以 `max(c,lambda_i)` 关闭；join 时把任务局部计数相加并限制不超过 1，把机器负载逐项相加，已忘机器的 c 取两个子 c 的最大值。空根无活跃机器，得到的 c 就是原 OPT。

在这一完整重定义下，join 只写子 c 的 max 是正确的；但原 PDF 的 OPT 定义并非这一语义，因此不能仅用“作者也许只数 closed machines”来解释印式。当前勘误选择保留原定义并给最小加项；新 primal-to-incidence 算法明确使用 closed-max，并在本任务 review 中逐节点证明其不变量、实际输出和位复杂度。

两个修正只在每个已有状态的 join 目标中加一次父 lambda 的 max，或者采用等价的 closed-max 表值，没有新增负载坐标、没有数值展开、没有改变合法调度集合。故 `L^{O(k)} O(nm)`、OPT/最大每机资格度两个参数支、回溯和后续 FPTAS 结论的复杂度阶保持。Theorem 2 无需改成未证明或被反驳，原 primal Lemma 10–11 的机器组不交证明也不受本共享活跃机器问题影响。

## 七、最小共享正文处理建议

中文正文 Dual 段中显式展示的 Lemma 13 公式，加入父活跃负载 `max_{i in M_t}lambda_i`；紧随其后说明原因是活跃机器可同时收到左右子树负载。Incidence 段说明 Lemma 15 的对应目标也补同项，同时继续保留此前已修正的父负载守恒和任务拆分。原 PDF 的冻结字节保持不变，用本审计定位源式缺漏。

共享正文 SHA 改变后，沿其四个现有 owner 做版本和精确引用刷新；statement、参数、量词和 truth_status 无需因这个已付清的公式修正改动。M247 的 objections 补本轮定义核查、完整反例与充分修正；M232 原 primal 算法合同不变。worker 不自行改共享正文、registry 或队列；本审计交 Root 串行处理。
