---
id: customer-attraction/indexed-and-actual-fourth-b-joint-necessary-graph-program
kind: program
type_tag: 程序
title: 索引主题与实际第四步B分支的联合必要图程序
status: complete-source-review; original-default-verifier-replayed
truth_status: 固定16直方图支持的必要行系统及精确可行点核验；非真实SPE或半覆盖定理
review_level: full-source-and-dependency-reading; one-unmodified-default-verification; current-input-interface-audit
scope: 六人共同目录完整历史纯策略SPE的必要条件；程序实际仅搜索固定16旧直方图支持、1905列
summary: 原4621B程序把索引回复图、末位报价及真实第四步强制实际末主题的隐藏投影共同计价；本轮默认入口5108行精确通过，并保留各扩展开关的实际组合与单独local-v2的未绑定变量问题。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5/combined_branch_master.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5/combined_branch_master.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5/combined_branch_master_exact.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5/split_basic_graph.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5/cross_source_graph.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_3/all_reply_actual_floors.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_3/continuous_old_query_cuts.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_2/tail3_B_projection.py
---

# 索引主题与实际第四步B分支的联合必要图程序

主源 `9aa0e3af9d15dc62a830` 是4621B Python程序，[原件](../../tools/evidence/combined-branch-master-program/original/combined_branch_master.py)SHA-256为 `b29b0615415747d39a2af80f3b370b1dfd13afdf3e7ee1256576ca85e26c9dd5`，两冻结提交字节相同。它将几种由同一完整历史SPE导出的必要行放入同一个LP，而没有构造完整策略。

本轮在隔离目录对未改原码**只执行一次默认 `--verify`**：重建5108行、1905列，原有理点全部行的最小slack为0，归一化比较覆盖为1，实际覆盖为

\[
W=\frac{7788343487189316604380335059457339}
{16141009471373384499891913301798724}<\frac12.
\]

这是该固定支持必要系统的可行性证据。它既不认证此值是精确最优值，也不把这个点提升为六人SPE反例。默认核验未调用 `linprog`；NumPy/SciPy仍因模块顶层导入而是运行依赖。

## 数学对象、共同身份与固定支持

底层模型是有限单位客户、有限非空共同主题目录、六名单位权提供者依次观察全部有序历史选题，终局每客户向所有覆盖者均分1。完整历史纯SPE须在每个有序历史指定合法行动并满足所有单步偏离；主题可重复、可为空，平局和离轨历史也保留。这里记实际路径为 $A_1,\ldots,A_6$，比较六元组为 $T_1,\ldots,T_6$，客户实际成员位为 $a\in\{0,1\}^6$，$d=\sum_i1_{T_i}$。若启用程序自动附加的 `--optimum`，比较六元组必须实现最大六主题覆盖；其余许多必要行本身允许任意六个合法比较主题。

索引分支在实际前三题后强制第四题 $T_i$，第五、第六题按同一策略续局为 $B_i,C_i$。每客户用八种三位词 $(t_i,b_i,c_i)$ 的计数直方图 $h$ 描述六个比较索引，$\sum h=6$、$d=\sum t h$。第五步改选 $B_j$ 或 $C_j$ 后的末回复记 $R$；实际第五人改选此末回复之后又产生末回复 $Z$。这些角色的身份和出现的历史必须保留；$B_i$、$C_i$、$R$、$Z$ 不等于实际 $A_6$。

程序从旧 `attractive_nested_exact.json` 读取**16条固定hist描述符**，丢掉其旧质量再建列：1个 $K$、16个hist质量、194个回复组各3个显式二元联合状态01/10/11，共582个 `joint-reply` 列，以及1306个 `overlap` 列，总计1905列。00质量由hist质量减其余三状态恢复。各组代表指定索引家族及对角轨道下的R/Z边际；overlap是两R边际交叠的松弛变量，受两个上界控制。它们不是同一完整客户原子的联合分布证书。

归一化与目标仅用hist列：

\[
 O=\sum_{a,h}\mu_{a,h}1_{d>0}=1,\qquad
 W=\sum_{a,h}\mu_{a,h}1_{\sum a>0}.
\]

$K$ 是目录主题大小的公共上界变量，通过容量行限制各主题；它不是最优六主题覆盖 $O$。有理客户质量可统一放大成整数，但这仅解决已给联合客户类型的单位化，不替缺失的共同实现或完整SPE补证。

