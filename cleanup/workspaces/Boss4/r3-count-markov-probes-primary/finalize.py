from pathlib import Path
import hashlib,json,os,subprocess

S=Path(__file__).resolve().parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=S/'archives/customer-attraction/tools/evidence/count-markov-probes-primary'
W=S/'cleanup/workspaces/Boss4/r3-count-markov-probes-primary'
NEW='archives/customer-attraction/state/计算/计数统一续局的有限枚举与辅助终局分离--计算.md'
COUNTER='archives/customer-attraction/state/反例/完整历史与计数统一策略的严格分离--反例.md'
QUESTION='archives/customer-attraction/state/问题/完整历史计数策略净化--问题.md'
EQ='archives/customer-attraction/state/等价/终局见证DAG的完整历史可实现性--等价.md'
PE=Path('archives/customer-attraction/tools/evidence/true-spe-outcome-witness-primary')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def fp(p):return {'path':str(p.relative_to(R)),'size':p.stat().st_size,'sha256':sha(p)}

sources=json.loads((E/'primary-manifest.json').read_text())['sources']
dump(E/'source-manifest.json',{'primary_count':5,'primary_bytes':sum(x['size'] for x in sources),
 'runtime_external_code_dependencies':0,'runtime_external_input_files':0,
 'runtime_executed_primary_code_ids':[x['id'] for x in sources[:3]],
 'runtime_scope':'all three newly executed main programs import Python standard library only and generate real inputs from recorded seeds/defaults; original independent audit/report are reused, not run again',
 'sources':sources})
reused=[]
for p,why in [(PE/'original'/sources[3]['path'],'same original independent standard-library audit'),
              (PE/'replay-markov/execution.json','actual prior one original std audit invocation,0.6825053691864014s/exit0'),
              (PE/'replay-markov/markov_obstruction_report.json','prior byte-identical full198865B report,648/130776 exact exhaustion'),
              (PE/'independent-input-review.json','prior additional exact input/menus/triple review; not another full exhaustion')]:
    q=R/p;assert q.is_file()
    reused.append({**fp(q),'why_reused':why,'new_executions_this_batch':0})
assert (R/PE/'original'/sources[3]['path']).read_bytes()==(S/sources[3]['saved_path']).read_bytes()
assert (R/PE/'replay-markov/markov_obstruction_report.json').read_bytes()==(S/sources[4]['saved_path']).read_bytes()
dump(E/'reused-evidence.json',{'primary_audit_and_report_same_SHA':True,'old_original_audit_executions':1,
 'new_original_audit_executions':0,'previous_report_byte_identical':True,
 'scope':'all existing original-model witness, legal types, fresh boundary and exhaustive count-policy separation; no new half theorem or novelty claim',
 'references':reused})

related={
 COUNTER:'完整正文全文重读；31客户、调和编译、全历史31表/155IC、648/130776、7对6和22428<22429已充分，5主题合法例与新6主题辅助025不同。',
 QUESTION:'root已按严格CAG例修正refuted；旧16000/499与固定微扰历史保留，不把本三main次数塞进旧统计。',
 'archives/customer-attraction/state/定理/子集调和势的Möbius反演--定理.md':'全文读双反演/唯一性/重复计数扩张/有符号域/位长；足够一般定理已存在，不重造。',
 'archives/customer-attraction/state/定理/无重复辅助博弈的完整历史编译--定理.md':'全文核p>=n、清分母/K4M+1、全部重复离轨历史严格fresh、子树扩展和不保福利；本6主题表未另编客户。',
 'archives/customer-attraction/state/障碍/匿名计数势的客户相容性--障碍.md':'全文读轴关系/固定人数关系/非负反演/单调次模不足，generic table任意匿名收益不是客户模型。',
 'archives/customer-attraction/state/算法/可信续局菜单与完整策略重构--算法.md':'已读同SHA数学复用；max-min menus permitting independent ordered children, no count-uniform action assumption.',
 EQ:'全文既读归纳及M1；同k可随目标c不同行动，保留被否计数净化之外的正确DAG存在性。',
 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md':'此前完整实读同SHA；严格目录SET/完整ordered histories/单位客户vs标签扩展均保，不能merge labels。',
 'archives/customer-attraction/state/定理/五人半覆盖--定理.md':'此前完整实读同SHA；5人独立证明与本有限扫描及6人开放区分。'
}
dump(E/'related-material.json',{'search_scope':'repo state count-Markov/计数策略/净化/fresh/调和势/Möbius/客户相容性 and exact original filenames/SHA in published evidence',
 'related_objects':[{**fp(R/p),'semantic_comparison':note,'primary_in_this_batch':False} for p,note in related.items()],
 'provenance_note':'metadata-only inventory hits were not counted as whole-file mathematical review or primary work',
 'existing_generic_probe_run_found':False,'decision':'run all three distinct original probe main entries once; reuse the fully published independent old audit/report'})

