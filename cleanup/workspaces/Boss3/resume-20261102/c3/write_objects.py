from pathlib import Path
import json
R=Path('/workspace/scratch/cd4305a146e6/co-work-anl-boss3');W=R/'cleanup/workspaces/Boss3/resume-20261102/c3';B=R/'archives/customer-attraction/tools/evidence/branch-geometry-source-resumed-boss3';S=R/'archives/customer-attraction/state';PFX='research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/branch_geometry/';C='68fad804ec5946cb296f77dc5b336308a66abf12';objects={}
def add(cat,title,id,status,summary,sources,body):
 rel=cat+'/'+title+'--'+cat+'.md';kind={'引理':'lemma','计算':'computation','程序':'program'}[cat]
 refs=[p if p.startswith(('research/','evidence/','tests/')) else PFX+p for p in sources]
 fm='---\n'+f'id: {id}\nkind: {kind}\ntype_tag: {cat}\ntitle: {title}\nstatus: {status}\nsummary: {summary}\nsource_refs:\n'+''.join('  - '+json.dumps('source:'+C+':'+p,ensure_ascii=False)+'\n' for p in refs)+'---\n\n'
 (S/rel).parent.mkdir(parents=True,exist_ok=True);(S/rel).write_text(fm+body.strip()+'\n');objects[rel]={'id':id,'source_paths':refs}

