"""Write semantic resources after all five sources and real dependencies were read."""
from pathlib import Path
import ast
import difflib
import hashlib
import json
import re

E=Path(__file__).resolve().parent
S=E.parents[2]
R=S.parent.parent/'boss4-research'
F=S/'archives/weighted-congestion/state/资料'
W=S/'cleanup/workspaces/Boss4/r3-frontier-board-programs-next'
F.mkdir(parents=True,exist_ok=True)
W.mkdir(parents=True,exist_ok=True)
sources=json.loads((E/'source-manifest.json').read_text())
deps=json.loads((E/'dependency-manifest.json').read_text())
byid={x['id']:x for x in sources+deps}
def read(x):return (S/x['saved_path']).read_text()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def object_file(name,ident,summary,selected,body):
    path=F/(name+'--资料.md')
    meta={'id':'weighted-congestion/'+ident,'kind':'resource','type_tag':'资料','title':name,
          'status':'historical-software-audit-with-new-isolated-fixture-evidence','summary':summary}
    refs=list(dict.fromkeys('source:'+z['commit']+':'+z['path'] for x in selected for z in x['sources']))
    path.write_text('---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in meta.items())+
        'source_refs:\n'+''.join('  - '+json.dumps(x,ensure_ascii=False)+'\n' for x in refs)+
        '---\n\n# '+name+'\n\n'+body.strip()+'\n')
    return str(path.relative_to(S))

