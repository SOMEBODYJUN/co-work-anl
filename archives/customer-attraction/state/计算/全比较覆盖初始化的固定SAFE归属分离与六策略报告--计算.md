---
id: "customer-attraction/full-comparison-coverage-fixed-SAFE-ownership-separation-and-six-policy-report"
kind: "computation"
type_tag: "计算"
title: "全比较覆盖初始化的固定SAFE归属分离与六策略报告"
status: "complete"
truth_status: "two-exact-fixed-ordered-T-SAFE-role-cap-obstructions; six-case-CLIP-and-owner-LP-source-diagnostics-not-universal-feasibility"
review_level: "5535B源码与7188B全部报告完整实读；只补两固定SAFE见证，5+2个到达context；原main/172LP/旧全树IC/二次势审计均0"
scope: "六份旧完整SPE的全O直接查询份额初始化；固定全利润SAFE或确定性CLIP核；不等同加强H/r/δ INIT或实际Hall净R钱包"
summary: "两个比较元组分别分割61/11客户全集，每客户只有唯一合法owner，故分数归属也不能改变固定SAFE付款。质量91/5>18、61/12>5，固定T最佳cap比分别91/90、61/60；换序T/CLIP/其它路由仍另有自由度。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-ab2c6df20538474c948f5f24e59437ee/global_credit/test_role_cap.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-ab2c6df20538474c948f5f24e59437ee/global_credit/role_cap_results.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:examples/customer_attraction/root_tax_failure.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/customer_attraction/root_tax_failure.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:examples/customer_attraction/coverage_opportunity_failure.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/customer_attraction/coverage_opportunity_failure.json"
---

# 固定输入与被检查的量词

采用[单位客户共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)，保空主题、重复、同覆盖异标签、所有有序历史及平局。本程序不给新游戏或新均衡，而读取六个旧实例及其完整σ。客户类型的正整数重数表示不同单位客户；策略按完整有序历史查表，不合并同计数历史。

固定actual叶z、利润u、最优**有序**比较元组T及并集O。每个客户类型x选一个合法归属角色 $o(x)\in E_x=\{i:T_i\ni x\}$。原程序要攻击的强断言是：**每份最优有序T、每份合法owner**经同一固定初始化和SAFE/CLIP核，全部最终角色质量都不超过 $2u_j$。它不是“存在某T、某归属、某合法路由”的一般付款候选。

源码的初始化对**全部** $x\in O$直接使用owner角色i的actual-prefix合法查询T_i：将该客户的一单位在真实查询叶全部覆盖者间按份额拆分，past/current份额直接入对应actual角色、future份额进入以下固定核。它没有显式实现现行[加强INIT/I-PAY/R-FLOW/ROLE](../候选/固定比较元组的线性共同付款证书--候选.md)的H/r/δ及optional-common变量，也没有实现[实际Hall取消后的净R钱包](../候选/分数归属与实际净券的共同钱包--候选.md)。三者虽都提归属与ROLE，原始库存/自由变量/预算不相同。

# 全利润SAFE与固定CLIP核的自足定义

使用零起角色编号i。对任意context有序历史h、$|h|=i$，记规定动作 $a=\sigma(h)$、本枝真实叶 $B=\mathrm{finish}_\sigma(h)$，及reset真实叶 $A=\mathrm{finish}_\sigma(z_{<i},a)$。规定收益 $v=u_i(B)$，actual-prefix查询收益 $D=u_i(A)\le u_i$。对a中的客户类型x，重数n_x、两叶负载 $c_A(x),c_B(x)>0$，除i外覆盖者集合为 $J_A(x),J_B(x)$。置

\[
q_{jx}=\frac{n_x}{c_A(x)c_B(x)}\quad(j\in J_A\setminus J_B),
\]

\[
\delta_h=\sum_{x\in a}\frac{n_x(1+|J_A(x)\cap J_B(x)|)}{c_A(x)c_B(x)},
\quad P_h=\sum_{j,x}q_{jx},
\quad N_h=\sum_{x\in a}\frac{n_x|J_B(x)\setminus J_A(x)|}{c_A(x)c_B(x)}.
\]

逐客户计数给

\[
\delta_h+P_h=v,\qquad\delta_h=D-N_h\ge0. \tag{1}
\]

全利润SAFE核 $K_h\in\Delta_m$ 递归定义为：$\delta_h/v$吸收于actual角色i；每条past正边j<i以 $q_{jx}/v$吸收于角色j；future边j>i以该份额进入 $K_{A_{<j}}$。future深度严格增加，past只吸收不再递归，故有限；(1)按深度归纳给非负及列和1。v=0时原代码返回零向量，不能单凭该分支说它是概率列；本六个正实例的正源到达context均有v>0。

CLIP先取消正边总量

\[
c_h=\min\{P_h,N_h+u_i-D\}=\min\{P_h,u_i-\delta_h\},
\]

