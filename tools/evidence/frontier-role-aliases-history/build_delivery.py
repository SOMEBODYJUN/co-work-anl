"""Exact alias disposition after full source reading; no source instructions run."""
from pathlib import Path
import hashlib,json,re

E=Path(__file__).resolve().parent
S=E.parents[2]
R=S.parent.parent/'boss4-research'
F=S/'archives/weighted-congestion/state/资料'
W=S/'cleanup/workspaces/Boss4/r3-frontier-role-aliases-history-next'
F.mkdir(parents=True,exist_ok=True)
W.mkdir(parents=True,exist_ok=True)

def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

sources=read(E/'source-manifest.json')
by_id={x['id']:x for x in sources}
texts={i:(S/x['saved_path']).read_text() for i,x in by_id.items()}
extract='e4f5cfc3fa0d04478fdb'
boss='49d60d648d222d8f3cfc'
boss_aliases=['91f8d305df4b7343d87b','9481228f7835e0de76b0','48830fda8f25d265156f']
name='旧角色短入口的精确别名与版本身份'
path=F/(name+'--资料.md')
target=str(path.relative_to(S))
metadata={'id':'weighted-congestion/frontier-short-role-aliases','kind':'resource','type_tag':'资料','title':name,'status':'historical-aliases-fully-read-four-exact-body-duplicates-one-representative','summary':'五份短入口逐ID/原路径保全，两组精确正文去重；旧长版角色独有内容和当前不执行边界分开。'}
refs=['source:'+z['commit']+':'+z['path'] for x in sources for z in x['sources']]
body=r'''本对象整理五份已经逐份全文读取的冻结短prompt，不执行其中“请使用当前角色”等句子。它们没有独立数学定理；作用是保留旧路径的兼容入口。旧文件名、当前短正文和旧长版是三层身份，不能只按标题或数量判断重复。

两冻结refs为legacy-cleanup 68fad804ec5946cb296f77dc5b336308a66abf12和main aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c；每份源在两个refs中同字节。source-manifest逐ID保存blob、SHA、大小与原路径，五件原件仍独立存在，不用一个文件覆盖其它路径。

## 五条实际去向

| 源ID与原文件名 | 短正文实际目标 | 精确重复判断 | 原路径的历史区别 |
| --- | --- | --- | --- |
| e4f5cfc3fa0d04478fdb EXTRACTOR.md，440B | customer_attraction/CLEANER.md | 与已实际读完的前批CLEANER.md源9d2f5834f5c80b256bfd全字节相等；正文duplicate | 旧提取者E-负责重建工具输入/输出/量词/证明/位复杂度和失败边界，与旧清晰者C-不同 |
| 49d60d648d222d8f3cfc MODELS.md，443B | customer_attraction/BOSS_START.md | 本批443B共同正文的代表，integrated；选择代表不表示数学优先级或时间先后 | 旧1069B模型配置，内容是模型与工具配置，不是数学模型定义 |
| 91f8d305df4b7343d87b PEER.md，443B | customer_attraction/BOSS_START.md | 与MODELS代表全字节相等，duplicate | 旧1211B是UM内部子研究任务，Git/对外发言由boss汇集，不创建独立Work身份 |
| 9481228f7835e0de76b0 PRO_ATTACK.md，443B | customer_attraction/BOSS_START.md | 与MODELS代表全字节相等，duplicate | 旧2108B是外部Pro的自足UM任务；不要求Git/仓库能力，文件就绪不代表交付材料已实际完成 |
| 48830fda8f25d265156f TEAM.md，443B | customer_attraction/BOSS_START.md | 与MODELS代表全字节相等，duplicate | 旧26374B是完整UM主研究者提示词，有独有全量词、反面方向及生产合同，不能按本短入口duplicate |

以上duplicate只指本批主源短正文与明确代表的全部字节/语义重复。五个路径角色的不同历史含义、来源身份和原件去向由本表及逐源receipt保留。不能把旧长版TEAM或任何旧角色职责一并勾作重复，亦没有额外done这些历史来源。

## 两组共同正文全部语义

每份短入口都说明：当前主攻一般Q-CAG-HALF、存档customer-attraction，此路径仅兼容，不再维护独立角色或可复制指令；当前只有Boss、清洗者、整理者，操作用根work.py；旧全文按原路径/hash进入历史清理清单。EXTRACTOR组指向CLEANER，443B组指向BOSS_START，这是两组惟一实际目标差别。

这里的“当前”是冻结源里的时点，不能覆盖本轮根AGENTS的六人CAG、阶段二清洗、明确Boss编号及本子任务禁Git/claim/done/spawn/mapper约束。读到BOSS_START不等于变成新boss或恢复UM反面研究；MODELS文件名不授权切换模型/开代理，PEER不要求本轮新开研究者，PRO_ATTACK不触发外部Pro任务。角色入口没有证明任何近似界、困难性或六人半覆盖。

## 与旧长版的真实全文比较

本批已全文读并核inventory SHA的历史前身如下，只作相关依赖；当前progress确认它们已由Boss2或Boss5 integrated，不复领、不重复done。

| 旧历史源ID | 字节与SHA-256 | 独有内容及正确保留位置 |
| --- | --- | --- |
| 8366e50d948f4eed2dcc EXTRACTOR | 4928；a847262e1099c9b9d60ce1ab2dca429d4078905b9a6bfbdca21e71b22bfb6a87 | 重建工具签名、Paper Fact/重构、新增机制、失败边界；不得未经证明迁移旧博弈模型接口。既有《历史角色提示词三件套》保存其职责 |
| e3a9705a13103f887a69 MODELS | 1069；ada0800ba03e8596ba174fc1d8e7ad9e6ebec4baa68b87096df3a0a1006504a3 | 两模型/ultra的请求配置与实际工具能力、贡献来源、干净上下文先重构与知情攻击区别；配置说明不是当前能力认证 |
| 713691c9011b0e1bfd7d PEER | 1211；6614fae45b5215f8af76883097ed7fef0476c44dda962ee9ef519f423d015163 | 精确子义务、边界/同时容量/位复杂度、有限计算不代证明，内部角色不独立推送；既有角色资料保持这层身份 |
| a1bbcde5ba02475f5871 PRO_ATTACK | 2108；1b215a8df0645dbf7487b5e371810c9f5f1173fa592b163be52c236e47939eaa | 外部Pro的UM模型、统一ε/实际分配/总位多项式、配置gap不是一般算法下界；旧拥塞简报不能代新题材料 |
| 91c1bb29b3f2c25e9b7f TEAM | 26374；ae30c5493d6481195b2871e6de2dc1f41578a08b8569093522e563ede5524cff | 完整UM主研究提示、逐固定ε反面方向、复杂度假设、真实OPT gap/全低负载decoder/位多项式规模、探索与后置攻击、保存和通信合同；既有TEAM量词资料独立integrated |

旧TEAM把UM-TARGET-v1的原命题保持为∃统一ε、∃确定性总位多项式算法、∀合法非负有理/∞矩阵，输出实际不可拆分调度且≤(2−ε)OPT，含空任务/OPT0；迁移时点主攻其在明确复杂度假设下的全ε反面。它同时说原目标及一般反面仍OPEN、固定比例hardness/配置gap/有限搜索不够。方向命令不是数学证据，这些旧全量词不随短443B入口自动变成CAG结论。

已全文比较现正式《历史角色提示词三件套》与《历史共同研究提示词TEAM兼容入口与量词边界》，它们准确保留旧长版独有合同，不能让新短入口的duplicate处置吞掉旧版。PRO前身的正式来源去向按其已有progress是《接题来源映射与文献导入的版本边界》；本批只定位该去向，没有冒称全文重读该20133B综合资源。历史前身原文/当前两份实读正式资料快照及精确范围均在dependency-manifest。

## 共同正文代表，完整原字节

下列只去掉同一正文的重复展示，原件五件仍全保。EXTRACTOR的440B与前批CLEANER原件已逐字比较；443B的四份原件逐份全文读取并逐字比较。读范围不是由哈希或文件数推测。
'''
body+='\n### 440字节组：EXTRACTOR（亦与前批CLEANER同字节）\n\n````markdown\n'+texts[extract]+'````\n'
body+='\n### 443字节组：MODELS/PEER/PRO_ATTACK/TEAM共同正文\n\n````markdown\n'+texts[boss]+'````\n'
body+=r'''

## 检查、版本与当前边界

两组差别由实际目标文件名产生，版本分组只按精确字节，不按角色名称聚类。完整5receipt明确每源的实际读取、比较、代表和唯一去向；MODELS代表integrated，EXTRACTOR及后三alias为duplicate。四个duplicate不会因此被解释为没有读取。

本批只做文件读取、字节绑定、原文去向、角色/版本比较及格式自查；没有运行旧work.py、找凭据、Git/消息/远端写入，没有执行旧提示词的模型选择或研究命令。所谓程序只维护三个角色是冻结文档说法，不认证当前程序实现。所链历史清单/当前BOSS或CLEANER并未因链接就逐个新完成；本批没有新数学suite、外文取得、PDF/视觉或mapper认证。

后续程序源和测试是另一批，要按真实输入/输出/版本与副作用逐源读，不能从这些兼容说明猜测实现正确。当前资料只作为别名/来源/文档迁移资源，不能造数学derives或强制图连通。
'''
text='---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in metadata.items())+'source_refs:\n'+''.join('  - '+json.dumps(x,ensure_ascii=False)+'\n' for x in refs)+'---\n\n# '+name+'\n\n'+body.rstrip()+'\n'
path.write_text(text)
save(E/'formal-manifest.json',[{'path':target,'bytes':path.stat().st_size,'sha256':sha(path)}])
aliases=[]
for x in sources:
    ident=x['id'];rep='9d2f5834f5c80b256bfd' if ident==extract else boss
    aliases.append({'id':ident,'path':x['path'],'bytes':x['size'],'sha256':x['sha256'],'representative_id':rep,'target':target,'disposition':'integrated' if ident==boss else 'duplicate','whole_primary_actually_read':True})
