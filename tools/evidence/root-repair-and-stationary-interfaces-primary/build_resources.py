from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import json,hashlib

R=Path('/workspace/scratch/37f0f9248cfc');C=R/'boss4-next-cache';REPO=R/'boss4-research'
S=C/'r3-root-repair-and-stationary-interfaces-primary';E=Path('tools/evidence/root-repair-and-stationary-interfaces-primary');W=Path('cleanup/workspaces/Boss4/r3-root-repair-and-stationary-interfaces-primary-next')
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):p=S/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
def read(p):return json.loads((S/p).read_text())
primary=read(E/'source-manifest.json');related=read(E/'related-source-manifest.json');byid={x['id']:x for x in primary+related}
ids=[x['id'] for x in primary];expected=['43fcfd09b6d0ae5d96b5','c57e4ec366e7af1be467','ef21819792cb2a9aac5f','793061843887102a114a','62fadc53e30b4b1c856b']
claim=read(E/'actual-claim-receipt.json');assert set(ids)==set(expected)==set(claim['ids']) and claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced'
for x in primary:
 p=json.loads((REPO/'cleanup/progress'/f"{x['id']}.json").read_text());assert p['owner']=='Boss4' and p['disposition']=='in-progress' and p['source_sha256']==x['sha256']
def link(i):return '../../../../'+byid[i]['preserved_path']
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
def header(id,kind,typ,title,status,summary,sources):
 a=['---',f'id: "customer-attraction/{id}"',f'kind: "{kind}"',f'type_tag: "{typ}"',f'title: "{title}"',f'status: "{status}"',f'summary: "{summary}"','source_refs:']
 for i in sources:
  for z in inv[i]['sources']:a.append(f'  - "source:{z["commit"]}:{z["path"]}"')
 return '\n'.join(a)+'\n---\n\n'
contexts=[
'archives/customer-attraction/state/引理/完整槽插入税与跨角色价格恒等式--引理.md',
'archives/customer-attraction/state/资料/首次饱和与独立审查的版本路由--资料.md',
'archives/customer-attraction/state/候选/最优并集税与平均真实菜单的付款接口--候选.md',
'archives/customer-attraction/state/反例/笛卡尔银行目录的逐人分数门槛反族--反例.md',
'archives/customer-attraction/state/问题/自由extra-one与iid安全值边界--问题.md',
'archives/customer-attraction/state/定义/自由分数背景安全门槛--定义.md',
'archives/customer-attraction/state/引理/笛卡尔目录的最优查询缺陷与三倍根修复--引理.md',
'archives/customer-attraction/state/定理/两名剩余三比较任意背景半覆盖--定理.md',
]
ctx=[]
for n in contexts:
 b=(REPO/n).read_bytes();cp(REPO/n,E/'context'/n);ctx.append({'path':n,'bytes':len(b),'sha256':sha(b),'snapshot':str(E/'context'/n),'actual_read':'full mathematical read in current/prior DM comparison, exact bytes reused; no extra source done'})
js(E/'context-manifest.json',ctx)
reuse=[]
for x in primary:
 old=C/'r3-first-saturation-and-insertion-credit-primary/tools/evidence/first-saturation-and-insertion-credit-primary/related'/x['id']/x['path']
 assert old.read_bytes()==(S/x['preserved_path']).read_bytes()
 reuse.append({'id':x['id'],'bytes':x['size'],'sha256':x['sha256'],'prior_full_read':'DM related-only, no primary done then','same_bytes':True,'old_path':str(old),'current_original':x['preserved_path'],'read_reuse':'honest complete prior read reused, pertinent passages checked; no claimed independent first reading'})
js(E/'prior-related-full-read-reuse.json',reuse)

