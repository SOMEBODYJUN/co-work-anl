---
id: "customer-attraction/beta-clone-fixed-full-strategy-lift-impossible-local-contract"
kind: "counterexample"
type_tag: "反例"
title: "Beta克隆固定策略提升的不可补全局部合同"
status: "proved-auxiliary-lift-counterexample; no-half-counterexample"
summary: "39人合法背景中的完整σ含hA两人子SPE；三clone单位实现保fresh24，但重复A0后的每个末位BR均给25，故固定所有fresh行为不能补全；非实际根到达或更弱终局lift反例。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/full_tree/beta_clone_fixed_strategy_lift_failure.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/full_tree/beta_clone_fixed_strategy_lift_failure.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/parent/beta_clone_review.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/parent/beta_clone_review.md"]
source_ids: ["41760f3ce20d91f738ae", "871a567d3f25d03e5102"]
review_status: "原五Markdown全文与全仓正式对象比较；知情解析清洗，原先手算/后读稿与两实现scope保真，数学CLI0"
truth_status: "静态表示/固定策略lift反例/同叶碰撞债已证；更弱可信lift与背景半利润未由这些源解决"
---

# 合法原背景与必须保留的原局部完整SPE

原客户兴趣及整数数目：AB36、C3、AC36、BC10，共85不同单位客户；仅AC客户有背景1。对每个AC客户x加共同主题P_x={x}，先固定36次有序历史h依次各选P_x，合法实现该背景，再余3玩家。目录三regular加36singletons，共39；整局39玩家，但**不声称h或hA为根实际路径**。

在h后的任一剩余历史，任何P_x利润≤1，而C仅由背景0的C/BC共13客户就对任意真实后继保至少13/3，因此singletons在剩余子局严格劣于某regular。固定剩余首人已选A，hA后第二人A/B/C的真实末位规定为B/A/A；全部末位regular利润为

| 第二行动 / 末位候选 | A | B | C |
|---|---:|---:|---:|
| A | 21 | 22 | 22 |
| B | 24 | 17 | 20 |
| C | 27 | 23 | 31/2 |

指定末位各为BR，singletons≤1不干扰。第二位在这些真回复下分别24、22、22，故规定A最优。对所有singleton首动作孩子任取完整BI；对h后其他首行动孩子和更早祖先也BI补齐，得原完整σ包含此hA子SPE。只需要合法离轨节点也须SPE，不能把这一步夸成h实际根到达证明。

# 完全非负有限单位clone实例

每原主题3clone。背景0客户喜欢其全部相关clone并复制2520次。每原AC客户x的相关标签为A₀,A₁,A₂,C₀,C₁,C₂,(P_x)₀,(P_x)₁,(P_x)₂共9个；每非空子集R放

\[
\frac{2520}{10\binom9{|R|}}
\]

个不同单位客户。|R|=0,…,9的每pattern整数分别252,28,7,3,2,2,3,7,28,252；空R删去。除2520后是P~Uniform[0,1]的条件独立Bernoulli有限兴趣分解，不是客户随机行动。

B三个clone覆盖相同，应商成同一个合法集合B₀；所用A₀/A₁和C clones因正pattern覆盖不同。每个singleton clone总质量（除2520）1/2；C clone仅背景0客户仍保13/3，所以任何singleton clone都不可能是末位BR。本文只需这些全部类别的排除，无须把标签别名当额外主题。

# Fresh局部合同与重复孩子的全部真BR

固定clone合法历史(A₀)。若逐项保留原σ的fresh原主题行为，当前必须选fresh A（对称写A₁），末位按原σ选B₀。该fresh叶当前收益24；在(A₀,A₁)末位fresh B/C各22、fresh A21、复用A₀或A₁各19，所以原选B₀合法。

若当前在(A₀)改为重复A₀，末位全部regular类别为：

| 末位动作 | 末位利润 | 当前重复者利润 |
|---|---:|---:|
| fresh A | 22 | 19 |
| B₀ | 22 | 21 |
| fresh C | 23 | 25 |
| 重复A₀ | 18 | 18 |

所有singleton clones≤1/2，其他未用A/C clones与对应fresh行相同，B别名合并不改行。因此末位**每个BR都为某fresh C**，不能另选B平局威胁；重复孩子的全部完整SPE都给当前25>fresh合同24，IC严格失败，统一乘2520仍成立。

关键积分自足如下。对AC客户，I,J条件P=p独立Bernoulli(p)，重复者份额

\[
E\frac{I}{2I+J}=\int_0^1[p(1-p)/2+p^2/3]dp=7/36;
\quad E\frac{J}{2I+J}=\int_0^1[p(1-p)+p^2/3]dp=5/18.
\]

零分子项取0。末位C收入36·5/18+3+10=23；当前重复者36/2+36·7/36=25。末位fresh A得36/3+36·5/18=22，B得36/3+10=22，重复A₀得36/3+36/6=18，表穷尽全部选项。不能把盈利偏离建在不可信末位上。

# 被否定和未被否定的量词

这严格否定：把某给定原完整σ在**所有fresh历史**的原主题选择逐项保留，再补全部重复孩子。一个合法离轨hA局部合同已经足以排除整个提升。重复让fresh C末位价从22升23，原B平局威胁消失；冻结他人的fresh静态优势不适用于这种真实响应。

它不否定重选其他fresh行为后仅保原实际叶，亦不否定只找某clone SPE使覆盖≤原剩余利润。原主题投影AAC给重复者背景收益27，clone25≤27，仍可严格大于要求保留的AAB24；故与[同叶复用折扣](../引理/Beta克隆的单次增益与复用上尾债务--引理.md)完全相容。没有证明本hA实际根到达，没有主half/六人反例、新颖性或最小性认证。

原父方先独立手算这些表后读定稿，direct_exchange先只收类型/局部策略/待检合同，独立积分并做另一有限单位实现，未导作者发现器。其脚本报告用60倍、5100单位客户**含零兴趣**，只用A₀,A₁,B₀,C₀和每P_x一个clone；核原39标签两人子局1560比较及较小clone局部全动作表。不是作者2520倍完整三clone输入，也没有枚举后者全部SPE。那份原计划独立审查Markdown未留下，父方页只记录实际收到内容，不伪称不存在文稿完成。

本批程序/JSON未读未跑；原发现attack_beta_clone_local_lift仅提出类型，probe有限阴性不是普遍lift证明。严格反例由上述全类别BR、积分、有限非负单位客户构造承担。
