---
id: "customer-attraction/unfiltered-all-tail-mean-cap-collapse"
kind: "lemma"
type_tag: "引理"
title: "释放实际标签且无未来门槛的全尾均值cap塌缩"
status: "proved-exact-domain-and-zero-price-option; no-covariance-payment"
summary: "固定实际前缀、允许全部raw尾及全部进入标签，只约束进入收益均值时，删除槽域恰为过去负载加剩余未来质量的自由目录凸包；可取cap价格零。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round12/credible/cap_extremality_working.md"
---

# 适用域及精确结论

采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)：有限单位客户、有限非空目录\(\mathcal S\)、任意\(m\ge1\)名单位提供者，允许空主题、重复、零客户和任意离轨历史平局。固定完整纯SPE \(\sigma\)、实际前缀\(h_i\)、实际角色\(i\)收益\(u_i\)，记
\[
b_i(x)=\sum_{j<i}\mathbf1_{x\in B_j},\qquad r_i=m-i+1.
\]
当前人被强制进入后，未来尚有\(r_i-1\)个行动槽。

令\(\mathcal Z_i^{\rm raw}\)为延伸\(h_i\)的所有合法终局，允许任意进入主题及任意未来主题，**连原实际行动标签也全部释放**，不要求未来是SPE，也不加任何未来逐叶floor、均值floor或净成本约束。记\(d_i(z)=u_i(z)\)，删除固定角色\(i\)后的负载\(\ell_i(z)=c(z)-\mathbf1_{z_i}\)。只施加归一彩票和进入均值cap：
\[
\mathcal D_i^{\rm raw}=
\{E_q\ell_i(z):q\in\Delta(\mathcal Z_i^{\rm raw}),\ E_qd_i(z)\le u_i\}.
\]

**精确域等式为**
\[
\boxed{\mathcal D_i^{\rm raw}=
b_i+(r_i-1)\operatorname{conv}\{\mathbf1_T:T\in\mathcal S\}.}
\tag{COLLAPSE}
\]
这里凸包表示提供者行动质量，不是客户负载坐标总和。原实际进入收益cap在这个无未来约束的全raw删除负载域中，不再缩小任何负载方向。

# 双包含证明与原完整IC的作用

任意raw叶的删除负载都由固定过去\(b_i\)及\(r_i-1\)个合法未来主题相加。因此其均值属于右端，给出(COLLAPSE)的“\(\subseteq\)”；这一步不使用cap或均衡。

反向固定任意主题\(T\)。在原实际历史强制\(T\)后，原\(\sigma\)给一个真实孩子SPE终局\(z_T^0\)。对每个\(x\in T\)，该终局中当前及未来覆盖者数至多\(r_i\)，故
\[
d_i(z_T^0)\ge\sum_{x\in T}\frac1{b_i(x)+r_i}.
\]
原完整SPE在\(h_i\)的整名玩家IC给
\[
\boxed{u_i\ge d_i(z_T^0)\ge
f_i^{\rm safe}(T):=\sum_{x\in T}\frac1{b_i(x)+r_i}.}
\tag{SAFE}
\]
构造raw叶\(z_T^{\rm copy}\)：进入者选\(T\)，全部\(r_i-1\)个未来槽也选\(T\)。它不必是SPE，但其进入收益恰为\(f_i^{\rm safe}(T)\le u_i\)，所以单点彩票已满足cap；其删除负载为
\[
\ell_i(z_T^{\rm copy})=b_i+(r_i-1)\mathbf1_T.
\]
右端每个目录生成点均可行。由于\(\mathcal D_i^{\rm raw}\)为有限彩票约束域的凸投影，其凸性给整个右端可行，证明“\(\supseteq\)”。没有用逐客户加权IC；逐客户分母下界先合成主题收益，再只使用原玩家一次整IC。

\(r_i=1\)时无未来槽，两端均为\(\{b_i\}\)，证明仍成立。空主题给零收益和相同固定过去，零客户及平局也没有除零或严格比较需求。

