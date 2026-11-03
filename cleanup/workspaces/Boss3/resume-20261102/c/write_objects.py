from pathlib import Path
import json
REPO=Path('/workspace/scratch/cd4305a146e6/co-work-anl-boss3')
STATE=REPO/'archives/customer-attraction/state'
PREFIX='research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/'
COMMIT='68fad804ec5946cb296f77dc5b336308a66abf12'
E='../../tools/evidence/boss3-c16-resumed'
files={}
def add(kind,name,id,title,status,summary,sources,body):
 path=f'{kind}/{name}--{kind}.md'
 typekind={'定理':'theorem','障碍':'obstruction','反例':'counterexample','程序':'program','资源':'resource'}[kind]
 fm='---\n'+f'id: {id}\nkind: {typekind}\ntype_tag: {kind}\ntitle: {title}\nstatus: {status}\nsummary: {summary}\nsource_refs:\n'+''.join('  - '+json.dumps('source:'+COMMIT+':'+PREFIX+s,ensure_ascii=False)+'\n' for s in sources)+'---\n\n'
 text=fm+body.strip()+'\n'
 (STATE/path).parent.mkdir(parents=True,exist_ok=True)
 (STATE/path).write_text(text)
 files[path]={'id':id,'sources':sources}

add('定理','固定人数全支持Shapley的三角身份基与等计数交换','customer-attraction/fixed-population-all-support-triangular-shapley-identities','固定人数全支持Shapley的三角身份基与等计数交换','proved-for-all-positive-integer-m-p; once-original-Fraction-replay; signed-linear-image-only','固定人数终局收益以可见覆盖坐标为三角参数，恰v-d条独立身份充要刻画共同有符号客户表示；另保等计数标签收益差的正系数交换式。',['tree/all_support_shapley_circuits.md#1','tree/all_support_shapley_circuits.md#2','tree/all_support_shapley_circuits.md#3','tree/verify_all_support_shapley.py#audit'],r'''
# 固定人数的对象与正边际

令非空有限标签集P有p个标签，固定整数m≥1。计数q∈Z_{≥0}^P、|q|=m，A=supp(q)，仅对q_a>0定义一位选a者的收益F_(q,a)。同覆盖不同标签、空主题、重复选择和零客户均允许。下文是一份共同终局资料的表示定理；没有把完整策略的有序历史改成计数历史。

对非空兴趣类型B⊆P，以同一张实有符号质量w_B定义
\[
 C(S)=\sum_{B:B\cap S\ne\varnothing}w_B,\qquad
 F_{q,a}=\sum_{B\ni a}\frac{w_B}{q(B)},\quad q(B)=\sum_{b\in B}q_b.
\]
C(∅)=0，只需要|S|≤m的可见覆盖资料。真实单位客户模型还要求w_B为非负整数；本定理的线性等价允许负数。有理非负质量可统一清分母成为单位客户，负号不能这样消除。

对R⊆A\{a}，设
\[
 \lambda_R(q,a)=\int_0^1 t^{q_a-1}
 \prod_{b\in R}(1-t^{q_b})
 \prod_{b\in A\setminus(R\cup\{a\})}t^{q_b}\,dt.
\tag{1}
\]
每个λ_R严格正，和为1/q_a，而且
\[
 F_{q,a}=\sum_{R\subseteq A\setminus\{a\}}\lambda_R
       [C(R\cup\{a\})-C(R)].
\tag{2}
\]
逐类型证明：若a∉B，两侧均零；若a∈B，非零覆盖边际要求R避开B。对其余标签的两种选择求和，被积式成为t^{q(B)-1}，积分为1/q(B)。线性相加给(2)，全过程不需要w≥0。各因子在0<t<1正，给λ的严格正性；对全部R求和后只余t^{q_a-1}，给系数和。

用于精确实现的有限公式是
\[
 \lambda_R=\sum_{D\subseteq R}\frac{(-1)^{|D|}}{m-q(R)+q(D)}.
\tag{3}
\]
分母至少q_a>0。交错形式应按有理数求值，其一般正性由积分承担。将(2)移项得到两侧非负系数的等式
\[
 F_{q,a}+\sum_{\varnothing\ne R\subseteq A\setminus\{a\}}\lambda_RC(R)
 =\sum_{R\subseteq A\setminus\{a\}}\lambda_RC(R+a).
\tag{4}
\]
等式在signed模型中仍真，只有将每个边际视作非负余项时才额外使用客户非负性。

# 消去低人数层后的完整三角身份基

全部固定m收益顶点为V={(q,a): |q|=m,q_a>0}。它的大小和可见非空覆盖坐标数分别是
\[
 v=p\binom{m+p-2}{p-1},\qquad
 d=\sum_{k=1}^{\min(m,p)}\binom pk.
\]
对每个非空支持A、|A|≤m，从支持恰为A的收益顶点任取一个基准ρ_A=(q^A,a_A)。设β(q,a)=λ_(A\{a})(q,a)>0。把(2)写成
\[
 F_{q,a}=\beta(q,a)C(A)+L_{q,a}(C),
\tag{5}
\]
其中L只含A的真子集覆盖：最高支持项C(A)只由R=A\{a}出现一次。

按|A|递增，用基准方程恢复
\[
 C(A)=\frac{F_{\rho_A}-L_{\rho_A}(C)}{\beta(\rho_A)}.
\tag{6}
\]
将恢复值代入同支持的每个非基准方程(5)，恰得到v−d条齐次线性身份。这些身份独立，且一个固定m的全收益向量具有共同signed客户表示，当且仅当它满足这些身份。

证明充分性包含两个不能省去的步骤。首先，每个非基准方程有一个独有的非基准收益变量、系数1；(6)只递归使用各支持的基准变量，不使用非基准变量。因此v−d条独立，解空间维数d，所有收益由d个恢复覆盖坐标唯一决定。其次，任意这些截断C都确有共同signed实现：任意补充|S|>m的覆盖值，固定C(∅)=0，再取
\[
 w_B=\sum_{D\subseteq B}(-1)^{|B|-|D|}
       [C(P)-C(P\setminus D)]\quad(\varnothing\ne B\subseteq P).
\tag{7}
\]
布尔反演给Σ_(B⊆D,B≠∅)w_B=C(P)−C(P\D)，故所得客户确恢复所有C(S)。由(2)又恢复全部给定F。有理输入使λ、恢复和反演全部有理。必要性直接由(2)。这同时补足原稿以覆盖行满秩描述的存在性论证，不靠有限秩测试证明一般m,p。

同支持效率Σ_a q_aF_(q,a)=C(A)是客户表示的推论，因而已经包含在完整身份中。仅给这个总和并不恢复全部跨标签分配。成熟[正边际与平衡贡献定理](共同客户收益的正边际与平衡贡献--定理.md)用全部1…m层的E+BC扩展变量刻画同一signed空间；这里独有的是只保第m层的显式v−d独立消元基，二者条件相容。

# 等计数标签的正交换

当q_a=q_b=r>0，置D=A\{a,b}，定义
\[
 \theta_R=\int_0^1t^{r-1}\prod_{c\in R}(1-t^{q_c})
                    \prod_{c\in D\setminus R}t^{q_c}\,dt
 \quad(R\subseteq D).
\]
则θ_R>0、Σ_Rθ_R=1/r，而且
\[
 F_{q,a}-F_{q,b}
 =\sum_{R\subseteq D}\theta_R[C(R+a)-C(R+b)].
\tag{8}
\]
同时命中a,b的类型两边都消去；只命中其中一个时同(2)的积分证明。右侧只含A真子集，最高支持覆盖确已消失。没有使用这些覆盖差非负。

两个特例可直接复用：

* A={a,b}、q_a=r、q_b=s、r+s=m时，λ_∅=1/m、λ_{b}=s/(rm)，故mrF_(q,a)+sC(b)=rC(a)+sC(ab)。m3时同双支持有四个收益顶点；加已恢复的单主题覆盖，恰有三个独立约束，须与[完整二主题纠错](固定完整策略的二主题耦合二倍界--定理.md)的秩三条件相符。
* m个不同标签各一次时，λ_R=|R|!(m−|R|−1)!/m!，θ_R=|R|!(m−|R|−2)!/(m−1)!。m3的abc上，6F_a+C_b+C_c+2C_bc=2C_a+C_ab+C_ac+2C_abc，故2(F_a−F_b)=C_a−C_b+C_ac−C_bc。后二式有三支持分配信息，仅查二支持收益顶点不能代替。

# 原代码、一次实跑与准确停止处

3347B原verify_all_support_shapley.py全文读：以Fraction逐个兴趣类型核边际、三角消元、每条身份在全部客户列上为零、身份秩及等计数交换；不导solver、NumPy或SciPy。其本次原样一次执行exit0/stderr0，输出如下。一般定理由前文证明承担。

|m,p|固定层顶点v|覆盖维数d|独立身份v−d|逐类型边际检查|逐类型交换检查|
|---|---:|---:|---:|---:|---:|
|1,3|3|3|0|21|0|
|2,4|16|10|6|240|90|
|3,4|40|14|26|600|180|
|4,3|30|7|23|210|42|
|3,6|126|41|85|7938|3780|

[原件及执行记录](../../tools/evidence/boss3-c16-resumed/README.md)保留源码、完整stdout、SHA及环境。源md与代码全部阅读；程序只验证列出的五组，没有把原稿“独立审查进行中”改成他人已审或外审。

与[共同signed四人障碍](../障碍/共同有符号客户的四人超二福利与局部负原子--障碍.md)的逻辑联系是：那份负质量表自动满足本页所有身份，却有形式SPE的比较值160/79>2和可见负原子。因此完整span仍不代替非负客户cone。接续half支付还需一份完整策略的所有真实激励Γ非负组合以及在非负客户上非负的余项；本定理不自动提供乘子或福利界。阶段三可登记“表示等价/特化”和“线性完整仍不足”的有条件关系，目前以本文准确证据保留，不从旧图复制超边。
''')

