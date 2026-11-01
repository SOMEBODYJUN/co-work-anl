---
id: "customer-attraction/actual-fourth-B-three-tail-projection-program"
kind: "program"
type_tag: "程序"
title: "实际第四步B分支的三人尾投影程序"
status: "complete-code-reviewed; original-export-byte-exact; raw-menu-reconstruction-passed"
truth_status: "universal-necessary-projection-and-one-old-margin-separation; not-half-theorem"
review_level: "full-code-certificate-and-relevant-input-read; one-isolated-original-run; exact-21504-state-independent-reconstruction"
scope: "六人完整历史SPE中实际第四位强制实际末主题B的真三人尾；448可见系数格和指定旧点边缘"
summary: "保3075B标准库投影器、全部448精确系数及旧点输入；原--export一次逐字节重现证书，从S/Z/V重建21504含交集状态全等。最大隐藏投影给普遍必要行，负值仅排指定旧边缘；联合图调用table不读旧点、不导入发现LP。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_2/tail3_B_projection.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_2/tail3_B_projection.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_2/tail3_B_projection.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/audit_tail3_B_projection.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_2/tail3_B_projection_certificate.json"
---

# 原程序与本轮结论

主源 `0eede36b323de30ee462` 的[原程序](../../tools/evidence/tail3-B-projection-program/original/tail3_B_projection.py)为3075B，SHA-256为 `63677e14e8c9f257b32f385642bfdf47c71932ce7b251c5970013cf1993c6d01`，两个冻结提交字节相同。它将同一完整策略中一条实际第四位偏离分支的八族真关系作非负整数组合，消去隐藏会员，生成448个精确有理系数，再将该行作用于一份指定旧点的实际会员/比较重数边缘。

本轮完整实读源码、4806B数学稿、原审查稿及1416B父方审计源码；全部448系数按64个实际六位模式、每行d=0…6逐项读完。原 `--export` 入口在独立布局只执行一次，新36617B证书逐字节等冻结原证书；另从S/Z/V未消交集形式独立重构21504个含交集状态，所有系数及旧边缘负值一致。普遍必要关系的合法性来自下面真节点证明；有限遍历核的是系数展开，不是穷举所有游戏或策略。

既有[隐藏上包络引理](../引理/实际末主题三人分支的隐藏上包络与主图合账--引理.md)已保解析证明，当时明示未读原程序及448表。本页补其程序、实际输入、全表与本轮执行，不将旧阅读时态改写成此前已运行，也不将本页程序运行重复记成新的数学发现。

# 同一策略的实际第四位B分支

在[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)中，取任意有限单位客户、有限非空共同目录、恰六名玩家及覆盖所有有序历史的纯SPE \(\sigma\)。实际路径是 \((A_1,A_2,A_3,C,A,B)\)，其中 \(B=A_6\)，实际收益为 \(u_1,\ldots,u_6\)。在原前三步 \(h=(A_1,A_2,A_3)\) 后强制第四位改选合法主题B，原策略给真实尾 \((B,Q,R)\)。

任取六个合法比较主题 \(T_i\)，允许重复、空主题；令 \(Y_i=\sigma_6(h,B,T_i)\)。Q、R、各Y均来自同一策略，所有真实历史相同处必须保持策略一致。B不是另一Ti分支的 \(B_i\)，Q/R也不能与其它分支同名字母认作同主题。强制第四位B及强制第五位Ti不被假设为新节点的最佳行动；只使用其原源IC和实际后继最佳回复。

对客户x记固定B后的过去负载
\[
p_x=\sum_{j\le3}\mathbf1_{A_j}(x)+\mathbf1_B(x),\qquad
U_p(X,Y)=\sum_{x\in X}\frac1{p_x+1+\mathbf1_Y(x)}.
\]
真两尾收益 \(v_Q=U_p(Q,R),v_R=U_p(R,Q)\)。下面八族总slack非负；单个客户系数本身可以为负。