runtime=[]
for name in ['count','fresh','generic']:
    d=json.loads((E/f'replay-{name}/execution.json').read_text());assert d['returncode']==0 and not d['timed_out']
    runtime.append({'program':name,'execution_path':str((E/f'replay-{name}/execution.json').relative_to(S)),
                    **{k:d[k] for k in ['wall_seconds','source_sha256','stdout_bytes','stderr_bytes','original_entry_runs_this_batch','solver_calls']}})
fresh=json.loads((E/'independent-fresh-review.json').read_text())
dump(W/'runtime-summary.json',{'new_original_main_runs':3,'new_original_runs_by_program':runtime,
 'new_original_audit_runs':0,'old_original_audit_runs_reused':1,'solver_calls_total':0,
 'new_independent_review_runs':1,'new_independent_review_timed':False,
 'count_results':{'exhaustive_binary_inputs':128,'binary_last_maps':2244,'random_inputs':10000,
                  'cumulative_last_maps_after_random':15342,'random_last_maps_increment':13098,
                  'distinct_random_inputs_not_certified':True},
 'generic_results':json.loads((E/'replay-generic/stdout.txt').read_text()),
 'fresh_results':{'trial_zero_based':205,'attempted_trials_including_current':206,
                  'prior_skipped_count_not_emitted':True,'current_peak_assignment_rows':32,
                  'full_roots':fresh['full_root_sets'],'count_roots':fresh['count_uniform_root_sets'],
                  'complete_fresh_nodes':37,'including_self_comparisons':156,'excluding_self_comparisons':119,
                  'last_maps':32,'second_maps':144,'CAG_customers_compiled':False,
                  'strict_worst_auxiliary_total_separation':False,'full_and_count_min_auxiliary_total':6},
 'frozen_stdout_for_three_probes_provided':False})

