# root独立解析复核：新核与换位

2026-10-24。已读作者稿后从单位客户定义重新推导，不称盲审。Q-CAG-HALF仍OPEN；无外审/新颖性认证。

## 退券及CLIP

对象：[credible正文](../credible/safe_coupon_netting.md)。固定context，逐客户覆盖者集合给v−D=P−N及D−N=J+L>0。actual完整IC给D≤u，故F=N+u−D在[0,u]。将整行βu同比例退βF合法，净当前actual行非负，past正边仍为原actual标签。全过程没有重权原客户IC。

任取原正边子量c≤min(P,F)，删出流c并将当前净行增加c，恒等v=(u−F+c)+(P−c)保持。c=min(P,F)给当前min(v,u)、外送(v−u)+；这种标量重采不保持客户血缘，但原利润图允许它。原正future/past边删减后域不变，递增角色DAG有限。固定初始注入、同原v分母，删边得β新≤β旧；κ新=h新/max(v,u)≤β新。故新正actual券load≤旧gross券load；没有相对于旧net券load的单调性。

这也给局部最少外送：若当前实际整行系数限定≤β，则它至多承接βu，输入βv至少外送β(v−u)+。CLIP达到此值。没有推出全局容量，未用off-history slack ell≥0。

## fresh利润分母

对象：[relay正文](../relay/fresh_profit_normalization.md)。只在a\C上求和时，nu−P=J+L=d_F−N>0。正边由fresh客户见证，后继规定叶同样有fresh利润，故nu=0的域不会正接收。用nu归一化仍为角色DAG、全fresh质量守恒。完整actual IC给d_F=u−Y−e，从而没有正X或past券；Y+N+e在[0,u]，可作安全当前整行退款。

每个β仍是一个固定context的单一标量；不能称按客户施加IC。nu≤v可能增大后续β，不能将新核描述为费用改进或与旧核SOURCE/HIT免检拼接。尚缺同角色跨context净券总量的共同容量，未实质用ell。

## 可信相邻换位

对象：[global正文](../global/credible_adjacent_transposition.md)。全部孩子独立可取最小根收益，所以mu=max_X min_child u_X恰为节点最低SPE首利。固定AB尾SPE时，AB可实现当且仅alpha≥mu、beta≥mu_A。相同AB/BA前缀负载保证整个尾树重标后所有收益比较保持；BA可实现当且仅beta≥mu、alpha≥mu_B。据此增序换位条件、固定终局counts的lex最大正常形成立。

若在任意历史换入同规定终局负载的子SPE，每个严格祖先的一次强制query完成叶若原来到达该历史，现在仍到达并接同负载叶；否则未变。故所有严格祖先收益和IC保持。内部菜单可变，不保Mpath/WP坏性。

末位静态插入界OPT≤(2m−1)u_m来自共同目录中m个最优主题及m−1个实际过去主题的插入收益相加。故真正half坏counts的lex实现有LAST-DIP阈值障碍，但这里只得mu_child>u_i，不得≥tau。没有完成阈值障碍支付。


## 定义级精确回归

[root脚本](audit_clip.py)不导入作者代码或求解器，展开六份既有完整策略的单位客户，以Fraction重算全部3635条原IC、每context的SAFE/CLIP、角色DAG和净券守恒。529个context有真正非零标量取消。使用任意正context各注入一利润单位以激活传播，不是OPT初始化，更不是容量或福利试验。[冻结输出](clip_audit.json)通过。

新正券逐券不超过旧gross，净账总量守恒；124个实际券的CLIP新量高于原net量，确认不能报告对旧net逐点改善。这是定义/实现回归；普遍正确性由上述解析证明承担，没有新游戏、规模搜索或一般阴性推论。
