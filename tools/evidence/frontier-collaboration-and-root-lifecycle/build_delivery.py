"""Complete historical root/program and collaboration-test semantic resources."""
from pathlib import Path
import ast,hashlib,json,re
E=Path(__file__).resolve().parent;S=E.parents[2];R=S.parent.parent/'boss4-research';F=S/'archives/weighted-congestion/state/资料';W=S/'cleanup/workspaces/Boss4/r3-frontier-collaboration-and-root-lifecycle-next';F.mkdir(parents=True,exist_ok=True);W.mkdir(parents=True,exist_ok=True)
def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
src=read(E/'source-manifest.json');deps=read(E/'dependency-manifest.json');releases=read(E/'release-dependency-manifest.json');byid={x['id']:x for x in src+deps+releases}
def text(i):return (S/byid[i]['saved_path']).read_text()
def obj(name,ident,summary,selected,body):
 p=F/(name+'--资料.md');meta={'id':'weighted-congestion/'+ident,'kind':'resource','type_tag':'资料','title':name,'status':'historical-software-complete-read-with-finite-versioned-evidence','summary':summary};refs=list(dict.fromkeys('source:'+z['commit']+':'+z['path'] for x in selected for z in x['sources']));p.write_text('---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in meta.items())+'source_refs:\n'+''.join('  - '+json.dumps(x,ensure_ascii=False)+'\n' for x in refs)+'---\n\n# '+name+'\n\n'+body.strip()+'\n');return str(p.relative_to(S))
function_notes={
'credential':'外部文件中TOKEN匹配取set恰一个不同串；不做远端认证。',
'environment':'剔除11个Git路由变量、禁交互；可生成临时可执行ASKPASS shell并保TemporaryDirectory对象。',
'run':'Git subprocess包装，45秒超时、限定token正则脱敏/1200字符错误；不天然禁止真实网络。',
'value':'把run stdout解码strip成字符串，不额外认证。',
'default_repo':'按自身文件/父目录.git存在推repo，找不到则cwd/co-work-anl；不是自动认证实际根。',
'checked_repo':'resolve后要求目录/.git存在且Git顶层等所给root；否则先start提示。',
'auth':'显式文件优先本地wcg.tokenFile；外部路径形状验证、可记路径，然后构造环境。',
'actor':'显式start actor、WCG_ACTOR、已存actor、R-UUID回退；安全ID/既有绑定一致才可记本地config。',
'write_lock':'git-common-dir/wcg-checkpoint/writer.lock非阻塞flock；仅同common-dir writer协调。',
'sync':'目标分支fetch/merge，必要时stash含未跟踪并恢复index，真实冲突保备份；synced不等于pushed。',
'save_id':'安全save首次绑定，既有绑定拒绝显式改；默认依程序版本和start阶段不同。',
'role_id':'限定存档角色词表，首次绑定，拒绝换角色；不是验证Work/用户实际身份。',
'workspace_path':'安全save/actor拼research/workspaces并逐组件拒绝本地symlink。',
'workspace_init':'目标分支下profile/schema/instance校验、显式resume；新文件才创建，不覆已有README草稿，仍需checkpoint发表。',
'visit':'限定工作区相对普通UTF8文件；fetch所选远端ref，ls-tree普通blob再show；不采用本地草稿。',
'start':'新clone/旧恢复、origin核对、版本分支/身份/存档/角色顺序、workspace回执及可选近期公屏；非事务性零副作用操作。',
'board':'转发相邻board.py，legacy附绑定board分支；若缺程序报sync提示。',
'main':'ASKPASS/argparse/命令分发及错误边界；非start通常也先auth/actor/save，本地配置可能写。',
'checked_branch':'legacy核ref格式/坏名称/token形状，文件分支排除公屏命名。',
'branch_id':'legacy取显式/已绑/当前长期分支fallback或main；拒绝改已有绑定。',
'board_branch':'legacy取显式/已绑/长期分支专用board或wcg/board；与文件分支分离。'}
functions=[];constants=[]
for ident in ['d9b5b49ab665613450d6','3c0404b7974eca538863']:
 tree=ast.parse(text(ident));values={}
 for n in tree.body:
  if isinstance(n,ast.FunctionDef):functions.append({'source_id':ident,'name':n.name,'start_line':n.lineno,'end_line':n.end_lineno,'complete_semantic_role':function_notes[n.name]})
  if isinstance(n,ast.Assign):
   for target in n.targets:
    if isinstance(target,ast.Name) and target.id in ['REMOTE','TOOLS','WORKSPACES','DEFAULT_SAVE','DEFAULT_BRANCH','DEFAULT_BOARD_BRANCH','DEFAULT_START_SAVE','RESEARCH_ENTRIES','ROLE_PROMPTS','CLEANUP_ROLE_PROMPTS']:values[target.id]=ast.literal_eval(n.value)
 constants.append({'source_id':ident,'exact_constants':values})
save(E/'root-function-inventory.json',functions);save(E/'root-constant-contracts.json',constants)
b1=r'''
本对象完整保存两份根work.py的真实生命周期控制，不把旧根入口作为本轮新指令。main源d9b5b49ab665613450d6是26199字节/522行，SHA6946299455b653526a548d7108a29480ab328acf7cc4392bfa6959e870229f1d，只有aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c；legacy源3c0404b7974eca538863是31695字节/618行，SHAbc2cfda7fc2b12b7fa21d75b1266a14bc6993a40e6a31cc90e0f8eb88b301c4e，只有68fad804ec5946cb296f77dc5b336308a66abf12。

两份此前均已逐段独立全文读取作为兼容入口真实依赖，本批正式认领后重核全字节SHA并复用完整读取，18/21个顶层函数及全部常量/CLI/异常均保留。完整原件在[逐源表](../../../../tools/evidence/frontier-collaboration-and-root-lifecycle/source-manifest.json)，[精确diff](../../../../tools/evidence/frontier-collaboration-and-root-lifecycle/root-version.diff.json)、[逐函数行号/语义](../../../../tools/evidence/frontier-collaboration-and-root-lifecycle/root-function-inventory.json)、[全部常量/入口字典](../../../../tools/evidence/frontier-collaboration-and-root-lifecycle/root-constant-contracts.json)另存。

## repo、凭据、actor、save与role是哪些合同

程序可作为上传的独立bootstrap或仓库根入口。default_repo仅按文件位置及.git存在猜root，否则用cwd/co-work-anl；checked_repo另核真实Git顶层。默认REMOTE是冻结源的GitHub仓库字符串，本批未访问。run清11个Git路由变量、禁终端提示、45秒超时；凭据外部文件按限定TOKEN正则取唯一不同匹配串，不要求全文只有token，也没有网络认证。auth取显式token_file或本地wcg.tokenFile，拒绝resolve后在repo内，显式选项可写本地路径config。environment按需创建临时0700 ASKPASS shell，用shlex.join调用当前Python/当前脚本，列表保留TemporaryDirectory生命周期；helper中不写token，Username/Password只回固定用户/外部匹配串。原代码不自带file-only协议或全局配置隔离，本批复现器才增加。

actor选择顺序为显式start参数、WCG_ACTOR、已存wcg.actor、R-UUID随机回退；安全ID1至64，已有ID不同则拒绝，首次记本地config。save也首次记wcg.save，拒绝已绑clone显式换save；role仅在适用存档词表中首次绑定/拒绝改绑。它们是自声明本地标签，**不是服务端权限或实际人/Work认证**。这些旧随机回退和三角色程序不覆盖当前明确Boss编号、结果分支和清洗协议。

非start命令通常也先checked_repo/auth/actor/save，故read/visit/pending等可能创建身份/save配置或临时helper；不能概括成完全零本地副作用。只读访问函数保护HEAD/index/草稿的性质与“不写任何本地文件”不同。startup失败也不保证回滚此前clone/auth/config/sync等步骤；其顺序必须按具体版本解释。

## 同步、保存和本地/远端状态

write_lock与checkpoint共用git-common-dir/wcg-checkpoint/writer.lock，非阻塞flock，只协调同一common dir，跨clone由正常Git竞争处理。sync拒绝错文件分支、未完Git操作或unmerged index，fetch所选远端分支到tracking ref；若remote tip已是HEAD祖先，直接返回synced，可能仍有本地未发布提交。否则把脏工作含未跟踪stash，再普通merge，失败先abort，之后按原index恢复stash；恢复成功只丢自己仍在stash顶的副本，冲突时保完整stash及双方内容并报错。它会更新本clone tracking refs/FETCH_HEAD和可能工作树，区别于board客户端在临时仓库读。

synced表示同步关系/保留工作，不是checkpoint pushed；root checkpoint只是把显式paths/message（legacy另create-branch）转给同repo相邻checkpoint.py并传认证环境，不在root重实现scope/history/descriptor审计。snapshot、pushed_head、remote_tip及数学完成仍分别由各自真实证据承担。未完成/候选/错误草稿可以被程序备份，程序不会读数学来判真。

## 工作区身份和访问

workspace_path用安全save/actor拼research/workspaces/save/actor，逐本地组件拒绝symlink。workspace_init须在main（main版）或绑定目标（legacy版），profile/README不得为symlink；profile恰schema/save/actor/instance，schema精确int1且instance为32位小写hex。新clone本地instance与已发表同号profile不同，只有显式resume才采用旧instance，否则保材料并拒绝。不存在的profile/README才用排他创建，已有README/草稿不覆；本地wcg.instance记配置。回执remote_directory_exists只是tracking tree里目录存在，不代表这次本地新草稿已发表；仍要实际checkpoint。

visit限定安全actor与工作区内相对文件，拒绝绝对、越界、反斜杠、NUL/换行/冒号以及本地workspace symlink路线；fetch所选远端文件分支后，用literal ls-tree只接受100644/100755 blob再show/UTF8解码。main只读origin/main，legacy默认绑定branch并可显式另branch。它不会把未推送本地草稿当远端文件，也不切换HEAD或改index/草稿；但会更新tracking refs/FETCH_HEAD，且分发前auth/actor/save仍有前述可能副作用。源码当前Path解析行为和有限测试不等于所有路径/平台的完备证明。

## start的真实时序与handoff

共同流程先拒绝负board-limit。新repo须空目标、凭据在外；clone后核origin fetch/push和用户给remote完全一致；启动会按版本做auth、分支、身份/存档/角色、sync、工作区。main版在sync前选择actor/save/role及Git署名；旧wcg/work分支可安全sync后保旧main到本地recovery ref并重命名main。legacy版先确定/记wcg.branch及公屏路线、sync，比较正在运行的bootstrap位置/原字节与同步后repo根程序；不同则在绑定新阶段/角色之前转交根程序，显式参数原样带入。后者不是把旧上传程序永远当当前实现。

legacy在实际根程序后才选择actor、save、role、board配置，再准备workspace；必要旧wcg/work迁移仍保recovery。两个版本都返回repo/branch/actor/save/workspace、已注册研究入口/角色路径、recent_board_limit等JSON。默认board_limit=0仅回执，不自动读公屏；显式正值在回执之后调用board view。故首个JSON不单独认证后续board读取成功。未知save返回空题目入口/提示，不猜别的数学模型。

## 全部命令路由

| 命令 | 实际调用与边界 |
| --- | --- |
| start | 上述clone/绑定/sync/workspace/可选board read，不是本轮自动执行授权 |
| sync | 文件分支直接同步，保冲突/备份；synced不等于发表 |
| read | board view显式save，可带json/thread/limit；负limit拒绝 |
| send | board say显式actor/save，转text或text-file、thread/reply/asset/kind/event-id、mentions/to |
| dm | 必须另一安全非空收件人；有text才say，无text走双方peer view，不退回公开 |
| inbox | view显式actor/save/inbox；默认unread，可all/limit/json |
| ack | board ack逐ID、actor/save，只有已读含义不采纳数学 |
| workspace | 本人工作区准备/显式resume，不发表 |
| visit | 远端已推送普通文本工作区访问，保护HEAD/index/草稿 |
| pending | 本地outbox列表，非按当前save过滤 |
| retry/discard | 原event ID及发送者转给board，保原body/save而不重路由当前主题 |
| checkpoint | 相邻checkpoint程序，显式paths替默认的语义由该程序承担 |
| board-init | 仅legacy，初始化绑定board，已有schema3消息保留 |

两版main捕获Stop/OSError/ValueError、按限定SECRET脱敏并exit2；argparse也有自身退出码。它没有当前clean claim/done接口；本轮Root正在使用的新版管理程序与这两冻结实现不是同一源码身份。

## 全部函数角色和版本差别
'''
b1+='\n| 函数（共同名只列一次） | 真实职责 |\n| --- | --- |\n'+''.join('| `'+n+'` | '+d+' |\n' for n,d in function_notes.items())
b1+=r'''

| 控制 | main d9… | legacy 3c… |
| --- | --- | --- |
| 新clone文件分支 | main | cleanup/research-foundation-20261028，显式/旧绑定可保 |
| 新start save/role | customer-attraction/boss | 长期默认分支用repository-cleanup/cleaner；普通main兼容仍CAG/boss |
| 公屏 | wcg/board | 长期分支默认wcg/board-cleanup-20261028，wcg.boardBranch绑定，不得等文件分支 |
| checked_branch/branch_id/board_branch | 无这三函数 | 核ref、名字、token形状，拒绝公屏作文件分支/改已绑定路线 |
| 研究入口字典 | CAG/UM/shared（shared prompt=null） | 加collaboration清理入口/角色映射 |
| workspace/sync/visit | main固定路线 | 按绑定分支；visit可显式别的branch |
| 首次发布/初始化 | root无create-branch/board-init参数 | checkpoint --create-branch及board-init转发 |
| bootstrap更新 | 无legacy新增的同步后handoff层 | 同一上传文件可交还同步后新根程序，保显式参数 |

当前根规则则是明确Boss编号、rebuild/research-v2、六人CAG的精确域与清洗阶段，不继承旧R-UUID、默认研究题、main或另建远端分支许可。本对象只保历史控制和准确用途；代码路径/角色关系不推导任何UM/WC/CAG数学结论。

## 实际验证与复用

两root已在前批按精确SHA配全部真实代码/存在性输入，main26、legacy34原生命周期测试PASS。本批保原JSON/原stderr并核source_inputs，**不重跑这60个无疑旧实例**。本批另新增每ref17协作测试，含10独立本地clone、20消息、10并发checkpoint及私聊/workspace边界，见[协作检查资源](协作路由测试的完整义务与版本证据--资料.md)。这些有限软件证据不认证所有并发、生产服务、有效凭据或数学真假；未在业务clone运行旧start、改身份或向真实公屏发消息。
'''
p1=obj('根生命周期程序的绑定同步与版本合同','frontier-root-lifecycle-control-contract','两根实现18/21函数全文和默认/分支/身份/workspace/路由完整合同，复用精确旧60实例并区分新协作检查。',[x for x in src if x['path']=='work.py'],b1)

test_notes=[
'十个独立本地P00–P09 clone；每个给环后继1DM+1公开提及，并发共20不同ID；公开每人仅10消息且无PRIVATE，inbox各2来自前驱；ack后空。再十个并发checkpoint仅本人workspace，保未跟踪本地草稿，远端各note/SHA可重放，只main与board两个远端ref。',
'retries=1时fetch离线保私聊pending原intent；真实本地push后注入丢响应仍留pending；第三次同ID恢复只一事件并清pending、默认render无私聊文本。',
'默认Markdown/JSON/thread/limit及派生BOARD.md不含私聊sentinel，公开事件仍可见，raw state不当权限隔离。',
'inbox只给收件者的DM、提及；普通公开不通知、不送Charlie；双方peer view只相应DM。',
'私聊回复不得公开、换收件人、第三方或跨save；反向同双方同save允许。',
'公开回复不能跨save；无save历史事件按shared，显式shared回复兼容。',
'同ID改to/save/mentions均Conflict，保持原一事件。',
'离线私聊pending下Charlie retry/discard在变更前拒绝；原Alice可恢复且只一事件。',
'unread查询不自动标记，limit1只显示最新；ack精确删被读ID，Charlie非法ack不改Bob游标。',
'显式空actor/save/peer或自己peer都拒绝，不作公开默认值。',
'重复workspace/start保自定义README、未发表草稿、profile字节和暂存状态。',
'visit拒actor/路径越界、绝对、反斜杠、冒号、换行及本地symlink，不读fixture私有sentinel。',
'visit取远端已发表peer文本且HEAD/index/status/未暂存草稿字节保持。',
'已发表同号profile的另clone需显式resume，随后instance及既有正文保持，远端只两分支。',
'错主题分支或detached时sync拒绝且HEAD不变。',
'dm/send的空收件者及空dm读取都拒绝，不能把私聊sentinel落公开。',
'远端symlink叶不当普通file读，显式空save也拒绝。']
tests=[];index=0
for ident in ['4a9d84f0b03bbbf6c01a','086e17d599de8edb10a2']:
 for n in ast.walk(ast.parse(text(ident))):
  if isinstance(n,ast.FunctionDef) and n.name.startswith('test_'):
   tests.append({'source_id':ident,'name':n.name,'start_line':n.lineno,'end_line':n.end_lineno,'actual_assertion_scope':test_notes[index]});index+=1
assert len(tests)==17;save(E/'test-assertion-inventory.json',tests)
b2=r'''
本对象完整整理test_collaboration_concurrency.py源4a9d84f0b03bbbf6c01a（6523字节/132行，SHA1138797e282479a26d2725c2dcddf593acff2e5a9d776d243b423db5cc954cb2）和test_collaboration_safety.py源086e17d599de8edb10a2（14771/248，SHA7ae9fb938865fbfc53c1a762854fbcf90df47a1632bd2d443c8fce48bc803c64）。两件两冻结refs同字节，全部fixture、导入、断言和main独立实读，原件不修。

它们只有2个并发+15个安全测试；import test_work/test_board是模块导入，手动调用其setUp/cleanup准备fixture，**不执行旧TestCase方法**。本批discover只匹配test_collaboration*.py，结果也确为每版17，而非把之前26/34/22测试再算一遍。路径fixture含真Git bare remote/clone、合成作者/actor和合成凭据，所依赖八件原码此前均已完整读并核SHA复用。

## 全部17项真实义务
'''
b2+='\n| 原测试名 | 实际条件与断言 |\n| --- | --- |\n'+''.join('| `'+x['name']+'` | '+x['actual_assertion_scope']+' |\n' for x in tests)
b2+=r'''

私聊只按actor/to在展示/导出中筛选，完整Git事件同仓可读，没有访问控制或加密。ack是本地read receipt不代表数学采纳。workspace身份碰撞检测不是实际人认证；seed中的“proof/boundary/result”文本只是fixture数据。本地十clone的20消息/10 checkpoint不能推广成500真实Work或GitHub吞吐。只有指定场景与这些断言有新增实测证据。

## 本批新增与此前精确复用

新[复现器](../../../../tools/evidence/frontier-collaboration-and-root-lifecycle/run_isolated.py)按同ref真字节/执行位配root、board、checkpoint、wrapper、test_work和test_board fixture；完整依赖在[dependency-manifest](../../../../tools/evidence/frontier-collaboration-and-root-lifecycle/dependency-manifest.json)。main17/17 PASS（原日志27.559秒）、legacy17/17 PASS（33.137秒），新增34个实例，各只跑一次。原stdout/stderr、Python/Git版本、命令、环境和输入SHA在[runs/summary.json](../../../../tools/evidence/frontier-collaboration-and-root-lifecycle/runs/summary.json)和各JSON。旧root生命周期26/34实例只复用，原回执source_inputs逐项绑定本批两个root SHA。

所有Git/start/合成身份/消息/迁移/保存都只在新临时root，GIT_ALLOW_PROTOCOL=file，系统/全局配置禁用，清旧Git/WCG路由与SSH代理，禁交互。无业务clone的身份更改、真实公屏/远端/有效凭据操作。临时目录已清除，真实输入/代码/日志保全；原程序本身没有这套强制隔离，因此不能把复现器属性冒称原程序安全定理。没有数学suite、阶段三图导入、外文/PDF/视觉或生产认证。

## 四份历史运行记录：全部字段实读，不能串错版本

本批完整读取23515字节的四份related JSON并核inventory SHA。它们均已Boss2 integrated，当前progress和两正式相关资源亦完整读完，快照/owner在comparison-manifest；本批不再claim/done或覆盖其原页。它们是作者历史执行记录，保其当时覆盖，不能用表面95/103/109计数套当前源码。

| 记录 | 历史真实记载 | 本批正确比较 |
| --- | --- | --- |
| incremental_chat_release，57cb…，3078B | base4c71…；95测试=22board+5entry+35checkpoint+2并发+15安全+16work，66.518秒；十clone/20消息/10保存 | 并发SHA b929…、安全1700…均不同本批113879…/7ae9…；不能继承为本批17 PASS。旧board同SHA只说明该组件身份，不升级整个suite |
| active_topic_routing_release，bc0…，16650B | 初次109项69.649秒后只改入口元数据，又21项work14.983秒；初/终源hash集、384/406链接、7项routing失败回归、peer24数学文件字节保留均分阶段记 | 整体109未在末版本重跑；旧并发e46f…/安全1549…与本批不同。旧当前题UM及旧tools/work实现不是本批根main/legacy，不把历史final称当前 |
| unrelated_machines_scope_release，8088…，1875B | checkpoint42和全suite103，注册/未知save、删除/旧主题阻断/peer草稿和十clone兼容 | checkpoint/test_work源hash与本批不同；是旧scope分离证据，非全数学/当前17精确认证 |
| message_routing_model，9d1…，1912B | 500 logical workers、249500定向对；各消息频率负载、竞争1/55/5050/125250尝试及reject计数，source hash和限制 | 是有限逻辑/条件对抗模型，非500实际Work或吞吐预测；本批未重跑其model源，也没把本次十clone视作扩容 |

active记录还把初/终源码hash、实际已转录但未独立存全stdout、后续入口修正、路由探针fake Board、source recovery与post-peer merge各自列明。本批保全部JSON字段原件，不补造历史原log或执行动作。它的路由探针明确pending/retry/discard保原save、直接board缺save解释shared、默认view公开跨save聚合；不能从旧“当前UM”文字覆盖本批CAG兼容与现六人焦点。

已全文比较Boss2《协作清洗与研究工作台设计》《协作并发与存档隔离三源有限证据》：二者已分开设计/工程/生产容量/数学，所保旧运行和未实现能力保持自身身份。本批新增的是四个主源完整代码合同和新SHA配对17x2实测，不追改它们的历史已读或执行范围。所有claims/proofs、clean收据和图关系仍须独立证据，软件测试不代替它们。
'''
p2=obj('协作路由测试的完整义务与版本证据','frontier-collaboration-tests-and-versioned-evidence','两协作测试完整17义务、新每ref17实测及旧95/103/109/500逻辑模型的SHA边界；不复done Boss2来源。',[x for x in src if x['path']!='work.py'],b2)
save(E/'formal-manifest.json',[{'path':p,'bytes':(S/p).stat().st_size,'sha256':sha(S/p)} for p in [p1,p2]])
save(E/'reading-scope.json',{'claim_capture':'/workspace/scratch/37f0f9248cfc/boss4-r3-next9ag-claim.json','claim_pushed_tip':'f6e45a9fec80c36de9276aa1d2e1da06e99f3163','claim_sync_tip':'fd6a2c1a06a73dd011b011c870f831ba0aca902a','tip_note':'both actual receipt values preserved; not asserted equal','primary_bytes':79188,'primary_full_read_lines':{'4a9d84f0b03bbbf6c01a':132,'086e17d599de8edb10a2':248,'d9b5b49ab665613450d6':522,'3c0404b7974eca538863':618},'root_full_read_reuse':'previous independent whole sources exact SHA, all18/21functions now semantically retained','new_test_read_ranges':{'4a9d84f0b03bbbf6c01a':[[1,132]],'086e17d599de8edb10a2':[[1,200],[201,248]]},'related_full_releases':4,'related_release_bytes':23515,'related_Boss2_resources_full_read':2,'eight_code_dependencies':'previous whole sources exact SHA reused','extra_sources_done':[],'unread_primary_or_truncated_ranges':[]})
receipts=[]
for x in src:
 root=x['path']=='work.py';receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':f'完整{x["size"]}字节/{len(text(x["id"]).splitlines())}行全文实际语义读取，inventory SHA复核。'+('两root此前独立全读精确复用，18/21函数/常量/全部CLI/异常独有内容逐项归位。' if root else '132/248行两测试全部fixture/导入/17断言/main独立实际读完，原件不改。'),'comparison_note':'与真实同ref root/board/checkpoint/fixtures、另一版本及现规则比较；四历史release全字段/两Boss2正式资源/已done ownership实际比对，旧SHA不同不继承PASS；先前root26/34实测精确复用不重跑，新17每ref准确记新增。','decision_note':'integrated为自足软件资源，保全部版本/副作用/输入/有限证据与未覆盖范围；旧R身份、分支/角色prompt不执行为当前指令，不把pushed/ack/hash/有限测试升级数学或生产认证，不复done相关Boss2源。','disposition':'integrated','targets':[p1,p2] if root else [p2]})
save(W/'semantic-receipts.json',receipts);save(W/'next-candidates.json',read(E/'next-candidate-snapshot.json'));(W/'relation-review.md').write_text('''# 关系范围\n\n两资源解释根实现/协作fixture和版本证据，关系是实现、来源与有限检查。无新数学derives/attacks，不造图连通或进入mapper。新四主源integrated；Boss2四release和两资料只比较不覆盖/复done。所有历史phase/actor/数学OPEN保持原时态，当前根规则优先。\n''')
save(E/'attempts-and-boundaries.json',{'claim':'verified unique pushed Boss4 receipt and four actual IDs before materializing primary; preserved differing push/sync tip values','exports':'root2 exact prior full-byte reuse; two primary tests and four related releases read-only clean show all exit0; source export processes yielded after metadata then actual exit0 polled','new_runs':'17 collaboration test methods per ref, once each; modules imported only prepare fixtures, no repeated old suites','reused_runs':'prior main26/legacy34 lifecycle exact SHA evidence, no rerun','historical_records':'four fully read Boss2-done sources; old SHA mismatch or conditional model, no inherited exact PASS','never_used':['shared Git writes/claim/done/checkpoint/spawn/mapper','real business start/identity/public-board/remote/credentials','production500 Work/throughput claims','math/PDF/browser suites'],'extra_sources_done':[]})
checks=[]
def check(n,v):
 checks.append({'check':n,'passed':bool(v)})
 if not v:raise AssertionError(n)
inv={x['id']:x for x in map(json.loads,(R/'cleanup/inventory.jsonl').read_text().splitlines())}
for x in src+deps+releases:
 p=S/x['saved_path'];check('exact identity '+x['id'],all(x[k]==inv[x['id']][k] for k in ['path','size','sha256','blob','sources']));check('exact bytes '+x['id'],p.stat().st_size==x['size'] and sha(p)==x['sha256'])
c=read(E/'actual-claim-receipt.json');check('actual claim subset',c['status']=='pushed' and c['actor']=='Boss4' and {x['id'] for x in src}<=set(c['ids']) and c['local_sync']['status']=='synced');check('all39 function roles',len(functions)==39 and len([x for x in functions if x['source_id']=='d9b5b49ab665613450d6'])==18);check('17 complete assertions',len(tests)==17 and len({x['name'] for x in tests})==17)
for v,root_id,count in [('main','d9b5b49ab665613450d6',26),('legacy','3c0404b7974eca538863',34)]:
 q=read(E/'runs'/f'{v}.json');log=(E/'runs'/f'{v}.stderr.txt').read_text();check('new17 suite '+v,q['returncode']==0 and 'Ran 17 tests' in log and log.rstrip().endswith('OK') and len(re.findall('^test_',log,re.M))==17);check('file-only real-code pairing '+v,q['environment_guards']['GIT_ALLOW_PROTOCOL']=='file' and not q['real_remote_or_effective_credentials'] and any(x['id']==root_id and x['sha256']==byid[root_id]['sha256'] for x in q['source_inputs']));prior=read(E/'context'/f'{v}-work.json');oldlog=(E/'context'/f'{v}-work.stderr.txt').read_text();check('prior lifecycle exact binding '+v,prior['returncode']==0 and f'Ran {count} tests' in oldlog and any(x['id']==root_id and x['sha256']==byid[root_id]['sha256'] for x in prior['source_inputs']))
for ident in [x['id'] for x in releases]:check('Boss2 prior ownership '+ident,read(E/'context'/f'existing-progress-{ident}.json')['owner']=='Boss2')
for p in [p1,p2]:
 t=(S/p).read_text();meta=t.split('---\n',2)[1];check('flat MATEK '+p,all(re.search('^'+k+':',meta,re.M) for k in ['id','kind','type_tag','title','status','summary','source_refs']));check('formal C0 '+p,not any(ord(c)<32 and c not in '\n\r\t' for c in t));check('formal trailing '+p,all(l==l.rstrip() for l in t.splitlines()))
check('four receipt identities',len(receipts)==4 and {x['id'] for x in receipts}=={x['id'] for x in src})
for x in receipts:check('complete semantic receipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note']) and all((S/p).is_file() for p in x['targets']))
result={'passed':True,'checks':len(checks),'scope':'exact identity/full-read scope/finite software evidence/ownership/receipts/format only; not production or mathematics','formal_forbidden_C0':0,'formal_trailing_whitespace':0,'details':checks};save(E/'self-check.json',result);save(W/'self-check.json',result)
(E/'README.md').write_text('''# 四主源根生命周期与协作测试\n\n79188B主源全部语义实读，两root522/618行此前完整独立读取按SHA复用，两测试132/248行完整新读。39函数/17断言全部保自足资料；八实际代码依赖完整旧读精确复用。\n\n新增每ref17协作实例PASS（34），原root26/34实例无疑复用不重跑。四历史release23515B全JSON与两Boss2已done资源全读，旧95/103/109和500逻辑模型不扩当前SHA/生产容量；相关源不复done。file-only新临时仓库/合成身份与ASKPASS，未触真实业务身份、公屏、远端、凭据或共享Git写，无数学状态升级。\n''');(W/'delivery.md').write_text('''# 四源交付\n\n两自足资料、四integrated收据、四原件/八真实代码依赖/旧证据与新有限日志。Root按exact manifest复制后实际pushed再done；本子任务不shared Git/claim/done/spawn。下一候选仅实际local progress快照，须Root全局Owner核。\n''')
print(json.dumps({'formal_files':2,'formal_bytes':sum((S/p).stat().st_size for p in [p1,p2]),'primary_bytes':79188,'receipts':4,'checks':len(checks),'passed':True},ensure_ascii=False))