| 族 | 总量与来源 | 整数权 |
| --- | --- | ---: |
| F | \(u_4-\sum_{x\in B}1/(p_x+\mathbf1_Q+\mathbf1_R)\)，实际第四位改B的真实IC |3360|
| G | 下面三类真菜单IC之和 \(S+Z/12+V/6\) |96|
| H2Q | \(u_2-\sum_{x\in Q}1/(5+\mathbf1_{A_1})\)，实际第二位安全偏离 |660|
| H2R | H2Q中将Q换R |595|
| H3R | \(u_3-\sum_{x\in R}1/(4+\mathbf1_{A_1}+\mathbf1_{A_2})\)，实际第三位安全偏离 |220|
| LQ | \(u_6-\sum_{x\in Q}1/(1+\sum_{j\le5}\mathbf1_{A_j})\)，实际末位对Q的精确报价 |522|
| LR | LQ中将Q换R |522|
| E | \(6v_R-\sum_xd_x/(p_x+\mathbf1_Q+1)\)，真末位R逐一查询六Ti |108|

其中 \(d_x=\sum_i\mathbf1_{T_i}(x)\)。H2/H3的分母只是偏离者连同其后所有剩余玩家都覆盖该客户时的上界，未冻结偏离后的行动；LQ/LR确实使用原实际末位收益，不能换成另枝R收益。

真菜单的三族为
\[
S=\sum_i[v_Q-U_p(T_i,Y_i)],\quad
Z=\sum_i[v_R-U_p(Y_i,Q)],
\]
\[
V=\sum_{i\ne j}[U_p(Y_i,T_i)-U_p(Y_j,T_i)].
\]
S由真第五位IC，Z由原真末位R把Yi作为合法查询，V由每个Yi在其Ti历史后的末位IC，故 \(G=S+Z/12+V/6\ge0\)。G不是第九份可随意独立使用的利润预算。全部系数权非负，因此
\[
J=3360F+96G+660H2Q+595H2R+220H3R+522LQ+522LR+108E\ge0.
\]
这里没有K容量项，也未把互斥分支利润合并成实际福利。

# raw函数的八个逐客户式和隐藏消元

实际会员位记 \(a=(a_1,\ldots,a_6)\)，\(c=\sum a_j\)，\(b=a_6\)，\(p=a_1+a_2+a_3+b\)，\(q=\mathbf1_Q,r=\mathbf1_R\)，\(\ell=\sum_i\mathbf1_{Y_i}\)。实际份额 \(u_{j,x}=a_j/c\)，零分子份额取0。原 `raw(bits,d,q,r,ell)` 返回与权字典同名的八项：
\[
F_x=u_{4,x}-\frac b{p+q+r},
\]
\[
G_x=\frac{6q+r/2}{p+q+r}-\frac d{p+1}
-\frac\ell{12(p+q+1)}+\frac{d\ell}{6(p+1)(p+2)},
\]
\[
H2Q_x=u_{2,x}-\frac q{5+a_1},\quad
H2R_x=u_{2,x}-\frac r{5+a_1},\quad
H3R_x=u_{3,x}-\frac r{4+a_1+a_2},
\]
\[
LQ_x=u_{6,x}-\frac q{1+\sum_{j\le5}a_j},\quad
LR_x=u_{6,x}-\frac r{1+\sum_{j\le5}a_j},\quad
E_x=\frac{6r}{p+q+r}-\frac d{p+q+1}.
\]
源码 `safe(num,den)` 只在分子非零时构造Fraction；在内部合法域中，分子非零保证相应分母正。其余分母恒正。它不是任意外部参数的通用域验证器；真正域由table的有限循环固定。

若保同索引交集 \(h_x=\sum_i\mathbf1_{T_i}\mathbf1_{Y_i}\)，可行区间为
\[
\max(0,d+\ell-6)\le h_x\le\min(d,\ell).
\]
令 \(D=(p+1)(p+2)\)，未消元的真菜单系数为
\[
S_x=\frac{6q}{p+q+r}-\frac d{p+1}+\frac{h_x}D,\quad
Z_x=\frac{6r}{p+q+r}-\frac\ell{p+q+1},\quad
V_x=\frac{d\ell-6h_x}D.
\]
组合G中的h项严格抵消，得到原raw公式。这解释为何代码只需d及ell，不应把它描述为假设Ti与Yi会员独立。