body1=r'''
本对象保存两个冻结board.py的完整消息协议、Git副作用和精确版本差别。legacy源673a94bf8c2a50db4be5为30226字节/644行，SHA650b504f1c483b068a3f651a3d07c07f7106bf7e11fde84f38a5db5a204ceafd；main源99da839bfd62db2365a0为30102字节/640行，SHA11dc1a9ca8f3d1dc789cece1ac11fe9a2589323c55f2ea490d4ccba2d3027831。前者只在legacy-cleanup 68fad804ec5946cb296f77dc5b336308a66abf12，后者只在main aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c；两件都已逐行独立全文读完，不把diff当成未读正文的替代。

完整源码在[逐源原件及SHA表](../../../../tools/evidence/frontier-board-programs/source-manifest.json)，精确[legacy→main差分](../../../../tools/evidence/frontier-board-programs/legacy-to-main.diff.json)另存。它们属于历史研究基础设施，不是当前操作入口或数学定理；本轮不调用真实公屏、找凭据或切换身份。

## 消息和状态的全部合同

持久状态为events有序列表与last_time；每条event恰含id、actor、kind、body、schema、seq、time。schema必须为精确int 3，seq必须为精确int且等于已有事件数加一；bool不充当整数。time为非负精确整数，但代码**不比较前一个时间**，last_time只是最后追加事件的时间，不保证时钟单调。

intent恰含id/actor/kind/body。id为32个小写十六进制字符；actor匹配首字母数字、之后字母数字或点/下划线/连字符，总长1至101。寻址用address另限1至64，用于save、to、mentions、收件箱/已读；这两个长度上限不同。kind仅为message、discussion、progress、help、objection、review_request、review、barrier、result九种标签。标签review/result本身不证明已经数学审查或获得结果。

body仅允许text、thread、reply_to、asset、save、to、mentions：text为非空白字符串；可选thread为非空单行且至多160字符；reply_to为合法消息ID；save和to为安全address，to不能等于发送者；mentions为无重复的address列表，私聊中的mentions不得超出两参与者。result必须带asset，其他kind也可带。validate_intent先用JSON序列化的token样式正则guard检查内容，再校验字段。正则识别限定GitHub-token形状，不是所有秘密、来源可信性或数学语义的判定器。

transition要求ID不与历史重复。reply_to必须已有，父子save必须相同（缺省save为shared）；若父消息私聊，子消息必须保持同一对参与者。公开父消息没有这一私聊参与者限制；thread也不必与父相同。成功时深拷贝状态和event再追加，失败不会改输入状态。它没有成员注册、权限角色、占用研究方向、数学claim/done、对象证明状态或目标模型的语义检查。

## 私聊、提及、已读和投影

无to的消息公开；有to时参与者是actor和to。visible只是筛选函数，原始Git事件和Board.read仍包含完整记录，同仓可读，**没有权限隔离**。attention对私聊只通知收件者；公开消息不通知自己，但提及自己或回复自己消息会进入attention。回复不自动继承thread/save，客户端须传正确save，否则transition拒绝跨存档回复。

seen/ack用git-common-dir下本地wcg缓存，按actor:save的SHA建立锁和游标文件。ack先读取公屏，验证事件存在、同save、可见且确实attention，再在flock下将旧集合与新ID求并，临时文件flush/fsync后os.replace。输出meaning明确是read receipt only; not mathematical adoption。它不发送接受消息、不改变远端正文或证明状态；换clone不自动继承这份本地游标。

render默认最近50条可见消息，显示序号、actor、kind、UTC、事件链接、thread/save/to/mentions/reply与冻结asset JSON，text原样保留含W ≠ w等Unicode，不解释TeX或证明。view支持thread、limit、save、actor、peer、inbox、unread；负limit拒绝，0全部，JSON默认不限、Markdown默认50。peer/inbox/unread需要actor，unread还需显式save；只传actor并不启用个人视图。可见性选择中的actor仅在inbox或peer时生效，unread本身不是attention过滤器；想看个人未读须按真实命令组合筛选。

view JSON沿用完整state的last_time但events可能筛选、限长、不连续，故是导出投影，不能当作完整规范日志重新decode；回复父消息也可能不在投影里。BOARD.md是派生展示，不代替events完整记录。

## 冻结文件：实际核的是哪些命题

asset恰为branch、commit、path、sha256四个字符串。commit为完整40或64位小写十六进制；sha256为64位。PurePosixPath拒绝绝对路径、..、空路径、冒号、NUL/CR/LF；后续还须真实普通文件。check_asset在临时仓库fetch命名远端branch，检查commit是FETCH_HEAD祖先、ls-tree模式为100644或100755 blob、读取commit:path全部字节并核SHA256。分支名另经Git check-ref-format。不是只检查描述符文本。

这只证明该命名分支可达某提交、某普通文件的字节绑定，不验证数学正文、文献归属、claim真实性、独立审查或算法复杂度。两个版本都允许合法非main分支；main渲染文案说“研究资产统一保存在main”，**程序的check_asset未强制这一策略**。原测试还确实发布过work分支资产。已成功记录的同ID同intent会直接重放已有事件，不再要求资产分支仍存在；这是发送幂等恢复，不是重新证明现时资产可达。

## 实际Git调用与故障恢复

Board初始化查真实repo根、origin URL、分支ref格式、git-common-dir；拒绝URL内token样式或http(s) userinfo，retries精确int且1至50。默认公屏分支wcg/board。缓存目录在git-common-dir/wcg，outbox按schema:branch哈希命名，临时Git目录亦在此。即使view/pending也先构造Board并可能创建本地缓存，不能把所有命令概括为零写入。

git包装移除GIT_DIR/WORK_TREE/COMMON_DIR/INDEX_FILE/OBJECT_DIRECTORY等11个路由变量，禁交互提示，45秒超时；错误仅按token样式脱敏并截前1000字符。setup为临时repo执行init、配置固定署名、添加同origin；checkout只在临时repo浅fetch公屏分支并detach。普通读/发布不checkout调用者工作分支、不改调用者index/FETCH_HEAD，但本地缓存/游标/outbox有写入。源没有隔离真实网络的强制file协议限制；本批复现器另加了该限制。

publish先验证intent，再以临时文件flush/fsync+硬链接排他建立固定ID的pending；已有pending内容不同时Conflict。每次重试新临时repo读取最新远端：同ID同intent已存在就删除pending并返回，异内容Conflict；否则核asset、分配seq/time、transition、写事件和BOARD.md、普通commit/push，随后重新读取远端确认ID存在才清pending。网络/一般BoardError最多重试retries次并指数等待加确定性jitter（上限短暂停），Conflict/ValidationError不自动重试。失败保留原ID和intent，retry复用，discard仅删本地pending；公开pending可在未指定actor时操作，私聊pending要求原发送者actor。此是自声明actor的逻辑约束，不是用户认证。

init用ls-remote：已有分支只read并保留消息；只有退出码2才创建空schema3公屏，再普通push并read确认，不能从初始化返回词推断某消息已发表。migrate要求完整expected_head：若已是当前有效schema，返回already-current并保留事件，即使head不同；只有非当前schema才要求head精确匹配已检查提交，删除该公屏目录并写空schema3，再普通快进push。无强推；lost-response或并发迁移后read有效公屏可以确认别人的迁移结果。它不会把旧不可解记录语义迁移成新事件，故“迁移”包含明确删除旧目录这一实质副作用。

decode逐个按文件名排序的events/*.json读取，校验全事件和精确seq_ID文件名，拒绝经过的目录/记录符号链接。meta必须恰为整数schema3。然而events目录不存在时glob为空，仍返回空state；非JSON附加文件也不参与读取。该行为不能被描述成全仓文件完整性或无遗漏认证。

## 两版本的独有差别

| 位置 | legacy 673a… | main 99da… | 不应混同的范围 |
| --- | --- | --- | --- |
| render说明 | 启动回执绑定的文件分支；branch/commit/SHA | 资产统一main；commit/SHA | 是文案/旧控制差别；asset实际仍含branch，两版均允许非main |
| README生成 | 独立write_readme；根work.py、各自文件分支、稳定发布身份 | 内联write_empty；main的tools/work.py、提示词角色号 | 初始化/迁移README字节有差别，旧命令不作本轮指令 |
| 每次publish | 同时重写README和BOARD | 只重写BOARD | main发布不会顺带刷新旧README；不能把两源码当全文件duplicate |

其余diff没有改消息状态机、认证入口、asset判定或重试核心。源码/运行结果逐版本保留。当前根规则则是rebuild/research-v2、明确Boss编号、公屏另有本轮分支、阶段二实读和阶段三解释关系分开；本五源不覆盖这些规则，也不替本轮clean receipts或Root串行checkpoint。

## 已实际验证和用途

在真实依赖逐字节物化的全新隔离临时仓库，每版本原22项board测试及5项entry测试各运行一次，均PASS；新增9个纯本地边界例每版本也通过。详见[认证与测试资源](公屏认证入口与隔离测试的证据范围--资料.md)。这些是**新增有限软件证据**，没有操作实际公屏、有效凭据或真实远端，不认证生产服务器、所有并发/恶意历史或数学结果。

本资源可复用来理解历史消息、区分“发送确认/字节冻结/已读/数学采纳/完成归档”，及审查旧看板何时会写本地或远端。没有新增数学命题、阶段三图导入或强制连通关系。
'''
p1=object_file('公屏消息状态机与冻结资产的版本合同','frontier-board-state-and-version-contract',
    '两board版本全部读取，完整消息/资产/重试/迁移合同；文案与实际分支策略、筛选与认证、发送与数学状态分开。',sources[:2],body1)

