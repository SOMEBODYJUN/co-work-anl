from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json,hashlib,re
stage=Path(__file__).resolve().parents[4];repo=stage.parent.parent/'boss4-research';ev=Path('archives/unrelated-machines/tools/evidence/um-following-audit-primary');ws=Path('cleanup/workspaces/Boss4/r3-um-following-audit-primary')
def j(path,x):
 p=stage/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def s(path,x):
 p=stage/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(x.strip()+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((stage/ev/'manifest.json').read_text());by={x['id']:x for x in m['records']};objs=json.loads((stage/ws/'object-paths.json').read_text());get=lambda name:next(x for x in m['records'] if Path(x['path']).name==name)
# Construct only immutable fixture tables by the displayed bridge definition; do not import/call original programs.
a=json.loads((stage/get('bounded_collision_label_floor_audit.json')['evidence_path']).read_text());f=json.loads((stage/get('pairwise_label_resource_floor.json')['evidence_path']).read_text())
cases=[(x['resource_sets'],x['demands'],x['name']) for x in f['cases']]+[([],[],'empty_root_terminal'),([[0,1],[1,2,3,4],[3]],[2,3,1],'heterogeneous_private_resources')]
bridge=[]
for sets,demands,name in cases:
 old=next(x for x in a['normative']['actual_schedule_checks'] if x['name']==name);q=len(sets);resources=sorted({u for x in sets for u in x});rid={u:2*q+1+i for i,u in enumerate(resources)};n=2*q+1+len(resources);k=[q]+[1]*q+demands+[0]*len(resources);edges=[]
 for x,support in enumerate(sets):edges.extend([(0,x+1),(x+1,q+1+x)]+[(q+1+x,rid[u]) for u in support])
 out=[[] for _ in range(n)]
 for u,v in edges:out[u].append(v)
 jobs=[{'identity':['root',0,0],'finite':[[0,'1']]}]
 for u in range(n):
  if not k[u]:continue
  z=min(k[u],len(out[u]))
  for t in range(z):jobs.append({'identity':['token',u,t],'finite':[[u,str(F(1,k[u]))]]+[[v,'1'] for v in out[u]]})
  if z<k[u]:jobs.append({'identity':['filler',u,0],'finite':[[u,str(F(k[u]-z,k[u]))]]})
 assert (n,len(jobs))==(old['vertices'],old['jobs']);loads=[F(0)]*n
 for job,owner in zip(jobs,old['assignment']):loads[owner]+=dict((i,F(p)) for i,p in job['finite'])[owner]
 assert list(map(str,loads))==old['loads']
 bridge.append({'name':name,'materialization':'read-only expanded from preserved input/bridge definition and actual old sigma; not an original-program run','source_run':get('bounded_collision_label_floor_audit.json')['evidence_path'],'input':{'n':n,'edges':edges,'demands':k,'resource_sets':sets,'bundle_demands':demands},'original_jobs':jobs,'historical_tree':old['tree'],'historical_sigma':old['assignment'],'historical_loads':old['loads'],'historical_score':old['score'],'historical_b_star':old['b_star'],'historical_makespan':old['makespan']})
j(ev/'fixtures/four-original-bridge-inputs-and-historical-witnesses.json',bridge)
j(ev/'runtime-dependencies-and-run-binding.json',{'new_original_program_runs':0,'reason':'Exact-SHA sufficient old runs and all program inputs/dependencies retained; no repetition merely to increase run counts. New verifier checks immutable input/output identities and arithmetic, never imports original primary modules.','claim_capture':m['claim_capture'],'claim_tip':m['claim_tip'],'bindings':[
{'primary_id':'d5a14149ab0edb517bc1','sha256':by['d5a14149ab0edb517bc1']['sha256'],'old_manifest':str(ev/'historical-runs/cartesian_menu_reverse_v1/manifest.json'),'historical_command':'python audit_normalized_flat_cartesian_tensor_reverse_amplification.py --output-dir /absolute/fresh/output_dir','actual_run_evidence':'cartesian_menu_reverse_amplification_review.md records root actual fresh-directory15-file byte-identical reproduction; root_original_matrix_verification separately records4710job/fulltable check and second t1 enumeration.','historical_exit_code':None,'historical_elapsed_seconds':None,'new_stdout':False,'imports':'standard library only; fixedExactSHA is identity text, no file read; main fixedt1..4','old_output_files':15,'root_extra_files':1,'overwrite_refusal_actual_actor':'fee, not root/current cleaner'},
{'primary_id':'8db8d8577400f86d0b4e','sha256':by['8db8d8577400f86d0b4e']['sha256'],'old_record':get('dual_rail_threshold_soundness_boundary_audit.json')['evidence_path'],'old_payload':'root_actual_runs.boss11_dual_rail_cube_cut_actual.json.tested_constructor_sha256 plus complete frozenA3fixture','historical_command':'python3 tests/audits/unrelated_machines/balanced_dual_rail_fullcube.py --A 3; additionally tested.construct(A) executed inside old independentA1..5 run','historical_exit_code':None,'new_stdout':False,'imports':'standard library only; --A default3; no external input files'},
{'primary_id':'e92ad715a0c9aff7de17','sha256':by['e92ad715a0c9aff7de17']['sha256'],'old_record':get('dual_rail_threshold_soundness_boundary_audit.json')['evidence_path'],'old_payload':'root_actual_runs.boss11_dual_rail_cube_cut_actual.json','historical_command':'python3 tests/audits/unrelated_machines/balanced_dual_rail_fullcube_independent.py','historical_exit_code':None,'new_stdout':False,'runtime_dependency':'Same-directory balanced_dual_rail_fullcube.py imported with importlib as tested subject; original oracle/checker/half certificate do not call testedformula/flow helpers.','frozen_group_exit_codes':'aggregate process_exit_codes has8 zeros; no command-index map retained, so individual exit code remains null'},
{'primary_id':'122e8b2a473d0aeaf6d8','sha256':by['122e8b2a473d0aeaf6d8']['sha256'],'old_record':get('bounded_collision_label_floor_audit.json')['evidence_path'],'old_payload':'normative','historical_command':'python3 tests/audits/unrelated_machines/bounded_collision_bundle_floor.py','historical_exit_code':0,'exit_code_evidence':'bounded_collision_label_floor_review.md final implementation/root paragraph explicitly states both final root reruns exit0','historical_elapsed_seconds':a['normative']['elapsed_seconds'],'new_stdout':False,'runtime_dependency':get('rooted_dag_token_bridge.py')['evidence_path'],'input_fixture':get('pairwise_label_resource_floor.json')['evidence_path'],'fixture_path_semantics':'Path(__file__).resolve().parents[3]/examples/unrelated_machines/pairwise_label_resource_floor.json, notcwd','actual_schedule_domains':'4 bundle cases plus21 selected menu cases, notall2490 menu cases'},
{'primary_id':'3cb3475471e5beaf4e40','sha256':by['3cb3475471e5beaf4e40']['sha256'],'old_record':get('bounded_collision_label_floor_audit.json')['evidence_path'],'old_payload':'independent','historical_command':'python3 tests/audits/unrelated_machines/bounded_collision_bundle_independent.py','historical_exit_code':0,'exit_code_evidence':'original review explicitly root reran both final scripts exit0','new_stdout':False,'imports':'standard library only; no normative/bridge import','seed':2026101711,'actual_schedule_generation':False,'scheduling_scope':'algebra on2-score and2-bstar only; no physical schedule emitted'}
],'nonclaims':['No current original entrypoint execution, newprimary stdout or fabricated time/exit code.','Complete source comparison does not mark unrelated old result/source IDs primarydone.','Old15tensor generated outputs plusrootextra are complete historical data; no extra original run.']})
j(ev/'source-semantic-units.json',[
{'id':'d5a14149ab0edb517bc1','destination':objs[0],'units':['ExactSHA and stdlib CLI/freshmkdir/openx/floatrejection','full resource-scanP and direct independent finite-table checker','cyclic actual sigma, allunselectedstatejobs, real timeinterval/nooverlap','allordered complementaryg/state intersection certs and formula crosscheck','hardguardt1only1024complete optimization/histogram','fixedt1..4 outputs15+rootindependentextra16 historical identity, no coordinatequota implementation']},
{'id':'8db8d8577400f86d0b4e','destination':objs[1],'units':['Ainteger instancefulltwoedge matrix and d/k/counts','allBmaskformula with(value,B)tie','IntegralFlow BFS reversecapacities and exact selectedport handles','physicalactualalljob sigma/load and railcount','A3hand7portdoublecertificate','CLIdefaultA3 and expandedinputcomplexity/nohardnessscope']},
{'id':'e92ad715a0c9aff7de17','destination':objs[1],'units':['allnonempty variablesubsetcuts forB0..d and optimizedclausecut formula','allloadbreakpoints plusfloor/mincap normalform','independent fullmatrix joborder/real load reconstruction','independent half3/2certificate and allsourceNO truthmasks','actualimporttestedconstructor withoutoracle formula/flow reuse','A1..5counts6342/352/11592/10/680, nofullphysicalassignmentenum']},
{'id':'122e8b2a473d0aeaf6d8','destination':objs[2],'units':['strict _normalized fullsupport→sortedtrim and ownerorder permutations','boundedfloor localpigeonhole/colorchoice/actualallocation validation','localfullscan onlyb1reject, nozero-scoretest','actualDAG/tree and menuoriginal-demand rescoring','groupdistinctdegree/fullmenu capacityprefixU/selecteddelta versusglobaldelta','two separate exponentialsmalloracle normalizations and state meanings','all finite r/q/owner variants/sharp/boundaries/invalidinput domains','real rootedbridge import/examplepath and4fullcaseplus21menu schedule calls']},
{'id':'3cb3475471e5beaf4e40','destination':objs[2],'units':['full original resourceparent oracle allows multiplelabels pergroup','selectedwhole-support Δ beforeanydemandtrim, unlikeproduction','globaldistinctgroups/no-labelindegree confusion','Gamma thresholdconstructor firstqualifyinglabel/ceil resources/reversegroupcolors','formula-onlysortedU crosscheck and exact originaldemand witness validation','scope of random/sharedcategories/extended64menus/hugebinarydemand/sharp2forK versusgeneralΔK1','no normativeimport/no actualschedule generation, bridgebound algebra only']}
])
# Existing formal paths compared before actual claim; preserve their current identities and optional prior scope statements.
context=json.loads((stage/ws/'context-preparation.json').read_text());j(ev/'related-formal-material.json',context['related_formal_read'])
j(ev/'comparison-findings.json',{'old_pages_modified':False,'findings':[
{'kind':'semantic implementation distinction, not claimed mathematical error','production':'bounded_collision_floor trims sorted support toK beforeΔ','independent':'collision_certificate counts whole selected support; maycertify weaker1/Δ','source_evidence':'7f2 _normalized/trimmed/owners versus b223 collision_certificate.used.update(resources)','destination':objs[2]},
{'kind':'oracle scope distinction','production':'exact_label_optimum one-label normalization has proof forβ≤1/groupdemand1; exact_bundle countsowners×subsets','independent':'originalresource-parent oracle permits several selectedlabels inonegroup','destination':objs[2]},
{'kind':'runtime independence precision','independent_cube':'imports same-directory tested constructor and callsconstruct; oracle formula/cuts/breakpoints independent of testedformula/flow','destination':objs[1]},
{'kind':'frozen output scope','tensor':'program generates15files; root independentverification isextra16; onlyt1 fullopt','destination':objs[0]}]})
notes={
'd5a14149ab0edb517bc1':('实际全文363行/16567B核efa03SHA，逐函数读所有矩阵/调度/区间/交点/t1oracle/freshoutput/精度保护与main，理解fixedt1..4非一般算法。','全文比较50d41组合稿、7a1fc原审查、既有裸菜单/配额分域及root重现页；核全部原15输出和root额外原矩阵记录身份，按实际P和每项证书完整验证。','新资源完整保存程序独有checker、输出保护、全部有限原任务/交点和t1枚举边界；旧一般证明不重新授定理，同SHA充分历史run复用，未冒称本批复跑或root亲做拒覆盖。'),
'8db8d8577400f86d0b4e':('全文157行/6143B核fb26SHA，实读A合法域、完整二端输入、全B公式/破平局、残余BFS流、原job物理分配、A3手工、CLI及hash。','与069d canonical§5–8/3b9审查、独立cut代码全文、冻结聚合constructor绑定、完整A3原输入/两sigma/loads及既有cube页比较。','保真实全部任务和精确满流构造/逐机负载、A1非NO及显式展开复杂度，主公式与一般下界自足关联；不把A3或固定B当一般证明，不新跑充分旧入口。'),
'e92ad715a0c9aff7de17':('全文164行/7204B核568cSHA，理解所有变量侧cut、全部物理负载breakpoints、独立原矩阵恢复、半量证书、源NO遍历及真实importlib链/实际被测construct调用。','与原构造、一般完整cube规范化/mincut证明、6342/352/11592/10/680冻结字段及A3原件逐项比；既有cube审查finite域和其它scalar/split合同分开。','自足写明全割条件为何充分、独立oracle不调被测formula/flow但导入被测模块，finiteA1..5非2^n调度枚举。原10证书与重复job检查计数保真，不虚构新run/单命令exit映射。'),
'122e8b2a473d0aeaf6d8':('逐行全文510行/25120B核7f2SHA，五生产API、辅助校验/指数oracles/main每分支读齐；另实读7086B原任务桥与759B真实输入fixture和相对路径。','全文读3ac04现行证明、ba26原review及既有低重数/跨层页；与独立原父点oracle、双路旧run及桥/fixtureSHA比较，保截断后Δ、原需求回算、q0/rootjob1和21menu实际回填。','自足保全部实际API/输入/数学/真实小oracle及finite主域，物化四份小原任务矩阵绑定旧sigma，未执行原main。已吸收主定理保归属，程序独有35,795/2490/21等执行域准确保存。'),
'3cb3475471e5beaf4e40':('全文303行/13256B核b223SHA，原资源父点/多标签真实树oracle、whole-selected-support Δ、Γ阈值/原需求check、U公式交叉与所有随机/退化/锐例范围完整理解。','与生产后截断Δ/一标签规范化/实际桥调用不同，比较独立原review statement-first先验、最终3ac修域及冻结421839/489061和4666计数；同一500随机类别交叠不累加。','保存独有无规范导入的真实原父点枚举、不同Γ构造、强/弱Δ差异及仅调度代数非物理输出范围；所有k锐性由证明另承载，充分真实旧run准确复用不冒作新独立实现。')}
receipts=[]
units=json.loads((stage/ev/'source-semantic-units.json').read_text())
for sid in m['primary_ids']:
 a,b,c=notes[sid];target=next(x['destination'] for x in units if x['id']==sid)
 receipts.append({'id':sid,'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a,'comparison_note':b,'decision_note':c,'disposition':'integrated','targets':[target,by[sid]['evidence_path'],str(ev/'manifest.json'),str(ev/'runtime-dependencies-and-run-binding.json'),str(ws/'数学自查.md')]})
j(ws/'semantic-receipts.json',receipts)
# Actual candidates are current local statuses; no claim operation here.
ids=['366efae229e35047de7f','14c27eb4d50f284464fa','5b9b83fcae1bb3c91099','4a1b8fc533696fbb6811','b99a62dba759d15bdc1e'];inv={x['id']:x for x in map(json.loads,(repo/'cleanup/inventory.jsonl').read_text().splitlines())};nexts=[]
for sid in ids:
 hits=[]
 for p in (repo/'cleanup/checklists').glob('*.md'):
  hits.extend((str(p.relative_to(repo)),line) for line in p.read_text().splitlines() if sid in line)
 assert len(hits)==1 and 'unread' in hits[0][1] and '未认领' in hits[0][1],(sid,hits)
 e=inv[sid];nexts.append({k:e[k] for k in ['id','path','size','sha256']}|{'local_status':'unread/未认领','checklist':hits[0][0],'not_claimed_here':True})
j(ws/'next-candidates.json',{'status':'current local snapshot; parent must check live ownership and actualclaim','candidates':nexts})
s(ev/'README.md','''# 五个原审计程序的完整实质证据

original保存5主源原字节；manifest保存32份原件/相关正文/依赖/原输入/真实旧输出的inventory身份和唯一实际claim回执tip。comparisons和非primary材料的保留不新增其source done。

本批新增原程序运行0。runtime-dependencies-and-run-binding.json保真实旧命令、充分同SHA执行、角色/依赖/退出码已知和未知；所有旧输出均保真。Cartesian目录含完整15程序输出及root额外独立核验，不能把第16件冒作原程序额外输出。

fixtures保存完整A3原输入/双sigma，另从四份小DAG和原桥公式静态物化原任务资格并绑定旧sigma；后者不是执行原构造/main。验证只消费这些冻结数据，源Python只AST解析，无primary导入。

三份自足正式资源保完整数学输入、算法/证明、真实有限域及接续边界。comparison-findings记录后截断Δ与所选全支持Δ、两种oracle、cube独立性和输出范围的准确差别，不覆盖已有共享页。''')
s(ws/'数学自查.md',r'''# 数学自查

已完整逐行读五主源1497行及7086B桥依赖/759B真实fixture，核全部inventory size/SHA；不是以前comparison读抵primarydone。实际claim只绑定唯一路径next15aa的f8aec6… pushed/Boss4/synced，旧776回执无交集未用于认领。

- Cartesian：每state原资源扫描，全部D3+D真实jobs保全；循环见证仅a≠全1外送。checker独立回读有限端和坐标式，全部起讫/原任务/机器负载回算；补组检查是有序D3、无序represented D3/2，不相加。只有t1全优化1024，t2..4只有见证/交点。15程序输出加rootextra16身份及所有hash分别核，精度/拒覆盖只保实际历史执行者。
- Cube：floor/ceil在整数原port数上；任意σ规范化依赖全cube置换对称，C≥d/A大目标分支不能漏。min_B保留，不把B=A固定。独立cut为所有非空变量子集、B0..d，物理断点集完整；其充分性依赖mincut等价，不靠“independent”标签。导入被测construct和oracle不调用其formula/flow两事实同时保留。A1不是NO。10证书/11592逐任务检查有重复输入，不能改成互异job数。
- Bounded：生产Δ在排序截束后算，独立证书用所选标签全支持，后者可更大。Δ_G只计不同group，非标签入度。原树可多标签，生产小oracle的单标签规范化另有证明，独立原父点oracle不施此限制。
- Group approximation：U是真实最优上界，不是精确b*；临时需求只作着色分流，原q/K必须回算。Γ阈值算法和排序生产API是不同实现，巨大K均不按数值展开。q0根终端桥job1/OPT1，空UM0不能混。
- Actual task bridge：四完整fixture和21/2490菜单才实调用桥；独立脚本只验桥代数，不声称其生成schedule。token压缩q=min(K,outdegree)、filler以及C<2解码域自足保存，实际依赖SHA/fixture路径核齐。
- 真实证据：32冻结来源、15+1tensoroutputs、A3完整输入/双证书、bounded四物化小P均检查全部字段/条目；新原main执行0，未知旧individualexit保null。bundle退出码0来自原review明记，旧elapsed只标历史。全JSON可解析，源仅AST解析。

既有一般证明妥善吸收，不因补源码再次授予新定理。已有正式页不改；独有执行范围和先验均落新资源。无未理解主源、无强勾、无一般UM/外审/新颖性升级。''')
s(ws/'关系与来源证据.md',r'''# 关系判断

属于阶段二入库时的关系核对，不复制或预做全仓旧超图。

| 参与对象 | 实际关系及承重范围 | 证据 |
|---|---|---|
| Cartesian原程序 → 已有裸菜单反例 | 实现/有限检查：原P、真实循环sigma和补组交点；一般∀t证明另承载，只有t1枚举优化 | efa03全代码与15原输出、50d41canonical§1–5/8 |
| Cartesian → 逐坐标配额 | 对比量词而非实现边：程序没有受限f匹配后端/物理一致gadget；t2完整Kronecker另是不同P | canonical§6–7、既有分域审查 |
| cube原构造/独立oracle → 双轨精确前沿 | 共同完整cube域；构造满流给真实全部jobs，独立cuts/breakpoints由同构规范化/mincut合同核最优 | fb26/568c原件、069d§5–8、A3完整双证书、旧聚合run |
| cube → scalar/split/exception | 仅其中scalar的特殊完整cube；其它外部成本/任务资格不同，不能互换run或physical枚举身份 | 原四合同review全文 |
| bounded生产 ↔ 独立原父点 | 同四层原需求；不同Δ截断、单标签规范化与多标签原父点、排序/Γ两构造给实现交叉核验 | 7f2/b223、3ac正文、ba26review |
| bounded → 原任务桥 | 实际任务翻译，保全部原jobs、零需求原终端与C<2解码；只对四层桥图像给近似 | 825桥全代码与4+21实际旧调用 |
| 低重数 → 大束/复制/全层quota | 共享资源身份语境下的不同限定结构；低重数地板不自动给源困难性，不能借后者标签升域 | 已读10份正式页的SHA见related-formal-material |

relation只作为来源、实现、有限检查、范围对比证据；没有从有限run生成一般推导边、没有因连通需求造边。既有shared正文不覆盖。''')
s(ws/'delivery.md','''# 交付

5个正式认领原源完整实质整理为3篇自足数学/程序资源，5receipt与准确manifest齐。copy-files.json给精确独立复制范围，父Root串行保存；当前不能称已推送。

本批新原入口运行0，充分同SHA历史run复用，真实依赖/输入和全部必要旧输出保全。验证是原字节/冻结证书/数学计数校验，不执行primarymain，也不把它叫新独立原程序run。

下一5个实际本地未领候选见next-candidates.json；未执行Git/claim/done/checkpoint/spawn。''')
print({'receipts':len(receipts),'new_original_program_runs':0,'materialized_bridge_fixtures':len(bridge)})
