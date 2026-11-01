---
id: "customer-attraction/last-payoff-ratio-two-path-relaxation-and-full-spe-screen"
kind: "computation"
type_tag: "计算"
title: "末位收益比例的两路径松弛与完整终局筛选"
status: "five-primary-sources-read; both-original-entrypoints-replayed-once"
summary: "三份NPZ全字段重构并由原生成器逐字节复现；局部LP可行不保证目标完整SPE，原精确筛选在三人/四人均排除目标路径，五人未运行完整SPE枚举。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round13/direct/last_ratio.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round13/direct/check_last_ratio.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round13/direct/last_ratio.py.3.npz"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round13/direct/last_ratio.py.4.npz"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round13/direct/last_ratio.py.5.npz"
---

# 程序对象和准确模型

五主源为两个完整Python程序和三份NPZ数据，共451248字节，均通过clean show导出并核冻结SHA。生成器1097B、检查器1057B；数据分别9538B、60930B、378626B。实际原件和manifest见[证据目录](../../tools/evidence/last-ratio-two-path-primary/README.md)。它们是有限探针，不是六人half证明、反例或一般末位比例定理。

对m∈{3,4,5}，共同目录保n=2m−1个标签0,…,n−1。客户兴趣类型是全部2ⁿ个0/1向量，包括全零类型。bits[t,x]表示类型x喜欢主题t；非负权重是各类型客户重数的归一化。原生成器先用浮点LP发现重数；原检查器把每个数按limit_denominator(10⁷)转成有理数，再取分母最小公倍数展开为不同单位客户。并非保留有权客户模型。

完整终局a=(a₀,…,a_{m−1})允许任意重复，其类型负载c_x(a)=Σ_i bits[a_i,x]。单位展开后的真实收益为Σ_xN_x bits[a_i,x]/c_x(a)，未覆盖项为零。原检查器用Q=lcm(1,…,m)缩放收益为整数，精确保重复行动、离轨历史和全部平局。

# 两路径局部LP实际约束了什么

固定两条候选终局
\[
 P^0=(0,1,\ldots,m-1),\quad
 P^1=(m-1,m,\ldots,2m-2).
\]
记u_{r,i,x}=bits[P_i^r,x]/c_x(P^r)，零负载项置零。对P⁰的全部i=0,…,m−1及P¹的i=1,…,m−1，令前缀负载b_{r,i,x}=Σ_{k<i}bits[P_k^r,x]，对每主题j加入
\[
 \sum_xN_x\left(u_{r,i,x}-
       \frac{bits[j,x]}{b_{r,i,x}+m-i}\right)\ge0. \tag{LOCAL}
\]
另加根比较Σ_xN_x(u_{0,0,x}−u_{1,0,x})≥0。LP令P⁰覆盖W=Σ_xN_x1_{c_x(P⁰)>0}=1，并最大化其末位收益。所有分母正；浮点linprog调用HiGHS，生成器只在success时保存数据，没有保存精确对偶证书。

(LOCAL)来自真实偏离利润的最坏后继下界：当前选j后至多m−i名剩余角色覆盖同一客户，所以真实查询利润至少Σ_xN_x bits[j,x]/(b_x+m−i)。SPE若有该规定路径，必满足这些必要不等式。但早期位置的不同偏离后继尚未指定，也没有所有子博弈的最佳回复，因此这些行**不充分**构成完整SPE。末位i=m−1没有未来，分母才给准确末位比较；额外一条根比较也不补全全部离轨策略。

总行数n²+1，三数组分别26×32、50×128、82×512。程序不接受任意m的通用CLI输入；顶层固定运行这三个人数。其“末位收益/指定路径覆盖”不是OPT/W，也没有求六人目标。

# 三份NPZ的完整读取和精确有限数据

每个文件恰有bits、weights、rows、names四字段。bits和全部行逐元素按原定义重构；names的每个(r,i,j)及最后root均核对，未只读shape或摘要。读取names时用仅允许NumPy数组重构的reader，并逐一比较预期标签；所有数值字段直接读，原始NPZ不改。

新辅助检查保原有理化规则，把行乘Q后逐项还原整数系数，再对全部整数客户求精确残量。三份均满足权重非负、指定P⁰覆盖等于分母scale、每一LOCAL及根行残量非负。浮点残差中约10⁻¹⁷负值没有当作数学违例；精确整数最小残量均为0。