notes=[
 ('integrated',[NEW],
  '2154B正式claim后clean show全文核两冻结SHA：P3 payoff Fraction/六无序多重集末回复菜单/所有mp、第二人BR与根minmax、full各有序孩子独立局部映射、两循环128+10000/seed1001/累计totalmaps/break和未使用details全读。',
  '与正确完整R递归、一般全层赋值、旧16000/499实验和合法5主题严格例比较；full缓存集合不等于统一动作、三人第二层无额外合流。未将有限阴性同一般净化真值混淆。',
  '新统一有限枚举资源完整解释必要充分门槛，原main1次6.504905659s/exit0；128binary同2244maps、10000random同累计15342/增量13098。std独立无外部依赖，真实原stdout保留，无旧冻结输出可冒同。'),
 ('integrated',[NEW],
  '1784B正式claim后全文核SHA：无重复subset states/φ边际，R菜单、全局赋值行、去重与两cap退出、peak语义；m3p6/35φ值/seed786/1000上限/skip和first mismatch控制流全读。',
  '辅助有符号收益/动作fresh限制不同原客户模型；旧5主题合法例已更强，不把本新6主题例继承严格最差福利。Möbius/正偏置编译已有全文，当前未额外造客户。',
  '原main1次0.263336127s/exit0，trial205/onlyfull025/peak32/35φ原stdout完整。新独立std1次0solver穷尽32last/144second及37节点156IC，完整roots4/3；本辅助两域最差和都6，不half。'),
 ('integrated',[NEW],
  '2305B正式claim后全文核SHA：comps/LCM整数U与可选table、完整R递归/状态同时赋值/动作到终局去重/两cap/peak、args默认m4p3trial500、seed1001/skips/equality早停全读。',
  '全层同时赋值保计数一致，终局行去重非策略数量；任意table不保证调和客户相容。全仓未发现此原码已充分同SHA原main可复用，不能照父笼统“后三已跑”虚构。',
  '新资源自足算法正确性/有限边界；必要原默认main唯一1次0.200219959s/exit0/equal500 skipped0 peak12内部0.160888910s，0外部输入/0solver。无重复额外参数扫描或一般净化结论。'),
 ('duplicate',[COUNTER],
  '6642B正式claim后重新完整读两冻结SHA：compile_exact双变换/全32势值/正K、full_R与fresh证书、25末前缀140比较/五second界、31完整政策/155IC、648全映射130776second、全报告main均读。',
  '既有严格分离正文保全部法律客户/明确31表/全部菜单与完整proof，已发表一次std原run0.682505369s/报告全字节同；本批raw码同SHA。与新6主题仅辅助025的域和最差和差别明确。',
  'duplicate：已有独有数学充分且精确run充分，不重复同一原audit。原run执行事件/报告/代码与目标SHA逐一引用，new_original_audit_runs0；不是新half反例或新颖性承诺。'),
 ('duplicate',[COUNTER],
  '198865B正式claim后全JSON读：32φ/31signed/31legal/完整31policy、root及收益/福利/OPT、7对6集合/22428对22429、648条last映射每10键和roots原顺序无损紧凑全文、130776及155/双6404/3全字段。',
  '正式报告与现成已发表replay198865B逐字节同bc359e…；现有自足反例含全客户、全完整表与所有终局福利及合法完整域必要排除证明。旧问题页已refuted，不恢复OPEN。',
  'duplicate，仅本5primary正式receipt；现成完整原审计与报告复用new run0，不复制重造同一反例。全部648原记录原样保留，old comparison当时未done仍保持历史身份。')
]
receipts=[]
for x,(disp,targets,read,compare,decision) in zip(sources,notes):
    receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,
       'unique_content_accounted_for':True,'read_note':read,'comparison_note':compare,
       'decision_note':decision,'disposition':disp,'targets':targets})
dump(W/'semantic-receipts.json',receipts)
dump(W/'relations-review.json',{'status':'semantically reviewed; phase-three graph not fabricated','new_object':NEW,
 'relations':[
 {'target':COUNTER,'type':'distinct finite precursor and stronger original-model result','reason':'six-label auxiliary sample only separates root sets; legal five-label compiled example additionally separates worst coverage and remains half-positive'},
 {'target':QUESTION,'type':'status and historical scope correction','reason':'finite scans retain original sample scope; general purification already refuted and old experiments not retrospectively relabeled'},
 {'target':EQ,'type':'representation distinction','reason':'outcome-set memoization/full target DAG preserve independent ordered histories, unlike one global action per count'},
 {'target':'archives/customer-attraction/state/定理/子集调和势的Möbius反演--定理.md','type':'potential realization interface','reason':'arbitrary Boolean potential has signed inverse but repeat values determined; no new proof duplicate'},
 {'target':'archives/customer-attraction/state/定理/无重复辅助博弈的完整历史编译--定理.md','type':'conditional migration boundary','reason':'legal full-history migration requires positive bias and filling all repeat subtrees; this new6 table not compiled and welfare not preserved'}],
 'not_inferred':['half counterexample','universal count purification from finite negatives','old original discovery novelty','cap None as empty outcome set','raw unordered states as complete ordered policy']})

