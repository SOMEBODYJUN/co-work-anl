---
id: customer-attraction/admissible-union-menu-independent-reconstruction-and-static-lower-bound
kind: resource
type_tag: 资源
title: 可信全端点菜单的别名复核与静态付款下界
status: exact-representation-and-conditional-sufficiency-proved; ADM-upper-budget-unproved
summary: ADM作者5451B/独审8430B/入口3359B的完整量词；逐端点商、一个有限别名树达到全并集、正确minimax和OPT≤2mM_adm证明，与私有填充全部强制重复cap及有限攻击停止线分开。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/next_general/normal_form/admissible_union_menu.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/next_general/tree_dual/review_admissible_union_menu.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round3_general/menu/README.md
---

# 模型与全部cap合法端点

有限单位客户、有限非空共同主题目录S、m≥1名单位玩家、终局均分；每个有序历史规定纯策略并要求SPE。空主题、重复行动、同覆盖不同标签、零客户、任意离轨平局均保留。固定一份原完整SPE实现的实际经济路径z=(S₁,…,S_m)、actual前缀h_i、最终收益u_i和W=Σu_i。

R(h_i,A)指固定过去h_i及强制当前经济A后，**只要求之后尾玩家是完整子SPE**的全部有序终局。被强制当前玩家不在这个孩子里重新证明A最优。定义
\[
D_{iA}=\{y\in R(h_i,A):d_i(y)\le u_i\},\qquad
D=\bigcup_{i,A}D_{iA}.
\]
每格有限非空：原σ的真实强制孩子给一个见证。实际行动格D_i,Si含z，但也须包括其它低当前收益的可信尾，不能固定为{z}。每个y都含过去、当前及全部后继，恰m个合法经济行动；插入查询的分母是1+c_x(y)，不删当前、不少算一槽。原actual收益和cap u_i不随所选端点改变。

对查询分布p令p_x=Pr_(T~p)[x∈T]，插入值G_p(y)=Σ_xp_x/(1+c_x(y))。对有限非空端点集E记
\[
F(E)=\min_{Q\in\Delta(E)}\max_{T\in S}E_Q ins_T(y),\quad
M_{adm}=F(D).
\]
真正未证的付款候选ADM?是每份可实现z均有M_adm≤W/m。旧包络对经济实际列固定{z}、其它cap完成取MAX描述最不利实现；这里实际列放开、全部端点取有利MIN。不能交换旧包络min/max来证明新候选。

# 一次有限信号扩目录实现全D

统一取L≥1+max_(i,A)|D_iA|，每经济A添加L个完全同覆盖标签(A,0),…,(A,L−1)，actual规定(S_i,0)。在每个actual零标签前缀h_i⁰，将D_iA全部端点分配给非零标签，余标签重复任一端点；A≠S_i的零标签孩子任选该格一个端点，actual零标签继续原actual路径。

每个所贴孩子取旧完整尾SPE见证，未来忽略信号、规定选零标签，并按旧**有序经济历史**执行。任意标签偏离投影为合法经济偏离，故保每个孩子的全部IC。每个非actual标签历史有唯一首偏离位置i与首偏离标签；不同这类孩子两两不交，并覆盖全部非actual历史。经济行动没变但信号非零也是不同孩子，可承接D_i,Si的其它完成。

在actual节点，零规定行动真完成仍给u_i；所有偏离标签按cap至多u_i，所以全部actual IC成立。各贴入子树有自己的完整SPE，因此拼成一棵完整纯SPE。其actual路径菜单的经济端点**恰等于D**：所有列按构造在D中，每个D端点都已装入；内部离轨子树其它端点不是actual路径菜单列，不能额外加入。L开始时一次固定，不依查询p或最终混合Q。

这只是同覆盖纯信号别名，不添加私有客户、不改经济支付；并不要求actual标签fresh。原actual经济主题可重复，仍用零标签表示相同实际路径。

# 反向只需逐端点商

任意有限别名博弈中保经济actual z的完整SPE，在任一actual标签前缀强制(A,ell)后，尾部限制是完整子SPE。固定这个标签前缀，对每个旧经济有序尾历史选一个标签lift；规定经济行动类的代表取原标签策略自己的规定标签，其它类任取代表，沿各选代表递归延伸。

