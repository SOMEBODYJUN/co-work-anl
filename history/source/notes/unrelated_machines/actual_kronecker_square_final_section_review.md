# 完整处理矩阵平方反放大与指派LP乘法：canonical第七节最终读后审查

## 实际对象、顺序与冻结版本

本记录审查 `co-work-anl-boss11/research/current/unrelated_machines/private_graft_and_resource_repetition.md` 的**完整§7，含§7.1–7.4**；不声称重审既有§1–6。最终文件SHA256：

`6e0f4996e94e5873425d2f29d95be494a60cc5eaf1b62f6e46541df5d5c479da`。

审查者先仅据精确数学对象独立生成seed/square、给出另一份100任务完整证书和解析证明，冻 `kronecker_independent_exact_first.md`；之后实际全文读作者原Exact/Proof/checker/证书，冻v1读后记录；再全文读新结构Proof/checker并独立核15件同时交换，冻v2结构记录；随后实际读canonical完整§7的6b766旧版和当前6e0f最终版。**本记录是最终实际读后，非新盲审。** 所有先前版本与hash在同目录前两份读后记录中保存。

本次另用独立程序直接解析canonical的15行任务/旧端/新端表，与已按原资格精确核过的结构表逐行比较，完全一致。摘要存 `canonical_section7_independent_audit.json`。未修改任何共享仓库文件或作者冻结材料。

## 两个精确身份及数学结论

1. `UM-ACTUAL-KRONECKER-NO-TO-YES-v1`：seed完整8机10job/20有限端；每个完整实际tensor平方64机100job/400有限端。seed OPT精确3/2，square OPT精确1，每个整数k≥1的完整偶次幂OPT精确1。这个身份不宣称一般hardness。
2. `UM-UNPRUNED-ASSIGNMENT-LP-KRONECKER-v1`：任意合法非负有理UM的未剪枝assignment LP满足F(P⊗Q)=F(P)F(Q)。不是剪枝LST、配置LP或实际OPT的乘法结论。

§7.1的原机器、job字典序、F₂资源公式都与独立重构一致；所有任务对和machine pairs均保留，mixed AB/BA各16、BB64、AA4。seed lower bound强迫已选根导出两条incidence而在交点撞unit；达到3/2调度包含全部十job，正确。

§7.2的初态公式已独立代数核：SS16行都1，AB/BA真实双射分别填SR/RS16行，RR映射矩阵[[a,1],[1,c]]行列式1+ac；唯一a=c=1块发生对角2、非对角0。十五枚job的旧端、原新端资格、真实乘积处理时间都独立核过；13台受影响machine的移出/移入量与正文逐项相同，其余51行不变。因此最终64个原machine load均恰1。canonical十五行与独立已核交换表一致。

AA unit给square下界1，有限坐标求和乘积分解给偶次幂上界1，全selector tuple给下界1。k为完整tuple幂的整数指数；显式输出敏感边界已说清，不把10^(2k)件任务隐写成binary k多项式。

## LP域、零值及不可用边攻击

§7.3现在明确合法m≥1、n≥0、非负有理时间与每job非空finite资格。合法资格保证LP可行，m≥1使T被非负行负载约束为非负，归因已修正。

Primal两最优分配相乘给每个机器对负载恰为原两行负载之积，故≤F(P)F(Q)。Dual取y,z单位单纯形上的最优点，乘积仍总质量1；每job-pair的有限资格集合确为笛卡尔积，非负min乘积因式分解，求和给反向。双方向正确。

m≥1使T可直接视为自由变量而仍有T≥0，因此dual Σy=1不需要F>0归一化。若显式约束T≥0，初始dual Σy≤1也可借非负性补足质量。有限0、F=0、n=0、unused machine、任意∞模式均覆盖；min只在原非空finite资格中取，不计算0×∞。m=0与负处理时间不在已写域。

seed半/半primal全行1，dual(S)=1/6、dual(R)=1/12的八权和1，objective=2/6+8/12=1，故F(seed)=1。强对偶是该泛化唯一额外标准事实，与有限平方证书的证明角色分开。没有把一般LP恒等扩成配置LP。

## 来源与证据角色

§7开头已明确：公屏seq260/264先前报告同类10机14job parity half-selector实际square现象；此处未取得其完整冻结证明，不替旧报告认证，不认领现象首次发现。审查者没有读到旧实例完整原件，因此也不为其具体数值真值作独立认证。本次可独立确认的是本8/10 seed、完整新证书与十五件交换。

作者search、作者独立于search的checker、作者原证书、审查者另构的不同证书、Exact-first数学重构、作者读后和最终canonical读后分别是不同角色；正文与review链接未把其中任何一种冒充另一种。原优化器optimal/success不参与实际数学上界有效性。外审、全球新颖性和论文价值仍未认证。

## 最终范围与裁定

当前完整§7两个精确身份均通过本次指定范围的最终读后攻击，**无standing fatal**。同时替换措辞已明确，不承诺逐件顺序中间容量。来源去重与LP域归因已修正。

只关闭任意真实3/2-gap seed的完整Kronecker平方自动保NO/gap放大的全域合同；不排hard-image限定产品、新物理一致性gadget或一般near2困难性。无NP-hard源、无主目标算法，UM-TARGET-v1仍OPEN。该记录可作为这两个§7身份的最终内部读后完成依据，不能登记成新的盲审或外审。