用直方图压缩索引置换，在所用对称线性必要行中可用同指标与异指标的重数计算；它并不将全部有序历史压缩为无序计数策略。任一真实SPE能产生这些必要统计，但不一定落在程序固定的16个hist支持中。因此固定支持不可行也只排除此支持；此处得到可行点更不推出完整博弈存在。

## 默认5108行从何而来

导入主模块会向全局 `sys.argv` 自动补齐 `--priced --optimum --old-query-cuts --mixed-pair`，然后导入下层程序。这四项不是用户必须另写的参数，也不能只看主函数附近的65行增量推断默认系统大小。

| 层及数学作用 | 最终净计入行数 | 累计净行数 |
|---|---:|---:|
|`nr.old_system()`：448种 $(a,d)$ 上的旧必要行，经hist描述符提升|702|702|
|`full_new_reply_closure`：5个旧索引紧凑行、两家族各16个新末回复基本行；60个R–R、30个R–旧主题、10个旧主题–R比较|37+100|839|
|`actual_fifth_nested`：Z的24基本行、30个Z–旧、10个旧–Z比较，以及194个联合状态质量上界|64+194|1097|
|`attractive_nested`：60个Z–R、60个R–Z、60个配对R–R比较；1306个overlap各两个上界|180+2612|3889|
|`split_basic_graph`：第二索引家族的28个基本行，各拆成对角和非对角|56|3945|
|`cross_source_graph`：12个实际来源报价、2个容量行、8个最优比较替换行、960个隐藏回复报价行|982|4927|
|`all_reply_actual_floors`：R/Z三个轨道对六个实际来源的报价|36|4963|
|被冻结旧查询切面及混合强PAIR行|8+72|5043|
|被冻结连续参数旧查询切面|64|5107|
|实际第四步强制实际末主题B的三人尾隐藏投影|1|5108|

表按最终联合系统中保留的行计数，并非每个旧独立程序的输出行数：`full_new_reply_closure` 自身的1033行还含194个旧R边际上界；`actual_fifth_nested` 先删这194行，再以194个三显式联合状态之和上界替换。故旧独立1033行、上表839个暂计行与嵌套后1097行互不矛盾。

拆分层保留原行并新增两片；源码逐列断言两片和等于相应原行，默认复跑确实执行了这28个断言。连续切面用的是JSON内的64个已选有理参数，既不在此重新运行180个发现LP，也不把JSON所记发现点负slack当成本轮点的slack。混合强PAIR用同一末回复与旧查询主题的真实倒二比较，乘积项可由旧主题成员位乘该回复质量线性表示。

跨来源960行的网格为4个来源位置、2个被迫旧回复族、3个查询族、2种中/末定价模式、5个非负价格及4个末查询权重；隐藏回复的二元成员位在非负加权真实IC之后消去。所用[共同末位报价引理](../引理/共同末位报价与隐藏回复投影--引理.md)强调同一末回复必须同时承担源码中的所有比较，不能为每个查询另选回复。

### 旧702行及实际数据依赖

702行也不是一个无依赖常量。`new_reply_budget.old_system` 调用 `joint_system.build`，再加入保存的16个共同菜单切面、18个强配对切面和1个第四步全索引投影表，并断言行数702。实际层次为：

\[
331+50+6+200+8+14+6+35+1+14+2+16+18+1=702.
\]

依次是六人基本/报价行、桥行、6个自由回复切面、嵌套时域200行、8个maxroot切面、14个强PAIR、6个初始共同菜单、35个紧凑联合、1个旧根饱和、14个 `target_joint`、2个AB投影表、16个追加菜单、18个追加PAIR及1个第四步投影表。`target_joint.json` 在本次冻结依赖中真实存在；其路径可选不等于本次可以漏掉14行。

这些程序和使用的原JSON树均保在[共享依赖目录清单](../../tools/evidence/combined-branch-master-program/source-manifest.json)。当前接口审计精确读取所用系数、检查2399个实际使用的非负权重，并检查三个投影查找表各覆盖全部448种 $(a,d)$ 且归一化系数正。maxroot中的 $C$ 是有符号K系数，不能误作为非负乘子检查。原JSON的发现记录、旧证书和浮点诊断仍原字节保留；本轮没有重新执行这三个历史投影表的全部隐藏直方图最大化，也没有重新验证八个maxroot证书的推导。**当前5108通过表示按冻结行定义精确回代成功**；历史行的通用有效性需连同其原推导理解，不能由可行点反向证明。

