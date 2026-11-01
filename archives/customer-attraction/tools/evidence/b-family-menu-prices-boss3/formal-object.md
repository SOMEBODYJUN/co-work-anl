---
id: "customer-attraction/b-family-oracle-and-four-menu-price-original-point"
kind: "computation"
type_tag: "计算"
title: "实际末主题分支分离器与四菜单补价原点核验"
status: "complete"
truth_status: "new5692-point-exactly-replayed; old5664-point-new-price-violation-exactly-separated; coefficient-LP-float-only"
review_level: "六主源全文/全字段实读；原5692矩阵同实现复跑；独立标准库重算全部列身份、条件边缘和新28行；未新增外审"
scope: "六人共同目录完整历史纯SPE的必要行；固定16个旧hist支撑的两个4849列点；源1至4的分支分离/系数模板"
summary: "保全单枝有理分离接口、独立隐藏系数LP、最大M根170行和四菜单28价；同W的5664与5692点有214个质量差异，前者恰违反source2菜单末价，后者全矩阵有理通过；均非完整SPE。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_2/B_family_oracle.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_2/B_menu_prices_master.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_2/all_menu_prices_exact.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_2/branch_family_lp.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_2/maxroot_identity_exact.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_2/maxroot_identity_master.py"
---

# 对象范围与本批实际确认

采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)：有限单位客户、有限非空共同目录、六名单位提供者观察完整有序历史依次选择，客户在终局覆盖者间均分。空主题、重复选择、零客户和任意离轨平局均保留。$W$ 是实际根覆盖，$K=\max_{S\in\mathcal S}\lvert S\rvert$；六个允许重复的合法比较主题 $T_1,\ldots,T_6$ 的并集覆盖记 $O$，只有取真正最优元组时才称 $O=\operatorname{OPT}_6$。

本批将六份原源归入一个程序/计算对象：分离器、系数 LP、最大根构造器、四菜单补价构造器及其前后两个精确输入点。数学必要行不由数值输出创造；真实行合法性、有限点可行性、浮点模板最优值和完整 SPE 是不同结论。一般与恰六人 half 仍未由这里闭合。

原字节、全部描述符和全部有理质量均保在[证据目录](../../tools/evidence/b-family-menu-prices-boss3/README.md)；[源清单](../../tools/evidence/b-family-menu-prices-boss3/source-manifest.json)逐项给源 ID、大小、SHA-256、双冻结提交和 primary/related 区别。旧结论及历史缺输入边界见[三源共同容量上包络](../引理/实际末主题三源分支的共同容量上包络--引理.md)、[旧回复直方图的条件联合](../引理/真实末主题分支与旧回复直方图的条件联合--引理.md)、[原补价时序审查](../审查/指定四菜单补价点与旧未闭点的审查时序--审查.md)。本页补上后来真正取得原点与代码后的核验，不倒改那些页面当时“未读/未跑”的事实。

## 同一策略上的分支行，及分离器的实际输入前提

记实际主题 $A_1,\ldots,A_6$，$B=A_6$。在实际位置 $i$ 的原有序前缀强制改为 $B$，后继沿同一份原 SPE，形成

\[
P_i=(A_1,\ldots,A_{i-1},B,H_1,\ldots,H_{6-i}).
\]

实际源差 $F_i=u_i-v_i(P_i)\ge0$，但强制者在新枝上不被假定最优；互斥枝收入也不被换成实际 $u_j$ 或合并成 $W$。分支最后两位只有在 $i\le4$ 时都是未被强制的真实后继，这正是下面菜单行合法性的前提。

固定该真末两人前负载 $p$、末两位会员 $x,y$，六个真查询的比较会员重数 $d$、新真末回复重数 $\ell$，令 $D=(p+1)(p+2)$、$h=\sum_j1_{T_j}1_{R_j}$。从[真实菜单引理](../引理/真实末两人菜单交集消去--引理.md)的 $S,Z,V$ 得

\[
M=S+V/6,\qquad
M_x=6\frac{x}{p+x+y}-\frac d{p+1}
+\frac{d\ell}{6(p+1)(p+2)},\qquad
Z_x=6\frac y{p+x+y}-\frac\ell{p+x+1}.
\tag{1}
\]

