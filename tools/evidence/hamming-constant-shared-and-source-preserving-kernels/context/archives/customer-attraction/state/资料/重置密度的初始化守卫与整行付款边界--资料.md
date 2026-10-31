---
id: "customer-attraction/reset-density-initialization-guards-and-whole-row-payment-boundary"
kind: "resource"
type_tag: "资料"
title: "重置密度的初始化守卫与整行付款边界"
status: "exact-version-guards-and-conditional-per-context-payment; common-wallet-open"
summary: "rawround7子边不蕴含rho/c INIT，owner/保强子容量Ronly可接；同客h_x/v_x需一次beta_max整行IC而非逐客IC，任意删边仅流合法，双context例只反纯流到共同系数的推断。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/global_credit_next/README.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/global_credit_next/README.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/global_credit_next/customer_density_reset_invariant.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/global_credit_next/customer_density_reset_invariant.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/parent/reset_density_review.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/parent/reset_density_review.md"]
source_ids: ["025e794ef21c87db36be", "0694ec3291f43b6b5235", "03940d6b0545bb88647f"]
review_status: "三主稿全文及两related原核/坐标正文全文；纯流父审与wholeIC核审查范围分开，当前知情解析非新blind"
truth_status: "INV/INIT/EDGE下逐receiver客户密度已证，合法核下逐context付款条件成立；多context同角色钱包cap与half未由此解决"
---

# 初始化更正是承重条件

[密度定理](../引理/同客重置流的逐接收点密度--引理.md)要求每source/receiver边b≤ρ/c_receiver。原作者初稿过宽援引raw round7坐标子边，后来明确撤回，父审也将更正写入审查域：raw仅有a_kjx≤min(p_kx/(c_Y−1),1/c_Y)，一般不推出a≤p_kx/c_Y。

纯标量校准p1/2,c_Y2,a1/2满足前一上界，却超过p/c=1/4；它只说明这两已列标量约束不蕴含所需guard，**不是**完整CAG/坐标初始化实例或half反例。不能据它声称实际raw round7必产生density>1；准确结论只是本定理不能免费套用。

另一已正式整理的round8 NEW-CAP为min(p,1/δ)/c_W，并另证其初始化可行性；对fresh客户δ1、p≤1恰为p/c_W。它是满足强guard的不同版本，不把此前raw round7自动修成原稿已审版本。owner INIT，以及保旧INIT+CLIP强逐客户子容量的R-only选择和further clipping，都可在核INV/INIT/EDGE后接入。相关12742B坐标稿§7给旧每客户均分current A_i=Σ_(x∈T_i∩R)p_ix/c_Wi、future Q_i=r_i^R−A_i；合法取消future总量min(Q_i,u_i−A_i)转current，可得min(r_i^R,u_i)，同时保每future边≤p_ix/c_Wi。最大current数值不需扩张raw边上限；并非所有仅同总额的分配自动保该逐边guard。

source current消耗角色第一份整行钱包，可能挤压更早source净券余额；合法最大current选择不代表支配所有全局路由。提前整付I也未继承旧SOURCE-NET的G取消、I路由f/γ/η共同选择，不能把两版本好处叠加或多领W。

# 一次max系数整行IC，非逐客户IC

为解释条件付款，另完整实读6755B来源保留核原件§3。对真实context规定a/叶B、actual-reset叶A，x∈a有v_x=1/c_B，D_x=1/c_A，原正/负价总P_x,N_x满足v_x−D_x=P_x−N_x；ell_x=v_x−P_x=D_x−N_x=[1+|J_A∩J_B|]/(c_Ac_B)>0。

同context各origin的同客输入先合h_x，β_x=h_x/v_x，β_*=max_xβ_x。原核按β_x q_jx向正边送同客流，当前L=Σ_xβ_xell_x≥0，Σh=L+Σ正外送。完整SPE只在actual-prefix reset上给**一条整行**IC e=u_i−Σ_(x∈a)D_x≥0，而非每客户D_x≤actual(i,x)。用一次β_*行退款

\[
F=\beta_*u_i-L
=\beta_*e+\sum_x(\beta_*-\beta_x)D_x+\sum_x\beta_xN_x\ge0.
\]

因为L≥0也有F≤β_*u_i，故合法留下L≤β_*u_i。fresh源x不在actual C，没有对应actual物理同客券；传播保x不表示当前吸收也从actual(i,x)付，实际仍用角色整行利润。层蛋糕每层固定X_s={x:β_x≥s}用一次整行IC，总系数恰β_*，不是对每个x另领一份u_i。

若按本密度合同跑原同客核，β_*≤1给L≤u_i。各context均可这样付，却仍可能同一个actual行被许多context重复请求；没有得到总钱包上限。u_i0时含客户的reset主题会给D>0与SPE矛盾，所以合法SPE付款不生正输入的零收益例外；纯流定理本身不需这个IC事实。

# 删边、重采和分母版本不能混用

同客正负同价取消若仍保v−D=P′−N′，原退款公式用N′重算仍合法，且剩同x非终端谱系可有负载严格增性质。密度证明本身不依这个加强，不把它扩到未取消旧核。

任意删正边会减少外送、增加当前吸收，可能破退款非负；EDGE下的density仍真，但wholeIC付款不自动继承。必须用原同客核、同客取消核或另有合法CLIP退款证明，并重算流/费用。新核以h_x/(1/c_B(x))逐客归一，通常不是旧full-v标量h/u_i(B)的纯删边，也不继承后者较小系数/列cap。

固定集合X的标量核h/Σ_(x∈a∩X)v_x只保支持X，不保每origin x；全局fresh分母ν保N\C，但可重采到比较O外fresh客户。两者都不能混进本逐客cut领取更低β系数。源12742B的I互补直接同客支付是另一合法出口，能用actual I未花券清I-future，却不保持原full-SAFE源时间下界；它不自动证明原限定RESIDUAL-CAP或本多context FRESH-RESIDUAL。

# 一个只属纯流域的双context校准

以下是本轮知情解析例，**σ不是SPE**，只检验密度合同到共同系数的逻辑；没有程序运行。m3、客户{x,y}、目录E=∅、X={x}、Y={y}。完整确定策略：根E；第二位在首X后X，其余E；末位在XX后X、在EY后Y，其余E。实际EEE，C空。

source1强制X给Y¹=XXX，ρ₁(x)=1；source2在actual前缀E强制Y给Y²=EYY，ρ₂(y)=1，其他库存0。只向s_x=(XX,3)注x的1/3、向s_y=(EY,3)注y的1/2，其余初始0；均等于各自ρ/c，total≤ρ。两receiver已末位，无EDGE外送，所有INV/INIT/EDGE成立。

c_Bsx(x)=3、c_Bsy(y)=2，所以各β_*=1，但同actual角色3有两个不同contexts，Σβ_*=2。逐客户density/prefix界全成立，不能单从纯流推出角色总系数≤1。本例实际末位E不是BR，因此不能套上节wholeIC付款，也不反驳SPE版共同钱包候选或half；它准确显示还必须使用额外真实IC，而非只重复密度证明。 已有一般密度正式对象另存单客四角色密度和7/6的非SPE诊断；这里三角色双客例只贴合不同客户实现各context max的说明，不认领聚合障碍首次，也没重跑旧诊断。
