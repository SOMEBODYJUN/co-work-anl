---
id: "customer-attraction/profit-bellman-unbounded-and-overlap-credit-obstructions"
kind: "obstruction"
type_tag: "障碍"
title: "最优剩余利润的局部系数与共享负载信用"
status: "proved-analytic-two-full-SPE-families; exact-template-only"
summary: "精确算两个完整SPE族的背景最优利润，排除任意固定局部系数及只计共同负载的实例无关可加信用；保整体half余量与剩余信用义务。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/CLAIMS.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/CLAIMS.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/FAILED_ROUTES.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/FAILED_ROUTES.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/RESEARCH_STATE.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/RESEARCH_STATE.md"
---

# 最优剩余利润的局部系数与共享负载信用

## 对象与所排除的台阶

采用有限单位客户、有限共同非空目录、单位提供者、全部有序历史纯SPE，允许重复、空主题、零客户和任意平局。合法前缀的过去负载为整数b，余r人。定义
\[
F_r(b)=\max_{Z\in\mathcal S^r}\sum_x\frac{c_x(Z)}{b_x+c_x(Z)},\quad F_0(b)=0,
\]
零分子项取零。这是**剩余提供者利润**，不是已覆盖集合的总覆盖补全，也不是额外查询静态安全值。节点实际行动A、当前最终收益u、真实尾部利润V时，P=u+V。若对全部节点有F_r(b)≤2u+F_{r-1}(b+1_A)，再用尾部F≤2V，确实足够推出F_r≤2P及根half。下面否定的是这个局部充分台阶，不是F_r≤2P本身。

## 不交大主题族：每个有限局部系数均失败

每个n≥2，A有n名客户，B_1,…,B_{n-1}各有一名客户，所有客户池不交；恰n人，目录恰这n主题。策略在**每个**长度t<n的有序历史都选A。若过去a次A，当前照做、未来全A，其收益n/(a+n−t)≥1；改任一B_j后未来仍全A，收益1/(1+过去B_j次数)≤1。因此所有历史/再次偏离都最优，是真完整纯SPE，不只实际全A路径。

实际每人u=1，W=n。A及全部单例用n槽覆盖2n−1名客户，所以F_n(0)=OPT_n=2n−1。固定第一名A，若余n−1人中k人选A，其余槽换成不同单例不减利润，且足够单例可用。全部候选的精确最优值故为
\[
F_{n-1}(1_A)=\max_{0\le k\le n-1}\left[\frac{nk}{k+1}+n-1-k\right]
=2n-h_n,\quad h_n=\min_{j\in\{1,\ldots,n\}}(j+n/j).
\]
这包括k=0与重复单例，不是连续松弛。AM-GM给h_n≥2√n；取j=⌈√n⌉给h_n≤2√n+1。根台阶
\[
F_n(0)-F_{n-1}(1_A)=h_n-1\ge2\sqrt n-1
\]
无界。给定任意有限实α，取整数q≥2且q>(α+1)/2，n=q²，则h_n=2q，台阶2q−1>αu。故不存在人数无关有限α能支付所有局部台阶，空根已足够。α=2在n=3时台阶5/2失败，n≥4由下界≥3失败；n2不冒严格失败。

实际尾部V=n−1，余量2V−Ftail=h_n−2；根系数二债h_n−3，两者相差1，恰2W−OPT=1。尾部信用按√n增长而当前收益恒1；不能把本族称half反例，也不能只把2调成更大固定系数。已知实例族的新内容是此F的精确分析，不认证原实例新颖性。

## 交叠族：17/6是另一目标的精确工具值

每个n≥4令x=n−2，目录A,B,L_1,…,L_n。每个普通j<n有类型{L_j}:x、{A,L_j}:1、{B,L_j}:x；特殊叶有{L_n}:x、{B,L_n}:x、{A,B,L_n}:n−1。各重数为不同单位客户。

完整策略：空历史A；非空历史长≤n−2，若过去全B则A，否则B；末位精确BR、平局序B,A,L_1,…,L_n。其全部有序历史分类证明见[任意人数首步补全余额](../反例/任意人数首步补全余额--反例.md)，这里实际重读全证明后复用，不把在轨激励当完整性。该旧页的F是**总覆盖补全**；本页以下重新优化利润F。

实际A B^(n−1)，u_A=n−1/n，u_B=n−1/n−1/(n−1)，W=n²−2；每叶有私有x>0，全n叶是唯一无序最优支持，OPT=2n²−2n−2。表达n−1/n始终是n减1/n。

背景一名A，余n−1槽计数a,b,ℓ_j，d为不同正叶数。精确利润
\[
P=x d+x\sum_j\mathbf1_{b+\ell_j>0}
+\sum_{j<n}\frac{a+\ell_j}{1+a+\ell_j}
+(n-1)\frac{a+b+\ell_n}{1+a+b+\ell_n}.
\]
对f(c)=c/(1+c)，移走一个正覆盖者损失1/[c(c+1)]。

