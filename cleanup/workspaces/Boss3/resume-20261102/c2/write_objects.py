from pathlib import Path
import json
R=Path('/workspace/scratch/cd4305a146e6/co-work-anl-boss3');W=R/'cleanup/workspaces/Boss3/resume-20261102/c2';S=R/'archives/customer-attraction/state';B=R/'archives/customer-attraction/tools/evidence/direct-coverage-source-resumed-boss3';PFX='research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/';C='68fad804ec5946cb296f77dc5b336308a66abf12';objects={}
def add(cat,title,id,status,summary,src,body):
 rel=cat+'/'+title+'--'+cat+'.md';kind={'引理':'lemma','计算':'computation','审查':'review','程序':'program'}[cat]
 fm='---\n'+f'id: {id}\nkind: {kind}\ntype_tag: {cat}\ntitle: {title}\nstatus: {status}\nsummary: {summary}\nsource_refs:\n'+''.join('  - '+json.dumps('source:'+C+':'+PFX+x,ensure_ascii=False)+'\n' for x in src)+'---\n\n'
 (S/rel).parent.mkdir(parents=True,exist_ok=True);(S/rel).write_text(fm+body.strip()+'\n');objects[rel]={'id':id,'sources':src}

add('引理','真实第三位交叉查询的可信末回复门槛','customer-attraction/real-third-move-cross-query-credible-last-response-floor','proved-necessary-cross-query-IC-and-relay; ROW3-unresolved-by-these-sources','固定完整五人SPE在AB后强制五查询，保复制S_j后的真实末回复、BR最小门槛及旧人收益改变量；指定松弛点失败不证明一般ROW3。',['direct_coverage/credible_cross_query_reply.md','direct_coverage/README.md'],r'''
# 固定策略、真实位置与ROW3合同

采用[共同目录完整历史单位模型](../定义/共同目录完整历史模型--定义.md)：有限单位客户、有限非空共同目录、恰五位单位提供者依次观察全部有序历史各选一主题；客户在最终覆盖者间均分。空主题、重复、零客户及各历史任意平局保留。固定一份完整纯SPE σ，实际叶(A,B,C,D,E)、利润u₁…u₅和W=Σu_k。取达到OPT₅的五个合法比较槽T₀…T₄，允许重复。

在实际有序前缀h=(A,B)，客户旧负载b_x=1_A(x)+1_B(x)。第三位强制T_i后沿同一σ的真正后继为R_i、S_i。定义
\[
 U_b(X;Y,Z)=\sum_{x\in X}\frac1{b_x+1_Y(x)+1_Z(x)+1},\qquad
 d_i=U_b(T_i;R_i,S_i),\quad ROW3=\sum_{i=0}^4d_i.
\]
被强制的T_i不借枝内最优性，只由原实际节点IC给d_i≤u₃。源辅助候选为
\[
 ROW3\ge OPT_5-W.\tag{ROW3}
\]
若它成立且实际第三位是全体最低收益者之一，则ROW3≤5u₃≤W，故OPT₅≤2W。这只处理最低收益出现在第三位的情形，第一、二位还需别的论证；源说第四、五位对应行另有结果，本批未借未读原源新授认证。

当前[五人half](../定理/五人半覆盖--定理.md)已有普遍精确证书，旧稿五人主目标OPEN是历史。本页保这些来源尚未证明的ROW3接口，没有从half反向推出它，也没有机械搬到六人。零客户时所有求和0，不需除W。

# 非根分支的旧玩家利润不能删

实际旧两人最终利润和记B₀，实际末两人和V₀，第三位利润u=u₃；T_i真实枝对应B_i、V_i、d_i，Γ_i=u−d_i≥0。逐枝效率相减给
\[
 \boxed{W_i-W=(V_i-V_0)+(B_i-B_0)-\Gamma_i.}\tag{1}
\]
B_i−B₀无固定符号，在非根历史不可免费删掉。只有没有过去玩家的真根才令两项旧人利润均0。三/四人利润定理的下界也不会给V_i−V₀上界，互斥分支的尾利润不自动支付实际W。

# 复制S_j后的真实末回复

为区别[交叉回复税](../审查/交叉回复税与第二步D分支的独立七行排除--审查.md)中复制R_j的回复，记
\[
 K^S_{ij}=\sigma_5(h,T_i,S_j).
\]
这是第i查询枝第四位改合法S_j后的真正末回复。完整SPE给
\[
 U_b(R_i;T_i,S_i)\ge U_b(S_j;T_i,K^S_{ij}),\tag{2}
\]
\[
 U_b(K^S_{ij};T_i,S_j)\ge U_b(Q;T_i,S_j)
 \quad\text{每个合法 }Q.\tag{3}
\]
前者用真实第四位最优性，后者用真实末位BR。不能把(h,T_i,S_j)换成(h,T_j,R_j)，也不能任挑K而不核(3)。同主题使有序历史重合时，同一σ强制同回复；原平局始终保留。

置F_i(X)=Σ_(x∈X)1/(b_x+1+1_(T_i)(x))。逐客户：同时命中两个主题者对差贡献0，只命中一者不受另一槽影响，故
\[
 U_b(S_j;T_i,K)-U_b(K;T_i,S_j)=F_i(S_j)-F_i(K).
\tag{4}
\]
合(2)—(4)得对每合法Q
\[
 U_b(R_i;T_i,S_i)\ge U_b(Q;T_i,S_j)
                 +F_i(S_j)-F_i(K^S_{ij}).\tag{5}
\]
这个最后势差未被证明有共同索引平均符号，因此不是闭合ROW3。

令BR(b+1_(T_i),S_j)为旧背景加T_i及第四位S_j之后，末位在整个共同目录的最佳回复集合；有限非空目录使其非空。原K^S属于它，因而
\[
 \boxed{U_b(R_i;T_i,S_i)\ge
 \max_j\min_{K\in BR(b+1_{T_i},S_j)}U_b(S_j;T_i,K).}\tag{6}
\]
任意K都给单次收益≥Σ_(x∈S_j)1/(b_x+1_(T_i)(x)+2)，所以(6)可严格强于仅用人数上界的安全分母。各min只丢平局信息，未声称这些独立最坏回复可同时组成另一份σ。

# 精确诊断与复用边界

[十八主题物化计算](../计算/十八主题物化目录的三人可信性诊断--计算.md)把旧77行必要松弛的冻结11轨道支持编为185正整数兴趣型。每个T_i后拟R_i,S_i中的第四位只得4632856876；改S_j（j≠i）后，唯一末位BR R_j让偏离者得7718643666，严格多3085786790。原程序逐五个循环邻居j=i+1检查，输入对五索引完全置换对称，故全部j≠i的结论由对称性推出；没有虚报源码显式枚举20对。

这是三人剩余子局的可信性诊断。拟CDE及拟查询尾均不可信；两个空行动不能免费前置为最优者。旧19,008类型/77行坏必要点仍只限制该松弛，精确物化不声称舍入保住所有原行。

1059B入口与5600B数学稿全部读，并比较当前五人证明、[前缀旧接口](../资源/五人前缀信用接口与内部独审的历史范围--资源.md)和[六索引第三位直方图投影](真实第三位六索引菜单的完整直方图投影--引理.md)。它们的后继数/索引数不同，不自动相推。阶段三可登记真实IC必要条件、固定坏点反驳及旧人信用/势差缺口，不能据同名ROW重复造结论。完整来源与版本见[证据](../../tools/evidence/direct-coverage-source-resumed-boss3/README.md)；无外审、新颖性或一般ROW3认证。
''')

