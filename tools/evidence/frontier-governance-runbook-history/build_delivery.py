"""Five historical governance sources: full resource, scope and exact receipts.

No legacy instruction or command in the sources is executed by this writer.
"""
from pathlib import Path
import collections, hashlib, json, re

E=Path(__file__).resolve().parent
S=E.parents[2]
R=S.parent.parent/'boss4-research'
F=S/'archives/weighted-congestion/state/资料'
W=S/'cleanup/workspaces/Boss4/r3-frontier-governance-runbook-history-next'
F.mkdir(parents=True,exist_ok=True)
W.mkdir(parents=True,exist_ok=True)

def read(p):
    return json.loads(p.read_text())

def save(p,obj):
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

sources=read(E/'source-manifest.json')
by_id={x['id']:x for x in sources}
formal=[]

def write(name,ident,summary,ids,body):
    refs=['source:'+z['commit']+':'+z['path'] for i in ids for z in by_id[i]['sources']]
    refs=list(dict.fromkeys(refs))
    meta={'id':ident,'kind':'resource','type_tag':'资料','title':name,
          'status':'historical-governance-source-fully-read-not-current-execution-instruction',
          'summary':summary}
    text='---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in meta.items())
    text+='source_refs:\n'+''.join('  - '+json.dumps(x,ensure_ascii=False)+'\n' for x in refs)+'---\n\n# '+name+'\n\n'+body.rstrip()+'\n'
    p=F/(name+'--资料.md');p.write_text(text);rel=str(p.relative_to(S));formal.append(rel);return rel

def original(ident):
    z=by_id[ident]
    # Four-backtick fence safely contains source's own triple-backtick commands.
    return '\n## 完整冻结原文：'+ident+'\n\n原路径 `'+z['path']+'`，'+str(z['size'])+'字节，SHA256 `'+z['sha256']+'`。\n\n````markdown\n'+(S/z['saved_path']).read_text()+'````\n'

save_ids=['d78ecf1fb73afec03867','6f98455158cbf0135936']
save_body=r'''这两份源保存的是历史 checkpoint 与异步公屏的阅读/报告合同，不含独立数学定理。本批只将它们作为冻结材料完整阅读；下方命令文本不被执行，也不构成当前消息发送、分支修改或研究角色授权。当前本轮程序/分支和数学焦点由根规则及现有任务确定。

## 阶段保存实际声称什么

CHECKPOINT 先要求可复用正文、精确身份和对应核验，再通过旧 tools/work.py checkpoint。它列出的默认范围是“当前加权拥塞主题”的正式稿、候选、审查、程序、证据和共同账本；其他文件要显式列入。各独立 clone 使用 main，程序执行commit/普通push/远端确认，可达后才返回pushed并给commit/hash/descriptor；重复运行不造空提交，真实冲突保留双方并停住。

这些是该文档的操作主张，不是本批重新验证了其实现或当前默认范围。尤其同批RUNBOOK已转向CAG、两份先前AGENTS又有不同分支约定，所以不能据这段旧默认值去保存本轮六人清洗成果。原字节保留，不改成新的命令说明，也不让它覆盖当前禁止本子任务Git操作的分工。

其可复用的知识边界是：候选按候选保存，失败按准确失败保存；提交不提升数学状态，阶段成果不等于主问题解决。成果不能只留公屏；重要结果可用已推送的冻结descriptor分享；日常中途工作无需所有人预先审查，承重结论升级另需独立攻击。这是研究记录与数学论证的分离，不是建立本轮额外批准流程。

## 异步公屏实际声称什么

board/README把消息和BOARD.md放在wcg/board分支、main保留入口。它描述提示词指定角色号的Work对话按群聊读取、发表、回应，再继续研究；thread与reply-to连接讨论，成果消息附已推送文件descriptor。read/send示例、RUNBOOK和PROTOCOL入口完整保留在原文。

“查看实时公屏”URL是冻结文件内的链接字符串，不表示本批访问了实时分支、读取了任何消息或确认当前频道布局。另一个validation链接固定到bd7798d5bbcc8086217ff54d7f91b445d0374b4f，是历史验证入口；本批未读取或重跑它，不能将URL存在升级成软件PASS。此说明也没有授权本轮发送普通消息或私聊。

当前仍要求实际pushed后才能声称远端保存。本文档保存历史pushed语义供审查，不把“文档说程序会返回”与“某次操作确实已完成”混为一谈。本批的真实推送由协调方另行处理；资料本身不代替推送回执。
'''
for ident in save_ids:
    save_body+=original(ident)