每个经济比较由对应标签节点IC给出；规定分支的经济终局保留，因此得到旧完整尾SPE见证。该强制列y属于R(h_i,A)，原alias actual节点IC又给d_i(y)≤u_i，所以y∈D_iA。这里每列可有不同的旧商策略，**未声称同一旧策略同时保留整张alias菜单**，也不需要这种更强断言。

任意保路径alias菜单E_σ⊆D，扩大最小化方列集合只会降低值，所以F(D)≤F(E_σ)=M_path(σ)。上面的有限L树达到E_σ=D，故
\[
M_{adm}=\min_{\text{finite aliases},\ \sigma\mapsto z}M_{path}(\sigma).
\]
这是真正达到的min，不仅infimum；重复经济查询标签是相同行，重复端点是相同列，均不改变值。

# minimax的量词及双信号边界

有限零和minimax给
\[
F(D)=\max_{p\in\Delta(S)}\min_{y\in D}G_p(y).
\]
因此ADM?精确等价于∀p ∃i,A,y∈D_iA，G_p(y)≤W/m。端点可随p变化；不是先挑一个端点供所有p。双信号可以为固定p装一个所选端点，却不能据此说一棵双信号树装下同格任意多个端点或任意Q的全部支持。统一有限L构造解决的是同时装下全D，不能将逐p存在与一树全实现混同。

# 独审直接证明的静态下界与half充分性

取**任意**支撑于合法m行动终局的背景分布Q，不要求Q自身为静态NE、root菜单或完整SPE分布。令
\[
L_x=E_Qc_x(y),\quad q_A=\frac1m\sum_{j=1}^mPr_Q[y_j=A],
\quad L_x=mq_x,
\]
\[
g(T)=\sum_{x\in T}\frac1{1+L_x},\qquad M=\max_Tg(T).
\]
取任意最优m槽比较题T_j，可重复，客户重数d_x=Σ_j1_(x∈T_j)为整数。d_x≥1时1≤(d_x+L_x)/(1+L_x)。先在比较覆盖上求和、再为L项加非负的覆盖外项，得
\[
OPT_m\le\sum_{j=1}^mg(T_j)+\sum_x\frac{L_x}{1+L_x}
=\sum_{j=1}^mg(T_j)+mE_{A\sim q}g(A)\le2mM.
\]
reciprocal凸性逐客户给g(T)≤E_Qins_T(y)，故对每个合法m槽Q均有
\[
\boxed{OPT_m\le2m\max_TE_Qins_T(y).}
\]
有限D上有达到F(D)的Q，遂得已证下界OPT_m≤2mM_adm。若再证明未证上界ADM?，才得到OPT_m≤2W；表示定理本身不付这个上界。

等价地，真正整数静态安全值v_(m+1)=min_(Q on all legal m-slot backgrounds)max_TE_Qins_T满足v_(m+1)≤M_adm，因为D只是这些合法背景的子集；与OPT_m≤2m v_(m+1)合并同样闭合。这里actual玩家仍m，额外查询是第m+1槽。两个集合限制方向均不反转，不把整数值与自由分数值宣称相等。

m1尾见证为空、L和minimax仍有限合法；零客户/空题/重复与W0都只用弱不等式及分母1+L≥1，不取福利比或0/0。这是原独审给的充分性重构，不是本次新一般福利界。

# 已付末两人界与真正cap缺口

