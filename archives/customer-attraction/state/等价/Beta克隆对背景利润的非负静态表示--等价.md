---
id: "customer-attraction/beta-clone-positive-static-background-profit-representation"
kind: "equivalence"
type_tag: "等价"
title: "Beta克隆对背景利润的非负静态表示"
status: "proved-static-and-restricted-fresh-tree; unrestricted-fixed-strategy-lift-refuted"
summary: "非负有理有限兴趣型把合法整数背景利润精确变成全鲜clone覆盖；无约束最优恰F_r，只有受限fresh树保SPE，静态优势不代动态补全。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/full_tree/beta_clone_background_representation.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/full_tree/beta_clone_background_representation.md"]
source_ids: ["a9c56de460b0753a7053"]
review_status: "原五Markdown全文与全仓正式对象比较；知情解析清洗，原先手算/后读稿与两实现scope保真，数学CLI0"
truth_status: "静态表示/固定策略lift反例/同叶碰撞债已证；更弱可信lift与背景半利润未由这些源解决"
---

# 不是把背景份额直接改成带权客户

固定[原模型](../定义/共同目录完整历史模型--定义.md)有限原主题标签集A、任意合法整数背景负载b_x、剩r≥1名单位玩家。每原主题a造q≥r个clone标签(a,j)。目标是将原**剩余玩家总利润**表示为另一个空背景单位客户游戏的覆盖；不将其误写成原客户通常覆盖或旧玩家在内的总福利。

对原单位客户x，其接受原主题集合B_x，对应L=q|B_x|个相关clone。b_x=0时给一个质量1、接受全部相关clone的客户；b≥1时，对每个相关标签子集R放非负有理质量

\[
w_R=b\frac{|R|!(b+L-|R|-1)!}{(b+L)!}.
\]

它来自P密度b(1−p)^(b−1)，条件P=p独立将各相关clone纳入R：积分b∫₀¹p^|R|(1−p)^(b+L−|R|−1)dp正是w_R。全部R质量和1；空R无人可覆盖可删。L0时也只空兴趣，所有收入/覆盖贡献零。原客户分别相加，有限个有理兴趣型用同一正整数M清分母展开成**不同单位客户**，没有负质量/非单位提供者。P不是游戏中随机客户选择，只是确定有限重数的积分记账。

# 全鲜终局逐人精确相等

任取r个clone标签全部互异的终局，对原客户x有k个所选标签对应喜欢它的原主题。k0时贡献0；k≥1时覆盖概率E[1−(1−P)^k]=k/(b+k)，且这k个不同标签对称，故每玩家份额为1/(b+k)。b0直接P1，份额1/k亦相同。

因此全鲜终局的每位clone收入，恰等于其原主题投影在原背景游戏的收入；clone福利恰为Σ_x k_x/(b_x+k_x)，即原剩余总利润，所有量在M展开后同倍放大。原主题重复仍允许，只需用不同clone。

定义

\[
F_r(b)=\max_{T_1,\ldots,T_r}\sum_{x:c_x(T)>0}\frac{c_x(T)}{b_x+c_x(T)}.
\]

**无约束clone游戏的r槽最优覆盖也恰为F_r(b)**（按M共同缩放）。下界：每原主题元组可用q≥r的互异clone实现。上界：若某(a,j)重复，换其中一次为同原主题未用clone(a,j′)，仍有该旧标签的其他使用者，所以每相关原客户的不同所选标签数d增加1，覆盖d/(b+d)不降，不相关客户不变。q≥r保证可找fresh。反复freshen后保持原主题投影的多重集且全鲜，其覆盖≤F_r；原终局亦≤F_r。此证明只覆盖静态最优，不声称freshening保持SPE。

# 受限树保持SPE与动态缺口

在只允许选择**未用clone**的受限树，任一全鲜历史按其原有序投影执行给定原完整SPE σ，并任选未用clone。每当前候选及其真实受限后继都全鲜，逐玩家份额身份保原σ的全部比较，故这是受限fresh树完整SPE。

受限树不是原共同目录游戏：原clone目录还允许复用旧标签。重复后若照搬原投影策略，后继收入不再由全鲜公式给出，后继未必理性；任取BI填重复孩子也不保证偏离者足够低。更强的“固定原完整σ，在所有fresh历史逐项保留，再补重复孩子”现已被[24到25反例](../反例/Beta克隆固定策略提升的不可补全局部合同--反例.md)否定。该失败不破坏静态表示或无约束OPT身份。

一个正确的静态事实仍不足：冻结其余终局标签，原主题a的旧clone已有n≥1使用者，给当前一个fresh同主题clone的利润不低于重复旧clone。逐客户条件P=p、其余相关负载Z，差为

\[
p(1-p)\left[\frac1{1+Z}-\frac1{n+1+Z}\right]\ge0.
\]

对P、Z和客户求和保非负。但这冻结了别人，SPE后继会响应fresh/reused选择；不能从这条式排除动态复用。

# 标签商与条件用途

部分clone可能同覆盖；静态收入/OPT不受商影响，真实集合目录只留一份同覆盖集合。完整SPE若要商，应按[覆盖标签完整策略商](覆盖等价标签的完整策略商--等价.md)重构策略，不是原动作表随意删列。下面碰撞统计S/R/H_t属于某标签提升，不能当商目录内在量。

若将来能对所有原背景SPE构造某份无约束clone SPE τ且W_c(τ)≤原实际剩余利润P_σ，则根HALF(r)与OPT_clone=F_r(b)会给F_r(b)≤2W_c(τ)≤2P_σ。全鲜实际叶投影原实际叶的更强lift足以满足此W条件，但都未由静态表示证明。固定**整个fresh策略**版本已否，不排除这两更弱接口。

当前背景半利润F_r(b)≤2P是不同于裸并集BG/UNION-BG/新增覆盖GLOBAL的对象，详[背景账本](../资料/背景总份额归纳的两种覆盖量与失效接口--资料.md)；后者一些失败不自动否定本对象。当前五人根half也不直接给一般背景lift；若上述W-lift对固定r成立，则对应根HALF(r)才可用，不能把原39人背景合法化的人数拿来替clone剩余r。