## 主源独有的一行：实际第四步强制实际B

这里普通字母 $B$ 专指 $A_6$。在历史 $(A_1,A_2,A_3)$ 强制第四步选B，真实后两题为Q、R；第五步改选 $T_i$ 后真实末题为 $Y_i$。给定客户，令 $k=a_1+a_2+a_3$、$b=a_6$、$p=k+b$、$q=1_Q$、$r=1_R$、$z=p+q+r$、$e=\sum_i1_{Y_i}$，实际收益贡献 $u_j=a_j/(\sum_i a_i)$。分子为0时收益贡献取0。

投影器在同一真实客户上组合八类必要不等式，其中G是三族真菜单IC的组合 \(S+Z/12+V/6\)：

\[
\begin{aligned}
F&=u_4-b/z,\\
G&=6q/z+r/(2z)-d/(p+1)-e/[12(p+q+1)]+de/[6(p+1)(p+2)],\\
H_{2Q}&=u_2-q/(5+a_1),&H_{2R}&=u_2-r/(5+a_1),\\
H_{3R}&=u_3-r/(4+a_1+a_2),\\
L_Q&=u_6-q/(1+\sum_{j\le5}a_j),&L_R&=u_6-r/(1+\sum_{j\le5}a_j),\\
E&=6r/z-d/(p+q+1).
\end{aligned}
\]

其中F来自真实第四步偏离，G是三族真菜单IC的组合 \(S+Z/12+V/6\)，H是早期来源保底，L是同一实际末位对Q/R的报价，E是当前分支末位对六个比较主题的查询。每一行是对客户求和后非负，并非逐客户非负。原程序采用

\[
J=3360F+96G+660H_{2Q}+595H_{2R}+220H_{3R}+522L_Q+522L_R+108E,
\qquad
\psi(a,d)=\max_{q,r\in\{0,1\},\ e\in\{0,\ldots,6\}}J.
\]

于是同一真实SPE满足 $\sum_x\psi(a(x),d(x))\ge\sum_xJ(x)\ge0$。这里必须取**上包络**，不是把必要性方向颠倒为最小值。J对e仿射，端点0、6足够；`table()`仍逐一检查448种 $(a,d)$ 的28个隐藏状态最大值等于8个端点状态最大值。

联合程序仅把 $\psi(a,d)$ 放在hist列，其他列包括K均置0。它没有把Q/R硬认成某个索引回复，也没有新建该实际B分支的联合客户变量。索引分支与实际B分支的行可以同时使用，是因为它们均由同一完整策略与同一实际路径导出；可行松弛点仍可能无法将两套局部信息共同实现。详见[实际B分支合账引理](../引理/实际末主题三人分支的隐藏上包络与主图合账--引理.md)和[配套投影程序](实际第四步B分支的三人尾投影程序--程序.md)。

## 命令行域及原码的扩展分支问题

`TARGET` 的文件名前缀优先级是 `--local-v2`、`--new-local`、`--latest`、默认。添加约束的条件却是两个独立的if块，不能从输出名前缀推断全部已启用行。以下行数来自实读源码及冻结数组长度；**只有第一行本轮运行过**。

| 参数（可另加 `--verify`） | 使用的新增行 | 行数／TARGET |
|---|---|---|
|无扩展参数|默认5108|5108／`combined_branch_master`|
|`--latest`|32连续+8末位组合+29容量组合+3早期实际B投影|5180／`combined_branch_latest`|
|`--new-local`|5嵌套回复+4重查询|5117／`combined_branch_local`|
|`--latest --new-local`|上述72+9|5189／`combined_branch_local`|
|`--local-v2`|拟加5嵌套+5重查询+8组合|原码不能完成build；见下述未绑定变量|
|`--latest --local-v2`|72+18|5198／`combined_branch_local_v2`|

`portfolio` 只在 `if '--latest' in sys.argv` 内导入，成为 `build()` 的局部变量；v2 JSON的 `portfolio` 列表有8项。因此单独 `--local-v2`（或仅加 `--new-local` 而不加latest）会在第一项 `portfolio.row` 引用未绑定的局部变量。这是当前静态审查发现，未伪造失败运行日志，也未改原码。普通local JSON没有portfolio项，故不会在这一点报错，但它单独运行与带latest运行会写**同一TARGET名**而约束数不同。两个local旗标都出现时选v2数据。

