#!/usr/bin/env python3
"""Author the three complete resource bodies from fully read ledger values."""
from pathlib import Path
import json
E=Path(__file__).resolve().parent;S=E.parents[2];D=S/'archives/customer-attraction/state/资源';D.mkdir(parents=True,exist_ok=True)
load=lambda p:json.loads((E/'original'/p).read_text())
m=load('research/path_migration.json');b=load('research/branch_cleanup.json');c=load('research/source_crosswalk.json');n=json.loads((E/'normalized-records.json').read_text());a=json.loads((E/'ledger-structural-audit.json').read_text())
def front(ident,title,summary,paths):
 return '\n'.join(['---','id: customer-attraction/'+ident,'kind: resource','type_tag: 资源','title: '+title,'status: historical-ledger-semantics-with-specific-current-correction','summary: '+summary,'source_refs:']+['  - source:'+co+':'+p for p in paths for co in ['68fad804ec5946cb296f77dc5b336308a66abf12','aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c']]+['---','','# '+title,'',''])
def cell(v):return str(v).replace('|',r'\|').replace('\n','<br>')
def code(v):return '`'+cell(v)+'`'
body=r'''## 对象、原件与读取范围

本表保存旧树的五种路径身份：移动、规范代码入口替代、第一轮退役、测试入口重合以及重建根文档。它是恢复合同，不是所有原文件的字节相等证书、数学替代证明或当前删除指令。本批全文读version和全部86个映射条目，保留79个不同原键、67个不同目标；7个测试键与moved重复，不能把86当86个独立来源。

[原JSON](../../../../tools/evidence/source-migration-crosswalk/original/research/path_migration.json)7,217字节，两冻结版本同字节，精确SHA及源commit见[原件清单](../../../../tools/evidence/source-migration-crosswalk/source-manifest.json)。以下全部映射在正文列出，原始路径和历史保存目标按旧仓库根解释。它们不要求当前archives树恢复旧层级。

## 五字段不能混用

| 字段 | 实际计数及合同 |
| --- | --- |
| moved | 58；旧目标名到历史、输入、证书、运行、测试等角色的新去处。没有hash字段，路径对应本身不保证内容未改 |
| retired_code_paths | 10；旧分散代码入口改指唯一规范包。可以重构，不能由同角色推出逐字节等价或完整软件实现 |
| first_curation_retired | 8；旧根/旧math摘要退役到retired_snapshots恢复入口。多对一不表示八原文件本来相同；完整原版本需按其来源恢复 |
| retired_test_entrypoints | 7；逐项等于moved的对应测试行，是测试角色的重复登记，不额外新增7文件或7次测试 |
| reestablished_root_docs | 3；CLAIMS/FAILED_ROUTES/RESEARCH_STATE根路径重新承担当前导航，同时历史快照入口仍在。它要求理解新旧身份共存，不能照旧“旧路径必须不存在”删除新根文档 |

旧build_crosswalk把moved与retired_code_paths合成68个来源解释分母，要求解释列表恰覆盖它们；它没有把其余8/7/3全部收入分母。旧check_assets对moved、退役代码、第一轮退役要求旧不存在/新存在，对重建根文档则要求两边都存在；它没有遍历retired_test_entrypoints。两个程序的实际合同已保存在[生成合同](旧路径解释账本的覆盖与生成合同--资源.md)和[资产巡检](旧资产巡检的文件角色与哈希边界--资源.md)，本批未调用它们。

“现行算法”“规范包”“内部审读”等须回数学正文/真实程序/对应版本证据。尤其共同目录两阶段设施的客户按原子负载费用作NE，与顺序客户吸引终局均分及每份全历史纯SPE不同；路径留在同仓不使两个模型相等。旧有限菜单极小值、真实局部极小值、存在性、实例最优和位多项式也不能因换入口合并。

## 全部映射

'''
for field,title in [('moved','移动'),('retired_code_paths','规范代码替代'),('first_curation_retired','第一轮退役'),('retired_test_entrypoints','测试入口重合'),('reestablished_root_docs','重建根文档')]:
 body+='### '+title+'：'+field+'\n\n| 原路径 | 旧保存/替代入口 |\n| --- | --- |\n'+'\n'.join('| '+code(k)+' | '+code(v)+' |' for k,v in m[field].items())+'\n\n'
