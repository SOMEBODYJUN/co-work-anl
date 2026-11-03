---
id: customer-attraction/repeated-prefix-single-double-branch-and-eight-cell-menu-three-LPs
kind: program
type_tag: 程序
title: 重复前缀单分支双分支与八格菜单的三套LP
status: complete-three-source-program-contracts; all-long-reports-read; no-new-execution
truth_status: necessary-row-relaxations-and-numeric-discovery; not-exact-optima-or-SPE-counterexamples
review_level: all-six-primary-full-read-or-exact-SHA-prior-fullread-reuse; related-current-mathematics-and-later-review-read
scope: m≥3的C^(m−2)AB实际路径；single46行、double77行、比较T三人菜单50行
summary: 自足保三套真实倒三节点/末菜单必要行、端点和八格计数的完整域、输出控制流及数值证据边界；m可大于5/7会员位数，玩家数与标签数分开。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-731efdb50dd844178e597d804bdd4596/terminal_geometry/repeated_prefix_branch_lp.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-731efdb50dd844178e597d804bdd4596/terminal_geometry/repeated_prefix_two_branches_lp.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-731efdb50dd844178e597d804bdd4596/terminal_geometry/repeated_prefix_optimal_menu_lp.py
---

## 实际路径、共同模型与真实节点

有限单位客户、有限非空共同标签目录，m名单位权提供者按全部有序历史依次行动；客户在最终覆盖者中均分。保空覆盖、同覆盖不同标签、重复行动、零客户及任意离轨最佳回应平局。固定任意完整纯SPE，实际路径为C^(m−2)AB、m≥3；它没有被压成计数统一策略。旧[模型页](../定义/共同目录完整历史模型--定义.md)的严格集合目录与当前标签域分开说明，不改变旧定义。

固定实际倒三前缀C^(m−3)。单分支记录强制倒三改B后的真实(C^(m−3),B,Q,R)，双分支还记录强制改A后的真实(C^(m−3),A,V,Z)。倒三被强制者不假设在孩子节点最优；之后Q/R、V/Z均是同一σ的真实后继。固定任意m个可重复比较主题Tᵢ，实际倒二前缀C^(m−2)后强制Tᵢ，原末位回复为Lᵢ。所有出现的标签都在共同目录，所以可作其它相应真实节点的合法查询。

实际覆盖W，比较并集O=|∪Tᵢ|；O不自动是OPTₘ。三个脚本不构造客户实例或完整σ，只在逐客户系数上取非负质量，要求若干**聚合**必要行非负；通过这些行不足认证完整SPE。

## single46行与double77行的全部公式

客户实际及真实分支会员位为(c,a,b,q,r)或(c,a,b,q,r,v,z)，不是m个玩家的编码。m可以超过5或7；只有出现的主题按会员位记，重复C的负载通过m计算。置

\[
p=(m-3)c,\quad g=(m-2)c,\quad s=g+a+b,\quad t=p+b+q+r,\quad t'=p+a+v+z,
\]

\[
u_C=c/s,\quad u_A=a/s,\quad u_B=b/s,\quad z_Q=q/t,\quad z_R=r/t,
\quad z_V=v/t',\quad z_Z=z/t'.
\]

零分子份额定义为零，正分子时分母必正。比较/回复重数d、ℓ及同索引交数h满足0≤d,ℓ≤m、max(0,d+ℓ−m)≤h≤min(d,ℓ)，D=(g+1)(g+2)。两程序共同具有：

|行|逐客户系数|
|---|---|
|S|m u_A−d/(g+1)+h/D|
|Z|m u_B−ℓ/(g+a+1)|
|V|(dℓ−mh)/D|
|TT_diag|ℓ/(g+1)−h/D−d/(g+2)|
|TT_off|(m−1)(ℓ−d)/(g+1)+(d²−d−(m−1)h)/D|
|C_to_B_true|u_C−b/t|

双分支另有C_to_A_true=u_C−a/t′。S是实际倒二对全部Tᵢ的真后继IC；Z是实际末位查询Lᵢ；V是各Tᵢ后的真末位互查其它Lⱼ。TT对角/非对角是各末位在Tᵢ后查询Tᵢ/Tⱼ。它们是有序索引聚合，不多除一个m。

