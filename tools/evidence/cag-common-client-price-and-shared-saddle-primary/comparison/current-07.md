---
id: "customer-attraction/optimal-overlap-complement-payment-and-fresh-residual-interface"
kind: "lemma"
type_tag: "引理"
title: "最优交集客户的互补付款与新鲜余量接口"
status: "I-complement-proved-under-given-coordinate-split; fresh-common-wallet-unproved"
summary: "同一坐标分割下actual交集余券足付I-future；fresh须按ν新分母从头跑，保同次两预算余量、匹配h的跨行依赖与R-only旧INIT去重，不把共同cap升级。"
source_refs:
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/next_general/global_credit/coordinate_residual_attack.md"
---

# 模型、已给输入与结论分层

有限单位客户、有限非空共同主题目录、m≥1名单位提供者、全部有序历史上的完整纯SPE σ，保空主题、重复、零客户和任意离轨平局。固定actual叶B、覆盖C、利润u_l，Σu_l=W=|C|。比较m槽元组T可重复，并集O；取最优时|O|=OPT_m。置I=O∩C，G=C\O，R=O\C。

原源`120210a04f97952e8c88` 12742B全文。这里先把坐标初始化的**已给合同**写清，而非声称已求出最优T或一般共同付款：对x∈T_i给p_ix=1/c_T(x)，同一次非负分割
\[
 p_{ix}=P^B_{ix}+c_{ix}+a_{ix},\quad
 d_i=\sum_xc_{ix}\le u_i.
\]
第一正价P^B已逐客户转成actual券H_lx，只有x∈I时非零，且
\[
 0\le H_{lx}\le w_{lx}:=\mathbf1_{x\in B_l}/c_B(x),\quad
 \sum_lH_{lx}=\sum_iP^B_{ix}.
\]
a_ix已沿初始化允许的真实W_i-future子边分到各原有context；不能把任意同总额的向量冒成合法坐标来源。p只在比较覆盖客户上定义，w只在actual覆盖客户上用，避免零分母。

已证明的是下面I-COMPLEMENT条件付款。后面的FRESH-RESIDUAL是同一次选择上的未证共同余量候选。二者与原full-SAFE/CLIP限定路由的存在性不同，不因新的直接出口而宣布原RESIDUAL-CAP成立。

# I-COMPLEMENT：同一actual客户剩余券足付全部I-future

对每个x∈I，记H_x=Σ_lH_lx，C_x^src=Σ_ic_ix，A_x^I=Σ_ia_ix。比较库存Σ_i p_ix=1给
\[
 1=H_x+C_x^{src}+A_x^I.\tag{I-INV}
\]
actual该客户一份钱包也恰为Σ_lw_lx=1。定义v_lx=w_lx−H_lx≥0；若1−H_x>0，取
\[
 J_{lx}=\frac{A_x^I}{1-H_x}\,v_{lx};
\]
若1−H_x=0，I-INV迫A_x^I=0，取J=0。于是
\[
 \sum_lJ_{lx}=A_x^I,\qquad 0\le H_{lx}+J_{lx}\le w_{lx}.\tag{I-CAP}
\]
这是同一个actual客户、同一份第二预算的联合容量，并非互斥叶各领取库存。对I求和，H_l+J_l≤u_l(B;I)，而剩余客户总券恰C_x^src：
\[
 \sum_l(w_{lx}-H_{lx}-J_{lx})=C_x^{src}.\tag{I-LEFT}
\]
current d_l≤u_l只花第一份整行钱包；H+J只花第二份的I部分，没有第三个W。current的来源标签x不要求actual角色l覆盖x，不能把c_ix自身当physical actual(i,x)券；I-LEFT的余券按actual覆盖者分布，未强制留在原current角色。

直接付J可以落在source owner之前的actual角色，因为没有调用该过去角色的IC。它是合法覆盖付款出口，却不是原SAFE图自动存在的一条边；所有I-future必须在入续局前删去，不能付J后又传播同一a_ix。它兼容已花H，正是此接口相对于“事先另付一份I”的精确内容。

# R-only的fresh利润分母必须新跑

