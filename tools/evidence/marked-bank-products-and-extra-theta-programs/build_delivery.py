from pathlib import Path
import json,hashlib,re,posixpath,platform
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';S=C/'r3-marked-bank-products-and-extra-theta-programs';E=Path('tools/evidence/marked-bank-products-and-extra-theta-programs');W=Path('cleanup/workspaces/Boss4/r3-marked-bank-products-and-extra-theta-programs-next')
IDS=['d3d430c1938a29ce99c2','f390f53649e416176fef','73780fead77dbf46e31f','be025ded1b19d3bde56c','fefdf3d7d3b163ccccc5'];P1='archives/customer-attraction/state/程序/任意标记保险与两个不等缺陷产品的原审计--程序.md';P2='archives/customer-attraction/state/程序/八旧策略的纯额外槽有理复算--程序.md';P3='archives/customer-attraction/state/程序/固定三人完整推送的两分布浮点探针--程序.md';PH='archives/customer-attraction/state/定理/真实退出缺陷的统一与异质前缀修复--定理.md';PE='archives/customer-attraction/state/资源/额外槽饱和势与真实偏离分支覆盖上界--资源.md';PM='archives/customer-attraction/state/资源/完整终局推送的自身折扣与末两位储备--资源.md';PJ='archives/customer-attraction/state/资源/四个子目录入口的审计实现与复用身份--资源.md'
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
def front(i,title,status,summary,ids):
 t='---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in [('id',i),('kind','program'),('type_tag','程序'),('title',title),('status',status),('summary',summary)])+'source_refs:\n'
 for j in ids:
  for v in inv[j]['sources']:t+='  - '+json.dumps('source:'+v['commit']+':'+v['path'],ensure_ascii=False)+'\n'
 return t+'---\n\n# '+title+'\n\n'