latest的早期B三行从冻结表读取各448个psi和K系数；该入口不重新证明表的生成。新增portfolio将多个合法末位查询用同一回复和非负权重共同定价；嵌套/重查询行保留同源后继关系。它们仍是有限的已选行，不是连续价格全闭包。后续账本中的5277行、2033列属于另外的条件实际B联合程序；不能改写为本源的5198行、1905列。参见[阶段点与未闭报价账本](../资源/显式回复主图的阶段点与未闭报价账本--资源.md)。

## 发现模式与精确核验模式

`build()` 返回列描述符、行名、Fraction矩阵、目标和归一化。无 `--verify` 时，将全矩阵转为浮点，逐行除以最大绝对系数（零行改除1），调用HiGHS最小化W，约束 $My\ge0$、$O(y)=1$、$y\ge0$，原/对偶可行容差均为 $10^{-9}$。status输出包含scope、success、status、浮点W、行列数、seconds。

只有求解成功且浮点W小于1/2才调用 `cl.exact_point`：按浮点支持及近活跃行选方程，用Fraction高斯消元恢复点，再对恢复值完整核非负、归一化、所有行和W小于1/2。此过程可能因支持/秩/恢复失败而抛异常；成功写 `TARGET_exact.json`，随后写status并加 `exact_verified`。它不输出精确对偶，因此成功只证明精确可行，不能将HiGHS的“最优”状态解释成该有理点的精确最优性。

`--verify` 重建矩阵，读取相应已有exact JSON列的weight，用Fraction检查非负、归一化、所有行非负、计算W等于保存W且小于1/2，打印后返回，不写报告。原函数通过zip使用位置，**没有检查列长度或非weight描述符一致性**。当前新增[接口检查](../../tools/evidence/combined-branch-master-program/check_interfaces.py)补核保存点与被导入旧布局的全部1905个非weight描述符严格相同、各坐标非负、O和W；这是保存布局比较，不能冒称第二套独立全图生成器。

## 当前执行证据、相关对象与接续

原入口在2026-11-01隔离运行，Python3.12.14、NumPy2.3.5、SciPy1.17.0，assert启用；墙钟44.107秒，建图打印31.751秒，exit0、stderr空。[执行事件](../../tools/evidence/combined-branch-master-program/rerun/execution.json)、[原stdout](../../tools/evidence/combined-branch-master-program/rerun/stdout.txt)和[原stderr](../../tools/evidence/combined-branch-master-program/rerun/stderr.txt)保持实际字节。原始输出163B，SHA为 `e76d2385a3d1a715191dc52b37d76cc7dac6c0dd1466d709a407553e43de80cf`。

运行前后核了隔离环境中49份已取得冻结文件的大小及SHA，全部不变；这是**可用文件清单**，不是49份均被默认入口加载的声明。共享保存包持久保46份原件，另引用父报告中的master大点；两个只供其他程序独立运行的大点不在本包重复。9份扩展专用代码/数据属于静态阅读，不由本次默认运行加载。根 `work.py` 副本只供上溯定位目录，既未导入也未执行；重现不需要仓库凭据。运行组织代码及[复现说明](../../tools/evidence/combined-branch-master-program/README.md)将这些边界分开。

[当前接口结果](../../tools/evidence/combined-branch-master-program/interface-audit.json)另核47份持久或共享原件、1905列布局、702行数据来源计数、旧权重非负及查表域；不再次生成全图。原点的完整字段、联合状态和重叠界审计见[联合必要图有理点](../计算/索引主题与实际B分支的联合必要图有理点--计算.md)。本轮的5108行复跑属于本程序证据，不冒为父数据页另一套独立矩阵实现。

这份原点后来被阈值生成器取作旧hist/R边际，而pair点修改了73组Z边际；**本次旧master5108通过不传递到修改后的pair Z**。[阈值物化程序](完整156主题的阈值物化收益矩生成器--程序.md)和[六人行松弛障碍](../障碍/六人行松弛与真实SPE闭包--障碍.md)说明共同客户实现、真实目录全最佳回复与完整历史闭包仍须另核。

下一步可以修复扩展参数组合与列接口检查，并针对改变Z后的点重新核相应旧行；这些应作为新版本及新执行事件，不覆盖本冻结源码。若要从局部行系统进到反例，需同时给出完整共同客户类型、所有目录主题及完整历史SPE；若要给普遍下界，则需跨越固定16支持和有限价格族。阶段三可据上述已读证据分别建立来源、实现、必要行合账、有限核验及后继构造使用关系，本轮不搬入旧图。
