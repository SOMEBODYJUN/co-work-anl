---
id: cag-symmetric-iid-closure-minimum-payoff-finite-cone-source-contracts
kind: resource
type_tag: 资源
title: 对称iid福利闭包与最低收益有限锥的来源合同
status: 四主稿7993B完整实读；17项actualclaim及本4owner/SHA核真；三探针/真实helper全读，0新LP或旧成功重跑
summary: 八客户强iid失败是既有CCE例闭包，作者与父审不同二次域参数一致；最低实际收益顺序行、有限价格菜单和实际终局支持受限背景的探索与真正安全值分开，旧成功不重跑。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d321c149379b425493c5e8a5e03c6f39/global/README.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d321c149379b425493c5e8a5e03c6f39/parent/iid_bridge_review.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d321c149379b425493c5e8a5e03c6f39/security/README.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d321c149379b425493c5e8a5e03c6f39/security/iid_nash_bridge_boundary.md
---

四稿1585/1338/1347/3723B共7993B全文读、size/SHA256/blob核真。八客户核心早已有[完整iid反例](../反例/独立同分布福利支付--反例.md)及[静态基准](../定理/静态独立同分布安全基准--定理.md)；本组不重新创造游戏或执行旧84/64算术。这里保每个源的完整状态、不同参数证明和两个实际有限探针接口，不能把四稿压成一句已知桥失败。

## 核心定义及更短的闭包逻辑

同一有限单位客户/共同目录，F_m(q)=Σ_Tw_T E H_{Bin(m,a_T(q))}是期望调和势，Ψ_m(q)=Σ_Tw_T[1−(1−a_T(q))^m]是m次iid期望覆盖。静态定理证明F_m的最大者恰是对称混合Nash，全部最大者具有同一覆盖Z_m。这里不是max_q Ψ_m(q)，不是最低CCE福利，也不是真安全值v_m。

既有八客户四主题三人完整SPE的W6，同实例全部静态CCE的最低期望福利544/87>6。任何对称混合Nash的独立产品都是CCE，故无需具体求q，即
\[
Z_3\ge544/87>6=W.
\]
这直接否定全称强iid福利支付W≥Z_m；不是新的八客户实例、最小性或新颖性结论。源3723B开头“尚待root独审”是原作者时点，1338B父稿随后已内部审读通过；不能把个人稿该状态当当前仍没人读过。

## 作者r与父审s的两种精确参数

八客户由不交core A2、B4和私客c,d组成，共同主题0=A、1=B、2=A+c、3=A+d。原完整策略根0、第二位恒1，末位全4×4表
\[
\begin{pmatrix}1&1&1&1\\1&2&3&2\\1&3&1&1\\1&2&1&1\end{pmatrix}
\]
定义全部21有序节点，实际011每人2。完整真实比较/OPT8已在既有反例自足保存，不把这张表当只在轨策略。

设g(t)=1−t+t²/3、r=(30−√669)/7，q=(0,r,(1−r)/2,(1−r)/2)。25<√669<26保证合法，纯收益
\[
\alpha_0=2g(1-r),\quad\alpha_1=4g(r),\quad
\alpha_2=\alpha_3=2g(1-r)+g((1-r)/2).
\]
\(\alpha_1-\alpha_2=(7r^2-60r+33)/12=0\)，而α₂−α₀=g((1−r)/2)>0，故精确是静态对称混合Nash。
\[
Z_3=12g(r)=\frac{156r-48}{7}
=\frac{4344-156\sqrt{669}}{49}>6.
\]
原作者另给一个短严格号证书：P(x)=7x²−60x+33在[0,1]严格递减，P(15/26)=483/676>0，所以r>15/26，Z₃−6=(156r−90)/7>0。它与旧正文的平方证书675²−669·26²=3381是同值的另一证明，不需浮点近似6.307…承担符号。

