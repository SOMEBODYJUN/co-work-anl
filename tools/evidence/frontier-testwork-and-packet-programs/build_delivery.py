"""Semantic curation from complete primary reads, exact dependencies and finite runs."""
from pathlib import Path
import ast,hashlib,json,re
E=Path(__file__).resolve().parent;S=E.parents[2];R=S.parent.parent/'boss4-research';F=S/'archives/weighted-congestion/state/资料';W=S/'cleanup/workspaces/Boss4/r3-frontier-testwork-and-packet-programs-next';F.mkdir(parents=True,exist_ok=True);W.mkdir(parents=True,exist_ok=True)
def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
src=read(E/'source-manifest.json');deps=read(E/'code-dependency-manifest.json');data=read(E/'data-dependency-manifest.json');byid={x['id']:x for x in src+deps+data}
def text(i):return (S/byid[i]['saved_path']).read_text()
def obj(name,ident,summary,selected,body):
 p=F/(name+'--资料.md');meta={'id':'weighted-congestion/'+ident,'kind':'resource','type_tag':'资料','title':name,'status':'historical-software-completely-read-finite-versioned-evidence','summary':summary};refs=list(dict.fromkeys('source:'+z['commit']+':'+z['path'] for x in selected for z in x['sources']));p.write_text('---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in meta.items())+'source_refs:\n'+''.join('  - '+json.dumps(x,ensure_ascii=False)+'\n' for x in refs)+'---\n\n# '+name+'\n\n'+body.strip()+'\n');return str(p.relative_to(S))
common_descriptions=[
'start默认0不自动带公屏历史，显式3/1/0按需投影，完整read仍有4消息。','负board-limit在恢复目录前拒绝。','合成对话自动R-UUID稳定，不产生旧wcg/work分支；这不是当前Boss身份规则。','旧wcg/work提交祖先、index、未暂存/未跟踪内容、peer和本地recovery ref在迁移main时保留。','缺repo恢复、001身份/外部文件路径记忆、重复相同身份、拒绝换002，敏感合成串不入config/输出。','已有clone的staged/unstaged/untracked bytes在start保留。','缺/坏/多个匹配/仓库内/过期凭据文件早失败，不替换原路径或改发。','sync保分层dirty/untracked内容并取peer，不留自己的临时stash。','提交冲突abort且HEAD/dirty/index/untracked保留，无MERGE_HEAD残留。','恢复未提交内容冲突时保完整stash和双方内容，重试明确因unmerged停止。','用户原stash不被本次sync清掉。','两个clone同题无注册发送，actor/事件顺序明确、无members/ideas。','checkpoint实际文件SHA/远端commit、result引用及重放保存，文本“证书”不证明数学。','新CAG存档默认范围取本题/本人workspace，旧WC/peer草稿留本地。','既有shared绑定不改，保持旧scope；拒绝强改CAG。','未知save不自动继承已注册题目入口。','上传非可执行root恢复空clone并建当前workspace；legacy显式--branch main，main版无该额外参数。','根/checkpoint默认save及RESEARCH_ENTRIES常量一致，所列路径只检查is_file，不验证文档数学。','boss/cleaner/editor按各自clone稳定绑定/精确prompt路径，拒绝角色切换。','UM绑定保持UM入口和scope，CAG草稿留本地，拒绝换save。','旧tools/work.py实际转交根实现可读取同fixture公屏。','缺repo/非空目标给明确错误并保keep文件。','sync/checkpoint共用同clone writer锁。','继承Git路由不改外部诱饵index。','上传带空格且不可执行root通过临时可执行ASKPASS回合成字符串；Git credential fill不作网络认证。','pending/retry/discard保持原ID，未知父回帖留pending，重试仍拒绝，discard不删已有远端消息。']
main_nodes=[n for n in ast.walk(ast.parse(text('0267e9382e7d95b35a5e'))) if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')];legacy_nodes=[n for n in ast.walk(ast.parse(text('de53a0261145104205aa'))) if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')];assert len(main_nodes)==26 and len(legacy_nodes)==34
legacy_extra=[
'新项目默认长期cleanup分支/专用board/repository-cleanup/cleaner；另研究save可共用分支/board，不额外建远端ref。','同一下载bootstrap在本地假Git远端两次更新根程序后各handoff到first/updated，上传文件字节不变、actor稳定。','绑定cleanup两个clone的保存/asset/peer同步留main不动，main另前进也不混入cleanup。','新旧board分离，各init不清消息。','拒绝重绑文件/board路线，错分支sync/checkpoint/workspace失败且未完成字节保留。','首次发布必须显式create，未授权时无新ref，授权后实际branch描述符且main不动。','首次发布同样审计所有未发布祖先，scope外旧commit不能搭便车。','visit默认绑定文件分支，可显式只读main同号workspace，不切换clone当前分支。']
scopes={n.name:d for n,d in zip(main_nodes,common_descriptions)};scopes.update({n.name:d for n,d in zip(legacy_nodes[:8],legacy_extra)});inventory=[]
for ident,nodes in [('0267e9382e7d95b35a5e',main_nodes),('de53a0261145104205aa',legacy_nodes)]:
 for n in nodes:inventory.append({'source_id':ident,'name':n.name,'start_line':n.lineno,'end_line':n.end_lineno,'actual_assertion_scope':scopes[n.name]})
