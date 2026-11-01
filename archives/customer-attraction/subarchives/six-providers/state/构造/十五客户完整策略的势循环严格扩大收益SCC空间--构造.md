---
id: "customer-attraction/fifteen-customer-SPE-potential-circulation-strict-SCC-expansion"
kind: "construction"
type_tag: "构造"
title: "十五客户完整策略的势循环严格扩大收益SCC空间"
status: "proved-complete-pure-SPE-and-strict-inclusion;not-half-counterexample"
review_level: "primary-independent-review-full-read;required-discovery-originals-compared;informed-analytic-reconstruction;no-current-math-rerun"
summary: "三主题15单位客户完整13历史策略，39真实比较均非负；四行逐类型零和，根行AB坐标不在唯一非平凡SCC的一维像空间，严格扩张但不求完整维数。"
cleanup_primary_ids: ["9e3fb9dac56e91215d76", "1c9328ee2dd9c1421567", "76307e651db964a863ac"]
legacy_ids: ["LC-SCC-STRICT-v1"]
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/independent_review/lattice_review.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/independent_review/lattice_review.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/independent_review/lattice_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/independent_review/lattice_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/independent_review/lattice_review.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/independent_review/lattice_review.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/full_tree/count_lattice_circulation.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/full_tree/count_lattice_circulation.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/full_tree/audit_lattice_circulation.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/full_tree/audit_lattice_circulation.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/full_tree/lattice_circulation_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/full_tree/lattice_circulation_audit.json"
---

# 十五客户完整策略的势循环严格扩大收益SCC空间

## 单位客户、全部策略与实际福利

三名单位权提供者，按顺序从共同目录{A,B,C}各选一次，观察全部有序历史。七个非空兴趣类型按(A,B,AB,C,AC,BC,ABC)排列，重数

\[
w=(3,2,3,2,3,1,1).
\]

每份重数表示不同单位客户，总15名；三标签均有正私有客户，覆盖两两不同，不是把相同覆盖标签当不同主题。重复行动保留。构造只证存在这份完整纯SPE，不声称所有平局产生相同实际路径。

根选A；第二人见A、B、C后分别选C、A、A。末位全部九历史的规定动作是：

| 第一 / 第二 | A | B | C |
|---|---|---|---|
| A | C | A | A |
| B | A | A | A |
| C | B | A | A |

连根和三个第二层节点共13个有序决策历史；不是匿名计数策略替代全部历史。实际路径ACA，总计数q₁=(2,0,1)。两个选A者各得

\[
3/2+3/2+3/3+1/3=13/3;
\]

选C者得2+3/3+1+1/3=13/3。因此W=13，恰漏B私有两客户。选择A,B,C覆盖全部15客户，故OPT₃=15，且2W−OPT₃=11>0。本例严格扩张付款空间，不是half反例，更不是直接的六人实例。

## 全部39项真实比较的有限解析证书

记Zσ(h)为给定历史后沿上表真实完成，角色i=|h|+1。对每个h、每个b∈{A,B,C}，真实松弛