claims={
'test_direct_send_and_async_reply_without_registration':'无注册异步发送/回复，四事件与thread/limit筛选；回复链接保持父身份。',
'test_same_topic_concurrent_independent_clones_both_succeed':'两个独立clone同步首次push，同题两不同ID都成功且seq为1/2。',
'test_same_message_race_and_cross_clone_replay_are_idempotent':'同intent并发和跨clone重放只一事件；同ID改正文Conflict。',
'test_lost_success_response_recovers_without_duplicate':'实际本地push后注入丢响应，恢复同ID、无重复、清pending。',
'test_failed_network_keeps_local_intent_and_retry_cli':'load注入Offline保原intent/ID；其他消息独立；CLI retry及重放相同。',
'test_local_discard_changes_no_remote_message':'失败pending可本地discard，不改变远端事件。',
'test_remote_receipt_recovers_after_asset_branch_disappears':'真实本地push后丢响应，再删work资产分支；同ID远端回执仍恢复一条。',
'test_frozen_asset_hash_commit_path_and_regular_file':'真实asset核可达/hash；错hash/提交、越界/目录/符号链接/非法类型/path点拒绝。',
'test_asset_network_failure_does_not_block_other_messages':'asset检查注入Offline，只阻该intent，其余消息和后续恢复可行。',
'test_dirty_checkout_fetch_head_and_staged_index_are_preserved':'dirty文件、staged index、HEAD/FETCH_HEAD字节保持，含注入Git路由变量。',
'test_cli_text_file_stable_id_and_json_export':'两行Unicode文本精确保留、固定ID幂等/JSON导出；互斥text参数及负limit拒绝。',
'test_invalid_fields_and_secret_fail_before_network_or_disk':'坏actor/text/thread/reply形状/secret样式/asset/kind/字段在load或pending前失败，retries0/bool/51拒绝。',
'test_unknown_reply_is_rejected_without_retry':'合法形状但未知父ID拒绝、不重试、无事件。',
'test_outbox_disappearing_during_confirmation_is_normal':'已发表同intent的pending读瞬间消失，恢复依然幂等。',
'test_migration_deletes_inspected_noncurrent_files_by_fast_forward':'schema1含不可解析旧记录需显式迁移；后继commit父为旧head、旧文件删除、schema3空。',
'test_migration_fences_new_noncurrent_changes':'检查后旧schema又变，旧expected_head触发Conflict，不覆盖新head。',
'test_migration_retains_current_messages_and_is_idempotent':'已current时即使expected为较旧head，也保已有消息并already-current，含CLI。',
'test_migration_lost_response_confirms_remote':'迁移本地实际push后丢响应，再读确认schema3空。',
'test_concurrent_migration_and_new_chat_message_are_preserved':'并发另一迁移并立即加消息，原迁移无force且读回保消息。',
'test_metadata_requires_integer_current_schema':'schema精确int；float/bool/额外字段/list/None拒绝。',
'test_initialize_current_board_does_not_clear_messages':'已有schema3初始化返回already initialized且原消息保留。',
'test_transition_failure_preserves_input_and_case_sensitive_symbols':'坏seq/schema/time及bool不改原state；W ≠ w大小写原样保留，不是数学证明。',
'test_explicit_then_remembered_file_and_dirty_work':'合成外部token文件含空格，记路径后复用；不泄漏内容/写入config，dirty文件和HEAD保留；手动ASKPASS只回合成字符串。',
'test_repo_argument_from_outside_and_native_auth':'从repo外显式--repo可用；无token选项时不写wcg.tokenFile。本地文件远端不要求真实认证。',
'test_inside_missing_or_invalid_credentials_fail_before_send':'仓库内文件、缺文件或不匹配字符串返回2，未发送/未记路径。',
'test_stale_remembered_file_is_an_explicit_failure':'已记路径被删，view明确失败，不静默换凭据。',
'test_help_and_board_error_exit_codes_are_preserved':'仓库外help为0且含say；空正文发送为2且无事件。',
}
test_inventory=[]
for ident in ['207fa0dc8920b57c0653','35511e58709fa3bd7815']:
    for node in ast.walk(ast.parse(read(byid[ident]))):
        if isinstance(node,ast.FunctionDef) and node.name.startswith('test_'):
            assert node.name in claims
            test_inventory.append({'source_id':ident,'test':node.name,'start_line':node.lineno,'end_line':node.end_lineno,'actual_assertion_scope':claims[node.name]})
