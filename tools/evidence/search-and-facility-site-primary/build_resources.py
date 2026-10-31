from pathlib import Path
import hashlib,json,os,shutil
S=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-search-and-facility-site-primary')
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=S/'tools/evidence/search-and-facility-site-primary'
W=S/'cleanup/workspaces/Boss4/r3-search-and-facility-site-primary-next'
W.mkdir(parents=True,exist_ok=True)
sources=json.loads((E/'source-manifest.json').read_text())
deps=json.loads((E/'dependency-manifest.json').read_text())
byid={d['id']:d for d in sources+deps}
def dump(p,d):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
ctx=json.loads((E/'context-manifest.json').read_text())
p='archives/customer-attraction/state/审查/总税搜索与首步桥增量证据--审查.md'
b=(R/p).read_bytes();q=E/'context'/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
if not any(x['path']==p for x in ctx):ctx.append(dict(path=p,saved_path=str(q.relative_to(S)),bytes=len(b),sha256=sha(b),read_status='complete actual formal text read; CAG search domain/minimum/canonical-confirm scope compared; related only'))
dump(E/'context-manifest.json',ctx)
comparisons=[]
for name,sid in [('five-site-full','66a6e2d9e62086d6d517'),('five-site-edges','6ca35d47c4014c6a1361')]:
 old=json.loads((S/byid[sid]['saved_path']).read_text());new=json.loads((E/'runs'/f'{name}-report.json').read_text())
 dif=[k for k in sorted(set(old)|set(new)) if old.get(k)!=new.get(k)]
 assert dif==['elapsed_seconds']
 comparisons.append(dict(name=name,old_id=sid,old_sha256=byid[sid]['sha256'],new_report_sha256=sha((E/'runs'/f'{name}-report.json').read_bytes()),differing_keys=dif,all_other_fields_equal=True,old_elapsed_seconds=old['elapsed_seconds'],new_report_elapsed_seconds=new['elapsed_seconds'],old_code_SHA_binding_absent=True,new_original_CLI_count=1))
dump(E/'new-old-report-comparison.json',comparisons)
# This digest preserves every source-specific numerical result, with the raw JSON retained.
domains={}
for sid in ['912c92b9572c9c92ca11','79d0b8c76eebaca202fa','c26e8f18cc84a854a492','66a6e2d9e62086d6d517','6ca35d47c4014c6a1361']:
 d=json.loads((S/byid[sid]['saved_path']).read_text())
 domains[sid]=dict(raw_sha256=byid[sid]['sha256'],all_original_fields_semantically_read=True,read_note='All metadata, actual generators, inputs, every stage/case/result/layout factor and limits read in full; recursive field traversal separately records structural coverage, not a proof.',report=d)
dump(E/'finite-domain-readback.json',domains)
paths=[
 'archives/customer-attraction/state/资料/全历史纯SPE终局搜索的递推与有限证据--资料.md',
 'archives/facility-games/state/资料/四地点两设施精确支持审计的完整合同--资料.md',
 'archives/facility-games/state/资料/五地点硬度审计的支持区间与完整续局--资料.md']
def link(target,origin):return os.path.relpath(target,Path(origin).parent).replace(os.sep,'/')
def render(i,ident,title,summary,ids,body):
 p=paths[i];refs=[]
 for sid in ids:
  d=byid[sid]
  for x in d['sources']:
   ref=f"source:{x['commit']}:{x['path']}"
   if ref not in refs:refs.append(ref)
 head='---\n'+''.join(f'{k}: {json.dumps(v,ensure_ascii=False)}\n' for k,v in dict(id=ident,kind='resource',type_tag='资料',title=title,status='source-complete-finite-scope',summary=summary).items())
 head+='source_refs:\n'+''.join('  - '+json.dumps(x,ensure_ascii=False)+'\n' for x in refs)+'---\n\n'
 body=body.replace('§',chr(92))
 for sid,d in byid.items():body=body.replace('@'+sid,link(d['saved_path'],p))
 body=body.replace('@E',link(str(E.relative_to(S)),p))
 for j,t in enumerate(paths):body=body.replace('@P'+str(j),link(t,p))
 for x in ctx:body=body.replace('@CTX'+x['path'],link(x['path'],p))
 out=S/p;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(head+body)
 return p
