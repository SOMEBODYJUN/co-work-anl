# Root对全客户广播消元的独立重构

2026-10-23（America/Los_Angeles）。本审查在读取作者稿后从单位客户定义重新推导，不称盲审。原Q-CAG-HALF仍OPEN；没有外审或新颖性认证。

对象为[credible正文](../credible/all_fresh_submarkov_elimination.md)。root先独立给出全客户正负coverer差的推广，作者随后明确过去出口的真实域；以下复核基础fresh核、全客户核和source初始化。

## 解析检查

固定natural context当前规定动作a，真实完成叶B与actual-prefix强制a后的完成叶A。对x∈a，两叶均由当前角色覆盖x，故c_A,c_B>0。删当前角色后的coverer集合J_A,J_B满足

    1/c_B−1/c_A=(|J_A\J_B|−|J_B\J_A|)/(c_Ac_B)。

将正差全部广播后，原利润的逐客户剩余恰为[1+|J_A∩J_B|]/(c_Ac_B)>0。求和就是ALL-LOSS，严格号只用于非空动作。fresh客户在A的所有其他coverer均为未来角色，B中的过去coverer只贡献负差；fresh LOSS中X、J、L和负N的符号正确。

用v=u_i(B)归一化，而不是用D=u_i(A)或原R捕获量归一化，是本稿与旧fairshare流的区别。对任意k个recipient，单客户贡献至多k/(k+1)，且客户权1/(c_Bv)总和至多一，故SUBSET成立。正future边终点(A_<j,j)的规定完成叶确为A；各context按完整有序历史区分。有限角色递增使全边出入可逐项相消。

全客户版本中，过去正recipient的主题是actual S_j，其客户必属actual C。A包含其未来强制query，故不能向A里的过去角色调用原IC。正文将它送到带(j,x)的actual coupon终端，避免了这个域错误。只递推future边，仍是有限DAG。质量恰分成diagonal/common-coverer剩余与past出口；使用actual IC slack e=u_i−D后得到COUPON-LEDGER，未丢失负N和负e。

源query通常不是natural context规定动作；INIT先按同一真实源叶均分给当前吸收与真实未来coverer，再仅把未来份额注入natural context，初始化正确。source和后续βu_i必须共用实际钱包，不能再次领取W。

附带检查：fresh行和至多(r−1)/r，其中r为当前剩余角色数。从h利润单位注入、只计该fresh-DAG总访问利润质量，至多(r+1)h/2：F(1)=1、F(r)≤1+(r−1)F(r−1)/r即可。这个数不控制βu_i成本，更不支付C券；不另立福利Claim。

## 精确回归和证据范围

[独立脚本](audit_broadcast.py)不导入作者代码或仓库求解器：展开实际单位客户，逐个有序历史重算全部原IC、两个completion、fresh/all-client局部式、source INIT及两种DAG全局账。使用Fraction，没有浮点容差；另含零客户、空主题及单人边界。[冻结输出](broadcast_audit.json)记录Python版本、输入名和结果。

六份既有策略的fresh正future边均为零，因此这些策略的全局回归没有测试非零fresh级联。输出如实保留计数，不得描述为一般多层fresh流的计算验证。全客户局部future正边及portfolio的past出口确非零。另对小coverer集合直接验证非零正差和LOSS，身份仅是标量代数回归，没有SPE认证。一般结论由解析证明和有限DAG求和承担。

复现（仓库根）：

    python research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/parent/audit_broadcast.py

## 通过范围与未付义务

基础fresh LOSS/SUBSET/DOMAIN、INIT、MASS/C-LEDGER及全客户ALL-LOSS/COUPON-LEDGER通过本次解析审查。可选chi只是重归一化，没有净成本改善结论。后加的prefix-deficit及谱系区间组件不在本次审查范围，另行核验。

没有证明COUPON-LOAD共同cap1，也没有证明负N或e可退到同一actual券。同一客户的负过去coverer可能来自g里的非实际主题，不能按客户名假配给actual S_j券。fresh正项消元后实际行βu_i可能反复出现；half的不确定性仍在这些行、past券及source费用的共同付款。

这是一份全输入付款表示和合法域澄清，不是新增福利下界。基础核未使用ell≥0；后续若声称利用真实孩子最优性解决费用，必须指明新的off-history比较如何压住共同C账，不能只重排恒等式。
