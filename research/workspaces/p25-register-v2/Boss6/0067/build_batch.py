import json, pathlib, hashlib, re
ROOT=pathlib.Path('.').resolve(); WORK=ROOT/'research/workspaces/p25-register-v2/Boss6/0067'
task=json.loads((ROOT/'research/operations/p25-register-v2/tasks/register-ab98f323ad-0067.json').read_text())
mats=task['definition']['materials']; texts={i+1:(ROOT/x['path']).read_text() for i,x in enumerate(mats)}
ids=json.loads((WORK/'allocated-identities.json').read_text())['object_ids']
model='有限不同单位客户、有限非空共同标签目录及任意覆盖映射、单位权顺序提供者；完整纯策略保全部有序历史、空覆盖、同覆盖异标签、重复行动、零客户和任意离轨弱平局。偏离后沿同一原策略的真实后继完成，客户价值在终局覆盖者间均分。辅助分数质量或非零背景另明示，不当作原单位游戏的SPE。'
def ref_path(p,section=None):
 p=str(p); d={'path':p,'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest()}
 if section:d['section']=section
 return d
def ref(i,section=None):return ref_path(mats[i-1]['path'],section)
def stable(i):return re.search(r'^id: ["\x27]?(.*?)["\x27]?$',texts[i],re.M).group(1)
def sources(i):
 return [mats[i-1]['path']]+re.findall(r'^\s*-\s*["\x27]?(source:[^\n"\x27]+|clean:[^\n"\x27]+)["\x27]?\s*$',texts[i],re.M)
objects=[]
def add(oid,i,title,kind,status,statement,quantifiers,assumptions,scope,objections,section=None,ev=(),external=()):
 e=[ref(j,s) if isinstance(j,int) else ref_path(j,s) for j,s in ev]
 e += [ref_path(p) for p in external]
 objects.append(dict(object_id=oid,version=1,title=title,kind=kind,truth_status=status,model=model,statement=statement,quantifiers=quantifiers,assumptions=assumptions,scope=scope,objections=objections,body=ref(i,section),evidence=e,sources=sources(i)))
add(stable(3),3,'真实最优前缀hybrid的利润重置精确账','identity','proved',
'固定同一完整σ和合法比较元组T，z_i为强制前i个T后沿σ完成的叶。令Δ_i,j=u_j(z_i)−u_j(z_(i−1))，γ_i=u_i(z_(i−1))−u_i(z_i)≥0，则W(z_m)−W(z_0)=Σ_iΣ_(j≠i)Δ_i,j−Σ_iγ_i；同一旧角色后来重置只望远镜成u_j(z_m)−u_j(z_j)，不是原根利润。',
'任意人数m≥1、每份完整σ、任意合法比较元组及其真实前缀链。',
['全部叶沿同一σ，不将互斥孩子利润相加当实际容量。'],
'精确恒等式及付款缺口；不主张slack非负或δ≤u。',
'52客户反例已否定普遍R_r(P)≤D+V；本页复用该反例而不重立身份。完整推导在两项同名子标题，full body同时保递推和hybrid两条账。')
add(ids[0],3,'根完整菜单平均安全值的W/m付款义务','conjecture','open',
'对同一完整纯SPE，根强制A后真实完整m槽叶Z(A)，K(T,A)=Σ_(x∈T)1/(1+c_x(Z(A)))，M_root=min_Q max_T E_Q K(T,A)。待证每个实例及每份σ均有M_root≤W(σ)/m；若成立，静态共同目录比较给OPT_m≤2mM_root≤2W。',
'所有有限原输入、m≥1及每份完整σ，存在根行动分布Q同时对全部合法T付款。',[],
'完整m槽背景再插入查询；不是删当前m−1槽、逐人M_root≤u1或child-min ROW。',
'成熟正文未证、亦未给直接反例；逐人强桥被否定不判本平均义务真伪。',section='根菜单平均候选与直接 ROW')
add(ids[1],4,'两不交主题使动态根保底不能乘人数支付福利','counterexample','proved',
'两人共同目录A、B不交且大小3、2；完整SPE唯一，两真实末位孩子均选另一主题，根选A，收益(3,2)、W=OPT2=5。动态α2=max_A min_(完整可信孩子)u_root=3，故W=5<2α2=6，否定普遍W≥mα_m。',
'存在所列五单位客户、两标签完整两人游戏；每个孩子BR唯一，因而α2无平局歧义。',[],
'动态首利均摊辅助桥；不反静态安全值聚合或half。',
'全文“两个被放弃的强桥”第二项给全部两层比较；第一项71客户遗漏反例归其现有owner。',section='两个被放弃的强桥')
add(ids[2],4,'36客户原倒数SPE在任意正常数切线价下发生真实盈利偏离','counterexample','proved',
'36客户三人六主题X/Y实例中各主题大小21，同组交9、跨组交13。原完整σ根X0、第二位跨组、末位在第二主题组取最小未用标签。在X0节点，第二位原Y0→Y1成本22，改X1→X2成本18。常数τ>0下u_i^tan=2τ|A_i|−τ²(|A_i|+Σ_(j≠i)|A_i∩A_j|)，故此真实偏离改善4τ²>0，原倒数利润两路均12。',
'同一个已证完整原σ，所有常数τ>0均非该切线二次游戏的SPE。',
['偏离后使用改变历史上的原σ回复X2，而不冻结Y1。'],
'原SPE到切线SPE的迁移障碍；不反只对切线SPE的passivity。',
'外部路由论文仅范围导航，不承担此解析反例。常数τ未宣称为候选鞍点价格。',section='旧36客户原SPE的正切线偏离',external=['archives/customer-attraction/state/反例/三人聚合末位保底--反例.md'])
add(stable(5),5,'固定actual路径的可信全菜单MILP与有理incumbent后核合同','algorithm','proved',
'固定可实现actual有序路径a，离轨(i,A)仅选可信终局z且u_i(z)≤u_i(a)，actual列固定a。以p∈Δ、每位置ψ_i及每离轨候选onehot y构造bigM约束ψ_i≤K(a)·p、ψ_i≤K(z)·p+B(1−y)，最大化Σψ−W，精确形式等于固定路径全部兼容完整菜单及查询的最坏值。任合法有理p及每离轨一个原候选z均能拼为同一完整SPE菜单，Fraction重算各min给该提案真实gap。',
'每个有限实例和固定可实现actual路径；数学有限优化全域，源码浮点incumbent只给逐提案值。',
['每离轨孩子是真子SPE且被当前actual收益cap筛选；首次离轨子树互不相交。','B非负且覆盖全部合法K列和ψ；p须显式非负、归一。'],
'完整m槽背景后额外插入查询；不适用删槽AFC。',
'原代码不要求res.success，浮点Optimal不是精确最优证书。两原36客户提案可解析拼完整43节点，gap−27/2、−473/48；48只为访问路径数，不是48个精确上界。',ev=[(6,None)])
add(stable(7),7,'E/F/R/H集合逆推精确最大化全部历史SPE的删槽菜单亏损','algorithm','proved',
'固定实例、查询p，E(q)=∪_a{z∈E(q+e_a):U_a(z)≥F(q)}，F(q)=max_a min_(z∈E(q+e_a))U_a(z)。固定B∈E(0)及actual动作a，离轨A仅取L={z∈E(q+e_A):U_A(z)≤U_a(B)}，actual列保B；对各离轨分别最大化G_p(z−e_A)，再全A取min得R_p。实际顺序DP H(q)=max_a[R_p(q,a,B)+H(q+e_a)]给max_σ gap(σ,p)=max_(B∈E(0))[H(0)−W(B)]。保argmax可展开完整有序策略；删除全关联客户保持gap严格不变。',
'所有有限单位输入、m≥1、固定任意合法p；最大化覆盖全部完整有序历史纯SPE，不限计数策略。',
['只缓存可实现终局集合，同计数不同历史可选不同叶。','真正首次离轨子树互不相交；actual孩子不得自由改叶。'],
'删当前位置后m−1槽；纯查询由IC直接付款，混合查询一般最大gap≤0仍未证。',
'源码整数IC/Fraction查询可实现数学合同；默认float best和materialize浮点矩阵不自成精确证书。七固定p小例为实现有限检查，不证明AFC。',ev=[(8,None)])
add(stable(10),10,'具名gc及单行regret的固定完整策略浮点分离合同','finite-search','finite',
'十个具名完整策略输入按实际覆盖q归一q·w=1，w≥0并保全部真实有序IC。gc程序以g_T=q_T/[1+(n−1)loads_T/n]最小化(g−c_target,a)·w，冻结最佳为四人四标签fractional_actual_load_failure、85动作、根counts[1,3,0,0]、a0、全关联型权1及浮点目标0。regret版本另最小化(q+c_target,incumbent−F_a)·w，两目标与S?不同。',
'所列十份形式策略及程序规模跳过条件内的有限枚举；不量化所有策略/质量，不宣称各目标精确最优。',
['输入动作表决定全部有序真实后继；p由最大动作推断、n由最大历史长度推断。'],
'有限浮点桥攻击与冻结零松弛记录；无精确对偶或half结论。',
'本页“regret报告/依赖缺失”只保原时点。旧工作路由已指当前另有85动作regret_best报告slack1/17和floor_scan冻结；本worker未实读该另源，不将原缺档说成当前不存在，也不把其报告升为精确证据。')
add(ids[3],12,'枚举支持并以全目录最廉价主题补槽精确求最优fresh费用','algorithm','proved',
'任合法实际m槽计数c，g(a)=Σ_(x∈a)1/(1+c_x)，g_min=min_a g(a)。枚举S⊆目录、|S|≤m，先最大化cov(S)，再最小化Σ_(a∈S)g(a)+(m−|S|)g_min，得到真正恰m槽覆盖最优元组的最小fresh费用K0。任元组重复槽各费≥g_min；反向最优支持不足m时加任何主题不能提高已最优覆盖，故用全目录最廉价主题补槽保持最优并取等。',
'所有有限非空目录、m≥1和非负整数实际计数总和m，包括空主题、零客户、最优支持少于m。',[],
'静态恰m槽优化算法，不需要该计数来自SPE。',
'16冻结根、2767多重集仅作实现证据，不证明S?。候选S?的精确有限阴性证据仍须其主owner接本页；本记录只负责ENUM算法。',section='计价对象与重复槽')
add(stable(14),14,'四个指定五人根松弛的精确最优点及其固定成员SPE不可补全','finite-model-theorem','proved',
'δ=5u−|T|=1截面上，Middle-False31行与Middle-True52行精确最大F_T(Q)−u=113/21；Copy100代数行、删28未闭合复制PAIR后的72合法行及Three-tail165行均精确最大16/3。正文完整有理点分别满足全部行且匹配113/21或COPY九合同上界；九位点忘D/E逐坐标等于七位Copy点。四点B2/B3均大小5u但有向差各1，故F_B2(B3)=u+4/5违反δ_B2=0根刚性，不能保持这些成员和u补成完整SPE。',
'上述明确五个有限系统与四个完整给定有理点；不可补全量化保持给定成员质量和u的一切原模型扩展。',
['100行中的28复制枝强PAIR只为代数定义，不假定其原CAG必要性。','113/21与16/3上界来自成熟全成员合同；不是浮点对偶状态。'],
'有限LP精确取等及指定点的原模型排除；不证真实SPE斜率最优或所有最优点不可实现。',
'原float恢复点未冒逐位等于未保存完整double向量；348行核为历史新事件，本次只复用成熟证明。',ev=[(16,None),(15,None)],external=['archives/customer-attraction/state/引理/五人共同大小根刚性加强--引理.md','archives/customer-attraction/state/引理/任意人数近饱和根主题刚性--引理.md'])
add(stable(15),15,'五人保真实复制末回复的44/3、13/5、16/3根刚性','lemma','proved',
'恰五人，u为实际根利润，K为全目录最大主题大小。任合法T,Q有F_T(Q)=|Q\\T|+|Q∩T|/5≤44u/3+13K/5−16|T|/3≤u+(16/3)(5u−|T|)。根强制T真实叶P=(T,B2,B3,B4,B5)，原倒二改B5后保真实末回复C；根IC、四cap、真倒二IC、原末比Q/C和复制末比Q九合同及128会员域完整非负证书给证明。覆盖聚合得OPT5≤220u/3+13K−388|T|/15，T最大给15OPT5+193K≤1100u。',
'每个五人有限原输入、每份完整σ、每个合法T,Q，包括空、相同和别名。',
['自然K≤5u；换共同上界M只保第一式，推出缺口式须另有M≤5u。','复制枝第四位被强制，不将其当优化者；九合同不使用任何PAIR。'],
'普遍必要根不等式；弱支配旧113/21与11/2行，但未宣称真实SPE斜率锐性或独立支付half。',
'完整两路径/九合同/恒等式/48值表均在body；17页提供128型原程序证据。历史独审实际仅到113/21，不补造COPY独审。',ev=[(17,None)])
add(ids[4],16,'第四位被强制复制后额外28条强PAIR的必要性义务','open-lemma','open',
'五人同一完整σ根强制T叶P=(T,B2,B3,B4,B5)，再在(T,B2,B3)强制第四位B5、末位真回复C。问在背景p=T+B2+B3上，是否对七合法命名主题的每个含重复无序对(X,Y)，H_p(B5,C)≥Σ_x[(1_X+1_Y)/(p_x+1)−1_X1_Y/((p_x+1)(p_x+2))]，其中H为两尾总收益加B5自重叠税。',
'所有上述五人完整σ与各28比较对的普遍必要性；不是某个有限点满足行。',
['复制枝只有C已知是末位BR，B5是被强制的首尾行动。'],
'probe_copy_reply100行系统中超过72已合法行的28条；原SPE必要性未闭合。',
'标准强PAIR使用第一尾IC，本枝不能直接取得。本页未给替代证明，亦未给反例；该open不损害已证COPY九合同或100行代数最优。',section='三、probe_copy_reply：129变量及28条未闭合额外行')
add(stable(20),20,'真实复制行库的有理系数验收与强制者守卫','method','proved',
'在根强制最大T及末主题复制枝的扩大会员域，CAP/COPY/真优化者FLOOR/真末两人PAIR/LAST行写为h_j−e_j o。若精确B≥0、λ≥0、Σe_jλ_j=1且ρ=Bv_T+C1_T−Σλ_jh_j≥0逐型成立，则对任意n合法比较并集O有O≤Br+CK。n≥3、c≤n−3时表内真末两人合法；c=n−2须删除最后强制倒二枝PAIR:c或验其权0，FLOOR亦只在最后强制之后。',
'所有有限原输入、同一完整σ、自然最大K及所列合法n/c和精确证书；不是任意冻结发现器浮点输出。',
['负C必须使用确切全目录最大K。','有理证书逐型非负与行的真实IC语义分别验收。'],
'指数会员系数方法；n6c4为16位65536型、254原列，守卫后253列。',
'原发现器不带强制PAIR守卫且逐项限分母不保归一/非负。小8704系数和两n4LP为有限实现证据，不担n6全域结论。',ev=[(23,None)])
add(ids[5],22,'覆盖列归一加统一CAP修复的向外有理恢复','algorithm','proved',
'对固定复制行几何，先将已保存乘子乘10^8取整a_j，令S=Σ_(PAIR/LAST)a_j>0并最终λ=a/S。统一整数系数尺度L下记A(ω)=Σa_j g_j(ω)。T外列若A>0，给全部非T CAP同加c=max ceil(A/[LΣ_(h>0)1_h])，使T外A≤0；全零型A0。再于T内取B=max(0,max[(A/S−CL)/v])，v=L v_T>0。于是全部会员型非负余项且覆盖列精确消去；另验B>0及真行守卫后给有效O≤Br+CK。',
'每个有限所列几何、合法有理C与非负整数初始权，S>0且行名/守卫合法时；只保证所构有限可行证书。',
['必须在修复后的A上重算B。','非法强制PAIR不能由整数核验补足数学语义。'],
'有理向外恢复方法，非最优性、最小修复或任意输入成功承诺。',
'四恢复线已归既有M-0b83e29b0a3d49fa9cae81f84f9e82ec，本记录仅保存可复用恢复机制。原四逐项有理化λ均S<1且o0有负余项，是方法必要性证据，不否其原B/C存在其它表示。',ev=[(23,None)])
add(stable(24),24,'4064扩大列域的41行八轨道分离及共同容器不可能','obstruction','proved',
'六人七极大、仅约束末位会员等于B0的4064列域，body八正有理轨道质量归一，全部6M/7L/28普通税T平均非负，而E[W−U/2]=−2027846/107130789，故该域上不存在共同非负乘子逐列支付。其正支持含(I,J)=({1},{4})与({2},{4})，迫实际倒二主题同时含不同全局私有块而无共同极大容器；故见证不能实现为任何此七极大目录的六行动组合。',
'所列4064列扩大域上所有固定非负41行乘子；不可实现涵盖任一共同容器路由。',
['只有末位等价固定，前五会员未附路由包含约束。'],
'精确系数锥不足，非固定真实路由域分离、完整SPE或half反例。',
'固定六集{1,…,6}目标亦负−12442/3967807，但不越共同容器矛盾；旧五路由17列及83行18列是不同对象。')
add(stable(25),25,'000010弱41行只分离全并集目标且被强混合行排除','obstruction','proved',
'固定容器路由000010的1631合法列上，body17正有理权使源41行平均非负并E[W−U/2]=−148577/8996100，排除该弱行全并集非负乘子证书。源共享倒二floor是1/12而成熟强包络是1/11；真正OPT6=U−min_j X_j，本权最小X0，E[W−OPT6/2]=7387/5997400>0。恢复强M4后平均−127428/41232125，故该合法目录/行动关联不能成为完整SPE。',
'该确定路由、弱41行和全并集目标的全部非负乘子；另对固定17权作精确强度/目标判断。',
['弱共享倒二1/12不可冒强1/11；末位B0标号与最小私有块省略分开。'],
'有效弱模板分离及精确纠错；不排除正确OPT6或强mixed行证书。',
'同尺寸另一000010/17列的固定六集分离用较强M4和不同权，不能合并。其余真实D/强PAIR也排除此权，不证明更强系统已足half。')
add(stable(26),26,'000010粗路由83行十八列分离与真实负载排除','obstruction','proved',
'固定000010、目标W−(U−X6)/2，18正有理列归一并使6M/7L/28普通T/42D_route全部平均非负，目标−42280/9125787，故不能在合法列域由该83行非负组合逐列证明目标。D_route分母为容器过去P_I(t)+6−t；真实过去Q_J(t)≤P_I(t)。同见证的精确真实负载行D_actual_(1,0)平均−799778/958207635<0，已不能实现为完整SPE或分离更强真实J负载系统。',
'所列路由、比较并集与83行全体非负固定乘子；排除结论只对所给18列形式质量。',
['M代码对核心用较弱β而非1/6；本支持无核心，不改平均。','普通税T不能换成多扣交叠的强PAIR仍沿用见证。'],
'粗容器计数模板的精确Farkas不足；非全部真实IC/half障碍。',
'本见证X6=0故该固定比较也最优；只有18支持无需枚全域。所有83平均与真D差额有完整正文证明，原包装main历史事件不计本次新运行。')
add(stable(28),28,'18客户完整SPE否定删除私有利润后的共享保底行','counterexample','proved',
'六人七极大主题：0有12私有单位客户；其余六主题为六环相邻两共享客户。每个有序历史恒选0，当前遵循收益12/(a+6−t)≥2，偏离任一环题收益≤2，故完整纯SPE。actual0^6、W12、OPT6=18。共享V6、所有共享actual份额0，原选择性行M_t=−6B_t<0（B=(1/21,2/37,1/16,2/27,1/11,7/72)），而正确总利润mixed行≥5/12。',
'存在所述18单位客户原实例及全历史恒0完整σ；六个被否共享行全部负。',[],
'否定从总利润保底消掉私有实际支付后只保共享的桥；不反原完整mixed、其它Q/T行或half。',
'见证确属原程序首组singles{0,6}、route00000、最小省略6；非利用未测域。本次无原LP/IC运行。',ev=[(27,None)])
add(stable(31),31,'双私有加K5关联的静态席位权重最优十九','obstruction','proved',
'十二单位客户、七极大主题为两个私有单例和K5五顶点各自关联的四条边客户。六人席位第六大ν=2/3，私有a0=a1=2。修正共享域权重LP为y0,y1≥2、yj+yk≥6(2≤j<k≤6)、y≥0，其精确最优19，由私有2+2、其余各3达到，十边约束各乘1/4及私有各1给匹配对偶。故不能满足静态因子二接口Σy≤12。',
'该固定真实目录的所列静态充分LP全部可行权；非所有付款方法。',[],
'修正私有/共享合同仍失败的精确方法实例。',
'OPT6=12；给两个私有权1、K5各半，分数覆盖成本9/2，已有真实六人定理反而保证每个完整SPE W≥6。未声称最差恰6。')
add(stable(32),32,'真实银行后继使均匀1/4逐客户Farkas证书失败','obstruction','proved',
'真实IC客户系数Γ_i,j,x=q_i,x/c_x−1_(x∈T_j)/(b_i,x+1_(x∈T_j)+f_i,j,x)，零分子项0。旧A=C两客户、B单例的两人完整SPE并无真实/冻结分母差，原算术漏了query指标。成熟四人十客户银行σ中，根改(2,1)使e2真实分母3而冻结1。选覆盖全部十客户的最优四槽((0,0),(1,1),(2,1),(3,2))，对e2目标t_x=−1，而全部λ_i,j=1/4的真实行和≥−5/6>−1，故不存在非负余项使t=Γ^Tλ+η。',
'存在所述已证原模型四人完整σ及一个覆盖最优元组，否定该固定均匀乘子的一切逐客户非负表示。',
['真实后继沿同一σ，不能无条件冻结actual suffix。'],
'指定均匀证书障碍及旧两人见证纠错；不排除其它非负乘子或全树Farkas。',
'银行完整控制器证据复用既有正文；本页只新增解析用途。若全部相关query真保持后缀负载，均匀λ仍可逐客户支付，范围保留。',external=['archives/customer-attraction/state/反例/逐客户条件与完整推送桥的反例层级--反例.md'])
add(ids[7],34,'381客户固定完整根菜单的精确矩阵值239604/3169','finite-game-value','proved',
'指定381单位客户、三人六主题、正文43动作完整策略，六个根forced真叶给6×6完整三槽后额外查询矩阵K。列Q=(1016,1273,0,0,0,880)/3169，行P=(1525,9362,0,0,0,4958)/15845，均为概率；max_a(KQ)_a=min_b(PK)_b=239604/3169，因此min_Q max_a(KQ)_a精确为该值，小于实际根137。纯列0 cap251/3亦小于137。',
'该唯一完整客户输入、固定全部43有序动作及其六列菜单上的所有概率混合。',
['完整m=3槽背景再插入查询，不是删根两尾。'],
'有限精确矩阵鞍点；不证明普遍FM或所有SPE菜单。',
'另查询D141/10<C6879/400只否强D≥C，不反此固定菜单付款；原缺381输入现补齐是来源增量，原审计本次未运行。',section='固定完整菜单的精确矩阵证书')
add(stable(39),39,'真正v3下全部真实水位池为零仍有正虚拟交换债','counterexample','proved',
'旧34单位三人完整σ的六根真叶两尾均高于真正v3=t=2411/246，故每个根分支VAR单位尾w1已KKT，J_a=H_a=Γ_a=0。actualZ0=(X0,Y0,Y1)，交换根到Y0并仅把旧X0尾降ρ99/100；X0负载谱12名2、11名3，t−g(ρ)=1342711/14637246>0，所以Gain和相对真实Y0孩子的Debt均≥1342711/1463724600>0。真实ΣH=0不能支付该正Debt。',
'存在所列固定单位完整SPE与真正同剩余人数静态安全阈值；所有六根真实池都为零。',
['虚拟交换保持同一Z0，真实Y0孩子另用Z_Y0和其基线/支撑。'],
'κ0域H独付虚拟交换Debt接口失败；非聚合、κ1、extra-one或half反例。',
'W32、OPT3=34、W−3v3=213/82仍正，可用高尾利润等其它资金未被排除。正文完整策略及真安全证书复用既有来源，本次未重跑258比较。')
add(ids[8],40,'单遍降权终点可需零权重入及正内点回调才能满足VAR','counterexample','proved',
'零权例b=(0,3,2)、根{x}、尾{x,z}/{x,y}、t16/15：先删S1再降S2至ρ正根8ρ²+17ρ−6=0，终点S1零权密度>t违反KKT；规范w=(1/2,0)恰全KKT。正内点例b_y=b_z=1、根{x}、尾{x,y}/{x,z}、t1：规范权均1/√2。单遍先处理者停q=(√5−1)/2，另一尾随后仍须下降，迫第一尾最终密度>t但权q<1，故需提高正权。',
'存在两份明确有限辅助VAR输入，分别否定只降一次和仅修复零权的通用求规范点方案。',
['VAR是全盒log势最大元；辅助密度不当作质量利润或原SPE。'],
'单遍信用算法仍可有效；被否的是把该终点等同规范VAR最大元。',
'零重入有独立90步区间及指定KKT实现证据；正内点回调为正文无理解析证明，未在14fixture中另计算。',section='单遍终点不是VAR终点：两份自足分离',ev=[(42,'100项log与90步零重入各有责任')])
add(stable(41),41,'同多重集低规范根严格交换与真实子树有符号重置债','lemma','proved',
'固定非负背景、t>0、r=n+1≥2份单位主题多重集Z，J(a;Z)为保根a的归一化VAR最大值。若规范根密度d_a*<t且有权1尾B，则交换标记保同负载/支撑/基线，稍降旧根严格增势，J(B;Z)>J(a;Z)。若原单位尾总利润V_a≥nt，则每个最大元至少有权1尾。同一完整σ的真孩子Z_a给Gain=J(B;Z_a)−J(a;Z_a)>0、Debt=J(B;Z_a)−J(B;Z_B)，准确J_B−J_a=Gain−Debt。若有限目录所有真孩子V_a≥nt且根全低t，选权1尾成闭有限图，循环上ΣDebt=ΣGain>0。',
'所有有限同叶辅助输入；真树结论对同一原σ，循环须全部动作或对所选出边封闭的子集。',
['真实Z_a/Z_B基线和支撑分别归一，不假设Debt非正。','孩子V_a≥nt是另需证明的假设，不从KKT或根IC自动得到。'],
'严格虚拟交换与精确债务定位；跨真实孩子共同付款仍open。',
'低规范根若先达≥t需付Γ；不能用有限图虚拟严格上升直接矛盾。已有零池例另排H独付，但不否其它高尾资金。',ev=[(39,None)])
add(stable(43),43,'真正v4下保高尾质量一的53客户水位无法保原孩子或原叶','counterexample','proved',
'53单位四人完整σ加任意整数c≥0全主题共同客户，真正v4=t0+c/4、t0=28481/2924，唯一低尾X0缺D647/8772，根P和两原高尾质量保1。任何满足低尾密度过线、同一全查询信用≤D和支撑的质量ρ必2/11<ρ<1。原P孩子根X0对X2的真实后继比较质量差2(ρ−1)/(ρ+2)<0；原(P,X0)第三人Y0对X1差3(ρ−1)/((ρ+1)(ρ+2))<0。两相关末位在该区间分别唯一BR Y1/X2，故重填其它末位也不能同时保原actual叶和第三人IC。',
'上述全共同核心整数c≥0族、所有满足窄水位合同的固定共同ρ，允许重填其余末位。',
['原高尾质量固定1；根P固定1；玩家质量在同一整棵孩子上不随未来行动追溯改变。'],
'固定高尾窄可信性接口反例；若放弃保高尾，统一缩尾另有正修复。',
'原6997报告scope过宽须按源码(1,ρ,1,1)解释；9522稿已有宽修复，不能把此record称全部共同质量不可能。本原入口仅c0/1/1000有限实现，任意c由解析抵消证明。',ev=[(44,None)])
add(ids[9],43,'三客户自由阈值的全部共同可行水位质量均破坏末位SPE','counterexample','proved',
'两人、不交A大小2和C大小1，原三节点全规定A是完整SPE。固定单位根A、自由阈值t4/3、唯一尾原u1且D1/3。规定A密度≥t与替根查询返还≤D共同迫唯一正质量w1/2，w0返还1>D。w1/2保信用/支撑/守恒，但末位规定A得2/3、改C得1，改善1/3；任0<w<1时规定减偏离=(w−1)/(1+w)<0。',
'存在所述三单位客户两标签原完整SPE；对全部共同可行质量失败。',
['t为自由阈值4/3，未称内生静态安全值。','同一尾质量固定用于其全部行动。'],
'自由阈值辅助可信性障碍，独立于真正v4的53客户固定高尾族。',
'水位代数与预算本身成立，失败在辅助加权孩子SPE；不反half或宽一般有条件统一缩尾。',section='三客户二人的自由阈值：全部共同可行质量均失败',ev=[(44,'原入口实际验证的有限义务')])
# Bind the necessary original implementations/certificates as immutable bytes.
extra_evidence={
 stable(5):[
 'archives/customer-attraction/tools/evidence/full-menu-milp-and-rational-proposals-primary/original/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/menu/menu_continuation_diagnostic.py',
 'archives/customer-attraction/tools/evidence/full-menu-milp-and-rational-proposals-primary/original/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round5/menu/aggregate_theta_diagnostic.jsonl'],
 stable(7):['archives/customer-attraction/tools/evidence/fresh-delete-slot-menu-primary/original/full_menu.py','archives/customer-attraction/tools/evidence/fresh-delete-slot-menu-primary/original/verify_oracle.py','archives/customer-attraction/tools/evidence/fresh-delete-slot-menu-primary/original/oracle_audit.jsonl'],
 stable(14):['archives/customer-attraction/tools/evidence/ra277-five-closure-primary/four-saved-points-exact-report.json'],
 stable(15):['archives/customer-attraction/tools/evidence/root-copy-reply-rigidity/original/audit_copy_reply_rigidity.json'],
 stable(20):['archives/customer-attraction/tools/evidence/fourcopy-fixed-capacity-discovery-audit/evidence/discovery_n6_c4.json','archives/customer-attraction/tools/evidence/fourcopy-fixed-capacity-discovery-audit/raw-discovery-exact-audit.json'],
 ids[5]:['archives/customer-attraction/tools/evidence/R-566-fourcopy-recovery/fourcopy_recover.py','archives/customer-attraction/tools/evidence/R-566-fourcopy-recovery/fourcopy_verify.py','archives/customer-attraction/tools/evidence/fourcopy-fixed-capacity-discovery-audit/evidence/discovery_n6_c4.json']}
for o in objects:
 for p in extra_evidence.get(o['object_id'],[]):o['evidence'].append(ref_path(p))
# One byte version per assigned material. A mixed page records closed local owners,
# while precise unaccepted owner requests stay explicit in routes and reason.
routes=json.loads((WORK/'owner-routes.json').read_text())
routes['routes'].append({'material':ref(27),'object_ids':['customer-attraction/mixed-private-diagnostic-rational-recovery-and-fixed42-original-audit'],'sections':['无需新LP即可迁移已证42权'],'mathematical_difference':'同4059列/显式42权/同δ正证书的15分组实现与强核心M的解析单调迁移；同一数学付款身份，不另建略异覆盖记录。其它mixed_private_probe非法M由本批18客户反例负责。','route_kind':'evidence','status':'pending-primary-owner-exact-evidence-publication','action':'请主body原作者实接本页path/SHA/唯一标题；比较原42权最小列与本页arg说法，保真正取等位置，勿复制略异主记录。'})
routes['fresh_reading']={'formal_materials':44,'read_scope':'本worker逐一完整实读44篇成熟正式正文；3–6与11显示截段均已补读。未把旧owner-routes当全文阅读证明。','shared_definition_files':['archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md'],'mathematical_executions':0,'raw_evidence_read_scope':'精确定位成熟正文指向的原码/JSON/证书及运行记录；本次未逐原件全文重审、未重新清洗、未重跑。'}
routes['routes'].append({'material':ref(36),'object_ids':['M-f8c942217eda474db14f57dd87bff8c1','M-e5b2ab3d2129428586e7950a62430282'],'sections':['有效同叶折扣为什么救不了真实重复孩子'],'mathematical_difference':'两个较弱clone提升（只保实际叶但可改其它fresh历史；仅保覆盖≤原背景利润）已有精确身份，不能因本页再new-id。','route_kind':'evidence','status':'pending-primary-owner-exact-evidence-publication','action':'含主body的原批作者请实接本页path/SHA/section；本批不复制既有open记录。'})
# Budget and cone have different quantifiers. The budget owner is still unresolved.
routes['routes'].append({'material':ref(11),'object_ids':[],'candidate_pending_object_ids':['customer-attraction/fixed-security-budget-cone-failures'],'candidate_pending_owner_task':'register-ab98f323ad-0070','sections':['五个固定游戏：有序完整SPE菜单的精确递归','全部五输入与结果：负violation恰是正GB'],'mathematical_difference':'五固定客户游戏、各一个安全最优p、所有完整SPE的严格正GB；不同于三固定σ/全客户质量锥的13证书。','status':'needs-decision-primary-owner-exact-id-and-evidence','action':'Boss/lead协调0070原主body作者给精确数学ID并实接本材料；不能只归CA-SELECTED-SECURITY-CONES。'})
for rr in routes['routes']:
 rr['fresh_statement_check']='本worker已实读本页精确陈述、模型/量词/条件、状态与论证位置，未沿用旧路由代读；仍待原主owner准确发布evidence。'
routes['context_updates'].append({'object_id':'customer-attraction/mixed-private-diagnostic-rational-recovery-and-fixed42-original-audit','current_incorrect_statement_excerpt':'最小列(I={6},E=15,J=15)','correct_statement':'首个原arg为整数mask (6,15,15)，其中I mask6={1,2}，E=J mask15={0,1,2,3}；未打印全部并列最小点，不能声称唯一arg。','primary_body':ref_path('archives/customer-attraction/state/程序/混合私有域的诊断与四十二行原始有理核验--程序.md'),'exact_location':'主body第69行原stdout与第72行明确mask解释','impact':'正δ、4059列普遍证书及覆盖结论均不变；正确非核心取等列支持27页强核心版本迁移后最小余量仍恰δ，错误singleton解释不应延续。','action':'请登记lead按旧DONE的定向替代/增量安排原主作者改版statement并接27页证据；不覆盖旧DONE回执，本批不复制主记录。','blocking':False})
# De-duplicate recovery additions, retaining the current exact request.
unique={}
for rr in routes['routes']:
 key=(rr['material']['path'],tuple(rr.get('object_ids',[])),tuple(rr.get('sections',[])))
 unique[key]=rr
routes['routes']=list(unique.values())
cu={}
for u in routes['context_updates']:cu[(u.get('object_id'),u.get('current_incorrect_statement_excerpt'),u.get('section'))]=u
routes['context_updates']=list(cu.values())
# Registry/batch lookup only, never overwrite an external object record.
lookup={}
for f in [ROOT/'research/registry.json']+sorted((ROOT/'research/registration/batches').glob('*.json')):
 for o in json.loads(f.read_text()).get('objects',[]):lookup.setdefault(o['object_id'],o)
material_rows=[]
for i,x in enumerate(mats,1):
 local=[o['object_id'] for o in objects if o['body']['path']==x['path'] or any(r['path']==x['path'] for r in o['evidence'])]
 body=[o['object_id'] for o in objects if o['body']['path']==x['path']]
 pending=[r for r in routes['routes'] if r['material']['path']==x['path']]
 if body: disposition='objects'; owners=local
 elif local: disposition='attachment'; owners=local
 elif pending:
  disposition='needs-decision';owners=list(dict.fromkeys(y for r in pending for y in r.get('object_ids',[]) if y in lookup))
 else:raise RuntimeError(('Unrouted material',i))
 reason='完整实读成熟正文，核精确身份、模型量词、条件、状态及完整证明/证据位置；复用已成熟证明，未重新清洗原码/大JSON或重跑数学。'
 if pending:
  reason+=' 本页跨批主owner尚未实接，状态needs-decision；精确ID、path/SHA、唯一标题和下一动作见0067/owner-routes.json。'
  if local:reason+=' 当前object_ids只列已闭合本批owner，待接外部数学仍明确保留，不能以本页已有本批对象宣称来源已闭合。'
 if i==19:
  # Accepted 472 owner already references the exact page; root-saturation remains pending.
  owners=list(dict.fromkeys(owners+['customer-attraction/three-provider-five-topic-strong-iid-gap-472']))
  reason+=' 472五/六主题有限反例主owner已精确接本页；另任意人数根近饱和解析来源B6仍待实接。'
 material_rows.append(dict(**x,disposition=disposition,object_ids=owners,reason=reason))
batch={'schema':2,'objects':objects,'materials':material_rows,'edge_files':[]}
(WORK/'owner-routes.json').write_text(json.dumps(routes,ensure_ascii=False,indent=2)+'\n')
(ROOT/'research/registration/batches/register-ab98f323ad-0067.json').write_text(json.dumps(batch,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'objects':len(objects),'materials':len(material_rows),'routes':len(routes['routes']),'needs_decision_materials':sum(x['disposition']=='needs-decision' for x in material_rows)},ensure_ascii=False))
