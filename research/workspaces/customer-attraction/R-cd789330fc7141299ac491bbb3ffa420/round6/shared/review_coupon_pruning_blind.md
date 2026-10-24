# 全客户 coupon 净化与最大 scalar 剪枝：按陈述的独立重构

2026-10-24，shared。先读恢复出的round5广播/密度账，再收到credible提出的新陈述（其中含关键公式与论证提示）；第1—5节在读取其round6新正文前写成，不称完全未获作者推导提示的严格盲审。随后对照[作者正文](../credible/safe_coupon_netting.md)§1—4一致，第6节另记录fresh-only对稿核查。核查范围是全输入局部净化、原IC域和剪枝，不是coupon全局cap或一般half。**以下明示代数通过；Q-CAG-HALF仍OPEN。**

## 1. 固定同一个 natural context 的原账

记规定完成叶上的当前利润为v；同一合法动作a在原actual-prefix下的reset收益为D；原实际当前利润为u。完整原IC给D≤u，设e=u−D≥0。round5全客户计数账给

\[
v=u+P-F,\quad F=N+e,\quad 0\le N\le D,
\quad0\le F\le u.
\]

P是全部正recipient边（future真context与past actual-coupon终点）的利润总额。另有D−N=J^{all}+L^{all}≥0。所有这些量均来自同一context，不跨互斥叶先加账。

当前raw actual-row券为βu，分在每个原实际(i,x)份额上，系数均为β。可对这些券统一退系数

\[
r=\beta F/u\le\beta,
\]

留下非负的整行系数

\[
\kappa^{row}=\beta(D-N)/u
=\beta(J^{all}+L^{all})/u\ge0.
\]

其净金额为β(D−N)。这正好把原signed ledger已有的−βN−βe同时与本context的βu相消。past正券仍保持原(j,x)标签；没有把某个旧负q^-强配给不对应的实际客户。

统一退整行券是同一实际利润的标量分解，不是对原IC按客户重权。它不能解释为“退掉e后，剩下的券仍单独支付整份βD”；被支付的是原ledger中已经减掉N后的净项。若u=0，则D=N=e=0；非空正利润context不可能，所有零项按零处理，不除0。

## 2. 可选最大 scalar 剪枝

在本context任选总量0≤c≤min(P,F)，从原正recipient边删除这么多利润容量，设P'=P−c、F'=F−c。逐客户选哪些正边不影响以下scalar身份：

\[
v=(u-F+c)+(P-c).
\]

因为0≤F≤u且c≤F，新的当前row净金额u−F+c仍在[0,u]，所有剩余正边仍有合法原recipient域。最大选择c=min(P,F)给

\[
P'=(v-u)_+,\qquad u-F+c=\min(v,u).
\]

因此仅在off-history利润v>原actual利润u时保留正传播。v≤u时该context可全部转为当前实际row券；v>u时当前row净支付u，剩余v−u仍从原正边子容量广播。

这里没有调用off-history回actual动作的额外slack非负；只用原全客户计数身份及actual节点完整IC的D≤u。

## 3. 局部最少外送与重算传播

固定归一化β=h/v，要求current actual券系数不超过β。任何守恒的正路由都有current金额l≤βu，所以非当前外送至少

\[
h-l\ge(h-\beta u)_+=\beta(v-u)_+.
\]

CLIP取l=min(h,βu)并保留所需总量的原正边，达到该下界。可行性由v−u=P−F及F≥0给出。这里只是本context局部最少外送，不是全局最优。

保留原规定利润v作为分母、初始注入b不变，所有future正边变为原边子容量，所以按严格角色DAG重算后β'≤β。past正边也只是原actual券出口的子容量。

**不能声称所有净券逐坐标下降。** 在同一β下，新current净额u−F+c比旧net u−F增加；β'下降不自动给新net≤旧net。成立的是新current净系数≤新raw β'≤旧raw β，而past正出口逐项β'q'≤βq。因此对每个原actual(j,x)，新正coupon load不超过旧gross load（源初常数不变时一起加入）；不是不超过旧net load。

## 4. controlled positive coupon LP

保留每条原正recipient边的客户/历史标签，令实际发送量f≥0，容量f≤βq。只把future边送入后继natural context，past边仍是actual(j,x)终点。令

\[
h=\beta v=b+\text{future incoming},\qquad
l=h-\sum_{all\ out}f.
\]

写取消总额c=βP−Σf，则l=β(u−F)+c。因此

\[
\beta(D-N)\le l\le\beta u
\]

与0≤c≤βF等价，且Σf≥0又给c≤βP。这是对原净化/剪枝自由的准确线性描述；past出口金额转为coupon系数时仍乘原c_Z(x)，current系数是l/u。所有原IC和正边域不变。

此系统没有自行给任一coupon cap可行；MAX-CLIP把l取到min(h,βu)，只在当前context最少外送，不保证跨context容量最优。

## 5. 与本轮 TOTAL-TRIM 的边界

TOTAL-TRIM可以任意删G单位R源，使剩源量OPT−W；这些删源不是actual Hall取消，不提供η或SOURCE-NET。局部净化与剪枝可对其余合法context使用，但必须重算同一源下的β与所有current/past券。

全图的current净额加保留正出口仍等于规定利润v，故利润注入质量守恒。净化把signed退款改成全非负coupon表示，不自行创造实际福利或总费用下降。

尚缺的是：共同选择源、owner、trim及路由后，证明这份全非负actual券需求在原W内。本文没有该全局上界；不把局部非负性或传播停止条件当作half付款。

## 6. fresh-only 变体的追加对稿核查

作者§5的ν为同一规定动作的fresh利润，D_F为actual-reset的fresh利润、Y为其C利润。恢复出的fresh LOSS给ν−P=D_F−N，而原actual IC给u=D_F+Y+e。因此

\[
\nu-P=u-Y-N-e,\qquad0\le Y+N+e\le u.
\]

同一整行安全退款与scalar剪枝可用，最大剪枝只保留(ν−u)_+。正fresh recipient确是未来真实context，接收者含该fresh客户而其ν>0，DAG闭合。仅fresh源才能注入该图；不能把包含C的source利润当作fresh源。ν≤v使相同注入下的β=h/ν可能较大，因此fresh-only不自动比full图费用或load更低。以上对稿范围通过，未额外证明共同cap。
