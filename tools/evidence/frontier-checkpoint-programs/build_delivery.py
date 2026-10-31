"""Materialize self-contained historical software resources and exact receipts."""
from pathlib import Path
import ast,hashlib,json,re
E=Path(__file__).resolve().parent;S=E.parents[2];R=S.parent.parent/'boss4-research'
F=S/'archives/weighted-congestion/state/资料';W=S/'cleanup/workspaces/Boss4/r3-frontier-checkpoint-programs-next'
F.mkdir(parents=True,exist_ok=True);W.mkdir(parents=True,exist_ok=True)
def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
src=read(E/'source-manifest.json');deps=read(E/'dependency-manifest.json');byid={x['id']:x for x in src+deps}
def obj(name,ident,summary,selected,body):
 p=F/(name+'--资料.md');meta={'id':'weighted-congestion/'+ident,'kind':'resource','type_tag':'资料','title':name,'status':'historical-software-full-read-with-isolated-finite-evidence','summary':summary};refs=list(dict.fromkeys('source:'+z['commit']+':'+z['path'] for x in selected for z in x['sources']));p.write_text('---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in meta.items())+'source_refs:\n'+''.join('  - '+json.dumps(x,ensure_ascii=False)+'\n' for x in refs)+'---\n\n# '+name+'\n\n'+body.strip()+'\n');return str(p.relative_to(S))

b1=r'''
本对象整理checkpoint.py两个冻结版本的全部保存、审计、分支和确认合同，不把历史程序作为当前执行规则。main源db6af3d64d99cc147969是20508字节/377行，SHA7c36a36e0cb814250f542f0ac9fd7ea31c66406b471364d7ee7e014c6532a24e；legacy源f4ad07192854bfc106ad是22196字节/397行，SHA1e9b5da42f49658aac50d301831de8e77f5e55d6f992488296572dc4496e8d35。前者仅在main aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c，后者仅在legacy-cleanup 68fad804ec5946cb296f77dc5b336308a66abf12。

两件原码此前作为board入口真实依赖已分别全文实读，本批正式认领后逐件复核原字节/SHA并复用该完整阅读，不把前批只调用helper的27项测试假称save已经验证。全部代码、精确source身份、[版本差分](../../../../tools/evidence/frontier-checkpoint-programs/checkpoint-version.diff.json)和[逐源表](../../../../tools/evidence/frontier-checkpoint-programs/source-manifest.json)保全；本批另新增真实隔离保存测试。

## 实际输入域、默认范围和认证

save输入为repo、paths列表、message、token_file，legacy另可create_branch。repo经Git定位根；save在git-common-dir/wcg-checkpoint创建缓存，以writer.lock非阻塞flock排除**同一Git common dir**的第二写者，不是跨clone全局锁。拒绝detached HEAD、未完merge/cherry-pick/revert/rebase和unmerged index。origin需唯一且fetch/push地址完全相同，拒绝token形状和http(s)内嵌userinfo。

显式paths整体替换默认范围，不是添加到默认范围。每项须repo内相对路径或repo内绝对路径，拒绝..、解析后越界和不存在且未跟踪项；Git匹配用literal pathspec。未指定paths时，default_paths按本地wcg.save（缺省customer-attraction）、wcg.actor查表：共享登记表COMMON_PATHS、对应存档SAVE_PATHS及本人的research/workspaces/save/actor。actor/save为1至64的安全标识；未知存档只保公共登记表和本人工作区，未注册数学目录必须显式指定。目录当前存在或仍有跟踪删除项才进入有效默认范围，无有效项则明确失败，不偷偷回旧拥塞范围。

完整常量逐字保于[scope-contracts.json](../../../../tools/evidence/frontier-checkpoint-programs/scope-contracts.json)，包括所有COMMON_PATHS、三个数学存档路径、legacy特有repository-cleanup范围和CAG两个glob。COMMON_PATHS含根README/RESEARCH_STATE/CLAIMS/FAILED_ROUTES及research的claims/assets/review_status/graph/index/source_crosswalk双格式/catalog双格式；shared是旧weighted_congestion相关目录，unrelated-machines只取相应主题目录，customer-attraction取CAG正文/问题/审查/代码/测试/证据/文献/运行说明等。CAG的tests/audits/customer_attraction*.py和evidence/runs/*/customer_attraction*会展开为实际及已跟踪删除匹配，不把glob字符串当宽泛提交范围。legacy的repository-cleanup另有collaboration、根work.py及frontier/tools/tests。目录名称不验证当前六人问题或其中数学真值。

凭据仅按显式token_file、WCG_CHECKPOINT_TOKEN_FILE、本地wcg.tokenFile顺序选择外部文件；拒绝resolve后位于repo内。token函数提取github_pat_/ghp_至少12后续字符的匹配，要求恰一个**不同匹配串**，不是整个文件格式或真实远端认证。只记文件路径，给后续Git设置相邻checkpoint.py的ASKPASS环境；Username回固定标识、Password读取已选文件。SECRET正则另含其他限定GitHub-token前缀及PRIVATE KEY起始样式；这是启发式排除，不是所有秘密的完备检测器。本批只使用原测试字面合成串，未读取真实凭据。

## 本地提交、旧历史审计和回执

程序先检查已暂存但不在所选scope的文件，存在则在提交前失败。收集HEAD相对所选scope变更、已暂存所选变更和未跟踪所选文件，拒绝当前变更中的符号链接、凭据样式文件名/内容以及空白或凭据样式commit message。执行范围内git add -A，再diff --cached --check，若有真实暂存内容才commit；没有配置作者时临时提供WCG Researcher署名，不创建空commit。

本地snapshot=此时HEAD。descriptor对git cat-file可读的blob列branch、commit、path、SHA256；describe_assets自身未复核文件模式，普通文件限制来自当前symlink检查和后续outgoing历史审计，不能从descriptor存在单独推定普通mode。删除仍在files中但没有blob descriptor。descriptor文件名按路径SHA前16位命名。无新提交时，若缓存receipt对应同snapshot会复用其files/outgoing记录；否则以选中scope下当前commit diff-tree补文件列表。程序先写status=local-only回执并输出LOCAL_CHECKPOINT，然后才尝试网络/历史审计。这个输出**不表示已推送**，也不表示claim/done或数学完成。

audit_outgoing不是只看最终文件或这次git add。它取remote_tip..head全部未发布祖先提交，逐个扫描原始commit元数据；以combined merge diff取实际新改变的文件名，逐名检查scope、凭据样式路径及普通blob模式100644/100755，并对每个不同blob全部字节扫描SECRET。曾经写入后覆盖/删除的secret、曾存在后删掉的symlink、merge resolution中的secret和已预提交的scope外文件都能阻止push；已经发表的远端peer在scope外的独立内容不会被当作本方新引入。此为指定实现/测试范围，不能泛化成任意Git攻击/秘密形式的完备安全证明。

## push、并发和哪些字段代表什么

每次push前必须成功fetch远端分支到私有本地ref，且不改FETCH_HEAD；不能用陈旧tracking ref猜baseline。fetch的+仅允许更新**本地私有ref**，push本身无force。fresh baseline后审计全部outgoing历史，将commits/files求并进回执，描述符改用当前准备push的head，记录checked_head，再普通push并重新fetch。

只有head确为新远端tip祖先时回执才变pushed，另给remote_tip和pushed_head。若push失败且远端仍为head祖先，视为认证/策略失败而停止；远端真实分叉时，若其他tracked工作脏则保本地snapshot并停止，否则普通merge。冲突时merge --abort并保原snapshot和冲突文件名；成功合并后head更新、再次fresh fetch/审计/push。循环最多20次，含短指数jitter；外部HEAD变化会停止。旧重试程序不覆盖本轮认证失败停止同凭据重试的明确规则，本批也没有对真实凭据执行它。

**commit字段保持最初本地snapshot，不保证等于pushed_head。** 并发merge后，checked_head/pushed_head和当次asset.commit指向合并后的head，remote_tip还可能是该head的后继；应按具体字段和祖先条件解释。新增隔离例在两版都实际得到commit≠pushed_head、资产commit=pushed_head。不能只看到commit或LOCAL_CHECKPOINT就把旧blob当成最终推送内容，更不能把本软件回执与当前clean语义收据混为一谈。

## 两冻结版本的完整实质差别

| 行为 | main db6… | legacy f4… |
| --- | --- | --- |
| 可保存文件分支 | 仅main；wcg/board专门拒绝，其余非main也拒绝 | 必须等于wcg.branch绑定值（缺省main），并check-ref-format |
| 公屏排除 | 固定wcg/board | 配置wcg.boardBranch、wcg/board和wcg/board-* |
| 默认repository-cleanup范围 | 没有专用表项，退回公共/本人workspace规则 | 专门加入collaboration、work.py、frontier tools/tests |
| descriptor.branch | 固定main | 实际绑定文件分支 |
| 远端分支不存在 | fresh fetch失败则local-only并停止 | 仅显式create_branch且非main、ls-remote确不存在时，可fetch main作审计baseline；head必须从当前远端main派生，仍普通push |
| CLI选项 | 无--create-branch | 有--create-branch，显式允许首次发布绑定分支 |

其余本地/历史/哈希/并发保存主体相同但两文件不是duplicate。新增实际例表明：同一已存在非main绑定分支和同一显式首次分支，legacy能pushed并描述实际branch，main在提交前拒绝。当前工作分支、长期公屏、Boss编号和不新建远端分支等要求由本轮根规则决定，不从任何旧实现恢复。

## 新增真实隔离验证与复用范围

related原test_checkpoint.py源2f4fa59cd9903d4c32e9（35108字节/649行，SHA163e29ac55bc28254adc3d4b615f26491a2cb734167d9c761f4fad12029dd346）已完整读完fixture与45项断言，没有额外done该测试源。它对两冻结ref同字节；分别配原checkpoint.py和checkpoint.sh，在fresh临时Git根及bare文件远端各运行一次。

本批新增main 45/45 PASS（原日志13.380秒），legacy 45/45 PASS（13.881秒），另每版6个新增有限例（3个保存语义、3个真实根程序兼容行为）均PASS。它们是90个原测试运行实例和12个新例，不是90种独立证明。精确输入、执行位、Python/Git版本、命令、原stdout/stderr和隔离环境见[runs/summary.json](../../../../tools/evidence/frontier-checkpoint-programs/runs/summary.json)、[复现器](../../../../tools/evidence/frontier-checkpoint-programs/run_isolated.py)和[新增例](../../../../tools/evidence/frontier-checkpoint-programs/probe_fixture.py)。

所有Git仅在新临时目录，GIT_ALLOW_PROTOCOL=file，系统/全局配置禁用，移除旧Git/WCG路由与SSH代理，禁交互，只有合成fixture字符串；无共享Git、真实公屏/远端、有效凭据或身份操作。临时目录已清除，输入及日志保全可重建。没有运行实际root start/sync/身份绑定、没有真实认证/部署/数学suite，没有把scope或secret扫描计数提升为数学真值。可复用的是精确保存合同和这些有限软件例，不能从pushed推断数学定理成立。
'''
p1=obj('研究快照保存的范围审计与双分支版本','frontier-checkpoint-scope-history-version','两checkpoint全文及真实45项测试；本地snapshot、outgoing历史、pushed_head与数学完成严格区分。',[x for x in src if x['path'].endswith('checkpoint.py')],b1)

descriptions=[
'保存并重放descriptor的真实普通blob SHA/远端提交。','重复保存无空commit。','scope外未暂存脏文件保留且不入提交。','scope外已暂存文件阻止本次commit且index保留。','显式paths包括根文件/含空格中文路径。','删除被提交但无blob descriptor。','fetch/push注入离线保本地snapshot，同命令重试只保存一次。','真实本地push后注入丢响应仍可fetch确认。','远端不交变更自动merge并保双方。','同文件真冲突abort保本地snapshot/正文。','其他tracked工作脏时分叉停止且内容不丢。','同common-dir活跃writer锁拒绝第二写者。','detached及公屏分支拒绝。','凭据样式正文/commit message、越界/缺路径在提交前拒绝。','暂存合成secret又把工作树改回HEAD，scope add覆盖旧index而不泄漏。','外部合成token只记路径、不进config或JSON回执内容。','继承Git路由不能写诱饵index。','本地commit与push间peer移动仍能merge两方。','缺Git署名时临时署名支持commit与merge。','checkpoint.sh可从clone外按--repo执行完整CLI。','无效/仓库内token文件拒绝。','origin fetch/push目的地不同则提交前拒绝。','此前scope外commit不能搭本次scope push便车。','显式覆盖backlog范围时receipt/outgoing/descriptors含全部相关提交/文件。','历史secret被安全文字覆盖仍阻止push。','历史secret后来删除仍阻止push。','历史凭据文件名和原始commit元数据即使后来删除仍拒绝。','历史symlink后来删除仍拒绝。','已公开peer的scope外不交变更不阻止merge，不误记本方outgoing。','合并resolution历史secret拒绝，原left祖先保留。','默认scope只含本人workspace，不取peer草稿。','UM存档取本主题/公共登记表/本人workspace，排除旧WC及相似前缀。','无绑定时默认当前CAG与本人当前workspace，排除旧WC/shared/peer。','CAG平铺audits/已跟踪删除audits/paper资产正确入scope，排除相似目录和peer。','无绑定但仅有旧scope时不回退WC，要求显式范围。','UM绑定下预提交旧WC不能搭便车。','未知存档只公共登记表和本人workspace，不猜未注册数学目录。','未知存档无有效默认项拒绝；显式paths可保存。','显式shared保旧主题默认值。','已跟踪删除UM资产仍保在默认scope。','默认本人workspace与显式处理peer范围的区别。','预提交peer workspace不在默认scope，阻止push。','actor含../不能逃默认目录。','无actor时坏save也被拒绝。','fresh remote baseline不可得时不尝试push，保本地commit。']
test=byid['2f4fa59cd9903d4c32e9'];tree=ast.parse((S/test['saved_path']).read_text());nodes=[n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')];assert len(nodes)==len(descriptions)==45
inventory=[{'name':n.name,'start_line':n.lineno,'end_line':n.end_lineno,'assertion_scope':d} for n,d in zip(nodes,descriptions)];save(E/'test-assertion-inventory.json',inventory)
b2=r'''
本对象保全三个完整兼容入口：board.sh源988a0574030a7fded769为230字节/5行；checkpoint.sh源794a190330ebe5b3679b为149字节/4行；tools/work.py源b054428c6de628f29738为534字节/13行。三件两冻结refs同字节，完整SHA/原路径见[原件清单](../../../../tools/evidence/frontier-checkpoint-programs/source-manifest.json)，逐份完整阅读；没有以入口小/相同版本数代替读取。

## 每份入口实际执行什么

board.sh是bash set -euo pipefail，在子shell根据BASH_SOURCE求自身目录，exec python3相邻board_entry.py并将全部参数按原边界转发。它自己不解析actor、save或token，不证明被调用程序/依赖正确；相邻入口可写本地config、读外部路径并调用公屏，因此不能把shell五行概括成纯只读。前批完整board/entry源码资源与同SHA两版27项成功fixture证据已准确保留在context；该成功绑定的source_inputs逐项含本源board.sh SHA，**本批复用而不重跑**。这些旧fixture只是真实依赖的本地测试，不是服务端认证或当前公屏PASS。

checkpoint.sh同样set -euo pipefail并定位自身，exec python3相邻checkpoint.py，全部参数原样转发，不依赖当前cwd。它不会自动补存档、增加paths或改变版本；运行行为由相邻20508/22196B程序决定。本批两套45原测试中的完整launcher用--repo从clone外实际调用它，源字节和执行位真实配入fixture。

tools/work.py在模块顶层按自身resolve路径parents[3]寻找repo根work.py，根文件缺失即SystemExit（import同样先检查），提示使用完整根附件；作为__main__时runpy.run_path(root,run_name='__main__')，import时运行根文件并把非dunder全局名字复制进兼容模块。因此它没有独立CLI实现，也没有把根程序固定为某SHA。相同534字节wrapper配两个不同根work.py可有不同控制行为；import并不等于只读解析源码，实际会执行根文件顶层代码。对本次已完整读完的两个根版本，顶层为定义/常量，导入未调用main；未来别的根程序不能据此自动认证无副作用。

## 真实根依赖：全文读取而不额外done

| 根work.py冻结版本 | 完整大小/行数及SHA | 真实控制语义 |
| --- | --- | --- |
| main d9b5b49ab665613450d6 | 26199/522；6946299455b653526a548d7108a29480ab328acf7cc4392bfa6959e870229f1d | 默认CAG存档，main文件分支；保旧wcg/work迁移到main；固定公屏wcg/board |
| legacy 3c0404b7974eca538863 | 31695/618；bc2cfda7fc2b12b7fa21d75b1266a14bc6993a40e6a31cc90e0f8eb88b301c4e | 新start默认cleanup/research-foundation-20261028与repository-cleanup、专用公屏；旧绑定可保，支持显式分支、公屏、首次发布；同步后可把bootstrap交还实际根程序 |

两件均独立逐行全文读完并核inventory SHA，仅作相关依赖，不复领/额外done。根源码全保于[依赖表](../../../../tools/evidence/frontier-checkpoint-programs/dependency-manifest.json)。两者共有外部凭据文件形状验证/临时ASKPASS、repo校验、actor/save/role绑定、本地writer锁、stash保脏工作后fetch/merge/恢复、workspace身份profile及resume、只读取远端已发表普通workspace文件、read/send/dm/inbox/ack/pending/retry/discard/checkpoint转发。这些函数的存在和代码全读不等于本批运行过它们。

main根程序只有boss/cleaner/editor的CAG绑定，新start默认boss；legacy加清理角色映射、文件分支wcg.branch/公屏wcg.boardBranch、board-init、visit --branch、checkpoint --create-branch和先同步再handoff。两者actor都有旧R-UUID随机回退。它们都不覆盖当前根规则的明确Boss编号、rebuild/research-v2、六人CAG数学焦点、阶段二/三分开和本轮认证边界。本批没有调用start、改身份、同步真实clone或执行所链旧角色prompt；根work.py源码出现的URL/远端名称只是冻结代码数据，未访问。

新增每版本三个wrapper例只执行**真实同ref根代码的--help、import，以及缺根失败**：help退出0含checkpoint；import得到可调用main和相应默认常量；无root以明确错误退出1。没有用伪造stub冒充canonical根实现，也没有把帮助/导入成功扩成root工作流或test_work全suite PASS。

## 45项原测试的全部实际义务

test_checkpoint.py的完整649行已实际读完，下面逐项保assertion；ROOT/导入定位、合成作者、bare remote、work/peer clone、初始shared绑定/note/outside基线、锁/故障补丁/原main均保原件。其两冻结ref同字节，但只在新的隔离目录和同ref程序配对运行，不与真实旧clone混绑；该related测试源未额外done。
'''
b2+='\n| 原测试 | 实际assertion |\n| --- | --- |\n'+''.join('| `'+x['name']+'` | '+x['assertion_scope']+' |\n' for x in inventory)
b2+=r'''

## 新证据、版本和仍未认证的内容

在已交付evidence/资料中未找到两checkpoint SHA的save suite成功run（前批27项仅helper/ASKPASS，明确不等于保存路径）。本批新增每版45原测试及6个额外例，各只运行一次，均exit0；原stderr包含LOCAL_CHECKPOINT行与unittest的ok交错，整体末尾明确Ran 45 tests/OK，不能用单行末尾匹配误判失败。原日志秒数main13.380、legacy13.881；复现器外层壁钟见JSON，不混用。新增保存例保留实际本地snapshot和merge后pushed_head及descriptor提交，两个非main分支例按版本分别观察“提交前拒绝”和“pushed”，不能只记六个PASS而抹平行为不同。

本地fixture中的全部Git均file协议、新临时仓库；禁系统/全局配置、清旧路由/身份/SSH代理、禁交互，只用源码构造的合成token。未访问真实认证文件、真实公屏或远端；业务repo仅为读取冻结源/现规则，不对其运行保存或身份操作。没有新增数学/外文/视觉/生产认证；正则秘密扫描、路径哈希、pushed、帮助或测试数量都不代表数学正确、来源已审或全仓完成。

这些入口适合复用来定位“实际执行哪个版本”、确认旧封装不是独立算法，以及区分根依赖、本地保存、远端可达、文件哈希和数学采纳。未运行的根程序全工作流、test_work双版本suite、真实服务认证、任意跨平台/并发/故意损坏场景仍各需自己的证据；本批没有以这些未做事项捏造失败或无疑PASS。原件不修，所有相关源保持各自ID和Owner。
'''
p2=obj('兼容程序入口的真实依赖与保存测试范围','frontier-checkpoint-wrapper-dependencies-tests','三包装入口完整语义、双根依赖全文、45原断言和有限新增验证；复用board成功run不重复。',[x for x in src if not x['path'].endswith('checkpoint.py')],b2)

save(E/'formal-manifest.json',[{'path':p,'bytes':(S/p).stat().st_size,'sha256':sha(S/p)} for p in [p1,p2]])
reading={'claim_capture':'actual-claim-receipt.json','primary_bytes':sum(x['size'] for x in src),'full_read_sources':{x['id']:{'bytes':x['size'],'lines':len((S/x['saved_path']).read_text().splitlines()),'scope':'whole source; exact reused previous actual full read for board.sh/checkpoint.py; newly full-read checkpoint.sh/work.py'} for x in src},'related_full_reads':{x['id']:{'bytes':x['size'],'lines':len((S/x['saved_path']).read_text().splitlines()),'scope':'whole source independently read, no additional done'} for x in deps},'unread_primary_or_truncated_ranges':[],'extra_sources_done':[]}
save(E/'reading-scope.json',reading)
receipts=[]
for x in src:
 is_checkpoint=x['path'].endswith('checkpoint.py')
 receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':f'完整{x["size"]}字节/{reading["full_read_sources"][x["id"]]["lines"]}行实际全文实读；checkpoint.py与board.sh已在前批作真实依赖全读，本批核完全相同inventory SHA复用完整读；新两入口逐行读完，原件独立保留。','comparison_note':'与同ref/不同ref实际依赖、两完整checkpoint/根work.py、45原assertion及当前根规则比对。新增45+6每版有限隔离结果完整保存；board.sh同SHA前批27成功绑定复用不重跑；原角色/分支控制不覆盖当前。','decision_note':'integrated为自足软件资源；完整范围/量词、状态、实际Git/认证/入口副作用与未验证范围保全。local-only/pushed/hash/测试不当数学完成；无真实公屏/有效凭据/身份或共享Git操作，不额外done相关源。','disposition':'integrated','targets':[p1,p2] if is_checkpoint else [p2]})
save(W/'semantic-receipts.json',receipts);save(W/'next-candidates.json',read(E/'next-candidate-snapshot.json'))
(W/'relation-review.md').write_text('''# 资料关系审查\n\n两资料共同解释兼容调用、实际版本、scope/history审计和有限软件证据。与前批board资料是实现/来源/证据范围关系，无新数学derives或attacks；不把pushed/hash/ack当数学证明或清洗done。不进入mapper或强制连通。五源原件/身份独立保留，相关根/测试不额外done。\n''')
save(E/'attempts-and-boundaries.json',{'claim':'only started primary after exact capture status/actor/IDs/local_sync verified','exports':'3 primary exact copies from previously read dependencies after claim; 2 primary read-only clean show; 3 related sources clean show and full reads','previous_run_reused':'board.sh exact SHA occurs in previous full paired 27-suite source inputs; no repeat','new_runs':'45 original plus6 extra per checkpoint ref pairing, one time each, all exit0','no_failures_or_primary_truncations':True,'never_run':['shared Git mutation/claim/done/checkpoint/spawn','real public board/remote/credentials/identity','actual root start/sync/save in real checkout','test_work suites','math/PDF/browser suites'],'extra_sources_done':[]})
checks=[]
def check(n,v):
 checks.append({'check':n,'passed':bool(v)})
 if not v:raise AssertionError(n)
inv={x['id']:x for x in map(json.loads,(R/'cleanup/inventory.jsonl').read_text().splitlines())}
for x in src+deps:
 p=S/x['saved_path'];check('exact identity '+x['id'],all(x[k]==inv[x['id']][k] for k in ['path','size','sha256','blob','sources']));check('exact bytes '+x['id'],p.stat().st_size==x['size'] and sha(p)==x['sha256'])
claim=read(E/'actual-claim-receipt.json');check('actual claim exact',claim['status']=='pushed' and claim['actor']=='Boss4' and set(claim['ids'])=={x['id'] for x in src} and claim['local_sync']['status']=='synced')
check('45 assertions accurately enumerated',len(inventory)==45 and len({x['name'] for x in inventory})==45)
for variant in ['main','legacy']:
 for suite in ['original45','new6']:
  result=read(E/'runs'/f'{variant}-{suite}.json');check('new isolated suite exit0 '+variant+suite,result['returncode']==0 and result['environment_guards']['GIT_ALLOW_PROTOCOL']=='file' and not result['real_remote_or_effective_credentials'])
 log=(E/'runs'/f'{variant}-original45.stderr.txt').read_text();check('45 raw unittest result '+variant,'Ran 45 tests' in log and log.rstrip().endswith('OK') and len(re.findall('^test_',log,re.M))==45)
 observations=json.loads((E/'runs'/f'{variant}-new6.stdout.txt').read_text());check('six actual finite observations '+variant,len(observations)==6)
 check('snapshot versus pushed head '+variant,observations[0]['result']['commit']!=observations[0]['result']['pushed_head'])
 expected='pushed' if variant=='legacy' else 'rejected-before-commit';check('two non-main version boundaries '+variant,all(x['result']['status']==expected for x in observations[1:3]))
 prior=read(E/'context'/f'{variant}.json');check('prior exact board.sh successful binding '+variant,prior['returncode']==0 and any(x['id']=='988a0574030a7fded769' and x['sha256']==byid['988a0574030a7fded769']['sha256'] for x in prior['source_inputs']))
for p in [p1,p2]:
 t=(S/p).read_text();meta=t.split('---\n',2)[1];check('flat MATEK '+p,all(re.search('^'+k+':',meta,re.M) for k in ['id','kind','type_tag','title','status','summary','source_refs']));check('formal C0 '+p,not any(ord(c)<32 and c not in '\n\r\t' for c in t));check('formal trailing '+p,all(l==l.rstrip() for l in t.splitlines()))
check('five complete receipts',len(receipts)==5 and {x['id'] for x in receipts}=={x['id'] for x in src})
for x in receipts:check('semantic source receipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note']) and all((S/p).is_file() for p in x['targets']))
out={'passed':True,'checks':len(checks),'scope':'source exact binding/actual read scopes/finite runs/receipts/format only; not production or math proof','formal_forbidden_C0':0,'formal_trailing_whitespace':0,'details':checks};save(E/'self-check.json',out);save(W/'self-check.json',out)
(E/'README.md').write_text('''# checkpoint与兼容入口证据\n\n五原件43617B全部语义实读，三既有依赖完整实读按精确SHA复用，新两wrapper全文；相关测试35108B与双根work.py26199/31695B均完整独立实读不额外done。新增每ref45原测试+6有限例均PASS，前批board.sh成功绑定精确复用不重复。\n\n两份自足资料保本地快照、outgoing历史/范围、双分支差别、wrapper真实依赖、全部45义务与边界；原字节不修。file-only新临时Git仓库，无真实公屏、远端、有效凭据、身份或共享Git写。程序pushed/hash不表示数学真值或当前clean完成。\n''')
(W/'delivery.md').write_text('''# 五源交付\n\n两自足软件资源、五条integrated语义收据、五原件及真实依赖/测试、逐版本有限日志。Root按exact manifest复制后实际checkpoint pushed再done。此子任务不做共享Git/claim/done/spawn。下一候选仅实际本地progress快照，Root另核全局Owner再领。\n''')
print(json.dumps({'formal_files':2,'formal_bytes':sum((S/p).stat().st_size for p in [p1,p2]),'primary_bytes':sum(x['size'] for x in src),'receipts':5,'checks':len(checks),'passed':True},ensure_ascii=False))
