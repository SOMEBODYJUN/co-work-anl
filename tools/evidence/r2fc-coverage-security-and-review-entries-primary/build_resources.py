from pathlib import Path
import json,hashlib
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';S=C/'r3-r2fc-coverage-security-and-review-entries-primary';E=Path('tools/evidence/r2fc-coverage-security-and-review-entries-primary');W=Path('cleanup/workspaces/Boss4/r3-r2fc-coverage-security-and-review-entries-primary-next');P='archives/customer-attraction/state/资源/覆盖矩与扩大势入口的模型和独审合同--资源.md';IDS=['7ff889463b6b3535ac58','0d9f1d7b2cb2dafd4296','44357124372fb651a98f']
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):p=S/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
mp=C/'learning-next-r2fc-entries-local/local-export-manifest.json';raw=json.loads(mp.read_text());rows=[]
for x in raw['rows']:
 b=Path(x['local_path']).read_bytes();v=inv[x['id']];assert x['id'] in IDS and len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];q=E/'original'/x['id']/x['path'];cp(x['local_path'],q);rows.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'read_status':'first full actual mathematical reading GE; earlier GB byteavailability only'})
js(E/'source-manifest.json',rows);cp(mp,E/'actual-root-supplied-primary-manifest.json');cp(C/'learning-gb-next-readable-README/local-export-manifest.json',E/'earlier-byteavailability-only-manifest.json')
mp=C/'learning-ge-related-review-and-audit-inputs/local-export-manifest.json';raw=json.loads(mp.read_text());related=[]
for x in raw['rows']:
 b=Path(x['local_path']).read_bytes();v=inv[x['id']];assert len(b)==v['size'] and sha(b)==v['sha256'];q=E/'related'/x['id']/x['path'];cp(x['local_path'],q);related.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'read_status':'all mathematical text/sections fully read GE, related only no extra done'})