save(E/'work-test-assertion-inventory.json',inventory)
prior45=read(E/'context/test-assertion-inventory.json')
b1=r'''
本对象完整整理三个测试源/一个shell源的独有软件义务，不用测试数量或旧角色名当数学证明。主源共：test_checkpoint.py源2f4fa59cd9903d4c32e9（35108字节/649行）、main test_work.py源0267e9382e7d95b35a5e（33040/580）、legacy test_work.py源de53a0261145104205aa（45241/777）、work.sh源6a406a34c340855b3f7f（85/3）。完整source commits/SHA/执行位及原件在[逐源表](../../../../tools/evidence/frontier-testwork-and-packet-programs/source-manifest.json)。main/legacy两test_work逐段独立完整实读，全部fixture/断言/入口均读；checkpoint的完整阅读和两ref45项成功run从前批精确SHA复用，不再运行。

## 两套真实程序及输入不同

main测试仅在aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c，legacy仅在68fad804ec5946cb296f77dc5b336308a66abf12。两者共同26个test名，legacy另有8个；不能把同名方法或旧“24通过”记录套成同一个程序版本。[精确diff](../../../../tools/evidence/frontier-testwork-and-packet-programs/work-test-version.diff.json)与[全部60个实例的行号/断言义务](../../../../tools/evidence/frontier-testwork-and-packet-programs/work-test-assertion-inventory.json)保原边界。

共同fixture在新临时root下建bare文件remote、publisher和带空格的new conversation目录，将真实同ref根work.py、tools/work.py wrapper、board.py、checkpoint.py复制进seed，写baseline note/outside，main commit/push并初始化假公屏。合成token由源码ghp_+fixture重复串构造，外部文件名含空格；没有有效凭据。调用始终用sys.executable和本地remote。源clean_env仅移除指定Git路由/ASKPASS变量；本批复现器另强制file协议和禁全局/系统配置，不将这些额外保护冒称原程序自带。

legacy work()在目标不存在、start无显式branch、且不是project_defaults测试时自动加入--branch main，故26兼容测试里“仍main/CAG”不代表legacy默认新项目也是main/CAG。其两个project-default/bootstrap测试才覆盖长期cleanup默认及同步后handoff。上传独立程序的兼容测试亦明确--branch main。main版不含这个插入层，其默认就是main/CAG。这是两个真实控制版本，不是两个数学模型或当前身份要求。

真实代码依赖逐件完整实读过并以SHA复用：根work.py main26199/legacy31695，board.py main30102/legacy30226，checkpoint.py main20508/legacy22196，统一534B wrapper；清单在[代码依赖](../../../../tools/evidence/frontier-testwork-and-packet-programs/code-dependency-manifest.json)。main根主程序支持main/CAG及旧分支迁移；legacy扩展文件/board绑定、清理阶段和首次branch发布。旧actor随机回退、main/cleanup默认值不覆盖当前明确Boss编号、rebuild/research-v2、六人CAG及阶段二/三规则。

另有10件真实RESEARCH_ENTRIES文档字节按同ref物化（含大UM/CAG README和三件collaboration文档），这里只为原测试is_file存在性断言。它们的SHA与字节全部核对，**不声称逐份重读其中数学**，不写假stub、不额外done所引ID。详见[数据输入的精确read_scope](../../../../tools/evidence/frontier-testwork-and-packet-programs/data-dependency-manifest.json)。程序返回prompt路径不等于执行该角色；本批测试只在临时合成对话操作，不重置本轮身份或对真实公屏发消息。

## 全部共同26项与legacy独有8项
'''
b1+='\n| 两版共有测试名 | 实际义务 |\n| --- | --- |\n'+''.join('| `'+n.name+'` | '+scopes[n.name]+' |\n' for n in main_nodes)
b1+='\n| legacy独有测试名 | 实际义务 |\n| --- | --- |\n'+''.join('| `'+n.name+'` | '+scopes[n.name]+' |\n' for n in legacy_nodes[:8])
b1+=r'''

## checkpoint测试全部45项：精确复用而不复跑

此主源两refs同字节，SHA163e29ac55bc28254adc3d4b615f26491a2cb734167d9c761f4fad12029dd346。前批已独立全文读649行、真实配main/legacy程序各45项PASS（13.380/13.881秒）；本批复制实际运行JSON/原stderr与45义务表，核原source_inputs包含同SHA，并未再次运行。它校验软件snapshot/descriptor/scope/history/并发，不证明note里的“result”是数学定理。原setUp默认shared专测历史scope；另有专门未绑定CAG和未知save测试。
'''
b1+='\n| 原checkpoint测试 | 实际义务 |\n| --- | --- |\n'+''.join('| `'+x['name']+'` | '+x['assertion_scope']+' |\n' for x in prior45)
b1+=r'''

## work.sh的全部三行与真实接续

````bash
#!/usr/bin/env bash
set -euo pipefail
exec python3 "$(dirname -- "$0")/work.py" "$@"
````

它按调用路径$0的dirname找相邻wrapper，全部参数边界转发；不独立解析save/身份/认证或实现研究算法，不绑定根实现SHA。与使用BASH_SOURCE的另外两个shell入口保持区别。本批分别配真实同ref根程序，从临时repo外调用--help均exit0且包含checkpoint；这只验证该位置/参数的转交，不认证所有shell/符号链接调用场景。

## 实际新增运行和未覆盖内容

完整读完源码/测试后才启动[隔离复现器](../../../../tools/evidence/frontier-testwork-and-packet-programs/run_work_isolated.py)：main26/26 PASS（原日志20.182秒）、legacy34/34 PASS（40.274秒），共60个新增原测试实例；另work.sh帮助各一次。之前checkpoint90实例只复用。精确输入/执行位、命令、解释器/Git版本、原stdout/stderr在[runs/work-summary.json](../../../../tools/evidence/frontier-testwork-and-packet-programs/runs/work-summary.json)及各version JSON；outer wall time与原unittest时间分开。

全部init/start/合成身份/发送/迁移/credential fill仅在新临时file Git fixtures。credential fill询问形式含github.com只是在本地调用合成ASKPASS，没有网络认证；真实凭据/真实公屏/现业务clone身份和文件保存未操作。真实业务repo只读冻结材料和当前规则。不存在用stub假装canonical根实现；也没有把固定fixture通过当所有并发、损坏存储、跨平台、当前生产或数学正确性的完备证明。未完成、错误或候选正文可被程序备份，pushed/回执/测试与数学采纳分别保留。
'''
p1=obj('历史生命周期测试的版本路线与完整义务','frontier-lifecycle-test-versions-and-obligations','26/34生命周期测试及45保存测试完整语义，真实版本输入/有限运行与当前身份、数学真值分开。',[x for x in src if x['id']!='8981310291bda5d63e07'],b1)

