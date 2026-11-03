---
id: customer-attraction/third-and-second-position-D-copy-fixed-point-completion
kind: computation
type_tag: 计算
title: 第三位与第二位复制D的固定点补全
status: fixed-source-numerical-necessary-extensions; exact-D7-reused; no-new-LP
summary: 旧64原子保质量，第三位D双尾133行1024分型的float最小最大违量负；再加第二位D三尾283行8192分型为正，两LP均optimal，固定非延拓由既有精确七行证书承担。
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/branch_geometry/third_D_completion.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/branch_geometry/third_D_completion.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/branch_geometry/two_D_completion.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/branch_geometry/two_D_completion.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/branch_geometry/second_D_envelope.md"
---

# 固定旧点、不同真实位置与变量

原模型是有限单位客户、共同有限非空目录、五位单位提供者、全部有序历史纯SPE，空主题/重复/零客户/平局保留。实际(A,B,C,D,E)；旧三个固定路径actual=ABCDE、second=AEUVW、third=ABEXY，另有AB/AE三元和second四元查询直方图、三个末回复菜单。输入是旧437必要行的64正有理原子点，SHA18e074ba51357dfa03090fe9b97b8ff868b9c83b2687c7da7ff6f7b39489abe1，未有完整策略。

两个新分支分别是第三位在(A,B)后强制实际D得到(A,B,D,P,Q)，和第二位在(A)后强制D得到(A,D,R,S,T)。P/Q是前者的两个真后继，R/S/T是后者的三个真后继，不能因为目录字母相同就互认后继或政策。

第三位补全还保L_i=σ₅(A,B,D,T_i)的末回复菜单。单客户新位p=1_P、q=1_Q；ℓ=Σ1_(L_i)、h=Σt_i1_(L_i)，共同查询重数j=Σt_i。精确域是0≤h≤j、0≤ℓ−h≤5−j；对仿射目标四个角(0,0),(j,j),(5−j,0),(5,j)足够。当前64旧原子全j1，所以每个有4个不同角。

# 第三位D的133条必要行

7410B third_D_completion.py全文读。它保持每旧原子总质量m_α，把该质量分到(p,q,ℓ,h)局部类型。64×4位组合×4角=1024个非负分型质量，另有一个自由ε变量。报告variable_count1024不含ε，实际LP有1025变量。

记b₀=a+b+d，新尾总负载b₀+p+q，u_P=p/(b₀+p+q)、u_Q=q/(b₀+p+q)，零分子份额0。133行分为以下完整族：

|族|行数|真实含义|
|---|---:|---|
|旧actual/secondE/thirdE真角色查P/Q|20|三个旧路径中10个真正决策角色，各查两个新合法主题；被强制E不借最优性|
|F3D|1|旧第三位C的实际利润不小于强制D后同一原σ收益d/(b₀+p+q)|
|新P/Q查十个固定旧主题及彼此|22|P的安全分母b₀+2；Q在其真末节点用b₀+p+1|
|新P/Q查五比较槽|2|每current利润乘5，减j/其查询分母|
|新双尾tax对十比较索引对|1|10H−j(5−j)/(b₀+1)−j(j−1)/(b₀+2)，H=u_P+u_Q+p/[(b₀+1)(b₀+2)]|
|新P/Q与三个旧末回复菜单互查|12|旧菜单精确总比较及新角色安全分母|
|旧AB/AE第四、第五位查新P/Q|8|同一真实索引节点的当前利润与查询分母|
|新P/Q查AB/AE两回复菜单|8|每族五个合法回复主题的求和|
|旧second索引第三/四/五位查P/Q|6|保三个不同真实节点的过去负载/剩余人数|
|新P/Q查second的H/I/J菜单|6|合法共同目录五主题和|
|新D末回复菜单及其全部相互比较|47|五基础菜单行、10固定/2新主题、10旧角色、6旧菜单双向、4AB/AE节点、4AB/AE菜单、3second节点、3second菜单|