删全部I-future后，只有x∈R的原子边入口进入原真实context。对t=(g,j)，规定动作a=σ_j(g)、规定叶B_t，actual-prefix重置查询叶
\[
 A_t=finish_\sigma(B_{<j},a).
\]
设
\[
 \nu_t=u_j(B_t;N\setminus C),\quad D_t^F=u_j(A_t;N\setminus C),\quad
 Y_t=u_j(A_t;C),\quad e_t=u_j(B)-u_j(A_t)\ge0.
\]
最后一个非负性只用actual位置的一条完整query IC。为不把旧核名词当定义，对x∈a\C，记两叶覆盖角色集合S_A(x)、S_B(x)，a_x=|S_A|、b_x=|S_B|（两者都含角色j，所以均≥1）。每个k∈S_A\S_B的正接收边价为1/(a_x b_x)，每个k∈S_B\S_A的负价也为1/(a_x b_x)。对客户求和得P_t、N_t；q_tk是按接收角色k合并的正价。定义J_t^diag=Σ_x1/(a_x b_x)、L_t=Σ_x(|S_A∩S_B|−1)/(a_x b_x)，均非负。于是D_t^F−N_t=Σ_x|S_A∩S_B|/(a_x b_x)>0，只要ν_t>0；这是当前共同覆盖者带来的严格余量，而非另造正钱包。逐客户相减给
\[
 \nu_t-D_t^F=P_t-N_t,\quad
 \nu_t-P_t=D_t^F-N_t=J_t^{diag}+L_t>0\quad(\nu_t>0).\tag{NU-LOSS}
\]
对同客覆盖集合，分母差的剩余为(1+共同覆盖角色数)/(c_Ac_B)>0，故不是单靠总负载猜正性。

因为fresh客户不在actual C，reset叶的past actual角色不覆盖它；新增正覆盖者只能在j之后，接收点是A_t的真实prescribed context，亦被该客户见证ν>0。所以strict未来角色DAG闭合。h>0时ν>0；零输入/ν0节点直接跳过。按这次R入口**从头**定义
\[
 h_t=b_t+\sum_{s\to t}\beta_sq_{st},\qquad \beta_t=h_t/\nu_t.
\]
ν不是旧完整收益分母v_t，旧β/SOURCE费用/DIAGONAL不能沿用。NU-LOSS和完整IC合并成
\[
 \nu_t-P_t=u_j-Y_t-N_t-e_t>0,\quad
 0\le Y_t+N_t+e_t\le u_j.\tag{NU-SAFE}
\]
因此从同一个β_tu_j gross整行券统一退款β_t(Y_t+N_t+e_t)，留下非负净券β_t(J_t^diag+L_t)。查询中有利的actual-C利润Y_t明确退回，未漏掉也未另花第二份I/G库存。

旧off-history C利润X_t没放进ν，这份新流不带旧full-v核的+X_t−Y_t signed迁移；若换回full-v，必须恢复其未付C债。flow可在N\C内重采到O外客户，只保全局fresh，不保R或每个origin客户；不能为重采客户新造源库存。严格DAG有限，所有质量最终吸收。按actual角色合计新净券K_l≥0，有
\[
 \sum_lK_l=\sum_{i,x\in R}a_{ix}.\tag{R-MASS}
\]
这不是同客密度cut，不借传播客户身份证明钱包cap。

# 尚缺的同次共同余量

另一条在原离轨历史g成立的真松弛可定义为ℓ_t=u_j(B_t)−u_j(finish_σ(g,B_j))≥0，其中B_j是actual原主题；它比较同一g的两个合法行动。没有证明这些跨context松弛能共同支付同角色净券，不能把各行非负当总列上界。

总账精确为
\[
 |O|=\sum_l(d_l+H_l+J_l+K_l).
\]
若能选一个最优T、合法坐标剪枝、I直接券分配及fresh路由，使**同次**所有量满足
\[
 \boxed{K_l\le R_l^F:=2u_l-d_l-H_l-J_l\quad\forall l,}\tag{FRESH-RESIDUAL?}
\]
则得OPT≤2W。但这里只证明
\[
 R_l^F\ge(u_l-d_l)+u_l(B;G)\ge0,
\]
另有I-LEFT的实际余券；没有证明K_l≤R_l^F。每context的NU-SAFE、总质量守恒、甚至初次β≤1，都不支配同角色许多context的净券总和，不能再领一整份W。I为空、R为空或总客户为空均可直接按空和处理，不从退化例推出一般存在性。