add('障碍','重复互惠尾惩罚的最后位置闭包','customer-attraction/repeated-reciprocal-tail-last-mover-closure-obstruction','重复互惠尾惩罚的最后位置闭包','proved-template-obstruction-for-all-integer-t-ge2; once-finite-original-audit','指定C_i实际路径和两条互惠惩罚路径要求a≤(3−t)x/[2(t+1)]，但t≥2时第三条路径的末位已严格偏离，故此直接重复模板无法延伸。',['credible/reciprocal_tail_obstruction.md#Claim-1','credible/reciprocal_tail_obstruction.md#Claim-2','credible/audit_reciprocal_tail.py#main'],r'''
# 指定构造与真实量词

采用[共同目录完整历史单位模型](../定义/共同目录完整历史模型--定义.md)。客户块两两不交，至少k≥2组，|X_i|=x>0、|a_i|=a≥0、|b|=b≥0、|d|=d≥0；在单位模型中块大小为整数。共同目录为A_i=X_i∪a_i、B_i=X_i∪b、C_i=X_i、D=b∪d，人数m=k+t，t为正整数。

拟扩张的具体合同要求同一完整纯SPE有三条真实根相关路径：实际每组一次C_i再t次D；根改A_i后其余每组一次C_j再t次B_i；根改B_i后其余每组一次A_j再t次A_i。只有路径是假设，任何其余离轨动作仍须另外填写真实最优回复。要否定的是这个三路径合同，不能把它扩大成所有无拥挤SPE的效率界。

# 两条根/末位约束已压缩遗漏预算

实际每个早期C_i者收益x。第三条真实偏离的B_i者最终独取公共块b，并在X_i与t个A_i者分享，所得b+x/(t+1)。根最优性于是必要地给
\[
 b\le\frac{t}{t+1}x.\tag{1}
\]
在第二条路径的最后节点，指定B_i所得x/(t+1)+b/t；任取j≠i，此前C_j恰一次，改A_j得x/2+a。真实末位最佳回复要求
\[
 \frac{x}{t+1}+\frac bt\ge\frac x2+a.\tag{2}
\]
合并得到
\[
 \boxed{a\le\frac{3-t}{2(t+1)}x.}\tag{3}
\]
因此t1最多x/2，t2最多x/6，t3只能a0，t≥4已与x>0、a≥0矛盾。d没有进入这些局部比较，调d不能修补这两条必要条件。

# t≥2时第三条路径自身已经失败

第三条路径末位若继续选A_i，所得x/(t+1)+a/t；任一其他A_j此前恰一次，加入它得到(x+a)/2。改动的严格增益是
\[
 \frac{x+a}{2}-\frac{x}{t+1}-\frac at
 =\frac{t-1}{2(t+1)}x+\frac{t-2}{2t}a>0
 \quad(t\ge2).
\tag{4}
\]
第一项严格正，第二项非负，故即使a=0也不能保留该指定尾。这个末位历史是根偏离后的真实节点，不能靠修改未到达的别枝抵消。其与(3)不同：前者是若策略存在的必要预算，(4)直接排除t≥2的整组三路径假设；无需先满足(3)。t1的此增益为−a/2，并未被该式排除，原3/2模板x2、a=b=d1仍须其自己的完整SPE证明。

源数值例k2/t2/x3/a2：历史(B0,A1,A0)后指定A0为2，改A1为5/2。它只演示局部不可信，没有提供一个新的低福利完整SPE。

# 精确代码与保留用途

1404B原audit_reciprocal_tail.py全文读并原样一次执行。代码用x7/a11对t1…100按Fraction核(4)恒等式、t≥2正性及把(1)代(2)得到(3)的系数，再用逐名单位客户核上述2对5/2。stdout保100条系数检查的计数与前五上界，exit0/stderr0。解析结论覆盖所有t来自(1)—(4)，不是从100个数值推广。完整原件、stdout和执行身份见[证据](../../tools/evidence/boss3-c16-resumed/README.md)。

失败机制是多名重复惩罚者同时给其他已经用过的组制造更好的加入机会。后续可改变三条路径之一，研究不同惩罚主题、跨组分散、异质块或更深状态闭包；这些并未被本合同障碍排除。本文是具体构造的“反驳/必要条件”关系材料，不是一般half反例，也没有证明所有多尾惩罚不可能。未认证外审、新颖性或最小性。
''')