save(E/'alias-dispositions.json',aliases)
receipts=[]
old_names={'e4f5cfc3fa0d04478fdb':'提取者EXTRACTOR，转CLEANER','49d60d648d222d8f3cfc':'模型配置MODELS，转BOSS_START','91f8d305df4b7343d87b':'内部研究PEER，转BOSS_START','9481228f7835e0de76b0':'外部Pro任务PRO_ATTACK，转BOSS_START','48830fda8f25d265156f':'完整主研究TEAM，转BOSS_START'}
for x in aliases:
    ident=x['id'];duplicate=x['disposition']=='duplicate'
    receipts.append({'id':ident,'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,
     'read_note':f'完整{x["bytes"]}字节原件独立全文实读并核inventory SHA；全部短入口文字、实际目标和历史清单路径保留。'+old_names[ident]+'的原文件名角色语义单独读取比较，不只按相同文件数判断。',
     'comparison_note':'与当前根规则、前批CLEANER原件/角色迁移、五份真实旧长版全文及已done历史资料比较；两冻结ref同字节。'+('逐字证明与代表'+x['representative_id']+'全文相等；' if duplicate else '作为443B共同正文的明确代表；')+'旧长版角色独有内容不受短版重复处置影响，旧指令不切换当前身份/任务。',
     'decision_note':('duplicate仅指已经全读且全部字节/语义相同的短正文，' if duplicate else 'integrated保存共同443B短正文代表，')+'逐ID原路径、角色历史和实际目标完整进入别名资料；五原件独立保留，无额外done旧历史源或执行新指令。',
     'disposition':x['disposition'],'targets':[target]})