第一部分86行与末项47行合为133。例：Dmenu:S=5u_P−j/(b₀+1)+h/[(b₀+1)(b₀+2)]；Dmenu:V=(jℓ−5h)/同税分母；Dmenu:Z=5u_Q−ℓ/(b₀+p+1)。这些客户系数需按原子质量全局求和后非负，不能当每客户SPE。

固定质量的LP形式为
\[
 \min\varepsilon,\quad x\ge0,\quad
 \sum_{v\text{属}\alpha}x_v=m_\alpha,\quad
 G_rx\ge-\varepsilon\ \text{每个必要行 }r.\tag{1}
\]
ε自由；大正ε总可放松全部行，所以这是最小最大违量问题。对同一精确矩阵，ε*≤0等价于所选必要行可同时非负，ε*<0表示可严格满足；它仍不构造完整SPE。

10826B冻结报告status为HiGHS Optimal，row_count133、variable_count1024、maximum_violation=−0.001440312856564927。它保存全部14个活动行名和83个正split（每条atom/P/Q/ell/h/mass），本批全部消费：64旧原子均有分配，局部角均合法，保存float质量对旧有理m的最大归并误差3.608224830031759e−16。这个小误差只核账簿，没有认证133行精确可行；源没有输出有理恢复或完整动作表。本批0该LP重跑。

# 再加第二位D后的283行

5679B two_D_completion.py全文读。它保留前述(p,q,ℓ,h)，另加r,s,t∈{0,1}，得到64×2⁵×4=8192分型质量，加ε共8193变量。源码允许--source覆盖输入，优先用exact_mass否则旧mass_numerator/denominator；当前报告来源路径是原历史scratch位置，不是本次去读取的另一个工作区。

新行包括F2D；新三尾R/S/T在自己真实节点对旧十主题、P/Q、彼此、五比较/旧新菜单的安全比较；旧角色和所有索引角色对R/S/T的查询；旧菜单与新D菜单的双向比较；及三尾利润定理给的两行。与旧133行合并后恰283个字典行。

三人利润行用[任意合法背景三人5/3定理](../定理/固定背景三人利润界--定理.md)。在真前缀(A,D)后，R/S/T总利润V₃，而任何合法三主题比较的剩余利润≤5V₃/3：一条比较(B,P,Q)，另一条对十个五索引三元组求和，客户右侧为Σ_(k=1)^3 binom(j,k)binom(5−j,3−k)·k/(a+d+k)，左侧(50/3)V₃。它比较同背景下可达利润最大值，不认不同前缀的策略。

550B报告同样是HiGHS Optimal，row_count283、variable_count8192，但最小最大违量为+0.013551301796009453。其七活动行是F2D、D2:5:K:E、D2:5:sumopt、AE:4:R、AE:4:S、secondindexed:3:T、secondindexed:4:T。

这表述为“求解器成功求出正最小最大违量”：若是精确值，会说明ε=0的所选必要系统无解；不能写成求解器返回infeasible。550B本身是浮点证据。该固定点不可延拓的精确结论来自这七行的有理非负权/逐原子max证书，已在[C2独审](../审查/交叉回复税与第二步D分支的独立七行排除--审查.md#d7-fixed-primal)完成并由[一般投影包络](../引理/第二位复制实际D的七行投影包络--引理.md)说明，本批0重跑。

# 状态、比较与接续

旧点早有[根饱和不相容](../障碍/五人索引松弛点的根饱和不相容--障碍.md)和[去对角菜单](../引理/真实菜单去对角比较与五人索引点分离--引理.md)排除，第三位133必要行尚能数值补全没有矛盾。任何更小必要系统的可行点都不自动具备共同目录全策略资格。

本页全部两份源码/两份报告字段、83分配和活动行均保原字节。0原优化器/补全求解，未把数值负/正两次身份改写成精确SPE或新外审。阶段三可登记133到283必要行扩张、七活动行发现来源、精确D7联合排除与新全型列生成的范围差；当前五人half已有别证，六人目标未由此解决。完整证据见[本批入口](../../tools/evidence/branch-geometry-source-resumed-boss3/README.md)。