fd=json.loads((B/'saved-field-review.json').read_text());table='|轨道|c,d,e|h（000…111）|总整数质量|排列数|每型重数|\n|---:|---|---|---:|---:|---:|\n'
for i,x in enumerate(fd['frozen_orbits']):
 b,c,d,e,h=x['state'];table+=f"|{i}|{c},{d},{e}|"+','.join(map(str,h))+f"|{x['integer_orbit_weight']}|{x['distinct_permutations']}|{x['per_type_integer']}|\n"
body=r'''
# 十一轨道完整定义合法整数目录

这是恰三位单位提供者的有限诊断，目录18标签依次(C,D,E,T₀…T₄,R₀…R₄,S₀…S₄)，全部有序历史、重复和平局保留。旧负载b=0，不是已有完整五人根SPE。

每客户的固定会员位(c,d,e)及五个三元(t_i,r_i,s_i)的八格直方图h总数5，按下表给定。每行将h展开五词，枚举全部**不同排列**，每个排列均分该行总质量；相同mask相加。下表与规则已经完整定义输入。

{TABLE}

scale=120·10⁸=12000000000。frozen JSON另保十进制weight，但实际精确代码消费integer_orbit_weight。轨道质量均被排列数整除；共185不同正整数兴趣型、32164464720不同单位客户，最小型重数9345216、最大2771341224。重数是可逐名展开的客户，不是加权提供者。

mask中C/D/E占位0/1/2，T_i占3+i，R_i占8+i，S_i占13+i。30049B [完整catalog](../../tools/evidence/direct-coverage-source-resumed-boss3/original/research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/direct_coverage/materialized_row3_catalog.json)保全部185个topics/multiplicity。

# 精确全集递推及完整有序策略

3966B原exact_materialized_relaxation.py调用规范ExactSPESolver。每个前缀counts k的a孩子有全部可实现终局R(k+e_a)，门槛M(k)=max_a min_(z∈R(k+e_a))U_a(z)，保留各孩子中当前收益≥M(k)的终局。按count缓存的是**全集**；证书在每个有序孩子可独立挑续局，不强制同count统一动作。有限树必要/充分拼接证明亦见[人口全集递推](../反例/四主题二十二客户的人数福利下降--反例.md)。

精确根终局计数有20个。原程序为选中的一个终局展开完整策略，再调用不调用outcome solver的certificate.verify_certificate，核动作域完整、真实后继、声明计数和全部343=1+18+18²个有序决策历史、5831=343·17真改动作。27968B完整证书实际路径(S₁,R₁,R₀)。报告只保存20这个数量而未另导20向量列表，本批不虚构缺少的输出载体。

本次隔离树原样运行一次，四规范依赖模块与冻结inventory SHA一致；新catalog、完整策略、2392B报告全部逐字节同原，exit0/stderr0。全部源码/输入/环境/命令及SHA见[证据](../../tools/evidence/direct-coverage-source-resumed-boss3/README.md)。这是同实现重放；求解器与定义级验证器分模块，不等于另一位盲审或第二套全集实现。

# 拟CDE与拟查询尾的严格不可信

拟实际(C,D,E)覆盖12000000120、C利润2791921400，而精确根门槛6866184736，所以不在根SPE终局全集。每个T_i孩子拟(T_i,R_i,S_i)也不在该孩子SPE全集：R_i利润4632856876，child floor7718643666。

当第四位改S_j、j≠i，历史(T_i,S_j)的唯一末位BR为R_j，偏离者得7718643666，严格增益3085786790。冻结报告直接核每i的j=(i+1) mod5；输入轨道对五索引同时置换不变，任一不同有序对均可映到已核对，所以全部j≠i由对称性推出。这里复制S_j的K^S和[税引理](../审查/交叉回复税与第二步D分支的独立七行排除--审查.md)复制R_j的K^R不同。

# 真查询行的最小余额

五个T_i的比较并集O覆盖全部32164464720客户。它有五槽，不能作三人合法终局，也不直接命名OPT₃。每个强制根T_i后的当前最小可信收益均5348363202。

对每个20根终局z及每个可作其首行动的a，算法将各别枝取当前最小可信收益；若在轨a恰为某T_i，该项必须用z的实际首位收益替代该枝最小值。不同根孩子可独立拼SPE；此实例五T_i不同，没有重复查询历史相容性的漏项。得到
\[
 \min_{z,a}(ROW+W(z)-O)=13125108894>0,
 \qquad\text{除scale为 }2187518149/2000000000.
\]
原报告不打印最小者a或全(z,a)表，不能把默认证书根行动说成唯一最优索引；此结论由精确枚举合同承担。完整证书给其中一个真实SPE，未称唯一均衡。

# 浮点210型与精确185型是不同版本

2068B float报告保存210型、10根终局、target W1、O2.691249065506198、relaxed row1.1827582216869792、O−row1.5084908438192186、root floor0.530217850854412；五查询min约0.4479402593020312；拟尾R利润约0.44268998141840094、child floor约0.609635731649257；best true row slack1.139105783567194。

3104B float materializer读取可变n5/parent/row3_relaxation.json，使用浮点orbit质量和1e−10容差，不读当前frozen_row3_source_support.json。冻结精确支持明确从整数catalog恢复、保在父方后来编辑前。210/10与185/20不能称仅round误差，也不能把float数乘scale冒同一输入。该float父输入本批未取作运行依赖，0该入口新运行；完整旧报告仍保其所有字段。

# 结论、关系及接续

失败的是指定必要松弛坏点的拟CDE与拟回复实现；这里没有证明一般ROW3或构造五人half反例。若前置两个空行动，非空目录客户下根改非空T至少得|T|/5>0而空行动得0，所以不能直接得到五人SPE。

[旧64原子根饱和](../障碍/五人索引松弛点的根饱和不相容--障碍.md)与[真实去对角分离](../引理/真实菜单去对角比较与五人索引点分离--引理.md)排的是另一个437点，不是本185型输入；负差值、客户表和证书不可混用。与[真实S复制门槛](../引理/真实第三位交叉查询的可信末回复门槛--引理.md)是有限实现/反驳关系。原件与完整字段保全，未赋外审、新颖性、最小性或一般福利常数。
'''.replace('{TABLE}',table)
add('计算','十八主题物化目录的三人可信性诊断','customer-attraction/eighteen-topic-materialized-three-player-credibility-diagnostic','exact-finite-enumeration-and-separate-certificate-replay; proposed-motif-not-credible','冻结11轨道生成185正整数类型；三人20根终局与343有序节点完整证书重放，拟CDE及查询尾严格失败；浮点210型报告按不同输入版本保。',['direct_coverage/credible_cross_query_reply.md','direct_coverage/frozen_row3_source_support.json','direct_coverage/exact_materialized_relaxation.py','direct_coverage/exact_materialized_audit.json','direct_coverage/materialized_row3_catalog.json','direct_coverage/materialized_row3_true_spe.json','direct_coverage/materialize_row3_relaxation.py','direct_coverage/materialized_relaxation_audit.json'],body)
(W/'object-index.json').write_text(json.dumps(objects,ensure_ascii=False,indent=2)+'\n')