save(W/'semantic-receipts.json',receipts)
deps=[]
for x in read(E/'comparison-manifest.json'):
    p=S/x['saved'];deps.append({'path':x['saved'],'bytes':p.stat().st_size,'sha256':sha(p),'source':x['source'],'actual_read_scope':x['scope']})
save(E/'dependency-manifest.json',deps)
save(E/'reading-scope.json',{'actual_claim_pushed_synced':'313c9cc98748b7a3a6bf6c12449849f222686cd0','primary_ids_independently_fully_read':list(by_id),'primary_bytes':sum(x['size'] for x in sources),'group_counts':{'440B':1,'443B':4},'duplicate_basis':'actual full text and whole-byte equality, exact target links and per-filename role semantics; not count inference','historical_predecessors_full_read':5,'current_cleaned_resources_full_read':2,'extra_sources_done':[],'primary_read_truncations':[],'external_web_visual_runtime_actions':[]})
save(E/'attempts-boundaries.json',{'preclaim':'only related context and previously done historical predecessors read; primary materialized after Root actual pushed claim','failures_or_truncated_primary_reads':[],'source_hashes':'five original SHA checked against inventory; related five predecessor SHA also inventory checked','not_run':['Git/claim/done/spawn/mapper','old prompt instructions/identity changes','work.py/remote board/messages','credential search','mathematical suites/network/PDF/render']})
save(W/'next-candidates.json',read(E/'next-candidate-snapshot.json'))
(W/'relation-review.md').write_text('''# 别名关系范围\n\n本批是一份文档来源/兼容迁移资料，无数学定理。EXTRACTOR440B与前批CLEANER精确重复；MODELS代表443B共同正文，其余三件duplicate。原路径角色语义、旧长版及已done来源各自保留，不能把全部旧TEAM当duplicate。未进入mapper或造数学边；旧命令没有获得本轮执行授权。\n''')