save_path=write('阶段保存与异步研讨的历史证据合同','weighted-congestion/frontier-checkpoint-board-history','完整旧checkpoint与board说明、报告语义与当前未执行范围；提交/消息不代替数学。',save_ids,save_body)

role_ids=['68d87916bd603f7d0016','9d2f5834f5c80b256bfd','e7949e82834fb08f51e5']
role_body=r'''本资料保存旧RUNBOOK及两个角色路径在任务迁移后的兼容含义。五源两冻结refs均同字节，不能因路径叫weighted_congestion_frontier就恢复旧拥塞任务，也不能因文件名CLEANER/PAPER_WRITER把本对话切成相应角色。

| 冻结路径 | 实际指向及独有语义 | 保留的边界 |
| --- | --- | --- |
| RUNBOOK.md | 操作统一在customer_attraction/RUNBOOK.md，根work.py完整入口；shared/unrelated-machines旧绑定保留 | 写的是一般Q-CAG-HALF优先，恢复旧题另需当时新的用户指令；本轮现焦点按根AGENTS为六人和清洗任务，旧句不取消它 |
| prompts/CLEANER.md | 明说只是兼容链接，不再维护独立角色或可复制指令；指向customer_attraction/CLEANER.md | 不执行所链角色，不把旧清晰者完整UM提示词作当前cleaner指令 |
| prompts/PAPER_WRITER.md | 同样是兼容链接，但独有目标为customer_attraction/EDITOR.md | 论文者路径已归并为整理者入口，不等于旧W-随机身份写作角色仍在运行 |

三个入口都保当前CAG存档和根程序/历史清单定位；两个prompt明确只剩Boss、清洗者、整理者三角色。此为冻结历史组织状态，不覆盖当前Boss编号授权或本轮不部署数学Agent的规则。普通角色名不产生数学真值或审查层级。

## 与真实历史前身的全文比较

本批已实际全文读取三份独立历史前身，仅作相关比较，没有给它们额外done：

- 历史RUNBOOK源ID249ab71c9bc2fc7c7daf，2173字节，SHA cedfd6d3639eda519a28895f319ebcae07f2aa31604294ca6cb5d7a42a69f9f7。它的当前题是UM-TARGET-v1、save unrelated-machines，唯一程序曾在旧tools/work.py；新clone默认新题、旧shared绑定保留，显式paths替换整个默认范围，只有pushed且远端含提交才报告保存。它还列旧save/shared、队列retry保持原ID/原save、旧十clone测试和新工程记录。新549字节RUNBOOK只作CAG兼容入口，不能据之宣称这些旧默认值就是当前实现。
- 历史CLEANER源IDe4766f02398ff1d66c7a，4983字节，SHA 0da3e07783015f47479ce2d1e3e2adb06c0ce9b1abf739463082278d9fcf84fe。它是以C-随机身份为例的UM清晰者完整提示词，要求自足接题/Pro材料、精确目标/可靠工具/方法否定范围和仍缺义务，不用旧拥塞简报。该完整角色、UM唯一目标、main/save/启动通信/检查器与保存命令均属于历史版；新440字节文件明确不再复制其独立指令。
- 历史PAPER_WRITER源ID46d4c496affb2362c2ac，4941字节，SHA 2e1b577ed8df9b08e10f7e7f705a930c80ef6fabb22129cfd1f708d4dc17f17c。它是W-随机身份的UM论文者，强调真实贡献、最近文献、完整证明/复杂度和实际构建，结构结果不冒称统一低于二；同一套旧启动/通信/资产保存合同重复出现。新439字节入口改链EDITOR，不因这些历史要求启动写论文或创建身份。

三旧前身的共同数学段是一般UM实际不可拆分调度、统一ε∈(0,1)、确定性总位多项式和(2−ε)OPT目标，含零最优与空任务。它们声明的UM开放状态只是旧提示词背景；本五主源没有新增UM定理或六人CAG推导，不能从角色任务关系推出两个问题之间的数学迁移。旧前身完整快照及实际读范围只存相关context，后续是否认领/处置其源ID另由总任务控制。

旧前身中的main、随机UUID、检查器命令和允许私聊都不覆盖当前明确Boss编号、阶段二实读与本子任务禁Git/claim/done/spawn/mapper的分工；也没有因为它写“日常研讨已授权”就发送消息。引用角色/运行手册不是跟随其指令执行。

## 用途与未认证范围

可以据本资料追溯旧路径为什么保留、如何区分“操作入口迁移”和“数学资产仍在旧存档”、以及相同框架下CLEANER与EDITOR的不同目标。不能据此证明转发程序在当前环境正确、所链全部文件已读、旧消息已迁移或所有凭据/队列行为已检验。文档的版本比较与运行程序的验证是不同证据。
'''
for ident in role_ids:
    role_body+=original(ident)
