# owner 全角色运输 A/B 的独立解析核查

2026-10-23，shared。被审稿为[owner_hybrid_transport.md](../credible/owner_hybrid_transport.md)。**A、B 两项全输入命题均通过。** 过程准确说明：首次读取包含了作者完整证明，随后独立重构以下逐客户事件、全部切割和有理增广实现；本报告是独立解析对稿核查，**不是未读作者证明的盲审**。无外审或新颖性认证。

两项结果只断言同一个任意合法叶上的运输存在性；没有将不同真实叶的库存相加，也没有证明动态 half。Q-CAG-HALF 仍 OPEN。

## 1. 输入及静态 owner 支配

固定任意有限共同目录、m≥1、一个最优合法元组 T，最优并集 O；Q_i⊆T_i 互不交且并为 O。Q 仅为分析基线，不能调用原 IC 把 Q 当合法偏离。固定任意合法元组 B，记覆盖角色 C_x、总负载 c_x、J 内负载 c_x(J)，E={x∈O:x∉B_o(x)}。

对任意角色集 J，只替换 J 内的 Q 槽；每个实现可将未替换 Q_i 扩为合法 T_i，所以覆盖至多 |O|。全替换 J 后的 O 外新覆盖必由 owner∈J 且在 J 内无覆盖者的 O 客户支付。这给 HYB。

在 J 内独立以概率 p 替槽时，O 外新增概率为 1−(1−p)^{c_y(J)}。O 内只有 x∈E、o(x)∈J 可丢失，概率 p(1−p)^{c_x(J)}。因此原稿的 all-J Bernoulli 式和 HHYB 全范围成立。p=0 用可去端点，c_x(J)=0 时右侧积分为1而不是0；这正是无覆盖库存。c_y(J)=0 时左侧为 H_0=0，无需除以零。

## 2. 命题 A 的全部切割

给角色 i 加 source 容量 b_i=Σ_(y∈B_i\\O)1/c_y。对任意 J：

\[
b(J)=\sum_{y\notin O}\frac{c_y(J)}{c_y}
\le\left|\bigcup_{i\in J}(B_i\setminus O)\right|
\le |M(J)|.
\]

只对 c_y>0 写该分数；c_y=0 的项定义为0。对 x∈M(J)，owner 在 J、覆盖角色全在外：若 c_x>0，该客户出割角色边总容量为1；若 c_x=0，其到终点边容量为1。其它客户贡献非负，所以原网络出割容量≥|M(J)|≥b(J)。

这恰是超级源全部边可饱和的条件：任何 source-side 角色集合 J 的总割容量等于 b(J 的补集)+原图出割容量，至少为 b(全部角色)。有限最大流最小割给源总量可全送达终点。所有容量有理；也可统一乘公共分母后用整数流。删去循环不改变角色净流或任一 source/sink 总量。

owner 自环不能提供出割容量，删去它没有影响。角色边可以向前或向后；证明未使用递增角色假设。

## 3. 命题 B 的 all-J 调和割

令 k=c_y(J)、c=c_y。若 k=0，源项为0。若 1≤k≤c，因为 H_n/n 是递减正序列的前缀均值，

\[
\frac{kH_c}{c}\le H_k.
\]

所以

\[
b^H(J)\le\sum_{y\notin O}H_{c_y(J)}
\le\sum_{\substack{x\in E\\o(x)\in J}}\frac1{1+c_x(J)}.
\]

对右侧每个客户 x，写 k=c_x(J)、l=c_x−k。其 owner 在 J，终点边永远贡献1/(1+k+l)，每个 J 外覆盖者再贡献同量，总出割容量为

\[
\frac{1+l}{1+k+l}
=\frac1{1+k}+
\frac{kl}{(1+k+l)(1+k)}
\ge\frac1{1+k}.
\]

k=0、l=0、c=0 均直接合法：特别 c=0 时仅有单位终点库存，且恰达到右侧1。对其它 owner 不在 J 的客户不索取割信用。相加得到全部割≥b^H(J)，再次饱和 source 边，B 通过。

