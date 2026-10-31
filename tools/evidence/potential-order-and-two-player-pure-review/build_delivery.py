from pathlib import Path
import json,hashlib,re,posixpath
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';S=C/'r3-potential-order-and-two-player-pure-review';E=Path('tools/evidence/potential-order-and-two-player-pure-review');W=Path('cleanup/workspaces/Boss4/r3-potential-order-and-two-player-pure-review-next')
IDS=['660dfafc2b1f46eefb5a','77dc8f6a0eeacf046b19','9128fabeba5f47334bf8','5656d817863bfb636632','516fde591126a01e5b33']
PC='archives/customer-attraction/state/计算/二十四客户势最大根列的定义级核验--计算.md';PR='archives/customer-attraction/state/资源/两人纯列与势排序工作区的复用边界--资源.md'
PG='archives/customer-attraction/state/资料/完整根菜单的联合势义务与排序边界--资料.md';PP='archives/customer-attraction/state/引理/两名剩余完整终局菜单的纯列封顶--引理.md';PSH='archives/customer-attraction/state/引理/末位真实回复推送的锐曲率与双分支式--引理.md';PI='archives/customer-attraction/state/引理/完整槽插入税与跨角色价格恒等式--引理.md';P1='archives/customer-attraction/state/资源/真实分支十项合同与菜单可实现性账本--资源.md';PB='archives/customer-attraction/state/反例/银行完整根列的两查询最小分离--反例.md'
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
claimpath=R/'boss4-r3-next-hv-claim.json';claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(IDS)<=set(claim['ids'])
mp=C/'learning-hp-next-local-mathematics/local-export-manifest.json';m=json.loads(mp.read_text());primary=[];owners=[]
for i in IDS:
 x=next(x for x in m['rows'] if x['id']==i);v=inv[i];b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];owner=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==v['sha256'];owners.append(owner);q=E/'original'/i/x['path'];cp(x['local_path'],q);primary.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'headings':[l for l in b.decode().splitlines() if l.startswith('#')],'read_mode':'HV first actual entire original text andmath reading, allsections/table/endmatter; HP only verified byteavailability'})