mapping=json.loads(text('1cf29de35f3e8a430186'))
b2=r'''
本对象完整整理export_pro_packet.py源8981310291bda5d63e07（16800字节/342行，SHA b4b3e34252493c411cbaf5b06aa429d7d3c4933b560ba7a0f2f60a93d49af351），两冻结refs同字节；全部源码包括路径/围栏/链接扫描、prepare、ZIP回读、main和异常路径已逐行读完。它导出旧weighted-congestion接题资源，不是UM/CAG任务生成器或数学证明器，旧prompt不切换当前角色。

本批完成代码语义审查及有限真实输入拒绝；**没有重建旧整任务，没有正式canonical22文件ZIP或整包verified回执**。旧正式页当时取不到TASK/ZIP的事实保持不动。当前443B兼容入口、2108B历史UM提示、旧审查要求的整任务和提取TASK是不同字节身份；不能相互补名。

## 参数、路径和冻结读取

CLI要求--repo、--commit、--output-dir、--zip。先rev-parse核repo根，再用--verify/--end-of-options把指定commit-ish解析为完整40/64位提交；后续每件源经git show commit:path读取并按路径缓存，不读取dirty工作树。源限制research/前缀及安全相对POSIX路径：拒绝空、反斜杠、NUL、绝对路径以及任何空/./..路径段。该读取不自行检查Git普通file mode、论文真伪或当前运行脚本等于导出提交内SCRIPT；manifest.exporter_source只标所选提交的脚本字节。

output与zip必须仓库外新路径，lexists会拒绝既有文件/目录及dangling symlink，resolve后再核不在repo中，父目录须已存在；二者不能相同或祖孙包含。原git()包装没有当前工作台的Git环境清洗、超时或网络禁用保证；本批只在新临时repo并另加file协议/无全局认证环境运行。

## prepare的完整承重条件

程序从同一导出提交读PRO_BRIEF_SOURCES映射、review_status、任务、brief。数学源commit由mapping给出，必须完整hash；source_repository须HTTPS github.com且两段仓库路径。恰21个唯一S0–S20；review ledger IDs不能重复。brief和**整任务源文件**分别须等reviewed_brief_sha256和reviewed_task_source_sha256。任务必须恰一个以行首~~~text开启/~~~关闭的块；提取完整内容，只规范末尾为单LF。整个任务源SHA与提取TASK SHA不是同一命题。

TASK/brief使用的S数字标签须已注册；brief必须恰定义21个S链接，每个URL经unquote后等repository/blob/math_commit/该S第一source_file路径。每项所有source_files都从导出提交读取，再与旧数学commit该路径**全部字节相等**才接受，不是只比标题、选节或同路径。reviews/brief_reviews只复制其导出提交字节hash，历史review正文引用的证明hash不被重解释成当前源hash。

claim_ids必须全在导出提交ledger中，实际整条记录原样复制，不由README/review票数推断，也不验证其数学五轴真伪。此前发现的not_recorded、audit_only及坏applies_when字段不因复制进manifest而修复或升格。source记录除optional_path外的选节/scope说明等保留，source_files加原SHA、数学源SHA/commit，review URL固定在导出commit。

optional输出路径须安全且以optional/开头、无同名重复，总数恰19。真实mapping的19个是S2–S20；实现此处只数19，并不是另做标签到可选文件的一般定理。输出每篇是该S第一source_file的**整份文件**，不是只截mapping所写sections；所有原假设/历史内容仍在，不能把整篇一切Claim都当已被简报调用。S0/S1没有optional。默认2材料+19按需源+MANIFEST=22是满足前置条件后的合同，计数不自证已得到这22个。

## 链接转换和字节归档

brief原字节不动；只有optional文本的Markdown相对目的地址被转为数学源commit固定GitHub blob/tree URL。转换保query/fragment，角括号形式保留，按相对source目录normpath/URL解码/安全路径检查后quote编码；绝对、scheme/netloc、fragment根链接不改。扫描支持普通inline链接与reference定义，并跳过匹配的反引号/波浪围栏及完整inline-code跨度。它是所实现的有限Markdown扫描，不声明完整CommonMark解析；没有浏览器/视觉或所有语法认证。

MANIFEST同时保original_source_sha256、实际payload sha/bytes、transform/link改写数；source mapping/status/brief_reviews/exporter_source标其导出提交字节。MANIFEST本身不列入files的自引用hash；CLI额外输出其hash与zip hash。这些hash区别于数学commit、导出commit和历史证明冻结hash，不能合并。

write_and_verify以新目录0700、每文件xb、新ZIP x写入；ZIP成员名排序、时间固定1980、mode100644、DEFLATE9。随后检查成员集合与无重复、逐成员字节，实际extractall到临时目录，核manifest.files的每payload SHA，并逐件回读提取结果及输出目录，包括MANIFEST字节本身。失败会清理本次新目录/已创建ZIP；成功才CLI输出status=verified。它只证明本次字节/包合同，仍不证明数学正确、外审、优先权或发布消息。

## 真实映射全部范围与数学时态

本批实际完整读取相关PRO_BRIEF_SOURCES 469行/15727B全部字段（SHA75e017bcc11e214103a48cd90832c788515e1f6d585048621387f4a0cf08b1fa）。下表保21项选节、精确Claim ID和范围；完整所有23源路径/27审查路径及19optional名字以原JSON和数据依赖清单保全，不把引用变成额外done或重新证明。
'''
b2+='\n| S | 简报/源选节 | 全部Claim IDs与范围 |\n| --- | --- | --- |\n'+''.join('| '+x['id']+' | '+'；'.join(x['brief_sections'])+'；'+'；'.join(y['sections'] for y in x['source_files'])+' | '+('、'.join(x['claim_ids']) or '；'.join(x.get('claim_references_without_review_ledger_entry',[])))+'；'+x.get('scope_note','定义/Paper Fact，非新结果')+' |\n' for x in mapping['sources'])
b2+=r'''

已完整比较现正式《Pro冻结交付包的字节身份与实际证据边界》和《接题来源映射与文献导入的版本边界》，快照在comparison-manifest。它们保旧简报的全类Cd/ln d OPEN、S11未调用邻次扩展等历史口径；后来的近次数全态下界与精确三载荷对象各自有新证明，不能把旧导出状态倒填为已知新结论，也不能重发旧OPEN当当前全类答案。cohort存在至少一个、selector各自dual、模板全最小点障碍不等于原游戏无PNE、条件compiler需每front正η、固定hub不提供跨hub兼容等范围仍按精确来源；打包工具没有消除任何假设。

当前brief62627B已取得完整字节、hash匹配reviewed值，本子批只把它当真实hash/拒绝输入，**不冒称在此重新语义读完整数学brief**。相关640-entry ledger按此前全语义实读的精确SHA复用；数学commit的19篇原稿/27审查正文没有因此全部新取得/重读。10个路径存在性文档和brief的字节读取与主源代码/映射全文阅读分开，范围逐件在[data-dependency-manifest](../../../../tools/evidence/frontier-testwork-and-packet-programs/data-dependency-manifest.json)。

## 新增八组有限例与实际拒绝

[本批探针](../../../../tools/evidence/frontier-testwork-and-packet-programs/probe_packet.py)不修改原程序，实际完成八组：六种坏archive路径拒绝；完整单任务块提取及零/多块拒绝；prose/reference链接改写且inline/fenced code字节保持；编码目录逃逸拒绝；已存在/dangling/repo内输出拒绝；真实三文件小型ZIP写/解压/回读；坏manifest SHA回滚；真实当前资产输入拒绝。组内条件数和8组的计数分开，全部原观察在[packet-probes.json](../../../../tools/evidence/frontier-testwork-and-packet-programs/runs/packet-probes.json)。小型helper payload明确是synthetic三文件，绝非canonical22。

最后一组将真实当前map、640-status、brief、443B任务和导出器原字节，按inventory SHA物化为**新创建的临时Git提交**，不是伪造原历史提交。随后故意改dirty brief，调用未改原CLI；Git仍读已提交且hash正确的62627B brief，然后因当前任务SHA c4ab799d18139ca991bf3c03fe5d0db577a2deb369869a6ed7e8d2109627b1f1不同于旧reviewed任务76b12f434c6990930bbabe8b909ec96c4de7915afab4e38ae8211318846f0e89，exit1明确拒绝，无输出目录/ZIP。数学旧commit的blob读取在后续循环，未达到，故不能说本例重核全部原数学字节。

这个真实拒绝保全当前输入边界，没有重建缺失旧TASK、原正式ZIP、解包实物或verified；旧页当时缺原件事实不改。新临时root/file-only Git/合成输入不会访问真实公屏/凭据/网络，没有实际原仓库导出或额外数学suite。本资源可用于接续正确版本恢复和字节合同审查；仍需原任务/真实数学blob/实际导出commit才可能认证正式整包。主源代码完整处置与这些未满足运行前提分开。
'''
p2=obj('冻结接题导出器的字节合同与当前拒绝边界','frontier-pro-exporter-contract-and-refusal','342行导出器全文、真实21项映射与8组新有限例；当前TASK哈希漂移实际拒绝，未制造旧22文件包。',[x for x in src if x['id']=='8981310291bda5d63e07'],b2)

