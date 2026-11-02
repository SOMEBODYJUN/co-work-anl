---
id: "customer-attraction/background-total-share-induction-interfaces"
kind: "resource"
type_tag: "资料"
title: "背景总份额归纳的两种覆盖量与失效接口"
status: "accounting-proved;union-version-refuted;bare-version-unresolved-here"
summary: "自足保留BG与UNION-BG的不同比较量、两种精确删除缺口、61与11客户局部障碍，并以既有52客户GLOBAL证书更新整体UNION-BG。"
review_level: "source-reconstruction-and-internal-mathematical-check;no-external-review"
scope: "unit-customers;common-catalog;complete-ordered-history-pure-SPE"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2d91ff13b4b44effbe7e78a60470bcc7/direct/background_induction_and_private_root.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-2d91ff13b4b44effbe7e78a60470bcc7/direct/background_induction_and_private_root.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2d91ff13b4b44effbe7e78a60470bcc7/GENERAL_PROOF_WORKING.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-2d91ff13b4b44effbe7e78a60470bcc7/GENERAL_PROOF_WORKING.md"]
---

# 背景总份额归纳的两种覆盖量与失效接口

## 背景不是剩余利润，两个候选也不是同一个式子

在[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)中，固定一个合法过去产生的整数负载b_x，尚有r≥1人按完整子SPE继续，实际后缀负载为c_x。所有主题仍来自同一有限非空目录；比较允许重复，后继遵从原完整策略而非冻结原末位。定义

\[
H=\{x:b_x>0\},\quad A_{new}=\{x:b_x=0,c_x>0\},
\]
\[
V=\sum_{c_x>0}\frac{c_x}{b_x+c_x},\qquad
B=\sum_{b_x>0}\frac{b_x}{b_x+c_x}.
\tag{1}
\]

V是未来玩家总利润；B是固定旧玩家在同一最终叶中的总份额，旧玩家自身不必在当前节点再行动。逐客户守恒为B+V=|H|+|A_new|。分母只在相应正负载项中使用，无0/0。

对任意r个合法比较主题T_j，令O=∪_jT_j。原稿提出的两个全称候选是

\[
\mathrm{BG}:\ |O|\le B+2V
\iff |O\setminus H|\le |A_{new}|+V+|H\setminus O|;
\tag{2}
\]
\[
\mathrm{UNION\!\!\!\!-BG}:\ |H\cup O|\le B+2V
\iff |O\setminus H|\le |A_{new}|+V.
\tag{3}
\]

UNION-BG比BG强，差恰为|H\O|。二者在空背景都回到同人数半覆盖，但一般背景不能删去这项补偿。它们均不同于最大化未来利润的F_r(b)≤2V：F_r(b)的比较对象含客户分母而不是裸并集计数。

二者的r=1边界成立。末位实际主题S，利润u=V。任意合法T满足|T\H|≤Σ_{x∈T}1/(b_x+1)≤u。又B+2V=|H|+|S\H|+u≥|H∪T|≥|T|。零客户、空主题与u=0也被此式覆盖。一般r不能仅由该边界归纳过去。

## 直接删除一个比较主题的精确缺口

设实际首主题S、它在原完整终局的收益u、尾利润V−u。进入**实际孩子**后新旧背景为b+1_S，在同一叶的旧份额是B+u。若对r−1人的BG成立，取O_{−j}=∪_{k≠j}T_k，便有

\[
|O_{-j}|\le B+u+2(V-u)=B+2V-u.
\]

令p_j=|T_j\O_{−j}|，得到

\[
|O|\le B+2V+(p_j-u).\tag{4}
\]

所以min_jp_j≤u足以补缺；它不是SPE条件的直接后果。偏离孩子T_j中的背景份额和尾利润属于另一真实叶，不能换回这里的B,V。即使假设同一个归纳命题，也不能跨孩子保留收益。

原稿定义的PRIVATE-ROOT还把背景限制为空、比较元组限制为真正达到OPT_r，仍是假的。[四人实际根总税完整证书](../反例/四人实际根总税--反例.md)给61名不同单位客户、六共同主题A,B,C,D,E,F，真正最优(A,B,C,D)两两不交，大小(30,10,11,10)，覆盖全部61人。该完整259节点SPE前三位在每个历史选A，末位按真实均分收益最大化，平局F≻E≻D≻C≻B≻A；实际AAAF收益(9,9,9,11)，W=38。因此min_jp_j=10>9=u_root，严格反驳其全称量词。

