from pathlib import Path
import json,hashlib,os
S=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-kfac-greedy-and-flow-primary')
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=S/'tools/evidence/kfac-greedy-and-flow-primary'
W=S/'cleanup/workspaces/Boss4/r3-kfac-greedy-and-flow-primary-next';W.mkdir(parents=True,exist_ok=True)
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
primary=json.loads((E/'source-manifest.json').read_text());deps=json.loads((E/'dependency-manifest.json').read_text());byid={x['id']:x for x in primary+deps}
ctx=json.loads((E/'context-manifest.json').read_text())
paths=[
'archives/facility-games/subarchives/common-many/state/资料/旧帽与两类贪心坏选择的原始程序--资料.md',
'archives/facility-games/subarchives/common-many/state/资料/等权流对抗审计的全极小与残图边界--资料.md',
'archives/facility-games/state/资料/双设施四地点近远菜单候选的真实审计合同--资料.md']
def relative(target,p):return os.path.relpath(target,Path(p).parent).replace(os.sep,'/')
def write(i,ident,title,summary,ids,body):
 p=paths[i];refs=[]
 for sid in ids:
  for x in byid[sid]['sources']:
   ref=f"source:{x['commit']}:{x['path']}"
   if ref not in refs:refs.append(ref)
 head='---\n'+''.join(f'{k}: {json.dumps(v,ensure_ascii=False)}\n' for k,v in dict(id=ident,kind='resource',type_tag='资料',title=title,status='source-complete-exact-finite-scope',summary=summary).items())
 head+='source_refs:\n'+''.join('  - '+json.dumps(x,ensure_ascii=False)+'\n' for x in refs)+'---\n\n'
 body=body.replace('§',chr(92))
 for sid,d in byid.items():body=body.replace('@'+sid,relative(d['saved_path'],p))
 body=body.replace('@E',relative(E.relative_to(S),p))
 for j,t in enumerate(paths):body=body.replace('@P'+str(j),relative(t,p))
 for x in ctx:body=body.replace('@CTX'+x['path'],relative(x['path'],p))
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(head+body)
 return p
