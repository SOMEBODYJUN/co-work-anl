from pathlib import Path
import hashlib,json,os,platform,re,subprocess
import numpy,scipy

S=Path(__file__).resolve().parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=S/'archives/customer-attraction/tools/evidence/true-spe-outcome-evidence-primary'
W=S/'cleanup/workspaces/Boss4/r3-true-spe-outcome-evidence-primary'
P=S.parent/'r3-true-spe-outcome-witness-primary'
PE=Path('archives/customer-attraction/tools/evidence/true-spe-outcome-witness-primary')
NEW='archives/customer-attraction/state/计算/七主题固定输入基线与终局搜索版本--计算.md'
OLD='archives/customer-attraction/state/计算/终局见证DAG的原审计与固定锥预算复核--计算.md'
WEAK='archives/customer-attraction/state/反例/实际均匀缩放负载的弱付款桥--反例.md'
EQ='archives/customer-attraction/state/等价/终局见证DAG的完整历史可实现性--等价.md'
MARKOV='archives/customer-attraction/state/反例/完整历史与计数统一策略的严格分离--反例.md'

def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def fp(p):return {'path':str(p.relative_to(R)),'size':p.stat().st_size,'sha256':h(p)}
primary=json.loads((E/'primary-manifest.json').read_text())['sources']
runtime=json.loads((E/'runtime-manifest.json').read_text())['sources']
dump(E/'source-manifest.json',{'primary_count':5,'primary_bytes':26815,'runtime_only_count':7,
 'runtime_only_bytes':61520,'unique_raw_paths':12,'unique_raw_bytes':88335,'sources':primary+runtime,
 'other_read_sources_do_not_become_primary':True})

related_notes={
 OLD:'逐式全文重读；85原动作表、82行、四原始/对偶全支持、真实原17客户、两历史测量/七探索及上批run均已充分；本批前三主源duplicate对象。',
 WEAK:'全文核定义/无限四主题证明/原85表异于规范13节点/十三人自动机精确税桥与alpha1后修正；不把辅助桥失败移为half。',
 EQ:'全文核(h,k,c)归纳双向、M1由全部actual角色保证、非根非空父x、生成函数、源码范围/集合目录与标签域。',
 MARKOV:'全文读严格原模型31类型/完整表/155精确比较/648及130776穷尽、7/6根集合、22428/22429福利差；不是只观察一份非Markov策略。',
 'archives/customer-attraction/state/问题/完整历史计数策略净化--问题.md':'重新读已由root串行修正后的全文；原普遍净化及最差福利OPEN已否，16000随机/499tie与微扰历史范围保留。',
 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md':'全文重读原目录为集合、合法背景和利润/根覆盖区别、全部有序历史与标签软件扩展；基线七互斥覆盖适用严格子域。',
 'archives/customer-attraction/state/定理/固定完整策略的客户重数锥--定理.md':'全文重读真实Γ/紧截面/达到性标签合同/精确逐坐标对偶/全策略量词；四固定对偶不升级联合MIP。',
 'archives/customer-attraction/state/定理/五人半覆盖--定理.md':'全文重读五人完整53行/类型域/正余项独立证明状态；不把9/5基线当五人锐性，也不称六人已证。'
}
related=[{**fp(R/p),'semantic_comparison':note,'primary_in_this_batch':False} for p,note in related_notes.items()]
dump(E/'related-material.json',{'global_search_scope':'repo archives/customer-attraction/state; related terms 13/33/708669/29481/9/5/count Markov/净化/终局见证 plus explicit model/cone/five theorem',
 'full_related_objects':related,'new_object_addition':'focus on all historical numeric fields, version-specific dimensions, fixed/free baseline and a newly executed optional original branch; existing DAG theorem/counter and fixed-cone proof are reused'})

reused=[]
for path,role in [(PE/'replay-audit/execution.json','previous default original main, not executed again'),
                  (PE/'replay-audit/outcome_dag_audit.json','previous byte-identical default audit output, four saved duals replayed'),
                  (PE/'independent-input-review.json','previous independent 82-row/15-coordinate exact review, not executed again'),
                  (PE/'independent_input_review.py','previous independent code identity, not executed again')]:
    a=P/path;b=R/path
    assert a.read_bytes()==b.read_bytes(),path
    reused.append({'path':str(path),'size':a.stat().st_size,'sha256':h(a),'role':role,
                   'new_executions_this_batch':0,'published_local_bytes_match':True})
dump(E/'reused-evidence.json',{'same_SHA_inputs':[{k:x[k] for k in ['id','path','sha256']} for x in primary[:3]],
 'evidence':reused,'reuse_scope':'exact full-history feasibility and all four coefficientwise fixed-cone dual identities on the saved m4 policy; not seven missing full exploration candidates',
 'previous_default_main_runs':1,'previous_default_build_calls':60,'previous_default_exact_lp_calls':2,
 'previous_fixed_m4_dual_lp_calls':0,'new_default_main_runs':0,'new_m4_dual_replays_or_LP_calls':0})