actual末位BR给ins_T(z)≤u_m，因此M_adm≤u_m。倒二位固定同一个过去背景，按p独立取A,A′，各A选一个使当前收益d_A≤u_(m−1)的末位BR B(A)。现有同背景末两人去相关给
\[
E_{A'}G_p(h+A'+B(A'))\le E_{A,A'}U_h(A,B(A'))
\le E_Ad_A\le u_{m-1}.
\]
平均中至少一个cap端点够低，结合minimax得M_adm≤min(u_(m−1),u_m)，只用于m≥2。前部收益可低于这两项，所以它不推出W/m；多个后继使中间背景依A变，不能直接复用同背景去相关。

递归替换更晚尾即使对晚节点合法，可能抬高先前强制者收益而破d_i≤u_i，离开原D_iA。当前没有把这些跨位置丢失cap一次共同付给原W；这只是欠账，不是所有后续方法不可能。

# 入口保存的三类有限尝试

menu原README的程序/JSON只是历史报告，本三源不取未读那些代码或数据，不认证其实现/字段或新run：

| 原方法 | 原文报告的精确范围和停止点 |
|---|---|
| probe_adm.py / adm_discovery.json | 选定actual有序路径，以规范集合值BI取全部尾端点、Fraction筛当前cap、插入矩阵floatLP。若z本身对所有query已cap于W/m直接跳过，因为z∈D；其余仅有限采样。无正分离、无精确反例，非一般ADM保证。 |
| check_seed_family.py / seed_family_discovery.json | 从旧71客户失衡机制添加一个支持主题或改整数重数，欲保早低/末两高及插入失衡；无可用候选，未排某一般构造类，停止扩样。 |
| strict_cone_attack.py / strict_cone_discovery.json | 若完整策略每历史对不同经济行动严格最优，则反向归纳使每尾经济SPE端点唯一，可用其完整actual菜单测试ADM；现root-tax重构的float严格裕量未正，弱IC交替p/客户质量也未分离。无精确对偶、无全锥结论，更非固定人数定理。 |

严格唯一性须在**全部有序历史**逐不同经济行动成立；同覆盖信号标签本就允许平局，不能要求所有alias标签严格。只分离任选一份尾菜单不足以分离全部D；任意非空背景局部预算反例也不等于空根ADM反例。

# 与私有表示、Mfull和当前half的边界

已全文比较[私有别名转移](../定理/私有别名的完整提升与自由分数门槛转移--定理.md)及[等K损失表示](../引理/等大小私有填充的全历史损失游戏与菜单条件--引理.md)。它们加客户、改变支付，不是上述无支付改变的纯信号别名商：

- 私有别名每题加P>D客户，指定提升actual u_i′=P+u_i≥P；强制复制actual前缀已用别名时，全部P+|A|客户已有coverer，任意尾下当前≤(P+D)/2<P≤u_i′。故全部这样的强制重复端点自动cap合法，旧经济收益即使超旧u_i也不能删。
- 等大小K>2D填充的所有actual SPE fresh，u_i≥K−D；强制过去旧题当前≤K/2<K−D≤u_i，所有完整理性尾同样cap。重复格属于全D，私有查询系数从distinct的1/2变成重复的2/3，不能套distinct公式删掉它们。

于是私人表示的自由分数缺口转移不保存ADM；旧经济cap集合不能免费从新D商回。两种填充输出还自动half，不能以它们表述不同的辅助反例反推原half。此对照的私有两正文是在Root告知24AAL待推期间实际读当前R字节，不据文件存在捏造已发表回执。

已读[extra-one边界](../问题/自由extra-one与iid安全值边界--问题.md)：银行已否一般逐人extra-one、Mfull/NQ/全p-WP，不能继续把那些旧OPEN当现状态；它们不自动否有利全端点M_adm≤W/m。现[五人half](../定理/五人半覆盖--定理.md)另证，不回填2026-10-24原OPEN；一般/六人仍未由这三稿闭合。

# 原独审的先验与本次处置

tree_dual原审查明确对象是作者表示、minimax和充分性，“按root本次任务逐量词重新构造”，并另读模型、可信拼合、B10逐历史商证明。它未声称审前不看作者稿；不虚造这三份背景的更细先后。通过的是这些表示/条件结果，不是ADM上界、外审或新颖性认证。本次已读作者/独审和现有数学后的清洗亦非新blind。

作者5451与入口3359此前实际normal/fullread，本次首primary精确reuse，不重复源字节；新独审8430全部六节全文读，原原件保全。作者表示数学此前已由[第三轮完整资源](第三轮总入口与聚合安全值的未付合同--资源.md)展开，本次准确重复路由并接上独审新保全的静态充分性、端点商和原审查边界；入口的具体有限尝试和跳过条件亦独立保全。

7AAK actualfull7claim pushed465ccd…，raw needs-attention与独立3u/2tracked全same、无缺差冲突、stash3621fd…kept分列，其余4claim id不处置。当前0原import/LP/BI/Fraction/IC或新数学程序，亦不重放已有充分旧成功/阴性。来源、实际前置48AAH已pushed字节绑定、逐源收据与[自查证据](../../tools/evidence/admissible-menu-author-independent-review-and-entry-three-primary/README.md)说明历史与当前状态，旧冻结稿不改。
