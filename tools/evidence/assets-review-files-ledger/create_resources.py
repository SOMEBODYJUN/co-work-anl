"""Author lossless semantic resource objects from actually fully read primary ledgers.

This is a new representation writer, not an original checker or mathematical verifier.
"""
from pathlib import Path
import collections, hashlib, json, re, shutil

S=Path(__file__).resolve().parent
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=S/'tools/evidence/assets-review-files-ledger'
W=S/'cleanup/workspaces/Boss4/r3-assets-review-files-ledger-next'
D=S/'archives/customer-attraction/state/资源'
W.mkdir(parents=True,exist_ok=True);D.mkdir(parents=True,exist_ok=True)
B=chr(96);F=B*3
def dump(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
def copy(p,q):
    q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
    return {'source':str(p),'saved_path':q.relative_to(S).as_posix(),'bytes':q.stat().st_size,'sha256':sha(q.read_bytes())}
assets=json.loads((E/'original/research/assets.json').read_text())
reviews=json.loads((E/'original/research/review_status.json').read_text())
catalog=json.loads((E/'related/catalog/original/research/catalog.json').read_text())
sources=json.loads((E/'source-manifest.json').read_text())
refs=[f"source:{s['commit']}:{s['path']}" for row in sources for s in row['sources']]
def front(name,id,summary,rs=refs):
    vals={'id':id,'kind':'resource','type_tag':'资源','title':name,'status':'historical-ledger-fully-read-with-explicit-scope-corrections','summary':summary,'source_refs':rs}
    lines=['---']
    for k,v in vals.items():
        if isinstance(v,list):lines.append(k+':');lines += ['  - '+json.dumps(q,ensure_ascii=False) for q in v]
        else:lines.append(k+': '+json.dumps(v,ensure_ascii=False))
    return '\n'.join(lines+['---','','# '+name,''])
def write(name,id,summary,body):
    p=D/(name+'--资源.md')
    text=front(name,id,summary)+'\n'+body.rstrip()+'\n'
    bad=[(i,ord(c)) for i,c in enumerate(text) if ord(c)<32 and c not in '\t\n\r']
    if bad:raise ValueError(('forbidden C0',p,bad))
    text='\n'.join(l.rstrip() for l in text.splitlines())+'\n'
    p.write_text(text)
    return p.relative_to(S).as_posix()

comparison=[
'AGENTS.md','cleanup/README.md','cleanup/OBJECTS.md',
'archives/weighted-congestion/state/定理/全状态线性次数无均衡族--定理.md',
'archives/customer-attraction/state/定理/四人真实根偏离福利界--定理.md',
'archives/facility-games/state/归约/共同目录三五地点固定倍率的全布局守卫--归约.md',
'archives/facility-games/subarchives/common-many/state/算法/强制负载下界的自适应原池重置--算法.md',
'archives/facility-games/subarchives/common-many/state/反例/有向深度三树的盒势最小失稳--反例.md',
'archives/facility-games/subarchives/common-many/state/反例/固定贪心盒内收益字典序失稳--反例.md',
'archives/facility-games/subarchives/common-many/state/定理/冻结静止超载的偏离者受帽补全--定理.md']
deps=[copy(R/p,E/'comparison'/p) for p in comparison]
prev=R.parent/'boss4-next-cache/r3-catalog-semantic-resources/tools/evidence/catalog-semantic-resources/comparison'
for p in ['archives/customer-attraction/state/定理/五人半覆盖--定理.md',
          'archives/customer-attraction/state/反例/独立同分布福利支付--反例.md',
          'archives/customer-attraction/state/反例/实际前缀的独立同分布局部漂移--反例.md']:
    deps.append(copy(prev/p,E/'comparison'/p))
builders=R.parent/'boss4-next-cache/r3-research-index-builders/tools/evidence/research-index-builders/related/research'
for p in ['graph.json','current/claims.md']:
    deps.append(copy(builders/p,E/'related/research'/p))
graph=json.loads((E/'related/research/graph.json').read_text())
graphids={z['id'] for z in graph['nodes']}; graphclaims={z['id'] for z in graph['nodes'] if z['kind']=='claim'}
assetids={c for z in assets['entries'] for c in z['claims']}
reviewids={z['id'] for z in reviews['entries']}
fields=collections.Counter(k for z in assets['entries'] for k in z)
axis={k:dict(collections.Counter(z[k] for z in reviews['entries'])) for k in ['source_proof','current_proof','internal_review','external_review','implementation']}
chararrays=[{'index':i,'id':z['id'],'value':z['applies_when'],'proof':z['proof']} for i,z in enumerate(assets['entries']) if isinstance(z['applies_when'],list) and z['applies_when'] and all(isinstance(t,str) and len(t)==1 for t in z['applies_when'])]
meta={'scope':'new bounded metadata/representation analysis, not original checker execution, no mathematical targets marked done','assets':len(assets['entries']),'review_entries':len(reviews['entries']),'asset_fields':dict(fields),'review_fields':dict(collections.Counter(k for z in reviews['entries'] for k in z)),'axes':axis,'asset_distinct_ids':len(assetids),'review_distinct_ids':len(reviewids),'asset_ids_without_review':sorted(assetids-reviewids),'review_ids_without_asset':sorted(reviewids-assetids),'graph_nodes':len(graphids),'graph_claims':len(graphclaims),'graph_claims_without_asset':sorted(graphclaims-assetids),'graph_claims_without_review':sorted(graphclaims-reviewids),'character_arrays':chararrays}
dump(E/'metadata-analysis.json',meta)
for p in sorted((E/'related').rglob('*')):
    if p.is_file() and p.suffix not in {'.pyc'} and not any(d['saved_path']==p.relative_to(S).as_posix() for d in deps):
        deps.append({'source':'already materialized previous exact-SHA input; see reading-log','saved_path':p.relative_to(S).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
dump(E/'dependency-manifest.json',deps)

common_intro="""这份资源保留旧资产登记的全部原字段，而不是给各条引用证明重新认证。每一条下方 JSON 是该条完整源对象；条件、输出、限制、来源解释及软件角色均可在本页独立读取，不靠去查原 JSON 才知道结论范围。空数组、字段缺席、字符串和数组的区别保持原样。作者的 status、produces 和 limit 有时处于不同修订时点，应联合读；本页的解释不改冻结原件。

字段合同：id 是资产包身份；claims 是关联命题或义务身份，不是本条已证明它们的断言；applies_when 是作者登记的输入/量词；produces 是声称产出；status 和 limit 说明作者的审查与停止界。proof、implementation、tests、records、examples、reviews、candidates、sources 是不同的路径角色；source_role、source_scope、source_interpretation、scope_model、implementation_detail 是额外范围解释。角色本身不能代替证明、外审或完整实现。所有旧相对路径均以冻结源仓库根为基准；本批保全引用字符串，不承诺这些目标在新树仍同名，不额外勾选被引源。

每条记录的原序号从零开始；精确来源为 research/assets.json 的 entries[index]，两冻结提交 SHA 与原件见总合同。下面完整保留关键数学范围，包括反例只否定指定接口、条件推论、有限审计和算法实现的停止界。
"""
families={
'shared':('共同目录双设施资产的条件与角色',"""此组始终区分客户主动选择设施的原子负载博弈与顺序提供者均分客户的 CAG。shared_phi 明确两家带标签设施、有限共同目录、被覆盖客户必须服务、线性实际负载、独立混合精确客户 NE，且各布局可独立选续局。实例最优计算、普遍倍率、局部谱与硬度不同。

五地点是地点数而非五家设施；全布局归约对固定有理 1<a<φ 给弱 NP 完全性，YES 精确最优 a，NO 严格大于 a。允许间隙随二进制数值指数小，不是强 NP、固定 gap 或 FPTAS 否定。原第22项 applies_when 只剩字符集合，不能当模型；实际已全文比较正式全布局守卫，详见总合同纠错。"""),
'heterogeneous':('异构双设施资产的条件与角色',"""异构菜单、限制图几何、长环与稀疏大 reach 是不同条件。存在倍率证明与可调用 CLI 不等价；sparse_unbounded_rho 的证明完整却未登记对应 CLI，不能因 implementation 空而否定数学，也不能因有测试而声称生产实现。闭回应核心的坐标极小值达到、局部纯/混合客户量词和同址边界按每条原字段保留。"""),
'other':('局部精确均衡资产的条件与角色',"""有限支持谱、整数总重动态规划、MITM、二次延伸、polyhedral continuation 与局部原子/Wardrop 对照分别收费。伪多项式依数值总重，不自动是输入位长多项式。一个达到证书只验证给定倍率与完整续局，不能取代最优性证明；polyhedral 有理证书与一般可执行 LP 后端也不同。"""),
'multi_facility':('任意设施数资产的条件与角色',"""共同目录原子客户的任意显式 k≥2，与 CAG 提供者模型不同。因子二完整续局可由每个真实单方偏离的精确客户 NE 独立拼合；在轨均衡选择、离轨受帽补全、一般盒存在、有限构造、数学位多项式导入和 canonical 软件实现应逐层区分。

第27–30项 applies_when 为单字符数组，是来源登记缺损。实际相关正式页分别证明：给在轨收益下界与原池删除证书的自适应重置；深度三树唯一盒势极小者非 NE 但另有盒 NE；固定贪心盒内唯一收益字典序最大者非 NE 但原分配已 NE；冻结静止超帽客户并核其全部替代后 lift 残余 NE。前两类坏选择器不能否定一般盒存在。

有限严格改善保持最大负载不增、最小负载不减且有限终止，不给多项式步数。既有 MAX/RANGE 数学调度导入与已交付 canonical 实现分开；本批没有运行或交付调度器。前批独立 RANGE 论文导入有其实际已读版本/章节和输入域，也不改变旧页当时未取得论文的历史。"""),
'customer_attraction':('顺序客户吸引资产的范围与后续修正',"""单位客户在最终覆盖者间均分，所有有序历史上的同一完整纯 SPE 与任意历史依赖平局是承重条件。主题可空、可重复；真实偏离后继不能冻结为实际后续。静态 Nash/CCE 最差福利、独立同分布乘积分布的平均 Z，以及 SPE 福利是不同对象。

第36项旧 status 写四人 sharp 1499/750，但同条 limit 明说锐性 OPEN。已全文比较四人实际根偏离证明，成立的是 OPT4≤(1499/750)W 的普遍上界；128类非负余项和12个合法节点 slack 不承担达到常数的下界。三人5/3锐性不沿人数顺序推出四人锐性。第36项较旧五人2.061695…不是现行最佳；第347项及实际五人正式证明给 OPT5≤2W，53个精确乘子，软件证据只覆盖已交付的原验证器，literal 交叉核验依赖主 evaluator，不是第二份 standalone 证明验证器。

旧一般弱 iid 桥 OPEN 已被第344项既有完整 SPE 族否定；全 m≥41 依解析证明，有限 m=20 例可直接见 W=40、Z=60(1−(19/20)^20)>40。Z 是静态 iid 覆盖，不是 minimax 安全值。局部前缀漂移失败不单独等于全局桥反例；同源独立反例各保留。第343–350项的局部恒等式、枝缺口、定价隐藏回复、同源重查询和相关菜单必要条件，不能升级一般 half。当前仓库主问题固定六人，旧任意 m 的任务指令只作历史，不取代现焦点。"""),
'weighted_congestion':('加权拥塞资产的范围与后续修正',"""固定次数成本、权重、真实偏离负载、全状态与单条改善环的量词不可互换。只否定共同势/局部选择器/校准接口时，见证游戏可能仍有精确 PNE。有限浮点筛选、精确有理小例、参数化全称证明分别登记。

一批较早 limit 写原目标 Cd/ln d 仍 OPEN；同冻结后续全状态线性族已改变该数学状态。实际已全文读正式证明：每整数 p≥2^20，有限正有理权游戏，每人恰两条非空不交动作，所有资源费用为正有理系数乘 x^p，每个状态有严格 p/10 改善，余量至少 (2^p−p/10)/8。前沿相位覆盖与同次数三元锚定修复共同承担全部状态，不能只用改善环或有限审计替代。于是每固定 C≥1、d0≥2 选足够大 p≥d0 且 p/10>Cp/ln p，可否定全类 Cd/ln d 保证。未声称构造规模位多项式、最优常数、外审或优先权。

后段结构重构有端点面积、类型尺度、实例区间、正核/社会下降修复，以及近单位权和 d−1200⌈log2d⌉² 的加性近次数族；每项以自己的输入域及实现限制为准。S7 作者也是正修复 reviewer，不能把同一人的记录当独立 S7 审查；原记录另明确 root check，须保留这两种角色。"""),
'occupancy':('正占用核资产的独立工具范围',"""正占用核是不先假设博弈的结构工具。排序、占用、light forcing 或具体提升接口的证明不能自动产生一般博弈均衡或固定因子桥。输入域、输出、实现与障碍各按原字段；对 WC 的来源/启发可以保留，但本批不由元数据建立数学推导边。"""),
'unrelated':('不相关并行机资产的条件与实现边界',"""此组完整保留一般 UM 目标、条件算法、指定源族、decoder/证书接口、复制编译器障碍和有限实现。一般确定性 uniform-in-ε 目标与固定 k、给定小 δ、给定稳定点 y 或给定 target 的算法不等价；C2 证书提取不是 finder，给定 y 的 matching 不是稳定点 finder。

候选与条件状态保持原值。pDM 全域需修复；KDM quota 障碍的条件 hardness §§4–5 有持续量词异议，不能拿其有限审计认证它们。CC_r 的无重叠一致性不等于 SA，raw K2/row degree 的缺口不等于任意 canonical SoS 缺口。列出的 NP 编译器障碍不自动否定所有 UM hardness 或所有算法。

第295项旧 high/low-gamma 解释已撤回，原定理不因旧审计被追溯改写。新 gated norm=1 整域13/8 与旧 flat 菜单有不同域；Q-alone 19/10 系列是数学位多项式规范，有限 moment/交换审计不等于 LP/MW/FW、profile、prefix 和 alljobs 集成后端。point pullback 的反例只否定所述点/映射，不是所有点均失败。Top-two 目标也不等于普通 makespan 全行总负载。

外部论文若只登记 source_role 为 background/criterion，不视作本批已阅读或认证其内容。本批原文是元数据全表；没有新增外文论文取得、一般调度程序或外审认证。所有 package 路径和真实 standalone 审计路径保全，implementation 空数组不代表不存在别处的有限 API，仍须读 review 的具体实现轴。""")}
def family(z):
    p=' '.join(z['proof'])
    for key in ['customer_attraction','weighted_congestion','unrelated','occupancy','multi_facility','heterogeneous','shared']:
        if key in p:return key
    return 'other'
groups=collections.defaultdict(list)
for i,z in enumerate(assets['entries']):groups[family(z)].append((i,z))
asset_targets=[];assetmap=[]
for key,(name,intro) in families.items():
    body=common_intro+'\n## 这组实际保存的对象边界\n\n'+intro+'\n\n## 全部条目及完整字段\n\n'
    for i,z in groups[key]:
        body+='## 资产 '+str(i)+'：'+z['id']+'\n\n'
        body+='以下为完整原条目；其数学断言与作者审查均保持所述范围。\n\n'+F+'json\n'+json.dumps(z,ensure_ascii=False,indent=2)+'\n'+F+'\n\n'
    p=write(name,'research-assets/'+key+'-ledger','逐项保全本组旧资产的模型条件、产出、限制、来源和软件角色，作者标签不升为当前证明。',body)
    asset_targets.append(p)
    for i,z in groups[key]:assetmap.append({'index':i,'id':z['id'],'target':p,'heading':'资产 '+str(i)+'：'+z['id'],'source_record':z})
dump(E/'asset-record-destinations.json',sorted(assetmap,key=lambda z:z['index']))

review_body="""本对象是旧 research/review_status.json 的完整五轴账本。头部 version=1，checked_on=2026-10-23；scope 声明覆盖 current/claims.md 的身份，五字段和 graph_status 独立，明确不是同行认证。日期是作者检查日期，不是本轮重新证明日期。全部640条已经逐字阅读，原字段含义如下：

| 字段 | 独立判断对象 | 不可自动推出 |
| --- | --- | --- |
| source_proof | 来源证明或新工作/综合/笔记身份 | 当前证明已完成 |
| current_proof | 本来源当前证明的作者标记 | 无条件、全域、定理正确或所有关联问题已解决 |
| internal_review | 当前算术/多路/候选/自攻记录 | 外审、盲独立审查或新颖性 |
| external_review | 同行外审记录 | 本表无一条登记外审 |
| implementation | 软件/audit/有限例/部分/无实现 | 数学算法不存在，或一般后端已经实现 |
| graph_status | 展示状态与细化范围文字 | 取代前面五轴 |

implementation_detail 393条、source_proof_detail 7条、internal_review_detail 5条、novelty 2条、supplementary_scope_reviews 5条、review_note 3条全部保留。有些 detail 明确给全源码行数/实际重放次数、递归1200链 RecursionError、原型所缺接口等，不能压成一个 PASS。supplementary_scope_reviews 只补所述局部复核，不改变其余轴。旧 high/low-gamma 的三个 review_note 明记撤回2026-10-18旧解释，不能让新更正冒充当时审计已发现。

## 全表分布与集合边界

"""
for k,v in axis.items():review_body+='- '+k+'：'+json.dumps(v,ensure_ascii=False)+'。\n'
review_body+="""

current_proof 的608个 complete 是作者按各条范围给的状态，另有19 candidate、8 conditional、2 depends_on_claims、3 direct；不允许把它们聚成640个完成数学定理。external_review 全640条都是 not_recorded。

asset claims 的不同身份640个，review 也640条，但不是同一集合：Q-CAG-HALF 只有资产包，旧图 kind=obligation；CERT-SOUND 只有 review，旧图 kind=lemma。实际620个 kind=claim 全被两表覆盖；图另有 lemma/obligation 等类型，集合等基数不能推出身份一致。图/claims 原件只作这项结构比较，没有本批额外清洗其全部数学。

## 必须保持的实际范围

四人1499/750只为福利上界、不认证锐性。一般弱 iid 桥已由既有完整 SPE 族反驳；五人 half 有完整精确计算机辅助证书，但 literal 交叉脚本导入 main evaluator，不是第二 standalone 验证器。六人目标不由五人成功或局部行验证推出。

WC 第602–608的共同尺度/社会包络/时钟前沿/峰值全状态等记录明确：校准接口 NO 不等于原游戏无解、规模超限只能报未完成、单条最佳回复循环不等于全局 NO；费用常数项或必用成本不得被零势压缩漏掉。第627项 S7 同作者/reviewer 与另外 root 检查的独立性如原字段陈述。

UM 均有实际接口限制：给τ held-cycle path 至多n步不含一般target finder；known structured backend 不等于一般UM；1200链递归失败是已记录真实实现边界；固定 k 的多项式次数不能称 uniform-in-k；数学有理 LP 规格和 bit complexity 证明不等于生产LP后端。候选、conditional、standing quantifier objections 保全。

下方每条是完整原对象，所有额外字符串/嵌套补充范围可在本页读到；JSON 语义保全而非复制一列总状态。相对路径以原冻结仓库根为基准。

## 全部640个身份

"""
for i,z in enumerate(reviews['entries']):
    review_body+='## 审查 '+str(i)+'：'+z['id']+'\n\n'+F+'json\n'+json.dumps(z,ensure_ascii=False,indent=2)+'\n'+F+'\n\n'
review_target=write('旧研究五轴审查的逐身份范围','research-assets/review-five-axis-complete','完整640项五轴、graph展示与全部可选detail；外审未记录，数学/实现/有限审计分开。',review_body)
dump(E/'review-record-destinations.json',[{'index':i,'id':z['id'],'target':review_target,'heading':'审查 '+str(i)+'：'+z['id'],'source_record':z} for i,z in enumerate(reviews['entries'])])

wcrows=[(i,z) for i,z in enumerate(catalog['entries']) if z['topic']=='weighted_congestion']
files_raw=(E/'original/research/weighted_congestion_frontier/FILES.md').read_text()
files_body="""FILES 是按人工数学成果包组织的旧 WC 读取入口，不是501份已证明定理或本批程序PASS的账本。实际有501条数据行，54个原 package 值（含空值）；空 package 的末段仍有表格并未遗漏。每行中文名称、位置、用途、角色、配套路径和 Claim 显示来自真实 catalog/assets。前批已逐条实读同 SHA 的501行名称/用途与全部语义，本批读取整个 FILES 外壳并以真实JSON重建全534265字节完全一致，非计数或DOM摘要代读。

完整表示绑定采用本批独立静态 writer：读取旧 check_wc_assets.py 的 render AST 字符串常量、旧 build_catalog.py 的 TOPICS/ROLES/PACKAGE_TITLES 常量及真实 catalog/assets，由新 rows/topic 实现重建排序、转义、Claim 前三及总数显示。没有 import/执行旧检查器，没有 INTEGRATION 哈希审核、没有 replay.py 或数学子suite运行。本次表示相等只认证 FILES 确为这些实际输入的该表示。

## 外壳独有合同和历史缺口

先读旧数学地图再选成果包；文件角色不代替审查等级，精确命题与五轴分开。原分支、commit、原 SHA、去处与退役理由另在 INTEGRATION；本批不把文件链接当已读取证明。

原命令 python3 tests/audits/weighted_congestion/replay.py --list 只供选择，再传代码路径；原规则要求临时重建旧相对布局且不覆盖冻结证据。实际浮点筛选、有限有理核验和一般证明范围不同。本批不重跑这些旧成功套件。

来源缺口的原断言是：resource_cone/review.md、nonseparable_frontier/proof.md 及所引未见程序、r2_orbit/review.md 在作者当时观察分支中未找到；不补造已审/已证，也不将其升为本轮完整全仓不存在证明。原 family/重复导航稿退出现行旧树、在 main 祖先可恢复，是作者历史说明，本批未 Git 对象核验。

## 当前数学时态

一些旧包的用途/限制保留原 Cd/ln d OPEN；后续全状态线性下界已否定原全类目标。正式证明逐态存在严格改善依前沿覆盖及同次数锚定修复，不能由路径环、某包题名或有限PASS推出。新的发展问题、特殊域和算法问题仍按各自条件开放；不会把历史表重写为已认证的证明。

## 全部行的自足保全

下列附录保留 FILES 的完整表格、包标题和可见Claim字符串，便于独立读全部名称/用途/角色。旧相对 Markdown 链接只作为冻结文本，在 fenced text 中不会误导为新树可点目标。完整原件也单独以原字节保存。

"""
files_body+=F+'text\n'+files_raw.rstrip('\n')+'\n'+F+'\n\n'
files_body+="原行的完整结构化去向及对应 catalog 索引见证据 files-record-destinations.json；不额外勾选501个被引源。所有18角色字典和人工用途的前批资源仍是相关表示，metadata 路径不自动成为推导超边。\n"
files_target=write('加权拥塞旧文件链的全部用途与导出合同','research-assets/wc-files-complete','完整FILES外壳及501数据行真实语义，与真实输入全字节绑定；历史缺口及当前线性下界分开。',files_body)
dump(E/'files-record-destinations.json',[{'catalog_index':i,'path':z['path'],'target':files_target,'source_record':z} for i,z in wcrows])

main_body="""本资源吸收三份冻结文件的独有登记内容：assets.json 的351资产包，review_status.json 的640身份审查，以及 WC FILES.md 的501行读取入口。它们是数学内容的范围/角色/审查/可复现性登记；包含真实数学断言但本批没有把351份被链证明重新证明一遍。全部主源已实际语义阅读，未读引用仍按引用处理。下列主题页逐条完整保留原条件、产出、限制和字段，未来读者无需凭总计猜内容。

## 版本和原件

两冻结提交：legacy-cleanup 68fad804ec5946cb296f77dc5b336308a66abf12；main aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c。三份文件均在两提交内容相同。

| 源路径 | 字节 | SHA-256 |
| --- | ---: | --- |
"""
for z in sources:main_body+='| '+B+z['path']+B+' | '+str(z['size'])+' | '+B+z['sha256']+B+' |\n'
main_body+="""

原件、source-manifest、真实依赖、全量去向、reading views 与自查位于 tools/evidence/assets-review-files-ledger。范围定位 entries[index] 从零开始，序号保留而不改身份。

## 资产、审查与文件链

"""
for p in asset_targets+[review_target,files_target]:main_body+='- ['+Path(p).stem+']('+Path(p).name+')。\n'
main_body+="""

资源类别不改变原数学对象所属存档；这里集中保存同一研究登记链，不按算法路线重组数学主树。相同字段可复用实际读过的精确字符串，不同量词不合并。全部351完整条目和640完整审查嵌套字段已在主题页保全；原始输入仅存档一次。

## 五处适用域损坏：实际发现而非新猜测

完整扫描351条得到恰五处 applies_when 为非空单字符数组：

| 原索引 | 资产身份 | 对应实际完整正文的范围 |
| ---: | --- | --- |
| 22 | five-site-fixed-factor-hardness | 两带标签设施；固定有理1<a<φ；共同五地点；正二进制原子客户；弱NP完全 |
| 27 | adaptive_greedy_reset_and_floor | 显式正有理原子/共同目录/k≥2；给在轨NE收益及删除装箱证书；有限完成，位多项式强化另依调度合同 |
| 28 | depth_three_box_selector_boundary | 特定k15严格贪心深度三树；16态6盒，唯一盒势极小者非NE但另有盒NE |
| 29 | boxed_lexmax_selector_boundary | 特定k11五站/64态24盒；固定占位盒内唯一收益字典序最大者非NE，原分配已NE |
| 30 | frozen_stationary_overload_completion | 给固定布局/普通帽/全覆盖纯种子，冻结超帽客户，核其全部替代；残余完成lift全游戏NE |

每个字符数组原值及 proof 路径保存在 metadata-analysis.json 和完整条目；不能把字符拼接成原句，因为重复字符及次序信息可能已丢。它们的形状像误将字符串去重为字符列表，这是我们的形状推断，未证明损坏产生在哪个作者程序。未修冻结 JSON，也未把上表回填冒充原字段。

实际 check_assets.py 完整源码只 require(applies_when and status and produces)，不验证其类型、每个条件是否完整可读；非空字符列表会通过这一个 gate。这是对源码布尔表达式的直接归纳，未执行整个旧检查器。建议最小修正是显式约定 applies_when 为非空完整条件字符串数组，拒绝全单字符数组；该结构修正仍不能证明数学域正确。本批未应用于冻结生成器或输入。

实际逐篇全文比较上述五篇新树正式正文，条件和有限/多项式/实现界分别得到上表说明。原表仍用其历史 status/limit，包括后来证明一般盒存在后应停止沿用的旧开放话语。旧正式页当时未取得 RANGE 主论文的事实保留；前批已读论文的独立导入不扩大到未交付 canonical 实现。

## 三处须追到数学的时态冲突

1. 第36项 status 写四人 sharp1499/750，limit 又写锐性 OPEN。实际完整四人根偏离证明只给 OPT4≤1499W/750，并声明不认证尖锐性；本资源不把作者冲突字段升为下界。三人锐性不自动给四人锐性。
2. 同项旧五人2.061695…及若干桥OPEN已被后续精确五人half/弱iid反例更新。五人53乘子的全域算术证明与实际交付验证器/依赖主 evaluator 的literal交叉脚本分开；弱iid m≥41族是既有解析结论，非本次发现，m20参数的直接有限见证与一般证明也分开。每份完整历史SPE、单位客户、共同目录、平局和空/重复主题始终保留。当前六人主问题不能因旧任意m任务指令改变。
3. WC较旧 Cd/ln d OPEN 与后续每p≥2^20全状态严格p/10改善同处冻结包。实际已全文读后者的全状态证明：前沿相位短窗不兼容、返回边、三元锚定修复和同次数整数预算共同给余量(2^p−p/10)/8。构造有限但规模不承诺多项式。取lnp>10C否定原任意固定C的次线性保证；不由有限审计或单环代证。

已读五人、iid全局/局部、四人、WC全状态正式页的快照和SHA见 dependency-manifest；没有覆盖其他Owner页，也不额外done它们。

## 五轴、显示和身份不等同

640条 external_review 全为 not_recorded。608 complete 只按所述范围，19 candidate、8 conditional、2 depends_on_claims、3 direct 分开。实现有63 implemented、382 audit_only、26 finite_example、16 not_applicable、20 partial、133 none；每条实际 detail 比分类更精确。implementation空路径与无数学算法、数学算法与已实现后端均不同。

asset各claims共640个不同身份，review也640条，却分别多Q-CAG-HALF/多CERT-SOUND。实读相关旧图记录，前者obligation后者lemma；620个kind=claim均覆盖。此处只核字段/身份，未读取全部图边关系的数学，也不声称其新图可直接导入。

FILES行只显示一个路径所关联Claim排序前三与总数，并不能由可见三项推出完整包身份；真实assets全部引用保留。相同标题/角色和配套路径不是证明依赖。另14个catalog.related字段未被旧消费者显示的问题已在前批实际归档；FILES全字节一致不证明所有catalog字段可见。

## 实际检查与复现边界

主源三件共1628475字节全部核 inventory SHA；直接读取已有缓存，无Git访问。351 assets全字段及640 review全字段原语义已读，精确重复人类字符串和已读 catalog 路径用有完整字典的视图复用；曾被输出截断的assets22–46没有当场标读完，后按小块/单条36补读。review连续0–639现全部完成。FILES外壳本批全读，501行与前批同SHA catalog已逐行实读语义通过新独立完整表示绑定复用；不是只按计数声称阅读。

新 bind_files.py 的一次完整表示检查PASS：534265字节、SHA2c906f6b1d7eecfc40f675ab817494679af9257bdf9ecd45cea18e473db454ee完全相等。新 self-check 只检原字节、全字段损失、资源去向、主源身份、图Claim覆盖、全部正式页C0和行尾空白；不是原旧suite运行或数学证明认证。曾对仅位置参数的read_review.py误传--help，得到ValueError；后按源码正确调用，无主源变化，失败如实存证。

旧check_assets的真实其它依赖包括graph、migration、crosswalk、learning manifest、代码目录及证据报告，尾部还调用active/WC/catalog检查器；本批不伪造布局、不运行这些旧链，不声称目录存在性或所有哈希PASS。旧check_wc对INTEGRATION的.py/.json字节审核与本批FILES静态表示绑定不是同一检查。没有新增数学有限游戏试验、外文取得、PDF/浏览器渲染或交互PASS。

## 接续与关系判断

应将这些页用于定位精确模型/证据/实现限制，再按引用对象实际读证明；字符数组的将来修复需以完整正文核域、保新版本，不覆写原输入。当前阶段二保存资源，阶段三逐对象建立有解释来源/实现/有限检查/反驳关系，不从351包、640ID或501链接机械造推导边。元数据孤立允许，无强制入边或连通。
"""
main_target=write('研究资产与五轴审查的语义合同','research-assets/ledger-contract','三源全部语义、351资产与640审查及501读取行保全；字符数组、锐性/时态纠错和真实表示检查边界明确。',main_body)
formal=asset_targets+[review_target,files_target,main_target]
dump(E/'formal-pages.json',formal)
dump(E/'reading-log.json',{'primary':'All three complete; metadata semantics only, no referenced proof targets extra done','assets':{'header':True,'complete_indices':list(range(351)),'raw_first':list(range(22)),'exact_dedup_view':'full strings at first use; exact catalog paths prior fully read; all role/optional fields, claims and list types retained','truncation_recovery':'22..46 initial output truncated and not acknowledged; reread22..26,27..35,36 separately with larger output,37..61 then rest in safe chunks'},'review':{'header':True,'complete_indices':list(range(640)),'raw_first':[0,1,2],'exact_dedup_view':'all novel human strings printed in full before codes reused; all five axes/graph/optional nested details retained','blocks':[[3,72],[73,172],[173,272],[273,372],[373,472],[473,572],[573,639]]},'FILES':{'all_shell_read':True,'all_501_row_semantics':'prior catalog-semantic-resources actual full-read same SHA input; complete new byte representation equality','package_values_including_empty':54,'whole_byte_binding':'full-files-binding.json'},'actual_comparison_full_texts':comparison+['prior exact five-half/iid/local snapshots in comparison'],'graph_and_claims_dependency_scope':'full structural fields/ID sets and two relevant node records only this batch; their whole mathematical claims not claimed read','old_math_suite_runs':0,'new_math_experiments':0,'new_static_representation_runs':1,'external_paper_or_render_passes':0})
dump(E/'attempts-and-boundaries.json',{'helper_help_error':{'command':'python read_review.py --help','exit_code':1,'exception':"ValueError: invalid literal for int() with base 10: '--help'",'cause':'new helper accepts integer positional ranges; read source and used correct ranges','input_mutation':False},'output_truncation':'initial assets22..46 view output truncated; no full-read acknowledgement until smaller re-reads; preserved views can overlap','prior_catalog_2198_checks':'did not cover C0; separate authorized format recovery was completed in prior batch, not retroactively hidden; all current formal pages have actual forbidden-C0 check','no_git':'no Git access or writes this batch; no lazy-fetch retry','old_programs':'not executed; no suite or INTEGRATION byte certification; no fake dependency run'})
dump(E/'self-check-plan.json',{'scope':'bounded source binding, full-field resource roundtrip, destinations, metadata sets, C0 and whitespace; no mathematical proof certification','required_originals':3,'required_asset_records':351,'required_review_records':640,'required_wc_catalog_rows':501,'required_formal_pages':len(formal),'char_array_expected_indices':[22,27,28,29,30]})
relation="""# 关系判断

三主源形成资产范围/审查轴/人工读取表示的资源关系：assets列模型与产出/限制、review分离五轴、FILES从真实catalog/assets显示501用途。完整字节表示相等只支持表示关系。每条元数据路径/Claim聚合不直接是数学推导。

实际正式正文支持四人上界而不认证锐性、五人half与一般弱iid旧桥纠错、WC全状态线性下界更新旧OPEN；五篇设施正式数学支持损坏applies_when之外的准确模型说明。其他Owner原页和冻结源不覆盖。MAX/RANGE数学导入与canonical实现保持分离。

第三阶段按证据逐对象解释来源、实现、有限核验、反驳和条件推广，不将351/640/501个索引机械导成边，不造强制连通或入边；资源暂未入新图的原因是当前阶段二完整语义保存尚在持续。
"""
(W/'relation-review.md').write_text(relation)
notes={
'790a17806fa34be04140':('完整773683字节header及351资产全部字段实读；applies_when/produces/limit/status/claims、八路径角色和所有optional解释均读取，精确重复字符串仅在实际已读后去重引用；截断22–46后按小块及36单条补读，未把计数当实读。','全文比较五篇损坏适用域对应设施正式数学、四人实际根界、五人half、全局/局部iid及WC全状态证明；角色/数学/软件/内外审分开。发现五处字符数组和四人sharp内冲突，保原件另写准确纠错；640身份集合与review不等同。','八专题完整保全351原对象、全部数学条件/产出/限制与来源解释，原字段/缺席/类型精确保全；独立总合同解释新旧时态及结构检查漏项，不额外done被引351包目标，不跑旧suite。',asset_targets+[main_target]),
'4564afcb575533e1c830':('完整320527字节header与640审查逐身份全字段/可选嵌套详情实读，连续0–639全部完成；精确重复human string在首见完整实读后复用，五轴、graph_status、393implementation_detail等不合并。','与351资产、620旧graph claim结构及两个独有kind、实际四人/五人/iid/WC完整正式证明比较；全部640外审not_recorded，candidate/conditional/direct保持，implementationdetail精确边界不被简化成PASS。','640完整源对象在自足五轴资源保全；保留撤回旧gamma解释、有限验证/缺实现/量词异议及审查独立性区别；不将作者complete升为所有引用源已证/已审，不新增数学认证或外审。',[review_target,main_target]),
'066c20466ed140e4bd78':('完整534265字节FILES外壳、全部包标题和501行名称/用途/角色/关联Claim语义；501同SHA真实catalog记录前批已逐条实读，本批读完独有外壳且新独立完整表示重建全字节相等，不以501计数或摘要代读。','实际check_wc/build_catalog源码、真实assets/catalog输入与旧路径/角色合同比较；完整静态AST常量与独立rows/topic重建PASS。另全文比较WC全状态线性证明，旧OPEN与当前后续分开；来源缺口只保作者当时观察。','完整FILES文本和501结构去向自足保全，实际表示绑定证据/原件SHA归档；未运行INTEGRATION检查或任何replay数学套件，未宣称全部被引证明/退役不存在性重新核实。',[files_target,main_target])}
receipts=[]
for z in sources:
    read,comp,decision,targets=notes[z['id']]
    receipts.append({'id':z['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':read,'comparison_note':comp,'decision_note':decision,'disposition':'integrated','targets':targets})
dump(W/'semantic-receipts.json',receipts)
candidatepaths=['research/current/claims.md','research/graph.json','research/index.html','research/reviews/README.md','research/templates/claim.md']
candidates=[]
for line in (R/'cleanup/inventory.jsonl').read_text().splitlines():
    z=json.loads(line)
    if z['path'] in candidatepaths:
        p=R/'cleanup/progress'/(z['id']+'.json')
        if not p.exists():candidates.append({'id':z['id'],'path':z['path'],'bytes':z['size'],'sha256':z['sha256'],'availability':'local progress file absent at read; Root must check latest global owner before formal claim','reason':'same metadata chain; full actual semantic read required, existing structure/byte binding is not already done'})
dump(W/'next-candidates.json',candidates)
(E/'README.md').write_text("""# 三源证据及真实边界

original保存三原件，不修损坏字段。source-manifest绑定inventory实际SHA；dependency-manifest是实际物化依赖，comparison保存真正已读正式正文/规则快照。related graph/claims仅结构与必要节点定位，不冒充全部数学审读。

read_assets.py/read_review.py及reading-views是实际完整阅读视图，精确重复字典及已读catalog路径复用；reading-progress/reading-log记录全部范围和截断补读。资产22/27/28/29/30的原applies_when字符数组是原输入问题，不是视图产生。

bind_files.py为新独立静态表示检查，实际一次完整534265字节一致，非运行旧check_wc或数学suite。metadata-analysis是新全字段/身份集合检查，不能认证数学。全量逐条去向保留source_record，正式页完整JSON可逆提取。

check_resources.py仅执行新必要结构/全字段/格式核验，不执行旧程序。C0检查为真实新增，不能追溯称前批2198检查覆盖。attempts-and-boundaries保存helper误传--help失败与truncation补读；没有PDF、交互、外文或新数学试验PASS。
""")
dump(E/'run-evidence.json',{'source_binding':'three cached originals actual full inventory SHA checked','new_complete_FILES_binding':json.loads((E/'full-files-binding.json').read_text()),'new_metadata_analysis':'metadata-analysis.json','old_check_assets_or_wc_or_catalog_executed':False,'old_replay_or_math_suite_executed':False,'new_math_audit_experiment':False,'helper_help_error_recorded':'attempts-and-boundaries.json','no_git_or_network':True,'scope':'representation/metadata and actual semantic reading only'})
print(json.dumps({'formal_pages':len(formal),'asset_records':len(assetmap),'review_records':640,'wc_rows':len(wcrows),'sources':3,'candidates':len(candidates)},ensure_ascii=False))
