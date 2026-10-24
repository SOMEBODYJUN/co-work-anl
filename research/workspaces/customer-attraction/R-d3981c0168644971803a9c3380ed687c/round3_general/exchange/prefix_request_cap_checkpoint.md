# peer prefix请求cap2：精确检验形式与未付点

2026-10-24，探索检查点，不是完成的一般付款引理。

## 1. 原候选的准确量词

固定任意原模型完整纯SPE及实际有序终局B=(B_1,...,B_m)，实际收益为u_j(B)。
每个分支alpha指定切点i_alpha和合法强制主题T_alpha；此前保持实际有序前缀，随后执行同一份完整策略，得到真实完成W^alpha。切点允许等于目标角色l，也允许同切点有多个孩子。只有j<i_alpha的固定旧角色可作源。

令c_B(x)、c_alpha(x)为两份完整m人叶的客户负载，定义

\[
q^+_{\alpha j,l}=
\sum_{x\in B_j\cap(B_l\setminus W^\alpha_l)}
\frac1{c_B(x)c_\alpha(x)},\qquad j<i_\alpha\le l.
\]

因为j是固定旧角色，求和客户在W^alpha中仍被B_j覆盖，两分母均正。
非负请求lambda_alpha,j只要求每个源j分别满足

\[
\sum_{\alpha:j<i_\alpha}\lambda_{\alpha j}u_j(W^\alpha)
\le u_j(B).
\tag{SRC}
\]

待证候选为每个目标l的

\[
\sum_{\alpha,j<i_\alpha\le l}\lambda_{\alpha j}q^+_{\alpha j,l}
\le2u_l(B).\tag{PCAP?}
\]

本分支没有证明它，也没有证明它足够推出half。peer已有末位cap2解析证明和逼近2的反族，本分支未重证或独审那些材料。真正待攻的是l<m的多尾情形。

## 2. 消去请求变量的精确形式

对固定目标l和源j<l，定义

\[
\rho_{jl}=\max_{\alpha:j<i_\alpha\le l}
\frac{q^+_{\alpha j,l}}{u_j(W^\alpha)},
\]

空集合最大值取0；零源利润时比值取0。该约定合法：u_j(W^alpha)=0意味着B_j没有任何正价值客户，故q^+=0。
则(SRC)下的左侧最大值**恰为**

\[
L_l=\sum_{j<l}u_j(B)\rho_{jl}.\tag{TEST}
\]

上界由逐源q<=rho*u直接相加。反向因分支集有限，每个正预算源可独立选择达到rho的一个孩子alpha，并取lambda=u_j(B)/u_j(W^alpha)；不同源的请求没有共同分支容量约束，所以可以同时实现全部最大值。原(SRC)中i_alpha>l的请求不贡献目标目标，取零即可。

因此原候选等价于L_l<=2u_l(B)。这只是去除lambda的有限线性规划消元，不能算新一般付款。

## 3. 为什么原真实IC尚未完成付款

在实际l节点，原SPE确实给全部合法主题A的真实偏离

\[
u_l(B)\ge u_l(Z_{B_{<l},A}).\tag{IC-l}
\]

若A=B_j，旧j与偏离者l在该**同一完成叶**收益相同。因此复制旧源是一个合法的比较。
但(TEST)的分母u_j(W^alpha)来自许多可能早于l分叉的不同历史，(IC-l)并未把它们换成复制B_j后的源利润。W^alpha在位置l的原策略动作也可能完全不同于B_l。不能把这些支路源归一化因子逐一搬到实际l节点，或把单叶的券分配套用在多支路之和上。

静态上，q^+<=u_j(W^alpha)/2，因为其客户同时在实际B_j、B_l中，c_B>=2。但这只给每个源的请求贡献<=u_j(B)/2，求和得到L_l<=sum_(j<l)u_j(B)/2；它没有由2u_l(B)支付该前缀利润。

故这里需要真实后继IC的跨历史关系，而非仅源库存、q逐客户为正或复制后的同叶等收益。尚未构造该关系。

后续root指定检验的whole-profit保护桥“复制旧源的真实回报至少为其原利润的一半”已由本分支[35客户完整SPE](copy2_counterexample.md)否定；同例还给u_1=18>2u_2=16。它的实际源与目标主题不交，所以q^+=0，**并未否定本页PCAP?**。不能以该桥失败替代原交集支持预算的判断。

## 4. 定点检查的真实范围

probe_prefix_request_cap.py不导入规范BI或verifier，而从已存客户类型和完整策略重放每个有序历史，逐个合法行动重算真实完成与Fraction收益。然后对实际各目标直接计算(TEST)，保留每个源达到最大值的孩子和饱和lambda。

输入仅11份旧证书：root-tax、fractional-actual-load、prefix-balance、global-decorrelation、individual-security、worst-PNE、worst-CCE、eight-CCE、aggregate-theta、collision-free及上传的四人十二主题auxiliary证书。全部通过定义级SPE重放，未见PCAP?违反。这个事实不是一般证据或独立审查，不推出cap1，更不证明half。

保存的输出属于明确候选的旧例定点检查，不是新的特殊人数正面结果。root要求停止扩输入后已停止；后续应一般解析或明确可信switch，而不是扩大阴性扫描。