write(0,'facility-games/common-many/three-original-greedy-obstruction-audits','旧帽与两类贪心坏选择的原始程序',
'三份原入口及全部实际十客户JSON完整实读，各新原CLI一次；准确保全旧全局帽44、任意修复顺序32/15及唯一普通势极小者215/107，区分站点纯/站内均匀NE、所有mixed离轨续局和另一好NE。',
['d165f0b0cbc484ee0ad3','8e4166732a1d048fddfb','2a77d0eb61bccece8dae','812637c4d5d7e327de64','36882baacad2b171cf66','a47ce4a499fcf500b8eb'],
"""# 旧帽与两类贪心坏选择的原始程序

## 原程序、实际输入和模型

[cap程序](@d165f0b0cbc484ee0ad3)、[potential程序](@8e4166732a1d048fddfb)、[repair-order程序](@2a77d0eb61bccece8dae)分别为4299、4255、6881B，连同三个真实十客户JSON逐行实读并核inventory SHA。三主源在legacy/main冻结字节相同，原件保持独立sourceID。前者在run()读取JSON；后两者在模块加载时读JSON、定义函数，只有__main__才执行audit()。旧heaviest入口曾导入repair-order后覆盖其模块变量，并不执行本源audit；不能用那个成功替代本批原入口。

采用[共同目录任意设施数原子模型](@CTXarchives/facility-games/subarchives/common-many/state/定义/共同目录任意设施数模型--定义.md)：带标签设施同时选址；被覆盖正权原子客户必须服务、独立随机化，以包含自身完整权重的条件负载为成本。客户先确定一个物理站，再在该站q_s家设施间独立均匀时，当前实际成本是w_i+(W_s−w_i)/q_s，改另一站t为w_i+W_t/q_t。站点纯/站内均匀只是客户NE的一类；后文离轨严格支配结论则覆盖任意独立mixed客户NE。

三个输入都k=8，地点按A,E,B,C,D,G排序，规范贪心占用同为q=(1,1,2,1,3,0)。cap JSON用整数0,…,5，对应此顺序；另外两JSON保存名称。不能按字母重排破平局次序，也不能直接把名称JSON冒称生产Instance的整数接口。规范贪心首次开站把尚未覆盖客户全部归该站；已开站再放设施的分数为原池重量/(q_s+1)，未开站分数为新覆盖客户重量，原池在此过程中冻结。

| 客户角色及菜单 | cap重量 | repair重量 | potential重量 |
|---|---:|---:|---:|
| A私有 | 20 | 80 | 200 |
| X，AB | 8 | 32 | 128 |
| Y，BEG | 24 | 96 | 231 |
| B私有 | 20 | 81 | 240 |
| Z，AC | 10 | 40 | 68 |
| C私有 | 30 | 120 | 330 |
| T，BD | 13 | 52 | 60 |
| D私有 | 67 | 268 | 740 |
| E私有 | 20 | 82 | 200 |
| G私有（在轨未覆盖） | 20 | 80 | 199 |

真实原件分别为[cap JSON](@812637c4d5d7e327de64)、[repair JSON](@a47ce4a499fcf500b8eb)、[potential JSON](@36882baacad2b171cf66)。删掉G私有客户、把Y改成只有BE、交换三个输入的数字，都会改变被检结论。

## cap：旧全局普通帽失败与指定偏离者可受帽同时成立

贪心逐步为D80、B52、C40、D40、D80/3、B26、A20、E20，末γ=20，原总重(A,E,B,C,D,G)=(20,20,52,40,80,0)。五次严格修复X:B→A、Z:C→A、T:D→B、X:A→B、Y:B→E的旧/新实际成本为30>28、40>38、106/3>35、38>73/2、89/2>44。终总重(30,44,41,30,67,0)，程序从原条件费用核全部可达已占站比较，得到在轨精确NE。B一家设施收益a=41/2。

B中一家移至原未开G后，B,E,G各一设施，各有不可挪的私有20，Y重量24只能选这三站。不论怎样作可行站点纯种子，Y所在站普通负载至少44>2a=41；20和24各自≤41，不能当作“单名超帽巨原子”孤立。因此旧的全局普通帽41不可能，最小可行帽恰44。该量词是全部可行纯赋值，不是所有mixed NE，也不是“偏离者不能受帽”。

原程序随后显式给真实偏离布局的一份带标签纯客户NE。原布局标签按站递增为A,E,B,B,C,D,D,D，第二个B标签3改为G；八家负载为(30,44,28,20,30,67,13,0)。其中Y留E与换G成本44平局，X在B成本28优于A38，Z在A30优于C40，T在D13优于B41，D的67与另一个空D只平局。偏离者G只收20≤41。因此反例针对旧全局装箱接口，不能否定后来冻结超载补全定理的指定偏离者安全结论。这里的精确纯NE亦是一份独立混合NE，不把在轨站内均匀与离轨纯标签分配混同。

## repair：坏严格顺序和所有离轨mixed NE的32/15

贪心D320、B209、C160、D160、D320/3、B209/2、E82、A80，γ=80，原总重(80,82,209,160,320,0)。C/D在160平局时按既有站序选C。原CLI检查五步指定严格改善：

| 迁移 | 旧成本 | 新成本 |
|---|---:|---:|
| X:B→A | 241/2 | 112 |
| Z:C→A | 160 | 152 |
| T:D→B | 424/3 | 281/2 |
| X:A→B | 152 | 293/2 |
| Y:B→E | 357/2 | 178 |

终总重(120,178,165,120,268,0)是站点纯/站内均匀NE；B一家a=165/2。B一家移G后，Y只能在B,E,G中选，G只有Y96与私有80可达；B/E不可移私有重量分别81/82。对任意其他客户独立混合，Y选G条件费用恒176，选B≥177、E≥178，所以每个mixed客户NE都强迫Y到G，偏离收益恒176，比为32/15>2。这个“所有离轨NE”结论来自明确严格支配不等式，不是枚举有限混合概率猜出的。

同一贪心占用只让Z:C→A一步就得到另一好NE，总重(120,82,209,120,320,0)，B一家209/2。程序核其全部原NE与所有已占/新开目标的转移预算：源多设施时无孤儿，源单设施时把可达目标的原成员作orphan_overlap；已占目标总重加该重不超过(q_t+1)a，新开目标新覆盖加该重不超过a。因此坏顺序没有反驳存在安全选择。

四个可动客户X,Y,Z,T各有两个已占选项，共16个站点纯分配，程序逐一比较最小设施收益，唯一最大者是(B,E,A,B)，最小收益165/2。唯一最大第一坐标已足以推出升序收益字典序最大者唯一，不需要另枚举所有字典序排序算法；这是固定贪心布局，不是跨布局字典序。原程序不枚举所有mixed在轨NE，也不检查所有严格修复顺序。

## potential：精确优化oracle也会选坏点

其贪心D800、B599、D400、C398、B599/2、D800/3、A200、E200，γ=200；最后A/E并列按原站序。原总重(200,200,599,398,800,0)。四共享客户同样只有16个站点纯分配，全部被源程序枚举，精确客户势为

§[
P(a)=§sum_{s:q_s>0}§frac{W_s(a)^2-§sum_{i:a_i=s}w_i^2}{2q_s}.
§]

移动i:s→t改变P的量为w_i[W_t/q_t−(W_s−w_i)/q_s]，故全局最小者必为该站点纯/站内均匀类的NE。精确分类为：

| X,Y,Z,T | 总重A,E,B,C,D | P |
|---|---|---:|
| B,B,A,D（好） | 268,200,599,330,800 | 86264 |
| B,E,A,B（坏） | 268,431,428,330,740 | 86200 |

这两个是所枚举16个站点纯分配中的全部NE，不声称全部一般mixed NE仅此两份。程序进一步在全部16赋值上直接核坏点为唯一全局势极小者，也是唯一最大最小设施收益者，因而唯一固定布局升序lexmax。即便计算无困难，这两个指定选择器仍会选不安全点；不能和“求最优势本身强NP难”的复杂性结论混为一谈。

坏点B一家收益214。其移G后，Y231选G条件费用430；B≥231+240=471、E≥231+200=431，所以每个mixed客户NE强迫Y到G，偏离收益430，倍率215/107>2。好NE则满足γ全盒、C原孤儿重叠330+68≤2·268及新开G客户199≤γ；原CLI实际核这些条件，而没有生成完整离轨规则的JSON。

## 真实执行及与现行数学的关系

全文比较[既有坏选择反例](@CTXarchives/facility-games/subarchives/common-many/state/反例/固定贪心均衡的坏选择与静止超帽边界--反例.md)、[五JSON与快速入口](@CTXarchives/facility-games/subarchives/common-many/state/计算/五份贪心输入与轻量全盒回归的精确合同--计算.md)、[旧六套审计](@CTXarchives/facility-games/subarchives/common-many/state/计算/贪心选择器六套原审计的精确复现--计算.md)。这些来源已保数学反例及heaviest变体；本批新增三份原程序的逐源合同和完整原CLI证据，不把旧12样本快速入口或heaviest导入算成运行本三audit。

三个原CLI各新运行一次，Python3.12.14、-I -B，无-O，真实三个JSON置于全新外部相对树；exit均0，stderr均空，耗时0.026300、0.026730、0.032521秒。原stdout分别105、75、76B的简短通过说明，全部保存在[运行目录](@E/runs/)；源码内部真实断言覆盖如上。没有伪造原脚本未输出的详细机器JSON，没有跑全仓suite、生产CLI或三份完整设施续局。

共同目录盒NE存在与一般异权位复杂度仍按现行证明/开放问题分开；这些反例限制的是旧帽、任意顺序、普通势和固定布局lexmax选择器，不限制新的截断归位选择器。它们也不提供CAG六人half的反例或证明。
""")
write(1,'facility-games/common-many/equal-light-adversary-all-minimizers-resource','等权流对抗审计的全极小与残图边界',
'完整实读22239B原对抗审计、12755B规范流、18707B含嵌入构造器的历史全文和全部实际fixture/报告；复用同主源及五依赖SHA成功，保6691输入、全体极小者、仅历史实现残图插桩和异权/局部NE反例的准确量词。',
['cd26f8a883a5ebf2e64d','e19c1dd1197f68906d4a','ab58636ad8af7c408652','25ebede9c2862ae31bfb','ee665883c39a34e0e6b9','41b0ab6732ba2f681e68'],
"""# 等权流对抗审计的全极小与残图边界

## 主源、实际依赖和抽象输入

[对抗审计原件](@cd26f8a883a5ebf2e64d)22239B完整实读；它既不信生产证书的布尔值，也不把BOX/H预先作为优化域过滤。直接依赖为[规范equal_light_flow.py](@e19c1dd1197f68906d4a)、[完整历史Pro原文及嵌入代码](@ab58636ad8af7c408652)、[等权local-NE fixture](@25ebede9c2862ae31bfb)、[两轻权fixture](@ee665883c39a34e0e6b9)，连同141B包说明全部按inventory SHA核原字节并实读。规范程序与历史嵌入程序是两个不同实现，不互称同源或独立外审。

规范化输入为非增正整数q_t，c_t∈[0,1]，逐名可动客户同权δ∈(0,1)，每个非空菜单A_i去重排序后home=min A_i。重复/原序可接受，归属仍按规范编号；q可巨大二进制而不展开每家设施。原设施输入到此接口的具体映射另保留显式k和站点次序。空q、空客户的抽象网络被作为程序边界测试，不据此把原模型非空地点目录改为空目录。

令h_i=min A_i、b_t=c_t−δ·#{i:h_i=t}、X_t=b_t+δ·#{i:a_i=t}，b可以为负。独立oracle对每个合法逐客户分配计算

§[
§Phi(a)=§sum_t§frac{X_t(a)^2-§sum_{i:a_i=t}w_i^2}{2q_t}.
§]

在等权时，Φ=Σb_t²/(2q_t)+δΨ，其中Ψ=Σ[b_tN_t+δN_t(N_t−1)/2]/q_t。枚举全部合法赋值后保留全部并列全局最小者，再逐一核：0≤X≤1、所有原菜单比较(X_{a_i}−δ)/q_{a_i}≤X_v/q_v、以及H:(X_{a_i}−δ)/q_{a_i}≤(1−δ)/q_{h_i}。优化域没有盒或H限制，因而不能用“结果通过因为输入先筛掉坏状态”解释该审计。

规范/历史两个solver分别返回一个赋值，oracle检查它属于所有全局极小者集合，精确X/目标恒等、augmentations=N。它不要求两个solver在平局时返回相同赋值，更没有只比两实现彼此一致而不查全局最优。

## 历史嵌入实现与插桩的精确身份

程序只从固定历史原文抽取唯一python代码块，SHA必须等于340ee161a21e3384091b2461c666bda73fe3e96cc838e3c88cb7b45335186a50，否则拒绝。该块已完整实读；在唯一四空格“a = []”前插入八空格audit_residual调用，放在每次单位增广结束处，插桩SHA为8d6c360953099810fba903a108bda7db2b7287b8d7f2af8445602c7c49ef988d。两个字节块分别另存[原块](@E/read-embedded-equal-flow.py.txt)和[插桩读回](@E/instrumentation-readback.py.txt)，未改冻结源码。

构造新内存ModuleType，注入审计回调后exec编译该精确块；模块名称不是__main__，所以嵌入stdin/stdout CLI不运行。其equal_weight_box_ne在每个输入正常调用；不接受任意外部模块、用户传入路径或网络代码。只有这一历史图结构接受Floyd全点最短路残图检查：有正容量的边构成残图，所有distance[u][u]必须为0，另统计可沿零费用环的实例图。规范构造器只检查独立全局oracle的输出及自身断言，审计没有窥取其内部残图。

旧记录中的6791个archived residual graphs和4015个含zero-cost cycles图指历史实现增广阶段的受查图，不是6791个不同原游戏，不是canonical残图认证，也不把零费用环当负环失败。检查范围是全部网格、首80随机例及special；其余随机例仍核两solver全局最优，但不执行历史残图Floyd。

## 真实输入域和同SHA成功复用

[全部原成功报告](@41b0ab6732ba2f681e68)8783B已逐字段实读，status=all_passed，seed=2026100719。其source_sha256同时绑定a7ac…本审计、956884…规范流、d1f545…历史原文和两个实际fixture；嵌入/插桩SHA也与实际抽取和唯一替换吻合。因此本批原CLI新增0次，未重复4500随机或1000恒等式suite。原CLI可设--random-cases/--identity-cases，负计数拒绝，输出已存在计算前拒绝，最终用x写并建父目录；无Git/网络运行依赖。

| 输入类 | 实际数量与完整参数 |
|---|---|
| exhaustive grid | 2187：q取(1,1),(2,1),(3,2)；两c各0,1/2,1；δ取1/3,1/2,2/3；3名逐名客户菜单各为{0},{1},{0,1} |
| seeded random | 4500：m1至5、N0至6，q各1至8后非增排序；c取0、1或randint(0,5)/5；δ∈{1/2,1/3,2/3,1/101,100/101}；各站独立公平入菜单，空菜单改随机单点 |
| 大二进制/空/重复顺序 | 3：q=(10^90+3,10^80+7)、δ=1/(10^70+33)、8客户双菜单；空网络；q=(2,1)、c=(0,1)、δ1/2及两个含重复/倒序菜单 |
| 严格贪心映射的等权local fixture | 1：下节完整六原子输入 |
| 异权fixture | 仅展示边界，不进入6691次等权solver调用 |
| 路径恒等式 | 1000个额外代数样本，不是1000次optimizer调用 |

6691个等权输入共89521合法赋值，7902个全局极小者全部查，537例有并列最小，5674例某最优X达到0或1，4925例base有负项；两实现各6691次global oracle比较。两者各拒绝8种非法输入：不同可动权、q非非增、q含True、c为float、空菜单、菜单True、权重0或1。这些拒绝检查不等于对所有坏类型完整穷举。

独立程序记录的每个计数是其实际控制流量，不是distinct NE数；生成器源、种子、所有参数与两fixture都是完整可重现输入。旧JSON没有逐4500随机输入数组，本文不虚称逐项读了不存在的数组，也不生成新随机suite来扩大样本。

## 任意局部NE不足：完整等权四状态

真实六原子私有130/H、80/M、52/L、50/R，另25/HM及25/ML，k=7。严格唯一贪心H,M,H,M,L,H,R及155,105,155/2,105/2,52,155/3,50，归一化q=(3,2,1,1)、γ=50、c=(1/10,1/10,1/25,0)、δ=1/2。可动者分别home H、M，全部四状态如下：

| 目的地 | X | Ψ | 原NE | H | 全盒 |
|---|---|---:|---|---|---|
| H,M | (1/10,1/10,1/25,0) | −1/3 | 是 | 是 | 是 |
| H,L | (1/10,−2/5,27/50,0) | −7/75 | 否 | 是 | 否 |
| M,M | (−2/5,3/5,1/25,0) | −3/20 | 否 | 是 | 否 |
| M,L | (−2/5,1/10,27/50,0) | −4/25 | 是 | 是 | 否 |

坏态物理总重H130、M105、L77、R50。两客户真实跨站成本65<205/3、77<155/2，故确为原精确独立NE；归一化外部比较为−1/5<−2/15、1/25<1/20。它破下盒，不是盒NE存在反例。唯一全局最小者是home H,M；“每一个全局极小者安全”和“每一个NE安全”不可互换。

## 异权端点与路径恒等式的独有边界

两轻权实际私有143/H、90/M、47/L、45/R，共享36/HM、44/ML，原JSON站序R,H,M,L；严格贪心开站/重数重排后为H,M,L,R。γ=45、q=(3,2,1,1)、c=(44/45,44/45,2/45,0)、w=(4/5,44/45)。home与away四赋值的势Φ依次326/6075、118/1215、2414/6075、302/6075。away M,L是唯一势最小者，X=(8/45,4/5,46/45,0)，为原NE但破上盒和H；另外两状态非NE、非全盒、非H。

同时沿L→M→H返路的两权为44/45、4/5。一般路径u_0,…,u_{ell+1}的代数恒等式为

§[
§Delta§Phi=-w_0§frac{X_{u_0}-w_0}{q_{u_0}}
+§sum_{j=1}^{§ell}(w_{j-1}-w_j)§frac{X_{u_j}-w_j}{q_{u_j}}
+w_{§ell}§frac{X_{u_{§ell+1}}}{q_{u_{§ell+1}}}.
§]

该例三项恰−88/2025、0、32/675，总8/2025>0，返路反而升势；内部异权项即使为0也不够，端点接受阈值不同仍出问题。H失败2/45>1/90，接受端8/45≤1−4/5却>1−44/45。故它只反驳指定普通势/返路推广，不反驳一般异权盒NE存在或所有位多项式算法。

1000个恒等式样本取ell0至5、ell+1个权为randint(1,9)/10、ell+2个X为randint(−10,30)/10、q1至8；不要求q排序或X在盒中，因为这是纯代数检验，不调用等权选择器。它们校验公式而不证明全部实输入公式，公式本身由逐点二次展开自足推出。

## 证明、现行实现和来源边界

[已读等权流算法](@CTXarchives/facility-games/subarchives/common-many/state/算法/等重轻客户下盒流与无约束细化--算法.md)给所有无约束全局极小者自动全盒/H的交换证明及N次最短增广的位复杂度。中间点等权抵消、home菜单最小秩及非增q是承重条件。规范模块12755B还保巨大十进制输入/输出的分块精确转换，Bellman-Ford负边、前驱环拒绝、slot前缀、原选项NE、H及目标恒等都已实际全文读过；本批不据有限6691输入宣称所有序列化边界都经过运行。

历史Pro文字自报4982实例、13910赋值和5496极小者，只是原附文声明；其linked ZIP/分别代码附件未取得，不能与本6691/89521/7902累加。三外部URL及“论文Theorem/Algorithm”说明是原程序保存的来源边界，本批没有重新获取或阅读这些论文/网页，不作新文献归纳；受限同链Nashification与本物理q源自权重扣除的模型不同，也不把它导入成当前canonical完整离轨的已交付实现。

规范流只提供位多项式在轨子类，完整离轨/默认补全仍是另一有限程序。与[旧原等权审计5242例](@CTXarchives/facility-games/subarchives/common-many/state/计算/等重流全局极小值与增广实现的有限审计--计算.md)有重叠，不能把两计数相加为独立统计。当前两份精确旧成功与本次[三贪心原运行](@P0)彼此分开。第三阶段关系仅作语义说明，未导旧图或mapper。
""")
write(2,'facility-games/two-facility-four-site-near-far-menu-audit-resource','双设施四地点近远菜单候选的真实审计合同',
'完整读6673B主源、4976B near_select及186行旧结果，同两代码SHA成功准确复用；保全近远重客户模式、真实16布局完整续局、坐标近似/c²有限断言，纠正误归CAG/四设施、六客户域和随机行身份。',
['8bb33ff5bfd5b36ce7d0','27dcbc1b3521b65d42b1','d027eeb6603c80ef3c5a'],
"""# 双设施四地点近远菜单候选的真实审计合同

## 领域与源身份

[主程序6673B](@8bb33ff5bfd5b36ce7d0)全文实读，直接导入[near_select依赖4976B](@27dcbc1b3521b65d42b1)，以及两个真实71B包说明；依赖只在__main__运行其自身2004例，import在本主源中只加载函数及独立计数器，不执行那个suite。本主源则在模块顶层生成并检查全部186例，argparse在计算后才执行；因此import主源就会运行审计，--help也先算全部例，不是无副作用的库。

本体SHA699657ffae7f31d399ac5ce4c2227a5f15aa8d5b6c33e3cb529ea66015982138，near依赖bb556c714919c28f6f537eca290d1b81c615dc197eccfe64f3d05c4a55508d8b；两个冻结refs相同。旧[完整186行结果](@d027eeb6603c80ef3c5a)同时列这两个SHA且全部断言成功，故本批新增原CLI0次，未再次触发顶层循环。schema/base/Python/两源hash等附加字段来自旧归档包装，原脚本本身输出counts/seed/results/status；保留其真实生成层次。

它是两家带标签设施、四共同地点S={0,1,2,3}、正有理原子客户及精确条件负载NE的候选菜单实验，完整规则有16个有序布局。随机客户的覆盖菜单可为空，表示所有布局都不被服务；空客户集也合法。它不是四家设施，不是单位提供者顺序CAG，也没有完整有序历史行动。旧文件放在customer-attraction存档不能改变数学定义域。本资源归facility-games；与旧34单位客户三人CAG安全值重放分开。

## 完整NE单元与近/远小菜单

对位置(s,t)归纳客户为私有a,b和共同权列表ww，总可达权W=a+b+Σw_i。三态z_i=−1/0/1给纯次/名义混合/纯首；Δ=X−Y满足(1−m_0)Δ=a−b+Σw_i z_i，且混合概率(1+Δ/w_i)/2。onecell将Δ与纯/混合阈值及指定区间相交；m_0=1且右端0保连续闭区间。allcells对全部3^n状态枚举，直接按条件成本核端点。这是有限全支持oracle，复杂度随共同客户数指数增长，不能把整个审计脚本叫EPTAS实现。

给η∈{1/8,1/4,1/2}，H=ηW，heavy是严格w_i>H的共同客户，其余light≤H。heavy个数<1/η；模式数3^heavy。每个模式同时产生：

* near：调用near_select寻找|Δ|≤H的一个精确NE代表；返回后再次按原条件费用验证。
* far：分别限制Δ∈[H,W]或[−W,−H]，把light全部纯选低负载端（正Δ选次，负Δ选首），保heavy指定模式，再用onecell得到精确点或闭区间。
* W=0：直接给Δ=0、空概率列表，所有收益0；约定倍率至少1。

near_select对固定heavy模式令k_h为heavy混合数，D=a−b+Σ纯heavy z_iw_i，S_l为light总量。若k_h=0或|D|≤S_l，light按非增权/编号依次向当前较轻侧纯放以更新残差r；k_h=0时必须|r|≤H，k_h>0且r非零时选指定最小合格light作唯一部分混合，取Δ=sign(r)(w_j−|r|)/k_h。r=0时Δ=0。若|D|>S_l，则要求k_h≥2，先令t=(|D|−S_l)/(k_h−1)，light全在一侧，逐个翻转尚未移动且w_i<t者，更新t=(|D|−S_l+2Σ已翻转w)/(k_h−1)，每light至多一次；t>H则无输出，否则Δ=−sign(D)t。最后heavy混合概率按Δ恢复并直接核NE。该具体代表和far区间是候选菜单，不擅称列出全部near概率向量。

依赖内部比较记在near模块自己的C，主程序报告的166968来自主check()，包含allcells中同一端点为两坐标重复调用check；它不是所有实际执行比较的去重总数。7295个near模式对应14590个far模式；成功代表/区间可重叠，也不是不同NE数。

## 完整续局选择与三个alpha字段

solve从每个菜单取首/次坐标最低收益，D_1(t)=max_r min_NE菜单 L_1(r,t)、D_2(s)=max_r min_NE菜单 L_2(s,r)。对路径(s,t)的一个Δ区间，总收益W，平衡目标为Δ_0=W(D_1−D_2)/(D_1+D_2)，分母0时取0；夹至区间后最小化max{1,D_1/X,D_2/Y}。正数除0记不可行None、0/0记0，原零收益布局用原不等式语义处理。

actual为选定路径及菜单，实际构造全部16布局：路径用所选点，首设施偏离(r,t)选首坐标最低菜单NE，次设施偏离(s,r)选次坐标最低NE，其余布局取首个菜单项。两种实际偏离布局不冲突。每布局重新核客户概率及条件费用，之后核6个有标签设施偏离；不是只检查威胁表或抽象数值。

optimal_alpha是完整全支持oracle允许任意精确续局的最优倍率；menu_bound是小菜单与其坐标威胁给出的最小上界；actual_alpha来自上述真实完整续局的实际偏离。令c=(1+η)/(1−η)，原每例断言逐布局坐标最低值满足m≤mhat≤c·m，威胁D≤U≤cD，并断言actual≤menu_bound≤c²·optimal、optimal≤2。这里对每个报告输入都实际检查，但未给任意输入的全称坐标近似证明或生产EPTAS；原码连完整3^n oracle一起运行。零坐标的乘性比较强制对应菜单坐标也0，不是忽略小分母。

## 全部真实输入与结果行身份

seed=20261009003，先生成全部graphs，随后每例从同一RNG状态取η；不能把η选择移进前180例生成循环而声称同种子同输入。随机180例各有0至6客户，权为randrange(1,40)/choice(1,2,3,20,2^30)，每个四地点独立概率0.6覆盖，可生成空菜单。这六客户上限仅属随机部分。

再追加原PARTITION gap输入src=(1,1)、(1,2)、(1,2,4)，n=2max(len(src),2)，客户数分别10、10、12；变量近单位权与macro/private/cross见四地点gap参数，实际代码在本体逐字给出。最后三输入为单名10客户覆盖全部地点；两名10及1/2^40但覆盖都为空；两名2/(地点0,1)及1/2^50/(地点2,3)。它们不是把所有客户数统一限制为六。

完整186行结果逐项实读，全部menu_bound=actual_alpha；非平凡行精确如下，行号为JSON results零基：

| 行 | 输入身份 | η | optimal_alpha | menu_bound=actual_alpha |
|---:|---|---:|---:|---:|
| 22 | seeded random | 1/8 | 85/81 | 85/81 |
| 63 | seeded random | 1/8 | 16/15 | 16/15 |
| 69 | seeded random | 1/2 | 34/31 | 34/31 |
| 104 | seeded random | 1/2 | 1 | 47/46 |
| 159 | seeded random | 1/2 | 8589934592/8291672987 | 同左 |
| 180 | src=(1,1)，10客户 | 1/4 | 13/10 | 2301/1760 |
| 181 | src=(1,2)，10客户 | 1/4 | 2124/1625 | 2275/1728 |
| 182 | src=(1,2,4)，12客户 | 1/8 | 144508/110895 | 5135/3888 |

其它178行三个alpha均1，包含最后三个special。报告总数186 inputs、2976=186·16布局、73304 full cells examined、14590 far patterns、7295 near patterns、166968主程序条件费用计数、1116=186·6实际设施偏离。不把重叠菜单项称distinct NE，不把每个原报告数字解释成独立新证据。

## 与旧页的纠错、运行和接续

旧[共享EPTAS与34客户审查](@CTXarchives/customer-attraction/state/审查/共享EPTAS候选与34客户独立安全值增量--审查.md)误说三源全属CAG、称四设施、将22/63/69随机行标gap-family、称菜单/实际分离，并把六客户限制扩到全部输入。当前原程序及真实186行结果给出上述纠正；34客户独立安全值重放仍是原CAG对象，不随第一项迁档而改模型。另给[带beforeSHA替换提案](@E/suggested-existing-eptas-page-corrections.json)，没有覆盖旧正文或额外done其报告源。

原CLI打印counts/status，完整results由--output保存；输出存在检查在全部计算和argparse之后，write_text不是原子排他写。近带依赖在import时不运行其main，但本主源自身顶层有真实计算副作用。旧成功同时绑定两非平凡代码SHA，两个真实包说明无执行语句；本批只核字节/读源码/报告，不运行任何新EPTAS或near-band suite，不把旧归档provenance字段伪装成当前新运行。

该候选适合做近/远菜单、exact NE、零收益、小分母及近似坐标接口回归；若要一般EPTAS仍须独立证明全输入近/远菜单近似、生成和有理位复杂度、完整证书算法与ε转换。它不关一般实例最优FPTAS困难，也不提供CAG六人half结果。与[等权多设施流](@P1)即使都出现菜单/负载也属于不同参数接口，不互相移用性质。
""")
# Correct the exact probe command text, not another original-source invocation.
probe=json.loads((E/'runtime-flags-probe.json').read_text())
probe['command'][-1]='import sys,json;print(json.dumps(dict(version=sys.version,optimize=sys.flags.optimize,isolated=sys.flags.isolated)))'
dump(E/'runtime-flags-probe.json',probe)
# Fully read reports retained without invented per-random-instance records.
reportread={}
for sid in ['41b0ab6732ba2f681e68','d027eeb6603c80ef3c5a']:
 raw=(S/byid[sid]['saved_path']).read_bytes();d=json.loads(raw)
 reportread[sid]=dict(bytes=len(raw),sha256=sha(raw),actual_read_scope='All original fields, every explicit result row/fixture and exact generator/seed/control-flow code read; no absent random sample array claimed',report=d)