$M,Z$ 各为非负**整行**；$G=M+Z/12$ 才是原统一组合。同索引交集 $h$ 在 $S+V/6$ 中消去，不能把 $M_x$ 或某条安全行的单客户贡献要求为非负。零分子的份额取零，其余分母恒正。

两个模板还列出实际各角色对具名 $H_j$ 的安全查询、真后继对实际/本枝具名主题的安全查询、各真后继对六 $T_j$ 的平均安全行，以及 $K-\lvert H_j\rvert\ge0$。安全分母是该**原查询节点**已有客户负载加剩余人数；偏离后的后继允许改变。内部查询的收入和前缀均取 $P_i$，不取实际路径。分离器所导入 `max_branch_lp.branch_rows` 与另一个 `branch_family_lp.branch_rows` 不是同一 Python 函数：前者还接收最大主题位；本分离器仅令该位为 dummy 0。dummy 查询行因而退化为“真实收益非负”，不要求目录必须有空主题。

`B_family_oracle.py` 的有效六人合同应明确限制：

- `source` 是一基实际源，$i\in\{1,2,3,4\}$；
- 质量键是六位 $a\in\{0,1\}^6$ 与 $d\in\{0,\ldots,6\}$，输入质量及 $K$ 非负；
- $K$ 使用共同目录的同一个最大大小，不能为不同枝免费增加；
- 正分母参数和非负容差按接口本义使用。

原函数没有显式检查这些范围。特别它也会机械接受 `source=5`，但此时式(1)的第五位已被强制，不能从 SPE 得到它的 $M\ge0$；因此不认证该范围外返回的切为真实博弈必要式。默认系数 LP 及已交付三枝实际只用源1至4或2/3/4，不受这一未检查前提影响。本批保原字节，未擅改原接口。

## 有理分离器为何能脱离浮点对偶成立

对任意非负有理行权 $\lambda$，令 $f_\lambda(a,d,h,\ell)$ 为所选真行的逐客户组合，$\kappa$ 是所有 CAP 权之和。程序计算完整的448项表

\[
\psi_\lambda(a,d)=
\max_{\substack{h\in\{0,1\}^{6-i}\\\ell\in\{0,6\}}}
f_\lambda(a,d,h,\ell),\qquad
\kappa=\sum_{\text{CAP行}}\lambda_{\text{CAP}}.
\tag{2}
\]

隐藏位逐客户独立最大化是对真实策略关联的放宽；因式子对 $\ell$ 仿射，端点0/6覆盖真实整数回复数。真实隐藏状态落在该域，故对实际可见质量 $t_{a,d}$，

\[
\kappa K+\sum_{a,d}t_{a,d}\psi_\lambda(a,d)
\ \ge\ \kappa K+\sum_x f_\lambda(x)
\ \ge0.
\tag{3}
\]

上包络必须取 max；取 min 会反转所需方向。任意非负权都给式(3)，所以权不必继续满足数值对偶约束。

`separate` 先对输入可见支撑的隐藏完成解“最大共同余量”浮点 LP。若余量达到 $-\text{tolerance}$，返回 `None` 只表示该数值容差下没有分离，**不是精确可行完成证书**。否则将非正对偶边际取反、截为非负，并以默认分母 $10^8$ 舍入；随后用 `Fraction` 重算全部448个最大值，并要求式(3)在所给有理点上严格负，失败便抛异常。正是“非负有理权＋完整 max 表＋精确负点值”使一个成功返回的切可独立核验，而不是 SciPy 的成功字段。浮点输入通过 `Fraction(str(value))` 解释为其十进制表示的精确质量，不恢复原浮点背后未给出的有理数。

本批完整读该接口及真实行解码，未调用 `separate` 搜索新切，也没有把另页三组已保存整数权冒称本接口本次新输出。该程序依赖的 `max_branch_lp.py` 作为 related 原件保全，由同批另一清洗线处置。

## 独立隐藏系数 LP 的本次原入口