add('审查','交叉回复税与第二步D分支的独立七行排除','customer-attraction/crossed-reply-tax-and-second-to-D-seven-row-review','general-tax-identity-accepted; fixed-old-primal-D7-extension-excluded; once-original-audit','保独审的64符号会员恒等式与512新分型精确包络；一般税和固定D7互不推导，后续去对角/锚定公式另注明推导与审查时态。',['direct_coverage/peer_relations_independent_review.md','direct_coverage/audit_peer_relations.py','direct_coverage/peer_relations_independent_audit.json','fresh_proof/crossed_reply_tax.md','branch_geometry/separate_second_D.py','branch_geometry/separate_second_D.json'],r'''
# 两项独立审查对象与证据时态

3908B原peer review全文实读，3715B audit全文实读；父方又按冻结源导出7491B crossed_reply_tax.md、2831B separate_second_D.py、2030B其JSON作比较依赖，未额外认领/done。两项对象分别用下列#crossed-reply-tax与#d7-fixed-primal定位，不把一般税引理与一个旧点的延拓排除接成互相推导。

原审者先读同行数学/七式，再从模型重构，无优化器/同行代数helper导入；不是未读稿盲审，也非外审。本次只原样执行其标准库审计一次，输出494B同原字节，exit0/stderr0。它是同一独立实现的重放，不增加一位独审者；完整原件、八依赖、命令/环境/SHA见[证据](../../tools/evidence/direct-coverage-source-resumed-boss3/README.md)。

## crossed-reply-tax

固定原模型的一份完整历史纯SPE、任意恰剩三人的有序历史h，旧负载b_x为非负整数。任取q≥1个合法查询T_i，允许重复；其真正后继为R_i,S_i，d_i=U_b(T_i;R_i,S_i)。定义
\[
 V_b(X;Y,Z)=\sum_{x\in X}\frac1{b_x+1+1_Y+1_Z},\quad
 F_i(X)=\sum_{x\in X}\frac1{b_x+1+1_{T_i}},
\]
\[
 g_i(X,Y)=\sum_{x\in X\cap Y}\frac1{(b_x+1+1_{T_i})(b_x+2+1_{T_i})},
 \quad\tau_i=g_i(R_i,R_i)-g_i(S_i,R_i)\ge0.
\]
τ_i是在R_i\S_i上的和，且F_i(X)−g_i(X,Y)=V_b(X;T_i,Y)。空主题、零客户和所有平局均保。

本税证明复制的是R_j，故记K^R_(ij)=σ_last(h,T_i,R_j)，区别[直接可信诊断](../引理/真实第三位交叉查询的可信末回复门槛--引理.md)复制S_j的K^S。三条真IC slack为
\[
 L^1_{ij}=V_b(R_i;T_i,S_i)-V_b(R_j;T_i,K^R_{ij}),
\]
\[
 L^2_{ij}=V_b(K^R_{ij};T_i,R_j)-V_b(S_j;T_i,R_j),quad
 L^3_{ij}=V_b(S_i;T_i,R_i)-V_b(K^R_{ij};T_i,R_i),
\]
全部非负，分别是真第四位改R_j、真末位K^R对S_j、原末位S_i对合法K^R。共同目录使这些主题在各精确有序节点合法，未把旧人收益搬枝。

令两主题增量调和势Φ_b(X,Y)=Σ_x Σ_(k=1)^(1_X+1_Y)1/(b_x+k)。逐客户精确恒等式为
\[
 d_i-V_b(T_i;R_j,S_j)=L^1_{ij}+L^2_{ij}
 +F_i(S_i)-F_i(K^R_{ij})+\Phi_b(R_j,S_j)-\Phi_b(R_i,S_i),\tag{1}
\]
\[
 F_i(S_i)-F_i(K^R_{ij})=L^3_{ij}+g_i(S_i,R_i)-g_i(K^R_{ij},R_i).\tag{2}
\]
i,j独立同分布时两Φ项平均抵消。加E_iτ_i后，剩余为
\[
 \Delta+E_i\tau_i=E_{ij}(L^1+L^2+L^3)
 +E_{ij}[g_i(R_i,R_i)-g_i(K^R_{ij},R_i)]\ge0,\tag{3}
\]
其中Δ=E_i d_i−E_(ij)V_b(T_i;R_j,S_j)。最后余项是在R_i\K^R上的非负和。uniform给
\[
 \sum_i d_i-\frac1q\sum_{ij}V_b(T_i;R_j,S_j)+\sum_i\tau_i\ge0.\tag{4}
\]
原独审认可这条带税去相关及同一概率律的加权版本；未认可无税Δ≥0或ROW3。

代码对(t_i,r_i,s_i,r_j,s_j,k)六会员位的64组合，把所有表达写成1/(b+1)、1/(b+2)、1/(b+3)的有理系数，并用1/[(b+k)(b+k+1)]=1/(b+k)−1/(b+k+1)。每个系数都精确为零，因此恒等式涵盖全部符号背景b，不是有限b抽样。IC的合法性仍靠前面的真实节点说明，64个代数零式本身不使任意伪收益表成为SPE。

### 后续同行稿的去对角与锚定补充

所取得的比较稿还含后补式，原494B独审报告未逐项另列它们；本页重构以下短推导，不把旧审查范围倒写。

相同精确历史给K^R_(ii)=S_i，所有L和查询差/Φ差在i=j均0。删这些对角，再平均，得uniform税可减为
\[
 \sum_i d_i-\frac1q\sum_{ij}V_b(T_i;R_j,S_j)
 +\frac{q-1}{q}\sum_i\tau_i\ge0.\tag{5}
\]
任意概率ρ_i同理将税换为Σ_iρ_i(1−ρ_i)τ_i。q1时两边0；重复查询造成更多历史重合也不破坏此充分式。系数是已展示的改进，不主张普遍最小税。

五查询单客户(t_i,r_i,s_i)、j_T=Σt_i的行系数是
\[
 \sum_i\frac{t_i}{b+1+r_i+s_i}
 -\frac{j_T}{5}\sum_i\frac1{b+1+r_i+s_i}
 +\frac45\sum_i\frac{r_i(1-s_i)}{(b+t_i+1)(b+t_i+2)}.
\]
全局求客户和非负；各单客户系数不必非负。实际第三位背景b∈{0,1,2}时可按三元联合直方图表示，但没有抹去有序历史。

若同一前缀的原实际三尾为C,D,E、u=V_b(C;D,E)，令τ_C在D\E上以b+1_C为背景定义。将(5)的q2应用于(T_i,C)，乘2后得
\[
 d_i+u-V_b(T_i;D,E)-V_b(C;R_i,S_i)+\tau_i+\tau_C\ge0.
\]
对五i求和，τ_C出现5次。锚定须同一前缀和同一σ的真实C枝；隐藏回复是σ_last(h,T_i,D)和σ_last(h,C,R_i)，不是冻结D/E。该式仍需共同实际资金支付，不能把多份互斥尾利润直接认作W。

## d7-fixed-primal

另一个输入是旧437行索引点five_player_indexed_bound.json，77420B、SHA 18e074ba51357dfa03090fe9b97b8ff868b9c83b2687c7da7ff6f7b39489abe1。它有64正有理原子，十位ABCDEUVWXY；AE_hist为五个(t,r,s)三元直方图，second_hist为五个(t,h,i,j)四元直方图。三族的查询重数都相同；独审逐原子核此一致性。本批只消费该旧JSON的primal质量/会员与相关直方图，不重新审437行、对偶或别的字段资格。

实际第二位由B改为实际第四位合法D，真实新路径为(A,D,R,S,T)。新主题会员用ρ,σ,τ；旧实际总负载M=a+b+c+d+e，新总z=a+d+ρ+σ+τ。零分子份额统一0。定义旧AE与second族的已知量
\[
 A_4=\sum_i\frac{r_i}{a+e+t_i+r_i+s_i},\quad
 C_{AE}=\sum_i\frac1{a+e+t_i+2},
\]
\[
 H_3=\sum_i\frac{h_i}{a+t_i+h_i+i_i+j_i},\quad
 H_4=\sum_i\frac{i_i}{a+t_i+h_i+i_i+j_i},
\]
\[
 C_3=\sum_i\frac1{a+t_i+3},\quad C_4=\sum_i\frac1{a+t_i+h_i+2},\quad j_T=\sum_i t_i.
\]
七条逐客户行依次为
\[
 b/M-d/z,\quad \tau/z-e/(a+d+\rho+\sigma+1),\quad
 5\tau/z-j_T/(a+d+\rho+\sigma+1),
\]
\[
 A_4-\rho C_{AE},\quad A_4-\sigma C_{AE},\quad
 H_3-\tau C_3,\quad H_4-\tau C_4.\tag{6}
\]
全局客户和都非负。第一条是真第二位IC；二/三条是新真实末位对E及五最优槽的完整BR；四/五条是原AE第四位分别查新R/S的安全分母；六/七条是原(A,T_i,...)第三/四位查新T。安全分母只上界未来覆盖者，未冻结后继。

冻结非负乘子为

|行|λ|
|---|---:|
|F2D|25623/31250|
|last:E|80557/1000000|
|last:sumopt|211/100000|
|AE4:R|5221/200000|
|AE4:S|5221/200000|
|second3:T|3963/250000|
|second4:T|3667/125000|

这些是发现器float dual四舍五入后的有理提案，和1000001/1000000；非延拓证书只需各λ≥0，不需归一化或最优。对每旧原子α，令m_α为其正质量，枚举(ρ,σ,τ)∈{0,1}³并设γ_α=max Σ_kλ_k row_k。原独审从单位会员重新写七式、不导同行seven helper或优化器，全部64×8=512型精确求值，64个γ都等于冻结列表，且
\[
 \sum_\alpha m_\alpha\gamma_\alpha
 =-\frac{336525906357864252494704662357779526105596687}
 {24837228663957176671172182423497877773536000000}<0.\tag{7}
\]
任一真实延拓只能把每个旧原子质量拆到这八型，其七行非负加权和必≥0，却≤(7)，矛盾。忽略主题碰撞和历史重合只扩大八型域，仍负就足以排真实延拓。结论只否定保此旧点数据的second→D延拓；不是增强系统全域上界、精确minimax最优、五人或六人SPE反例。

同行发现器的numeric minimax0.013551301796009557与有理(7)约−0.013549253457823079分别是发现值和可核证书，不能按正负相反便称精确相等。本次未调用其NumPy/SciPy优化器，也未取其third_D_completion依赖；七式及旧输入在独审源码中已自含。

# 与现行结果和后续工作的关系

[根饱和不相容](../障碍/五人索引松弛点的根饱和不相容--障碍.md)和[去对角菜单](../引理/真实菜单去对角比较与五人索引点分离--引理.md)早已用别的合法条件排同64点；D7保独有的新分支/新主题消元证书，不重复认领旧点或旧437认证。一般税与D7可各自复用，均没有解决ROW3；当前五人主定理已有另证，当前焦点六人仍需相应真历史与共同预算。阶段三应分别给税恒等式、实现/独审、固定点非延拓与范围比较关系，不能把三条同输入分离互造依赖。没有外审、新颖性或全松弛锐性声明。
''')