这里终点是 missing-owner 价格，不是实际遗漏。c_x>0 且 owner 未覆盖的客户也在 E；其 role 边容量1/(c_x+1)确是 owner 势分解中的该覆盖者 error。此点与[owner 势 UNIT/JOINT](owner_exchange_potential.md)完全一致。

## 4. 边界及范围

m=1 时两张图均可退化成角色到终点的库存运输，最优单主题保证供给不超过库存。O 为空时所有合法主题都为空，源量为零。空 J、全 J、重复标签、重复最优槽、空 owner 块和无任何覆盖者均没有除零或缺割。

A 的 sink 仅真正未覆盖的 O 客户；B 的 sink 包括已被非owner覆盖的客户。A 与 B 是各自可用的两份证书，不能把它们的同一客户容量重复领取。任意离轨 B 可有新的 O 外客户，不能将其统称为实际 G。

网络允许向更早角色转运；该存在性不能直接粘到递增真实捕获流。不同叶的可行流也未给一个共同 whole-IC 系数。原稿这些限制写得准确。

## 5. 独立精确实现核验

[审计代码](audit_owner_transport_independent.py)不导入作者代码或 SPE 求解器。对9个专门覆盖上述边界的有限目录、14个 owner 分割，核852个合法元组的全部11474个角色割；直接枚举 Bernoulli 替槽的覆盖多项式，再逐系数积分，独立验证 HHYB 差额。另以 Fraction 增广路径分别验证852张 A 图及852张 B 图均送满源量。

[冻结输出](audit_owner_transport_independent.json)为 PASS，含1761个零覆盖 O 客户情形、2370个已覆盖 missing-owner 情形、301个零负载 O 外项。有限核验只检查公式实现与边界；一般性来自上面的全割解析证明。

## 6. 后续实际 G 取消及 SOURCE-NET 的追加核查

原稿后续§5把 B 取实际叶。A 的终点全为 R=O\\C、角色边全为 I=O∩C，故送满 G source 给取消量γ_x∈[0,1]、Σγ=G。若预指定δ_x∈[0,1]且每owner δ_i≤b_i^G，先将这部分源直接送入本owner的对应 R sink；残余任意cut的source与sink容量同减δ(J)，I边不变，原全cut条件保留。因此所有预指定δ可同时扩充为完整γ。这一加强解析通过。

取a_i=|Q_i∩R|、δ_i=min{b_i^G,a_i}，可在本owner内按任意非负客户价格优先取消。角色守恒给

\[
\eta_i=u_i-(\operatorname{out}_f(i)-\operatorname{in}_f(i))
=u_i(I)+\gamma_i\ge0,
\quad\sum_i\eta_i=W.
\]

对剩余ρ_x=1−γ_x，递增捕获流按客户初始量线性。令本role初始源产生的吸收为A_i^src，它只在最优查询T_i上，且A_i^src≤D_i(T_i)。同节点总吸收可精确拆为source与更早role到达两部分，原同一标量w=(A^src+A^in)/D固定分母不变，故对应付款也线性拆开。

若b_i^G≤a_i，则γ_i≥b_i^G，从而η_i≥u_i，本地源成本K_i^src=u_i A_i^src/D_i(T_i)≤u_i≤η_i。若b_i^G>a_i，则本owner全部R被取消，K_i^src=0≤η_i。零分母时无正源吸收，成本取零。所以所有role的SOURCE-NET同时通过；root只是没有更早到达量的特例。它不要求根本身满足IC。

此成本分拆不另领取第二条IC或第二份NET。后续进入量K_i^in是否能共同支付到非负残余η_i−K_i^src，仍未证明。原稿没有把SOURCE-NET当成全部行已付款，范围正确。

## 7. 同叶锚定联合资金的另文核对范围

[锚定联合稿](anchored_owner_transport.md)由shared提出、credible独立重构核对。任意锚集K只得到静态出流资金与捕获资金互不重用；当K是完整最优前缀时，活跃角色全在原σ真实后继中，才可用这些利润购买未来原完整IC。任意旧角色的改枝利润不自动是其IC左端。该适用域区分已同步作者与root；没有额外跨叶结论。
