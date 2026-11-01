from pathlib import Path
import json,hashlib,re,posixpath
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';GS=C/'r3-d22-frontier-ledger-primary';S=C/'r3-independent-profit-isolation-and-menu-proofs';E=Path('tools/evidence/independent-profit-isolation-and-menu-proofs');W=Path('cleanup/workspaces/Boss4/r3-independent-profit-isolation-and-menu-proofs-next')
IDS=['efb09bff2fbae18ba384','c9ccc7817c179b3b1396','73e78b9e31ec4e9518da','4fa30e438229f7d5436d','66007ee43711768dbc97']
P='archives/customer-attraction/state/资源/独立利润消元与惩罚菜单证据的复用边界--资源.md';P1='archives/customer-attraction/state/资源/真实分支十项合同与菜单可实现性账本--资源.md';P2='archives/customer-attraction/state/障碍/最优剩余利润的局部系数与共享负载信用--障碍.md';P4='archives/customer-attraction/state/障碍/双向隔离惩罚的福利上限与逃逸预算--障碍.md';PF='archives/customer-attraction/state/反例/任意人数首步补全余额--反例.md'
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
claimpath=R/'boss4-r3-next-hd-claim.json'
if not claimpath.exists():raise SystemExit('HD actual claim absent: no primary receipt written')
claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and set(IDS)<=set(claim['ids'])
assert claim['local_sync']['status']=='synced','stop for actual independent recovery; never rewrite raw needs-attention'
previous=json.loads((GS/'tools/evidence/d22-frontier-ledger-primary/related-source-manifest.json').read_text());primary=[];owners=[]
for i in IDS:
 x=next(x for x in previous if x['id']==i);v=inv[i];b=(GS/x['preserved_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];owner=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==v['sha256'];owners.append(owner);q=E/'original'/i/x['path'];cp(GS/x['preserved_path'],q);primary.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'headings':[l for l in b.decode().splitlines() if l.startswith('#')],'read_mode':'GS actual entire original mathematical text; HD complete actual byte/SHA reuse and per-section comparison, not another first read or claimed blind review','prior_snapshot':str(GS/x['preserved_path'])})
assert sum(x['size'] for x in primary)==24864
js(E/'source-manifest.json',primary);cp(claimpath,E/'actual-unprojected-claim-receipt.json');js(E/'actual-primary-ownership-snapshot.json',owners)
contexts=[]
for p in [P1,P2,P4,PF]:
 b=(REPO/p).read_bytes();prior=GS/p if (GS/p).exists() else GS/'tools/evidence/d22-frontier-ledger-primary/context'/p;assert b==prior.read_bytes();q=E/'context'/p;cp(REPO/p,q);contexts.append({'path':p,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'reading':'prior actual full mathematical reading/preparation, now exact whole-byte comparison; no quantity-driven reread of done source','prior_snapshot':str(prior)})
js(E/'context-manifest.json',contexts);cp(GS/'tools/evidence/d22-frontier-ledger-primary/read-scope-and-evidence-status.json',E/'actual-prior-GS-read-scope.json');cp(GS/'tools/evidence/d22-frontier-ledger-primary/formal-resource-manifest.json',E/'actual-prior-GS-formal-manifest.json')
front='---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in [('id','customer-attraction/independent-profit-elimination-and-punishment-menu-evidence-reuse'),('kind','resource'),('type_tag','资源'),('title','独立利润消元与惩罚菜单证据的复用边界'),('status','full-five-source-semantic-review; alternative-proof-retained; source-reported-DAG-not-newly-certified'),('summary','保存独审不同次序的严格利润消元、隔离证明最少比较、共享信用等价数值界、奖励密度局部冲突与八人DAG各程序证据角色；复用已完整对象，不新增数学定理或原程序运行。')])+'source_refs:\n'
for x in primary:
 for y in x['sources']:front+='  - '+json.dumps('source:'+y['commit']+':'+y['path'],ensure_ascii=False)+'\n'
front+='---\n\n# 独立利润消元与惩罚菜单证据的复用边界\n\n'
body=r'''## 五份原稿与已有对象

五份24864B原文在GS必要related阶段已实际全文读，HD核同字节后逐节比较，不虚构再次第一读或新增盲审。模型均为有限单位客户、有限共同非空目录、单位提供者、全部有序历史纯SPE，保空主题、重复和任意离轨平局。

| 原稿及独有用途 | 已有完整数学与本资源补充 |
| --- | --- |
| efb09bff2fbae18ba384 / 3417B利润族独审 | 结论已在[利润/信用障碍](../障碍/最优剩余利润的局部系数与共享负载信用--障碍.md)，但独审“先消A、再消叶重复、再消多B”的严格证明不同于原分b=0/b≥1的换槽论证，下面完整保留。它没有重证原族全部历史SPE。 |
| c9ccc7817c179b3b1396 / 3802B无界独审 | 全A完整SPE、精确F与无界实α、尾信用及共享函数冲突全部同已有对象；精确duplicate数学，保先盲重构历史和另一组等价数值界，不增加独立审稿人数。 |
| 73e78b9e31ec4e9518da / 4353B隔离独审 | [隔离障碍](../障碍/双向隔离惩罚的福利上限与逃逸预算--障碍.md)已完整保同一证明；duplicate，补清哪些激励行实际未用、逐项范围和同一真实分支条件。 |
| 4fa30e438229f7d5436d / 4278B打破隔离探索 | E缺口、阈值和重复追随者冲突已在隔离对象，补未完成奖励设计的最终密度比较；不能据同局部核心给所有异质奖励no-go。 |
| 66007ee43711768dbc97 / 9014B纯根菜单稿 | [真实分支账本](../资源/真实分支十项合同与菜单可实现性账本--资源.md)已保完整模型/客户/根列/DAG证明合同/矩阵匹配，下面保发现器、直接核验、父独立核验和另一重造DAG的证据角色及原文CLI身份。未读原代码/原DAG不是当前已认证执行。 |

“root未读发现稿”“独立研究员先见陈述”均是当时原审查先验。当前清洗知道两方稿件，不新增一个盲审者，也不声称外审或新颖性。

## 交叠族的另一套全整数最优性证明

固定n≥4、x=n−2，目录恰A,B,L_1,…,L_n。每个普通j<n有不同单位客户{L_j}:x、{A,L_j}:1、{B,L_j}:x；特殊叶有{L_n}:x、{B,L_n}:x、{A,B,L_n}:n−1。完整SPE及实际A B^(n−1)的全部有序历史证明由[原族](../反例/任意人数首步补全余额--反例.md)承担；本独审的新增任务是固定第一名A后的**剩余利润**优化，不把那页总覆盖补全F与这里利润F同名混用。

剩n−1槽，计数a,b,ℓ_j，总和n−1，t为正叶数。实际客户给
\[
P=x t+x\sum_j\mathbf1_{\{b+\ell_j>0\}}
+\sum_{j<n}\frac{a+\ell_j}{1+a+\ell_j}
+(n-1)\frac{a+b+\ell_n}{1+a+b+\ell_n}.
\]
所有零分子取零。对f(c)=c/(1+c)，移去一名正覆盖者损失1/[c(c+1)]，下面每次换槽均保持整数和目录合法。

**第一步，消去A。** a≥1时存在缺失叶。特殊叶缺失时，把一名A换成特殊叶，特殊共享项a+b+ℓ_n不变，普通背景共享总损失≤(n−1)/2<x，新私有获x且B共享覆盖不减，严格改善。特殊叶已选时，存在未选普通叶，把A换到它：此新普通叶的a+ℓ不变，其他普通项总损失≤(n−2)/2，特殊项因a+ℓ_n≥2损失≤(n−1)/6。总损失≤(4n−7)/6<x（差为(2n−5)/6>0），新私有获x，B共享不减。于是最优a=0。

**第二步，消去叶重复。** 若某ℓ_j≥2，把其中一次换成缺失叶。原叶仍覆盖、不丢私有或B共享旧覆盖；新私有获x。普通背景共享损失≤1/6，特殊≤(n−1)/6，均严格小于x。因此最优每叶至多一次。

**第三步，B至多一次。** b≥2时，把一名B换成缺失叶，仍有B维持全部B共享覆盖。新私有获x，特殊背景共享损失≤(n−1)/6<x；若换入特殊叶则此共享项不变。故最优b≤1。

**第四步，只剩两类。** b0时选n−1不同叶，含特殊叶最优，值P_0=2(n−1)x+(2n−3)/2。b1时选n−2不同叶，普通换成特殊叶增加(n−1)/6−1/2=(n−4)/6≥0，得P_1=2(n−1)x+(7n−13)/6。P_1−P_0=(n−4)/6≥0，n4平局保留。因此
\[
F_{n-1}(\mathbf1_A)=2(n-1)(n-2)+(7n-13)/6.
\]
这套不同顺序的消元是原独审独有证明，不是对有限n点外推。u_1=n−1/n、F_n(0)=OPT=2n²−2n−2，故局部系数二余额(23−5n)/6−2/n在n≥5负；α<17/6最终失败。全局half余量2(n−1)>0、真实尾信用的精确值仍按已有利润对象保留。本页不再造同一个局部反例定理。

原独审称仅先收到客户类型/待核公式，未读发现稿消元；其独立代码枚举n4…8共15501计数候选只核有限实现，完整SPE来自既有族。HD未读或运行该代码/输出，不把文字记录升级为新run。

## 无界独审的等价数值界与隔离证明的实际依赖

全A大主题族n人、A有n客户、n−1个不交singleton，每个有序历史都A是完整SPE：照做收益n/(过去A+余人)≥1，改singleton≤1。u1，Wn，OPT2n−1；固定一名A后Ftail=2n−h_n，h_n=min整数1≤j≤n(j+n/j)，h_n≥2√n。对任意有限α可选任意充分大n使2√n−1>α，或如现页选平方人数；二者同一构造/量词，不是不同底层反例。真实tail额外信用h_n−2付根债h_n−3，余量1。

共享负载模板只依r及每客户(b,c)，实例无关且f(0,c)=f(b,0)=0。两个完整族同r=n−1迫
\[
f_r(1,r)\ge(2-h_n)/n,\qquad
f_r(1,r)\le\frac{(23-5n)/6-2/n}{n-1}.
\]
既有对象用前界>−1/2、后界<−1/2排n≥16。c9独审另写前界≥−7/16、后界<−19/30。这里保其等价加强：h_n≤2√n+1给前界≥1/n−2/√n；令t=√n≥4，
\[
\frac1{t^2}-\frac2t+\frac7{16}
=\frac{7t^2-32t+16}{16t^2}\ge0
\]
（分子在t4为0、此后增）。后界的分子加(19/30)(n−1)为(16−n−10/n)/5<0，故严格<−19/30。是同一解析矛盾的数值表达，允许负f、不排独占项/实例或目录/非可加信息，不新建第二信用障碍。

隔离独审保相同三比较：两真实枝局部负载相同给v_i=|B_i∩(X_i∪Y_i)|/2+|B_i∩D|；A_i枝末位改D给v_i≥d；实际早期可改B_i给x_i≥v_i；实际末位D可改A_i给d≥x_i/2+y_i。因此逐项
\[
d\le x_i\le2d,\qquad 0\le y_i\le d-x_i/2\le x_i/2.
\]
注意这条证明**没有使用**当前玩家改A_i的IC，也没有使用B_i枝末位A_i自己的BR；不把未用行伪列成证明依赖。但两枝几何/实际D/客户全集/旧C_j避开池均承重，三个比较不产生完整SPE的存在性。原独审的非均匀等号、k1/零界已在隔离对象完整证明；duplicate不是按标题或同计数自动判断。

## 逃逸探索未完成：两种重复方案的范围

原隔离实际C_1…C_k,D有m=k+1。撤隔离后，A_i枝末位B_i收益v_i、实际i改B_i后的最终收益b_i，以及A_i枝末节点改D收益d_i^Q来自同一完整策略。定义Δ_i=v_i−b_i（可负）、T_i=d−d_i^Q≥0、E=Σ(Δ_i+T_i)。已有对象已完整证S≥kd−E与
\[
2(k+1)OPT\le(3k+2)W+(2k+1)E,
\]
并保真half反例必须E>(k+2)d/3，非充分条件也未由W支付。

随后r个相同尾追随者是**另一具体重复方案**，不能把前段m=k+1率界机械套入。若实际尾部r次D=Z∪R，拟惩罚A_i后r次B_i=X_i∪Y_i∪Z，局部核心大小a>0，实际末位BR需|R|/r≥|X_i|/2+|Y_i|≥a/2，拟分支末位BR需a/(r+1)≥|R|。合并r(r+1)≤2；r≥2不可信，r1迫Y_i为空。这不是一般多追随者定理。

原探索末段还有不同公共奖励块的局部障碍：当惩罚行动的局部核心贡献相同、其余区别只为等大正奖励块的最终份额，末位按奖励密度选择。以已覆盖次数分别3和1为例，最后加入本人后份额分别R/4和R/2，R>0时前者严格较小。**此数式是本资源对原文字机制的直接条件化展开**，不是未读程序结果。若另有核心负载差、不同奖励规模/重叠或额外客户，不能用它排除；原稿也没有完成一般升级构造。

## 八人纯菜单稿：有限证书的逻辑与软件身份

固定其32客户/8主题/8玩家输入与真实根列。每列在根另一块q0=(2,1,1,0)，额外D查询37/10>u13/4，actualW=OPT32；匹配混合值851/280<u，只反纯列，不由这个输入反mixed/weak/half。现在一般FM另有真正零根银行反例，不能因此把本稿的局部非反驳表述误写成现行FM仍OPEN。

原MD描述DAG schema为CA_COMPLETE_SPE_DAG_v1，内含原instance、root ID、八根目标及nodes；节点counts/target/action/children。每条合法动作边加对应一次计数、深度增1；指定动作孩子target等于父；叶depth8且counts=target；每个非叶对每个合法b检查U_a(parenttarget)≥U_b(child_b.target)。从叶向根归纳给每子博弈SPE，任意有序历史沿其动作边行走，合并DAG状态是本构造的合法策略选择，不把一般问题限制为匿名历史。

原文报告13872节点/6435叶/59496含自身比较，展开2396745个有序决策历史；59496=8(13872−6435)只是这个报告的算术一致性，不是当前读遍原节点。所有根列、单位客户表、两块无一般直和、插入+1与原根不删，以及两组混合原始/对偶公式已完整保在现账本。HD不把只读MD语义冒成原JSON/代码实读或原CLI PASS。

| 原文文件及角色 | 已实际知道与未取得的边界 |
| --- | --- |
| `counterexample/pure_menu_two_block_dag.json` | 原稿称其保完整输入和策略数据；HD未取得全文实读，不能由schema或节点数代替全数据。 |
| `counterexample/verify_pure_menu_dag.py` | 原文称直接展开单位客户，不导规范model/SPE oracle/证书核验器，核可达节点、全边与全比较；描述默认仅stdout、`--output 新路径`排他创建、已有输出不覆盖。这里只保作者软件合同，源码/实际parser/cwd/默认输入和依赖未在HD确认或执行。 |
| `counterexample/pure_menu_two_block_audit.json` | 原文称保根数值与完整矩阵，是发现方直接核验的冻结输出；未新读取其全部字段，不作当前输出字节绑定。 |
| `parent/verify_two_block_dag.py` 及 `two_block_dag_independent_audit.json` | 原文称父独立单位客户重构得到同节点/叶/比较和松弛0，以及有理矩阵匹配；HD未取得/运行，不把另一份README引用算独立再审。 |
| `independent_pushforward/two_block_pure_menu_review.md` | 原文称另一研究员用整数集合BI、自造DAG/单位客户核验，不导发现实现；此引用文稿不在本批已全文实读材料中，保源称身份不加认证范围。 |
| `counterexample/build_pure_menu_dag.py` | 原文称发现/重建器会导规范集合BI，不属于独立核验链；不能把发现solver正确性当有限DAG验证前提，也不因此否定经独立比较证明的条件逻辑。 |

原稿“在仓库根运行核验器”的文字属于当时复验说明；当前未读代码不确认可用的具体执行命令。HD没有补运行、没有覆盖冻结原DAG或报告，也没有把原工具的数学核验方式升级为已交付canonical算法/复杂度认证。

## 接续、原件与处置

[五原件清单](../../../../tools/evidence/independent-profit-isolation-and-menu-proofs/source-manifest.json)保真实字节、两个冻结来源、GS首次实际读的原路径与当前SHA。efb的不同完整消元、4fa的奖励密度未完成机制、660的程序/输出角色在本资源自足补保；c9与73的完整数学已由原正式对象覆盖，duplicate另明实际读段、先验身份和准确去向。

新正式对象只有这一个资源，不新建重复利润/信用/隔离/菜单定理。旧成功数学/CLI/BI/LP审计重跑为0，新增数学程序0；当前证明/原作者有限报告/未读数据/未完成构造分别标记，不额外done引用脚本/JSON或独审稿，不作第三阶段图导入。
'''
put(P,front+body);js(E/'formal-resource-manifest.json',[{'path':P,'bytes':(S/P).stat().st_size,'sha256':sha((S/P).read_bytes())}])
related=[]
for i in ['5807ac87276a9bc80ce0','0efa8da260f6c6ee8015','bdd683848aab07c77142']:
 x=next(x for x in previous if x['id']==i);v=inv[i];b=(GS/x['preserved_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'];q=E/'related'/i/x['path'];cp(GS/x['preserved_path'],q);related.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'reading':'GS full mathematical reading, current sameSHA dependency comparison only; already GY primary disposition not repeated'})
js(E/'related-source-manifest.json',related)
prefix='research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/'
refs=[]
for name in ['counterexample/pure_menu_two_block_dag.json','counterexample/verify_pure_menu_dag.py','counterexample/pure_menu_two_block_audit.json','parent/verify_two_block_dag.py','parent/two_block_dag_independent_audit.json','independent_pushforward/two_block_pure_menu_review.md','counterexample/build_pure_menu_dag.py']:
 refs.append({'original_referenced_path':prefix+name,'inventory_records':[v for v in inv.values() if v['path']==prefix+name],'read_status':'inventory metadata and actual9014Bsource statement only; rawblob/code/JSON/review not exported/fullread or executed in HD, no claim of failed availability attempt'})
js(E/'unread-original-certificate-and-program-reference-identities.json',refs)
coverage=[
{'id':IDS[0],'disposition':'integrated','targets':[P2,P],'units':['object alln>=4/x=n-2/unittypes/exactF notcoverage/ownfullSPEreviewnotclaimed','root historicalunread-discovery prior/sourceindependentmethod','strict eliminateA missing specialvsordinary and(4n-7)/6<x','strict removeleafduplicates thenextraB withallintegerprofiles','P0/P1/n4ties/everycase Fexact','Bellman2 n>=5false andalpha17/6bound/globalmargin2(n-1)','15501n4to8oldfinitecountreport notuniversalproof ornewcodeexecution']},
{'id':IDS[1],'disposition':'duplicate','targets':[P2,P],'units':['originalallbigcompleteorderedhistory proof andtruejointdeviations','allk exactprofitoptimizerepeatedsingletons/eliminatebyslots/hnbounds','anyfinitealpha arbitrarylargen versusprior squaren selectionequivalent','n3 explicit5/2/n>=3fail coefficient2','tailh-2/rootdebth-3/globalmargin1/notF<=2Porhalfrefuted','sameinstanceindependentf/twozeroaxes/unboundednproof andn16alternative-7/16/-19/30bounds','internalblindreview identity notnewperson/finiteauditnotgeneralproof']},
{'id':IDS[2],'disposition':'duplicate','targets':[P4,P],'units':['firststatement-onlyreconstruction thenread discovery/oldinternalrole notnewblind','samevrealbranches/oldprefix/actions fixed/extraNcatalogues','R1d<=x<=2d andy<=d-x/2<=x/2','threeactualcomparisons notusingcurrentA-IC orBbranchlastA-BR','OPTcoversentireN andnonuniformpointwiseequality d even','k1no derangement/d0allzero/poolgeometryhypotheses allessential','realSPE existence notfrom necessarypoint; escapes otherbranches retained']},
{'id':IDS[3],'disposition':'integrated','targets':[P4,P],'units':['Edefs vi/bi/dQ realbranches/T>=0/Delta signed/S>=kd-E','modifiedwelfarebound andhalfnecessaryS/Ethreshold notpaidbysystem','repeatedrD/rB localcore a inequalities andr(r+1)<=2/Yzero r1','differentr-tailarchitecture notmixm=k+1 bound','publicrewardblocksalonefinaldensity mechanism commoncore/equalblocks/oncevstriple','directconditionedR/4<R/2 rendering ofwordargument notauthorcomputednewinput','no genericheterogeneousrewardno-go/no validcompleteSPEcounter/nohalffromfailedattempt']},
{'id':IDS[4],'disposition':'integrated','targets':[P1,P],'units':['exactpurefullrootclaim/b+1/queryindependent/oldrootnotdeleted','all32unitclients/2blockcounts/qT/rootpaymenu/actualpath/u/W/OPT','DAGschema/root/nodefields/fullactions/targetmatching/leafdepth/orderedhistoryexpansion proof','13872/6435/59496/2396745 authorreport notrawreadcurrentPASS','37/10percolumnotherblock andcorrect137/60/359/120 olddenominatorrepair','uniformD safe123/40 andexact851/280 rawdual rationalprofiles allinpriorledger','sourceprogramroles directvsparent independentvsotherintegerBInewDAGvsdiscoverybuilder','defaultstdout/--outputexclusive describedonlynotcurrentparser/cwd/actualCLIcert','authorrelativepaths/citedrawJSON/code/unreadreview noavailabilityfailedclaim','source-local nonrefutationofmixed notcurrentgeneralFMOPEN']}
]
js(E/'semantic-coverage-map.json',coverage)
scope={'primary_sources':5,'primary_bytes':sum(x['size'] for x in primary),'primary_lines':sum(x['lines'] for x in primary),'first_actual_read':'GS complete original text/math reading of all5 as necessary related; HD exactsamebyte reuse and everysection semantic comparison, not fictional reread/blindreview','primary_dispositions':{'integrated':3,'duplicate':2},'new_formals':1,'new_mathematical_theorems_or_counterexamples':0,'unique_new_resources':['independent elimination order A then repeated leaves then extraB withstrict bounds','conditional equalreward density argument and architecture-number separation','explicit program/output/review/discovery roles and MD-onlyCLI contract'],'already_covered_mathematics':'profit/infiniteallbig/sharedf/isolation/puremenu/mixedmatching statements andcoreproofs reused with precise sourceidentity; alternateequivalentbounds do not create another theorem','current_formal_contexts':len(contexts),'related_original_mathematical_sources':len(related),'related_extra_done':0,'new_original_CLI_calls':0,'new_math_program_runs':0,'old_success_replays':0,'new_SPE_LP_BI_random_runs':0,'new_local_blob_helper_calls':0,'network_or_lazy_fetch':0,'shared_Git_writes':0,'claim_done_checkpoint_show_calls':0,'real_account_board_auth_operations':0,'phase3_graph_import':0,'raw_claim_ids':len(claim['ids']),'primary_claim_intersection':IDS,'claim_projection_performed':False,'source_programs_inputs_reports_status':'all7referencedDAG/program/report/anotherreview paths only inventorymetadata and fullMDsource descriptions; no rawblob export/codeorJSONfullread/currentCLIrun, and no claim that they were unavailable','new_formula_inference':'R/4<R/2 is explicit conditional expansion of oldcommoncore/equalreward finaldensity prose; mathematicalderivation not a programrun or a newfullSPEinstance','old_internal_review_identity':'efb/newprofit optimization alone notoldfamilyfullSPEreaudit; c9fullallbigSPE+F independentreconstruction; 73statement-onlythencomparedgeometricproof; none made newcurrentreviewer','GS_target_publication':'Root previously explicitly reported actualGSbody50b4cd81ada9c439a7ace88af8911738188fb998 anddoneff40e003c09886c872568e0cdddf29f6c457f176; HD independently checks actual currentfullbytes against that accepted packet','GY_format_recovery':'Root reported applied separately to two oldpages; this HD packet neither rewrites GY originaldelivery/proposal status nor touches those sharedtargets','derived_builder_calls':1,'derived_builder_failures':0}
assert scope['primary_bytes']==24864;js(E/'read-scope-and-evidence-status.json',scope)
notes=[
('3417B独审于GS已全文数学读，HD核同SHA逐段比较对象/全整数规范化/所有严格损失界/有限回归和审查先验，不虚称新第一读。','结论在GS利润对象已有，但现有正文用b0/b>=1消元；本稿不同的先消A两分支、再消叶重复/多B的完整严格步骤此前未自足保留，现资源逐式写全，原族全历史SPE仍引用已实读规范证明。','integrated：补一套有用独立证明和准确有限/普遍角色，不造第二个利润定理或反例族，n4边界/17/6/整体half正裕量完整保，0复跑15501旧回归。'),
('3802B无界独审GS已实际全文读，HD字节及SHA核同，完整策略/全部n精确F/无界α/尾信用/共享函数末段逐项对照。','同一all-big与同一f冲突已经自足；任意充分大n与现页平方n是同一量词，独审-7/16/-19/30等价界和先读原始类型未读发现稿的历史身份精确纳资源，不新增审稿人数。','duplicate：全部数学对象/关键证明已有准确目标，不按同标题自动判重，不把n2to8有限回归冒任意n证明，不重跑旧程序，实例族旧有不认新颖性。'),
('4353B隔离独审GS已全部实读，HD核同字节逐段比对三个真实比较、R1点态界、非均匀等号及假设清单/边界。','现隔离对象完整保主证明；资源明确它没有使用当前改A的IC或另一枝最后A自身BR，但局部池/全N覆盖/实际D/两个真实分支不能删；必要条件不证明完整策略存在。','duplicate：同一条件架构定理与证明完整去向已在现页，保k1/d0/正偶等号与可逃逸模型；独立盲重构是原历史不变成新外审。'),
('4278B逃逸探索GS全文已读，HD同SHA复用并核vi/bi/dQ/E每符号、两个结构的玩家数及全部失败/未完成尾段。','E定量界和重复追随者冲突已有；此前只概述异质奖励待证，现资源完整保存共同核心/等奖励块最终密度的局部阻碍，以明确条件R/4<R/2展开文字，不当实际程序run或一般no-go。','integrated：未完成构造仍可接续，E必要非充分/Delta可负/r尾方案不机械套k+1界/额外核心或异质奖励未被排除；不以这次失败证half。'),
('9014B纯菜单正文GS已全数学实读，HD核同SHA对照全部客户/根列/完整DAG证明逻辑/实际路径/两组混合数值/最后软件复验段。','现账本已保完整数学；本资源补发现器与直接单位核验、父独立核验/冻结报告、另一研究员重造DAG的角色，以及默认stdout/--output排他创建仅属作者MD描述。七引用文件只inventory身份，没有新读原DAG/code/JSON或引用review。','integrated：全部独有资源用途准确自足保，原13872/6435/59496/2396745报告不升级当前有限认证或canonical实现，旧插入分母纠错不复活，纯/混合/自由背景/half不同范围；0新原CLI或BI。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 实际多组原claim pushed/synced完整保留，仅本5交集/owner/sourceSHA核齐。','comparison_note':b,'decision_note':c,'disposition':x['disposition'],'targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(E/'README.md',r'''# 独立审查与未完成惩罚/菜单资源

HD5原24864B均GS已真全文读，核同SHA逐段与四当前正式数学正文全字节比较；3integrated+2duplicate，1新资源0新定理。严格保独审另一消元、审查先验/等价数值界、隔离真正使用的三比较、逃逸E与等奖励密度局部障碍、八人证书的各程序/报告/另一review角色。

原DAG/code/rawJSON/另一引用review只核inventory身份与MD来源描述，不冒全文实读/失败可用性测试/当前原CLI认证；默认stdout和--output排他创建仅保原作者合同。0原CLI/数学/SPE/LP/BI/随机/旧成功/helper/network/sharedGit/账号行为。已有GS定理对象不重复生成，GY修复原包不改。

完整多组claim字节保留，仅5交集/owner/sourceSHA写receipt。白名单所有目标路径/字节/SHA精确，Root先pushed正文依赖再done，不作第三阶段图导入或凭格式计数证明数学。
''')
put(W/'relation-review.md',r'''# 阶段二关系

efb是同一利润F最优值的另一套严格消元证明，不同顺序的替代论证保为资源，不新冠同一定理；c9同all-big与信用冲突两族证明可duplicate，原等价数值界和审查先验保准确。

73重构同隔离三比较，未用的IC不伪列依赖，真实分支几何却不能删；4fa撤隔离的E和重复尾架构与等奖励密度各为不同条件合同，局部失败不反一般half或全部异质设计。

660完整DAG的深度归纳逻辑与未读有限证书数据区分；发现solver、直接核验、父重构、另一BI重造与各冻结报告不是同一种证据。作者CLI说明不变当前可执行认证，纯反例的混合安全不使现行FM一般仍OPEN。

无新数学程序或旧成功重跑，无外审/新颖性或canonical实现升级。不重复done related或引用源；不导phase3旧图、不为连通造边。
''')
nextids=['d51be5e16b588a9c5b11','be35ac9e54f0b79a4117','fb08b92429fc3b32a751','729c23b4e89e761e0043','aa188e3cd37022c8cb39'];nextrows=[]
for i in nextids:
 x=next(x for x in previous if x['id']==i);b=(GS/x['preserved_path']).read_bytes();assert sha(b)==inv[i]['sha256'] and len(b)==inv[i]['size'];q=REPO/'cleanup/progress'/f'{i}.json';pr=json.loads(q.read_text()) if q.exists() else None
 if pr is None:nextrows.append({**inv[i],'local_path':str(GS/x['preserved_path']),'progress_observed':None,'read_status':'GS entire original math text actually read, honest sameSHA reuse possible after newactualclaim; no rawreferencedcode/JSON certification'})
js(W/'next-candidates.json',nextrows)
cp(Path(__file__),E/'build_delivery.py')
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
def tex_balanced(s,left,right):
 def count(delim):return sum(ord(s[i])==92 and s[i+1]==delim and (i==0 or ord(s[i-1])!=92) for i in range(len(s)-1))
 return count(left)==count(right)
assert tex_balanced(chr(92)+'[x'+chr(92)+']','[',']') and not tex_balanced(chr(92)+'[x','[',']') and tex_balanced(chr(92)*2+'[2pt]','[',']')
for x in primary+related:
 b=(S/x['preserved_path']).read_bytes();ck('exactsource sizeSHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('exactsource blobSHA1 '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('unprojected realclaim preserved',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes());ck('actualsubsetowner gate',set(IDS)&set(claim['ids'])==set(IDS) and all(x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[x['id']]['sha256'] for x in owners));ck('actualclaim pushedsynced',claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and claim['local_sync']['remote_tip']==claim['remote_tip'])
for x in contexts:ck('actualcurrent/prior contextwholebytes '+x['path'],len((S/x['snapshot']).read_bytes())==x['bytes'] and sha((S/x['snapshot']).read_bytes())==x['sha256'] and (S/x['snapshot']).read_bytes()==(REPO/x['path']).read_bytes())
t=(S/P).read_text();ck('flatMATEK',all(re.search('^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']));ck('formal nonLF C0zero',not any(ord(c)<32 and c!='\n' for c in t));ck('formal trailingwhitespacezero',all(l==l.rstrip() for l in t.splitlines()));ck('TeXactualdelimiters balanced',tex_balanced(t,'[',']') and tex_balanced(t,'(',')'));links=[]
for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
 if '://' in dest or dest.startswith('#'):continue
 n=posixpath.normpath(str(Path(P).parent/dest.split('#',1)[0]));q=S/n if (S/n).exists() else REPO/n;ck('actual relative link '+dest,q.exists());links.append({'source':P,'destination':dest,'resolved':n,'bytes':q.stat().st_size,'sha256':sha(q.read_bytes())})
js(E/'formal-link-check.json',links)
ck('strict alternativeelimination allfoursteps',all(x in t for x in ['第一步，消去A','第二步，消去叶重复','第三步，B至多一次','第四步，只剩两类','(4n−7)/6<x','n4平局']));ck('duplicate bounds anddependencyminimum',all(x in t for x in ['−7/16','−19/30','没有使用','当前玩家改A_i的IC']));ck('conditional rewardprose inference notnewrun',all(x in t for x in ['R/4和R/2','直接条件化展开','不是一般多追随者定理']));ck('DAGcode/report notnewcertified',all(x in t for x in ['59496','2396745','默认仅stdout','源码/实际parser/cwd/默认输入和依赖未在HD确认','引用文稿不在本批已全文实读材料']));ck('all7unreadreferences explicit',len(refs)==7 and all('no claim of failed' in x['read_status'] for x in refs))
ck('5complete receipts 3integrated2duplicate',len(receipts)==5 and {x['id'] for x in receipts}==set(IDS) and sum(x['disposition']=='integrated' for x in receipts)==3 and sum(x['disposition']=='duplicate' for x in receipts)==2)
for x in receipts:ck('semanticreceipt complete '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']) and all((S/p).exists() or (REPO/p).exists() for p in x['targets']))
ck('onlyone newformal object',list((S/'archives').rglob('*.md'))==[S/P]);ck('allnewmathCLIoldreplayszero',all(scope[k]==0 for k in ['new_original_CLI_calls','new_math_program_runs','old_success_replays','new_SPE_LP_BI_random_runs','new_local_blob_helper_calls','network_or_lazy_fetch','shared_Git_writes']))
for x in nextrows:ck('actualnextavailable '+x['id'],Path(x['local_path']).exists() and sha(Path(x['local_path']).read_bytes())==x['sha256'] and x['progress_observed'] is None)
obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:u=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen=any('/'+z+'/' in rel for z in ['original','related','context']);bad=[i+1 for i,l in enumerate(u.splitlines()) if l!=l.rstrip()];c0=[{'offset':i,'code':ord(c)} for i,c in enumerate(u) if ord(c)<32 and c!='\n']
 if bad or c0:obs.append({'path':rel,'frozen':frozen,'trailing_lines':bad,'nonLF_C0':c0})
ck('all derived C0andwhitespacezero',not any(not x['frozen'] for x in obs));js(E/'transport-format-observations.json',{'observed':obs,'original_related_context_frozen_bytes_unchanged':True})
put(W/'delivery.md',f'''# HD交付

五primary24864B/{scope['primary_lines']}行GS已实际related全文实读，HD核同SHA并逐独有段/实际证明比较；3integrated+2duplicate、1资源、0新定理。不同严格消元/条件等奖励密度/证书各代码角色补全，其余完整数学按精确现目标duplicate，不按字数/标题/数量判断。

真实原{len(claim['ids'])}ids pushed/synced {claim['remote_tip']} 原字节保，不作五ID伪投影；本5交集、owner/sourceSHA及已推GS四数学正文逐byte核齐。0新数学CLI/SPE/LP/BI/随机/旧成功/helper/network/sharedGit/账号行为，原DAG/code/rawreport/另一review未取得实读，不冒当前认证或失败可用性。

Root先checkpoint正文依赖再done。下一{len(nextrows)}件本地原件GS已全数学读，可诚实复用但需Root新actualclaim；GY原冻结包和其proposal-only事实不改，Root独立应用修复不倒填本批。
''')
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'relative_links':len(links),'formal_nonLF_C0':0,'formal_trailing_whitespace':0,'scope':'source/owner/rawclaim/currenttargets/coverage/receipt/links/format/transport checks only; actualmath through full source reading and analytical reconstruction, no automatic mathematical certification'})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':24864,'primary_lines':scope['primary_lines'],'new_formals':1,'formal_bytes':(S/P).stat().st_size,'receipts':5,'dispositions':{'integrated':3,'duplicate':2},'checks':len(checks),'relative_links':len(links),'new_math_runs':0,'raw_claim_ids':len(claim['ids']),'claim_tip':claim['remote_tip'],'next_candidates':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