P1=Path('archives/customer-attraction/state/候选/真实子树价格向量的共同静态背景归纳--候选.md')
body=(C/'learning-dy-common-background-draft.md').read_text().split('\n\n',1)[1]
body=body.replace('真正静态安全值v_r(b)允许查询独立的r−1合法整数主题对手混合。',r'''真正静态安全值允许查询独立的r−1合法整数主题对手混合，准确为

\[
v_r(b)=\min_{Q\in\Delta(\mathcal S^{r-1})}\max_{T\in\mathcal S}
\mathbb E_Q\sum_{x\in T}\frac1{b_x+1+c_x(B)}.
\]

有限零和minimax给其与max-query/min-static的通常安全值相等；本页只用上述min-cap表示及有限单纯形紧性保证最小值取到。''')
intro=f'''全文主源是[共同分布尝试4830B]({link('62fadc53e30b4b1c856b')})、[root-only检查点4419B]({link('43fcfd09b6d0ae5d96b5')})及[security路由1192B]({link('793061843887102a114a')})；均两冻结分支同字节。三件在DM只作related全读，现认领后正式逐源处置。原2026-10-23研究角色和路线限制只作历史材料，不覆盖当前执行指令。原件未改；没有新一般聚合下界、外审或新颖性声明。

'''
body=body.replace('## 模型和两个实际量',intro+'## 模型和两个实际量',1)
body+=r'''

## 当前对象的准确接续

[分数值定义](../定义/自由分数背景安全门槛--定义.md)和[extra-one边界](../问题/自由extra-one与iid安全值边界--问题.md)给t≤v的准确当前合同；[银行完整SPE](../反例/笛卡尔银行目录的逐人分数门槛反族--反例.md)使个体目标失败而不否定聚合。上述R的条件接入使用[三倍根修复](../引理/笛卡尔目录的最优查询缺陷与三倍根修复--引理.md)，与fresh缺陷候选身份不同。[任意背景两尾定理](../定理/两名剩余三比较任意背景半覆盖--定理.md)仅解决指定局部接口。

root-only源的其余有限和历史边界也完整见[已交版本路由](../资料/首次饱和与独立审查的版本路由--资料.md)，此处不覆写旧交付当时未执行stationary审计的事实。安全README所指指定SF-root现有[本批独立有限核验](../反例/真实尾平稳均值的额外查询封顶--反例.md)，并不支付本页所有子树价格向量。本文无原程序、新SPE扫描或安全LP运行；仅保准确条件步骤与真实未付义务。
'''
put(P1,header('real-subtree-price-vectors-common-static-background-induction','candidate','候选','真实子树价格向量的共同静态背景归纳','valid-conditional-vector-and-slot-embeddings; aggregate-payment-open; individual-extra-one-refuted','完整保留孩子标量与查询独立价格向量的归纳尝试、父槽嵌入和错误上界方向；root-only与FREE-ROOT另保量词，旧整数extra-one由Jensen和银行反族纠正而不误否定聚合。',[expected[0],expected[3],expected[4]])+body)

P3=Path('archives/customer-attraction/state/引理/两名剩余完整终局菜单的纯列封顶--引理.md')
body=(C/'learning-dy-pure-column-draft.md').read_text().split('\n\n',1)[1]
intro=f'''主源[6504B全人数独立重构]({link('ef21819792cb2a9aac5f')})已全文读，主体的全人数在轨系数边界已完整归入[插入税对象](../引理/完整槽插入税与跨角色价格恒等式--引理.md)；此页保它侧审独有的两人裸回复身份、精确交集税和纯列论证。另完整比较[5748B原身份稿]({link('c7681bcaecb3e63137ff')})、[6035B任意p推送]({link('6c84043505685faee8ec')})与[6262B菜单义务]({link('68ed7412ef2da880f80f')})，仅作related不额外done。源作者独立重构/内部审查与本次读后归档、外审分别说明；无外审或新颖性认证。

'''
body=body.replace('## 一般联合身份不提供一般符号',intro+'## 一般联合身份不提供一般符号',1)
body=body.replace('这是对每个p推送Q=p的曲率余项',r'''这里L来自在每个真实B后，把末位R与独立同边际R'比较：其裸值平均抵消，余下恰是sum g_x(p_xq_x−j_x)。membership展开给

\[
D_x=\frac{p_x}{b_x+1}-g_xj_x,\quad
C_x=p_x\left[\frac1{b_x+1}-g_x(p_x+q_x)
+\frac{2g_xj_x}{b_x+3}\right],
\]

代入并用0≤j_x≤p_x便得到显示的非负分解。这是对每个p推送Q=p的曲率余项''')
put(P3,header('two-remaining-full-terminal-menu-pure-column-cap','lemma','引理','两名剩余完整终局菜单的纯列封顶','proved-for-two-remaining-with-true-final-BR; no-general-joint-regret-sign','保完整终局COL与准确正交集税；恰一位后继的BR使最大裸回复列同时封顶全部额外查询，另比全局双主题势选择和任意p曲率推送，禁止外推到多后继。',['ef21819792cb2a9aac5f','c7681bcaecb3e63137ff','6c84043505685faee8ec','68ed7412ef2da880f80f'])+body)