rows=json.loads((B/'replay/commuting/stdout.json').read_text())['rows']
table='|应用族|λ|精确slack|约值|\n|---|---:|---|---:|\n'+''.join(f"|{x['family']}|{x['lambda']}|{x['slack']}|{x['approx']:.12g}|\n" for x in rows)
body=r'''
# 三人真实节点与同负载双尾上界

采用[共同目录完整历史单位模型](../定义/共同目录完整历史模型--定义.md)。单位客户与提供者、有限非空共同目录、全部有序历史纯SPE；空主题、重复、零客户与任意离轨平局保留。固定一份完整σ，在一个真正恰剩三人的节点，旧客户负载为b_x，当前规定行动者最终利润v。取任一合法查询Q，q_x=1_Q(x)，置p_x=b_x+q_x。

假设已知同一目录、同一负载p下的一份真正两人SPE，其结果(R,S)、两人利润r,s。它可以来自另一个有序历史，回复政策无需相同。定义
\[
 H=r+s+\sum_{x\in R}\frac1{(p_x+1)(p_x+2)}.
\]
[末两人税界](固定背景两人税界--引理.md)保证对任意合法比较对(P,Q')，其两人总利润
\[
 R_p(P,Q')=\sum_x\frac{c_x}{p_x+c_x}\le H,\qquad c_x=1_P+1_{Q'}.
\tag{1}
\]
零分子项取0。非零背景时r+s与R_p都是剩余两人利润，不能当完整终局覆盖。这里转移的是共同目录下静态最大两人总利润F₂(p)的上界，不识别重新排序历史的策略。

# 全部非负λ的精确界

对每个实数λ≥0，令L_λ(p,0)=0，q=1时p≥1并定义
\[
 L_\lambda(p,1)=\min\left\{\frac1p,\frac{1+2\lambda}{p+2}\right\}.
\]
则
\[
 \boxed{v+\lambda H\ge\sum_xL_\lambda(p_x,q_x).}\tag{2}
\]
证明：当前人真正改Q后，原σ的真实后两人结果(P,Q')具有旧负载p，故v≥Σ_x q_x/(p_x+c_x)。由(1)，H≥Σ_x c_x/(p_x+c_x)。非负λ相加得到Σ(q+λc)/(p+c)。若q=1，p≥1，函数对实c≥0的导数符号为λp−1，所以在c∈{0,1,2}上的最小值位于0或2，正是L。若q=0，贡献非负；p=c=0按零分子0处理。即证，无需任何前缀交换或匿名平局。

λ1时p≥1使1/p≤3/(p+2)，故
\[
 v+H\ge\sum_{x\in Q}\frac1{b_x+1}.\tag{3}
\]
亦可逐客户验q1时q/(p+c)+c/(p+c)−q/p=c(p−q)/[p(p+c)]≥0，q0另按非负处理。λ0则为通常三人安全分母1/(b+3)保底。λ须作为整行全局标量选定，不能每客户任挑不同λ而只付一次v/H。

# 真有序前缀的三个应用

五人旧索引实际(A,B,C,D,E)，固定同一σ的真实分支(A,T_i,H_i,I_i,J_i)以及(A,B,T_i,R_i^AB,S_i^AB)、(A,E,T_i,R_i^AE,S_i^AE)。在真正第三位节点(A,T_i)以B查询，后两人的负载a+t_i+b与已知(A,B,T_i)后的双尾相同，故
\[
 z_{H_i}+\lambda H_{AB,i}\ge\sum_x L_\lambda(a_x+b_x+t_{ix},b_x).
\tag{4}
\]
查询E并用AE已知双尾给第二族。对五i求和只需原second_hist和AB/AE直方图及共同查询重数，未要求跨族同一索引配对；这个特定和的分族结构可复用。

另在真实第三位(A,E)查询B，使用已知(A,B,E)后的双尾(X,Y)，得到
\[
 z_U+\lambda\left[z_X+z_Y+\sum_x\frac{x_x}{(a_x+b_x+e_x+1)(a_x+b_x+e_x+2)}\right]
 \ge\sum_xL_\lambda(a_x+b_x+e_x,b_x).
\tag{5}
\]
两种有序前缀后续可完全不同，式(4)(5)只借同负载下F₂相同这个静态事实。[交叉历史均匀对称化](交叉有序历史的均匀净成本对称化--引理.md)保的是另一种有符号cap转移，[一般收费审查](../审查/一般目录全局收费交接与索引二层真实节点--审查.md)已否定免费交换前缀席位；与本引理不冲突。

# 旧64原子点的全部λ测试

对这些应用，q1时p∈{1,2,3}，折点仅λ=1/3、1/2、1，另含端点0。每段slack为仿射；λ≥1后右侧不变、左侧斜率H≥0。因此四折点全正就说明该**固定输入**的整条λ≥0族全正，不是由几个数外推一般博弈。

2116B原audit_commuting_prefix.py全部读，读取同SHA旧64原子primal，用Fraction完整评三族×四折点。本批在隔离目录原样一次执行，exit0/stderr0；原源未附独立输出文件，新2409B stdout保全部结果：

{TABLE}

所以这三族直接应用没有排掉旧437点；不能推断对较新557/728等模板的作用。与[第二位D七行包络](第二位复制实际D的七行投影包络--引理.md)不同：后者另暴露真正新分支、确切排该旧点，本引理不借那次负差作自己成功。

4190B数学稿的“root independently reconstructed”是旧内部历史；本次是作者重构一般证明和同一原诊断一次运行，未加外审、全球新颖性或half结论。完整原件/运行/比较见[证据](../../tools/evidence/branch-geometry-source-resumed-boss3/README.md)。阶段三关系是末两人税界依赖、同负载静态迁移、三个条件应用和一次固定点有限诊断，不是政策可交换定理。
'''.replace('{TABLE}',table)
add('引理','同负载末两人税界的前缀迁移','customer-attraction/same-load-two-tail-tax-prefix-transfer','proved-general-lambda-interface; old-fixed-point-all-knots-positive; once-original-diagnostic','三人真节点查Q后，用任一同负载真双尾的税上界支付可达双尾总利润；端点最小化得全部λ界，保不同有序历史政策不相同及十二折点未排旧点。',['commuting_prefix_tool.md','audit_commuting_prefix.py'],body)