`branch_family_lp.py` 自行建立系数模板。默认 $n=6$、源为1/2/3/4；可见实际会员64种，比较数只需 $d=0,1,6$，每枝隐藏全位型与 $\ell=0,6$。每个可见格有各枝自由上包络变量 $t_i$；所有真实行乘子非负，并共同选择 $\beta$。实际 CAP、枝 CAP 和安全行 $6u_j-K\ge0$ 的净 $K$ 系数另以一条共同预算约束为不大于零。

给定实际位，$d=0$ 的覆盖指示为0；$1\le d\le6$ 时为1。各固定隐藏型系数对 $d,\ell$ 双仿射，max 后对 $d$ 凸，故在 $d=1,6$ 检查上界可用端点插值覆盖中间整数；$d=0$ 必须单列。这解释了其192个可见角格与分离器448表的区别，并非遗失了中间比较数。

本次原默认入口确实运行一次，得到23425条不等式、1087变量，HiGHS报告 optimal，

\[
\beta\approx2.3266306390622455.
\]

完整浮点活跃乘子保在[原 stdout](../../tools/evidence/b-family-menu-prices-boss3/replay/branch-lp-stdout.txt)；默认源1/2未活跃，源3/4和若干实际行活跃。[运行记录](../../tools/evidence/b-family-menu-prices-boss3/replay/branch-lp-execution.json)给原命令、环境、7.13秒和exit0，stderr空。此值与[既有探索账本](../资源/末主题嵌套查询的内层激励与有限线性探索账本--资源.md)所报约2.3266306391一致。本批没有有理恢复并验证这些系数，也没有精确 Farkas 证书，因此既不将它认证为严格福利上界或精确模板最优值，也不将大于二解释成游戏坏比率或 half 反例。

## 最大主题根身份的170行与四菜单的28行

`maxroot_identity_master.py` 在三B枝联合图后显式保留一个共同最大主题 $M$。其真根枝为 $(M,H_1,\ldots,H_5)$，16个旧hist各拆 $M\in\{0,1\}$、五隐藏位与 $\ell\in\{0,6\}$，共2048列。$M$ 在客户上的会员不能只用免费标量 $K$ 代替：另有

\[
\sum_{\text{最大根状态}}M_x\,y_x=K
\tag{4}
\]

的双向等式，且每个旧hist的该族状态质量和等于原hist质量。新真行包括103条本枝行、6条实际角色查 $M$ 的安全价、27条本枝/旧 $T_j,B_j,C_j$ 双向查询；再加16条边缘和式(4)的正反方向，计 $103+6+27+2(16+1)=170$。27条由五真后继各查三旧词共15条，以及旧 $B_j,C_j$ 分别查 $M,H_1,\ldots,H_5$ 共12条构成。它保留同一旧hist相关性，没有混用各互斥枝总收入。

`B_menu_prices_master.py --all-families` 识别的是四个**指定**菜单：actual2/3/4强制 $B$ 的三枝菜单，及上述最大 $M$ 根枝菜单。对各菜单真回复 $Y_1,\ldots,Y_6$，$\ell_x=\sum_j1_{Y_j}(x)$；令实际位置 $a$ 之前的负载为 $L_{a-1}(x)$。原完整 SPE 的实际安全查询平均和共同目录容量给

\[
u_a-\sum_x\frac{\ell_x}{6[\,7-a+L_{a-1}(x)\,]}\ge0
\quad(a=1,\ldots,6),\qquad
K-\sum_x\ell_x/6\ge0.
\tag{5}
\]

$a=6$ 是实际末位的精确普通主题价；其他位置允许偏离后真实后继改变，只使用安全分母。式(5)对 $\ell$ 仿射，保持原端点凸化。构造器在每族的状态列放实际份额减新回复平均成本；因为各族逐hist边缘等式成立，实际份额求和恰为同一个 $u_a$，不会凭复制条件状态多算实际收入。

因此本次图的具体层次为

\[
5180+314+170+28=5692,\qquad1905+896+2048=4849.
\]

三B枝314行、旧基图5180行见[单枝与三枝精确点](实际末主题单枝与三枝条件联合的精确点--计算.md)。`--all-families` 不声称对全目录所有新回复做无限闭包；尤其未自动增加新 $H/M/Y$ 与旧 $R/Z$ 的全部乘积、全 $Z\to Z$ 或全部 PAIR 关系。加入这些关系须进一步细分共同条件状态，不能免费继承只以旧hist条件联合的论证。