# 可以选择零cap价格，但未获得新的库存

固定任意客户shadow \(w\)，负载目标只依赖\(\ell\)。由(COLLAPSE)，
\[
H_i=\max_{L\in\mathcal D_i^{\rm raw}}w\cdot L
=w\cdot b_i+(r_i-1)\max_{T\in\mathcal S}w\cdot\mathbf1_T.
\]
所有raw列的负载本来就在右端，所以cap对偶可取
\[
\mu_i=0,\qquad\eta_i=H_i,
\qquad\eta_i+\mu_i d_i(z)-w\cdot\ell_i(z)\ge0
\quad\text{对所有raw }z.
\]
选一个shadow最大主题的全复制叶即达到\(H_i\)，故这组对偶确为最优。结论是**存在**\(\mu_i=0\)的最优价格，不是所有对偶最优解都必须\(\mu_i=0\)。此放松不能仅靠“进入均值cap”保证额外的正\(\mu_i I_i\)信用；原源约化成本仍可能有值，但那是自由目录shadow差的一部分，不是新cap杠杆。

# 与可信端点、actual-tag冻结及均值门槛的区别

[可信端点三域](可信端点均值cap的三域与松弛信用--引理.md)仅允许每个精确进入历史后的**完整孩子SPE见证**，且实际行动只留原实际端点。其逐叶cap允许独立首次偏离子树拼接；逐行动/全行均值彩票则是分析背景。这里的全复制叶未必满足孩子最佳回复，所以不能把(COLLAPSE)反推到该可信域。

若仍冻结实际标签，只能保证每个\(T\ne B_i\)的全复制raw生成点存在。\(T=B_i\)的全复制叶可能因改了实际尾而被排除；本页不据此断言该冻结域必等于自由凸包，也不把例外忽略。一个具体输入可以恰好仍相等，但需单独核验。

若释放标签却另加[严格未来均值门槛](逐历史均值门槛的受限实际标签域--引理.md)或[统一净成本](规范门槛均值域与复制偏离的精确成本--引理.md)，全复制叶可能违反新增约束。原源仍给非空性，但本页双包含中的反向可行性不再自动成立。因此不能把“无floor全raw塌缩”写成所有raw分析路线不可能，也不能由它删除后续有条件工具。

# cap-extremality稿的其余合同及停界

本源还澄清两点，均与现行三域正文核对：先逐叶删去超cap端点再凸化，不自动给对所有未过滤可信端点有效的单个价格；全行均值cap用**原\(\sigma\)查询源**后，原整IC供\(I_i\ge0\)，其对偶差准确为\(G=\sum_i\mu_iI_i+R\)。大\(\mu_i\)在此乘正松弛，不需另付\(\mu_i u_i\)。这些事实保留CAP-SLACK，但未支付
\[
\operatorname{Cov}\le D+\sum_i(1+\mu_i)I_i+R+
                         (\gamma+Q_{\rm stat})/2.
\]
某可信见证内的真实未来偏离叶，其偏离者不必仍最佳回复，故该叶未必是同一进入历史后的完整孩子SPE端点；不能只凭“真实偏离”给它套可信端点对偶。全raw放松本来为修补这项资格，但本页说明最粗且无floor的版本会失去cap限制。

源3456字节全文已读；原稿记载与tree平行提出均值cap、root澄清原source后修正早期条件查询顾虑。这里只保其历史陈述和完整数学，不新增外审或独立发现。比较原可信菜单、现行三域/门槛/真实流及后续对偶审查，确认无程序源、无扫描或全路线否定。原件和各比较指纹见[证据](../../tools/evidence/cap-extremality-transfer-reviews/README.md)。现行五人half由另证定理成立；本域等式与尚未付协方差均未解决六人目标。关系为原IC保底→raw生成点→精确凸域→零价选项；其他域仅作有条件比较，正式超图留第三阶段。