render(0,'customer-attraction/all-history-terminal-search-resource','全历史纯SPE终局搜索的递推与有限证据',
'实读329行独立整数搜索及全部27136实例报告；保所有历史纯SPE终局的精确递推、13阶段生成域与5/9实例，复用同SHA成功，不把有限无反例或13次旧规范交叉检查扩成六人一般半覆盖。',
['4a0a68157e801a180ce5','912c92b9572c9c92ca11'],
"""# 全历史纯SPE终局搜索的递推与有限证据

## 研究对象和实际资源

[原程序329行](@4a0a68157e801a180ce5)是独立整数搜索器；[全部历史报告](@912c92b9572c9c92ca11)含27136个输入的阶段汇总、每阶段最坏输入与其全部SPE终局、13次规范递推交叉比较，未保存27136份完整逐例策略。程序16033B、SHA为46cf6d23d6b7e5d8490b4726fd9c1111641196ec77420ecb8e16dbaa4653e2d6，两个冻结分支字节相同。本页把本次正式程序源与此前已整理报告绑定；报告本身及四个规范包依赖只作已读比较，不额外完成它们。

模型是有限单位客户、共同非空主题目录、m名单位提供者观察全部有序历史后依次选主题。客户只在终局覆盖自己的提供者之间均分。类型重数是可展开的单位客户数，不是设施模型的战略原子权重。k个主题的非空兴趣mask按1至2^k−1排序，允许重数0、空主题、重复选择和零客户；空兴趣客户不在数组中，其删除不改变收益或覆盖最优值。本体整数断言要求数组长度正确、每项type为int且非负，拒绝True；CLI只使用下述生成域，不宣称对任意非法k、m提供完整输入校验。

当前六人问题还量化任意有限目录、任意客户数、所有完整历史纯SPE及任意离轨平局。本程序对所给有限输入精确求所有可能终局；这与只在每个计数选一条全局tie rule不同，也不直接输出完整有序历史策略证书。

## 整数几何、收益和全SPE递推

geometry枚举各层非负计数组合c，|c|从0至m；终局q满足|q|=m。设L=lcm(1,…,m)，兴趣集合I的终局覆盖者数d_I(q)=Σ_{a∈I}q_a。每名选择a的提供者的L倍收益为

§[
P_a(q)=§sum_{I§ni a,§,d_I(q)>0}w_I§frac{L}{d_I(q)}.
§]

每个非零分母至多m，故全部收益比较确为整数；福利为Σ_{d_I(q)>0}w_I。叶集合同时给出最大m主题覆盖值：允许重复和空主题时，任意至多m主题解可补至恰m次选择。因此OPT取所有叶的最大福利，非均衡最优值。OPT=0时报告比值约定为1，未执行0/0。

在叶上E(q)={q}。在计数c，令

§[
T(c)=§max_b§min_{r§in E(c+e_b)}P_b(r),§qquad
E(c)=§bigcup_a§{q§in E(c+e_a):P_a(q)§ge T(c)§}.
§]

必要性：若当前选择a并实现q，则它的收益必须不小于每个偏离分支所指定SPE续局收益，因而不小于各分支最低可实现值的最大值。充分性：对每个未选分支b独立指定一个实现其最低收益的SPE，再在选定分支实现q；不等式保证当前行动最优。由有限树归纳得到完整历史纯SPE。

相同计数的子局具有相同可实现终局集合，故缓存按计数合法；这不要求两个不同有序历史使用同一续局。未选分支在树上不同，允许分别指定，正是保全离轨平局的关键。算法保留所有可实现终局计数，而非声称终局可唯一恢复某份完整策略。动作置换轨道代表只对输入重数向量去重，不把均衡策略强行对称化。

residual(q)是该终局未覆盖客户在单一主题中的最大数；residual_bad检验是否有已占用主题a满足P_a(q)<L·residual(q)。若命中，记录该实例内按客户总数/终局/action排序的一个见证。主循环只在客户数严格小于当前首记录时插入并最多保留10条；它不是所有坏例清单，也不保证全局最小坏例。此次真实报告residual_lemma_counterexamples为空，不能描述成“已经找到该引理反例”。

## 实际27136输入及生成规则

报告seed=20261009、random_per_size=600、skip_tiny=false、confirm=true、extended=true；扩展随机种子为10·seed+1=202610091。有限域及每阶段最小比为：

| 域 | 数量 | 最小比 |
|---|---:|---:|
| k=3，重数0至2全部动作置换轨道；m=3,4,5 | 1485 | 2/3 |
| k=4，重数0或1全部动作置换轨道；m=3,4,5 | 5976 | 2/3 |
| 随机k=4；m循环3,4,5 | 600 | 29/38 |
| 随机k=5；m循环3,4,5 | 600 | 83/106 |
| 随机k=6；m循环3,4,5 | 600 | 217/269 |
| 扩展k=3,m=8 | 4000 | 33/38 |
| 扩展k=4,m=6 | 4000 | 129/151 |
| 扩展k=4,m=8 | 4000 | 15/17 |
| 扩展k=5,m=6 | 3000 | 123/146 |
| 扩展k=6,m=6 | 1500 | 55/63 |
| 扩展k=7,m=5 | 1000 | 268/309 |
| 扩展k=7,m=6 | 300 | 733/813 |
| large-versus-disjoint-small结构族 | 75 | 5/9 |

普通随机的四种模式轮换：独立30%概率非零且重数0至20；从(0,0,0,1,2,3,5,8,13,21,34)抽重数；只向单元素/双元素兴趣集给1至30；只向单元素/(k−1)元素兴趣集给1至50。扩展样本用密度0.09、0.2、0.5及条件重数0至100。结构族对m∈{3,4,5}、small∈{1,2,3,6,12}、delta∈{−2,−1,0,1,2}，取m+1个互不相交主题：大主题max(1,m·small+delta)客户，其余m个各small客户。全部真实重数/阶段最坏终局值保存在原JSON和[完整读取回录](@E/finite-domain-readback.json)，此表不代替已实读的逐字段原件。

## 5/9见证及其完整策略解释

最小比实例有k=6、m=5、10个客户：主题A有5名私有客户，另外五个互不相交主题各1名。全选A福利5，而选择A和四个小主题福利9，所以比为5/9。报告精确终局集合是全5人在A，或4人在A且1人在某一个小主题，共六个计数。这里不是六名提供者的反例。

可直接补出不依赖机器扫描的完整策略解释：在每个有序历史后都选A。跟随时最终A提供者数至多5，当前收益至少1；偏到任意小主题，客户总量仅1，偏离收益至多1。于是每个历史都满足最优回复，包含平局，是完整历史纯SPE。该说明是对已读实例的本页推导，原报告存的是终局集合，不是这份字面全树策略。

它给出一般半覆盖界上方的有限坏比见证。27136个输入均未发现half violation，亦未发现residual不等式反例；这些失败搜索不证明两个全称命题，也不给任意六人输入的5/9普遍下界。

## 证据绑定、CLI和可接续用途

原报告的audit_script_sha256正好绑定当前46cf…程序，status为completed，记录耗时34.784秒及base_git_commit=e111593b3212cc56474c298ff1284dbdd7cca010。因此本批复用这份成功，新增原CLI运行0次。程序核心无项目导入；仅--confirm动态使用customer_attraction规范包。四个现有规范包文件已按inventory字节归档并按此前同SHA全文阅读复用，但旧报告未列这四个当时源SHA，所以不把13次旧比较升级成对当前整栈的新运行认证。

--confirm只检查13个阶段各自最坏记录，并在有保留residual坏例时另检查首例；本次没有后一例。13个root outcome sets全部相同，不是对27136个输入都运行了规范求解器。程序输出多条阶段JSON进度，最后输出简化summary；完整JSON由--output保存，不能把整段stdout当单个JSON解析。目标已存在会在计算前拒绝；后续mkdir和write_text不是原子排他写。Git rev-parse HEAD只用于后置基线元数据，本批没有执行它。

[先有报告审查](@CTXarchives/customer-attraction/state/审查/总税搜索与首步桥增量证据--审查.md)正确保留有限5/9和一般half缺口。本页新增程序本体、真实生成域、递推充分必要性、全部续局量词与输入/输出合同。可用于构造精确小例、检查候选局部引理、与另一个精确实现比较；不可替代六人half证明或外部论文认证。两设施相关审计在[四地点资源](@P1)和[五地点资源](@P2)，模型分别保留。
""")
render(1,'facility-games/four-site-two-facility-audit-resource','四地点两设施精确支持审计的完整合同',
'完整实读177行全布局审计、151行独立审计及真实构造器/32和19输入；绑定同SHA旧成功不复跑，证明闭支持与条件费用的关系，纠正yes字段和设施数，并保有限实验与无FPTAS证明的区别。',
['a4954c4665e08897643a','f859371ea34882324c83','9f32aa2a4194de92d3b6','79d0b8c76eebaca202fa','c26e8f18cc84a854a492'],
"""# 四地点两设施精确支持审计的完整合同

## 原件和模型

本页收纳[全布局审计177行](@a4954c4665e08897643a)、[独立审计151行](@f859371ea34882324c83)的完整软件和数学合同。前者导入[2137B四地点构造器](@9f32aa2a4194de92d3b6)，后者完全自行重建参数、客户菜单、支持单元和条件费用，不导入构造器或规范均衡求解器。两份主源各在冻结legacy/main相同，不因两来源定位而重复算两份输入。

这里是两家有标签设施选择四个共同地点B,C,A,D。正权原子客户在所选地点可达设施中独立混合，以自己的条件期望总负载最小为最优回复；设施收益是分到自己的期望客户权重。完整续局规则为16个有序布局各指定一个精确客户NE。领导者相对偏离倍率至少为1，选择规则可以依布局独立指定。它不是四家设施，也不是顺序CAG覆盖模型。

对某布局，设只可达首/次设施的背景负载A_0、B_0，共同客户权重w_i，选择首设施概率p_i。期望负载X=A_0+Σw_i p_i、Y=B_0+Σw_i(1−p_i)。客户i选择两边的条件费用分别为X+w_i(1−p_i)、Y+w_i p_i，必须加入自己确定选择的权重；直接用X与Y作两边费用会得到另一个模型。本程序逐定义重算这些式子。

## 全闭支持：离散状态为什么覆盖连续概率

状态z_i=−1、0、1分别表示纯次、名义混合、纯首，名义混合允许端点。令m_0为名义混合数，Δ=X−Y，则

§[
(1-m_0)§Delta=A_0-B_0+§sum_iw_i z_i.
§]

纯首要求Δ≤w_i，纯次要求Δ≥−w_i，混合要求−w_i≤Δ≤w_i，且p_i=(1+Δ/w_i)/2。因此每个状态的可行集是一个点，或m_0=1且右侧为0时的完整闭区间；右侧非零时无解。三态全枚举覆盖每个精确独立混合NE，包括一名混合者连续区间和概率0/1端点。没有把实概率限定到某个网格。状态单元可重叠，同一均衡可出现多次，accepted cells不等于不同均衡数。

第一审计对每单元端点和中点核对概率域、X±Y与原条件费用；第二审计检查端点并对选中的Δ再次检查条件费用。单元参数化和每个线性条件对整个区间成立的论证来自上式，不把有限端点数目本身当成连续覆盖证明。反射(s,t)→(t,s)把概率变成1−p、交换负载，故无序布局加反射覆盖有标签布局。

## 第一审计：真坐标威胁和完整规则最优值

对所有十个无序布局（包含四个对角）全枚举。记d(s,t)为布局(s,t)首设施在全部客户NE中的最低收益，反向坐标由总负载减首设施最高值获得。令

§[
D_t=§max_s d(s,t).
§]

对路径(s,t)的一个NE单元，首收益x∈[l,h]，总收益V不变；完整规则可实现的最小倍率为min_x max{1,D_t/x,D_s/(V−x)}。因为首设施和次设施的实际单边偏离布局不相同，可分别指定实现相应坐标最低值的NE；其余布局任取NE即可补全规则。代码把目标V D_t/(D_t+D_s)夹到[l,h]，再在全部单元和布局中最小化。正威胁除以零视为无穷（内部None）；0/0视为0。把原布局本身含入D_t不会抬高结果，因为倍率已经≥1。

源变量source_yes精确枚举原始输入的所有子集，检验是否有原PARTITION等分；encoded_yes枚举补零变量的所有±号并核对等价。报告yes是这个原离散判定答案，绝不是支持/guard枚举内部标签，更不是“存在FPTAS”。对YES断言全局最优=13/10，对NO断言全局最优≥13/10+1/(100n²)；NO核心全部单元都非区间且|Δ−τ|≥3/(8n)。其它九无序布局均>131/100，五个非核心非对角布局还逐单元核对唯一负载。

[同SHA旧成功报告](@79d0b8c76eebaca202fa)完整读取32行结果、每行十布局精确分数及元数据。生成器为：单元素1至6；长度2、值1至4的非降多重组合；长度3、值1至3的非降组合；再加[1,1,1,1]、[1,1,1,4]、[2^100,2^100]、[2^100,2^100+1]、[1,2^200]、[1,1,2^180]。六类非法构造输入为空、0、负数、分数1/2、True、字符串，均按原CLI拒绝。计数为32输入、8YES/24NO、886344枚举、59340 accepted closed cells、811138条件费用比较。客户巨大整数不是浮点近似。

报告source_sha256同时绑定30f0…审计及320904…构造器，且全部运行成功。本批准确复用，原CLI新增0次。它的“当时未取得原始linked audit package”保留为当时事实；现在已实际取得本体不等于反改旧报告历史。CLI成功报告写出前才检查输出是否已存在；有mkdir/write_text，非原子x写。后置Git基线读取未在本批重跑。

## 第二审计：独立重建、解析对角guard与完整YES证书

第二份无需项目导入。对核心BC和另外五个无序非对角布局枚举全闭支持；五者唯一纯NE负载为BA:(2n,R−q)、CA:(2n,R)、BD/CD:(2n,d)、AD:(R−M,d)。它没有枚举全部对角支持，但并未因此漏掉全局低因子候选：程序同时检查下列七个解析排除界均>1.31，

§[
§frac{27}{20},§frac{R-q}{d},§frac{2n}{R-5n/2},
§frac{R-q}{9n/4},§frac{R}{9n/4},§frac{2d}{R},§frac{40}{27}.
§]

这些界对应其它路径布局的实际偏离，任何对角NE都至少有一方负载≤reach/2；结合上述坐标威胁即可排除低于这些界的对角解。核心记录core_guard_lower_bound是min_NE max{1,R/X,(R−q)/Y}，不是随意支持谓词。对本19输入该值均<1.31，因而与已证解析排除界结合，正是其全局最小倍率；这个等式的逻辑需要上述解析合同，不能仅从JSON字段名读出。

partition(src)返回一个原等分子集或None；isyes=结果非None。YES时从该子集加补零项至n/2个变量，把这些变量置首，其余置次，macro以1/2+1/(10n²)混合；所有对角用1/2，各反向布局反射。程序实际核16个布局客户NE及6个有标签设施偏离，且在归一化权重和整数缩放两版本都核，8YES共96个偏离比较。NO逐核心单元核m_0≠1、距τ至少3/(8n)及局部倍率≥1.3+1/(44n²)，再核较弱全局目标1.3+1/(100n²)。

19个实际源按n分层，完整列表如下：

| n | 输入 | 原PARTITION答案 |
|---|---|---|
| 4 | [1]、[2]、[1,2]、[1,3]、[2,3]、[3,5]、[1,10^12+1] | NO（7项） |
| 4 | [1,1]、[2,2]、[10^12+1,10^12+1] | YES（3项） |
| 6 | [1,2,4]、[1,1,1]、[2,2,3] | NO（3项） |
| 6 | [1,1,2]、[2,3,5] | YES（2项） |
| 8 | [1,2,4,8] | NO（1项） |
| 8 | [1,1,1,1]、[1,2,3,6]、[7,7,13,1] | YES（3项） |

[同f23ec…代码SHA旧成功](@c26e8f18cc84a854a492)记录92496个support cells examined、17890 accepted、932718条件比较、8YES/11NO。此代码顶层直接解析CLI并运行全部19例，import并非只加载定义；输出检查也在计算之后。本批无需重新import或运行。旧报告额外schema/base/python/source哈希来自其归档包装，原CLI本身只输出counts/cases/status，不把这些附加元数据说成源码直接产生。

例如[1]核心最小=6136/4695；[1,10^12+1]实际为1416000000002832/1083461538463705，二者不是同一分数。one_nominal_mixed_cells记录名义状态数，YES可有端点重叠，不能称均衡数量。两份输入和支持比较有重叠，不合并为51个独立样本或合并比较计数。

## 构造器、全输入证明和有限审计的分工

对非空正整数原向量a，T=Σa，n=2max(|a|,2)，补零至n项。设α=13/10、M=5n/2、V=11n/2、τ=1/(2n)、q=ατ、R=α(V+τ)/2、d=27n/10，

§[
w_i=1+§frac{na_i-T}{16n^2T},§quad
§sum_iw_i=n,§quad §sum_i|w_i-1|§le§frac1{8n}.
§]

客户依序为macro M（可达全部四点）、n个变量w_i（BC）、cross q（BA）、B私有n−q、C私有n、A私有R−M−q、D私有n/5。统一乘80n²T得到整数权重：macro200n³T，变量80n²T+5na_i−5T，余五项52nT、80n³T−52nT、80n³T、86n³T−26nT、16n³T。总位长为输入位长的多项式；构造器不求NE或原PARTITION答案。

核心Σ符号w_i=0等价原等分：整数符号和若非0不能被总扰动≤1/(8n)抵消；符号和为0强制各有n/2项，再化回原等分。NO没有恰一混合者区间，所有核心NE与τ分离≥3/(8n)，给核心倍率至少1.3+1/(44n²)，其它布局解析排除后全局至少1.3+1/(100n²)。YES显式完整续局倍率1.3。

完整全输入、所有实概率NE及编码分析在[四地点无FPTAS证明](@CTXarchives/facility-games/state/证明/四地点无FPTAS间隙的全支持与编码核算--证明.md)，本页已全文比较。其复杂度结论有条件：除非P=NP，不存在此精确客户NE/任意完整续局模型的确定性FPTAS；选择逆多项式epsilon即可区分原等分。不能仅由32或19例通过推出该定理，也不把其否定扩成无PTAS/EPTAS、近似客户NE或相关均衡。

## 现正文纠错与接续

旧[四地点和近带审查](@CTXarchives/facility-games/state/审查/四设施独立核验与近带有限审计--审查.md)在当时只有JSON时，把yes误称支持/guard谓词，并误记n=4层YES为4、NO为6，以及上述大整数例的分数。当前实际程序和完整证明已补齐定义证据；不因未枚举对角支持就把解析全布局排除降为无效。旧[共享流审查](@CTXarchives/facility-games/state/审查/共享流与多设施有限审计边界--审查.md)还将这组“四地点两设施”误叫“四设施”。本页作当前纠正，另给[带旧SHA最小替换提案](@E/suggested-existing-facility-page-corrections.json)，不覆盖他人正文、不重done那些已处理报告，也不改旧raw。

这两个精确闭支持实现可比较候选选择器和四地点gap实例；它们是有限回归与解析证明的实现接点，不是任意规模多项式求解器。近带审计的heavy-support representative有自己的输入和条件，本批不借四地点修订给它追加数学保证；CAG六人半覆盖也没有迁移结论。
""")
render(2,'facility-games/five-site-hardness-closed-support-audit-resource','五地点硬度审计的支持区间与完整续局',
'完整读409行主审计、58行边界审计及5190B真实构造器；隔离原CLI各一次，14/9例与旧报告除耗时外全同；区分闭支持、按负载去重、对角正规化、YES完整证书和固定因子弱NP硬度的普遍证明。',
['aba4ae48ffacdaea5c90','64fbe1e82a8a643c43b7','68753e23b4abb3316644','66a6e2d9e62086d6d517','6ca35d47c4014c6a1361'],
"""# 五地点硬度审计的支持区间与完整续局

## 原件、输入和证据身份

[主审计409行](@aba4ae48ffacdaea5c90)导入[真实构造器5190B](@68753e23b4abb3316644)，不导入仓库均衡求解器；[边界审计58行](@64fbe1e82a8a643c43b7)用runpy.run_path加载前者定义。模型仍是两家有标签设施、五个共同地点、正权独立混合的原子客户和完整25布局续局，客户最小化条件负载，设施最大化期望服务权重。不是五设施，也不是CAG。

原件两冻结版本相同，主审计SHA53c89b9ca894b201b027efc3cfb4b12d840f71d983def576eec8db770108cdcf，边界SHA9fd534645dcdf7960e47b81e1ceefe078266f53bf0f48ce2a44808d71f5ba7ef。旧[14例报告](@66a6e2d9e62086d6d517)及[9例报告](@6ca35d47c4014c6a1361)没有审计程序SHA的运行绑定；先前同53c89程序三例窄重放也不覆盖这两个完整CLI。因此本批仅补两次真实原CLI，各程序一次，均在新隔离目录用完整实际依赖，原输出及共享树不改。

## 全支持、负载去重和直接客户NE验证

local先把统一缩放后的权重确认为整数，再对共同客户枚举−1/0/1三态。与[四地点资源](@P1)同理，

§[
(1-m_0)§Delta=A-B+§sum_iw_i z_i,§qquad
p_i=(1+§Delta/w_i)/2§quad(z_i=0).
§]

纯首要求Δ≤w_i，纯次要求Δ≥−w_i，混合要求|Δ|≤w_i。m_0=1且右端0给完整闭区间，否则非空单元为一个有理点。每个精确实概率NE都落入某闭状态，不使用有限概率网格。accepted_closed_supports在去重前计数；pieces按首收益闭区间(l,h)去重，保一个代表state。不同状态给相同负载区间时，同一负载可由保留state实现，足以做坐标优化；它没有声称恢复全部概率向量或不同均衡个数。

核心布局(3,4)的bridge客户编号4被证明应纯次。每个接受状态的区间两端均检查其概率为0，发生在负载去重之前，避免只检查某代表而漏掉反例；随后所有保留片段端点和中点都经validate_ne按真实定义重算。对概率p，条件费用为X+w(1−p)、Y+wp；程序不以支持式自身充当唯一验证器。概率对区间是仿射，故这些状态给连续NE描述。

witness把区间点还原为共享客户列表、概率和负载；反向布局交换负载、概率取1−p。min_witness可指定请求布局中的任一坐标，最小次坐标来自首收益最大端点，方向变换显式处理，不把无序布局的首坐标硬用成有标签次坐标。

## 坐标威胁和对角正规化的确切作用

full=true时枚举15个无序布局（包括5个对角）并反射至25个有序布局，按真实全部坐标最低值优化每个完整规则。每个区间上最小max{1,D_t/x,D_s/(V−x)}在平衡点V D_t/(D_t+D_s)或相邻端点取得；零收益/正威胁记无穷。此分支给逐布局和全局精确值。

full=false枚举10个非对角布局，令H_t为对手留在t时所有非对角进入者可实现最低收益的最大值，R_t为地点t的总可达权重。对角最优项精确为G_t=max{1,2H_t/R_t}，由对角平分NE达到；任何对角NE至少有一方收益≤R_t/2。对每个非对角单元先忽略“跳到对手同一地点”的约束，算放松因子，令所有放松项的最小值为a_O，对角最小a_D=min_tG_t。

这时全局精确最优仍为min{a_D,a_O}：若a_O≥a_D，取平分对角完整规则；若a_O<a_D，则对每t都有H_t>a_O R_t/2。在达到a_O的路径(s,t)，x≥H_t/a_O>R_t/2、y≥H_s/a_O>R_s/2，故平分同地点偏离不再有额外约束，放松最优可以补成真完整规则。等号时取对角即可。

因此false不是“没算对角所以全局只是候选”，它使用已证明正规化；但JSON中每个非对角layout factor此时是忽略对角偏离的逐路径放松值，不能逐项冒充该固定路径的真实最优。报告alpha_star的全局解释依赖正规化证明。小例full=true还另算false并核全局值一致。主审计有限运行和该一般论证角色分开。

## 固定因子的真实归约输入

构造器从非空正整数numbers和整数target∈[0,Σnumbers]出发。source_answer对原numbers全部子集精确判断SUBSET SUM，是source_yes字段真实含义。给定有理因子a须满足1<a且a²<a+1，即1<a<φ。constants用逐次减半的dyadic e寻找严格guard；r_2=a+e，r_3=max{1,a r_2/2}+4e，r_4=max{1,r_2/a,a r_3/2}+e，r_10=1+1/a。选择e至以下全部严格条件成立：1<r_4<r_3<r_2<r_10，r_2>a，r_2>a r_10/2，r_3>a r_2/2，r_4>a r_3/2，a r_4>r_2，a r_4<2，r_2+r_3+r_4<4。精确余量为

§[
§eta=§frac14§min§left§{1,§frac{r_{10}-r_2}{1+1/(2a)},
2-a r_4,r_4-1,§frac{4-r_2-r_3-r_4}{3}§right§}>0.
§]

Fraction(a)也接受可被转换的float，但原CLI实际输入均为下面列出的精确有理数；不能把浮点近φ当严密端点。

若原有N项b_j，设M=2Σb+1，用对(M5^j+b_j,M5^j)作bounded编码，U为这2N项总和，R_0=MΣ5^j+target，R=2U−R_0，d_0=R−U>0。令Q_0=2U+R+1；raw micro为每个bounded项加Q_0，再加入2N+1个纯Q_0，共4N+1个micro，原始总量W_0。缩放λ=eta/(W_0+d_0+Q_0)，并令W=λW_0、d=λd_0、Q=λQ_0。余参数为

§[
H=1-W-d,§quad T=(H+1-Q)/2,§quad
v_1=T/a,§quad v_2=r_2-H,§quad v_3=r_3-H,
§]
§[
z=r_4-1+d,§quad P=1-v_2-v_3-z-W.
§]

客户为H,v_1,v_2,v_3,z,P及全部micro。五地点可达编号分别为{0,1}、{0,2}、{0,3}、{0,4}+micro、{2,3,4,5}+micro，两设施均可选全部五点。构造器检查全部正权及严格reach排序[H+v_1,r_2,r_3,r_4,1]，z−d>W、T>a r_4/2、a v_3<a v_2<T等。随后乘全部分母LCM并除整数GCD作统一缩放；这不改变概率、NE及倍率。

固定a时构造的位长对离散输入多项式；a逼近1或φ时寻找e的成本需另外计入a的输入及严格余量，不能从固定常数结论擅自升为统一时界。构造器只编译实例；它不产生客户NE，不解决原SUBSET SUM。

## 主审计的真实断言、证书和全部14例

每例检查原子集答案与bounded ternary编码等价；核心最小首负载mu≥T，且mu=T当且仅当原YES。全局alpha_star在YES为a、NO严格>a。用一基地点记R_1,…,R_5为缩放后reach，H及v_i亦为同尺度权重，B_h为核心(4,5)首收益最大端点；除目标路径(1,4)外的14项排除余量逐项是：

| 布局类 | 被检查为严格正的余量 |
|---|---|
| 11、22、33 | R_2−aR_1/2、R_3−aR_2/2、R_4−aR_3/2 |
| 44、55 | mu−aR_4/2、R_1−aR_5/2 |
| 12、13、23 | R_3−av_1、R_4−av_1、R_4−av_2 |
| 24、34 | mu−av_2、mu−av_3 |
| 15 | R_2−aR_5 |
| 25、35 | 各为R_1−aH |
| 45 | R_1−aB_h |

报告只保存上述最小余量除integer_scale，具体14项均由原代码实际检查。记录normalized_gap=(mu−T)不是alpha_star−a，不混作倍率gap。

YES时certificate构造全部25布局续局，路径为零基(0,3)，对角平分，其余指定坐标最小NE；核所有客户NE和8个真实设施偏离。默认主CLI在内存构造并检查证书，未额外调用verify_complete_certificate，也未在结果JSON内逐份存出完整概率证书。原代码和真实输入足以重放，但不能把仅含统计结果的JSON叫25布局证书文件。

默认无--quick运行先做1103个因子/常数域probe：分母2至60的所有合域有理候选，加1.000001及精确近φ有理数；96个macro约简检查比较micro为(1)、(1,2)、(1,1,2)，extra为1或2，macro1至8，B为0或3的完整/约简区间。严格边界例A=1、B=0、common=(3,1)、p=(1/2,0)是NE，负载(5/2,5/2)，说明差量恰等micro总量时大客户未必被迫纯次，严格大于不能改弱。因子1、2、1.618034共3个越域输入被拒绝。

14个真实归约实例如下，YES/NO均指原SUBSET SUM：

| numbers / target | a | full | 答案 |
|---|---|---|---|
| [2] / 1、2 | 7/5、3/2、8/5、809/500各一对 | true | 每对NO、YES（8例） |
| [2,3] / 2、4、5 | 3/2、809/500各一组三项 | false | 每组YES、NO、YES（6例） |

例如[2]/1、a=3/2的alpha_star=2528491/1685624，normalized_gap=55/2543616；[2]/2同a为YES且alpha_star=3/2。后一例195个distinct load pieces、495个accepted closed supports，两个数都不是均衡总数。NO离散gap下界为λ·integer_scale/[2·(raw_micro长度−1)]，它可以随输入位长指数小；这条五地点弱NP硬度证据不自动产生四地点那种逆多项式FPTAS间隙。

## 边界审计的9例与运行入口

边界CLI的run_path使用默认名称<run_path>，只加载主审计定义及其真实导入，不进入其__main__。随后边界main显式调用audit_case九次。因此本批是两个原CLI调用、14+9个归约例检查；不是再执行一次主CLI的1103/96探针，也不是两个独立均衡实现。

| numbers / target | a | full | 答案 |
|---|---|---|---|
| [2]/0 | 3/2 | true | YES |
| [2,2]/0、1、2、4 | 3/2 | false | YES、NO、YES、YES |
| [2]/1、2 | 1000001/1000000 | true | NO、YES |
| [2]/1、2 | 161803398874989/100000000000000 | true | NO、YES |

六个YES例将完整证书serial后JSON roundtrip，再调用verify_complete_certificate按实际客户NE/布局覆盖/偏离重新核验。这个6次反序列化证书验证是默认主CLI没有单独执行的边界专有内容；结果文件不逐份保存证书。空源、0/负数项、target<0、target>sum、True共6种非法源被拒。近φ的YES最大整数位长277，有限精确大分数仍可核；不把它视为φ端点归约。

## 本批新增运行和一般结论的边界

两份原CLI在Python3.12.14、-I -B、optimize=0的新完整镜像运行，依赖仅真实90B包docstring、构造器及标准库；不存在fake shared/__init__.py，也不需要Git基线占位。完整主CLI外层耗时2.520秒，报告内耗时2.477；边界外层1.548秒，内1.493。二者exit=0、stderr为空，stdout为单个完整JSON且与新输出文件相同。--output必填并open(x)排他写，不创建父目录；本次预建新目录，无旧文件覆盖。repository_checks_run=false按原字段保留，没有暗称跑过全仓suite。

[运行记录和新报告](@E/runs/)绑定所有实际源/依赖SHA；[逐字段新旧比较](@E/new-old-report-comparison.json)证实两份完整JSON仅elapsed_seconds不同。旧报告没有代码SHA不被追溯伪补；新报告配独立run record才有当前绑定。三个同SHA旧成功（CAG search及两四地点审计）没有重复运行。

一般结论是：固定有理1<a<φ时，精确客户NE、完整续局和a倍率决策的弱NP完全性由数学归约及证明承担；[已读构造器/正规化正文](@CTXarchives/facility-games/state/计算/小目录硬度构造器与五地点样本的精确合同--计算.md)完整保存该证明、参数输入和位复杂度。本页两次有限回归支持具体实现与23个指定输入，不单独证明该全称定理，不给规范实现未交付模块追加认证，不推CAG六人half，也不把严格NO gap冒充统一近似困难界。
""")
dump(E/'formal-resource-manifest.json',[dict(path=p,bytes=(S/p).stat().st_size,sha256=sha((S/p).read_bytes())) for p in paths])
# Only suggested edits; preserve exact older bytes and historical acquisition limitations.
target='archives/facility-games/state/审查/四设施独立核验与近带有限审计--审查.md'
old=(R/target).read_text()
section=old[old.index('## 四地点独立支持审计'):old.index('## 近带主审计')]
newsection="""## 四地点独立支持审计

### 输入、真实谓词与计数

本源是两家设施、四个共同地点、正权原子客户的精确条件负载NE模型。当前已全文取得151行独立审计程序及对应构造器、完整证明；partition(src)精确枚举原向量等分子集，yes表示原PARTITION有解，而非支持/guard内部谓词。19例记录92496个support cells examined、17890 accepted cells、932718个条件费用比较，原等分YES8/NO11，YES完整规则在归一化/整数版本共96个实际偏离检查。它不是“存在FPTAS”的标签，也不是成功概率。

### 全部输入与精确数值

| n | 输入层数 | YES | NO |
|---|---:|---:|---:|
| 4 | 10 | 3 | 7 |
| 6 | 5 | 2 | 3 |
| 8 | 4 | 3 | 1 |

n=4的YES为[1,1]、[2,2]、[10^12+1,10^12+1]；n=6为[1,1,2]、[2,3,5]；n=8为[1,1,1,1]、[1,2,3,6]、[7,7,13,1]。完整19输入、全部分数、代码/旧报告SHA及模型合同见[四地点两设施精确支持审计](../资料/四地点两设施精确支持审计的完整合同--资料.md)。[1]的core guard为6136/4695；[1,10^12+1]实际为1416000000002832/1083461538463705，二者不同。

### 支持覆盖、解析guard与历史边界

程序对核心BC及五个其它无序非对角布局枚举所有闭三态支持，包含名义混合端点及一混合者区间，并从原条件费用核NE。它没有枚举全部对角支持，而以每个对角NE至少一方负载不超过reach/2及七个解析偏离guard排除低因子对角解；非核心五布局检查唯一NE。核心core_guard_lower_bound是全核心NE上的min max{1,R/X,(R−q)/Y}，并非任意内部标签。本19输入该值均<1.31，结合其它路径解析下界>1.31给全局最小倍率。YES构造完整16布局规则，NO全核心支持给正gap。

one_nominal_mixed_cells记录允许端点重叠的名义状态数，不是均衡数目。两份32/19例审计输入重叠，计数不合并；有限成功本身不证明全输入复杂度结论。原JSON“当时未取得原始audit package”的文字是历史事实，本轮已取得源码不追改其字节。完整全输入及位复杂度论证另见[四地点无FPTAS证明](../证明/四地点无FPTAS间隙的全支持与编码核算--证明.md)。该精确两设施模型与CAG六人顺序覆盖模型不同。

"""
repl=[
 ('四地点源在 19 个 n=4,6,8 实例上内部 yes/no 谓词为 8/11','四地点源在 19 个 n=4,6,8 实例上原PARTITION答案 yes/no 为 8/11'),
 ('四地点源把 '+chr(96)+'yes/no'+chr(96)+' 作为其支持枚举和对角 guard 的内部判定','四地点源的 '+chr(96)+'yes/no'+chr(96)+' 是原PARTITION等分判定答案，支持枚举和解析对角guard核其归约性质'),
 (section,newsection),
 ('和未完备支持限制全部保留','和未枚举对角支持但有解析排除的真实范围全部保留'),
 ('提供一个可重复的 Fraction 支持枚举模板，供补齐完整 support closure 时比较','提供一个可重复的 Fraction 全核心/非对角闭支持枚举模板，与解析对角排除及全布局实现比较'),
 ('提供四地点有限 guard 的精确有理下界，供寻找真正的全称 lower-bound lemma，但仍需独立证明','提供四地点有限guard的精确有理下界，与已交付全称gap证明和位复杂度核算比较；有限运行本身不代替证明')]
