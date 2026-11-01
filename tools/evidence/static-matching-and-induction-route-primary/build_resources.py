from pathlib import Path
import json,hashlib

R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache'
S=C/'r3-static-matching-and-induction-route-primary';E=Path('tools/evidence/static-matching-and-induction-route-primary');W=Path('cleanup/workspaces/Boss4/r3-static-matching-and-induction-route-primary-next')
P1='archives/customer-attraction/state/反例/最优组合冻结匹配的一单位缺口--反例.md'
P2='archives/customer-attraction/state/资料/双尾推送与单色续局的版本接口--资料.md'
IDS=['1180cae0f024e775d79a','a7579960b289fff40c97','50c0718e3bf1ceb1d744','bb80664d0d0c61cbe335']
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):p=S/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
def source_row(i,p,role):
 x=inv[i];b=Path(p).read_bytes();assert len(b)==x['size'] and sha(b)==x['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
 q=E/role/i/x['path'];cp(p,q);return {**x,'preserved_path':str(q),'lines':len(b.splitlines()),'read_status':'all original fields and mathematical text actually read; no filename-only completion'}
mdmp=C/'learning-ex-next-readable-md/local-export-manifest.json';mdrows=json.loads(mdmp.read_text())['rows'];by={x['id']:Path(x['local_path']) for x in mdrows}
by[IDS[1]]=REPO/'archives/customer-attraction/tools/evidence/origin-retraction-workspace/related/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/static_matching_counterexample.json'
primary=[source_row(i,by[i],'original') for i in IDS];js(E/'source-manifest.json',primary);cp(mdmp,E/'actual-MD-supply-manifest.json')
relatedmp=C/'learning-fj-related-local-inputs/local-export-manifest.json';rraw=json.loads(relatedmp.read_text());related=[source_row(x['id'],x['local_path'],'related') for x in rraw['rows']];js(E/'related-source-manifest.json',related);cp(relatedmp,E/'actual-related-local-supply-manifest.json');cp(C/'local_blob_export.py',E/'authorized-local-export-helper.py.txt');js(E/'missing-local-inventory-bindings.json',[inv[x['id'] if isinstance(x,dict) else x] for x in rraw['missing']])
js(E/'derived-builder-recovery.json',{'calls':2,'failed_before_formal_body_write':1,'failure':'TypeError: unhashable type: dict when joining missing-row records to inventory','fix':'Use actual missing-row id field, not the whole record as dictionary key.','original_bytes_or_mathematical_program_changed':False,'new_math_runs':0,'note':'First packaging attempt stopped after primary/related exact copying, before any formal object write; corrected rerun is file construction only.'})
context_paths=[
'archives/customer-attraction/state/计算/弱匹配与分区查询的精确核验--计算.md',
'archives/customer-attraction/state/资源/最优补全账本与局部安全付款的命题分层--资源.md',
'archives/customer-attraction/state/候选/真实最优组合的净差匹配与共同付款--候选.md',
'archives/customer-attraction/state/障碍/最优组合真实偏离匹配不足--障碍.md',
'archives/customer-attraction/state/计算/来源回撤原程序与有序策略的精确重放--计算.md',
'archives/customer-attraction/state/资料/完整根菜单的联合势义务与排序边界--资料.md',
'archives/customer-attraction/state/反例/真实尾平稳均值的额外查询封顶--反例.md',
]
contexts=[]
for n in context_paths:
 b=(REPO/n).read_bytes();q=E/'context'/n;cp(REPO/n,q);contexts.append({'path':n,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_status':'full actual mathematical text read this FJ comparison'})
js(E/'context-manifest.json',contexts)
oldbase=REPO/'archives/customer-attraction/tools/evidence/origin-retraction-workspace';oldnames=['replay/execution.json','replay-input-manifest.json','replay/original.stdout.txt','replay/original.stderr.txt','replay/origin_retraction_exact_audit.json','original/research/workspaces/customer-attraction/R-3bc48d936f044f12b0fa743482ff5eb0/flow/audit_origin_retraction.py']
old=[]
for n in oldnames:
 b=(oldbase/n).read_bytes();q=E/'reused-evidence'/n;cp(oldbase/n,q);old.append({'path':str(q),'parent_path':str(oldbase.relative_to(REPO)/n),'bytes':len(b),'sha256':sha(b)})
js(E/'reused-evidence-manifest.json',old)
d=json.loads(by[IDS[1]].read_text());acts={tuple(x['history']):x['action'] for x in d['certificate']['actions']}
customers='\n'.join('| '+','.join(map(str,x['topics']))+' | '+str(x['multiplicity'])+' |' for x in d['instance']['customers'])
third='\n'.join('| '+str(a)+' | '+' | '.join(str(acts[a,b]) for b in range(6))+' |' for a in range(6))
last='\n'.join('| '+str(a)+','+str(b)+' | '+' | '.join(str(acts[a,b,c]) for c in range(6))+' |' for a in range(6) for b in range(6))
match='\n'.join('| '+','.join(map(str,x['target']))+' | '+x['query']+' |' for x in d['all_assignments'])
p1=r'''---
id: "customer-attraction/optimal-static-assignment-one-unit-gap"
kind: "counterexample"
type_tag: "反例"
title: "最优组合冻结匹配的一单位缺口"
status: "complete-52-unit-full-policy-certificate; old-same-SHA-SPE-validation-reused; no-new-run"
summary: "52单位客户四人六主题的完整259节点SPE有W47、唯一最优支持0145覆盖52，全部24冻结匹配12个48和12个293/6；保正确条件弱化、真实V及分区R区别。"
legacy_ids: ["B10-STATIC-OPTIMAL-ASSIGNMENT-NO-v1"]
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/optimal_static_matching_counterexample.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/optimal_static_matching_counterexample.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/static_matching_counterexample.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/static_matching_counterexample.json"
---

# 最优组合冻结匹配的一单位缺口

## 精确被反驳的量词及模型

有限单位客户、四名单位权提供者、有限非空共同目录。提供者依次观察全部有序历史选一主题，客户在最终覆盖者间均分。完整纯SPE允许重复、离轨历史和平局；本实例六主题互异且非空，不删掉普遍模型允许的空主题/零客户情形。

固定实际有序终局S=(S_1,…,S_m)，客户实际覆盖数c_x。把一个达到OPT_m的长度m最优元组T（保重复出现）匹配给实际角色，定义冻结查询
\[
F_i(T)=\sum_{x\in T}\frac1{c_x+1-\mathbf1_{x\in S_i}},\qquad Q(\pi)=\sum_iF_i(T_{\pi(i)}).\tag{FROZEN}
\]
分母只在x∈T处使用，始终正。该式固定除角色i外的实际行动，**不**沿改变后历史调用原SPE回复。被否定的强桥为：每个实例、每份完整纯SPE，存在某个达到OPT_m的元组和某个匹配使Q≤W。本例同时量化所有最优元组和全部匹配，不只展示一个坏选择。真实偏离V、一次收费分区R以及聚合安全值是别的对象。

[4111B主稿](../../../../tools/evidence/static-matching-and-induction-route-primary/original/1180cae0f024e775d79a/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/optimal_static_matching_counterexample.md)及[32574B全证书](../../../../tools/evidence/static-matching-and-induction-route-primary/original/a7579960b289fff40c97/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/static_matching_counterexample.json)全部实际阅读，包括JSON十个顶层字段、两certificate字段、259个action及24项匹配。原件冻结不改；以下策略表是原完整动作的无损展示。

## 52单位客户及全部策略

标签0,…,5。每行是互不相交的单位客户块，左列恰为可接受标签全集；重数是多个不同单位客户，不是客户权重。

| 全部可接受标签 | 单位客户数 |
| --- | ---: |
CUSTOMERS

合计52。根规定3；第二人在首动作0,…,5后依次规定(2,0,3,3,2,0)。第三人在有序历史(a,b)后规定为：

| a\b | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- | --- |
THIRD

末位在有序历史(a,b,c)后规定为下表的c列。它覆盖所有216个末位节点，保同计数不同顺序和全部离轨历史。

| (a,b)\c | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- | --- |
LAST

根、6个第二节点、36个第三节点及216末节点，共259节点，原JSON各有且只有一个动作。实际路径(3,3,2,2)，terminal_counts=(0,0,2,2,0,0)只记录标签次数，不能替代完整有序策略。四人各47/4，W=47。

完整SPE证书的定义级核验是：对每层i=0,…,3、每个h∈{0,…,5}^i，沿同一表完成z(h)；对每个a∈{0,…,5}比较u_i(z(h))≥u_i(z(h,a))。客户利润按本页单位表和终局覆盖者数精确求和。既有同SHA[原来源回撤审计](../计算/来源回撤原程序与有序策略的精确重放--计算.md)已经一次执行成功，涵盖本输入全部259节点1554项含自身比较，即1295项非自身比较；该程序的真实后继未冻结。本批全文读原10829B代码并核旧输入/执行/输出绑定，**不再执行该程序**。

这份旧origin代码会重算本输入SPE、W和目标支持的最优覆盖，但不读取或认证本JSON的全部all_assignments/unique_optimal_supports字段。因此下面的唯一最优性和全部冻结匹配另给直接论证，不把旧run范围扩大。

## 唯一最优支持：不靠忽略重复主题

支持{0,1,4,5}触及上表每一行，覆盖全部52，所以OPT_4=52。任何达到52的组合必须覆盖仅喜欢1、仅喜欢4、仅喜欢5的三个正重数块，故必须含1、4、5。至多剩一个槽；为了同时覆盖{0,2}和{0,3}两块，此槽必须为0。故唯一最优支持正是{0,1,4,5}，四槽各一次，重复/少于四主题不可能得到52。这个解析论证也说明所有最优有序终局恰为四主题的24个排列。

## 全部24匹配为何只有两个值

由(FROZEN)逐客户相加给下表。前两角色原主题3、后两原主题2，冻结查询中行相同来自终局行动对称，不是对完整策略的匿名/平局假设。

| 实际位置i | 查询0 | 查询1 | 查询4 | 查询5 |
| --- | ---: | ---: | ---: | ---: |
| 1 | 51/4 | 38/3 | 51/4 | 71/6 |
| 2 | 51/4 | 38/3 | 51/4 | 71/6 |
| 3 | 47/4 | 35/3 | 47/4 | 35/3 |
| 4 | 47/4 | 35/3 | 47/4 | 35/3 |

以全部主题都用后一行价格作基线，和为47/4+35/3+47/4+35/3=281/6。将某目标交给前两槽之一，0/1/4各增加1，5增加1/6。若5在前两槽，两个增量为1和1/6，得Q=48；否则两个增量均1，得Q=293/6。各类恰2·3!=12个匹配。这是对全部存在量词的解析穷尽；不需要信任JSON排序或求解器最优性。原24项完整为：

| 按实际位置1,2,3,4分配的目标 | Q |
| --- | ---: |
MATCH

例如(0,5,1,4)给51/4+71/6+35/3+47/4=48。所有Q≥48>47=W，最小严格缺口1。因此强桥被完整SPE否定；2W−OPT_4=94−52=42>0，绝非half反例。

## 无条件客户账目与没有被本例否定的弱化

对任意m≥1、任意实际终局及最优m主题匹配，设O、C为比较/实际并集。每个O\C客户至少出现在一个查询中且无其它实际覆盖者，故对Q贡献至少1；每个O∩C客户至少在一个查询中被至多m位分享，故至少贡献1/m。因此
\[
Q\ge |O\setminus C|+|O\cap C|/m,\qquad
\operatorname{OPT}_m\le Q+(1-1/m)W.\tag{COVER}
\]
后一式用|O∩C|≤W，零客户也成立。若强桥Q≤W成立会给OPT≤(2−1/m)W；但只要某最优匹配有Q≤(1+1/m)W，就已由(COVER)推出half。这里48<235/4=(1+1/4)47，**本例没有反驳这个较弱冻结预算**，也不据本例宣称它一般成立。

[弱匹配与分区精确核验](../计算/弱匹配与分区查询的精确核验--计算.md)对同52客户另得minR=263/12、均值R815/36；R只给每个最优客户选一次收费owner，和重复整主题Q不同。一般PFR-OPT存在R≤W已由[十四客户完整SPE](唯一最优分区冻结查询的十四客户反例--反例.md)另行否定，不能因本52输入的R小就恢复普遍分区桥。真实V沿改变前缀的原策略继续；[净差真实匹配](../候选/真实最优组合的净差匹配与共同付款--候选.md)也不被此冻结Q反例自动否定。

## 发现、独审与当前证据身份

主稿记search.py为集合值逆向归纳、全部最优组合/匹配的有限探针；两批随机样本及14既有实例未分离只是历史有限记录。cone_attack.py固定全历史策略后用全部真实IC行约束客户重数，强制指定四支持唯一最优和全部24个Q>W；seed1022第50个策略实例给浮点候选。recover_integer.py在该候选正支撑求整数重数、要求缺口≥1并最小化客户总数。原浮点LP/整数发现点仅为发现过程，不需要求解器全局最优才能成立本反例；也不认证52全局最小。

必要比较[2869B独审原稿](../../../../tools/evidence/static-matching-and-induction-route-primary/related/a78d96dc6f303010aea7/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/direct_global/static_matching_counterexample_independent_review.md)全文已读；它报告标准库独立实现、展开52客户、1554比较中285平局1269严格，并枚举1296有序终局。但其4852B audit代码与3789B同名JSON本地缺blob，本批未读或执行，不把它当新复现或用285扩大当前old-origin输出字段；原作者“独审无fatal”有其历史身份。

实际复用的origin成功代码SHA23fa930019f22e9e12fd99859e37a250485d7ae740e9946b409527c80ccf2c79，本输入SHA9e7cf1437a7b03fe89d843d4ae20efa3c6a4137373098ed1220d4370656a5245，旧stdout/报告SHA6488b65a790c2af4bab4f0019a10f6cd4f784d6318fd12517232ba6cfd077cd9；0.368130922秒exit0是旧实际执行，不是本批新增耗时。其另外五fixture不成为本批新样本。新数学CLI、SPE重演、匹配扫描或优化器均0；本页新增整理是完整策略展示和两项解析穷尽。[完整证据](../../../../tools/evidence/static-matching-and-induction-route-primary/README.md)保原件/哈希、真实读取及复用边界，无外审或新颖性认证。
'''
for k,v in [('CUSTOMERS',customers),('THIRD',third),('LAST',last),('MATCH',match)]:p1=p1.replace(k,v)
put(P1,p1)
p2=r'''---
id: "customer-attraction/two-tail-and-monochromatic-interface-version-routes"
kind: "resource"
type_tag: "资料"
title: "双尾推送与单色续局的版本接口"
status: "historical-route-resources-completely-preserved; individual-WP-FM-extra-one-refuted; other-contracts-separated"
summary: "完整保两README的每个稿件/程序角色、任意背景r2正面定理、tail-price反族、单色税与静态势边界，纠正旧一般个体菜单/extra-one开放时态，不把路由或有限LP当证明。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/induction/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/induction/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/tree/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/tree/README.md"
---

# 双尾推送与单色续局的版本接口

## 两个不同入口及共同当前模型

[1406B归纳README](../../../../tools/evidence/static-matching-and-induction-route-primary/original/50c0718e3bf1ceb1d744/research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/induction/README.md)和[1302B树README](../../../../tools/evidence/static-matching-and-induction-route-primary/original/bb80664d0d0c61cbe335/research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/tree/README.md)各全文实读。它们同属原Boss10个人备份但内容、身份、源ID不同，不能按相同文件名去重。两冻结提交各自同SHA；“下一步”“停止同模板样本”是当时研究路线，不切换当前Boss4清洗身份、不重开实验。旧一般half OPEN保时态；当前六人每份完整纯SPE half仍未由本批解决，五人已有独立正式定理。

模型为有限单位客户/共同非空目录，顺序完整有序历史纯SPE，保空主题、重复、零客户及任意离轨平局。固定节点过去客户负载b≥0、余r≥1，强制当前B后同一原策略完成Z(B)=(B,Y_B)，Y_B长度r−1；d_B当前在该枝利润，u=max_B d_B。对查询T与列随机化独立，定义
\[
K_{T,B}=\sum_{x\in T}\frac1{b_x+1+c_x(Z(B))},\quad
D(p)=\sum_Bp_Bd_B,\quad C(p)=p^TKp,\quad
M_{full}=\min_Q\max_T(KQ)_T.\tag{MENU}
\]
完整列含当前根自身，恰r个竞争槽。r−1真实尾菜单、所有合法静态r槽、指定分数均值、全路径菜单不能互换。

## 每条原入口的数学角色和真值

| 原入口 | 原文实际内容/用途 | 当前处置与区别 |
| --- | --- | --- |
| induction/two_player_full_terminal_pushforward.md | B10-TWO-PLAYER-INTEGER-PUSH-SHARP-v1；任意背景恰两人、任意p，保存真实末位BR平均slack及锐正曲率；原内部root重构/盲审通过 | 正面r2推送仍有效，见[完整锐式](../引理/末位真实回复推送的锐曲率与双分支式--引理.md)。不能推广为r≥3或所有SPE叶静态PNE。 |
| induction/full_root_menu_mixed_obligations.md | 完整r槽minimax与META充分路线、r2纯防御短证、791势下降/348高插入二环、根+末位BR非SPE模板 | [完整菜单义务](完整根菜单的联合势义务与排序边界--资料.md)保恒等式、PAY条件与证据；逐位置Mfull普遍合同现已被银行族否定，旧OPEN失效。791原JSON缺，现348真实证据不冒认证791。 |
| induction/tail_price_strengthening_counterfamily.md | 空背景两人完整SPE反加强2C≤D+v(q_tail)；本族k=13,t=1/3，15客户14主题、各根收益1、缺口1/351；p非META | [两类价格尺度障碍](../反例/后继边际价格付款的两类尺度障碍--反例.md)保完整解析域；r2原强式及此例Mfull未被它否定，不能将这里的非META p称META反例。原“独立检查待安排”只属当时状态。 |
| tree/virtual_adjacency_handoff.md | 单色真实后缀虚拟相邻税候选、r1三比较、频次筛选重复性、全B静态PNE全局势引理 | 未用有限阴性样本认证一般VA；同背景静态势引理独立有效，不能控制改前缀后的真实多玩家SPE。必要3843B原文全文比较，见下一节。 |
| tree/virtual_tax_probe.py | 固定完整策略锥/浮点递归LP探索，未冻结完整运行证据 | 实际本地缺3296B程序，本批没有读源码或运行；只保README的真实资源角色，不认证浮点样本或精确排除。 |
| tree/full_terminal_menu_interface.md | 完整r槽minimax、旧r−1尾菜单区别、381旧例有理原始/对偶核对 | 必要4790B全文已读，顶部2026-10-25已明示FM反驳，后段2026-10-22 OPEN是历史；381输入/原audit未取得，本批仅保存作者数值主张，不冒重算。 |

## r2真定理、一般个体合同反驳与仍有效的条件蕴含

有限零和minimax使Mfull≤u等价于：每个行分布p，存在某纯列B使Σ_Tp_TK_(T,B)≤u。固定p可取不同B；这不要求同一个纯列封所有p。对每p都成立的强式D(p)≥C(p)，因D(p)≤u，可取Q=p再用minimax推出Mfull≤u。r=1、r=2的强式有效；r≥3有真实完整SPE令D<C。仅一个p的D<C不自动反Mfull，也不自动反弱式C≤u；[34客户原例](../反例/空根稀释的强推送失败与弱桥范围--反例.md)就有D<C<u。

但是普遍弱式“每个p都有C(p)≤u”和普遍逐位置完整菜单都已由[银行完整菜单反例](../反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md)否定，不再保持本README的旧OPEN。原整数extra-one也不是尚无反例：银行m4根u=4/3<19/14=t5≤v5，Jensen给分数均值门槛t≤真正整数混合安全值v。它是零**过去背景**根，不需空主题。源的自由静态r槽逐人合同u≥v_(r+1)(b)因而失败；不否定另一个聚合W≥m v_m，也不直接解决FREE-ROOT或half。

静态v_(m+1)(0)≥OPT_m/(2m)及“若各actual节点Mfull≤u则half”的条件推导仍正确。个体前提假不等于静态比较假；[合法前缀完整证明](../引理/合法前缀的静态额外槽预算与条件归约--引理.md)保k+r=m及两份m计数预算。不能用过去README的OPEN抹掉后来反例，也不能用后来反例追改旧文当时的读取/审查事实。

381作者记录只说明一个旧强反例不分离FM：r3/6主题/381客户，旧p给D141/10<C6879/400、u137，报Mfull239604/3169、列Q=(1016,1273,0,0,0,880)/3169、行对偶p=(1525,9362,0,0,0,4958)/15845，纯列cap251/3<u。输入及原audit当前未取得，不能把上述数字称本批定义级认证，更不能替代已成熟34例或银行反例。全p充分条件2C≤D+max_T(Kp)_T、低值对称Nash路线也须各自量词；META充分性不等于minimax必要性。

## 单色税的实际义务和可独立使用的静态势引理

必要比较[单色3843B全文](../../../../tools/evidence/static-matching-and-induction-route-primary/related/276852a177c7326ea276/research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/tree/virtual_adjacency_handoff.md)定义实际后缀A B^r，r≥1，
\[
u_A=\sum_{x\in A}\frac1{b_x+1+r\mathbf1_B(x)},\quad
q(T)=\sum_{x\in T}\frac1{b_x+1+r\mathbf1_B(x)},\quad
\tau_A=\sum_{x\in A\setminus B}\frac1{(b_x+1)(b_x+2)}.
\]
VA(r)要所有T满足q(T)≤u_A+τ_A；q冻结B^r并非真实偏离。r1令f(X)=Σ_X1/(b+1)、g(X,Y)=Σ_(X∩Y)1/[(b+1)(b+2)]、U=f−g，F为T后的真末位回复。三真实slack分别s1=U(A,B)−U(T,F)、s2=U(F,T)−U(B,T)、s3=U(B,A)−U(F,A)，均≥0，精确
\[
u_A+\tau_A-U(T,B)=s1+s2+s3+
\sum_{x\in A\setminus F}\frac1{(b_x+1)(b_x+2)}\ge0.
\]
r≥2的多个后继不能直接合成一个目录行动。原稿报小目录完整终局集递归和固定策略重数LP阴性，但浮点、无完整冻结证书；本批没有证明/反驳一般VA。两主题频次筛选l(2k+1)≥k²−1来自最后A直接改B及末位预算，原稿明确与R31旧Claim B完全重复，不新冠一条定理。

同背景的有效独立引理是：若r名同时静态玩家全选B为PNE，则B^r在所有r主题元组中全局最大化Φ_b(Z)=Σ_xΣ_(j=1)^(c_x(Z))1/(b_x+j)，实b≥0亦可。PNE给每T
\[
\sum_{x\in T\setminus B}\frac1{b_x+1}
\le\sum_{x\in B\setminus T}\frac1{b_x+r}.
\]
将任意r主题Z的各槽相加，左为B外Σ d_x/(b_x+1)，右为B内Σ(r−d_x)/(b_x+r)。从B^r到Z，势在B外增加≤左，B内减少≥右，故Φ_b(Z)≤Φ_b(B^r)。一个实际完整SPE单色后缀的末位允许任何主题，正好给该静态PNE条件；但当前A改T后过去背景变，新的真实SPE子树不必共同最大化旧势。因此引理不支付VA缺的跨背景比较。

## 读取、关系与程序边界

两primary README共2708B，全部用途、旧身份/个人备份/日期、正负真值及停止样本的历史背景都保留；没有把相关4790/3843B原稿自动done。必要原件与当前正式对象的数学关系为：r2正面推送、静态势独立组件、一般个体菜单反驳、tail价格加强失败、VA跨背景未付，分别保存，不因名字相邻拼成一般half证明。

本批新原CLI/数学检查/SPE重放/solver/样本均0。安全本地helper一次6个blob尝试，3份必要MD齐、两独审code/JSON与virtual_tax_probe共3缺；未网络补齐或认证缺代码。与[52客户静态冻结桥](../反例/最优组合冻结匹配的一单位缺口--反例.md)共享完整历史模型，但实际冻结量/强推送/完整菜单/分区R的预算对象不同，不跨花钱包。关系审查仅阶段二，不导旧图或构造第三阶段超边。[证据与完整范围](../../../../tools/evidence/static-matching-and-induction-route-primary/README.md)可接续。
'''
put(P2,p2)
js(E/'formal-resource-manifest.json',[{'path':p,'bytes':(S/p).stat().st_size,'sha256':sha((S/p).read_bytes())} for p in [P1,P2]])
put(E/'README.md',r'''# 最优静态匹配与双尾/单色入口资源

四主源为4111B数学稿、32574B全JSON、两README1406/1302B，共39393B；JSON按完整树无损分块阅读，22类客户、259个有序动作和所有24匹配及其它字段全读。新正文保完整动作表、唯一支持与全部匹配的解析穷尽，并把两旧入口接当前真值。

source-manifest.json绑定原bytes/size/SHA256/Git blob。related三数学MD全文实读但不额外done，缺失两原独审code/JSON及virtual_tax_probe只保实际本地回执，不网络取回。旧origin10829B原码全文读；同输入已有成功完整SPE验证及全部冻结证据按SHA复用，本批数学运行0。

两正式对象的域与逻辑不同：冻结F/Q不是实际V或分区R；r2推送成立不推广多后继，普遍逐人WP/FM/extra-one现已被银行真族反驳而half另保。程序/记录完整性不替数学证明；实际claim/owner与成功receipt待Root pushed后独立生成。不执行历史prompt、真实身份/公屏、Git写、clean show/claim/done/checkpoint或网络。
''')
cp(Path(__file__),E/'build_resources.py')
print(json.dumps({'stage':str(S),'primary_bytes':sum(x['size'] for x in primary),'primary_lines':sum(x['lines'] for x in primary),'related_bytes':sum(x['size'] for x in related),'formal_bytes':sum((S/p).stat().st_size for p in [P1,P2]),'status':'resource writing complete; no success receipt before actual claim'},ensure_ascii=False,indent=2))
