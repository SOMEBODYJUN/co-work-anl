# 完整矩阵平方与未剪枝指派LP乘法的作者读后独立审查

## 实际顺序与冻结对象

审查者先仅从 parent 的 seed/产品定义独立生成完整 P⊗P，寻得与作者不同的100任务证书，写完独立解析证明/64行实际分配表并冻结 `kronecker_independent_exact_first.md`；之后才收到作者材料路径。故本记录确是独立陈述重构后的全文读后攻击，不是先读作者Proof再冒充盲审。

本次已实际全文读：

- `hardness_amplification/EXACT_ONLY.md`，SHA256 `5453474934b7f7a162f2e4631e48b0df86b6cb7b01c7e68f11b13669618187f2`。
- `hardness_amplification/PROOF.md`，SHA256 `d8d40984521677e6cdcb68b3d5b67ee16cb16596d4356215f00cba7e2d66bf87`。
- `hardness_amplification/verify_certificate.py` 全文与 `square_certificate.json` 全部100项 assignment/64行 loads。

完整读取并检查 `square_input.json` 的全部6400原位置（400有限端），作者证书100项按原资格公式再核一次，无导入作者checker。另运行已读作者checker，与独立检查一致。输入SHA256 `e1ddd488baaae57191ca64136100ae21d8bfe45e0e5215396d13010cd69d2d1c`，证书SHA256 `e9549591650682d90bb5918be55a3e74c8f7df4694cec4f50b54b09ddfe70f21`。

此版本**尚未读取新补的 STRUCTURAL_PROOF.md 或 verify_structural_schedule.py**；后者必须另列实际事件，不能用本记录替代。

## Seed、平方和偶次幂攻击结果

没有发现所述范围的错误。Seed C<3/2 时两个被selector占用的状态都必须导出全部incidence，其两条affine line必相交，资源负载2；给出的3/2达到调度完整。所有参数都固定，没有NP-hard源。

平方确为64机、100原jobs、400有限端；selector×incidence和incidence×selector各16件、incidence×incidence64件、selector×selector4件都保留。独立原资格重算确认作者的每个执行端有限、处理时间是原两坐标乘积，64机真实负载均恰1。任一selector×selector任务的所有有限端时间1，给OPT≥1。因此OPT平方精确1，无须信任MILP报告。

偶次幂使用实际平方调度的坐标积，Fubini有限求和给每个tuple机器负载为q个1之积；全部原任务均执行。全selector tuple仍强迫OPT≥1。因此每个固定或任意整数q≥1的等式都成立；显式构造仅输出敏感，不是binary q下的位多项式算法。

## 一般未剪枝指派LP乘法恒等的单独核验

采用普通UM域：m_P,m_Q≥1，n_P,n_Q≥0，有限p、q均非负有理，每个实际job有非空有限资格。产品有限资格恰为两坐标有限资格的笛卡尔积，即使一个原有限处理时间为0，也绝不把0×∞解释成有限边。

F(P)=min T，变量x≥0，各job列和1，各machine负载≤T。可以把T视为自由变量：m≥1使各行负载非负，约束已经迫T≥0，包括n=0。其严格对偶是y≥0、Σ_i y_i=1，以及各job自由α_j满足α_j≤y_i p_ij（所有原有限端），最大化Σ_jα_j。消去α得

  F(P)=max_{y≥0,Σy=1} Σ_j min_{i∈E(j)} y_i p_ij。

min均在非空有限集；单纯形紧、目标连续，最优y取得。Primal的各列单纯形积也紧，有限系数保证F有限取得。若在primal另显式加T≥0，其初始dual是Σy≤1，但非负时间允许把不足质量补到任一机器且目标不减，因此相同最优值可取Σy=1；不存在被漏掉的正值归一化前提。

Primal上界：取两最优x,u，令产品质量v_(i,h),(j,k)=x_ij u_hk。各job-pair列和1，有限支撑保持，每机器对的负载恰等于两原分数机器负载之积≤F(P)F(Q)。

Dual下界：最优y,z的乘积y_i z_h仍非负且总和1。所有数非负，故每个job-pair有

  min_(i∈E_P(j),h∈E_Q(k)) (y_i p_ij)(z_h q_hk)
  = (min_i y_i p_ij)(min_h z_h q_hk)。

对全部原job pairs求和正好是F(P)F(Q)。故等式F(P⊗Q)=F(P)F(Q)闭合。

边界攻击：

- 有有限0边或零对偶坐标：上述乘积与min分解仍成立，没有除法/正值归一化。
- F(P)=0或F(Q)=0：primal乘积直接给F(product)≤0，非负性给反向；无需假设正OPT。
- 任一n=0：产品无job，F(product)=0，空和dual0，等式仍成立。
- m=1、未用机器、任意∞模式：资格非空及单纯形证明已覆盖。
- m=0不在UM域；若独立陈述“任意矩阵”而不明示m≥1会有空单纯形语义缺口。建议canonical直接写m_P,m_Q≥1、n_P,n_Q≥0。
- 不允许负有限时间：非负性是min乘积分解与primal负载乘法界的实际前提。

此恒等只属于**未剪枝**assignment LP；不能把F误标为包含p≤T门槛的LST值，更不能借此声称配置LP或实际OPT乘法。

Seed对偶y(S)=1/6、y(R)=1/12总和1；两selector各贡献1/6，八incidence各贡献1/12，和1。半/半primal逐机负载1，故F(seed)=1。独立还发现逐端不变量c(S)=2、c(R)=1，w(selector)=2、w(incidence)=1且c_i p_ij=w_j，可作为全部square行必须饱和1的额外健全性检查。

## 范围与结论

上述冻结Exact+旧Proof+原证书范围无standing fatal。完整实际Kronecker平方确把OPT=3/2降至1，所有偶次幂均1，一般未剪枝assignment LP精确乘法成立。

仅为具体product接口的方法反例，非主目标反证、非NP-hard归约、非一般算法；没有外部论文定理承重（LP强对偶为标准有限有理LP事实），没有新颖性或外审认证。结构公式/15次交换在本版未读，不包含在此结论中。