proposals=[]
def propose(path,replacements,evidence):
 data=(R/path).read_bytes();text=data.decode();applied=[]
 for a,b in replacements:
  count=text.count(a);assert count==1,(path,a,count)
  text=text.replace(a,b);applied.append(dict(old=a,new=b,expected_count=1))
 prev=E/'proposed-facility-corrections'/path;prev.parent.mkdir(parents=True,exist_ok=True);prev.write_text(text)
 proposals.append(dict(path=path,before_sha256=sha(data),before_bytes=len(data),after_sha256_if_applied=sha(text.encode()),replacements=applied,evidence=evidence,applied_to_shared_tree=False,preview_path=str(prev.relative_to(S)),preview_role='review-only external text; not a canonical replacement in transport whitelist'))
propose(target,repl,'Primary f859 lines73–78/99–145 and a495 lines90–134; all19 raw cases; existing complete four-site proof fully read. Preserve historical unavailable-package wording as then-fact.')
target2='archives/facility-games/state/审查/共享流与多设施有限审计边界--审查.md'
txt=(R/target2).read_text()
rr=[]
for token in ['和四设施有限枚举的证据边界','### 补集变换与四设施枚举','该来源是四设施有限支持枚举与硬度探针']:
 assert txt.count(token)==1
 rr.append((token,token.replace('四设施','四地点两设施')))
