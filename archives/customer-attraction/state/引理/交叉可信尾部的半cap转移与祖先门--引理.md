---
id: "customer-attraction/cross-history-credible-tail-half-cap-transfer-and-ancestor-gate"
kind: "lemma"
type_tag: "引理"
title: "交叉可信尾部的半cap转移与祖先最佳回复门"
status: "proved-local-transfer-and-ic-upper-bound; credible-domain-closure-unproved"
summary: "同计数交叉孩子可移植固定尾部SPE，半半混合保负载而使根cap增加根与当前利润和的半差；父节点及中间IC仍需核验，不能免费引用可信端点对偶。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round12/geometry/cross_history_mean_cap_transfer.md"
---

# 同计数孩子与可移植的尾部

采用[有限单位客户、共同非空目录与完整历史纯SPE模型](../定义/共同目录完整历史模型--定义.md)，任意人数、合法有序前缀\(h\)、空/重复主题、零客户和任意离轨平局。固定进入角色\(i\)、更晚当前角色\(j\)、同一有序中间序列\(z\)及主题\(A,A'\)。两处固定孩子历史
\[
g_1=(h,A,z,A'),\qquad g_2=(h,A',z,A)
\]
在角色\(j\)行动后已有相同客户负载和相同剩余人数。

给定\(g_1\)后的一份完整尾部SPE \(\tau\)，可在\(g_2\)的每个后缀历史使用相同后缀动作。两处过去计数相同，故每个未来真实偏离及规定完成的收益相同，移植后仍是完整**尾部**SPE。这不要求原给定\(\sigma\)在两处采用同尾，也不说明将当前强制行动重新变成最佳回复。

取原\(\sigma\)两份真实cross-child尾\(\tau_1,\tau_2\)。原两叶
\[
y_1=(h,A,z,A',\tau_1),\qquad
y_2=(h,A',z,A,\tau_2)
\]
中进入者/当前角色利润分别为\((r_1,c_1)\)、\((r_2,c_2)\)。对同一固定尾，交换两根主题只交换这两人的完整终局收益；固定中间及尾角色的收益不变。

# 对称混合的确切半差额

仅在端点凸组合中，让两处各一半用\(\tau_1\)、一半用\(\tau_2\)。新根利润和与当前利润和均为
\[
R_{\rm sym}=C_{\rm sym}=\frac{r_1+r_2+c_1+c_2}{2}.
\]
因此根进入cap合计变化准确为
\[
\boxed{R_{\rm sym}-(r_1+r_2)
=\frac{c_1+c_2-r_1-r_2}{2}.}
\tag{TRANSFER}
\]
完整负载分布合计仍为两尾各一份，任何完整负载shadow总和保持。删除固定进入角色\(i\)时，两处根主题仍是\(A,A'\)各一份，所以其删除槽shadow总和也保持。根获得的利润转移同时从当前角色利润中扣去，不能给两人各保一份。

令\(v_1,v_2\)为原\(\sigma\)在\((h,A,z)\)、\((h,A',z)\)两处的当前规定收益。原完整IC只在它们自己的真实分支上给
\[
c_1\le v_1,\qquad c_2\le v_2.
\]
故
\[
\boxed{R_{\rm sym}-(r_1+r_2)
\le\frac{v_1+v_2-r_1-r_2}{2}.}
\tag{IC-TRANSFER}
\]
\(v_1,v_2\)是跨根分支值，不是原实际路径同名角色的\(u_j\)。若\(v_1+v_2\le r_1+r_2\)，操作不增加合计根cap；没有这个条件时，正半差额仍未付。

# 尾部SPE资格不等于完整孩子SPE资格

每个\(\tau\)在固定当前动作之后确实可信，但改变尾会改变当前角色遵循原规定行动的收益，也可能改变其其他行动的比较；因此当前角色不必仍愿意选原动作。中间\(z\)角色与更早祖先的收益和IC也可能改变。根cap不增与负载shadow合计保持，都没有替代这些逐节点条件。

准确的无承诺门槛为
\[
M(g)=\max_T\min_{v\in\mathcal R(g,T)}u_{|g|+1}(v).
\]
完整路径\(y\)是某份孩子SPE端点，当且仅当其每个后缀角色满足\(u_k(y)\ge M(y_{<k})\)，证明为节点IC必要性和离轨兄弟的独立最小孩子拼接，见[受限标签门槛页](逐历史均值门槛的受限实际标签域--引理.md)。若还需保持祖先的终局收益上限或别的承诺，就必须在同一个受约束域中检查；无承诺\(M\)不能免费替代它。

旧[相邻可信换位稿](../../tools/evidence/cap-extremality-transfer-reviews/original/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round6/global/credible_adjacent_transposition.md)已给最短的具体门：在固定前缀\(h\)，一份\((A,B,\tau)\)叶的首两利润为\(\alpha,\beta\)，尾部本来可信，则
\[
(A,B,\tau)\text{可补成完整SPE}
\iff\alpha\ge M(h),\ \beta\ge M(h,A),
\]
而交换后的准确条件是
\[
(B,A,\tau)\text{可补成完整SPE}
\iff\beta\ge M(h),\ \alpha\ge M(h,B).
\]
即使同计数保证尾可移植，新的第二节点仍可能因\(M(h,B)>\alpha\)被挡住。更长交叉中还需所有中间节点的对应条件。本页混合不是该完整可信域自动具备的对称闭包，因此不能直接引用只覆盖完整孩子SPE端点的全行mean-cap对偶。

若能证明这项资格门及所需原实际标签约束，原cap乘子\(\mu_i\)才可合法给(TRANSFER)定价；随后还须支付半差额总量并控制原源概率容量。没有证明源银行可逐pair重复使用，也没有joint endpoint descent。

# 与raw均值floor及NET整差额的准确比较

[均值floor放松](逐历史均值门槛的受限实际标签域--引理.md)把部分不可信重置叶纳入允许raw列，但显式收费所有受影响祖先floor，且实际标签改尾仍有例外。全raw统一NET域又是另一个域：令
\[
B_i=d_i+\sum_{k>i}(M-u_k)=2d_i-\sum_{k\ge i}u_k+\sum_{k>i}M.
\]
上述混合保合计剩余利润及规范门槛和，根利润增半差额，所以其NET变化是
\[
\Delta\sum_{\rm pair}B_i=c_1+c_2-r_1-r_2,
\]
为本页根cap半差额的两倍。完整证明在[交叉NET对称化](交叉有序历史的均匀净成本对称化--引理.md)。raw取消父节点可信资格门后仍保这份有符号成本，不能把旧半差额与新NET对偶拼成免费可行变换。

# 来源、审查与停界

主源2719字节全文实读，旧相邻换位8016字节作为比较全文实读；后者有自己的缺陷/极端坏点结构，本批不额外认领其全部独有内容。本源原文记tree从定义内部核TRANSFER及IC上界，并指出父/中间门；这是局部代数与范围检查，不是合法全端点变换认证。本批无程序源、无finite scan、无外审或新颖性认领。原稿本来声明同计数移植是旧工具，保留这一归属。

公式对五人不改系数，却未给\(W\ge(9\gamma-Q_{\rm stat})/2\)；现行五人定理由别证完成。六人或一般half亦未由该局部关系闭合。原字节及比较见[资源](../../tools/evidence/cap-extremality-transfer-reviews/README.md)。关系是同计数游戏同构→尾移植、完整IC→局部半差额上界、门槛→完整孩子资格条件；没有从局部代数到全局付款的无条件边，正式超图留第三阶段。
