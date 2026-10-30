# 坐标初始化后的 I 互补付款与 fresh 剩余

2026-10-24，r2_global_credit。任意人数、任意有限共同目录、每份全部有序历史纯 SPE；空主题、零客户、重复行动和任意历史平局均保留。**Q-CAG-HALF 和原 RESIDUAL-CAP 仍 OPEN。** 本页给一个独立的实际付款接口，随后准确停在 fresh 来源的共同剩余容量。不得把这个扩展直接出口称为原 SAFE 图已实现 RESIDUAL-CAP。

输入采用 [round7 坐标双预算初始化](../../../R-cd789330fc7141299ac491bbb3ffa420/round7/parent/optimal_coordinate_initialization.md)及其 global/coupling 审查。fresh 消元只采用 [round6 的 fresh 利润分母](../../../R-cd789330fc7141299ac491bbb3ffa420/round6/relay/fresh_profit_normalization.md)，不沿用 round5 完整利润分母的旧流。

## 1. 同一初始化与同一两份实际钱包

固定原完整 SPE 的实际叶 \(B\)，实际覆盖 \(C\)，实际利润 \(u_l\)。取任意比较元组 \(T\)，并集 \(O\)，取最优时 \(|O|=\mathrm{OPT}_m\)。置

\[
I=O\cap C,\qquad G=C\setminus O,\qquad R=O\setminus C.
\]

原坐标初始化给每个 \(x\in T_i\)

\[
p_{ix}=1/c_T(x)=P^B_{ix}+c_{ix}+a_{ix},
\qquad c_{ix},a_{ix}\ge0,
\]

其中 \(a_{ix}\) 已按原合法 \(W_i\)-future 正边分到各真实 context，\(c_{ix}\) 是 current 来源标签；当前实际支付

\[
d_i=\sum_xc_{ix}\le u_i.
\]

这笔 \(d_i\) 用第一份 actual \(i\) 整行钱包；标签 \(x\) 不要求属于 \(B_i\)，不能当成 actual 同客户券。

记第一类实际客户券为 \(H_{lx}\)，\(H_l=\sum_xH_{lx}\)，则

\[
0\le H_{lx}\le w_{lx}:=\frac{\mathbf1_{x\in B_l}}{c_B(x)}
\quad(x\in I),
\]

且 \(H\) 只支出在 \(I\) 客户。它使用第二份实际钱包的一部分。对 \(x\notin C\)，\(H_{lx}=0\)，不定义无关零分母。

## 2. 一般实际付款接口：全部 I-future 可绕过续局图

**COORD-I-COMPLEMENT-PAYMENT（本页接口名，非共享 Claim 登记）。** 保持同一个 \(T\)、同一坐标剪枝、原 current \(d_i\) 和原第一类券 \(H_{lx}\) 不动。全部 \(I\) 客户的 future 来源可以用第二份 actual \(I\) 客户券的未花部分直接支付，不调用任何新的 IC。

证明。对每个 \(x\in I\)，令

\[
H_x=\sum_lH_{lx},\qquad C_x^{\rm src}=\sum_i c_{ix},\qquad
A_x^{I}=\sum_i a_{ix}.
\]

由于 \(x\) 的所有比较角色库存之和为1，原同一坐标分割给

\[
1=H_x+C_x^{\rm src}+A_x^I.
\tag{I-INV}
\]

actual 该客户的一份钱包为 \(\sum_lw_{lx}=1\)，因此未花 actual 券

\[
v_{lx}=w_{lx}-H_{lx}\ge0,
\qquad \sum_l v_{lx}=1-H_x\ge A_x^I.
\]

若 \(1-H_x>0\)，取

\[
J_{lx}=\frac{A_x^I}{1-H_x}\,v_{lx}.
\tag{I-PAY}
\]

若 \(1-H_x=0\)，I-INV 强迫 \(A_x^I=0\)，取全部 \(J_{lx}=0\)。于是同一个构造同时满足

\[
\sum_lJ_{lx}=A_x^I,
\qquad 0\le H_{lx}+J_{lx}\le w_{lx}.
\tag{I-CAP}
\]

这是真正的 actual 同客户共同容量，不是给互斥叶各领库存。对全部 \(x\in I\) 同时求和，置 \(J_l=\sum_{x\in I}J_{lx}\)，有