save(E/'formal-manifest.json',[{'path':p,'bytes':(S/p).stat().st_size,'sha256':sha(S/p)} for p in [p1,p2]])
save(E/'reading-scope.json',{'claim_receipt_path':'/workspace/scratch/37f0f9248cfc/boss4-r3-next15aa-claim.json','claim_tip':'f8aec6ba937b8d78e8c31f77a54296dc03f2df0f','initial_stale_capture':'earlier reused stem had unrelated15 IDs/tip776eb; zero intersection so no primary until actual new receipt, saved actual updated receipt','primary_full_reads':{x['id']:{'bytes':x['size'],'lines':len(text(x['id']).splitlines()),'actual_ranges':{'0267e9382e7d95b35a5e':[[1,215],[216,420],[421,580]],'de53a0261145104205aa':[[1,210],[211,410],[411,610],[611,777]],'8981310291bda5d63e07':[[1,210],[211,342]],'6a406a34c340855b3f7f':[[1,3]],'2f4fa59cd9903d4c32e9':[[1,230],[231,460],[461,649]]}[x['id']],'reused_previous_actual_complete_read':x['id']=='2f4fa59cd9903d4c32e9'} for x in src},'primary_bytes':130274,'code_dependencies':'seven previously complete independent full reads exact SHA reused','mapping_related_full_read':'all469 lines/all fields','brief_read':'all bytes/hash only for actual refusal, no new whole mathematical semantic read claim','existence_only_docs':10,'related_sources_done':[],'unread_or_truncated_primary_ranges':[]})
receipts=[]
for x in src:
 packet=x['id']=='8981310291bda5d63e07'
 receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':f'完整{x["size"]}字节/{len(text(x["id"]).splitlines())}行全文实际语义读取并核inventory SHA。'+('649行checkpoint测试精确复用前批完整读与真实45x2成功，不重复原run。' if x['id']=='2f4fa59cd9903d4c32e9' else '全部fixture/控制/异常/输出与独有内容已读，原件不改。'),'comparison_note':('与真实map全部469行、当前brief/task/status字节、两份完整正式Pro范围资源比较，实际当前task哈希拒绝；未读全部数学payload不冒称已读。' if packet else '与真实同ref root/board/checkpoint代码、另一测试版本/前批45义务及当前规则比较，路径存在性文档只真实字节/shape物化不冒称数学全读。')+'旧角色/默认控制不覆盖本轮。','decision_note':'integrated为完整自足软件资料，保全部来源/版本/义务、原字节与准确有限证据；不把计数/帮助/pushed/hash/小ZIP当数学或canonical整包完成。无真实公屏/凭据/身份操作，不额外done引用源。','disposition':'integrated','targets':[p2] if packet else [p1]})