对每个固定主题位e（single五位、double七位），两者都加入：

|行|逐客户系数|
|---|---|
|menu_to_e|(ℓ−m e)/(g+1)+(de−h)/D|
|C_floor_e|u_C−e/(p+3)|
|A_floor_e|u_A−e/(g+2)|
|B_exact_e|u_B−e/(g+a+1)|
|Q_floor_e|z_Q−e/(p+b+2)|
|R_exact_e|z_R−e/(p+b+q+1)|

menu_to是每个Tᵢ后的真末位查询该合法主题。C/A/Q的floor来自相应原真实节点强制它、后继任意改变后分母最多“原背景+剩余3/2人”；B/R是其实际末节点的精确查询。双分支每固定主题另有V_floor_e=z_V−e/(p+a+2)、Z_exact_e=z_Z−e/(p+a+v+1)。

最后对标签族T/L、总会员数k=d/ℓ，分别把上述C/A/B/Q/R（double还V/Z）行的左收益乘m，右e换成k。这是m个合法查询各用一次保底后求和，不是给单一玩家免费m份收益。计数因此为single 6+5·6+2·5=46；double 7+7·8+2·7=77。

single的46行与[任意actual的joint m5之46行](../障碍/五人末菜单与全位置保底联合行锥的精确边界--障碍.md)**不是同一个行集**。后者保m个actual位和全位置最坏保证，却不读取此倒三的真Q/R分支；不能按相同行数或相同ratio转授证书。

## 所有h端点怎样覆盖完整客户域

固定会员位、d、ℓ，各行对h仿射，w=1_{c+a+b>0}、o=1_{d>0}与h无关。因此只列可行区间两个端点（相同则set去重）已经保其凸包的全部线性优化值。端点对数是(m+1)²+(m−1)²=2(m²+1)，故single列64(m²+1)、double列256(m²+1)。这不是只选有利平局，也不是有限游戏采样；原完整SPE的所有真实客户都投到这些域中，但LP还容许没有完整σ实现的列组合。

三个程序均规范W=1并最大化比较覆盖O；W/O不是输入某个实际实例的已算福利比。零覆盖SPE不参与这个归一方向，其原模型half由根任意非空主题正收益偏离直接处理。

## indexed三人菜单的完整50行合同

第三套不是只记录两个固定分支。对每个Tᵢ，在C^(m−3)的倒三原节点强制Tᵢ，取同σ的真实末两回复Qᵢ,Rᵢ。每客户的三元会员模式按**000,001,010,011,100,101,110,111**词典序存八格n_{tqr}，总数m；d=Σnt、ℓ=Σnq、v=Σnr。报告中的counts必须按这个原顺序读，不按直觉调换Q/R或把counts当主题大小。

设p=(m−3)c。对每个i，

\[
F_i={t_i\over p+t_i+q_i+r_i},\quad Q_i^*={q_i\over p+t_i+q_i+r_i},\quad R_i^*={r_i\over p+t_i+q_i+r_i},
\]

\[
F=\sum_iF_i,\ Q=\sum_iQ_i^*,\ R=\sum_iR_i^*,\ tax=\sum_i{q_i\over(p+t_i+1)(p+t_i+2)},\quad H=Q+R+tax,
\]

\[
D_Q=\sum_i1/(p+t_i+2),\quad D_R=\sum_i1/(p+t_i+q_i+1).
\]

所有求和均由八格计数直接加权，不丢同一分支交集。对K=T/Q/R，记kᵢ=tᵢ/qᵢ/rᵢ、M_K=d/ℓ/v、q_K=Σᵢkᵢ/(p+tᵢ+2)、r_K=Σᵢkᵢ/(p+tᵢ+qᵢ+1)。源码完整50行是：