save(E/'test-assertion-inventory.json',test_inventory)
body2=r'''
本对象完整整理board_entry.py源8bf0d5ec0cfafef1274c（1931字节/46行）、test_board.py源207fa0dc8920b57c0653（20420字节/401行）和test_board_entry.py源35511e58709fa3bd7815（5356字节/104行）。三件在两个冻结refs均同字节，完整SHA与原路径在[五源清单](../../../../tools/evidence/frontier-board-programs/source-manifest.json)。全部原码、注释、fixture、assertion和main均已实际读完。

它们不含独立数学证明。Unicode示例W ≠ w只是消息字节保留测试；kind=result、read回执、文件hash或27项PASS均不能提升数学命题状态。双board核心与版本差异详见[消息状态机](公屏消息状态机与冻结资产的版本合同--资料.md)。

## 入口真实路由与认证边界

board_entry用add_help=False/allow_abbrev=False仅解析--repo（默认.）与--token-file，其余参数原序转给相邻board.py。若剩余有--help或-h，直接运行board.py帮助，不初始化repo或凭据。正常路径先通过checkpoint.value/git查repo根，再按显式token-file、WCG_CHECKPOINT_TOKEN_FILE、repo本地wcg.tokenFile的优先级选**文件路径**。没有选到路径时保留原生Git认证能力，不会替用户发现或生成token。

若选到路径，resolve后拒绝位于repo内，再调用checkpoint.token静默验证。显式--token-file会把已通过验证的路径写进该repo的本地config；这是真实写入，不是仅只读查看。入口给子进程GIT_ASKPASS=相邻checkpoint.py、WCG_CHECKPOINT_TOKEN_FILE=路径及WCG_CHECKPOINT_ASKPASS=1，移除11个Git路由变量并禁终端交互，然后返回board.py退出码。Stop/OSError/ValueError被格式化、按checkpoint的SECRET正则脱敏并退出2。旧错误处理/外部文件要求是本源操作设计，不改变本轮不找凭据、不真实发消息的分工。

checkpoint.token实际从文件字节提取github_pat_或ghp_形状、至少12个后续字符的匹配，取set，要求**恰一个不同的匹配串**；它并不要求整个文件等于一个token，重复相同串仍只算一个。这个形状验证没有向服务端认证。ASKPASS分支以环境标记及单一参数启用：Username提示回固定x-access-token，Password提示读取所选文件并输出匹配串。只有合成fixture调用了这一支；没有读取本轮真实凭据。

## 真实依赖及版本配对

入口依赖完整checkpoint模块，entry测试还通过board.sh启动，不能把缺依赖当可运行原测试。已实际取到并核inventory SHA/全文读完三件相关依赖，只作输入，不额外done其ID：

| 依赖 | 原件字节/行数与SHA | 本批实际用途 |
| --- | --- | --- |
| board.sh，988a0574030a7fded769 | 230/5；19b639aefe3d2417a170915fff3ecc9a66d0c0e1bb8a36b950fd938e1c1227f0；双ref | bash set-euo包装，按自身目录exec python3 board_entry.py；真实配入两fixture |
| legacy checkpoint.py，f4ad07192854bfc106ad | 22196/397；1e9b5da42f49658aac50d301831de8e77f5e55d6f992488296572dc4496e8d35 | 配legacy board；全模块实读，但仅helper/ASKPASS被entry测试使用 |
| main checkpoint.py，db6af3d64d99cc147969 | 20508/377；7c36a36e0cb814250f542f0ac9fd7ea31c66406b471364d7ee7e014c6532a24e | 配main board；同样没有运行save/locked_save |

两个checkpoint版本的token/git/value/ROUTING/Stop/SECRET和ASKPASS共同接口满足entry依赖，但完整保存策略不同。legacy可按wcg.branch绑定文件分支、默认main，排除配置公屏及wcg/board-*，额外repository-cleanup默认范围，describe_assets带实际branch，并有显式create-branch路径；main版本只允许main、描述符固定main，无create-branch。二者都做scope/history审计、普通push后fetch祖先确认和local-only/pushed回执，代码完整保留在[依赖清单](../../../../tools/evidence/frontier-board-programs/dependency-manifest.json)。本批**没有运行checkpoint保存路径**，不把入口测试结果扩展到这些不同分支控制，更不拿旧默认范围作当前规则。

## 原fixture输入和全部测试义务

board测试在fresh fixture目录建本地bare remote及work clone，配置合成作者；初始asset.md、folder/child.md和link.md构成普通文件/目录/符号链接对照，main commit真实本地push后初始化公屏。时间初值1000；并发用独立clone、首次push屏障；网络故障/lost-response由补丁显式注入。entry测试有同样隔离bare remote、baseline文件，以及源码字面合成ghp_+fixture重复串，外部凭据文件名含空格；没有有效凭据，文件协议远端不验证GitHub认证。fixture的全部细节及assertion保留于原测试，不由本轮伪造外部服务。

下表是完整22+5项逐项assertion语义；名称/行段另有机器可定位的[测试义务表](../../../../tools/evidence/frontier-board-programs/test-assertion-inventory.json)。
'''
body2+='\n| 原测试 | 实际断言范围 |\n| --- | --- |\n'+''.join('| `'+x['test']+'` | '+x['actual_assertion_scope']+' |\n' for x in test_inventory)
body2+=r'''

## 本批新增运行：有限证据，不追溯改旧运行状态

在已交付evidence/资料中搜索两board SHA及test名，没有找到同SHA原成功run，只有旧路径索引。因此本次明确记为**新增**，没有声称重现任何历史公屏验证提交。先完成全部源码/测试/依赖读取，再由[隔离复现器](../../../../tools/evidence/frontier-board-programs/run_isolated.py)各创建全新临时repo，按同ref配对原字节/执行位，运行原unittest discover，无源修改。

| 配对 | 原测试结果 | 原测试日志时间 | 新纯边界例 |
| --- | --- | --- | --- |
| legacy board650b… + checkpoint1e9b… | 27/27 PASS，exit0 | 10.338秒 | 9例PASS |
| main board11dc… + checkpoint7c36… | 27/27 PASS，exit0 | 11.536秒 | 9例PASS |

总计54个原测试运行实例及18个新纯例；不是54种不同数学命题。两组stdout/stderr、版本、精确输入SHA、命令和环境限制在[runs](../../../../tools/evidence/frontier-board-programs/runs/summary.json)。解释器/Git版本以各JSON实际值为准。临时repo完成后清除，原件及测试代码/输入SHA/日志留存，可接续重建。

Git只允许file协议，系统/全局配置均禁用，清除Git路由、旧WCG身份/认证变量与SSH代理，禁终端提示；所有init/clone/push/迁移均限新临时路径的本地假远端。测试没有共享repo写、真实公屏写、身份重置、有效凭据读取或网络认证。原程序本身并不自带这些隔离限制，不能把复现器的保护性质归给原实现。

## 新增边界例与未覆盖范围

[纯本地探针](../../../../tools/evidence/frontier-board-programs/probe_boundaries.py)导入原board但将Git函数替换为遇调用即失败，逐版本实际验证九例，结果在[pure-boundaries.json](../../../../tools/evidence/frontier-board-programs/runs/pure-boundaries.json)：

1. 两事件时间10→1合法且last_time=1：只要求非负，不保证单调。
2. actor长度101能通过intent，address同值拒绝：消息发送与寻址上限不同。
3. 私聊raw state仍含事件，匿名render不显示、参与者render显示：投影不等于权限隔离。
4. 私聊回复换参与者拒绝且输入不变。
5. 回复跨save拒绝且输入不变。
6. 有schema3 meta但events目录缺失，decode返回空事件：不是记录目录完整性认证。
7. ack实际仅写临时本地游标，seen包含ID且meaning明确非数学采纳。
8. 合法non-main-fixture资产shape接受：main只是版本文案/上层政策，shape不强制main。
9. metadata精确整数3接受，bool True拒绝。

这是有限具体例，不是对任意损坏存储、所有并发交错、恶意actor/远端、跨平台文件系统或所有凭据形式的完备证明。原27项没有专门覆盖完整DM/mentions/inbox/unread组合；新增例也没有穷尽CLI组合、真实权限或真实认证。没有外部服务认证PASS、浏览器视觉PASS、实际看板部署、消息迁移、数学suite、数学Claim升级或阶段三关系导入。

本资料可作为历史入口调用审查、隔离测试接续以及“测试通过究竟证明什么”的准确输入。与前批《运行手册与旧角色兼容入口的迁移范围》比较时，只复用其冻结文档/当前规则区别；其此前仅文档实读的状态保留，不追溯声称它当时已拿到本次源码或运行。相关比较快照明确为前批external交付稿，当时repo目标路径尚未物化，故不虚报新发表。
'''
p2=object_file('公屏认证入口与隔离测试的证据范围','frontier-board-entry-and-isolated-test-scope',
    '入口/22+5原测试全文与真实依赖双版本；新增每版本27项隔离PASS和9边界例，不扩展到真实认证/生产/数学。',sources[2:],body2)