| m | 标签/全部类型 | 正重数类型 | 单位客户数和P⁰覆盖 | P⁰末位/覆盖 |
| ---: | ---: | ---: | ---: | ---: |
| 3 | 5/32 | 7 | 253 | 136/253 |
| 4 | 7/128 | 11 | 17200 | 4083/8600 |
| 5 | 9/512 | 16 | 6455743 | 2805564/6455743 |

全部非零兴趣向量和整数重数见frozen-inspection.json及client-types.tsv。这里这些P⁰恰覆盖全部正客户，故它们自身的覆盖等于该输入OPT_m；末位比例仍不是half福利比。未给原浮点LP的精确最优对偶，表中只称精确可行的发现输入，不把success自动升为精确最优性证明。

# 原完整终局筛选的正确递归

在已固定历史h、当前位置i=|h|，令S(h)为该子博弈全部完整纯SPE可实现的完整终局集合。原递归终点为S(h)={h}。对每个行动a先递归求非空S(h,a)，然后令
\[
 \alpha(h)=\max_a\min_{o\in S(h,a)}u_i(o).
\]
准确保留
\[
 \boxed{S(h)=\bigcup_a\{o\in S(h,a):u_i(o)\ge\alpha(h)\}.}\tag{SCREEN}
\]
必要性：任意SPE选择a时，其收益必须至少每个其他行动的所选可信孩子收益，后者至少该孩子最小值。充分性：对满足阈值的o，在选中孩子用实现o的完整SPE，其他孩子各选使当前i收益最小的完整SPE；不同有序孩子独立拼接，所有偏离不优，未来各子博弈仍是SPE。有限完全信息游戏的逆向归纳保证各孩子非空，所有平局用≥保留。

所以代码枚举的是完整纯SPE的**终局元组集合**；输出名nSPE为其大小，不是完整策略树份数。它不会声称已经输出每份策略树。pay函数直接用单位客户整数表而非LOCAL松弛，故可以真实排除LP目标。

# 两原入口各一次运行的实际结果

生成器在全新目录运行一次，原代码未改；三份新NPZ与对应冻结NPZ**整个文件逐字节相同**，不只是目标值或字段相等。原检查器在另一新目录使用三份冻结NPZ运行一次，exit0、stderr空，其明确的if m≤4使五人没有执行SCREEN。结果为

| m | 终局集合大小 | P⁰是否在集合 | 最大末位比例及对应终局 | 该终局Q缩放收益 |
| ---: | ---: | --- | --- | --- |
| 3 | 2 | 否 | 17/57；(4,2,1) | (504,456,408)，Q=6 |
| 4 | 1 | 否 | 3316/14193；(5,2,6,6) | (45624,45108,39792,39792)，Q=12 |
| 5 | 未计算 | 未检查 | 未计算 | 未计算 |

三人对应整数总收益1368、真实福利228；四人总收益170316、真实福利14193。四人重复主题6被保留。这里没有对未列三人另一终局增加新断言，也没有把两个有限样例扩为一般末位比例上界。五人数据虽精确通过LOCAL，尚未有完整SPE目标认证。

因此这组数据的可用结论是：原浮点两路径松弛与其精确有理客户实例可完全复现；三人/四人完整检查明确指出规定目标并非可实现SPE。即使某个局部末位比例大，也不能当作原模型的完整SPE或福利反例。

# 复现、关系与接续

原生成器依NumPy/SciPy，检查器另用标准库Fraction/lru_cache。所有真实命令、运行版本、源码hash、stdout/stderr及输出都保留于replay。源程序按__file__位置读写NPZ，复现必须先复制到新目录；不可在冻结original旁运行生成器覆盖原件。根辅助二进制读取程序初次用了当前NumPy不存在的私有header函数，已在任何原入口运行前改为公开版本reader；失败原helper及修正记录均保留。该辅助修正不改变五个主源。

与[实际负载切线银行](../候选/实际负载切线银行与共同误差付款--候选.md)及[真实重放付款问题](../问题/真实重放协方差的定量付款--问题.md)只有相同原模型/真实后继量词的联系；本LP没有相应共享鞍点、来源库存或共同误差付款。不能把其数值当作T-PAY、V-PAY或五人定理的认证。可接续工作是补全真实续局或分析明确的末位辅助命题，仍须按自身域处理；本批没有新一般定理、盲审、外审或六人反例，正式超图留第三阶段。
