from pathlib import Path
import json,hashlib,re,posixpath
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';GS=C/'r3-d22-frontier-ledger-primary';S=C/'r3-stationary-query-and-replicated-menu-audits';E=Path('tools/evidence/stationary-query-and-replicated-menu-audits');W=Path('cleanup/workspaces/Boss4/r3-stationary-query-and-replicated-menu-audits-next')
IDS=['d51be5e16b588a9c5b11','be35ac9e54f0b79a4117','fb08b92429fc3b32a751','729c23b4e89e761e0043','aa188e3cd37022c8cb39']
P='archives/customer-attraction/state/资源/平稳查询与复制菜单的有限证据合同--资源.md';P1='archives/customer-attraction/state/资源/真实分支十项合同与菜单可实现性账本--资源.md';PI='archives/customer-attraction/state/引理/完整槽插入税与跨角色价格恒等式--引理.md';PA='archives/customer-attraction/state/算法/可信续局菜单与完整策略重构--算法.md';PO='archives/customer-attraction/state/反例/唯一最优组合的全遗漏支付--反例.md';PE='archives/customer-attraction/state/等价/两份最优遗漏输入的二人收益等价--等价.md'
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
claimpath=R/'boss4-r3-next-hf-claim.json'
if not claimpath.exists():raise SystemExit('HF actual capture absent, no primaryreceipt generated')
claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(IDS)<=set(claim['ids'])
previous=json.loads((GS/'tools/evidence/d22-frontier-ledger-primary/related-source-manifest.json').read_text());primary=[];owners=[]
for i in IDS:
 x=next(x for x in previous if x['id']==i);v=inv[i];b=(GS/x['preserved_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];owner=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==v['sha256'];owners.append(owner);q=E/'original'/i/x['path'];cp(GS/x['preserved_path'],q);primary.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'headings':[l for l in b.decode().splitlines() if l.startswith('#')],'read_mode':'GS actual full original mathematical reading; HF exactsamebyte/section semantic reuse, not a fictional first read or rerun','prior_actual_snapshot':str(GS/x['preserved_path'])})
assert sum(x['size'] for x in primary)==26149
js(E/'source-manifest.json',primary);cp(claimpath,E/'actual-unprojected-claim-receipt.json');js(E/'actual-primary-ownership-snapshot.json',owners)
contexts=[]
for p in [P1,PI,PA,PO,PE]:
 b=(REPO/p).read_bytes();prior=GS/p if (GS/p).exists() else GS/'tools/evidence/d22-frontier-ledger-primary/context'/p
 if p in [P1,PO,PE]:assert b==prior.read_bytes()
 q=E/'context'/p;cp(REPO/p,q);contexts.append({'path':p,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_mode':'HF actual entire current formal text read for definitions/proof-domain comparison' if p in [PI,PA] else 'GS actualfullmath/preparation reused after exact whole-byte identity','prior_snapshot':str(prior) if p in [P1,PO,PE] else None})
js(E/'context-manifest.json',contexts);cp(GS/'tools/evidence/d22-frontier-ledger-primary/read-scope-and-evidence-status.json',E/'actual-prior-GS-read-scope.json')
related=[];exports=[]
for mp in [C/'learning-hf-next-audit-inputs/local-export-manifest.json',C/'learning-hf-next-readable-mathematics/local-export-manifest.json']:
 m=json.loads(mp.read_text());cp(mp,E/mp.parent.name/'actual-local-export-manifest.json');exports.append(m)
 for x in m['rows']:
  v=inv[x['id']];b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'];q=E/'related'/x['id']/x['path'];cp(x['local_path'],q);related.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'read_mode':'HF actual first complete original text/mathematical reading, as related comparison and parent-authorized nextsource prework; no primaryreceipt or extra done','original_export_path':x['local_path']})
assert len(related)==5;js(E/'related-and-next-prework-source-manifest.json',related);js(E/'actual-missing-program-report-inventory.json',[inv[x['id']] for m in exports for x in m['missing']]);cp(C/'local_blob_export.py',E/'authorized-local-export-helper.py.txt')
front='---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in [('id','customer-attraction/stationary-query-and-replicated-menu-finite-evidence-contracts'),('kind','resource'),('type_tag','资源'),('title','平稳查询与复制菜单的有限证据合同'),('status','complete-source-review; conditional-matrix-and-local-proof-preserved; full-cuts-source-report-only'),('summary','明确6286核的平稳/查询手算与原全IC审计边界，保条件复制矩阵的meta-NE、六向量有限分类及整数缩放/编码范围；局部last-low与14类遗漏已覆盖者精确duplicate，0新数学程序。')])+'source_refs:\n'
for x in primary:
 for y in x['sources']:front+='  - '+json.dumps('source:'+y['commit']+':'+y['path'],ensure_ascii=False)+'\n'
front+='---\n\n# 平稳查询与复制菜单的有限证据合同\n\n'
body=r'''## 来源与共同模型

本批五稿4495/6490/6701/3104/5359B，共26149B，均GS实际全文读，HF核同SHA逐项比较。有限单位客户、共同有限非空目录、单位提供者、全部有序历史纯SPE，保空主题、重复和任意离轨平局。原码、完整动作JSON或全部数值报告不能由一篇MD的“独立审计通过”代读。

本页补自足的平稳/查询复核、条件矩阵meta-Nash与有限分类/程序范围，既有完整数学见[真实分支账本](../资源/真实分支十项合同与菜单可实现性账本--资源.md)。没有新增实例或另冠同一个定理。

## 6286客户：固定槽核可以手算，完整SPE审计不代跑

该三人、六主题例的21类单位客户、43节点完整规则、六根真实列及所有数值已保在现账本。原策略形式与旧348客户例相同但重数不同；发现输入文件名`stationary_348_diagnostic.json`中的348不表示本输入仍348客户。独审称只读取其中query2条目的mask/重数，以及`high_insertion_2cycle_348_exact.json`的完整动作表；这是当时独立性的来源说明，不是HF新读取那两份JSON。

六个强制根列为
\[
Z_0=(0,3,4),\ Z_1=(1,3,4),\ Z_2=(2,3,4),\quad
Z_3=(3,0,1),\ Z_4=(4,0,1),\ Z_5=(5,0,1).
\]
P_BA=count_A(Z_B)/3，是source到均匀**完整三槽**的核。由这六列直接解pP=p：只有列2会流入标签2，故p_2=p_2/3=0；同理p_5=0。其余方程为2p_0=2p_1=p_3+p_4、2p_3=2p_4=p_0+p_1，归一化给
\[
p=(1,1,0,1,1,0)/4.
\]
这是当前对给定菜单的解析重建；后续发现稿b97b201c7a5d2373db80也明写这个解法。源独审的rank(Pᵀ−I)=5为另一有限核验报告，不必借未读报告才能解该核；但此手算没有核原43节点的全部激励。

查询2涉及的七种mask为4:550、12:229、13:99、29:396、36:380、44:237、46:132。对四个正概率列0/1/3/4独立查询，各型的平均倒数分别1、5/8、5/12、5/16、1、5/8、5/12。因此直接有
\[
(Kp)_2=550+380+(229+237)\frac58+(99+132)\frac5{12}+396\frac5{16}
=\frac{5765}4.
\]
actual列Z0中root0收益也可逐型核：
\[
361+\frac{587}2+\frac{99}2+\frac{396}3+360+99+\frac{132}2+\frac{99}2
=\frac{2821}2.
\]
故查询超该实际根123/4。以上是给定输入/菜单的手算，0代码执行，不是重新认证完整SPE。全部258含自身/215真偏离、最小松弛0、其他根收益、OPT_3=5189等仍按原作者单位审计MD证据身份保存；actualW4514且half余3839，不由这个例否定half。

独审的其他query向量和纯列cap已完整在现账本。五个纯列0/1/2/3/5安全，故自由mixed在这个例甚至不必混；唯一stationary p不是meta最佳回复，因为transient query2价格高于其self平均C(p,p)=185785/192。单独“有stationary p”和“有对称meta-NE p”不能拼成同一个p；对固定这个P,K，甚至不存在同时stationary和meta-NE的p。此精确固定核合同的否定不排内生改变核的另一构造，也不说明一般stationary self strong-push已失败。

## 平稳预算的完整定义及两个不同核/输入

[完整槽恒等式](../引理/完整槽插入税与跨角色价格恒等式--引理.md)HF已全文实读。Q是完整r槽的列分布，n_x为一列负载，n'_x是独立同分布副本。零负载的下列分子项取0，定义
\[
\bar U_Q=\frac1r\mathbb E_Q\sum_x\frac{n_x}{b_x+n_x},\qquad
T_Q=\frac1r\mathbb E_Q\sum_x\frac{n_x}{(b_x+n_x)(b_x+1+n_x)},
\]
\[
\Gamma_Q=\frac1{2r}\sum_x\mathbb E\frac{(n_x-n'_x)^2}{(b_x+1+n_x)(b_x+1+n'_x)}\ge0.
\]
从列中均匀抽槽得到主题边际q_Q，再独立重抽竞争列，其额外查询价格为Ubar−T+Gamma。pP=p时q_Q=p，故C(p,p)=Ubar_p−T_p+Gamma_p。6286例原独审报告Ubar9149/6,T98063/144,Gamma71303/576，D2821/2；于是D−Ubar=−343/3而D−C=85031/192>0。平稳没有角色平均收益可交换性，Gamma也不支付外部query2。

零背景rUbar是**混合列的期望覆盖**，不是一个actual列的W；有过去时它只是剩余玩家总利润。不能把上面9149/6代成4514/3。该例的固定完整槽核与此前DY1274客户真实尾槽例不是同输入/同查询背景。对同一个策略r>1虽有P_full=(I+(r−1)P_tail)/r、两核stationary集合相同，仍不能将r槽查询分母换成r−1槽，或把两份客户重数/数值相混。

## 条件复制矩阵：meta-Nash也是条件对象

每个16客户块四主题A/B/C/D，类型A:2,BD:4,AC:6,CD:3,ABCD:1。n不交块、4n人；q0=(2,1,1,0)，qA=(2,0,1,1)，qB=(1,1,1,1)，qC=(1,0,2,1)，qD=(1,0,1,2)。条件菜单R_n要求根T_j后本块qT、其他全q0，含root共4n槽；必须由**同一**完整SPE同时实现，不能假设一般直和。

现账本保完整单块查询矩阵L及异块h，n≥3的精确minimax是M_n=37/10−17/(12n)。补清原稿的meta-NE：Q均匀各D列时，四query价依次
\[
71/30+5/(6n),\quad 11/5-2/(3n),\quad16/5-1/(4n),\quad M_n.
\]
n≥3时D为最大，支持内D全取等，所以在行玩家收益K_AB、列玩家收益K_BA的对称两人游戏中，p=Q=uniform(D_j)确为对称meta-Nash，尽管K本身不必对称。此游戏描述的是插入矩阵，不是原顺序子博弈。对任何其余对称meta-NE p，value=max_A(Kp)_A≥min_Q max_A(KQ)_A=M_n；因而若R4真实现，**所有**此类meta-NE值都>u13/4，而不只某个坏p。

R4条件值803/240、gap23/240；R3值581/180<u。n1纯A安全cap16/5，n2值851/280；不能将n≥3的D最大公式机械代到n2。若R4实现，均匀D也使pᵀKp=M4>u，反弱WP；但自由静态每块qB把全查询压到16/5<u，actualW=OPT64，因此不是half反例。

独立两块稿90b16a6fa71daf25a8fc本批首次实际全文读：其最优列Q(C_j)=1/14,Q(D_j)=3/7不仅给KQ最大851/280，支持C/D均达到该值，故Q自己也为对称meta-NE。匹配零和行对偶p(C_j)=2/7,p(D_j)=3/14是**不同**分布；不能把匹配行对偶与这个meta-NE混成一个p。原独审报告独立整数BI用LCM840枚举12870计数前缀/6435终局、重造13872节点DAG再由单位审计核7437决策节点/59496比较；还报告B根另一候选(2,1,0,1)|q0不可实现。这里新读的是4023B独审数学文本，不是其代码/DAG/两份结果；HD先前未取得该review的历史事实不覆写成当时已读。

早期纠错f325ca53c510560b1607与独立接口681138cd2e959bc26dcb也全文比过：qD中旧D收益13/4，完整四槽后额外D为137/60；两块uniform-D的C359/120，比u低31/120。原规范BI记录(q0,q0)不在root可实现集，早期尚未独立压缩证书；后来的独立两块报告另保其后时点。旧“弱/extra-one/FM仍OPEN”是当时状态；现在零根银行族已独立反一般合同，不可由本例未反驳推出当前真值仍OPEN。

## 六个单块终局及三块有限分类

6701B稿的单块根可实现集合明确为
\[
\mathcal Q=\{(1,0,1,2),(1,0,2,1),(1,1,2,0),
(2,0,0,2),(2,0,1,1),(2,1,1,0)\}.
\]
最后一项是q0。原报告称n=1,2,3的root终局恰为Q^n中至多一个q0，其数6/35/200=5^n+n5^(n−1)。依据为每个枚举终局逐块属于Q、无两个q0，且枚举总数等于所有这些组合数，故**在这三个n**两有限集合相等。任意n仍猜想；此处没有把计数公式当任意n可信嫁接定理。

集合值逆归纳的逻辑已在[可信菜单算法](../算法/可信续局菜单与完整策略重构--算法.md)完整解释，HF实际全文核过。对计数前缀s，R(s)是所有完整历史纯SPE可实现终局，F(s)=max_a min_(z∈R(s+e_a))U_a(z)。root实际行动a与真实终局z满足U_a(z)≥F(s)，故
\[
R(s)=\bigcup_a\{z\in R(s+e_a):U_a(z)\ge F(s)\}.
\]
反向由选中孩子用z、每个其他有序孩子独立选最坏子SPE拼合，证明充分；不是仅保必要IC的松弛。计数缓存保的是**所有终局集**，不同有序历史仍可选择不同可信目标。枚举终局全集不枚举每一完整动作图，有限采样更不等于穷尽所有策略，也无多项式运行时保证。

## 原程序的整数域与审查覆盖

| 作者原有限报告 | 准确范围及尚未覆盖的认证 |
| --- | --- |
| 三块12人收益缩放LCM(1,…,12)=27720 | 普通玩家分母≤12，可用整数比较无浮点容差；这是原MD说明，HF本地helper未得到C++ blob，未读源码或新编译。 |
| 三块额外查询缩放LCM(1,…,13)=360360 | 插入查询额外+1，不能用原12人分母代替；原指定查询p=uniformD诊断独立于root列抽样。 |
| 2704156计数状态、1352078终局、3207136保留outcomes | 是单份C++的状态/终局集合记录，不是完整有序策略数、独立实现数或当前新run。 |
| 四根A/B/C/D指定目标均不可实现；last-low截面192/384/192/192，全截面最小F=37/10>13/4 | 该全部截面结果只有一个实现。B截面含额外不相容root前缀，检查更大集合仍全严格阻断不会削弱所需相容子集结论。未独立逐截面重算。 |
| 两块回归和程序范围 | 原文称n2复现旧三个状态计数/四类可实现根，不能替代n3独立审核；C++刻意拒绝n>3以防四位计数编码越界。未读代码不把此描述当当前实际parser测试。 |
| 最小门槛代表与另一独立局部稿 | 只独立解析一个余3人代表，不覆盖全部截面或任意n；区别见下一节。 |

指定真实子树替代诊断只取p=uniformD,u13/4：A/B/C/D在root自身≤u下可选60/39/35/35终局，最大p插入101/30、283/90、197/60、551/180；B/D不足，不能产这套指定p的mixed反例。最大目标qT|qE|q0，qE=(1,1,2,0)，D插入16/5比q0少1/2。这些最大/可实现性仍是单C++报告，本批未读原5925B报告所有字段；不由诊断失败证一般FM或排所有p。

## last-low的量词与局部729稿的duplicate去向

目标z，L={a:z_a>0,U_a(z)≤u}。若每个与指定root前缀相容、s≤z且Σ_(a∈L)(z_a−s_a)=1的非终端截面都有F(s)>u，取真实路径最后一个L行动便矛盾。因此不可实现。该一般引理不自动给三块全截面门槛，更不证明任意n。

3104B局部稿729c23b4e89e761e0043的全部实质证明已在现账本完整：合法前缀ACD|AAB|AAB尚余3人；只要当前规定D0，其最终13/4，改D1后任意真两人SPE新增只可能{C1,C2},{C1,D2},{C2,D2}，该偏离者最坏37/10>13/4。其余两人首C1可保37/10，非C1/C2/D2即时≤13/4，首C2/首D2的末位BR也已穷尽。该证明不排先C1/C2的其他排序，不能替代全部截面。原`verify_last_low_witness.py`称展开48单位客户、每首动作枚举12末动作、用Fraction且不导solver；HF本地blob未取到，不冒实际代码读/执行。数学文本证明完整，原实现边界另记，故该主稿按准确目标duplicate。

## 14类遗漏原稿：另一个完整duplicate身份

5359B aa188e3cd37022c8cb39的14兴趣类型与D22回复(B,R,R,R,S,R)在现账本有独立原件身份；当前[唯一最优遗漏族](../反例/唯一最优组合的全遗漏支付--反例.md)用12类型和(B,S,R,S,S,R)，[两输入等价](../等价/两份最优遗漏输入的二人收益等价--等价.md)已保共同大小/两两交集及三人不等价。B/Q处R-S是合法平局差，不能据“同证书”称客户表/selector/字节全同。

全部7节点/42比较/21对覆盖已按这些明确定义表完整覆盖；TQ唯一OPT38，actualAB为W35，交集2/遗漏36/实际独有33，half余32。保护价格B_D(16)=4>3是另由本例遗漏集每主题至多18、总36和T/Q各权1达到证明，不能仅以一般两两交集相同就断言所有高阶保护价格相同。原发现/父审计不新读或运行、原优化线索不认证最小性。此源全部独有数学与历史去向已保，准确duplicate，不新造一个二人反例。

## 实际读取、缺失边界与接续

[五主源](../../../../tools/evidence/stationary-query-and-replicated-menu-audits/source-manifest.json)保GS首读与HF同字节复用；[五份相关及下一批预读原件](../../../../tools/evidence/stationary-query-and-replicated-menu-audits/related-and-next-prework-source-manifest.json)HF实际全文首次读，尚不对它们写primary receipt。三种单块/多块/局部/平稳/遗漏输入和矩阵的域不互换。

两次安全本地helper共9个ID尝试，5份MD齐、4程序/报告本地缺blob；缺失不重试/不network。它们是3ea438c35454a47d226d、b94a4e2caf2abbfd0854、53a06d4d1ae0ca89c85e、e37e092b132faffbe938，原manifest保留，不宣称全局或别缓存永久不存在。当前新增的是给定六列的平稳解、query2七型和root0八型手算及文本证明比较；新数学**程序**、原CLI、LP/BI/随机/旧成功重跑全0。来源历史独审不新增外审或新颖性、canonical实现认证，不导第三阶段图。
'''
put(P,front+body);js(E/'formal-resource-manifest.json',[{'path':P,'bytes':(S/P).stat().st_size,'sha256':sha((S/P).read_bytes())}])
coverage=[
{'id':IDS[0],'disposition':'integrated','targets':[P1,PI,P],'units':['6286unitmasks/43nodepolicy all258/215 originalreportedSPE/OPT/W scope','discoveryinput query2 andold348filenames not348clientidentity','all6realcolumns/sourcepayvector/full3slotkernelnotDY1274tailinput','uniqueπ givenmenu handsolve p2=p5=0/fourcoordinates equal distinctfromoriginalrank5report','query2sevenmasks andactualroot0eightmasks exacthand sums/123/4 notnewprogram','C/D selfpositive/notmetaNE/transientquery/fivesafepurecolumns/freeFMnotrefuted','Ubar/T/Gamma definitions actualfinitecolumns/zero convention/expectedWnotoneactualW','sourceindependentauditprogram/reportroles no code/rawJSON reread or newCLI']},
{'id':IDS[1],'disposition':'integrated','targets':[P1,P],'units':['conditionalRn allcustomerblocks/realSPE rootgluing notdirectsum','completeL/hmatrix andalln>=3 matchingoriginaldual proof alreadyinledger','conditionaluniformD metaNE andallrelevantmetaNEvalue>=M notsequentialBR','n1/n2range notn>=3/Dhighest formula misuse','n4firstgap803/240/23/240/staticfreeqBcap andW=OPTnothalf','n3truecontinuation substitute diagnostics A/B/C/Dcounts/maxvalues/qE withBIrole','underlying2blockindependentMDnowfullreadbutnotitsrawcertification/earlywrongdenominatorrevocation']},
{'id':IDS[2],'disposition':'integrated','targets':[P1,PA,P],'units':['general lastlow lemma fullL/compatiblecut/strictF andproofusinglastLaction','setvaluedBI equality necessary+sufficient/alloutcomesnotonecountselector/fullorderedhistorygluing','all6Qvectors/rootfiniten1to3 exactclassification andcardinalityproof notarbitraryn','n3integerpay27720/extraquery360360/tolerancefree sourcecontract','2704156states/1352078leaves/3207136outcomes/root200andfourcutcounts/min37/10','Bcut largerincompatibleprefixsuperset logic valid','singleC++fullcuts/n2regressionnotn3independence/n>3reject4bitencoding','one3remaininglocalreviewnotallcuts/alternativeuniformDdiagnosticnotallp','C++and5925reportactuallylocalmissing no retry/no currentexecutionorrawfieldreview']},
{'id':IDS[3],'disposition':'duplicate','targets':[P1,P],'units':['legal9slotprefix/48unitclients/3remaining/onlycurrentD0 claimnotallorders','deviationD1 fullinsertiontable andtrue2personreplyclassification','C1guarantee37/10/otherthanC1C2D2 immediate<=13/4','lastBR C2/D2 pairs/allpossibleoutcomes subset3sets/earlyD1pay37/10or21/4','oneprefixnotfullthreeblockcounterfamily proof','originalstandardlibraryFractionprogramrole only/localmissingblob notreadornewrun']},
{'id':IDS[4],'disposition':'duplicate','targets':[PO,PE,P1,P],'units':['14rawunittypes/D22selector BRRR SR all7nodepaytable/42 comparisons','all21theme-paircovercounts/repeats/uniqueTQ optimum38/W35/intersection2/omission36/net3/half32','BDmaxformula clippedcoverage min18tau36/v16/attainedbyTQ equals4>3','auxexistoptimalomission bridge nothalf orNET/aggregate failure','D22andR171 sources same2player objectbut14versus12input andB/Q R/Sselector differences','sourceownroot/authoraudits notimportcanonical solver vsdiscoveryoptimizationrole no newcode/JSONreading','no externalnovelty/minimality orcurrentuniversalproofstateupgrade']}
]
js(E/'semantic-coverage-map.json',coverage)
scope={'primary_sources':5,'primary_bytes':sum(x['size'] for x in primary),'primary_lines':sum(x['lines'] for x in primary),'primary_first_full_read':'GS actual entire5original mathematical text; HF wholebyteSHA andeverysection comparison reusesthat actual reading, not another first read','dispositions':{'integrated':3,'duplicate':2},'new_formals':1,'new_named_theorems_or_instances':0,'related_next_original_sources':5,'related_next_bytes':sum(x['size'] for x in related),'related_next_first_full_read':'HF actual full original texts; parent explicitly authorized next5 pre-read/independentdraft beforeclaim; related/prework only no primarydone','current_formal_contexts':len(contexts),'HF_actual_full_new_formal_reads':[PI,PA],'other_formal_read_reuse':'GS actual full source/derivation after currentexactbytecomparison, not quantity-driven repeatedread','new_hand_analytic_component_checks':['given6rootcolumns uniqueπ solved withoutmatrixprogram','query2sevenmask manualFractional sums5765/4','actualroot0eightmask manualsum2821/2'],'full_IC_check_scope':'258/215allICandOPT/rawrank originallyreported byMD; no newfullSPEcertificateorrawcode/reports read','new_math_program_runs':0,'new_original_CLI_calls':0,'old_success_replays':0,'new_LP_BI_random_or_SPE_programs':0,'local_helper_calls':2,'local_blob_attempts':9,'local_exports':5,'local_missing_blobs':4,'missing_ids':['3ea438c35454a47d226d','b94a4e2caf2abbfd0854','53a06d4d1ae0ca89c85e','e37e092b132faffbe938'],'missing_retry_calls':0,'source_programs_acquired_or_executed':0,'network_or_lazy_fetch':0,'shared_Git_writes':0,'claim_done_checkpoint_show_calls':0,'real_board_account_auth_calls':0,'phase3_graph_import':0,'raw_claim_ids':len(claim['ids']),'primary_claim_intersection':IDS,'claim_projection_performed':False,'historical_source_status_corrections':'earlyweak/FM/extraOPEN notcurrentuniversalstate; existingzero-root bank countermodel separate from6286or2block nonrefutation','derived_builder_calls':1,'derived_builder_failures':0}
assert scope['primary_bytes']==26149;js(E/'read-scope-and-evidence-status.json',scope)
notes=[
('4495B独审GS已全部数学全文读，HF核同SHA逐段对21类型/43策略/六菜单/平稳唯一性/完整Kp与预算/各纯列/证据代码角色，不虚称新第一读。','全部例数已在GS账本；HF全文核插入税正式定义并新补给定菜单的p2=p5=0四项均等、query2七型和root0八型手算，明确它们不代全258IC/OPT/rank的原代码审计。新读发现原稿同样有解析π解，不称新颖性。','integrated：自足资源补Γ/预算的原定义、固定核/尾核/不同客户输入和stationary非metaNE范围；actualW与混合期望覆盖分开，0新原数学程序或证书认证，6286失败只指定构造。'),
('6490B条件复制菜单全文GS已实读，HF同SHA逐节对输入/全矩阵/一般n匹配/首n4阈值/条件假设/替代真实子树诊断与程序角色。','现账本保主要解析，新资源补uniformD作为条件对称metaNE和所有相关metaNE值下界，并分n2最优列Q也是metaNE而匹配行对偶p不同；新读两块独审文本不作原DAG或机器核验。','integrated：不假设一般直和，条件n4矩阵不造完整SPE反例/half反例；保自由静态qB安全和n3指定p诊断失败只一方向，不由本例不反驳写现行FM仍OPEN。'),
('6701B可信菜单/lastlow正文GS已全部数学读，HF核同SHA逐式对引理、整数BI/统计/全截面/替代诊断、全部六Q及后续猜想、编译复验范围。','新资源明确原账本未列的六Q向量、LCM27720普通收益/360360额外插入、四位计数编码n>3拒绝；当前可信菜单算法HF全文核必要/充分及有序子树拼合，不能将单实现所有数值冒独立全截面审核。','integrated：单C++三块有限排除与一个局部独审分层，n1to3分类不外推全n。原C++/5925JSON这次首次本地helper缺blob并不重试；无新编译/BI运行、无全字段JSON认证。'),
('3104B局部解析已GS实际全文读，HF同字节对合法前缀、D1真实偏离保证、全部末位BR/三类未来动作集合和程序说明逐项比较。','现GS账本已完整保存该局部证明，新资源再次给准确量词/程序证据去向，明确只能排此时D0，不排C1/C2先走或替代全部截面。','duplicate：全部独有数学证明已有准确正文，局部48客户程序的描述不等于此次代码实读或运行；本地blob缺未重试，不因有完整文本证明而冒软件PASS。'),
('5359B D22遗漏正文GS已全文实读，HF核同SHA逐项核14兴趣类型、完整回复表、所有末位比较/根16、21对覆盖和价格截断证明/核验来源。','当前唯一最优族12类型与原14类二人收益等价但三重交集不同；D22(B,R,R,R,S,R)与现(B,S,R,S,S,R)在B/Q处平局差原样保，保护价另由遗漏集最大主题18及TQ满覆盖证明，不泛从两两交集推出所有价格。','duplicate：源独有表/selector/审计身份及数学去向全保，不新增同一个游戏/新颖性/最小性，净差3与遗漏36、half余32和原辅助桥不同，原程序不复跑。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 原多组真实claim pushed/synced不投影保字节，仅本5subset/currentowner/sourceSHA核齐。','comparison_note':b,'decision_note':c,'disposition':x['disposition'],'targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(E/'README.md',r'''# 五原稿与平稳/复制/局部/遗漏合同

5primary26149B在GS已实际全文数学读，HF同SHA逐节对照；3integrated+2duplicate、1资源0新命名定理或实例。新补给定六菜单平稳方程、query2七型/root0八型手算；不把手算当全258IC/OPT新审计。预算定义/条件meta-NE/六Q/整数尺度及编码范围保全，局部last-low和14类遗漏按明确原件身份duplicate。

5后续MD在父授权下HF首次全文读并作为相关比较/下一批预读保留，不写它们primaryreceipt。首次两次纯本地helper9attempts=5MD齐/4程序或报告缺，不重试、不网络。原代码/rawJSON仍未全读或执行，原作者单实现与独立局部文本范围分开。0新数学程序/原CLI/旧成功/LP/BI/随机/sharedGit/真实身份行为。

完整多组claim保原字节，仅本5 owner/SHA交集处理。Root先checkpoint正文依赖再done；计数/链接/格式自查不代数学判断，不导第三阶段旧图。
''')
put(W/'relation-review.md',r'''# 阶段二关系

6286是固定均匀完整槽核构造的逐外部查询失败，transient2虽无stationary源质量仍需cap；其self D-C为正、五纯列安全，不反同例自由mixed。手算π/query只是该给定菜单的部分解析核对，原全部IC审计范围不扩大；budgetΓ定义与混合期望利润用现完整槽恒等式，不换成actual单列W。

条件复制矩阵的p=Q uniformD和最优两块Q的meta-NE性质是静态插入博弈，不是顺序真后继；R4不自动真实，三块单实现有限排除与独立一个局部代表分开。六Q/n<=3分类与一般n猜想、普通12人分母/额外13人分母、终局全集/完整策略采样分开。

729局部D0偏离保证和aa原14类遗漏完整证明已有对象，不再冠同一反例；D2214/参数12输入二人等价及R-S平局差不能扩成高阶全同。保护价用自身截断证明。

相关下一五原稿当前已全文读但未在本包完成primary；其中发现稿CC/COH/DFP与逃逸独审的独有后续量词留独立新批处理。0第三阶段图/mapper/强制连边，不据缺blob否定已有解析，也不凭MD引用认证原程序。
''')
nextrows=[]
for x in related:
 q=REPO/'cleanup/progress'/f"{x['id']}.json";pr=json.loads(q.read_text()) if q.exists() else None
 nextrows.append({**inv[x['id']],'local_path':str(S/x['preserved_path']),'progress_observed':pr,'read_status':'HF actual first complete original text/math reading as related and parent-authorized nextprework; no primaryreceipt until actualHPclaim subset/owner verified','next_group':'Root explicitly assigned HP5; actualclaim still required, no projected or invented receipt'})
js(W/'next-candidates.json',nextrows)
cp(Path(__file__),E/'build_delivery.py')
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
def tex_balanced(s,left,right):
 def count(delim):return sum(ord(s[i])==92 and s[i+1]==delim and (i==0 or ord(s[i-1])!=92) for i in range(len(s)-1))
 return count(left)==count(right)
assert tex_balanced(chr(92)+'[x'+chr(92)+']','[',']') and not tex_balanced(chr(92)+'[x','[',']') and tex_balanced(chr(92)*2+'[2pt]','[',']')
for x in primary+related:
 b=(S/x['preserved_path']).read_bytes();ck('exactsizeSHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('exactblobSHA1 '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('rawclaim byteidentical',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes());ck('actual5subset owner SHA',set(IDS)&set(claim['ids'])==set(IDS) and len(owners)==5 and all(x['owner']=='Boss4' and x['source_sha256']==inv[x['id']]['sha256'] for x in owners));ck('pushedsynced actualclaim',claim['status']=='pushed' and claim['local_sync']['status']=='synced' and claim['remote_tip']==claim['local_sync']['remote_tip'])
for x in contexts:ck('actualcontext exactsnapshot '+x['path'],len((S/x['snapshot']).read_bytes())==x['bytes'] and sha((S/x['snapshot']).read_bytes())==x['sha256'] and (S/x['snapshot']).read_bytes()==(REPO/x['path']).read_bytes())
t=(S/P).read_text();ck('flatMATEK',all(re.search('^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']));ck('formal nonLF C0zero',not any(ord(c)<32 and c!='\n' for c in t));ck('formal trailingzero',all(l==l.rstrip() for l in t.splitlines()));ck('TeXreal delimitersbalanced',tex_balanced(t,'[',']') and tex_balanced(t,'(',')'));links=[]
for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
 if '://' in dest or dest.startswith('#'):continue
 n=posixpath.normpath(str(Path(P).parent/dest.split('#',1)[0]));q=S/n if (S/n).exists() else REPO/n;ck('actualrelative link '+dest,q.exists());links.append({'source':P,'destination':dest,'resolved':n,'bytes':q.stat().st_size,'sha256':sha(q.read_bytes())})
js(E/'formal-link-check.json',links)
ck('handcomponents explicitlynotfullIC certification','没有核原43节点的全部激励' in t and 'query2七型' in t and '0代码执行' in t);ck('sixQandintegerencoding explicit',all(x in t for x in ['(2,0,0,2)','27720','360360','四位计数编码','n=1,2,3']));ck('conditionalmetane notrealSPE',all(x in t for x in ['对称meta-Nash','必须由**同一**完整SPE','独立两块稿','匹配零和行对偶']));ck('allcut/local contrast','只有一个实现' in t and '不排先C1/C2' in t);ck('uniqueomission inputsselectors distinct','(B,R,R,R,S,R)' in t and '(B,S,R,S,S,R)' in t and '14兴趣类型' in t)
ck('helper actual2calls5exports4missing',len(exports)==2 and sum(len(m['rows']) for m in exports)==5 and sum(len(m['missing']) for m in exports)==4);ck('allneworiginalprogramrunszero',all(scope[k]==0 for k in ['new_math_program_runs','new_original_CLI_calls','old_success_replays','new_LP_BI_random_or_SPE_programs','missing_retry_calls','network_or_lazy_fetch','shared_Git_writes']))
ck('5receipts 3integrated2duplicate',len(receipts)==5 and {x['id'] for x in receipts}==set(IDS) and sum(x['disposition']=='integrated' for x in receipts)==3 and sum(x['disposition']=='duplicate' for x in receipts)==2)
for x in receipts:ck('complete semanticreceipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']) and all((S/p).exists() or (REPO/p).exists() for p in x['targets']))
ck('only1newformal',list((S/'archives').rglob('*.md'))==[S/P]);ck('nextHPnotprimaryreceipts',not ({x['id'] for x in nextrows}&set(IDS)))
for x in nextrows:ck('actualnextlocal sameSHA '+x['id'],Path(x['local_path']).exists() and len(Path(x['local_path']).read_bytes())==x['size'] and sha(Path(x['local_path']).read_bytes())==x['sha256'])
obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:u=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen=any('/'+z+'/' in rel for z in ['original','related','context']);bad=[i+1 for i,l in enumerate(u.splitlines()) if l!=l.rstrip()];c0=[{'offset':i,'code':ord(c)} for i,c in enumerate(u) if ord(c)<32 and c!='\n']
 if bad or c0:obs.append({'path':rel,'frozen':frozen,'trailing_lines':bad,'nonLF_C0':c0})
ck('all derived C0andwhitespacezero',not any(not x['frozen'] for x in obs));js(E/'transport-format-observations.json',{'observed':obs,'frozen_original_related_context_unchanged':True})
put(W/'delivery.md',f'''# HF交付

5primary26149B/{scope['primary_lines']}行GS已真实全文读，HF核同SHA并逐段数学比较；3integrated+2duplicate、1资源0新命名定理/实例。给定六菜单π和query2/root0手算、Γ完整定义、条件metaNE、六Q/LCM/编码/单实现与局部独审范围自足保。0新数学程序/原CLI/旧成功/LP/BI/随机。

原{len(claim['ids'])}ids claim {claim['remote_tip']} actualpushed/synced原字节保，本5subset/owner/SHA核齐。两纯本地helper9attempts/5MD齐4code-report缺、不重试不network。5相关及父授权HP预读原件本批实际全文首读，但本包不对它们写primaryreceipt；精确path/SHA在next-candidates。

Root先checkpoint正文依赖再done；旧HD未取得review和本HF新读review按时点分别保，GY原包/Root应用历史不覆写。无sharedGit/账号/公屏或第三阶段图操作。
''')
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'relative_links':len(links),'formal_nonLF_C0':0,'formal_trailing_whitespace':0,'scope':'byte/owner/rawclaim/coverage/definitions/link/format/transport checks, not mathematical verification by counts; no program execution of original audits'})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':26149,'primary_lines':scope['primary_lines'],'new_formals':1,'formal_bytes':(S/P).stat().st_size,'receipts':5,'dispositions':{'integrated':3,'duplicate':2},'checks':len(checks),'relative_links':len(links),'new_math_runs':0,'raw_claim_ids':len(claim['ids']),'claim_tip':claim['remote_tip'],'next_HP_ids':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
