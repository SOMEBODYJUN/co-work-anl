# 固定比较 T 的联合付款 primal：合同重构及对稿审查

2026-10-24，inventory8。原任意人数、任意有限共同目录、每份完整历史纯SPE；**Q-CAG-HALF仍OPEN**。root给出合同后，先独立重构§0；该节写成时尚未读取作者primal正文。随后对全文核对，结论另记。不是完全盲题发现，不将可行性当已证。

## 0. 读取正文前的合同重构

固定sigma、actual B、比较T。p、r、qhat、W_i、H均由这些数据定义并固定。初始变量a_ijx在[0,qhat_ijx]内，Σ_j a_ijx≤r_ix，c_ix=r_ix−Σ_ja_ijx，d_i=Σ_xc_ix≤u_i。I客户future总额A_x用同一actual客户剩券w_lx−H_lx支付：J_lx≥0、H_lx+J_lx≤w_lx、Σ_lJ_lx=A_x。不能固定使用旧剪枝的J数值。

R客户仅进入真实natural contexts；每个context/reset叶和客户负载由固定sigma确定。未来new coverer的边变量等于h_tx/c_A(x)，共同coverer的边变量在[0,h_tx/c_A(x)]，其余边0。h为初始a与前驱边之和，L_tx=h_tx−Σ_future z非负。R没有actual past coverer或actual-prefix正输入sink。

初始每边a≤p/c_W且每源总a≤p，故多query一般密度引理可用：非actual目标首偏离k固定全部父角色为k，父节点同角色反链按源质量计数，直接来源owner=k的密度总额≤该owner所有p之和；得f_tx=c_Vh≤1。所有mandatory positive边完整保留，common边只减current，所以L_tx≤f_tx/c_A(x)，求和后一次完整IC给L_t≤u_role。未声称多个contexts共同只有一份u。

最终明确施加同一role容量d_l+H_l+J_l+Σ_(t:role=l)L_t≤2u_l。逐客户初始化p=P_B+c+a，I的a被J精确替代，R的future质量被有限DAG的L精确替代，故总和恒等于|O|。只要所有约束存在可行点，容量求和即得|O|≤2W；取最优T才得HALF。固定T的系数均固定，所有约束线性。一般可行性是未证承重，不可由DAG守恒或局部IC推断。

## 1. 全文对稿结论

完成§0后，完整读取 [residual8 primal](../residual/linear_joint_payment_certificate.md)及其[价格势正文](../residual/common_edge_price_potential.md)，未发现致命异议，合同审查通过。固定T/sigma后全部完成叶、分母、边集、r/H/qhat均固定，h/c_A是固定系数乘变量，故INIT、I-PAY、R-FLOW、ROLE确为有限线性系统；任意非最大初始a须在本次同坐标库存中重求d与J，正文正确保留此耦合。R边数给h/c_A≤L≤h(1+|M|)/c_A，且1+|M|≤c_V。GENERAL-DENSITY的多query推广亦成立：一个非actual目标首偏离k固定所有reset父role为k，父节点可多但同origin/client在该层构成质量反链；每条父边的目标密度贡献≤父h，直接来源owner只能为k，按全部query的p一起相加即得f≤Σ_(owner≤k)p≤1，无需T最优性或SPE。任意可行流可以按每节点来源输入比例拆回origin，所以该反链论证没有假设父唯一。随后先求和再用一次wholeIC，未按客户重权；多query的初始付款预算也未被广义密度引理偷渡。I源由同客户剩券J精确替换且不再传播，R严格未来守恒把全部R源精确替换为L，MASS与同一可行点ROLE求和才推出|O|≤2W，只有T最优时才给该SPE的HALF。忽略ROLE后系统非空，且有限源质量与DAG使P0紧；非负价格分离及common边价格递推正确，lambda恒1仍暴露尚未证明的原总资金不等式。**未证明一般ROLE可行性、某个最优T必可行、旧SAFE/CLIP版本RESIDUAL-CAP或一般HALF。** 无新扫描，外审与新颖性未认证。
