---
id: customer-attraction/fixed-actual-path-full-menu-milp-diagnostic-and-rational-proposal-postcheck
kind: program
type_tag: 程序
title: 固定实际路径全菜单的MILP诊断与有理提案后核
status: original-3948B-code-and-three-records-fully-read; no-new-MILP
truth_status: stated-finite-E-menu-formulation-valid; global-exact-optimality-not-certified
review_level: 三primary8302B及唯一36客户真实输入全文；四规范模块同SHA阅读复用；完整菜单/可信L数学比较
summary: p与每位置psi连续，离轨孩子可信计数onehot选择，actual列固定；bigM实现同时可拼菜单。任一incumbent后取合法候选并Fraction重算，不等全局上界；48是访问路径数，CLI无argparse/输出文件，raw needs-attention与Root零差恢复分开。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/menu/menu_continuation_diagnostic.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/menu/menu_continuation_diagnostic.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/menu/README.md
---

# 同一个U候选、完整m槽背景与E域

原3948B代码针对[完整菜单包络](../资源/固定实际路径的可信门槛与全菜单包络--资源.md)中的U：每份完整历史纯SPE、每个独立query分布p，应有Σ_i min_A G_p(Z_i(A))≤W。Z_i(A)是在actual前缀强制A后、沿同一完整策略完成的**完整m槽**终局；辅助查询额外插入，G_p(z)=Σ_t p_tK_t(c_z)、K_t(c)=Σ_(x∈t)1/[1+c_x]，不是实际当前收益，也不是删掉当前的m−1尾静态背景。

模型仍有限单位客户、有限非空共同目录、单位玩家，保所有有序history/重复/离轨平局/空主题及零客户。固定确可实现的actual有序path a、当前利润u_i(a)及W(a)。每个真正离轨孩子(h_i,A≠a_i)可选全部可信子SPE终局z，但须当前利润u_i(z)≤u_i(a)；actual行动列只能保a。不同首次离轨子树互不相交，所有选项可以同时贴成一份保actual的完整SPE。这个已证拼合是代码候选域的依据，不是U的预算证明。

程序用规范`sol.outcomes(prefix_counts+A)`表示全部可信孩子终局**计数**，再用`topic_payoff(A,z)≤payoff[i]`筛选。由单位对称收益只依终局计数，每个保留count都有有序子SPE实现；并不要求不同同计数历史使用同一选择器。当前forced动作不必在原节点最佳，其当前收益上限由E保证；真正后继IC由可信子SPE承担。非根孩子终局可能不属于根SPE，所以`kval`从根结果开始后又补入每个孩子的新终局，不能只查根可实现集合。

# 真实变量和bigM如何实现完整菜单

`optimize_path(ins,sol,path,time_limit=5)`先准确求actual计数q、payoff和W，对每个离轨(i,A)形成非空集合E_(i,A)的count候选。变量依次为k个p_t、m个ψ_i和每个候选z的binary y_(i,A,z)。原`n`局部变量是主题数、`m`为玩家数；不是把主题/玩家相混。

理论形式是

\[
 p_t\ge0,\quad\sum_tp_t=1,\quad0\le\psi_i\le B,
 \quad y_{i,A,z}\in\{0,1\},\quad\sum_zy_{i,A,z}=1,
\]

\[
 \psi_i\le K(q)\cdot p\quad\forall i,
 \qquad \psi_i\le K(z)\cdot p+B(1-y_{i,A,z})
 \quad(A\ne a_i,z\in E_{i,A}),
\]

最大化Σ_iψ_i−W。源码以min −Σψ求解，返回后再减固定W；固定path时两者同最优。B取所有已收集K分量的浮点最大值再加1，固定36客户数据足以覆盖所有合法p列值。对未选y0，因ψ≤B且Kp≥0，条件式无额外约束；选中y1恰成ψ≤Kp。每个(i,A)恰选一可信count，故最大ψ就是其全部行动列（含actual）的最小G。两点有理提案的合法性另作显式解析展开，见[计算对象](../计算/三十六客户全菜单诊断的两份完整提案--计算.md)。