save(E/'formal-manifest.json',[{'path':p,'bytes':(S/p).stat().st_size,'sha256':sha(S/p)} for p in [p1,p2]])
scope={sources[0]['id']:{'lines':644,'read_ranges':[[1,260],[261,450],[451,644]],'ref':'legacy only'},
       sources[1]['id']:{'lines':640,'read_ranges':[[1,255],[256,450],[451,640]],'ref':'main only'},
       sources[2]['id']:{'lines':46,'read_ranges':[[1,46]],'ref':'both'},
       sources[3]['id']:{'lines':401,'read_ranges':[[1,220],[221,401]],'ref':'both'},
       sources[4]['id']:{'lines':104,'read_ranges':[[1,104]],'ref':'both'}}
save(E/'reading-scope.json',{'actual_claim_pushed_synced':'47a1cac463702452cf7b62b023b826872a2d278b',
 'primary_actual_full_reads':scope,'primary_bytes':sum(x['size'] for x in sources),
 'related_full_reads':[{'id':x['id'],'lines':len(read(x).splitlines()),'bytes':x['size']} for x in deps],
 'comparison_current_rules_full_read':True,'primary_truncated_or_unread_ranges':[],
 'full_related_formal_read':'prior external role-migration resource, precise snapshot and status in comparison-manifest',
 'extra_source_done':[]})