add('程序','第三位查询固定策略锥的有限探针','customer-attraction/third-query-fixed-count-policy-cone-finite-probes','complete-source-and-saved-field-review; float-LP-discovery-and-one-exact-finite-record; no-universal-ROW3','三份count策略LP各330状态的输入/目标/保存点完整保，0.8加强式与ROW3分开；真全集探针只保14型119客户的有限正余额，未输出全策略。',['direct_coverage/probe_allbig_cone.py','direct_coverage/probe_row3_strong_cone.py','direct_coverage/probe_row_cone.py','direct_coverage/probe_true_row.py','direct_coverage/row3_allbig_cone.json','direct_coverage/row3_strong_cone_best.json','direct_coverage/row_cone_best.json','direct_coverage/true_row_probe_best.json'],r'''
# 三份固定count策略锥LP的共同合同

原probe_row_cone.py 2391B、probe_row3_strong_cone.py 2402B、probe_allbig_cone.py 1993B均全文读。固定K7/N5，变量为127个非空兴趣类型的非负质量。给一张种子质量w，以按count缓存的确定性逆向归纳生成完整count策略：每状态先真实完成各动作的孩子，再比当前角色终局收益；随机版本在1e−7浮点平局中用rng选择，allbig版本取第一个。

全部深度0…4共有330=Σ_d binom(d+6,6)个count态。每态保存规定动作与真实终局，对其他六动作加入终局收益差≥0，共1980条（含可能重复/零行）必要IC，固定actual coverage=1，在同一策略锥内重新优化质量。count策略在所有2801=Σ_(d=0)^4 7^d有序历史上按其counts展开；这是完整策略的真子类，不是一般历史净化。

在实际前两行动prefix之后，强制第三位每个比较a，再沿该固定策略求真实终局。普通目标是
\[
 score=W-O_J+\sum_{a\in J}d_a,
\]
strong版本将W系数改为4/5，allbig用普通目标。J是在**种子**w下选出的五主题最大并集；质量重优后一般不保证J仍为新OPT₅。代码只用float linprog，无Fraction primal/dual恢复或全域证书；有限未见负score不能证明ROW3。

随机两版本seed510257，默认最多100次；每第八次或失败后取16%稀疏、1…14整数质量的新种子，否则用LP点加每型不足.005噪声；score<−1e−7提前停。saved JSON只保最好score/path/opt/policy/actual_counts/weights，没有实际迭代总数/argv/求解器版本/成功日志，不把默认100当已执行数。脚本有main guard，但会覆盖同名best输出。本批0原LP/import NumPy/SciPy。

# 全部三个保存点及330态字段

三份策略各330个(q,a)记录已逐条消费：恰全部合法count决策态，无缺/重，动作0…6合法，跟随所得path/actual_counts与原字段一致。它们未另存2801行有序展开；正文明确该展开规则，不虚构独立全历史审计。

|原JSON|实际path|唯一/全部保存质量|比较J|保存score|
|---|---|---|---|---:|
|row3_allbig_cone|00000|mask1质量1|0,1,2,3,4|0.2|
|row3_strong_cone_best|46666|mask112质量1|0,1,2,3,4|5.551115123125783e−17|
|row_cone_best|60000|下列十型float质量|0,1,2,3,4|0.3117283950617284|

第一份种子原是主题0五客户、主题1…4各一私有客户，但LP保存点只有对0感兴趣的一名客户；其全部330规定动作0。强版本保存点唯一客户兴趣{4,5,6}，全部动作只4或6（分别52与278态）。这两输入的每个规定行动都覆盖客户：任意过去历史下未来按表均覆盖，遵从者最终得正份额，改不兴趣主题只0，改另兴趣主题仍相同负载。因此两份简单点可直接解析确认完整SPE，不需新优化或逐1980 IC重审。

两点均W=O_J=1、查询行1/5。普通score=1/5；strong的4/5−1+1/5精确为0，原5.55e−17只是float残差，不能写严格正加强余额。这也没有反ROW3。

第三份的全部十型质量为

|mask|保存float质量|mask|保存float质量|
|---:|---:|---:|---:|
|4|0.1440329218106996|9|0.18518518518518517|
|33|0.14814814814814817|36|0.02263374485596708|
|65|0.08230452674897122|68|0.030864197530864196|
|80|0.024691358024691357|97|0.4732510288065844|
|100|0.024691358024691357|114|0.0308641975308642|

其330动作中0有316、6有13、2有1。按保存的十进制数和策略计算W≈1、O_J≈7/6、row≈0.478395061728395，score与原float相符。没有把这些十进制数的有理解释自动授为精确IC可行点，也没有补一份未交付dual。全部原政策与质量保在证据。

# 真终局全集探针的14型整数记录

2238B probe_true_row.py也全文读。它固定n5/k7、整数尺度60，60整除1…5，按真实兴趣重数算整数收益、集合值R(counts)与每动作最小可信收益。每输入枚举21个五标签比较求真OPT，保所有最优J；只检查按W排序的前30个根SPE终局，再枚举可实现前三步到第三位的状态。相同count只保一个代表有序prefix；匿名收益/全集相同，但这不是完整σ集合或任意历史依赖策略枚举。种子510251、默认200个随机输入；保存iteration91不是本次新扫描。

797B true_row_probe_best.json的完整输入14个正整数类型：

|mask|人数|mask|人数|
|---:|---:|---:|---:|
|2|16|4|15|
|5|9|10|13|
|31|11|36|12|
|42|15|77|3|
|89|5|90|6|
|96|6|99|2|
|100|3|103|3|

共119单位客户，J={0,1,2,4,6}覆盖全部，故OPT₅=119直接由总客户上界与该J取等。保存W108、终局counts=(0,3,2,0,0,0,0)、prefix(2,2)、第三位action1。root_payoffs60七坐标为(568,1208,1428,902,252,826,376)，真正占用标签只有1/2，实际每位1玩家1208/60、每位2玩家1428/60，总3·1208/60+2·1428/60=108。程序对未占用标签也算了形式坐标，它们不是实际玩家利润，不解释为七个玩家。

第三位各query最小可信收益的60倍为(748,1208,1008,1172,552,1036,976)。在轨action1已经等于其minima，故对应J的row60=748+1208+1008+552+976=4492；gap60=(119−108)60=660；score60=3832，除60为958/15>0。原程序用完整集合值可实现性筛选此prefix与终局，但没有导出一张五人全动作证书，本次也未新运行该探针来另授一份完整σ。

保存点只是一次有限正余额；前30终局筛选、有限随机输入和每输入最优J不能支持一般ROW3。零负例或大正余额不付款其他输入的真实跨枝损失。

# 与成熟对象、版本和执行范围

已全文比较[历史/计数严格分离](../反例/完整历史与计数统一策略的严格分离--反例.md)：不能由count锥提升到全历史。与[十八主题精确物化](../计算/十八主题物化目录的三人可信性诊断--计算.md)的区别是：后者用全部终局集合和完整有序证书诊断一份拟尾，此处三LP固定子类且仅float发现，第四探针是另一份五人整数输入。

本批只实际运行exact_materialized_relaxation与audit_peer_relations各一次；0本四probe/LP/随机扫描。全部330×3政策、weights、path/count/score与真行记录全部字段由[保存数据阅读](../../tools/evidence/direct-coverage-source-resumed-boss3/saved-field-review.json)消费，旧原件不覆盖。当前五人主定理已另证，ROW3独立合同和六人目标不因此闭合。阶段三可登记实现、有限记录和真实量词限制，不授一般定理、外审、新颖性或最优界。
''')

(W/'object-index.json').write_text(json.dumps(objects,ensure_ascii=False,indent=2)+'\n')