\[
\delta_{h,b}=u_i(Z_\sigma(h))-u_i(Z_\sigma(h,b))
=\sum_{D\ne\varnothing}w_D\,[F_{q,a}(D)-F_{q',b}(D)],
\]

其中a是h的规定动作，q,q′从同一表完成获得；F的定义与正分母见[势配平引理](../引理/两层计数势端点配平的真实行双向支付--引理.md)。下表逐行列完13×3项（含自身），是冻结发现证书完整39值的无损重排；每项均可按上式直接复核，并非新程序运行结果。

| 历史h | 改A松弛 | 改B松弛 | 改C松弛 |
|---|---:|---:|---:|
| ∅ | 0 | 0 | 0 |
| A | 0 | 0 | 0 |
| B | 0 | 3/2 | 0 |
| C | 0 | 2 | 7/2 |
| AA | 1 | 0 | 0 |
| AB | 0 | 3/2 | 0 |
| AC | 0 | 0 | 3/2 |
| BA | 0 | 3/2 | 0 |
| BB | 0 | 5 | 5/3 |
| BC | 0 | 19/6 | 19/6 |
| CA | 0 | 0 | 3/2 |
| CB | 0 | 19/6 | 19/6 |
| CC | 0 | 5/3 | 5 |

所有值非负，故每个有序子博弈当前规定行动相对全部合法动作均最优。每人只在自己的层移动一次，完整策略于是为纯SPE。最小松弛零；根三个行动、若干离轨行动确有平局，不能改写为严格唯一均衡。有限39项证书只认证这一个固定输入，不承担普遍机制的所有m,p量词。

## 四条原真实行与势端点平衡

以下所有行均指同一完整策略；按七兴趣类型顺序：

\[
\begin{aligned}
g_0=\Gamma_{\varnothing,B}&=(1/2,-1,1/6,0,1/3,-1,0),\\
g_1=\Gamma_{A,A}&=(-1/2,0,-1/2,1,0,1,0),\\
g_2=\Gamma_{B,C}&=(1/2,0,1/3,-1,0,-1/2,0),\\
g_3=\Gamma_{CA,A}&=(-1/2,1,0,0,-1/3,1/2,0).
\end{aligned}
\]

设q₂=(2,1,0)、q₃=(1,1,1)。逐个真实完成对应为：

| 行 | 规定完成与当前行动 | 偏离完成与当前行动 |
|---|---|---|
| g₀：根改B | ACA，A，q₁ | BAA，B，q₂ |
| g₁：A后改A | ACA，C，q₁ | AAC，A，q₁ |
| g₂：B后改C | BAA，A，q₂ | BCA，C，q₃ |
| g₃：CA后改A | CAB，B，q₃ | CAA，A，q₁ |

所以g₀=F_{q₁,A}−F_{q₂,B}，g₁=F_{q₁,C}−F_{q₁,A}，g₂=F_{q₂,A}−F_{q₃,C}，g₃=F_{q₃,B}−F_{q₁,A}，且

\[
g_0+g_1+g_2+g_3=0\quad\text{逐类型恒成立}.\tag{4}
\]

每行在w上也取零。其总和重排为

\[
[F_{q_1,C}-F_{q_1,A}]+[F_{q_2,A}-F_{q_2,B}]+[F_{q_3,B}-F_{q_3,C}],
\]

正是势配平引理取背景r=e_A、三角标签顺序(C,A,B)的六边源。因此所有未映射势端点精确配平，λ₀=λ₁=λ₂=λ₃=1合法；收益顶点本身却未净流配平。由(4)，−g₀=g₁+g₂+g₃，故根行的负向能由三条原真实行非负支付。

## 完整收益图的十八端点与唯一非平凡SCC

收益顶点(q,a)中的q是终局计数，不是当前历史计数；真实边从偏离端点指向规定端点。下面以三位计数串q_Aq_Bq_C:a表示顶点，列出由全部39比较合并所得邻接，省略所有自环与重复边。该表可直接由13动作表的真实完成逐项获得，不用把程序的SCC断言当唯一理由。

| 收益顶点 | 非自环后继 |
|---|---|
| 300:A | 201:C |
| 210:A | ∅ |
| 210:B | 201:A，201:C |
| 201:A | 201:C，111:B |
| 201:C | ∅ |
| 120:A | ∅ |
| 120:B | 210:A |
| 111:A | ∅ |
| 111:B | 201:A，111:A |
| 111:C | 201:A，210:A |
| 102:A | ∅ |
| 102:C | 201:A，111:A，111:B |
| 030:B | 120:A |
| 021:B | 111:A |
| 021:C | 120:A |
| 012:B | 102:A |
| 012:C | 111:A |
| 003:C | 102:A |

201:A与111:B互相可达，外出仅达汇点201:C或111:A；其余非汇点只指向汇点或这两个顶点，且没有回到自身的非平凡路径。因此唯一非单点SCC恰为{((2,0,1),A),((1,1,1),B)}。其收益像空间是span{F_{q₃,B}−F_{q₁,A}}=span{g₃}；g₃的A坐标−1/2非零，故维数恰一。

但g₀的AB坐标1/6，而g₃的AB坐标零，所以g₀不在旧SCC像空间。g₀本身是原非负行锥C=cone{Γ}的生成行，(4)又给−g₀∈C，因此g₀∈C∩(−C)。结合[一般包含](../引理/两层计数势端点配平的真实行双向支付--引理.md)，得到旧SCC像空间严格包含于完整真实行锥的lineality，至少新增一个独立方向。

本页不声称完整lineality精确维数等于二；“SCC空间秩1、加入根行秩2”只给严格扩张见证。也不称势端点循环已穷尽所有双向方向。

## 原独立审查、发现工具和接续边界

2948B原审稿独立重建差分后读发现稿，再跟随四个真实节点核上述端点及逐类型行；4138B独立实现以Floyd–Warshall闭包区别于发现审计逐节点DFS，940B冻结报告给同一非平凡SCC、四行、13/39和W13/OPT15。实际代码/JSON范围详见[独立Floyd审查资源](../审查/计数势格循环的独立Floyd审计与冻结证据--审查.md)；本次不重复已成功有限原程序、未造新运行日志。

两个浮点发现探针仅提供候选来源，见[两种发现探针](../程序/真实行锥额外双向空间的两种发现探针--程序.md)。相关原稿称distinct探针seed840013、trial29找到本例，这是母稿历史而非本次运行；二主题先前候选迫同覆盖，不承担本页三主题两两不同覆盖的结论。probe程序是否精确后验、上限与实际字段按其自己的资源对象判断，不借本页实现认证全部搜索。

本例适用于一般全树付款机制，但不因归在六人子档就改成六人SPE，也不能无证明加dummy提供者迁移。一般half仍需任意真实σ上对实际与比较覆盖共同寻找非负行组合和逐类型非负余项。额外有符号自由度本身不提供这一全称付款。

来源：主独立审稿及三required-related发现稿/代码/全slack JSON均全文实读；本页完整保策略、客户、39比较、四行、十八端点、严格性及状态。原新颖性和外审未认证；源ref与版本见frontmatter。