dump(E/'complete-old-report-readback.json',reportread)
dump(E/'formal-resource-manifest.json',[dict(path=p,bytes=(S/p).stat().st_size,sha256=sha((S/p).read_bytes())) for p in paths])
target='archives/customer-attraction/state/审查/共享EPTAS候选与34客户独立安全值增量--审查.md'
record=next(d for d in ctx if d['path']==target);before=(S/record['saved_path']).read_bytes();old=before.decode()
pairs=[
('truth_status: "exact-fraction-finite-cag-replay-with-duplicate-source-boundary"','truth_status: "two-facility-atomic-menu-audit-and-independent-finite-CAG-replay"'),
('shared_eptas_candidate finite four-site probes plus independent exact replay','shared_eptas_candidate finite two-facility four-site probes plus independent exact replay'),
('本批三项来源都属于 customer-attraction/CAG 证据线。第一项是共享 EPTAS 候选的四设施有限 probe；后两项是','本批第一项是两设施四地点、原子客户条件负载NE的共享EPTAS候选有限审计，属于facility-games；后两项才是customer-attraction/CAG证据线，即'),
('第一项则是另一个共享 EPTAS candidate finite audit，单独保留其四设施 probe 量词。','第一项是独立的两设施四地点共享EPTAS候选审计，归档地不改变模型；当前源码合同见[双设施四地点近远菜单候选](../../../facility-games/state/资料/双设施四地点近远菜单候选的真实审计合同--资料.md)。'),
('有限四设施样本','有限两设施四地点样本'),
('有限 gap-family 行','随机样本的非平凡行'),
('菜单上界与实际值分离','最优倍率与菜单/实际倍率分离'),
('有限菜单/实际误差','最优与菜单/实际倍率的有限差距'),
('它采用 four-site/client/coverage 的候选接口，最多六客户，并且 source 自己没有 canonical EPTAS implementation。','它采用两设施、四地点、加权原子客户精确条件负载NE的接口；180随机例至多六客户，三个gap输入分别10、10、12客户，另有三边界例，并非全批最多六客户；source自己没有canonical EPTAS implementation。')]
replacements=[];new=old
for a,b in pairs:
 count=new.count(a);expected=3 if a=='有限 gap-family 行' else 1
 assert count==expected,(a,count)
 new=new.replace(a,b);replacements.append(dict(old=a,new=b,expected_count=expected))