add('反例','双单例直积目录的动态平局与静态偏离','customer-attraction/product-singletons-two-player-SPE-not-static-NE','双单例直积目录的动态平局与静态偏离','proved-by-all-five-ordered-decision-comparisons; source-has-JSON-only','两块singleton选择的四主题直积，完整两人SPE实际10/01覆盖全部7客户，冻结对手时10改11获益1/2；动态续局11使该改动无利。',['independent/product_nonNE.json'],r'''
# 输入、完整策略及实际收益

共同目录四标签依次00、01、10、11。两块客户互不相交：X0一名、X1两名、Y0一名、Y1三名；标签ij覆盖X_i∪Y_j，每块客户均为不同单位客户。等价兴趣类型为{00,01}:1、{10,11}:2、{00,10}:1、{01,11}:3，共7客户。两位单位提供者，允许重复行动。

完整纯策略在空根选10；第二人见00、01、10、11时分别选11、11、01、11。这列出全部1+4个有序决策历史。原JSON的certificate.actions共五行，declared terminal_counts=(0,1,1,0)，与路径(10,01)一致。

下面逐历史按单位客户均分列第二人的四个可能收益，列顺序00/01/10/11：

|第一人|选00|选01|选10|选11|指定最佳回复|
|---|---:|---:|---:|---:|---|
|00|1|7/2|5/2|5|11|
|01|3/2|2|3|7/2|11|
|10|3/2|4|3/2|4|01|
|11|2|5/2|2|5/2|11|

例如第一人10后，选01独取X0一名和Y1三名，收益4；选11得到X1的1及Y1的3，也为4，源策略选01保留该平局。第一人00后选10只得X1的2加共享Y0的1/2，即5/2。所有离轨与重复节点均在表中。

沿这些规定后继，根四个强制行动00/01/10/11的收益分别2、5/2、3、5/2，故根选10最优。以上末位表与根表给一份完整纯SPE；未用“直积策略必可分块”的假设。实际(10,01)的两收益为3、4，W=7；两主题覆盖所有客户，OPT₂=7。

# 静态偏离与真实偏离分离

冻结第二人的实际行动01，第一人把10改11，可取X1的2和Y1的3/2，收益7/2，严格大于实际3，增益1/2。故该实际行动组不是同时行动纯Nash均衡。原profitable_static_deviation=[2,3]表示标签索引2→3；两人游戏不把2解释成合法玩家索引。

真实顺序偏离至11后，第二人按同一完整策略改为11，根收益只5/2，所以这个静态获利不违反SPE。这是两个不交singleton块的全部笛卡尔积目录，仍能利用跨块末位平局响应；不能由直积几何自动把动态SPE化为各块静态Nash。

# 来源与复用

1187B原JSON全部字段、全部兴趣类型、五动作、两终局计数、静态改动数组均实读。源没有附此例的Python审计，本页给出自足的完整收益表和解析验证，没有冒称原程序或新CLI成功。它与[人数福利下降](四主题二十二客户的人数福利下降--反例.md)共用“不能冻结后继”的注意点，实例、人数、量词不同；与[历史/计数严格分离](完整历史与计数统一策略的严格分离--反例.md)又是不同净化命题。

本文保“推广/迁移的限制”证据：即使在此简单产品目录，静态最佳回复条件也不是完整动态SPE的必要条件。half余额7>0，不能把该静态NE失败说成福利反例、最小性或一般产品目录界。原件与阅读去向见[本批资源](../../tools/evidence/boss3-c16-resumed/README.md)。
''')

(REPO/'cleanup/workspaces/Boss3/resume-20261102/c/object-index.json').write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n')

add('反例','四主题二十二客户的人数福利下降','customer-attraction/four-topic-twenty-two-unit-all-SPE-welfare-decrease','四主题二十二客户的人数福利下降','proved-finite-all-ordered-SPE-classification-at-m3-m4; once-original-audit-replay','同一22客户四主题目录全部三人SPE覆盖22，全部四人SPE覆盖21；保精确全集递推、106个节点表、两份完整策略与早期27客户版本差。',['independent/population_nonmonotonicity.md#实例与结论','independent/population_nonmonotonicity.md#自足精确递推的正确性','independent/population_audit.py#all_ordered_spe','independent/population_audit.json','independent/population_small.json','independent/population_probe.json','independent/README.md'],r'''
# 同一合法目录下的全部SPE福利下降

在[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)，固定下面同一张单位客户资料，分别用三位、四位单位提供者。四标签依次A/B/C/D，所有有序历史、重复行动和各历史独立平局均保留。

|客户兴趣|不同单位客户数|
|---|---:|
|A|1|
|C|3|
|A,C|3|
|B,C|1|
|A,B,C|2|
|D|4|
|A,D|1|
|A,B,D|4|
|B,C,D|3|

共22客户。三人每份完整纯SPE终局计数恰(1,0,1,1)，福利22；四人每份完整纯SPE终局计数恰(0,0,2,2)，福利21，遗漏A的一个私有客户。A/C/D覆盖全部22，因此OPT₃=OPT₄=22。

结论同时否定最佳和最差SPE福利关于人数的一般单调性。本例由原source独立给出，区别于现有[十二客户三主题反例](人数增加的十二客户全部均衡福利下降--反例.md)：本例四主题、22客户、实际比较三主题对两个重复主题，前者三主题、12客户、福利12→11。它们共享失败命题，实例、完整表和验证事件不可互换。本对象不主张更小实例、最小损失或任意其他人数。

# 精确全集递推及证明

对任意完整有序前缀h，令R(h)为该子博弈所有完整纯SPE可实现的有序终局路径。深度m时R(h)={h}。当前玩家i=|h|，逐行动a先递归求R(ha)，定义
\[
 L(h)=\max_a\min_{z\in R(ha)}u_i(z),\qquad
 R(h)=\bigcup_a\{z\in R(ha):u_i(z)\ge L(h)\}.
\tag{1}
\]
每个R(ha)有限非空，由有限完美信息逆向归纳保证。

必要性：任何完整SPE在每个a孩子都指定一份真SPE，其当前玩家所得至少达到该孩子收益最小值；根实际收益不低于每个真实偏离，因而≥L(h)。充分性：给定保留的在轨终局z及其所在a孩子的完整SPE，在其余每个孩子独立选一份使当前玩家收益最小的SPE。于是所选当前行动不差于所有偏离，孩子仍各自可信，拼成完整SPE。此构造允许不同有序孩子使用不同平局，未把同计数历史绑定。递归因而同时给“全部”与“可实现”，不是只验证一棵实际路径。

按单位客户计算u_i(z)=Σ_(x接受z_i)1/[z中接受x的行动数]，所有分母正。原population_audit.py在完整有序树运行(1)，没有规范solver导入、没有按计数memoization。显示时将终局压成counts不改变递推的有序域。

# 根真实菜单、代表策略与全部结果

完整树给根四个行动后的自身收益范围。这里每一行范围恰为单值：

|强制根行动|三人根收益|三人孩子终局计数|四人根收益|四人孩子终局计数|
|---|---:|---|---:|---|
|A|6|(1,0,1,1)|31/6|(1,0,1,2)或(1,0,2,1)|
|B|9/2|(0,1,1,1)|7/2|(1,1,1,1)|
|C|8|(1,0,1,1)|21/4|(0,0,2,2)|
|D|8|(1,0,1,1)|21/4|(0,0,2,2)|

所以根只能C/D。三人的全部有序SPE路径是CDA与DCA；四人的全部是两C两D的六个排列。后者有21/4>31/6>7/2，根严格排除A/B；三人8>6>9/2。不能将强制根A的四人两终局当作根均衡结果。

保存的代表完整策略三人有21个有序决策节点、路径CDA、收益(8,8,6)；四人有85节点、路径CCDD、收益每人21/4。原population_small.json给全部21/85个history→action，declared terminal_counts也逐字段核与实际一致。原独审按所有1+4+…+4^(m−1)历史恢复后继，对每个合法行动作真实一步偏离比较：84与340项均包含自比较，真正改动分别63与255项。

106份节点表不只是根摘要：每份记录history、floor、四孩子各action/min/max/counts和本节点outcome_counts；本次原程序重新生成全部字段，与154564B冻结population_audit.json整体JSON相等。故表的全部数值已由一次同源精确运行逐项绑定；完整旧字节与新报告都保留以供重算。

# 早期27客户输入的独有去向

1323B population_probe.json不是22客户的同字节前身：其11类型共27客户，除上述九类的部分重数更大外，另有B私有1和A/C/D交叠2。它保存sample52、topics4、instance.players5，以及m1…5最小福利[16,25,26,25,26]。这是早期发现/减重前的独立有限记录；本次保全输入和五个数，没有将22客户独审冒成27客户五个人数的重新认证。

population_small.json才是减重后的22客户版本，保存minimum_welfare_3=22、minimum_welfare_4=21、两终局全集及完整策略。两份版本不可只因同一研究方向就删掉或混用权重。入口提到“独立代码”指实现未导规范solver，不代表另一研究员盲审；source末尾本来明确尚未由他人审查。

# 实际运行、关系与后续

本次原样population_audit.py执行一次，Python3.12.14、exit0、stderr0，环境/命令/cwd/SHA/完整stdout以及新旧报告对比见[证据](../../tools/evidence/boss3-c16-resumed/README.md)。没有重跑原规范发现器或随机减重。一般式(1)已独立给出数学证明，有限表给本例结论。

与[删位修复预算](../引理/删位归纳的有符号修复差与锚定最优边际--引理.md)的联系是反驳“同目录增加玩家使全部均衡覆盖单调”这一充分前提。此处OPT增量为0仍福利可下降，不能无补偿地做跨人数归纳。它不排除带修复差的正确归纳；三人half余额22、四人half余额20均正。没有外审、新颖性、原六人主目标反例或所有人数分类声明。
''')

