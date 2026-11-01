from pathlib import Path
from itertools import product
import json,hashlib

R=Path('/workspace/scratch/37f0f9248cfc');C=R/'boss4-next-cache';REPO=R/'boss4-research';S=C/'r3-complete-menu-certificates-and-review-primary';E=Path('tools/evidence/complete-menu-certificates-and-review-primary');W=Path('cleanup/workspaces/Boss4/r3-complete-menu-certificates-and-review-primary-next')
IDS=['38f33a2ab903eb816fc8','23b69044426c185f1653','f218c3c894b4635ecca2']
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):p=S/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())};claimpath=R/'boss4-r3-next-eo-claim.json';claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(claim['ids'])==set(IDS)
cp(claimpath,E/'actual-claim-receipt.json');owners={}
for i in IDS:
 x=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[i]['sha256'];owners[i]=x
js(E/'primary-ownership-snapshot.json',owners)
supply=json.loads((C/'learning-eo-local-input-manifest.json').read_text());cp(C/'learning-eo-local-input-manifest.json',E/'actual-local-supply-manifest.json');rows=[]
for x in supply['rows']:
 b=Path(x['local_path']).read_bytes();assert len(b)==x['size'] and sha(b)==x['sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'];dest=E/'original'/x['id']/x['path'];cp(x['local_path'],dest);rows.append({**x,'preserved_path':str(dest)})
js(E/'source-manifest.json',rows);byid={x['id']:x for x in rows}
def link(i):return '../../../../'+byid[i]['preserved_path']
codepaths={'f3a45abea06b9736fa4e':'archives/customer-attraction/tools/evidence/origin-retraction-workspace/original/research/workspaces/customer-attraction/R-3bc48d936f044f12b0fa743482ff5eb0/flow/audit_origin_retraction.py','f3b5851cc7fb29ce4d0f':'archives/customer-attraction/tools/evidence/extra-slot-programs-primary/original/f3b5851cc7fb29ce4d0f/source','46b1b3c7907ee8c886ce':'archives/customer-attraction/tools/evidence/continuation-security/examples/customer_attraction/individual_security_failure.json'}
related=[]
for i,n in codepaths.items():
 b=(REPO/n).read_bytes();x=inv[i];assert len(b)==x['size'] and sha(b)==x['sha256'];dest=E/'related'/i/x['path'];cp(REPO/n,dest);related.append({**x,'local_path':str(REPO/n),'preserved_path':str(dest),'read_scope':'actual complete code or base-instance read; no extra primary done'})
js(E/'related-source-manifest.json',related)
oldpaths=['archives/customer-attraction/tools/evidence/origin-retraction-workspace/replay-input-manifest.json','archives/customer-attraction/tools/evidence/origin-retraction-workspace/replay/execution.json','archives/customer-attraction/tools/evidence/origin-retraction-workspace/replay/origin_retraction_exact_audit.json','archives/customer-attraction/tools/evidence/extra-slot-programs-primary/runs/EXECUTIONS.json','archives/customer-attraction/tools/evidence/extra-slot-programs-primary/parent-report-comparison.json','archives/customer-attraction/tools/evidence/extra-slot-programs-primary/runs/parent-aggregate/stdout.txt']
oldmanifest=[]
for n in oldpaths:
 b=(REPO/n).read_bytes();dest=E/'reused-evidence'/n;cp(REPO/n,dest);oldmanifest.append({'path':n,'bytes':len(b),'sha256':sha(b),'preserved_path':str(dest),'scope':'full actual report/metadata read; original run historical and not repeated'})
eg=C/'r3-two-tail-pushforward-and-full-menu-boundaries-primary/tools/evidence/two-tail-pushforward-and-full-menu-boundaries-primary'
for n in ['runs/new-branch-arithmetic-001/report.json','runs/new-branch-arithmetic-001/run-metadata.json','calculate-menu-diagnostics.py']:
 cp(eg/n,E/'reused-EG-arithmetic'/n)