\[
H_l+J_l\le u_l(B;I),
\qquad \sum_lJ_l=\sum_{i,x\in I}a_{ix}.
\tag{I-ROLE}
\]

所以 current 的 \(d_l\le u_l\) 仍仅花第一份整行预算；\(H_l+J_l\) 仅花第二份预算中的 \(I\) 部分。没有第三份 \(W\)。每个实际 \(I\) 客户在第二份预算中的剩余恰为

\[
\sum_l(w_{lx}-H_{lx}-J_{lx})=C_x^{\rm src}.
\tag{I-LEFT}
\]

这不是把 current 来源标签强配给同角色 actual 客户：剩余按 actual 覆盖者分布，标签只确定总额，未规定它必须留在源 current 角色。

**域与接口范围。** 直接 actual 券支付可落在源 owner 之前的实际角色，因为没有调用该过去角色的 IC。它因此不保持原 full-SAFE 路由的源时间下界。它是合法的直接覆盖付款出口，**不是**原 full-SAFE/CLIP 核自动实现的一条边，故不证明原限定路由版本 RESIDUAL-CAP。全部 \(I\) 来源在进入续局重采前被移除，后续不能又传播同一批 \(a_{ix}\)。

root 已逐客户重构本付款；r2_credible 从精确陈述独立重构，通过 I-INV、I-PAY、非负、同一实际券容量及两预算分离，并指出这是与新 \(H\) 坐标的互补接口；未作全仓新颖性认证。与 fresh 核合成亦经其独立核对，见 [合成审查§0](../credible/coordinate_support_attack.md)。不将此内部检查称外审。

## 3. 仅 R 入口接 fresh-利润分母：必须从头重算

删除全部 \(I\) future 来源后，仅将 \(a_{ix}\)、\(x\in R\)，按原 future 子边送入其原真实 prescribed context。正入口有该 \(R\) 客户作见证，故该 context 的 fresh 利润严格正。

对 natural context \(t=(g,j)\)，当前规定动作 \(a=\sigma_j(g)\)，其规定叶为 \(B_t\)，actual-prefix reset query 叶为 \(A_t=\operatorname{finish}_\sigma(B_{<j},a)\)。定义

\[
\nu_t=u_j(B_t;N\setminus C),\quad
D_t^F=u_j(A_t;N\setminus C),\quad
Y_t=u_j(A_t;C),\quad e_t=u_j-u_j(A_t)\ge0.
\]

只在 \(a\setminus C\) 上取既有 fresh 正边 \(q_{t\ell}\)、\(P_t=\sum_\ell q_{t\ell}\)、负项 \(N_t\) 及 diagonal/common 项 \(J_t^{\rm diag},L_t\)。旧全文逐客户给

\[
\nu_t-D_t^F=P_t-N_t,
\qquad \nu_t-P_t=J_t^{\rm diag}+L_t=D_t^F-N_t>0
\tag{NU-LOSS}
\]

（严格号仅用于 \(\nu_t>0\)）。全部 positive recipients 仍是真实未来 prescribed contexts，且由同一 fresh 客户见证其 \(\nu>0\)。所以允许对本批新的 \(R\) 入口重新递推

\[
h_t=b_t+\sum_{s\to t}\beta_s q_{st},\qquad
\beta_t=h_t/\nu_t.
\]

所有 \(h,\beta\) **从头按这批入口与这个分母重算**；不沿用完整利润分母 \(v_t=u_j(B_t)\) 的旧 \(\beta\)、SOURCE 费用或旧 DIAGONAL。DAG 严格向未来，有限。

actual 整行 IC 与 NU-LOSS 同时给

\[
\nu_t-P_t=u_j-Y_t-N_t-e_t>0,
\qquad 0\le Y_t+N_t+e_t\le u_j.
\tag{NU-SAFE}
\]

故可从该 context 同一 \(\beta_t u_j\) gross 整行券安全退 \(\beta_t(Y_t+N_t+e_t)\)，留下非负 actual 整行净券 \(\beta_t(J_t^{\rm diag}+L_t)\)。这项有利的 \(C\) 查询利润 \(Y_t\) **明确退回**，没有把它漏掉，也没有把它视作可重复花的额外 \(I/G\) 库存。