## 两个大JSON全部字段与4849列的实际身份

两份输入都按完整 JSON 解析并保每一列原字节，未抽取成只有header。顶层 `scope` 限定固定16hist必要图；`O/W/strict_half_gap` 是下面的精确标量；`verified_rows/minimum_slack` 是各自作者报告；`positive_columns` 与本批实数正质量计数相符。`base_rows=702`、`first_raw_rows=37`、`additional_index_class_rows=100` 来自旧 exact_point helper 的固定元数据，不是将新5692行重新拆成这三个块，不能将三数相加冒称新矩阵大小。

| 列种类 | 全部列数 | 5664点正列 | 5692点正列 | 保存的语义字段 |
| --- | ---: | ---: | ---: | --- |
| K | 1 | 1 | 1 | 共同最大大小质量 |
| hist | 16 | 10 | 10 | actual六位、比较数d、八格旧 $(t,b,c)$ 重数、客户质量 |
| joint-reply | 582 | 79 | 84 | 旧hist编号、族/对角/两旧词的group、非零 $(R,Z)$ 状态、质量 |
| overlap | 1306 | 82 | 80 | 当前hist编号、两group、松弛共同R交叠质量 |
| actual-B-family-state | 896 | 57 | 61 | source2/3/4、当前hist、全部真后继位、回复数0/6、条件质量 |
| maximum-root-family-state | 2048 | 23 | 25 | 当前hist、M位、五真后继位、回复数0/6、条件质量 |
| 合计 | 4849 | 252 | 261 | 每个weight均按Fraction完整读取且非负 |

八格旧hist按 $(t,b,c)\in\{0,1\}^3$ 字典序，重数和为6，$d=\sum t$。582个 joint-reply 列是194个group的 $(0,1),(1,0),(1,1)$ 三状态，隐含 $(0,0)$ 质量为hist减三状态和，必须非负。`hist_column_old` 仍是旧闭包前编号，不能直接当现4849列索引；本批按全部旧1905描述符及原映射核对。overlap只保存两 $R$ 事件的非负共同量及两个边缘上界，不等于已经给出全部 $R/Z$ 的共同分布。

独立标准库核验逐一检查194个joint上界、2612个overlap边缘上界、三B枝和M根共64个hist边缘、全部新2944列的精确生成次序，以及式(4)、实际主题大小CAP和式(5)的全部28行。原继承1905列的所有描述符与已保存基图一一相同；新2944描述符按源码全域重建，避免原 `--verify` 只用zip而未检查长度/描述符的接口盲点。检查方法和两点全部新价精确值位于[独立程序](../../tools/evidence/b-family-menu-prices-boss3/audit_point_structure_and_prices.py)、[5692点报告](../../tools/evidence/b-family-menu-prices-boss3/replay/structure-and-prices-audit.json)和[5664点报告](../../tools/evidence/b-family-menu-prices-boss3/replay/maxroot-structure-and-prices-audit.json)。这些独立检查没有重写全部继承矩阵。

两点共有

\[
\begin{aligned}
O&=1,\\
W&=\frac{1905769909616898376137238949200623274593168205}
{3898693540058852735821709960049703833207552519}
\approx0.4888227017679696,\\
K&=\frac{315077695104813902155411870991625199707785785}
{1299564513352950911940569986683234611069184173},\\
O-2W&=\frac{87153720825055983547232061648457284021216109}
{3898693540058852735821709960049703833207552519}>0.
\end{aligned}
\tag{6}
\]

所以 `strict_half_gap` 实际表示 $O-2W$，不是 $\tfrac12-W$。这仍是必要系统中的有理点；缩放质量成单位客户整数也不会自动补齐合法目录、全历史策略与所有真实最优性。

## 同W不等于同一完成：前5664点确被新末价切开