save(W/'semantic-receipts.json',receipts);save(W/'next-candidates.json',read(E/'next-candidate-snapshot.json'));(W/'relation-review.md').write_text('''# 关系范围\n\n两资料是历史软件/来源/有限检查资源。生命周期和字节打包不能导出数学真值；与原Pro/保存资料保持版本和实际取得时态，不覆旧页。无新数学derives/attacks，不进入mapper或强制连通。五主源integrated，引用依赖没有额外done。\n''')
save(E/'attempts-and-boundaries.json',{'stale_capture':'first old stem had unrelated IDs; no primary read/write or receipt then; exact new unique receipt verified before primary','primary_exports':'checkpoint test exact prior byte reuse plus4 read-only clean show exports, all inventory hashes match','new_runs':'main26/legacy34 original lifecycle tests each once; shell help each once; exporter8 grouped finite checks including actual task-hash refusal','reused_runs':'prior checkpoint45 per ref, no rerun','not_done':['original canonical22 export/TASK/ZIP/verified','whole mathematical semantic read of brief or10 is_file-only docs','old math snapshot19source/27review byte verification','production/real credentials/real identity/public board','shared Git writes/claim/done/checkpoint/spawn/mapper','new math/PDF/browser suites']})
checks=[]
def check(n,v):
 checks.append({'check':n,'passed':bool(v)})
 if not v:raise AssertionError(n)