完整 off-history \(C\) 利润 \(X_t\) 没有纳入 \(\nu_t\)，因此这份新流不留下旧 \(v\) 核的 \(+X_t-Y_t\) signed 迁移。若改回完整 \(v\) 分母，必须恢复那笔未付 \(C\) 债，不能沿用本节无正 \(X\) 的结论。

将新净券按 actual 角色合计为 \(K_l\ge0\)，DAG 守恒给

\[
\sum_lK_l=\sum_{i,x\in R}a_{ix}.
\tag{R-MASS}
\]

重采可把 \(R\) 标签换成其它 \(N\setminus C\) 客户，包含 \(O\) 外客户；它只保持**全局 fresh**，不保持原客户标签或 \(R\) 本身。只要不为重采客户另造源，NU-LOSS/SAFE 已包含全部 fresh。这里没有把这种 support 闭合升级成共同实际钱包 cap。

## 4. 真正剩余：同一 fresh 净券必须落在同一两预算余量

新的直接付款接口给精确账

\[
|O|=\sum_l(d_l+H_l+J_l+K_l).
\]

\(I\) future 已由 I-CAP 实际付清；仍须证明某个最优 \(T\)、允许的坐标剪枝、直接券分配及 fresh 路由共同满足

\[
\boxed{K_l\le R_l^F:=2u_l-d_l-H_l-J_l\quad\text{对所有 }l.}
\tag{FRESH-RESIDUAL?}
\]

所有这些量必须取同一次选择。I-ROLE 只给可见余量

\[
R_l^F\ge(u_l-d_l)+u_l(B;G)\ge0,
\]

及 I-LEFT 中那些与 current-I 来源对应的额外 \(I\) 余券；**没有**给 \(K_l\le R_l^F\)。\(\sum K\) 守恒或逐 context NU-SAFE 不能支配同一角色多份净券的和，不能再为它领完整 \(W\)。

本页没有把 FRESH-RESIDUAL 的存在性当作 theorem。它若成立可直接闭合原 HALF；单独消去 \(I\) 来源不推出 HALF，也不保证原限定 full-SAFE 路由的 RESIDUAL-CAP 成立。

## 5. 最优 T 自由匹配：精确依赖与未闭合的交换

固定一个最优主题多重集，只排列其到 actual 角色的匹配。对单个 \(x\in I\)，令

\[
b=c_B(x)>0,\quad t=c_T(x)>0,\quad
h=|\{l:x\in B_l\cap T_l\}|,\quad a_i=\mathbf1_{x\in B_i}.
\]

对 \(x\in T_i\)，原第一正价的行和及剩余可精确写为

\[
P^B_{ix}=\frac{b-h}{t(b+1-a_i)},\qquad
r_{ix}=\frac{h+1-a_i}{t(b+1-a_i)}.
\tag{MATCH-ROW}
\]

而 actual \(l\) 的客户券为

\[
H_{lx}=\mathbf1_{x\in B_l\setminus T_l}
\left(\frac{h}{tb}+\frac{t-h}{t(b+1)}\right).
\tag{MATCH-COL}
\]

这也直接核 I-CAP 使用的 pointwise \(H_{lx}\le1/b\)。

交换 \(T_i,T_j\) 时，\(b,t\) 不动，但

\[
\Delta h=(\mathbf1_{x\in B_i}-\mathbf1_{x\in B_j})
(\mathbf1_{x\in T_j}-\mathbf1_{x\in T_i}).
\]

若 \(k\notin\{i,j\}\) 且 \(x\in T_k\)，它的剩余库存也改变

\[
\Delta r_{kx}=\frac{\Delta h}{t(b+1-a_k)}.
\]

所以不能把匹配视作只改变两行的独立线性 assignment 成本：其它比较角色的库存/行外送阈值也会改变。原 future 正边容量则对固定 \(i,T_i\) 只依赖真实 \(W_i\) 与 actual \(B\)；若把主题移到另一位置，必须在那个 actual 有序前缀上重新取原 \(\sigma\) 的真实 completion，不能把旧未来边重命名搬过去。

对 \(x\in R\)，\(b=h=0\)，\(P^B=0\)、\(r_{ix}=1/t\)；这些 fresh 客户没有 actual 交集 bonus 可供静态匹配交换降价。它们的第一批真实未来捕获仍须由完整后继 IC 支付，不能仅凭某个客户券过载宣称存在改进匹配环。