nextids=['e7f59c00e908624ee87a','4c81a8c32a9035cefbcc','4e109f497916963593c7','e54f25554db04d3a8f06','82abacd2460c6ebe3014']
inv={x['id']:x for x in map(json.loads,(R/'cleanup/inventory.jsonl').read_text().splitlines()) if x['id'] in nextids}
candidates=[]
for i in nextids:
    q=subprocess.run(['git','show',f'HEAD:cleanup/progress/{i}.json'],cwd=R,env={**os.environ,'GIT_NO_LAZY_FETCH':'1'},capture_output=True)
    state=json.loads(q.stdout) if q.returncode==0 else None;local=(R/'cleanup/progress'/f'{i}.json').exists()
    candidates.append({**{k:inv[i][k] for k in ['id','path','size','sha256']},
      'head_progress':state,'local_progress_exists':local,'available_at_check':state is None and not local,
      'reason':'coherent independent welfare-gap/policy-cone code plus three actual saved policies; exact input/dependencies and any historical counts must be read before selecting runs',
      'proposed_stage':'r3-markov-welfare-and-policy-cones-primary'})
dump(W/'next-candidates.json',{'metadata_only':True,'not_claimed_by_this_worker':True,'candidates':candidates,
 'note':'Availability is observed at local HEAD; future actual root claim/owner governs. No primary content read before claim.'})
dump(W/'self-review.json',{'status':'pass','mathematical_review':[
 'Complete ordered-history menus use max min per action and independent child subtrees; count-uniform uses whole-layer simultaneous assignments.',
 'Outcome-row dedup preserves earlier payoffs/existence, does not count full strategies; peak and cap estimate have explicit meanings.',
 'Special3player last maps unify unordered multiset pairs, full version may break reversed-history ties independently; exact Fraction comparisons preserve ties.',
 'Generic integer scaling LCM is exact because only occupied actions queried; arbitrary table path is not original customer compatibility.',
 'Fresh sample is auxiliary no-repeat only; full 37-node legal policy checked156incl119nonself, not unrestricted CAG policy.',
 'All32 last maps and144 second maps exact: roots4 vs3,only025. New6 auxiliary min sum both6, no false worst-welfare separation.',
 'Strong original5 legal counter remains old same object with648/130776 and22428<22429,not half; all31 types strictly positive hence distinct coverages.',
 'Source count cumulative15342 includes2244,random increment13098; current fresh trial205means206attempts,prior skip count unreported.',
 'Finite negatives do not resurrect refuted purification. Five theorem independent,six half not solved; no external review or novelty claims.'
 ],'provenance_review':[
 'Actual pushed18cd3b…/Boss4/synced and all5 HEAD owner/source SHA verified before stage/primary reads.',
 'Five full formal clean show exports,each full read plus both frozen byte matches; dependencies/comparisons not additional primary done.',
 'Three original main entries each1 newrun,std closure and builtin real seeds/defaults preserved; audit/report sameSHA adequate run reused0new.',
 'One own independent auxiliary review,untimed/0solver; raw new outputs preserved and no absent frozen stdout identity invented.',
 'Related math objects read/comparison fingerprinted; old generic original execution not found,therefore actual newrun rather than assumed reuse.',
 'Metadata-only whole-repo inventory hit was not counted as a complete mathematical source read or added primary.',
 'No shared Git/claim/done/sync/checkpoint/auth changes,no spawn; writes only this external stage.'
 ],'receipt_counts':{'integrated':3,'duplicate':2,'total':5},
 'remaining_limits':['Earlier skipped count before fresh205 not printed by original mismatch output; not inferred.',
 'No explicit unrestricted CAG policy for new6 auxiliary sample or claimed preservation of welfare through compilation.',
 'No universal finite-enumeration performance/upper bound/no-go conclusion.']})

