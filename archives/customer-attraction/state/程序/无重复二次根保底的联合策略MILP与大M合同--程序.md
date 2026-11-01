---
id: customer-attraction/fresh-quadratic-root-floor-joint-policy-milp-big-m-contract
kind: program
type_tag: 程序
title: 无重复二次根保底的联合策略MILP与大M合同
status: complete-source-contract-and-frozen-report-review; no-new-MILP-run
truth_status: exact-encoding-explained; original-floating-incumbent-not-a-counterexample-or-global-upper-bound
review_level: all-4179-byte-source-and-1081-byte-report-full-read; 847-byte-entry-and-6513-byte-referenced-manuscript-full-read
scope: 固定1≤m≤p的有符号对称二次fresh辅助博弈；全无重复有序历史纯策略；首位静态余集保底问题
summary: 逐约束重建完整策略/终局收益传播/真实IC与θ见证，解析给261变量1116行和有效大M；区分单位盒正齐次根搜索与旧差至少1程序，原超时没有精确最优上界。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-731efdb50dd844178e597d804bdd4596/root_fresh/README.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-731efdb50dd844178e597d804bdd4596/root_fresh/joint_fresh_floor.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-731efdb50dd844178e597d804bdd4596/root_fresh/joint_fresh_floor.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-731efdb50dd844178e597d804bdd4596/root_fresh/joint_p5m3.json
---

## 原来源和确切辅助域

本对象承接847B新入口、4179B程序与1081B报告，共6107B。代码/报告此前在工作区根入口清洗时已经normal/fullread，本批正式认领后同SHA精确复用，没有重复show或求解。新入口全文确认原运行是p5/m3、45秒、261变量1116行、超时且数值零，并要求停止同规模重复扫描。相关[完整原报告](../资源/五标签三人fresh根保底的原始超时可行候选--资源.md)保所有15系数、26政策动作和每字段，原件/捕获见[证据](../../tools/evidence/root-fresh-MILP-original-and-timeout-three-primary/README.md)。

取标签P={0,…,p−1}，1≤m≤p。合法有序历史h中标签互异，当前只能选a∉h；辅助终局集合S大小m，选a者利润

\[
f_a(S)=\alpha_a+\sum_{b\in S\setminus\{a\}}\beta_{ab},\qquad\beta_{ab}=\beta_{ba}.
\]

α和β允许任意符号。它是二次子集势的边际，**不是**单位客户输入；当前原CAG仍允许重复、空覆盖、同覆盖异标签、零客户及全部重复离轨历史。辅助的静态余集数为

\[
\theta_{p,m}=\min_{H\subseteq P,\ |H|=m-1}\max_{a\notin H}
\left(\alpha_a+\sum_{b\in H}\beta_{ab}\right).
\]

H先固定，query必须在H外。它不是原CAG的可重复背景安全值vₘ、末位θ_CAG或实际分数负载M。已有[辅助逐人候选](../候选/对称二次无重复辅助博弈的逐人静态保底--候选.md)问每份完整fresh纯SPE的每位最终利润是否都≥θ；本程序只直接攻击**根首位**。末位相对自身H最佳所以≥θ的定义级事实不自动保护根。

## 变量及连续域

源码不导入customer_attraction、规范ExactSPESolver或客户文件；只用标准库、NumPy、SciPy MILP/稀疏矩阵。它同时选择全部fresh有序节点的政策与系数，区别于只固定一份策略再搜索客户锥。

- n=p+binom(p,2)个连续系数，先α₀,…,α_(p−1)，再按itertools.combinations的无序对顺序放β；都在[−1,1]。README称“有理候选”，实际求解变量是浮点连续数，脚本不做有理重构。
- 每个h（长度d=0,…,m−1的无重复排列）及每个标签t都有连续V_(h,t)。它表示沿该节点所选真实后继完成后，按终局集计算标签t的边际；t未被实际选择时只是辅助形式边际，不冒一名存在的玩家。
- 每个合法动作a∉h有binary z_(h,a)，每节点一热。根z_(∅,0)=1，固定根标签0。
- 每个|H|=m−1和a∉H有binary y_(H,a)，每H一热，选择一个静态query见证。
- 连续τ用于θ的下界。所有非系数连续变量在[−(m+1),m+1]，二进制变量在{0,1}。

根固定0是明确编码。对本完全可置换的标签/系数域，若某根动作a的反例存在，可统一换名a↦0而保持收益差和全部约束，所以此固定不会漏掉**固定p,m根**反例；不据此把其它位置在原m人游戏的失败直接称根失败。

## 收益传播和真实全历史激励

记F_t(h)在|h|<m时为V_(h,t)，终端|h|=m时为

\[
F_t(h)=\alpha_t+\sum_{b\in h,\ b\ne t}\beta_{tb}.
\]

对每个h，源码先要求Σ_(a∉h)z_(h,a)=1。对每个合法a及所有t，用上下两条大M行编码

\[
z_{h,a}=1\Longrightarrow V_{h,t}=F_t(h\cdot a).
\]

因此选定动作的整张终局边际向量递归传播到父节点；并不是用独立数值填根路径而遗漏离轨政策。每个有序孩子都有自己的z，(a,b)与(b,a)可以独立破平局。

对每个b∉h、b≠a，另编码

\[
z_{h,a}=1\Longrightarrow V_{h,a}\ge F_b(h\cdot b).
\]

右侧是当前玩家改b后沿**孩子b自身完整政策**完成所得b利润，不是冻结原后继a的终局。由末层逆向归纳，这些真实比较与所有节点一热共同恰给完整fresh纯SPE。已经选a的旧玩家利润向量传播不要求其在后层再决策。

### 大M为何不额外截掉合法策略