body+=r'''## 核对、边界与接续

新增本地检查只读本批原字节和冻结inventory：68原键与解释表集合相等、7测试映射是moved的精确子集。全部路径/版本记录保留，不将缺失旧路径当数学失败，不把同一retired_snapshots目标当完整原件本身。复用既有结构结果也不成为重新运行旧suite或全部原数学审读。

一份来源可能保留在Git不可变提交、历史实体文件和新正文多个层次；“此路径退役”“原字节可恢复”“数学已被当前证明覆盖”是三个不同命题。这里完整处置的是这份迁移账本，所引用原稿、代码、输入、证书及其数学仍各按自己的源receipt处理，没有额外done。

与[逐文件历史来源保全](退役分支的逐项来源保全与恢复边界--资源.md)和[来源解释资源](来源解释账本的历史语义与当前校正--资源.md)的已知联系是来源恢复、导航和文件身份；未新增数学推导边。当前三级图允许孤立对象，不能由路径对应或共同目录制造因果关系。
'''
(D/'路径迁移的五类身份与退役例外--资源.md').write_text(front('source-path-migration-five-contracts','路径迁移的五类身份与退役例外','完整保存五字段86映射、79原键/67目标及测试子集、重建根文档例外，区分路径合同、字节恢复和数学替代。',['research/path_migration.json'])+body)
body=r'''## 资源身份与所有读取范围

`branch_cleanup.json`是一次旧远端分支收口的历史记录。schema1的全部顶层值、6个分支对象及其完整files数组、141条归档来源、42条当前树省略项、secret/数学/删除策略均已逐项实读。本资源保全这些合同和每个定位，但没有因为读清单而读完141份被列数学、全部聊天或执行其中代码。

[原清单](../../../../tools/evidence/source-migration-crosswalk/original/research/branch_cleanup.json)123,785字节，两冻结源同字节。原SHA、源commit以及本批实际读取的正式资源见[证据目录](../../../../tools/evidence/source-migration-crosswalk/README.md)。归档路径按旧根解释；附表中的hash是原记录的预期值，新的141项核对仅与精确冻结inventory相等，不能称已完成141份原tip字节双向核验。

## 顶层保存链与历史完成声明

原目标是当时远端只保留main和wcg/board，删除前保存独有数学与完整研究来源，不改变当时任意人数一般半覆盖目标。phase写`completed_remote_deletions_verified`、main_not_overwritten为true，是作者的历史操作报告，不是本批对当前远端的查询。

| 层次 | 原记录完整值 |
| --- | --- |
| base_main | `11a68141e0c85822ab8e9a06d7b81e230e369e8a` |
| preservation_merge | `4500d92740182736391b3f21a11c537739f9cdeb` |
| preservation_commit | `d5258e92db170bc04878d8d42f91a332ad3ffa40` |
| remaining main | `d5258e92db170bc04878d8d42f91a332ad3ffa40` |
| remaining wcg/board | `84cac2643ac75f50d610d0e307db24393541fb27` |

原deletion_policy要求先远端确认main，再按已观察的精确tip compare-and-delete；tip变化须重新检查。本页没有授权今天删除任何分支，不把旧main/wcg-board方案套到当前结果分支和公屏。当前焦点恰六人与三阶段清洗也不被旧“不改一般目标”措辞覆盖。

## 六分支、不同来源角色与恢复范围

四研究tip原base均为`562ff7a9326c9997379662acf5ecff1e69a87a9d`；两通信tip的base为null。6项status均为`deleted_with_exact_tip_compare_and_delete`。四研究分支reason是独有数学候选/审计归档而旧路由不采用；两通信分支reason是设置、进度、查新警报和指针已看，实质落盘资产进入源档。此reason是旧记录，不冒称本批已重新读这些事件正文。

| 分支 | 完整tip | commits_not_in_main（旧记录） | files条数 | history_preserved_in_main |
| --- | --- | ---: | ---: | --- |
'''
for r in b['branches']:body+='| '+code(r['name'])+' | '+code(r['tip'])+' | '+str(r['commits_not_in_main'])+' | '+str(len(r['files']))+' | '+str(r['history_preserved_in_main']).lower()+' |\n'
body+=r'''
四研究tip的本地只读祖先检查早已成功：它们是保存提交d5258、preservation_merge4500和冻结main aefc58ea的祖先；本批复用[原检查记录](../../../../tools/evidence/source-migration-crosswalk/comparison/tools/evidence/facility-front-primary/branch-preservation-check.json)，没有重复跑。同一旧shallow记录对68fa及通信tip的返回1不能证明历史缺失，也不是当前远端审计。

141实体归档只来自两个快照：multi_lane来自or-topic-battle的4f9269…，independent_review来自topic-selection的1b8928…。另两个研究tip的独有历史可按完整提交恢复；不能因为141归档只列两来源，就推断另外两支没内容或所有同路径版本相同。两套编号/候选/审查意见各保身份，不按同名Claim自动合并。

## 全部归档路由与原预期字节

所有141条status逐字相同：`historical source; original proof/candidate/observation levels retained; not promoted or independently re-reviewed in this cleanup`。下面不重复该句，但逐条保存branch、commit、原路径、归档路径、字节和SHA，恢复时先选择正确快照。它声明保留旧等级，不授予今日证明/独立性/外审/新颖性认证。

| # | branch / commit | 原路径 | 归档路径 | bytes / 原SHA-256 |
| --- | --- | --- | --- | --- |
'''
for i,r in enumerate(b['archived_sources']):body+='| '+str(i+1)+' | '+code(r['branch'])+' / '+code(r['commit'])+' | '+code(r['original_path'])+' | '+code(r['archived_path'])+' | '+str(r['bytes'])+' / '+code(r['sha256'])+' |\n'
body+=r'''
## 六分支files数组完整保留

这些字符串是当时比较输出/清单，研究分支的A/M前缀表示旧记录的增改，通信项没有这些前缀。它们不是当前Git diff，也不是每条数学已读证明。数组中同路径跨分支出现不自动表示同一字节。

'''
for r in b['branches']:
 body+='### '+r['name']+'\n\n```text\n'+'\n'.join(r['files'])+'\n```\n\n'