notes={
sources[0]['id']:('legacy全部644行实际独立读完，含全部CLI和异常路径；不是只读diff。','与main完整640行逐段及精确diff、原22+5测试和同ref checkpoint依赖比较；legacy每次publish刷新README、绑定文件分支文案独有。'),
sources[1]['id']:('main全部640行实际独立读完，含全部CLI和异常路径；不是从legacy自动勾读。','与legacy完整644行及diff比较；main内联README且publish不刷新，main文案不等于asset分支实际强制。'),
sources[2]['id']:('全部46行、参数路由、帮助短路、外部文件优先级/本地配置写入/ASKPASS/退出码实际读完。','与两完整checkpoint依赖、board.sh、5项真实entry tests及两version运行比较；只核helper及合成fixture，不宣称真实认证。'),
sources[3]['id']:('全部401行、fixture/并发/故障补丁/22项assertion/main实际读完。','与两个board全部代码、实际22+5各版本隔离run及9例边界比较；未把原测试计数作数学或完整CLI覆盖。'),
sources[4]['id']:('全部104行、ROOT/ENTRY依赖、合成凭据fixture、5项assertion/main实际读完。','与entry/board.sh/同ref checkpoint完整依赖及两version隔离run比较；手动ASKPASS仅合成字符串，本地file远端不认证GitHub。'),
}
receipts=[]
for x in sources:
    first=x['id'] in [sources[0]['id'],sources[1]['id']]
    n,c=notes[x['id']]
    receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,
      'read_note':n+f'完整{x["size"]}字节与inventory SHA吻合，所有实际读取范围及版本原件独立保全。',
      'comparison_note':c+' 并核当前根规则/对象合同与前批文档；旧角色/操作不覆盖当前Boss4和清洗任务。',
      'decision_note':'integrated为自足软件研究资料，保全部独有语义、实际副作用/缺口、原件代码/真实输入及新增有限软件证据；没有数学真值升级、真实公屏操作或额外done引用依赖。',
      'disposition':'integrated','targets':[p1,p2] if first else [p2]})