源码M_big=2(m+1)。系数绝对值≤1，终端F_t(h)至多含m+1项，所以它和所有传播V均在[−(m+1),m+1]。两值差绝对值≤2(m+1)，未选z=0的上下传播行及IC行因此充分放松。对实际被选标签只有m项，但给未被选t也留m+1界是必要的安全余量。

每个静态H的query边际只含m项，绝对值≤m。见证行实际为

\[
F_a(H)-\tau-M_{big}y_{H,a}\ge-M_{big},\quad
\sum_{a\notin H}y_{H,a}=1.
\]

y=1时强制τ≤F_a(H)，y=0时自动释放。故精确可行解有τ≤θ_(p,m)；相反给定系数可对每H选最大query并取τ=θ，且|θ|≤m落在变量界内。报告名`theta_lower`因此准确是一个选择器支持的下界，不是代码另枚举H后算出的θ等值证书；浮点候选仍需核残差。

目标向SciPy提供最小化V_(∅,0)−τ，报告取负得到最大化τ−根收益。若有严格正的**精确可行**解，完整政策就是辅助根保底的真反例；原脚本只返回浮点候选，没有独立验证步骤。

## 261变量、1116行的逐项来源

令P(p,d)=p!/(p−d)!、N=Σ_(d=0)^(m−1)P(p,d)、Z=Σ_dP(p,d)(p−d)，Y=binom(p,m−1)(p−m+1)。总变量n+pN+Z+Y+1，其中Z+Y个binary。

|类|p5/m3的数目|
|---|---:|
|α/β|5+10=15|
|全部26节点×5标签的V|130|
|政策z|5+5×4+20×3=85|
|θ见证y|binom(5,2)×3=30|
|τ|1|
|合计|261，其中115 binary、146 continuous|

源码的约束数为N+2pZ+Σ_dP(p,d)(p−d)(p−d−1)+binom(p,m−1)+Y。

|约束|p5/m3的数目|
|---|---:|
|每节点政策一热|26|
|每合法动作/全部标签的两向传播|2×5×85=850|
|被选动作对所有其它fresh动作的IC|20+60+120=200|
|每静态H见证一热|10|
|每query门槛|30|
|合计|1116|

这些是按原循环解析展开，非本轮新建矩阵或MILP运行；匹配原报告也不补造实际argv/求解器版本。原游戏若允许重复，同p5/m3前两层应有1+5+25个历史；这里26是fresh的1+5+20，不能称已核原CAG全部历史。

## 系数盒与旧171/591程序的真实区别

正比例缩放全部α/β会同比例缩放每位利润、θ和差，且保持全部SPE比较与平局。任意有限非零系数的严格根反例可正缩放到[−1,1]；所有传播值随之满足上述m+1界。故对**固定p,m**，若对此联合MILP给出精确全局最大值≤0，就能排除该p,m全部有理系数的根反例；当前报告没有给这条上界。不能仅因系数盒就说本编码漏掉同p,m的大系数根反例，也不能把固定p,m覆盖外推到任意人数/目录。

已完整比较[另一三人MILP资源](../资源/三人二次无重复保底的完整策略MILP与限时报告--资源.md)：3738B无guard的`fresh_m3_milp.py`固定m3、系数B20、要求θ−root≥1而零目标，原p5有171变量591行，45秒**无primal**返回。其单位差条件与固定B未必兼容任意失败的归一化；本4179B则有guard、任意m、无固定正差阈值、最大差目标，原有261/1116且有浮点候选。两者不能按fresh/45秒/五标签合并成一次运行或相互补证书。

## main、输出、报告缺口和编译路由

CLI默认--p5、--m3、--seconds45，--output是必需Path。代码没有显式校验1≤m≤p或seconds正数；非法输入不自动变成数学可行域。例如m>p会遇无动作节点的一热空和=1，p≤0或m≤0还可能没有固定根变量。参数异常/求解器拒绝不是候选反例。

main guard阻止import直接run；但顶层仍导入NumPy/SciPy。`seconds`从构好稀疏矩阵、紧接milp前开始计时，不包括前面枚举/建矩阵。options只有time_limit与mip_rel_gap0；gap0是请求，不把超时或浮点容差变成精确最优证明。文件write_text覆盖指定路径并加换行，未自动创建父目录；stdout只去掉coefficients/policy，保其它report字段。若sol.x不存在，四个primal字段不写；这次原报告实际有它们。没有输出V/z/y完整向量、残差、对偶界、mip_gap、搜索节点、版本或完整求解日志。

新847B入口准确引用R-3d6f的6513B`quadratic_graph_compiler.md`，该原文已本次正常取得、全文读，非以候选摘要替读。其作者频率二客户路线给K/pair/private非负重数和充分C，声称所有重复历史排old、双向策略及θ_CAG=B+θ_fresh，并解析给该充分C下OPT<2W；原候选待主检查/内审时态保留。现有[受限编译候选](../候选/频率二客户编译与二次fresh安全边界--候选.md)和[完整Möbius编译定理](../定理/无重复辅助博弈的完整历史编译--定理.md)各保自己的证明/偏置合同，不能将一个fresh负利润输入直接当客户质量。即使未来根floor反例有理化，它也只是否定辅助保底，不能由本MILP替代所有原重复偏离或福利比认证；[均匀偏置边界](../障碍/均匀客户偏置的福利与比较边界--障碍.md)另说明比例失真。

本轮0原程序import/run、0MILP/LP/BI/分数审计、0旧成功复跑。程序retained为完整合同，入口integrated于本对象与完整报告资源。7ZT原sync为synced，完整7IDclaim保全，只有本3primary逐源处置；不改旧冻包或当前R，不start/claim/done/adopt/改绑定。关系已实质判断，第三阶段再登记正式边。