按past优先、角色递增、客户类型索引递增删除；剩边仍非负，新的current金额为 $\min(v,u_i)=\delta_h+c_h$。再独立递归求CLIP核。它固定这一种最大取消次序，未优化所有删边或共同容量，也不能继承另一核已算的终点分布。

对于unit来源x、合法owner i，令 $A_i=\mathrm{finish}_\sigma(z_{<i},T_i)$，$c=c_{A_i}(x)$，它的角色概率列为

\[
P_{j;ix}=\frac1c\sum_{\ell\le i:\,x\in(A_i)_\ell}1_{j=\ell}
+\frac1c\sum_{\ell>i:\,x\in(A_i)_\ell}(K_{(A_i)_{<\ell}})_j. \tag{2}
\]

所有列和1，付款 $F_j=\sum_x n_xP_{j;o(x),x}$，所以 $\sum_jF_j=|O|$。这里是全O质量，不是净R残源质量；不能把其它机制的退款或Hall流加到这个固定F上。

# 两个固定最优T的精确障碍，归属事实上唯一

下表完整给两输入的兴趣类型、重数与SAFE unit来源角色列。T为客户全集分割，故各类型只有表中所列的唯一owner；分数owner simplex也只有这一点。被比较元组覆盖全部客户，显然达到真实OPT的全集上界，不需要浮点LP证明最优性。

第一输入为[四人实际根税完整SPE](../反例/四人实际根总税--反例.md)，六主题A/B/C/D/E/F，actual为AAAF，$u=(9,9,9,11),W=38$。取有序 $T=(A,B,C,D)$：

| 兴趣 | 人数 | 唯一owner角色 | unit SAFE角色向量 |
| --- | ---: | ---: | --- |
| A | 12 | 0 | (1/3,1/3,1/3,0) |
| B | 8 | 1 | (0,1,0,0) |
| C | 4 | 2 | (0,0,1,0) |
| D | 8 | 3 | (0,0,0,1) |
| AE | 6 | 0 | (1/3,1/3,1/3,0) |
| AF | 6 | 0 | (1/4,1/4,1/4,1/4) |
| CE | 3 | 2 | (0,0,1,0) |
| CF | 3 | 2 | (0,0,11/20,9/20) |
| AEF | 6 | 0 | (1/4,1/4,1/4,1/4) |
| BEF | 2 | 1 | (0,6/11,0,5/11) |
| CEF | 1 | 2 | (0,0,11/20,9/20) |
| DEF | 2 | 3 | (0,0,0,1) |

权和为

\[
F=(9,199/11,91/5,864/55),\qquad \sum_jF_j=61=\mathrm{OPT}_4.
\]

角色2质量 $91/5>18=2u_2$，严格超额1/5。其它角色的比例也由此向量直接确定，最大为91/90。因此在**这一份固定有序T和SAFE核**下，允许任意分数owner的最小共同cap比恰为91/90>1；不是只找到一个可通过更好owner修复的坏分配。

第二输入是十一客户覆盖机会的旧规范完整策略，主题A/B/T/D/E，actual AAB，$u=(5/2,5/2,3),W=8$。这份旧策略在AB、AT等四末位平局与后来extra-query证书不同，不能只按相同actual叶认作同一σ；完整差异解释见[额外查询反例](../反例/实际终局额外查询的三人反例--反例.md)。当前固定比较有序元组 $(A,B,T)$：

| 兴趣 | 人数 | 唯一owner角色 | unit SAFE角色向量 |
| --- | ---: | ---: | --- |
| A | 2 | 0 | (1/2,1/2,0) |
| B | 2 | 1 | (0,1,0) |
| T | 1 | 2 | (0,0,1) |
| TD | 1 | 2 | (0,0,1) |
| TE | 1 | 2 | (0,0,1) |
| ADE | 3 | 0 | (1/2,1/2,0) |
| BDE | 1 | 1 | (0,7/12,5/12) |

所以

\[
F=(5/2,61/12,41/12),\quad\sum_jF_j=11=\mathrm{OPT}_3,
\quad F_1-2u_1=1/12>0.
\]

同样因owner唯一，固定T的最佳分数归属cap比恰为61/60>1。这两个例子都满足原half，只反驳指定初始化/核/有序T的共同角色预算。重排同一比较主题会改变actual-prefix查询叶和角色位置，不能把此分离免费迁给新T。CLIP、加强INIT、可变common路由和实际Hall净券也有其它自由度，本页不排它们。

# 六份报告全部数值的准确层级

7188B报告为scope和六cases。每例完整保存name、人数、类型数、actual、全部u、W/OPT、含自身IC数、最优有序元组数和safe/clip两mode。每mode有∀owner违反布尔、跨最优T最小的fractional-owner最优比例、取得该最小的T和最坏T的最优比例；仅两个SAFE阳性项另存完整owners/全角色质量/目标精确分数。全部字段均已读。