父审用s=q₂=q₃=(1−r)/2，方程7s²+23s−5=0、q₁=1−2s。代换P(1−2s)=4(7s²+23s−5)，两个代数域只是换基。父稿称用Q[s]逐单位、全部真实历史/静态覆盖和收益守恒、作者根式代换与严格号；作者称Q(√669)枚举全部64静态有序终局及Nash偏离。这些是两份原实现的历史声明，不因当前已读全部稿就继承“事前未见作者”的盲审身份。

同实例的真正安全值为 $v_3=44/23$，且 $W-3v_3=6/23>0$，因此强/弱真正安全聚合和half都未被本例否定。一般m v_m≤Z_m≤OPT_m仍有效，失败的是动态全付Z。既有成功check_iid_examples.py/replay-iid.json含同八客户84完整比较、真正安全上下证及二次域Nash等式，核精确版本后复用，0重跑。当前不把未取原3072/2776两个不同程序冒已逐字节执行，也不另造一位外审者。


## 固定形式策略锥、真实Γ和实际最低收益行

1585B全局入口的12客户唯一严格SPE/1215满支持整数例、PNE全集/稳健性已在[严格反例](../反例/全部历史严格唯一均衡与静态PNE福利的分离--反例.md)完整保存。原随机发现、MILP压缩和五主题16客户中间例各守来源；最终四主题12客户结论不靠搜索器最优性，也不主张规模最小。

新min_price_attack.py实际导入5044B cone_opportunity_attack.py的policies/prepare。两份代码全读后可以写精确合同，而不是凭“full”或函数名判断：

1. policies递归遍历dict/list，只抽有actions列表及terminal_counts键的对象；同一策略可能在不同文件/标签再出现，未按hash去重。
2. prepare取p=len(terminal_counts)、m=sum(terminal_counts)，只接受2≤m≤5、2≤p≤8。actions先转有序历史字典，再检查字典长度为Σ_{i=0}^{m−1}p^i；walk遍历全部p进制有序树，沿规定动作算每节点实际终局。缺历史或非法分支会使walk失败，并不是成功返回部分树。
3. 它没有调用规范证书verifier，也不检查声明的terminal_counts与walk实际root相等；声明向量这里只给p,m。成功准备的是一个完整**形式策略**及其真实响应行，不是已认证某给定客户实例为SPE。
4. 每个非空兴趣mask B∈{1,…,2^p−1}是一个可重赋的客户类型列。对每个历史h、规定a及替代b≠a，行是
\[
R_{h,b}(B)=u_b(z(hb);B)-u_a(z(h);B).
\]
A_ub·x≤0正是所有有序非自身IC。实现把1/den系数存为NumPy浮点；上面的有理表达式是其数学定义，不表示数值矩阵已exact。不是冻结实际后缀，也不只查实际路径。每个p,m的行数为(p−1)Σp^i；p7/m5有2801历史、16806非自身比较，不能把显示表行数当完整策略。

若一个精确有理非负x满足全部这些IC，完整策略在该共同全类型实例中逐节点最优；清分母即可得到单位客户完整SPE。这与只有557/727等必要索引投影、尚缺策略/共同实现的点不同。当前floating LP输出未经过这种exact验收，所以不能径称新SPE反例。

允许全部非空兴趣类型，不仅重赋原游戏已有的类型；原来某主题是否空覆盖也不作为固定条件保留。令x_B≥0且Σ_B x_B=1，规范化的是**全部非空兴趣客户质量**，不是实际福利W=1。未感兴趣空类型不进列，零活跃客户游戏不在该LP归一超平面；正目标的搜索可忽略纯空类型，但不能从这项严格负数声称包括任意空客户稀释后的统一负裕量。

对实际根路径中某个出现主题a，增加
\[
u_a(root;x)-u_b(root;x)\le0
\quad\forall b\text{ 出现在实际路径且}b\ne a.
\]
单位玩家在相同终局选同主题收益相同，所以循环distinct actual themes足以指定一个最低实际收益位置类；minimum_topic是**主题标签**，不是玩家位置或强制根最小。没有重排策略。

## 有限查询菜单、LP目标方向与17份冻结报告