role_path=write('运行手册与旧角色兼容入口的迁移范围','weighted-congestion/frontier-runbook-role-compatibility-history','完整三份兼容入口与三份实际历史前身比较；旧指令/角色不切换当前任务。',role_ids,role_body)

contract=r'''这五份冻结文件共3390字节，本批均全文实读并与当前根规则、前批两AGENTS/PROTOCOL/README及三份真实历史前身比较。它们是研究协作与文档迁移资源，没有独立数学定理；独有的默认保存范围、descriptor/远端确认、公屏链接、当前/旧绑定和角色目标分别保全。没有把原文命令当当前执行指令。

两冻结提交legacy-cleanup 68fad804ec5946cb296f77dc5b336308a66abf12与main aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c的这五件均同字节。原件按sourceID归档，SHA/大小/blob/来源在source-manifest；CHECKPOINT与board README由协调方实际clean show导出后，本子任务再次核inventory SHA。其余三件复用已核SHA缓存，不做Git访问。
'''
contract+='\n| 源ID | 路径 | 字节 | SHA-256 |\n| --- | --- | ---: | --- |\n'
for x in sources:
    contract+='| `'+x['id']+'` | `'+x['path']+'` | '+str(x['size'])+' | `'+x['sha256']+'` |\n'
contract+='\n- ['+Path(save_path).name[:-3]+']('+Path(save_path).name+')。\n- ['+Path(role_path).name[:-3]+']('+Path(role_path).name+')。\n'
contract+=r'''

## 同一冻结集合里的三个时点

1. CHECKPOINT仍称默认保存“当前加权拥塞主题”、各clone main和旧tools/work.py完整命令；它不反映本轮实际清洗分支/作用范围。
2. 历史前身RUNBOOK/完整CLEANER/PAPER_WRITER描述UM-TARGET-v1、unrelated-machines新默认和旧shared绑定兼容。
3. 本批549/440/439字节兼容入口已转向一般Q-CAG-HALF、根work.py和三角色。先前批两AGENTS又分别保main495字节的一般CAG与legacy615字节的六人/cleanup文字。当前执行仍以根AGENTS和本轮明确任务为准，不能按ref名字、路径或“当前”一词选择旧指令。

这不是数学上三题有推导关系，也没有将旧WC状态改成CAG状态。原资产、旧绑定与旧事件保持身份的说明值得保留；不自动恢复旧研究、不因转向默认题改写旧shared事件。旧协议有价值原则可以用于理解来源，但不形成额外审批或操作授权。

## 不把历史报告合同当新运行证据

CHECKPOINT中的pushed含义、board README中的实时URL/历史validation定位是原作者操作说明。本批没有执行checkpoint/read/send、读取实时公屏、访问validation URL、改变绑定或发送DM；没有重新认证当前转发实现/队列/远端分支。代码/文档/某次实际回执分别保存。根任务后续真实pushed才是本批远端保存依据。

候选、失败和阶段成果按准确范围保存，提交不升级数学；日常工作不强制全员前置审查，承重数学状态提升需要真实独立攻击。这些语义没有被本批变成强制持续review角色。当前阶段二也不导入关系图或要求连通。

## 全文去向和自查

五源全部字节在两个主题资料的四反引号原文块内完整保留（安全包含原三反引号shell块），来源和实际命令本身不删。每个源均逐源integrated：即使共同兼容文字重复，CLEANER→CLEANER与PAPER_WRITER→EDITOR两个目标不同，当前批没有用未读角色名推断duplicate。后续若有完全相同字节的别名，可在实际实读/核SHA后引用相同资料并逐源说明，而不能只凭文件名或计数勾选。

原件、真实相关快照、来源/去向、五条receipt、C0/行尾空白和完整原文回读自查位于tools/evidence/frontier-governance-runbook-history及独立workspace。自查只认证字节/去向/格式，不证明数学或旧程序正确。三历史前身是比较依赖，不在本五源receipt集合中，也不额外done其源ID。
'''
contract_path=write('协作保存与兼容治理五源的版本审查','weighted-congestion/frontier-governance-five-source-contract','五源全部语义和版本差别、原件去向及当前未执行边界；不将旧规则作为新授权。',list(by_id),contract)