propose(target2,rr,'Actual four_site input menus have two labeled facilities and four common sites; no change to equal-light multifacility sections or old raw JSON.')
dump(E/'suggested-existing-facility-page-corrections.json',dict(scope='guarded proposals only; no existing formal page/source progress changed; previous BD4 proposals remain separately frozen',proposals=proposals))
# Five current primary receipts, not extra done for any dependencies/reports.
notes=[
('329行16033B主码已完整实读，BD相关实读原字节与本次clean show一致；本次独立正式claim/owner核验，不继承此前related完成。覆盖27136输入的旧报告全部字段/13阶段真实输入及规范四依赖既读同SHA范围完整核对。','同46cf成功报告复用，原CLI新增0；保count缓存不约束有序历史续局、无residual反例和5/9非六人反例，规范交叉只13最坏根且旧依赖SHA未列。',0),
('177行8593B主码、2137B真实构造器全文及32例/每例十布局/完整来源哈希实际读；闭支持m=1区间、坐标威胁、反射/完整规则独立性与整数编码理解。','同30f0主码与320904构造器成功绑定复用0新CLI；32例原PARTITION源答案，10无序含对角全支持，区分有限回归与已交付无FPTAS证明，旧四设施词纠正仅建议。',1),
('151行7161B全文、顶层CLI/全部19字面输入和实际旧4890B报告全部字段读；独立参数/原PARTITION判定、核心及五替代全闭支持、7解析guard、16布局YES证书全部理解。','同f23ec全stdlib成功复用0新调用；纠正旧审查内部谓词/4层3YES7NO/大例不同分数，解析对角排除不误降为漏全局，旧历史未取得说明不反改。',1),
('409行14872B全部源码、5190B实际导入构造器及90B根包全文、全部常数probe/macro/14归约例输入和所有新旧输出因子实读；25标签/负载去重/正规化/源子集判定理解。','必要一次完整原CLI非quick新运行exit0，1103常数/96macro/14例，2.520s外层；旧无auditorSHA仅耗时不同，前同SHA窄3例不冒充完整覆盖。',2),
('58行2313B全文及run_path实际409行依赖/构造器全部读；9真实输入、6坏源及6YES serialized证书验证流程和全部新旧大分数字段完整读。','必要一次原CLIexit0外层1.548s；run_path以<run_path>加载定义不进入主CLI，九audit_case与14主例分开，总2CLI并非两个独立solver；旧输出仅耗时不同。',2)]
receipts=[]
for d,(rn,cn,idx) in zip(sources,notes):
 receipts.append(dict(id=d['id'],full_file_reviewed=True,related_material_checked=True,unique_content_accounted_for=True,read_note=rn+' 两冻结refs同字节、inventory SHA/bytes已核。',comparison_note=cn,decision_note='全部独有数学/程序/实际输入与运行语义并入自足资料及原件；保有限/全称/条件和当前/历史时态，依赖和已处理报告无额外done，不改shared旧页，不导第三阶段图。',disposition='integrated',targets=[paths[idx]]))