给标签支持J，k=|J|，整数d1…k，查询权z_T=1/d（T∈J）否则0，总重τ=k/d。每类型的截断查询覆盖是min(1,|B∩J|/d)。被最大化的是
\[
\boxed{\sum_Bx_B\bigl[\min(1,|B\cap J|/d)
 -(k/d)u_a(root;B)-W_B(root)\bigr].} \tag{P}
\]
代码用linprog的最小化向量−target，报告−ans.fun，故max_violation确是**最大[C(z)−τu_a−W]**。不能倒转符号把负值当反例，也不能把它理解为原文件原客户实例的价格缺口：x在整个该策略锥内重选，source标签仅说明动作图出处。JSON的support是查询菜单J，不是actual_support程序中的竞争主题集合S；二者角色不同。

默认菜单J是全目录；--subsets时遍历所有大小2…p的支持（不含singleton），每个d1…k。--limit默认99999；发现报告目标>1e−7或达到limit即退出；best比较容差1e−12，保存质量阈值1e−9。只处理ans.success的LP，其余被忽略，不据这些浮点状态认证精确上界。

9882B冻结JSON有17个**标签报告**。m2…5、p4…7；所报histories全部与Σp^i一致，最大记录为m5/p7的2801历史。这不是17个不同游戏或17个独立策略：未在本批加载全部原cert目录，不能按相同实际路径合并或据不同标签认定独立。

全部17所报max_violation负，最大约−1/6；每个获胜菜单support恰为全目录。但报告不保存CLI argv，不能由“winner全目录”反推没启用--subsets，也不知道当时limit/输入目录是否截断。源码的全目录默认查询族及可选更宽族分别保留。报告中的浮点质量x可含显示截断，不是有理化的单位客户/全历史IC证书，更不是精确对偶证明。

一个清楚的语义例：dynamic_iid_local标签获胜质量只有mask127的1.0、m5/p7，目标约−1/5。这是所有七主题同覆盖的归一重赋点，不能说原标签对应的原始整数游戏价格值就是−1/5。负值只记录该有限float优化，没有证明一般B(min u)≤W或任意σ半覆盖。

source helper的另一个attack/main还有原individual/uniform机会目标；当前min_price只调用policies/prepare，不执行那个main。本批没有运行任一LP、没有重扫17模板或补180/1000阴性。

## 实际终局支持的受限整数背景：准确量词

1347B安全入口将actual_support_probe列为强模板边界。1449B原程序全读后，固定实例I及某个真SPE可实现终局计数z，S=supp(z)，定义
\[
\mathcal C_{m-1}(S)=\{q\in\mathbb Z_{\ge0}^{S}:\sum_{a\in S}q_a=m-1\},
\]
\[
\boxed{V_I(S)=\min_{Q\in\Delta(\mathcal C_{m-1}(S))}
 \max_{A\in\mathcal S}\mathbb E_Q
 \sum_{x\in A}\frac1{1+\sum_{a\in S}q_a1_{x\in a}}.} \tag{S}
\]
每列是合法整数竞争元组的计数类，Q可任意混合、相关，且在查询A之前固定；同一个Q同时压全部合法目录查询。这不是共同iid，也不是把平均分数负载放入倒数。限制仅对竞争者主题，查询仍为全目录。任意有序tuple与其计数类收益相同，所以用counts列不丢这类静态对手。

真正v_m允许全目录整数背景，所以v_m≤V_I(S)。程序的LP min v满足M Q≤v·1、Q≥0、ΣQ1；主循环在ExactSPESolver的**全部SPE可实现终局计数**中选择最大mV_I(supp z)−W(z)，不是只验一条指定策略。exact集合缓存不强制Markov政策；但LP本身是NumPy浮点/HiGHS，res.success未在value里显式检查，输出不是精确安全值证书。输出Q的背景计数是按实际support递增标签的局部坐标，概率仅保>1e−8项；它不是全目录p维计数，不能不重建support就解读。