signedbody=r'''
# 完整signed共同资料下的一个精确超二点

此处改变了真实模型的一条承重条件：共同兴趣类型质量允许负数。仍保留同一张客户表解释所有终局、所有偏离和所有人数为四的均分收益；不能把这些有符号数当作单位客户数。

标签P={0,1,2,3,4,5}，m4。每非空B⊆P用mask(B)=Σ_(a∈B)2^a编码，未列mask质量0，下面56个非零有理数完整指定这张signed表。定义
\[
 U_a(q)=\sum_{B\ni a}w_B/q(B)\quad(q_a>0,\ |q|=4),\qquad
 C(S)=\sum_{B:B\cap S\ne\varnothing}w_B.
\tag{1}
\]
每个所求分母为正。

{WEIGHT_TABLE}

27个正数、29个负数；这些是类型的计数，不是合法客户人数；非零类型确为56。全部259个有序决策历史均指定行动2，即σ(h)=2对每个|h|<4成立。该规则已逐条对比原exact与发现稿259行，因而正文直接给出完整策略，不只给在轨四次2。实际终局q=(0,0,4,0,0,0)，C({2})=1；固定四主题比较J={0,3,4,5}满足
\[
 C(J)=160/79>2C(\{2\}),\qquad 2C(\{2\})-C(J)=-2/79.
\tag{2}
\]
J是原保存的比较集合；源没有把它授为所有四主题的精确最大值。本页也只需(2)排除选定松弛的half行。

# 哪些必要条件确实全部保留

同一signed表自动满足全部真正逐客户线性身份，包括[全支持三角基](../定理/固定人数全支持Shapley的三角身份基与等计数交换--定理.md)、同支持效率Σ_a q_aU_a(q)=C(supp q)及跨标签Shapley关系。除此以外，本固定点的原精确核验检查了：

* 全部336个固定四人收益顶点均非负，最小175/1264。
* 所有259有序决策历史、每历史六行动，共1554项含自身比较均非负；其中1295项是真改动作，最小真激励差0。
* 对每个相同标签a、任意两个不同总数四的终局q,r且q_a,r_a>0，令κ=max_(B∋a)r(B)/q(B)，全部18480条κU_a(r)−U_a(q)≥0，最小0。
* 全部终局按同一类型表计算效率，不是各终局另配客户。

完整σ下每个当前节点偏离b时，真正的后继仍全选2，过去动作保持原有序前缀。逐节点比较上述式(1)的真实完成终局，即是有限完美信息游戏的一步偏离原则；所以σ是这个signed效用游戏的完整纯SPE。它没有被认证为原非负单位客户模型的SPE。

原verify_signed_obstruction.py仅用标准库Fraction、遍历和JSON；从发现稿的每个有理权重乘85320并round后统一除85320恢复精确表，再从全部动作逆序算真实终局。不把round自动当认证：恢复后才对以上全部收益、真实IC、稀释、效率和目标逐项断言。恢复出的56权重、259动作与冻结signed_obstruction_exact.json本次原样执行后逐字节相同；697B报告也逐字节相同。此一次运行exit0/stderr0，无NumPy/SciPy/LP/规范solver导入。全部环境与SHA见[证据](../../tools/evidence/boss3-c16-resumed/README.md)。

# 一个可见负原子已经排除所有真实非负实现

取可见支持A={1,3,4,5}和兴趣模式X={1,3,5}，则
\[
 \mu_A(X)=\sum_{B:B\cap A=X}w_B=-13541/17064<0.
\tag{3}
\]
这不是“本表有负权但也许换一个非负表即可”的弱观察。对任意共同覆盖资料，非空X⊆A的模式质量由这些覆盖数唯一决定：
\[
 \mu_A(X)=\sum_{D\subseteq X}(-1)^{|D|+1}C((A\setminus X)\cup D).
\tag{4}
\]
逐类型证明：若B碰到A\X，求和为0；若B∩A⊆X，只有B∩A=X时交错和为1，其余0。因此(4)不依赖选哪张实现表。

本例八个可见值为

|S|C(S)|S|C(S)|
|---|---:|---|---:|
|4|175/316|1,4|80/79|
|3,4|80/79|4,5|80/79|
|1,3,4|939/632|1,4,5|939/632|
|3,4,5|465/316|1,3,4,5|19885/17064|

代入−C4+C14+C34+C45−C134−C145−C345+C1345即(3)。任何保持本固定层全部收益的共同客户实现，都必须保持这些|S|≤4的C(S)，由三角恢复唯一性可见；非负客户必有μ_A(X)≥0，故不可能存在这种实现。添加看不见的客户或改变高阶覆盖也不能改正这个已可见的负原子。原报告枚举全部|A|≤4的非空模式共发现97个负原子；(3)是保存的最小值，不是仅一个数值误差。

# 发现记录、对称探针与当前范围

原signed_policy_n4_p6_b_best.json另有seed2804/trial0/float value2.0253164556963204，以及一个非负四类型seed字段：mask9:2、28:5、38:25、44:15。它是原文件中额外保存的source_nonnegative_customer_weights；当前signed_policy_search.py的payload没有自动写该字段，不能据现代码声称本次重新生成其历史随机过程。正文数学采用已恢复且全检的signed表；不将该非负seed的福利/策略检查与本表相混。

其余三人/五人signed发现点及五标签对称hub两份输出保在[有限探针资源](../资源/一般半覆盖旧工作区的有限探针与版本边界--资源.md)。尤其local_atoms=true的五标签输出float目标2只施加可见局部正性，不是此四人六标签负原子点；不同数组的优点不能拼接。原README所说他人独审tree进行中没有对应本批完成审稿，不能把原脚本独立实现、同源一次重放与另一研究员盲审/外审等同。

这里精确否定的是“共同signed线性身份、全部终局收益非负、全锐同题稀释和完整形式IC已经足以推出half”。真实客户非负锥比该必要松弛更小；其一般六人half不由本点反驳。与[三标签全局耦合缺口](共同有符号客户的全局三标签耦合缺口--障碍.md)是条件相似而结论不同：后者有每m表示分离族但W=OPT，这里固定m4有负half行且可见四标签负原子。本页无任意人数推广、模型不可能性、最小性或新颖性主张。
'''
data=json.loads((REPO/'archives/customer-attraction/tools/evidence/boss3-c16-resumed/original'/PREFIX/'tree/signed_obstruction_exact.json').read_text())
wt='|mask|兴趣标签B|质量w_B|\n|---:|---|---:|\n'+''.join(f"|{r['mask']}|"+','.join(str(a) for a in range(6) if r['mask']>>a&1)+f"|{r['weight']}|\n" for r in data['weights'])
signedbody=signedbody.replace('{WEIGHT_TABLE}',wt).replace('这些是类型的计数，不是合法客户人数；非零类型确为56。','这些是类型的计数，不是合法客户人数；非零类型确为56。')
add('障碍','共同有符号客户的四人超二福利与局部负原子','customer-attraction/four-player-common-signed-customer-super-two-and-negative-local-atom','共同有符号客户的四人超二福利与局部负原子','exact-fixed-signed-relaxation-obstruction; once-byte-identical-original-replay; not-real-CAG','四人六标签同一56型signed表的全常2完整SPE有W1与固定比较160/79；所有收益非负与18480稀释仍不能排除97个可见负原子，显式八覆盖行排真实实现。',['tree/signed_obstruction_exact.json','tree/signed_obstruction_report.json','tree/verify_signed_obstruction.py#run','tree/signed_policy_n4_p6_b_best.json','tree/signed_policy_n4_p6_b_run.json','tree/signed_policy_search.py#main'],signedbody)