js(E/'old-evidence-manifest.json',oldmanifest)
cycle=json.loads((S/byid[IDS[1]]['preserved_path']).read_text());empty=json.loads((S/byid[IDS[2]]['preserved_path']).read_text());base=json.loads((REPO/codepaths['46b1b3c7907ee8c886ce']).read_text());diag=json.loads((eg/'runs/new-branch-arithmetic-001/report.json').read_text());origin=json.loads((REPO/oldpaths[2]).read_text());parent=json.loads((REPO/oldpaths[5]).read_text())
assert set(cycle)=={'kind','instance','certificate','forced_paths','root_payoffs','potential','K','cycle','cycle_entry','root_u','verification'}
assert set(empty)=={'kind','source_instance','instance','query_probability','certificate','forced_root_paths','forced_root_payoffs','entry_X2_after_empty','entry_X2_after_X2','D','C','D_minus_C','u_minus_C','verification'}
assert empty['instance']['players']==base['players']==3 and empty['instance']['customers']==base['customers'] and empty['instance']['topics']==base['topics']+['Empty'] and 'certificate' not in base
tables=[]
for o,k in [(cycle,6),(empty,7)]:
 tab={tuple(x['history']):x['action'] for x in o['certificate']['actions']};expected={h for d in range(3) for h in product(range(k),repeat=d)};assert set(tab)==expected and len(tab)==len(o['certificate']['actions'])
 def rule(h):
  if not h:return 0
  if len(h)==1:return 3 if h[0]<3 else 0
  a,b=h;g=b if b<6 else a
  if g==6:return 0
  return next(t for t in range(0 if g<3 else 3,3 if g<3 else 6) if t not in h)
 assert all(v==rule(h) for h,v in tab.items())
 tables.append(tab)
 assert o['certificate']['terminal_counts']==[list(diag['cycle348' if k==6 else 'empty34']['six_forced_roots' if k==6 else 'seven_forced_roots'][0]).count(a) for a in range(k)]
assert all(tables[0][h]==tables[1][h] for h in tables[0])
assert cycle['forced_paths']==diag['cycle348']['six_forced_roots'] and cycle['root_payoffs']==diag['cycle348']['six_root_payoffs'] and cycle['potential']==diag['cycle348']['six_potentials'] and cycle['K']==diag['cycle348']['full_root_K'] and cycle['cycle']==[2,5] and cycle['cycle_entry']==['159/2','159/2'] and cycle['root_u']=='147/2'
assert origin['fixture_sha256']==inv[IDS[1]]['sha256'] and origin['status']=='passed' and origin['audits'][0]['complete_history_IC_checks']==258
assert cycle['verification']=={'valid':True,'histories':43,'deviations':215}
for a,b in [('forced_root_paths','seven_forced_roots'),('forced_root_payoffs','seven_root_payoffs'),('query_probability','query_probability'),('D','D'),('C','C'),('D_minus_C','D_minus_C'),('u_minus_C','u_minus_C')]:assert empty[a]==diag['empty34'][b]
assert empty['entry_X2_after_empty']==diag['empty34']['K_2_6'] and empty['entry_X2_after_X2']==diag['empty34']['K_2_2']
assert parent['sha256']==inv[IDS[2]]['sha256'] and parent['histories']==57 and parent['nonself_deviations']==342 and empty['verification']=={'valid':True,'histories':57,'deviations':342}
binding={'scope':'one new structural/serialized-field binding pass only; no payoff recomputation, original CLI, full SPE replay or mathematical numeric run','primary_complete_top_level_keys':{IDS[1]:list(cycle),IDS[2]:list(empty)},'complete_ordered_action_domains':{'348':43,'34plusEmpty':57},'compact_rule_matches_every_serialized_action':True,'all43_six_label_history_actions_shared':True,'base1465_vs_extended7992':{'same_three_players':True,'same13_customer_entries':True,'topics_append_only_Empty':True,'base_has_no_certificate':True},'terminal_count_fields_match_EG_actual_roots':True,'all_serialized_root_paths_payoffs_K_Phi_entries_and_gaps_match_prior_EG_result':True,'old_full_history_records_same_input_SHA':True,'kind_metadata_correction':{'original':empty['kind'],'actual_exact_order':'D<C<u','interpretation':'NOT-C-LT-U is not a valid literal truth assertion; correct scope D<C but not C>u'},'new_mathematical_runs':0,'shared_Git_or_network':0}
js(E/'structural-and-field-binding.json',binding)
def table(h,rs):return '| '+' | '.join(map(str,h))+' |\n| '+' | '.join(['---']*len(h))+' |\n'+''.join('| '+' | '.join(map(str,r))+' |\n' for r in rs)
types348=table(['客户兴趣标签','不同单位客户数'],[[','.join(map(str,x['topics'])),x['multiplicity']] for x in cycle['instance']['customers']]);types34=table(['客户兴趣标签','不同单位客户数'],[[','.join(map(str,x['topics'])),x['multiplicity']] for x in empty['instance']['customers']]);Ktable=table(['查询/强制根']+list(range(6)),[[i]+x for i,x in enumerate(cycle['K'])]);pathstable=table(['强制根','348真实叶','348根收益','34真实叶','34根收益'],[[i,','.join(map(str,cycle['forced_paths'][i])) if i<6 else '无标签6',cycle['root_payoffs'][i] if i<6 else '—',','.join(map(str,empty['forced_root_paths'][i])),empty['forced_root_payoffs'][i]] for i in range(7)])
P=Path('archives/customer-attraction/state/资料/完整根查询证书的字段与审计范围--资料.md')
refs=[]
for i in IDS:
 for x in inv[i]['sources']:refs.append('  - "source:'+x['commit']+':'+x['path']+'"')