preview=E/'proposed-existing-page'/target;preview.parent.mkdir(parents=True,exist_ok=True);preview.write_text(new)
dump(E/'suggested-existing-eptas-page-corrections.json',dict(scope='suggestions only; preserve existing CAG34 section and historical raw/receipts; no canonical overwrite',proposals=[dict(path=target,before_sha256=sha(before),before_bytes=len(before),after_sha256_if_applied=sha(new.encode()),replacements=replacements,preview_path=preview.relative_to(S).as_posix(),preview_role='external review only; not canonical target in copy manifest',applied_to_shared_tree=False,evidence='Full primary699657 and near_select bb556; full186 JSON result rows22/63/69/180–182; all16 layouts use two coordinates. Actual full source now available, older source-only limitations kept temporal.')]))
notes={
'cd26f8a883a5ebf2e64d':('22239B原程序全文、6691真实生成器/固定seed/全部五哈希依赖、18707B历史全文含完整嵌入代码、12755B规范实现及所有fixture/8783B报告每字段实读。','原报告同a7ac主码及四非平凡依赖SHA、嵌入340ee/插桩8d6完整字节绑定成功复用0新CLI；全合法赋值/全部极小者、仅历史残图/1000代数与异权边界区分，原附文自报计数不采用。',1),
'd165f0b0cbc484ee0ad3':('4299B程序全文及416B十原子真实JSON完整读；八步贪心/五改善/实际条件费用/纯标签离轨布局全理解。','新原CLI恰1次0.026300s exit0，原105B stdout保真；全局纯普通帽44与指定G20分开，不当全mixed不可能或否定安全NE存在。',0),
'8e4166732a1d048fddfb':('4255B全文及468B十原子实际JSON完整读；顶层读取、全部16站点纯分配、两类NE和势/最小收益唯一性、所有mixed离轨严格支配理解。','新原CLI恰1次0.026730s exit0，75B原stdout；unique ordinary-potential/固定布局lexmax失败与一般盒存在/计算困难分开，未造详细原JSON。',0),
'2a77d0eb61bccece8dae':('6881B全文及462B真实JSON完整读；五严格动作、另一好NE/全部转移预算、16赋值唯一max-min和32/15混合离轨强迫理解。','新原CLI恰1次0.032521s exit0，76B原stdout；旧heaviest的相关import不执行本audit，不当本源成功；坏指定顺序非全顺序失败。',0),
'8bb33ff5bfd5b36ce7d0':('6673B主码全文、4976B near_select和两个71B真实包说明、180随机/3gap/3边界完整输入生成代码、186原结果每行字段实读。','同699657与bb556旧成功复用0新CLI；精确两设施16布局/原条件费用、near/far和c²有限断言；纠正旧CAG/四设施/随机6客户外推和22/63/69行身份，不重复2004依赖suite。',2)}
receipts=[]
for d in primary:
 rn,cn,ix=notes[d['id']]
 receipts.append(dict(id=d['id'],full_file_reviewed=True,related_material_checked=True,unique_content_accounted_for=True,read_note=rn+' legacy/main同字节与inventory尺寸/哈希一致；本批按原始25回执实际交集并核owner。',comparison_note=cn,decision_note='独有数学/软件/实际输入/证明与有限证据完整归入自足资料及冻结原件；不额外done依赖、报告或旧数学源，不改shared原页/原件，不导第三阶段图。',disposition='integrated',targets=[paths[ix]]))