(REPO/'cleanup/workspaces/Boss3/resume-20261102/c/object-index.json').write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n')

add('程序','计数联合MILP的完整历史展开与限时证据','customer-attraction/count-joint-MILP-full-history-expansion-and-time-limit-record','计数联合MILP的完整历史展开与限时证据','source-contract-complete; exact-trivial-saved-primal; five-player-dual-unrecovered; no-fresh-optimization','count-dependent共同策略为真子类；保存五人七标签45秒限时ratio1点仅一全兴趣客户，完整2801动作有330计数态且无精确对偶；二人自测另有可读3/2对偶。',['credible/count_joint.py#candidate','credible/count_joint.py#main','credible/count_joint_7_5_00112.json','credible/count_joint_selftest.json'],r'''
# 真子类、变量与归一化

6287B原count_joint.py全文读。它在p标签、m人共同非负客户模型中联合选择类型质量及一份依计数的完整策略。每个非空兴趣mask对应w_B≥0，共2^p−1个；每个深度<m的计数k和标签a有连续U_(k,a)及二元z_(k,a)。U表示从该状态按所选共同计数策略完成后，一位a标签者的终局收益行，不是仅当前动作的短视收益。每状态Σ_a z_(k,a)=1。

给定有序目标path，沿其每个计数固定z_(k,path_i)=1。代码先累加整条path所得root变量实际上是**目标终局计数**；真正空根另名zero。不能把root误读成未走过的前缀。实际覆盖行c取该终局支持，指定比较支持O取portfolio；归一化c·w=1。

全部连续U置于[0,m]，空根被指定行动的U≤1。对每个主题T加|T|≤mU_(zero,path0)，及Σ_B w_B≤mp。前者是任何真实SPE可由根改T得到|T|/m保底的必要约束；实际总收益为1使实际根收益≤1，所以这些界在其所拟域中合理。再加Σ_a q_actual,a U_(zero,a)=1作终局效率。比较可选threshold仅加O·w≥threshold；它不是已有证明。

对每个状态k、可能指定动作a及每个标签t，用z_(k,a)激活U_(k,t)=U_(k+e_a,t)，若孩子深度已m则直接代单位客户最终收益线性行。对每个偏离b激活U_(k,a)≥U_(k+e_b,b)。两方向等式和真实激励都用m作条件常数；当z=0约束松弛。当索引合法、path长度m、portfolio为合法不同标签时，当前两份报告满足这些输入前提；程序没有额外的通用非法CLI容错证明。

所有同计数历史被强制共用一个动作和同一未来映射，所以它是真正的count-dependent子类。输出后明确展开每个h∈{0,…,p−1}^{<m}，令action(h)=policy(count(h))，再交给固定完整策略客户锥恢复/核验。不能从该MILP的阴性、最优值或限时界推到全部历史依赖SPE；一般净化已被[三人五主题严格分离](../反例/完整历史与计数统一策略的严格分离--反例.md)否定。

# 浮点发现与精确固定策略检查的边界

SciPy milp最小化−O·w，保存status/message/count_states/binary_actions/rows/variables/elapsed、float objective及float dual bound；floating_only恒true。有incumbent就按z最大者提策略，即使因时限停止也可进入后续；若res.x为空则proof=null。

后续StrategyCone.optimize只针对已经选定的完整策略重新优化客户质量，若精确primal恢复成功才整数克隆、独立逐历史检查，并用规范verify_certificate再验一次。saved ratio来自这个整数输入的实际全目录OPT/W，不是把MILP float目标直接改成定理。精确对偶失败时primal仍可保存，dual_bound=null且exact_dual_optimal=false。已经对读仓内[固定策略锥源码副本](../../tools/evidence/strategy-cones/original/tests/audits/customer_attraction_strategy_lp.py)，理解其βc−Gᵀμ≥O且μ≥0合同；本批没有将该比较副本冒成本次实际import绑定，没有运行或安装NumPy/SciPy/MILP。

# 五人七标签的全部保存字段及真实内容

count_joint_7_5_00112.json共有381649B。m5/p7，path=(0,0,1,1,2)，portfolio=(2,3,4,5,6)。保存MILP：

|字段|原值|
|---|---|
|status/message|1 / Time limit reached. (HiGHS Status 13: Time limit reached)|
|count_states/binary_actions|330 / 2310|
|rows/variables|46540 / 4747|
|elapsed|45.219719317秒|
|floating_objective|1.0|
|floating_dual_bound|3.7234042553191466|
|floating_only|true|

这些计数相合：Σ_(d=0)^4 binom(d+6,6)=330，每态7个z与7个U，加127个w，得4747变量。时限上界只是该数值子类搜索的float界，绝不是全历史SPE的严格上界。

proof保存127项integer_clones，前126项全0、最后mask127恰1，即唯一一位对全部七标签感兴趣的单位客户。全部2801个有序history→action行逐项消费，required set恰Σ_(d=0)^4 7^d=2801、无重复/缺漏、每动作合法；同计数共用330个动作，实际follow为00112，声明终局(2,2,1,0,0,0,0)一致。

对该真实输入，不论所有人如何行动，同一客户最终总负载恒5，故每位收益恒1/5；任意完整策略在每个历史均最优。这一直接理由自足认证保存策略的完整SPE，毋须再跑19607项逐节点比较。W=OPT=1、ratio=cone_comparison_optimum=1。exact_dual_optimal=false、dual_support=[]、dual_bound=null、all_ordered_histories=2801，全部字段按原样保。它只给一个平凡可行点，没有证得该策略锥最优，更没有证得整个MILP最优或五人坏比率不存在。

# 二人两标签自测的可读精确对偶

1185B count_joint_selftest.json：m2/p2、path00、portfolio01，MILP status0、3计数态、6二元动作、38行、15变量、elapsed0.00461382000003141，float objective=dual bound=1.5。完整三节点动作全0；整数类型(w_0,w_1,w_01)=(2,1,0)，实际两人选0、每人1，W2，OPT3，ratio3/2。

在该固定策略锥，末位历史0的真实比较是w_0/2−w_1≥0，历史1的比较是w_0−w_1/2≥0；根重复第一条。按排序的唯一非零IC行，row0=(1/2,−1,0)。令c=(1,0,1)、O=(1,1,1)，则
\[
 \tfrac32c-row0-O=(0,0,\tfrac12)\ge0.
\]
这对应保存dual_support=[[0,1]]、dual_bound3/2及exact_dual_optimal=true。配合(2,1,0)取等给该固定锥精确值3/2；没有从一份自测冒推出全部任意p,m。此对偶已直接解码，不需重跑旧优化器。

# 文件使用、依赖与关系

main guard保护import；命令默认p7/path00112/portfolio23456/45秒，有可选threshold，output必填且已存在拒写。ROOT由脚本parents[5]指仓根，sys.path加入仓根及tests/audits；依赖customer_attraction、customer_attraction_strategy_lp、NumPy/SciPy及稀疏矩阵。输出以serializable保存有理数为字符串，并另打印删去大proof或大动作/dual的摘要；stdout不是完整证书。

本次原件全字节保存，JSON所有字段、全部2801+3动作及127+3克隆项均完成解析和语义核对，数据阅读程序只核保存结构/平凡理由，0原MILP/LP/随机扫描。见[证据](../../tools/evidence/boss3-c16-resumed/README.md)。关系可登记为“实现：计数子类→完整历史展开”“有限验证：自测及保存primal”“限制：历史净化反例排除全域推论”；不得把文件名7_5或status1当一个一般数学结论。
''')

