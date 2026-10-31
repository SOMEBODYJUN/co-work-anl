---
id: "customer-attraction/heterogeneous-EJ-dictionary-all-price-menus-and-exact-budget-optimum"
kind: "theorem"
type_tag: "定理"
title: "异质EJ字典的全半轴菜单与精确最优预算"
status: "proved-V-shape-optimum3-old7over2-and-all-integer-copy-exits; budget-not-welfare"
summary: "E三个单客户资源/J两个双客户资源的完整H保末位非BR强制项，固定网格{0,1}给F(x)=3+(3/2)|x−2/3|；E2J1真M(2,3)/目标(2,2,4)/B6+C3=9，非half负种子。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round7_general/root/pooled_dictionary_seed_lp.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round7_general/convex/pooled_dictionary_lp_independent_review.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round7_general/CLAIMS.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round7_general/EVIDENCE.md"]
---

# 两种真实三人组件与目标

E为三个不交单客户资源，J为两个不交各两单位客户资源；三名单位玩家，共同目录各含其资源。目标都(A,A,B)，B≠A；末位真实BR，前两位不需SPE。E的u=(1/2,1/2,1)、W2、OPT3、B1；J的u=(1,1,2)、W4、OPT4、B4。E/J原机制有R44/R868先例，不认领新游戏。

令归一权重w_E=x、w_J=1−x，x∈[0,1]。所有H按当前强制A、下一强制B后**真正grandchild**定义；位置2的B就是强制末位动作、已无grandchild决策，非BR B不能预删。τ是局部辅助价格，非全实例统一λ。

# 四个H在整个τ≥0半轴的精确式

位置1：E根强制后，真实末位BR菜单(d,v)=(1/2,1/2),(1,1)，θ1，所以H_1E=min{(1+τ)/2,1}。J菜单(1,1),(1,2),(2,1)，θ1，所以H_1J=1−τ。

位置2在目标首A之后：E若当前复制A，强制末位复制同A终端d=v1/3、θ1，或末位fresh给d1/2,v1，下包络min{(1+2τ)/3,1/2}。当前改fresh B时，末位复制B的**非BR终端**给d=v1/2、θ1，末位第三资源给d=v1，其余终端线不更低，故该当前动作下包络min{(1+τ)/2,1}。后者≥1/2、前者≤1/2，max当前A给H_2E=min{(1+τ)/2,1}。

J当前复制旧A时，末位同A终端d=v2/3、θ2，fresh末位给d1,v2，下包络min{(2+4τ)/3,1}；当前fresh B时，末位复制B给d=v1、复制旧A给d2,v1，θ1，所以包络1。max当前给H_2J1。因此

|位置|E|J|
|---|---|---|
|1|min{(1+τ)/2,1}|1−τ|
|2|min{(1+τ)/2,1}|1|

H_2E(0)=1/2≠真实M_2E1；r2 supH=M与D0不允许逐τ先筛B。所有函数共同折点网格{0,1}含最终常值/负斜率尾，对全部x同时精确，非只两个价格抽样。

位置1在[0,1]的加权线为1−x/2+τ(3x/2−1)，τ≥1尾非增，所以

\[
 \Psi_1(x)=\max\{x,1-x/2\},\qquad \Psi_2(x)=1.
\]

目标u1=u2=1−x/2、B=4−3x，于是g1=(3x/2−1)_+、g2=x/2，0≤g1≤g2。双侧C在此化为2g1+3g2，得到完整分段式

\[
 \boxed{F(x)=B+C(g)=3+\frac32|x-2/3|,\quad
 \min_{0\le x\le1}F=3\text{且唯一在}x=2/3.}
\]

旧逐组件sup帽Ψ_old=(1,1)，g_old=(x/2,x/2)，F_old=4−x/2，min7/2在x1。这里比较的是**整个字典最优值**，两最优混合还不同，不是只发现非最大L或固定权重帽下降。3与7/2是修复预算，不是覆盖效率比率或原SPE福利。

# 任意整数s份E、t份J的真全强制门槛

s,t为非负整数且s+t>0，完整目录3^s2^t，所有客户不交。任意根向量独立重标签，仍用全部末位BR：若第二在k个E取非根，r个J取非根且末位复制根，p个J取非根且末位复制第二，则

\[
 U=(s+2t)/2+(k+2p)/2,\quad
 V=(s+2t)/2+(k+2r)/2,
\]

0≤k≤s,r+p≤t。第二总可所有E取非根、J任意，保证V≥s+t，任何真尾故k+2r≥s，得到根U≥(s+2t)/2+max(0,s−2t)/2。

达到：s≥2t时指定k=s−2t个E非根、其余复制根，全部J非根；s<2t时全部E复制根，仅ceil(s/2)个J非根。每个第二联合动作后末位在E取fresh，J与根相同则取另资源，J异根时仅全向量等于指定第二才复制根、其它向量复制第二。所有末位是真BR；非指定第二得至多s+t，指定第二至少s+t且p0，给完整真尾，全部根得相同值可任选规定根补全SPE。零s或零t按同式退化，s=t0不在字典归一域。

因此所有根强制的ell=M_1精确相同，位置2真实门槛由末位BR坐标分解为M_2=s+t，

\[
 M_1=(s+2t)/2+\tfrac12\max(0,s-2t)
 =\max\{s,(s+2t)/2\},\quad M_2=s+t.
\]

本E/J整数家庭恰达到连续Ψ，无需D舍入损失；不是所有字典的D都0。目标仍单独为各坐标(A,A,B)，u1=u2=(s+2t)/2,u3=s+2t，W=2s+4t、OPT=3s+4t、B=s+4t。根退出完整SPE叶与这个仅末位BR目标不能混。

x2/3清分母取s2,t1：真M=(2,3)，目标u=(2,2,4)，g=(0,1)，C3、B6、预算9>0。旧帽g_old=(1,1)、C5、旧预算11。新的优化归一预算3乘3=9，旧全局归一min7/2并非该固定s2/t1旧预算11/3，不能把不同权重比较混成同一实例费用。

# 原独立核查与有限声明

11700B独审从原资源利润手算四H/全半轴，关键保位置2强制非BR末位终端；它随后读父稿与pooled依赖，先验含全部公式、单调性/负种子放大/预期例结果，且检索见摘要，不是blind。其Fraction核声称无作者/规范模型/数值LP导入，完整线排列区间和端点核四H与最优x/预算；本批未由未读程序/报告填新PASS。

2693B EVIDENCE另报告原research父方独立单位BI七个明确算术参数（含非整除和E2J1）共150912项构造策略IC，E2J1为18主题/6174IC，M与目标/费同上。这与counter六参数6708节点/240198IC、作者单点1333/47988是不同实现与域，不能相加或互相替代。6174与(1+18+18²)·18的组数相容只是算术，不凭此认证未读代码实际循环。

全参数整数门槛、半轴H及最优值由上面解析证明承担；有限运行身份/字节可得性、五份主源处置与当前范围另保。没有严格负点，没有一般或六人half付款。

原件、准确程序缺件/0-run范围、关系和逐源处置见[本批证据](../../tools/evidence/finite-dictionary-epigraph-and-round7-ledger-primary/README.md)。