report=read(E/'runs/stationary-independent-001/report.json');meta=read(E/'runs/stationary-independent-001/run-metadata.json')
assert meta['exit_code']==0 and meta['call_number']==1 and report['unit_clients']==1274
rows=report['all_43_history_rows'];d={tuple(x['history']):x for x in rows}
def table(head,rs):return '| '+' | '.join(map(str,head))+' |\n| '+' | '.join(['---']*len(head))+' |\n'+''.join('| '+' | '.join(map(str,row))+' |\n' for row in rs)
types=report['positive_types'];type_table=table(['mask','单位客户数'],types)
last_table=table(['首/第二']+list(range(6)),[[a]+[d[a,b]['all_action_values'][d[a,b]['action']] for b in range(6)] for a in range(6)])
second_table=table(['首/第二候选']+list(range(6)),[[a]+d[(a,)]['all_action_values'] for a in range(6)])
static_rows=[]
for t in combinations(range(6),3):static_rows.append([','.join(map(str,t)),sum(count for mask,count in types if any(mask&(1<<a) for a in t))])
assert max(x[1] for x in static_rows)==1032
js(E/'derived-static-coverage-display-table.json',{'role':'new presentation calculation from the already verified source type table; not a second strategy audit or new sample scan','rows':static_rows,'combinations':20,'argument':'repeated labels add no coverage and can be filled with distinct labels from six, so these 20 rows determine OPT3'})
coverage_table=table(['三个不同标签','覆盖'],static_rows)
prices_table=table(['查询']+list(range(6)),[['指定3π']+report['six_stationary_mean_fractional_query_prices'],['自由均匀3q']+report['six_free_uniform_fractional_query_prices'],['两个整数对手0,5']+report['six_integer_static_query_prices']])
P2=Path('archives/customer-attraction/state/反例/真实尾平稳均值的额外查询封顶--反例.md')
body=f'''# 真实尾平稳均值的额外查询封顶

## 被否定的构造与本次证据身份

[3963B完整原文]({link('c57e4ec366e7af1be467')})定义SF-root：任意合法背景b、余r≥2名完整纯SPE，强制根A后尾为B_2(A),…,B_r(A)，令P(A,B)为r−1名真实后继中标签B的频率。取平稳主题分布pi，定义客户边际pi_x=sum_(A含x)pi_A，再用L_x=r pi_x作为确定分数背景，要求所有纯查询的价sum_(x∈T)1/(b_x+1+r pi_x)≤根actual u。stationarity确实给随机完整叶的平均客户负载E_pi c_x(Z(A))=r pi_x，但这不自动控制全部查询。

本例r3、b0、单位客户/单位玩家、六个合法标签，全43有序决策节点纯SPE，保重复、离轨及平局。固定核P只有一个pi，故有限反例也排除在同一个核内另选平稳分布的修复。它不量化自由q、任意静态背景或任意核。

两份被原文引用的audit源（b59d80ac2b02969bd86e代码/a14a025eaabac25f48df JSON）经安全本地读取均缺blob，未尝试网络，未读或执行它们。[缺失原回执](../../../../{E}/absent-original-stationary-audit-manifest.json)准确保留。下面使用本次新增的独立定义级实现，仅从绑定MD的21项完整表展开1274名不同单位客户，不导入发现者代码、规范solver、LP或旧证书；这是一份新有限核验，不冒充原CLI/原JSON复现。

## 全部单位客户与完整策略

mask第a位为1表示该单位客户被标签a覆盖，相同mask重数仍是不同客户。21类合计1274：

{type_table}

分X={{0,1,2}}、Y={{3,4,5}}。完整策略根0；第二人见首主题在X取3，否则0；任意二历史(a,b)后，末位取b所属组三标签中最小未出现者。每组3标签、此前最多2标签，所有重复/离轨历史都有定义，不删平局。

终局z的角色i利润逐单位客户为sum_(x喜欢z_i)1/[喜欢z中标签的玩家数]，当前强制某行动后始终沿上述同一策略完成。下表每格为该二历史指定末动作的收益，**同时等于全部六候选行动的最大值**：

{last_table}

第二人的六行动值（包括其改变引起的原末位真实回复）为：

{second_table}

前三行规定列3，后三行规定列0，均为行最大。根六个强制分支的自身收益依次541/2,541/2,541/2,541/2,541/2,503/2，规定0最优。因此36个末节点、6个中节点和根均最佳回应，逆向归纳证明完整纯SPE。没有把末位BR搬到另一个历史，也没有仅查actual路径。

实际叶(0,3,4)，利润(541/2,613/2,269)，W846。所有20个不同标签三元组的覆盖如下；重复不增加覆盖，总可补成不同三标签，因此这张全表也给允许重复时的OPT3：

{coverage_table}

最大1032由(0,1,2)达到，其未覆盖仅mask16的202人及mask48的40人，所以1274−242=1032。2W−OPT3=660>0，此完整SPE不反驳half。

## 唯一平稳分布及全部查询价格

六强制根叶依次(0,3,4),(1,3,4),(2,3,4),(3,0,1),(4,0,1),(5,0,1)。所以P的X行在3/4各给1/2，Y行在0/1各给1/2，第2/5列零。平稳方程先迫pi2=pi5=0，再迫两组总质量各1/2、四剩余坐标相等，故唯一pi=(1/4,1/4,0,1/4,1/4,0)。新增核验直接代回piP=pi，平稳方程加归一化秩6，与此解析唯一性一致。

按21类客户直接求和，得到全部六查询价：

{prices_table}

指定3pi均值的最大值在查询2，为123652/455=541/2+1149/910>根541/2。确定分数背景恰为完整叶期望负载仍会失败；不是挑错平稳类或仅找到浮点微差。

自由q均匀于六主题时，质量3背景的cap=441/2<541/2；固定两个合法整数对手(0,5)的cap=252，所以真正v3≤252且W−3v3≥90，不能把252叫精确v3。这份输入不否定自由extra-one或聚合桥。旧原文把一般Mfull/整数extra-one也记OPEN，当前已由[银行反族](../反例/笛卡尔银行目录的逐人分数门槛反族--反例.md)及Jensen纠正；那是另一个完整SPE，不追改本原文的历史字节，也不混成这个1274客户实例的结论。

固定均值SF-root与[完整随机列的插入税/平稳身份](../引理/完整槽插入税与跨角色价格恒等式--引理.md)不同；也不同于只评价同一个查询分布的二次型，不能由此直接否定每个stationary strong-push合同或所有自由菜单。在这个固定P内另选平稳分布不能修复；改变P是另一构造，未由此否定，更一般选择仍须明确它的量词和付款。

## 本次唯一新增核验和未取得的证据

[新增代码](../../../../{E}/new-independent-stationary-check.py)完整可读、仅Python标准库Fraction；真实输入是上述绑定原MD，不读任何原JSON。一次原样调用，Python版本/命令/cwd/代码SHA/输入SHA/时长/exit见[运行身份](../../../../{E}/runs/stationary-independent-001/run-metadata.json)，完整43行六行动收益与slack、核/价格见[新报告](../../../../{E}/runs/stationary-independent-001/report.json)。实际0.366842281秒、exit0、stderr空，核258项含43自身及215非自身比较，89项平局含自身，最小slack0。只有一次核验主体执行，没有把自比较全称为真实偏离。

正文20行静态覆盖表是随后从同一已核客户表生成的展示计算，不是第二次策略核验或扩样。原audit调用0次；父研究员当时重放原实现的说法仅保源作者历史记录，本次无法逐行评价缺失实现。DM旧页当时“未独立重核此例”事实不改；本页新增证据有自己的代码与运行身份，没有外审、新颖性或最小实例声明。
'''
put(P2,header('real-tail-stationary-mean-extra-query-cap-counterexample','counterexample','反例','真实尾平稳均值的额外查询封顶','finite-complete-SPE-counterexample-with-new-once-independent-recheck; original-audit-blobs-absent','1274单位客户三人六主题的全部43有序历史和258比较自足保留，唯一尾核平稳均值使查询2超过根1149/910；自由背景、聚合和half未由此否定。新增独立实现与缺失原audit明确分开。',['c57e4ec366e7af1be467','793061843887102a114a'])+body)
formals=[P1,P2,P3]
js(E/'formal-resource-manifest.json',[{'path':str(p),'bytes':(S/p).stat().st_size,'sha256':sha((S/p).read_bytes())} for p in formals])
cp(Path(__file__),E/'build_resources.py')
print(json.dumps({'new_formals':[str(p) for p in formals],'formal_bytes':sum((S/p).stat().st_size for p in formals),'claim_tip':claim['remote_tip'],'original_CLI':0,'new_independent_CLI':1,'static_display_rows':20},ensure_ascii=False))