body+=r'''
## 42项没有进入当时当前树的记录

42项共享同一disposition：旧操作指令、分支工具/测试、仅身份工作区或设置，源历史保存在main。这里完整保留原branch/path；不据此删除今天有数学内容的同名文件。旧“一般主攻”“main-only”及角色提示词只是待理解历史，不执行。

| branch | path |
| --- | --- |
'''
for r in b['omitted_current_tree_items']:body+='| '+code(r['branch'])+' | '+code(r['path'])+' |\n'
body+=r'''
## 原数学策略、secret记录与新增检查的真实边界

原数学策略明说：候选、证明草稿、复现观察、失败接口和新颖性限制分别保留，本次不重新认证任何选题成果。原secret_audit报告46 commits、3,236 distinct blobs、issues=[]；本批未重扫这些对象，不据此给当前仓库“无secret”结论，也没有查询当前远端删除或凭据。

本批新增检查确认141条archived_path的字节数/SHA预期均与冻结inventory相等。另发起过一个新的只读Git对象双向字节补核，因非TTY长时间无结果而Ctrl-C中断，exit130、stdout空、没有结果JSON；发现本clone是promisor/blob:none，缺对象查询可能隐式lazy fetch。本批没有141完成结果、没有重试或显式认证；是否曾补入对象不能由空输出判定。原脚本和取消边界见[实际记录](../../../../tools/evidence/source-migration-crosswalk/cancelled-byte-binding-attempt.json)。此不确定性不冒充PASS；后续若真需读缺对象，必须显式禁lazy fetch并报告缺项，不自动取远端。

4主源自己的原件字节/size/SHA均已精确验证，清单全部语义已读；这与141底层数学和新双向byte补核是不同任务。无须给这份历史清单增设今日远端/完整旧suite PASS前提，但也不能据清单认证那些未读材料。任何后续真正数学恢复仍应按source commit/path取原文、核独有内容和后续纠错，再单独receipt。

已知联系是[先有仓库恢复地图](../资料/仓库读取地图与退役双来源恢复--资料.md)的逐文件补全及[五类迁移](路径迁移的五类身份与退役例外--资源.md)的版本恢复背景，不是跨选题数学蕴含。本批未重做已done的BRANCHES/README/GROWTH等源，没有新增接受数学边。
'''
(D/'退役分支的逐项来源保全与恢复边界--资源.md').write_text(front('retired-branch-file-preservation-and-recovery-boundaries','退役分支的逐项来源保全与恢复边界','保全6分支全部files、141归档定位/预期hash和42省略项，分开历史操作声明、旧正祖先证据、新元数据匹配和取消的byte补核。',['research/branch_cleanup.json'])+body)
body=r'''## 两主源、全部语义与重新组织

JSON和生成Markdown是一份旧来源解释账本的两个表示。JSON version2含68个旧迁移/代码入口、606个新增来源、6个历史编辑判断及空sources数组；Markdown680行按保存角色排表，另有解释性外壳。两主源分别395,476和457,647字节，两冻结源各同字节；[原件与SHA](../../../../tools/evidence/source-migration-crosswalk/source-manifest.json)完整保留。

本批实际读完全部JSON字段和条目：68+606+6，包含每个source、provenance、rewritten_in、interpretation及两个额外archived_original_path；也读了Markdown全部非表格正文、全部表头和结构。所有680行的语义已逐条在JSON对应字段实读，新独立本地重构进一步确认**整份Markdown所有字节**与真实输入、外壳及行序完全一致；没有用先前的680行结构匹配冒充当时已经完成阅读。

本页把完全相同的interpretation文字提成187组，逐记录仍保所有路径/来源说明/去处/额外字段。相同组号只意味着文字重复，不表示源版本、数学对象、审查人或证明身份相同。它是一份历史说明资源；下文所有“已证”“独立”“实际读过”“取得附件”等未特别纠正者，都是原作者登记的历史断言，本账本不重新认证所链数学、外部论文、软件或审查独立性，也不额外done这些来源。

## 三种来源角色和不可相互替代的量词

68旧项必须与moved58+retired_code_paths10的原键集合相等；其中35历史/稿件及其他角色、输入/证书/冻结记录、测试/审计代码和规范实现分别登记，完整分组见附表。早期平方全局最大化、真实局部极小、有限菜单最小、精确实例最优、弱NP困难和一般位多项式不是一件事。两阶段设施主动原子客户NE与CAG每份全历史纯SPE也不是一个模型。

606新增源不虚构旧路径：用户贴文的出处提取、真正取得的ZIP/原附件、嵌入代码、尚未取得的链接包、团队发现器/冻结输入、内部陈述先行或读后稿、文献原版/作者稿/转换文件、无损gzip等各保来源。一个provenance写“当前会话授权”仅对其历史时点解释，不授权今天操作；scratch路径不是当前运行依赖，Git保存不是数学认证。

6项historical_editorial_assessment保存过去投稿/方向判断及关联背景，不把当时价值/优先权/期刊意见改写成现行证明，也不由当前后续结果反填当时已取得的材料。JSON两个archived_original_path是完整历史原交接入口的额外恢复定位，旧Markdown生成器不显示；本页明确保留。空sources数组没有额外隐含来源。

## 已实际核到的当前纠正：N031的弱iid桥

N031（原new_sources[30]）把dynamic_iid来源解释为背景iid势/KKT、租金债务、60客户局部失败，并写“intact weak global bridge”。这句话只能保为历史时点判断。以下已全文比较两个正式反例对象，不能把同一个局部正余量升级为普遍桥。

令$Z_m$为同一静态均分游戏的对称混合Nash独立抽样福利值，$W$为指定完整历史纯SPE实际覆盖。它不是真正静态minimax安全值$v_m$。60客户五人例有实际路径$(P,P,X0,Y0,Y1)$、收益$(12,12,10,12,12)$、$W=58,OPT_5=60$。实际节点PP与孩子PPX0的残余值为$97/3$、21，故第三人的10小于$(9/10)(97/3-21)=51/5$，局部漂移不足1/5；但全局$Z_5\le OPT_5$给$58-(9/10)Z_5\ge4$。因此**这个具体例子满足弱全局桥**，不意味着它对所有输入成立。完整有序策略、离轨比较与残余KKT见[实际前缀反例](../反例/实际前缀的独立同分布局部漂移--反例.md)。

普遍弱桥$W\ge(1-1/(2m))Z_m$已有另一完整SPE反族。为使本处的状态纠正自足，给出足以否定它的$m=20,J=100$机制：取两客户A块、$2(m-1)$客户B块、J个私有客户$c_j$互不交，目录为$A,B,Q_j=A\cup\{c_j\}$。根选A，所有其他非末位选B；末位在此前小主题行动数s=0时选Q1，s=1且唯一小主题为A时选B，s=1且唯一小主题为Qj时选另一个Q，s≥2时选B。该规则定义全部有序离轨重复历史。

全部动作比较按s分类：s≥2时B最终收益$2(m-1)/(m-s)>2$，小主题偏离至多$2/(s+1)+1\le5/3$；s=1且旧A时B得2，小动作得1或2；s=1且旧Qj时非末位B得$2(m-1)/(m-2)>2$，改A/同Q/其他Q只得1、3/2、2，末位另一Q与B并列2；s=0时非末位B与改A/改Q都得2，末位Q得3优于A的2和B的$2(m-1)/m$。根三类动作也都得2，所以完整规则是纯SPE，$W=2m$，$OPT_m=2m+\min(J,m-1)$。

定义$g_m(t)=m^{-1}\sum_{i=0}^{m-1}(1-t)^i$。静态对称Nash取$q_B=r^*,q_A=0,q_{Q_j}=(1-r^*)/J$，其中唯一内根由$U_B(r)=2(m-1)g_m(r)$与$U_Q(r)=2g_m(1-r)+g_m((1-r)/J)$相等确定；差连续严格递减且端点异号，未用A比Q严格差。于是$Z_m=mU_B(r^*)$。取$m=20,J=100,\bar r=25/27$：整数不等式$135\cdot25^{20}<29\cdot27^{20}$和Bernoulli界给$U_Q(\bar r)>5543/2700>513/250>U_B(\bar r)$，故$r^*<\bar r$。同时

$$\frac{39}{2}U_B(\bar r)-40=\frac{7-20007(2/27)^{20}}{500}>0.$$

因此$(39/40)Z_{20}>40=W$，严格否定普遍弱桥；该实例140客户、102主题，$OPT_{20}=59$而非140。另有固定102主题、每个$m\ge41$解析族；其完整常数证明、强桥八客户例及真实$v_m$比较见[强弱iid反例](../反例/独立同分布福利支付--反例.md)，本批没有重跑旧审计或另授外审/新颖性。这个反族仍满足half及真正安全值聚合：合法且不观察查询抽样的静态对手元组$B^{m-2},Q_1$，对查询$B,A,Q_1,$其他$Q_j$分别给收益2、1、3/2、2，故真正minimax值$v_m\le2=W/m$；同时$2W-OPT_m=2m-\min(J,m-1)>0$。不能把弱iid失败换成六人主目标反例。

原N031文字在原件及下方G组中保持不改；当前解释应读作“局部60客户例未反驳该弱桥；普遍桥后来已FALSE”。不覆写旧审计当时仍开放的事实，也不将本资源算一项新数学发现。

## 实际证据分层

新增[本地账本检查](../../../../tools/evidence/source-migration-crosswalk/inspect_ledger.py)只读本批字节和冻结inventory，不导入旧程序、不用Git或网络：完整457,647字节Markdown与独立重构一致；全部680记录/187精确文字组保留；所有source/解释路径在冻结清单存在；530条含64位SHA的provenance均有至少一token匹配对应冻结source SHA（gzip的容器与解压hash仍区分）。141归档预期size/hash也只与冻结元数据相等。不能将这些元数据结果写成全部源字节/论文正文/数学或软件PASS。

归档双向blob补核已取消且没有141完成结果，边界见[分支资源](退役分支的逐项来源保全与恢复边界--资源.md)。旧4tip祖先正证据复用，远端删除和secret scan未重新做。全部主源自身精确字节与语义完整性不依赖这个未完成的额外补核。

## 187组原解释文字

下面逐字保存所有不同interpretation；组内出现“current”“现行”“本轮”等指旧冻结账本语境。除了上面的明确当前纠正，不把它们转成今日真值。逐记录索引随后给完整source/provenance/去处，可精确区分同组内的版本和独立/读后顺序。

'''
for note in n['notes']:
 body+='<a id="historical-'+note['id'].lower()+'"></a>\n\n### '+note['id']+'\n\n'+note['text']+'\n\n'