这实现的是同时最不利E菜单及query的有限优化，不是把H=max_E偷偷改为最低当前收益L。E已经筛actual cap，H所最大化的是G；L最小化的是当前玩家利润，两对象不可替换。程序也未优化SM/TB或给菜单的全树共同W付款。

# MILP状态与返回提案的后核

系数K先用Fraction构造，再转浮点稀疏矩阵交SciPy `milp`；每path默认time_limit5秒、mip_rel_gap10^−8。若`res.x is None`仅返status文字；否则**不要求res.success/全局最优**便处理已有向量。它将前k个浮点坐标用分母上限100000恢复Fraction，再除其和得到p；每个离轨孩子用对应binary坐标argmax选一个原候选count。

因此即使浮点binary有容差，argmax仍只选一个真正属于E的count，不会造不存在的孩子。重新以Fraction遍历actual和每个所选列，计算每ψ_i的真正min及gap=Σψ−W，丢弃求解器的ψ坐标作为最终数值。若p确为非负概率，此返回值是一份可拼完整菜单的有理提案，不需另证明浮点binary恰整数才使该提案存在。

源码没有显式断言恢复p_t≥0或除前总和>0；任意将来阳性仍须核这两个概率条件。当前两原提案p分别纯主题5和四个1/4，非负归一可直接读出，后文显示其可信完整菜单及精确score。归一p恢复可能降低原浮点目标，源没有把该损失变成全局误差界。

`Optimal`/HiGHS Status7是浮点solver文字，不能取代精确对偶/上界或全部候选检查证书。若未来得到合法正gap，只需精确检查该一份见证即可反U，不需MILP全局最优；负gap或没有正提案则不证明U，甚至不证明这个固定输入的最坏有理值非正。

# 外层遍历、JSONL和计数口径

main从`sol.ordered_outcomes()`访问每条可实现有序actual path；这不是枚举全部完整策略，每path的离轨选择由MILP优化。每次调用之后done加1，即使没有incumbent也加；只在ans含numeric_gap且其**浮点值**大于旧best时打印一条new_best JSON。best排序用float(gap)，不是有理数精确排序。

若已有best的numeric_gap>10^−7即停，否则继续。最终再打印candidate、输入路径、paths_checked、best及finite scope。原JSONL的48表示访问了48条actual路径，不能说48个MILP均成功/Optimal；文件只展示两次改进的status，其余路径没有逐件日志。原36客户游戏的48可实现路径可由末位/倒二解析分类独立看出，后文给出，仍不让这48变成48份运行证书。

原2386B文件恰三行JSON：done1提案、done7提案、最终对象重复done7的best；不是三个独立发现，也不是全48份结果。源码只stdout打印JSONL，没有写该文件的语句。源文件名和`source`字符串不补造实际shell重定向、运行时长、解释器/solver版本或当时源码SHA。

# 必要输入、依赖与CLI

唯一游戏数据来自sys.argv[1]的JSON，接受直接Instance字典或外层`instance`。原日志指定`examples/customer_attraction/aggregate_theta_failure.json`，当前已全文读取冻结输入及18个客户块，hash绑定已发表原bytes。不需要外部策略证书：程序自行求可信结果/有序路径。规范四模块model/exact/certificate/__init__共25475B此前全文已读，本次核同SHA复用；另依NumPy、SciPy milp/Bounds/LinearConstraint和sparse.lil_matrix，不运行或推定当前版本。

代码有main guard，import只加载依赖/定义，不调用MILP。它不插入项目根sys.path，运行环境需可导入规范包；这不同于前一full-history攻击脚本主动加根路径。CLI没有argparse/help/output/time_limit参数，只取第一个位置参数作输入文件，额外argv未使用；`--help`是文件名，不是帮助模式。函数可直接给另一个time_limit，但本次没有调用。正常输出可能是多行进度加最终JSON，文件不存在时读入即失败，不自动生成目录或保存报告。

本批原码import、MILP、solver、IC/菜单/路径扫描、新数值程序均0。对两已报提案的下面分析只用明确输入和显示count列的解析式，不冒新执行成功。原source读取及目录约束不因历史needs-attention而省略；raw回执与Root独立恢复证明分别保在[证据](../../tools/evidence/full-menu-milp-and-rational-proposals-primary/README.md)。
