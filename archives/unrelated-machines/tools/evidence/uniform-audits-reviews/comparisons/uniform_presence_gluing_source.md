# 两个可读单位占用输出的两见证胶合锐界：冻结完整证明与四机锐族

对应候选 ID/version：UM-TWO-MEASUREMENT-UNIT-PRESENCE-SHARP-GLUING-v1。

精确陈述冻结文件 `two_measurement_unit_presence_sharp_gluing_exact_statement.md` 的 SHA256 为 `11e3e135889424280fef773bded2cfa8b9dd4c0fb53ee14a3be41c87016e1463`。本文件与 normal-form 消去审查完全分离，不使用该定理。

## 1. 对象和真实 unit matching

给定合法显式 {1,1/k} 实例，k≥2，以及实际完整 σ0、σ1，负载均≤T=1+1/k<2。给定两台不同机器 v,w，二者在σ0中unit-vacant，在σ1中unit-present。

每个见证中，实际运行时间为1的任务到机器形成一个 matching N_s：每件任务至多去一个机器，而每台机器不能接两枚 unit 任务，因为T<2。matching 的二部图一侧是原任务，另一侧是原机器；某件任务可在一份matching中出现、另一份不出现，这正是原 small↔unit 切换，未予排除。

将 N0、N1 的公共边单独保留，其对称差分解为交替路径与偶环。每个分量有两种匹配方向，分别取 N0 或 N1 的边。公共边的任务/机器不会再出现在非平凡差分分量中。各分量在 job 与 machine 两侧的顶点均互不相交。

## 2. 四种差分分量的全部任务解释

### machine–machine 路径

所有任务顶点都是度2，因而在两份见证中均以 unit 时间运行。选任一匹配方向都覆盖这些任务；内部机器始终恰有一枚 unit，两个机器端点的unit-presence相反。一端在N1中新增unit，另一端在N0中有unit而N1中没有。

### job–job 路径

内部任务在两见证中均为unit。两端任务分别只在N0或只在N1中以unit运行；各自另一份见证中的位置是一个实际 small 端。选任一匹配方向，恰有一端任务unit运行、另一端任务small运行。路径中的每台机器两方向均恰有一枚unit。

因此，这个分量可暂时等价为一枚 virtual small job：两个可选机器是两端任务各自的实际 small 位置，处理时间都为1/k。选其中一个位置后，就选使相应端点任务 small、另一端点任务 unit 的匹配方向。两个 small 位置相同也没有问题，可固定任一实现该位置的方向。该虚拟描述只是算法中的组合变量，最终必须解码回全部原任务。

### job–machine 路径

路径的一个方向同时匹配端点任务与端点机器，称为 active；另一个方向二者均未匹配，称为 inactive。内部任务两方向均unit运行，内部机器unit-presence不变。inactive 时，端点任务应去它在另一份实际见证中使用的 small 端；active 时这枚任务unit运行，端点机器增加一枚unit。

故将该分量从inactive改active，只会删除端点任务的一枚 small 负载并在机器端点增加unit；不会在别处增加small负载。active可以是N0方向，也可以是N1方向。

### 偶环、公共边和没有unit边的任务

偶环与公共边上的任务始终unit运行，机器unit-presence始终1。任意不在N0∪N1中的原任务，在两份见证中都是small；它可暂时在两份见证的实际small机器之间作普通等时间分配。

以上分类覆盖全部原任务：unit degree为2的任务始终在分量内部；degree为1的任务恰是路径端点；degree为0的任务是small–small。不会丢任务、重复任务或把virtual job当作额外原任务。

## 3. 测量机器只能是新增unit的机器端点

机器 v,w 都在N0中未匹配、在N1中匹配，所以一定是某条差分路径的机器端点。它们不可能是公共边、环或路径内部机器。

machine–machine 路径的两个机器端点中恰有一个是N1新增端；job–machine路径只有一个机器端点。因此同一分量不可能包含 v,w 两者。改变一个测量机器所在路径的方向，不会改变另一个测量机器的unit-presence。

若要求00或11，直接输出σ0或σ1。以下只处理一个测量位须vacant、另一个须present的混合；将须vacant的机器记为 v，另一台记为 w。

## 4. vacant 输出位来自 job–machine 路径：直接实际翻转

若 v 是job–machine路径的机器端点，它在σ1中必为active方向。直接从完整σ1出发，将此一个分量的unit边改为inactive的N0方向。分量内部机器仍各有unit，v失去unit，没有任何机器新增unit。将唯一失去unit分配的端点任务送到它在σ0中的small端，增加1/k负载。

其他全部原任务保持σ1分配。第3节保证 w 不受该分量影响，所以 v 的presence为0、w仍为1。所有机器负载同时满足

Cmax≤T+1/k=1+2/k≤1+ceil((k+2)/2)/k=B(k)。                 (1)

该分支是真正移除测量机器的一整unit-presence，而非只移动某个指定SUjob后仍允许该机器被另一枚unit占据。

## 5. vacant 输出位来自 machine–machine 路径：全部 activation 与 small 流

若 v 位于machine–machine路径，先在该路径选择N0方向，使 v vacant。w若也来自machine–machine路径，则在其不同路径选择N1；其余此类路径按固定规则选N1。

