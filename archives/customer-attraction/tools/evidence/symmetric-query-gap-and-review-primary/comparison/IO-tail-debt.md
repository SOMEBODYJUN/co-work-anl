---
id: full-real-menu-tail-dilution-and-added-slot-credit
kind: lemma
type_tag: 引理
title: 完整真实菜单的逐尾稀释与额外槽信用
status: analytic-identity-valid; cross-position-payment-unproved
summary: "保真实尾动作的C−D望远镜与根额外槽H，当前IC松弛e不能删；FTA二次/全路径混合菜单与个体Mfull域分开，旧381数字仅来源自报，本批实际claim核实后完成清洗，原程序执行0。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/continuation_general/fresh/README.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/continuation_general/menu/README.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/continuation_general/README.md"]
---

# 完整真实菜单的逐尾稀释与额外槽信用

本页为五源完整实读、逐项核真实owner/SHA后的自足正文。原15项IO认领已pushed/synced6ee0cfa438457fb1d930d333113c2295da2d1669，只取本5；此前未认领草稿/暂停记录按原字节另保，未倒改。语义整合、正文推送与done分别记录。源fresh/menu给精确恒等式和未付跨位置预算；旧FTA、copositive及逐对充分条件早在R-486bb9稿，不认作本组新对象。一般六人half未由这些材料闭合。

## 同一真实分支的D、C及逐尾展开

有限单位客户/共同有限非空目录/单位玩家/全部有序历史纯SPE，保空、重复、零客户及任意平局。固定actual合法前缀，负载b，余r人。查询分布p，\(p_x=\Pr_{A\sim p}(x\in A)\)。强制当前A后仍沿同一σ的真实尾\(B_1(A),\ldots,B_{r-1}(A)\)，置a_x=1_A(x)、t_{j,x}=1_(B_j(A))(x)、d_{j-1,x}=Σ_(k<j)t_k、c_x=Σ_jt_j。A与额外查询T独立同分布p，定义

\[
D=\mathbb E_A\sum_x\frac{a_x}{b_x+1+c_x},\qquad
C^+=\mathbb E_{A,T}\sum_{x\in T}\frac1{b_x+1+a_x+c_x}.
\]

源fresh把C^+写C；这里加上标以区别旧“删当前槽”的C^-。D是真实当前强制收益均值，C^+是保当前根、尾及原背景的完整额外query价，没有新增一名真实SPE玩家。

令

\[
T_{tail}=\sum_{j=1}^{r-1}\mathbb E_A\sum_x
\frac{(a_x-p_x)t_{j,x}}
{(b_x+1+d_{j-1,x})(b_x+2+d_{j-1,x})},
\]
\[
H=\mathbb E_A\sum_x
\frac{a_xp_x}{(b_x+1+c_x)(b_x+2+c_x)}\ge0.
\]

则逐客户有

\[
\boxed{C^+-D=T_{tail}-H.}\tag{TAIL}
\]

证明：记g=b_x+1，binary a给单客户差
\((p_x-a_x)/(g+c_x)-a_xp_x/[(g+c_x)(g+c_x+1)]\)。展开
\(1/(g+c_x)=1/g-\sum_jt_{j,x}/[(g+d_{j-1,x})(g+d_{j-1,x}+1)]\)，初始项因E(a_x−p_x)=0消去，正好得到TAIL。分母均正，空行动/零客户不需0/0约定。T_tail有符号，尾动作来自各自真实有序分支，不是独立随机尾或冻结actual尾。

当前actual利润u，SPE给\(e=u-D\ge0\)，因此真实净债

\[
\boxed{C^+-u=T_{tail}-H-e.}\tag{NET}
\]

精确知道逐尾稀释并未给其总符号；额外槽信用H≥0也不自动支付它。删当前槽的\(C^-=\mathbb E_{A,T}\sum_{x\in T}1/(b_x+1+c_x)\)满足C^-−D=T_tail和C^-−C^+=H。额外一槽修正是确定代数，不是新增假设。

## actual全路径的一份W账

全局m玩家，actual位置i强制A后完整终局z_i(A)包含原actual过去、A和真实尾，共恰m槽。定义\(K_i(T,A)=\sum_{x\in T}1/[1+c_x(z_i(A))]\)。这里原过去已计入负载，与上节b写法相同。逐actual位置用p同分布查询/根，得到C_i^+=pᵀK_i p，e_i=u_i−D_i，H_i如上，κ_i=D_i−C_i^-。预算平衡精确给

\[
\boxed{W-\sum_i C_i^+=\sum_i e_i+\sum_i\kappa_i+\sum_i H_i
=\sum_i e_i-\sum_iT_{tail,i}+\sum_iH_i.}\tag{FTA-ID}
\]

旧无额外槽预算只有前两项，已被旧36客户完整SPE反；这不自动反新式，也不因H非负使新式成立。所有信用必须同一个p、同一完整策略和actual路径共同结算。

## 381旧输入复用的真实证明强度