add('引理','第二位复制实际D的七行投影包络','customer-attraction/second-position-actual-D-seven-row-projected-envelope','proved-universal-necessary-envelope; old-primal-exact-separation-reused-from-independent-review','固定完整五人策略的真第二位→D分支给七个非负整行，任意非负共同权经逐客户八态最大化得到必要包络；对称权可六态，旧点负证书复用不重跑。',['second_D_envelope.md','separate_second_D.py','separate_second_D.json'],r'''
# 真实分支与可见旧数据

采用[共同目录完整历史单位模型](../定义/共同目录完整历史模型--定义.md)，恰五位单位提供者、有限客户和共同有限非空目录，固定任意完整纯SPE。空主题、重复行动、零客户和所有有序历史平局保留。实际路径(A,B,C,D,E)，第二位收益u₂；任取五个合法比较槽T_i，可重复，记每客户j=Σ_i t_i。

同一原σ给真实分支(A,E,T_i,R_i^AE,S_i^AE)及(A,T_i,H_i,I_i,J_i)。再暴露第二位在真实(A)后改为实际第四位的合法D，原续局为(A,D,R,S,T)。只有这条分支是新对象；新R/S/T不等同任何旧索引主题。

对每客户旧会员a,b,c,d,e及各hist位，定义
\[
 K_{AE}=\sum_i\frac{r_i}{a+e+t_i+r_i+s_i},\quad C_{AE}=\sum_i\frac1{a+e+t_i+2},
\]
\[
 K_H=\sum_i\frac{h_i}{a+t_i+h_i+i_i+j_i},\quad
 K_I=\sum_i\frac{i_i}{a+t_i+h_i+i_i+j_i},
\]
\[
 C_H=\sum_i\frac1{a+t_i+3},\qquad C_I=\sum_i\frac1{a+t_i+h_i+2}.
\]
分子0项取0。新会员r,s,t用在以下新分支总负载a+d+r+s+t。七条客户系数依次为
\[
 \frac b{a+b+c+d+e}-\frac d{a+d+r+s+t},
\]
\[
 \frac t{a+d+r+s+t}-\frac e{a+d+r+s+1},\qquad
 \frac{5t}{a+d+r+s+t}-\frac j{a+d+r+s+1},
\]
\[
 K_{AE}-rC_{AE},\quad K_{AE}-sC_{AE},\quad
 K_H-tC_H,\quad K_I-tC_I.\tag{1}
\]
每一条**客户总和**均非负。首条是真第二位偏离比较；次两条是新真实末位对E及五T的BR；其余是原AE第四位和原(A,T_i)第三/四位对新合法R/S/T的安全分母比较。分母只上界未来覆盖者，不冻结未来行动；也不要求被强制D自己最优。

# 任意非负共同权的投影

取固定整行非负权(α,β,γ,δ,ε,ζ,η)，无需和1。对可见旧客户状态z，设
\[
\begin{aligned}
 M(z)={}&\alpha\frac b{a+b+c+d+e}+(\delta+\epsilon)K_{AE}+\zeta K_H+\eta K_I\\
 &+\max_{r,s,t\in\{0,1\}}\left\{
 \frac{-\alpha d+(\beta+5\gamma)t}{a+d+r+s+t}
 -\frac{\beta e+\gamma j}{a+d+r+s+1}\\
 &\hspace{42mm}-(\delta r+\epsilon s)C_{AE}-t(\zeta C_H+\eta C_I)
 \right\}.
\end{aligned}\tag{2}
\]
零分子即使分母0也取0；任何真非零项分母正。则对每份原完整五人SPE
\[
 \boxed{\sum_x M(z_x)\ge0.}\tag{3}
\]
证明：真实新分支给每客户一个特定(r_x,s_x,t_x)，将七个总slack按同一非负权相加≥0，正是未取max前的客户和；逐客户max只将它增大。局部max未必可由一张完整策略同时实现，扩大域仍保持必要性。不能用min替代max，也不能每客户自由选一套权却只借原七个全局slack。

旧AE_hist和second_hist及共同j已足够算全部K/C量，不需要隐藏的跨族配对。δ=ε时max只依k=r+s∈{0,1,2}及t∈{0,1}，可由八态缩成六态；未要求新R/S覆盖集相同。非对称权一般仍须八态。

# 旧点分离是本族的一组实例

冻结权分子按一百万分母为(819936,80557,2110,26105,26105,15852,29336)。它们与同目录separate JSON的约分形式一致，非负，和1.000001；非归一不影响(3)。代旧64正有理原子点得到
\[
 \sum_z m_zM(z)=
 -\frac{336525906357864252494704662357779526105596687}
 {24837228663957176671172182423497877773536000000}<0.
\]
此固定点的64×8精确计算、64 maxima、独立七式重构及一次真实运行已在[C2独立审查#d7-fixed-primal](../审查/交叉回复税与第二步D分支的独立七行排除--审查.md#d7-fixed-primal)完整保存。本批两separate主源与C2比较原件逐SHA相同，复用那次完整阅读/认证，0重新运行或重授独审。

由(3)的全称必要性，这个旧点不能保持原数据延拓成真第二位→D分支。它并未给“增加本行后整个松弛”的最优值，更不是完整SPE反例。separate发现器使用NumPy/SciPy先找λ；最终负号用有理数与全部八态承担，不靠LP数值最优。其ROOT/SOURCE/THIRD/SECOND/sh实际导入third_D_completion，本批已将该依赖完整读入，不能把单个separate.py叫独立运行包。

# 与浮点补全及当前主问题的联系

[固定点补全](../计算/第三位与第二位复制D的固定点补全--计算.md)先有133行第三位→D双尾数值可行，再有283行联合第二位→D正最小最大违量；本七行是后一诊断的活动行精简，正确固定点非延拓由本精确证书承担。后续[564/908全型列生成](../程序/第二位D分支的列生成与完整主题定价--程序.md)在扩大旧类型域重新搜质量，不能把旧64点被排的结论授给所有新列。

5808B源正文的一般任意非负权包络、八/六态和原子max方向已自足保存；源说“root已请求审查”是旧时状态，C2 primary真实独审接受的范围另按其记录。当前五人half已另证，六人主目标未因此闭合。阶段三可登记“七真IC联合推出包络”“固定λ特例/精确分离”“数值活动行来源”，不将程序导入等同逻辑依赖或宣称外审/新颖性。
''')
(W/'object-index.json').write_text(json.dumps(objects,ensure_ascii=False,indent=2)+'\n')