dump(W/'semantic-receipts.json',receipts)
(W/'relation-review.md').write_text("""# 第二阶段实际关系自查

CAG程序与已处理27136搜索报告是实现/同SHA有限证据绑定；其计数状态递推与完整有序历史SPE终局有充分必要性，5/9具体实例另有本页显式全历史策略解释。与六人half是有限检查支持及量词缺口，未证明普遍结论。

两四地点实现共享同一两设施硬度模型：第一全对角/非对角坐标最优，第二独立核心/替代支持加解析对角排除，证据和代码SHAs逐项区分。它们同已交付四地点全输入gap证明的关系是有限实现回归，不用有限计数当无FPTAS证明。

五地点主/边界审计共享实现，边界增加端点、近边界大有理数及6个序列化完整证书验证，不标成第二个独立solver。完整/正规化分支的全局最优证明与逐布局放松表区别明确；与已交付构造器正文为真实输入编译/数学证明/实现检查关系。严格gap可能指数小，不把四地点FPTAS间隙移来。

两设施原子条件负载模型和单位客户顺序CAG不同，不建half迁移。只记录可供后续第三阶段人员判断的关系，当前无图/mapper写入、无强制连通、无旧来源额外done。旧页纠错提案带before SHA供owner接续，BD4建议预览也只属外部比较。
""")
# Real next candidates only; no claim.
inv=[json.loads(l) for l in (R/'cleanup/inventory.jsonl').read_text().splitlines()]
wanted=['cd26f8a883a5ebf2e64d','d165f0b0cbc484ee0ad3','8e4166732a1d048fddfb','2a77d0eb61bccece8dae','8bb33ff5bfd5b36ce7d0']
cand=[]
for sid in wanted:
 d=next(x for x in inv if x['id']==sid);pp=R/'cleanup/progress'/f'{sid}.json'
 cand.append(dict(id=sid,path=d['path'],bytes=d['size'],sha256=d['sha256'],local_progress_exists=pp.exists(),eligibility='no local progress record at read; parent must verify authoritative ownership before claim',proposed_reason='related actual facility audit implementation, not pre-read or pre-done primary'))
dump(W/'next-candidates.json',cand)
(W/'delivery.md').write_text("""# 本批交付

五源完整实读48972B/1124行，三个自足正式资料；程序实际输入、全部相关报告/构造器与当前证明实读比较。三份同SHA旧成功复用，原CLI新增0；两五地点原CLI各一次，共2次，exit0，完整输出与旧报告仅耗时差异。所有其它source只比较，无额外done。

主权依据actual-claim-receipt.json与primary-ownership-snapshot.json。只写独立staging；无shared Git/身份/公屏/凭据/mapper操作。正文/证据/receipt须由Root先实际推送，再做done。本文件及程序记录不声称已经推送。

既有BD四页提案及其当前读回预览不修改BD96冻结包。新四地点两页仅给beforeSHA建议，所有preview在证据路径下，白名单不覆盖任何现有canonical页。copy-files.json列精确可复制文件，根transport清单不在自身白名单，避免自引用。
""")
print(json.dumps(dict(formal=[dict(path=p,bytes=(S/p).stat().st_size) for p in paths],receipts=len(receipts),new_original_runs=2,reused_same_SHA_runs=3),ensure_ascii=False))