save(W/'semantic-receipts.json',receipts)
save(W/'next-candidates.json',json.loads((E/'next-candidate-snapshot.json').read_text()))
(W/'relation-review.md').write_text('''# 研究资源的关系审查\n\n两份资料共同保消息状态机、字节资产、入口认证与有限软件证据。它们能解释历史文档如何调用、发送确认与数学采纳为什么不同，但没有新的数学derives/attacks，不认证当前六人CAG或旧UM/WC结果。不进入mapper、不强造图连通。两个board版本只有明确三处diff而非全文件duplicate，五源各保原件、ID和完整语义收据。\n''')
save(E/'attempts-and-boundaries.json',{'clean_show':'five primary successful exact SHA exports after actual claim; one related board.sh export; main primary process yielded after output then exited0, no failure/retry','previous_same_SHA_run_search':'searched delivered evidence/resources for both board SHA and test names; only old path-index, no successful exact run found','new_runs':'one full original 27-test suite per ref pairing plus one 9-case pure probe per board, original bytes unmodified','allowed_operations':'read-only clean show; fresh temporary file-only Git fixtures and local pure examples','never_used':['shared Git writes','claim/done/spawn/mapper','real public-board send/migrate/init','real remote/authentication','credential discovery or effective credentials','checkpoint.save/locked_save','PDF/browser/visual/math suites'],'related_sources_done':[]})

checks=[]
def check(n,ok):
    checks.append({'check':n,'passed':bool(ok)})
    if not ok:raise AssertionError(n)