add('资源','十三人精确税证书的构造与三重内部审计','customer-attraction/thirteen-player-refined-tax-constructor-and-three-internal-audits','十三人精确税证书的构造与三重内部审计','complete-source-and-all-fields-review; mature-SPE-result-reused; no-new-thirteen-player-audit','保全同SHA27243节点packet、构造器和三条不同内部证据链；盲BI27244状态与冻结packet分别标记，历史padding有限发现未升任意k。',['README.md','CLAIMS.md#B8-REFINED-ACTUAL-TAX-NO-v1','security/README.md','security/build_refined_tax_packet.py#build','security/padding_probe.py','security/audit_refined_tax_packet.py#audit','security/refined_tax_k10_packet.json.gz','security/refined_tax_k10_audit.json','credible/audit_refined_tax_blind.py#main','credible/refined_tax_blind_audit.json','credible/audit_security_packet.py#main','credible/security_packet_audit.json','root_audits/check_automaton.py#check','root_audits/check_automaton.py#self_checks','root_audits/refined_tax_root.json'],r'''
# 已成熟的数学结果与本批新增来源范围

[实际分数税反例](../反例/实际均匀缩放负载的弱付款桥--反例.md)已经自足保存13提供者、36单位客户、六不同主题及全部历史策略的精确税桥失败；[全历史核验](../计算/分数负载四主题族的全历史核验--计算.md)已有原自动机一次成功。本文补全本工作区当前认领原件的构造、三条审计实现、全报告字段和旧状态，不重复把成熟同证书授成新发现或再次112050-IC成功。

单位客户依次为A:2、B:2、T:1、TD:1、TE:1、ADE:3、BDE:1、P:25。完整策略actual=P十次/A/A/B，前12收益5/2、末位3，W33、OPT₁₃36；α12/13下g=(65/37,39/25,3,2381/925,2381/925,325/133)，G708669/123025，mM−W−G29481/123025>0。真正静态背景P九次/A/B/T给所有纯查询≤5/2，所以W−13v₁₃≥1/2，half余额30。这里复用的是精确既有定理，不把固定税桥反例扩大为安全值或half反例。

# 完整packet逐字段阅读与冻结身份

压缩原件372216B，SHA256 bad2b15d1abe89d9fa8671df84de8638a4b1ca46279712baa5482abb2bdf18ce，本次导出字节与现成熟输入相同。已解压解析全文件与全部27243条node记录：18675条字段恰action/children/counts/desired，8568条恰counts/terminal；全部6维count、规定action、六child索引、desired向量及terminal标记按其数学角色消费。另读scope、八兴趣型instance、root0、expected_path、expected_terminal_counts和constructor_stats，未以只读头部代替完整数据。

全部node深度数量为[1,6,25,66,137,263,473,803,1298,2013,3014,4380,6196,8568]；有27132个不同count向量，6094个不同desired向量。constructor_stats为count_states27132、terminal_states8568、retained_outcomes27944。等计数重复不是错误：自动机状态还含承诺终局信息，所以计数相同的有序历史可不同续局。原每行动唯一边、深度加1和全可达的成熟认证保证每个完整有序历史对应一个已查节点；自动机不是计数Markov净化。

本次保存字段阅读只统计/核同已认证输入与图式，不重新计算该成熟自动机112050项激励，不重授这次读文件为新独审。完整节点字节、原四份报告及其实现均保[原件目录](../../tools/evidence/boss3-c16-resumed/README.md)。

# 构造器与padding的准确依赖

2798B build_refined_tax_packet.py使用可导入的规范Instance/ExactSPESolver，读取仓根examples/customer_attraction/coverage_opportunity_failure.json。已对读现存冻结副本：五标签A/B/T/D/E，前七兴趣型共11客户，确与上表core相同。build默认k10、assert k偶数，添私有P及5k/2客户，总人数k+3。目标counts=(2,1,0,0,0,k)，必须先被集合值BI判在root outcomes中。

构造状态key=(prefix counts, promised terminal)；对每个行动取孩子的最低当前收益终局作偏离惩罚，规定孩子则保同一promise。挑选可达到目标且当前收益≥真实floor的动作；当promise为目标、core全空、P未达k时优先P，之后优先0/1/…/5。它递归为每个观察行动建边，terminal要求counts=promise，最后assert实际P^k AAB。输出路径硬编码refined_tax_k10_packet.json.gz，即使修改build(k)也会覆盖这个同名文件；有main guard，但执行是发现/构造程序，须有规范solver与fixture，不能当独立审计。

1607B padding_probe.py是另一种尺度：core人数各翻2，P客户5k，总人数仍k+3，默认k列表1/2/3/5/8/11；它对给定有限k查目标存在，再沿指定P^k AAB逐步查阈值，打印M/G/min_u/individual gap及stats。k10的输入恰是构造器k10单位资料的二倍缩放，但默认列表没有k10。源码没有本批独立保存的各kstdout，不能虚构默认六个都成功。该程序也没有任意k的解析闭包；旧README已指出直接交错旧SPE与固定P次数在额外core进入枝可能失可信性。任何任意k推广仍须新的全分支证明。

# 三条内部证据链的差异

|证据实现|真实输入/依赖|关键方法|冻结报告的范围|
|---|---|---|---|
|security/audit_refined_tax_packet.py|同一gzip；标准库|逐36单位客户、整数公分母360360；查所有边/可达、逆推终局并核desired|27243节点/18675决策；112050含self IC，19164ties，min0|
|credible/audit_security_packet.py|同一gzip；标准库Fraction|忽略所有desired，按counts深度从真child动作反推终局；核每深度历史重数|93375真改动作，min0，全可达，表示全部6^d历史|
|root_audits/check_automaton.py|同一gzip；标准库Fraction|递归由真边重建；校单位输入、效率、OPT子集枚举及通用覆盖税|112050含self比较，固定同数值；另零客户/一人和两负控|

三者都没有导入规范发现器、BI、NumPy或LP。security有desired断言；credible完全忽略该字段；root从真边算后再核可选desired，不能把三者说成同一实现。credible报告source_sha绑定同压缩原件；root还绑定checker_sha f54323bee5c93c6a97ae6d930a89e793f107904452fefe847b86f42ec6c48daf，与本批源码核同。原root的自检四项分别零客户PASS、一人PASS、盈利偏离被拒、错误观察边被拒。报告是旧运行证据，本次无这些入口新运行。

credible的每深度历史总数是6^0…6^13，决策历史总数2612138803、真改动作总数13060694015、叶历史13060694016；这证明压缩图展开的覆盖，不表示原程序逐十余亿历史另循环一遍。node重数沿每条观察边累加、每层等6^d、所有node均可达，给严谨的完整历史证据。

# 不读packet的盲BI重建是另一条证据

6856B audit_refined_tax_blind.py硬编码同一13人/六主题/36客户，不读取发现者packet，不导规范solver。它枚举8568个终局counts、直接逐单位客户算整数收益，以集合值BI递归全部27132计数态，再用状态(counts,promised outcome,active-path bit)构造自己的完整自动机。active只强制预定P^10AAB路径，其余合法动作选首个；每偏离孩子取使当前收益最小的可信终局。集合值count递推允许每个孩子独立promise，故不是把所有等count历史统一行动。

冻结refined_tax_blind_audit.json保存root outcomes11、27244个自动机状态、18675决策、93375真改动作、完整14层重数及13个实际路径准入检查。每个前12步target payoff与floor都5/2，末步3；精确W/OPT/g/G/gap同上。它比固定gzip多一个终端状态（8569对8568），而源码状态含active bit；这是不同构造表示的报告，不应把27244强改为27243或说两份策略节点逐字节相同。此源没有输出完整盲自动机节点文件；本批只保实际保存的全部字段，不虚构缺失的节点载体。原seconds0.9087751190000972是其旧运行时长，不能当本次时间。

CLI要求--output且拒覆盖已有文件。实际展开及IC检查发生在自己新建的图，数学可比性来自同一单位输入与定义级比较；“blind”指原研究流程声明未读packet，独立源码支持无导入，不等于我们本批也盲读、他人外审或全球新颖性认证。

# 旧身份、状态及复用去向

旧README标Boss8、workspace R-c50…、恢复基线461d46021e417fa5f6efbac4f7d8a7975fae60b5；CLAIMS的legacy B8-REFINED-ACTUAL-TAX-NO-v1保相同存在量词。此为旧资料身份，当前清洗者是Boss3；旧“六名实际并行”“root保存/无Git”等都不变成本次调用或推送事件。本批所有来源都以冻结commit和精确路径绑定。

本页与成熟反例是“来源/实现/独立有限核验”关系，和[同题删位静态补贴障碍](../反例/同题冻结删位静态补贴的十三人障碍--反例.md)是同一旧策略的另一静态推论，不重复造SPE。与新全支持signed障碍仅共享均分表示问题，模型正性不同，不能相互担保。当前一般half/六人half及真正全路径共同安全钱包仍需各自真实证明。本文完成原件清洗，无新十三人运行、无任意padding族、外审、新颖性或最小性声明。
'''.replace('等计数重复不是错误：','等计数重复不是错误：'))

