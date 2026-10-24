# 全 context 广播后的净券角色集合命中界

2026-10-24，relay。任意人数、一般共同目录、完整原SPE。root与credible收到精确陈述后分别独立重构通过（非盲）。**这是全部来源、全部客户重采后的净券质量约束，不是actual单券cap、钱包cap或half证明。**

## 1. 同一合法非负券图

可任选一种图，不能将两图付款相加：

* round5全客户正广播，分母为完整off-history利润v_t；N/e按round6 SAFE从同一当前整行净化。当前actual角色i吸收beta_t(J_t+L_t)，past正q吸收到其actual角色券，future正q送合法natural context。
* 本分支仅fresh利润归一化，分母nu_t；当前actual角色i吸收beta_t(J_t+L_t)，只有future正q，没有past出口。

统一记分母w_t>0、正边总价P_t<w_t。单位输入当前actual角色的吸收概率为1-P_t/w_t，每条future/past正边概率q_tj/w_t；总和1。future边严格增加角色，past边只进终点，所以是有限守恒吸收图。

已有逐客户PRICE给：对任意非负角色价格z_j，

    sum_(正recipient j)(q_tj/w_t)z_j
      <=max_U [sum_(j in U)z_j]/(1+|U|)。        (PRICE)

U仅取可能正recipient角色，当前i不在U。全客户权重为[1/c_B]/v，fresh权重为[1/c_B]/nu。past券与future context一起进入同一PRICE，不能各领一次质量。

同context合法NET-CANCEL或SAFE最大剪枝只删正边，仍保PRICE；按正确净账将删去质量落当前角色后仍守恒。不涵盖将分母改为v-chi后未经另证声称PRICE不变。

## 2. 任意目标角色集合的全图界

固定K subset [m]、k=|K|。令H_t(K)为从context t注入一单位后，最终actual净券角色属于K的质量。它包括全部跨客户重采、future转移与past终点，不是tracked单客户的访问次数。

显然0<=H<=1。若当前角色i in K，仅用H_t<=1；**不是一到K就假设停止**。若i outside K，令h=k/(k+1)，按角色逆序归纳：future recipient j在K时后续值至多1，不在K时至多h；past coupon取值1_(j in K)，亦符合这两类界。当前actual行吸收在K外，贡献0。

所以PRICE中的recipient价格：至多k个目标角色价格1，其余不超过h。对任意U，写a=|U intersect K|<=k、b=|U outside K|，则

    [a+b h]/(1+a+b)<=h，

因为a(1-h)<=h等价于a<=k。故H_t(K)<=h，归纳闭合：

    i(t) outside K  => H_t(K)<=k/(k+1)。         (GLOBAL-HIT)

空K给0；K为全部角色时无外源，结论真空。该证明将局部PRICE提升为真正全context终端界，没有把单行SUBSET冒充总访问量界。

## 3. 全部natural sources同时求和

给任意固定非负注入b_t，令B(K)=sum_(i(t) in K)b_t，B=sum b_t。整个图最终落入K的净券质量A(K)满足

    A(K)<=B(K)+[k/(k+1)]B(K^c)。               (MULTISOURCE)

这对同一份图、同一批来源同时成立。特别，来自其它角色source的最终角色j净券质量至多这些source总量的一半。不同目标角色不能各取这份一半后仍合计为一半；也没有得到总访问次数界。

## 4. 将合法INIT纳入同一证明

对R客户x，固定owner i与源量rho_x。在真实source query中给current actual角色i质量rho_x/c，每位真实future coverer各rho_x/c并进natural context。这一单位source行仍是PRICE型均分行；当前owned-R总吸收A_i^src<=D_i<=u_i。

令M(K)=sum_(x:o(x) in K)rho_x，则完整初始化后的最终券满足

    A(K)<=M(K)+[k/(k+1)]M(K^c)。               (INIT-HIT)

source当前券只记精确吸收A_i^src，不再叠加旧过付K_i^src。whole-IC写法是alpha=A_i^src/D_i，同一actual IC退alpha e_i后净金额alpha D_i=A_i^src；零量约定同旧INIT。

若初始化全O单位客户，须用全客户图。对x in Q_i，在source query的每个past actual coverer给actual(j,x)券1/c，current给actual i整行券1/c，future给natural context 1/c；总和1，past域合法，初始行仍满足PRICE。因此全O版本亦有INIT-HIT；不能把C源塞进仅fresh图。

## 5. 新增约束与未付项

本页给跨全部natural contexts、跨客户广播的净券终点role cut；不要求固定客户血缘，不合并同主题有序context。全客户的past券与current整行净券都按实际货币质量纳入A。

**未证明**它足以推出A(K)<=u(K)、实际(j,x)单券cap1、全O券cap2或总费用<=W。右侧M是比较来源库存，不是actual钱包u；替换二者会偷渡half。证明也未实质使用ell>=0的off-history最优性。

下一承重是把此全图角色cut与真off-history IC或其它普遍费用关系共同使用，控制同一actual行的多来源。未接通前主目标保持OPEN。