inv={x['id']:x for x in map(json.loads,(R/'cleanup/inventory.jsonl').read_text().splitlines())}
for x in src+deps+data:
 p=S/x['saved_path'];check('exact source identity '+x['id'],all(x[k]==inv[x['id']][k] for k in ['path','size','sha256','blob','sources']));check('exact source bytes '+x['id'],p.stat().st_size==x['size'] and sha(p)==x['sha256'])
c=read(E/'actual-claim-receipt.json');check('actual unique capture subset',c['status']=='pushed' and c['actor']=='Boss4' and {x['id'] for x in src}<=set(c['ids']) and c['remote_tip']=='f8aec6ba937b8d78e8c31f77a54296dc03f2df0f' and c['local_sync']['status']=='synced')
check('26 common/8 extra assertion identities',len(main_nodes)==26 and len(legacy_nodes)==34 and {n.name for n in main_nodes}<{n.name for n in legacy_nodes} and len(inventory)==60)
check('45 prior assertions preserved',len(prior45)==45)
for variant,count in [('main',26),('legacy',34)]:
 q=read(E/'runs'/f'{variant}-work.json');log=(E/'runs'/f'{variant}-work.stderr.txt').read_text();check('new finite suite '+variant,q['returncode']==0 and f'Ran {count} tests' in log and log.rstrip().endswith('OK') and len(re.findall('^test_',log,re.M))==count);check('file-only and shell helper '+variant,q['environment_guards']['GIT_ALLOW_PROTOCOL']=='file' and not q['real_remote_or_effective_credentials'] and q['work_sh_help_exit']==0 and q['work_sh_help_has_checkpoint']);old=read(E/'context'/f'{variant}-original45.json');check('prior45 exact source binding '+variant,old['returncode']==0 and any(x['id']=='2f4fa59cd9903d4c32e9' and x['sha256']==byid['2f4fa59cd9903d4c32e9']['sha256'] for x in old['source_inputs']))