notes=[
 ('duplicate',[OLD,WEAK],
  '7509B正式claim后clean show重新逐项全读85个ordered history/action与root(1,3,0,0)，双冻结SHA347134…；完整合法历史深0..3均保，非计数合并表。',
  '现有计算页完整给1+4+16+64表、82非零去重Γ和全部对偶行号；原17客户/β族13个离轨不同不能互换。前批原默认audit四对偶重放及独立重构均同SHA，有真实记录。',
  '全部独有内容已有充分自足目标，duplicate。保原件和原run精确引用，不重造对象/不重新解LP；本次正式primary不是前批比较输入的额外done。'),
 ('duplicate',[OLD,WEAK],
  '424B正式claim后全文核topics A/B/Q/D、players4及四客户类型{A}:3,{Q}:1,{A,D}:1,{B,Q,D}:12，全部字段及双冻结SHAfba8f2…核。',
  '完整比较现有无限族m4和计算页原点/四对偶：严格四覆盖互异，17客户W16/OPT17、静态gQ61/13、弱差11/26；原85表与规范族不同但分别完整SPE。',
  'duplicate到原反例及固定锥计算页。原件本stage保留，未对该实例再次跑优化；保弱桥反例而非half，实际客重是不同单位客户。'),
 ('duplicate',[OLD],
  '4512B正式claim后全文逐15系数×4、四整数原始点、β7/4,7/4,655/364,2711/1547及18项非零μ、85/255/W/OPT全部字段，双冻结SHAd47c7…核。',
  '已有页完整85动作表/82行排序/15类型坐标、四目标和所有原始/对偶支持；前批独立JSON全4 min residual0。范围only fixed complete strategy不变，R=W−G与13例后修正精确核。',
  'duplicate，复用已充分同SHA证据不重跑四LP。固定锥全客户上界保留；一般全人数新预算桥已否、恰六人half未判。'),
 ('integrated',[NEW,OLD],
  '12713B全文重新读：7探索全部mode/float/精确摘要/WOPT/nodes/checks/变量数/版本；fixed嵌入127重数、自由floor1.8无incumbent、首解2.565s、三接续和源码审计SHA/四m4对偶scope全字段。',
  '逐7行核组合公式与有序树数；固定嵌入与另一primary逐字段同。前三cap=m/M=m、后4cap1/M1，七摘要无完整策略/客户/对偶不冒本轮重新认证；一般预算桥后13例已否。',
  '新计算对象完整保数字/版本/状态/目标语义及真实固定/free对照。未跑7历史扫描/自由基线；固定optional main仅1次单记，既有默认与四对偶复用分离。'),
 ('integrated',[NEW],
  '1657B完整127重数表/7正型11客户、m5p7q5000000、42345/41888/77064、历史status0/8.096889s/float1.8/2801/16806/W5OPT9/9/5全读，双冻结SHAdc2c45…核。',
  '此与摘要fixed字段全同不重复计run。原large_baseline实际输入为硬编码无JSON；7代码闭包61520B；所有历史选0直接完整SPE证明适用严格SET目录；不指认未保存MILP动作。',
  '新对象给自足完整离轨IC与OPT9解析证明。唯一原optional入口一次wall8.313892858s/内部0.945768153s/exit0，1658B仅seconds异；另标准库explicit policy一次19607含自身比较/0solver，原动作表未保存边界明确。')
]
receipts=[]
for src,(disp,targets,read,compare,decision) in zip(primary,notes):
    receipts.append({'id':src['id'],'full_file_reviewed':True,'related_material_checked':True,
                     'unique_content_accounted_for':True,'read_note':read,'comparison_note':compare,
                     'decision_note':decision,'disposition':disp,'targets':targets})
dump(W/'semantic-receipts.json',receipts)
dump(W/'relations-review.json',{'status':'reviewed; no phase-three graph fabricated','new_object':NEW,
 'relations':[
 {'other':EQ,'kind':'realization/interface','reason':'same exact DAG existence model and bounded formulation; numeric fixed/free runs do not prove new global bound'},
 {'other':OLD,'kind':'complement and duplicate coverage','reason':'three complete m4 inputs already fully absorbed with exact replay; new page preserves full exploration metadata and previously unexecuted optional baseline'},
 {'other':WEAK,'kind':'scope correction','reason':'R=W-G identifies old new-budget bridge with all-m exact tax already refuted; fixed m4 results remain correct'},
 {'other':MARKOV,'kind':'domain distinction','reason':'baseline happens to have count-uniform policy but general DAG does not require false count purification'},
 {'other':'archives/customer-attraction/state/定理/五人半覆盖--定理.md','kind':'finite benchmark vs universal theorem','reason':'11-customer 9/5 point is one legal five-player input; independent five theorem supplies general half, not this scan'}],
 'not_claimed':['half counterexample','six-player proof','new exact joint-MIP upper bound','phase-three hyperedge publication','global novelty or external review']})