另已实读旧 `R-a0bb57fa24044a8794bc7991918a19c6/static_matching/optimal_static_matching_counterexample.md`：存在最优元组与匹配使全部冻结偏离和 \(\le W\) 的 FOMA-EXISTS **为假**，完整例 \(W=47,\mathrm{OPT}=52,\min K=48\)。本页没有依赖它，也不把它的失败当作 HALF 或 FRESH-RESIDUAL 的反例。

## 6. 核查与准确交接

本页没有扫描或生成新有限实例。I 互补付款由显式逐客户构造证明，root 和 r2_credible 分别重构确认；它只负责清掉原坐标初始化的 \(I\) future。fresh 核的正性、域与 SAFE 原证明见 round6 relay 全文，合成必须按本页重新算流与同一剩余钱包。

r2_credible 另核初始 fresh 注入域：同一非零初始 context 的首偏离 owner 唯一，同一 \(W_i\) 上初始 \(a_{ijx}\le q^W_{ij}(x)\le1/c_{W_i}(x)\)，故第一次注入甚至满足 \(b_t^R\le\nu_t\)；后续重新合流不继承该系数上界。root 实读 \(\nu\) 正文后确认本页 I+fresh 接合合法。二者均未证明共同列 cap。

未闭合的实质是 FRESH-RESIDUAL。off-history 真 slack \(\ell_t\ge0\) 比较规定动作与原实际主题，但还没有将其共同用于限制同一 actual 角色的多来源 \(\beta\) 净券。MATCH-ROW/COL 只是匹配依赖的精确检查，不计新增一般福利推进；不能以新命名、守恒或静态运输替代这项共同付款。

## 7. 提前整付 I 的 R-only 变形：与旧 INIT/CLIP 去重

root 进一步提出把全部 \(I\) 在初始化之前直接用 actual \(I\) 一份付清。只对 \(R\) 坐标保留库存 \(p_{ix}=1/c_T(x)\)，此时静态中间分母为1，原 \(q_{ix}=(c_{W_i}(x)-1)/c_{W_i}(x)\)。同一正部论证允许当前付 \(d_i^R=\min(r_i^R,u_i)\)，其中 \(r_i^R=\sum_{x\in T_i\cap R}p_{ix}\)，并将 \((r_i^R-u_i)_+\) 沿原 fresh 子边外送。

本分支核对旧 source INIT 与 round6 标量 CLIP 后，确认这个极大 current 数值已经可由它们的合成实现，不另认领新机制。事实上旧按客户均分的初始 current 和 future 为

\[
A_i=\sum_{x\in T_i\cap R}\frac{p_{ix}}{c_{W_i}(x)}\le u_i,
\qquad Q_i=\sum_xp_{ix}\frac{c_{W_i}(x)-1}{c_{W_i}(x)}=r_i^R-A_i.
\]

只需取消旧 future 总量 \(\min\{Q_i,u_i-A_i\}\)，把同量转为当前 actual 整行付款，即得到 \(\min(r_i^R,u_i)\) 和 \((r_i^R-u_i)_+\)。甚至可以保留更强的逐客户子容量

\[
a_{ix}\le p_{ix}\frac{c_{W_i}(x)-1}{c_{W_i}(x)}
\le\min\{p_{ix},q_{ix}\},
\]

原每条 future 边不超过 \(p_{ix}/c_{W_i}(x)\)。这里没有把新的 raw \(q\) 扩张误称为必要；同一最大 current 已由旧输入支持。

旧 SOURCE-NET 还固定 \(G\) 取消、\(I\) 路由 \(f\)、\(\gamma\) 与净收入 \(\eta\)，而这里提前付 \(I\) 并未继承那些共同选择；不能把其已付初始化的好处再叠加。反之，极大 source current 虽是合法选择，也可能占用同角色更早来源的净券余量，故没有证明它支配所有全局路由。可允许 current 与 future 在原非负库存/边容量中共同优化；**不能因此宣称**存在共同 cap。

这一变形的剩余仍是 \(\nu\) 图费用由 \((u_i-d_i^R)+u_i(B;G)\) 支付。没有取得这条一般关系，也不因换一个更短初始化就提高 HALF 状态。I 互补正文保留的实际新增内容仅是与原已付 \(H\) 完全兼容的直接补余接口，不作新颖性或福利改进声明。