将所有job–machine分量一律设为active。这满足w若来自job–machine路径时的present要求。没有任何须vacant的job–machine测量端点，所以无需留下inactive例外。

偶环与公共边选定一个固定方向。job–job路径暂不选方向，而是保留第2节的virtual small变量。它们的机器unit-presence不依赖方向，因此此时所有机器的最终unit-presence已经确定，并且v=0、w=1。

剩下需要分配的small变量只有：

1. 原来在σ0、σ1中都small的原任务，各可选其两份实际small位置；
2. 每条job–job路径的一枚virtual small变量，可选其两个端点任务的实际small位置。

对这些变量在两位置各放一半；相同位置合并为一份。记每机分数任务数为μ_i。再令 n_i^s 为原σ_s在机器i上实际安排的small任务数。则

μ_i≤(n_i^0+n_i^1)/2。                                  (2)

原因是原small–small任务与job–job路径的virtual变量，贡献恰等于这些原任务的small均值；所有job–machine端点任务在原均值中贡献一半small，但现被设为active而不再产生small，故只删除均值质量。其他任务两见证均unit，不贡献small。

现在建立small变量到上述两个原small机器的二部流，机器整数任务容量取 ceil μ_i。给定半半分配已证明分数满流可行；整数容量流给出覆盖全部变量的实际整数分配。

原small–small任务直接去流选定的原端。对virtual变量，按流选定的small位置恢复相应job–job路径方向：一个原端点任务small，另一端点及全部内部任务unit。各差分分量的unit顶点互不相交，且job–job路径所有机器的unit-presence恒定，所以这些恢复不会破坏已固定边界或其他分量。

至此全部原任务都恰有一个原合法目的机器。没有分数任务执行，也没有凭virtual jobs虚构额外资源。

## 6. 全部机器的同时负载界

由T=1+1/k，原见证某机若有unit，则该机small任务数≤1；若无unit，则small任务数≤k+1。按unit-presence在两见证中的三类情形，结合(2)：

* 两份见证均unit-present：最终仍unit-present，μ_i≤1，整数small数≤1，负载≤T。
* 两份见证均unit-vacant：最终仍unit-vacant，μ_i≤k+1，负载≤T。
* 两份见证的unit-presence不同：μ_i≤(k+2)/2，整数small数≤ceil((k+2)/2)。最终若present，负载≤B(k)；若vacant，负载只会再少1。

这三类穷尽全部原机器，故第5节构造整体 Cmax≤B(k)。与第4节合并，两个混合边界均有实际完整构造。

## 7. 总位复杂度与参数边界

unit差分只使用两份实际见证中的边，总边数至多2n；寻找分量、设置方向、解码每个原任务均为显式多项式。small流每个真实/virtual变量最多两个边，机器容量可截到变量数；分数证书分母仅为2。没有按k数值复制任务或机器。所有最终负载是1/k整数倍，其编码和精确检查按输入及两见证的总位长多项式。固定输入次序处理并列即可确定化全部选择。

k=2、3分别给B=2，不声称绝对次二胶合。对偶k，B=3/2+1/k；对奇k，B=3/2+3/(2k)。因此所有k≥4时B≤9/5，在k5达到这个最大值；k趋无穷时B趋3/2。另有B≤(3/2)T，奇k等号。

空任务无法满足两台测量机器在σ1中新出现unit的附加合同，故本定理不制造空实例反例。它不声称自动找到两个严格见证，也不处理非统一small时间。

## 8. 四机锐族与真实 mixed OPT

对每个k≥2，取机器P,Q,M,N，unit任务x仅可P/M，unit任务y仅可Q/N。另有两组各k+2枚small任务，第一组每枚仅可M/Q，第二组每枚仅可P/N，时间均1/k。全部其它边∞。

σ0：x→P，y→Q，第一组M上k+1枚/Q上1枚，第二组N上k+1枚/P上1枚。σ1：x→M，y→N，第一组Q上k+1枚/M上1枚，第二组P上k+1枚/N上1枚。两见证的所有机器负载都恰为T，M/N的presence分别00与11。

混合10强制x→M、y→Q，因此第一组的两个可用机器都先有unit；其k+2枚small任务必有某机至少ceil((k+2)/2)枚，负载至少B(k)。两组各自尽量平均分即可达到B(k)：第一组两个unit机器负载为1加其small负载，第二组两个无unit机器负载更低。混合01对称。因此两个混合边界的精确最优值均为B(k)，证明统一上界锐。

这族有4台机器、2k+6枚任务，每件最多两个有限端。它的显式大小为O(k)，只用于逐k存在的锐性族；没有声称仅按log k输出k枚任务。全输入无边界约束的OPT恰为T：一致模式中每个small二机组的总负载为1+(k+2)/k=2T，故最大负载≥T；非一致模式的B(k)也≥T，而上述一致调度达到T。

k=3因此给出真正可读的二位复制器：两严格模式负载4/3，任何非一致边界精确需要2。由于2/(4/3)=3/2，它不构成近二近似困难性。k大时本定理反而说明任何这种两个可读输出的两见证硬件都存在负载≤9/5的混合。

## 9. 审查范围

完整证明等待陈述先行重构之后的读后攻击。此处未运行代码，未登记或修改canonical。没有借用root的normal-form新定理，没有把旧SU小码擦除当作本机器presence结果，也没有声称一般UM正面或反面完成。