body+='## 全部逐来源记录\n\n### E001–E068：旧迁移与代码入口\n\n| 记录 | 原路径 | preserved_at | rewritten_in | 原解释组 / 额外恢复定位 |\n| --- | --- | --- | --- | --- |\n'
for r in [r for r in n['records'] if r['group']=='entries']:
 note='['+r['historical_note_id']+'](#historical-'+r['historical_note_id'].lower()+')';extra='；archived_original_path='+code(r['archived_original_path']) if 'archived_original_path' in r else '';body+='| '+r['record_id']+' | '+code(r['original'])+' | '+code(r['preserved_at'])+' | '+code(r['rewritten_in'])+' | '+note+extra+' |\n'
body+='\n### N001–N606：新增来源\n\n| 记录 | source | provenance（原登记） | rewritten_in | 原解释组 |\n| --- | --- | --- | --- | --- |\n'
for r in [r for r in n['records'] if r['group']=='new_sources']:
 note='['+r['historical_note_id']+'](#historical-'+r['historical_note_id'].lower()+')';suffix='；**当前弱iid纠正见上文**' if r['index']==30 else '';body+='| '+r['record_id']+' | '+code(r['source'])+' | '+cell(r['provenance'])+' | '+code(r['rewritten_in'])+' | '+note+suffix+' |\n'