ids=['f60cb51c0f182ef1c1cc','adf8034d7d01f0949d87','104bf29b448557ae655f','6543d29d729f96c9276b','1c15c43ca580c43498d7']
inv={x['id']:x for x in map(json.loads,(R/'cleanup/inventory.jsonl').read_text().splitlines()) if x['id'] in ids}
nexts=[]
for i in ids:
    result=subprocess.run(['git','show',f'HEAD:cleanup/progress/{i}.json'],cwd=R,
                          env={**os.environ,'GIT_NO_LAZY_FETCH':'1'},capture_output=True)
    state=json.loads(result.stdout) if result.returncode==0 else None
    local=R/'cleanup/progress'/f'{i}.json'
    available=state is None and not local.exists()
    nexts.append({**{k:inv[i][k] for k in ['id','path','size','sha256']},
                  'available_at_local_HEAD_check':available,'head_progress':state,
                  'local_progress_exists':local.exists(),
                  'why_next':'same strategy_duality group: three discovery probe contracts require formal read and any necessary real main; independent audit/report already full-read/run as comparison only and not primary done',
                  'proposed_stage':'r3-count-markov-probes-primary'})
dump(W/'next-candidates.json',{'scope':'read-only metadata check; no claim or primary read before actual pushed receipt',
 'candidates':nexts,'note':'owner may change after observation; root serial actual claim governs. Existing std audit run may be honestly reused without another identical run.'})