header='\n'.join(['---','id: "customer-attraction/complete-root-query-certificate-fields-and-audit-scope"','kind: "resource"','type_tag: "资料"','title: "完整根查询证书的字段与审计范围"','status: "full-original-field-bindings-and-same-SHA-evidence-reused; no-new-math-run"','summary: "两份三人完整策略JSON的全部字段、单位客户、100有序动作和原审计消费范围自足保留；区分根查询K与付款流K、根混合D/C与三位置聚合，并纠正34输入kind标签的真值歧义。"','source_refs:']+refs+['---',''])+'\n'
body=r'''# 完整根查询证书的字段与审计范围

## 三份原件和已有数学对象

[5009B内部独审](SRC_REVIEW)、[7417B二环JSON](SRC_CYCLE)、[7992B空主题JSON](SRC_EMPTY)均完整实读，两个冻结位置各同字节。此前EG仅作related，未因此成为primary done；本批重新核size/SHA256/blobSHA1并复用完整阅读，不虚增独立首读或运行。

独审的全部证明、实背景/独立性/共同目录条件、精确等号、单客户任意b,t锐族已完整归入[锐曲率与双分支引理](../引理/末位真实回复推送的锐曲率与双分支式--引理.md)，本源按准确去向duplicate。它历史上先据陈述盲证再读发现稿，不等于本次读后整理又做盲证，也不是外审。余两源是两个不同单位客户实例的完整有序策略和数值证书，不用同一策略模板合并客户输入。

以下模型都是三名单位提供者、有限非空共同目录、客户在最终覆盖者间均分，保重复、有序离轨历史和任意合法平局。重数只压缩不同单位客户，不是加权原子玩家；主题6仅在第二实例出现且为空覆盖。

## 两份完整单位客户输入

348实例标签0至5分别X0,X1,X2,Y0,Y1,Y2；18类均展开为不同单位客户：

TYPES348

34实例13类如下，标签0至5同名，另加Empty=6，没有客户接受6：

TYPES34

其source_instance指向[1465B基础实例](SRC_BASE)，本批全文核实际SHA。players与13项customers完全相等，topics只追加Empty；**基础文件没有certificate**，不能说它自带本7992B文件的57动作或追加空主题后自动继承SPE。

## 完整策略的无损紧写与动作计数

两输入共同的六标签规则：根0；第二人见首主题属于X={0,1,2}取3，否则0；二历史(a,b)后末位取b所属组三标签中最小未出现者。34扩展还规定首6后第二人0；当b=6而a非空时，末位取a所属组三标签中最小未出现者，a=b=6时取0。b不空时仍用b的原组内规则，a=6不排除任何组六标签。每组3标签、此前至多2标签，规则处处有定义。

本批对原动作数组逐行做**结构一致性**比较：前者恰1+6+36=43有序键，后者1+7+49=57，所有43个无6历史上的规定动作相等；新加的是一个二人节点和13个末位节点。初稿曾把b空时误紧写为全局最小标签，结构断言在(3,6)/(4,6)/(5,6)三历史分别发现源动作4/3/3与初稿0不符；已按原表修正，失败记录保留。没有在这一步重算利润或SPE，也没有改原策略。相同动作表不意味着不同客户权重下自动都是SPE；各自旧审计分别绑定其输入SHA。

certificate.terminal_counts分别(1,0,0,1,1,0)和(1,0,0,1,1,0,0)，与已在EG算出的actual叶(0,3,4)计数一致。全部强制根路径和根玩家收益为：

ROOTPATHS

这里六个root_payoffs不是actual三个角色的利润向量。348实际角色利润为(147/2,171/2,71)，W230、OPT3=270；34实际利润(29/3,67/6,67/6)，W32、OPT3=34。两者都满足half；有限辅助桥失败不是六人主目标反例。

## 348 JSON的全部数值字段

kind=HIGH-INSERTION-2-CYCLE-NOT-MENU-COUNTEREXAMPLE是描述标签，instance/certificate给真实对象；forced_paths、root_payoffs已在上表列全。potential六项均304，指Phi(Z)=Σ_xΣ_(j=1)^(c_x(Z))1/j，**不是福利304**。根额外查询矩阵K的行是独立查询t、列是强制根a后的完整三槽，K_ta=Σ_(x喜欢t)1/[1+c_x(Z(a))]：

QUERYK

cycle=(2,5)、cycle_entry=(159/2,159/2)、root_u147/2给两条高插入边。EG同SHA输入的一次根算术已逐项核六根K/Phi和收益，另得两边联合R12、交集税6、裸后继势漂移0；所以159/2=147/2+12−6。列0/3的cap69<u，其余列cap159/2；此二环阻断一般无环/严格共同标量排序，不否定该实例可选好纯列或自由菜单。完整解释见[联合势资料](../资料/完整根菜单的联合势义务与排序边界--资料.md)。

verification.valid=true、histories43、deviations215是原报告字段；现有原程序的258项包括43自身与215非自身，口径一致。并非215个不同实例，也没有因此认证任意参数。

## 为什么旧回撤报告的K不是这个K

[10829B审计代码](SRC_ORIGIN_CODE)已全文读。它只从本JSON消费instance及certificate.actions；不用kind、序列化root K、potential、cycle或verification字段。程序逐每个有序历史、每个六行动重算真实后继利润，对348做258项含自身比较，随后才审计固定比较(5,2,4)的来源回撤流。

该报告的K是三角色间的3×3付款传播矩阵，与本JSON的6×6根查询矩阵对象/维数/单位均不同。本fixture的R_source全0、付款K全0，不能从它是零声称根查询K为零或二环不存在。此例未触发非平凡回撤；报告其余52客户及边界例不是本三源的新处理范围。

原代码标准库Fraction、无solver，main有保护，但会按HERE.parents[4]找原路径、在代码目录覆写同名报告；不能在共享树为“再看一次”执行它。[旧执行记录](OLD_ORIGIN_EXEC)明确exit0、生成字节等于冻结，输入清单绑定本SHA；[旧完整输出](OLD_ORIGIN_REPORT)也实读并保留。本轮不执行/导入，零新的回撤或SPE重放。旧报告只验证了其实际消费的字段，根查询附带值由EG单独核，不扩大旧运行覆盖。

## 34 JSON：根混合数字与kind标签

query_probability=(0,0,1/10,0,0,0,9/10)是独立同分布的源B和查询A law，保留全部三位竞争者。entry_X2_after_empty=32/3是查询2面对强制空根的完整叶(6,0,1)；entry_X2_after_X2=13/2是查询2面对(2,3,4)。forced_root_payoffs及路径已列全，因此

\[
D=\frac1{10}\frac{29}3=\frac{29}{30},\quad
C=\frac1{10}\left[\frac1{10}\frac{13}2+\frac9{10}\frac{32}3\right]=\frac{41}{40},
\quad D-C=-\frac7{120},\quad u-C=\frac{1037}{120}>0.
\]

这些对应D,C,D_minus_C,u_minus_C全部根部字段，已和EG既有计算逐字段一致。真实顺序是D<C<u；原kind字串EXACT-D-LT-C-NOT-C-LT-U的NOT-C-LT-U若按字面当成“非C<u”就不真。原标签原样保留，准确数学应说“D<C，但没有C>u”，不能让kind字符串代替数值/真值。它不是实际u封顶、自由Mfull或half反例。

verification的57历史、342非自身偏离与[3119B父方审计代码](SRC_PARENT_CODE)吻合。该代码实际比较全部57×7=399项，仅计数时跳过57自身。它无main保护，读取输入后在顶层直接核验并打印；**import也会执行**。本批仅全文读代码，不导入或复跑，旧成功/源SHA/stdout绑定记录已保留。

## 同一输入的三位置聚合量不能冒充根D/C

记Z_i(a)为actual前缀强制位置i选a、再沿同一原策略完成的全部三槽；D_i(p)=E_a当前角色利润(Z_i(a))，G_i(p)=E_(a,t独立同分布p)额外查询t面对Z_i(a)的利润。父方代码在actual每个位置分别强制query2或空6；下表列的是三个纯行动系数，不是已按p平均后的D_i(p)、G_i(p)：

| actual位置 | 强制query叶 | 强制空叶 | D_i纯query收益 | H_i空位查询 | G_i纯额外查询 |
| --- | --- | --- | ---: | ---: | ---: |
| 1 | 2,3,4 | 6,0,1 | 29/3 | 32/3 | 13/2 |
| 2 | 0,2,1 | 0,6,1 | 32/3 | 32/3 | 7 |
| 3 | 0,3,2 | 0,3,6 | 67/6 | 67/6 | 7 |

总D_0=63/2,H_0=65/2,G_0=41/2。对p_e=e delta2+(1−e)delta6，根部与三位置总量准确为

\[
D_{root}(e)-C_{root}(e)=-e+\frac{25}6e^2,
\quad\sum_iD_i(p_e)-\sum_iG_i(p_e)=-e+12e^2.
\]

空行动当前收益和空查询价格均0，所以每位置D_i(p_e)=eD_i纯，G_i(p_e)=e[(1−e)H_i+eG_i纯]。前者直接由根的29/3、32/3、13/2展开，后者由全位置D_0−H_0=−1,H_0−G_0=12；这是该固定输入对所有e的双抽样解析身份。根JSON取e1/10给−7/120；聚合旧审计取e1/24给D21/16、G4/3、差−1/48。甚至同取e1/10，聚合差为+1/50而根差为负，说明不能跨目标偷换一个D或gap字段。

旧审计在七个e值直接核该多项式，不是一般p/全部输入证明；其代码没有把G−D改成G−W。弱聚合ΣG≤W、允许另选Q的菜单和原half仍是不同量词。本批这些多项式是依据已读固定行值的解析展开，没有新增数值程序执行。

## 逐字段去向和本次实际工作边界

两JSON全部top-level、instance/customer条目、certificate的100个有序动作、完整路径、根收益及全部附带值都已有明确去向：数据与完整策略在本页/原件，根数学在EG两正式对象，旧运行只认其实际消费与输出范围。[新字段绑定](../../../../EVID/structural-and-field-binding.json)记录字节、键域、动作紧写、基础实例追加空标签和与旧结果逐字段相等；它是结构检查，不是新数学审计。

5009B独审的记号r_x等于发现稿j_x，独审K等于BR总slack L，不等于本页任一矩阵K；完整证明/等号已在[锐曲率对象](../引理/末位真实回复推送的锐曲率与双分支式--引理.md)自足保留。本轮没有原CLI或新增数学核验程序运行、SPE复演、solver、样本扫描、Git写或网络。EG旧run、两原程序成功和本批结构比较分别记，不合称新独立实现或外审；相关代码/基础实例只比较，不额外done。
'''
replacements={'SRC_REVIEW':link(IDS[0]),'SRC_CYCLE':link(IDS[1]),'SRC_EMPTY':link(IDS[2]),'SRC_BASE':'../../../../'+next(x['preserved_path'] for x in related if x['id']=='46b1b3c7907ee8c886ce'),'SRC_ORIGIN_CODE':'../../../../'+next(x['preserved_path'] for x in related if x['id']=='f3a45abea06b9736fa4e'),'SRC_PARENT_CODE':'../../../../'+next(x['preserved_path'] for x in related if x['id']=='f3b5851cc7fb29ce4d0f'),'OLD_ORIGIN_EXEC':'../../../../'+str(E/'reused-evidence'/oldpaths[1]),'OLD_ORIGIN_REPORT':'../../../../'+str(E/'reused-evidence'/oldpaths[2]),'TYPES348':types348,'TYPES34':types34,'ROOTPATHS':pathstable,'QUERYK':Ktable,'EVID':str(E)}
for a,b in replacements.items():body=body.replace(a,b)
put(P,header+body)
contexts=['archives/customer-attraction/state/引理/末位真实回复推送的锐曲率与双分支式--引理.md','archives/customer-attraction/state/资料/完整根菜单的联合势义务与排序边界--资料.md','archives/customer-attraction/state/计算/来源回撤原程序与有序策略的精确重放--计算.md','archives/customer-attraction/state/审查/额外槽扫描的实际强桥目标与两份定义级核验--审查.md']
ctx=[]
for n in contexts:
 b=(REPO/n).read_bytes();cp(REPO/n,E/'context'/n);ctx.append({'path':n,'bytes':len(b),'sha256':sha(b),'snapshot':str(E/'context'/n),'read':'actual full prior EG formal read, same bytes reused; no extra done'})
js(E/'context-manifest.json',ctx);js(E/'formal-resource-manifest.json',[{'path':str(P),'bytes':(S/P).stat().st_size,'sha256':sha((S/P).read_bytes())}]);cp(Path(__file__),E/'build_resources.py')
print(json.dumps({'claim_tip':claim['remote_tip'],'actual_primary':len(rows),'primary_bytes':sum(x['size'] for x in rows),'primary_lines':sum(x['lines'] for x in rows),'formal_bytes':(S/P).stat().st_size,'new_math_runs':0,'new_structural_binding_passes':1},ensure_ascii=False))