body+='\n### H001–H006：历史编辑判断\n\n所有kind均为`historical_editorial_assessment`，related_accounts为背景导航，不是证明前提。\n\n| 记录 | original | preserved_at | related_accounts | 原解释组 |\n| --- | --- | --- | --- | --- |\n'
for r in [r for r in n['records'] if r['group']=='historical_records']:
 note='['+r['historical_note_id']+'](#historical-'+r['historical_note_id'].lower()+')';body+='| '+r['record_id']+' | '+code(r['original'])+' | '+code(r['preserved_at'])+' | '+'；'.join(code(p) for p in r['related_accounts'])+' | '+note+' |\n'
body+=r'''
## 与先有资源和第三阶段的关系

[旧来源解释生成合同](旧路径解释账本的覆盖与生成合同--资源.md)讲算法的集合和输出约束，本页补全部实际登记语义、187组文字及当前N031校正；[迁移资源](路径迁移的五类身份与退役例外--资源.md)讲五字段身份，[逐文件分支恢复](退役分支的逐项来源保全与恢复边界--资源.md)讲原tip和141路由。已done的导航/程序源仅比较，不复领。

这些是恢复、来源、表示和有限检查关系，不是680条数学超边。当前第三阶段须实际读正式数学对象、共同条件和证据后逐边解释，允许孤立；不会因为源和新稿有对应、同组解释相同、历史字节保存或某行写“已审”而制造数学推导边。
'''
(D/'来源解释账本的历史语义与当前校正--资源.md').write_text(front('source-crosswalk-historical-semantics-and-current-correction','来源解释账本的历史语义与当前校正','完整保全680记录所有字段及187组解释，整份生成MD新字节绑定；将作者历史断言与元数据/当前弱iid反族校正分开，不额外done被链数学。',['research/source_crosswalk.json','research/source_crosswalk.md'])+body)
for p in D.glob('*.md'):print(p.name,len(p.read_bytes()))