add('计算','第三位与第二位复制D的固定点补全','customer-attraction/third-and-second-position-D-copy-fixed-point-completion','fixed-source-numerical-necessary-extensions; exact-D7-reused; no-new-LP','旧64原子保质量，第三位D双尾133行1024分型的float最小最大违量负；再加第二位D三尾283行8192分型为正，两LP均optimal，固定非延拓由既有精确七行证书承担。',['third_D_completion.py','third_D_completion.json','two_D_completion.py','two_D_completion.json','second_D_envelope.md'],r'''
# 固定旧点、不同真实位置与变量

原模型是有限单位客户、共同有限非空目录、五位单位提供者、全部有序历史纯SPE，空主题/重复/零客户/平局保留。实际(A,B,C,D,E)；旧三个固定路径actual=ABCDE、second=AEUVW、third=ABEXY，另有AB/AE三元和second四元查询直方图、三个末回复菜单。输入是旧437必要行的64正有理原子点，SHA18e074ba51357dfa03090fe9b97b8ff868b9c83b2687c7da7ff6f7b39489abe1，未有完整策略。

两个新分支分别是第三位在(A,B)后强制实际D得到(A,B,D,P,Q)，和第二位在(A)后强制D得到(A,D,R,S,T)。P/Q是前者的两个真后继，R/S/T是后者的三个真后继，不能因为目录字母相同就互认后继或政策。

第三位补全还保L_i=σ₅(A,B,D,T_i)的末回复菜单。单客户新位p=1_P、q=1_Q；ℓ=Σ1_(L_i)、h=Σt_i1_(L_i)，共同查询重数j=Σt_i。精确域是0≤h≤j、0≤ℓ−h≤5−j；对仿射目标四个角(0,0),(j,j),(5−j,0),(5,j)足够。当前64旧原子全j1，所以每个有4个不同角。

# 第三位D的133条必要行

7410B third_D_completion.py全文读。它保持每旧原子总质量m_α，把该质量分到(p,q,ℓ,h)局部类型。64×4位组合×4角=1024个非负分型质量，另有一个自由ε变量。报告variable_count1024不含ε，实际LP有1025变量。

记b₀=a+b+d，新尾总负载b₀+p+q，u_P=p/(b₀+p+q)、u_Q=q/(b₀+p+q)，零分子份额0。133行分为以下完整族：

|族|行数|真实含义|
|---|---:|---|
|旧actual/secondE/thirdE真角色查P/Q|20|三个旧路径中10个真正决策角色，各查两个新合法主题；被强制E不借最优性|
|F3D|1|旧第三位C的实际利润不小于强制D后同一原σ收益d/(b₀+p+q)|
|新P/Q查十个固定旧主题及彼此|22|P的安全分母b₀+2；Q在其真末节点用b₀+p+1|
|新P/Q查五比较槽|2|每current利润乘5，减j/其查询分母|
|新双尾tax对十比较索引对|1|10H−j(5−j)/(b₀+1)−j(j−1)/(b₀+2)，H=u_P+u_Q+p/[(b₀+1)(b₀+2)]|
|新P/Q与三个旧末回复菜单互查|12|旧菜单精确总比较及新角色安全分母|
|旧AB/AE第四、第五位查新P/Q|8|同一真实索引节点的当前利润与查询分母|
|新P/Q查AB/AE两回复菜单|8|每族五个合法回复主题的求和|
|旧second索引第三/四/五位查P/Q|6|保三个不同真实节点的过去负载/剩余人数|
|新P/Q查second的H/I/J菜单|6|合法共同目录五主题和|
|新D末回复菜单及其全部相互比较|47|五基础菜单行、10固定/2新主题、10旧角色、6旧菜单双向、4AB/AE节点、4AB/AE菜单、3second节点、3second菜单|

第一部分86行与末项47行合为133。例：Dmenu:S=5u_P−j/(b₀+1)+h/[(b₀+1)(b₀+2)]；Dmenu:V=(jℓ−5h)/同税分母；Dmenu:Z=5u_Q−ℓ/(b₀+p+1)。这些客户系数需按原子质量全局求和后非负，不能当每客户SPE。

固定质量的LP形式为
\[
 \min\varepsilon,\quad x\ge0,\quad
 \sum_{v\text{属}\alpha}x_v=m_\alpha,\quad
 G_rx\ge-\varepsilon\ \text{每个必要行 }r.\tag{1}
\]
ε自由；大正ε总可放松全部行，所以这是最小最大违量问题。对同一精确矩阵，ε*≤0等价于所选必要行可同时非负，ε*<0表示可严格满足；它仍不构造完整SPE。

10826B冻结报告status为HiGHS Optimal，row_count133、variable_count1024、maximum_violation=−0.001440312856564927。它保存全部14个活动行名和83个正split（每条atom/P/Q/ell/h/mass），本批全部消费：64旧原子均有分配，局部角均合法，保存float质量对旧有理m的最大归并误差3.608224830031759e−16。这个小误差只核账簿，没有认证133行精确可行；源没有输出有理恢复或完整动作表。本批0该LP重跑。

# 再加第二位D后的283行

5679B two_D_completion.py全文读。它保留前述(p,q,ℓ,h)，另加r,s,t∈{0,1}，得到64×2⁵×4=8192分型质量，加ε共8193变量。源码允许--source覆盖输入，优先用exact_mass否则旧mass_numerator/denominator；当前报告来源路径是原历史scratch位置，不是本次去读取的另一个工作区。

新行包括F2D；新三尾R/S/T在自己真实节点对旧十主题、P/Q、彼此、五比较/旧新菜单的安全比较；旧角色和所有索引角色对R/S/T的查询；旧菜单与新D菜单的双向比较；及三尾利润定理给的两行。与旧133行合并后恰283个字典行。

三人利润行用[任意合法背景三人5/3定理](../定理/固定背景三人利润界--定理.md)。在真前缀(A,D)后，R/S/T总利润V₃，而任何合法三主题比较的剩余利润≤5V₃/3：一条比较(B,P,Q)，另一条对十个五索引三元组求和，客户右侧为Σ_(k=1)^3 binom(j,k)binom(5−j,3−k)·k/(a+d+k)，左侧(50/3)V₃。它比较同背景下可达利润最大值，不认不同前缀的策略。

550B报告同样是HiGHS Optimal，row_count283、variable_count8192，但最小最大违量为+0.013551301796009453。其七活动行是F2D、D2:5:K:E、D2:5:sumopt、AE:4:R、AE:4:S、secondindexed:3:T、secondindexed:4:T。

这表述为“求解器成功求出正最小最大违量”：若是精确值，会说明ε=0的所选必要系统无解；不能写成求解器返回infeasible。550B本身是浮点证据。该固定点不可延拓的精确结论来自这七行的有理非负权/逐原子max证书，已在[C2独审](../审查/交叉回复税与第二步D分支的独立七行排除--审查.md#d7-fixed-primal)完成并由[一般投影包络](../引理/第二位复制实际D的七行投影包络--引理.md)说明，本批0重跑。

# 状态、比较与接续

旧点早有[根饱和不相容](../障碍/五人索引松弛点的根饱和不相容--障碍.md)和[去对角菜单](../引理/真实菜单去对角比较与五人索引点分离--引理.md)排除，第三位133必要行尚能数值补全没有矛盾。任何更小必要系统的可行点都不自动具备共同目录全策略资格。

本页全部两份源码/两份报告字段、83分配和活动行均保原字节。0原优化器/补全求解，未把数值负/正两次身份改写成精确SPE或新外审。阶段三可登记133到283必要行扩张、七活动行发现来源、精确D7联合排除与新全型列生成的范围差；当前五人half已有别证，六人目标未由此解决。完整证据见[本批入口](../../tools/evidence/branch-geometry-source-resumed-boss3/README.md)。
''')