源menu报告原独立程序从381单位客户类型重放43有序历史/258含自身比较，actual(4,1,3)、p=(0,0,17/20,3/20,0,0)，得到

| i | D_i | C_i^+ | D_i−C_i^+ |
|---|---:|---:|---:|
| 1 | 141/10 | 6879/400 | −1239/400 |
| 2 | 141/10 | 5349/400 | 291/400 |
| 3 | 141/10 | 5349/400 | 291/400 |

Σ(D_i−C_i^+)=−657/400。因此原文只反无slack的Σ(D−C^+)≥0，末两位正去相关不自动支付早期债；actual W−ΣC_i^+仍正，没有由此反FTA、Mpath、Mfull、安全值或half。它是旧强推送反例的复用，不是新实例；源说尚未另做独立攻击。

本批没有381原类型/完整动作表闭包，也未取该程序全文；[当前完整菜单资料](../资料/完整真实菜单的条件对偶与旧实例账本--资料.md)同样保旧381为缺输入作者记录。上表按完整MD来源保存，非本次258新IC认证，不与34客户输入/其它循环例混合。五主源均MD、原入口0。

## FTA、个体Mfull和全路径Mpath的可行域

FTA是\(\forall p:\sum_i p^T K_i p\le W\)。它与单个actual节点\(M_{full,i}=\min_{Q\in\Delta(S)}\max_T\mathbb E_{A\sim Q}K_i(T,A)\le u_i\)不同。后者普遍已由[完整银行根列](../反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md)否定，但root单位置反例不否Σ跨位置预算。

旧5308B full_terminal_debt原文还定义更自由的**全路径**菜单：允许Q混合所有(i,A)的z_i(A)完整m槽列，要求共同查询cap≤W/m。对应记号

\[
M_{path}(\sigma)=\min_{Q\in\Delta(\{(i,A)\})}\max_T
\mathbb E_{(i,A)\sim Q}\sum_{x\in T}\frac1{1+c_x(z_i(A))}.
\]

FTA对每p取i均匀/A~p给平均≤W/m，故每p至少一个纯(i,A)查询价≤W/m；有限minimax才给一个共同Q，推出Mpath≤W/m。只对某个真正安全值最优p*有FTA，也足够W≥m v_(m+1)(0)，但不由只一个p*自动得到全部query共同cap。两条充分路线量词分别保留；本批未证/未否该精确Mpath，不把旧OPEN当全仓新认证。

任何z_i(A)都是合法m主题静态竞争列，故Mpath≥v_(m+1)(0)。静态锐比较OPT_m≤2m v_(m+1)(0)可自足证明：任意m静态列分布令均值负载L_x、g(T)=Σ_T1/(1+L_x)、G=max_Tg。最优m元组O的重数d_x给\(1_{d_x>0}\le(d_x+L_x)/(1+L_x)\)，所以OPT≤Σ_jg(T_j)+EΣ_(列主题)g≤2mG；Jensen方向G≤maxquery E真实价，再minimax取最小得界。大小m+1的大主题加m−1个不交singleton给OPT2m，纯大query保证v≥1/allm背景选大保证v≤1，故常数2m锐。这样FTA或上述Mpath界若成立，确可推出half；前提未被恒等式证明。

## 二次型与有限诊断的准确范围

令M_(T,A)=Σ_iK_i(T,A)，FTA等价A=W11ᵀ−(M+Mᵀ)/2在非负正交锥copositive，非普通PSD。对角M_AA≤W由加回当前槽只降价、D节点IC得到。逐对M_AB+M_BA≤2W是充分而非必要条件；两点支持的精确条件为A_aa,A_bb≥0且A_ab+sqrt(A_aa A_bb)≥0，不推广任意多点。source明确FTA/coproduct/pairwise已有R486先例。

本组源报告九份可读完整证书query优化、两组三人形式策略/93有理query/63客户类型重权均无正见证，query值Fraction复算；另一次未存新扫描的pairwise数值max0不作新定理。仅有限域，标签重权可产生同覆盖集合，不以标签数冒不同集合数。不得从这些阴性提升FTA或half。

## 相同覆盖商与两个有序重置

4628B duplicate quotient全文证明：从原σ为每个商有序历史H递归选lift；其规定类代表强制取原σ实际动作，其它类各选一个原alias。偏离类后商续局恰模拟被选alias真实子树，故保SPE/actual覆盖和逐人收益；反向用类固定代表即可lift。不同有序历史仍不同，非计数Markov净化。

同actual位置的商菜单每类只保一原alias列，重复query行原就相同，所以自由Mfull/Mpath移除列只会上升，W/actual收益保；可用于未来自由菜单正分离见证合法化。它不自动保某个原二次FTA坏p，不能未经另证把列子集单调性扩成同p二次型单调。

成对根后(h,A,B)与(h,B,A)是不同有序历史，不能免费同续局；完整额外查询有m+1静态槽，而真前缀插两动作只余r−2真实玩家，删一位必须重算其原续局。原尝试只得到既有账本，未证明新符号。下一付款必须保IC slack与两种有序前缀重置，不能把此恒等式当全局机制。