`coeff` 按固定八权求 \(J_x\)，`table` 给出
\[
\psi(a,d)=\max_{q,r\in\{0,1\},\ \ell\in\{0,\ldots,6\}}J_x(a,d,q,r,\ell).
\]
真实客户隐藏值包含在此扩大域，所以逐客户 \(J_x\le\psi\)，求和得普遍必要行
\[
\boxed{\sum_x\psi(a_x,d_x)\ge J\ge0.}
\]
必须取最大上包络；改取最小值会失去此推导。扩大域可以允许同一实际历史在隐藏表示中的不相容选择，这是放松必要条件，不是额外的策略独立性假设，也不声称每个最大点可由SPE实现。

可见域64个实际位模式乘7个d，共448格；隐藏q/r四种、ell七种。因 \(J_x\) 对ell仿射，固定q/r时最大值在0或6。源码每格仍分别枚举端点8态和完整28态并断言最大值相同，总16128次coeff调用，其中完整隐藏态12544；这些计数是局部系数状态，不是完整策略数。d的六个比较主题只需合法，不要求最优六元组。

# table接口、命令行及未做的输入验证

源码仅用Fraction、product、Path、defaultdict、hashlib和json，主入口另导入argparse；不导入发现LP、NumPy、SciPy或历史行生成器。导入会设置常量及 \(ROOT=\texttt{__file__.parents[5]}\)，但不会执行table或读旧点。固定祖先深度要求原路径层数，不能把代码随便放浅目录再称相同运行合同。

| 接口 | 实际行为 |
| --- | --- |
| raw、coeff | 按给定局部参数返回八系数或加权系数，不调用策略求解器 |
| table() | 从固定域重算448个Fraction，返回键 `(六位字符串,d)` 的dict；不读取证书或旧点 |
| verify_and_export(False) | 重算table，读取固定旧点，仅聚合hist的actual_bits/d/weight，断言投影严格负，返回不含table的证书字段 |
| verify_and_export(True) | 同上，并写源码同目录的tail3_B_projection_certificate.json；若目标已存在抛FileExistsError |
| 原CLI | 唯一选项--export；无选项时不写证书，仍算全表和旧点负值；最终打印不含table的JSON |

`verify_and_export` 读旧点不核其全部原约束，不使用new-reply列、K列或旧点W。它计算并导出输入SHA，而非先断言某个硬编码输入SHA。也不显式检查全部hist质量非负、总质量、表schema或原点元数据；当前包装器和独立审计增加的检查不能反写成原程序已有。

生成的八个顶层字段是status、weights、coefficient_domain、old_point_path、old_point_sha256、old_point_value、old_point_value_decimal、table，完整值见[原证书](../../tools/evidence/tail3-B-projection-program/related/tail3_B_projection_certificate.json)。status明示仅必要投影及旧点分离；域中包含64、d0…6、四QR、ell0…6及端点相等标志；table每项是actual_bits/d/psi。唯一浮点字段old_point_value_decimal仅作显示，严格负值断言使用Fraction。原输出没有保存最大赋值、完整策略、证明树或新福利界。

# 指定旧点的真实数据范围

唯一数据输入为[旧1033点](../../tools/evidence/tail3-B-projection-program/related/full_new_reply_closure_exact.json)，源 `9e51f2c756ebb1a91fbf`，56652B，SHA-256 `24a2f9fa7e7a47e26e065b41ada98e1788a5b448251fb8c1e881557c1f7c9f11`。原路径为 `research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/full_new_reply_closure_exact.json`。其211列为16个hist、194个new-reply和1个K，原scope已明示不是SPE、游戏或精确最优性声明。

本任务实读其全部元数据和16个实际被程序访问的hist记录；不把另外195列的全部数学语义或原1033行可行性记成已核。10个正hist按(actual_bits,d)合并为8个正边缘，全部d=1；总质量为1。八个投影系数为