targets={ident:[save_path,contract_path] if ident in save_ids else [role_path,contract_path] for ident in by_id}
save(E/'resource-targets.json',targets)
save(E/'formal-manifest.json',[{'path':p,'bytes':(S/p).stat().st_size,'sha256':sha(S/p)} for p in formal])
read_notes={
'd78ecf1fb73afec03867':'完整1034字节CHECKPOINT实读，包含原shell块、旧WC默认保存范围/显式路径、独立clone main、commit/push/远端确认/pushed descriptor、空提交/冲突、候选失败及独立攻击界。',
'68d87916bd603f7d0016':'完整549字节RUNBOOK兼容入口实读，包含CAG当前入口/根程序、shared与UM旧绑定保留、恢复旧题授权和历史清单；与2173字节真实UM前身完整比较。',
'6f98455158cbf0135936':'完整928字节board README实读，包含wcg/board/main定位、指定角色号、thread/reply-to/冻结descriptor、read/send示例和固定commit validation链接；不声称读实时链接。',
'9d2f5834f5c80b256bfd':'完整440字节CLEANER兼容文件实读，明确不维护独立角色/可复制指令，目标customer_attraction/CLEANER；与4983字节UM旧C-角色前身全文比较。',
'e7949e82834fb08f51e5':'完整439字节PAPER_WRITER兼容文件实读，目标是EDITOR而非旧独立论文者；三角色/根入口/旧hash全文去向保存，与4941字节旧W-角色前身全文比较。'}
receipts=[]
for ident in by_id:
    receipts.append({'id':ident,'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,
      'read_note':read_notes[ident],
      'comparison_note':'全文比较当前根AGENTS/OBJECTS/cleanup、前批双AGENTS与协议/README及三历史前身；区分旧WC/main、UM/save和CAG兼容时点，旧任务/命令/角色不覆盖当前六人清洗。文档pushed/live链接不作本次执行证据。',
      'decision_note':'独有保存/公屏/绑定/角色目标及全部原文进入自足资料；共同字句未替代逐源阅读。integrated仅为文档资源处置，不运行旧命令、不发消息、不额外done引用源或证明。',
      'disposition':'integrated','targets':targets[ident]})
save(W/'semantic-receipts.json',receipts)
deps=[]
for row in read(E/'preclaim-context.json'):
    p=S/row['saved'];deps.append({'path':row['saved'],'bytes':p.stat().st_size,'sha256':sha(p),'source':row['source'],'actual_read_scope':row['scope']})
save(E/'dependency-manifest.json',deps)
save(E/'reading-scope.json',{'actual_claim_confirmed':'ea3104d097fbb7cd99ce70a61c04f7f60e71f1c3 pushed/synced reported by Root','primary_ids_full_read':list(by_id),'primary_bytes':sum(x['size'] for x in sources),'primary_output_truncated':False,'new_related_full_reads':['249ab71c9bc2fc7c7daf historical RUNBOOK','e4766f02398ff1d66c7a historical CLEANER','46d4c496affb2362c2ac historical PAPER_WRITER'],'current_rules_and_previous_protocol_resource':'complete prior actual reading reused, snapshots bound','excluded':'all live board/validation/referred current roles and programs not automatically read/executed; no extra source done'})
save(E/'attempts-boundaries.json',{'primary_export':'Root actual clean show exit0 for CHECKPOINT1034B and board README928B; this agent verified exact inventory SHA after reading full originals','other_primary':'same SHA cache files materialized only after successful formal claim','git_network_program_or_message_actions_by_this_agent':[],'old_successful_suite_reruns':[],'source_read_failures_or_truncations':[],'new_checks':'exact primary/related bytes, full source preservation in formal blocks, precise receipt targets, flat metadata, C0 and whitespace only'})
save(W/'next-candidates.json',read(E/'next-candidate-snapshot.json'))
(W/'relation-review.md').write_text('''# 本批关系审查\n\n五源是文档迁移与协作资源，没有独立数学定理。旧checkpoint、公屏消息、兼容角色和历史前身之间是来源/迁移/报告合同，不能冒充数学推导。完整主源已归位；未进入mapper、不造图连通。旧指令只作内容，不产生本轮Git/通信/角色执行授权。\n''')