inv={x['id']:x for x in map(json.loads,(R/'cleanup/inventory.jsonl').read_text().splitlines())}
for x in sources+deps:
    p=S/x['saved_path'];check('exact inventory identity '+x['id'],all(x[k]==inv[x['id']][k] for k in ['path','size','blob','sha256','sources']));check('exact frozen file '+x['id'],p.stat().st_size==x['size'] and sha(p)==x['sha256']);check('full read line coverage '+x['id'],len(read(x).splitlines())== (scope[x['id']]['lines'] if x['id'] in scope else {'988a0574030a7fded769':5,'f4ad07192854bfc106ad':397,'db6af3d64d99cc147969':377}[x['id']]))
for x in sources:
    spans=scope[x['id']]['read_ranges'];check('continuous actual full-read ranges '+x['id'],spans[0][0]==1 and spans[-1][1]==scope[x['id']]['lines'] and all(a[1]+1==b[0] for a,b in zip(spans,spans[1:])))
old=read(sources[0]);new=read(sources[1]);patch=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='legacy/board.py',tofile='main/board.py'))
check('exact recorded dual-version diff',patch==json.loads((E/'legacy-to-main.diff.json').read_text())['unified_diff']);check('exact three diff hunks',sum(l.startswith('@@ ') for l in patch.splitlines())==3)
check('all 27 test assertions accounted',len(test_inventory)==27 and len({x['test'] for x in test_inventory})==27)
for v in ['legacy','main']:
    q=json.loads((E/'runs'/f'{v}.json').read_text());log=(E/'runs'/f'{v}.stderr.txt').read_text();check('new isolated original suite '+v,q['returncode']==0 and 'Ran 27 tests' in log and log.rstrip().endswith('OK'));check('local-file-only protocol '+v,q['environment_guards']['GIT_ALLOW_PROTOCOL']=='file' and not q['real_remote_network_credentials_used'])
pure=json.loads((E/'runs/pure-boundaries.json').read_text());check('18 actual pure finite cases',len(pure)==2 and all(len(x['cases'])==9 and x['git_network_calls']==0 for x in pure))
for p in [p1,p2]:
    text=(S/p).read_text();meta=text.split('---\n',2)[1];check('flat MATEK '+p,all(re.search('^'+k+':',meta,re.M) for k in ['id','kind','type_tag','title','status','summary','source_refs']));check('formal C0 '+p,not any(ord(c)<32 and c not in '\n\r\t' for c in text));check('formal trailing whitespace '+p,all(l==l.rstrip() for l in text.splitlines()))
check('exact five receipts',len(receipts)==5 and {x['id'] for x in receipts}=={x['id'] for x in sources})
for x in receipts:check('semantic receipt complete '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note']) and all((S/p).is_file() for p in x['targets']))
result={'passed':True,'checks':len(checks),'scope':'exact bytes/read scope/versions/test evidence/receipts/format only; not mathematics or production certification','formal_forbidden_C0':0,'formal_trailing_whitespace':0,'details':checks}
save(E/'self-check.json',result);save(W/'self-check.json',result)
(E/'README.md').write_text('''# 五源看板程序证据\n\n两个board.py、entry、两tests均完整实读，原件88035B精确绑定inventory。相关board.sh和checkpoint.py双版本亦完整实读/核SHA，未额外done。两自足资料保全部状态机/版本/认证/测试义务。\n\n新增隔离原27-test suite每版本一次均PASS（54运行实例），新增9个纯边界例每版PASS（18实例）。file协议/全新临时Git仓库/合成凭据；未动真实公屏、有效凭据或共享Git。原代码不修。完整输入SHA、依赖版本、命令、日志、边界和未覆盖范围均在本目录；不据计数认证数学。\n''')
(W/'delivery.md').write_text('''# 五源交付\n\n五原件逐行全读、双版本精确比较，两份自足资源、五条integrated收据。原件不改；54原测试实例和18纯边界实例是本批新增有限软件证据，不是历史服务器/认证/数学PASS。Root按精确manifest复制、实际checkpoint pushed后done；本子任务没有操作真实公屏/凭据或共享Git。下一候选仅本地progress快照，须Root核全局owner后再认领。\n''')
print(json.dumps({'formal_files':2,'formal_bytes':sum((S/p).stat().st_size for p in [p1,p2]),'primary_bytes':sum(x['size'] for x in sources),'receipts':len(receipts),'checks':len(checks),'passed':True},ensure_ascii=False))