|行族|精确系数/数量|
|---|---|
|root_C_T_true|m u_C−F；1行|
|pair_TT|m(m−1)H−Σᵢ[2d(m−d)/(p+tᵢ+1)+2d(d−1)/(p+tᵢ+2)]；1行|
|Q_actual_e / R_actual_e|Q−eD_Q；R−eD_R，对e=c,a,b共6行|
|pair_same_actual_e|H−Σᵢ2e/(p+tᵢ+2e)，e=0时和为0；3行|
|pair_T_actual_e|mH−Σᵢ[d/(p+tᵢ+1)]（e0），或mH−Σᵢ[(m−d)/(p+tᵢ+1)+2d/(p+tᵢ+2)]（e1）；3行|
|C_actual_e / A_actual_e / B_actual_e|u_C−e/(p+3)、u_A−e/(p+c+2)、u_B−e/(p+c+a+1)；9行|
|Q_all_K / R_all_K|mQ−M_KD_Q、mR−M_KD_R；6行|
|Q_diag_K / R_diag_K|Q−q_K、R−r_K；6行|
|Q_off_K / R_off_K|(m−1)Q−M_KD_Q+q_K、(m−1)R−M_KD_R+r_K；6行|
|C_all_K / A_all_K / B_all_K|m u_C−M_K/(p+3)、m u_A−M_K/(p+c+2)、m u_B−M_K/(p+c+a+1)；9行|

root行由同一倒三节点m次真实偏离求和；Q行是真第四位两人剩余最坏保证，R行是真末节点精确查询；all/diag/off分别对应全部索引、同索引及异索引的合法查询。pair族使用每个Tᵢ后真两人子局的**普通税比较**H_i≥U(X,Y)+U(Y,X)，对显示比较索引求和。它没有使用[强PAIR多保一份交叠](../引理/末两人重叠比较与任意索引聚合--引理.md)；不能把原报告解释成更强模板的最优。

`compositions(m,8)`枚举全部非负整数八格向量，故列8·binom(m+7,7)，m3…8分别960、2640、6336、13728、27456、51480。它保存每客户单分支三位交集，但并未绑定不同客户和不同Tᵢ孩子的完整共同策略。

## 实现控制流、浮点合同与输出

三个脚本都只导入标准库及NumPy、SciPy linprog/csr_matrix，没有本地helper、输入文件或随机源。精确Fraction列转float后建稀疏LP，最大化O，Rx≥0、W=1、x≥0。success时ratio=−fun；point只保x>1e−8，multiplier只保HiGHS不等式边际<−1e−8再取负。所有输出分数来自`Fraction(float(...)).limit_denominator(10**8)`；没有随后的全行有理可行性、全列dual或原始/对偶匹配检查。

三个main均受guard保护，`--max-m`默认分别single12、double12、indexed8，从m3逐项调用run；每项打印去掉point/multiplier的摘要，逐步覆盖同目录同名JSON、scope和累计reports、indent=2加LF。源码导入不跑main，但本轮连导入也没有。**single原63528B报告实际含m3…20，超过代码默认12**；它可由显式更大参数或其它调用产生，原件未记录argv，本页只保实际输出域，不虚构作者按默认命令运行。另两份域恰配默认，也不能据此断言原argv。

全部34报告与每个支持/乘子见[报告资源](../资源/重复前缀三套LP的三十四份原报告与证书界限--资源.md)。本轮没有新LP、Fraction、SPE或旧成功复跑；AST/JSON/hash/链接等包静态检查不认证数学。

## 与已经取得的正证书及后续独审

double的m5数值1.9927595047949187与已有[18行CCCAB半覆盖证书](../证明/五人重复三首主题的双分支半覆盖证书--证明.md)是发现与精确证明的不同层级。该精确证书取目标恰2的18有理/千分权，并不证明原浮点1.9927595本身是精确最优或普遍福利常数。single m5>2只说明原必要行松弛的数值范围，不能证明C→A分支对所有可能证明都必要。

本轮必要相关正常读取后，已发现原独立整数审查进一步接受五人(E,F,C,A,B)、C⊆E∩F。其真实背景p取代2c、全部16×6表及审查范围见[增量独审](../审查/五人包含式前三步证书的后续独审与原表合同--审查.md)。这补足此前9源中扩展数据表缺少的合同，不修改冻结原件或旧stage，也不把本轮知情清洗冒成新独审。

[双块glued程序](实际末菜单联合行锥与双块边缘粘合程序--程序.md)实际依赖本double77行和indexed50行，只耦合共同(c,a,b,d)边际，并非自动检查跨菜单完整IC。原三报告和glued报告不能按数值高低互授精确界。一般五人half已有全称证明，六人/一般half仍须按各自全称量词接续；三套程序都未给原目标反例或精确最优分类。