dump(W/'semantic-receipts.json',receipts)
(W/'relation-review.md').write_text("""# 第二阶段关系自查

三贪心原审计实现已有三个明确障碍。cap是旧全局普通帽与指定偏离者低负载NE的分离；repair/potential是固定占用的不安全选择器，但有另一好NE。原显式反例及对任意mixed离轨的严格支配推导保全，不把“有限CLI”降格成没有证明反例，也不把一例上升为所有算法失败。

等权流主源与规范/历史嵌入实现为定义级全局oracle交叉核验。全体全局极小者量词、局部NE不足、异权端点项及仅历史残图分别解释。与既有无约束流证明、5242旧审计有实现/有限检查/重叠关系，不累加独立样本。一般异权位复杂度、完整离轨软件总时间依旧分开。

shared EPTAS源属于两设施四共同地点条件负载模型；当前CAG归档旧审查的标签和输入范围纠错只建议，34客户CAG重放保持其身份。近/远菜单真实续局与坐标近似有限断言是候选/回归，不是生产EPTAS全输入证明。跨模型仅说明区别，不建CAG half蕴含。

本批13相关inventory文件与9现正文全读/哈希比较，只作真实依赖与上下文，不额外源done。正式超图留第三阶段，无mapper/强制连通/旧图导入。
""")
inv={x['id']:x for x in map(json.loads,(R/'cleanup/inventory.jsonl').read_text().splitlines())}
want=['4b6ecf840027c41cfff3','55fb3925a6d44e62fd2f','788ed29d939a1e0c8b9e','b0abf271408afe39053e']
cand=[]
for sid in want:
 d=inv[sid];p=R/'cleanup/progress'/f'{sid}.json'
 cand.append(dict(id=sid,path=d['path'],bytes=d['size'],sha256=d['sha256'],local_progress_exists=p.exists(),local_progress=json.loads(p.read_text()) if p.exists() else None,eligibility='candidate only; parent must check current authoritative ownership; no primary read or receipt'))
dump(W/'next-candidates.json',cand)
(W/'delivery.md').write_text("""# 五主源交付

原始25源pushed/synced capture完整保留，不伪造五ID投影回执；本批实际expected交集五源、owner均Boss4。主码44347B/957行全文及13真实相关源70376B、9现正文82134B完整比较。三份自足资料及五receipt待Root先推正文再done，当前不声称pushed。

新增原CLI恰3次，三个不同贪心fixture各一次成功；等权流6691及双设施菜单186同主码/实际依赖SHA旧成功复用0新CLI。运行/原件/报告层级保真，probe仅查看同Python标志，不运行数学源码。没有共享Git/网络/账号/公屏/凭据/图操作。

旧CAG审查一页仅给beforeSHA提案及external preview，白名单不覆盖该canonical文件。原件和旧证据历史状态不反改；copy-files.json逐字节白名单可复制新增正式资料、E证据和W自查/receipt。root transport清单不自列，避免循环哈希。
""")
print(json.dumps(dict(formal=[dict(path=p,bytes=(S/p).stat().st_size) for p in paths],receipts=len(receipts)),ensure_ascii=False))