| 实际六位 |000000|000001|000010|000101|001010|010001|100011|111100|
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| psi(a,1) |−204|−1086|57|594|8|−461/2|−5005/6|4631/4|

完整边缘质量及逐项贡献保在[当前独立报告](../../tools/evidence/tail3-B-projection-program/independent-audit.json)，其精确和为
\[
-\frac{76248331950086821053066283859725637}{10861094041779216693185920113322280}<0,
\]
约−7.020317811150833。故这个可见边缘不能完成为满足本小图真行的隐藏会员分布，更不能是完整SPE的边缘。它只排该指定边缘；旧1097/3889扩展边缘相同是已读作者稿的声明，本轮没有读取两扩展原件重新核身份。

# 当前原入口和独立重构分别核了什么

[一次运行包装器](../../tools/evidence/tail3-B-projection-program/run_original_once.py)先核源码、旧点、冻结证书三件SHA，复制到隔离目录的原相对路径；执行未修改源码 `python -B tail3_B_projection.py --export`，assert启用，不导入父方审计器或求解器。实际Python3.12.14、退出0、stderr空，新证书36617B，SHA-256 `4d34cd746ce35dd48827c9014a85106c5defac30fc5f1159ae6085d4fd8fa1df`，逐字节等冻结源。stdout906B恰是证书除table外的全部字段；输入前后字节不变，临时目录删除。实际路径、argv、时间和哈希保在[执行记录](../../tools/evidence/tail3-B-projection-program/rerun/execution.json)。本轮在写入开放前的clone外完成运行，随后按原字节归档证据，没有再执行一次来改记录路径。

[独立核验器](../../tools/evidence/tail3-B-projection-program/audit_raw_menu.py)不导入上述作者程序或父方审计器，从S/Z/V含h式重新枚举：12544个(q,r,ell)状态、21504个可行h状态，逐状态核交集抵消；448格的全域最大值、端点最大值及原表值完全一致，表顺序亦相同。另核旧16hist非负、桶数及d身份、总质量和8正边缘，重算上述严格负Fraction及显示浮点。该实现是知情读取后的第二实现，不称盲审或外审。

已读原1416B父方审计器也从S/Z/V枚举21504状态，但本任务没有执行它；原审查PASS保历史身份。本轮独立实现的结果不能被加成第三次独立原入口运行。原证书与本轮新证书同字节，两个来源用途仍分别留存。

# 联合图接口、后续范围与接续

同批完整读 `combined_branch_master.py`：其默认build在其它必要行后调用branch.table()，仅在hist列放psi，K及其余隐藏列放0，名称为actual-fourth-forced-actual-B-projection。它不调用verify_and_export，不读取本旧1033点，也不读已导出的448证书。因此该程序作为联合图依赖只需源码及标准库；不能把本CLI的旧点负值当联合图新点负值。

主图中同一实际六位/d字段允许将不同真实分支必要行合在同一个点，不识别plain B分支Q/R与Ti分支回复。旧5108联合点仍低于half，其W与另一5075点相同，不能把提升归因于本psi一行；本次联合图默认--verify由配套任务唯一执行，本页不重复或预报其结果。

[后续三源共同容量投影](../引理/实际末主题三源分支的共同容量上包络--引理.md)另含actual2/3/4的K成本；[条件联合与菜单报价](../引理/真实末主题分支与旧回复直方图的条件联合--引理.md)另保hist相关性及新Yi菜单价格。它们与本无K、固定actual4的八权投影不是同一条行，不能用当前448表的PASS认证新表或全部后继关系。旧弱702域不改善的浮点报告也不是精确全局最优证明。

可复用资产是纯标准库table接口、真节点八族推导、完整系数表和精确旧边缘分离。若改权、换源位置或加K，需重新证明相应真行并重算表；若加到主图，须重做同点联合核验。该程序没有新福利因子、完整策略或六人half结论。三级关系留后续阶段按本页来源、程序、计算、引理和联合图合同分别登记。
