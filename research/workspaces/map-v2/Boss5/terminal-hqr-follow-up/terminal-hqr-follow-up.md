# 真第三位HQR和旧末位模板的双向固定点比较

拟3B端点：

- `customer-attraction/three-cross-family-terminal-templates-matching-exact-certificates-and-floating-traces`
- `cag-dual-terminal-737-exact-primal-and-full-type-dual`
- `M-049f49c6150f4a8b969b1b33c33523ac`
- `customer-attraction/actual-third-thirteen-row-two-state-hinge`
- `customer-attraction/explicit-actual-third-7497-row-rational-necessary-point`

原文：`archives/customer-attraction/state/引理/真实第三位投影的五人最大根包络--引理.md` §1–2；`archives/customer-attraction/state/引理/实际第三位十三行投影的两态铰链分解--引理.md` §1–4；`archives/customer-attraction/state/程序/真实第三位固定查询闭包与双菜单替换定价--程序.md` §固定主题闭包；`archives/customer-attraction/state/程序/最大根铰链定价的索引域与冻结发现记录--程序.md` §3；`archives/customer-attraction/state/程序/显式实际第三位扩展的受限列与旧池定价--程序.md` §数学输入及真实历史、§一组共享HQR的完整747行、§初始受限问题与投影删除。归档7497点是 `archives/customer-attraction/tools/evidence/five-full-actual-extension-primary/original/certificate/exact_full_actual_extension_known_v1.json`，SHA256 8b28de8d89c76684bc95c3eb3f890e6f4ee4492cb152102281d125912e2a30e2。

## 旧末位最优点不能提升到7497的指定必要系统

写实际五题会员为a,b,c,d_act,e，客户实际根及第三位份额分别为a和c除以该五位之和（零分子取0）。在任意真实五人纯SPE，强制根选裸大小最大主题M后再按同策略继续，首位收益至少K/5（K=|M|）。根IC给实际根收益u_A≥偏离收益，故K≤5u_A。该根界亦由7497继承的 `max:root:IC` 加逐客户v_M≥m/5推出，独立于整数原客户假定，可直接用于必要质量提升。

P7取实际第三位(A,B)，p=a+b，u=u_C，D为原合法五索引比较元组（共同T重数），J为固定合法主题W重复五次（十位的第8位，AEUVW的末题，不是标量实际福利W，也不是Sbranch整族mW）。P7行就是7497继承的 `PFixed:actual:W`。K项系数1085>0，代入5u_A所得为原行上界，完全只读旧字段。四个终端模板精确原始点的这个上界都负，所以各点均无保旧投影质量的7497可行提升。

P13取同一真实实际第三位。十三行中m=1_M只在307(m−h)出现，z4只在66·tax(Y,z4;1,1)出现。固定HQR态时把z4从0改1，税系数差为−1/(p+h+1)（Y=0）或1/(p+h+1)−2/(p+h+2)=−(p+h)/((p+h+1)(p+h+2))（Y=1），总非正。故取z4=0给逐客户更松上界，仍可对HQR八态取最大。把聚合正项307K换为307·5u_A后也只读旧字段。四个终端精确点在该上界上仍严格负。这里P13是对13条747共享实际HQR行按同一隐藏态非负加权再逐客户极大，故任何7497可行提升都必须通过它，即使7497删去冗余的单独旧P13投影行。

两个不同上界的四个精确值见伴随JSON。7497冻结64旧型用真实存储的max_bits重算也确实满足所选P7（逐精确值等冻结 `PFixed:actual:W`）、P13及K≤5u_A。

## 反向终端分离

显式85型按原证书先合并为64个旧型，再忘记max_bits（重合时合并质量；线性行直接求和等价）。旧717的定义确为5421→6541→6750→7497的继承公共块；全部717键也都在7497冻结结果内。忘记字段保持W与O，因此任一7497可行向量投影落入717。有限7497冻结点在727/728/737共有的额外AB→Sbranch坐标1O为严格负（exact JSON完整分数）。这一行将固定客户的AB源p=a+b+t_i+r_i、真实末题s_i，与Sbranch的第一非锚点会员（族mU）在同t的完整目标tuple内重排；每次去对角系数为(4s_i−K_menu+z_{π(i)})/(p+1)。该冻结点虽通过7497全部指定行，但它的旧字段投影分别不满足727、728、737。这三个可行集各不包含7497投影，也不被7497投影包含，且7497投影严格小于717。

结论只比较指定线性必要系统。排除的是明确的四个原始质量点、7497冻结点和由它们直接证成的可行集关系。没有排除所有各模板最优点，没有求两类条件交集最优，没有推出真实策略、真实最优比较菜单或六人福利结论。

在仓库根目录运行 `python research/workspaces/map-v2/Boss5/terminal-hqr-follow-up/check_terminal_hqr_followup.py .`。脚本复用3A的原始点读取器，使用标准库有理数重算四点的P7/P13上界、7497点的投影原值、根界及反向终局行。输出与同目录 `terminal-hqr-follow-up-exact.json` 对照。