若b=0，有A或重复叶时，换一槽为未用普通叶；总槽n−1保证至少两叶缺失，普通叶存在。移A的所有背景内损失≤n−1，移重复叶更小；A外不失覆盖，新叶增加2x=2n−4>n−1，因此严格改善。最优恰n−1个不同叶，含特殊叶，得到P_0=2(n−1)x+(2n−3)/2。

若b≥1，保留一个B，把A、额外B或重复叶依次换为未用普通叶。不会减少A外旧覆盖，新增至少x私有客户。移A背景内损失≤(n−1)/2+(n−1)/6=2(n−1)/3≤x；移额外B≤(n−1)/6，移重复普通叶≤1/6，移重复特殊叶≤(n−1)/12，均≤x。新叶背景内贡献非负，故可不减至a=0,b=1、n−2个不同叶。用特殊叶替换普通叶的利润增量(n−1)(2/3−1/2)−1/2=(n−4)/6≥0。故可含特殊叶和n−3普通叶，得P_1=2(n−1)x+(7n−13)/6。P_1−P_0=(n−4)/6≥0，所以
\[
F_{n-1}(1_A)=2(n-1)(n-2)+(7n-13)/6.
\]
全部整数多重集合已消元，n4等号包括在内。根差与余额为
\[
\Delta=(17n-23)/6,\quad 2u_A+Ftail-OPT=(23-5n)/6-2/n.
\]
n4余额0；每个n≥5为负，n5为−11/15。必要局部系数R_n=n(17n−23)/[6(n²−1)]→17/6；任意α<17/6最终失败（ε=17/6−α，n≥5,n>4/ε时17/6−R_n=(23n−17)/[6(n²−1)]<4/n<ε）。但17/6不是通用候选，被前节无界族加强。

实际V=n²−n−2+1/n，其2V−Ftail=(17n−35)/6+2/n；减根债仍2W−OPT=2(n−1)>0。不能以局部余额负否定整体利润half或原half。作者及独审所报n4…8合15501计数候选只核有限实现；本批没有读其程序/报告或新跑该回归，全n结论由上述消元及既有SPE证明承担。

## 共同负载可加信用的精确不可能性

一个充分信用合同是
\[
F_r(b)\le2P_h+C_h,\quad
\Delta_h+C_{hA}-C_h\le2u_h,\quad C_{terminal}\ge0,\quad C_{empty}\le0.
\]
从终端0≤C_terminal开始用局部式和尾部界可递推第一式，根边界才给half。这不是所有half证明的必要形式。循环取C_h=F_r−2P_h只把局部式化等式，根条件重述主问题，不能算证明。

排除的模板严格为C_r(b,c)=Σ_x f_r(b_x,c_x)，其中c是真实剩余r人负载，同一函数族仅依r及该客户两个非负整数负载；不依实例、客户总数、目录、其他客户或策略信息，且f_r(0,c)=f_r(b,0)=0。可负、无连续/单调/凸性假设。

all-big根后n个A客户的(b,c)=(1,n−1)，由尾部界强制
\[
f_{n-1}(1,n-1)\ge(2-h_n)/n.
\]
交叠族根后仅n−1名特殊共享客户同为(1,n−1)；普通A客户为(1,0)，其他背景0，全消失。空根信用0，由根递推强制
\[
f_{n-1}(1,n-1)\le\frac{(23-5n)/6-2/n}{n-1}.
\]
当n≥16，前界≥1/n−2/√n>−1/2；后界在n≥10已严格<−1/2，因为其分子减−(n−1)/2为(10−n)/3−2/n<0。于是同r的同一个f(1,r)上下界冲突。两个输入均真完整SPE，非抽象非均衡负载分离。

all-big第一子节点更精确要求2−h_n≤C_A≤3−h_n。这说明负信用及独占/主题替代结构的信息承重，不说明放开c=0就足够。允许背景独占项、实例或目录信息、非可加信用、全真实菜单等未被排除。尚缺独立于未知half差额的可计算状态及真实分支信用转移证明。

## 来源和接续

以上解析完整读并比较两份发现/两份独审及信用稿：related IDs5807ac87276a9bc80ce0、efb09bff2fbae18ba384、0efa8da260f6c6ee8015、c9ccc7817c179b3b1396、9bf8a294ee059185147e，全部原字节见[相关源清单](../../../../tools/evidence/d22-frontier-ledger-primary/related-source-manifest.json)。原“先盲重构再对照”是当时审查先验，当前知情清洗不新增独立审稿人。无新数学程序、无旧成功重跑、无外审/新颖性认证。上述三障碍互相加强/合用，不反驳真安全聚合、自由静态门槛或六人half。