# Primary claim verifies actual full raw multigroup IDs, never projected.
claimpath=R/'boss4-r3-next-jz-claim.json';claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(IDS)<=set(claim['ids'])
mp=C/'learning-ju-needed-original-source/actual-source-manifest.json';m=json.loads(mp.read_text());primary=[];owners=[]
for i in IDS:
 x=next(x for x in m['rows'] if x['id']==i);v=inv[i];b=Path(x['local_path']).read_bytes();assert len(b)==v['size']==x['size'] and sha(b)==v['sha256']==x['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];show=json.loads(Path(x['actual_normal_show_capture']).read_text());assert show['source']==v and show['output']==x['local_path'];owner=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==v['sha256'];owners.append(owner);q=E/'original'/i/x['path'];cp(x['local_path'],q);cp(x['actual_normal_show_capture'],E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name);primary.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'read_mode':'JZ actual5fullcode text read in2complete outputbatches, actualinputdependencyread complete before deciding anyrun; normalshowbyte/SHA/blob andcapture verified; no originalmoduleimport or execution'})
assert sum(x['size'] for x in primary)==25341
js(E/'source-manifest.json',primary);cp(mp,E/'actual-normal-show-source-manifest.json');cp(claimpath,E/'actual-unprojected-claim-receipt.json');js(E/'actual-primary-ownership-snapshot.json',owners);cp(C/'learning-ju-next-program-inputs/local-export-manifest.json',E/'first-local-five-code-missing-unchanged.json')
inputmp=C/'learning-jz-true-inputs-and-frozen-outputs/local-export-manifest.json';im=json.loads(inputmp.read_text());assert len(im['rows'])==16 and len(im['missing'])==4;inputs=[]
for x in im['rows']:
 v=inv[x['id']];b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'];q=E/'true-input-repository'/x['path'];cp(x['local_path'],q);inputs.append({**v,'preserved_path':str(q),'read_mode':'8fullinstances all13,841B customer/type/topic fields actuallyread; 8certificates allnonactionmetadata andcomplete14352history-actions read via exactlosslesssubtree335nodes/roundtrip, notSPE/security-primal-dual validation'})
js(E/'actual-theta-true-input-manifest.json',inputs);cp(inputmp,E/'first-local-inputs16-and-frozenoutputs4missing-unchanged.json');cp(C/'jz-exact-theta-input-inventory.json',E/'code-PAIRS-extracted-input-inventory.json');cp(C/'jz_read_policy_inputs.py',E/'lossless-policy-reading/reader.py')
for p in (C/'jz-input-reading-prework').iterdir():
 if p.is_file():cp(p,E/'lossless-policy-reading'/p.name)
contexts=[]
for p in [PH,PE,PM,PJ]:
 b=(REPO/p).read_bytes();q=E/'context'/p;cp(REPO/p,q);contexts.append({'path':p,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_mode':'previousactualcomplete math reading reused currentwholebyte snapshot; no oldsource/code run borrowed'})
js(E/'context-manifest.json',contexts)
b1=r'''## 三个不同的原实现与共同单位模型

三个源码4931/5862/6096B均实际全文读。固定单位客户、单位提供者、共同有限非空目录、每个有序历史的纯SPE；任意标记保险/异质编译的全m证明在[现定理](../定理/真实退出缺陷的统一与异质前缀修复--定理.md)。这里保存有限实现合同，不重认一般定理、独审或75客户游戏首次。

三个文件只导标准库Fraction、functools、itertools、pathlib/json（parent另hashlib/platform），不导作者/规范模型/solver。marked-bank只在__main__进入main；两个75脚本**顶层就计算、检查、写JSON和打印**，不能import当只读加载。均以Path(__file__).with_suffix('.json')写源码旁同名输出，而非写cwd；真实复现必须复制到独立空目录，不能覆盖冻结输出或共享树。本批原CLI/原模块import/新SPE或旧成功复跑全0，旧输出身份另保，不以代码保存当已执行。

## 任意标记银行：26游戏不是全m数值证明

`audit(m,marks)`用k个大小2的银行、大小d=m−k的Y、d−1个大小1叶，marks为0基非末位标记，正常动作按标记选fresh银行、其余Y。收益为尺寸/同标签最终次数，整数尺寸代表不交单位客户块。BI以计数缓存，一次真偏离后若dirty则永久进入这个BI；完整历史audit本身不合并顺序。

每个正常位置i及每个强制动作都审：重复银行/叶先定BI；Y进入Y模式；freshF进入F模式。clean先填空银行，再Y至d（Y模式）或d−1（F模式），最后复制F。`child_is_bi`检测重复银行、叶、Y超限；permanent标志一旦真就不复位。即使后面计数看似clean也不回原模式；最后复制F可标BI因已经终端无差。每低退出孩子枚举其后全部有序历史及所有m个当前动作，Fraction断言每IC margin≥0，并检查强制者最终cap≤1。正常角色自身银行收益2/其他1，W_bank=m+k、OPT_bank=2m−1另直接断言。

实际__main__只m2…5、每个非空marks⊆{0,…,m−2}，共1+3+7+15=26游戏；每游戏m²个强制孩子，总518。原输出15353决策历史/75913含自身比较，是**各低退出孩子审计累计**，同一绝对历史可在不同强制入口重复计，不冒单个全树unique节点。它们支持指定实现有限域，任意m的clean/BI全树证明靠现定理，不靠把26外推。

## 作者75：计数终局全集、完整联合表与逐单位检查

作者`credible/audit_heterogeneous_product.py`固定m3,j2。旧不交A/B客户大小(6,24)、目标AAB，是原A1/B4全部×6。两银行组件分别marks(0,1)尺度5、marks(1)尺度4；输入完全在源码，不需要外JSON。第二层有先Y后bank的非前缀标记顺序。

`oldout(c)`递归保存可实现**终局计数**集合，阈值=max_A min_(child terminal)当前份额；保达到阈值的终局。`oldrho(i,A)`挑对旧当前人最低的真终局，再给每个有序孩子完整策略见证；非规定孩子独立取其最低终局。按oldnormal收益(3,3,24)，重算缺陷(5,9)。银行各自构造永久BI低退出表。

联合目录恰2×3×3=18主题。源码先列长度0/1/2的全部18元联合历史（1+18+324=343），找到前j位首次联合异常；**只改保险也重置旧坐标**到对应最低真孩子，所有分量一起进入各自永久策略。无异常用normal；不是从在轨表猜离轨，也不是仅逐坐标偏离。

然后把三坐标不交块显式展开为75个不同客户ID，每联合主题取对应块并。逐单位算终局负载、三人利润，343×18=6174比较含自身都断言非负；对18³=5832有序终局直接求覆盖最大。断言actual u=(17,21,33)、W71、OPT75、gap−67=旧30−60−(2·14+9)。D9,R14，异质损耗37、统一5D45；原输入gap已负，不是half反例种子。

输出含全部343条history→联合action完整表、尺寸/缺陷/费用/最小margin等。其73799B JSON与父方1136B JSON不同，不能同名合并或互当同一次运行；本程序的顶层定义即执行，静态读/AST检查没有运行这些断言。

## 父方75：独立有序集合与块份额表达

`parent/audit_heterogeneous_product.py`硬编码尺寸((6,24),(10,10,5),(8,8,4))，normal=((0,0,1),(0,1,0),(1,2,1))。旧全集`old_outcomes(h)`保**有序终局**，而非作者终局计数；同样用max-min阈值保存所有可实现终局并构造每个有序孩子policy。父方bank函数从首次退出后的每个前缀扫描是否第一次dirty，保持永久BI，目标F固定，不导作者函数。

其`player_payoff`直接用各不交整数块size/count的Fraction相加，不逐一循环75客户ID；这是同一个单位客户分区的精确聚合表达，不能称再次逐单位展开。两实现同18主题/343历史/6174联合比较及5832 OPT终局，独立输入表示与低退出实现保留，数学游戏相同不等代码SHA相同或新一次外审。

父方1136B原报告全文实际读，source_sha256=6870c2baf0adc700d3efb671590b37920ca1a6fccc8efd9c60e13c1c6eb1c5c5与当前6096B源精确同SHA，原Python3.12.14、最小IC margin0、passed true及全部参数吻合。它是**原报告内部**的源字节绑定，不是另已保存了命令、退出码、时长或stdout/stderr执行capture，更不表示当前重跑。作者73799B JSON所有标量与343个joint-history动作完整实读（联合标签9a+3b+c无损表示），没有sourceSHA字段；marked-bank11150B全部26条记录和总表也完整读，均cap1、minmargin0、all_passed true，但同样没有执行SHA/时长日志。它们只能保同冻结版本的原有限输出身份，不伪造旧执行元数据或升级全m证明。

## 复用与程序证据的限度

[完整原代码、正常show与输入/输出清单](../../../../tools/evidence/marked-bank-products-and-extra-theta-programs/source-manifest.json)保两个冻结版本、实际原件SHA/blob与本批阅读。marked-bank有限子树检查、作者逐单位产品、父方块表达产品各自作用清楚；原一般证明、原历史盲重构、目前知情源码清洗与原运行分开。没有新福利范围、代码认证外审或新颖性。若以后运行，必须固定同SHA原件/真实依赖/隔离sidecar，并分别记一次CLI与有限断言数量，不把6174比较叫6174次运行。
'''
put(P1,front('customer-attraction/marked-bank-and-two-unequal-deficit-product-original-audits','任意标记保险与两个不等缺陷产品的原审计','code-completely-reviewed; finite-original-evidence-preserved; no-new-execution','三个原实现全部输入/控制流/副作用与有限量词自足保：低退出累计历史、作者逐单位75与父方块表达75分开；全m证明另有现定理，0重复旧成功。',IDS[:3])+b1)
b2=r'''## 原程序及八个真实输入

5107B原程序全文实读，只有标准库argparse/itertools/json/Fraction/pathlib。它复现一次既有八证书theta-extra诊断，不生成客户、策略或新反例，不验证全SPE IC。输入恰PAIRS常量的八份examples JSON及八份certificates JSON，全部冻结字节已保存；客户JSON共13841B逐型全文读，包括每个topic label、人数、兴趣集合和重数。

证书加载顺序为strategy字段、否则certificate字段、否则自身；将所有actions读成history tuple→action字典，**随后只沿空历史恢复actual路径**，不核每个离轨动作理性。没有使用security原始/对偶、terminal_counts或expected福利字段来认证策略。它们仍随原件保存、全部元数据已实际读，不能把证书自己的scope声明当这次核验。

完整策略动作表不是只看root或条数。本批把全部8份共14352条有序history→action按相同后继子树无损去重，335个逐输入节点全部action/children实读，并展开roundtrip与每条原动作相等；其中三份六主题三人策略是同一函数，客户重数各不同。五人十主题证书11111条→215节点，五人七主题证书2801条→54节点；其他各43/43/43/21/259/31条分别13/13/13/8/11/8节点。此为**完整输入阅读表示**，只核字典域/无重复/动作范围及无损还原，不算新增SPE/安全值/原始对偶验证，不合并原策略不同有序历史。

## 定义、枚举与准确软件合同

给终局/静态背景B及主题T，源码按每兴趣型贡献Fraction(multiplicity,extra+Σ_(a∈B)1_(a喜欢该型))求和。actual收益extra0，因为玩家自己的那次行动已在B；额外查询extra1，背景有m个竞争主题，真实SPE仍原m人。

恢复actual路径后逐个主题取actual终局利润。枚举combinations_with_replacement(range(p),m)全部C(p+m−1,m)纯背景多重集，对每背景取全部p个查询的最大价，再取最小，恰纯静态ϑ_(m+1)。背景查询仅依计数，所以这样枚举没有将SPE policy限制成count-based。只在严格减小时更新witness，得到字典序首个最小背景。

每行stdout打印name/m/actual/all actual payoffs/theta/witness/minpay−theta，没有新JSON文件、没有全IC回放、没有优化混合安全值或完整真实菜单。`--repo-root`可显式指定；默认Path(__file__).resolve().parents[5]依原research/workspaces/.../direct相对位置找仓库，平移到散文件目录须传真实输入根，不能把找错文件失败冒数学反例。

## 八个原诊断对象与保留结果

以下为原已完成诊断记录，[既有资源](../资源/额外槽饱和势与真实偏离分支覆盖上界--资源.md)已保数学状态，本批没有重跑这些成功计算：

| name | m / 标签数 | 原minactual u | 原ϑextra | 原最小背景 |
| --- | --- | --- | --- | --- |
| individual_security_failure | 3 / 6 | 29/3 | 23/3 | (0,1,2) |
| aggregate_theta_failure | 3 / 6 | 10 | 15/2 | (0,1,2) |
| five_individual_security | 5 / 10 | 81/5 | 69/5 | (0,1,2,3,4) |
| local_security_increment | 3 / 6 | 95/3 | 51/2 | (0,1,2) |
| eight_cce_welfare_gap | 3 / 4 | 2 | 2 | (0,0,1) |
| dynamic_iid_local | 5 / 7 | 10 | 8 | (0,1,2,6,6) |
| root_tax_failure | 4 / 6 | 9 | 26/3 | (0,0,4,4) |
| worst_cce_welfare_failure | 3 / 5 | 3 | 11/4 | (0,0,4) |

actual有序路径从策略分别是(0,3,4)、(0,3,4)、(4,5,6,7,8)、(0,3,4)、(0,1,1)、(6,6,0,3,4)、(0,0,0,5)、(0,4,4)，不是上表静态最小背景，也不把名字中的CCE当当前SPE策略类型。原八输入无违不证明通用theta floor；eight例相等还排固定严格改善。当前银行族已反逐人extra theta，八旧阴性不能使其复活，聚合桥仍须另判断。

## 实际本批证据边界

原代码/16真实JSON与所有无损策略表示在[输入清单](../../../../tools/evidence/marked-bank-products-and-extra-theta-programs/actual-theta-true-input-manifest.json)。旧安全值、CCE原/对偶或动态iid附带字段虽完整实际读，**没有**因此被本程序使用或当前重新证明。0原CLI/旧成功复跑/新θ或SPE检查；不把本代码保存/语义审查叫重新八例PASS。既有精确表按原历史证据复用，没有此原脚本的已存运行元数据就不虚造execution SHA或当前时间。
'''
put(P2,front('customer-attraction/eight-stored-policies-exact-extra-slot-theta-reproduction','八旧策略的纯额外槽有理复算','source-and-all16true-inputs-completely-reviewed; historical-diagnosis-not-repeated','精确保8真实实例/完整ordered策略的实际读取、只actualpath非IC验证、全部m槽多重集Fraction查询与输出/根路径和背景区别；旧八例阴性不认证普遍theta。',[IDS[3]])+b2)
b3=r'''## 实际源码、模型与输入边界

3345B源码全文实读，依赖Python标准库及NumPy/SciPy linprog。本批环境元数据Python3.12.14、NumPy2.3.5、SciPy1.17.0；未import原模块，顶层会立即构造数据、解**四个LP**、写同名JSON并打印。0本批原CLI/求解调用，旧成功/阴性不重跑。

所有输入在源码：M3,K6标签、63个非空兴趣mask；MEM是63×6二元会员矩阵。root0，第二位首主题0/1/2后选3、首3/4/5后选0；末位选第二主题组里最小未用标签。43有序决策节点、每节点6个动作含自身，共258个真实IC行。L=lcm(1,2,3,4)=12，payoff按每类负载取L//load再除L，原IC系数来自完整策略真实后继而非冻结actual尾。

客户权重为63个非负实数、总量1。正重权可导致不同标签同覆盖；这里是必要IC的固定形式policy锥，不能未经有理化/单位化/标签合法化就叫原模型完整新反例。代码不输入任意实例、不给通用solver，也不枚举其他策略。

## 完整m槽与两个线性规划

实际叶Z=finish(())。对给定p，q_x=Σ_ap_aMEM_xa，prices[i,a,x]=q_x/[1+load_x(finish(Z[:i]+(a,)))]，包括固定actual过去、强制a、全部真后继共3槽；不是删掉当前槽的tail。

`test(p)`将Σ_iΣ_ap_a prices[i,a,x]−covered_x作为每客户目标系数。linprog最小化其负数，约束IC·w≥0、Σw1、w≥0，求Σ_i完整推送P_i−W的浮点最大。`uniform_budget(p)`另给每角色自由变量y_i，并对每a加y_i≤prices[i,a]·w；最小化covered·w−Σ_i y_i，等价最大Σ_i min_a g_p(Z_i(a))−W。后一锥不是逐位置Mfull，也不是只检查根。

仅两预选查询：p2=p5=1/2、其他0，及六标签均匀。每个p分别跑push与uniform，**一次CLI主体含4次linprog调用，不是4次独立原程序运行**。本批没有启动该主体。

所有res仅assert success；把x>1e−8的浮点权重用Fraction(float(x)).limit_denominator(10⁷)展示，没有再对有理化重数检查原IC、没有保存完整有理对偶，也不证明LP精确最优。源码中浮点成功与证书真值必须分开。

## 旧输出的用途与限制

1392B冻结输出全部字段实际读：两push gap为−0.125、−0.09104938271604927，uniform gap为−0.125、−0.09722222222222224。两push及均匀p的uniform输出都展示mask2/4/16/32各1/6、mask9为1/3；half-on2/5的uniform输出展示六个singleton masks1/2/4/8/16/32各1/6。仅两种显示权重，不意味着同一精确LP对偶或认证极值。负值只有限数值诊断，不认证该锥无违，更不证明一般FTA/Mpath或half。完整尾折扣与真实末两人reserve的解析合同见[既有资源](../资源/完整终局推送的自身折扣与末两位储备--资源.md)，这些数字没有替早期债付款。

源文件输出Path(__file__).with_suffix('.json')，会写源码旁。冻结JSON和代码同版本保存不等于有code-hash/版本/对偶的执行认证；若后来复现，只能独立复制原代码并记录NumPy/SciPy/调用次数及原四LP，不能覆盖原输出或调p后仍称原suite。此处0新LP/浮点probe/旧成功重演、0新目标反例，不把已假Mfull移成FTA或根Mpath失败，不认证新颖性或外审。
'''
put(P3,front('customer-attraction/fixed-three-player-full-terminal-two-query-float-probe','固定三人完整推送的两分布浮点探针','complete-code-and-embedded-input-audit; finite-float-results-not-certificates','固定43节点/258IC/63类型、两p四LP的完整m槽与自由逐角色菜单目标准确保；浮点weights有理展示未复核，无对偶或全域认证，顶层执行/sidecar副作用分开。',[IDS[4]])+b3)
js(E/'formal-resource-manifest.json',[{'path':p,'bytes':(S/p).stat().st_size,'sha256':sha((S/p).read_bytes())} for p in [P1,P2,P3]])
ompath=C/'learning-jz-frozen-output-original/actual-source-manifest.json';om=json.loads(ompath.read_text());outputs=[];frozen={}
for x in om['rows']:
 v=inv[x['id']];b=Path(x['local_path']).read_bytes();assert len(b)==v['size']==x['size'] and sha(b)==v['sha256']==x['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];cap=json.loads(Path(x['actual_normal_show_capture']).read_text());assert cap['source']==v and cap['output']==x['local_path'];q=E/'frozen-original-outputs'/x['id']/x['path'];cp(x['local_path'],q);cp(x['actual_normal_show_capture'],E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name);outputs.append({**v,'preserved_path':str(q),'read_mode':'actual allfields/26markedrecords/343authorjointactionrows/fullparenthashreport/full4floatingLPfields read; author343 exactbijection9a+3b+c allrows actuallyread, notnewIC/audit execution'});frozen[x['id']]=json.loads(b)
assert len(outputs)==4 and sum(x['size'] for x in outputs)==87477
js(E/'frozen-output-manifest.json',outputs);cp(ompath,E/'actual-normal-show-frozen-output-manifest.json')
parent=frozen['06068e36ffe4499b4538'];author=frozen['11e83f89dec391d5b2fe'];bank=frozen['48a2a60361a45c8678ed'];probe=frozen['0833067167a458cefed7'];assert parent['source_sha256']==inv[IDS[2]]['sha256'] and parent['passed'] and parent['python']=='3.12.14';assert 'source_sha256' not in author and 'source_sha256' not in bank and 'source_sha256' not in probe
enc=lambda a:9*a[0]+3*a[1]+a[2]
rows=[{'history_joint_labels':[enc(a) for a in r['history']],'action_joint_label':enc(r['action'])} for r in author['actions']]
assert len(rows)==343 and all(set(r)=={'history','action'} for r in author['actions'])
def dec(a):return [a//9,(a%9)//3,a%3]
assert [{'history':[dec(a) for a in r['history_joint_labels']],'action':dec(r['action_joint_label'])} for r in rows]==author['actions']
js(E/'frozen-output-reading/author75-all343-joint-policy-lossless.json',{'schema':'exactreadingbijection-not-new-SPE-audit','source_id':'11e83f89dec391d5b2fe','source_sha256':inv['11e83f89dec391d5b2fe']['sha256'],'encoding':'jointlabel=9old+3bank1+bank2; inverse=(label//9,(label%9)//3,label%3)','all_nonaction_fields':{k:v for k,v in author.items() if k!='actions'},'all_policy_entries':rows,'roundtrip_exact':True})
js(E/'frozen-evidence-binding-and-runtime-boundary.json',{'parent75':{'report_id':'06068e36ffe4499b4538','report_source_sha256':parent['source_sha256'],'original_code_sha256':inv[IDS[2]]['sha256'],'same_exact_source_sha':True,'original_report_python':parent['python'],'original_passed_field':parent['passed'],'independent_execution_argv_returncode_elapsed_capture_present':False,'new_run':False},'other3outputs':{'frozen_co_version_size_SHA_blob_verified':True,'execution_source_sha_field_present':False,'independent_execution_log_present':False,'author75_all343_andbank26_records_actually_read':True,'probe_values_are_float_candidates_not_exact_dual_or_universal_certificates':True},'theta8':{'prior_exact_table_preserved':True,'original_script_executed_by_this_batch':False,'saved_same_SHA_originalCLI_stdout_or_execution_metadata_claimed':False},'current_available_versions_not_execution':{'python':'3.12.14','numpy':'2.3.5','scipy':'1.17.0'},'actual_new_originalCLI_runs':0,'original_module_imports':0,'new_LP_BI_random_or_SPE_runs':0,'old_success_replays':0})
coverage=[{'id':IDS[0],'disposition':'integrated','targets':[P1,PH],'units':['fullsource imports/functions/memo/countpayoff/normalpolicy/BI tiepriority','all marks normal-prefix forcedchild modeBI/Y/F/permanentBI allordered repeatedhistory IC/cap','mainm2to5 nonemptymarks excludeslast/26games518children/15353cumulative notunique/75913including self','sourcewith_suffixJSONsideeffect only__main__/allm proofelsewhere','fulloriginal26records read/cofrozen hashnotexecutionlog/no sourceSHA/no newrun']},
{'id':IDS[1],'disposition':'integrated','targets':[P1,PH],'units':['embeddedold6,24/targetAAB/j2/twolayers{01}5,{1}4/18jointactions','oldoutcountsets maxminthreshold/truetargetoldrho fullorderedwitness/deficits5,9','bankclean order/F target/Ycap/BIpermanent codedallbranchways','firstjointanomaly includesonlyinsurance resettingallcoordinates/343fulljointpolicy','actual75distinctcustomerIDs/loadFraction/utilities all6174including self/5832OPTprofiles/assert17,21,33W71O75gapminus67/cost37vs45','top-levelmathbodyandJSONsideeffect/importnotread-only','all73799Bsourceoutput fields343actions read viaexactjointencoding/notnew execution orhashedreport proof']},
{'id':IDS[2],'disposition':'integrated','targets':[P1,PH],'units':['independentfixedSIZES/NORMAL/BANKS oldorderedoutcomes vsauthorcountoutcomes','fulloldpolicy floor/witness product firstexit includesinsurance-only','permanentBI scanallpostexitprefixes originalF target/18actions/343hist6174comp','integerblockFraction shares equivalentunitmodel notsecondexplicit75customerloop','OPT5832/assertallpayoffs/size/di/cost fixedsinglefinitecase notallm','top-levelruns/writesJSON no import','original1136report fullread sourceSHA exactlymatches6096code/Python3.12.14/passed/min0 notindependentargvexitcodetimecapture/notcurrentexecution']},
{'id':IDS[3],'disposition':'integrated','targets':[P2,PE],'units':['wholecode PAIRS exact8input8cert filenames pluswrapperselection allsourcefields read','full8instances alltopics/m/type/multiplicity actualread13841B','full8policy14352entries allnonactionmetadata actualreadlossless335nodes/roundtrip/domain/duplicatefieldcheck no extraJSONsource done','orderedactualpath only/minactualpay exactFraction vsstaticmcompetitor extra1','allbackgroundmultisets C(p+m-1,m)/allpqueries/no strategycountrestriction/tiefirstlex','stdoutonly8rows/defaultrootparents5/explicitrepo-root no filewrite/argparse mainonly','all8prior theta/witness/minpay/sourceactualpaths preserved/noSPEsecurityCCEcertcheck or globaltheorem/newrun']},
{'id':IDS[4],'disposition':'integrated','targets':[P3,PM],'units':['fullsource imports numpy/SciPy/63nonemptymasksMEM/typeweightsnormalizedreals/fixedM3K6complete43nodes','allIC258including self exactintegerL12thenfloat/finish truebranches/actualpast intact','full3slotkernel q/(1+loads)/push einsumsumroles exactLPexpression','uniform66vars y_i<=all6columns freelysign/ymin perrole notfixedroot/freeMfull','twofixedp half2,5 anduniform6/4solvercalls perbody0thisbatch','assertsuccessonly/threshold1e-8/Fractionfloatlimit1e7 notexactICrecheck/dualnotstored','sidecarJSON/toplevelrun/sourcefloatoldweights2patterns/all4negativevalues fullread notpositivecertificate or FTA/Mpathfalse','versionsavailable metadata only no originalimport/CLI/LP/negative-suite rerun']}
]
js(E/'semantic-coverage-map.json',coverage)
readsummary=json.loads((C/'jz-input-reading-prework/summary.json').read_text());scope={'primary_sources':5,'primary_bytes':25341,'primary_lines':sum(x['lines'] for x in primary),'actual_primary_read':'all5sourcecode fulltext in2complete batches afterRootnormalshow SHA/capture verified; beforeactualclaim allowedprep, finalreceipts onlyafteractual12claim ownerSHA','true_theta_inputs':16,'true_theta_input_bytes':sum(x['size'] for x in inputs),'full_instance_JSON_bytes':sum(x['size'] for x in inputs if x['path'].startswith('examples/')),'certificates_all_nonaction_metadata_read':True,'all8policy_read_representations':readsummary,'all_policy_entries':sum(x['all_entries'] for x in readsummary),'sum_per_input_unique_subtrees_actually_read':sum(x['DAG_nodes'] for x in readsummary),'input_reading_dedup_program_executions':1,'input_dedup_roundtrip_is_not_SPE_theta_security_CCE_verification':True,'frozen_outputs':4,'frozen_output_bytes':87477,'frozen_outputs_all_fields_read':True,'frozen_author75_policy_rows_actually_read':343,'new_formals':3,'dispositions':{'integrated':5},'new_theorems_game_instances_or_independent_reviews':0,'new_math_program_runs':0,'original_math_CLI_calls':0,'original_module_imports':0,'new_LP_BI_random_SPE_theta_runs':0,'old_success_replays':0,'sameSHA_parent_report_binding_not_execution_log':True,'theta_originalCLI_saved_execution_metadata_claimed':False,'metadata_reader_preflight_abort':{'count':1,'cause':'normalshowcapture source.id nested, initialreader expected topid; KeyError before sourcecode print or any originalbody; correctedmetadatareader then verifiedall5','original_program_execution':False},'helper_calls_in_JZ':1,'local_blob_attempts_in_JZ':20,'local_exports_in_JZ':16,'local_missing_blobs_in_JZ':4,'earlier_JU5code_missing_preserved':True,'missing_retry_or_network_fallback_calls':0,'Root_separate_normalshow_origins':9,'own_clean_show_calls':0,'raw_claim_ids':len(claim['ids']),'primary_claim_intersection':IDS,'claim_projection_performed':False,'shared_Git_writes':0,'claim_done_checkpoint_calls':0,'network_or_lazy_fetch':0,'real_board_account_auth_operations':0,'phase3_graph_import':0,'derived_packaging_builder_calls':1,'derived_packaging_builder_failures':0}
assert scope['full_instance_JSON_bytes']==13841 and scope['all_policy_entries']==14352 and scope['sum_per_input_unique_subtrees_actually_read']==335
js(E/'read-scope-and-evidence-status.json',scope)
notes=[('4931B源码全部imports/辅助函数/BI缓存/模式/永久退出/完整递归IC/全main及JSON副作用实际全文读，原11150B26条输出全字段读。','现异质定理与原marked实现逐项比，真实全部normal-prefix forcedchild及alllaterordered范围准确，15353/75913是低退出审计累计不冒单树unique；原co-version输出没有sourceSHA或独立运行日志。','integrated：自足程序保实际输入域/控制流/有限断言/副作用与原输出真实身份，0新math/原CLI/旧成功复跑；不以26游戏外推全m或把函数定义静态读叫main执行。'),
('5862B作者75源码全部顶层逻辑/oldout/oldrho/bank/fulljoint构造/逐单位检查/完整OPT枚举/报告写入全文读，73799B原JSON全部元数据与343条联合history/action无损编码逐行读。','与现编译及父方另一实现比较，作者终局计数集合、75显式客户ID、18主题/343/6174/5832与全坐标首次退出逻辑全部保；两source不同SHA/表示，旧原JSON不假绑未存executionSHA。','integrated：新程序对象保这份完整实现而非再造同定理/实例。source顶层执行，未import或复跑；源码/真实内置输入/全部输出保，旧有限断言非一般half/全m认证，0额外doneJSON。'),
('6096B父方源码从imports至JSON/print全部实际读，1136B原输出所有字段读并核其sourceSHA和Python。','父方ordered旧终局集合/独立permanentBI重构、整数不交块Fraction份额与作者逐单位实现分别归位；同75游戏/18主题/全部343节点6174比较/5832OPT有限域准确，原内部report sourceSHA6870...与当前代码精确一致。','integrated：准确复用原passed报告内部hash绑定，不伪造历史argv/退出码/时间/stdout日志或当前run；不称父方也逐一遍历75客户，不把同输出当同代码或新外审，0重复旧成功。'),
('5107Btheta原程序全部PAIRS16路径/包装选择/有序路径/utility额外槽/背景枚举/print/parser/defaultroot全文读；8真实客户JSON13841B全型实读，8证书所有非动作字段及完整14352动作无损335节点全读。','同原数学稿/现JH八例表与当前银行状态比对，程序只actualpath+纯extra theta，不核全IC/附带security或CCE对偶；静态多重集与ordered策略不同，原背景witness与actual路径分别完整保。','integrated：自足可复现输入/接口/副作用及范围，0新原CLI或重算八旧成功；未存该脚本executionSHA/stdio就不杜撰，数据无损roundtrip为阅读结构检查不是SPE证书，0额外done16JSON。'),
('3345Bprobe全部固定policy/63typesMEM/IC和kernels/test/uniform/两p/顶层fourLP/输出全文读；1392B原结果所有字段、四gap与两类weights完整实读。','精确重构push/uniform目标与约束、258含self比较/完整3槽/总质量1，不混删当前槽或Mfull；展示weights只是浮点转Fraction未IC复核，未存有理对偶或执行版本，原当前依赖版本仅可用性元数据。','integrated：自足软件合同与有限浮点身份，不把负值当锥或全域认证，不因输入暂缺重跑原阴性，0原import/CLI/LP/数学run；不扩任何half/Mpath反例或canonical求解器认证。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 原12ids真实pushed/synced claim与本5owner/sourceSHA核，保完整原capture不伪投影。','comparison_note':b,'decision_note':c,'disposition':x['disposition'],'targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(E/'README.md',r'''# JZ五原程序完整清洗

五源码25341B实际全文/全部输入输出副作用读，5integrated，3自足程序对象。Root正常show5code+4frozenoutputs九原capture全保；此前本地5code缺失/另一次20依赖16齐4output缺失均原字节并存，不倒填当时可取。

8真实实例JSON13841B全文读，8证书全部非动作字段/14352history-actions经可全还原335个逐输入子树节点完整实读、roundtrip等原每条动作；这是一项阅读表示检查，不是SPE/θ/security/CCE新验证。4原输出87477B全部字段实读，含26marked记录、作者75全部343联合动作；父方旧sourceSHA精确匹配当前程序，但没有独立保存的历史命令/退出码/时长capture，不能叫它存在。

0本批原模块import/原CLI/LP/BI/随机/θ/SPE/旧成功复跑。marked累计子树节点不当全树unique；作者显式逐单位/父方块Fraction75实现分开，顶层程序不能import当只读。theta只actualpath/静态extra枚举，probe两p四floatLP无精确对偶，输入源码读取不升级一般数学。

所有原件、真实依赖、旧输出、阅读表示、准确SHA与逐源处置自足保。Root先推正文与证据再done；不额外done16输入/4输出，不改冻结历史/旧页，无sharedGit/账号公屏/mapper。
''')
put(W/'relation-review.md',r'''# 阶段二关系

三个保险程序是同一已证全树编译的不同有限实现合同：marked强制低退出子树累计、作者75完整单位客户展开、父方75独立有序/块表达，各自source与输出绑定不能按同名/同数合并；全m真值由现解析定理承担。原co-version输出、原内部sourceSHA绑定和外部执行日志是三个命题，后者没有就不声称有。

theta程序的真正输入是16个固定JSON；完整policy数据已无损实读，但代码只用actual路径并枚举纯静态m槽extra背景，不核全IC或原安全/CCE对偶。读完整证书不等重新认证那些字段。八旧阴性不复活已被银行否定的逐人桥，亦不自动反聚合/half。

probe保固定标签策略锥与两p四LP；必要IC+浮点有理显示未给完整单位SPE/精确duals。complete-slot/del-current-slot、perrole自由菜单/rootMfull/全路径Mpath不同，不能以一个旧失败或负诊断跨域付款。0新数学运行、无外审/新颖性，0额外done引用输入输出或旧图导入/强制连通。
''')
# Actual three nextmath sources were already fully read as authorized JU prework, notyetprimary.
preworkpath=C/'ju-next-math-prework/reading-status.json';pre=json.loads(preworkpath.read_text());nextrows=[]
for x in pre['rows']:
 v=inv[x['id']];b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'];q=REPO/'cleanup/progress'/f"{x['id']}.json"
 if not q.exists():nextrows.append({**v,'local_path':x['local_path'],'progress_observed':None,'read_status':'actual fullprework source read already, notprimary; preserve givenread_note, no fakereread/receipt/newclaim','read_note':x['read_note']})
cp(preworkpath,E/'actual-next-math-prework-reading-status.json');js(W/'next-candidates.json',nextrows);cp(C/'local_blob_export.py',E/'authorized-local-export-helper.py.txt');cp(Path(__file__),E/'build_delivery.py')
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
def tb(s,l,r):
 def count(d):return sum(ord(s[i])==92 and s[i+1]==d and (i==0 or ord(s[i-1])!=92) for i in range(len(s)-1))
 return count(l)==count(r)
for x in primary+inputs+outputs:
 b=(S/x['preserved_path']).read_bytes();ck('exactsourceSHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('exactsourceblob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('raw12claim preserved',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes() and len(claim['ids'])==12);ck('actual5subsetownerSHA',set(IDS)<=set(claim['ids']) and all(x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[x['id']]['sha256'] for x in owners));ck('actualclaimpushedsynced',claim['status']=='pushed' and claim['local_sync']['status']=='synced' and claim['local_sync']['remote_tip']==claim['remote_tip'])
for x in contexts:ck('contextreadSHA '+x['path'],len((S/x['snapshot']).read_bytes())==x['bytes'] and sha((S/x['snapshot']).read_bytes())==x['sha256'])
ck('parentold_internalhash_not_externalexecutionlog',parent['source_sha256']==inv[IDS[2]]['sha256'] and parent['passed'] and parent['python']=='3.12.14' and parent['ordered_decision_histories']==343 and parent['all_joint_action_comparisons_including_self']==6174 and parent['terminal_profiles_for_OPT']==5832);ck('bankold26allrecords',len(bank['records'])==bank['bank_games']==26 and bank['exit_children']==518 and bank['ordered_decision_histories']==15353 and bank['all_action_comparisons']==75913 and bank['all_passed']);ck('authorold343policyand75',len(author['actions'])==343 and author['customers']==75 and author['topics']==18 and author['actual_payoffs']==['17','21','33'] and author['W_new']==71 and author['OPT_new']==75 and author['half_gap']==-67);ck('author343readingencoding_roundtrip',[{'history':[dec(a) for a in r['history_joint_labels']],'action':dec(r['action_joint_label'])} for r in rows]==author['actions']);ck('otheroutputsnohashorlog',all('source_sha256' not in x for x in [bank,author,probe]));ck('probeold4floatvalues_scope',probe['all_history_IC']==258 and probe['types']==63 and len(probe['push'])==len(probe['uniform'])==2 and all(x['gap']<0 for z in ['push','uniform'] for x in probe[z]))
ck('all16inputs8instances13841B',len(inputs)==16 and sum(x['size'] for x in inputs if x['path'].startswith('examples/'))==13841)
for x in readsummary:
 d=json.loads((S/E/'lossless-policy-reading'/(x['name']+'-policy-dag.json')).read_text());ck('full_losslesspolicyreading '+x['name'],d['roundtrip_exact'] and len(d['nodes'])==x['DAG_nodes'] and d['all_history_entries']==x['all_entries'] and d['source_entry_extra_keys']==[])
ck('full14352entries335perinputnodes',sum(x['all_entries'] for x in readsummary)==14352 and sum(x['DAG_nodes'] for x in readsummary)==335);ck('zero mathbody originalCLI oroldreplays',scope['new_math_program_runs']==scope['original_math_CLI_calls']==scope['original_module_imports']==scope['new_LP_BI_random_SPE_theta_runs']==scope['old_success_replays']==0);ck('local20dep16ok4missingretained',len(im['rows'])==16 and len(im['missing'])==4 and scope['helper_calls_in_JZ']==1 and scope['missing_retry_or_network_fallback_calls']==0)
links=[]
for p in [P1,P2,P3]:
 t=(S/p).read_text();ck('flatMATEK '+p,all(re.search('^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']));ck('formalC0zero '+p,not any(ord(x)<32 and x!='\n' for x in t));ck('formaltrailingzero '+p,all(l==l.rstrip() for l in t.splitlines()));ck('actualTeXbalance '+p,tb(t,'[',']') and tb(t,'(',')'))
 for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://' in dest or dest.startswith('#'):continue
  n=posixpath.normpath(str(Path(p).parent/dest.split('#',1)[0]));q=S/n if (S/n).exists() else REPO/n;ck('link '+dest,q.exists());links.append({'source':p,'destination':dest,'resolved':n,'bytes':q.stat().st_size,'sha256':sha(q.read_bytes())})
js(E/'formal-link-check.json',links)
t1=(S/P1).read_text();t2=(S/P2).read_text();t3=(S/P3).read_text();ck('finitebanksnotuniqueallm','各低退出孩子审计累计' in t1 and '不是另已保存了命令' in t1 and '原CLI' in t1);ck('two75representationsdifferent','有序终局' in t1 and '不逐一循环75客户ID' in t1 and '只改保险' in t1);ck('theta_datareading_notSPE','335' in t2 and '14352' in t2 and '不算新增SPE' in t2 and '只沿空历史恢复actual路径' in t2);ck('probe4LPnot4runs','四个LP' in t3 and '不是4次独立原程序运行' in t3 and '没有保存完整有理对偶' in t3);ck('all5receiptsintegrated',len(receipts)==5 and {x['id'] for x in receipts}==set(IDS) and all(x['disposition']=='integrated' for x in receipts))
for x in receipts:ck('completereceipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']) and all((S/p).exists() or (REPO/p).exists() for p in x['targets']))
ck('exact3formal',set(str(p.relative_to(S)) for p in (S/'archives').rglob('*.md'))=={P1,P2,P3})
for x in nextrows:ck('actualnextfullreadbyteavailable '+x['id'],sha(Path(x['local_path']).read_bytes())==x['sha256'] and not (REPO/'cleanup/progress'/f"{x['id']}.json").exists())
obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:u=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen=any('/'+z+'/' in rel for z in ['original','related','context','true-input-repository','frozen-original-outputs']);bad=[i+1 for i,l in enumerate(u.splitlines()) if l!=l.rstrip()];c0=[{'offset':i,'code':ord(c)} for i,c in enumerate(u) if ord(c)<32 and c!='\n']
 if bad or c0:obs.append({'path':rel,'frozen':frozen,'trailing_lines':bad,'nonLF_C0':c0})
ck('allnewderivedC0trailingzero',not any(not x['frozen'] for x in obs));js(E/'transport-format-observations.json',{'observed':obs,'frozen_original_input_output_context_unchanged':True})
put(W/'delivery.md',f'''# JZ交付

5primary25341B/{scope['primary_lines']}行完整实读；16真实theta输入{scope['true_theta_input_bytes']}B（客户JSON13841B全型、14352策略条目无损335子树全读）及4原输出87477B全部语义实读。5integrated、3自足程序对象；0新数学程序/原CLI/import/LP/BI/随机/θ/SPE或旧成功复跑。输入表示reader1次只是无损阅读/结构roundtrip，非数学SPE认证。

原12ids claim{claim['remote_tip']}实际pushed/synced保原字节，本5owner/sourceSHA核。Rootnormalshow5源码+4输出独立新capture与初次5code missing/另20依赖16齐4outputs missing并存不改旧历史。父方75原报告sourceSHA强绑当前code/Python，仍无独立命令/退出码/时长capture，不捏造日志；其他co-version输出无执行SHA不强绑。

原26累计子树统计、作者75逐单位/父方块Fraction、theta只actualpath和extra枚举、probe一次主体4LP无对偶皆准确保。下一{len(nextrows)}源共{sum(x['size'] for x in nextrows)}B已有全文预读但未primary，无预claim/receipt。Root先推正文依赖再done，0sharedGit/账号公屏/mapper，16input+4output不额外done。
''')
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'relative_links':len(links),'formal_nonLF_C0':0,'formal_trailing_whitespace':0,'scope':'completeoriginalcode/actualallinputsemanticreading/frozenreporthashbinding/rawclaimowner/coverage/links/format/transport','mathematics':'0newverificationruns; datareading losslessDAG andencoding roundtrip do notprove SPE/LP/globalhalf; oldreportinternalhash isnotexternalexecutionlog'})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':25341,'primary_lines':scope['primary_lines'],'true_theta_input_bytes':scope['true_theta_input_bytes'],'frozen_output_bytes':87477,'new_formals':3,'formal_bytes':sum((S/p).stat().st_size for p in [P1,P2,P3]),'receipts':5,'dispositions':{'integrated':5},'checks':len(checks),'relative_links':len(links),'new_math_runs':0,'new_original_CLI_runs':0,'old_success_replays':0,'raw_claim_ids':len(claim['ids']),'claim_tip':claim['remote_tip'],'next_candidates':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