rd=json.loads((B/'saved-field-review.json').read_text());cg=rd['column_generation'];b=cg['cg_second_D.json'];f=cg['cg_second_D_full.json']
history='|it|加列后总数|新增|float β|最小定价余量（×120）|缓存context|原秒数|\n|---:|---:|---:|---:|---:|---:|---:|\n'+''.join(f"|{x['iteration']}|{x['columns']}|{x['new_columns']}|{x['beta']:.16g}|{x['pricing_minimum_scaled']:.16g}|{x['contexts']}|{x['seconds']:.12g}|\n" for x in f['full_iteration_records'])
dual='|新908行|保存float λ|\n|---|---:|\n'+''.join(f"|{n}|{v:.17g}|\n" for n,v in f['new_row_positive_duals'].items())
body=r'''
# 同一旧557行上加七行或351行

这里研究[五人完整历史模型](../定义/共同目录完整历史模型--定义.md)的必要条件客户类型松弛，不输出完整策略。原子包括十位ABCDEUVWXY、AB/AE各8格及second 16格直方图、三个末回复菜单(ℓ,h)，另加真正second→D分支(A,D,R,S,T)的三个会员位D2_bits=(r,s,t)。三族直方图总数均5且共同t=1重数j；菜单满足0≤h≤j、0≤ℓ−h≤5−j。空主题/重复/零客户与全部离轨平局不删。

6919B price_second_D.py继承外部R-c473/round4_pricing/full_pricing.py的Universe(overlap=1)，给旧557行追加[七个真D2行](../引理/第二位复制实际D的七行投影包络--引理.md)，共564。6367B price_second_D_full.py再用4198B second_D_rows.py的351行替代那七行，共908。全部原码全文读，基类15042B也全文读；旧557解析前提/精确上下界复用[成熟定价合同](五人保交叠全型与常锚点跨族定价的精确恢复合同--程序.md)，本批没有重审旧437/557矩阵。

564与908冻结JSON的前557个行名逐个完全相同，其前437又与canonical旧primal.rows完全相同；不是只因都写557就假定同版。旧557由437+10末位去对角+110同族强PAIR组成，overlap1保一份重叠。新D2_bits只是旧类型的扩展，旧行不依赖它，因此已有旧557精确上界可以在更强系统中继承；要认定564或908的新精确最优，仍需同域匹配有理primal与全域dual。

# 351行的全部族与三人利润接口

second_D_rows先以P=Q=ℓ=h=0调用two_D_completion.extras作代码复用，然后**删除**第三位D、Dmenu、P/Q查询及(B,P,Q)比较相关行；这不是数学假设那些主题为空。留下以下131行，加220条固定三主题行：

|族|行数|含义|
|---|---:|---|
|F2D|1|实际第二位对强制D真实三尾的精确IC|
|新R/S/T真角色安全查询|69|每角色23：十旧固定+另两新主题、sumopt、三旧menu、AB/AE/second共七菜单|
|旧actual/secondE/thirdE真角色查R/S/T|30|actual五角色、E强制后第三至五、第三E强制后第四/五各查三新主题|
|三个旧末回复菜单查R/S/T|9|已有精确末节点查询求和|
|旧AB/AE第四、第五位查R/S/T|12|同一真实索引背景与未来人数|
|旧second索引第三/四/五位查R/S/T|9|各自过去负载保留|
|真三尾对十个最优三索引组合|1|(50/3)V₃与完整查询重数式|
|十个旧固定标签的允许重复三元组|220|每组三主题在背景a+d的剩余利润≤(5/3)V₃|

共1+69+30+9+12+9+1+220=351。固定三元数是binom(12,3)=220，允许重复行动，未把主题数十误当比较人数。三人定理只用于(A,D)后的真三尾，强制D自己不借枝内最优性；它控制的是剩余利润，不是把非零背景总覆盖搬来。

# 分解与完整类型定价为何可做

原基类读canonical indexed审计的定义前缀，精确/向量版各exec一次，不运行其成熟审计main；导入partition_pair_closure/offdiagonal_closure。它准备所有792个三元及15504个四元直方图，按共同j分组，局部特征M均以120倍表示。

对固定十位、D2_bits和j，新351行的任意加权和由decomposition返回：六个j的常数、AB/AE/Sbranch三个族各自的局部特征系数、三个旧menu的ℓ/h系数。常数和menu系数是raw单位；局部M是120倍raw，count特征在full price中特别乘120，常数/menu也乘120后相加，不能混尺度。函数涵盖F2D、新真角色对固定/菜单查询、旧真角色/末菜单查新主题、索引角色查新主题以及两类三人利润行；不是忽略跨族项，而是这些特定行在固定新位后恰好分族可加。

price先在各共同j下分别最大化完整直方图分数，再把menu仿射目标在四角(0,0),(j,j),(5−j,0),(5,j)最大化。外层1024十位×8新会员×6j=49152个条件；contexts126/181等是缓存键数量，不是检查过的客户数、游戏数或完整域的大小。不同客户的局部最大者可不共同实现σ，扩域只用于必要系统和对偶分离。

有限列LP为max O、W=1、Gx≥0、x≥0。对float β/λ，定价目标是120(βw−o)减加权必要行的完整隐藏域最大值。所有正负客户系数须保；actual未覆盖w0的原子不能删。非负λ且全域余量**精确**≥0才给O≤βW；float停止本身不够。

# 阈值、保存时点与输入精确绑定

程序预处理把系数乘120、断言距最近整数<1e−7再转int64；稀疏加权行仅取|λ|>1e−11，负候选须尺度余量<−1e−7；main每轮请求100列。只有返回候选才以原直接行值对照，容差1e−5。保存dual字典只写λ>1e−10，故不是完整原向量，不能从缺键推断该求解器分量精确0。

两程序从canonical旧64原子与可选exact_optimum_primal_overlap1.json的67原子五结构字段取并，忽略后者exact_mass作为LP质量。旧/新共有六个基础结构，去重得125结构；每个配八D2_bits得1000列，再加全十位1、j0/j5两锚，初始1002列。以上顺序与字段逐个绑定到564的全部1002原子，同时与908的前1002原子完全相同；不是按数量猜了另一个61原子717点。

每轮先解当前列LP，再定价新增，日志columns/atoms是加列后，β及out.x是加列前，新质量补0。主循环新增去重数count0即停；一般还可能因候选已存在而停，未assert完整有理域非负。默认maxiter35/25分别为564/908；原实际argv/软件环境未保，不能把默认次数当实跑次数。

# 564份完整冻结记录

731110B cg_second_D.json全字段消费：564行名、1002完整原子、1002质量含932个明确0及70正、全部51稀疏dual、单轮history。1000列j1，另j0/j5各一；全部70正项j1，其中19项actual未覆盖。W_float=1.0000000000000013，O=β=2.042155490337933。

唯一轮it0记录columns1002/new0、pricing min −4.5308867768767414e−11、contexts126、seconds1.5102148056030273。七个D2行在保存的稀疏dual中均无正条目；这不自动证明精确λ都0或该增强系统精确值等于旧557值。缺失的是新系统匹配有理primal/全域认证，而非小数看起来一致即可。

# 908份完整冻结记录

1358160B cg_second_D_full.json全字段消费：908行名、1862完整原子和1862质量含1788零/74正、全部60稀疏dual、11轮history。全列j1有1858、j0有3、j5有1；全部74正项j1，其中21项actual未覆盖。W_float=.999999999999999，O=β=2.0386744431163377。全部原质量的小数/float.hex、零坐标索引、原子域及dual名/值在[完整字段记录](../../tools/evidence/branch-geometry-source-resumed-boss3/saved-field-review.json)和原JSON保全，没有只读beta。

{HISTORY}

新增总数860，初始1002到1862；末轮没有新增，最小float余量仍是−7.626255182913155e−11，没有把它改写为精确0。精确有限列LP随列扩张目标不降，末两轮微小回落是浮点记录，不作为精确最优值序列。

保存的新D2full正dual十四项如下；其余46条属于共同旧557行，原字典与完整行名全部保。

{DUAL}

这里“完整主题定价”指声明的全直方图必要类型域，而非枚举所有完整SPE；输出>2也不反五人half。原报告没有908有理原始/对偶恢复或新独立全域证明，本批没有补造。

# 来源、运行与后续关系

本批原LP、price、补全求解和seven/peer旧审计均0新运行；唯一原入口为前缀迁移12个Fraction折点诊断。七原始代码全部实读，五JSON全域字段/所有原子和每个零/正坐标处理，七依赖冻结SHA核同；基类全文读，旧557辅助实现沿成熟对象复用，不重授其认证。完整来源见[证据](../../tools/evidence/branch-geometry-source-resumed-boss3/README.md)。

[一般七行包络](../引理/第二位复制实际D的七行投影包络--引理.md)给真实节点必要性及固定权精确排旧点；[局部补全](../计算/第三位与第二位复制D的固定点补全--计算.md)说明发现来源；这里在全型域重新分配质量，两种点不能互换。现行五人half由别证成立，六人目标未解决。阶段三应分开登记行族联合定义系统、实现、旧上界继承、float发现和精确缺口，不把导入图当逻辑图，也不宣称新颖性/外审/锐性。
'''.replace('{HISTORY}',history).replace('{DUAL}',dual)
add('程序','第二位D分支的列生成与完整主题定价','customer-attraction/second-D-column-generation-and-full-histogram-pricing','complete-source-and-all-saved-fields; 564-and-908-floating-only; no-new-optimizer','564/908共享557行及精确1002列种子，完整保1002/1862原子、70/74正质量、51/60稀疏dual和1/11轨迹；351新行/全域分解与浮点认证缺口明确。',['price_second_D.py','price_second_D_full.py','second_D_rows.py','cg_second_D.json','cg_second_D_full.json'],body)

(W/'object-index.json').write_text(json.dumps(objects,ensure_ascii=False,indent=2)+'\n')
