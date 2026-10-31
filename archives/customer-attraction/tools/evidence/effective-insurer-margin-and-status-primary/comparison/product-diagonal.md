---
id: "customer-attraction/homogeneous-big-theme-product-diagonal-optimal-menu-boundary"
kind: "lemma"
type_tag: "引理"
title: "同质大主题产品的对角最优菜单边界"
status: "proved-specific-SM-attack-boundary-for-all-m-q; not-general-method-impossibility"
summary: "m≥2/q≥1同质all-big actual产品有一个对角最优元组每行L=q，和qm严格高于净缺口q(m−1)；单步barL也不降，后加§7独有解析范围非原三审已审。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/dynamic_matching/README.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/dynamic_matching/README.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/harmonic_debt/product_transfer_independent_review.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/harmonic_debt/product_transfer_independent_review.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/independent_attack/product_transfer_independent_review.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/independent_attack/product_transfer_independent_review.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/source_reset/product_independent_review.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/source_reset/product_independent_review.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/dynamic_matching/product_transfer_lemma.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/dynamic_matching/product_transfer_lemma.md"]
source_ids: ["9826517b238bcb4e1b77", "2a7fefaf181c46e608ea", "cb41970a61296e3fa636", "34b184d5d1a61f83fc40", "30e8d20848c6519f641f"]
review_status: "五MD全文/原SHA与已有完整产品对象比较；原三独审实际section范围另保，知情重构不是新blind/原审计重演"
truth_status: "明示产品过滤/闭包/有限条件放大/同质对角边界已证；未提供SM严格种子或half反例，六人未解"
---

# 特定产品和准确被排除的攻击

单组件m≥2玩家，Big=B有m名客户，另m−1个singleton各一名客户，与Big及彼此不交；客户/玩家全单位，目录恰这m主题。每个有序历史都选B的策略完整SPE：过去a次B、当前后未来全B时当前B收益m/(a+余人数)≥1，而任何singleton偏离≤1。

q≥1同质组件完整Cartesian产品、actual取该策略的积，故全历史SPE，W=qm，OPT=q(2m−1)，净缺口q(m−1)。本引理只固定这个actual产品/同质输入，不排其他actual联合SPE、异质组件或别的一般方法。

原30e§7问：能否压低混合向量查询的全续局L，反[最弱SM存在最优元组桥](../资料/全续局产品转移与全部最优元组攻击--资料.md)？答案是该同质输入/actual产品不行，因为存在一个对角最优排列，其m行各L=q。

# 非Big过去域的唯一真后继

考虑任意产品有序历史，**每个坐标的过去都至少已有一次非B行动**。这个域在未来任何行动下永久保留。对剩余人数向后归纳：末位在每坐标选B的分母至多m−1，所以收益至少m/(m−1)>1；任意singleton收益≤1，故末位唯一BR是全B向量。

假设所有更晚子博弈唯一全B。当前选任意向量后仍在该域，真后继都全B；若当前在某坐标选B，同样最终该坐标Big覆盖人数≤m−1、利润>1，若选singleton则≤1。其他坐标未来也已唯一，不存在跨坐标平局补偿，改变任何坐标为singleton都严格亏。当前唯一全B，完成对**全部有序子历史/所有联合偏离**的归纳。

这是比“存在allB后继”强的唯一性，只在每坐标已有非B过去域；不可推广到任意背景/所有目录。m2时m/(m−1)=2仍严格，零个后继时归纳直接终止。

# 对角最优排列每行恰q

在actual前缀B⃗^(i−1)强制查询B^q：每坐标当前覆盖m客户、最终Big覆盖人数最多m，故任何真实后继当前收益≥1，合计≥q。全B真后继达到q，所以L_i^prod(B^q)=q。

强制任一个singleton的对角向量S_a^q：每坐标立即有非B过去，后继由上节唯一全B；actual过去全B没有该singleton，当前每坐标独享它，收益1。因此L_i^prod(S_a^q)=q。末位i=m没有后继时也直接等q。

取m个比较行：一行B^q，其余m−1行每个scalar singleton的q次向量各一次，按任何位置配对。每坐标投影恰Big+全部singleton，覆盖2m−1，故这是合法产品最优元组。逐行刚才结论给

\[
\sum_{i=1}^m L_i^{prod}(T_i)=qm>q(m-1)=OPT_{prod}-W_{prod}.
\]

余量q>0。即使其他混合向量L真的下降，存在式仍可选这个对角元组，所以不能仅靠它们反SM-opt-exists。不声称所有最优元组都等qm，也不把这个特定攻击停界写成SM普遍真或half证明。

# 原单步LP也没有下降

同一单组件actual前缀，强制singletonA后，下一角色θ=m/(m−1)。后继域已含非B，所以它选B后未来全B，(d,v)=(1,m/(m−1))；选同singletonA则(1/2,1/2)，选其他singleton则(1,1)。没有v高于θ的供体，LP平均v≥θ只支持B行，故barL_i(A)=1，末位直接同值。

强制B后，下一门槛θ=1：选B在任何后继至少1、全B尾达到1，而单例当前≤1。任意未过滤LP菜单叶若下一动作B，两位同主题收益**精确d=v**；若下一动作singleton，则d≥1≥v。故所有菜单叶d−1≥v−θ，LP给Ed≥Ev≥1，全B达到，所以barL_i(B)=1。这是不依求解器的直接重构，与源§7的盈余关系一致。

原稿还描述单组件尾SPE至多出现一次singleton：首次非B后上节单坐标唯一全B，使其后不能再出现；若下一B且更晚有singleton，两位Big的正盈余相等。该描述不提供多层转移额外收益，完整产品子SPE的对角结论已由唯一域归纳直接覆盖，而非仅一层barL阴性。

# 后加版本与来源限制

这是10723B主源最后§7的解析内容；harmonic原审查自述读§1–6，independent_attack只§2/3/5加§4见证，source_reset只§1–5。它们当前文件SHA被绑定不表示曾审后加§7。此页本次全原文后知情重构其全m/q证明，保原未开始异质/更深耦合方向，不冒原blind/外审/新颖性或新程序扫描。