这里使用已有完整输入、21行早期比较及259节点证明，不冒称本次又独立重跑259节点。此例仍有61<2·38，未否定BG在零背景的目标，更未给主问题反例。

## 保留背景并集后仍是一个局部收费障碍

若对r−1人的UNION-BG成立，在实际孩子得到

\[
|H\cup S\cup O_{-j}|\le B+2V-u.
\]

精确集合差为

\[
q_j=|T_j\setminus(H\cup S\cup O_{-j})|-|S\setminus(H\cup O)|,
\]
\[
|H\cup O|-|H\cup S\cup O_{-j}|=q_j,
\qquad |H\cup O|\le B+2V+(q_j-u).\tag{5}
\]

负项来自实际S在原背景及比较O之外的新覆盖，不能省掉。min_jq_j≤u也是假的，已有[十一客户在轨机会损失证书](../反例/在轨最优补全损失的逐期收费--反例.md)完整证明。其三人五主题完整31节点策略实际AAB，收益(5/2,5/2,3)。取真实首步A作背景H=A、尚余r=2、当前S=A。比较(B,T)在H外各有互不相交的三客户块，因此两种删除q_j都为3，负项为零，均大于当前u=5/2。

这里(B,T)达到的是max|H∪O|=11；不能误称它必须达到不含背景的裸OPT_2。这个局部失败本身没有反驳背景整体预算。事实上此叶B=5/2、V=11/2，B+2V=27/2≥11，所以这一实例满足UNION-BG。它复用了同一δ_i≤u_i收费失败，不能重新命名为未证局部桥。

## 后续GLOBAL证书已否定整体UNION-BG

原稿2026-10-23将两条整体候选都列未证；这是历史状态。由(1)，对全部r主题最大化(3)右侧比较量，恰得到

\[
\max_{T_1,\ldots,T_r}|(T_1\cup\cdots\cup T_r)\setminus H|
\le |A_{new}|+V.\tag{6}
\]

这就是已有[实际前缀新增覆盖GLOBAL反例](../反例/实际前缀的剩余利润与新增覆盖--反例.md)中的O_r(b)≤Δ+P，映射为P=V、Δ=|A_new|。因此整体UNION-BG当前为假；这是同一明确数学对象的代数重述，不能另造一个新52客户反例身份。

该既有证书在六主题A,B,T,Q,R,S、52客户、四名玩家上给全部259个有序节点的完整纯SPE，实际ABAB收益(8,9,8,9)。客户类型按位掩码1,2,4,8,20,24,36,40,49,50的重数分别为10,12,5,5,2,2,2,2,6,6。前缀h=(A,B)合法且在根实际路径；H=A∪B有34人，实际后缀仍A,B，无新客户。旧玩家最终总份额B=17，未来V=17，故B+2V=51。取比较O=T∪Q，18名新客户与H不交，得到

\[
|H\cup O|=52>51=B+2V\quad\text{（严格缺口1）}.\tag{7}
\]

而**同一比较的裸BG**只有|O|=18≤51；更进一步，该52客户目录任意两主题并集最大为34，仍≤51。因此这里没有反驳裸BG。根也有W=34、OPT_4=52、2W−OPT=16>0。不能将非空前缀加强的失败升级成根半覆盖反例。

本批仅重新精确计算该已认证实际路径的背景账与36个有序比较对；不重跑已充分认证的259节点策略。完整策略编码、真实后继和平局依赖见既有反例，其同计数不同顺序可选不同动作。手写两人尾局和嵌入根证书的离轨平局可以不同，不能在未读原动作表时视为同一策略。

## 状态与用途

式(1)—(5)是一般代数/集合关系；r=1边界已证。PRIVATE-ROOT和逐节点min q≤u已由旧真SPE证书否定；整体UNION-BG进一步由后续GLOBAL真根证书否定。裸BG未被这里三例否定，也未在本批得到证明；未从局部删除失败推断它为假。若要继续裸BG，需要利用|H\O|补偿或别的真实跨枝付款，不能继续使用已败局部余量。

[有理自查](../../../../tools/evidence/action-admission-and-background-union-primary/exact-check-report.json)记录(7)及两种候选在同一输入上的数值边界。原稿、当前完整反例和本次代入的身份分别保留；没有外审、全局新颖性或最小规模断言。