checks=[]
def check(name,ok):
    checks.append({'check':name,'passed':bool(ok)})
    if not ok:
        raise AssertionError(name)

inv={x['id']:x for x in map(json.loads,(R/'cleanup/inventory.jsonl').read_text().splitlines())}
for x in sources:
    p=S/x['saved_path']
    check('primary exact byte/SHA '+x['id'],p.stat().st_size==x['size'] and sha(p)==x['sha256'])
    check('exact inventory identity '+x['id'],all(x[k]==inv[x['id']][k] for k in ['path','size','sha256','blob','sources']))
    text=(S/targets[x['id']][0]).read_text()
    check('complete original formal block '+x['id'],'````markdown\n'+p.read_text()+'````' in text)
    check('full source line count '+x['id'],len(p.read_text().splitlines())>0)
for p in formal:
    t=(S/p).read_text();meta=t.split('---\n',2)[1]
    check('formal flat MATEK '+p,all(re.search('^'+k+':',meta,re.M) for k in ['id','kind','type_tag','title','status','summary','source_refs']))
    check('formal C0 '+p,not any(ord(c)<32 and c not in '\n\r\t' for c in t))
    check('formal trailing whitespace '+p,all(l.rstrip()==l for l in t.splitlines()))
for x in deps:
    check('real dependency byte/SHA '+x['path'],(S/x['path']).stat().st_size==x['bytes'] and sha(S/x['path'])==x['sha256'])
check('exact5 primary receipt set',{x['id'] for x in receipts}==set(by_id) and len(receipts)==5)
for x in receipts:
    check('full semantic receipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note']) and all((S/p).is_file() for p in x['targets']))
check('two role destinations distinct','../../customer_attraction/CLEANER.md' in (S/by_id['9d2f5834f5c80b256bfd']['saved_path']).read_text() and '../../customer_attraction/EDITOR.md' in (S/by_id['e7949e82834fb08f51e5']['saved_path']).read_text())
check('old checkpoint WC/current runbook CAG both retained','当前加权拥塞主题' in (S/by_id['d78ecf1fb73afec03867']['saved_path']).read_text() and '当前主攻Q-CAG-HALF' in (S/by_id['68d87916bd603f7d0016']['saved_path']).read_text())
out={'scope':'new exact byte/full literal preservation/receipt and format only; no old code/math/visual/live-board certification','passed':True,'checks':len(checks),'formal_forbidden_C0':0,'details':checks}
save(E/'self-check.json',out);save(W/'self-check.json',out)
(E/'README.md').write_text('''# 治理与兼容入口五源证据\n\n五件原文均实际完整读取、核inventory SHA；CHECKPOINT/board README由Root actual clean show后再核SHA，另三件复用同SHA缓存。两主题资料完整保全部原文，四反引号可包含旧shell代码块。\n\n三历史前身已全文读作真实版本比较，仅为dependency，不在5receipt范围。旧角色与指令不切换当前任务，不执行任何旧Git/checkpoint/通信命令。live URL只保原文字符串，不声称访问或PASS。\n\n自查只检字节、全原文、receipt及MATEK/C0/空白，不是数学/软件/远端保存认证。协调方应先实际pushed再done。\n''')
(W/'delivery.md').write_text('''# 五源完整交付\n\n三份资料自足保全五主源3390B及实际历史对照。均逐源integrated；兼容文字重复也保存各自不同目标和读取证据，不凭角色名自动duplicate。无Git/claim/done/mapper或旧程序执行，无live board/validation认证。\n\n按copy-files精确复制，实际checkpoint pushed后再done；下一5别名候选仅当时local无progress，Root核owner/claim后可续派。\n''')
print(json.dumps({'formal_files':len(formal),'formal_bytes':sum((S/p).stat().st_size for p in formal),'source_bytes':sum(x['size'] for x in sources),'receipts':len(receipts),'checks':len(checks),'passed':True},ensure_ascii=False))