probe=read(E/'runs/packet-probes.json');check('eight actual finite packet groups',probe['passed'] and probe['counted_cases']==len(probe['cases'])==8 and not probe['real_remote_or_effective_credentials']);last=probe['cases'][-1]['observed'];check('actual true-byte current input refusal',last['returncode']==1 and not last['output_exists'] and not last['zip_exists'] and last['dirty_worktree_not_used'] and last['current_task_sha']!=last['old_task_sha_unavailable'])
check('true source mapping all21 labels',len(mapping['sources'])==21 and {x['id'] for x in mapping['sources']}=={'S'+str(i) for i in range(21)})
for p in [p1,p2]:
 t=(S/p).read_text();meta=t.split('---\n',2)[1];check('flat MATEK '+p,all(re.search('^'+k+':',meta,re.M) for k in ['id','kind','type_tag','title','status','summary','source_refs']));check('formal C0 '+p,not any(ord(c)<32 and c not in '\n\r\t' for c in t));check('formal trailing '+p,all(l==l.rstrip() for l in t.splitlines()))
check('five receipt source identities',len(receipts)==5 and {x['id'] for x in receipts}=={x['id'] for x in src})
for x in receipts:check('complete semantic receipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note']) and all((S/p).is_file() for p in x['targets']))
result={'passed':True,'checks':len(checks),'scope':'source identity/read scope/finite evidence/receipts/format only, not mathematics or canonical historical ZIP certification','formal_forbidden_C0':0,'formal_trailing_whitespace':0,'details':checks};save(E/'self-check.json',result);save(W/'self-check.json',result)
(E/'README.md').write_text('''# 生命周期与打包程序证据\n\n五原件130274B全部主源语义实读，三测试649/580/777行、shell3行、导出器342行。七代码依赖完整旧读精确SHA复用；映射469行全字段新实读。brief只完整byte/hash，十文档只原is_file断言的真字节，不冒称新数学全读，不额外done。\n\n新增26+34原测试、两shell帮助、8组导出有限例；前批45x2保存测试复用不复跑。真实当前输入TASK哈希漂移实际拒绝、无canonical整包；小型三文件ZIP是helper例。file-only全新临时Git/合成身份与ASKPASS，不碰实际公屏/凭据/现业务身份。旧缺TASK/ZIP和旧OPEN时态准确保留。\n''');(W/'delivery.md').write_text('''# 五源交付\n\n两自足资料、五integrated receipts、原件及真实依赖/有限运行证据。Root据exact manifest复制并实际pushed后done；此子任务不做shared Git/claim/done/spawn。下一候选仅local progress实际快照，须Root全局Owner核查。\n''')
print(json.dumps({'formal_files':2,'formal_bytes':sum((S/p).stat().st_size for p in [p1,p2]),'primary_bytes':130274,'receipts':5,'checks':len(checks),'passed':True},ensure_ascii=False))