add('资源','一般半覆盖旧工作区的有限探针与版本边界','customer-attraction/general-half-workspace-finite-probes-and-version-boundaries','一般半覆盖旧工作区的有限探针与版本边界','complete-source-contracts-and-finite-record-preservation; unresolved-probes-not-theorems','汇合交换对称菜单、末位加强式、Markov1000阴性及三/五人signed和两hub输出的独有有限内容；保存原动作与权重但不给未有精确恢复的点新SPE资格。',['README.md','workspace.json','independent/README.md','background/exchangeable_probe.py','background/exchangeable_probe.json','global/additive_terminal_search.py','global/last_player_probe.py','independent/markov_root_probe.py','independent/markov_3x3.json','tree/signed_policy_search.py','tree/signed_policy_n3_p6_best.json','tree/signed_policy_n3_p6_run.json','tree/signed_policy_n5_p6_best.json','tree/signed_policy_n5_p6_run.json','tree/symmetric_hub_probe.py','tree/symmetric_hub_local0.json','tree/symmetric_hub_local1.json'],r'''
# 总入口、模型与独有数据的组织

本页保留旧R-c50fecc37aa44fb4a69a2122bb70e5fe工作区中没有形成普遍定理的有限程序/输出。已全文读全部17个Python、7个Markdown及workspace身份入口及所有JSON/压缩字段；原件48个共1260542B逐个冻结size/SHA核同，逐源去向见[证据清单](../../tools/evidence/boss3-c16-resumed/README.md)。这是原研究资料的有限合同，不以入口“独审进行中”或“OPEN”代替当下数学判断。

原workspace.json的schema1/save customer-attraction/actor R-c50…/instance4aa4c59ccdd743df8bb16563a1ef8912只记版本身份；不含新数学命题。旧README的一般目标量化任意人数，当前仓另有五人证明、焦点恰六人；旧一般OPEN与本批未解决六人相容，但“所有旧分支都已有核验”不是本文声明。原independent入口停止残余覆盖/计数净化两条路的理由已分别由真实反例接续；新22客户与产品实例已各自成正文，不以历史入口压缩代替它们。

# A. 两群内部交换对称的菜单松弛

1738B exchangeable_probe.py令两群各L标签，客户类型按一群命中a个、另一群b个的轨道(a,b)分组。变量为**整个轨道总质量**，每个具体类型分到该质量/binom(L,a)binom(L,b)；不是每类型同样大的轨道质量。非负有理质量可乘共同分母与轨道大小成为真实单位客户，但可信策略还另有义务。

一根选X标签、m−1个不同Y标签跟随的根收益系数为
\[
 r_X(a,b)=\frac aL\sum_{h=0}^{\min(b,m-1)}
 \frac{\binom bh\binom{L-b}{m-1-h}}{\binom L{m-1}(h+1)},
\]
r_Y交换a,b。代码的miss(L,a,t)=binom(L−t,a)/binom(L,a)是t个标签全避开的比例。比较集合有r个X、m−r个Y时覆盖系数
\[
 o_r(a,b)=1-miss(L,a,r)miss(L,b,m-r).
\]
每r单独解非负轨道质量LP，限制r_X·w≤1、r_Y·w≤1，最大化o_r·w。**没有加入以后每位提供者的真实激励，也没有给出完整行动树或实际福利**；故这是菜单松弛，不是一个SPE效率实例。

6387B输出完整14组L=m=2…15，每组保best的r/value/support及m+1个all_values。所有浮点值本次完整消费，逐项与
\[
 2[m^2-r(m-r)]/(m+1)
\]
在1e−10内相符。m≥3保存best支持仅轨道(1,1)，质量2m²/(m+1)；该轨道确有根收益1和该公式的比较覆盖，给明确有理可行点。m2保存另一个同值支持(0,1)与(2,1)，质量各4/3。m12/m15的best r取m而非0是float微差，两端对称，不能据此宣称真不对称最优。

源码只将非零LP质量limit_denominator(100000)后保存，没有精确恢复/dual检查；本页不把14组float optimum转成任意m上界定理。本次没有导入SciPy或重跑这14组；缺的正是完整后继可信性与共同实际预算。

# B. OPT≤2W−u_last的两个发现器

1075B last_player_probe.py仅两人。默认k4，枚举每个根行动后的末位回复函数reply∈[k]^k；固定根选0，加入所有根真实比较及每个末位节点的全部最佳回复，再以actual coverage=1归一，在全部至多两主题比较（允许重复的组合表示）优化O−2C+u_last。覆盖重复不增益，所以此比较域合理。全部系数送浮点linprog，无Fraction恢复；发现positive>1e−7或unbounded即提前返回。k4若不提前停将有4^4个reply、每个10个比较LP；源码没有随批冻结stdout/结果JSON，不能说这些都执行完或都阴性。

2471B additive_terminal_search.py为任意指定m/k/trials/seed。用Random(seed)给每非空类型以.27概率取1…50整数质量，从每个完整有序历史递归选择终局收益最大动作（允许1e−5浮点平局）。对这个固定完整动作树建立所有非自真实激励行，重新优化非负客户质量、actual C=1，以每个min(m,k)不同标签比较最大化O−2C+u_last；正gap>1e−7保存浮点权重、全部动作、trial/seed/actual/opt_index。

这不是集合值全SPE枚举：一次只取一棵由随机种子和平局给出的树，然后在其锥内优化；数值输出也没有精确可行性证书。没有本批对应failure JSON或运行日志，不能从源码名称/未附文件推断加强式普遍真或假。加强式若普遍成立可推出half，但支付末位那一份额外余量是新的承重条件；未与成熟末两人引理混并。本批0这两个入口运行。

# C. 计数策略净化的1000例历史阴性

3568B markov_root_probe.py独立于通常集合值求解器的策略选择方式：按从深到浅的count DAG，对每个计数态统一选择一个最佳孩子终局；当不同并列动作产生同一终局映射时取商。全层映射选完才记一个根终局，不能逐状态各自由选而忽略count汇合相容性。

它仍导规范Instance/CustomerType/ExactSPESolver求完整历史终局全集作比较。若找到的count根集合已等于全集可提前停，这时无需枚举所有count策略；若达到cap但未相等则标不完整、该输入skipped。192B markov_3x3.json全部字段：status finite_no_counterexample、samples checked1000、skipped0、max_quotient_policies232、topics players均3、seed816、cap1000000。每非空类型重数由randrange(5)产生，有限范围不覆盖任意目录/客户规模。

原independent入口已经停止把它作正面路线；现有[三人五主题严格分离](../反例/完整历史与计数统一策略的严格分离--反例.md)给合法反例及完整枚举，故不能延续“无反例所以净化或真”的一般结论。当前0重跑1000样本，原保存的每个参数与终止计数完整保留。

# D. 三/五人signed策略搜索及数值候选

5227B signed_policy_search.py枚举固定n,p的全部终局收益行F，构造全部同标签锋利稀释和−F≤0，浮点归一化、round12位去重。策略由某张质量表逆向归纳产生完整history→action；初始为稀疏非负随机表，LP得到signed warm后后续可由signed表取策略，因此不保证所有发现策略都来自真实客户实例。

每棵完整树的全部非自IC追加到同一signed类型变量w∈R^(2^p−1)；实际覆盖归一化1，最大化一个min(n,p)标签比较的覆盖。signed覆盖未必单调，代码只选这些比较集合，不能把任意已存target自动命名完整signed OPT。LP成功后逐权重limit_denominator(10^7)保存，未做精确原始/对偶检查。policy(exact=True)函数虽存在，main没有调用这一支；原发现文件里的分数字符串不能仅因是分数就当精确SPE。

全部两组报告逐字段消费、原动作全文保存：

|发现文件|seed/trial|保存float比较|完整动作行|非零signed权重|实际路径/计数|
|---|---|---:|---:|---:|---|
|n3_p6_best|2802/10|1.8333333333333384|43|41（22正/19负）|3,5,3 / (0,0,0,2,0,1)|
|n5_p6_best|2801/0|1.9758711808833556|1555|62（30正/32负）|5,4,4,4,4 / (0,0,0,0,4,1)|

n3_run完整12条trial0…11，n5_run完整60条trial0…59；每条target/root/value/elapsed均保留，末elapsed分别1.0172843933105469与400.94562792778015秒。它们不是当前新计时，也没有足够原argv/版本资料让本页宣称历史执行逐字节重建。n3最大值trial10，n5最大值trial0；无null记录。五人旧候选没有超过2，不能拿它代替现五人一般证明；负客户表也不在该证明原模型内。

这两份saved actions已完整核required有序history域、无重复/缺漏、合法动作并恢复实际路径；没有再授全部有理化权重IC/稀释可行性。与此不同，四人六标签点有单独exact恢复及全检，已成[精确signed障碍](../障碍/共同有符号客户的四人超二福利与局部负原子--障碍.md)，其一次成功不自动转移到三人/五人文件。源程序达到float>2+1e−6会提前停，四人b_run仅一条与该停止条件相符，不把单条探索当穷尽策略空间。

# E. 五标签对称常hub的两份LP输出

1955B symmetric_hub_probe.py固定n4/p5、hub0。九轨道(h,k)指是否含hub及命中四卫星中的k个；变量是**每个具体类型质量**，与A节的轨道总质量不同，展开矩阵O对每个mask仅指向其轨道、不除binomial。加入全常hub策略在每个过去count的偏离行、所有收益非负/锐稀释；local=true时另加每个|A|≤4、每个非空模式X的投影质量非负。

原输出：local0目标float2.0253164556965357，九轨道按(0,1),(0,2),(0,3),(0,4),(1,0),(1,1),(1,2),(1,3),(1,4)的分数分别
\[
 (65/316,0,0,-9/158,-41/158,55/158,-15/158,15/158,9/158).
\]
local1目标2.0，同序
\[
 (1/6,0,0,0,-1/3,1/3,0,0,0).
\]
两份831B/786B JSON所有m/p/hub/orbits/objective/local_atoms字段完整保。目标比较是四个卫星并集，actual hub覆盖归一化1；有理化后没有附精确可行性/dual证书。local1有负hub-only系数，局部≤4的非负不等于一张全局非负客户表；也不能把local1条件贴给local0的>2目标。本文只保存两个明确候选和源LP合同，不发明未交付的精确核验。

此脚本没有main guard，import就准备矩阵并执行两个LP，且会覆盖symmetric_hub_local0/1.json；不能为了看函数而安全地import。它依同目录signed_policy_search.prepare及NumPy/SciPy。本次0 import/LP，冻结原输出未改。

# 关系与实际运行账

上述未闭合程序都保可接续的输入域、目标、限制与真实保存点；没有因为是探索稿就退休。有成熟反例的Markov一般净化正确关闭；真正开放的终局加强式、全后继可信性或精确恢复缺口准确保留。

本批只原样运行四个必要有限入口各一次：22客户population、四人signed exact、全支持Shapley、互惠尾。所有输出和执行身份见[证据](../../tools/evidence/boss3-c16-resumed/README.md)；没有新LP/MILP、随机扫描、十三人IC或优化器安装/import。关系登记材料已经按表示/反驳/实现/有限验证分别写在正文，暂未以本阶段临时整理调用正式三级图build；不能为连通把这些不同松弛拼成逻辑依赖。外审、新颖性、最小性与一般福利常数均未由本页认证。
''')

# Correct a LaTeX spelling while retaining the source's nonnegative integer domain.
for rel in files:
 p=STATE/rel
 p.write_text(p.read_text().replace(r'Z_{\u22650}',r'\mathbb Z_{\ge0}'))
(REPO/'cleanup/workspaces/Boss3/resume-20261102/c/object-index.json').write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n')