execution=json.loads((E/'replay-large-baseline/execution.json').read_text())
dump(W/'runtime-summary.json',{'environment':{'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__},
 'new_original_entry_runs':1,'new_original_branch':'audit_outcome_dag.py --large-baseline',
 'new_milp_calls':1,'new_exact_fixed_cone_lp_calls':0,'new_independent_review_runs':1,
 'new_independent_review_solver_calls':0,'new_independent_review_timed':False,
 'not_run':['default audit main','generic DAG main','seven historical scans','free-multiplicity floor baseline','four m4 dual LP or replay'],
 'history_counts':{'m5p7_full_ordered_decision_nodes':2801,'including_self_comparisons':19607,
                    'excluding_self_comparisons':16806,'m5p7_threshold_count_states':330},
 'new_original_report_bytes':execution['new_report_bytes'],'new_original_report_sha256':execution['new_report_sha256'],
 'byte_identical_to_frozen':False,'only_JSON_difference':'/milp/seconds','original_selected_strategy_persisted':False,
 'independent_policy':'all ordered histories select big topic 0; not asserted identical to original selected witness'})
dump(W/'self-review.json',{'status':'pass','mathematics':[
 'Full legal ordered-history domain kept; all-big payoff5/(g+r)>=1 vs singleton<=1 at every h proves explicit SPE.',
 'OPT9 proven by big+4 singleton versus at most5 without big; 11 distinct unit customers and seven distinct coverages.',
 '2801 histories,19607 incl self,16806 nonself,330 count-threshold states kept separate; no JSON row count treated as full policy.',
 'Seven exploratory records retain float and exact-summary distinctions; missing complete strategy/clones/duals not recertified.',
 'Fixed and free multiplicity models differ by floor row; known feasible fixed point rules out impossibility inference from timeout.',
 'Saved four fixed-cone duals already exactly replayed/reconstructed; no duplicate new LP or unsupported global bound.',
 'Static query not actual SPE payoff; R=W-G gives already refuted all-m exact-tax bridge, exact-six and half remain separate.',
 'Original raw baseline not a full action-table certificate; explicit independent strategy and new original branch clearly distinct.',
 'Five-player general theorem exists independently,9/5 benchmark not claimed sharp or universal; six goal unchanged.'
 ],'source_and_provenance':[
 'Actual BL capture pushed/Boss4/synced683eb21…; actual five owners in HEAD and source SHA checked.',
 'All five clean show exports after formal claim, full read and both frozen bytes verified; no dependency gets extra done.',
 'Seven same-SHA code files verified both commits; large branch reads zero JSON input files and uses source-built multiplicities.',
 'One original optional run/one own untimed exact review; prior default runs and original historical timing not overwritten.',
 'Reused evidence currently in repo byte-identical to previous mature stage; no overwrite of old shared body by worker.',
 'No Git/claim/done/sync/checkpoint/auth mutation or subagent. All writes external stage. No credentials or new network retry.'
 ],'receipts':{'duplicate':3,'integrated':2,'primary_total':5},
 'remaining_gaps':['Seven historical scratch reports lack complete original actions/clones/duals in summary; retained as historical fields only.',
 'Original baseline branch does not persist selected action table; exact runtime assertion and explicit analytic policy are separate evidence.',
 'No universal half or joint-MIP optimality/infeasibility certified by these finite runs.']})

(E/'README.md').write_text('''# 七主题固定基线与终局探索证据

主正文：[七主题固定输入基线与终局搜索版本](../../../state/计算/七主题固定输入基线与终局搜索版本--计算.md)。

本包仅五个正式primary：7509B完整m4表、424B实例、4512B四对偶、12713B探索摘要、1657B固定基线。primary-manifest保全部clean show原件、inventory SHA及两冻结提交的字节核验；source-manifest将五主源与七运行代码严格分开。

前三源已有[固定锥完整正文](../../../state/计算/终局见证DAG的原审计与固定锥预算复核--计算.md)和same-SHA实际精确证据，receipt为duplicate。reused-evidence只引用已有default原run和独立82行/15坐标核对，不称本轮再次执行。

本轮原audit --large-baseline唯一一次，新隔离replay-tree七原码61520B保持路径，零JSON输入。分支以源代码构造127重数；replay-large-baseline保存stdout、stderr、execution和1658B新report。wall8.313892858001054s/内部0.9457681529966067s，exit0，W5/OPT9，2801节点/16806非自身；新旧仅seconds异。原分支不保存所选动作表。

independent_baseline_review.py是新标准库独立定点核对：明确所有历史action0，不导原helper/规范包/优化器，一次未计时、19607含自身比较，报告independent-baseline-review.json；不是原MILP策略动作身份认证。另核7摘要组合维数/节点数、fixed嵌入与独立JSON相同、原新只seconds异，没有重新认证七个缺动作/重数的历史候选。

七项历史搜索、free floor、generic main、default原main及四m4对偶本轮0次；上批default60MILP/2LP与本轮optional1MILP分开。旧cap=m/M=m、current1/1、数值状态/精确证据/一般量词均保留。R=W−G的全人数新预算桥已由13例否定，六人half未由此判。

逐源receipt、数学自查、关系说明、运行摘要和下一候选位于cleanup/workspaces/Boss4/r3-true-spe-outcome-evidence-primary；copy-files是精确运输清单，根代理串行复制/推送/登记。本worker未改共享旧页、未写Git、未claim/done或再开代理。
''')
(W/'HANDOFF.md').write_text('''# BL五源交付

唯一claim capture boss4-r3-credible-next5bl-claim.json，pushed683eb21f79b93815427d13c748ffd247eab48901/Boss4/synced，实际五owner和SHA保存。五receipt：c0d7c7c0952b288ed370、1aa60f6582e1ade29db4、dbbb96f5098589f83146 duplicate；c782c5bbd16b7460dbd7、a7e1d9e53642641b7214 integrated。

新增正式正文一个：archives/customer-attraction/state/计算/七主题固定输入基线与终局搜索版本--计算.md。前三源target上一批终局见证固定锥资源/既有分数负载反例；上一65文件和净化旧页纠正已在本clone中见到并逐字节核对，不在本包复制旧正文，不重done旧五源。

原optional入口一次wall8.313892858001054s/内部0.9457681529966067s/exit0，1658B新SHA411978b6460639eb8a2a4dbfc36cda86baa51832c682bea0df0213cee0511bd2，仅seconds异。原分支1MILP/0LP/零JSON输入；七代码文件61520B。全历史19607含自身/16806非自身与2801节点分开；原输出未存动作表。标准库自己的明确all-big策略检查一次/0solver/未计时，不混成原策略。

七历史探索只是原摘要属性，没有缺失完整见证的重新认证；保全部7 float/value/WOPT/节点/维数/版本。free floor无incumbent只诊断联合启动。全人数精确预算桥已否；四人一个固定锥通过、五人别证、六人开放保域。

请按copy-files.json精确文件清单串行复制，先发布正文/证据，后仅五primary receipt登记。数学自查/所有本地链接验证/12份原件SHA与7份运行代码不变检查见validation.json；不把机器字段通过称数学证明。

下一实际metadata候选在next-candidates.json：count_markov_probe、fresh_markov_probe、markov_generic_probe、markov_obstruction_audit与report五源，观测时未owner/未done；后二已作比较有完整原run可复用。待新的真pushed capture再正式处理，不提前primary/receipt。Git/claim/done由root串行。
''')
print(json.dumps({'metadata_written':True,'next_available':[x['id'] for x in nexts if x['available_at_local_HEAD_check']],
                  'new_formal_bytes':(S/NEW).stat().st_size},ensure_ascii=False))