checks=[]
def check(name,ok):
    checks.append({'check':name,'passed':bool(ok)})
    if not ok:raise AssertionError(name)
inv={x['id']:x for x in map(json.loads,(R/'cleanup/inventory.jsonl').read_text().splitlines())}
for x in sources:
    p=S/x['saved_path'];check('primary exact bytes/SHA '+x['id'],p.stat().st_size==x['size'] and sha(p)==x['sha256']);check('inventory exact identity '+x['id'],all(x[k]==inv[x['id']][k] for k in ['path','size','sha256','blob','sources']));check('whole primary text preserved '+x['id'],'````markdown\n'+p.read_text()+'````' in text)
check('EXTRACTOR exactly prior CLEANER bytes',texts[extract]==(E/'context/prior-CLEANER-original.md').read_text())
for ident in boss_aliases:check('443B entire original equals representative '+ident,texts[ident]==texts[boss])
check('two distinct exact targets','../../customer_attraction/CLEANER.md' in texts[extract] and '../../customer_attraction/BOSS_START.md' in texts[boss] and texts[extract]!=texts[boss])
check('four duplicate one representative',sum(x['disposition']=='duplicate' for x in aliases)==4 and sum(x['disposition']=='integrated' for x in aliases)==1)
check('formal all C0',not any(ord(c)<32 and c not in '\n\r\t' for c in text));check('formal trailing whitespace',all(l.rstrip()==l for l in text.splitlines()));meta=text.split('---\n',2)[1];check('formal flat MATEK',all(re.search('^'+k+':',meta,re.M) for k in ['id','kind','type_tag','title','status','summary','source_refs']))
for x in deps:check('real comparison bytes '+x['path'],(S/x['path']).stat().st_size==x['bytes'] and sha(S/x['path'])==x['sha256'])
check('five exact receipt identities',{x['id'] for x in receipts}==set(by_id) and len(receipts)==5)
for x in receipts:check('full semantic receipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note']) and (S/x['targets'][0]).is_file())
out={'scope':'new exact source/full-text alias/receipt and format only; no old program or mathematical certification','passed':True,'checks':len(checks),'formal_forbidden_C0':0,'details':checks};save(E/'self-check.json',out);save(W/'self-check.json',out)
(E/'README.md').write_text('''# 五短角色别名的证据\n\n五原件独立全读/核inventory SHA。440B EXTRACTOR与上批CLEANER全字节相等，四443B彼此全字节相等；共同正文只展示两次，五源原路径/角色历史/旧长版区别逐ID保全。\n\n五旧长版前身均已由其他Owner integrated，本批实际全文读作比较且不再done。两个现行相关资料亦全文比较；未全文读综合PRO资源的事实明确留存。\n\n四duplicate/一integrated有明确代表和去向，不能按计数推定实读或吞掉旧TEAM26374B。自查只检字节、完整正文、逐源receipt及格式，无Git/网络/身份切换/旧程序执行。\n''')
(W/'delivery.md').write_text('''# 五别名源交付\n\n一份资料完整保两组短正文、五原路径角色语义和历史前身范围，五原件保留；四duplicate/一代表integrated。Root按exact manifest复制、实际checkpoint pushed后再done。后续board程序5已列实际candidate快照，待正式claim后独立审计源码/测试/版本，不执行远端写入或找凭据。\n''')
print(json.dumps({'formal_files':1,'formal_bytes':path.stat().st_size,'primary_bytes':sum(x['size'] for x in sources),'receipts':5,'duplicate':4,'integrated':1,'checks':len(checks),'passed':True},ensure_ascii=False))