| 旧输入 | m/类型 | W/OPT | 含自身IC | 最优有序T数 | SAFE best / worst | CLIP best / worst |
| --- | --- | --- | ---: | ---: | --- | --- |
| portfolio_matching_failure | 2/10 | 44/45 | 30 | 2 | 0.5563241107 / 0.5785123967 | 0.5652173913 / 0.5909090909 |
| root_tax_failure | 4/12 | 38/61 | 1554 | 24 | 0.9277777778 / 1.0111111111 | 0.9166666667 / 1 |
| individual_security_failure | 3/13 | 32/34 | 258 | 24 | 0.53125 / 0.5738916256 | 0.53125 / 0.5561576355 |
| eight_cce_welfare_gap | 3/4 | 6/8 | 84 | 6 | 0.75 / 1 | 0.75 / 1 |
| coverage_opportunity_failure | 3/7 | 8/11 | 155 | 6 | 0.85 / 1.0166666667 | 0.8333333333 / 1 |
| prefix_balance_failure | 4/12 | 14/22 | 1554 | 24 | 0.8534813357 / 0.8850374464 | 0.8579668978 / 0.8895230085 |

best/worst均是**先在每个固定T最小化owner比例，再跨最优T取min/max**；不是固定一份owner同时服务全部T。每固定T的浮点LP变量 $y_{xi}\ge0$为实际客户质量，约束 $\sum_{i\in E_x}y_{xi}=n_x$、$\sum_{xi}P_{j;ix}y_{xi}\le2\rho u_j$，最小化共同ρ。86个有序元组、两mode共172个LP；原报告未保存每个LP的最优分数owner或有理对偶。表中数值沿用原浮点诊断，不能由接近1或小于1认证普遍可行，也不能把最坏T的浮点大于1一概改成精确不可行。本页仅对上两份**唯一owner**的具体T给出无LP精确证明。

原∀owner检查本身按精确核运行：对每个目标角色j，每个客户类型独立选择合法owner使 $P_{j;ix}$最大，再求加权和。因此线性目标允许将该类型全部单位客户分给同一最优owner；这个最大化包含异质单位owner或分数owner，不是误限成“类型必须整体归属”。报告CLIP在六旧输入中未见∀owner违反，是该有限来源记录，不是所有游戏的正面定理；也不表示CLIP全域或任意初始化已被认证。

# 程序合同、最小新复核与复用范围

5535B程序有main guard，模块import会加载NumPy/SciPy并定义run，但不读六例或启动实验；main固定六文件名，从**cwd**的examples及certificates双路径读入，不扫新实例。每份先清点完整history集合，再对所有动作沿σ完成，精确核IC，共3635个含自身比较。它以Fraction算kernel/极端owner阳性值，再转float做172个HiGHS归属LP。失败LP会assert，函数无通用输入校验器合同；六输入利润为正，不把阳性比例除数扩成任意零利润游戏。

main最终覆写同目录`role_cap_results.json`并打印全部报告，未保存原运行argv/环境/stdio或12输入指纹。本批没有倒填旧生成事件，没有运行或import原main/run、没有重跑172LP及已成熟的完整SPE检查。已有[父方全利润CLIP审计](../程序/父方全利润剪枝的六策略原审计与三份流--程序.md)同用六输入，却是每个context单位利润注入、比较gross/net/clip的不同实验，不能用其成功冒充本源全O-owner合同的运行。

本轮只写标准库Fraction定义核，读取上两份同SHA旧实例/完整策略和两个明确owner见证。它不导原脚本、solver、优化器；只为(1)(2)到最终F的**具体新见证绑定**重建到达的5及2个SAFE context，两个全角色向量和目标质量/cap/ratio与冻结报告精确相同。每个type的unit列及查询叶是本轮新增保存，原7188B报告没有这些逐列数据。另核输入全有序键及目标T覆盖全部单位客户；没有再次遍历全部旧IC。0.067秒、exit0、stderr0，实际argv/代码及输入指纹见[执行记录](../../tools/evidence/role-cap-and-background-checkpoints-boss3/replay/execution-record.json)，全部unit列和查询叶见[两个精确见证](../../tools/evidence/role-cap-and-background-checkpoints-boss3/replay/two-safe-witnesses.json)。

四份旧raw JSON均完整读取，其源σ有效性复用现有全历史证明及同冻结字节；覆盖机会采用原D平局版本，不借后来的E版本替代。其它四case的八个输入文件未在本批重新加载或认证，六报告的更大范围按其来源身份保留。26客户二次势固定证书也未运行，本页不另授新颖性或外审。

可复用资产是固定核的明确质量守恒、两个分割比较T无归属自由的精确ROLE失败，以及完整六例诊断谱。未完成的仍是每份原SPE能否在更大兼容机制中选同一个T/初始化/路由/owner支付全部角色；有限CLIP阴性、浮点最优或新增流守恒都不能补这个全称义务。