js(E/'related-source-manifest.json',related);cp(mp,E/'actual-related-local-supply-manifest.json');cp(C/'local_blob_export.py',E/'authorized-local-export-helper.py.txt');js(E/'missing-code-inventory-bindings.json',[inv[x['id']] for x in raw['missing']])
names=[
'archives/customer-attraction/state/定理/固定人数完整策略的覆盖矩表示--定理.md',
'archives/customer-attraction/state/定理/覆盖矩锥极射线与自适应类型稀疏化--定理.md',
'archives/customer-attraction/state/障碍/精确保留激励数值的折叠与末层方向边界--障碍.md',
'archives/customer-attraction/state/障碍/覆盖矩锚预算与真子目录的全局缺口--障碍.md',
'archives/customer-attraction/state/障碍/单调递减边际势的强安全聚合障碍--障碍.md',
'archives/customer-attraction/state/计算/覆盖矩表示与非负实现的精确核验--计算.md',
'archives/customer-attraction/state/资源/覆盖矩与势支付工作台的状态校正--资源.md',
'archives/customer-attraction/state/反例/五客户无拥挤SPE负载桥障碍--反例.md',
'archives/customer-attraction/state/反例/三人碰撞自由族福利障碍--反例.md',
'archives/customer-attraction/state/资源/无拥挤完整均衡族原稿与有限探索的准确范围--资源.md',
]
contexts=[]
for n in names:
 b=(REPO/n).read_bytes();q=E/'context'/n;cp(REPO/n,q);contexts.append({'path':n,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_status':'full actual current mathematical object text read GE; snapshot does not assert its pending/shared Git publication status'})
js(E/'context-manifest.json',contexts)
canonical=REPO/'archives/customer-attraction/tools/evidence/coverage-moment-geometry';cp(canonical/'manifest.json',E/'canonical-coverage-audit-original-manifest.json');report=(canonical/'original/audit.json').read_bytes();code=(canonical/'original/audit.py').read_bytes();v=inv['237a9c14a68cbe08a526'];j=inv['10b27e972bf58a53c84e'];assert len(report)==j['size'] and sha(report)==j['sha256'];js(E/'audit-version-binding.json',{'workspace_program':v,'canonical_program_observed_bytes':len(code),'canonical_program_observed_sha256':sha(code),'same_program_bytes':sha(code)==v['sha256'],'workspace_frozen_report':j,'canonical_report_observed_bytes':len(report),'canonical_report_observed_sha256':sha(report),'same_report_size_SHA_bound':True,'comparison_method':'workspace frozen inventory size/SHA versus actual canonical bytes; workspace report not newly exported or full-field read','execution_scope':'published old11313canonical program replay only; missing11506workspace code not read/run/identical certified; no new execution','report_read_scope':'bytehash comparison and existing full computation object; not a claim to newly read every raw report field'})
aliases=[]
for x in related:
 same=[v for v in inv.values() if v['sha256']==x['sha256'] and v['id']!=x['id']]
 for v in same:
  p=REPO/'cleanup/progress'/f"{v['id']}.json";pr=json.loads(p.read_text()) if p.exists() else None;aliases.append({'related_source_id':x['id'],'sameSHA':x['sha256'],'canonical_source':v,'canonical_progress':pr,'role':'exact original-byte duplicate identity, not extra review person or new implementation'})
js(E/'independent-review-original-aliases.json',aliases)
body=r'''---
id: "customer-attraction/coverage-moment-and-generalized-potential-entry-model-review-contracts"
kind: "resource"
type_tag: "资源"
title: "覆盖矩与扩大势入口的模型和独审合同"
status: "three-entry-sources-completely-reviewed; CR-PM-and-DR-domains-separated; original-audit-version-gaps-retained"
summary: "完整保三README的覆盖矩CR1…6、PM1…3、独审时间/域与扩大DR边界；补support预算混合式的纯对角前提，区分11506工作码与11313旧成功实现及同字节报告，0新数学运行。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/coverage_representation/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/coverage_representation/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/independent_mechanism/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/independent_mechanism/README.md"
---

# 覆盖矩与扩大势入口的模型和独审合同

## 三份不同入口及当前问题

[安全入口1506B](../../../../tools/evidence/r2fc-coverage-security-and-review-entries-primary/original/7ff889463b6b3535ac58/research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/README.md)、[覆盖表示入口2886B](../../../../tools/evidence/r2fc-coverage-security-and-review-entries-primary/original/0d9f1d7b2cb2dafd4296/research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/coverage_representation/README.md)、[独立机制入口1752B](../../../../tools/evidence/r2fc-coverage-security-and-review-entries-primary/original/44357124372fb651a98f/research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/independent_mechanism/README.md)在GE首次完整语义实读；GB只核6144B可用字节。原Boss7/独立子研究员、2026-10-21、根统一checkpoint、不自行Git/外发等作历史，不切换当前Boss4、不发送原消息或执行旧研究命令。两个冻结提交各自同SHA，不按同名README重复删除。

原CAG是有限单位客户/单位提供者、共同有限非空主题目录、完整有序历史纯SPE，保空主题、同覆盖标签、重复、零客户和全部离轨平局。六人half仍未由这些入口解决；原任意人数OPEN不能覆盖现在另有五人定理。真正强/弱聚合W≥m v_m和W≥(m−1/2)v_m有自己的静态安全值合同，不能以以下扩大模型反驳。

## 覆盖矩六项：线性空间与非负合同

令p≥1个标签、m≥1，全部非空形式兴趣类型B⊆[p]，k_T(B)=1_(T∩B≠空)，V_m=span{k_T:1≤|T|≤min(m,p)}，d=Σ_(j≤min(m,p))C(p,j)。完整形式σ不必预先SPE，在每个有序历史有动作；Γ是真正改变行动后沿同一策略完成的收益差。矩向量y=M_m w，真实客户要求w≥0，像锥K_m=cone{v_B}，其中(v_B)_T=k_T(B)。

| 身份及原文件角色 | 精确结论和接续范围 |
| --- | --- |
| CR1 / coverage_moment_geometry | 所有m人终局收益行span恰V_m，维d；收益可需负覆盖系数，不能把势的正展开照搬到收益。 |
| CR2 / 同稿、成文独审 | 对每份完整形式σ，末层及全树Γ的signed span都为{f∈V_m:f([p])=0}，维d−1；加根覆盖恢复V_m。取每计数一个代表只是span证明，不匿名化σ。 |
| CR3 / 同稿、独审域修订 | m≥2每非空类型列为不同极射线，p≥2才以非零泛函暴露真面；m1只有p个单点极射线，p1单列平凡。指数列障碍不排多项式facet/扩展表述。 |
| CR4 / 精确OPT外折叠障碍 | m≥2、p≥m+1不交单客户的完整fresh策略有W=OPT=m；保全部Γ数值及W迫保单/双矩，非负性迫OPT外p−m单例仍在。只保SPE不等式则可改全兴趣客户，合同不同。 |
| CR5 / 自适应稀疏化 | 每份非负有理输入可在其正支持内核消元到≤d类型，清分母同倍放大全部数值与比率；类型集合依输入，不是固定删列基或有限判定算法。m≥2对称差2C(ab)−C(a)−C(b)保不同覆盖。 |
| CR6 / 后续方向边界 | m≥2，前m−1位处处空、末位fresh单例的完整形式σ，所有末层IC成立而早期0可改fresh得1，W1/OPTm；明确非SPE。m≥3的half失败只属于这个放松，不是原目标反例。 |

三类约束不能混合：signed span允许负系数；非负真实比较行锥要求λ≥0；真实客户矩又要求y∈K_m。坐标全非负不够，例如单/双矩(1,1,3)不是真客户。限制到某实例正类型域还可能失去全兴趣坐标，不能照搬全域余维一。lineality、暴露术语、不同覆盖严格类及m1/p1都由独审明确处理。

全部自足证明见[表示定理](../定理/固定人数完整策略的覆盖矩表示--定理.md)、[实现锥/稀疏化](../定理/覆盖矩锥极射线与自适应类型稀疏化--定理.md)、[精确折叠与末层边界](../障碍/精确保留激励数值的折叠与末层方向边界--障碍.md)。原入口说若只保同σ的SPE不等式而不保每行数值，CR4障碍不适用，是承重限制，不能删掉。

来源R7e…/full_tree_dual旧消息所称coverage-span稿未被该作者找到，当时实际目录是收益图/SCC稿；本批也不凭消息认证未取得资产。共享mobius_compiler已有Boolean势双Möbius反演、正偏置编译/固定人数匿名势约束；这里的创新身份至多是原内部研究主张，不认证外部新颖性。固定人数层的表示不等于全Boolean势表唯一反演。

## 正矩锚族：全局预算不能被局部合法性替代

positive_moment_locality给PM1…3，固定m2但标签无界。anchor z、n≥2个变量I，b_n=⌊n²/4⌋，全局预算
\[
L(y)=b_n y_z-\sum_{\{i,j\}\subseteq I}(2y_{ij}-y_i-y_j)
+(n-1)\sum_{i\in I}(y_{zi}-y_z)
\]
在类型列上，若k=|B∩I|、s=1_(z∈B)，值为s0时k(k−1)，s1时b_n−k(n−k)，均≥0，所以L∈K_2*。

PM2取任意r≥1、n2r+1变量加anchor，令y_z=y_zi=1、y_i=1/2、y_ij=(3r−1)/[2(2r−1)]。删变量时均匀r子集并含anchor给真客户；删anchor时r层总质量α=n/[2(2r−1)]、r+1层总质量β=n(r−1)/[2(r+1)(2r−1)]给真客户。总客户数不是额外矩坐标，不要求α+β=1。每个真子目录合法，全局却L(y)=−r/(2r−1)<0，所以不是合法CAG或SPE输入。PM3由同一y见任何真子目录有效预算的非负和都不能生成L。

[锚预算完整证明](../障碍/覆盖矩锚预算与真子目录的全局缺口--障碍.md)保存所有局部模型和任意r代数；不从r≤6样本外推。README报告audit_positive_moment_locality枚举r1…6的21834非空类型及两局部模型502单/双矩，属原作者有限实现声明，本批5238B原码缺，未执行或新认证这些计数。

对固定σ、比较支持O(≤m标签)，有限锥对偶准确要求
\[
2e_{R_\sigma}-e_O=G_\sigma^T\lambda+a,\qquad
\lambda\ge0,\quad a\in K_m^*.
\]
Rσ是actual支持，Gσ是覆盖坐标下真实IC行。这是给定σ的证书形式，未证明所有σ都有这样的λ；PM1仅供应可试全局正余项a，不付真实跨分支乘子。原“停止再扩类似局部族、回真实σ”只保研究历史，不发新研究指令。

## CAG的support预算与扩大DR边界

对合法CAG客户负载c_x(q)，Φ(q)=Σ_xH_(c_x(q))，Φ空0，删除一个覆盖者使势减1/c。因此逐客户相加得
\[
|q|\Phi(q)=W(\operatorname{supp}q)+\sum_aq_a\Phi(q-e_a).\tag{SUPPORT}
\]
同一support重复行动不改变总收益W。纯重复a给2Φ(2a)=3Φ(a)。将总收益P(2a+b)=P(a+b)展开为3Φ(2a+b)−2Φ(a+b)−Φ(2a)=2Φ(a+b)−Φ(a)−Φ(b)，再用这个纯对角关系，才得
\[
6\Phi(2a+b)=\Phi(a)-2\Phi(b)+8\Phi(a+b).\tag{REPEAT}
\]
所以README的三人混合式有CAG纯对角预算这个共同前提，不能将它孤立说成任意势模型的充分判据。给定合法客户覆盖W时(SUPPORT)按人数递推唯一确定Φ；任意support函数即使满足递推，也还缺真实非负覆盖实现。

[扩大单调DR势的完整反例](../障碍/单调递减边际势的强安全聚合障碍--障碍.md)是三人六动作截断|q|≤3势，效用为删除位边际，并非客户均分模型。其完整43节点SPE actual034、u=(0,105,56)、总收益P161、真正两对手静态值v56；P<3v168、首两105<112，而弱P−(5/2)v=21>0。六动作不等于六玩家，P不称CAG覆盖W，161<168不反原聚合安全或half。

该输入Φ1=Φ11=161，破纯对角预算；甚至只看三人终局，111各人收益0会迫CAG主题1为空，但001中唯一标签1玩家却得161，已经矛盾。根源码verify_dr_boundary和冻结报告原先只按作者声明；当前Root另有一次标准库新定义检查核168mono/252DR/258IC/21静态背景，原CLI0。它不是给原缺3967B源码认证或新增一名盲审者，也不证明扩大DR点可编译为合法CAG。

安全入口其余dr_potential_probe、所有*_n*k*和dr_groups数值JSON均为扩大模型浮点诊断；随机完整policy锥可退化、后来按真实势/分组生成，是搜索设计动机而非无反例证明。dr_boundary_exact是作者精确证书标签，其它没有自动精确等级。本批不读取/运行全部数值文件，不按通配名额外done引用源。

## 独核的实际范围、先验与同字节别名

三份必要独审原稿14428/3971/10790B均实际全文读，原件见[related清单](../../../../tools/evidence/r2fc-coverage-security-and-review-entries-primary/related-source-manifest.json)，本批不额外done它们。它们分别与已完成canonical源781c…/34736…/af985…同SHA；不同路径不增加审查者人数。

| 审查/实现身份 | 实际内容和边界 |
| --- | --- |
| coverage_representation_independent_review | 先独立从定义证明CR2/3，后收到作者完整稿核CR1…5并回读已修边界，无未解决fatal；不依作者程序、不冒另一次独立运行。CR6不在该成文独审范围。 |
| PM2后续心算 | 入口仅说independent_mechanism另从定义心算复核PM2且无异议，**未另写独立审查文件**；不同于上项已成文CR审查，不倒扩为PM1…3全套独审。 |
| collision_free_spe_independent_review | 原审查者未读发现稿/代码，从五单位客户和真回复表独立重构二人四主题，5历史20含self比较、16终局；无拥挤W4/OPT5同时反所有f0=0/f1=1可加纯负载桥，不反half。 |
| collision_free_family_independent_review | 未读global发现稿/未调用oracle，独立Q/B加强状态归纳并与原根交叉核对；Q须允许多个旧A，fresh B需专门可信分支，子树有序互不冲突、人数严格递减。不是有限k枚举的归纳外推。 |

五客户端点及[任意k完整族](../反例/三人碰撞自由族福利障碍--反例.md)已有自足全文；后者文件名沿旧稳定对象，但结论是每k≥1、m=k+1，**存在**完整SPE、W2k+2/OPT3k+2、比率趋3/2，不是所有SPE固定该路径、更不是只三人。本族对统一纯终局负载付款在f0=0时给必要f1≥3/2，不说该系数充分。原纯遗漏“全部红客户覆盖由actual蓝W付”另已被两人族否定；遗漏与净差不同，不能当half等价式。此处不代领Root四个globalproof稿。

## 审计代码版本与读取边界

本批一次安全helper尝试7件，三独审MD齐、四工作区程序11506B audit_coverage_geometry、5238B PM审计、3967B DR验证、4128B碰撞独审代码均缺blob，无网络/重试。原README的“已实际运行全过”保当时作者身份，不冒本批读缺代码或执行。

尤其已有[覆盖矩精确核验](../计算/覆盖矩表示与非负实现的精确核验--计算.md)实跑的是11313B canonical程序SHA317268b1…，不是缺失11506B工作码SHA6a750484…；两份代码不能凭同题名视为同SHA。工作区13248B冻结输出的inventory大小/SHA082fd977…与实际canonical已核报告大小/哈希一致，冻结身份绑定保于[版本表](../../../../tools/evidence/r2fc-coverage-security-and-review-entries-primary/audit-version-binding.json)。报告相同不认证缺代码相同或该源码入口已跑。

那份已完成有限资源实际涵盖22组秩/56形式策略、极射线、两类障碍和5组有理稀疏化，另有CR6有限非SPE测试；不能按原标题CR1…5抹掉它的有限CR6段，也不能把该段移给独审的普遍CR6证明。PM21834/502及五客户原码运行仍各保自己的来源/版本/计数，不由canonical覆盖审计包办。

GE新增数学CLI/原审计/随机LP/根定义检查/旧成功复跑均0；所有普遍数学由现自足证明承担。三入口全部字段、每个资源角色、历史审查与缺口已归位，[证据与读取范围](../../../../tools/evidence/r2fc-coverage-security-and-review-entries-primary/README.md)保完整22ID原claim及本3owner交集；不作伪三ID认领回执、不导第三阶段旧图，无外审或全球新颖性认证。
'''
put(P,body);js(E/'formal-resource-manifest.json',[{'path':P,'bytes':(S/P).stat().st_size,'sha256':sha((S/P).read_bytes())}])
put(E/'README.md',r'''# R2fc三入口的模型与独审资源

GE3原README总6144B完整实读，三份必要独审原稿29189B实际全文读，十份相关正式数学全文比较。唯一新自足资源保CR1…6/PM1…3、support预算及纯对角承重、扩大DR非CAG、独审时序/CR6与PM2范围、程序版本/同字节报告边界。

本批新数学/CLI/SPE/LP/旧成功复跑0。一次safehelper7尝试=3MD齐4代码缺；不网络不重试，不额外done related/引用代码或RootGC4。完整原claim必须保22IDs，只按本3交集/owner生成semantic receipts。

下一可读独审3源已全部related读，且与已完成canonical原件逐SHA同，可诚实duplicate或精确别名去向；不能因同字节多记审查人数。Root正文依赖先pushed后done，代理0sharedGit/show/claim/done/checkpoint/真实身份通信。
''');cp(Path(__file__),E/'build_resources.py')
print(json.dumps({'stage':str(S),'primary_bytes':sum(x['size'] for x in rows),'primary_lines':sum(x['lines'] for x in rows),'related_bytes':sum(x['size'] for x in related),'formal_bytes':(S/P).stat().st_size,'new_math_runs':0},ensure_ascii=False,indent=2))