原 `maxroot_identity_exact.json` 为1440157B、SHA-256 `d3c456a03806aef08378e96f89387b83d77161081a260b3764b8aa8f8097d43a`；补价后 `all_menu_prices_exact.json` 为1441208B、SHA-256 `46e52c1cec4a5cac3e6d7fe3bbe8d227cd663e428ca7f4e955182343eedb418e`。前者报告5664行、252正列，后者报告5692行、261正列。

[完整点比较](../../tools/evidence/b-family-menu-prices-boss3/replay/point-comparison.json)确认：全部4849个描述符逐项相同，$K$ 及全部16个hist质量逐项相同，$W$ 也完全相同；但214个隐藏质量改变，分别为joint-reply70、overlap52、三B枝状态52、M根状态40。这不是将相同向量贴上不同header。

把新28行独立精确作用于旧5664点，恰有一条为负：source2的 $Y$ 菜单在**实际第六位**的普通价，

\[
-\frac{10026222041073744940623089144705030946499310342386311577}
{652887283919685192981664984788241385973843146740115858240}<0.
\tag{7}
\]

在新5692点，同一条余量恰为0；全部28行均非负，其中24条严格正、4条为零。四个零行是source2实际第六价、source2菜单CAP、source4实际第六价及最大M菜单CAP；每条完整有理余量均保在独立报告，不以小数容差替代严格符号。

这补足[旧时序审查](../审查/指定四菜单补价点与旧未闭点的审查时序--审查.md)“紧前具体资产未取得”的证据边界：现在已取得该5664点并核同W与隐藏重排，不能倒填为旧审查当时已经核过。相邻5494三B枝点也有同W，但其source4的实际2/3/4/6价和CAP仍负，source2/3七价全正；这是[另一份单枝/三枝核验](实际末主题单枝与三枝条件联合的精确点--计算.md)的实际结果，本页直接交叉引用，不冒作本页重新运行。5494、5664、5692分别是不同列范围或不同隐藏质量的固定支持完成，同一个W不传递新增约束的可行性。

## 本次真实运行、依赖与未认证范围

新5692点实际以原 `B_menu_prices_master.py --all-families --verify` 执行一次，未重新求 LP。47份已归档冻结基图依赖先以原材料化工具核SHA恢复到clone外独立运行树，再覆盖本批原代码/精确输入；根 `work.py` 仅是旧模块找根用的无执行注释标记。真实[执行记录](../../tools/evidence/b-family-menu-prices-boss3/replay/verify-execution.json)、[stdout](../../tools/evidence/b-family-menu-prices-boss3/replay/verify-stdout.txt)、[stderr](../../tools/evidence/b-family-menu-prices-boss3/replay/verify-stderr.txt)保留5692行、4849列、式(6)的精确 $W$、最小余量0、62.08秒和exit0；普通Python断言启用。stdout的构造时间约31.89秒包含原全图重建。

这是原全矩阵的**同实现复跑**，并非第二套5692行实现或外审。独立标准库程序补了全列身份、全部质量字段和新增28行的另一实现；它没有据此认证全目录闭包。前5664点没有为本批再次长跑其全矩阵，原5664行/min0仍准确保为作者冻结报告；其全部描述符/质量、式(6)、所有条件边缘与新28行已本轮实算，式(7)是本轮新核而非header转述。

`maxroot_identity_master.py` 的独立优化入口还会写 `maxroot_identity_exact/status.json`，本批没有运行它；它的 `build` 确由上述5692原核验调用。`B_family_oracle.py` 无默认命令行入口，本批未制造一次不存在的原oracle搜索事件。浮点 branch-family 默认入口与精确 verify 入口各自只执行一次，输出角色分开保存。[既有父方checkpoint复放说明](../资源/R5662研究checkpoint的版本清单与有限复核--资源.md)中的历史5692通过也是历史事件，本页不将它冒作当前执行日志。

这些资产能用于精确重放指定必要图、定位未付的新主题价格及复用合法有理分离接口。原量词不要求计数型策略或统一平局；本必要图也没有枚举完整有序策略树。没有交付完整 SPE 反例、普遍六人half证明、严格最优福利常数或外部新颖性认证。对象间真实行、实现、版本更新和局部否定关系已在正文解释，第三阶段再按其精确语义建边。
