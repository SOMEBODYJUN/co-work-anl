from pathlib import Path
import json,hashlib,re,posixpath
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';HF=C/'r3-stationary-query-and-replicated-menu-audits';S=C/'r3-covariance-menu-coherence-and-escape-review';E=Path('tools/evidence/covariance-menu-coherence-and-escape-review');W=Path('cleanup/workspaces/Boss4/r3-covariance-menu-coherence-and-escape-review-next')
IDS=['90b16a6fa71daf25a8fc','f325ca53c510560b1607','681138cd2e959bc26dcb','b93aa6e5de99b7936688','b97b201c7a5d2373db80']
P='archives/customer-attraction/state/资源/真实菜单协方差与逃逸余项的审查合同--资源.md';P1='archives/customer-attraction/state/资源/真实分支十项合同与菜单可实现性账本--资源.md';PI='archives/customer-attraction/state/引理/完整槽插入税与跨角色价格恒等式--引理.md';P4='archives/customer-attraction/state/障碍/双向隔离惩罚的福利上限与逃逸预算--障碍.md';PH='archives/customer-attraction/state/资源/独立利润消元与惩罚菜单证据的复用边界--资源.md';PB='archives/customer-attraction/state/反例/银行完整根列的两查询最小分离--反例.md';PV='archives/customer-attraction/state/引理/合法前缀的静态额外槽预算与条件归约--引理.md'
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
claimpath=R/'boss4-r3-next-hp-claim.json';claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(IDS)<=set(claim['ids'])
previous=json.loads((HF/'tools/evidence/stationary-query-and-replicated-menu-audits/related-and-next-prework-source-manifest.json').read_text());primary=[];owners=[]
for i in IDS:
 x=next(x for x in previous if x['id']==i);v=inv[i];b=(HF/x['preserved_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];owner=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==v['sha256'];owners.append(owner);q=E/'original'/i/x['path'];cp(HF/x['preserved_path'],q);primary.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'headings':[l for l in b.decode().splitlines() if l.startswith('#')],'read_mode':'HF actual first full original math text as related/parentauthorizedprework; HP exactsamebyte reuse and allunique-section comparison, not new blindreading or mathematical rerun','prior_snapshot':str(HF/x['preserved_path'])})
assert sum(x['size'] for x in primary)==22703
js(E/'source-manifest.json',primary);cp(claimpath,E/'actual-unprojected-claim-receipt.json');js(E/'actual-primary-ownership-snapshot.json',owners);cp(HF/'tools/evidence/stationary-query-and-replicated-menu-audits/read-scope-and-evidence-status.json',E/'actual-prior-HF-read-scope.json')
rep=json.loads((S/E/'hypothesis-clarification-proposals/replacement-manifest.json').read_text());contexts=[]
priorpaths={P1:C/'r3-d22-frontier-ledger-primary'/P1,PI:HF/'tools/evidence/stationary-query-and-replicated-menu-audits/context'/PI,PB:C/'r3-minimal-support-and-uniform-time-primary'/PB,PV:C/'r3-weak-pushforward-and-static-prefix-primary'/PV}
for p in [P1,PI,P4,PH,PB,PV]:
 b=(REPO/p).read_bytes();beforeafter=next((x for x in rep if x['target']==p),None)
 if beforeafter:assert sha(b) in [beforeafter['before_sha256'],beforeafter['proposed_sha256']]
 elif p in priorpaths:assert b==priorpaths[p].read_bytes()
 q=E/'context'/p;cp(REPO/p,q);contexts.append({'path':p,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_mode':'previousactual complete math source/derivation plus currentexactbytecomparison; repeated-tail wording separately reviewed through b93 andminimalproposal','proposal_related_target':bool(beforeafter),'Root_current_version_observed':sha(b),'publication':'actual current bytes snapshot, no fabrication of remote operation by this agent'})
js(E/'context-manifest.json',contexts)
front='---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in [('id','customer-attraction/true-menu-covariance-coherence-and-escape-remainder-review'),('kind','resource'),('type_tag','资源'),('title','真实菜单协方差与逃逸余项的审查合同'),('status','complete-five-source-review; algebra-and-qualified-obstructions; common-payment-unproved'),('summary','保共同客户CC1…4和同全局终局域的COH换分布项、r2平稳基线/固定双不动点障碍、逃逸三非负余项及重复尾最小假设；两旧纠错/两块证明按精确对象duplicate，元均衡条件与当前银行反例分开。')])+'source_refs:\n'
for x in primary:
 for y in x['sources']:front+='  - '+json.dumps('source:'+y['commit']+':'+y['path'],ensure_ascii=False)+'\n'
front+='---\n\n# 真实菜单协方差与逃逸余项的审查合同\n\n'
body=r'''## 五源的身份及域

五原稿4023/2182/3480/3659/9359B，共22703B，HF已经实际全文首读，HP核同SHA逐节比较。单位客户、单位提供者、有限共同非空目录，完整纯SPE在全部合法有序历史规定动作，保空主题、重复、零客户及任意离轨平局。旧一般OPEN不抹去当前五人half定理；六人目标未由本页闭合。

两块独立证书/分母纠错的完整数学已在[真实分支账本](../资源/真实分支十项合同与菜单可实现性账本--资源.md)及HF交付资源中保全，按准确对象duplicate。此页自足补共同客户随机变量与跨节点换菜单的精确债务、逃逸三余项和条件元均衡接口的现行状态，不新造同一实例或定理。

## CC1—CC4：同一客户、同一真实策略、同一列分布

固定合法有序前缀h，过去客户负载b_x≥0，余r≥1。对同一完整纯策略σ，强制当前根B后真后继Y_B，完整剩余列Z(B)=(B,Y_B)，含root共r槽。根分布p与额外查询独立；逐客户定义
\[
a_x(B)=\mathbf1_{\{x\in B\}},\quad k_x(B)=c_x(Y_B),\quad
v_x(B)=\frac1{b_x+1+k_x(B)},\quad
t_x(B)=\frac{a_x(B)}{(b_x+1+k_x(B))(b_x+2+k_x(B))},\quad p_x=\mathbb E_p a_x.
\]
当a1，v−t=1/(b+2+k)；当a0，v−t=v。故v−t正是同完整列后额外查询该客户的价格，不能把v本身当完整槽查询分母。真实根平均D与独立同p查询C为
\[
D(p)=\sum_x\mathbb E_p[a_xv_x],\qquad
C(p,p)=\sum_x p_x\mathbb E_p[v_x-t_x].
\]
逐客户加减p_x E_pv_x，严格得
\[
D(p)-C(p,p)=\sum_x\operatorname{Cov}_p(a_x,v_x)+\sum_xp_x\mathbb E_pt_x.\tag{CC1}
\]
若0<p_x<1，记μ_j=E_p[v_x|a_x=j]，则
\[
C_x-D_x=p_x(1-p_x)(\mu_0-\mu_1)
-p_x^2\mathbb E_p\!\left[\frac1{(b_x+1+k_x)(b_x+2+k_x)}\mid a_x=1\right].\tag{CC2}
\]
这里相反方向债务首项是源会员/真实后缀负载适应性，次项为插入正税。p_x=0或1直接用CC1，不定义空条件期望。

根实际收益u=max_B d_B，e(p)=u−D(p)≥0。对给定p，弱push C(p,p)≤u恰等价
\[
-\sum_x\operatorname{Cov}_p(a_x,v_x)\le e(p)+\sum_xp_x\mathbb E_pt_x.\tag{CC3}
\]
代数没有给左侧符号或支付机制。对另一个共同真实列分布Q，额外查询仍按p抽取，得
\[
C(p,Q)-D(p)=\sum_xp_x(\mathbb E_Qv_x-\mathbb E_pv_x)
-\sum_x\operatorname{Cov}_p(a_x,v_x)-\sum_xp_x\mathbb E_Qt_x.\tag{CC4}
\]
其换分布漂移未被支付。每个客户分别选便宜Q_x不能拼成一个所有客户共用的合法Q。CC1与[完整槽插入/根税恒等式](../引理/完整槽插入税与跨角色价格恒等式--引理.md)的ROOT是同一坐标，不重复认另一份一般支付；Gamma方差身份也不自动控制CC4。

## COH：子节点重新开菜单不是父菜单的条件律

本节只讨论尚有后继玩家的子节点hS（r≥2）；终端子节点没有新的行动菜单。为避免把r槽和r−1槽测试函数相减，把原稿简写的terminal统一为**同一个原游戏全局m槽终局域**。记
\(\widehat Z_h(B)=(h,B,\text{σ真实后继})\)，含固定过去h；Q_h是强制B~p_h、之后完全按σ所得的全局终局律。若p_h(S)>0，纯σ使
\[
\operatorname{Law}_{Q_h}(\widehat Z\mid B=S)=\delta_{\widehat Z_h(S)}.\tag{COH1}
\]
但子节点hS的新菜单是强制下一位C~p_{hS}再按σ，通常
\[
Q_{hS}=\operatorname{Law}_{C\sim p_{hS}}(\widehat Z_{hS}(C)),\tag{COH2}
\]
不是COH1。对任何同全局终局域的测试函数F，精确换基项为
\[
\mathbb E_{Q_{hS}}F-\mathbb E_{Q_h}[F\mid B=S]
=\mathbb E_{C\sim p_{hS}}F(\widehat Z_{hS}(C))-F(\widehat Z_h(S)).\tag{COH3}
\]
若只记剩余后缀，必须给child补回已经固定的S再放同域；不能无说明删原root比较槽数。此为本页对源COH1…3的域澄清，公式本身未赋符号。

p_h(S)=0时父菜单连该正概率条件律都没有，子节点作为合法历史仍有自己的σ/新菜单。把每个节点独立重采样的非负方差相加，不能当一个共同过滤下的全方差望远镜；必须先构造全树相容抽样律，并证明所用比较仍是原σ的真实续局。即使只随机一个根、较深真实历史揭示根后条件协方差为0，跨根条件均值之间的协方差仍保留，未凭零条件项消失。局部角色收益随深度变也不自动是同一个F。

## r=2的平稳正面基线与r=3反例不是同一命题

源b97的正面基线可由两人f−g代数自足展开。恰余2人，末位真实回复ρ(B)，令
\[
f(T)=\sum_{x\in T}\frac1{b_x+1},\quad
g(T,V)=\sum_{x\in T\cap V}\frac1{(b_x+1)(b_x+2)},\quad
U(T,V)=f(T)-g(T,V).
\]
完整槽核P_full=(I+P_ρ)/2；pP_full=p等价pP_ρ=p。对每个合法查询T，末位BR给U(ρ(B),B)≥U(T,B)。平稳使E f(ρ(B))=E f(B)，g对称，故E U(ρ(B),B)=E U(B,ρ(B))=D(p)≤u。又ρ(B)与B同分布，
\[
\mathbb E U(T,\rho(B))=\mathbb E U(T,B)\le D(p)\le u.
\]
左为只保真实末位槽的额外查询价；把原root B加回复整列只增负载，完整两槽查询更小。因此此stationary构造对r2安全，含空主题/零客户/任意合法过去。r1完整列查询也≤裸主题最大值u。这里是既有两人基线的解析展开，不新造定理/不运行程序；不能外推r≥3。

6286客户、六主题、三人的给定完整菜单在现账本及HF资源中有全部原始重数/策略：唯一平稳π=(1,1,0,1,1,0)/4，而query2价5765/4>u2821/2，self C=185785/192<u，五个纯列安全。原发现稿同时明确固定P,K的另一精确合同
\[
\exists p:\quad pP=p\quad\text{且}\quad (Kp)_T\le p^TKp\ \forall T.\tag{DFP}
\]
在此例也为假：唯一π已被query2击破meta最佳回复，不能改选stationary class。未排允许内生改变核的另一个新合同，不反该例stationary self strong-push或自由mixed，也不反half。

发现稿引用的四种材料身份分开：`stationary_full_slot_counterexample_6286.json`称存原客户/43动作/全K/准确范围；`probe_stationary_full_menu.py`称固定原形式策略、保全部SPE行优化指定核，重构有理点后精确核；`stationary_348_diagnostic.json`有query2和query5两条阳性，本正文只用query2，不能把query5当同一输入重复佐证；独立单位审计由round5_audit另一实现展开6286客户/重算全部比较。HP新读的是9359B数学原稿，不是这些代码或JSON；不因此升级原全IC/OPT认证或声称代码不可得。

## 自由真实菜单与内生元均衡：保条件归约、改旧OPEN

681源旧称“自由完整根菜单”，指在**同一σ真实根列**中自由混合，不指任意静态r主题元组。K_AB=Σ_(x∈A)1/(b_x+1+c_x(Z(B)))，root仍在列、查询独立，所有真根偏离d_B≤u。有限minimax给
\[
M_{full}=\min_Q\max_A(KQ)_A=\max_p\min_B(p^TK)_B.
\]
反FM需某个p使**每列**pᵀK[:,B]>u；只给pᵀKp>u一般不够。另构造对称两人元游戏：行收益K_AB、列收益K_BA，不要求K矩阵对称。任一对称NE(p,p)的value v=pᵀKp满足(Kp)_A≤v、支持内取等。若能对某个这样的p证u≥v，就可取Q=p得FM；这是充分条件，不说每个便宜Q都是meta-NE，亦不说真实顺序后继为meta最佳回复。

这组逻辑仍成立，旧一般OPEN状态却不能照抄。[真实零根银行列](../反例/银行完整根列的两查询最小分离--反例.md)在m4给u4/3、Mfull59/36>u，故对任何meta-NE都有value=max_A(Kp)_A≥Mfull>u，没有安全meta-NE。一般真正自由静态extra-one的逐人门槛另由同银行族和Jensen下界19/14≤v5反驳，见[静态预算条件归约](../引理/合法前缀的静态额外槽预算与条件归约--引理.md)；不能仅由¬FM逻辑推出更弱自由背景命题为假。静态minimax/Nash的数学存在性不认证一个新求解算法、时间界或canonical实现。

## 逃逸预算：精确三非负余项及最小几何

固定k≥1，m=k+1，N恰为互不交X_i,Y_i,D之并，C_i=X_i、A_i=X_i∪Y_i及D是合法主题。给定完整SPE实际C_1…C_k,D，记x_i,y_i,d,S=Σx_i,Y=Σy_i，则W=S+d，k个A_i加D覆盖全N，OPT=S+Y+d。

实际i节点改A_i后，原真实末位选合法B_i，收益s_i；该末节点改D收益q_i；实际i改B_i后本人真实最终收益t_i。这里**不需要**B_i只在本地池支撑，不需要其分支末位指定A_i，也不要求两枝有可比较负载。只用
\[
x_i-t_i\ge0,\quad s_i-q_i\ge0,\quad d-x_i/2-y_i\ge0.
\]
令E=Σ_i[(s_i−t_i)+(d−q_i)]，则
\[
S-kd+E=\sum_i[(x_i-t_i)+(s_i-q_i)]\ge0.
\]
更强的完整恒等式为
\[
\begin{aligned}
&(3k+2)W+(2k+1)E-2(k+1)OPT\\
&=(2k+1)\sum_i[(x_i-t_i)+(s_i-q_i)]
+2(k+1)\sum_i[d-x_i/2-y_i]\ge0.
\end{aligned}\tag{ESC}
\]
由W/OPT展开即证，不需要E≥0；d−q_i≥0本来真，而s_i−t_i可负。只知真OPT>2W时，Y>S+d结合末位界Y≤kd−S/2，得S<2(k−1)d/3及E≥kd−S>(k+2)d/3。d0迫全局池空，k1迫S<0，都无严格half反例。E仍未被W支付，这只是该实际路径结构的必要条件，不是一般half证明。

## 重复尾模板的显式假设与两页最小提案

这是另一个有r≥1个尾追随者的具体方案，不套前述k+1人数率界。固定D=Z⊔R，局部核心X_i∪Y_i与D不交，B_i=X_i∪Y_i∪Z；除已指定实际C_i/偏离A_i和所列尾行动外，其他动作不覆盖核心或R。actual末端r次D，拟A_i枝末端r次B_i。实际末位D改B_i的公共Z项抵消，需|R|/r≥|X_i|/2+|Y_i|；拟分支末位B_i改D的公共Z同样抵消，未覆盖R首次得|R|，需(|X_i|+|Y_i|)/(r+1)≥|R|。非零核心a给r(r+1)≤2，r≥2不可能，r1强制Y_i空。

若Z/R重叠、其他中间行动预覆盖R或核心，写定分母即会改变；不能沿用这两比较。共同Z贡献在每次单节点比较中抵消，关键是R分离/未被其他未指定动作覆盖，不给一般E额外强加这些重复模板条件。

[两页最小提案](../../../../tools/evidence/covariance-menu-coherence-and-escape-review/hypothesis-clarification-proposals/replacement-manifest.json)给GS隔离页与HD资源各自完整before/SHA、完整proposed及零context patch，只补上述r/不交/其他动作条件及架构区分，公式和metadata不改。本代理不覆shared、旧包不重写；Root若另审读应用，以Root实际应用证据为准，原proposal仍保持创建时身份。此澄清不是把旧source/done整体判错。

## 两块独审与纠错的精确duplicate

90b稿的两块32客户/八人/八主题根表、13872DAG/7437决策节点/59496比较、整数BI840缩放/12870前缀/6435叶、B根另一候选(2,1,0,1)|q0不可实现，以及Q/p匹配851/280、Q自身为meta-NE均已HF全文保在资源。其数学主证明和输入已在既有账本自足；不把MD“单位审计通过”当HP新读DAG/程序或新run。

f325纠错撤销的是用旧D玩家13/4替额外查询137/60的阳性；q0另块37/10，两块uniformD的C359/120、gap−31/120。条件k块C_k=37/10−17/(12k)仅k≥4才超u；需全真实嫁接/全部root偏离。qD单块查询向量(16/5,23/15,59/20,137/60)有纯安全cap，但不能推出所有完整菜单必有纯列，后来的八人反例已否此一般桥。早期规范BI(q0,q0)不可实现与尚未独立证书是当时事实，后续独立重造DAG另保时点。全部独有数学/版本与撤销用途现已明确去向，duplicate不新造同一反例。

本批五份原文全部定义、公式、状态与代码/输出用途已分主对象和此资源保全；没有新数学程序/原CLI/LP/BI/随机/旧成功复跑。CC/COH没有付一般协方差或换菜单债务，ESC只在指定实际路径，局部负结果不反六人half，也不认证外审、新颖性或未交付算法。
'''
put(P,front+body);js(E/'formal-resource-manifest.json',[{'path':P,'bytes':(S/P).stat().st_size,'sha256':sha((S/P).read_bytes())}])
mp=C/'learning-hp-next-local-mathematics/local-export-manifest.json';nmanifest=json.loads(mp.read_text());assert len(nmanifest['rows'])==5 and nmanifest['missing']==[];cp(mp,E/'actual-next-byteavailability-local-export-manifest.json');cp(C/'local_blob_export.py',E/'authorized-local-export-helper.py.txt')
coverage=[
{'id':IDS[0],'disposition':'duplicate','targets':[P1,P],'units':['two32unitblock exact8rootmenu/actualD0/rootincolumn/allrootd<=u','independentintegerBI840/12870prefix/6435terminal root8targets feasible andBwrongtargetnotfeasible','DAG13872 includesmemorytarget index/all8edges/historynotanonymized','secondindependentunitcode32clients/all7437node59496comparisons claimednotnewread/codeexecution','full+1purequery37/10/W=OPT32/actualhalfholds','exactQ upperandpdual851/280/59/280margin andQ itselfsymmetricmetaNE','oldnohalf/freemixedconclusion source-local notcurrentgeneralOPEN/nowdifferentactualreportscope']},
{'id':IDS[1],'disposition':'duplicate','targets':[P1,P],'units':['old13/4rootwronglysubstitutedfornewquery137/60 fatalcorrection','2uniformD C359/120/gap-31/120/rootwithdrawalbeforedraft/cert','oldcanonicalBI qDq0rootbranchesfeasible/q0q0notroot/notindependentreconstructedtimepoint','conditionalkblockCformula strictthresholdk>=4 nofullgluing orallotherrootcontrol','fullsingleqDqueryvector/cap16/5/oldnextpurebridge laterrefuted8DAG','generalweak/extra/halfnotrefutedbythisattempt independentofcurrentotherbankcounter']},
{'id':IDS[2],'disposition':'integrated','targets':[P],'units':['independent5unittypes oldquerydenominator/2copies correction andconditionalk>=4','legalnode/samepureσ/rootincluded rcolumns/u rootmax independentquery/K notr-1','exactminimax rowseparationforallrealcolumns notonlypKp unsafe','symmetricmetagame payK_AB andK_BA notsymmetricmatrix/existsNE andBRproperty','someendogenoussafeNE sufficesFM notallp/none-realcontinuationMETA BR transfer','oldunproved/FM/extraOPEN correctedbyactualzero-root bankwithseparatefreestaticlowerbound','no newNashalgorithmtimecanonicalcert fromexistence']},
{'id':IDS[3],'disposition':'integrated','targets':[P,P4],'units':['allactualC1..CkD/disjointN/OPTfullcover/W quantities','s/q/t realbranches/all3ICslacks/E signed terms','newexactnonnegidentity ESC notjustwelfarebound/noE>=0','strictS/Ehalfnecessarybound/d0/k1/realcomparisonstrictness','minimalassumptions BsupportandBbranchlastactionnotused butAbranchlastBneeded','repeatrtail r>=1 DdisjointZ R/coreDdisjoint otheractionsnoR/core','lastnodeZcancellation/tworequiredinequalities/r>=2impossible/r1Yzero','twooldformalminimalexplicit-assumption proposals no sharedwrite/source/doneoverallinvalidation']},
{'id':IDS[4],'disposition':'integrated','targets':[P,PI],'units':['commoncustomer a/k/v/t/p definitions fullr includesroot/additional+1 independentquery','CC1covariance/tax andCC2Bernoulli conditional/cornerp0p1','CC3u-D slack exactweakduty/CC4commonQ drift no sign/customerdifferentQinvalid','COH1parentconditiondirac/COH2freshchildmenu/COH3signedswitch/allglobalterminaldomainclarification','zero-supportchildconditionalundefined/globalcoherentlaw obligation/lawvariance notindependentnodebudget','r2positive stationarytransport baseline proof/r1boundary/r3notextend','full6286masks/policy/menu/d vector/258IC report/uniqueπ/query2 prices andhalf margins inheritedexactledger','selfbudgetpositive/purecols safe/transientquery/fixedDFP no solution notendogenouskernelgeneralization','discoveryfixedσ LPandfractionpoint/code/JSON/diagnosticquery2andquery5different find/unitauditroles no newrun','generalhalf5known/6open/sourcebudget/COH no universalupperbound or newexternalnovelty']}
]
js(E/'semantic-coverage-map.json',coverage)
scope={'primary_sources':5,'primary_bytes':sum(x['size'] for x in primary),'primary_lines':sum(x['lines'] for x in primary),'primary_first_full_read':'HF actual firstfull original math texts underrelated/prework authorization, HP exactsameSHA allsection comparison, not fictionalfirstreading or anotherblindreview','dispositions':{'integrated':3,'duplicate':2},'new_formals':1,'new_named_theorems_or_instances':0,'novel_source_content_preserved':['CC4withQdifferentp andallBernoulli/cornerstates','COH1to3 onexplicitcommonfullglobalterminaldomain andnonterminalchildcondition','r2stationary baseline algebraexpanded notnewresult','fixedP,Kdoublefixedpoint failure notgenericendogenouskernelno-go','ESC exact3nonnegativeICremainders withminimalBgeometry','repeat-taildisjointZ/R andnootherR/corecoverage explicitminimal2targetproposals'],'source_program_code_or_rawJSON_read_or_execution':0,'new_math_program_runs':0,'new_original_CLI_calls':0,'old_success_replays':0,'new_SPE_LP_BI_random_program_runs':0,'local_helper_calls':1,'local_blob_attempts':5,'local_exports':5,'local_missing_blobs':0,'helper_role':'next5MD byteavailability only; their text not fullread inHP, no primaryreceipt','next_source_semantic_reading_claim':False,'shared_Git_writes':0,'claim_done_checkpoint_show_calls':0,'network_or_lazy_fetch':0,'real_account_board_auth_operations':0,'phase3_graph_import':0,'raw_claim_ids':len(claim['ids']),'primary_claim_intersection':IDS,'claim_projection_performed':False,'hypothesis_proposals':2,'hypothesis_shared_overwrites_by_this_agent':0,'hypothesis_proposal_scope':'explicitassumptions forparticularrepeat-tailarchitecture only, rootbeforeSHAapplyreview; metadata/formula/sourcefrozenrawunchanged','prior_GS_HD_HF_packets':'notrewritten orretroactively upgraded, historicalmissing/MDreadandRootactualapplication stages distinct','derived_builder_calls':1,'derived_builder_failures':0,'hypothesis_preparer_calls':1,'hypothesis_preparer_failures':0}
assert scope['primary_bytes']==22703;js(E/'read-scope-and-evidence-status.json',scope)
notes=[
('4023B两块独立构造稿HF已实际全文首读，HP核同字节逐节对客户/八根/完整有序DAG/BI与单位核验/混合原始对偶及NE结论，不假装新首读。','GS和HF已有完整主数学；本资源给精确原独立BI840/12870/6435与7437/59496/错误B另目标不实现的角色去向；旧HD未读review的历史不改写，当前也未读其原code/DAG/reports。','duplicate：完整两块辅助桥对象和关键证明已有目标，独立审查历史身份不多算新人员、机器run或新颖性；不由此例mixed安全推一般FM真或half结论。'),
('2182B分母纠错HF已全文实际读，HP同SHA对所有数值/撤销时点/早期BI记录/条件k复制式/单块cap/后续方向逐段保全。','旧13/4为原D收益、137/60为新查询，均匀两块359/120及差-31/120已自足；早期尚无独立压缩证书与后期独立DAG按时间区分，q0q0不可实现记录不是一般直和。','duplicate：全部独有数学/失败过程与来源状态已有准确去向，不恢复被撤销弱阳性；旧要攻纯列的计划后来已反驳，一般weak/extra/FM当前由另外银行例处理，0旧成功复跑。'),
('3480B独立纠错/菜单接口全文HF已真读，HP核同字节按合法前缀/全r槽/查询独立/两种minimax/内生NE充分条件及当时OPEN完整比对。','保原K非对称也可构造对称游戏；某个安全对称NE给FM是充分非必要声明，不将坏pKp一项当所有列分离。用既有零根银行Mfull>u更新一般安全NE/FM假命题，与静态freeextra另证下界分开。','integrated：新资源自足当前量词/状态纠错和跨真实分支适用域，数学Nash存在不变算法或canonical运行认证，不把元最佳回复搬到真实顺序历史。'),
('3659B逃逸独审HF已全文实际读，HP同SHA逐式重建一般E定义、三个真实比较、精确非负恒等式、严格阈值/零界和全部重复尾假设/审查建议。','现GS只给福利式与必要阈值，本源更强ESC精确三余项和较弱B_i几何条件补资源；重复方案D=Z⊔R、core-D不交、其他未指定行动不预覆盖core/R须显式，形成两当前正文最小before/after/patch提案。','integrated：一般E不需E>=0或B_i本地支撑/另枝末位A，不能误加重复方案强假设；两提案不覆shared或旧包，不把旧done整体判错，r>=2失败仅具体架构。'),
('9359B共同客户/平稳构造发现稿HF已全部正文/表格/尾段实际首读，HP核同SHA逐项核CC1to4、COH1to3、r2基线、6286完整例/DFP和每份输出用途。','CC1与已有ROOT同坐标，CC4换Q与子菜单COH漂移尚未支付；本资源把COH测试函数定在共同全局m槽域并限非终端child，r2用f-g/平稳完整展开。6286full-slot与DY1274tail/旧348权表不同；uniqueπ非metaNE仅固定P,K不共同不动点。','integrated：所有独有数学/数据角色归位，发现诊断query2和query5不当同一输入重复证据；源称258/OPT核验未升级当前原代码/JSON实读或run，CC/COH/DFP不自动否half或解决一般支付。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 原多组真实claim完整保留，按本5交集/当前owner/sourceSHA核验，不伪投影或自行done。','comparison_note':b,'decision_note':c,'disposition':x['disposition'],'targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(E/'README.md',r'''# 真实菜单协方差/换基与逃逸独审

5primary22703B在HF已实际全文首读，HP核同SHA逐节比较；3integrated+2duplicate、1资源0新命名定理/实例。完整CC1…4/COH1…3/r2基线/固定DFP、ESC三非负余项和重复模板最小假设保全，两个旧纠错/两块独审按准确数学对象duplicate。

两处已交派生正文需显式补D=Z⊔R/core与D不交/其他动作不预覆盖core-R，最小before/after/zero-contextpatch仅在evidence；本代理未覆shared，旧包不改，Root实际应用另记。新资源不给一般E强加这些只属重复模板的条件。

1次安全helper核下一5MD字节全齐，无缺；尚不声称这下一5文本已读完，也不写其primaryreceipt。0新数学/原CLI/SPE/LP/BI/随机/旧成功/network/sharedGit/身份或公屏行为。完整原多组claim保留，仅本5subset/owner/sourceSHA生成当前receipt。Root先推正文依赖再done，不进入第三阶段图。
''')
put(W/'relation-review.md',r'''# 阶段二关系

共同客户ROOT=CC1是同一精确坐标，条件Bernoulli式和换Q漂移补完整变量范围。COH3在同一全局终局域比较新child菜单与parent条件Dirac，揭示不是共同抽样律，非负局部方差不能自行望远镜。r2stationary用同目录BR和f-g平稳交换成立；r3固定P,K的DFP失败不排另构内生核，也不反该例self预算/half。

对称元游戏的安全NE只给真实列FM充分接口，坏pKp不等全列分离。银行当前Mfull>u使通用安全NE接口为假；自由静态extra是不同域并有独立Jensen证据，不能只以强桥否定推出弱桥否定。

ESC精确三非负IC项只需给定无拥挤路径和指定A枝末位B，B支撑/另一枝末位动作非依赖；重复r尾需要明确Z/R分离和其他动作避core/R。两份最小提案补此范围，不改整个旧结果真值，不把必要条件点当完整SPE存在。

两个旧分母纠错/两块独审数学已有精确去向，不造重复反例/新审稿人/新run。下一5只是实际字节候选，无预领/成功receipt，0阶段三超图导入或强制连通。
''')
nextrows=[]
for x in nmanifest['rows']:
 v=inv[x['id']];b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'];q=REPO/'cleanup/progress'/f"{x['id']}.json";pr=json.loads(q.read_text()) if q.exists() else None
 if pr is None:nextrows.append({**v,'local_path':x['local_path'],'progress_observed':None,'read_status':'actualbyteavailability only inHP, no new fullsemantic/code review or primaryreceipt; earlierrelatedread if any must be established separately after claim'})
js(W/'next-candidates.json',nextrows)
cp(Path(__file__),E/'build_delivery.py')
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
def tex_balanced(s,left,right):
 def count(delim):return sum(ord(s[i])==92 and s[i+1]==delim and (i==0 or ord(s[i-1])!=92) for i in range(len(s)-1))
 return count(left)==count(right)
assert tex_balanced(chr(92)+'[x'+chr(92)+']','[',']') and not tex_balanced(chr(92)+'[x','[',']') and tex_balanced(chr(92)*2+'[2pt]','[',']')
for x in primary:
 b=(S/x['preserved_path']).read_bytes();ck('primary exactsize SHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('primary exactblob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('rawclaim byteidentical',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes());ck('actual5subset currentowner',set(IDS)&set(claim['ids'])==set(IDS) and all(x['owner']=='Boss4' and x['source_sha256']==inv[x['id']]['sha256'] for x in owners));ck('pushedsynced realclaim',claim['status']=='pushed' and claim['local_sync']['status']=='synced' and claim['remote_tip']==claim['local_sync']['remote_tip'])
for x in contexts:ck('exactcontext snapshot '+x['path'],len((S/x['snapshot']).read_bytes())==x['bytes'] and sha((S/x['snapshot']).read_bytes())==x['sha256'])
t=(S/P).read_text();ck('flatMATEK',all(re.search('^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']));ck('newformal C0zero',not any(ord(c)<32 and c!='\n' for c in t));ck('newformal trailingzero',all(l==l.rstrip() for l in t.splitlines()));ck('actualTeXdelimiters balanced',tex_balanced(t,'[',']') and tex_balanced(t,'(',')'));links=[]
for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
 if '://' in dest or dest.startswith('#'):continue
 n=posixpath.normpath(str(Path(P).parent/dest.split('#',1)[0]));q=S/n if (S/n).exists() else REPO/n;ck('actualrelative link '+dest,q.exists());links.append({'source':P,'destination':dest,'resolved':n,'bytes':q.stat().st_size,'sha256':sha(q.read_bytes())})
js(E/'formal-link-check.json',links)
ck('CC1to4 alltyped',all('tag{'+x+'}' in t for x in ['CC1','CC2','CC3','CC4']));ck('COH1to3 commonterminal/nonterminal/support domain',all('tag{'+x+'}' in t for x in ['COH1','COH2','COH3']) and 'r≥2' in t and '全局m槽终局域' in t and 'p_h(S)=0' in t);ck('r2positive fulltail transport notr3extension',r'E U(T,\rho(B))' in t and '不能外推r≥3' in t);ck('fixed DFP notgeneric','tag{DFP}' in t and '允许内生改变核' in t);ck('ESCexact/minimaldomain','tag{ESC}' in t and '不需要E≥0' in t and '不需要**B_i只在本地池支撑' in t);ck('repeatedtail disjoint /otheractions explicit','D=Z⊔R' in t and '其他动作不覆盖核心或R' in t)
ck('5complete receipts3integrated2duplicate',len(receipts)==5 and {x['id'] for x in receipts}==set(IDS) and sum(x['disposition']=='integrated' for x in receipts)==3 and sum(x['disposition']=='duplicate' for x in receipts)==2)
for x in receipts:ck('semanticreceipt complete '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']) and all((S/p).exists() or (REPO/p).exists() for p in x['targets']))
for x in rep:
 before=(S/x['before_path']).read_bytes();after=(S/x['proposed_path']).read_bytes();ck('proposal exactbefore '+x['target'],len(before)==x['before_bytes'] and sha(before)==x['before_sha256']);ck('proposal exactafter '+x['target'],len(after)==x['proposed_bytes'] and sha(after)==x['proposed_sha256']);u=after.decode();ck('proposal metadataunchanged '+x['target'],before.decode().split('---',2)[1]==u.split('---',2)[1]);ck('proposalformatzero '+x['target'],not any(ord(c)<32 and c!='\n' for c in u) and all(l==l.rstrip() for l in u.splitlines()));ck('no sharedtarget transportoverwrite '+x['target'],not (S/x['target']).exists());ck('hypothesisconditions explicit '+x['target'],'D=Z⊔R' in u and '其余行动均不覆盖X_i∪Y_i∪R' in u)
ck('only1newformal topstate',list((S/'archives').rglob('*.md'))==[S/P]);ck('alloriginalmathprograms0',all(scope[k]==0 for k in ['new_math_program_runs','new_original_CLI_calls','old_success_replays','new_SPE_LP_BI_random_program_runs','network_or_lazy_fetch','shared_Git_writes']));ck('actualhelper1call5byteexports0missing',len(nmanifest['rows'])==5 and nmanifest['missing']==[])
for x in nextrows:ck('actualnextavailable '+x['id'],Path(x['local_path']).exists() and len(Path(x['local_path']).read_bytes())==x['size'] and sha(Path(x['local_path']).read_bytes())==x['sha256'] and x['progress_observed'] is None)
obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:u=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen=any('/'+z+'/' in rel for z in ['original','related','context','before']);bad=[i+1 for i,l in enumerate(u.splitlines()) if l!=l.rstrip()];c0=[{'offset':i,'code':ord(c)} for i,c in enumerate(u) if ord(c)<32 and c!='\n']
 if bad or c0:obs.append({'path':rel,'frozen':frozen,'trailing_lines':bad,'nonLF_C0':c0})
ck('allnewderived C0/trailingzero',not any(not x['frozen'] for x in obs));js(E/'transport-format-observations.json',{'observed':obs,'frozen_original_context_before_unchanged':True})
put(W/'delivery.md',f'''# HP交付

5primary22703B/{scope['primary_lines']}行HF已真实全文首读，HP核同SHA逐独有段/全仓现对象比较；3integrated+2duplicate、1自足资源0新命名定理/实例。完整CC1…4/COH1…3/r2stationary基线/固定DFP/ESC精确三余项/重复尾明确条件保全。

原{len(claim['ids'])}ids claim {claim['remote_tip']} actualpushed/synced整件保，仅本5subset/currentowner/sourceSHA处理。2最小hypothesis提案before/after/zero-contextpatch仅evidence，不直接覆shared或改旧包/metadata/公式；Root实际应用另证。1helper5下一MD实际byte齐0缺，仅byte候选不冒全文，0新数学/原CLI/SPE/LP/BI/随机/旧成功/network/sharedGit/账号行为。

Root先推正文依赖后done，下一{len(nextrows)}实际本地候选path/SHA和读范围准确记录，不预claim/成功receipt，不导第三阶段图。
''')
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'relative_links':len(links),'formal_nonLF_C0':0,'formal_trailing_whitespace':0,'scope':'actualsource/owner/rawclaim/coverage/typing/link/format/proposal/transport checks only; mathematical reading/derivation not replaced by counters or originalprogramPASS'})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':22703,'primary_lines':scope['primary_lines'],'new_formals':1,'formal_bytes':(S/P).stat().st_size,'receipts':5,'dispositions':{'integrated':3,'duplicate':2},'checks':len(checks),'relative_links':len(links),'hypothesis_proposals':2,'proposal_status':'evidenceonly/not appliedbyagent/no top-levelsharedtargetoverwrite inwhitelist','new_math_runs':0,'raw_claim_ids':len(claim['ids']),'claim_tip':claim['remote_tip'],'next_candidates':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