(E/'README.md').write_text('''# 计数策略探针证据

[新自足资源](../../../state/计算/计数统一续局的有限枚举与辅助终局分离--计算.md)说明三种枚举、精确量词/算术、cap语义、全部生成输入和辅助发现。五primary211750B、双冻结原件见primary-manifest/source-manifest；运行没有额外代码或数据输入依赖。

replay-count/fresh/generic分别保存原main唯一1次的started/execution/stdout/stderr及独立树原字节源码。count128binary与10000random都同，末映射累计2244→15342（增量13098）；generic默认m4p3/500全同/skipped0/peak12；fresh只尝试至0起205号，输出完整35φ/onlyfull025/peak32。各为Python标准库，无优化器。没有冻结stdout，不能称历史输出复现。

independent_fresh_review.py另外一次0solver/未计时精确核上述6主题无重复辅助表：37节点/156含自身比较、32末映射/144第二映射，完整根025/035/125/345而计数根035/125/345；JSON保所有末映射结果和完整合法fresh动作表。本例两域最差辅助和都6，不是最差覆盖分离，也没有编译客户。

[原五主题严格反例](../../../state/反例/完整历史与计数统一策略的严格分离--反例.md)已完整保31客户/31动作/648及130776和22428<22429，原audit/report本批正式全文读/SHA核后duplicate。reused-evidence引用已发表同SHA原std审计一次0.682505369s/198865B全字节相同的旧记录，新audit运行0次。旧Markov报告所有648原记录保在original；复用不升级为新发现/half。

逐源receipt、自查、关系、实际运行摘要、下一五metadata与HANDOFF位于cleanup/workspaces/Boss4/r3-count-markov-probes-primary；copy-files.json为精确复制白名单，由根代理串行发布/登记。本worker无共享Git写入/认领/勾选或认证尝试。
''')
(W/'HANDOFF.md').write_text('''# BR五源完整交付

正式capture boss4-r3-credible-next5br-claim.json，pushed18cd3b896520ab0ecfbaf48b8fc233129fb72981/Boss4/synced；五HEAD owner/SHA与双冻结原件均核。

唯一新正文 archives/customer-attraction/state/计算/计数统一续局的有限枚举与辅助终局分离--计算.md；三探针integrated，audit/report duplicate到既有完整原模型严格分离。原件五211750B，不额外done比较/依赖，不重造已有完整定理/反例。

原三个main各1次，exit0/stderr空，标准库/零外部输入/0solver：count6.504905659s，128binary+10000random同，累计maps2244/15342随机增量13098；fresh0.263336127s，trial205辅助only025/35φ/peak32（不宣称1000全跑或先前skip0）；generic默认500同/skipped0/peak12，0.200219959s。后三源中generic此前充分运行未找到，真实新跑1次；只有audit/report有充分同SHA旧run复用，未据口头概括虚构run。

新独立std辅助核1次/未计时/0solver：根4vs3，32last/144second、37nodes/156incl119nonself/ties53/min0；完整37动作/全部32映射入证据。6主题辅助例只分离根集合，两域min辅助和同6；5主题旧合法例才有最差覆盖严格分离，原audit新0次。不能当half反例。

自查与validation核原件、三运行树代码、旧证据字节、完整本地链接、receipt目标和37动作/35φ/32映射结构。按copy-files精确白名单串行复制，先正文/证据checkpoint，后只本五receipt done。

下一metadata实际available组：e7f59c00e908624ee87a/4c81a8c32a9035cefbcc/4e109f497916963593c7/e54f25554db04d3a8f06/82abacd2460c6ebe3014，两个独立程序加m5k7/m6k8/m8k8保存policy。待root实际claim再正式全文处理，当前未预读primary。
''')
print(json.dumps({'written':True,'formal_bytes':(S/NEW).stat().st_size,'primary_bytes':sum(x['size'] for x in sources),
                  'available_next':[x['id'] for x in candidates if x['available_at_check']]},ensure_ascii=False))