实际main从**当前cwd**的examples/customer_attraction/*.json扫描，过滤topic_count>7或players>5；value的非空support/非负m−1组合前提是m≥1，代码没有给零玩家空support的完整边界处理。本批不执行扫描、不把“程序存在”称全部目录通过。source所提36客户“受限12”保为原报告，本组没有该扫描stdout或明确绑定的完整输入/对偶，未新认证它的精确最优值12，也不把它改叫真正全目录v。

## 已核五客户输入的三类对手值（比较推论）

为精确解释(S)和平均分数背景的区别，可直接使用[已有五客户完整SPE](../反例/实际路径支持限制的分数背景--反例.md)，不是新实例或原36数据。客户兴趣重数{1}:1、{0,2}:2、{1,2}:2；两人目录0/1/2。根0；末位0后1、1或2后2。末位收益三行分别(1,3,3)、(2,3/2,3)、(1,2,2)，根三个真实完成收益都2，故是全部4有序节点的完整SPE。实际路径为01，$W=\operatorname{OPT}_2=5$。

实际支持{0,1}的**整数**背景矩阵（行query0/1/2、列背景0/1）为
\[
\begin{pmatrix}1&2\\3&3/2\\3&3\end{pmatrix}.
\]
任意混合Q的query2值恒3，另外两行≤3，所以(S)受限整数最优恰3。它不是只否“均匀删一位”的某个取法，连任意重选Q都cap不住W/2=5/2。

若改为平均分数背景q=(s,1−s,0)，query2为2/(1+s)+2/(2−s)，减8/3恰2(2s−1)²/[3(1+s)(2−s)]≥0；s1/2的其他查询4/3和2，因此分数实际支持cap恰8/3。允许全目录背景2时各查询(1,2,2)，而纯query2面对0/1/2收益(3,3,2)，匹配证明真正安全值 $v_2=2$。

| 同一五客户完整SPE的对手类 | 最优cap | 2cap−W |
|---|---:|---:|
| 只用实际主题的任意整数元组混合Q | 3 | 1 |
| 只用实际主题的平均分数负载 | 8/3 | 1/3 |
| 全目录真正整数元组混合Q | 2 | −1 |

所以实际支持强平均福利cap失败不等于真正安全聚合失败；两种受限数值也不能相互替换。这是既有完整输入的解析对照推论，不是重跑新LP，不用它认证原36客户值12。原half仍显然成立W=OPT。

## 冻结候选目录、依赖与真实运行次数

三个原探针/报告14192B和真实helper5044B均由Root正常show取得、size/SHA/blob核真、全文读，原capture完整保全。原六项first-local缺记录与单helper缺记录不覆盖，不叫永久远端不可得。规范模型/exact/certificate/__init__四文件的同冻结版本也已完整读并保全，它们是actual_support声明导入；min_price只用custom helper/NumPy/SciPy，未调用规范SPE verifier。

源码的literal globs在两个冻结commit的inventory里各有22个examples JSON、29个certificate JSON候选，完整路径/size/SHA列表单列。**仅是冻结metadata候选普查**，没有加载全部JSON、执行策略递归或推断各项skip；不能把29−17叫12个跳过，因为每JSON可给0/1/多个策略标签，实际argv/cwd未记录。

本批original CLI0、新数学实验0、外部LP求解0、旧84/64/弱iid/strict成功重跑0。只读冻结JSON17记录并核历史数几何一致；generic锥的所有行和目标方向由完整源码推导，浮点结果保持原范围。原3072作者二次域脚本、2776父脚本/426报告此组未取，不借别组PASS冒该原实现执行；核心数学由已有完整proof与同SHA成功充分承担。

当前四主source已actualclaim：完整17项pushed/synced原回执、本4owner/SHA核真后才封语义receipt。三探针/helper/规范包仅比较依赖，不额外primary done。原“个人备份/尚未shared”与当前已发布iid/strict/weak成果分开，外审/新颖性未认证；一般六人/全目录half和真正W≥m v_m仍缺全局真实付款。