# 最优主题匹配不是独立线性assignment成本

固定一个最优主题多重集，只排列到actual位置。对x∈I记b=c_B(x)>0、t=c_T(x)>0、h=|{l:x∈B_l∩T_l}|，a_i=1_(x∈B_i)。逐正价接收actual角色可算
\[
 P^B_{ix}=\frac{b-h}{t(b+1-a_i)},\qquad
 r_{ix}=p_{ix}-P^B_{ix}=\frac{h+1-a_i}{t(b+1-a_i)}.\tag{MATCH-ROW}
\]
每个actual接收者l∈B_x\T_x从h个actual同客source各收1/(tb)，从t−h个非actual source各收1/[t(b+1)]，故
\[
 H_{lx}=\mathbf1_{x\in B_l\setminus T_l}
 \left(\frac{h}{tb}+\frac{t-h}{t(b+1)}\right)\le1/b.\tag{MATCH-COL}
\]
交换T_i,T_j时，b,t固定而
\[
 \Delta h=(\mathbf1_{x\in B_i}-\mathbf1_{x\in B_j})
 (\mathbf1_{x\in T_j}-\mathbf1_{x\in T_i}).
\]
任何k≠i,j且x∈T_k的余库存也改变`Δr_kx=Δh/[t(b+1−a_k)]`。因此不只是两行成本改变。把某主题搬到另一actual位置，还要在该新有序prefix上重新取原σ的真实W_i，不能给旧future边重命名。

x∈R时b=h0、P^B0、r_ix=1/t，没有actual交集bonus；不能只因一个客户券过载就断言有改善匹配环。源引用旧FOMA-EXISTS的W47/OPT52/min frozen K48作为另一个已失败静态接口；本证明不依它，也不把那个失败当FRESH-RESIDUAL或half反例。

# 提前整付I的R-only变形与旧INIT去重

若事先把全部I直接用第二actual-I钱包付清，只保R坐标库存p_ix，则旧INIT给
\[
 A_i=\sum_{x\in T_i\cap R}\frac{p_{ix}}{c_{W_i}(x)}\le u_i,\quad
 Q_i=\sum_xp_{ix}\frac{c_{W_i}(x)-1}{c_{W_i}(x)}=r_i^R-A_i.
\]
A_i≤u_i用p_ix≤1、非负性及一次完整query IC，绝非逐客户IC。合法取消future总量min(Q_i,u_i−A_i)，转成current后，恰得
\[
 d_i^R=\min(r_i^R,u_i),\quad future=(r_i^R-u_i)_+.
\]
每条旧future子边仍≤p_ix/c_Wi，同客总量仍≤p_ix(c_Wi−1)/c_Wi。因此这个数值上的极大current已由旧INIT+CLIP可实现，不认新机制；raw round7只有较弱子边上限时不免费继承这个强guard，见[初始化/整行付款边界](../资料/重置密度的初始化守卫与整行付款边界--资料.md)。

同一非零初始context的首次偏离owner唯一，原弱每客户子边≤1/c_W亦可给第一次注入b_t^R≤ν_t；**不是**之后合流β的永久上限，也不是强ρ/c密度定理的全部INIT假设。最大current可能占用更早source的角色余量，未证支配所有全局路由。提前I未继承旧SOURCE-NET的G取消、I路由f/γ/η共同选择，不能同时拿两版本好处；真正残余仍是新ν费用由同一次余钱包支付。

# 证据与当前用途

本页是原MD所有七节的自足数学保全，包括与旧最大current的准确去重、MATCH跨行依赖和原内部解析核查读序；没有原程序/新数值扫描。旁读[同客父审范围](../审查/同客重置父审的纯流范围与核版本--审查.md)的wholeIC βmax核与本ν重采流不是同一接口。这里未证明原RESIDUAL-CAP、FRESH-RESIDUAL或一般half；现五人half另证成立亦不自动给此路由共同cap，恰六人未由本接口解决。无外审或全球新颖性认证。