assert sum(x['size'] for x in primary)==15616
js(E/'source-manifest.json',primary);cp(mp,E/'actual-primary-local-export-manifest.json');cp(claimpath,E/'actual-unprojected-claim-receipt.json');js(E/'actual-primary-ownership-snapshot.json',owners)
contexts=[]
for p in [PG,PP,PSH,PI,P1,PB]:
 b=(REPO/p).read_bytes();q=E/'context'/p;cp(REPO/p,q);contexts.append({'path':p,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_mode':'HV actual full currentformal text read for24/r2/domain comparisons' if p in [PG,PP,PSH] else 'previousactual full math derivation/read and currentwholebyte snapshot for price/background/oldledger comparisons'})
js(E/'context-manifest.json',contexts)
missingmp=C/'learning-hv-related-24-audit-inputs/local-export-manifest.json';miss=json.loads(missingmp.read_text());assert miss['rows']==[] and len(miss['missing'])==4;cp(missingmp,E/'actual-four-original24-audit-local-missing.json');js(E/'missing-original24-inventory-records.json',[inv[x['id']] for x in miss['missing']])
oldbase=REPO/'archives/customer-attraction/tools/evidence/origin-retraction-workspace';oldreport=(oldbase/'replay/origin_retraction_exact_audit.json').read_bytes();oldj=json.loads(oldreport);auditnames=[{k:z[k] for k in ['name','m','topics','unit_clients','complete_history_IC_checks']} for z in oldj['audits']];assert len(auditnames)==6 and all(z['unit_clients'] not in [24,791] for z in auditnames)
cp(oldbase/'replay-input-manifest.json',E/'prior-9173-replay-input-manifest.json');js(E/'prior-success-suite-membership-binding.json',{'report_path':str((oldbase/'replay/origin_retraction_exact_audit.json').relative_to(REPO)),'report_bytes':len(oldreport),'report_sha256':sha(oldreport),'actual_case_scalar_metadata_read':auditnames,'inspection_scope':'actual6caseidentity/scalarfields andinputmanifest only, not a new fullnestedreportreview or execution','no_24_or_791_fixture':True,'consequence':'prior348/52/etc fullSPE success cannot certify reweighted24sourcepolicy; no replayperformed'})
D=S/E/'new-independent-24-check';run=json.loads((D/'run-001/run-metadata.json').read_text());report=json.loads((D/'run-001/report.json').read_text());derived=json.loads((D/'derived-input-24.json').read_text());assert run['returncode']==0 and run['stderr_bytes']==0 and report['IC_including_self']==399 and report['IC_nonself']==342 and report['complete_policy_nodes']==57 and report['source_sha256']==inv[IDS[0]]['sha256'] and report['derived_input_sha256']==sha((D/'derived-input-24.json').read_bytes())
assert run['new_code_sha256']==sha((D/'check_phi24_from_units.py').read_bytes()) and run['report_sha256']==sha((D/'run-001/report.json').read_bytes())
def front(id,kind,tag,title,status,summary,subset):
 t='---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in [('id',id),('kind',kind),('type_tag',tag),('title',title),('status',status),('summary',summary)])+'source_refs:\n'
 for x in primary:
  if x['id'] not in subset:continue
  for y in x['sources']:t+='  - '+json.dumps('source:'+y['commit']+':'+y['path'],ensure_ascii=False)+'\n'
 return t+'---\n\n# '+title+'\n\n'
bc=r'''## 输入、量词与被反驳的精确选择规则

三名单位提供者、24名不同单位客户，有限共同目录七标签0…6，依全部有序历史选一次主题，最终客户在覆盖者间均分。标签0…5为X0/X1/X2/Y0/Y1/Y2，6为空。允许重复主题、任意离轨平局。原文B10-FULL-MENU-PHI-RISE-OBSTRUCTION-v1的24客户输入与完整策略首次实际全文读，本页是**新增一次定义级有限核验**，不是原作者CLI复跑或另一个盲审。

给定同一完整SPE，强制首行动b后的真三槽列Z(b)，原根收益d_b，actual u=max_b d_b。定义Phi(Z)=Σ_x H_(c_x(Z))，额外查询K_ab=Σ_(x∈a)1/(1+c_x(Z(b)))，**不删除原root**。本输入同时否定：

- K_ab>u就必有Phi(Z(a))>Phi(Z(b))；
- 每个势最大根列都阻断全部额外查询。

它明确存在好的势最大列，不由此反驳“存在一个好势最大列”、纯列存在、自由mixed、ownpay或half。后续别的反例状态在资源对象另述，不能把本输入的局部非反驳改写为一般候选仍OPEN。

## 全部单位客户和全部历史策略

mask的第a位表示喜欢主题a，重数是不同单位客户数；全部15行如下。

| mask | 数量 | mask | 数量 | mask | 数量 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 3 | 9 | 3 | 12 | 2 |
| 16 | 3 | 21 | 1 | 23 | 1 |
| 29 | 1 | 33 | 2 | 36 | 2 |
| 42 | 1 | 43 | 1 | 46 | 1 |
| 53 | 1 | 54 | 1 | 58 | 1 |

总数24，mask均<64所以6为空。只看正重类型2、16、9、12、33、36的membership列就能区分七个标签，故六非空主题及空主题两两不同。

完整策略：根0；第二位见首0/1/2则3，其他首行动则0；末位见两个非空行动时，在第二行动所属三主题组{0,1,2}或{3,4,5}里选尚未出现的最小标签；恰一非空标签a时取(1,0,0,4,3,3)[a]；两项均6时取0。两个相同非空行动属于“两非空”情形，不因标签相同当成只有一位非空玩家。

这在1+7+49=57个有序决策节点全部有定义，含空、重复及所有离轨历史；不是只给actual路径或把同计数历史强制合并。改变了旧34客户证书的重数，不能直接搬旧34或348的PASS。

## 实际唯一数学执行及完整性依据

原4份引用审计源码/24JSON本地首次helper均缺blob，未重试/未network；已成功9173B旧六fixture报告也没有24/791例，因此本批另写[4355B定义级程序](../../../../tools/evidence/potential-order-and-two-player-pure-review/new-independent-24-check/check_phi24_from_units.py)，读取[MD逐行转录输入](../../../../tools/evidence/potential-order-and-two-player-pure-review/new-independent-24-check/derived-input-24.json)。派生输入不是未取得的原48526B JSON，SHA50cc99d747a346593f9649dab1a1d05680af887b96481164c3b73d7b7a30cde8绑定实际5644B原MD SHAe523e3ebffb86906b8d67675e2f8c18223c03bf0043d729f9a9ab4515507fb0b。

程序只用标准库Fraction、product和JSON，展开24名单位客户。每个长度0/1/2的有序历史h，先按σ补全规定叶；对每个合法行动a强制一次后，沿**同一个σ**的新历史继续，精确比较当前位最终份额。57×7=399含self比较、342真正偏离全部非负，最小松弛0。每位只行动一次，全部子博弈当前行动最优且子树同样满足，故有限逆向归纳证明这份完整策略为纯SPE；不枚举所有可能策略。

本次数学程序实际仅1次，Python3.12.14、断言开启，0.050853418秒，exit0、stderr0，原CLI0、旧成功重跑0、791run0。启动child前有一次包装前置断言中止，未创建run目录/未执行数学主体，代码与输入未改；不把它记为第二次数学核验。[运行metadata](../../../../tools/evidence/potential-order-and-two-player-pure-review/new-independent-24-check/run-001/run-metadata.json)和[148917B完整新报告](../../../../tools/evidence/potential-order-and-two-player-pure-review/new-independent-24-check/run-001/report.json)保命令/cwd/版本/哈希、全57动作/399差值、七列与49项K。新报告SHAa7d04a5a6ebad912d64f4ee5571ee3ba044f7a3011ff64047ace3d12cb621ecf；不声称与未读原报告逐字节相同。

## 七个真根列与定量反驳

| 强制root b | 完整Z(b) | 原根d_b | 完整Phi | max_a K_ab |
| ---: | --- | ---: | ---: | ---: |
| 0 | (0,3,4) | 35/6 | 143/6 | 11/2 |
| 1 | (1,3,4) | 35/6 | 143/6 | 73/12 |
| 2 | (2,3,4) | 35/6 | 143/6 | 16/3 |
| 3 | (3,0,1) | 35/6 | 143/6 | 11/2 |
| 4 | (4,0,1) | 35/6 | 143/6 | 73/12 |
| 5 | (5,0,1) | 35/6 | 143/6 | 16/3 |
| 6 | (6,0,1) | 0 | 18 | 41/6 |

actualZ0=(0,3,4)，收益(35/6,41/6,19/3)，W19，u35/6。query2对column4给K24=73/12，超u1/4，而Phi Z2=Phi Z4=143/6且均为最大。所以高插入不强制严格升势，且一个势最大列仍可能坏。

column0同样势最大，完整查询向量(43/12,11/2,21/4,47/12,43/12,11/2,0)，cap11/2<u，余量1/3。因此好势最大列/纯blocker在**此输入**真存在；d0=u故此纯列也满足所有K_a0<d0的ownpay。总客户24<2W38已足够排此例half违反，本次未枚举OPT或求客户数最小性。

下列完整K是本次新增实现的输出，行query、列强制root；原MD的给定cap/column0向量已全部核对，不把这张新表冒原未读JSON。
'''
km='\n| query / root | '+' | '.join(str(i) for i in range(7))+' |\n| ---: | '+' | '.join(['---:']*7)+' |\n'
for i,row in enumerate(report['K_rows_query_columns_root']):km+='| '+str(i)+' | '+' | '.join(row)+' |\n'
end=r'''
## 791来源例与有限检查的边界

实际已全文读的原MD另称：同形式策略、19类型791客户有完整57节点/399比较的旧精确证书，actual u187、W597；a5,b1时K_(5,1)=196>u而Phi Z5=1505/2<Phi Z1=1511/2。它比24等势例更强地反驳“高插入至少不降势”。本批没有取得其原类型/动作/报告字段，0次791运行，只按明确的源称有限结果保留，不由24或348证书替代其验证；此前现页“791缺失/原稿声明”仍是那时的真实证据边界。

固定策略锥LP/整数优化只提供发现线索；`phi_rise_candidate.json`、`phi_rise_small_candidate.json`是原检查点，不认证全局最小性。新增程序没有导入规范SPE模型/solver或发现者审计，没有优化客户数，没有给一般mixed/六人half证明、外审或新颖性。独有24输入和新有限证书可复用作势选择量词的回归；一般多后继联合遗憾仍须真实支付。
'''
put(PC,front('customer-attraction/24-unit-potential-max-root-column-definition-check','computation','计算','二十四客户势最大根列的定义级核验','new-once-exact24-fullhistory-PASS; original791-source-only','完整24单位客户/57有序策略新增一次399IC与K/Phi核验，坏/好最大势列同存；原程序缺失不借旧348/34 PASS，791仅源称结果。',[IDS[0]])+bc+km+end)
br=r'''## 五源的实际对象和审查时点

五原文5644/2606/2101/2555/2710B共15616B在HV首次全部实读；HP只核过可用字节。24完整输入及全部历史策略新增一次定义级通过，见[有限计算对象](../计算/二十四客户势最大根列的定义级核验--计算.md)；两人纯列独审数学已完整覆盖，三份README仍有资源角色/状态纠错价值，不因入口标签自动退休。

旧Boss10/子审查者、个人备份/未提升canonical、停止同模板优化均是源历史，不改变当前Boss4或三阶段清洗指令。一般n目标未被这些页解决；当前另有五人half，六人仍自己的问题。

## 两人纯列2606B独审：准确duplicate

[现两人纯列引理](../引理/两名剩余完整终局菜单的纯列封顶--引理.md)已经完整保原数学的任意**非负实**背景b、共同有限目录、每个首行动A后的真实末位BR R_A及全部平局/空/零边界。定义f(A)=Σ_A1/(b+1)，g_x=1/[(b+1)(b+2)]，h_x=2/[(b+1)(b+2)(b+3)]，D_A=U(A,R_A)。精确身份为
\[
D_A+f(R_A)-f(R_B)-K_{A,B}
=[U(R_A,A)-U(R_B,A)]
+\sum_{x\in A\cap B}(g_x-h_x\mathbf1_{R_B}(x)).
\]
只用R_A是固定A后的BR；R_B是共同目录合法比较，不假装它在A后也最佳。单客户余项≥g_x−h_x=1/[(b+2)(b+3)]>0。取B*最大化f(R_B)，同一列同时给全部queryA：
\[
D_A-K_{A,B^*}\ge f(R_{B^*})-f(R_A)
+\sum_{x\in A\cap B^*}\frac1{(b_x+2)(b_x+3)}\ge0.
\]
只有最后转成actual u=max_A D_A才用根最优。不用独立抽样或先挑querylaw；矩阵行A同时是另一条真实首分支，列B是竞争源，不能换索引。

这与[任意p锐推送](../引理/末位真实回复推送的锐曲率与双分支式--引理.md)是不同接口：前者一固定列封全部行，后者每个p的独立查询Q=p有曲率余项。且这里界是**行分支D_A**，不是所选列自己的d_B*；不要据纯cap≤u直接说更强ownpay已证。裸回复f排序只适用恰一后继，不能把多后继组合当一个BR或改成一般完整终局Phi排序。原2606B是先见proof_tree身份陈述的独立重构历史，不是5009B任意p独审的同一文件，不多算新审稿人或当前新run。

## 三种势选择量词与当前状态

24已实际新核：高K不必**严格**升Phi；并非**每个**最大Phi列都好，但确有**一个**好的最大Phi列。它的等势不反“至少不降Phi”；791源称严格下降另承担该更强排除，未本批验证原数据。348既有二环/正联合遗憾有其已成功同SHA证据，不重跑或改成24/791证书。

后来的八人纯菜单反例来源报告每个真实完整root列都有查询超u，故按该完整证书认可也排“总存在一个好最大Phi列”的普遍版本；不能从24局部非反驳留一般纯列OPEN。本批未新认证八人原DAG/代码。任意mixed、全路径/聚合预算和half是不同域，不因某条标量选择失败一并判负。

一般联合COL/PAY的域与r≥3未付符号见[联合势义务](../资料/完整根菜单的联合势义务与排序边界--资料.md)，当前普遍实际根Mfull已由真正银行反例否定；条件恒等式、r2正面组件仍有效。

## exchange入口的ownpay旧OPEN需纠正

原精确候选为存在与query独立的真实根列分布Q，使每个a都有Σ_b Q_b(K_ab−d_b)≤0。它的d_b是**列root本人**的真收益，不是query行d_a，列含原root。任何给定完整SPE都有d_b≤u，因此ownpay⇒E_QK_ab≤E_Qd_b≤u⇒FM。普遍FM已被[零根银行列](../反例/银行完整根列的两查询最小分离--反例.md)反驳，所以这个更强的普遍ownpay也不能继续照抄OPEN。

该银行m4的每列d_b=u4/3，Mfull59/36，故min_Q max_a ΣQ(K_ab−d_b)=59/36−4/3=11/36>0。这个推论只用已完整银行SPE/矩阵，不重跑控制器、不构造新实例，也不据此说r2纯列定理失败。反之24本输入有column0所有K<d0，确实没有反ownpay，原MD这一局部范围保持。

## 三份入口逐项的资源用途

| 源入口 | 全部独有用途、现在的准确去向 |
| --- | --- |
| counterexample/README / 2101B | 双向隔离任意k锐架构、E>(k+2)|D|/3必要非充分、重复末位惩罚失败、两块撤销、八人纯/混合分界及DAG发现/直接核验/冻结输出的角色，已有[十合同账本](../资源/真实分支十项合同与菜单可实现性账本--资源.md)。`pure_menu_cone_probe.py`/`pure_menu_cones_*.json`称在固定完整策略锥用二元变量为每root列挑坏query，是数值探索，未读这些程序/通配全部输出，不承担一般证明。未来追随者/跨组/稀释D还须全离轨历史与惩罚者自己的最优性。 |
| exchange/README / 2555B | 71客户遗漏/42比较/21对/保护价格与24、791各精确审计的原角色完整保；同71证书“独立重现”不认证新颖性，14/12输入及不同R-S选择器已经分别保。`probe_integral_price.py`/`integral_price_probe_m3.json`只有限完整策略锥阴性，不证一般价格预算；两个Phi候选JSON只是发现检查点。允许局部欠债/完整OPT−W与遗漏单独支付分开；ownpay旧一般OPEN按上节纠正，停止优化是历史不变清洗停工命令。 |
| round5_audit/README / 2710B | 原审查者只读模型/三被审正文/必要接口、不读发现核验代码。原Φ排序只复核量词已有root证据，**未再核数值**；真正新增独立重构是背景价格全人数族m≥2、2≤r≤m；一般联合势身份只审代数和r2 BR，r≥3遗憾无符号，未重跑二环。后加6286独审从原mask/43动作表展开，不将个人备份状态当当前尚无正式对象。 |

价格全人数重构、标准库单位审计及有限参数输出、全槽预算一般机制的完整数学已在[插入税与跨角色身份](../引理/完整槽插入税与跨角色价格恒等式--引理.md)：mL/L两不交主题的每历史完整SPE、actual前缀k=m−r、固定r当前增量付款无正统一系数；该族全p强推送/FM/half反而成立。README的代码称遍历二元有序历史与全部合法前缀，有限参数只核实现，全m/r由解析承担；本批没读/运行它的原代码或报告。

原审查入口新增stationary4495B已另全文处置：6286唯一完整槽stationary不逐查询安全，self strong在该例仍真、五纯列安全。不能把一次独审对三旧资产的侧审范围拓成三个数值新run，也不把后加stationary算原三稿全部重审。

## 保存与证据边界

[源manifest](../../../../tools/evidence/potential-order-and-two-player-pure-review/source-manifest.json)保五原件SHA/两个冻结版本和真实首读范围；源码/输入/输出/执行元数据完整存新24检查目录。原4缺只指首次安全本地blob导出结果，不声明全局永久不存在，不重试/不network；791旧缺状态和原作者审查时点不覆写。

新增数学程序仅24一次，原CLI/791/旧成功复跑/LP/BI/随机均0。已读三个正式数学对象完整比较，其他旧source仅准确复用，未额外done引用程序/JSON。外审、新颖性、原发现全局最小性和canonical通用算法均不由本资源认证，不导第三阶段旧图。
'''
put(PR,front('customer-attraction/two-player-pure-and-potential-order-workspace-reuse-boundaries','resource','资源','两人纯列与势排序工作区的复用边界','r2-proof-duplicate; entryresources-integrated; genericownpay-refuted-separately','精确保三入口的数值/侧审/程序角色、r2纯列全部实背景与索引，区分24好坏最大Phi列及791源称严格下降；ownpay一般旧OPEN由银行反例逻辑纠正。',IDS)+br)
js(E/'formal-resource-manifest.json',[{'path':p,'bytes':(S/p).stat().st_size,'sha256':sha((S/p).read_bytes())} for p in [PC,PR]])
nextmp=C/'learning-hv-next-round5-entry-inputs/local-export-manifest.json';nextm=json.loads(nextmp.read_text());assert len(nextm['rows'])==5 and nextm['missing']==[];cp(nextmp,E/'actual-next-byteavailability-local-export-manifest.json');cp(C/'local_blob_export.py',E/'authorized-local-export-helper.py.txt')
coverage=[
{'id':IDS[0],'disposition':'integrated','targets':[PC,PR],'units':['all3quantifiers highK->strictPhi / everymaxPhi block /existsgoodmaxPhi distinguished','15actual24unittypes/all7different labels/6Empty policy/full57ordered histories includingrepeat/empty','all7rootZ/d/Phi/caps/fullgivenvector0/actualpay/W','K24 gap1/4 equalmaxPhi andsafe maxPhi0 gap1/3','all4original24audits/code/JSON localmissingnotreplayed old348/34','NEWonce independent24MDtranscription full399IC/342nonself/sourceK-Phi expectednumbers allpass','79119typereport u187/W597/K51/Phi strictdown sourceonly notnewrawdataread','originalcode --case791 andcandidateLP/checkpointroles preservednotcurrentCLIcert','no minimal24/globalhalf/mixed/ownpayfailurefromthisinput/nooldhistoricalmissingrewrite']},
{'id':IDS[1],'disposition':'duplicate','targets':[PP,PSH,PR],'units':['arbitrarynonnegrealbackground versuslegalintegerprefixapplication','f/g/h definitions exacttwo membershipexpansion andpointwiseidentity','trueBRRAafterA notRBafterA/indicesqueryA vscompetitiveB','uniformcurvaturetax lowerbound >0 perclient','Bstar argmaxbarefRB samecol allquery K<=DA<=u','actualrootoptimalityneededonlylast conversion/notmixedsampling','empty/ties/zero/domainr2 noaggregatefutureasoneBR','oldindependentblindidentitystatementreview distinctfrom5009sharpmeanreview/noextranewperson']},
{'id':IDS[2],'disposition':'integrated','targets':[PR],'units':['oldcounterexamplerole/generalhalfOPEN historicalcurrent5/6state','isolationallk finiteexactsharp notuniversalratio','E necessarynot sufficient/truepunisherBR upgradedconstructionuncompleted','two-copywithdrawal/pure8vs851mixed/WOPT','DAGdirectunitcheck/outputs/discoverybuilder andnumericpurecone binaryquery-percolumn roles no codefullread','futurecrossbranchload/core/Dprecoverage hypotheses andfullorderedoffpath obligationnotinstructionsfornewrole']},
{'id':IDS[3],'disposition':'integrated','targets':[PR,PC],'units':['omission71fullproof/42IC/21covers/price/sourceindependentroot reproduction notnovel','24eq/791down auditandcandidatecheckpoint roles','14vs12tables/R-Sselector currentcorrection andnotnewinputsamebytes','OPT-Wdynamic net notallomission/allowlocallynegativecredit separate','preciseownpayQ K_ab-d_b strongertFM oldOPEN nowfalse byactualbankm4 logicalproof/value11/36','finiteintegralpricecone negativeprobe no theorem/stoppedspecialn historicalnotstopcleaning','new24 code notoldunreadcandidateoroldoriginalaudits pass']},
{'id':IDS[4],'disposition':'integrated','targets':[PR,PI,PG],'units':['originalmodel/3reviewedtext/interfaces/no discoverycode/currentbackupstatus historical','didnotrecomputePhi orr2numericcerts onlyquantifiers; rootoldindependent separate','independentreconstructionallm>=2/all2<=r<=m actualprefixpricefamily completeorderedhistory','unitscodeallbinaryhistories/legalprefixmatrix finiteparameters notallnproof','INSUbar/tax/nonnegativeGamma queryLOW lowernotrootupper andno menusign','added6286newunitreview onlygivenmasks/actions/uniqueπ/selfstrongsafe/fivepurecols','table3originalassets potrise side-review/meta_price full/identitygeneralalgebra+r2BR/no fullr>=3sign/no cycle rerun','no oldauditor statement convertednew24originalrun ornewexternalreview']}
]
js(E/'semantic-coverage-map.json',coverage)
scope={'primary_sources':5,'primary_bytes':sum(x['size'] for x in primary),'primary_lines':sum(x['lines'] for x in primary),'primary_first_full_read':'HV actual full all5 MDs, alltables/proofs/lastparagraphs and3entryroles; previousHP byteavailability only','dispositions':{'integrated':4,'duplicate':1},'new_formals':2,'new_unique_game_instances':0,'existing_source24_now_newly_checked':True,'new_independent_math_program_runs':1,'new_math_body_executions':1,'original_math_CLI_calls':0,'old_success_replays':0,'791_runs':0,'LP_BI_random_runs':0,'math_wrapper_preflight_abort_before_child':1,'math_wrapper_abort_changed_code_or_input':False,'new_24_code_sha256':run['new_code_sha256'],'new_24_input_sha256':run['derived_input_sha256'],'new_24_report_sha256':run['report_sha256'],'new_24_elapsed_seconds':run['elapsed_seconds'],'new_24_returncode':run['returncode'],'new_24_report_scope':'all57orderednodes,399including57self and342nonself, rootZ/d/Phi/caps/full7x7K; noOPT/minimality/791/originalcodebytecert','no_oldPASS_borrowing':'actualold9173sixfixture list/scalar metadata andinputmanifest read, no24or791; notnew fullnestedreportread oroldexecution','original24code_JSON_fullread':False,'source791_evidence':'fullprimaryMD reportedfinitevalues only, no raw19types/actions/report fields read/recreated','contexts_fullactualreads':[PG,PP,PSH],'local_helper_calls':2,'local_blob_attempts':9,'local_exports':5,'local_missing_blobs':4,'original24missing_ids':['43567027efc4cc9b0277','e8e48d51ea8a1350e274','4699c79f3d451ea9e9e6','161586ff432335201eed'],'missing_retry_calls':0,'next5_status':'actualMDbytesonly, nofullnewsemanticreading inHV/no primaryreceipt','shared_Git_writes':0,'claim_done_checkpoint_show_calls':0,'network_or_lazy_fetch':0,'real_board_account_auth_operations':0,'phase3_graph_import':0,'raw_claim_ids':len(claim['ids']),'primary_claim_intersection':IDS,'claim_projection_performed':False,'derived_packaging_builder_calls':1,'derived_packaging_builder_failures':0,'new_code_data_preparation_only_calls':1}
assert scope['primary_bytes']==15616;js(E/'read-scope-and-evidence-status.json',scope)
notes=[
('5644B势排序稿HV首次实际完整读，全部15类型/57规则/7根表/quantifierthreeway/791尾段/发现程序角色实读，不将旧24标题或348输入当全文。','当前旧成功9173六fixture无24/791、原4源码/24JSON本地首次缺，故新增1次定义级24单位检查：完整399IC/全部根K/Phi匹配，原CLI0/7910/旧成功0；源码/派生输入/全报告/实际运行meta完整保。','integrated：自足计算保此独有紧凑实例的全部输入和策略/好坏maxPhi列/1/4反驳，非一般half或ownpay反例；791严格下降只按原稿报告不冒新认证，24不称客户数最小。'),
('2606B纯列独审HV首次全文读，任意逐客户实背景、所有f/g/h/正税身份/选择式/索引和独立历史及最后边界均完整读。','现DY纯列与EG锐推送已完整覆盖这套同一两人身份/实b扩展，核只RA是A后BR、RB是合法比较、根最优性只用于最后转u，A行/来源B列不可交换。','duplicate：全部独有数学有精确目标，原blindreview先验保源身份，不与5009平均式审稿合并，不据K<=D_A误推列自身d_B ownpay；无新r2程序/数值重算。'),
('2101B反例入口HV首次完整实读，每项文件用途、allk范围、E严格必要、两副本撤销、纯8DAG/混合/数值锥/下一义务与角色状态保全。','对现十合同/isolation/HP显式重复尾假设/纯菜单证据角色比对；特别固定完整锥二元变量为每根挑坏query仅数值探索，不宣称读wildcard全部输出或引用程序。','integrated：保有用资源和准确下一问题域，不因旧README/备份标签退休，不把allk架构3/2近界成普遍half，不执行旧独立攻击/身份/Git研究命令。'),
('2555B交换入口HV首次全文实读，所有已完成/当前状态/停止探索段与每程序输出用途完整保。','原ownpay精确K_ab-d_b比rootu菜单强；用现银行Mfull>u逻辑纠正旧OPEN，并由每列d_b=u得m4 ownpay最小值11/36。24本例纯0自身d0封顶、遗漏原14/现12及R-S平局按精确对象保留。','integrated：原同证书/作者root独立重现不加新颖性或新run，浮点候选/旧整数价有限阴性与现在24新增定义级PASS分开，不改旧冻结记录或把停止优化当清洗终止。'),
('2710B独审入口HV首次全部正文/三项表格/新增stationary条目完整读，作者读取先验和没有重跑的内容同样保。','与现全m/r合法过去重构、完整槽预算、联合势r2符号/r>=3缺口及6286例逐项比较；作者数值独立验证只承当时范围，势反例仅量词侧审，非新的399/cycle审计。','integrated：三旧资产侧审和后加6286分别归位，单位代码/有限输出/全参数解析/新增24case执行互不借用；不把个人未canonical写成当前正式对象不存在，0重复其原code或旧成功。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 原多组真实claim保完整字节，只本5subset/currentowner/sourceSHA处理，不伪造投影。','comparison_note':b,'decision_note':c,'disposition':x['disposition'],'targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(E/'README.md',r'''# HV势排序/纯列/三入口清洗

五primary15616B全部HV首次全文实读，三现数学对象全文对照；4integrated+1duplicate，2新自足对象（24有限计算/入口资源），不新造同一个游戏或泛定理。新24检查实际一次：57完整有序节点/399含selfIC/342nonself，全rootK/Phi匹配；原CLI0/7910/旧成功0。

原4源码/24JSON本地helper首次缺，旧9173六fixtures没有24/791，所以不能借旧pass。新code4355B/MD转录input/148917B report/实际meta全保，不伪原代码输出；wrapper一次前置assert在child前中止，无run目录/代码数据改动，不算两次数学执行。两helper9attempts=5下一MD齐4原audit/code-data缺，不重试不network；下一只byte未全文，不primarydone。

资源保真实root列ownpay与row D_A区别/旧ownpayOPEN现在银行反例否定、24好坏maxPhi量词、791源称边界、三入口程序与审查时序。Root先推正文依赖后done，代理无sharedGit/账号/公屏/mapper。
''')
put(W/'relation-review.md',r'''# 阶段二关系

24定义级finite certificate保独有输入/完整σ和反例量词，不将旧348/34同形式策略pass移到新重数；高插入等势只反strict升势和所有maxPhi都好，actual纯0安全不反本例mixed/ownpay/half。791strict降势仍原稿报告，不被24或旧missing状态替代。

两人裸回复f排序是恰一后继BR的精确税身份，任意非负实背景只是代数域扩展；不将r3完整Phi排序当同机制，不混合row D_A和column d_B。一般ownpay强于FM，银行¬FM故其普遍旧OPEN应改，但r2正面接口和此24实例的ownpay不被否定。

三README各自数学资源角色/独立审查范围和程序claim保留；侧审量词不等数值全审，原有限参数回归不承担全m/r，oldfloat候选不等精确证书。0额外done引用原code/JSON或下一5，0phase3图导入，不为连通造边。
''')
nextrows=[]
for x in nextm['rows']:
 v=inv[x['id']];b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'];q=REPO/'cleanup/progress'/f"{x['id']}.json";pr=json.loads(q.read_text()) if q.exists() else None
 if pr is None:nextrows.append({**v,'local_path':x['local_path'],'progress_observed':None,'read_status':'HV actualbyteavailability only, no newfullsemanticreading/primaryreceipt; Root nextactualclaim and fullread needed'})
js(W/'next-candidates.json',nextrows)
cp(Path(__file__),E/'build_delivery.py')
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
def tex_balanced(s,left,right):
 def count(delim):return sum(ord(s[i])==92 and s[i+1]==delim and (i==0 or ord(s[i-1])!=92) for i in range(len(s)-1))
 return count(left)==count(right)
assert tex_balanced(chr(92)+'[x'+chr(92)+']','[',']') and not tex_balanced(chr(92)+'[x','[',']') and tex_balanced(chr(92)*2+'[2pt]','[',']')
for x in primary:
 b=(S/x['preserved_path']).read_bytes();ck('sourceexactsizeSHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('sourceexactblob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('rawclaim byteidentical',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes());ck('actual5subsetownerSHA',set(IDS)&set(claim['ids'])==set(IDS) and all(x['owner']=='Boss4' and x['source_sha256']==inv[x['id']]['sha256'] for x in owners));ck('actualclaim pushedsynced',claim['status']=='pushed' and claim['local_sync']['status']=='synced' and claim['local_sync']['remote_tip']==claim['remote_tip'])
for x in contexts:ck('contextfrozenactual '+x['path'],len((S/x['snapshot']).read_bytes())==x['bytes'] and sha((S/x['snapshot']).read_bytes())==x['sha256'])
ck('new24exactcode/input/reportSHA',run['new_code_sha256']==sha((D/'check_phi24_from_units.py').read_bytes()) and run['derived_input_sha256']==sha((D/'derived-input-24.json').read_bytes()) and run['report_sha256']==sha((D/'run-001/report.json').read_bytes()));ck('new24actualonceexit0stderr0',run['run_index']==1 and run['returncode']==0 and run['stderr_bytes']==0 and run['original_CLI_calls']==run['791_case_runs']==run['old_success_replays']==0);ck('new24complete399reportdata',report['complete_policy_nodes']==len(report['policy'])==57 and report['IC_including_self']==len(report['all_IC'])==399 and report['IC_nonself']==342 and report['minimum_slack']=='0');ck('new24rootandcase',report['root_u']=='35/6' and report['actual_W']==19 and report['bad_maxPhi_column']['u_gap']=='1/4' and report['good_maxPhi_column']['strict_margin']=='1/3');ck('new24notoldJSONinput',derived['schema']=='new-MD-transcription-not-original-JSON' and derived['source_sha256']==inv[IDS[0]]['sha256'] and report['source_sha256']==inv[IDS[0]]['sha256']);ck('old6suite not24or791',len(auditnames)==6 and all(z['unit_clients'] not in [24,791] for z in auditnames));ck('original4actuallylocalmissing',miss['rows']==[] and len(miss['missing'])==4)
links=[]
for p in [PC,PR]:
 t=(S/p).read_text();ck('flatMATEK '+p,all(re.search('^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']));ck('nonLF C0zero '+p,not any(ord(c)<32 and c!='\n' for c in t));ck('trailingzero '+p,all(l==l.rstrip() for l in t.splitlines()));ck('actualTeXbalanced '+p,tex_balanced(t,'[',']') and tex_balanced(t,'(',')'))
 for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://' in dest or dest.startswith('#'):continue
  n=posixpath.normpath(str(Path(p).parent/dest.split('#',1)[0]));q=S/n if (S/n).exists() else REPO/n;ck('actualrelative link '+dest,q.exists());links.append({'source':p,'destination':dest,'resolved':n,'bytes':q.stat().st_size,'sha256':sha(q.read_bytes())})
js(E/'formal-link-check.json',links)
ct=(S/PC).read_text();rt=(S/PR).read_text();ck('24program/791authorscope separate','原CLI0' in ct and '791run0' in ct and '未本批验证原数据' in rt);ck('all24originaltypes policy andquantifiers','恰一非空标签' in ct and '两个相同非空行动' in ct and '好的势最大列' in ct);ck('rowcolumnownpayindexdomain','行分支D_A' in rt and 'K_ab−d_b' in rt and '11/36' in rt);ck('r2realbackgrounddomain','非负实' in rt and '不假装它在A后也最佳' in rt);ck('entry3rolesfullypresent',all(x in rt for x in ['counterexample/README','exchange/README','round5_audit/README','二元变量','未再核数值','2≤r≤m']))
ck('5receipts4integrated1duplicate',len(receipts)==5 and {x['id'] for x in receipts}==set(IDS) and sum(x['disposition']=='integrated' for x in receipts)==4 and sum(x['disposition']=='duplicate' for x in receipts)==1)
for x in receipts:ck('complete semanticreceipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']) and all((S/p).exists() or (REPO/p).exists() for p in x['targets']))
ck('exact2newformal',set(str(p.relative_to(S)) for p in (S/'archives').rglob('*.md'))=={PC,PR});ck('mathbody1not2andnooriginalreplays',scope['new_math_body_executions']==scope['new_independent_math_program_runs']==1 and scope['original_math_CLI_calls']==scope['old_success_replays']==scope['791_runs']==0 and scope['math_wrapper_preflight_abort_before_child']==1);ck('helpers2calls9attempts5exports4missing',len(nextm['rows'])==5 and len(miss['missing'])==4 and scope['local_helper_calls']==2 and scope['local_blob_attempts']==9)
for x in nextrows:ck('actualnextavailable '+x['id'],Path(x['local_path']).exists() and len(Path(x['local_path']).read_bytes())==x['size'] and sha(Path(x['local_path']).read_bytes())==x['sha256'] and x['progress_observed'] is None)
obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:u=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen=any('/'+z+'/' in rel for z in ['original','related','context']);bad=[i+1 for i,l in enumerate(u.splitlines()) if l!=l.rstrip()];c0=[{'offset':i,'code':ord(c)} for i,c in enumerate(u) if ord(c)<32 and c!='\n']
 if bad or c0:obs.append({'path':rel,'frozen':frozen,'trailing_lines':bad,'nonLF_C0':c0})
ck('allnewderivedC0trailingzero',not any(not x['frozen'] for x in obs));js(E/'transport-format-observations.json',{'observed':obs,'frozen_original_context_unchanged':True})
put(W/'delivery.md',f'''# HV交付

5primary15616B/{scope['primary_lines']}行首次实际全文读，4integrated+1duplicate，2自足正式对象。24有限输入首次新增定义级执行1次，全57节点/399IC/342非self和rootK/Phi通过；原CLI/791/旧成功/LP/BI/随机均0。另wrapper一次preflight在启动child前中止，代码数据未改，主体仍一次。

原{len(claim['ids'])}ids claim {claim['remote_tip']} actualpushed/synced原字节保，仅本5subset/owner/sourceSHA。原4审计code/24JSON首次本地缺不重试，旧9173报告六fixtures无24/791；新code/MD转录input/148917report/真实运行元数据齐，不冒原件或generic solver认证。

两helpers9attempts=5下一MD齐4原code/data缺，无network/sharedGit/账号或phase3图。下一{len(nextrows)}原件仅byteavailable未本批全文，Rootactualclaim后继续。Root先推正文与真实依赖再done。
''')
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'relative_links':len(links),'formal_nonLF_C0':0,'formal_trailing_whitespace':0,'math_checks':'new24 independentonce actual399finiteSPE/K/Phi check inrunmetadata; these packagingcounters do notprove other mathematics','scope':'rawsource/owner/claim/executionbindings/input/target/coverage/links/format/transport'})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':15616,'primary_lines':scope['primary_lines'],'new_formals':2,'formal_bytes':sum((S/p).stat().st_size for p in [PC,PR]),'receipts':5,'dispositions':{'integrated':4,'duplicate':1},'checks':len(checks),'relative_links':len(links),'new_independent_math_runs':1,'new_original_CLI_runs':0,'old_success_replays':0,'791_runs':0,'raw_claim_ids':len(claim['ids']),'claim_tip':claim['remote_tip'],'next_candidates':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
